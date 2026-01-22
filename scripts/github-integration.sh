#!/bin/bash
# OCTALUME v2.0 - GitHub Integration
# Automated GitHub issue/PR management
# Compatible with Claude Code CLI

set -e

INTEGRATIONS_DIR="${INTEGRATIONS_DIR:-.claude/integrations}"
CONFIG_FILE="$INTEGRATIONS_DIR/github.json"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m'

# Initialize GitHub integration
init_github() {
    mkdir -p "$INTEGRATIONS_DIR"
    
    if [ ! -f "$CONFIG_FILE" ]; then
        echo '{
  "version": "2.0.0",
  "repo": null,
  "defaultLabels": ["enhancement"],
  "issueTemplate": "feature",
  "prTemplate": "default",
  "autoLink": true
}' > "$CONFIG_FILE"
    fi
    
    # Try to detect repo from git remote
    if command -v git &> /dev/null && [ -d ".git" ]; then
        local remote=$(git remote get-url origin 2>/dev/null || echo "")
        if [[ "$remote" =~ github\.com[:/]([^/]+)/([^/.]+) ]]; then
            local owner="${BASH_REMATCH[1]}"
            local repo="${BASH_REMATCH[2]}"
            repo="${repo%.git}"
            
            if command -v jq &> /dev/null; then
                local temp_file=$(mktemp)
                jq --arg repo "$owner/$repo" '.repo = $repo' "$CONFIG_FILE" > "$temp_file" && mv "$temp_file" "$CONFIG_FILE"
            fi
        fi
    fi
}

# Check if gh CLI is available
check_gh_cli() {
    if ! command -v gh &> /dev/null; then
        echo -e "${YELLOW}⚠ GitHub CLI (gh) not installed${NC}"
        echo -e "  Install: ${CYAN}brew install gh${NC} or ${CYAN}apt install gh${NC}"
        echo -e "  Docs: https://cli.github.com/"
        return 1
    fi
    
    if ! gh auth status &> /dev/null; then
        echo -e "${YELLOW}⚠ GitHub CLI not authenticated${NC}"
        echo -e "  Run: ${CYAN}gh auth login${NC}"
        return 1
    fi
    
    return 0
}

# Create a GitHub issue
create_issue() {
    local title="$1"
    local body="$2"
    local labels="${3:-enhancement}"
    
    if [ -z "$title" ]; then
        echo -e "${RED}Error: Issue title required${NC}"
        echo "Usage: github-integration.sh issue <title> [body] [labels]"
        exit 1
    fi
    
    check_gh_cli || exit 1
    
    echo -e "${BLUE}📋 Creating GitHub Issue${NC}"
    echo -e "   Title: $title"
    
    local issue_url=$(gh issue create \
        --title "$title" \
        --body "${body:-Created via OCTALUME v2.0}" \
        --label "$labels" \
        2>/dev/null)
    
    if [ -n "$issue_url" ]; then
        echo -e "${GREEN}✓ Issue created: $issue_url${NC}"
        
        # Extract issue number and save to memory
        local issue_number=$(echo "$issue_url" | grep -oE '[0-9]+$')
        save_issue_to_memory "$issue_number" "$title"
    else
        echo -e "${RED}✗ Failed to create issue${NC}"
        exit 1
    fi
}

# Create a Pull Request
create_pr() {
    local title="$1"
    local body="$2"
    local base="${3:-main}"
    local draft="${4:-false}"
    
    if [ -z "$title" ]; then
        # Auto-generate title from branch
        local branch=$(git branch --show-current 2>/dev/null)
        title=$(echo "$branch" | sed 's/feature\///' | tr '-' ' ' | sed 's/.*/\u&/')
    fi
    
    check_gh_cli || exit 1
    
    echo -e "${BLUE}🔀 Creating Pull Request${NC}"
    echo -e "   Title: $title"
    echo -e "   Base: $base"
    
    local draft_flag=""
    if [ "$draft" = "true" ] || [ "$draft" = "--draft" ]; then
        draft_flag="--draft"
    fi
    
    # Generate PR body from commits if not provided
    if [ -z "$body" ]; then
        body=$(generate_pr_body)
    fi
    
    local pr_url=$(gh pr create \
        --title "$title" \
        --body "$body" \
        --base "$base" \
        $draft_flag \
        2>/dev/null)
    
    if [ -n "$pr_url" ]; then
        echo -e "${GREEN}✓ Pull Request created: $pr_url${NC}"
        
        # Extract PR number
        local pr_number=$(echo "$pr_url" | grep -oE '[0-9]+$')
        save_pr_to_memory "$pr_number" "$title"
    else
        echo -e "${RED}✗ Failed to create PR${NC}"
        exit 1
    fi
}

# Generate PR body from commits
generate_pr_body() {
    local base="${1:-main}"
    local current=$(git branch --show-current 2>/dev/null)
    
    echo "## Summary"
    echo ""
    echo "<!-- Brief description of changes -->"
    echo ""
    echo "## Changes"
    echo ""
    
    # List commits
    git log --oneline "$base..$current" 2>/dev/null | while read -r line; do
        echo "- $line"
    done
    
    echo ""
    echo "## Checklist"
    echo ""
    echo "- [ ] Tests pass locally"
    echo "- [ ] Documentation updated"
    echo "- [ ] QA checks pass (\`/qa-run\`)"
    echo ""
    echo "---"
    echo "*Created with OCTALUME v2.0*"
}

# List open issues
list_issues() {
    local state="${1:-open}"
    local limit="${2:-10}"
    
    check_gh_cli || exit 1
    
    echo -e "${BLUE}📋 GitHub Issues ($state)${NC}"
    echo "========================"
    echo ""
    
    gh issue list --state "$state" --limit "$limit" 2>/dev/null || {
        echo -e "${YELLOW}No issues found${NC}"
    }
}

# List open PRs
list_prs() {
    local state="${1:-open}"
    local limit="${2:-10}"
    
    check_gh_cli || exit 1
    
    echo -e "${BLUE}🔀 Pull Requests ($state)${NC}"
    echo "========================"
    echo ""
    
    gh pr list --state "$state" --limit "$limit" 2>/dev/null || {
        echo -e "${YELLOW}No pull requests found${NC}"
    }
}

# View issue details
view_issue() {
    local issue_number="$1"
    
    if [ -z "$issue_number" ]; then
        echo -e "${RED}Error: Issue number required${NC}"
        exit 1
    fi
    
    check_gh_cli || exit 1
    
    gh issue view "$issue_number" 2>/dev/null || {
        echo -e "${RED}Issue #$issue_number not found${NC}"
        exit 1
    }
}

# View PR details
view_pr() {
    local pr_number="$1"
    
    if [ -z "$pr_number" ]; then
        echo -e "${RED}Error: PR number required${NC}"
        exit 1
    fi
    
    check_gh_cli || exit 1
    
    gh pr view "$pr_number" 2>/dev/null || {
        echo -e "${RED}PR #$pr_number not found${NC}"
        exit 1
    }
}

# Link commit to issue
link_issue() {
    local issue_number="$1"
    local message="$2"
    
    if [ -z "$issue_number" ]; then
        echo -e "${RED}Error: Issue number required${NC}"
        exit 1
    fi
    
    # Add to commit message template
    local msg="${message:-Work on issue}"
    
    echo -e "${BLUE}🔗 Linking to Issue #$issue_number${NC}"
    echo ""
    echo "Use this in your commit message:"
    echo -e "${CYAN}git commit -m \"$msg (fixes #$issue_number)\"${NC}"
    echo ""
    echo "Keywords for auto-close:"
    echo "  - fixes #$issue_number"
    echo "  - closes #$issue_number"
    echo "  - resolves #$issue_number"
}

# Close issue
close_issue() {
    local issue_number="$1"
    local comment="$2"
    
    if [ -z "$issue_number" ]; then
        echo -e "${RED}Error: Issue number required${NC}"
        exit 1
    fi
    
    check_gh_cli || exit 1
    
    if [ -n "$comment" ]; then
        gh issue close "$issue_number" --comment "$comment" 2>/dev/null
    else
        gh issue close "$issue_number" 2>/dev/null
    fi
    
    echo -e "${GREEN}✓ Issue #$issue_number closed${NC}"
}

# Save issue to memory
save_issue_to_memory() {
    local issue_number="$1"
    local title="$2"
    
    local memory_file=".claude/memory/memory.json"
    if [ -f "$memory_file" ] && command -v jq &> /dev/null; then
        local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
        local temp_file=$(mktemp)
        
        jq --arg num "$issue_number" \
           --arg title "$title" \
           --arg ts "$timestamp" \
           '.current_context.github_issues += [{"number": $num, "title": $title, "created": $ts}]' \
           "$memory_file" > "$temp_file" 2>/dev/null && mv "$temp_file" "$memory_file" || true
    fi
}

# Save PR to memory
save_pr_to_memory() {
    local pr_number="$1"
    local title="$2"
    
    local memory_file=".claude/memory/memory.json"
    if [ -f "$memory_file" ] && command -v jq &> /dev/null; then
        local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
        local temp_file=$(mktemp)
        
        jq --arg num "$pr_number" \
           --arg title "$title" \
           --arg ts "$timestamp" \
           '.current_context.github_prs += [{"number": $num, "title": $title, "created": $ts}]' \
           "$memory_file" > "$temp_file" 2>/dev/null && mv "$temp_file" "$memory_file" || true
    fi
}

# Show repo status
repo_status() {
    check_gh_cli || exit 1
    
    echo -e "${BLUE}📊 Repository Status${NC}"
    echo "===================="
    echo ""
    
    # Get repo info
    gh repo view --json name,description,defaultBranchRef,stargazerCount,forkCount 2>/dev/null | \
        jq -r '"Name: \(.name)\nDescription: \(.description // "N/A")\nDefault Branch: \(.defaultBranchRef.name)\nStars: \(.stargazerCount)\nForks: \(.forkCount)"' || true
    
    echo ""
    echo -e "${CYAN}Open Issues:${NC} $(gh issue list --state open --json number 2>/dev/null | jq 'length')"
    echo -e "${CYAN}Open PRs:${NC}    $(gh pr list --state open --json number 2>/dev/null | jq 'length')"
}

# Show help
show_help() {
    echo -e "${BLUE}OCTALUME v2.0 - GitHub Integration${NC}"
    echo "===================================="
    echo ""
    echo "Commands:"
    echo "  issue <title> [body] [labels]   Create a new issue"
    echo "  pr [title] [body] [base]        Create a pull request"
    echo "  issues [state] [limit]          List issues"
    echo "  prs [state] [limit]             List pull requests"
    echo "  view-issue <number>             View issue details"
    echo "  view-pr <number>                View PR details"
    echo "  close <issue-number> [comment]  Close an issue"
    echo "  link <issue-number>             Get commit link syntax"
    echo "  status                          Show repo status"
    echo "  help                            Show this help"
    echo ""
    echo "Examples:"
    echo "  ./scripts/github-integration.sh issue \"Add login feature\""
    echo "  ./scripts/github-integration.sh pr \"Feature: User Auth\" \"\" main"
    echo "  ./scripts/github-integration.sh issues open 20"
    echo "  ./scripts/github-integration.sh link 42"
    echo ""
    echo "Prerequisites:"
    echo "  - GitHub CLI (gh) installed"
    echo "  - Authenticated: gh auth login"
}

# Main command dispatcher
init_github

case "${1:-help}" in
    issue)
        create_issue "$2" "$3" "$4"
        ;;
    pr)
        create_pr "$2" "$3" "$4" "$5"
        ;;
    issues)
        list_issues "$2" "$3"
        ;;
    prs)
        list_prs "$2" "$3"
        ;;
    view-issue)
        view_issue "$2"
        ;;
    view-pr)
        view_pr "$2"
        ;;
    close)
        close_issue "$2" "$3"
        ;;
    link)
        link_issue "$2" "$3"
        ;;
    status)
        repo_status
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
