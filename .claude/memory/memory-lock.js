#!/usr/bin/env node

/**
 * Memory Lock Manager
 * Provides locking mechanism for concurrent memory access
 *
 * This is the CRITICAL component that prevents:
 * - RF-004: Memory race conditions
 */

import { readFileSync, writeFileSync, existsSync, mkdirSync, unlinkSync } from 'fs';
import { join, dirname } from 'path';

const LOCK_DIR = '.claude/memory/locks';
const LOCK_TIMEOUT_MS = 30000; // 30 seconds

/**
 * Acquire a lock on a memory file
 */
function acquireLock(memoryKey, requester, timeoutMs = LOCK_TIMEOUT_MS) {
  const lockDir = LOCK_DIR;
  if (!existsSync(lockDir)) {
    mkdirSync(lockDir, { recursive: true });
  }

  const lockFile = join(lockDir, `${memoryKey}.lock`);
  const lockInfo = {
    key: memoryKey,
    acquired_by: requester,
    acquired_at: new Date().toISOString(),
    timeout_ms: timeoutMs,
    expires_at: new Date(Date.now() + timeoutMs).toISOString()
  };

  // Check if lock already exists
  if (existsSync(lockFile)) {
    try {
      const existingLock = JSON.parse(readFileSync(lockFile, 'utf-8'));
      const expiresAt = new Date(existingLock.expires_at).getTime();
      const now = Date.now();

      // Check if lock has expired
      if (now < expiresAt) {
        return {
          success: false,
          error: 'Lock already held',
          held_by: existingLock.acquired_by,
          expires_at: existingLock.expires_at
        };
      } else {
        // Lock expired, remove it
        unlinkSync(lockFile);
      }
    } catch (e) {
      // Corrupt lock file, remove it
      try {
        unlinkSync(lockFile);
      } catch (e2) {
        // Ignore
      }
    }
  }

  // Create lock file
  try {
    writeFileSync(lockFile, JSON.stringify(lockInfo, null, 2));
    return { success: true, lock: lockInfo };
  } catch (e) {
    return {
      success: false,
      error: 'Failed to create lock file',
      details: e.message
    };
  }
}

/**
 * Release a lock
 */
function releaseLock(memoryKey, requester) {
  const lockFile = join(LOCK_DIR, `${memoryKey}.lock`);

  if (!existsSync(lockFile)) {
    return { success: false, error: 'Lock not found' };
  }

  try {
    const lockInfo = JSON.parse(readFileSync(lockFile, 'utf-8'));

    // Verify the requester owns the lock
    if (lockInfo.acquired_by !== requester) {
      return {
        success: false,
        error: 'Lock held by another requester',
        held_by: lockInfo.acquired_by,
        requested_by: requester
      };
    }

    unlinkSync(lockFile);
    return { success: true, released: true };
  } catch (e) {
    return {
      success: false,
      error: 'Failed to release lock',
      details: e.message
    };
  }
}

/**
 * Force release a lock (for recovery)
 */
function forceReleaseLock(memoryKey, requester) {
  const lockFile = join(LOCK_DIR, `${memoryKey}.lock`);

  if (!existsSync(lockFile)) {
    return { success: false, error: 'Lock not found' };
  }

  try {
    unlinkSync(lockFile);
    return {
      success: true,
      released: true,
      forced_by: requester,
      message: 'Lock force released'
    };
  } catch (e) {
    return {
      success: false,
      error: 'Failed to force release lock',
      details: e.message
    };
  }
}

/**
 * Check lock status
 */
function checkLock(memoryKey) {
  const lockFile = join(LOCK_DIR, `${memoryKey}.lock`);

  if (!existsSync(lockFile)) {
    return { locked: false };
  }

  try {
    const lockInfo = JSON.parse(readFileSync(lockFile, 'utf-8'));
    const expiresAt = new Date(lockInfo.expires_at).getTime();
    const now = Date.now();
    const expired = now >= expiresAt;

    return {
      locked: !expired,
      lock_info: lockInfo,
      expired: expired,
      time_until_expiry_ms: expired ? 0 : expiresAt - now
    };
  } catch (e) {
    return {
      locked: false,
      error: 'Failed to read lock',
      details: e.message
    };
  }
}

/**
 * List all active locks
 */
function listLocks() {
  const lockDir = LOCK_DIR;
  if (!existsSync(lockDir)) {
    return { locks: [] };
  }

  const { readdirSync } = require('fs');
  const locks = [];

  try {
    const files = readdirSync(lockDir);
    for (const file of files) {
      if (file.endsWith('.lock')) {
        const lockFile = join(lockDir, file);
        try {
          const lockInfo = JSON.parse(readFileSync(lockFile, 'utf-8'));
          const expiresAt = new Date(lockInfo.expires_at).getTime();
          const now = Date.now();
          const expired = now >= expiresAt;

          locks.push({
            key: lockInfo.key,
            acquired_by: lockInfo.acquired_by,
            acquired_at: lockInfo.acquired_at,
            expires_at: lockInfo.expires_at,
            expired: expired,
            time_until_expiry_ms: expired ? 0 : expiresAt - now
          });
        } catch (e) {
          // Invalid lock file
          locks.push({
            file: file,
            error: 'Invalid lock file',
            details: e.message
          });
        }
      }
    }
  } catch (e) {
    return {
      error: 'Failed to list locks',
      details: e.message
    };
  }

  return { locks };
}

/**
 * Clean up expired locks
 */
function cleanupExpiredLocks() {
  const lockDir = LOCK_DIR;
  if (!existsSync(lockDir)) {
    return { cleaned: 0, locks: [] };
  }

  const { readdirSync, unlinkSync } = require('fs');
  const cleaned = [];
  const now = Date.now();

  try {
    const files = readdirSync(lockDir);
    for (const file of files) {
      if (file.endsWith('.lock')) {
        const lockFile = join(lockDir, file);
        try {
          const lockInfo = JSON.parse(readFileSync(lockFile, 'utf-8'));
          const expiresAt = new Date(lockInfo.expires_at).getTime();

          if (now >= expiresAt) {
            // Lock expired, remove it
            unlinkSync(lockFile);
            cleaned.push({
              key: lockInfo.key,
              acquired_by: lockInfo.acquired_by,
              expired_at: new Date(expiresAt).toISOString()
            });
          }
        } catch (e) {
          // Invalid lock file, remove it
          try {
            unlinkSync(lockFile);
            cleaned.push({
              file: file,
              error: 'Invalid lock file removed'
            });
          } catch (e2) {
            // Ignore
          }
        }
      }
    }
  } catch (e) {
    return {
      error: 'Failed to cleanup locks',
      details: e.message
    };
  }

  return { cleaned_count: cleaned.length, cleaned };
}

/**
 * Execute a function with lock held
 */
async function withLock(memoryKey, requester, fn, timeoutMs = LOCK_TIMEOUT_MS) {
  // Acquire lock
  const acquireResult = acquireLock(memoryKey, requester, timeoutMs);
  if (!acquireResult.success) {
    throw new Error(`Failed to acquire lock: ${acquireResult.error}`);
  }

  try {
    // Execute function
    const result = await fn();

    // Release lock
    releaseLock(memoryKey, requester);

    return result;
  } catch (error) {
    // Release lock even if function fails
    try {
      releaseLock(memoryKey, requester);
    } catch (e) {
      // Ignore release errors
    }

    throw error;
  }
}

// CLI interface
if (import.meta.url === `file://${process.argv[1]}`) {
  const args = process.argv.slice(2);
  const command = args[0];

  switch (command) {
    case 'acquire': {
      const memoryKey = args[1];
      const requester = args[2];
      const timeout = parseInt(args[3]) || LOCK_TIMEOUT_MS;
      const result = acquireLock(memoryKey, requester, timeout);
      console.log(JSON.stringify(result, null, 2));
      process.exit(result.success ? 0 : 1);
    }

    case 'release': {
      const memoryKey = args[1];
      const requester = args[2];
      const result = releaseLock(memoryKey, requester);
      console.log(JSON.stringify(result, null, 2));
      process.exit(result.success ? 0 : 1);
    }

    case 'force-release': {
      const memoryKey = args[1];
      const requester = args[2];
      const result = forceReleaseLock(memoryKey, requester);
      console.log(JSON.stringify(result, null, 2));
      process.exit(result.success ? 0 : 1);
    }

    case 'check': {
      const memoryKey = args[1];
      const result = checkLock(memoryKey);
      console.log(JSON.stringify(result, null, 2));
      process.exit(0);
    }

    case 'list': {
      const result = listLocks();
      console.log(JSON.stringify(result, null, 2));
      process.exit(0);
    }

    case 'cleanup': {
      const result = cleanupExpiredLocks();
      console.log(JSON.stringify(result, null, 2));
      process.exit(0);
    }

    default:
      console.error(JSON.stringify({
        error: 'Unknown command',
        usage: 'memory-lock.js <command> [args...]',
        commands: [
          'acquire <memoryKey> <requester> [timeoutMs]',
          'release <memoryKey> <requester>',
          'force-release <memoryKey> <requester>',
          'check <memoryKey>',
          'list',
          'cleanup'
        ]
      }, null, 2));
      process.exit(1);
  }
}

export {
  acquireLock,
  releaseLock,
  forceReleaseLock,
  checkLock,
  listLocks,
  cleanupExpiredLocks,
  withLock
};
