# Auto-Claude Deep Technical Analysis

**Version Analyzed**: 2.7.4 (AndyMik90/Auto-Claude)  
**Date**: January 2026  
**Purpose**: Feature comparison for OCTALUME framework retrofitting

---

## 1. Thinking Levels System

### Token Budgets
Auto-Claude implements 5 thinking levels with specific token budgets:

```python
THINKING_BUDGET_MAP = {
    "none": None,        # No extended thinking
    "low": 1024,         # Quick decisions
    "medium": 4096,      # Moderate analysis
    "high": 16384,       # Deep thinking for QA review
    "ultrathink": 65536, # Maximum reasoning depth (64K tokens!)
}
```

### Phase-Specific Thinking Levels
Different spec phases have different thinking requirements:

```python
SPEC_PHASE_THINKING_LEVELS = {
    # Heavy phases - ultrathink (deep analysis)
    "discovery": "ultrathink",
    "spec_writing": "ultrathink",
    "self_critique": "ultrathink",
    
    # Light phases - medium (after compaction)
    "requirements": "medium",
    "research": "medium",
    "context": "medium",
    "planning": "medium",
    "validation": "medium",
    "quick_spec": "medium",
    "historical_context": "medium",
    "complexity_assessment": "medium",
}
```

### Default Phase Configuration
```python
DEFAULT_PHASE_MODELS = {
    "spec": "sonnet",
    "planning": "sonnet",  # Changed from opus (fix #433)
    "coding": "sonnet",
    "qa": "sonnet",
}

DEFAULT_PHASE_THINKING = {
    "spec": "medium",
    "planning": "high",
    "coding": "medium",
    "qa": "high",
}
```

### Key Insight
- Thinking levels are **phase-aware** - different phases need different reasoning depths
- `ultrathink` (64K tokens) is reserved for heavy phases: discovery, spec writing, self-critique
- Coding uses "none" - no extended thinking needed for implementation
- QA uses "high" (16K) for deep verification analysis

---

## 2. Context Compaction System

### Phase Summary Workflow
After each phase completes, its output is summarized for subsequent phases:

```python
async def summarize_phase_output(
    phase_name: str,
    phase_output: str,
    model: str = "sonnet",
    target_words: int = 500,  # ~500-1000 recommended
) -> str:
```

### Key Features
1. **Input Truncation**: Max 15,000 characters per phase output
2. **Target Summary Length**: ~500 words (configurable)
3. **Bullet Point Format**: Concise, actionable summaries
4. **Fallback on Error**: Returns truncated raw output if summarization fails

### Summary Prompt Structure
```markdown
Summarize the key findings from the "{phase_name}" phase in {target_words} words or less.

Focus on extracting ONLY the most critical information:
- Key decisions made and their rationale
- Critical files, components, or patterns identified
- Important constraints or requirements discovered
- Actionable insights for implementation
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
    "validation": [],  # No output files to summarize
}
```

### Format for Injection
```python
def format_phase_summaries(summaries: dict[str, str]) -> str:
    """Format summaries for agent context injection"""
    formatted = ["## Context from Previous Phases\n"]
    for phase_name, summary in summaries.items():
        formatted.append(f"### {phase_name.title()}\n{summary}\n")
    return "\n".join(formatted)
```

---

## 3. Gotchas System

### MCP Tool Definition
```python
@tool(
    "record_gotcha",
    "Record a gotcha or pitfall to avoid. Use this when you encounter something that future sessions should know.",
    {"gotcha": str, "context": str},
)
```

### Dual Storage Approach
1. **File-Based** (Primary): `memory/gotchas.md` - Always works offline
2. **Graphiti Graph DB** (Secondary): For cross-session retrieval and Memory UI

### Gotcha Entry Format
```markdown
## [2026-01-21 12:30]
<gotcha description>

_Context: <context>_
```

### Extraction from Sessions
Gotchas are automatically extracted at session end:

```json
{
  "gotchas_discovered": [
    {
      "gotcha": "What to avoid or watch out for",
      "trigger": "What situation causes this problem",
      "solution": "How to handle or prevent it"
    }
  ]
}
```

---

## 4. Discoveries System

### MCP Tool Definition
```python
@tool(
    "record_discovery",
    "Record a codebase discovery to session memory. Use this when you learn something important about the codebase.",
    {"file_path": str, "description": str, "category": str},
)
```

### Codebase Map Structure
Stored in `memory/codebase_map.json`:

```json
{
  "discovered_files": {
    "src/api/auth.py": {
      "description": "JWT authentication handler",
      "category": "authentication",
      "discovered_at": "2026-01-21T12:30:00Z"
    }
  },
  "last_updated": "2026-01-21T12:30:00Z"
}
```

### Extraction Schema
```json
{
  "file_insights": [
    {
      "path": "relative/path/to/file.ts",
      "purpose": "Brief description of file role in the system",
      "changes_made": "What was changed and why",
      "patterns_used": ["pattern names"],
      "gotchas": ["file-specific pitfalls"]
    }
  ],
  "patterns_discovered": [
    {
      "pattern": "Description of the coding pattern",
      "applies_to": "Where/when to use this pattern",
      "example": "File or code reference"
    }
  ]
}
```

---

## 5. Session Insights Extraction

### Automatic Post-Session Processing
```python
async def extract_session_insights(
    spec_dir: Path,
    project_dir: Path,
    subtask_id: str,
    session_num: int,
    commit_before: str | None,
    commit_after: str | None,
    success: bool,
    recovery_manager: Any,
) -> dict:
```

### Full Insight Schema
```json
{
  "file_insights": [...],
  "patterns_discovered": [...],
  "gotchas_discovered": [...],
  "approach_outcome": {
    "success": true,
    "approach_used": "Description of the approach taken",
    "why_it_worked": "Why this approach succeeded (null if failed)",
    "why_it_failed": "Why this approach failed (null if succeeded)",
    "alternatives_tried": ["other approaches attempted"]
  },
  "recommendations": [
    "Specific advice for future sessions working in this area"
  ]
}
```

### Input Collection
```python
def gather_extraction_inputs(
    spec_dir, project_dir, subtask_id, session_num,
    commit_before, commit_after, success, recovery_manager
) -> dict:
    return {
        "subtask_id": subtask_id,
        "subtask_description": _get_subtask_description(spec_dir, subtask_id),
        "session_num": session_num,
        "success": success,
        "diff": get_session_diff(project_dir, commit_before, commit_after),
        "changed_files": get_changed_files(project_dir, commit_before, commit_after),
        "commit_messages": get_commit_messages(project_dir, commit_before, commit_after),
        "attempt_history": _get_attempt_history(recovery_manager, subtask_id),
    }
```

---

## 6. Subagent Orchestration

### Agent Types Registry
Auto-Claude defines 20+ agent types, each with specific tool permissions:

```python
AGENT_CONFIGS = {
    # SPEC CREATION PHASES (Minimal tools, fast startup)
    "spec_gatherer": {
        "tools": BASE_READ_TOOLS + WEB_TOOLS,
        "mcp_servers": [],
        "auto_claude_tools": [],
        "thinking_default": "medium",
    },
    "spec_writer": {
        "tools": BASE_READ_TOOLS + BASE_WRITE_TOOLS,
        "mcp_servers": [],
        "thinking_default": "high",
    },
    "spec_critic": {
        "tools": BASE_READ_TOOLS,
        "mcp_servers": [],
        "thinking_default": "ultrathink",
    },
    
    # BUILD PHASES (Full tools + Graphiti memory)
    "planner": {
        "tools": BASE_READ_TOOLS + BASE_WRITE_TOOLS + WEB_TOOLS,
        "mcp_servers": ["context7", "graphiti", "auto-claude"],
        "mcp_servers_optional": ["linear"],
        "auto_claude_tools": [
            TOOL_GET_BUILD_PROGRESS,
            TOOL_GET_SESSION_CONTEXT,
            TOOL_RECORD_DISCOVERY,
        ],
        "thinking_default": "high",
    },
    "coder": {
        "tools": BASE_READ_TOOLS + BASE_WRITE_TOOLS + WEB_TOOLS,
        "mcp_servers": ["context7", "graphiti", "auto-claude"],
        "auto_claude_tools": [
            TOOL_UPDATE_SUBTASK_STATUS,
            TOOL_GET_BUILD_PROGRESS,
            TOOL_RECORD_DISCOVERY,
            TOOL_RECORD_GOTCHA,
            TOOL_GET_SESSION_CONTEXT,
        ],
        "thinking_default": "none",  # Coding doesn't use extended thinking!
    },
    
    # QA PHASES (Read + test + browser + Graphiti memory)
    "qa_reviewer": {
        "tools": BASE_READ_TOOLS + BASE_WRITE_TOOLS + WEB_TOOLS,
        "mcp_servers": ["context7", "graphiti", "auto-claude", "browser"],
        "auto_claude_tools": [
            TOOL_GET_BUILD_PROGRESS,
            TOOL_UPDATE_QA_STATUS,
            TOOL_GET_SESSION_CONTEXT,
        ],
        "thinking_default": "high",
    },
}
```

---

## 7. Dynamic Tool Selection

### Tool Categories
```python
# Core file operation tools
BASE_READ_TOOLS = ["Read", "Glob", "Grep"]
BASE_WRITE_TOOLS = ["Write", "Edit", "Bash"]
WEB_TOOLS = ["WebFetch", "WebSearch"]

# MCP tools by category
CONTEXT7_TOOLS = ["mcp__context7__resolve-library-id", "mcp__context7__get-library-docs"]
LINEAR_TOOLS = [...18 tools for project management...]
GRAPHITI_MCP_TOOLS = ["mcp__graphiti-memory__search_nodes", ...]
ELECTRON_TOOLS = ["mcp__electron__get_electron_window_info", ...]
PUPPETEER_TOOLS = ["mcp__puppeteer__puppeteer_navigate", ...]
```

### Dynamic Server Selection
```python
def get_required_mcp_servers(
    agent_type: str,
    project_capabilities: dict | None = None,  # From detect_project_capabilities()
    linear_enabled: bool = False,
    mcp_config: dict | None = None,  # Per-project overrides
) -> list[str]:
```

### Per-Agent Overrides
Environment variables allow per-agent customization:
- `AGENT_MCP_<agent_type>_ADD=server1,server2`
- `AGENT_MCP_<agent_type>_REMOVE=server1,server2`

---

## 8. Complexity Assessment

### Complexity Tiers
```python
class Complexity(Enum):
    SIMPLE = "simple"    # 1-2 files, single service, no integrations
    STANDARD = "standard"  # 3-10 files, 1-2 services, minimal integrations
    COMPLEX = "complex"  # 10+ files, multiple services, external integrations
```

### Keyword Detection
```python
SIMPLE_KEYWORDS = ["fix", "typo", "update", "change", "rename", ...]
COMPLEX_KEYWORDS = ["integrate", "api", "database", "migrate", "docker", ...]
MULTI_SERVICE_KEYWORDS = ["backend", "frontend", "worker", "service", ...]
```

### Assessment Signals
```python
signals = {
    "simple_keywords": count,
    "complex_keywords": count,
    "multi_service_keywords": count,
    "external_integrations": count,
    "infrastructure_changes": bool,
    "estimated_files": int,
    "estimated_services": int,
}
```

### Phase Selection by Complexity
```python
def phases_to_run(self) -> list[str]:
    if self.complexity == Complexity.SIMPLE:
        return ["discovery", "historical_context", "quick_spec", "validation"]
    elif self.complexity == Complexity.STANDARD:
        phases = ["discovery", "historical_context", "requirements"]
        if self.needs_research:
            phases.append("research")
        phases.extend(["context", "spec_writing", "planning", "validation"])
        return phases
    else:  # COMPLEX
        return [
            "discovery", "historical_context", "requirements", "research",
            "context", "spec_writing", "self_critique", "planning", "validation"
        ]
```

---

## 9. Implementation Plan Schema

### Full JSON Structure
```json
{
  "feature": "Feature name",
  "workflow_type": "feature|refactor|investigation|migration|simple",
  "services_involved": ["backend", "frontend"],
  "phases": [
    {
      "phase": 1,
      "name": "Phase name",
      "type": "implementation|investigation|migration",
      "subtasks": [
        {
          "id": "phase-1-task-1",
          "description": "Subtask description",
          "status": "pending|in_progress|completed|failed",
          "service": "backend",
          "all_services": false,
          "files_to_modify": ["path/to/file.py"],
          "files_to_create": ["path/to/new.py"],
          "patterns_from": ["path/to/reference.py"],
          "verification": {
            "type": "test|lint|api|browser|manual|none",
            "run": "npm test",
            "url": "http://localhost:3000/api/test",
            "method": "GET",
            "expect_status": 200,
            "expect_contains": "success",
            "scenario": "Manual test description"
          },
          "expected_output": "For investigation tasks",
          "actual_output": "What was discovered",
          "started_at": "ISO timestamp",
          "completed_at": "ISO timestamp",
          "session_id": 1,
          "critique_result": {}
        }
      ],
      "depends_on": [],
      "parallel_safe": false
    }
  ],
  "final_acceptance": ["Acceptance criteria"],
  "created_at": "ISO timestamp",
  "updated_at": "ISO timestamp",
  "spec_file": "spec.md",
  "status": "backlog|in_progress|ai_review|human_review|done",
  "planStatus": "pending|in_progress|review|completed",
  "recoveryNote": "Optional recovery note",
  "qa_signoff": {
    "status": "approved|rejected",
    "issues_found": []
  }
}
```

### Workflow Types
```python
class WorkflowType(Enum):
    FEATURE = "feature"         # Multi-service feature (phases = services)
    REFACTOR = "refactor"       # Migration work (phases = add, migrate, remove)
    INVESTIGATION = "investigation"  # Bug hunting (phases = investigate, hypothesize, fix)
    MIGRATION = "migration"     # Data migration (phases = prepare, test, execute, cleanup)
    SIMPLE = "simple"           # Single-service enhancement (minimal overhead)
```

---

## 10. Verification System

### Verification Types
```python
class VerificationType(Enum):
    TEST = "test"      # Run test command
    LINT = "lint"      # Run linter
    API = "api"        # HTTP request verification
    BROWSER = "browser"  # Browser automation
    MANUAL = "manual"  # Human verification
    NONE = "none"      # No verification
```

### Verification Schema
```python
@dataclass
class Verification:
    type: VerificationType
    run: str | None = None         # Command to run
    url: str | None = None         # URL for API/browser tests
    method: str | None = None      # HTTP method
    expect_status: int | None = None  # Expected HTTP status
    expect_contains: str | None = None  # Expected content
    scenario: str | None = None    # Description for manual tests
```

---

## 11. Build Progress Tracking

### Progress Calculation
```python
def get_progress(self) -> dict:
    total_subtasks = sum(len(p.subtasks) for p in self.phases)
    done_subtasks = sum(
        1 for p in self.phases for s in p.subtasks 
        if s.status == SubtaskStatus.COMPLETED
    )
    failed_subtasks = sum(
        1 for p in self.phases for s in p.subtasks 
        if s.status == SubtaskStatus.FAILED
    )
    completed_phases = sum(1 for p in self.phases if p.is_complete())
    
    return {
        "total_phases": len(self.phases),
        "completed_phases": completed_phases,
        "total_subtasks": total_subtasks,
        "completed_subtasks": done_subtasks,
        "failed_subtasks": failed_subtasks,
        "percent_complete": round(100 * done_subtasks / total_subtasks, 1),
        "is_complete": done_subtasks == total_subtasks and failed_subtasks == 0,
    }
```

### MCP Tool for Real-time Progress
```python
TOOL_GET_BUILD_PROGRESS = "mcp__auto-claude__get_build_progress"
```

---

## 12. Parallel Safe Flags

### Phase-Level Parallelization
```python
@dataclass
class Phase:
    phase: int
    name: str
    type: PhaseType
    subtasks: list[Subtask]
    depends_on: list[int] = field(default_factory=list)
    parallel_safe: bool = False  # Can subtasks in this phase run in parallel?
```

### Phase Availability
```python
def get_available_phases(self) -> list[Phase]:
    """Get phases whose dependencies are satisfied."""
    completed_phases = {p.phase for p in self.phases if p.is_complete()}
    available = []
    for phase in self.phases:
        if phase.is_complete():
            continue
        deps_met = all(d in completed_phases for d in phase.depends_on)
        if deps_met:
            available.append(phase)
    return available
```

---

## 13. MCP Tool Registry

### Auto-Claude Custom Tools
```python
# Tool name constants
TOOL_UPDATE_SUBTASK_STATUS = "mcp__auto-claude__update_subtask_status"
TOOL_GET_BUILD_PROGRESS = "mcp__auto-claude__get_build_progress"
TOOL_RECORD_DISCOVERY = "mcp__auto-claude__record_discovery"
TOOL_RECORD_GOTCHA = "mcp__auto-claude__record_gotcha"
TOOL_GET_SESSION_CONTEXT = "mcp__auto-claude__get_session_context"
TOOL_UPDATE_QA_STATUS = "mcp__auto-claude__update_qa_status"
```

### Dynamic MCP Server Creation
```python
def create_auto_claude_mcp_server(spec_dir: Path, project_dir: Path):
    """Create the MCP server with all auto-claude tools."""
    # Returns configured MCP server instance
```

### Tool Permission by Agent Type
Each agent type only sees tools relevant to their role via `allowed_tools`:

| Agent Type | Auto-Claude Tools |
|------------|-------------------|
| planner | get_build_progress, get_session_context, record_discovery |
| coder | update_subtask_status, get_build_progress, record_discovery, record_gotcha, get_session_context |
| qa_reviewer | get_build_progress, update_qa_status, get_session_context |
| qa_fixer | update_subtask_status, get_build_progress, update_qa_status, record_gotcha |

---

## 14. Session Memory Persistence

### Dual Storage Architecture
1. **File-Based** (Always available):
   - `memory/session_001.json` - Per-session insights
   - `memory/codebase_map.json` - File discoveries
   - `memory/gotchas.md` - Accumulated gotchas
   - `memory/patterns.md` - Discovered patterns

2. **Graphiti Graph DB** (When enabled):
   - Cross-session retrieval
   - Memory UI display
   - Entity relationships

### Session Insight Schema
```python
def save_session_insights(spec_dir: Path, session_num: int, insights: dict):
    session_data = {
        "session_number": session_num,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "subtasks_completed": insights.get("subtasks_completed", []),
        "discoveries": {
            "files_understood": {},
            "patterns_found": [],
            "gotchas_encountered": []
        },
        "what_worked": insights.get("what_worked", []),
        "what_failed": insights.get("what_failed", []),
        "recommendations_for_next_session": insights.get("recommendations", []),
    }
```

### Post-Session Processing
Auto-Claude automatically processes each session:
1. Extracts insights using LLM
2. Saves to file-based storage
3. Optionally saves to Graphiti
4. Records good commits for rollback safety
5. Updates recovery manager with attempt history
6. Updates Linear (if enabled)

---

## QA Validation Loop

### Self-Validating Architecture
```python
MAX_QA_ITERATIONS = 50
MAX_CONSECUTIVE_ERRORS = 3

async def run_qa_validation_loop(...) -> bool:
    while qa_iteration < MAX_QA_ITERATIONS:
        # 1. Run QA Reviewer
        status, response = await run_qa_agent_session(...)
        
        if status == "approved":
            return True
        elif status == "rejected":
            # Check for recurring issues (3+ occurrences → human escalation)
            if has_recurring:
                await escalate_to_human(spec_dir, recurring_issues, qa_iteration)
                return False
            
            # 2. Run QA Fixer
            fix_status, fix_response = await run_qa_fixer_session(...)
            
            # 3. Loop back to reviewer
```

### Recurring Issue Detection
Issues appearing 3+ times trigger human escalation.

---

## Summary: Features for OCTALUME Retrofitting

### High-Priority Features
1. **Thinking Levels System** - Phase-aware thinking budgets (64K for complex analysis)
2. **Context Compaction** - Summarize phase outputs to manage token usage
3. **Gotchas/Discoveries System** - Dual-storage memory with MCP tools
4. **Session Insight Extraction** - Automatic post-session learning capture
5. **Complexity Assessment** - Dynamic phase selection based on task analysis

### Medium-Priority Features
6. **Implementation Plan Schema** - Full subtask/phase/verification structure
7. **Dynamic Tool Selection** - Agent-type-aware tool permissions
8. **QA Validation Loop** - Self-validating with recurring issue detection
9. **Parallel Safe Flags** - Phase-level parallelization control

### Architecture Patterns
- **Dual Storage**: File-based primary + Graph DB secondary
- **Phase-Aware Configuration**: Different models/thinking levels per phase
- **MCP Tool Registry**: Custom tools for build management
- **Graceful Degradation**: Fallbacks when services unavailable
