#!/bin/bash
# OCTALUME v2.0 - Git Worktree Manager
# Automated parallel development environment management
# Compatible with Claude Code CLI

set -e

WORKTREE_DIR="${WORKTREE_DIR:-.claude/worktrees}"
ACTIVE_FILE="$WORKTREE_DIR/active.json"
PROJECT_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || echo ".")

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Initialize worktree tracking
init_tracking() {
    mkdir -p "$WORKTREE_DIR"
    if [ ! -f "$ACTIVE_FILE" ]; then
        echo '{
  "version": "2.0.0",
  "worktrees": [],
  "history": []
}' > "$ACTIVE_FILE"
        echo -e "${GREEN}✓ Worktree tracking initialized${NC}"
    fi
}

# Create new worktree for a feature
create_worktree() {
    local feature_name="$1"
    local base_branch="${2:-main}"
    
    if [ -z "$feature_name" ]; then
        echo -e "${RED}Error: Feature name required${NC}"
        echo "Usage: worktree-manager.sh create <feature-name> [base-branch]"
        exit 1
    fi
    
    init_tracking
    
    # Sanitize feature name for directory
    local safe_name=$(echo "$feature_name" | tr ' ' '-' | tr '[:upper:]' '[:lower:]')
    local worktree_path="../worktrees/$safe_name"
    local branch_name="feature/$safe_name"
    
    # Check if worktree already exists
    if git worktree list | grep -q "$safe_name"; then
        echo -e "${YELLOW}⚠ Worktree '$safe_name' already exists${NC}"
        exit 1
    fi
    
    echo -e "${BLUE}🌳 Creating worktree for: $feature_name${NC}"
    echo -e "   Base branch: $base_branch"
    echo -e "   Path: $worktree_path"
    echo -e "   Branch: $branch_name"
    
    # Create the worktree
    git worktree add -b "$branch_name" "$worktree_path" "$base_branch"
    
    # Update tracking file
    local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    local temp_file=$(mktemp)
    
    if command -v jq &> /dev/null; then
        jq --arg name "$safe_name" \
           --arg path "$worktree_path" \
           --arg branch "$branch_name" \
           --arg base "$base_branch" \
           --arg created "$timestamp" \
           '.worktrees += [{
             "name": $name,
             "path": $path,
             "branch": $branch,
             "baseBranch": $base,
             "created": $created,
             "status": "active",
             "commits": 0
           }]' "$ACTIVE_FILE" > "$temp_file" && mv "$temp_file" "$ACTIVE_FILE"
    fi
    
    echo -e "${GREEN}✓ Worktree created successfully${NC}"
    echo -e ""
    echo -e "To switch to this worktree:"
    echo -e "  ${CYAN}cd $worktree_path${NC}"
    echo -e ""
    echo -e "Or use Claude command:"
    echo -e "  ${CYAN}/worktree-switch $safe_name${NC}"
}

# List all active worktrees
list_worktrees() {
    init_tracking
    
    echo -e "${BLUE}🌳 Active Worktrees${NC}"
    echo "===================="
    
    git worktree list --porcelain | while read -r line; do
        case "$line" in
            worktree\ *)
                path="${line#worktree }"
                ;;
            HEAD\ *)
                head="${line#HEAD }"
                ;;
            branch\ *)
                branch="${line#branch refs/heads/}"
                echo -e "${GREEN}→${NC} $branch"
                echo -e "   Path: $path"
                echo -e "   HEAD: ${head:0:8}"
                echo ""
                ;;
        esac
    done
}

# Merge worktree back to base branch
merge_worktree() {
    local feature_name="$1"
    local delete_after="${2:-false}"
    
    if [ -z "$feature_name" ]; then
        echo -e "${RED}Error: Feature name required${NC}"
        echo "Usage: worktree-manager.sh merge <feature-name> [--delete]"
        exit 1
    fi
    
    local safe_name=$(echo "$feature_name" | tr ' ' '-' | tr '[:upper:]' '[:lower:]')
    local branch_name="feature/$safe_name"
    local worktree_path="../worktrees/$safe_name"
    
    # Get base branch from tracking
    local base_branch="main"
    if command -v jq &> /dev/null && [ -f "$ACTIVE_FILE" ]; then
        base_branch=$(jq -r --arg name "$safe_name" '.worktrees[] | select(.name == $name) | .baseBranch // "main"' "$ACTIVE_FILE")
    fi
    
    echo -e "${BLUE}🔀 Merging $branch_name into $base_branch${NC}"
    
    # Switch to main branch in main worktree
    git checkout "$base_branch"
    
    # Merge the feature branch
    if git merge --no-ff "$branch_name" -m "Merge $branch_name into $base_branch"; then
        echo -e "${GREEN}✓ Merge successful${NC}"
        
        # Record in history
        local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
        if command -v jq &> /dev/null && [ -f "$ACTIVE_FILE" ]; then
            local temp_file=$(mktemp)
            jq --arg name "$safe_name" \
               --arg branch "$branch_name" \
               --arg base "$base_branch" \
               --arg merged "$timestamp" \
               '.history += [{
                 "name": $name,
                 "branch": $branch,
                 "mergedInto": $base,
                 "mergedAt": $merged,
                 "action": "merged"
               }] | .worktrees = [.worktrees[] | select(.name != $name)]' "$ACTIVE_FILE" > "$temp_file" && mv "$temp_file" "$ACTIVE_FILE"
        fi
        
        if [ "$delete_after" = "--delete" ] || [ "$delete_after" = "-d" ]; then
            echo -e "${YELLOW}🗑 Removing worktree...${NC}"
            git worktree remove "$worktree_path" --force 2>/dev/null || true
            git branch -d "$branch_name" 2>/dev/null || true
            echo -e "${GREEN}✓ Worktree and branch removed${NC}"
        fi
    else
        echo -e "${RED}✗ Merge failed - resolve conflicts manually${NC}"
        exit 1
    fi
}

# Discard worktree without merging
discard_worktree() {
    local feature_name="$1"
    
    if [ -z "$feature_name" ]; then
        echo -e "${RED}Error: Feature name required${NC}"
        echo "Usage: worktree-manager.sh discard <feature-name>"
        exit 1
    fi
    
    local safe_name=$(echo "$feature_name" | tr ' ' '-' | tr '[:upper:]' '[:lower:]')
    local branch_name="feature/$safe_name"
    local worktree_path="../worktrees/$safe_name"
    
    echo -e "${YELLOW}⚠ Discarding worktree: $safe_name${NC}"
    echo -e "   This will delete the branch and all uncommitted changes!"
    echo ""
    
    # Remove worktree
    git worktree remove "$worktree_path" --force 2>/dev/null || true
    
    # Delete branch
    git branch -D "$branch_name" 2>/dev/null || true
    
    # Update tracking
    local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    if command -v jq &> /dev/null && [ -f "$ACTIVE_FILE" ]; then
        local temp_file=$(mktemp)
        jq --arg name "$safe_name" \
           --arg discarded "$timestamp" \
           '.history += [{
             "name": $name,
             "discardedAt": $discarded,
             "action": "discarded"
           }] | .worktrees = [.worktrees[] | select(.name != $name)]' "$ACTIVE_FILE" > "$temp_file" && mv "$temp_file" "$ACTIVE_FILE"
    fi
    
    echo -e "${GREEN}✓ Worktree discarded${NC}"
}

# Get worktree status
status_worktree() {
    local feature_name="$1"
    
    if [ -z "$feature_name" ]; then
        # Show all worktrees status
        list_worktrees
        return
    fi
    
    local safe_name=$(echo "$feature_name" | tr ' ' '-' | tr '[:upper:]' '[:lower:]')
    local worktree_path="../worktrees/$safe_name"
    
    if [ -d "$worktree_path" ]; then
        echo -e "${BLUE}📊 Status for: $safe_name${NC}"
        echo "========================"
        
        pushd "$worktree_path" > /dev/null
        
        echo -e "${CYAN}Branch:${NC} $(git branch --show-current)"
        echo -e "${CYAN}Commits ahead:${NC} $(git rev-list --count main..HEAD 2>/dev/null || echo 0)"
        echo -e "${CYAN}Modified files:${NC} $(git status --porcelain | wc -l)"
        echo ""
        echo -e "${CYAN}Recent commits:${NC}"
        git log --oneline -5 2>/dev/null || echo "  No commits yet"
        
        popd > /dev/null
    else
        echo -e "${RED}Worktree '$safe_name' not found${NC}"
        exit 1
    fi
}

# Switch to worktree directory
switch_worktree() {
    local feature_name="$1"
    
    if [ -z "$feature_name" ]; then
        echo -e "${RED}Error: Feature name required${NC}"
        echo "Usage: worktree-manager.sh switch <feature-name>"
        exit 1
    fi
    
    local safe_name=$(echo "$feature_name" | tr ' ' '-' | tr '[:upper:]' '[:lower:]')
    local worktree_path="../worktrees/$safe_name"
    
    if [ -d "$worktree_path" ]; then
        echo -e "${GREEN}→ Switching to worktree: $safe_name${NC}"
        echo "cd $worktree_path"
        # Note: actual cd must be done by caller (source this script or use eval)
    else
        echo -e "${RED}Worktree '$safe_name' not found${NC}"
        exit 1
    fi
}

# Sync worktree with base branch
sync_worktree() {
    local feature_name="$1"
    
    if [ -z "$feature_name" ]; then
        echo -e "${RED}Error: Feature name required${NC}"
        exit 1
    fi
    
    local safe_name=$(echo "$feature_name" | tr ' ' '-' | tr '[:upper:]' '[:lower:]')
    local worktree_path="../worktrees/$safe_name"
    
    if [ -d "$worktree_path" ]; then
        echo -e "${BLUE}🔄 Syncing worktree with base branch${NC}"
        
        # Get base branch
        local base_branch="main"
        if command -v jq &> /dev/null && [ -f "$ACTIVE_FILE" ]; then
            base_branch=$(jq -r --arg name "$safe_name" '.worktrees[] | select(.name == $name) | .baseBranch // "main"' "$ACTIVE_FILE")
        fi
        
        pushd "$worktree_path" > /dev/null
        
        echo -e "Fetching latest from origin..."
        git fetch origin "$base_branch" 2>/dev/null || true
        
        echo -e "Rebasing onto $base_branch..."
        if git rebase "origin/$base_branch"; then
            echo -e "${GREEN}✓ Sync successful${NC}"
        else
            echo -e "${YELLOW}⚠ Rebase conflicts detected - resolve manually${NC}"
            git rebase --abort
        fi
        
        popd > /dev/null
    else
        echo -e "${RED}Worktree '$safe_name' not found${NC}"
        exit 1
    fi
}

# Show help
show_help() {
    echo -e "${BLUE}OCTALUME v2.0 - Git Worktree Manager${NC}"
    echo "======================================"
    echo ""
    echo "Commands:"
    echo "  create <name> [base]  Create new worktree for feature"
    echo "  list                  List all active worktrees"
    echo "  merge <name> [-d]     Merge worktree back (optionally delete)"
    echo "  discard <name>        Delete worktree without merging"
    echo "  status [name]         Show worktree status"
    echo "  switch <name>         Switch to worktree directory"
    echo "  sync <name>           Sync worktree with base branch"
    echo "  help                  Show this help"
    echo ""
    echo "Examples:"
    echo "  ./worktree-manager.sh create user-auth"
    echo "  ./worktree-manager.sh create payment-api develop"
    echo "  ./worktree-manager.sh merge user-auth --delete"
    echo "  ./worktree-manager.sh list"
}

# Main command dispatcher
case "${1:-help}" in
    create)
        create_worktree "$2" "$3"
        ;;
    list)
        list_worktrees
        ;;
    merge)
        merge_worktree "$2" "$3"
        ;;
    discard)
        discard_worktree "$2"
        ;;
    status)
        status_worktree "$2"
        ;;
    switch)
        switch_worktree "$2"
        ;;
    sync)
        sync_worktree "$2"
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo -e "${RED}Unknown command: $1${NC}"
        show_help
        exit 1
        ;;
esac
