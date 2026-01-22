#!/bin/bash
#
# OCTALUME v2.1 - rm Command Validator
# Validates rm commands against dangerous patterns
#
# Usage: validate-rm.sh "rm -rf path/to/delete"
# Exit: 0 = allowed, 1 = blocked
#

set -euo pipefail

COMMAND="$*"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Colors
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m'

# Blocked patterns (absolute blocks)
BLOCKED_PATTERNS=(
    "-rf /"
    "-rf /*"
    "-rf ~"
    "-rf ~/"
    "-rf \$HOME"
    "-rf /home"
    "-rf /etc"
    "-rf /var"
    "-rf /usr"
    "-rf /bin"
    "-rf /sbin"
    "-rf /boot"
    "-rf /root"
    "--no-preserve-root"
    "-rf .."
    "-rf ../"
)

# Warning patterns (require confirmation)
WARNING_PATTERNS=(
    "-rf node_modules"
    "-rf .git"
    "-rf dist"
    "-rf build"
    "-rf target"
    "-rf __pycache__"
    "-rf .venv"
    "-rf venv"
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

# Check for blocked patterns
for pattern in "${BLOCKED_PATTERNS[@]}"; do
    if [[ "$COMMAND" == *"$pattern"* ]]; then
        log_blocked "Dangerous rm pattern detected: '$pattern'"
        echo "BLOCKED: rm command contains dangerous pattern '$pattern'"
        exit 1
    fi
done

# Check if trying to delete root-level paths
if echo "$COMMAND" | grep -qE 'rm\s+(-[a-z]+\s+)?/[a-z]+$'; then
    log_blocked "Cannot delete root-level directories"
    echo "BLOCKED: rm command targets root-level directory"
    exit 1
fi

# Check path depth (prevent deleting too high up)
extract_paths() {
    echo "$COMMAND" | grep -oE '[^\s]+' | tail -n +2 | grep -v '^-'
}

for path in $(extract_paths); do
    # Skip flags
    [[ "$path" == -* ]] && continue
    
    # Expand path
    expanded_path=$(realpath -m "$path" 2>/dev/null || echo "$path")
    
    # Count depth from project root
    depth=$(echo "$expanded_path" | tr '/' '\n' | wc -l)
    
    if [[ $depth -lt 4 ]]; then
        log_blocked "Path '$path' is too high in directory tree (depth: $depth)"
        echo "BLOCKED: rm targets path with insufficient depth"
        exit 1
    fi
done

# Check for warning patterns (allowed but logged)
for pattern in "${WARNING_PATTERNS[@]}"; do
    if [[ "$COMMAND" == *"$pattern"* ]]; then
        log_warning "Deleting common directory: '$pattern'"
    fi
done

# If we get here, command is allowed
log_allowed "rm command passed validation"
echo "ALLOWED"
exit 0
