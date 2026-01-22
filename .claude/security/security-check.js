#!/usr/bin/env node
/**
 * OCTALUME v2.1 - Security Command Checker
 * 
 * Validates commands against the security allowlist before execution.
 * 
 * Usage:
 *   node security-check.js check "rm -rf node_modules"
 *   node security-check.js check "git push origin main" --role DEVELOPER
 *   node security-check.js list-roles
 *   node security-check.js list-commands [role]
 */

const fs = require('fs');
const path = require('path');
const { execSync, spawn } = require('child_process');

const ALLOWLIST_FILE = path.join(__dirname, 'allowlist.json');
const VALIDATORS_DIR = path.join(__dirname, 'validators');

// Load allowlist
function loadAllowlist() {
    if (!fs.existsSync(ALLOWLIST_FILE)) {
        console.error('❌ Allowlist not found:', ALLOWLIST_FILE);
        process.exit(1);
    }
    return JSON.parse(fs.readFileSync(ALLOWLIST_FILE, 'utf8'));
}

// Extract base command from full command string
function extractBaseCommand(command) {
    const parts = command.trim().split(/\s+/);
    return parts[0];
}

// Check if command matches a pattern
function commandMatches(command, pattern) {
    if (pattern.includes('*')) {
        const regex = new RegExp('^' + pattern.replace(/\*/g, '.*') + '$');
        return regex.test(command);
    }
    return command === pattern || command.startsWith(pattern + ' ');
}

// Find command in allowlist categories
function findCommandCategory(command, allowlist) {
    const baseCmd = extractBaseCommand(command);
    
    // Check base_commands
    if (allowlist.base_commands.commands.includes(baseCmd)) {
        return { category: 'base_commands', allowed: true };
    }
    
    // Check write_commands
    if (allowlist.write_commands.commands.includes(baseCmd)) {
        const needsValidation = allowlist.write_commands.requires_validation?.includes(baseCmd);
        return { category: 'write_commands', allowed: true, needsValidation };
    }
    
    // Check dangerous_commands
    const dangerousCmd = Object.keys(allowlist.dangerous_commands.commands).find(cmd => 
        commandMatches(command, cmd)
    );
    if (dangerousCmd) {
        const config = allowlist.dangerous_commands.commands[dangerousCmd];
        if (config.blocked) {
            return { category: 'dangerous_commands', allowed: false, blocked: true, message: config.message };
        }
        return { category: 'dangerous_commands', allowed: true, validator: config.validator, config };
    }
    
    // Check package_managers
    for (const [manager, commands] of Object.entries(allowlist.package_managers)) {
        if (commands.some(cmd => commandMatches(command, cmd))) {
            return { category: 'package_managers', subCategory: manager, allowed: true };
        }
    }
    
    // Check build_tools
    if (allowlist.build_tools.commands.some(cmd => commandMatches(command, cmd))) {
        return { category: 'build_tools', allowed: true };
    }
    
    // Check test_runners
    if (allowlist.test_runners.commands.some(cmd => commandMatches(command, cmd))) {
        return { category: 'test_runners', allowed: true };
    }
    
    // Check linters_formatters
    if (allowlist.linters_formatters.commands.some(cmd => commandMatches(command, cmd))) {
        return { category: 'linters_formatters', allowed: true };
    }
    
    // Check version_control
    for (const [subCat, commands] of Object.entries(allowlist.version_control)) {
        if (subCat === 'description') continue;
        if (commands.some(cmd => commandMatches(command, cmd))) {
            return { category: 'version_control', subCategory: subCat, allowed: true };
        }
    }
    
    return { category: null, allowed: false };
}

// Check role permissions
function checkRolePermission(role, commandResult, allowlist) {
    const roleConfig = allowlist.role_permissions[role];
    if (!roleConfig) {
        return { allowed: false, reason: `Unknown role: ${role}` };
    }
    
    const { category, subCategory } = commandResult;
    
    // Check denied list first
    for (const denied of roleConfig.denied) {
        if (denied === category) {
            return { allowed: false, reason: `Role '${role}' denied access to '${category}'` };
        }
        if (subCategory && denied === `${category}.${subCategory}`) {
            return { allowed: false, reason: `Role '${role}' denied access to '${category}.${subCategory}'` };
        }
    }
    
    // Check allowed list
    for (const allowed of roleConfig.allowed) {
        if (allowed === category) {
            return { allowed: true };
        }
        if (subCategory && (allowed === `${category}.${subCategory}` || allowed === category)) {
            return { allowed: true };
        }
    }
    
    return { allowed: false, reason: `Role '${role}' not allowed for '${category}'` };
}

// Run validator script
function runValidator(validatorName, command) {
    const validatorPath = path.join(VALIDATORS_DIR, validatorName);
    
    if (!fs.existsSync(validatorPath)) {
        console.error(`⚠️  Validator not found: ${validatorName}`);
        return { allowed: true, warning: 'Validator missing' };
    }
    
    try {
        const result = execSync(`bash "${validatorPath}" "${command}"`, {
            encoding: 'utf8',
            stdio: ['pipe', 'pipe', 'pipe']
        });
        
        return { allowed: result.includes('ALLOWED'), output: result };
    } catch (error) {
        return { allowed: false, output: error.stderr || error.message };
    }
}

// Main check function
function checkCommand(command, role = null) {
    const allowlist = loadAllowlist();
    
    console.log(`\n🔍 Checking: "${command}"`);
    if (role) console.log(`   Role: ${role}`);
    console.log('─'.repeat(50));
    
    // Find command category
    const result = findCommandCategory(command, allowlist);
    
    if (result.blocked) {
        console.log(`❌ BLOCKED: ${result.message || 'Command is blocked'}`);
        return false;
    }
    
    if (!result.category) {
        console.log(`❌ BLOCKED: Command not in allowlist`);
        console.log(`   Base command '${extractBaseCommand(command)}' not recognized`);
        return false;
    }
    
    console.log(`📂 Category: ${result.category}${result.subCategory ? '.' + result.subCategory : ''}`);
    
    // Check role permissions if role specified
    if (role) {
        const roleCheck = checkRolePermission(role, result, allowlist);
        if (!roleCheck.allowed) {
            console.log(`❌ BLOCKED: ${roleCheck.reason}`);
            return false;
        }
        console.log(`👤 Role check: ✅ Allowed for ${role}`);
    }
    
    // Run validator if required
    if (result.validator) {
        console.log(`🔧 Running validator: ${result.validator}`);
        const validatorResult = runValidator(result.validator, command);
        
        if (!validatorResult.allowed) {
            console.log(`❌ BLOCKED by validator`);
            if (validatorResult.output) {
                console.log(validatorResult.output);
            }
            return false;
        }
        console.log(`   Validator: ✅ Passed`);
    }
    
    console.log(`\n✅ ALLOWED`);
    return true;
}

// List available roles
function listRoles() {
    const allowlist = loadAllowlist();
    
    console.log('\n👥 Available Roles\n');
    console.log('─'.repeat(50));
    
    for (const [role, config] of Object.entries(allowlist.role_permissions)) {
        console.log(`\n${role}:`);
        console.log(`  Allowed: ${config.allowed.join(', ')}`);
        console.log(`  Denied:  ${config.denied.length > 0 ? config.denied.join(', ') : 'none'}`);
    }
}

// List commands for a role
function listCommands(role = null) {
    const allowlist = loadAllowlist();
    
    console.log('\n📋 Command Categories\n');
    console.log('─'.repeat(50));
    
    const categories = [
        { name: 'base_commands', data: allowlist.base_commands },
        { name: 'write_commands', data: allowlist.write_commands },
        { name: 'dangerous_commands', data: allowlist.dangerous_commands },
        { name: 'package_managers', data: allowlist.package_managers },
        { name: 'build_tools', data: allowlist.build_tools },
        { name: 'test_runners', data: allowlist.test_runners },
        { name: 'linters_formatters', data: allowlist.linters_formatters },
        { name: 'version_control', data: allowlist.version_control }
    ];
    
    for (const cat of categories) {
        console.log(`\n📂 ${cat.name}`);
        
        if (role) {
            const roleConfig = allowlist.role_permissions[role];
            if (roleConfig) {
                const allowed = roleConfig.allowed.some(a => a === cat.name || a.startsWith(cat.name + '.'));
                const denied = roleConfig.denied.some(d => d === cat.name || d.startsWith(cat.name + '.'));
                
                if (denied) {
                    console.log(`   [❌ Denied for ${role}]`);
                    continue;
                }
                if (!allowed) {
                    console.log(`   [⚠️  Not explicitly allowed for ${role}]`);
                }
            }
        }
        
        if (cat.data.commands) {
            if (Array.isArray(cat.data.commands)) {
                console.log(`   ${cat.data.commands.slice(0, 10).join(', ')}${cat.data.commands.length > 10 ? '...' : ''}`);
            } else {
                // Object (dangerous_commands)
                console.log(`   ${Object.keys(cat.data.commands).join(', ')}`);
            }
        } else {
            // Nested categories (package_managers, version_control)
            for (const [subCat, cmds] of Object.entries(cat.data)) {
                if (subCat === 'description') continue;
                if (Array.isArray(cmds)) {
                    console.log(`   ${subCat}: ${cmds.slice(0, 5).join(', ')}${cmds.length > 5 ? '...' : ''}`);
                }
            }
        }
    }
}

// CLI
const args = process.argv.slice(2);
const command = args[0];

switch (command) {
    case 'check':
        if (!args[1]) {
            console.error('Usage: security-check.js check "<command>" [--role ROLE]');
            process.exit(1);
        }
        const cmdToCheck = args[1];
        const roleIdx = args.indexOf('--role');
        const role = roleIdx > -1 ? args[roleIdx + 1] : null;
        
        const allowed = checkCommand(cmdToCheck, role);
        process.exit(allowed ? 0 : 1);
        break;
        
    case 'list-roles':
        listRoles();
        break;
        
    case 'list-commands':
        listCommands(args[1]);
        break;
        
    default:
        console.log(`
OCTALUME v2.1 - Security Command Checker

Usage:
  node security-check.js <command> [options]

Commands:
  check "<cmd>"     Validate a command
    --role ROLE     Check against role permissions
  
  list-roles        Show available roles and permissions
  list-commands     Show allowed command categories
    [role]          Filter by role

Examples:
  node security-check.js check "rm -rf node_modules"
  node security-check.js check "git push origin main" --role DEVELOPER
  node security-check.js list-roles
  node security-check.js list-commands TECH_LEAD
`);
}
