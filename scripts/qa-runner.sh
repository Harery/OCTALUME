#!/bin/bash
# OCTALUME v2.0 - Automated QA Runner
# Comprehensive quality assurance validation system
# Compatible with Claude Code CLI

set -e

QA_DIR="${QA_DIR:-.claude/qa}"
CRITERIA_DIR="$QA_DIR/criteria"
REPORTS_DIR="$QA_DIR/reports"
CONFIG_FILE="$QA_DIR/config.json"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m'

# Counters
PASSED=0
FAILED=0
SKIPPED=0
WARNINGS=0

# Initialize QA
init_qa() {
    mkdir -p "$REPORTS_DIR"
    echo -e "${BLUE}🔍 OCTALUME v2.0 QA Runner${NC}"
    echo "================================="
}

# Check if command exists
command_exists() {
    command -v "$1" &> /dev/null
}

# Run a command check
run_command_check() {
    local cmd="$1"
    local timeout="${2:-60}"
    local skip_if_missing="${3:-false}"
    
    # Extract base command
    local base_cmd=$(echo "$cmd" | awk '{print $1}')
    
    # Check if npm script
    if [[ "$cmd" == npm\ run* ]]; then
        local script=$(echo "$cmd" | sed 's/npm run //')
        if ! grep -q "\"$script\"" package.json 2>/dev/null; then
            if [ "$skip_if_missing" = "true" ]; then
                return 2  # Skip
            fi
            return 1  # Fail
        fi
    fi
    
    # Run with timeout
    if timeout "$timeout" bash -c "$cmd" > /dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

# Run a grep check
run_grep_check() {
    local pattern="$1"
    local max_matches="${2:-0}"
    local exclude="${3:-}"
    local include="${4:-}"
    
    local exclude_args=""
    if [ -n "$exclude" ]; then
        for exc in $exclude; do
            exclude_args="$exclude_args --exclude=$exc"
        done
    fi
    
    local include_args=""
    if [ -n "$include" ]; then
        include_args="--include=$include"
    fi
    
    local count=$(grep -rE "$pattern" . $exclude_args $include_args 2>/dev/null | wc -l || echo 0)
    
    if [ "$count" -le "$max_matches" ]; then
        return 0
    else
        echo "$count matches found (max: $max_matches)"
        return 1
    fi
}

# Check file exists
check_file_exists() {
    local file="$1"
    [ -f "$file" ]
}

# Check directory exists
check_directory_exists() {
    local dir="$1"
    [ -d "$dir" ]
}

# Check file contains patterns
check_file_contains() {
    local file="$1"
    shift
    local patterns=("$@")
    
    if [ ! -f "$file" ]; then
        return 1
    fi
    
    for pattern in "${patterns[@]}"; do
        if ! grep -q "$pattern" "$file" 2>/dev/null; then
            return 1
        fi
    done
    return 0
}

# Run phase criteria
run_phase() {
    local phase="$1"
    local criteria_file="$CRITERIA_DIR/${phase}-criteria.json"
    
    if [ ! -f "$criteria_file" ]; then
        echo -e "${YELLOW}⚠ No criteria file for $phase${NC}"
        return
    fi
    
    echo ""
    echo -e "${MAGENTA}━━━ Phase $phase ━━━${NC}"
    
    local phase_name=$(jq -r '.name' "$criteria_file")
    echo -e "${CYAN}$phase_name${NC}"
    echo ""
    
    # Process each criterion
    local criteria_count=$(jq '.criteria | length' "$criteria_file")
    
    for ((i=0; i<criteria_count; i++)); do
        local id=$(jq -r ".criteria[$i].id" "$criteria_file")
        local name=$(jq -r ".criteria[$i].name" "$criteria_file")
        local type=$(jq -r ".criteria[$i].type" "$criteria_file")
        local required=$(jq -r ".criteria[$i].required" "$criteria_file")
        
        printf "  %-40s" "$name"
        
        local result=0
        case "$type" in
            command)
                local cmd=$(jq -r ".criteria[$i].check.command" "$criteria_file")
                local timeout=$(jq -r ".criteria[$i].check.timeout // 60" "$criteria_file")
                local skip=$(jq -r ".criteria[$i].check.skipIfMissing // false" "$criteria_file")
                run_command_check "$cmd" "$timeout" "$skip"
                result=$?
                ;;
            file)
                local file=$(jq -r ".criteria[$i].check.file // empty" "$criteria_file")
                local any_of=$(jq -r ".criteria[$i].check.anyOf // empty" "$criteria_file")
                
                if [ -n "$file" ]; then
                    check_file_exists "$file"
                    result=$?
                elif [ -n "$any_of" ]; then
                    result=1
                    for f in $(echo "$any_of" | jq -r '.[]'); do
                        if check_file_exists "$f"; then
                            result=0
                            break
                        fi
                    done
                fi
                ;;
            structure)
                local dirs=$(jq -r ".criteria[$i].check.directories // empty" "$criteria_file")
                if [ -n "$dirs" ]; then
                    result=0
                    for dir in $(echo "$dirs" | jq -r '.[]'); do
                        if ! check_directory_exists "$dir"; then
                            result=1
                            break
                        fi
                    done
                fi
                ;;
            grep)
                local pattern=$(jq -r ".criteria[$i].check.pattern // .criteria[$i].check.patterns[0]" "$criteria_file")
                local max=$(jq -r ".criteria[$i].check.maxMatches // 0" "$criteria_file")
                run_grep_check "$pattern" "$max"
                result=$?
                ;;
            git)
                if [ -d ".git" ]; then
                    result=0
                else
                    result=1
                fi
                ;;
            *)
                result=2  # Skip unknown types
                ;;
        esac
        
        case $result in
            0)
                echo -e "${GREEN}✓ PASS${NC}"
                ((PASSED++))
                ;;
            1)
                if [ "$required" = "true" ]; then
                    echo -e "${RED}✗ FAIL${NC}"
                    ((FAILED++))
                else
                    echo -e "${YELLOW}⚠ WARN${NC}"
                    ((WARNINGS++))
                fi
                ;;
            2)
                echo -e "${CYAN}○ SKIP${NC}"
                ((SKIPPED++))
                ;;
        esac
    done
}

# Generate report
generate_report() {
    local phase="$1"
    local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    local report_file="$REPORTS_DIR/qa-report-${phase:-all}-$(date +%Y%m%d%H%M%S).json"
    
    local total=$((PASSED + FAILED + SKIPPED))
    local score=0
    if [ $total -gt 0 ]; then
        score=$((PASSED * 100 / (PASSED + FAILED)))
    fi
    
    cat > "$report_file" << EOF
{
  "timestamp": "$timestamp",
  "phase": "${phase:-all}",
  "summary": {
    "passed": $PASSED,
    "failed": $FAILED,
    "skipped": $SKIPPED,
    "warnings": $WARNINGS,
    "total": $total,
    "score": $score
  },
  "status": "$([ $FAILED -eq 0 ] && echo 'pass' || echo 'fail')"
}
EOF
    
    echo ""
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}📊 QA Summary${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo -e "  ${GREEN}Passed:${NC}   $PASSED"
    echo -e "  ${RED}Failed:${NC}   $FAILED"
    echo -e "  ${YELLOW}Warnings:${NC} $WARNINGS"
    echo -e "  ${CYAN}Skipped:${NC}  $SKIPPED"
    echo ""
    echo -e "  ${MAGENTA}Score:${NC}    ${score}%"
    echo ""
    
    if [ $FAILED -eq 0 ]; then
        echo -e "${GREEN}✓ All required checks passed!${NC}"
    else
        echo -e "${RED}✗ $FAILED required check(s) failed${NC}"
    fi
    
    echo ""
    echo -e "Report saved: $report_file"
}

# Auto-fix common issues
auto_fix() {
    echo -e "${BLUE}🔧 Attempting auto-fix...${NC}"
    echo ""
    
    local fixed=0
    
    # Fix lint issues
    if command_exists npx && [ -f "package.json" ]; then
        if grep -q '"lint:fix"' package.json 2>/dev/null; then
            echo -e "  Running lint:fix..."
            npm run lint:fix 2>/dev/null && ((fixed++)) || true
        elif grep -q '"lint"' package.json 2>/dev/null; then
            if grep -q "eslint" package.json 2>/dev/null; then
                echo -e "  Running eslint --fix..."
                npx eslint . --fix 2>/dev/null && ((fixed++)) || true
            fi
        fi
    fi
    
    # Fix formatting
    if command_exists npx; then
        if [ -f ".prettierrc" ] || [ -f ".prettierrc.json" ]; then
            echo -e "  Running prettier..."
            npx prettier --write . 2>/dev/null && ((fixed++)) || true
        fi
    fi
    
    echo ""
    if [ $fixed -gt 0 ]; then
        echo -e "${GREEN}✓ Applied $fixed auto-fixes${NC}"
        echo -e "  Run QA again to verify: ${CYAN}./scripts/qa-runner.sh${NC}"
    else
        echo -e "${YELLOW}⚠ No auto-fixes available${NC}"
    fi
}

# Show status of last run
show_status() {
    local latest=$(ls -t "$REPORTS_DIR"/qa-report-*.json 2>/dev/null | head -1)
    
    if [ -z "$latest" ]; then
        echo -e "${YELLOW}No QA reports found. Run QA first:${NC}"
        echo -e "  ${CYAN}./scripts/qa-runner.sh${NC}"
        return
    fi
    
    echo -e "${BLUE}📊 Last QA Report${NC}"
    echo "================="
    echo ""
    
    local timestamp=$(jq -r '.timestamp' "$latest")
    local phase=$(jq -r '.phase' "$latest")
    local passed=$(jq -r '.summary.passed' "$latest")
    local failed=$(jq -r '.summary.failed' "$latest")
    local score=$(jq -r '.summary.score' "$latest")
    local status=$(jq -r '.status' "$latest")
    
    echo -e "  Time:    $timestamp"
    echo -e "  Phase:   $phase"
    echo -e "  Passed:  ${GREEN}$passed${NC}"
    echo -e "  Failed:  ${RED}$failed${NC}"
    echo -e "  Score:   ${MAGENTA}${score}%${NC}"
    echo ""
    
    if [ "$status" = "pass" ]; then
        echo -e "  Status:  ${GREEN}✓ PASS${NC}"
    else
        echo -e "  Status:  ${RED}✗ FAIL${NC}"
    fi
}

# Show help
show_help() {
    echo -e "${BLUE}OCTALUME v2.0 - QA Runner${NC}"
    echo "=========================="
    echo ""
    echo "Usage: qa-runner.sh [command] [options]"
    echo ""
    echo "Commands:"
    echo "  run [phase]    Run QA checks (all phases or specific P1-P8)"
    echo "  fix            Attempt to auto-fix common issues"
    echo "  status         Show status of last QA run"
    echo "  help           Show this help"
    echo ""
    echo "Examples:"
    echo "  ./scripts/qa-runner.sh run        # Run all phases"
    echo "  ./scripts/qa-runner.sh run P3     # Run only P3 (Development)"
    echo "  ./scripts/qa-runner.sh fix        # Auto-fix issues"
    echo "  ./scripts/qa-runner.sh status     # Check last run"
    echo ""
    echo "Phases:"
    echo "  P1 - Project Initialization"
    echo "  P2 - Requirements & Planning"
    echo "  P3 - Development"
    echo "  P4 - Testing"
    echo "  P5 - Security & Compliance"
    echo "  P6 - Documentation"
    echo "  P7 - Deployment"
    echo "  P8 - Maintenance & Monitoring"
}

# Main
main() {
    local command="${1:-run}"
    local phase="$2"
    
    init_qa
    
    case "$command" in
        run)
            if [ -n "$phase" ]; then
                run_phase "$phase"
            else
                for p in P1 P2 P3 P4 P5 P6 P7 P8; do
                    if [ -f "$CRITERIA_DIR/${p}-criteria.json" ]; then
                        run_phase "$p"
                    fi
                done
            fi
            generate_report "$phase"
            ;;
        fix)
            auto_fix
            ;;
        status)
            show_status
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            echo -e "${RED}Unknown command: $command${NC}"
            show_help
            exit 1
            ;;
    esac
}

main "$@"
