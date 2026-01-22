#!/bin/bash
# .claude/memory/search.sh - Search memory bank

# Check for jq dependency
if ! command -v jq &> /dev/null; then
    echo '{"error": "jq is required but not installed. Install with: sudo apt install jq (Ubuntu) or brew install jq (macOS)"}'
    exit 1
fi

MEMORY_FILE=".claude/memory/memory.json"

# Check if memory file exists
if [ ! -f "$MEMORY_FILE" ]; then
    echo '{"error": "Memory file does not exist"}'
    exit 1
fi

# Parse arguments
CATEGORY="$1"
SEARCH_TERM="$2"

# Build jq query
if [ -n "$CATEGORY" ] && [ -n "$SEARCH_TERM" ]; then
    # Search within category for term
    jq -r --arg category "$CATEGORY" --arg term "$SEARCH_TERM" \
       '.memory[$category] | to_entries[] | select(.value.value | test($term; "i")) | .value' "$MEMORY_FILE"
elif [ -n "$CATEGORY" ]; then
    # List all in category
    jq -r --arg category "$CATEGORY" \
       '.memory[$category] | to_entries[] | .value' "$MEMORY_FILE"
elif [ -n "$SEARCH_TERM" ]; then
    # Search all categories for term
    jq -r --arg term "$SEARCH_TERM" \
       '.memory | to_entries[] | .value | to_entries[] | select(.value.value | test($term; "i")) | .value' "$MEMORY_FILE"
else
    # List all memory
    jq '.' "$MEMORY_FILE"
fi
