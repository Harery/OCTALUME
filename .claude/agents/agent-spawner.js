#!/usr/bin/env node

/**
 * Agent Spawner
 * Implements the agent spawn/return mechanism with timeout detection
 *
 * This is the CRITICAL component that prevents:
 * - CB-004: Agent spawn mechanism is pseudocode
 * - RF-002: Agent orphaning (no timeout detection)
 */

import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import { join, dirname } from 'path';
import { spawn as childSpawn } from 'child_process';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Agent configurations
const AGENTS = {
  initializer: {
    name: 'Lifecycle Initializer Agent',
    description: 'Initializes new lifecycle projects with complete structure',
    prompt_file: '.claude/agents/INITIALIZER.md',
    timeout_ms: 300000, // 5 minutes
    max_retries: 1
  },
  orchestrator: {
    name: 'Lifecycle Orchestrator',
    description: 'Coordinates phase-specific sub-agents',
    prompt_file: '.claude/ORCHESTRATOR.md',
    timeout_ms: 600000, // 10 minutes
    max_retries: 2
  },
  coder: {
    name: 'Lifecycle Coding Agent',
    description: 'Makes incremental progress on features',
    prompt_file: '.claude/agents/CODING.md',
    timeout_ms: 900000, // 15 minutes
    max_retries: 3
  },
  phase_01_vision_strategy: {
    name: 'Phase 1: Vision & Strategy Agent',
    description: 'Executes Phase 1 of the lifecycle',
    prompt_file: 'skills/phase_01_vision_strategy/SKILL.md',
    timeout_ms: 1200000, // 20 minutes
    max_retries: 2
  },
  phase_02_requirements_scope: {
    name: 'Phase 2: Requirements & Scope Agent',
    description: 'Executes Phase 2 of the lifecycle',
    prompt_file: 'skills/phase_02_requirements_scope/SKILL.md',
    timeout_ms: 1200000, // 20 minutes
    max_retries: 2
  },
  phase_03_architecture_design: {
    name: 'Phase 3: Architecture & Design Agent',
    description: 'Executes Phase 3 of the lifecycle',
    prompt_file: 'skills/phase_03_architecture_design/SKILL.md',
    timeout_ms: 1800000, // 30 minutes
    max_retries: 2
  },
  phase_04_development_planning: {
    name: 'Phase 4: Development Planning Agent',
    description: 'Executes Phase 4 of the lifecycle',
    prompt_file: 'skills/phase_04_development_planning/SKILL.md',
    timeout_ms: 900000, // 15 minutes
    max_retries: 2
  },
  phase_05_development_execution: {
    name: 'Phase 5: Development Execution Agent',
    description: 'Executes Phase 5 of the lifecycle',
    prompt_file: 'skills/phase_05_development_execution/SKILL.md',
    timeout_ms: 3600000, // 60 minutes (iterative)
    max_retries: 3
  },
  phase_06_quality_security: {
    name: 'Phase 6: Quality & Security Agent',
    description: 'Executes Phase 6 of the lifecycle',
    prompt_file: 'skills/phase_06_quality_security/SKILL.md',
    timeout_ms: 1800000, // 30 minutes
    max_retries: 2
  },
  phase_07_deployment_release: {
    name: 'Phase 7: Deployment & Release Agent',
    description: 'Executes Phase 7 of the lifecycle',
    prompt_file: 'skills/phase_07_deployment_release/SKILL.md',
    timeout_ms: 1200000, // 20 minutes
    max_retries: 1
  },
  phase_08_operations_maintenance: {
    name: 'Phase 8: Operations & Maintenance Agent',
    description: 'Executes Phase 8 of the lifecycle',
    prompt_file: 'skills/phase_08_operations_maintenance/SKILL.md',
    timeout_ms: 900000, // 15 minutes
    max_retries: 2
  }
};

// Active agent tracking
let activeAgents = new Map();
const agentStatePath = '.claude/agents/active-agents.json';

/**
 * Load active agent state
 */
function loadAgentState() {
  if (existsSync(agentStatePath)) {
    try {
      return JSON.parse(readFileSync(agentStatePath, 'utf-8'));
    } catch (e) {
      return { active_agents: [], completed_agents: [], orphaned_agents: [] };
    }
  }
  return { active_agents: [], completed_agents: [], orphaned_agents: [] };
}

/**
 * Save active agent state
 */
function saveAgentState(state) {
  const dir = dirname(agentStatePath);
  if (!existsSync(dir)) {
    mkdirSync(dir, { recursive: true });
  }
  writeFileSync(agentStatePath, JSON.stringify(state, null, 2));
}

/**
 * Spawn an agent
 */
async function spawnAgent(agentType, context = {}, options = {}) {
  const agentConfig = AGENTS[agentType];
  if (!agentConfig) {
    return {
      success: false,
      error: `Unknown agent type: ${agentType}`,
      available_agents: Object.keys(AGENTS)
    };
  }

  // Check if agent's prompt file exists
  const promptFile = join(process.cwd(), agentConfig.prompt_file);
  if (!existsSync(promptFile)) {
    return {
      success: false,
      error: `Agent prompt file not found: ${agentConfig.prompt_file}`
    };
  }

  // Generate agent ID
  const agentId = `${agentType}-${Date.now()}`;
  const spawnedAt = Date.now();

  // Create agent record
  const agentRecord = {
    id: agentId,
    type: agentType,
    name: agentConfig.name,
    description: agentConfig.description,
    spawned_at: spawnedAt,
    spawned_by: options.parent_agent || 'user',
    context: context,
    timeout_ms: options.timeout_ms || agentConfig.timeout_ms,
    status: 'spawning',
    retry_count: 0
  };

  // Add to active agents
  const state = loadAgentState();
  state.active_agents.push(agentRecord);
  saveAgentState(state);
  activeAgents.set(agentId, agentRecord);

  // Set timeout for orphan detection
  const timeoutMs = agentRecord.timeout_ms;
  const timeoutId = setTimeout(() => {
    handleAgentTimeout(agentId);
  }, timeoutMs);

  agentRecord.timeout_id = timeoutId;

  return {
    success: true,
    agent: agentRecord,
    prompt_file: agentConfig.prompt_file,
    message: `Agent ${agentType} spawned successfully`,
    next_steps: [
      'Load the agent prompt file',
      'Execute the agent with the provided context',
      'Call agentComplete() when done',
      `Agent will timeout after ${timeoutMs}ms if no response`
    ]
  };
}

/**
 * Mark agent as complete
 */
function agentComplete(agentId, result = {}) {
  const agent = activeAgents.get(agentId);
  if (!agent) {
    // Check if it's in persisted state
    const state = loadAgentState();
    const persistedAgent = state.active_agents.find(a => a.id === agentId);

    if (!persistedAgent) {
      return { success: false, error: `Agent not found: ${agentId}` };
    }

    // Clear timeout if exists
    if (persistedAgent.timeout_id) {
      clearTimeout(persistedAgent.timeout_id);
    }

    // Move to completed
    state.active_agents = state.active_agents.filter(a => a.id !== agentId);
    persistedAgent.status = 'completed';
    persistedAgent.completed_at = Date.now();
    persistedAgent.result = result;
    state.completed_agents.push(persistedAgent);
    saveAgentState(state);

    return { success: true, agent: persistedAgent };
  }

  // Clear timeout
  if (agent.timeout_id) {
    clearTimeout(agent.timeout_id);
  }

  // Update agent record
  agent.status = 'completed';
  agent.completed_at = Date.now();
  agent.result = result;
  agent.duration_ms = agent.completed_at - agent.spawned_at;

  // Update state
  const state = loadAgentState();
  state.active_agents = state.active_agents.filter(a => a.id !== agentId);
  state.completed_agents.push(agent);
  saveAgentState(state);

  activeAgents.delete(agentId);

  return { success: true, agent };
}

/**
 * Handle agent timeout
 */
function handleAgentTimeout(agentId) {
  const agent = activeAgents.get(agentId);
  if (!agent) {
    return;
  }

  // Mark as orphaned
  agent.status = 'orphaned';
  agent.orphaned_at = Date.now();
  agent.orphan_reason = 'timeout';

  // Update state
  const state = loadAgentState();
  state.active_agents = state.active_agents.filter(a => a.id !== agentId);
  state.orphaned_agents.push(agent);
  saveAgentState(state);

  activeAgents.delete(agentId);

  console.error(`[AGENT TIMEOUT] Agent ${agentId} (${agent.type}) timed out after ${agent.timeout_ms}ms`);
}

/**
 * Mark agent as failed
 */
function agentFailed(agentId, error, retryable = false) {
  const agent = activeAgents.get(agentId);
  if (!agent) {
    return { success: false, error: `Agent not found: ${agentId}` };
  }

  const agentConfig = AGENTS[agent.type];

  // Check if we should retry
  if (retryable && agent.retry_count < agentConfig.max_retries) {
    agent.retry_count++;
    agent.status = 'retrying';
    agent.last_error = error;

    // Reset timeout
    if (agent.timeout_id) {
      clearTimeout(agent.timeout_id);
    }
    agent.timeout_id = setTimeout(() => {
      handleAgentTimeout(agentId);
    }, agent.timeout_ms);

    return {
      success: true,
      agent,
      retry: true,
      retry_count: agent.retry_count,
      max_retries: agentConfig.max_retries
    };
  }

  // Mark as failed (no more retries)
  if (agent.timeout_id) {
    clearTimeout(agent.timeout_id);
  }

  agent.status = 'failed';
  agent.failed_at = Date.now();
  agent.error = error;
  agent.duration_ms = agent.failed_at - agent.spawned_at;

  // Update state
  const state = loadAgentState();
  state.active_agents = state.active_agents.filter(a => a.id !== agentId);
  state.completed_agents.push(agent);
  saveAgentState(state);

  activeAgents.delete(agentId);

  return { success: true, agent, retry: false };
}

/**
 * Get all active agents
 */
function getActiveAgents() {
  const state = loadAgentState();
  return state.active_agents;
}

/**
 * Get all orphaned agents
 */
function getOrphanedAgents() {
  const state = loadAgentState();
  return state.orphaned_agents;
}

/**
 * Get completed agents
 */
function getCompletedAgents() {
  const state = loadAgentState();
  return state.completed_agents;
}

/**
 * Recover orphaned agent
 */
function recoverAgent(agentId, recoveryAction = 'terminate') {
  const state = loadAgentState();
  const orphanIndex = state.orphaned_agents.findIndex(a => a.id === agentId);

  if (orphanIndex === -1) {
    return { success: false, error: `Orphaned agent not found: ${agentId}` };
  }

  const orphan = state.orphaned_agents[orphanIndex];

  if (recoveryAction === 'terminate') {
    // Remove from orphans and add to completed with failed status
    state.orphaned_agents.splice(orphanIndex, 1);
    orphan.status = 'terminated';
    orphan.recovered_at = Date.now();
    orphan.recovery_action = 'terminated';
    state.completed_agents.push(orphan);
    saveAgentState(state);

    return { success: true, agent: orphan, action: 'terminated' };
  } else if (recoveryAction === 'retry') {
    // Move back to active
    state.orphaned_agents.splice(orphanIndex, 1);
    orphan.status = 'active';
    orphan.recovered_at = Date.now();
    orphan.recovery_action = 'retry';
    orphan.retry_count++;
    state.active_agents.push(orphan);

    // Set new timeout
    const timeoutId = setTimeout(() => {
      handleAgentTimeout(agentId);
    }, orphan.timeout_ms);
    orphan.timeout_id = timeoutId;

    activeAgents.set(agentId, orphan);
    saveAgentState(state);

    return { success: true, agent: orphan, action: 'retry' };
  }

  return { success: false, error: `Unknown recovery action: ${recoveryAction}` };
}

/**
 * Check for stale agents (should be called periodically)
 */
function checkStaleAgents() {
  const state = loadAgentState();
  const now = Date.now();
  const staleAgents = [];

  for (const agent of state.active_agents) {
    const elapsed = now - agent.spawned_at;
    if (elapsed > agent.timeout_ms * 2) {
      // Agent is way past timeout (double the timeout)
      staleAgents.push({
        ...agent,
        stale_reason: 'exceeded_double_timeout',
        elapsed_ms: elapsed,
        timeout_ms: agent.timeout_ms
      });
    }
  }

  return { stale_agents, active_count: state.active_agents.length };
}

/**
 * Cleanup old completed agents
 */
function cleanupOldCompletedAgents(olderThanDays = 7) {
  const state = loadAgentState();
  const cutoffTime = Date.now() - (olderThanDays * 24 * 60 * 60 * 1000);

  const oldCount = state.completed_agents.length;
  state.completed_agents = state.completed_agents.filter(a => {
    return a.completed_at && a.completed_at > cutoffTime;
  });

  const removedCount = oldCount - state.completed_agents.length;
  saveAgentState(state);

  return { removed_count: removedCount, remaining_count: state.completed_agents.length };
}

// CLI interface
if (import.meta.url === `file://${process.argv[1]}`) {
  const args = process.argv.slice(2);
  const command = args[0];

  switch (command) {
    case 'spawn': {
      const agentType = args[1];
      const contextJson = args[2] || '{}';
      const context = JSON.parse(contextJson);
      const result = await spawnAgent(agentType, context);
      console.log(JSON.stringify(result, null, 2));
      process.exit(result.success ? 0 : 1);
    }

    case 'complete': {
      const agentId = args[1];
      const resultJson = args[2] || '{}';
      const result = JSON.parse(resultJson);
      const completeResult = agentComplete(agentId, result);
      console.log(JSON.stringify(completeResult, null, 2));
      process.exit(completeResult.success ? 0 : 1);
    }

    case 'fail': {
      const agentId = args[1];
      const error = args[2] || 'Unknown error';
      const retryable = args[3] === 'true';
      const failResult = agentFailed(agentId, error, retryable);
      console.log(JSON.stringify(failResult, null, 2));
      process.exit(0);
    }

    case 'list-active': {
      const agents = getActiveAgents();
      console.log(JSON.stringify(agents, null, 2));
      process.exit(0);
    }

    case 'list-orphaned': {
      const agents = getOrphanedAgents();
      console.log(JSON.stringify(agents, null, 2));
      process.exit(0);
    }

    case 'list-completed': {
      const agents = getCompletedAgents();
      console.log(JSON.stringify(agents, null, 2));
      process.exit(0);
    }

    case 'recover': {
      const agentId = args[1];
      const action = args[2] || 'terminate';
      const result = recoverAgent(agentId, action);
      console.log(JSON.stringify(result, null, 2));
      process.exit(result.success ? 0 : 1);
    }

    case 'check-stale': {
      const result = checkStaleAgents();
      console.log(JSON.stringify(result, null, 2));
      process.exit(result.stale_agents.length > 0 ? 1 : 0);
    }

    case 'cleanup': {
      const days = parseInt(args[1]) || 7;
      const result = cleanupOldCompletedAgents(days);
      console.log(JSON.stringify(result, null, 2));
      process.exit(0);
    }

    case 'list-agents': {
      console.log(JSON.stringify(AGENTS, null, 2));
      process.exit(0);
    }

    default:
      console.error(JSON.stringify({
        error: 'Unknown command',
        usage: 'agent-spawner.js <command> [args...]',
        commands: [
          'spawn <agentType> [contextJson]',
          'complete <agentId> [resultJson]',
          'fail <agentId> <error> [retryable=true|false]',
          'list-active',
          'list-orphaned',
          'list-completed',
          'recover <agentId> [terminate|retry]',
          'check-stale',
          'cleanup [days]',
          'list-agents'
        ]
      }, null, 2));
      process.exit(1);
  }
}

export {
  spawnAgent,
  agentComplete,
  agentFailed,
  getActiveAgents,
  getOrphanedAgents,
  getCompletedAgents,
  recoverAgent,
  checkStaleAgents,
  cleanupOldCompletedAgents,
  AGENTS
};
