#!/bin/bash
# OCTALUME Session Hook - Auto-save session on exit
# Place in .claude/hooks/ for automatic execution

MEMORY_DIR="$(dirname "$0")/../memory"
MEMORY_MANAGER="$MEMORY_DIR/memory-manager.js"

# Get current session ID from environment or generate new
SESSION_ID="${OCTALUME_SESSION_ID:-session-$(date +%s)}"
PHASE="${OCTALUME_PHASE:-unknown}"

# Collect session data
TIMESTAMP=$(date -Iseconds)
WORKING_DIR=$(pwd)
GIT_BRANCH=$(git branch --show-current 2>/dev/null || echo "none")

# Get modified files if in git repo
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    MODIFIED_FILES=$(git diff --name-only 2>/dev/null | head -20 | tr '\n' ',' | sed 's/,$//')
else
    MODIFIED_FILES=""
fi

# Create session record
cat > "$MEMORY_DIR/sessions/${SESSION_ID}.json" << EOF
{
  "id": "$SESSION_ID",
  "timestamp": "$TIMESTAMP",
  "phase": "$PHASE",
  "working_directory": "$WORKING_DIR",
  "git_branch": "$GIT_BRANCH",
  "files_modified": "${MODIFIED_FILES}",
  "status": "completed",
  "summary": "Session auto-saved on exit"
}
EOF

echo "[OCTALUME] Session saved: $SESSION_ID"
