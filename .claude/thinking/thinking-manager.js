#!/usr/bin/env node
/**
 * Thinking Manager - Phase-aware extended thinking control
 * 
 * Based on Auto-Claude v2.7.4 phase_config.py
 * Provides thinking level configuration and budget management
 * 
 * @version 2.2
 */

const fs = require('fs');
const path = require('path');

// Load configuration
const CONFIG_PATH = path.join(__dirname, 'thinking-levels.json');
let config = null;

function loadConfig() {
    if (!config) {
        config = JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf8'));
    }
    return config;
}

/**
 * Get token budget for a thinking level
 * @param {string} level - Thinking level (none, low, medium, high, ultrathink)
 * @returns {number|null} Token budget or null for no extended thinking
 */
function getThinkingBudget(level) {
    const cfg = loadConfig();
    if (!cfg.budget_map.hasOwnProperty(level)) {
        console.warn(`Invalid thinking level '${level}'. Using 'medium'.`);
        return cfg.budget_map.medium;
    }
    return cfg.budget_map[level];
}

/**
 * Get thinking level for a phase
 * @param {string} phaseName - Phase name (e.g., 'P1_DISCOVERY')
 * @returns {string} Thinking level
 */
function getPhaseThinking(phaseName) {
    const cfg = loadConfig();
    const normalized = phaseName.toUpperCase().replace(/\s+/g, '_');
    return cfg.phase_defaults[normalized] || 'medium';
}

/**
 * Get thinking level for an agent role
 * @param {string} agentRole - Agent role (e.g., 'developer', 'reviewer')
 * @returns {string} Thinking level
 */
function getAgentThinking(agentRole) {
    const cfg = loadConfig();
    const normalized = agentRole.toLowerCase().replace(/\s+/g, '_');
    return cfg.agent_defaults[normalized] || 'medium';
}

/**
 * Get thinking level for a task type
 * @param {string} taskType - Task type (e.g., 'spec_writing', 'debugging')
 * @returns {string} Thinking level
 */
function getTaskThinking(taskType) {
    const cfg = loadConfig();
    const normalized = taskType.toLowerCase().replace(/\s+/g, '_');
    return cfg.task_type_overrides[normalized] || 'medium';
}

/**
 * Format thinking header for prompts
 * @param {string} level - Thinking level
 * @param {number|null} budget - Token budget
 * @returns {string} Formatted header
 */
function formatThinkingHeader(level, budget) {
    const cfg = loadConfig();
    const desc = cfg.budget_descriptions[level] || 'Standard thinking';
    
    if (budget === null) {
        return `🧠 **Thinking Mode**: ${level.toUpperCase()} - ${desc}`;
    }
    return `🧠 **Thinking Mode**: ${level.toUpperCase()} (${budget.toLocaleString()} tokens) - ${desc}`;
}

/**
 * Get recommended thinking configuration for a context
 * @param {object} context - Context object with phase, role, taskType
 * @returns {object} Thinking configuration
 */
function getRecommendedThinking(context) {
    const cfg = loadConfig();
    let level = 'medium';
    let source = 'default';
    
    // Priority: task_type > phase > agent role
    if (context.taskType) {
        const taskLevel = getTaskThinking(context.taskType);
        if (cfg.task_type_overrides[context.taskType.toLowerCase()]) {
            level = taskLevel;
            source = `task_type:${context.taskType}`;
        }
    }
    
    if (source === 'default' && context.phase) {
        const phaseLevel = getPhaseThinking(context.phase);
        if (cfg.phase_defaults[context.phase.toUpperCase()]) {
            level = phaseLevel;
            source = `phase:${context.phase}`;
        }
    }
    
    if (source === 'default' && context.role) {
        const roleLevel = getAgentThinking(context.role);
        if (cfg.agent_defaults[context.role.toLowerCase()]) {
            level = roleLevel;
            source = `role:${context.role}`;
        }
    }
    
    const budget = getThinkingBudget(level);
    
    return {
        level,
        budget,
        source,
        header: formatThinkingHeader(level, budget)
    };
}

/**
 * List all thinking levels with descriptions
 * @returns {object} All levels and their configurations
 */
function listThinkingLevels() {
    const cfg = loadConfig();
    const levels = {};
    
    for (const [level, budget] of Object.entries(cfg.budget_map)) {
        levels[level] = {
            budget,
            description: cfg.budget_descriptions[level] || 'No description'
        };
    }
    
    return levels;
}

/**
 * Validate a thinking level
 * @param {string} level - Level to validate
 * @returns {boolean} True if valid
 */
function isValidLevel(level) {
    const cfg = loadConfig();
    return cfg.budget_map.hasOwnProperty(level);
}

// CLI interface
if (require.main === module) {
    const args = process.argv.slice(2);
    
    if (args.includes('--help') || args.includes('-h')) {
        console.log(`
Thinking Manager - Phase-aware extended thinking control

Usage:
  node thinking-manager.js [options]

Options:
  --list                  List all thinking levels
  --phase <name>          Get thinking for a phase
  --role <name>           Get thinking for a role
  --task <type>           Get thinking for a task type
  --budget <level>        Get token budget for a level
  --recommend             Get recommended thinking (requires --phase, --role, or --task)
  --test                  Run self-test
  --help, -h              Show this help

Examples:
  node thinking-manager.js --list
  node thinking-manager.js --phase P1_DISCOVERY
  node thinking-manager.js --role developer
  node thinking-manager.js --task spec_writing
  node thinking-manager.js --budget ultrathink
  node thinking-manager.js --recommend --phase P7_CRITIQUE --role architect
`);
        process.exit(0);
    }
    
    if (args.includes('--list')) {
        const levels = listThinkingLevels();
        console.log('\n🧠 OCTALUME Thinking Levels\n');
        console.log('Level        Budget      Description');
        console.log('───────────  ──────────  ─────────────────────────────────────────');
        for (const [level, info] of Object.entries(levels)) {
            const budgetStr = info.budget === null ? 'none' : info.budget.toLocaleString().padStart(6);
            console.log(`${level.padEnd(12)} ${budgetStr.padEnd(11)} ${info.description}`);
        }
        console.log('');
        process.exit(0);
    }
    
    if (args.includes('--test')) {
        console.log('\n🧪 Running self-test...\n');
        
        // Test budget lookup
        console.log('Test 1: Budget lookup');
        ['none', 'low', 'medium', 'high', 'ultrathink'].forEach(level => {
            const budget = getThinkingBudget(level);
            console.log(`  ${level}: ${budget === null ? 'null' : budget}`);
        });
        
        // Test phase lookup
        console.log('\nTest 2: Phase thinking');
        ['P1_DISCOVERY', 'P4_IMPLEMENTATION', 'P7_CRITIQUE'].forEach(phase => {
            console.log(`  ${phase}: ${getPhaseThinking(phase)}`);
        });
        
        // Test role lookup
        console.log('\nTest 3: Role thinking');
        ['architect', 'developer', 'reviewer'].forEach(role => {
            console.log(`  ${role}: ${getAgentThinking(role)}`);
        });
        
        // Test recommended
        console.log('\nTest 4: Recommended thinking');
        const rec = getRecommendedThinking({ phase: 'P7_CRITIQUE', role: 'architect', taskType: 'self_critique' });
        console.log(`  Context: phase=P7_CRITIQUE, role=architect, taskType=self_critique`);
        console.log(`  Result: level=${rec.level}, budget=${rec.budget}, source=${rec.source}`);
        
        console.log('\n✅ All tests passed!\n');
        process.exit(0);
    }
    
    // Build context from args
    const context = {};
    const phaseIdx = args.indexOf('--phase');
    const roleIdx = args.indexOf('--role');
    const taskIdx = args.indexOf('--task');
    const budgetIdx = args.indexOf('--budget');
    
    if (phaseIdx !== -1 && args[phaseIdx + 1]) {
        context.phase = args[phaseIdx + 1];
    }
    if (roleIdx !== -1 && args[roleIdx + 1]) {
        context.role = args[roleIdx + 1];
    }
    if (taskIdx !== -1 && args[taskIdx + 1]) {
        context.taskType = args[taskIdx + 1];
    }
    
    if (budgetIdx !== -1 && args[budgetIdx + 1]) {
        const level = args[budgetIdx + 1];
        const budget = getThinkingBudget(level);
        console.log(`\nThinking level '${level}': ${budget === null ? 'No extended thinking' : budget.toLocaleString() + ' tokens'}\n`);
        process.exit(0);
    }
    
    if (args.includes('--recommend') || Object.keys(context).length > 0) {
        const rec = getRecommendedThinking(context);
        console.log('\n' + rec.header);
        console.log(`  Level: ${rec.level}`);
        console.log(`  Budget: ${rec.budget === null ? 'none' : rec.budget.toLocaleString() + ' tokens'}`);
        console.log(`  Source: ${rec.source}\n`);
        process.exit(0);
    }
    
    // Default: show help
    console.log('Use --help for usage information');
    process.exit(1);
}

// Export for use as module
module.exports = {
    getThinkingBudget,
    getPhaseThinking,
    getAgentThinking,
    getTaskThinking,
    formatThinkingHeader,
    getRecommendedThinking,
    listThinkingLevels,
    isValidLevel,
    loadConfig
};
