#!/bin/bash
# .claude/memory/save.sh - Save entry to memory bank

# Check for jq dependency
if ! command -v jq &> /dev/null; then
    echo '{"error": "jq is required but not installed. Install with: sudo apt install jq (Ubuntu) or brew install jq (macOS)"}'
    exit 1
fi

MEMORY_FILE=".claude/memory/memory.json"
MEMORY_DIR=$(dirname "$MEMORY_FILE")

# Ensure memory file exists
mkdir -p "$MEMORY_DIR"
if [ ! -f "$MEMORY_FILE" ]; then
    cat > "$MEMORY_FILE" <<'EOF'
{
  "version": "1.0.0",
  "created_at": null,
  "updated_at": null,
  "memory": {
    "decisions": {},
    "progress": {},
    "blockers": {},
    "notes": {}
  },
  "statistics": {
    "total_entries": 0,
    "decisions": 0,
    "progress": 0,
    "blockers": 0,
    "notes": 0
  }
}
EOF
fi

# Parse arguments
KEY="$1"
VALUE="$2"
CATEGORY="$3"
CONTEXT="${4:-}"
PHASE="${5:-}"

# Validate required arguments
if [ -z "$KEY" ] || [ -z "$VALUE" ] || [ -z "$CATEGORY" ]; then
    echo '{"error": "Missing required arguments: key, value, category"}'
    exit 1
fi

# Validate category
if [[ ! "$CATEGORY" =~ ^(decision|progress|blocker|note)$ ]]; then
    echo '{"error": "Category must be: decision, progress, blocker, or note"}'
    exit 1
fi

# Get current timestamp
TIMESTAMP=$(date -Iseconds)

# Update memory file using jq
TMP_FILE=$(mktemp)
jq --arg key "$KEY" \
   --arg value "$VALUE" \
   --arg category "$CATEGORY" \
   --arg context "$CONTEXT" \
   --arg phase "$PHASE" \
   --arg timestamp "$TIMESTAMP" \
   '
   .created_at = if .created_at == null then $timestamp else .created_at end |
   .updated_at = $timestamp |
   .memory[$category][$key] = {
     "key": $key,
     "value": $value,
     "category": $category,
     "timestamp": $timestamp,
     "context": $context,
     "phase": $phase
   } |
   .statistics.total_entries = (.statistics.total_entries + 1) |
   if ($category == "decision") then
     .statistics.decisions = (.statistics.decisions + 1)
   elif ($category == "progress") then
     .statistics.progress = (.statistics.progress + 1)
   elif ($category == "blocker") then
     .statistics.blockers = (.statistics.blockers + 1)
   elif ($category == "note") then
     .statistics.notes = (.statistics.notes + 1)
   end
   ' "$MEMORY_FILE" > "$TMP_FILE"

if [ $? -eq 0 ]; then
    mv "$TMP_FILE" "$MEMORY_FILE"
    echo "{\"success\": true, \"key\": \"$KEY\", \"timestamp\": \"$TIMESTAMP\"}"
else
    rm -f "$TMP_FILE"
    echo '{"error": "Failed to save memory"}'
    exit 1
fi
