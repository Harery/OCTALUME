#!/bin/bash
#
# OCTALUME v2.2 - AI Merge Resolver
# Resolves git merge conflicts using AI assistance
#
# Usage:
#   ./ai-merge-resolver.sh [worktree-name]
#   ./ai-merge-resolver.sh --check
#   ./ai-merge-resolver.sh --resolve file.js
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
WORKTREES_DIR="$PROJECT_ROOT/.claude/worktrees"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# AI Merge prompt template
AI_MERGE_PROMPT='You are resolving a git merge conflict. Analyze both versions and produce the correct merged result.

## Conflict Context

File: {{FILE_PATH}}
Base Branch: {{BASE_BRANCH}}
Feature Branch: {{FEATURE_BRANCH}}

## Conflict Content

```
{{CONFLICT_CONTENT}}
```

## Instructions

1. Understand what BOTH sides are trying to achieve
2. Combine the changes logically
3. Preserve all intended functionality from both branches
4. Ensure the result is syntactically correct
5. Do NOT include conflict markers in output

## Output

Return ONLY the resolved code (no explanations, no markers):
'

# Check for conflicts
check_conflicts() {
    local conflicts=$(git diff --name-only --diff-filter=U 2>/dev/null || echo "")
    
    if [[ -z "$conflicts" ]]; then
        echo -e "${GREEN}✅ No merge conflicts found${NC}"
        return 0
    fi
    
    echo -e "${YELLOW}⚠️  Merge conflicts detected in:${NC}"
    echo ""
    echo "$conflicts" | while read -r file; do
        echo -e "  ${RED}✗${NC} $file"
    done
    echo ""
    
    return 1
}

# Extract conflict sections from a file
extract_conflicts() {
    local file="$1"
    
    if [[ ! -f "$file" ]]; then
        echo "File not found: $file"
        return 1
    fi
    
    # Check if file has conflict markers
    if ! grep -q "^<<<<<<< " "$file"; then
        echo "No conflict markers found in: $file"
        return 1
    fi
    
    cat "$file"
}

# Get current branches
get_branch_info() {
    local base_branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")
    local merging_branch=""
    
    # Check if we're in a merge state
    if [[ -f ".git/MERGE_HEAD" ]]; then
        merging_branch=$(git name-rev --name-only "$(cat .git/MERGE_HEAD)" 2>/dev/null || echo "unknown")
    fi
    
    echo "$base_branch|$merging_branch"
}

# Generate AI prompt for a specific file
generate_merge_prompt() {
    local file="$1"
    local branch_info=$(get_branch_info)
    local base_branch=$(echo "$branch_info" | cut -d'|' -f1)
    local feature_branch=$(echo "$branch_info" | cut -d'|' -f2)
    local conflict_content=$(extract_conflicts "$file")
    
    local prompt="$AI_MERGE_PROMPT"
    prompt="${prompt//\{\{FILE_PATH\}\}/$file}"
    prompt="${prompt//\{\{BASE_BRANCH\}\}/$base_branch}"
    prompt="${prompt//\{\{FEATURE_BRANCH\}\}/$feature_branch}"
    prompt="${prompt//\{\{CONFLICT_CONTENT\}\}/$conflict_content}"
    
    echo "$prompt"
}

# Save merge prompt for manual resolution
save_merge_prompt() {
    local file="$1"
    local prompt_dir="$PROJECT_ROOT/.claude/qa/.merge-prompts"
    mkdir -p "$prompt_dir"
    
    local safe_name=$(echo "$file" | tr '/' '_')
    local prompt_file="$prompt_dir/${safe_name}.md"
    
    generate_merge_prompt "$file" > "$prompt_file"
    echo "$prompt_file"
}

# Apply resolved content to file
apply_resolution() {
    local file="$1"
    local resolved_content="$2"
    
    # Backup original
    cp "$file" "${file}.conflict-backup"
    
    # Write resolved content
    echo "$resolved_content" > "$file"
    
    # Verify no conflict markers remain
    if grep -q "^<<<<<<< \|^=======$\|^>>>>>>> " "$file"; then
        echo -e "${RED}❌ Resolution still contains conflict markers${NC}"
        mv "${file}.conflict-backup" "$file"
        return 1
    fi
    
    echo -e "${GREEN}✅ Resolution applied to: $file${NC}"
    echo "   Backup saved to: ${file}.conflict-backup"
    
    # Stage the resolved file
    git add "$file"
    
    return 0
}

# Resolve conflicts in a worktree
resolve_worktree() {
    local worktree_name="$1"
    local worktree_path="$WORKTREES_DIR/$worktree_name"
    
    if [[ ! -d "$worktree_path" ]]; then
        echo -e "${RED}❌ Worktree not found: $worktree_name${NC}"
        return 1
    fi
    
    cd "$worktree_path"
    
    echo -e "${BLUE}🔧 Resolving conflicts in worktree: $worktree_name${NC}"
    echo ""
    
    # Check for conflicts
    local conflicts=$(git diff --name-only --diff-filter=U 2>/dev/null || echo "")
    
    if [[ -z "$conflicts" ]]; then
        echo -e "${GREEN}✅ No conflicts in worktree${NC}"
        return 0
    fi
    
    local count=0
    local prompt_files=()
    
    echo "$conflicts" | while read -r file; do
        ((count++)) || true
        echo -e "${CYAN}[$count] Processing: $file${NC}"
        
        local prompt_file=$(save_merge_prompt "$file")
        prompt_files+=("$prompt_file")
        
        echo "   Prompt saved: $prompt_file"
    done
    
    echo ""
    echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${YELLOW}AI Merge Resolution Instructions${NC}"
    echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
    echo ""
    echo "Prompts have been generated for each conflicted file."
    echo ""
    echo "To resolve:"
    echo "1. Open the prompt file in Claude Code"
    echo "2. Copy the AI's resolved output"
    echo "3. Run: ./ai-merge-resolver.sh --apply <file> <resolved-content-file>"
    echo ""
    echo "Or resolve manually and run:"
    echo "   git add <file>"
    echo "   git merge --continue"
    echo ""
}

# Interactive resolution mode
interactive_resolve() {
    local file="$1"
    
    echo -e "${BLUE}🔧 AI Merge Resolver - Interactive Mode${NC}"
    echo -e "   File: ${CYAN}$file${NC}"
    echo ""
    
    # Generate and display prompt
    local prompt_file=$(save_merge_prompt "$file")
    
    echo -e "${GREEN}Prompt generated:${NC} $prompt_file"
    echo ""
    echo "─────────────────────────────────────────────────────────────"
    echo ""
    cat "$prompt_file" | head -50
    echo ""
    echo "─────────────────────────────────────────────────────────────"
    echo ""
    echo -e "${YELLOW}Next steps:${NC}"
    echo "1. Copy the prompt above (or from $prompt_file)"
    echo "2. Send to Claude and get resolved code"
    echo "3. Save resolved code to a file (e.g., /tmp/resolved.txt)"
    echo "4. Run: ./ai-merge-resolver.sh --apply $file /tmp/resolved.txt"
    echo ""
}

# Apply resolution from file
apply_from_file() {
    local conflict_file="$1"
    local resolution_file="$2"
    
    if [[ ! -f "$resolution_file" ]]; then
        echo -e "${RED}❌ Resolution file not found: $resolution_file${NC}"
        return 1
    fi
    
    local resolved_content=$(cat "$resolution_file")
    apply_resolution "$conflict_file" "$resolved_content"
}

# Show help
show_help() {
    cat << EOF
OCTALUME v2.2 - AI Merge Resolver

Usage:
  ./ai-merge-resolver.sh [command] [options]

Commands:
  --check                     Check for merge conflicts
  --resolve <file>            Generate AI prompt for a file
  --apply <file> <resolved>   Apply resolved content from file
  --worktree <name>           Resolve conflicts in a worktree
  --help                      Show this help

Examples:
  # Check for conflicts
  ./ai-merge-resolver.sh --check

  # Generate prompt for a file
  ./ai-merge-resolver.sh --resolve src/index.js

  # Apply AI resolution
  ./ai-merge-resolver.sh --apply src/index.js /tmp/resolved.txt

  # Resolve worktree conflicts
  ./ai-merge-resolver.sh --worktree feature-auth

Workflow:
  1. Run --check to identify conflicted files
  2. Run --resolve for each file to generate AI prompts
  3. Send prompts to Claude, save resolved output
  4. Run --apply to apply the resolution
  5. Run: git merge --continue

EOF
}

# Main
main() {
    local command="${1:-}"
    
    case "$command" in
        --check|-c)
            check_conflicts
            ;;
        --resolve|-r)
            if [[ -z "${2:-}" ]]; then
                echo "Usage: ai-merge-resolver.sh --resolve <file>"
                exit 1
            fi
            interactive_resolve "$2"
            ;;
        --apply|-a)
            if [[ -z "${2:-}" ]] || [[ -z "${3:-}" ]]; then
                echo "Usage: ai-merge-resolver.sh --apply <conflict-file> <resolution-file>"
                exit 1
            fi
            apply_from_file "$2" "$3"
            ;;
        --worktree|-w)
            if [[ -z "${2:-}" ]]; then
                echo "Usage: ai-merge-resolver.sh --worktree <name>"
                exit 1
            fi
            resolve_worktree "$2"
            ;;
        --help|-h)
            show_help
            ;;
        "")
            # Default: check for conflicts
            check_conflicts
            ;;
        *)
            # Assume it's a worktree name
            if [[ -d "$WORKTREES_DIR/$command" ]]; then
                resolve_worktree "$command"
            else
                echo "Unknown command: $command"
                echo "Run --help for usage"
                exit 1
            fi
            ;;
    esac
}

main "$@"
