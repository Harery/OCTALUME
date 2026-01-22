---
description: Validate a command against security allowlist
argument-name: command
argument-description: The command to validate (in quotes)
---

# Security Command Check

Validates commands against the OCTALUME security allowlist before execution.

## Running Check

```bash
node .claude/security/security-check.js check "$ARGUMENTS"
```

## With Role Validation

```bash
# Check as specific role
node .claude/security/security-check.js check "$ARGUMENTS" --role TECH_LEAD
node .claude/security/security-check.js check "$ARGUMENTS" --role DEVELOPER
node .claude/security/security-check.js check "$ARGUMENTS" --role QA_LEAD
```

## Understanding Results

- **ALLOWED**: Command passed all checks
- **BLOCKED**: Command failed validation
  - Not in allowlist
  - Role doesn't have permission
  - Validator rejected (dangerous pattern)

## Available Roles

| Role | Access Level |
|------|--------------|
| TECH_LEAD | Full access (except sudo) |
| DEVELOPER | Standard dev commands |
| QA_LEAD | Read + test commands |
| DEVOPS | Full access |
| SECURITY_ARCHITECT | Read + lint only |
| READ_ONLY | Read-only access |

## Useful Commands

```bash
# List all roles
node .claude/security/security-check.js list-roles

# List commands for a role
node .claude/security/security-check.js list-commands DEVELOPER
```

## Security Features

1. **Command Allowlist**: Only allowed commands can run
2. **Role Permissions**: Access based on team role
3. **Validators**: Extra checks for dangerous commands
4. **Secret Scanning**: Detects credentials in git commits
5. **Protected Branches**: Prevents push to main/master
