#!/usr/bin/env node

/**
 * Task-Skill Binding System
 * Binds tasks to skills and verifies execution
 *
 * This is the CRITICAL component that prevents:
 * - CB-006: Tasks not bound to skills
 */

import { readFileSync, writeFileSync, existsSync } from 'fs';
import { join } from 'path';

// Task to skill mappings for each phase
const TASK_SKILL_BINDINGS = {
  phase_01_vision_strategy: {
    'create-business-case': {
      skill: 'phase_01_vision_strategy',
      required: true,
      output_artifact: 'P1-BUSINESS-001',
      validation_function: 'validateBusinessCase'
    },
    'create-prd': {
      skill: 'phase_01_vision_strategy',
      required: true,
      output_artifact: 'P1-VISION-001',
      validation_function: 'validatePRD'
    },
    'market-analysis': {
      skill: 'phase_01_vision_strategy',
      required: true,
      output_artifact: 'P1-MARKET-001',
      validation_function: 'validateMarketAnalysis'
    },
    'stakeholder-alignment': {
      skill: 'phase_01_vision_strategy',
      required: true,
      output_artifact: 'P1-STAKE-001',
      validation_function: 'validateStakeholderAlignment'
    }
  },
  phase_02_requirements_scope: {
    'define-functional-requirements': {
      skill: 'phase_02_requirements_scope',
      required: true,
      output_artifact: 'P2-REQ-001',
      validation_function: 'validateFunctionalRequirements'
    },
    'define-non-functional-requirements': {
      skill: 'phase_02_requirements_scope',
      required: true,
      output_artifact: 'P2-NFR-001',
      validation_function: 'validateNFRs'
    },
    'create-traceability-matrix': {
      skill: 'phase_02_requirements_scope',
      required: true,
      output_artifact: 'P2-TRACE-001',
      validation_function: 'validateTraceabilityMatrix'
    }
  },
  phase_03_architecture_design: {
    'design-system-architecture': {
      skill: 'phase_03_architecture_design',
      required: true,
      output_artifact: 'P3-ARCH-001',
      validation_function: 'validateSystemArchitecture'
    },
    'design-security-architecture': {
      skill: 'phase_03_architecture_design',
      required: true,
      output_artifact: 'P3-SEC-001',
      validation_function: 'validateSecurityArchitecture'
    },
    'conduct-threat-modeling': {
      skill: 'phase_03_architecture_design',
      required: true,
      output_artifact: 'P3-THREAT-001',
      validation_function: 'validateThreatModel'
    }
  },
  phase_04_development_planning: {
    'create-wbs': {
      skill: 'phase_04_development_planning',
      required: true,
      output_artifact: 'P4-WBS-001',
      validation_function: 'validateWBS'
    },
    'create-resource-plan': {
      skill: 'phase_04_development_planning',
      required: true,
      output_artifact: 'P4-RESOURCE-001',
      validation_function: 'validateResourcePlan'
    },
    'create-sprint-plan': {
      skill: 'phase_04_development_planning',
      required: true,
      output_artifact: 'P4-SPRINT-001',
      validation_function: 'validateSprintPlan'
    }
  },
  phase_05_development_execution: {
    'implement-feature': {
      skill: 'phase_05_development_execution',
      required: true,
      output_artifact_pattern: 'P5-CODE-{feature_id}',
      validation_function: 'validateFeatureCode'
    },
    'write-unit-tests': {
      skill: 'phase_05_development_execution',
      required: true,
      output_artifact_pattern: 'P5-TEST-{feature_id}',
      validation_function: 'validateUnitTests'
    },
    'code-review': {
      skill: 'phase_05_development_execution',
      required: true,
      validation_function: 'validateCodeReview'
    }
  },
  phase_06_quality_security: {
    'run-unit-tests': {
      skill: 'phase_06_quality_security',
      required: true,
      output_artifact: 'P6-TEST-UNIT-001',
      validation_function: 'validateTestResults'
    },
    'run-integration-tests': {
      skill: 'phase_06_quality_security',
      required: true,
      output_artifact: 'P6-TEST-INT-001',
      validation_function: 'validateTestResults'
    },
    'security-scan': {
      skill: 'phase_06_quality_security',
      required: true,
      output_artifact: 'P6-SEC-SCAN-001',
      validation_function: 'validateSecurityScan'
    },
    'performance-test': {
      skill: 'phase_06_quality_security',
      required: true,
      output_artifact: 'P6-PERF-001',
      validation_function: 'validatePerformanceTest'
    },
    'uat-signoff': {
      skill: 'phase_06_quality_security',
      required: true,
      output_artifact: 'P6-UAT-001',
      validation_function: 'validateUATSignoff'
    }
  },
  phase_07_deployment_release: {
    'deploy-to-production': {
      skill: 'phase_07_deployment_release',
      required: true,
      output_artifact: 'P7-DEPLOY-001',
      validation_function: 'validateDeployment'
    },
    'run-smoke-tests': {
      skill: 'phase_07_deployment_release',
      required: true,
      output_artifact: 'P7-SMOKE-001',
      validation_function: 'validateSmokeTests'
    },
    'test-rollback': {
      skill: 'phase_07_deployment_release',
      required: true,
      output_artifact: 'P7-ROLLBACK-001',
      validation_function: 'validateRollbackPlan'
    }
  },
  phase_08_operations_maintenance: {
    'setup-monitoring': {
      skill: 'phase_08_operations_maintenance',
      required: true,
      output_artifact: 'P8-MON-001',
      validation_function: 'validateMonitoring'
    },
    'setup-incident-procedures': {
      skill: 'phase_08_operations_maintenance',
      required: true,
      output_artifact: 'P8-INCIDENT-001',
      validation_function: 'validateIncidentProcedures'
    },
    'establish-on-call': {
      skill: 'phase_08_operations_maintenance',
      required: true,
      validation_function: 'validateOnCallRotation'
    }
  }
};

/**
 * Get skill for a task
 */
function getSkillForTask(phaseId, taskId) {
  const phaseBindings = TASK_SKILL_BINDINGS[phaseId];
  if (!phaseBindings) {
    return { error: `Phase not found: ${phaseId}` };
  }

  const binding = phaseBindings[taskId];
  if (!binding) {
    return { error: `Task not found in phase: ${taskId}` };
  }

  return binding;
}

/**
 * Bind task to skill and record execution
 */
function bindTaskToSkill(projectStatePath, phaseId, taskId, executionContext = {}) {
  const projectState = JSON.parse(readFileSync(projectStatePath, 'utf-8'));

  const binding = getSkillForTask(phaseId, taskId);
  if (binding.error) {
    return { success: false, error: binding.error };
  }

  // Create task execution record
  const taskExecution = {
    id: `task-${Date.now()}`,
    phase: phaseId,
    task: taskId,
    skill: binding.skill,
    bound_at: new Date().toISOString(),
    status: 'bound',
    required: binding.required,
    expected_artifact: binding.output_artifact || binding.output_artifact_pattern,
    validation_function: binding.validation_function,
    context: executionContext
  };

  // Add to project state
  if (!projectState.task_executions) {
    projectState.task_executions = [];
  }
  projectState.task_executions.push(taskExecution);

  writeFileSync(projectStatePath, JSON.stringify(projectState, null, 2));

  return { success: true, task_execution: taskExecution };
}

/**
 * Mark task as started
 */
function markTaskStarted(projectStatePath, taskExecutionId, startedBy = null) {
  const projectState = JSON.parse(readFileSync(projectStatePath, 'utf-8'));

  const taskExecution = projectState.task_executions?.find(t => t.id === taskExecutionId);
  if (!taskExecution) {
    return { success: false, error: `Task execution not found: ${taskExecutionId}` };
  }

  taskExecution.status = 'started';
  taskExecution.started_at = new Date().toISOString();
  taskExecution.started_by = startedBy;

  writeFileSync(projectStatePath, JSON.stringify(projectState, null, 2));

  return { success: true, task_execution };
}

/**
 * Mark task as completed
 */
function markTaskCompleted(projectStatePath, taskExecutionId, result = {}) {
  const projectState = JSON.parse(readFileSync(projectStatePath, 'utf-8'));

  const taskExecution = projectState.task_executions?.find(t => t.id === taskExecutionId);
  if (!taskExecution) {
    return { success: false, error: `Task execution not found: ${taskExecutionId}` };
  }

  taskExecution.status = 'completed';
  taskExecution.completed_at = new Date().toISOString();
  taskExecution.result = result;

  // Verify artifact was created if expected
  if (taskExecution.expected_artifact && result.artifact) {
    taskExecution.artifact_created = result.artifact;
  }

  writeFileSync(projectStatePath, JSON.stringify(projectState, null, 2));

  return { success: true, task_execution };
}

/**
 * Verify task execution (validation)
 */
function verifyTaskExecution(projectStatePath, taskExecutionId) {
  const projectState = JSON.parse(readFileSync(projectStatePath, 'utf-8'));

  const taskExecution = projectState.task_executions?.find(t => t.id === taskExecutionId);
  if (!taskExecution) {
    return { success: false, error: `Task execution not found: ${taskExecutionId}` };
  }

  const validation = {
    task_execution_id: taskExecutionId,
    task: taskExecution.task,
    skill: taskExecution.skill,
    status: taskExecution.status,
    verified: false,
    issues: []
  };

  // Check if task was completed
  if (taskExecution.status !== 'completed') {
    validation.issues.push({
      severity: 'error',
      message: `Task not completed (status: ${taskExecution.status})`
    });
    return validation;
  }

  // Check if expected artifact was created
  if (taskExecution.expected_artifact && !taskExecution.artifact_created) {
    validation.issues.push({
      severity: 'error',
      message: `Expected artifact not created: ${taskExecution.expected_artifact}`
    });
  }

  // Verify artifact exists in project state
  if (taskExecution.artifact_created) {
    const artifactExists = projectState.artifacts?.[taskExecution.artifact_created];
    if (!artifactExists) {
      validation.issues.push({
        severity: 'error',
        message: `Artifact not found in project state: ${taskExecution.artifact_created}`
      });
    }
  }

  // Check validation result
  if (taskExecution.result && taskExecution.result.validation_result) {
    if (!taskExecution.result.validation_result.passed) {
      validation.issues.push({
        severity: 'error',
        message: 'Task validation failed',
        details: taskExecution.result.validation_result
      });
    }
  }

  validation.verified = validation.issues.length === 0;
  validation.issues_count = validation.issues.length;

  return validation;
}

/**
 * Get all incomplete tasks for a phase
 */
function getIncompleteTasks(projectStatePath, phaseId) {
  const projectState = JSON.parse(readFileSync(projectStatePath, 'utf-8'));

  const phaseBindings = TASK_SKILL_BINDINGS[phaseId];
  if (!phaseBindings) {
    return { error: `Phase not found: ${phaseId}` };
  }

  const taskIds = Object.keys(phaseBindings);
  const completedTaskIds = (projectState.task_executions || [])
    .filter(t => t.phase === phaseId && t.status === 'completed')
    .map(t => t.task);

  const incompleteTasks = taskIds
    .filter(taskId => !completedTaskIds.includes(taskId))
    .map(taskId => ({
      task: taskId,
      skill: phaseBindings[taskId].skill,
      required: phaseBindings[taskId].required
    }));

  return {
    phase: phaseId,
    total_tasks: taskIds.length,
    completed_tasks: completedTaskIds.length,
    incomplete_tasks: incompleteTasks.length,
    incomplete: incompleteTasks
  };
}

/**
 * Get task-skill binding summary for a phase
 */
function getPhaseTaskSummary(projectStatePath, phaseId) {
  const projectState = JSON.parse(readFileSync(projectStatePath, 'utf-8'));

  const phaseBindings = TASK_SKILL_BINDINGS[phaseId];
  if (!phaseBindings) {
    return { error: `Phase not found: ${phaseId}` };
  }

  const taskIds = Object.keys(phaseBindings);
  const summary = {
    phase: phaseId,
    tasks: []
  };

  for (const taskId of taskIds) {
    const binding = phaseBindings[taskId];
    const executions = (projectState.task_executions || [])
      .filter(t => t.phase === phaseId && t.task === taskId);

    const latestExecution = executions.length > 0 ? executions[executions.length - 1] : null;

    summary.tasks.push({
      task: taskId,
      skill: binding.skill,
      required: binding.required,
      expected_artifact: binding.output_artifact || binding.output_artifact_pattern,
      execution_count: executions.length,
      latest_status: latestExecution?.status || 'not_started',
      latest_execution_id: latestExecution?.id || null
    });
  }

  return summary;
}

// CLI interface
if (import.meta.url === `file://${process.argv[1]}`) {
  const args = process.argv.slice(2);
  const command = args[0];

  const projectStatePath = args[1] || '.claude/project-state.json';

  if (!existsSync(projectStatePath)) {
    console.error(JSON.stringify({ error: 'Project state file not found' }, null, 2));
    process.exit(1);
  }

  switch (command) {
    case 'get-skill': {
      const phaseId = args[2];
      const taskId = args[3];
      const result = getSkillForTask(phaseId, taskId);
      console.log(JSON.stringify(result, null, 2));
      process.exit(result.error ? 1 : 0);
    }

    case 'bind': {
      const phaseId = args[2];
      const taskId = args[3];
      const contextJson = args[4] || '{}';
      const context = JSON.parse(contextJson);
      const result = bindTaskToSkill(projectStatePath, phaseId, taskId, context);
      console.log(JSON.stringify(result, null, 2));
      process.exit(result.success ? 0 : 1);
    }

    case 'start': {
      const taskExecutionId = args[2];
      const startedBy = args[3] || null;
      const result = markTaskStarted(projectStatePath, taskExecutionId, startedBy);
      console.log(JSON.stringify(result, null, 2));
      process.exit(result.success ? 0 : 1);
    }

    case 'complete': {
      const taskExecutionId = args[2];
      const resultJson = args[3] || '{}';
      const result = JSON.parse(resultJson);
      const completeResult = markTaskCompleted(projectStatePath, taskExecutionId, result);
      console.log(JSON.stringify(completeResult, null, 2));
      process.exit(completeResult.success ? 0 : 1);
    }

    case 'verify': {
      const taskExecutionId = args[2];
      const result = verifyTaskExecution(projectStatePath, taskExecutionId);
      console.log(JSON.stringify(result, null, 2));
      process.exit(result.verified ? 0 : 1);
    }

    case 'incomplete': {
      const phaseId = args[2];
      const result = getIncompleteTasks(projectStatePath, phaseId);
      console.log(JSON.stringify(result, null, 2));
      process.exit(0);
    }

    case 'summary': {
      const phaseId = args[2];
      const result = getPhaseTaskSummary(projectStatePath, phaseId);
      console.log(JSON.stringify(result, null, 2));
      process.exit(0);
    }

    default:
      console.error(JSON.stringify({
        error: 'Unknown command',
        usage: 'task-skill-binder.js <command> <project-state> [args...]',
        commands: [
          'get-skill <phaseId> <taskId>',
          'bind <phaseId> <taskId> [contextJson]',
          'start <taskExecutionId> [startedBy]',
          'complete <taskExecutionId> [resultJson]',
          'verify <taskExecutionId>',
          'incomplete <phaseId>',
          'summary <phaseId>'
        ]
      }, null, 2));
      process.exit(1);
  }
}

export {
  getSkillForTask,
  bindTaskToSkill,
  markTaskStarted,
  markTaskCompleted,
  verifyTaskExecution,
  getIncompleteTasks,
  getPhaseTaskSummary,
  TASK_SKILL_BINDINGS
};
