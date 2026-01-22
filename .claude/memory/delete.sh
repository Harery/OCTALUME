#!/bin/bash
# .claude/memory/delete.sh - Delete entry from memory bank

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

# If category specified, delete from specific category
if [ -n "$CATEGORY" ]; then
    # Validate category
    if [[ ! "$CATEGORY" =~ ^(decision|progress|blocker|note)$ ]]; then
        echo '{"error": "Category must be: decision, progress, blocker, or note"}'
        exit 1
    fi

    # Check if key exists
    if ! jq -e --arg key "$KEY" --arg category "$CATEGORY" '.memory[$category][$key]' "$MEMORY_FILE" > /dev/null 2>&1; then
        echo "{\"error\": \"Key '$KEY' not found in category '$CATEGORY'\"}"
        exit 1
    fi

    # Delete entry and update statistics
    TMP_FILE=$(mktemp)
    jq --arg key "$KEY" --arg category "$CATEGORY" \
       'del(.memory[$category][$key]) |
        .statistics.total_entries = (.statistics.total_entries - 1) |
        if ($category == "decision") then
            .statistics.decisions = (.statistics.decisions - 1)
        elif ($category == "progress") then
            .statistics.progress = (.statistics.progress - 1)
        elif ($category == "blocker") then
            .statistics.blockers = (.statistics.blockers - 1)
        elif ($category == "note") then
            .statistics.notes = (.statistics.notes - 1)
        end |
        .updated_at = (now | strftime("%Y-%m-%dT%H:%M:%SZ"))
        ' "$MEMORY_FILE" > "$TMP_FILE"

    if [ $? -eq 0 ]; then
        mv "$TMP_FILE" "$MEMORY_FILE"
        echo "{\"success\": true, \"deleted\": \"$KEY\", \"category\": \"$CATEGORY\"}"
    else
        rm -f "$TMP_FILE"
        echo '{"error": "Failed to delete memory entry"}'
        exit 1
    fi
else
    # Search and delete from any category
    FOUND_CATEGORY=""
    for cat in decision progress blocker note; do
        if jq -e --arg key "$KEY" ".memory.$cat[$key]" "$MEMORY_FILE" > /dev/null 2>&1; then
            FOUND_CATEGORY="$cat"
            break
        fi
    done

    if [ -z "$FOUND_CATEGORY" ]; then
        echo "{\"error\": \"Key '$KEY' not found in any category\"}"
        exit 1
    fi

    # Delete from found category
    TMP_FILE=$(mktemp)
    jq --arg key "$KEY" --arg category "$FOUND_CATEGORY" \
       'del(.memory[$category][$key]) |
        .statistics.total_entries = (.statistics.total_entries - 1) |
        if ($category == "decision") then
            .statistics.decisions = (.statistics.decisions - 1)
        elif ($category == "progress") then
            .statistics.progress = (.statistics.progress - 1)
        elif ($category == "blocker") then
            .statistics.blockers = (.statistics.blockers - 1)
        elif ($category == "note") then
            .statistics.notes = (.statistics.notes - 1)
        end |
        .updated_at = (now | strftime("%Y-%m-%dT%H:%M:%SZ"))
        ' "$MEMORY_FILE" > "$TMP_FILE"

    if [ $? -eq 0 ]; then
        mv "$TMP_FILE" "$MEMORY_FILE"
        echo "{\"success\": true, \"deleted\": \"$KEY\", \"category\": \"$FOUND_CATEGORY\"}"
    else
        rm -f "$TMP_FILE"
        echo '{"error": "Failed to delete memory entry"}'
        exit 1
    fi
fi
