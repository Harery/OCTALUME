#!/bin/bash
#
# OCTALUME v2.1 - AI QA Review Session
# Orchestrates AI-powered quality assurance review
#
# Usage:
#   ./qa-ai-review.sh [phase] [--auto-fix]
#
# Options:
#   phase       Phase to review (P1-P8), defaults to current phase
#   --auto-fix  Attempt to auto-fix failed items
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
QA_DIR="$PROJECT_ROOT/.claude/qa"
MEMORY_FILE="$PROJECT_ROOT/.claude/memory/memory.json"
REPORTS_DIR="$QA_DIR/reports"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Configuration
PHASE="${1:-}"
AUTO_FIX=false

# Parse arguments
for arg in "$@"; do
    case $arg in
        --auto-fix)
            AUTO_FIX=true
            shift
            ;;
        P[1-8])
            PHASE="$arg"
            shift
            ;;
    esac
done

# Get current phase from memory if not specified
get_current_phase() {
    if [[ -f "$MEMORY_FILE" ]]; then
        local phase=$(jq -r '.context.current_phase // "P5"' "$MEMORY_FILE" 2>/dev/null)
        echo "${phase:-P5}"
    else
        echo "P5"
    fi
}

# Phase names
declare -A PHASE_NAMES=(
    ["P1"]="Vision and Strategy"
    ["P2"]="Requirements and Scope"
    ["P3"]="Architecture and Design"
    ["P4"]="Development Planning"
    ["P5"]="Development Execution"
    ["P6"]="Quality and Security"
    ["P7"]="Deployment and Release"
    ["P8"]="Operations and Maintenance"
)

# Load criteria for phase
load_criteria() {
    local phase="$1"
    local criteria_file="$QA_DIR/criteria/${phase}-criteria.json"
    
    if [[ ! -f "$criteria_file" ]]; then
        echo -e "${YELLOW}⚠️  No criteria file for $phase, using defaults${NC}"
        echo '{"phase":"'$phase'","required_files":[],"checks":[]}'
        return
    fi
    
    cat "$criteria_file"
}

# Get changed files
get_changed_files() {
    if git rev-parse --git-dir > /dev/null 2>&1; then
        # Get staged + unstaged changes
        git diff --name-only HEAD 2>/dev/null || git diff --name-only
    else
        echo ""
    fi
}

# Get git diff
get_diff_content() {
    if git rev-parse --git-dir > /dev/null 2>&1; then
        git diff HEAD 2>/dev/null | head -500 || git diff | head -500
    else
        echo "No git repository found"
    fi
}

# Generate the AI prompt
generate_prompt() {
    local phase="$1"
    local phase_name="${PHASE_NAMES[$phase]}"
    local criteria_file="$QA_DIR/criteria/${phase}-criteria.json"
    local changed_files=$(get_changed_files)
    local diff_content=$(get_diff_content)
    local criteria_content=$(load_criteria "$phase")
    
    # Read template
    local template=$(cat "$QA_DIR/ai-reviewer.md")
    
    # Replace placeholders
    template="${template//\{\{PHASE\}\}/$phase}"
    template="${template//\{\{PHASE_NAME\}\}/$phase_name}"
    template="${template//\{\{CRITERIA_FILE\}\}/$criteria_file}"
    template="${template//\{\{CHANGED_FILES\}\}/$changed_files}"
    template="${template//\{\{CRITERIA_CONTENT\}\}/$criteria_content}"
    template="${template//\{\{DIFF_CONTENT\}\}/$diff_content}"
    template="${template//\{\{FILE_LIST\}\}/$changed_files}"
    
    echo "$template"
}

# Save report
save_report() {
    local phase="$1"
    local report="$2"
    local timestamp=$(date +%Y%m%d_%H%M%S)
    
    mkdir -p "$REPORTS_DIR"
    
    local report_file="$REPORTS_DIR/${phase}_${timestamp}.json"
    echo "$report" > "$report_file"
    
    echo "$report_file"
}

# Display results
display_results() {
    local report="$1"
    
    echo ""
    echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${CYAN}                    AI QA REVIEW RESULTS                    ${NC}"
    echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
    echo ""
    
    # Parse JSON and display
    local verdict=$(echo "$report" | jq -r '.verdict // "UNKNOWN"')
    local summary=$(echo "$report" | jq -r '.summary // "No summary"')
    local passed=$(echo "$report" | jq -r '.score.passed // 0')
    local failed=$(echo "$report" | jq -r '.score.failed // 0')
    local warnings=$(echo "$report" | jq -r '.score.warnings // 0')
    local percentage=$(echo "$report" | jq -r '.score.percentage // 0')
    
    # Verdict with color
    case "$verdict" in
        PASS)
            echo -e "Verdict: ${GREEN}✅ PASS${NC}"
            ;;
        FAIL)
            echo -e "Verdict: ${RED}❌ FAIL${NC}"
            ;;
        NEEDS_REVIEW)
            echo -e "Verdict: ${YELLOW}⚠️  NEEDS REVIEW${NC}"
            ;;
        *)
            echo -e "Verdict: ${BLUE}❓ $verdict${NC}"
            ;;
    esac
    
    echo ""
    echo "Summary: $summary"
    echo ""
    echo -e "${BLUE}Score: $passed passed, $failed failed, $warnings warnings ($percentage%)${NC}"
    echo ""
    
    # Show failed items
    if [[ "$failed" -gt 0 ]]; then
        echo -e "${RED}Failed Items:${NC}"
        echo "$report" | jq -r '.failed[]? | "  ❌ \(.criterion)\n     Issue: \(.issue)\n     File: \(.file // "N/A")\n     Fix: \(.suggestion // "N/A")\n"'
    fi
    
    # Show warnings
    if [[ "$warnings" -gt 0 ]]; then
        echo -e "${YELLOW}Warnings:${NC}"
        echo "$report" | jq -r '.warnings[]? | "  ⚠️  \(.criterion)\n     \(.issue)\n     Recommendation: \(.recommendation // "N/A")\n"'
    fi
    
    # Show next steps
    echo -e "${CYAN}Next Steps:${NC}"
    echo "$report" | jq -r '.next_steps[]? | "  → \(.)"'
    
    echo ""
    echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
}

# Main
main() {
    # Determine phase
    if [[ -z "$PHASE" ]]; then
        PHASE=$(get_current_phase)
    fi
    
    local phase_name="${PHASE_NAMES[$PHASE]:-Unknown}"
    
    echo ""
    echo -e "${BLUE}🔍 OCTALUME AI QA Review${NC}"
    echo -e "   Phase: ${CYAN}$PHASE - $phase_name${NC}"
    echo -e "   Auto-fix: ${AUTO_FIX}"
    echo ""
    
    # Check for changes
    local changed_files=$(get_changed_files)
    if [[ -z "$changed_files" ]]; then
        echo -e "${YELLOW}⚠️  No changed files detected${NC}"
        echo "   The AI reviewer works best with uncommitted changes."
        echo ""
    fi
    
    # Generate prompt
    echo -e "${BLUE}📝 Generating review prompt...${NC}"
    local prompt=$(generate_prompt "$PHASE")
    
    # Save prompt for reference
    local prompt_file="$QA_DIR/.last-review-prompt.md"
    echo "$prompt" > "$prompt_file"
    echo -e "   Prompt saved to: $prompt_file"
    echo ""
    
    # Instructions for running with Claude
    echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}To run the AI review, use one of these methods:${NC}"
    echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
    echo ""
    echo -e "${CYAN}Option 1: Claude Code (Recommended)${NC}"
    echo "   In Claude Code, run:"
    echo "   /qa-ai-review"
    echo ""
    echo -e "${CYAN}Option 2: Copy prompt manually${NC}"
    echo "   Copy the content from: $prompt_file"
    echo "   Paste into Claude and get JSON response"
    echo "   Save response to: $REPORTS_DIR/${PHASE}_$(date +%Y%m%d_%H%M%S).json"
    echo ""
    echo -e "${CYAN}Option 3: API call${NC}"
    echo '   curl -X POST "https://api.anthropic.com/v1/messages" \'
    echo '     -H "x-api-key: $ANTHROPIC_API_KEY" \'
    echo '     -H "content-type: application/json" \'
    echo "     -d '{\"model\":\"claude-sonnet-4-20250514\",\"max_tokens\":4096,\"messages\":[{\"role\":\"user\",\"content\":\"...\"}]}'"
    echo ""
    
    # If there's a recent report, show it
    local latest_report=$(ls -t "$REPORTS_DIR/${PHASE}_"*.json 2>/dev/null | head -1)
    if [[ -n "$latest_report" ]]; then
        echo -e "${BLUE}📊 Latest report for $PHASE:${NC} $latest_report"
        echo ""
        
        read -p "Display latest report? [y/N] " -n 1 -r
        echo ""
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            display_results "$(cat "$latest_report")"
        fi
    fi
}

main "$@"
