#!/bin/bash
# user-prompt-submit-hook - Runs before user prompt is sent to Claude
# .claude/hooks/user-prompt-submit.sh

# Read the user prompt
USER_PROMPT=$(cat)

# Example: Check for sensitive keywords
if echo "$USER_PROMPT" | grep -qi "password\|secret\|api_key"; then
    echo "[SECURITY] Prompt contains sensitive keywords - be careful" >&2
fi

# Example: Auto-add context from project state
if [ -f ".claude/project-state.json" ]; then
    CURRENT_PHASE=$(jq -r '.current_phase' .claude/project-state.json 2>/dev/null)
    if [ -n "$CURRENT_PHASE" ] && [ "$CURRENT_PHASE" != "null" ]; then
        # Don't modify the prompt, just log the context
        echo "[CONTEXT] Current phase: $CURRENT_PHASE" >&2
    fi
fi

# Output the prompt (must output to stdout)
echo "$USER_PROMPT"
