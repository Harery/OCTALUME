#!/usr/bin/env node

/**
 * Phase Handoff Verification System
 * Verifies deliverables are properly handed off between phases
 *
 * This is the CRITICAL component that prevents:
 * - RF-009: No handoff verification
 */

import { readFileSync, writeFileSync, existsSync } from 'fs';
import { join } from 'path';

/**
 * Create a handoff package
 */
function createHandoff(fromPhase, toPhase, deliverables, handoffBy) {
  const handoff = {
    id: `HANDOFF-${fromPhase}-TO-${toPhase}-${Date.now()}`,
    from_phase: fromPhase,
    to_phase: toPhase,
    created_at: new Date().toISOString(),
    created_by: handoffBy,
    status: 'pending', // pending, acknowledged, accepted, rejected
    deliverables: deliverables,
    acknowledgment: null,
    acceptance: null
  };

  return handoff;
}

/**
 * Record handoff in project state
 */
function recordHandoff(projectStatePath, handoff) {
  const projectState = JSON.parse(readFileSync(projectStatePath, 'utf-8'));

  if (!projectState.handoffs) {
    projectState.handoffs = [];
  }

  projectState.handoffs.push(handoff);

  writeFileSync(projectStatePath, JSON.stringify(projectState, null, 2));

  return { success: true, handoff };
}

/**
 * Acknowledge handoff
 */
function acknowledgeHandoff(projectStatePath, handoffId, acknowledgedBy, comments = null) {
  const projectState = JSON.parse(readFileSync(projectStatePath, 'utf-8'));

  const handoff = projectState.handoffs?.find(h => h.id === handoffId);
  if (!handoff) {
    return { success: false, error: `Handoff not found: ${handoffId}` };
  }

  if (handoff.status !== 'pending') {
    return {
      success: false,
      error: `Handoff not in pending status (current: ${handoff.status})`
    };
  }

  handoff.status = 'acknowledged';
  handoff.acknowledgment = {
    acknowledged_by: acknowledgedBy,
    acknowledged_at: new Date().toISOString(),
    comments: comments
  };

  writeFileSync(projectStatePath, JSON.stringify(projectState, null, 2));

  return { success: true, handoff };
}

/**
 * Accept handoff
 */
function acceptHandoff(projectStatePath, handoffId, acceptedBy, verificationResults = null) {
  const projectState = JSON.parse(readFileSync(projectStatePath, 'utf-8'));

  const handoff = projectState.handoffs?.find(h => h.id === handoffId);
  if (!handoff) {
    return { success: false, error: `Handoff not found: ${handoffId}` };
  }

  handoff.status = 'accepted';
  handoff.acceptance = {
    accepted_by: acceptedBy,
    accepted_at: new Date().toISOString(),
    verification_results: verificationResults
  };

  // Mark deliverables as received
  if (handoff.deliverables && handoff.deliverables.length > 0) {
    if (!projectState.received_deliverables) {
      projectState.received_deliverables = [];
    }

    for (const deliverable of handoff.deliverables) {
      projectState.received_deliverables.push({
        ...deliverable,
        received_from: handoff.from_phase,
        received_at: new Date().toISOString(),
        received_by: acceptedBy,
        handoff_id: handoffId
      });

      // Track artifact in project state
      if (deliverable.artifact_id) {
        if (!projectState.artifacts) {
          projectState.artifacts = {};
        }
        if (!projectState.artifacts[deliverable.artifact_id]) {
          projectState.artifacts[deliverable.artifact_id] = {
            id: deliverable.artifact_id,
            received_from: handoff.from_phase,
            received_at: new Date().toISOString(),
            handoff_id: handoffId
          };
        }
      }
    }
  }

  writeFileSync(projectStatePath, JSON.stringify(projectState, null, 2));

  return { success: true, handoff };
}

/**
 * Reject handoff
 */
function rejectHandoff(projectStatePath, handoffId, rejectedBy, reason, missingDeliverables = []) {
  const projectState = JSON.parse(readFileSync(projectStatePath, 'utf-8'));

  const handoff = projectState.handoffs?.find(h => h.id === handoffId);
  if (!handoff) {
    return { success: false, error: `Handoff not found: ${handoffId}` };
  }

  handoff.status = 'rejected';
  handoff.acceptance = {
    rejected_by: rejectedBy,
    rejected_at: new Date().toISOString(),
    reason: reason,
    missing_deliverables: missingDeliverables
  };

  // Set phase status back to blocked
  if (projectState.current_phase === handoff.to_phase) {
    projectState.phase_status = 'blocked';
    projectState.blocked_reason = `handoff_rejected:${handoffId}`;
  }

  writeFileSync(projectStatePath, JSON.stringify(projectState, null, 2));

  return { success: true, handoff };
}

/**
 * Verify handoff completeness
 */
function verifyHandoff(handoff, projectState) {
  const verification = {
    handoff_id: handoff.id,
    from_phase: handoff.from_phase,
    to_phase: handoff.to_phase,
    verified: false,
    issues: [],
    deliverables_verified: []
  };

  // Check all deliverables
  if (handoff.deliverables && handoff.deliverables.length > 0) {
    for (const deliverable of handoff.deliverables) {
      const delivVerification = {
        deliverable: deliverable,
        verified: false,
        issues: []
      };

      // Check if deliverable has required fields
      if (!deliverable.type) {
        delivVerification.issues.push({
          severity: 'error',
          message: 'Deliverable type not specified'
        });
      }

      // Check if artifact exists
      if (deliverable.artifact_id) {
        const artifactExists = projectState.artifacts?.[deliverable.artifact_id];
        if (!artifactExists) {
          delivVerification.issues.push({
            severity: 'error',
            message: `Artifact not found: ${deliverable.artifact_id}`
          });
        } else {
          delivVerification.verified = true;
        }
      } else {
        // Non-artifact deliverable (e.g., decision, approval)
        delivVerification.verified = true;
      }

      verification.deliverables_verified.push(delivVerification);

      if (delivVerification.issues.length > 0) {
        verification.issues.push(...delivVerification.issues);
      }
    }
  }

  verification.verified = verification.issues.length === 0;

  return verification;
}

/**
 * Get pending handoffs for a phase
 */
function getPendingHandoffs(projectStatePath, phaseId) {
  const projectState = JSON.parse(readFileSync(projectStatePath, 'utf-8'));

  const pendingHandoffs = (projectState.handoffs || [])
    .filter(h => h.to_phase === phaseId && h.status === 'pending');

  return {
    phase: phaseId,
    pending_count: pendingHandoffs.length,
    handoffs: pendingHandoffs
  };
}

/**
 * Get handoff history
 */
function getHandoffHistory(projectStatePath, fromPhase = null, toPhase = null) {
  const projectState = JSON.parse(readFileSync(projectStatePath, 'utf-8'));

  let handoffs = projectState.handoffs || [];

  if (fromPhase) {
    handoffs = handoffs.filter(h => h.from_phase === fromPhase);
  }

  if (toPhase) {
    handoffs = handoffs.filter(h => h.to_phase === toPhase);
  }

  return {
    from_phase: fromPhase,
    to_phase: toPhase,
    count: handoffs.length,
    handoffs: handoffs
  };
}

// CLI interface
if (import.meta.url === `file://${process.argv[1]}`) {
  const args = process.argv.slice(2);
  const command = args[0];

  const projectStatePath = args[1] || '.claude/project-state.json';

  switch (command) {
    case 'create': {
      const fromPhase = args[2];
      const toPhase = args[3];
      const deliverablesJson = args[4] || '[]';
      const handoffBy = args[5] || 'system';
      const deliverables = JSON.parse(deliverablesJson);

      const handoff = createHandoff(fromPhase, toPhase, deliverables, handoffBy);
      const result = recordHandoff(projectStatePath, handoff);
      console.log(JSON.stringify(result, null, 2));
      process.exit(result.success ? 0 : 1);
    }

    case 'acknowledge': {
      const handoffId = args[2];
      const acknowledgedBy = args[3];
      const comments = args[4] || null;
      const result = acknowledgeHandoff(projectStatePath, handoffId, acknowledgedBy, comments);
      console.log(JSON.stringify(result, null, 2));
      process.exit(result.success ? 0 : 1);
    }

    case 'accept': {
      const handoffId = args[2];
      const acceptedBy = args[3];
      const verificationJson = args[4] || null;
      const verificationResults = verificationJson ? JSON.parse(verificationJson) : null;
      const result = acceptHandoff(projectStatePath, handoffId, acceptedBy, verificationResults);
      console.log(JSON.stringify(result, null, 2));
      process.exit(result.success ? 0 : 1);
    }

    case 'reject': {
      const handoffId = args[2];
      const rejectedBy = args[3];
      const reason = args[4];
      const missingJson = args[5] || '[]';
      const missingDeliverables = JSON.parse(missingJson);
      const result = rejectHandoff(projectStatePath, handoffId, rejectedBy, reason, missingDeliverables);
      console.log(JSON.stringify(result, null, 2));
      process.exit(result.success ? 0 : 1);
    }

    case 'pending': {
      const phaseId = args[2];
      const result = getPendingHandoffs(projectStatePath, phaseId);
      console.log(JSON.stringify(result, null, 2));
      process.exit(0);
    }

    case 'history': {
      const fromPhase = args[2] || null;
      const toPhase = args[3] || null;
      const result = getHandoffHistory(projectStatePath, fromPhase, toPhase);
      console.log(JSON.stringify(result, null, 2));
      process.exit(0);
    }

    default:
      console.error(JSON.stringify({
        error: 'Unknown command',
        usage: 'handoff-verify.js <command> <project-state> [args...]',
        commands: [
          'create <fromPhase> <toPhase> <deliverablesJson> [handoffBy]',
          'acknowledge <handoffId> <acknowledgedBy> [comments]',
          'accept <handoffId> <acceptedBy> [verificationJson]',
          'reject <handoffId> <rejectedBy> <reason> [missingDeliverablesJson]',
          'pending <phaseId>',
          'history [fromPhase] [toPhase]'
        ]
      }, null, 2));
      process.exit(1);
  }
}

export {
  createHandoff,
  recordHandoff,
  acknowledgeHandoff,
  acceptHandoff,
  rejectHandoff,
  verifyHandoff,
  getPendingHandoffs,
  getHandoffHistory
};
