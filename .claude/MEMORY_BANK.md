---
name: "lifecycle_memory_bank"
description: "Persistent memory bank for Unified Enterprise Lifecycle. Stores decisions, progress, blockers, and notes across Claude Code sessions."
type: "memory"
version: "1.0.0"
---

# MEMORY BANK SYSTEM

**Persistent memory storage across Claude Code sessions**

---

## WHAT IS THE MEMORY BANK?

The memory bank provides persistent storage for information that needs to survive across multiple Claude Code sessions, including:

- **Decisions** - Architectural decisions, go/no-go outcomes
- **Progress** - Phase completion, feature status
- **Blockers** - Issues blocking progress
- **Notes** - General notes and observations

---

## MEMORY STORAGE STRUCTURE

```json
// .claude/memory.json
{
  "version": "1.0.0",
  "created_at": "2025-01-11T00:00:00Z",
  "updated_at": "2025-01-11T00:00:00Z",
  "memory": {
    "decisions": {
      "cloud-provider": {
        "key": "cloud-provider",
        "value": "AWS",
        "category": "decision",
        "timestamp": "2025-01-11T00:00:00Z",
        "phase": "phase_03_architecture_design",
        "context": "Chose AWS for existing team expertise and regional availability"
      },
      "database": {
        "key": "database",
        "value": "PostgreSQL",
        "category": "decision",
        "timestamp": "2025-01-11T00:00:00Z",
        "phase": "phase_03_architecture_design",
        "context": "Chose PostgreSQL for ACID compliance and JSON support"
      }
    },
    "progress": {
      "phase-1-complete": {
        "key": "phase-1-complete",
        "value": "2025-01-10T15:30:00Z",
        "category": "progress",
        "timestamp": "2025-01-10T15:30:00Z",
        "context": "Phase 1 (Vision & Strategy) completed with executive approval"
      }
    },
    "blockers": {},
    "notes": {
      "team-availability": {
        "key": "team-availability",
        "value": "Senior backend developer available starting Feb 1",
        "category": "note",
        "timestamp": "2025-01-11T00:00:00Z",
        "context": "Plan backend architecture work accordingly"
      }
    }
  },
  "statistics": {
    "total_entries": 4,
    "decisions": 2,
    "progress": 1,
    "blockers": 0,
    "notes": 1
  }
}
```

---

## MEMORY CATEGORIES

| Category | Purpose | Example |
|----------|---------|---------|
| `decision` | Architectural and business decisions | Cloud provider, database, framework |
| `progress` | Phase/feature completion timestamps | Phase 1 complete, F-001 done |
| `blocker` | Current blockers with resolution status | Blocked on security review |
| `note` | General notes and observations | Team availability, risks |

---

## MEMORY OPERATIONS

### Save Memory

```bash
# Using MCP tool (recommended)
lifecycle_save_memory(
  key: "cloud-provider",
  value: "AWS",
  category: "decision",
  context: "Chose AWS for team expertise"
)

# Using bash
echo '{
  "key": "cloud-provider",
  "value": "AWS",
  "category": "decision",
  "context": "Chose AWS for team expertise"
}' | .claude/memory/save.sh
```

### Load Memory

```bash
# Using MCP tool (recommended)
lifecycle_load_memory(key: "cloud-provider")

# Using bash
.claude/memory/load.sh cloud-provider

# Output:
# {
#   "key": "cloud-provider",
#   "value": "AWS",
#   "category": "decision",
#   "timestamp": "2025-01-11T00:00:00Z",
#   "phase": "phase_03_architecture_design",
#   "context": "Chose AWS for team expertise"
# }
```

### Search Memory

```bash
# Using MCP tool
lifecycle_search_memory(
  category: "decision",
  search_term: "database"
)

# Using bash
.claude/memory/search.sh decision database
```

### List All Memory

```bash
# Using MCP tool
lifecycle_list_memory()

# Using bash
.claude/memory/list.sh

# Output grouped by category
```

### Delete Memory

```bash
# Using MCP tool
lifecycle_delete_memory(key: "cloud-provider")

# Using bash
.claude/memory/delete.sh cloud-provider
```

---

## MEMORY LIFECYCLE

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    MEMORY LIFECYCLE                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  1. CREATE    → Memory is saved with timestamp and category                │
│                                                                             │
│  2. RETRIEVE  → Memory can be loaded by key, category, or search term     │
│                                                                             │
│  3. UPDATE    → Existing memory can be updated (preserves history)         │
│                                                                             │
│  4. EXPIRE    → Old memory can be archived (after phase completion)        │
│                                                                             │
│  5. DELETE    → Memory can be deleted when no longer needed                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## BEST PRACTICES

### When to Use Memory

| Situation | Memory Category | Example Key |
|-----------|-----------------|-------------|
| Technical decision made | `decision` | `database-choice`, `framework-selection` |
| Phase completed | `progress` | `phase-1-complete`, `phase-2-complete` |
| Feature completed | `progress` | `F-001-complete`, `F-002-complete` |
| Blocking issue | `blocker` | `security-review-pending` |
| Team availability | `note` | `backend-dev-available` |
| Risk identified | `note` | `vendor-lock-in-risk` |
| Go/No-Go decision | `decision` | `phase-1-go-no-go` |

### Key Naming Conventions

```
decisions:    {component}-{decision-type}
              Examples: cloud-provider, database-choice, frontend-framework

progress:     {phase|feature}-{status}
              Examples: phase-1-complete, F-001-done, phase-2-approved

blockers:     {component}-{blocker-type}
              Examples: api-dependency, security-review, budget-approval

notes:        {topic}-{detail}
              Examples: team-availability, risk-vendor, timeline-adjustment
```

### Memory Retention

| Category | Retention Policy | Archive Trigger |
|----------|------------------|-----------------|
| `decision` | Keep until project end | Never |
| `progress` | Keep until project end | Never |
| `blocker` | Delete when resolved | Resolution |
| `note` | Review weekly | Time-based |

---

## MEMORY INTEGRATION WITH CLAUDE CODE

### Auto-Save Hooks

Configure in `.claude/hooks/post-tool-response.sh`:

```bash
#!/bin/bash
# Auto-save important decisions to memory

TOOL_RESPONSE=$(cat)

# Detect phase completion
if echo "$TOOL_RESPONSE" | grep -q "phase.*complete"; then
    PHASE=$(echo "$TOOL_RESPONSE" | grep -oP 'phase_\d+' | head -1)
    .claude/memory/save.sh "phase-$PHASE-complete" "$(date -Iseconds)" "progress" "Phase $PHASE completed"
fi

# Detect go/no-go decisions
if echo "$TOOL_RESPONSE" | grep -q "go.*no.*go"; then
    DECISION=$(echo "$TOOL_RESPONSE" | grep -oP '(go|no-go)' | head -1)
    .claude/memory/save.sh "go-no-go-$(date +%Y%m%d)" "$DECISION" "decision" "Go/No-Go decision for phase transition"
fi
```

### Auto-Load on Session Start

Configure in `.claude/hooks/user-prompt-submit.sh`:

```bash
#!/bin/bash
# Auto-load relevant memory on session start

# Load current blockers
BLOCKERS=$(.claude/memory/search.sh blocker)
if [ -n "$BLOCKERS" ]; then
    echo "[MEMORY] Current blockers: $BLOCKERS" >&2
fi

# Load recent decisions
DECISIONS=$(.claude/memory/list.sh decisions | tail -5)
if [ -n "$DECISIONS" ]; then
    echo "[MEMORY] Recent decisions: $DECISIONS" >&2
fi
```

---

## MEMORY API

### Save Memory

```json
// Input
{
  "key": "string (required)",
  "value": "string (required)",
  "category": "decision|progress|blocker|note (required)",
  "context": "string (optional)",
  "phase": "string (optional)"
}

// Output
{
  "success": true,
  "key": "cloud-provider",
  "timestamp": "2025-01-11T00:00:00Z"
}
```

### Load Memory

```json
// Input
{
  "key": "cloud-provider"
}

// Output
{
  "key": "cloud-provider",
  "value": "AWS",
  "category": "decision",
  "timestamp": "2025-01-11T00:00:00Z",
  "context": "Chose AWS for team expertise"
}
```

### Search Memory

```json
// Input
{
  "category": "decision",
  "search_term": "database"
}

// Output
{
  "results": [
    {
      "key": "database",
      "value": "PostgreSQL",
      "category": "decision",
      "timestamp": "2025-01-11T00:00:00Z"
    }
  ],
  "count": 1
}
```

---

## MEMORY FILE LOCATIONS

```
.claude/memory/
├── memory.json           # Main memory storage
├── archive/              # Archived memory (old/unused)
│   └── archived-2025-01.json
├── save.sh               # Save memory script
├── load.sh               # Load memory script
├── search.sh             # Search memory script
├── list.sh               # List all memory
└── delete.sh             # Delete memory
```

---

## SEE ALSO

- **Context Engineering**: `../CONTEXT_ENGINEERING.md` - Context optimization
- **Project State**: `../project-state.json` - Current phase and artifacts
- **Progress Log**: `../../claude-progress.txt` - Session history

---

**This memory bank provides persistent storage across Claude Code sessions.**
