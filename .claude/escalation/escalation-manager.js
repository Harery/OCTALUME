#!/usr/bin/env node

/**
 * Escalation Manager
 * Handles escalation paths when phases fail or go/no-go decisions are NO-GO
 *
 * This is the CRITICAL component that prevents:
 * - CB-005: No escalation path for NO-GO decisions
 * - CB-002: Go/no-go decisions not enforced
 * - RF-006: Go/No-Go failure stalls project
 */

import { readFileSync, writeFileSync, existsSync } from 'fs';
import { join } from 'path';

// Escalation levels
const ESCALATION_LEVELS = {
  L1: 'Project Manager',
  L2: 'Product Owner',
  L3: 'Executive Sponsor',
  L4: 'CTO/CIO',
  L5: 'Executive Committee'
};

// Escalation reasons
const ESCALATION_REASONS = {
  PHASE_GATE_FAILED: 'phase_gate_failed',
  GO_NO_GO_NO_GO: 'go_no_go_no_go',
  APPROVAL_TIMEOUT: 'approval_timeout',
  BLOCKER_UNRESOLVED: 'blocker_unresolved',
  RESOURCE_UNAVAILABLE: 'resource_unavailable',
  SECURITY_VIOLATION: 'security_violation',
  COMPLIANCE_FAILURE: 'compliance_failure'
};

// Escalation paths by phase
const ESCALATION_PATHS = {
  phase_01_vision_strategy: {
    primary_approver: 'Executive Sponsor',
    escalation_path: ['Product Owner', 'Executive Sponsor', 'CEO'],
    timeout_hours: 72,
    auto_escalate: true
  },
  phase_02_requirements_scope: {
    primary_approver: 'Product Owner',
    escalation_path: ['Product Owner', 'Executive Sponsor', 'CTO'],
    timeout_hours: 48,
    auto_escalate: true
  },
  phase_03_architecture_design: {
    primary_approver: 'CTA',
    escalation_path: ['CTA', 'CTO', 'Executive Sponsor'],
    timeout_hours: 72,
    auto_escalate: true
  },
  phase_04_development_planning: {
    primary_approver: 'Tech Lead',
    escalation_path: ['Tech Lead', 'Project Manager', 'Product Owner'],
    timeout_hours: 48,
    auto_escalate: true
  },
  phase_05_development_execution: {
    primary_approver: 'QA Lead',
    escalation_path: ['QA Lead', 'Tech Lead', 'Product Owner'],
    timeout_hours: 24,
    auto_escalate: true
  },
  phase_06_quality_security: {
    primary_approver: 'Product Owner',
    escalation_path: ['Product Owner', 'Executive Sponsor', 'CTO'],
    timeout_hours: 48,
    auto_escalate: true
  },
  phase_07_deployment_release: {
    primary_approver: 'Executive',
    escalation_path: ['DevOps Lead', 'CTO', 'CEO'],
    timeout_hours: 24,
    auto_escalate: true
  },
  phase_08_operations_maintenance: {
    primary_approver: 'SRE Lead',
    escalation_path: ['SRE Lead', 'DevOps Lead', 'CTO'],
    timeout_hours: 4,
    auto_escalate: true
  }
};

/**
 * Create a new escalation
 */
function createEscalation(projectStatePath, escalationData) {
  const projectState = JSON.parse(readFileSync(projectStatePath, 'utf-8'));

  const escalation = {
    id: `ESC-${Date.now()}`,
    created_at: new Date().toISOString(),
    status: 'open', // open, acknowledged, escalated, resolved, rejected
    reason: escalationData.reason,
    phase: escalationData.phase,
    original_decision: escalationData.decision, // 'go' or 'no-go'
    requester: escalationData.requester,
    description: escalationData.description,
    impact: escalationData.impact || 'undefined',
    proposed_resolution: escalationData.proposed_resolution || null,
    escalation_path: [],
    current_level: 0,
    timeline: [],
    artifacts: []
  };

  // Determine escalation path
  const phasePath = ESCALATION_PATHS[escalationData.phase];
  if (phasePath) {
    escalation.escalation_path = phasePath.escalation_path;
    escalation.primary_approver = phasePath.primary_approver;
    escalation.timeout_hours = phasePath.timeout_hours;
    escalation.auto_escalate = phasePath.auto_escalate;
  }

  // Add to project state
  if (!projectState.escalations) {
    projectState.escalations = [];
  }
  projectState.escalations.push(escalation);

  // Set current phase status to blocked
  if (projectState.current_phase === escalationData.phase) {
    projectState.phase_status = 'blocked';
    projectState.blocked_reason = escalation.id;
  }

  writeFileSync(projectStatePath, JSON.stringify(projectState, null, 2));

  return escalation;
}

/**
 * Acknowledge an escalation
 */
function acknowledgeEscalation(projectStatePath, escalationId, acknowledgedBy, comments = null) {
  const projectState = JSON.parse(readFileSync(projectStatePath, 'utf-8'));
  const escalation = projectState.escalations?.find(e => e.id === escalationId);

  if (!escalation) {
    return { success: false, error: 'Escalation not found' };
  }

  escalation.status = 'acknowledged';
  escalation.timeline.push({
    action: 'acknowledged',
    by: acknowledgedBy,
    at: new Date().toISOString(),
    comments: comments
  });

  writeFileSync(projectStatePath, JSON.stringify(projectState, null, 2));

  return { success: true, escalation };
}

/**
 * Escalate to next level
 */
function escalateToNextLevel(projectStatePath, escalationId, escalatedBy, comments = null) {
  const projectState = JSON.parse(readFileSync(projectStatePath, 'utf-8'));
  const escalation = projectState.escalations?.find(e => e.id === escalationId);

  if (!escalation) {
    return { success: false, error: 'Escalation not found' };
  }

  if (escalation.current_level >= escalation.escalation_path.length - 1) {
    return { success: false, error: 'Already at maximum escalation level' };
  }

  escalation.current_level++;
  escalation.status = 'escalated';
  escalation.timeline.push({
    action: 'escalated',
    from: escalation.escalation_path[escalation.current_level - 1],
    to: escalation.escalation_path[escalation.current_level],
    by: escalatedBy,
    at: new Date().toISOString(),
    comments: comments
  });

  writeFileSync(projectStatePath, JSON.stringify(projectState, null, 2));

  return { success: true, escalation };
}

/**
 * Resolve an escalation
 */
function resolveEscalation(projectStatePath, escalationId, resolvedBy, resolution, newDecision = null) {
  const projectState = JSON.parse(readFileSync(projectStatePath, 'utf-8'));
  const escalation = projectState.escalations?.find(e => e.id === escalationId);

  if (!escalation) {
    return { success: false, error: 'Escalation not found' };
  }

  escalation.status = 'resolved';
  escalation.resolved_at = new Date().toISOString();
  escalation.resolved_by = resolvedBy;
  escalation.resolution = resolution;

  if (newDecision) {
    escalation.new_decision = newDecision;
  }

  escalation.timeline.push({
    action: 'resolved',
    by: resolvedBy,
    at: new Date().toISOString(),
    resolution: resolution,
    new_decision: newDecision
  });

  // If resolution results in GO, unblock the phase
  if (newDecision === 'go' && projectState.phase_status === 'blocked') {
    projectState.phase_status = 'in_progress';
    projectState.blocked_reason = null;
  }

  writeFileSync(projectStatePath, JSON.stringify(projectState, null, 2));

  return { success: true, escalation };
}

/**
 * Reject an escalation (deny escalation request)
 */
function rejectEscalation(projectStatePath, escalationId, rejectedBy, reason) {
  const projectState = JSON.parse(readFileSync(projectStatePath, 'utf-8'));
  const escalation = projectState.escalations?.find(e => e.id === escalationId);

  if (!escalation) {
    return { success: false, error: 'Escalation not found' };
  }

  escalation.status = 'rejected';
  escalation.rejected_at = new Date().toISOString();
  escalation.rejected_by = rejectedBy;
  escalation.rejection_reason = reason;

  escalation.timeline.push({
    action: 'rejected',
    by: rejectedBy,
    at: new Date().toISOString(),
    reason: reason
  });

  writeFileSync(projectStatePath, JSON.stringify(projectState, null, 2));

  return { success: true, escalation };
}

/**
 * Check for timeout escalations
 */
function checkTimeoutEscalations(projectStatePath) {
  const projectState = JSON.parse(readFileSync(projectStatePath, 'utf-8'));
  const now = Date.now();
  const escalationsToAutoEscalate = [];

  if (!projectState.escalations) {
    return { escalations: [] };
  }

  for (const escalation of projectState.escalations) {
    if (escalation.status !== 'open' && escalation.status !== 'acknowledged') {
      continue;
    }

    if (!escalation.auto_escalate || !escalation.timeout_hours) {
      continue;
    }

    const lastAction = escalation.timeline[escalation.timeline.length - 1];
    if (!lastAction) {
      continue;
    }

    const lastActionTime = new Date(lastAction.at).getTime();
    const timeoutMs = escalation.timeout_hours * 60 * 60 * 1000;

    if (now - lastActionTime > timeoutMs) {
      if (escalation.current_level < escalation.escalation_path.length - 1) {
        escalationsToAutoEscalate.push({
          escalation_id: escalation.id,
          phase: escalation.phase,
          current_level: escalation.current_level,
          next_level: escalation.current_level + 1,
          overdue_hours: Math.floor((now - lastActionTime) / (60 * 60 * 1000))
        });
      }
    }
  }

  return { escalations: escalationsToAutoEscalate };
}

/**
 * Process go/no-go decision with automatic escalation
 */
function processGoNoGoDecision(projectStatePath, phaseId, decision, approver, comments = null) {
  const projectState = JSON.parse(readFileSync(projectStatePath, 'utf-8'));

  // Record the decision
  if (!projectState.go_no_go_decisions) {
    projectState.go_no_go_decisions = {};
  }
  if (!projectState.go_no_go_decisions[phaseId]) {
    projectState.go_no_go_decisions[phaseId] = [];
  }

  const decisionRecord = {
    decision,
    approver,
    at: new Date().toISOString(),
    comments
  };

  projectState.go_no_go_decisions[phaseId].push(decisionRecord);
  projectState.last_go_no_go = {
    phase: phaseId,
    decision,
    approver,
    at: decisionRecord.at
  };

  // If NO-GO, create automatic escalation
  if (decision === 'no-go') {
    const escalation = createEscalation(projectStatePath, {
      reason: ESCALATION_REASONS.GO_NO_GO_NO_GO,
      phase: phaseId,
      decision: decision,
      requester: approver,
      description: `Go/no-go decision for ${phaseId} was NO-GO`,
      impact: comments || 'Phase cannot proceed',
      proposed_resolution: null
    });

    writeFileSync(projectStatePath, JSON.stringify(projectState, null, 2));

    return {
      success: true,
      decision: 'no-go',
      escalation_created: true,
      escalation_id: escalation.id,
      message: 'NO-GO decision recorded and escalation created'
    };
  }

  // If GO, update phase status
  if (decision === 'go') {
    // Check if there are open escalations for this phase
    const openEscalations = (projectState.escalations || [])
      .filter(e => e.phase === phaseId && (e.status === 'open' || e.status === 'acknowledged'));

    // Resolve any open escalations
    for (const esc of openEscalations) {
      resolveEscalation(projectStatePath, esc.id, approver, `GO decision received for ${phaseId}`, 'go');
    }

    // Update phase status
    projectState.phase_status = 'approved_to_proceed';

    writeFileSync(projectStatePath, JSON.stringify(projectState, null, 2));

    return {
      success: true,
      decision: 'go',
      escalations_resolved: openEscalations.length,
      message: 'GO decision recorded, phase approved to proceed'
    };
  }

  writeFileSync(projectStatePath, JSON.stringify(projectState, null, 2));

  return { success: true, decision };
}

/**
 * Get all escalations
 */
function getAllEscalations(projectStatePath) {
  const projectState = JSON.parse(readFileSync(projectStatePath, 'utf-8'));
  return projectState.escalations || [];
}

/**
 * Get escalation by ID
 */
function getEscalation(projectStatePath, escalationId) {
  const projectState = JSON.parse(readFileSync(projectStatePath, 'utf-8'));
  return projectState.escalations?.find(e => e.id === escalationId) || null;
}

// CLI interface
if (import.meta.url === `file://${process.argv[1]}`) {
  const args = process.argv.slice(2);
  const command = args[0];

  const projectStatePath = args[1] || '.claude/project-state.json';

  if (!existsSync(projectStatePath)) {
    console.error(JSON.stringify({ error: 'Project state file not found', path: projectStatePath }, null, 2));
    process.exit(1);
  }

  switch (command) {
    case 'create':
      const createResult = createEscalation(projectStatePath, {
        reason: args[2],
        phase: args[3],
        decision: args[4],
        requester: args[5],
        description: args[6],
        impact: args[7],
        proposed_resolution: args[8]
      });
      console.log(JSON.stringify(createResult, null, 2));
      process.exit(0);

    case 'acknowledge':
      const ackResult = acknowledgeEscalation(projectStatePath, args[2], args[3], args[4]);
      console.log(JSON.stringify(ackResult, null, 2));
      process.exit(ackResult.success ? 0 : 1);

    case 'escalate':
      const escResult = escalateToNextLevel(projectStatePath, args[2], args[3], args[4]);
      console.log(JSON.stringify(escResult, null, 2));
      process.exit(escResult.success ? 0 : 1);

    case 'resolve':
      const resolveResult = resolveEscalation(projectStatePath, args[2], args[3], args[4], args[5]);
      console.log(JSON.stringify(resolveResult, null, 2));
      process.exit(resolveResult.success ? 0 : 1);

    case 'reject':
      const rejectResult = rejectEscalation(projectStatePath, args[2], args[3], args[4]);
      console.log(JSON.stringify(rejectResult, null, 2));
      process.exit(rejectResult.success ? 0 : 1);

    case 'go-no-go':
      const decisionResult = processGoNoGoDecision(projectStatePath, args[2], args[3], args[4], args[5]);
      console.log(JSON.stringify(decisionResult, null, 2));
      process.exit(decisionResult.success ? 0 : 1);

    case 'list':
      const escalations = getAllEscalations(projectStatePath);
      console.log(JSON.stringify(escalations, null, 2));
      process.exit(0);

    case 'check-timeouts':
      const timeoutResult = checkTimeoutEscalations(projectStatePath);
      console.log(JSON.stringify(timeoutResult, null, 2));
      process.exit(0);

    default:
      console.error(JSON.stringify({
        error: 'Unknown command',
        usage: 'escalation-manager.js <command> <project-state> [args...]',
        commands: [
          'create <reason> <phase> <decision> <requester> <description> [impact] [proposed_resolution]',
          'acknowledge <escalationId> <acknowledgedBy> [comments]',
          'escalate <escalationId> <escalatedBy> [comments]',
          'resolve <escalationId> <resolvedBy> <resolution> [newDecision]',
          'reject <escalationId> <rejectedBy> <reason>',
          'go-no-go <phaseId> <go|no-go> <approver> [comments]',
          'list',
          'check-timeouts'
        ]
      }, null, 2));
      process.exit(1);
  }
}

export {
  createEscalation,
  acknowledgeEscalation,
  escalateToNextLevel,
  resolveEscalation,
  rejectEscalation,
  processGoNoGoDecision,
  checkTimeoutEscalations,
  getAllEscalations,
  getEscalation,
  ESCALATION_LEVELS,
  ESCALATION_REASONS,
  ESCALATION_PATHS
};
