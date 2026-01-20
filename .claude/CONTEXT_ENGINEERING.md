---
name: "lifecycle_context_engineering"
description: "Context engineering utilities for Unified Enterprise Lifecycle. Compaction, structured note-taking, memory management, and just-in-time retrieval."
type: "context"
version: "1.0.0"
---

# LIFECYCLE CONTEXT ENGINEERING

**Strategies for Managing Context Across Long-Running Projects**

Based on Anthropic's "Effective Context Engineering for AI Agents" research, this system provides utilities for managing context across multiple sessions and long-horizon tasks.

---

## CONTEXT ENGINEERING PRINCIPLES

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    CONTEXT ENGINEERING PRINCIPLES                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  1. CONTEXT IS FINITE                                                      │
│     └─ Treat context as a precious resource                                │
│                                                                             │
│  2. CONTEXT ROT                                                            │
│     └─ Performance degrades as tokens increase                             │
│                                                                             │
│  3. PROGRESSIVE DISCLOSURE                                                  │
│     └─ Load information only as needed                                     │
│                                                                             │
│  4. JUST-IN-TIME RETRIEVAL                                                  │
│     └─ Retrieve data at runtime, not upfront                               │
│                                                                             │
│  5. COMPACTION                                                             │
│     └─ Summarize and compress when approaching limits                      │
│                                                                             │
│  6. STRUCTURED NOTE-TAKING                                                 │
│     └─ Maintain memory outside context window                              │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## CONTEXT MANAGEMENT STRATEGIES

### 1. Compaction

When approaching context window limit (80% full):

```python
# Pseudo-code for compaction
def compact_context(current_context, threshold=0.8):
    if len(current_context) < threshold * MAX_CONTEXT:
        return current_context

    # Step 1: Clear old tool results
    clear_tool_results(older_than=50)

    # Step 2: Summarize completed work
    summary = generate_summary(context=current_context)
    save_summary(summary)

    # Step 3: Keep recent files accessible
    keep_recent_files(count=5)

    # Step 4: Compress message history
    compressed_history = compress_messages(messages=current_context.messages)
    return compressed_history
```

**Compaction Prompt**:

```
You are compacting the conversation context to continue working across multiple sessions.

COMPACT THE FOLLOWING:
1. Summarize completed work and decisions made
2. Preserve architectural decisions and unresolved bugs
3. Discard redundant tool outputs and messages
4. Keep recent 5 files accessible

OUTPUT FORMAT:
# Session Summary - {date}

## Completed
- Phase X deliverables completed
- Artifacts: P{X}-*

## In Progress
- Phase Y currently working on Z

## Decisions
- Decision 1: ...
- Decision 2: ...

## Unresolved
- Bug/Issue 1: ...
- Bug/Issue 2: ...

## Next Steps
1. Continue Phase Y
2. Complete deliverable D
3. Move to Phase Z

DO NOT:
- Include raw tool outputs
- Include full file contents
- Include verbose conversation history
```

### 2. Structured Note-Taking

Maintain persistent memory outside context window:

```markdown
# claude-progress.txt

## Session History

### Session 1 - 2025-01-11
**Phase**: Phase 1 - Vision & Strategy
**Completed**:
- Created PRD document (P1-VISION-001)
- Created business case (P1-BUSINESS-001)
- Aligned stakeholders

**Decisions**:
- Use React for frontend
- Use Node.js for backend
- Use PostgreSQL for database

**Unresolved**:
- Need to decide on cloud provider (AWS vs Azure vs GCP)

**Next**: Begin Phase 2 - Requirements & Scope

### Session 2 - 2025-01-12
**Phase**: Phase 2 - Requirements & Scope
**Completed**:
- Defined functional requirements (P2-REQ-001)
- Defined NFRs (P2-NFR-001)
- Created traceability matrix (P2-TRACE-001)

**Decisions**:
- Chose AWS as cloud provider
- Use TypeScript for type safety

**Unresolved**:
- Need to define data retention policy

**Next**: Begin Phase 3 - Architecture & Design

---

## Phase Progress

### Phase 1: Vision & Strategy ✅
- Status: complete
- Artifacts: P1-VISION-001, P1-BUSINESS-001
- Go/No-Go: ✅ GO

### Phase 2: Requirements & Scope ✅
- Status: complete
- Artifacts: P2-REQ-001, P2-NFR-001, P2-TRACE-001
- Go/No-Go: ✅ GO

### Phase 3: Architecture & Design 🔄
- Status: in_progress
- Artifacts: P3-ARCH-001 (in progress)
- Go/No-Go: ⏳ PENDING

---

## Feature Progress

Total Features: 250
Completed: 50
In Progress: 5
Blocked: 0

### Recently Completed
- ✅ F-001: User registration
- ✅ F-002: User login
- ✅ F-003: Password reset

### In Progress
- 🔄 F-004: Email verification
- 🔄 F-005: Two-factor authentication

---

## Blockers

None currently

---

## Traceability

Last Commit: abc123
Last Build: build-456
Last Deploy: prod-789

---

## Compliance Status

HIPAA: In Progress
SOC 2: Not Started
PCI DSS: Not Applicable
```

### 3. Just-In-Time Retrieval

Instead of loading everything upfront, retrieve data at runtime:

```python
# BAD: Load everything upfront
all_requirements = load_all_requirements()  # 50,000 tokens
all_architecture = load_all_architecture()  # 30,000 tokens
all_code = load_all_code()  # 100,000 tokens

# GOOD: Load on-demand
when "need requirements for authentication":
    requirements = load_requirements(scope="authentication")  # 500 tokens

when "need architecture for auth service":
    architecture = load_architecture(component="auth_service")  # 1,000 tokens

when "need code for login controller":
    code = load_code(file="src/auth/login_controller.ts")  # 2,000 tokens
```

**Just-In-Time Tools**:

```json
{
  "name": "load_artifact",
  "description": "Load a specific artifact by ID or phase",
  "input_schema": {
    "type": "object",
    "properties": {
      "artifact_id": {
        "type": "string",
        "description": "Artifact ID (e.g., P1-VISION-001)"
      },
      "phase": {
        "type": "string",
        "description": "Phase (e.g., phase_01_vision_strategy)"
      },
      "type": {
        "type": "string",
        "description": "Artifact type (e.g., PRD, architecture, test_plan)"
      }
    }
  }
}
```

---

## CONTEXT OPTIMIZATION TECHNIQUES

### 1. Progressive Disclosure

```
Level 1: Metadata (name, description) - 500 tokens
    ↓ When relevant
Level 2: SKILL.md body - 3,000 tokens
    ↓ When needed
Level 3: Referenced files - On-demand
```

### 2. File Reference Strategy

Instead of loading full file contents, pass references:

```python
# BAD: Pass full contents
context += file_contents  # 10,000 tokens

# GOOD: Pass reference
context += f"See file://{file_path} for details"  # 50 tokens
# Agent loads file when needed using Read tool
```

### 3. Tool Result Clearing

Clear tool results after they're no longer needed:

```python
def clear_old_tool_results(messages, keep_last=10):
    """Clear tool results older than last N messages"""
    for msg in messages[:-keep_last]:
        if msg.get("role") == "tool_result":
            msg["content"] = "[Tool result cleared for context efficiency]"
    return messages
```

### 4. Message Compression

Compress verbose messages:

```python
def compress_messages(messages):
    """Compress message history"""
    compressed = []
    for msg in messages:
        if msg.get("role") == "user":
            compressed.append(msg)
        elif msg.get("role") == "assistant":
            compressed.append({
                "role": "assistant",
                "content": summarize_assistant_message(msg["content"])
            })
        elif msg.get("role") == "tool_result":
            compressed.append({
                "role": "tool_result",
                "content": summarize_tool_result(msg["content"])
            })
    return compressed
```

---

## LONG-HORIZON TASK MANAGEMENT

### For Multi-Session Projects

**Session Start Template**:

```markdown
# Session Start - {date}

## Get Oriented

1. Current directory: `{pwd}`
2. Current phase: {read .claude/project-state.json}
3. Recent work: {git log --oneline -10}
4. Progress log: {read claude-progress.txt}

## Verify Environment

1. Run init.sh: `source scripts/init.sh`
2. Run tests: `npm test`
3. Check status: `git status`

## Choose Next Task

1. Read feature list: `cat feature_list.json`
2. Select next failing feature (prioritize P0, then P1, etc.)
3. Plan implementation

## Work on Feature

1. Implement feature
2. Write tests
3. Verify manually (as human user would)
4. Fix bugs

## End Session

1. Update feature status
2. Update progress log
3. Commit to git
4. Leave clean state
```

### Memory Tools

```json
{
  "name": "memory_save",
  "description": "Save information to memory outside context window",
  "input_schema": {
    "type": "object",
    "properties": {
      "key": {
        "type": "string",
        "description": "Memory key (e.g., 'decision-cloud-provider')"
      },
      "value": {
        "type": "string",
        "description": "Value to store"
      },
      "category": {
        "type": "string",
        "enum": ["decision", "progress", "blocker", "note"],
        "description": "Memory category"
      }
    }
  }
}
```

---

## CONTEXT BUDGETING

### Recommended Token Allocation

```
┌─────────────────────────────────────────────────────────────────┐
│                    CONTEXT BUDGET (200K tokens)                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  System Prompt:        3,000 tokens   (1.5%)                   │
│  Tool Definitions:     5,000 tokens   (2.5%)   [deferred load] │
│  Project State:        2,000 tokens   (1%)                     │
│  Recent Files:        20,000 tokens   (10%)                    │
│  Message History:     50,000 tokens   (25%)                    │
│  Current Task:       100,000 tokens   (50%)                    │
│  Safety Buffer:       20,000 tokens   (10%)                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Budget Enforcement

```python
def check_context_budget(current_context):
    """Check if we're approaching context limit"""
    usage = len(current_context)
    budget = MAX_CONTEXT * 0.8  # 80% threshold

    if usage > budget:
        warnings.warn(f"Context at {usage/MAX_CONTEXT*100:.1f}% capacity")
        return "compact"
    elif usage > budget * 0.9:
        warnings.warn(f"Context at {usage/MAX_CONTEXT*100:.1f}% capacity - COMPACT NOW")
        return "compact_immediately"
    else:
        return "ok"
```

---

## CONTEXT QUALITY METRICS

### Signal-to-Noise Ratio

```
Signal = Relevant information for current task
Noise = Irrelevant information, old tool results, verbose messages

Target: Signal/Noise > 0.7
```

### Context Efficiency

```
Context Efficiency = (Useful Tokens / Total Tokens) * 100

Target: > 70%
```

### Information Density

```
Information Density = (Unique Information / Total Tokens) * 100

Target: > 60%
```

---

## CONTEXT ENGINEERING BEST PRACTICES

### 1. Use File References

```python
# Instead of:
context += read_file("large_file.txt")  # 10,000 tokens

# Use:
context += "See large_file.txt for detailed specifications"  # 50 tokens
# Agent will read file when needed
```

### 2. Clear Old Tool Results

```python
# After tool result is processed
if tool_result_age > 50_messages:
    clear_tool_result(tool_result_id)
```

### 3. Summarize Completed Work

```python
# After completing a phase
summary = summarize_phase_completion(phase)
save_to_memory(key=f"phase_{phase}_summary", value=summary)
```

### 4. Use Structured Memory

```python
# Instead of keeping everything in context
memory.save("decision-cloud-provider", "AWS chosen for X, Y, Z reasons")
memory.save("progress-phase-1", "Complete, artifacts: P1-VISION-001, P1-BUSINESS-001")
```

### 5. Retrieve On-Demand

```python
# When specific information is needed
artifact = memory.load("P3-ARCH-001")  # Load architecture document
requirements = memory.load("P2-REQ-001")  # Load requirements
```

---

## CONTEXT ENGINEERING TOOLS

```json
{
  "tools": [
    {
      "name": "context_compact",
      "description": "Compact conversation context when approaching limit",
      "input_schema": {
        "type": "object",
        "properties": {
          "strategy": {
            "type": "string",
            "enum": ["summary", "tool_result_clear", "message_compress", "all"],
            "description": "Compaction strategy"
          },
          "keep_last": {
            "type": "integer",
            "description": "Number of recent messages to keep intact"
          }
        }
      }
    },
    {
      "name": "context_save_memory",
      "description": "Save information to memory outside context window",
      "input_schema": {
        "type": "object",
        "properties": {
          "key": {"type": "string"},
          "value": {"type": "string"},
          "category": {"type": "string"}
        }
      }
    },
    {
      "name": "context_load_memory",
      "description": "Load information from memory",
      "input_schema": {
        "type": "object",
        "properties": {
          "key": {"type": "string"},
          "category": {"type": "string"}
        }
      }
    },
    {
      "name": "context_check_budget",
      "description": "Check current context usage and recommend action",
      "input_schema": {
        "type": "object",
        "properties": {}
      }
    },
    {
      "name": "context_load_artifact",
      "description": "Load specific artifact on-demand",
      "input_schema": {
        "type": "object",
        "properties": {
          "artifact_id": {"type": "string"},
          "phase": {"type": "string"},
          "type": {"type": "string"}
        }
      }
    }
  ]
}
```

---

## SEE ALSO

- **Orchestrator**: `../ORCHESTRATOR.md` - Multi-agent coordination
- **Tool Search**: `tools/TOOL_SEARCH.md` - Dynamic tool discovery
- **Memory Tools**: `tools/MEMORY.md` - Persistent memory management

---

**This context engineering system implements Anthropic's effective context engineering research.**

---

**Review Completed By:** OCTALUME TEAM
**Date:** 2026-01-13
**Next Review Recommended:** After major framework updates or every 6 months
