#!/bin/bash
#
# OCTALUME v2.1 - chmod Command Validator
# Validates chmod commands to prevent dangerous permission changes
#
# Usage: validate-chmod.sh "chmod 777 file"
# Exit: 0 = allowed, 1 = blocked
#

set -euo pipefail

COMMAND="$*"

# Colors
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m'

# Dangerous permissions
DANGEROUS_PERMISSIONS=(
    "777"
    "666"
    "o+w"
    "a+w"
    "+w"
)

# Protected paths
PROTECTED_PATHS=(
    "/etc"
    "/var"
    "/usr"
    "/bin"
    "/sbin"
    "/boot"
    "/root"
    "/home"
    "~"
    "\$HOME"
)

log_blocked() {
    echo -e "${RED}❌ BLOCKED${NC}: $1" >&2
}

log_warning() {
    echo -e "${YELLOW}⚠️  WARNING${NC}: $1" >&2
}

log_allowed() {
    echo -e "${GREEN}✅ ALLOWED${NC}: $1" >&2
}

# Check for dangerous world-writable permissions
for perm in "${DANGEROUS_PERMISSIONS[@]}"; do
    if [[ "$COMMAND" == *"$perm"* ]]; then
        # Allow 777 on specific directories
        if [[ "$COMMAND" == *"node_modules"* ]] || [[ "$COMMAND" == *".cache"* ]] || [[ "$COMMAND" == *"tmp"* ]]; then
            log_warning "World-writable permission on cache/temp directory"
        else
            log_blocked "Dangerous permission '$perm' detected"
            echo "BLOCKED: chmod with dangerous permission '$perm'"
            echo "Tip: Use more restrictive permissions like 755 (dirs) or 644 (files)"
            exit 1
        fi
    fi
done

# Check for protected paths
for protected in "${PROTECTED_PATHS[@]}"; do
    if [[ "$COMMAND" == *"$protected"* ]]; then
        log_blocked "Cannot change permissions on protected path: $protected"
        echo "BLOCKED: chmod targets protected path"
        exit 1
    fi
done

# Check for recursive chmod on high-level directories
if [[ "$COMMAND" == *"-R"* ]] || [[ "$COMMAND" == *"--recursive"* ]]; then
    # Extract path
    path=$(echo "$COMMAND" | grep -oE '[^\s]+$')
    
    if [[ -n "$path" ]] && [[ "$path" != -* ]]; then
        # Check depth
        expanded=$(realpath -m "$path" 2>/dev/null || echo "$path")
        depth=$(echo "$expanded" | tr '/' '\n' | wc -l)
        
        if [[ $depth -lt 4 ]]; then
            log_blocked "Recursive chmod on high-level directory (depth: $depth)"
            echo "BLOCKED: Recursive chmod targets directory too high in tree"
            exit 1
        fi
    fi
    
    log_warning "Recursive chmod detected - verify target directory"
fi

# SUID/SGID checks
if [[ "$COMMAND" == *"+s"* ]] || [[ "$COMMAND" == *"4"* && "$COMMAND" =~ [4-7][0-7]{2} ]]; then
    log_blocked "Setting SUID/SGID bit is not allowed"
    echo "BLOCKED: SUID/SGID permission change detected"
    exit 1
fi

log_allowed "chmod command passed validation"
echo "ALLOWED"
exit 0
