#!/bin/bash
# .claude/memory/load.sh - Load entry from memory bank

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
KEY="$1"
CATEGORY="$2"

# Validate key argument
if [ -z "$KEY" ]; then
    echo '{"error": "Missing required argument: key"}'
    exit 1
fi

# If category specified, search in specific category
if [ -n "$CATEGORY" ]; then
    # Validate category
    if [[ ! "$CATEGORY" =~ ^(decision|progress|blocker|note)$ ]]; then
        echo '{"error": "Category must be: decision, progress, blocker, or note"}'
        exit 1
    fi
    jq -r --arg key "$KEY" --arg category "$CATEGORY" \
       '.memory[$category][$key] // empty' "$MEMORY_FILE"
else
    # Search in all categories
    jq -r --arg key "$KEY" '
        .memory.decisions[$key] //
        .memory.progress[$key] //
        .memory.blockers[$key] //
        .memory.notes[$key] //
        empty
    ' "$MEMORY_FILE"
fi
