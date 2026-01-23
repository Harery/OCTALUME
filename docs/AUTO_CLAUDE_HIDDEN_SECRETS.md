# Auto-Claude v2.7.4 Hidden Secrets Analysis
## Deep Dive for OCTALUME Retrofit

**Analysis Date**: 2025-01-21  
**Source**: Extracted AppImage binary analysis  
**Target**: OCTALUME v2.2+ Retrofit Candidates

---

## 🔍 Executive Summary

After extracting and analyzing the Auto-Claude v2.7.4 AppImage, we discovered **14 major hidden systems** that make it powerful. This document catalogs each system with implementation details for OCTALUME retrofit.

---

## 1. 🧠 THINKING LEVELS SYSTEM

### Discovery Location
- `resources/backend/phase_config.py`
- `resources/backend/agents/tools_pkg/models.py`

### Implementation Details

```python
# Token budgets per thinking level
THINKING_BUDGET_MAP = {
    "none": None,      # No extended thinking - for coding tasks
    "low": 1024,       # Light analysis - commit messages, merge resolution
    "medium": 4096,    # Moderate analysis - research, context gathering
    "high": 16384,     # Deep thinking - QA review, planning
    "ultrathink": 65536,  # Maximum reasoning - spec critique, discovery
}
```

### Per-Phase Thinking Levels
```python
SPEC_PHASE_THINKING_LEVELS = {
    "discovery": "ultrathink",      # 65K tokens
    "spec_writing": "ultrathink",   # Deep spec analysis
    "self_critique": "ultrathink",  # Critical review
    "requirements": "medium",       # 4K tokens
    "research": "medium",
    "context": "medium",
    "planning": "medium",
    "validation": "medium",
}
```

### Per-Agent Defaults (from AGENT_CONFIGS)
| Agent Type | Thinking Level | Token Budget |
|------------|---------------|--------------|
| spec_gatherer | medium | 4,096 |
| spec_researcher | medium | 4,096 |
| spec_writer | high | 16,384 |
| spec_critic | ultrathink | 65,536 |
| planner | high | 16,384 |
| coder | none | 0 |
| qa_reviewer | high | 16,384 |
| qa_fixer | medium | 4,096 |
| merge_resolver | low | 1,024 |
| commit_message | low | 1,024 |
| insights | medium | 4,096 |
| ideation | high | 16,384 |

### OCTALUME Retrofit Priority: **HIGH** ⭐⭐⭐
Phase-aware thinking levels can dramatically improve quality without cost explosion.

---

## 2. 📊 AGENT CONFIGURATION REGISTRY

### Discovery Location
- `resources/backend/agents/tools_pkg/models.py`

### Full Implementation
```python
AGENT_CONFIGS = {
    # SPEC CREATION PHASES
    "spec_gatherer": {
        "tools": BASE_READ_TOOLS + WEB_TOOLS,
        "mcp_servers": [],
        "auto_claude_tools": [],
        "thinking_default": "medium",
    },
    "spec_researcher": {
        "tools": BASE_READ_TOOLS + WEB_TOOLS,
        "mcp_servers": ["context7"],
        "auto_claude_tools": [],
        "thinking_default": "medium",
    },
    "spec_writer": {
        "tools": BASE_READ_TOOLS + BASE_WRITE_TOOLS,
        "mcp_servers": [],
        "auto_claude_tools": [],
        "thinking_default": "high",
    },
    "spec_critic": {
        "tools": BASE_READ_TOOLS,
        "mcp_servers": [],
        "auto_claude_tools": [],
        "thinking_default": "ultrathink",
    },
    
    # BUILD PHASES
    "planner": {
        "tools": BASE_READ_TOOLS + BASE_WRITE_TOOLS + WEB_TOOLS,
        "mcp_servers": ["context7", "graphiti", "auto-claude"],
        "mcp_servers_optional": ["linear"],
        "auto_claude_tools": [
            "mcp__auto-claude__get_build_progress",
            "mcp__auto-claude__get_session_context",
            "mcp__auto-claude__record_discovery",
        ],
        "thinking_default": "high",
    },
    "coder": {
        "tools": BASE_READ_TOOLS + BASE_WRITE_TOOLS + WEB_TOOLS,
        "mcp_servers": ["context7", "graphiti", "auto-claude"],
        "auto_claude_tools": [
            "mcp__auto-claude__update_subtask_status",
            "mcp__auto-claude__get_build_progress",
            "mcp__auto-claude__record_discovery",
            "mcp__auto-claude__record_gotcha",
            "mcp__auto-claude__get_session_context",
        ],
        "thinking_default": "none",
    },
    
    # QA PHASES
    "qa_reviewer": {
        "tools": BASE_READ_TOOLS + BASE_WRITE_TOOLS + WEB_TOOLS,
        "mcp_servers": ["context7", "graphiti", "auto-claude", "browser"],
        "auto_claude_tools": [
            "mcp__auto-claude__get_build_progress",
            "mcp__auto-claude__update_qa_status",
            "mcp__auto-claude__get_session_context",
        ],
        "thinking_default": "high",
    },
    "qa_fixer": {
        "tools": BASE_READ_TOOLS + BASE_WRITE_TOOLS + WEB_TOOLS,
        "mcp_servers": ["context7", "graphiti", "auto-claude", "browser"],
        "auto_claude_tools": [
            "mcp__auto-claude__update_subtask_status",
            "mcp__auto-claude__get_build_progress",
            "mcp__auto-claude__update_qa_status",
            "mcp__auto-claude__record_gotcha",
        ],
        "thinking_default": "medium",
    },
    
    # UTILITY PHASES
    "insights": {
        "tools": BASE_READ_TOOLS + WEB_TOOLS,
        "mcp_servers": [],
        "auto_claude_tools": [],
        "thinking_default": "medium",
    },
    "merge_resolver": {
        "tools": [],
        "mcp_servers": [],
        "auto_claude_tools": [],
        "thinking_default": "low",
    },
    "commit_message": {
        "tools": [],
        "mcp_servers": [],
        "auto_claude_tools": [],
        "thinking_default": "low",
    },
    
    # ROADMAP & IDEATION
    "roadmap_discovery": {
        "tools": BASE_READ_TOOLS + WEB_TOOLS,
        "mcp_servers": ["context7"],
        "auto_claude_tools": [],
        "thinking_default": "high",
    },
    "competitor_analysis": {
        "tools": BASE_READ_TOOLS + WEB_TOOLS,
        "mcp_servers": ["context7"],
        "auto_claude_tools": [],
        "thinking_default": "high",
    },
    "ideation": {
        "tools": BASE_READ_TOOLS + WEB_TOOLS,
        "mcp_servers": [],
        "auto_claude_tools": [],
        "thinking_default": "high",
    },
}
```

### Dynamic Tool Selection
```python
def get_required_mcp_servers(
    agent_type: str,
    project_capabilities: dict | None = None,
    linear_enabled: bool = False,
    mcp_config: dict | None = None,
) -> list[str]:
    """
    Dynamic MCP server selection based on:
    - Agent type capabilities
    - Project type (is_electron, is_web_frontend)
    - Per-project config overrides
    - AGENT_MCP_<agent>_ADD/REMOVE environment variables
    """
```

### OCTALUME Retrofit Priority: **HIGH** ⭐⭐⭐
Central registry pattern enables phase-aware tool control.

---

## 3. 🧬 DUAL-LAYER MEMORY SYSTEM

### Discovery Location
- `resources/backend/agents/memory_manager.py`
- `resources/backend/integrations/graphiti/memory.py`

### Architecture
```
┌─────────────────────────────────────────┐
│           Memory Manager                 │
├─────────────────────────────────────────┤
│  PRIMARY: Graphiti (when enabled)       │
│  ├── Semantic search                    │
│  ├── Cross-session context              │
│  ├── Patterns & Gotchas storage         │
│  └── Session insights with embeddings    │
├─────────────────────────────────────────┤
│  FALLBACK: File-based (always works)    │
│  ├── memory/session_insights/*.json     │
│  ├── memory/gotchas.md                  │
│  ├── memory/codebase_map.json           │
│  └── memory/attempt_history.json        │
└─────────────────────────────────────────┘
```

### Memory Operations
```python
async def get_graphiti_context(spec_dir, project_dir, subtask):
    """Retrieve relevant context from knowledge graph."""
    # 1. Build search query from subtask description
    # 2. Get relevant context items (semantic search)
    # 3. Get patterns and gotchas specifically
    # 4. Get recent session history
    # 5. Format as markdown for agent context

async def save_session_memory(spec_dir, project_dir, subtask_id, 
                              session_num, success, subtasks_completed,
                              discoveries=None):
    """
    Save session insights with dual-layer strategy:
    - PRIMARY: Graphiti (provides semantic search, cross-session)
    - FALLBACK: File-based (zero dependencies)
    """
```

### Patterns & Gotchas Retrieval (THE FIX for learning loop!)
```python
# This retrieves PATTERN and GOTCHA episode types for cross-session learning
patterns, gotchas = await memory.get_patterns_and_gotchas(
    query, num_results=3, min_score=0.5
)
```

### OCTALUME Retrofit Priority: **MEDIUM** ⭐⭐
Pattern/gotcha tracking would help learning. Graphiti requires LadybugDB.

---

## 4. 📦 CONTEXT COMPACTION SYSTEM

### Discovery Location
- `resources/backend/spec/compaction.py`

### Full Implementation
```python
async def summarize_phase_output(
    phase_name: str,
    phase_output: str,
    model: str = "sonnet",
    target_words: int = 500,
) -> str:
    """
    Summarize phase output to maintain continuity while reducing tokens.
    
    Uses Sonnet for cost efficiency since this is simple summarization.
    """
    # Limit input to avoid token overflow
    max_input_chars = 15000
    truncated_output = phase_output[:max_input_chars]
    
    prompt = f"""Summarize the key findings from "{phase_name}" in {target_words} words.
    
Focus on extracting ONLY the most critical information:
- Key decisions made and their rationale
- Critical files, components, or patterns identified
- Important constraints or requirements discovered
- Actionable insights for implementation

Be concise and use bullet points."""
    
    # Run lightweight summarization agent
    ...

def format_phase_summaries(summaries: dict[str, str]) -> str:
    """Format accumulated summaries for injection into agent context."""
    formatted_parts = ["## Context from Previous Phases\n"]
    for phase_name, summary in summaries.items():
        formatted_parts.append(
            f"### {phase_name.replace('_', ' ').title()}\n{summary}\n"
        )
    return "\n".join(formatted_parts)
```

### Phase Output Mapping
```python
phase_outputs = {
    "discovery": ["context.json"],
    "requirements": ["requirements.json"],
    "research": ["research.json"],
    "context": ["context.json"],
    "quick_spec": ["spec.md"],
    "spec_writing": ["spec.md"],
    "self_critique": ["spec.md", "critique_notes.md"],
    "planning": ["implementation_plan.json"],
    "validation": [],  # No output files
}
```

### OCTALUME Retrofit Priority: **HIGH** ⭐⭐⭐
Token reduction between phases is critical for long builds.

---

## 5. 💡 INSIGHT EXTRACTION SYSTEM

### Discovery Location
- `resources/backend/insight_extractor.py`

### Full Implementation
```python
async def extract_session_insights(
    spec_dir, project_dir, subtask_id, session_num,
    commit_before, commit_after, success, recovery_manager
) -> dict:
    """
    Extract rich insights from completed coding sessions.
    Uses LLM analysis of git diff, changed files, commit messages.
    """
    
    # Gather inputs
    inputs = gather_extraction_inputs(...)
    
    # Build prompt for extraction
    prompt = _build_extraction_prompt(inputs)
    
    # Run Claude Haiku for fast extraction
    extracted = await run_insight_extraction(inputs, project_dir)
    
    return {
        "file_insights": [...],      # Per-file discoveries
        "patterns_discovered": [...], # Reusable patterns found
        "gotchas_discovered": [...],  # Pitfalls to avoid
        "approach_outcome": {
            "success": True/False,
            "approach_used": "...",
            "why_it_worked": "...",
            "why_it_failed": "...",
            "alternatives_tried": [...]
        },
        "recommendations": [...]      # For next session
    }
```

### Extraction Prompt Template
```markdown
Extract structured insights from this coding session.
Output ONLY valid JSON with:
- file_insights: Per-file discoveries
- patterns_discovered: Reusable patterns found
- gotchas_discovered: Pitfalls to avoid
- approach_outcome: What worked/failed and why
- recommendations: For next session
```

### OCTALUME Retrofit Priority: **HIGH** ⭐⭐⭐
Post-session learning enables continuous improvement.

---

## 6. 🔄 RECOVERY SYSTEM

### Discovery Location
- `resources/backend/services/recovery.py`

### Full Implementation
```python
class FailureType(Enum):
    BROKEN_BUILD = "broken_build"      # Code doesn't compile
    VERIFICATION_FAILED = "verification_failed"
    CIRCULAR_FIX = "circular_fix"      # Same fix attempted multiple times
    CONTEXT_EXHAUSTED = "context_exhausted"
    UNKNOWN = "unknown"

@dataclass
class RecoveryAction:
    action: str   # "rollback", "retry", "skip", "escalate"
    target: str   # commit hash, subtask id, or message
    reason: str

class RecoveryManager:
    """
    Manages recovery from build failures.
    
    - Track attempt history across sessions
    - Classify failures and determine recovery actions
    - Rollback to working states
    - Detect circular fixes (same approach repeatedly)
    - Escalate stuck subtasks for human intervention
    """
    
    def __init__(self, spec_dir, project_dir):
        self.memory_dir = spec_dir / "memory"
        self.attempt_history_file = self.memory_dir / "attempt_history.json"
        self.build_commits_file = self.memory_dir / "build_commits.json"
    
    def classify_failure(self, error: str, subtask_id: str) -> FailureType:
        """Classify failure type from error message."""
        error_lower = error.lower()
        
        build_errors = [
            "syntax error", "compilation error", "module not found",
            "import error", "cannot find module", "unexpected token",
            "indentation error", "parse error"
        ]
        if any(be in error_lower for be in build_errors):
            return FailureType.BROKEN_BUILD
        ...
    
    def record_attempt(self, subtask_id, session, success, approach, error=None):
        """Record an attempt for later analysis."""
    
    def record_good_commit(self, commit_hash, subtask_id):
        """Record a known-good commit for rollback."""
    
    def get_recovery_action(self, subtask_id, failure_type) -> RecoveryAction:
        """Determine what recovery action to take."""
```

### Attempt History Schema
```json
{
  "subtasks": {
    "subtask-001": {
      "attempts": [
        {
          "session": 1,
          "success": false,
          "approach": "Direct implementation...",
          "error": "Import error: module not found",
          "timestamp": "2025-01-21T10:30:00"
        },
        {
          "session": 2,
          "success": true,
          "approach": "Installed missing dependency first",
          "timestamp": "2025-01-21T10:45:00"
        }
      ]
    }
  },
  "stuck_subtasks": ["subtask-003"],
  "metadata": {
    "created_at": "...",
    "last_updated": "..."
  }
}
```

### OCTALUME Retrofit Priority: **HIGH** ⭐⭐⭐
Recovery system prevents infinite loops and enables true walk-away automation.

---

## 7. 📊 COMPLEXITY ASSESSMENT

### Discovery Location
- `resources/backend/runners/spec_runner.py`

### Complexity Tiers
```
SIMPLE (1-2 files):
  Discovery → Quick Spec → Validate
  [3 phases]

STANDARD (3-10 files):
  Discovery → Requirements → Context → Spec → Plan → Validate
  [6 phases]

STANDARD + Research (external deps):
  Discovery → Requirements → Research → Context → Spec → Plan → Validate
  [7 phases]

COMPLEX (10+ files/integrations):
  Full 8-phase pipeline with research and self-critique
  [8 phases]
```

### Assessment Factors
- Number of files/services involved
- External integrations and research requirements
- Infrastructure changes (Docker, databases, etc.)
- Whether codebase has existing patterns to follow
- Risk factors and edge cases

### OCTALUME Retrofit Priority: **MEDIUM** ⭐⭐
Adaptive phase selection based on task complexity.

---

## 8. 🔧 CUSTOM MCP TOOLS

### Discovery Location
- `resources/backend/agents/tools_pkg/models.py`

### Auto-Claude Custom Tools
```python
# Progress tracking
TOOL_UPDATE_SUBTASK_STATUS = "mcp__auto-claude__update_subtask_status"
TOOL_GET_BUILD_PROGRESS = "mcp__auto-claude__get_build_progress"

# Knowledge capture
TOOL_RECORD_DISCOVERY = "mcp__auto-claude__record_discovery"
TOOL_RECORD_GOTCHA = "mcp__auto-claude__record_gotcha"

# Session management
TOOL_GET_SESSION_CONTEXT = "mcp__auto-claude__get_session_context"
TOOL_UPDATE_QA_STATUS = "mcp__auto-claude__update_qa_status"
```

### External MCP Integrations
```python
# Context7 - Documentation lookup
CONTEXT7_TOOLS = [
    "mcp__context7__resolve-library-id",
    "mcp__context7__get-library-docs",
]

# Linear - Project management
LINEAR_TOOLS = [
    "mcp__linear-server__list_teams",
    "mcp__linear-server__get_team",
    "mcp__linear-server__list_projects",
    ...
]

# Graphiti - Knowledge graph
GRAPHITI_MCP_TOOLS = [
    "mcp__graphiti-memory__search_nodes",
    "mcp__graphiti-memory__search_facts",
    "mcp__graphiti-memory__add_episode",
    "mcp__graphiti-memory__get_episodes",
    "mcp__graphiti-memory__get_entity_edge",
]

# Browser automation (QA only)
PUPPETEER_TOOLS = [
    "mcp__puppeteer__puppeteer_connect_active_tab",
    "mcp__puppeteer__puppeteer_navigate",
    "mcp__puppeteer__puppeteer_screenshot",
    ...
]

ELECTRON_TOOLS = [
    "mcp__electron__get_electron_window_info",
    "mcp__electron__take_screenshot",
    "mcp__electron__send_command_to_electron",
    "mcp__electron__read_electron_logs",
]
```

### OCTALUME Retrofit Priority: **MEDIUM** ⭐⭐
Custom MCP server for build tracking would be powerful.

---

## 9. 📝 POST-SESSION PROCESSING

### Discovery Location
- `resources/backend/agents/session.py`

### Session Lifecycle
```python
async def post_session_processing(
    spec_dir, project_dir, subtask_id, session_num,
    commit_before, commit_count_before, recovery_manager,
    linear_enabled=False, status_manager=None, source_spec_dir=None
) -> bool:
    """
    Process session results and update memory automatically.
    This runs in Python (100% reliable) instead of relying on agent.
    """
    
    # 1. Sync implementation plan back to source (for worktree mode)
    if sync_spec_to_source(spec_dir, source_spec_dir):
        print_status("Implementation plan synced", "success")
    
    # 2. Check if implementation plan was updated
    plan = load_implementation_plan(spec_dir)
    subtask = find_subtask_in_plan(plan, subtask_id)
    subtask_status = subtask.get("status", "pending")
    
    # 3. Check for new commits
    commit_after = get_latest_commit(project_dir)
    new_commits = commit_count_after - commit_count_before
    
    if subtask_status == "completed":
        # 4. Record successful attempt
        recovery_manager.record_attempt(subtask_id, session_num, True, ...)
        
        # 5. Record good commit for rollback safety
        recovery_manager.record_good_commit(commit_after, subtask_id)
        
        # 6. Record Linear session result (if enabled)
        if linear_enabled:
            await linear_subtask_completed(...)
        
        # 7. Extract rich insights from session (LLM-powered)
        extracted_insights = await extract_session_insights(...)
        
        # 8. Save session memory (Graphiti=primary, file=fallback)
        await save_session_memory(...)
        
        return True
    else:
        # Record failed attempt, extract insights anyway
        ...
        return False
```

### OCTALUME Retrofit Priority: **HIGH** ⭐⭐⭐
Automated post-session processing ensures nothing is lost.

---

## 10. 🔐 TOOL INPUT VALIDATION

### Discovery Location
- `resources/backend/security/tool_input_validator.py`

### Safe Tool Input Extraction
```python
def get_safe_tool_input(block):
    """
    Safely extract tool input, handling None, non-dict, etc.
    Prevents crashes from malformed tool responses.
    """
```

### OCTALUME Retrofit Priority: **LOW** ⭐
Already have security validators in v2.1.

---

## 11. 🌳 SPEC PHASES MIXIN PATTERN

### Discovery Location
- `resources/backend/spec/phases/executor.py`

### Architecture
```python
class PhaseExecutor(
    DiscoveryPhaseMixin,       # Discovery and context gathering
    RequirementsPhaseMixin,    # Requirements, historical context, research
    SpecPhaseMixin,            # Spec writing and self-critique
    PlanningPhaseMixin,        # Implementation planning and validation
):
    """
    Combines multiple mixins for modular phase handling.
    Each mixin handles a specific category of phases.
    """
```

### Phase Methods
- `phase_discovery()` - Analyze project structure
- `phase_requirements()` - Gather requirements
- `phase_research()` - External API/library research
- `phase_context()` - Build context from existing code
- `phase_quick_spec()` - Fast spec for simple tasks
- `phase_spec_writing()` - Write detailed spec.md
- `phase_self_critique()` - Ultrathink critique of spec
- `phase_planning()` - Create implementation plan
- `phase_validation()` - Validate before build

### OCTALUME Retrofit Priority: **MEDIUM** ⭐⭐
Mixin pattern is cleaner than monolithic phase handler.

---

## 12. 📖 PROJECT INDEXING

### Discovery Location
- `resources/backend/spec/discovery.py`
- `resources/backend/analyzer.py`

### Index Schema
```json
{
  "project_type": "nodejs",
  "services": {
    "backend": {
      "entry_point": "src/index.ts",
      "dependencies": [...],
      "dev_dependencies": [...],
      "key_directories": {
        "src": "Source code",
        "tests": "Test files"
      }
    }
  },
  "infrastructure": {
    "docker_compose": ["docker-compose.yml"],
    "dockerfiles": ["Dockerfile"]
  },
  "conventions": {
    "linting": "eslint",
    "formatting": "prettier",
    "git_hooks": "husky"
  }
}
```

### OCTALUME Retrofit Priority: **MEDIUM** ⭐⭐
Project analysis helps with context building.

---

## 🎯 RETROFIT PRIORITY MATRIX

| Feature | Priority | Effort | Impact | v2.2 |
|---------|----------|--------|--------|------|
| Thinking Levels | ⭐⭐⭐ HIGH | Medium | High | ✅ |
| Context Compaction | ⭐⭐⭐ HIGH | Medium | High | ✅ |
| Insight Extraction | ⭐⭐⭐ HIGH | Medium | High | ✅ |
| Recovery System | ⭐⭐⭐ HIGH | High | High | ✅ |
| Post-Session Processing | ⭐⭐⭐ HIGH | Medium | High | ✅ |
| Agent Config Registry | ⭐⭐⭐ HIGH | Low | High | ✅ |
| Dual-Layer Memory | ⭐⭐ MED | High | Medium | Partial |
| Complexity Assessment | ⭐⭐ MED | Low | Medium | ✅ |
| Custom MCP Tools | ⭐⭐ MED | High | Medium | v2.3 |
| Mixin Phase Pattern | ⭐⭐ MED | Medium | Low | v2.3 |
| Project Indexer | ⭐⭐ MED | Medium | Medium | v2.3 |
| Tool Input Validation | ⭐ LOW | Low | Low | v2.1 ✓ |

---

## 📋 v2.2 IMPLEMENTATION CHECKLIST

### Phase 1: Core Systems
- [ ] Thinking levels configuration
- [ ] Phase-aware thinking budgets
- [ ] Agent configuration registry

### Phase 2: Token Optimization
- [ ] Context compaction between phases
- [ ] Phase output summarization
- [ ] Token budget monitoring

### Phase 3: Learning Systems
- [ ] Post-session insight extraction
- [ ] Pattern/gotcha recording
- [ ] Attempt history tracking

### Phase 4: Recovery
- [ ] Failure classification
- [ ] Circular fix detection
- [ ] Automatic rollback support
- [ ] Human escalation triggers

### Phase 5: Complexity Handling
- [ ] Task complexity assessment
- [ ] Adaptive phase selection
- [ ] Resource allocation per complexity

---

## 🔮 Cannot Retrofit (Requires Electron/LadybugDB)

1. **12 Parallel Agent Terminals** - Requires Electron IPC
2. **Visual Kanban Board** - Requires Electron GUI
3. **Full Graphiti Knowledge Graph** - Requires LadybugDB
4. **Real-time IPC Events** - Requires Electron
5. **Puppeteer/Electron Browser Tools** - Requires GUI environment

---

## 📚 Source Files Reference

| System | File Path |
|--------|-----------|
| Thinking Levels | `backend/phase_config.py` |
| Agent Configs | `backend/agents/tools_pkg/models.py` |
| Memory Manager | `backend/agents/memory_manager.py` |
| Context Compaction | `backend/spec/compaction.py` |
| Insight Extraction | `backend/insight_extractor.py` |
| Recovery System | `backend/services/recovery.py` |
| Session Processing | `backend/agents/session.py` |
| Phase Executor | `backend/spec/phases/executor.py` |
| Spec Phases | `backend/spec/phases/spec_phases.py` |
| Discovery | `backend/spec/discovery.py` |

---

*Generated from Auto-Claude v2.7.4 AppImage extraction*  
*For OCTALUME v2.2+ retrofit planning*
