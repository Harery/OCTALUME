#!/bin/bash
# OCTALUME v2.0 - Changelog Generator
# Automatic changelog generation from git commits
# Compatible with Claude Code CLI

set -e

CHANGELOG_FILE="${CHANGELOG_FILE:-CHANGELOG.md}"
VERSION_FILE="${VERSION_FILE:-package.json}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m'

# Commit type mapping
declare -A TYPE_MAP=(
    ["feat"]="Added"
    ["feature"]="Added"
    ["add"]="Added"
    ["fix"]="Fixed"
    ["bugfix"]="Fixed"
    ["bug"]="Fixed"
    ["change"]="Changed"
    ["update"]="Changed"
    ["refactor"]="Changed"
    ["perf"]="Changed"
    ["docs"]="Documentation"
    ["doc"]="Documentation"
    ["style"]="Changed"
    ["test"]="Testing"
    ["tests"]="Testing"
    ["chore"]="Maintenance"
    ["build"]="Maintenance"
    ["ci"]="Maintenance"
    ["remove"]="Removed"
    ["delete"]="Removed"
    ["deprecate"]="Deprecated"
    ["security"]="Security"
    ["breaking"]="Breaking Changes"
)

# Get current version
get_version() {
    if [ -f "package.json" ]; then
        grep -oP '"version":\s*"\K[^"]+' package.json 2>/dev/null || echo "0.0.0"
    elif [ -f "Cargo.toml" ]; then
        grep -oP '^version\s*=\s*"\K[^"]+' Cargo.toml 2>/dev/null || echo "0.0.0"
    elif [ -f "pyproject.toml" ]; then
        grep -oP '^version\s*=\s*"\K[^"]+' pyproject.toml 2>/dev/null || echo "0.0.0"
    else
        echo "0.0.0"
    fi
}

# Parse commit type from message
parse_commit_type() {
    local message="$1"
    local type="Other"
    
    # Conventional commits: type(scope): description
    local pattern='^([a-z]+)(\([^)]+\))?:.*'
    if [[ "$message" =~ $pattern ]]; then
        local commit_type="${BASH_REMATCH[1]}"
        type="${TYPE_MAP[$commit_type]:-Other}"
    # Issue reference: #123 description or (fixes #123)
    elif [[ "$message" == *"#"* ]]; then
        type="Fixed"
    fi
    
    echo "$type"
}

# Parse commit message (remove type prefix)
parse_commit_message() {
    local message="$1"
    
    # Remove conventional commit prefix
    local pattern='^[a-z]+(\([^)]+\))?:[[:space:]]*(.*)'
    if [[ "$message" =~ $pattern ]]; then
        echo "${BASH_REMATCH[2]}"
    else
        echo "$message"
    fi
}

# Get commits since last tag
get_commits_since_tag() {
    local tag="$1"
    
    if [ -n "$tag" ] && git rev-parse "$tag" &>/dev/null; then
        git log "$tag"..HEAD --oneline --pretty=format:"%h|%s|%an|%ai" 2>/dev/null
    else
        git log --oneline --pretty=format:"%h|%s|%an|%ai" 2>/dev/null
    fi
}

# Get latest tag
get_latest_tag() {
    git describe --tags --abbrev=0 2>/dev/null || echo ""
}

# Generate changelog content
generate_changelog() {
    local version="$1"
    local since_tag="$2"
    local date=$(date +%Y-%m-%d)
    
    echo -e "${BLUE}📝 Generating Changelog${NC}"
    echo "======================="
    echo ""
    
    # Group commits by type
    declare -A GROUPS
    
    while IFS='|' read -r hash message author commit_date; do
        [ -z "$hash" ] && continue
        
        local type=$(parse_commit_type "$message")
        local clean_message=$(parse_commit_message "$message")
        
        GROUPS[$type]+="- $clean_message (\`$hash\`)"$'\n'
    done <<< "$(get_commits_since_tag "$since_tag")"
    
    # Build changelog entry
    local entry=""
    entry+="## [$version] - $date"$'\n\n'
    
    # Order: Breaking, Added, Changed, Deprecated, Removed, Fixed, Security, Documentation, Testing, Maintenance, Other
    local order=("Breaking Changes" "Added" "Changed" "Deprecated" "Removed" "Fixed" "Security" "Documentation" "Testing" "Maintenance" "Other")
    
    for section in "${order[@]}"; do
        if [ -n "${GROUPS[$section]}" ]; then
            entry+="### $section"$'\n\n'
            entry+="${GROUPS[$section]}"$'\n'
        fi
    done
    
    echo "$entry"
}

# Write to changelog file
write_changelog() {
    local version="$1"
    local since_tag="$2"
    
    local new_content=$(generate_changelog "$version" "$since_tag")
    
    if [ -f "$CHANGELOG_FILE" ]; then
        # Insert after header
        local temp_file=$(mktemp)
        
        # Read existing content
        local header_found=false
        local after_header=false
        
        while IFS= read -r line; do
            if ! $header_found && [[ "$line" =~ ^#\ Changelog ]]; then
                echo "$line" >> "$temp_file"
                header_found=true
            elif $header_found && ! $after_header && [[ "$line" =~ ^## ]]; then
                echo "" >> "$temp_file"
                echo "$new_content" >> "$temp_file"
                echo "$line" >> "$temp_file"
                after_header=true
            else
                echo "$line" >> "$temp_file"
            fi
        done < "$CHANGELOG_FILE"
        
        # If no existing version entry found, append after header
        if ! $after_header; then
            echo "" >> "$temp_file"
            echo "$new_content" >> "$temp_file"
        fi
        
        mv "$temp_file" "$CHANGELOG_FILE"
    else
        # Create new changelog
        cat > "$CHANGELOG_FILE" << EOF
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

$new_content
EOF
    fi
    
    echo -e "${GREEN}✓ Changelog updated: $CHANGELOG_FILE${NC}"
}

# Preview changelog without writing
preview_changelog() {
    local version="${1:-$(get_version)}"
    local since_tag="${2:-$(get_latest_tag)}"
    
    echo -e "${BLUE}📝 Changelog Preview${NC}"
    echo "===================="
    echo ""
    
    generate_changelog "$version" "$since_tag"
}

# Bump version
bump_version() {
    local bump_type="${1:-patch}"
    local current=$(get_version)
    
    IFS='.' read -r major minor patch <<< "$current"
    
    case "$bump_type" in
        major)
            major=$((major + 1))
            minor=0
            patch=0
            ;;
        minor)
            minor=$((minor + 1))
            patch=0
            ;;
        patch)
            patch=$((patch + 1))
            ;;
        *)
            echo -e "${RED}Invalid bump type: $bump_type${NC}"
            echo "Use: major, minor, or patch"
            exit 1
            ;;
    esac
    
    local new_version="$major.$minor.$patch"
    
    echo -e "${BLUE}📦 Version Bump${NC}"
    echo -e "   Current: ${YELLOW}$current${NC}"
    echo -e "   New:     ${GREEN}$new_version${NC}"
    
    echo "$new_version"
}

# Full release flow
release() {
    local bump_type="${1:-patch}"
    local new_version=$(bump_version "$bump_type")
    local latest_tag=$(get_latest_tag)
    
    echo ""
    echo -e "${MAGENTA}━━━ Release $new_version ━━━${NC}"
    echo ""
    
    # Update version in package.json if exists
    if [ -f "package.json" ]; then
        if command -v jq &> /dev/null; then
            local temp_file=$(mktemp)
            jq --arg v "$new_version" '.version = $v' package.json > "$temp_file" && mv "$temp_file" package.json
            echo -e "${GREEN}✓ Updated package.json version${NC}"
        else
            sed -i "s/\"version\":\s*\"[^\"]*\"/\"version\": \"$new_version\"/" package.json
            echo -e "${GREEN}✓ Updated package.json version${NC}"
        fi
    fi
    
    # Generate changelog
    write_changelog "$new_version" "$latest_tag"
    
    echo ""
    echo -e "${CYAN}Next steps:${NC}"
    echo "  1. Review changes: ${CYAN}git diff${NC}"
    echo "  2. Commit: ${CYAN}git add -A && git commit -m \"chore: release v$new_version\"${NC}"
    echo "  3. Tag: ${CYAN}git tag -a v$new_version -m \"Release v$new_version\"${NC}"
    echo "  4. Push: ${CYAN}git push && git push --tags${NC}"
}

# List recent commits
list_commits() {
    local count="${1:-20}"
    local since_tag=$(get_latest_tag)
    
    echo -e "${BLUE}📋 Recent Commits${NC}"
    if [ -n "$since_tag" ]; then
        echo -e "Since tag: ${CYAN}$since_tag${NC}"
    fi
    echo "=================="
    echo ""
    
    get_commits_since_tag "$since_tag" | head -n "$count" | while IFS='|' read -r hash message author date; do
        local type=$(parse_commit_type "$message")
        printf "${GREEN}%s${NC} [${YELLOW}%-12s${NC}] %s\n" "$hash" "$type" "$message"
    done
}

# Show help
show_help() {
    echo -e "${BLUE}OCTALUME v2.0 - Changelog Generator${NC}"
    echo "====================================="
    echo ""
    echo "Commands:"
    echo "  generate [version]     Generate changelog for version"
    echo "  preview [version]      Preview changelog without writing"
    echo "  release [major|minor|patch]  Full release with version bump"
    echo "  commits [count]        List recent commits"
    echo "  version                Show current version"
    echo "  help                   Show this help"
    echo ""
    echo "Commit Conventions (Conventional Commits):"
    echo "  feat:     New feature → Added"
    echo "  fix:      Bug fix → Fixed"
    echo "  docs:     Documentation → Documentation"
    echo "  refactor: Code change → Changed"
    echo "  test:     Tests → Testing"
    echo "  chore:    Maintenance → Maintenance"
    echo "  breaking: Breaking change → Breaking Changes"
    echo ""
    echo "Examples:"
    echo "  ./scripts/changelog-generator.sh preview"
    echo "  ./scripts/changelog-generator.sh generate 1.2.0"
    echo "  ./scripts/changelog-generator.sh release minor"
    echo "  ./scripts/changelog-generator.sh commits 30"
}

# Main
case "${1:-help}" in
    generate)
        version="${2:-$(get_version)}"
        write_changelog "$version" "$(get_latest_tag)"
        ;;
    preview)
        preview_changelog "$2" "$3"
        ;;
    release)
        release "$2"
        ;;
    commits)
        list_commits "$2"
        ;;
    version)
        echo "Current version: $(get_version)"
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
