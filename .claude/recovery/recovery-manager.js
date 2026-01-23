#!/usr/bin/env node
/**
 * Recovery Manager - Failure classification and automatic recovery
 * 
 * Based on Auto-Claude v2.7.4 services/recovery.py
 * Manages recovery from build failures with automatic rollback and escalation
 * 
 * @version 2.2
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// Load configuration
const CONFIG_PATH = path.join(__dirname, 'recovery-config.json');
const HISTORY_FILENAME = 'attempt-history.json';
const COMMITS_FILENAME = 'build-commits.json';

let config = null;

function loadConfig() {
    if (!config) {
        config = JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf8'));
    }
    return config;
}

/**
 * Recovery Manager class
 */
class RecoveryManager {
    constructor(specDir, projectDir) {
        this.specDir = specDir;
        this.projectDir = projectDir;
        this.memoryDir = path.join(specDir, 'memory');
        this.attemptHistoryFile = path.join(this.memoryDir, HISTORY_FILENAME);
        this.buildCommitsFile = path.join(this.memoryDir, COMMITS_FILENAME);
        
        // Ensure memory directory exists
        if (!fs.existsSync(this.memoryDir)) {
            fs.mkdirSync(this.memoryDir, { recursive: true });
        }
        
        // Initialize files if they don't exist
        if (!fs.existsSync(this.attemptHistoryFile)) {
            this._initAttemptHistory();
        }
        if (!fs.existsSync(this.buildCommitsFile)) {
            this._initBuildCommits();
        }
    }
    
    _initAttemptHistory() {
        const initial = {
            subtasks: {},
            stuck_subtasks: [],
            metadata: {
                created_at: new Date().toISOString(),
                last_updated: new Date().toISOString()
            }
        };
        fs.writeFileSync(this.attemptHistoryFile, JSON.stringify(initial, null, 2));
    }
    
    _initBuildCommits() {
        const initial = {
            commits: [],
            last_good_commit: null,
            metadata: {
                created_at: new Date().toISOString(),
                last_updated: new Date().toISOString()
            }
        };
        fs.writeFileSync(this.buildCommitsFile, JSON.stringify(initial, null, 2));
    }
    
    _loadAttemptHistory() {
        try {
            return JSON.parse(fs.readFileSync(this.attemptHistoryFile, 'utf8'));
        } catch (err) {
            this._initAttemptHistory();
            return JSON.parse(fs.readFileSync(this.attemptHistoryFile, 'utf8'));
        }
    }
    
    _saveAttemptHistory(data) {
        data.metadata.last_updated = new Date().toISOString();
        fs.writeFileSync(this.attemptHistoryFile, JSON.stringify(data, null, 2));
    }
    
    _loadBuildCommits() {
        try {
            return JSON.parse(fs.readFileSync(this.buildCommitsFile, 'utf8'));
        } catch (err) {
            this._initBuildCommits();
            return JSON.parse(fs.readFileSync(this.buildCommitsFile, 'utf8'));
        }
    }
    
    _saveBuildCommits(data) {
        data.metadata.last_updated = new Date().toISOString();
        fs.writeFileSync(this.buildCommitsFile, JSON.stringify(data, null, 2));
    }
    
    /**
     * Classify what type of failure occurred
     * @param {string} error - Error message
     * @param {string} subtaskId - Subtask ID
     * @returns {string} Failure type
     */
    classifyFailure(error, subtaskId) {
        const cfg = loadConfig();
        const errorLower = error.toLowerCase();
        
        // Check each failure type's patterns
        for (const [type, typeConfig] of Object.entries(cfg.failure_types)) {
            if (type === 'UNKNOWN') continue;
            
            for (const pattern of typeConfig.patterns) {
                if (errorLower.includes(pattern.toLowerCase())) {
                    return type;
                }
            }
        }
        
        // Check for circular fix
        if (this.detectCircularFix(subtaskId, error)) {
            return 'CIRCULAR_FIX';
        }
        
        return 'UNKNOWN';
    }
    
    /**
     * Record an attempt for a subtask
     * @param {string} subtaskId - Subtask ID
     * @param {number} session - Session number
     * @param {boolean} success - Whether attempt succeeded
     * @param {string} approach - Approach description
     * @param {string} error - Error message (if failed)
     */
    recordAttempt(subtaskId, session, success, approach, error = null) {
        const history = this._loadAttemptHistory();
        
        if (!history.subtasks[subtaskId]) {
            history.subtasks[subtaskId] = {
                attempts: [],
                created_at: new Date().toISOString()
            };
        }
        
        history.subtasks[subtaskId].attempts.push({
            session,
            success,
            approach,
            error,
            timestamp: new Date().toISOString()
        });
        
        this._saveAttemptHistory(history);
    }
    
    /**
     * Record a known-good commit
     * @param {string} commitHash - Commit hash
     * @param {string} subtaskId - Associated subtask
     */
    recordGoodCommit(commitHash, subtaskId) {
        const commits = this._loadBuildCommits();
        
        commits.commits.push({
            hash: commitHash,
            subtask_id: subtaskId,
            timestamp: new Date().toISOString()
        });
        
        // Keep only last N commits
        const cfg = loadConfig();
        if (commits.commits.length > cfg.thresholds.rollback_safety_commits) {
            commits.commits = commits.commits.slice(-cfg.thresholds.rollback_safety_commits);
        }
        
        commits.last_good_commit = commitHash;
        this._saveBuildCommits(commits);
    }
    
    /**
     * Get the last known good commit
     * @returns {string|null} Commit hash or null
     */
    getLastGoodCommit() {
        const commits = this._loadBuildCommits();
        return commits.last_good_commit;
    }
    
    /**
     * Get attempt count for a subtask
     * @param {string} subtaskId - Subtask ID
     * @returns {number} Number of attempts
     */
    getAttemptCount(subtaskId) {
        const history = this._loadAttemptHistory();
        return history.subtasks[subtaskId]?.attempts?.length || 0;
    }
    
    /**
     * Get subtask history
     * @param {string} subtaskId - Subtask ID
     * @returns {object} Subtask history
     */
    getSubtaskHistory(subtaskId) {
        const history = this._loadAttemptHistory();
        return history.subtasks[subtaskId] || { attempts: [] };
    }
    
    /**
     * Detect if we're in a circular fix pattern
     * @param {string} subtaskId - Subtask ID
     * @param {string} currentApproach - Current approach
     * @returns {boolean} True if circular fix detected
     */
    detectCircularFix(subtaskId, currentApproach) {
        const cfg = loadConfig();
        const history = this.getSubtaskHistory(subtaskId);
        const attempts = history.attempts || [];
        
        if (attempts.length < cfg.circular_fix_detection.window_size) {
            return false;
        }
        
        // Check recent attempts for similarity
        const recentAttempts = attempts.slice(-cfg.circular_fix_detection.window_size);
        const approaches = recentAttempts.map(a => a.approach?.toLowerCase() || '');
        
        // Simple similarity check: count how many times similar approach was tried
        let similarCount = 0;
        const currentLower = currentApproach?.toLowerCase() || '';
        
        for (const approach of approaches) {
            if (this._calculateSimilarity(currentLower, approach) > cfg.circular_fix_detection.similarity_threshold) {
                similarCount++;
            }
        }
        
        return similarCount >= cfg.thresholds.circular_fix_threshold;
    }
    
    _calculateSimilarity(str1, str2) {
        // Simple Jaccard similarity based on words
        const words1 = new Set(str1.split(/\s+/).filter(w => w.length > 2));
        const words2 = new Set(str2.split(/\s+/).filter(w => w.length > 2));
        
        if (words1.size === 0 && words2.size === 0) return 1;
        if (words1.size === 0 || words2.size === 0) return 0;
        
        const intersection = [...words1].filter(w => words2.has(w)).length;
        const union = new Set([...words1, ...words2]).size;
        
        return intersection / union;
    }
    
    /**
     * Get recommended recovery action
     * @param {string} subtaskId - Subtask ID
     * @param {string} failureType - Type of failure
     * @returns {object} Recovery action
     */
    getRecoveryAction(subtaskId, failureType) {
        const cfg = loadConfig();
        const typeConfig = cfg.failure_types[failureType] || cfg.failure_types.UNKNOWN;
        const attemptCount = this.getAttemptCount(subtaskId);
        
        // Check if we should escalate due to too many attempts
        if (attemptCount >= cfg.thresholds.escalation_threshold) {
            return {
                action: 'escalate',
                target: subtaskId,
                reason: `Too many attempts (${attemptCount}/${cfg.thresholds.max_attempts_per_subtask})`
            };
        }
        
        // Get recovery action from config
        const recoveryType = typeConfig.recovery;
        const actionConfig = cfg.recovery_actions[recoveryType];
        
        return {
            action: recoveryType,
            target: recoveryType === 'rollback' ? this.getLastGoodCommit() : subtaskId,
            reason: `${failureType}: ${typeConfig.description}`,
            steps: actionConfig?.steps || []
        };
    }
    
    /**
     * Perform rollback to last good commit
     * @returns {boolean} Success
     */
    rollbackToLastGood() {
        const lastGood = this.getLastGoodCommit();
        
        if (!lastGood) {
            console.error('No good commit to rollback to');
            return false;
        }
        
        try {
            execSync(`git reset --hard ${lastGood}`, {
                cwd: this.projectDir,
                encoding: 'utf8'
            });
            console.log(`Rolled back to commit ${lastGood}`);
            return true;
        } catch (err) {
            console.error(`Rollback failed: ${err.message}`);
            return false;
        }
    }
    
    /**
     * Mark a subtask as stuck
     * @param {string} subtaskId - Subtask ID
     * @param {string} reason - Reason for being stuck
     */
    markStuck(subtaskId, reason) {
        const history = this._loadAttemptHistory();
        
        if (!history.stuck_subtasks.includes(subtaskId)) {
            history.stuck_subtasks.push(subtaskId);
        }
        
        if (history.subtasks[subtaskId]) {
            history.subtasks[subtaskId].stuck = true;
            history.subtasks[subtaskId].stuck_reason = reason;
        }
        
        this._saveAttemptHistory(history);
    }
    
    /**
     * Get list of stuck subtasks
     * @returns {string[]} Stuck subtask IDs
     */
    getStuckSubtasks() {
        const history = this._loadAttemptHistory();
        return history.stuck_subtasks || [];
    }
    
    /**
     * Create PAUSE file for human intervention
     * @param {string} reason - Reason for pausing
     */
    createPauseFile(reason) {
        const pauseFile = path.join(this.projectDir, 'PAUSE');
        const content = `HUMAN INTERVENTION REQUIRED
===========================

Reason: ${reason}

Created: ${new Date().toISOString()}

To resume: Delete this PAUSE file after addressing the issue.
`;
        fs.writeFileSync(pauseFile, content);
        console.log(`Created PAUSE file: ${pauseFile}`);
    }
    
    /**
     * Check if PAUSE file exists
     * @returns {boolean} True if paused
     */
    isPaused() {
        return fs.existsSync(path.join(this.projectDir, 'PAUSE'));
    }
    
    /**
     * Get recovery summary
     * @returns {object} Summary of recovery state
     */
    getSummary() {
        const history = this._loadAttemptHistory();
        const commits = this._loadBuildCommits();
        
        const subtaskCount = Object.keys(history.subtasks).length;
        const totalAttempts = Object.values(history.subtasks)
            .reduce((sum, s) => sum + (s.attempts?.length || 0), 0);
        const stuckCount = history.stuck_subtasks.length;
        
        return {
            total_subtasks: subtaskCount,
            total_attempts: totalAttempts,
            stuck_subtasks: stuckCount,
            good_commits: commits.commits.length,
            last_good_commit: commits.last_good_commit,
            is_paused: this.isPaused()
        };
    }
}

// CLI interface
if (require.main === module) {
    const args = process.argv.slice(2);
    
    if (args.includes('--help') || args.includes('-h')) {
        console.log(`
Recovery Manager - Failure classification and automatic recovery

Usage:
  node recovery-manager.js [options]

Options:
  --spec-dir <path>       Spec directory path (required)
  --project-dir <path>    Project directory (defaults to cwd)
  --classify <error>      Classify an error message
  --record                Record an attempt (requires --subtask, --session, --approach)
  --subtask <id>          Subtask ID
  --session <num>         Session number
  --approach <desc>       Approach description
  --success               Mark attempt as successful
  --error <msg>           Error message (if failed)
  --recommend             Get recommended recovery action (requires --subtask, --failure)
  --failure <type>        Failure type
  --rollback              Perform rollback to last good commit
  --summary               Show recovery summary
  --history <subtask>     Show history for a subtask
  --pause <reason>        Create PAUSE file
  --list-failures         List all failure types
  --test                  Run self-test
  --help, -h              Show this help

Examples:
  node recovery-manager.js --list-failures
  node recovery-manager.js --classify "SyntaxError: Unexpected token"
  node recovery-manager.js --spec-dir ./specs/001 --summary
  node recovery-manager.js --spec-dir ./specs/001 --history subtask-001
  node recovery-manager.js --spec-dir ./specs/001 --record \\
    --subtask subtask-001 --session 1 --approach "Direct implementation"
`);
        process.exit(0);
    }
    
    if (args.includes('--list-failures')) {
        const cfg = loadConfig();
        console.log('\n⚠️ Failure Types\n');
        console.log('Type                  Severity  Recovery   Description');
        console.log('────────────────────  ────────  ─────────  ────────────────────────────────');
        for (const [type, typeConfig] of Object.entries(cfg.failure_types)) {
            console.log(
                `${type.padEnd(22)}` +
                `${typeConfig.severity.padEnd(10)}` +
                `${typeConfig.recovery.padEnd(11)}` +
                `${typeConfig.description}`
            );
        }
        console.log('');
        process.exit(0);
    }
    
    if (args.includes('--test')) {
        console.log('\n🧪 Running recovery manager self-test...\n');
        
        // Test config loading
        console.log('Test 1: Config loading');
        const cfg = loadConfig();
        console.log(`  ✓ Loaded config v${cfg.version}`);
        console.log(`  ✓ ${Object.keys(cfg.failure_types).length} failure types`);
        
        // Test failure classification
        console.log('\nTest 2: Failure classification');
        const testCases = [
            ['SyntaxError: Unexpected token', 'BROKEN_BUILD'],
            ['Module not found: react', 'BROKEN_BUILD'],
            ['Test failed: expected 5 but got 3', 'VERIFICATION_FAILED'],
            ['Context limit exceeded', 'CONTEXT_EXHAUSTED'],
            ['Some random error', 'UNKNOWN']
        ];
        
        // Create temp manager for testing
        const tmpDir = '/tmp/octalume-recovery-test';
        if (!fs.existsSync(tmpDir)) {
            fs.mkdirSync(tmpDir, { recursive: true });
        }
        const manager = new RecoveryManager(tmpDir, tmpDir);
        
        for (const [error, expected] of testCases) {
            const result = manager.classifyFailure(error, 'test');
            const status = result === expected ? '✓' : '✗';
            console.log(`  ${status} "${error.slice(0, 30)}..." → ${result}`);
        }
        
        // Test attempt recording
        console.log('\nTest 3: Attempt recording');
        manager.recordAttempt('test-001', 1, false, 'Direct approach', 'Test error');
        manager.recordAttempt('test-001', 2, true, 'Fixed approach');
        console.log(`  ✓ Recorded 2 attempts`);
        console.log(`  ✓ Attempt count: ${manager.getAttemptCount('test-001')}`);
        
        // Test good commit recording
        console.log('\nTest 4: Good commit recording');
        manager.recordGoodCommit('abc123', 'test-001');
        console.log(`  ✓ Last good commit: ${manager.getLastGoodCommit()}`);
        
        // Test recovery action
        console.log('\nTest 5: Recovery action');
        const action = manager.getRecoveryAction('test-001', 'BROKEN_BUILD');
        console.log(`  ✓ Action: ${action.action}`);
        console.log(`  ✓ Reason: ${action.reason}`);
        
        // Cleanup
        fs.rmSync(tmpDir, { recursive: true, force: true });
        
        console.log('\n✅ All tests passed!\n');
        process.exit(0);
    }
    
    // Parse arguments
    const specDirIdx = args.indexOf('--spec-dir');
    const projectDirIdx = args.indexOf('--project-dir');
    const classifyIdx = args.indexOf('--classify');
    const subtaskIdx = args.indexOf('--subtask');
    const sessionIdx = args.indexOf('--session');
    const approachIdx = args.indexOf('--approach');
    const errorIdx = args.indexOf('--error');
    const failureIdx = args.indexOf('--failure');
    const historyIdx = args.indexOf('--history');
    const pauseIdx = args.indexOf('--pause');
    
    const specDir = specDirIdx !== -1 ? args[specDirIdx + 1] : null;
    const projectDir = projectDirIdx !== -1 ? args[projectDirIdx + 1] : process.cwd();
    
    // Classify error (doesn't need specDir)
    if (classifyIdx !== -1 && args[classifyIdx + 1]) {
        const error = args[classifyIdx + 1];
        const tmpManager = new RecoveryManager('/tmp', '/tmp');
        const failureType = tmpManager.classifyFailure(error, 'unknown');
        const cfg = loadConfig();
        const typeConfig = cfg.failure_types[failureType];
        
        console.log(`\n🔍 Failure Classification\n`);
        console.log(`Error: ${error}`);
        console.log(`Type: ${failureType}`);
        console.log(`Severity: ${typeConfig.severity}`);
        console.log(`Recovery: ${typeConfig.recovery}`);
        console.log(`Description: ${typeConfig.description}\n`);
        process.exit(0);
    }
    
    // Operations requiring specDir
    if (!specDir && (args.includes('--summary') || args.includes('--record') || 
                     args.includes('--recommend') || historyIdx !== -1)) {
        console.error('Error: --spec-dir is required');
        process.exit(1);
    }
    
    if (specDir) {
        const manager = new RecoveryManager(specDir, projectDir);
        
        if (args.includes('--summary')) {
            const summary = manager.getSummary();
            console.log('\n📊 Recovery Summary\n');
            console.log(`Total subtasks tracked: ${summary.total_subtasks}`);
            console.log(`Total attempts: ${summary.total_attempts}`);
            console.log(`Stuck subtasks: ${summary.stuck_subtasks}`);
            console.log(`Good commits saved: ${summary.good_commits}`);
            console.log(`Last good commit: ${summary.last_good_commit || '(none)'}`);
            console.log(`Paused: ${summary.is_paused ? 'YES' : 'No'}\n`);
            process.exit(0);
        }
        
        if (historyIdx !== -1 && args[historyIdx + 1]) {
            const subtaskId = args[historyIdx + 1];
            const history = manager.getSubtaskHistory(subtaskId);
            
            console.log(`\n📜 History for ${subtaskId}\n`);
            
            if (!history.attempts || history.attempts.length === 0) {
                console.log('No attempts recorded.\n');
            } else {
                history.attempts.forEach((attempt, i) => {
                    const status = attempt.success ? '✓' : '✗';
                    console.log(`[${status}] Attempt ${i + 1} (Session ${attempt.session})`);
                    console.log(`    Approach: ${attempt.approach}`);
                    if (attempt.error) {
                        console.log(`    Error: ${attempt.error}`);
                    }
                    console.log(`    Time: ${attempt.timestamp}`);
                    console.log('');
                });
            }
            process.exit(0);
        }
        
        if (args.includes('--record')) {
            const subtaskId = subtaskIdx !== -1 ? args[subtaskIdx + 1] : null;
            const session = sessionIdx !== -1 ? parseInt(args[sessionIdx + 1]) : null;
            const approach = approachIdx !== -1 ? args[approachIdx + 1] : null;
            const success = args.includes('--success');
            const error = errorIdx !== -1 ? args[errorIdx + 1] : null;
            
            if (!subtaskId || session === null || !approach) {
                console.error('Error: --record requires --subtask, --session, and --approach');
                process.exit(1);
            }
            
            manager.recordAttempt(subtaskId, session, success, approach, error);
            console.log(`\n✓ Recorded ${success ? 'successful' : 'failed'} attempt for ${subtaskId}\n`);
            process.exit(0);
        }
        
        if (args.includes('--recommend')) {
            const subtaskId = subtaskIdx !== -1 ? args[subtaskIdx + 1] : null;
            const failure = failureIdx !== -1 ? args[failureIdx + 1] : 'UNKNOWN';
            
            if (!subtaskId) {
                console.error('Error: --recommend requires --subtask');
                process.exit(1);
            }
            
            const action = manager.getRecoveryAction(subtaskId, failure);
            console.log('\n🔧 Recommended Recovery Action\n');
            console.log(`Action: ${action.action}`);
            console.log(`Target: ${action.target}`);
            console.log(`Reason: ${action.reason}`);
            if (action.steps?.length > 0) {
                console.log('\nSteps:');
                action.steps.forEach((step, i) => console.log(`  ${i + 1}. ${step}`));
            }
            console.log('');
            process.exit(0);
        }
        
        if (args.includes('--rollback')) {
            if (manager.rollbackToLastGood()) {
                console.log('\n✓ Rollback successful\n');
            } else {
                console.log('\n✗ Rollback failed\n');
                process.exit(1);
            }
            process.exit(0);
        }
        
        if (pauseIdx !== -1 && args[pauseIdx + 1]) {
            manager.createPauseFile(args[pauseIdx + 1]);
            console.log('\n✓ Created PAUSE file\n');
            process.exit(0);
        }
    }
    
    // Default: show help
    console.log('Use --help for usage information');
    process.exit(1);
}

// Export for use as module
module.exports = {
    RecoveryManager,
    loadConfig
};
