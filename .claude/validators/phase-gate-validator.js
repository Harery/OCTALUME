#!/usr/bin/env node

/**
 * Phase Gate Validator
 * Enforces entry and exit criteria for phase transitions
 *
 * This is the CRITICAL component that prevents:
 * - CB-001: Phase gate validation bypass
 * - CB-007: Entry criteria not validated
 * - CB-008: Exit criteria not validated
 */

import { readFileSync, writeFileSync, existsSync } from 'fs';
import { join } from 'path';

const PHASE_GATES = {
  phase_01_vision_strategy: {
    entry_criteria: [
      { id: 'p1-entry-1', criteria: 'Business idea or opportunity identified', required: true, validated: false },
      { id: 'p1-entry-2', criteria: 'Executive sponsor identified', required: true, validated: false }
    ],
    exit_criteria: [
      { id: 'p1-exit-1', criteria: 'Business case approved by Executive Sponsor', required: true, validated: false, artifact: 'P1-BUSINESS-001' },
      { id: 'p1-exit-2', criteria: 'PRD completed and reviewed', required: true, validated: false, artifact: 'P1-VISION-001' },
      { id: 'p1-exit-3', criteria: 'Technical feasibility confirmed by CTA', required: true, validated: false },
      { id: 'p1-exit-4', criteria: 'Security considerations documented', required: true, validated: false },
      { id: 'p1-exit-5', criteria: 'Stakeholders aligned and committed', required: true, validated: false },
      { id: 'p1-exit-6', criteria: 'Budget and resources identified', required: true, validated: false }
    ],
    approver: 'Executive Sponsor',
    next_phase: 'phase_02_requirements_scope'
  },
  phase_02_requirements_scope: {
    entry_criteria: [
      { id: 'p2-entry-1', criteria: 'Approved PRD from Phase 1', required: true, validated: false, artifact: 'P1-VISION-001' },
      { id: 'p2-entry-2', criteria: 'Business case approved', required: true, validated: false, artifact: 'P1-BUSINESS-001' }
    ],
    exit_criteria: [
      { id: 'p2-exit-1', criteria: 'Functional requirements approved', required: true, validated: false, artifact: 'P2-REQ-001' },
      { id: 'p2-exit-2', criteria: 'Non-functional requirements approved', required: true, validated: false, artifact: 'P2-NFR-001' },
      { id: 'p2-exit-3', criteria: 'Security requirements defined', required: true, validated: false },
      { id: 'p2-exit-4', criteria: 'Compliance requirements identified', required: true, validated: false },
      { id: 'p2-exit-5', criteria: 'Traceability matrix created', required: true, validated: false, artifact: 'P2-TRACE-001' }
    ],
    approver: 'Product Owner',
    next_phase: 'phase_03_architecture_design'
  },
  phase_03_architecture_design: {
    entry_criteria: [
      { id: 'p3-entry-1', criteria: 'Approved requirements from Phase 2', required: true, validated: false, artifact: 'P2-REQ-001' },
      { id: 'p3-entry-2', criteria: 'Traceability matrix approved', required: true, validated: false, artifact: 'P2-TRACE-001' }
    ],
    exit_criteria: [
      { id: 'p3-exit-1', criteria: 'System architecture approved', required: true, validated: false, artifact: 'P3-ARCH-001' },
      { id: 'p3-exit-2', criteria: 'Security architecture approved', required: true, validated: false, artifact: 'P3-SEC-001' },
      { id: 'p3-exit-3', criteria: 'Data architecture approved', required: true, validated: false, artifact: 'P3-DATA-001' },
      { id: 'p3-exit-4', criteria: 'Threat models completed', required: true, validated: false, artifact: 'P3-THREAT-001' },
      { id: 'p3-exit-5', criteria: 'Technology stack decisions made', required: true, validated: false, artifact: 'P3-TECH-001' }
    ],
    approver: 'CTA',
    next_phase: 'phase_04_development_planning'
  },
  phase_04_development_planning: {
    entry_criteria: [
      { id: 'p4-entry-1', criteria: 'Approved architecture from Phase 3', required: true, validated: false, artifact: 'P3-ARCH-001' },
      { id: 'p4-entry-2', criteria: 'Security architecture approved', required: true, validated: false, artifact: 'P3-SEC-001' }
    ],
    exit_criteria: [
      { id: 'p4-exit-1', criteria: 'WBS approved', required: true, validated: false, artifact: 'P4-WBS-001' },
      { id: 'p4-exit-2', criteria: 'Resource plan approved', required: true, validated: false, artifact: 'P4-RESOURCE-001' },
      { id: 'p4-exit-3', criteria: 'Sprint plan created', required: true, validated: false, artifact: 'P4-SPRINT-001' },
      { id: 'p4-exit-4', criteria: 'Risk assessment completed', required: true, validated: false, artifact: 'P4-RISK-001' },
      { id: 'p4-exit-5', criteria: 'CI/CD pipeline planned', required: true, validated: false }
    ],
    approver: 'Tech Lead',
    next_phase: 'phase_05_development_execution'
  },
  phase_05_development_execution: {
    entry_criteria: [
      { id: 'p5-entry-1', criteria: 'Approved plan from Phase 4', required: true, validated: false, artifact: 'P4-WBS-001' },
      { id: 'p5-entry-2', criteria: 'Sprint plan approved', required: true, validated: false, artifact: 'P4-SPRINT-001' }
    ],
    exit_criteria: [
      { id: 'p5-exit-1', criteria: 'All features complete', required: true, validated: false, dynamic: true },
      { id: 'p5-exit-2', criteria: 'Unit tests passing', required: true, validated: false },
      { id: 'p5-exit-3', criteria: 'Code review complete', required: true, validated: false },
      { id: 'p5-exit-4', criteria: 'Sprint velocity stable', required: false, validated: false }
    ],
    approver: 'QA Lead',
    next_phase: 'phase_06_quality_security',
    // NEW: Define completion condition for iterative phase
    completion_condition: {
      type: 'feature_completion',
      threshold: 0.95, // 95% of features must be complete
      minimum_sprints: 3,
      maximum_sprints: 20,
      stable_velocity_sprints: 3
    }
  },
  phase_06_quality_security: {
    entry_criteria: [
      { id: 'p6-entry-1', criteria: 'Complete development from Phase 5', required: true, validated: false },
      { id: 'p6-entry-2', criteria: 'Unit tests passing', required: true, validated: false }
    ],
    exit_criteria: [
      { id: 'p6-exit-1', criteria: 'All unit tests passing', required: true, validated: false, artifact: 'P6-TEST-UNIT-001' },
      { id: 'p6-exit-2', criteria: 'All integration tests passing', required: true, validated: false, artifact: 'P6-TEST-INT-001' },
      { id: 'p6-exit-3', criteria: 'Security scan passed', required: true, validated: false, artifact: 'P6-SEC-SCAN-001' },
      { id: 'p6-exit-4', criteria: 'Performance tests passed', required: true, validated: false, artifact: 'P6-PERF-001' },
      { id: 'p6-exit-5', criteria: 'UAT signed off', required: true, validated: false, artifact: 'P6-UAT-001' },
      { id: 'p6-exit-6', criteria: 'Compliance validated', required: true, validated: false, artifact: 'P6-COMP-001' }
    ],
    approver: 'Product Owner',
    next_phase: 'phase_07_deployment_release'
  },
  phase_07_deployment_release: {
    entry_criteria: [
      { id: 'p7-entry-1', criteria: 'Validated build from Phase 6', required: true, validated: false, artifact: 'P6-TEST-INT-001' },
      { id: 'p7-entry-2', criteria: 'Security sign-off obtained', required: true, validated: false, artifact: 'P6-SEC-SCAN-001' }
    ],
    exit_criteria: [
      { id: 'p7-exit-1', criteria: 'Deployed to production', required: true, validated: false, artifact: 'P7-DEPLOY-001' },
      { id: 'p7-exit-2', criteria: 'Smoke tests passing', required: true, validated: false, artifact: 'P7-SMOKE-001' },
      { id: 'p7-exit-3', criteria: 'Rollback plan tested', required: true, validated: false, artifact: 'P7-ROLLBACK-001' },
      { id: 'p7-exit-4', criteria: 'Release notes published', required: true, validated: false, artifact: 'P7-RELNOTE-001' }
    ],
    approver: 'Executive',
    next_phase: 'phase_08_operations_maintenance'
  },
  phase_08_operations_maintenance: {
    entry_criteria: [
      { id: 'p8-entry-1', criteria: 'Released to production', required: true, validated: false, artifact: 'P7-DEPLOY-001' },
      { id: 'p8-entry-2', criteria: 'Monitoring active', required: true, validated: false }
    ],
    exit_criteria: [
      { id: 'p8-exit-1', criteria: 'Monitoring baseline established', required: true, validated: false, artifact: 'P8-MON-001' },
      { id: 'p8-exit-2', criteria: 'Incident procedures active', required: true, validated: false, artifact: 'P8-INCIDENT-001' },
      { id: 'p8-exit-3', criteria: 'On-call rotation established', required: true, validated: false }
    ],
    approver: 'SRE Lead',
    next_phase: 'project_closure',
    // NEW: Define terminal state for Phase 8
    terminal_state: {
      type: 'ongoing_to_closure',
      closure_triggers: [
        'end_of_life',
        'project_completion',
        'strategic_sunset'
      ],
      closure_criteria: [
        'All incidents resolved',
        'Documentation archived',
        'Knowledge transfer complete',
        'Stakeholder notification sent'
      ]
    }
  },
  project_closure: {
    // NEW: Phase 8 terminal state and project closure
    entry_criteria: [
      { id: 'closure-entry-1', criteria: 'Closure trigger identified', required: true, validated: false },
      { id: 'closure-entry-2', criteria: 'Phase 8 handoff complete', required: true, validated: false }
    ],
    exit_criteria: [
      { id: 'closure-exit-1', criteria: 'All artifacts archived', required: true, validated: false, artifact: 'FINAL-ARCHIVE-001' },
      { id: 'closure-exit-2', criteria: 'Final retrospective complete', required: true, validated: false, artifact: 'FINAL-RETRO-001' },
      { id: 'closure-exit-3', criteria: 'Project report published', required: true, validated: false, artifact: 'FINAL-REPORT-001' }
    ],
    approver: 'Executive Sponsor',
    next_phase: null // Terminal state
  }
};

/**
 * Validate entry criteria for a phase
 */
function validateEntryCriteria(phaseId, projectState) {
  const phase = PHASE_GATES[phaseId];
  if (!phase) {
    return { valid: false, errors: [`Phase ${phaseId} not found`] };
  }

  const errors = [];
  const warnings = [];

  for (const criterion of phase.entry_criteria) {
    // Check if criterion is marked as validated in project state
    const isValidated = projectState.phase_validation?.[phaseId]?.entry_criteria?.[criterion.id];

    if (!isValidated && criterion.required) {
      if (criterion.artifact) {
        // Check if artifact exists
        const artifactExists = projectState.artifacts?.[criterion.artifact];
        if (!artifactExists) {
          errors.push(`Required artifact missing: ${criterion.artifact} (${criterion.criteria})`);
        }
      } else {
        errors.push(`Entry criterion not met: ${criterion.criteria}`);
      }
    }
  }

  return {
    valid: errors.length === 0,
    errors,
    warnings,
    phase: phaseId,
    criteria_type: 'entry'
  };
}

/**
 * Validate exit criteria for a phase
 */
function validateExitCriteria(phaseId, projectState) {
  const phase = PHASE_GATES[phaseId];
  if (!phase) {
    return { valid: false, errors: [`Phase ${phaseId} not found`] };
  }

  const errors = [];
  const warnings = [];

  for (const criterion of phase.exit_criteria) {
    // Check if criterion is marked as validated in project state
    const isValidated = projectState.phase_validation?.[phaseId]?.exit_criteria?.[criterion.id];

    if (!isValidated && criterion.required) {
      if (criterion.artifact) {
        // Check if artifact exists
        const artifactExists = projectState.artifacts?.[criterion.artifact];
        if (!artifactExists) {
          errors.push(`Required artifact missing: ${criterion.artifact} (${criterion.criteria})`);
        }
      } else if (criterion.dynamic) {
        // Dynamic criteria require runtime validation
        warnings.push(`Dynamic criterion requires validation: ${criterion.criteria}`);
      } else {
        errors.push(`Exit criterion not met: ${criterion.criteria}`);
      }
    }
  }

  // Special handling for Phase 5 completion condition
  if (phaseId === 'phase_05_development_execution' && phase.completion_condition) {
    const featureList = projectState.feature_list;
    if (featureList) {
      const total = featureList.total_features || 0;
      const completed = featureList.completed_features || 0;
      const completionRate = total > 0 ? completed / total : 0;

      if (completionRate < phase.completion_condition.threshold) {
        errors.push(`Feature completion rate (${(completionRate * 100).toFixed(1)}%) below threshold (${(phase.completion_condition.threshold * 100)}%)`);
      }
    }
  }

  return {
    valid: errors.length === 0,
    errors,
    warnings,
    phase: phaseId,
    criteria_type: 'exit'
  };
}

/**
 * Check if phase transition is allowed
 */
function canTransitionToNext(currentPhaseId, projectState) {
  // First validate exit criteria of current phase
  const exitValidation = validateExitCriteria(currentPhaseId, projectState);
  if (!exitValidation.valid) {
    return {
      allowed: false,
      reason: 'Exit criteria not met',
      errors: exitValidation.errors
    };
  }

  // Get next phase
  const currentPhase = PHASE_GATES[currentPhaseId];
  const nextPhaseId = currentPhase.next_phase;

  if (!nextPhaseId) {
    return {
      allowed: false,
      reason: 'No next phase defined (terminal state)',
      next_phase: null
    };
  }

  // Validate entry criteria of next phase
  const entryValidation = validateEntryCriteria(nextPhaseId, projectState);
  if (!entryValidation.valid) {
    return {
      allowed: false,
      reason: 'Next phase entry criteria not met',
      next_phase: nextPhaseId,
      errors: entryValidation.errors
    };
  }

  return {
    allowed: true,
    current_phase: currentPhaseId,
    next_phase: nextPhaseId,
    approver: currentPhase.approver
  };
}

/**
 * Mark a criterion as validated
 */
function markCriterionValidated(phaseId, criteriaType, criterionId, projectStatePath, artifactId = null) {
  const projectState = JSON.parse(readFileSync(projectStatePath, 'utf-8'));

  if (!projectState.phase_validation) {
    projectState.phase_validation = {};
  }
  if (!projectState.phase_validation[phaseId]) {
    projectState.phase_validation[phaseId] = {};
  }
  if (!projectState.phase_validation[phaseId][criteriaType]) {
    projectState.phase_validation[phaseId][criteriaType] = {};
  }

  projectState.phase_validation[phaseId][criteriaType][criterionId] = {
    validated: true,
    validated_at: new Date().toISOString(),
    artifact: artifactId
  };

  writeFileSync(projectStatePath, JSON.stringify(projectState, null, 2));

  return { success: true, criterion: criterionId, phase: phaseId };
}

/**
 * Get all phase gates for inspection
 */
function getAllPhaseGates() {
  return PHASE_GATES;
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

  const projectState = JSON.parse(readFileSync(projectStatePath, 'utf-8'));

  switch (command) {
    case 'validate-entry':
      const phaseId = args[2];
      const entryResult = validateEntryCriteria(phaseId, projectState);
      console.log(JSON.stringify(entryResult, null, 2));
      process.exit(entryResult.valid ? 0 : 1);

    case 'validate-exit':
      const exitPhaseId = args[2];
      const exitResult = validateExitCriteria(exitPhaseId, projectState);
      console.log(JSON.stringify(exitResult, null, 2));
      process.exit(exitResult.valid ? 0 : 1);

    case 'can-transition':
      const currentPhase = args[2] || projectState.current_phase;
      const transitionResult = canTransitionToNext(currentPhase, projectState);
      console.log(JSON.stringify(transitionResult, null, 2));
      process.exit(transitionResult.allowed ? 0 : 1);

    case 'mark-validated':
      const markPhase = args[2];
      const criteriaType = args[3];
      const criterionId = args[4];
      const artifact = args[5];
      const markResult = markCriterionValidated(markPhase, criteriaType, criterionId, projectStatePath, artifact);
      console.log(JSON.stringify(markResult, null, 2));
      process.exit(0);

    case 'list-gates':
      console.log(JSON.stringify(getAllPhaseGates(), null, 2));
      process.exit(0);

    default:
      console.error(JSON.stringify({
        error: 'Unknown command',
        usage: 'phase-gate-validator.js <command> <project-state> [args...]',
        commands: [
          'validate-entry <phaseId>',
          'validate-exit <phaseId>',
          'can-transition [phaseId]',
          'mark-validated <phaseId> <entry|exit> <criterionId> [artifactId]',
          'list-gates'
        ]
      }, null, 2));
      process.exit(1);
  }
}

export {
  validateEntryCriteria,
  validateExitCriteria,
  canTransitionToNext,
  markCriterionValidated,
  getAllPhaseGates,
  PHASE_GATES
};
