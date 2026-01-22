#!/bin/bash
#
# OCTALUME v2.1 - Git Command Validator
# Validates git commands for security (secrets, force push, protected branches)
#
# Usage: validate-git.sh "git commit -m 'message'" [--file path/to/check]
# Exit: 0 = allowed, 1 = blocked
#

set -euo pipefail

COMMAND="$1"
CHECK_FILE="${2:-}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Colors
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m'

# Protected branches (cannot push directly)
PROTECTED_BRANCHES=(
    "main"
    "master"
    "production"
    "prod"
    "release"
    "staging"
)

# Secret patterns to scan for
SECRET_PATTERNS=(
    'password\s*[=:]\s*["\047][^"\047]+'
    'api_key\s*[=:]\s*["\047][^"\047]+'
    'apikey\s*[=:]\s*["\047][^"\047]+'
    'secret\s*[=:]\s*["\047][^"\047]+'
    'token\s*[=:]\s*["\047][^"\047]+'
    'AWS_SECRET_ACCESS_KEY'
    'AWS_ACCESS_KEY_ID'
    'PRIVATE_KEY'
    '-----BEGIN\s+(RSA\s+)?PRIVATE\s+KEY-----'
    '-----BEGIN\s+OPENSSH\s+PRIVATE\s+KEY-----'
    'ghp_[a-zA-Z0-9]{36}'
    'github_pat_[a-zA-Z0-9]{22}_[a-zA-Z0-9]{59}'
    'sk-[a-zA-Z0-9]{48}'
    'xox[baprs]-[0-9]{10,13}-[0-9]{10,13}-[a-zA-Z0-9]{24}'
)

# Allowed secret-like patterns (false positives)
ALLOWED_PATTERNS=(
    'password.*example'
    'password.*placeholder'
    'password.*\$\{'
    'password.*process\.env'
    'password.*os\.environ'
    'api_key.*example'
    'secret.*example'
    'token.*example'
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

# Check for force push
check_force_push() {
    if [[ "$COMMAND" == *"push"* ]] && [[ "$COMMAND" == *"--force"* || "$COMMAND" == *"-f"* ]]; then
        log_blocked "Force push is not allowed"
        echo "BLOCKED: Force push detected"
        return 1
    fi
    return 0
}

# Check for protected branch push
check_protected_branch() {
    if [[ "$COMMAND" == *"push"* ]]; then
        for branch in "${PROTECTED_BRANCHES[@]}"; do
            if [[ "$COMMAND" == *"$branch"* ]]; then
                log_blocked "Cannot push directly to protected branch: $branch"
                echo "BLOCKED: Push to protected branch '$branch'"
                return 1
            fi
        done
        
        # Check current branch
        current_branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "")
        for branch in "${PROTECTED_BRANCHES[@]}"; do
            if [[ "$current_branch" == "$branch" ]]; then
                log_warning "You are on protected branch '$branch'. Consider using a feature branch."
            fi
        done
    fi
    return 0
}

# Scan for secrets in staged files
scan_for_secrets() {
    local files_to_check=""
    
    if [[ -n "$CHECK_FILE" ]]; then
        files_to_check="$CHECK_FILE"
    elif [[ "$COMMAND" == *"commit"* ]]; then
        # Get staged files
        files_to_check=$(git diff --cached --name-only 2>/dev/null || echo "")
    fi
    
    if [[ -z "$files_to_check" ]]; then
        return 0
    fi
    
    local found_secrets=0
    
    for file in $files_to_check; do
        [[ ! -f "$file" ]] && continue
        
        # Skip binary files
        if file "$file" | grep -q "binary"; then
            continue
        fi
        
        # Skip common false-positive files
        case "$file" in
            *.lock|*.sum|package-lock.json|yarn.lock|pnpm-lock.yaml)
                continue
                ;;
        esac
        
        for pattern in "${SECRET_PATTERNS[@]}"; do
            if grep -qiE "$pattern" "$file" 2>/dev/null; then
                # Check if it's an allowed pattern (false positive)
                local is_allowed=0
                for allowed in "${ALLOWED_PATTERNS[@]}"; do
                    if grep -qiE "$allowed" "$file" 2>/dev/null; then
                        is_allowed=1
                        break
                    fi
                done
                
                if [[ $is_allowed -eq 0 ]]; then
                    log_blocked "Potential secret found in '$file' matching pattern: $pattern"
                    grep -inE "$pattern" "$file" 2>/dev/null | head -3 >&2
                    found_secrets=1
                fi
            fi
        done
    done
    
    if [[ $found_secrets -eq 1 ]]; then
        echo ""
        echo "BLOCKED: Potential secrets detected in staged files"
        echo "If these are false positives, add them to .gitignore or use environment variables"
        return 1
    fi
    
    return 0
}

# Check for hard reset
check_hard_reset() {
    if [[ "$COMMAND" == *"reset"* ]] && [[ "$COMMAND" == *"--hard"* ]]; then
        log_warning "Hard reset detected - this will discard uncommitted changes"
    fi
    return 0
}

# Check for destructive rebase
check_rebase() {
    if [[ "$COMMAND" == *"rebase"* ]]; then
        for branch in "${PROTECTED_BRANCHES[@]}"; do
            if [[ "$COMMAND" == *"$branch"* ]]; then
                log_warning "Rebasing onto protected branch '$branch'"
            fi
        done
    fi
    return 0
}

# Main validation
main() {
    # Always check force push
    check_force_push || exit 1
    
    # Check protected branches
    check_protected_branch || exit 1
    
    # Scan for secrets on commit
    if [[ "$COMMAND" == *"commit"* ]]; then
        scan_for_secrets || exit 1
    fi
    
    # Warnings (non-blocking)
    check_hard_reset
    check_rebase
    
    log_allowed "git command passed validation"
    echo "ALLOWED"
    exit 0
}

main
