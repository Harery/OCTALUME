#!/usr/bin/env node

/**
 * State Synchronization Manager
 * Synchronizes project-state.json and memory.json
 *
 * This is the CRITICAL component that prevents:
 * - RF-010: State desynchronization
 */

import { readFileSync, writeFileSync, existsSync } from 'fs';
import { join } from 'path';
import { acquireLock, releaseLock, withLock } from './memory-lock.js';

const PROJECT_STATE_PATH = '.claude/project-state.json';
const MEMORY_PATH = '.claude/memory/memory.json';
const SYNC_LOCK_KEY = 'state-sync';
const SYNC_REQUESTER = 'state-sync-manager';

/**
 * Synchronize memory decisions into project state
 */
function syncMemoryToProjectState(projectStatePath, memoryPath) {
  return withLock(SYNC_LOCK_KEY, SYNC_REQUESTER, () => {
    const projectState = JSON.parse(readFileSync(projectStatePath, 'utf-8'));
    const memory = JSON.parse(readFileSync(memoryPath, 'utf-8'));

    const syncResult = {
      synced_at: new Date().toISOString(),
      changes: []
    };

    // Sync decisions
    if (memory.memory?.decisions) {
      if (!projectState.decisions) {
        projectState.decisions = {};
        syncResult.changes.push({ type: 'initialized', field: 'decisions' });
      }

      for (const [key, value] of Object.entries(memory.memory.decisions)) {
        if (!projectState.decisions[key] ||
            JSON.stringify(projectState.decisions[key]) !== JSON.stringify(value)) {
          projectState.decisions[key] = value;
          syncResult.changes.push({
            type: 'synced',
            field: 'decisions',
            key: key,
            category: value.category,
            timestamp: value.timestamp
          });
        }
      }
    }

    // Sync blockers
    if (memory.memory?.blockers) {
      if (!projectState.blockers) {
        projectState.blockers = {};
        syncResult.changes.push({ type: 'initialized', field: 'blockers' });
      }

      const hasActiveBlockers = Object.keys(memory.memory.blockers).length > 0;
      const wasBlocked = projectState.phase_status === 'blocked';

      for (const [key, value] of Object.entries(memory.memory.blockers)) {
        if (!projectState.blockers[key] ||
            JSON.stringify(projectState.blockers[key]) !== JSON.stringify(value)) {
          projectState.blockers[key] = value;
          syncResult.changes.push({
            type: 'synced',
            field: 'blockers',
            key: key,
            category: value.category,
            timestamp: value.timestamp
          });
        }
      }

      // Update phase status based on blockers
      if (hasActiveBlockers && !wasBlocked) {
        projectState.phase_status = 'blocked';
        projectState.blocked_reason = 'memory_blockers';
        syncResult.changes.push({
          type: 'phase_status_changed',
          from: projectState.phase_status,
          to: 'blocked',
          reason: 'Active blockers in memory'
        });
      } else if (!hasActiveBlockers && wasBlocked && projectState.blocked_reason === 'memory_blockers') {
        projectState.phase_status = 'in_progress';
        projectState.blocked_reason = null;
        syncResult.changes.push({
          type: 'phase_status_changed',
          from: 'blocked',
          to: 'in_progress',
          reason: 'All blockers resolved'
        });
      }
    }

    // Sync progress
    if (memory.memory?.progress) {
      if (!projectState.memory_progress) {
        projectState.memory_progress = {};
        syncResult.changes.push({ type: 'initialized', field: 'memory_progress' });
      }

      for (const [key, value] of Object.entries(memory.memory.progress)) {
        if (!projectState.memory_progress[key] ||
            JSON.stringify(projectState.memory_progress[key]) !== JSON.stringify(value)) {
          projectState.memory_progress[key] = value;
          syncResult.changes.push({
            type: 'synced',
            field: 'progress',
            key: key,
            category: value.category,
            timestamp: value.timestamp
          });
        }
      }
    }

    // Update sync timestamp
    projectState.last_memory_sync = syncResult.synced_at;

    writeFileSync(projectStatePath, JSON.stringify(projectState, null, 2));

    return {
      success: true,
      sync_result: syncResult
    };
  });
}

/**
 * Synchronize project state into memory
 */
function syncProjectStateToMemory(projectStatePath, memoryPath) {
  return withLock(SYNC_LOCK_KEY, SYNC_REQUESTER, () => {
    const projectState = JSON.parse(readFileSync(projectStatePath, 'utf-8'));
    const memory = JSON.parse(readFileSync(memoryPath, 'utf-8'));

    const syncResult = {
      synced_at: new Date().toISOString(),
      changes: []
    };

    // Sync current phase
    if (projectState.current_phase) {
      const progressKey = `current-phase-${projectState.current_phase}`;
      if (!memory.memory?.progress?.[progressKey]) {
        if (!memory.memory.progress) {
          memory.memory.progress = {};
        }
        memory.memory.progress[progressKey] = {
          key: progressKey,
          value: projectState.current_phase,
          category: 'progress',
          timestamp: new Date().toISOString(),
          context: 'Current phase from project state'
        };
        syncResult.changes.push({
          type: 'synced',
          field: 'progress',
          key: progressKey,
          value: projectState.current_phase
        });
      }
    }

    // Sync phase status
    if (projectState.phase_status) {
      const statusKey = `phase-status-${projectState.current_phase}`;
      if (!memory.memory?.progress?.[statusKey]) {
        if (!memory.memory.progress) {
          memory.memory.progress = {};
        }
        memory.memory.progress[statusKey] = {
          key: statusKey,
          value: projectState.phase_status,
          category: 'progress',
          timestamp: new Date().toISOString(),
          context: `Phase ${projectState.current_phase} status`
        };
        syncResult.changes.push({
          type: 'synced',
          field: 'progress',
          key: statusKey,
          value: projectState.phase_status
        });
      }
    }

    // Sync completed phases
    if (projectState.completed_phases && projectState.completed_phases.length > 0) {
      for (const phase of projectState.completed_phases) {
        const progressKey = `phase-complete-${phase}`;
        if (!memory.memory?.progress?.[progressKey]) {
          if (!memory.memory.progress) {
            memory.memory.progress = {};
          }
          memory.memory.progress[progressKey] = {
            key: progressKey,
            value: 'complete',
            category: 'progress',
            timestamp: new Date().toISOString(),
            context: `Phase ${phase} completed`
          };
          syncResult.changes.push({
            type: 'synced',
            field: 'progress',
            key: progressKey,
            phase: phase
          });
        }
      }
    }

    // Update sync timestamp
    memory.last_project_state_sync = syncResult.synced_at;
    memory.updated_at = syncResult.synced_at;
    memory.statistics.total_entries = Object.keys(memory.memory.decisions).length +
                                        Object.keys(memory.memory.progress).length +
                                        Object.keys(memory.memory.blockers).length +
                                        Object.keys(memory.memory.notes).length;

    writeFileSync(memoryPath, JSON.stringify(memory, null, 2));

    return {
      success: true,
      sync_result: syncResult
    };
  });
}

/**
 * Bidirectional synchronization
 */
function syncBoth(projectStatePath, memoryPath) {
  return withLock(SYNC_LOCK_KEY, SYNC_REQUESTER, async () => {
    // First sync memory to project state
    const memToProjResult = await syncMemoryToProjectState(projectStatePath, memoryPath);

    // Then sync project state to memory
    const projToMemResult = await syncProjectStateToMemory(projectStatePath, memoryPath);

    return {
      success: true,
      memory_to_project_state: memToProjResult.sync_result,
      project_state_to_memory: projToMemResult.sync_result,
      total_changes: memToProjResult.sync_result.changes.length +
                     projToMemResult.sync_result.changes.length
    };
  });
}

/**
 * Check synchronization status
 */
function checkSyncStatus(projectStatePath, memoryPath) {
  const projectState = JSON.parse(readFileSync(projectStatePath, 'utf-8'));
  const memory = JSON.parse(readFileSync(memoryPath, 'utf-8'));

  const status = {
    project_state_last_sync: projectState.last_memory_sync || null,
    memory_last_sync: memory.last_project_state_sync || null,
    sync_difference_ms: null,
    needs_sync: false,
    issues: []
  };

  if (projectState.last_memory_sync && memory.last_project_state_sync) {
    const projSync = new Date(projectState.last_memory_sync).getTime();
    const memSync = new Date(memory.last_project_state_sync).getTime();
    status.sync_difference_ms = Math.abs(projSync - memSync);

    // If sync difference is more than 1 minute, sync is needed
    if (status.sync_difference_ms > 60000) {
      status.needs_sync = true;
      status.issues.push({
        severity: 'warning',
        message: 'Sync difference exceeds 1 minute',
        difference_ms: status.sync_difference_ms
      });
    }
  } else {
    status.needs_sync = true;
    status.issues.push({
      severity: 'error',
      message: 'No sync timestamp found'
    });
  }

  // Check for decision desynchronization
  if (projectState.decisions && memory.memory?.decisions) {
    const projDecisionKeys = Object.keys(projectState.decisions);
    const memDecisionKeys = Object.keys(memory.memory.decisions);

    const missingInMemory = projDecisionKeys.filter(k => !memDecisionKeys.includes(k));
    const missingInProject = memDecisionKeys.filter(k => !projDecisionKeys.includes(k));

    if (missingInMemory.length > 0) {
      status.needs_sync = true;
      status.issues.push({
        severity: 'warning',
        message: 'Decisions in project state not in memory',
        count: missingInMemory.length,
        keys: missingInMemory
      });
    }

    if (missingInProject.length > 0) {
      status.needs_sync = true;
      status.issues.push({
        severity: 'warning',
        message: 'Decisions in memory not in project state',
        count: missingInProject.length,
        keys: missingInProject
      });
    }
  }

  return status;
}

/**
 * Repair desynchronized state
 */
function repairState(projectStatePath, memoryPath) {
  return withLock(SYNC_LOCK_KEY, SYNC_REQUESTER, async () => {
    const syncStatus = checkSyncStatus(projectStatePath, memoryPath);
    const repairResult = {
      repaired_at: new Date().toISOString(),
      issues_found: syncStatus.issues.length,
      repairs: []
    };

    // Perform bidirectional sync to repair
    const syncResult = await syncBoth(projectStatePath, memoryPath);
    repairResult.repairs.push({
      action: 'bidirectional_sync',
      changes: syncResult.total_changes
    });

    // Verify repair
    const statusAfter = checkSyncStatus(projectStatePath, memoryPath);
    repairResult.issues_after = statusAfter.issues.length;
    repairResult.sync_needed_after = statusAfter.needs_sync;

    return {
      success: true,
      repair_result: repairResult
    };
  });
}

// CLI interface
if (import.meta.url === `file://${process.argv[1]}`) {
  const args = process.argv.slice(2);
  const command = args[0];

  const projectStatePath = args[1] || PROJECT_STATE_PATH;
  const memoryPath = args[2] || MEMORY_PATH;

  switch (command) {
    case 'sync-mem-to-proj': {
      const result = syncMemoryToProjectState(projectStatePath, memoryPath);
      console.log(JSON.stringify(await result, null, 2));
      process.exit(0);
    }

    case 'sync-proj-to-mem': {
      const result = syncProjectStateToMemory(projectStatePath, memoryPath);
      console.log(JSON.stringify(await result, null, 2));
      process.exit(0);
    }

    case 'sync': {
      const result = syncBoth(projectStatePath, memoryPath);
      console.log(JSON.stringify(await result, null, 2));
      process.exit(0);
    }

    case 'status': {
      const result = checkSyncStatus(projectStatePath, memoryPath);
      console.log(JSON.stringify(result, null, 2));
      process.exit(result.needs_sync ? 1 : 0);
    }

    case 'repair': {
      const result = repairState(projectStatePath, memoryPath);
      console.log(JSON.stringify(await result, null, 2));
      process.exit(0);
    }

    default:
      console.error(JSON.stringify({
        error: 'Unknown command',
        usage: 'state-sync.js <command> [project-state] [memory]',
        commands: [
          'sync-mem-to-proj',
          'sync-proj-to-mem',
          'sync',
          'status',
          'repair'
        ]
      }, null, 2));
      process.exit(1);
  }
}

export {
  syncMemoryToProjectState,
  syncProjectStateToMemory,
  syncBoth,
  checkSyncStatus,
  repairState
};
