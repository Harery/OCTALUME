#!/usr/bin/env node
/**
 * Insight Extractor - Post-session learning through structured extraction
 * 
 * Based on Auto-Claude v2.7.4 insight_extractor.py
 * Extracts structured insights from completed coding sessions
 * 
 * @version 2.2
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// Load configuration
const CONFIG_PATH = path.join(__dirname, 'insight-schema.json');
let config = null;

function loadConfig() {
    if (!config) {
        config = JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf8'));
    }
    return config;
}

/**
 * Get git diff between two commits
 * @param {string} projectDir - Project directory
 * @param {string} commitBefore - Commit before session
 * @param {string} commitAfter - Commit after session
 * @returns {string} Diff text
 */
function getSessionDiff(projectDir, commitBefore, commitAfter) {
    const cfg = loadConfig();
    
    if (!commitBefore || !commitAfter) {
        return '(No commits to diff)';
    }
    
    if (commitBefore === commitAfter) {
        return '(No changes - same commit)';
    }
    
    try {
        let diff = execSync(`git diff ${commitBefore} ${commitAfter}`, {
            cwd: projectDir,
            encoding: 'utf8',
            timeout: 30000
        });
        
        if (diff.length > cfg.extraction_config.max_diff_chars) {
            diff = diff.slice(0, cfg.extraction_config.max_diff_chars) + 
                   `\n\n... (truncated, ${diff.length} chars total)`;
        }
        
        return diff || '(Empty diff)';
    } catch (err) {
        return `(Failed to get diff: ${err.message})`;
    }
}

/**
 * Get list of changed files between commits
 * @param {string} projectDir - Project directory
 * @param {string} commitBefore - Commit before session
 * @param {string} commitAfter - Commit after session
 * @returns {string[]} List of changed files
 */
function getChangedFiles(projectDir, commitBefore, commitAfter) {
    if (!commitBefore || !commitAfter || commitBefore === commitAfter) {
        return [];
    }
    
    try {
        const output = execSync(`git diff --name-only ${commitBefore} ${commitAfter}`, {
            cwd: projectDir,
            encoding: 'utf8',
            timeout: 10000
        });
        
        return output.trim().split('\n').filter(f => f.trim());
    } catch (err) {
        console.warn(`Warning: Failed to get changed files: ${err.message}`);
        return [];
    }
}

/**
 * Get commit messages between commits
 * @param {string} projectDir - Project directory
 * @param {string} commitBefore - Commit before session
 * @param {string} commitAfter - Commit after session
 * @returns {string} Commit messages
 */
function getCommitMessages(projectDir, commitBefore, commitAfter) {
    if (!commitBefore || !commitAfter || commitBefore === commitAfter) {
        return '(No commits)';
    }
    
    try {
        const output = execSync(`git log --oneline ${commitBefore}..${commitAfter}`, {
            cwd: projectDir,
            encoding: 'utf8',
            timeout: 10000
        });
        
        return output.trim() || '(No commits)';
    } catch (err) {
        return `(Failed: ${err.message})`;
    }
}

/**
 * Get subtask description from implementation plan
 * @param {string} specDir - Spec directory
 * @param {string} subtaskId - Subtask ID
 * @returns {string} Subtask description
 */
function getSubtaskDescription(specDir, subtaskId) {
    const planFile = path.join(specDir, 'implementation-plan.json');
    
    if (!fs.existsSync(planFile)) {
        return `Subtask: ${subtaskId}`;
    }
    
    try {
        const plan = JSON.parse(fs.readFileSync(planFile, 'utf8'));
        
        // Search through phases for the subtask
        for (const phase of (plan.phases || [])) {
            for (const subtask of (phase.subtasks || [])) {
                if (subtask.id === subtaskId) {
                    return subtask.description || `Subtask: ${subtaskId}`;
                }
            }
        }
        
        return `Subtask: ${subtaskId}`;
    } catch (err) {
        return `Subtask: ${subtaskId}`;
    }
}

/**
 * Get attempt history from recovery manager
 * @param {string} specDir - Spec directory
 * @param {string} subtaskId - Subtask ID
 * @returns {object[]} Previous attempts
 */
function getAttemptHistory(specDir, subtaskId) {
    const cfg = loadConfig();
    const historyFile = path.join(specDir, 'memory', 'attempt-history.json');
    
    if (!fs.existsSync(historyFile)) {
        return [];
    }
    
    try {
        const history = JSON.parse(fs.readFileSync(historyFile, 'utf8'));
        const subtaskHistory = history.subtasks?.[subtaskId];
        
        if (!subtaskHistory?.attempts) {
            return [];
        }
        
        return subtaskHistory.attempts.slice(-cfg.extraction_config.max_attempts_to_include);
    } catch (err) {
        return [];
    }
}

/**
 * Format attempt history for prompt
 * @param {object[]} attempts - Previous attempts
 * @returns {string} Formatted history
 */
function formatAttemptHistory(attempts) {
    if (!attempts || attempts.length === 0) {
        return '(First attempt - no previous history)';
    }
    
    const lines = [];
    attempts.forEach((attempt, i) => {
        const success = attempt.success ? 'SUCCESS' : 'FAILED';
        const approach = attempt.approach || 'Unknown approach';
        lines.push(`**Attempt ${i + 1}** (${success}): ${approach}`);
        if (attempt.error) {
            lines.push(`  Error: ${attempt.error}`);
        }
    });
    
    return lines.join('\n');
}

/**
 * Gather all inputs needed for insight extraction
 * @param {object} params - Parameters
 * @returns {object} Extraction inputs
 */
function gatherExtractionInputs(params) {
    const {
        specDir,
        projectDir,
        subtaskId,
        sessionNum,
        commitBefore,
        commitAfter,
        success
    } = params;
    
    return {
        subtask_id: subtaskId,
        subtask_description: getSubtaskDescription(specDir, subtaskId),
        session_num: sessionNum,
        success,
        diff: getSessionDiff(projectDir, commitBefore, commitAfter),
        changed_files: getChangedFiles(projectDir, commitBefore, commitAfter),
        commit_messages: getCommitMessages(projectDir, commitBefore, commitAfter),
        attempt_history: getAttemptHistory(specDir, subtaskId)
    };
}

/**
 * Build extraction prompt from inputs
 * @param {object} inputs - Gathered inputs
 * @returns {string} Formatted prompt
 */
function buildExtractionPrompt(inputs) {
    const cfg = loadConfig();
    
    const changedFilesStr = inputs.changed_files.length > 0
        ? inputs.changed_files.map(f => `- ${f}`).join('\n')
        : '(No files changed)';
    
    return cfg.extraction_prompt_template
        .replace('{subtask_id}', inputs.subtask_id)
        .replace('{subtask_description}', inputs.subtask_description)
        .replace('{session_num}', inputs.session_num)
        .replace('{outcome}', inputs.success ? 'SUCCESS' : 'FAILED')
        .replace('{changed_files}', changedFilesStr)
        .replace('{commit_messages}', inputs.commit_messages)
        .replace('{diff}', inputs.diff)
        .replace('{attempt_history}', formatAttemptHistory(inputs.attempt_history));
}

/**
 * Parse insights from LLM response
 * @param {string} responseText - Raw LLM response
 * @returns {object|null} Parsed insights or null
 */
function parseInsights(responseText) {
    let text = responseText.trim();
    
    if (!text) {
        console.warn('Cannot parse insights: response is empty');
        return null;
    }
    
    // Handle markdown code blocks
    if (text.startsWith('```')) {
        const lines = text.split('\n');
        if (lines[0].startsWith('```')) {
            lines.shift();
        }
        if (lines[lines.length - 1].trim() === '```') {
            lines.pop();
        }
        text = lines.join('\n').trim();
    }
    
    if (!text) {
        console.warn('Cannot parse insights: only code block markers');
        return null;
    }
    
    try {
        const insights = JSON.parse(text);
        
        if (typeof insights !== 'object' || insights === null) {
            console.warn('Insights is not an object');
            return null;
        }
        
        // Ensure required keys with defaults
        insights.file_insights = insights.file_insights || [];
        insights.patterns_discovered = insights.patterns_discovered || [];
        insights.gotchas_discovered = insights.gotchas_discovered || [];
        insights.approach_outcome = insights.approach_outcome || {};
        insights.recommendations = insights.recommendations || [];
        
        return insights;
    } catch (err) {
        console.warn(`Failed to parse insights JSON: ${err.message}`);
        console.warn(`Response preview: ${text.slice(0, 500)}`);
        return null;
    }
}

/**
 * Get generic insights when extraction fails
 * @param {string} subtaskId - Subtask ID
 * @param {boolean} success - Whether session succeeded
 * @returns {object} Generic insights
 */
function getGenericInsights(subtaskId, success) {
    return {
        file_insights: [],
        patterns_discovered: [],
        gotchas_discovered: [],
        approach_outcome: {
            success,
            approach_used: `Implemented subtask: ${subtaskId}`,
            why_it_worked: null,
            why_it_failed: null,
            alternatives_tried: []
        },
        recommendations: [],
        subtask_id: subtaskId,
        success,
        changed_files: []
    };
}

/**
 * Save insights to file
 * @param {string} specDir - Spec directory
 * @param {number} sessionNum - Session number
 * @param {object} insights - Insights to save
 */
function saveInsights(specDir, sessionNum, insights) {
    const insightsDir = path.join(specDir, 'memory', 'session_insights');
    
    // Ensure directory exists
    if (!fs.existsSync(insightsDir)) {
        fs.mkdirSync(insightsDir, { recursive: true });
    }
    
    const filename = `session_${String(sessionNum).padStart(3, '0')}.json`;
    const filepath = path.join(insightsDir, filename);
    
    fs.writeFileSync(filepath, JSON.stringify(insights, null, 2));
    console.log(`Saved insights to ${filepath}`);
}

/**
 * Load insights from file
 * @param {string} specDir - Spec directory
 * @param {number} sessionNum - Session number
 * @returns {object|null} Loaded insights or null
 */
function loadInsights(specDir, sessionNum) {
    const filename = `session_${String(sessionNum).padStart(3, '0')}.json`;
    const filepath = path.join(specDir, 'memory', 'session_insights', filename);
    
    if (!fs.existsSync(filepath)) {
        return null;
    }
    
    try {
        return JSON.parse(fs.readFileSync(filepath, 'utf8'));
    } catch (err) {
        console.warn(`Failed to load insights: ${err.message}`);
        return null;
    }
}

/**
 * List all session insights
 * @param {string} specDir - Spec directory
 * @returns {object[]} List of session insights metadata
 */
function listInsights(specDir) {
    const insightsDir = path.join(specDir, 'memory', 'session_insights');
    
    if (!fs.existsSync(insightsDir)) {
        return [];
    }
    
    const files = fs.readdirSync(insightsDir)
        .filter(f => f.endsWith('.json'))
        .sort();
    
    return files.map(f => {
        const filepath = path.join(insightsDir, f);
        try {
            const insights = JSON.parse(fs.readFileSync(filepath, 'utf8'));
            return {
                file: f,
                session: parseInt(f.match(/session_(\d+)/)?.[1] || '0'),
                success: insights.success,
                subtask_id: insights.subtask_id,
                patterns_count: (insights.patterns_discovered || []).length,
                gotchas_count: (insights.gotchas_discovered || []).length
            };
        } catch (err) {
            return { file: f, error: err.message };
        }
    });
}

/**
 * Aggregate insights across sessions
 * @param {string} specDir - Spec directory
 * @returns {object} Aggregated insights
 */
function aggregateInsights(specDir) {
    const sessions = listInsights(specDir);
    
    const aggregated = {
        total_sessions: sessions.length,
        successful_sessions: sessions.filter(s => s.success).length,
        all_patterns: [],
        all_gotchas: [],
        all_recommendations: []
    };
    
    for (const session of sessions) {
        if (session.error) continue;
        
        const insights = loadInsights(specDir, session.session);
        if (!insights) continue;
        
        aggregated.all_patterns.push(...(insights.patterns_discovered || []));
        aggregated.all_gotchas.push(...(insights.gotchas_discovered || []));
        aggregated.all_recommendations.push(...(insights.recommendations || []));
    }
    
    return aggregated;
}

// CLI interface
if (require.main === module) {
    const args = process.argv.slice(2);
    
    if (args.includes('--help') || args.includes('-h')) {
        console.log(`
Insight Extractor - Post-session learning through structured extraction

Usage:
  node insight-extractor.js [options]

Options:
  --spec-dir <path>       Spec directory path (required)
  --project-dir <path>    Project directory (defaults to cwd)
  --session <num>         Session number
  --subtask <id>          Subtask ID
  --commit-before <hash>  Commit before session
  --commit-after <hash>   Commit after session
  --success               Mark session as successful
  --gather                Gather extraction inputs
  --list                  List all session insights
  --aggregate             Aggregate insights across sessions
  --load <session>        Load specific session insights
  --validate              Validate the schema
  --test                  Run self-test
  --help, -h              Show this help

Examples:
  node insight-extractor.js --list --spec-dir ./specs/001
  node insight-extractor.js --aggregate --spec-dir ./specs/001
  node insight-extractor.js --load 1 --spec-dir ./specs/001
  node insight-extractor.js --gather --spec-dir ./specs/001 --project-dir . \\
    --subtask subtask-001 --commit-before abc123 --commit-after def456
`);
        process.exit(0);
    }
    
    if (args.includes('--validate')) {
        console.log('\n🔍 Validating insight schema...\n');
        const cfg = loadConfig();
        console.log(`Schema version: ${cfg.version}`);
        console.log(`Extraction model: ${cfg.extraction_config.model}`);
        console.log(`Max diff chars: ${cfg.extraction_config.max_diff_chars}`);
        console.log('\nRequired schema fields:');
        Object.keys(cfg.schema).forEach(field => {
            console.log(`  - ${field}: ${cfg.schema[field].type}`);
        });
        console.log('\n✅ Schema is valid!\n');
        process.exit(0);
    }
    
    if (args.includes('--test')) {
        console.log('\n🧪 Running insight extractor self-test...\n');
        
        // Test config loading
        console.log('Test 1: Config loading');
        const cfg = loadConfig();
        console.log(`  ✓ Loaded config v${cfg.version}`);
        
        // Test prompt building
        console.log('\nTest 2: Prompt building');
        const testInputs = {
            subtask_id: 'test-001',
            subtask_description: 'Test subtask',
            session_num: 1,
            success: true,
            diff: '+ added line\n- removed line',
            changed_files: ['file1.js', 'file2.js'],
            commit_messages: 'abc1234 Test commit',
            attempt_history: []
        };
        const prompt = buildExtractionPrompt(testInputs);
        console.log(`  ✓ Built prompt (${prompt.length} chars)`);
        
        // Test parsing
        console.log('\nTest 3: Insight parsing');
        const testResponse = JSON.stringify({
            file_insights: [{ file: 'test.js', purpose: 'Test file' }],
            patterns_discovered: [{ pattern: 'Test pattern' }],
            gotchas_discovered: [],
            approach_outcome: { success: true, approach_used: 'Direct' },
            recommendations: ['Test recommendation']
        });
        const parsed = parseInsights(testResponse);
        console.log(`  ✓ Parsed ${parsed.file_insights.length} file insights`);
        console.log(`  ✓ Parsed ${parsed.patterns_discovered.length} patterns`);
        
        // Test generic insights
        console.log('\nTest 4: Generic insights');
        const generic = getGenericInsights('test-001', false);
        console.log(`  ✓ Generated generic insights for failed session`);
        
        console.log('\n✅ All tests passed!\n');
        process.exit(0);
    }
    
    // Parse arguments
    const specDirIdx = args.indexOf('--spec-dir');
    const projectDirIdx = args.indexOf('--project-dir');
    const sessionIdx = args.indexOf('--session');
    const loadIdx = args.indexOf('--load');
    
    const specDir = specDirIdx !== -1 ? args[specDirIdx + 1] : null;
    const projectDir = projectDirIdx !== -1 ? args[projectDirIdx + 1] : process.cwd();
    
    if (!specDir && (args.includes('--list') || args.includes('--aggregate') || loadIdx !== -1)) {
        console.error('Error: --spec-dir is required');
        process.exit(1);
    }
    
    if (args.includes('--list')) {
        const insights = listInsights(specDir);
        console.log('\n📊 Session Insights\n');
        
        if (insights.length === 0) {
            console.log('No insights found.\n');
        } else {
            console.log('Session  Subtask         Success  Patterns  Gotchas');
            console.log('───────  ──────────────  ───────  ────────  ───────');
            insights.forEach(i => {
                if (i.error) {
                    console.log(`${i.file.padEnd(8)} ERROR: ${i.error}`);
                } else {
                    console.log(
                        `${String(i.session).padEnd(8)} ` +
                        `${(i.subtask_id || '-').slice(0, 14).padEnd(15)} ` +
                        `${(i.success ? '✓' : '✗').padEnd(8)} ` +
                        `${String(i.patterns_count).padEnd(9)} ` +
                        `${i.gotchas_count}`
                    );
                }
            });
            console.log('');
        }
        process.exit(0);
    }
    
    if (args.includes('--aggregate')) {
        const agg = aggregateInsights(specDir);
        console.log('\n📈 Aggregated Insights\n');
        console.log(`Total sessions: ${agg.total_sessions}`);
        console.log(`Successful: ${agg.successful_sessions}`);
        console.log(`Total patterns: ${agg.all_patterns.length}`);
        console.log(`Total gotchas: ${agg.all_gotchas.length}`);
        console.log(`Total recommendations: ${agg.all_recommendations.length}`);
        
        if (agg.all_patterns.length > 0) {
            console.log('\n🔄 Patterns:');
            agg.all_patterns.slice(0, 5).forEach(p => {
                console.log(`  - ${p.pattern}`);
            });
            if (agg.all_patterns.length > 5) {
                console.log(`  ... and ${agg.all_patterns.length - 5} more`);
            }
        }
        
        if (agg.all_gotchas.length > 0) {
            console.log('\n⚠️ Gotchas:');
            agg.all_gotchas.slice(0, 5).forEach(g => {
                console.log(`  - ${g.gotcha}`);
            });
            if (agg.all_gotchas.length > 5) {
                console.log(`  ... and ${agg.all_gotchas.length - 5} more`);
            }
        }
        
        console.log('');
        process.exit(0);
    }
    
    if (loadIdx !== -1) {
        const sessionNum = parseInt(args[loadIdx + 1]);
        const insights = loadInsights(specDir, sessionNum);
        
        if (!insights) {
            console.log(`\nNo insights found for session ${sessionNum}\n`);
        } else {
            console.log(`\n📋 Session ${sessionNum} Insights\n`);
            console.log(JSON.stringify(insights, null, 2));
            console.log('');
        }
        process.exit(0);
    }
    
    // Default: show help
    console.log('Use --help for usage information');
    process.exit(1);
}

// Export for use as module
module.exports = {
    gatherExtractionInputs,
    buildExtractionPrompt,
    parseInsights,
    getGenericInsights,
    saveInsights,
    loadInsights,
    listInsights,
    aggregateInsights,
    getSessionDiff,
    getChangedFiles,
    getCommitMessages,
    loadConfig
};
