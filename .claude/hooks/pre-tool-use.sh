#!/bin/bash
# pre-tool-use-hook - Runs before a tool is executed
# .claude/hooks/pre-tool-use.sh

# Read the tool call (JSON format)
TOOL_CALL=$(cat)

# Parse tool name
TOOL_NAME=$(echo "$TOOL_CALL" | jq -r '.tool // empty' 2>/dev/null)

if [ -z "$TOOL_NAME" ]; then
    echo "$TOOL_CALL"
    exit 0
fi

# Log all tool usage
echo "[$(date '+%Y-%m-%d %H:%M:%S')] TOOL: $TOOL_NAME" >> .claude/hooks/tool-log.txt 2>/dev/null

# Example: Block Write/Edit in .claude/ directory (except specific files)
if [ "$TOOL_NAME" = "Write" ] || [ "$TOOL_NAME" = "Edit" ]; then
    FILEPATH=$(echo "$TOOL_CALL" | jq -r '.arguments.filepath // .arguments.path // empty' 2>/dev/null)
    if [[ "$FILEPATH" == .claude/* ]]; then
        # Allow some files, block others
        if [[ "$FILEPATH" != .claude/project-state.json ]] && \
           [[ "$FILEPATH" != .claude/hooks/* ]] && \
           [[ "$FILEPATH" != *.txt ]]; then
            echo "[HOOK] Write/Edit blocked for $FILEPATH (protected file)" >&2
            # Uncomment next line to actually block
            # exit 1
        fi
    fi
fi

# Example: Track git operations
if [ "$TOOL_NAME" = "Bash" ]; then
    COMMAND=$(echo "$TOOL_CALL" | jq -r '.arguments.command // empty' 2>/dev/null)
    if [[ "$COMMAND" == git* ]]; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] GIT: $COMMAND" >> .claude/hooks/git-log.txt 2>/dev/null
    fi
fi

# Output the tool call (must output to stdout)
echo "$TOOL_CALL"
