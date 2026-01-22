---
name: "lifecycle_hooks"
description: "Hooks configuration for Unified Enterprise Lifecycle Framework. Defines user-prompt-submit, pre-tool-use, and post-tool-response hooks for automation and validation."
type: "hooks"
version: "1.0.0"
---

# LIFECYCLE HOOKS CONFIGURATION

**Hooks for automation, validation, and custom workflows in Claude Code**

---

## WHAT ARE HOOKS?

Hooks are scripts or commands that run at specific points during Claude Code execution:

1. **user-prompt-submit-hook** - Runs before user prompt is sent to Claude
2. **pre-tool-use-hook** - Runs before a tool is executed
3. **post-tool-response-hook** - Runs after a tool response is received

---

## HOOK CONFIGURATION

Hooks are configured in `.claude/settings.json`:

```json
{
  "hooks": {
    "userPromptSubmit": ".claude/hooks/user-prompt-submit.sh",
    "preToolUse": ".claude/hooks/pre-tool-use.sh",
    "postToolResponse": ".claude/hooks/post-tool-response.sh"
  }
}
```

---

## HOOK 1: user-prompt-submit-hook

**Purpose**: Validate and preprocess user prompts before sending to Claude

**Use Cases**:
- Validate prompt content
- Add context automatically
- Log prompts for audit
- Filter sensitive information

**Location**: `.claude/hooks/user-prompt-submit.sh`

**Input**: User prompt text via stdin
**Output**: Modified prompt via stdout (or exit 1 to reject)

### Template

```bash
#!/bin/bash
# .claude/hooks/user-prompt-submit.sh

# Read the user prompt
USER_PROMPT=$(cat)

# Example: Check for sensitive keywords
if echo "$USER_PROMPT" | grep -qi "password\|secret\|api_key"; then
    # Log security warning
    echo "[SECURITY] Prompt contains sensitive keywords" >&2

    # You could block or sanitize here
    # exit 1  # Uncomment to block
fi

# Example: Auto-add context from project state
if [ -f ".claude/project-state.json" ]; then
    CURRENT_PHASE=$(jq -r '.current_phase' .claude/project-state.json 2>/dev/null)
    if [ -n "$CURRENT_PHASE" ]; then
        echo "[Context: Current phase is $CURRENT_PHASE]"
    fi
fi

# Output the (possibly modified) prompt
echo "$USER_PROMPT"
```

---

## HOOK 2: pre-tool-use-hook

**Purpose**: Intercept and validate tool use before execution

**Use Cases**:
- Validate tool parameters
- Add logging/auditing
- Implement custom permissions
- Modify tool behavior

**Location**: `.claude/hooks/pre-tool-use.sh`

**Input**: JSON object via stdin with tool name and arguments
**Output**: Modified JSON via stdout (or exit 1 to block)

### Template

```bash
#!/bin/bash
# .claude/hooks/pre-tool-use.sh

# Read the tool call
TOOL_CALL=$(cat)

# Parse tool name
TOOL_NAME=$(echo "$TOOL_CALL" | jq -r '.tool // empty')
TOOL_ARGS=$(echo "$TOOL_CALL" | jq -r '.arguments // empty')

# Example: Block certain tools in production
if [ -f ".production" ] && [ "$TOOL_NAME" = "Edit" ]; then
    if [ ! "$(git diff --name-only | grep -v '.claude/')" = "" ]; then
        echo "[PRODUCTION] Edit blocked in production environment" >&2
        exit 1
    fi
fi

# Example: Log Write operations
if [ "$TOOL_NAME" = "Write" ] || [ "$TOOL_NAME" = "Edit" ]; then
    FILEPATH=$(echo "$TOOL_ARGS" | jq -r '.filepath // empty')
    echo "[TOOL] $TOOL_NAME on $FILEPATH" >> .claude/hooks/tool-log.txt
fi

# Example: Validate git operations
if [[ "$TOOL_NAME" == "Bash" ]] && echo "$TOOL_ARGS" | jq -r '.command' | grep -q "^git"; then
    GIT_CMD=$(echo "$TOOL_ARGS" | jq -r '.command')
    echo "[GIT] $GIT_CMD" >> .claude/hooks/git-log.txt
fi

# Output the (possibly modified) tool call
echo "$TOOL_CALL"
```

---

## HOOK 3: post-tool-response-hook

**Purpose**: Process tool responses after execution

**Use Cases**:
- Extract and store information
- Trigger follow-up actions
- Update project state
- Monitor for errors

**Location**: `.claude/hooks/post-tool-response.sh`

**Input**: JSON object via stdin with tool response
**Output**: Modified response via stdout

### Template

```bash
#!/bin/bash
# .claude/hooks/post-tool-response.sh

# Read the tool response
TOOL_RESPONSE=$(cat)

# Example: Track artifact creation
if echo "$TOOL_RESPONSE" | jq -e '.content[0].text' | grep -q "artifact_id"; then
    ARTIFACT_ID=$(echo "$TOOL_RESPONSE" | jq -r '.content[0].text' | jq -r '.artifact_id // empty')
    if [ -n "$ARTIFACT_ID" ]; then
        echo "$ARTIFACT_ID" >> .claude/hooks/artifacts-log.txt
    fi
fi

# Example: Update project state on phase completion
if echo "$TOOL_RESPONSE" | jq -e '.content[0].text' | grep -q "phase.*complete"; then
    # Extract phase and update state
    # This could trigger automatic phase transition
    echo "[PHASE] Phase completed, updating state" >&2
fi

# Example: Detect errors
if echo "$TOOL_RESPONSE" | jq -e '.isError' > /dev/null; then
    ERROR_MSG=$(echo "$TOOL_RESPONSE" | jq -r '.content[0].text')
    echo "[ERROR] Tool error: $ERROR_MSG" >> .claude/hooks/error-log.txt
fi

# Output the (possibly modified) response
echo "$TOOL_RESPONSE"
```

---

## LIFECYCLE-SPECIFIC HOOK EXAMPLES

### Phase Transition Hook

```bash
#!/bin/bash
# .claude/hooks/phase-transition.sh

# Called when transitioning between phases
CURRENT_PHASE=$1
NEXT_PHASE=$2

# Validate exit criteria
echo "Validating exit criteria for $CURRENT_PHASE..."
# Add validation logic here

# Update project state
jq ".current_phase = \"$NEXT_PHASE\"" .claude/project-state.json > /tmp/state.json
mv /tmp/state.json .claude/project-state.json

echo "Transitioned from $CURRENT_PHASE to $NEXT_PHASE"
```

### Feature Completion Hook

```bash
#!/bin/bash
# .claude/hooks/feature-complete.sh

FEATURE_ID=$1
ARTIFACTS=$2

# Update feature status
jq ".features[] |= if .id == \"$FEATURE_ID\" then .status = \"passing\" | .artifacts = $ARTIFACTS else . end" \
    feature_list.json > /tmp/features.json
mv /tmp/features.json feature_list.json

# Update progress log
echo "$(date): Feature $FEATURE_ID completed with artifacts: $ARTIFACTS" >> claude-progress.txt
```

### Security Scan Hook

```bash
#!/bin/bash
# .claude/hooks/security-scan.sh

SCAN_TYPE=$1

case $SCAN_TYPE in
    sast)
        echo "Running SAST scan..."
        # Run SAST tool
        ;;
    sca)
        echo "Running SCA scan..."
        # Run SCA tool
        ;;
    dast)
        echo "Running DAST scan..."
        # Run DAST tool
        ;;
esac
```

---

## HOOK DIRECTORY STRUCTURE

```
.claude/
├── hooks/
│   ├── user-prompt-submit.sh       # Prompt validation
│   ├── pre-tool-use.sh              # Tool use validation
│   ├── post-tool-response.sh        # Response processing
│   ├── phase-transition.sh          # Phase transition logic
│   ├── feature-complete.sh          # Feature completion logic
│   ├── security-scan.sh             # Security scan triggers
│   ├── tool-log.txt                 # Tool usage log
│   ├── git-log.txt                  # Git operation log
│   ├── artifacts-log.txt            # Artifact creation log
│   └── error-log.txt                # Error log
└── settings.json                    # Hook configuration
```

---

## ENABLING HOOKS

Add to `.claude/settings.json`:

```json
{
  "hooks": {
    "userPromptSubmit": ".claude/hooks/user-prompt-submit.sh",
    "preToolUse": ".claude/hooks/pre-tool-use.sh",
    "postToolResponse": ".claude/hooks/post-tool-response.sh"
  }
}
```

Make hooks executable:

```bash
chmod +x .claude/hooks/*.sh
```

---

## HOOK BEST PRACTICES

1. **Keep hooks fast** - They block execution
2. **Log everything** - Create audit trails
3. **Exit gracefully** - Don't break if a hook fails
4. **Test hooks** - Verify before deploying
5. **Document hooks** - Comment complex logic

---

## DEBUGGING HOOKS

Enable debug output:

```bash
# Add to hook for debugging
echo "[HOOK DEBUG] Input: $INPUT" >&2
echo "[HOOK DEBUG] Processing..." >&2
```

Check hook logs:

```bash
tail -f .claude/hooks/tool-log.txt
tail -f .claude/hooks/error-log.txt
```

---

## SEE ALSO

- **Settings**: `../settings.json` - Main configuration
- **Commands**: `../commands/` - Slash command hooks
- **Agents**: `../agents/` - Agent-specific hooks

---

**This hooks configuration enables automation and validation for the Unified Enterprise Lifecycle.**

---

---

**Version 1.0.0 | OCTALUME Enterprise Lifecycle Framework**
