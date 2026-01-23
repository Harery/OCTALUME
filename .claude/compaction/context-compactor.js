#!/usr/bin/env node
/**
 * Context Compactor - Token optimization through phase summarization
 * 
 * Based on Auto-Claude v2.7.4 spec/compaction.py
 * Summarizes phase outputs to maintain continuity while reducing tokens
 * 
 * @version 2.2
 */

const fs = require('fs');
const path = require('path');

// Load configuration
const CONFIG_PATH = path.join(__dirname, 'compaction-config.json');
let config = null;

function loadConfig() {
    if (!config) {
        config = JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf8'));
    }
    return config;
}

/**
 * Gather output files from a completed phase
 * @param {string} specDir - Path to spec directory
 * @param {string} phaseName - Name of the completed phase
 * @returns {string} Concatenated content of phase output files
 */
function gatherPhaseOutputs(specDir, phaseName) {
    const cfg = loadConfig();
    const phaseConfig = cfg.phase_outputs[phaseName];
    
    if (!phaseConfig || !phaseConfig.files || phaseConfig.files.length === 0) {
        return '';
    }
    
    const outputs = [];
    const maxFileSize = cfg.settings.max_input_chars / phaseConfig.files.length;
    
    for (const filename of phaseConfig.files) {
        const filePath = path.join(specDir, filename);
        
        if (fs.existsSync(filePath)) {
            try {
                let content = fs.readFileSync(filePath, 'utf8');
                
                // Truncate large files
                if (content.length > maxFileSize) {
                    content = content.slice(0, maxFileSize) + cfg.settings.truncation_marker;
                }
                
                outputs.push(`**${filename}**:\n\`\`\`\n${content}\n\`\`\``);
            } catch (err) {
                console.warn(`Warning: Could not read ${filePath}: ${err.message}`);
            }
        }
    }
    
    return outputs.join('\n\n');
}

/**
 * Build summarization prompt for a phase
 * @param {string} phaseName - Phase name
 * @param {string} content - Phase output content
 * @returns {string} Formatted prompt
 */
function buildSummarizationPrompt(phaseName, content) {
    const cfg = loadConfig();
    
    return cfg.summarization_prompt
        .replace('{phase_name}', phaseName.replace(/_/g, ' '))
        .replace('{target_words}', cfg.settings.target_words)
        .replace('{content}', content);
}

/**
 * Format accumulated phase summaries for injection
 * @param {object} summaries - Dict mapping phase names to summaries
 * @returns {string} Formatted string for agent context injection
 */
function formatPhaseSummaries(summaries) {
    const cfg = loadConfig();
    
    if (!summaries || Object.keys(summaries).length === 0) {
        return '';
    }
    
    const parts = [cfg.summary_template.header];
    
    for (const [phaseName, summary] of Object.entries(summaries)) {
        const phaseHeader = cfg.summary_template.phase_header
            .replace('{phase_name}', phaseName.replace(/_/g, ' '));
        const phaseContent = cfg.summary_template.phase_content
            .replace('{summary}', summary);
        
        parts.push(phaseHeader + phaseContent);
    }
    
    parts.push(cfg.summary_template.footer);
    
    return parts.join('');
}

/**
 * Inject compacted context into a prompt
 * @param {string} prompt - Original prompt
 * @param {object} summaries - Phase summaries
 * @returns {string} Prompt with context injected
 */
function injectContext(prompt, summaries) {
    const context = formatPhaseSummaries(summaries);
    
    if (!context) {
        return prompt;
    }
    
    // Inject after first heading or at start
    const headingMatch = prompt.match(/^(#.*?\n)/);
    if (headingMatch) {
        return prompt.replace(headingMatch[0], headingMatch[0] + '\n' + context + '\n');
    }
    
    return context + '\n' + prompt;
}

/**
 * Get phases that should be summarized before a target phase
 * @param {string} targetPhase - The phase about to run
 * @returns {string[]} List of phases to summarize
 */
function getPhasesToSummarize(targetPhase) {
    const cfg = loadConfig();
    const phases = Object.keys(cfg.phase_outputs);
    const targetIndex = phases.indexOf(targetPhase);
    
    if (targetIndex <= 0) {
        return [];
    }
    
    // Get all previous phases that have summarize=true
    return phases
        .slice(0, targetIndex)
        .filter(phase => cfg.phase_outputs[phase].summarize);
}

/**
 * Estimate token count (rough approximation)
 * @param {string} text - Text to estimate
 * @returns {number} Estimated token count
 */
function estimateTokens(text) {
    // Rough estimate: ~4 chars per token for English
    return Math.ceil(text.length / 4);
}

/**
 * Get compaction statistics
 * @param {string} original - Original content
 * @param {string} summary - Summarized content
 * @returns {object} Statistics
 */
function getCompactionStats(original, summary) {
    const originalTokens = estimateTokens(original);
    const summaryTokens = estimateTokens(summary);
    const savings = originalTokens - summaryTokens;
    const percentage = originalTokens > 0 ? Math.round((savings / originalTokens) * 100) : 0;
    
    return {
        original_chars: original.length,
        summary_chars: summary.length,
        original_tokens_est: originalTokens,
        summary_tokens_est: summaryTokens,
        tokens_saved: savings,
        savings_percentage: percentage
    };
}

/**
 * Load existing summaries from file
 * @param {string} specDir - Spec directory path
 * @returns {object} Existing summaries
 */
function loadSummaries(specDir) {
    const summaryFile = path.join(specDir, 'phase-summaries.json');
    
    if (fs.existsSync(summaryFile)) {
        try {
            return JSON.parse(fs.readFileSync(summaryFile, 'utf8'));
        } catch (err) {
            console.warn(`Warning: Could not load summaries: ${err.message}`);
        }
    }
    
    return {};
}

/**
 * Save summaries to file
 * @param {string} specDir - Spec directory path
 * @param {object} summaries - Summaries to save
 */
function saveSummaries(specDir, summaries) {
    const summaryFile = path.join(specDir, 'phase-summaries.json');
    fs.writeFileSync(summaryFile, JSON.stringify(summaries, null, 2));
}

// CLI interface
if (require.main === module) {
    const args = process.argv.slice(2);
    
    if (args.includes('--help') || args.includes('-h')) {
        console.log(`
Context Compactor - Token optimization through phase summarization

Usage:
  node context-compactor.js [options]

Options:
  --spec-dir <path>       Spec directory path (required for most operations)
  --phase <name>          Phase to gather outputs from
  --gather                Gather phase outputs (requires --phase and --spec-dir)
  --format                Format existing summaries (requires --spec-dir)
  --stats                 Show compaction statistics
  --phases-for <target>   Get phases to summarize before target phase
  --list                  List phase output configurations
  --test                  Run self-test
  --help, -h              Show this help

Examples:
  node context-compactor.js --list
  node context-compactor.js --phases-for P4_IMPLEMENTATION
  node context-compactor.js --gather --phase P1_DISCOVERY --spec-dir ./specs/001
  node context-compactor.js --format --spec-dir ./specs/001
`);
        process.exit(0);
    }
    
    if (args.includes('--list')) {
        const cfg = loadConfig();
        console.log('\n📦 Phase Output Configuration\n');
        console.log('Phase              Files                                   Summarize');
        console.log('─────────────────  ──────────────────────────────────────  ─────────');
        for (const [phase, conf] of Object.entries(cfg.phase_outputs)) {
            const files = conf.files.length > 0 ? conf.files.join(', ') : '(none)';
            const summarize = conf.summarize ? '✓' : '✗';
            console.log(`${phase.padEnd(18)} ${files.padEnd(40)} ${summarize}`);
        }
        console.log('');
        process.exit(0);
    }
    
    if (args.includes('--test')) {
        console.log('\n🧪 Running context compactor self-test...\n');
        
        // Test config loading
        console.log('Test 1: Config loading');
        const cfg = loadConfig();
        console.log(`  ✓ Loaded config with ${Object.keys(cfg.phase_outputs).length} phases`);
        
        // Test phases to summarize
        console.log('\nTest 2: Phases to summarize');
        const phases = getPhasesToSummarize('P4_IMPLEMENTATION');
        console.log(`  For P4_IMPLEMENTATION: ${phases.join(', ')}`);
        
        // Test token estimation
        console.log('\nTest 3: Token estimation');
        const testText = 'This is a test string with about forty characters.';
        console.log(`  "${testText}"`);
        console.log(`  Estimated tokens: ${estimateTokens(testText)}`);
        
        // Test formatting
        console.log('\nTest 4: Summary formatting');
        const testSummaries = {
            'P1_DISCOVERY': '- Found 10 files\n- Main entry: index.js',
            'P2_RESEARCH': '- Using React 18\n- TypeScript config needed'
        };
        const formatted = formatPhaseSummaries(testSummaries);
        console.log('  Formatted output preview:');
        console.log(formatted.slice(0, 200) + '...');
        
        console.log('\n✅ All tests passed!\n');
        process.exit(0);
    }
    
    const specDirIdx = args.indexOf('--spec-dir');
    const phaseIdx = args.indexOf('--phase');
    const phasesForIdx = args.indexOf('--phases-for');
    
    if (phasesForIdx !== -1 && args[phasesForIdx + 1]) {
        const target = args[phasesForIdx + 1];
        const phases = getPhasesToSummarize(target);
        console.log(`\nPhases to summarize before ${target}:`);
        if (phases.length === 0) {
            console.log('  (none)\n');
        } else {
            phases.forEach(p => console.log(`  - ${p}`));
            console.log('');
        }
        process.exit(0);
    }
    
    if (args.includes('--gather') && phaseIdx !== -1 && specDirIdx !== -1) {
        const phase = args[phaseIdx + 1];
        const specDir = args[specDirIdx + 1];
        
        if (!phase || !specDir) {
            console.error('Error: --gather requires --phase and --spec-dir');
            process.exit(1);
        }
        
        console.log(`\nGathering outputs from ${phase}...`);
        const outputs = gatherPhaseOutputs(specDir, phase);
        
        if (!outputs) {
            console.log('No outputs found for this phase.\n');
        } else {
            console.log(`\nGathered ${outputs.length} characters:\n`);
            console.log(outputs.slice(0, 500) + (outputs.length > 500 ? '...' : ''));
            console.log('');
        }
        process.exit(0);
    }
    
    if (args.includes('--format') && specDirIdx !== -1) {
        const specDir = args[specDirIdx + 1];
        
        if (!specDir) {
            console.error('Error: --format requires --spec-dir');
            process.exit(1);
        }
        
        const summaries = loadSummaries(specDir);
        
        if (Object.keys(summaries).length === 0) {
            console.log('\nNo existing summaries found.\n');
        } else {
            const formatted = formatPhaseSummaries(summaries);
            console.log('\n' + formatted);
        }
        process.exit(0);
    }
    
    // Default: show help
    console.log('Use --help for usage information');
    process.exit(1);
}

// Export for use as module
module.exports = {
    gatherPhaseOutputs,
    buildSummarizationPrompt,
    formatPhaseSummaries,
    injectContext,
    getPhasesToSummarize,
    estimateTokens,
    getCompactionStats,
    loadSummaries,
    saveSummaries,
    loadConfig
};
