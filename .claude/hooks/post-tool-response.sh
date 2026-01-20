#!/bin/bash
# post-tool-response-hook - Runs after a tool response is received
# .claude/hooks/post-tool-response.sh

# Read the tool response (JSON format)
TOOL_RESPONSE=$(cat)

# Check for errors
IS_ERROR=$(echo "$TOOL_RESPONSE" | jq -r '.isError // false' 2>/dev/null)

if [ "$IS_ERROR" = "true" ]; then
    ERROR_CONTENT=$(echo "$TOOL_RESPONSE" | jq -r '.content[0].text // empty' 2>/dev/null)
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: $ERROR_CONTENT" >> .claude/hooks/error-log.txt 2>/dev/null
fi

# Example: Track artifact creation
if echo "$TOOL_RESPONSE" | jq -e '.content[0].text' > /dev/null 2>&1; then
    RESPONSE_TEXT=$(echo "$TOOL_RESPONSE" | jq -r '.content[0].text' 2>/dev/null)

    # Check if response contains artifact_id
    if echo "$RESPONSE_TEXT" | jq -e '.artifact_id' > /dev/null 2>&1; then
        ARTIFACT_ID=$(echo "$RESPONSE_TEXT" | jq -r '.artifact_id' 2>/dev/null)
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] ARTIFACT: $ARTIFACT_ID" >> .claude/hooks/artifacts-log.txt 2>/dev/null
    fi
fi

# Output the response (must output to stdout)
echo "$TOOL_RESPONSE"
