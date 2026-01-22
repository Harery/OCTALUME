#!/bin/bash
#
# OCTALUME v2.3 - Linear Integration
# Wrapper for Linear API with OCTALUME conventions
#
# Usage:
#   ./linear-integration.sh issue create "Title" "Description"
#   ./linear-integration.sh issue list
#   ./linear-integration.sh sync
#
# Requires: LINEAR_API_KEY environment variable
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
CONFIG_FILE="$PROJECT_ROOT/.claude/integrations/linear.json"
CACHE_DIR="$PROJECT_ROOT/.claude/integrations/.linear-cache"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Linear API endpoint
LINEAR_API="https://api.linear.app/graphql"

# Check for API key
check_auth() {
    if [[ -z "${LINEAR_API_KEY:-}" ]]; then
        echo -e "${RED}❌ LINEAR_API_KEY not set${NC}"
        echo ""
        echo "Set your Linear API key:"
        echo "  export LINEAR_API_KEY='lin_api_...'"
        echo ""
        echo "Get your key from: https://linear.app/settings/api"
        exit 1
    fi
}

# GraphQL query helper
query_linear() {
    local query="$1"
    local variables="${2:-{}}"
    
    local response=$(curl -s -X POST "$LINEAR_API" \
        -H "Content-Type: application/json" \
        -H "Authorization: $LINEAR_API_KEY" \
        -d "{\"query\": \"$query\", \"variables\": $variables}")
    
    # Check for errors
    if echo "$response" | jq -e '.errors' > /dev/null 2>&1; then
        echo -e "${RED}❌ Linear API Error:${NC}" >&2
        echo "$response" | jq '.errors' >&2
        return 1
    fi
    
    echo "$response"
}

# Load configuration
load_config() {
    if [[ -f "$CONFIG_FILE" ]]; then
        cat "$CONFIG_FILE"
    else
        echo '{}'
    fi
}

# Initialize cache
init_cache() {
    mkdir -p "$CACHE_DIR"
}

# ─────────────────────────────────────────────────────────────
# TEAM & PROJECT COMMANDS
# ─────────────────────────────────────────────────────────────

list_teams() {
    echo -e "${BLUE}👥 Linear Teams${NC}"
    echo ""
    
    local query="query { teams { nodes { id name key } } }"
    local response=$(query_linear "$query")
    
    echo "$response" | jq -r '.data.teams.nodes[] | "\(.key)\t\(.name)\t\(.id)"' | column -t -s $'\t'
}

list_projects() {
    local team_key="${1:-}"
    
    echo -e "${BLUE}📁 Linear Projects${NC}"
    echo ""
    
    local query="query { projects(first: 50) { nodes { id name state teams { nodes { key } } } } }"
    local response=$(query_linear "$query")
    
    if [[ -n "$team_key" ]]; then
        echo "$response" | jq -r ".data.projects.nodes[] | select(.teams.nodes[].key == \"$team_key\") | \"\(.name)\t\(.state)\t\(.id)\"" | column -t -s $'\t'
    else
        echo "$response" | jq -r '.data.projects.nodes[] | "\(.name)\t\(.state)\t\(.id)"' | column -t -s $'\t'
    fi
}

# ─────────────────────────────────────────────────────────────
# ISSUE COMMANDS
# ─────────────────────────────────────────────────────────────

issue_create() {
    local title="$1"
    local description="${2:-}"
    local team_key="${3:-}"
    local priority="${4:-0}"
    
    echo -e "${BLUE}📝 Creating Linear issue...${NC}"
    
    # Get team ID if key provided
    local team_id=""
    if [[ -n "$team_key" ]]; then
        local teams_query="query { teams { nodes { id key } } }"
        local teams_response=$(query_linear "$teams_query")
        team_id=$(echo "$teams_response" | jq -r ".data.teams.nodes[] | select(.key == \"$team_key\") | .id")
    else
        # Use first team
        local teams_query="query { teams(first: 1) { nodes { id } } }"
        local teams_response=$(query_linear "$teams_query")
        team_id=$(echo "$teams_response" | jq -r '.data.teams.nodes[0].id')
    fi
    
    if [[ -z "$team_id" ]]; then
        echo -e "${RED}❌ Could not determine team${NC}"
        return 1
    fi
    
    # Escape for JSON
    local escaped_title=$(echo "$title" | sed 's/"/\\"/g')
    local escaped_desc=$(echo "$description" | sed 's/"/\\"/g' | sed ':a;N;$!ba;s/\n/\\n/g')
    
    local mutation="mutation { issueCreate(input: { teamId: \\\"$team_id\\\", title: \\\"$escaped_title\\\", description: \\\"$escaped_desc\\\", priority: $priority }) { success issue { id identifier title url } } }"
    
    local response=$(query_linear "$mutation")
    
    if echo "$response" | jq -e '.data.issueCreate.success' > /dev/null 2>&1; then
        local issue_id=$(echo "$response" | jq -r '.data.issueCreate.issue.identifier')
        local issue_url=$(echo "$response" | jq -r '.data.issueCreate.issue.url')
        
        echo -e "${GREEN}✅ Issue created: $issue_id${NC}"
        echo "   URL: $issue_url"
    else
        echo -e "${RED}❌ Failed to create issue${NC}"
        echo "$response" | jq '.'
    fi
}

issue_list() {
    local state="${1:-}"
    local limit="${2:-20}"
    
    echo -e "${BLUE}📋 Linear Issues${NC}"
    echo ""
    
    local filter=""
    if [[ -n "$state" ]]; then
        case "$state" in
            todo|Todo)
                filter="filter: { state: { type: { eq: \\\"unstarted\\\" } } }"
                ;;
            progress|"In Progress")
                filter="filter: { state: { type: { eq: \\\"started\\\" } } }"
                ;;
            done|Done)
                filter="filter: { state: { type: { eq: \\\"completed\\\" } } }"
                ;;
        esac
    fi
    
    local query="query { issues(first: $limit $filter) { nodes { identifier title state { name } priority assignee { name } } } }"
    local response=$(query_linear "$query")
    
    echo "$response" | jq -r '.data.issues.nodes[] | "\(.identifier)\t\(.title | .[0:40])\t\(.state.name)\tP\(.priority)\t\(.assignee.name // "-")"' | column -t -s $'\t'
}

issue_view() {
    local identifier="$1"
    
    local query="query { issue(id: \\\"$identifier\\\") { id identifier title description state { name } priority assignee { name } project { name } labels { nodes { name } } url createdAt } }"
    local response=$(query_linear "$query")
    
    echo ""
    echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
    echo "$response" | jq -r '.data.issue | "Issue: \(.identifier) - \(.title)\n\nState: \(.state.name)\nPriority: P\(.priority)\nAssignee: \(.assignee.name // "Unassigned")\nProject: \(.project.name // "None")\nLabels: \(.labels.nodes | map(.name) | join(", "))\n\nDescription:\n\(.description // "No description")\n\nURL: \(.url)"'
    echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
}

issue_update() {
    local identifier="$1"
    local field="$2"
    local value="$3"
    
    echo -e "${BLUE}✏️ Updating issue $identifier...${NC}"
    
    # First get the issue ID
    local get_query="query { issue(id: \\\"$identifier\\\") { id } }"
    local get_response=$(query_linear "$get_query")
    local issue_id=$(echo "$get_response" | jq -r '.data.issue.id')
    
    local update_field=""
    case "$field" in
        title)
            update_field="title: \\\"$value\\\""
            ;;
        priority)
            update_field="priority: $value"
            ;;
        state)
            # Would need to get state ID
            echo "State update not yet implemented"
            return 1
            ;;
    esac
    
    local mutation="mutation { issueUpdate(id: \\\"$issue_id\\\", input: { $update_field }) { success } }"
    local response=$(query_linear "$mutation")
    
    if echo "$response" | jq -e '.data.issueUpdate.success' > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Issue updated${NC}"
    else
        echo -e "${RED}❌ Failed to update issue${NC}"
    fi
}

# ─────────────────────────────────────────────────────────────
# SYNC COMMANDS
# ─────────────────────────────────────────────────────────────

sync_to_memory() {
    echo -e "${BLUE}🔄 Syncing Linear to OCTALUME memory...${NC}"
    
    init_cache
    
    # Get all issues assigned to me
    local query="query { viewer { assignedIssues(first: 100) { nodes { identifier title description state { name } priority project { name } labels { nodes { name } } } } } }"
    local response=$(query_linear "$query")
    
    # Save to cache
    echo "$response" > "$CACHE_DIR/my-issues.json"
    
    local count=$(echo "$response" | jq '.data.viewer.assignedIssues.nodes | length')
    echo -e "${GREEN}✅ Synced $count issues to cache${NC}"
    
    # Could integrate with memory.json here
    # For now, just cache the data
}

# ─────────────────────────────────────────────────────────────
# HELP
# ─────────────────────────────────────────────────────────────

show_help() {
    cat << 'EOF'
OCTALUME v2.3 - Linear Integration

Usage:
  ./linear-integration.sh <command> [options]

Team & Project Commands:
  teams                         List all teams
  projects [team-key]           List projects

Issue Commands:
  issue create <title> [desc] [team] [priority]
  issue list [state] [limit]
  issue view <identifier>
  issue update <id> <field> <value>

Sync Commands:
  sync                          Sync Linear data to local cache

States: todo, progress, done
Priority: 0 (none), 1 (urgent), 2 (high), 3 (medium), 4 (low)

Examples:
  # List teams
  ./linear-integration.sh teams

  # Create an issue
  ./linear-integration.sh issue create "Fix bug" "Description here" ENG 2

  # List in-progress issues
  ./linear-integration.sh issue list progress

  # View an issue
  ./linear-integration.sh issue view ENG-123

Environment:
  LINEAR_API_KEY    Your Linear API key (required)

Get your API key from: https://linear.app/settings/api

EOF
}

# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────

main() {
    local command="${1:-help}"
    
    # Help doesn't need auth
    if [[ "$command" == "help" ]] || [[ "$command" == "--help" ]] || [[ "$command" == "-h" ]]; then
        show_help
        exit 0
    fi
    
    check_auth
    
    case "$command" in
        teams)
            list_teams
            ;;
        projects)
            list_projects "${2:-}"
            ;;
        issue)
            local subcommand="${2:-list}"
            case "$subcommand" in
                create)
                    issue_create "${3:?Title required}" "${4:-}" "${5:-}" "${6:-0}"
                    ;;
                list)
                    issue_list "${3:-}" "${4:-20}"
                    ;;
                view)
                    issue_view "${3:?Issue identifier required}"
                    ;;
                update)
                    issue_update "${3:?ID required}" "${4:?Field required}" "${5:?Value required}"
                    ;;
                *)
                    echo "Unknown issue command: $subcommand"
                    ;;
            esac
            ;;
        sync)
            sync_to_memory
            ;;
        *)
            echo "Unknown command: $command"
            show_help
            ;;
    esac
}

main "$@"
