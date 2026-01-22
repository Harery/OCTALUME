#!/bin/bash
#
# OCTALUME v2.3 - GitLab Integration
# Wrapper for GitLab CLI (glab) with OCTALUME conventions
#
# Usage:
#   ./gitlab-integration.sh issue create "Title" "Description"
#   ./gitlab-integration.sh mr create
#   ./gitlab-integration.sh pipeline status
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
CONFIG_FILE="$PROJECT_ROOT/.claude/integrations/gitlab.json"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Check for glab CLI
check_glab() {
    if ! command -v glab &> /dev/null; then
        echo -e "${RED}❌ GitLab CLI (glab) not found${NC}"
        echo ""
        echo "Install glab:"
        echo "  brew install glab          # macOS"
        echo "  sudo apt install glab      # Ubuntu/Debian"
        echo "  winget install glab        # Windows"
        echo ""
        echo "Or see: https://gitlab.com/gitlab-org/cli"
        exit 1
    fi
}

# Load configuration
load_config() {
    if [[ -f "$CONFIG_FILE" ]]; then
        cat "$CONFIG_FILE"
    else
        echo '{}'
    fi
}

# Get phase labels
get_phase_labels() {
    local phase="${1:-}"
    local config=$(load_config)
    
    if [[ -n "$phase" ]]; then
        echo "$config" | jq -r ".labels.\"$phase\" // \"$phase\"" 2>/dev/null || echo "$phase"
    else
        echo ""
    fi
}

# ─────────────────────────────────────────────────────────────
# ISSUE COMMANDS
# ─────────────────────────────────────────────────────────────

issue_create() {
    local title="$1"
    local body="${2:-}"
    local labels="${3:-}"
    local assignee="${4:-}"
    
    echo -e "${BLUE}📝 Creating GitLab issue...${NC}"
    
    local cmd="glab issue create --title \"$title\""
    
    if [[ -n "$body" ]]; then
        cmd="$cmd --description \"$body\""
    fi
    
    if [[ -n "$labels" ]]; then
        cmd="$cmd --label \"$labels\""
    fi
    
    if [[ -n "$assignee" ]]; then
        cmd="$cmd --assignee \"$assignee\""
    fi
    
    eval "$cmd"
    
    echo -e "${GREEN}✅ Issue created${NC}"
}

issue_list() {
    local state="${1:-opened}"
    local labels="${2:-}"
    
    echo -e "${BLUE}📋 Listing GitLab issues (state: $state)${NC}"
    echo ""
    
    local cmd="glab issue list --state $state"
    
    if [[ -n "$labels" ]]; then
        cmd="$cmd --label \"$labels\""
    fi
    
    eval "$cmd"
}

issue_view() {
    local issue_id="$1"
    
    glab issue view "$issue_id"
}

issue_close() {
    local issue_id="$1"
    
    echo -e "${BLUE}🔒 Closing issue #$issue_id...${NC}"
    glab issue close "$issue_id"
    echo -e "${GREEN}✅ Issue closed${NC}"
}

# ─────────────────────────────────────────────────────────────
# MERGE REQUEST COMMANDS
# ─────────────────────────────────────────────────────────────

mr_create() {
    local title="${1:-}"
    local description="${2:-}"
    local target="${3:-main}"
    local draft="${4:-false}"
    
    echo -e "${BLUE}🔀 Creating Merge Request...${NC}"
    
    # Auto-generate title from branch name if not provided
    if [[ -z "$title" ]]; then
        local branch=$(git rev-parse --abbrev-ref HEAD)
        title=$(echo "$branch" | sed 's/[-_]/ /g' | sed 's/octalume\///')
    fi
    
    # Auto-generate description if not provided
    if [[ -z "$description" ]]; then
        description="## Changes\n\n$(git log --oneline $target..HEAD | head -10)"
    fi
    
    local cmd="glab mr create --title \"$title\" --description \"$description\" --target-branch \"$target\""
    
    if [[ "$draft" == "true" ]]; then
        cmd="$cmd --draft"
    fi
    
    # Remove source branch after merge
    cmd="$cmd --remove-source-branch"
    
    eval "$cmd"
    
    echo -e "${GREEN}✅ Merge Request created${NC}"
}

mr_list() {
    local state="${1:-opened}"
    
    echo -e "${BLUE}📋 Listing Merge Requests (state: $state)${NC}"
    echo ""
    
    glab mr list --state "$state"
}

mr_view() {
    local mr_id="$1"
    
    glab mr view "$mr_id"
}

mr_merge() {
    local mr_id="$1"
    local squash="${2:-true}"
    
    echo -e "${BLUE}🔀 Merging MR !$mr_id...${NC}"
    
    local cmd="glab mr merge $mr_id --remove-source-branch"
    
    if [[ "$squash" == "true" ]]; then
        cmd="$cmd --squash"
    fi
    
    eval "$cmd"
    
    echo -e "${GREEN}✅ Merge Request merged${NC}"
}

mr_checkout() {
    local mr_id="$1"
    
    echo -e "${BLUE}📥 Checking out MR !$mr_id...${NC}"
    glab mr checkout "$mr_id"
}

# ─────────────────────────────────────────────────────────────
# PIPELINE COMMANDS
# ─────────────────────────────────────────────────────────────

pipeline_status() {
    echo -e "${BLUE}🔄 Pipeline Status${NC}"
    echo ""
    
    glab ci status
}

pipeline_list() {
    echo -e "${BLUE}📋 Recent Pipelines${NC}"
    echo ""
    
    glab ci list
}

pipeline_view() {
    local pipeline_id="${1:-}"
    
    if [[ -n "$pipeline_id" ]]; then
        glab ci view "$pipeline_id"
    else
        glab ci view
    fi
}

pipeline_run() {
    local branch="${1:-}"
    
    echo -e "${BLUE}🚀 Triggering pipeline...${NC}"
    
    if [[ -n "$branch" ]]; then
        glab ci run --branch "$branch"
    else
        glab ci run
    fi
    
    echo -e "${GREEN}✅ Pipeline triggered${NC}"
}

# ─────────────────────────────────────────────────────────────
# REPO COMMANDS
# ─────────────────────────────────────────────────────────────

repo_view() {
    glab repo view --web
}

repo_clone() {
    local repo="$1"
    
    glab repo clone "$repo"
}

# ─────────────────────────────────────────────────────────────
# HELP
# ─────────────────────────────────────────────────────────────

show_help() {
    cat << 'EOF'
OCTALUME v2.3 - GitLab Integration

Usage:
  ./gitlab-integration.sh <command> <subcommand> [options]

Issue Commands:
  issue create <title> [body] [labels] [assignee]
  issue list [state] [labels]
  issue view <id>
  issue close <id>

Merge Request Commands:
  mr create [title] [description] [target] [--draft]
  mr list [state]
  mr view <id>
  mr merge <id> [--no-squash]
  mr checkout <id>

Pipeline Commands:
  pipeline status
  pipeline list
  pipeline view [id]
  pipeline run [branch]

Repository Commands:
  repo view
  repo clone <repo>

Examples:
  # Create an issue
  ./gitlab-integration.sh issue create "Fix login bug" "Users can't login" "bug,P6"

  # Create a merge request
  ./gitlab-integration.sh mr create "Add authentication" "Implements OAuth2"

  # Check pipeline status
  ./gitlab-integration.sh pipeline status

  # Merge an MR with squash
  ./gitlab-integration.sh mr merge 42

Configuration:
  Edit .claude/integrations/gitlab.json for custom settings.

EOF
}

# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────

main() {
    check_glab
    
    local command="${1:-help}"
    local subcommand="${2:-}"
    
    case "$command" in
        issue)
            case "$subcommand" in
                create)
                    issue_create "${3:-}" "${4:-}" "${5:-}" "${6:-}"
                    ;;
                list)
                    issue_list "${3:-opened}" "${4:-}"
                    ;;
                view)
                    issue_view "${3:?Issue ID required}"
                    ;;
                close)
                    issue_close "${3:?Issue ID required}"
                    ;;
                *)
                    echo "Unknown issue command: $subcommand"
                    echo "Available: create, list, view, close"
                    ;;
            esac
            ;;
        mr)
            case "$subcommand" in
                create)
                    local draft="false"
                    [[ "${6:-}" == "--draft" ]] && draft="true"
                    mr_create "${3:-}" "${4:-}" "${5:-main}" "$draft"
                    ;;
                list)
                    mr_list "${3:-opened}"
                    ;;
                view)
                    mr_view "${3:?MR ID required}"
                    ;;
                merge)
                    local squash="true"
                    [[ "${4:-}" == "--no-squash" ]] && squash="false"
                    mr_merge "${3:?MR ID required}" "$squash"
                    ;;
                checkout)
                    mr_checkout "${3:?MR ID required}"
                    ;;
                *)
                    echo "Unknown mr command: $subcommand"
                    echo "Available: create, list, view, merge, checkout"
                    ;;
            esac
            ;;
        pipeline)
            case "$subcommand" in
                status)
                    pipeline_status
                    ;;
                list)
                    pipeline_list
                    ;;
                view)
                    pipeline_view "${3:-}"
                    ;;
                run)
                    pipeline_run "${3:-}"
                    ;;
                *)
                    echo "Unknown pipeline command: $subcommand"
                    echo "Available: status, list, view, run"
                    ;;
            esac
            ;;
        repo)
            case "$subcommand" in
                view)
                    repo_view
                    ;;
                clone)
                    repo_clone "${3:?Repository required}"
                    ;;
                *)
                    echo "Unknown repo command: $subcommand"
                    echo "Available: view, clone"
                    ;;
            esac
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            echo "Unknown command: $command"
            show_help
            ;;
    esac
}

main "$@"
