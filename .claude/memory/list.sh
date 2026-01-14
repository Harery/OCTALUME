#!/bin/bash
# .claude/memory/list.sh - List memory entries

MEMORY_FILE=".claude/memory/memory.json"

# Check if memory file exists
if [ ! -f "$MEMORY_FILE" ]; then
    echo '{"error": "Memory file does not exist"}'
    exit 1
fi

# Parse arguments
FORMAT="${1:-json}"
CATEGORY="${2:-}"

# Validate format
if [[ ! "$FORMAT" =~ ^(json|compact|summary)$ ]]; then
    echo '{"error": "Format must be: json, compact, or summary"}'
    exit 1
fi

case "$FORMAT" in
    json)
        if [ -n "$CATEGORY" ]; then
            jq -r --arg category "$CATEGORY" '.memory[$category]' "$MEMORY_FILE"
        else
            jq '.' "$MEMORY_FILE"
        fi
        ;;
    compact)
        if [ -n "$CATEGORY" ]; then
            jq -r --arg category "$CATEGORY" '.memory[$category] | to_entries[] | "\(.key): \(.value)"' "$MEMORY_FILE"
        else
            jq -r '.memory | to_entries[] | "\(.key): \(.value | length) entries"' "$MEMORY_FILE"
        fi
        ;;
    summary)
        echo "Memory Summary:"
        echo "================"
        jq -r '.statistics | to_entries[] | "- \(.key | ascii_upcase): \(.value)"' "$MEMORY_FILE"
        echo ""
        echo "Recent entries (last 10):"
        jq -r '.memory | to_entries[].value | to_entries[] | .value | select(.timestamp != null) | "\(.timestamp): \(.key) = \(.value)"' "$MEMORY_FILE" | sort -r | head -10
        ;;
esac
