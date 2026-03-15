# Architecture

OCTALUME system architecture and design decisions.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           Client Layer                                   │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────────┐  │
│  │   CLI (Click)   │  │  Web Dashboard  │  │   MCP (Claude Code)     │  │
│  │                 │  │   (React)       │  │                         │  │
│  └────────┬────────┘  └────────┬────────┘  └────────────┬────────────┘  │
└───────────┼────────────────────┼─────────────────────────┼──────────────┘
            │                    │                         │
            └────────────────────┼─────────────────────────┘
                                 │
┌────────────────────────────────┼────────────────────────────────────────┐
│                         API Layer                                        │
│  ┌─────────────────────────────┴─────────────────────────────────────┐  │
│  │                     FastAPI Backend                                │  │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌───────────┐ │  │
│  │  │ Phase Router │ │ Agent Router │ │Artifact Routr│ │Compliance │ │  │
│  │  └──────────────┘ └──────────────┘ └──────────────┘ └───────────┘ │  │
│  └───────────────────────────────────────────────────────────────────┘  │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
┌────────────────────────────────┼────────────────────────────────────────┐
│                        Core Layer                                        │
│  ┌─────────────────────────────┴─────────────────────────────────────┐  │
│  │                      Phase Engine                                  │  │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌───────────┐ │  │
│  │  │Gate Validator│ │ Orchestrator │ │State Manager │ │Memory Bank│ │  │
│  │  └──────────────┘ └──────────────┘ └──────────────┘ └───────────┘ │  │
│  └───────────────────────────────────────────────────────────────────┘  │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
┌────────────────────────────────┼────────────────────────────────────────┐
│                      Domain Layer                                        │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌───────────────┐   │
│  │   Agents     │ │  Compliance  │ │     A2A      │ │    Models     │   │
│  │ (9 types)    │ │ (6 standards)│ │  Protocol    │ │  (Pydantic)   │   │
│  └──────────────┘ └──────────────┘ └──────────────┘ └─────────────┬─┘   │
└──────────────────────────────────────────────────────────────────┬──────┘
                                   │
┌──────────────────────────────────┼──────────────────────────────────────┐
│                      Storage Layer                                       │
│  ┌───────────────────────────────┴───────────────────────────────────┐  │
│  │                        File System                                  │  │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌───────────┐ │  │
│  │  │   state.json │ │  memory.json │ │   traces/    │ │ artifacts │ │  │
│  │  └──────────────┘ └──────────────┘ └──────────────┘ └───────────┘ │  │
│  └───────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Core Components

### PhaseEngine

Central orchestrator for phase execution.

**Responsibilities:**
- Phase initialization
- Phase transitions
- Gate validation orchestration
- State updates

**Dependencies:**
- StateManager
- GateValidator
- AgentOrchestrator

```python
class PhaseEngine:
    def __init__(
        self,
        state_manager: ProjectStateManager,
        gate_validator: GateValidator,
        orchestrator: AgentOrchestrator
    ):
        ...

    async def start_phase(self, state: ProjectState, phase: int) -> ProjectState
    async def complete_phase(self, state: ProjectState, phase: int) -> tuple[ProjectState, GateResult]
    async def transition_phase(self, state: ProjectState, from_phase: int, to_phase: int) -> tuple[ProjectState, GateResult]
    async def rollback_phase(self, state: ProjectState, to_phase: int, reason: str) -> ProjectState
```

---

### GateValidator

Quality gate validation.

**Responsibilities:**
- Entry criteria validation
- Exit criteria validation
- Go/no-go decisions
- Gate bypass management

```python
class GateValidator:
    def __init__(self, state_manager: ProjectStateManager):
        ...

    async def validate_entry(self, state: ProjectState, phase: int) -> GateResult
    async def validate_exit(self, state: ProjectState, phase: int) -> GateResult
    async def bypass_gate(self, state: ProjectState, phase: int, reason: str, approver: str) -> GateResult
    async def run_go_no_go(self, state: ProjectState, phase: int) -> dict
    def list_all_gates(self) -> list[dict]
```

---

### AgentOrchestrator

AI agent lifecycle management.

**Responsibilities:**
- Agent spawning
- Task delegation
- Agent communication
- Health monitoring

```python
class AgentOrchestrator:
    def __init__(self, state_manager: ProjectStateManager):
        ...

    async def spawn_agent(self, state: ProjectState, agent_type: str, task: str, config: dict) -> str
    async def delegate_task(self, state: ProjectState, agent_id: str, task: str, context: dict) -> str
    async def get_agent_status(self, state: ProjectState, agent_id: str) -> dict
    async def list_agents(self, state: ProjectState, phase: int, status: str) -> list[dict]
    async def terminate_agent(self, state: ProjectState, agent_id: str, reason: str) -> bool
    async def health_check(self, state: ProjectState) -> dict
    async def send_agent_message(self, state: ProjectState, ...) -> str
    async def broadcast_message(self, state: ProjectState, ...) -> list[str]
```

---

### ProjectStateManager

State persistence.

**Responsibilities:**
- State CRUD operations
- State serialization
- State validation

```python
class ProjectStateManager:
    def __init__(self, state_dir: Path | None = None):
        ...

    async def create(self, name: str, description: str, compliance_standards: list) -> ProjectState
    async def load(self) -> ProjectState | None
    async def save(self, state: ProjectState) -> None
    async def get_or_create(self) -> ProjectState
    async def get_summary(self, state: ProjectState) -> dict
```

---

### MemoryBank

Long-term memory storage.

**Responsibilities:**
- Memory entry storage
- Memory queries
- Trace logging

```python
class MemoryBank:
    def __init__(self, state_dir: Path | None = None):
        ...

    def save(self, category: str, key: str, value: Any, metadata: dict) -> str
    def load(self, category: str, key: str) -> Any | None
    def query(self, category: str, search_term: str, limit: int) -> list[dict]
    def add_trace(self, phase: int, action: str, ...) -> str
    def get_traces(self, phase: int, limit: int) -> list[dict]
```

---

## Data Models

### ProjectState

```python
class ProjectState(BaseModel):
    id: UUID
    name: str
    description: str | None
    current_phase: int = 1
    phases: dict[int, Phase]
    artifacts: dict[str, Artifact]
    agents: dict[str, Agent]
    compliance_standards: list[ComplianceStandard]
    artifact_counter: dict[str, int]
    created_at: datetime
    updated_at: datetime
```

### Phase

```python
class Phase(BaseModel):
    number: int
    name: str
    description: str
    owner: str
    status: PhaseStatus
    artifacts: list[str]
    agents: list[str]
    entry_criteria: list[str]
    exit_criteria: list[str]
    started_at: datetime | None
    completed_at: datetime | None
    duration_estimate_days: int = 7
```

### Artifact

```python
class Artifact(BaseModel):
    id: str  # Pattern: P{N}-{SECTION}-{###}
    phase: int
    name: str
    artifact_type: ArtifactType
    content: str | dict | None
    file_path: str | None
    compliance_tags: list[ComplianceStandard]
    linked_artifacts: list[str]
    created_at: datetime
    updated_at: datetime

    @field_validator('id')
    @classmethod
    def validate_id_format(cls, v: str) -> str:
        pattern = r'^P[1-8]-(DOC|CODE|TEST|CFG|DSN|RPT|DEC)-\d{3}$'
        if not re.match(pattern, v):
            raise ValueError('Invalid artifact ID format')
        return v
```

### Agent

```python
class Agent(BaseModel):
    id: str
    agent_type: AgentType
    phase: int
    task: str
    status: AgentStatus
    config: dict
    artifacts_created: list[str]
    started_at: datetime
    completed_at: datetime | None
    error: str | None
```

---

## MCP Server

The MCP server exposes 30+ tools via stdio transport.

```python
class OctalumeMCPServer:
    def __init__(self, state_dir: Path | None = None):
        self.server = Server("octalume")
        self.state_manager = ProjectStateManager(state_dir)
        self.gate_validator = GateValidator(self.state_manager)
        self.orchestrator = AgentOrchestrator(self.state_manager)
        self.engine = PhaseEngine(...)
        self.compliance_scanner = ComplianceScanner()
        self._register_tools()

    def _register_tools(self) -> None:
        # Register 30+ tools
        for tool_def in TOOLS:
            self.server.add_tool(Tool(**tool_def))

        self.server.set_tool_handler(self._handle_tool_call)
```

---

## Directory Structure

```
.octalume/
├── state.json           # Project state
├── memory/
│   └── memory.json      # Long-term memory
├── traces/
│   ├── phase_1.json
│   ├── phase_2.json
│   └── ...
└── artifacts/
    ├── P1-DOC-001.md
    ├── P2-REQ-001.md
    └── ...
```

---

## Technology Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| CLI | Click | Command-line interface |
| Web Frontend | React, TypeScript | Dashboard UI |
| Web Backend | FastAPI | REST API |
| MCP Server | mcp Python SDK | Claude Code integration |
| Data Models | Pydantic v2 | Validation & serialization |
| Logging | structlog | Structured logging |
| Testing | pytest, pytest-asyncio | Test framework |
| Package | hatch | Build & distribution |

---

## Design Decisions

### Why File-Based Storage?

- **Simplicity**: No external database required
- **Portability**: Easy to move between machines
- **Version Control**: State can be committed to git
- **Audit Trail**: File history provides traceability

### Why Async Throughout?

- **Non-blocking**: Multiple agents can run concurrently
- **Scalability**: Handles I/O-bound operations efficiently
- **MCP Compatibility**: Async matches MCP server pattern

### Why Pydantic v2?

- **Performance**: Faster than v1
- **Validation**: Automatic data validation
- **Serialization**: JSON schema generation
- **Type Safety**: Runtime type checking

---

## Extension Points

### Adding New Compliance Standards

```python
# octalume/compliance/new_standard.py

class NewStandardScanner:
    async def scan(self, state: ProjectState) -> dict:
        # Implement scanning logic
        ...

    async def generate_report(self, state: ProjectState, format: str) -> str:
        # Generate compliance report
        ...
```

### Adding New Agent Types

```python
# octalume/agents/new_agent.py

class NewAgentType:
    AGENT_TYPE = "new_type"

    async def execute(self, task: str, config: dict) -> dict:
        # Implement agent logic
        ...
```

### Adding New MCP Tools

```python
# octalume/mcp/server.py

TOOLS.append({
    "name": "lifecycle_new_tool",
    "description": "Description of new tool",
    "input_schema": {
        "type": "object",
        "properties": {...}
    }
})
```
