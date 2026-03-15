# Python API Reference

Programmatic access to OCTALUME's full capabilities.

## Installation

```bash
pip install octalume
```

## Core Components

### ProjectStateManager

Manages project state persistence.

```python
from octalume.core.state import ProjectStateManager
from pathlib import Path

# Initialize with default directory
manager = ProjectStateManager()

# Or with custom directory
manager = ProjectStateManager(state_dir=Path("/path/to/.octalume"))

# Create new project
state = await manager.create(
    name="my-project",
    description="Building something amazing",
    compliance_standards=["hipaa", "soc2"]
)

# Load existing project
state = await manager.load()

# Save changes
await manager.save(state)

# Get project summary
summary = await manager.get_summary(state)
```

---

### PhaseEngine

Executes phase transitions and manages lifecycle.

```python
from octalume.core.engine import PhaseEngine
from octalume.core.gates import GateValidator
from octalume.core.orchestrator import AgentOrchestrator

# Initialize with dependencies
manager = ProjectStateManager()
gate_validator = GateValidator(manager)
orchestrator = AgentOrchestrator(manager)
engine = PhaseEngine(manager, gate_validator, orchestrator)

# Start a phase
state = await engine.start_phase(state, phase_number=1)

# Get phase status
status = await engine.get_phase_status(state, phase_number=1)

# Complete a phase (runs quality gate)
state, gate_result = await engine.complete_phase(state, phase_number=1)
if gate_result.passed:
    print("Phase completed successfully!")
else:
    print(f"Gate failed: {gate_result.missing_artifacts}")

# Transition to next phase
state, gate_result = await engine.transition_phase(state, from_phase=1, to_phase=2)

# Rollback to previous phase
state = await engine.rollback_phase(state, to_phase=3, reason="Security audit failed")
```

---

### GateValidator

Validates quality gates for phase transitions.

```python
from octalume.core.gates import GateValidator

validator = GateValidator(manager)

# Validate entry criteria
entry_result = await validator.validate_entry(state, phase_number=2)
if not entry_result.passed:
    print(f"Cannot start phase: {entry_result.reasons}")

# Validate exit criteria
exit_result = await validator.validate_exit(state, phase_number=1)
print(f"Passed: {exit_result.passed}")
print(f"Missing artifacts: {exit_result.missing_artifacts}")
print(f"Failed criteria: {exit_result.failed_criteria}")

# Bypass gate (with approval)
bypass_result = await validator.bypass_gate(
    state=state,
    phase_num=1,
    reason="Emergency deployment approved by CTO",
    approver="cto@company.com"
)

# Run go/no-go decision
decision = await validator.run_go_no_go(state, phase_number=1)
print(f"Decision: {decision['decision']}")
print(f"Blockers: {decision['blockers']}")

# List all gates
gates = validator.list_all_gates()
```

---

### AgentOrchestrator

Spawns and manages AI agents.

```python
from octalume.core.orchestrator import AgentOrchestrator

orchestrator = AgentOrchestrator(manager)

# Spawn a new agent
agent_id = await orchestrator.spawn_agent(
    state=state,
    agent_type="architecture",
    task="Design the data layer architecture",
    config={
        "max_iterations": 10,
        "compliance_tags": ["hipaa"]
    }
)

# Delegate task to existing agent
task_id = await orchestrator.delegate_task(
    state=state,
    agent_id=agent_id,
    task="Create API design document",
    context={"priority": "high"}
)

# Get agent status
status = await orchestrator.get_agent_status(state, agent_id)

# List agents
agents = await orchestrator.list_agents(
    state=state,
    phase=3,
    status="running"
)

# Terminate agent
success = await orchestrator.terminate_agent(
    state=state,
    agent_id=agent_id,
    reason="Task completed"
)

# Health check
health = await orchestrator.health_check(state)

# Agent-to-agent messaging
message_id = await orchestrator.send_agent_message(
    state=state,
    from_agent="agent-arch-001",
    to_agent="agent-dev-001",
    message_type="handoff",
    payload={"design_doc": "P3-DSN-001"}
)

# Broadcast to all agents in a phase
message_ids = await orchestrator.broadcast_message(
    state=state,
    from_agent="orchestrator",
    message_type="phase_transition",
    payload={"next_phase": 4},
    phase_filter=3
)
```

---

### MemoryBank

Long-term memory storage.

```python
from octalume.core.memory import MemoryBank

memory = MemoryBank(state_dir=Path(".octalume/memory"))

# Save memory
entry_id = memory.save(
    category="decisions",
    key="database-choice",
    value={"chosen": "PostgreSQL", "reason": "ACID compliance needed"},
    metadata={"phase": 3, "decided_by": "architect"}
)

# Load memory
value = memory.load("decisions", "database-choice")

# Query memory
results = memory.query(
    category="decisions",
    search_term="database",
    limit=10
)

# Add trace
trace_id = memory.add_trace(
    phase=3,
    action="artifact_created",
    artifact_id="P3-DSN-001",
    agent_id="agent-arch-001",
    duration_ms=1500
)

# Get traces
traces = memory.get_traces(phase=3, limit=100)
```

---

## Models

### ProjectState

Main project state container.

```python
from octalume.core.models import ProjectState, PhaseStatus
from uuid import uuid4

state = ProjectState(
    id=uuid4(),
    name="my-project",
    description="Project description",
    current_phase=1,
    phases={},
    artifacts={},
    agents={},
    compliance_standards=[],
    artifact_counter={}
)
```

### Phase

Phase definition.

```python
from octalume.core.models import Phase, PhaseStatus

phase = Phase(
    number=1,
    name="Vision and Strategy",
    description="Define product vision and business case",
    owner="Product Owner",
    status=PhaseStatus.IN_PROGRESS,
    artifacts=[],
    entry_criteria=["business_idea_identified"],
    exit_criteria=["business_case_approved", "prd_completed"],
    started_at=datetime.now()
)
```

### Artifact

Traceable artifact.

```python
from octalume.core.models import Artifact, ArtifactType, ComplianceStandard

artifact = Artifact(
    id="P1-DOC-001",
    phase=1,
    name="Product Requirements Document",
    artifact_type=ArtifactType.DOCUMENT,
    content="# PRD\n...",
    file_path="docs/prd.md",
    compliance_tags=[ComplianceStandard.HIPAA, ComplianceStandard.SOC2],
    linked_artifacts=[]
)
```

### Agent

AI agent instance.

```python
from octalume.core.models import Agent, AgentStatus, AgentType

agent = Agent(
    id="agent-arch-001",
    agent_type=AgentType.ARCHITECTURE,
    phase=3,
    task="Design system architecture",
    status=AgentStatus.RUNNING,
    config={"max_iterations": 10}
)
```

### GateResult

Quality gate validation result.

```python
from octalume.core.models import GateResult

result = GateResult(
    passed=False,
    phase=1,
    missing_artifacts=["P1-DOC-002"],
    failed_criteria=["prd_approved"],
    warnings=["business_case_needs_review"]
)
```

## Enums

### PhaseStatus

```python
from octalume.core.models import PhaseStatus

PhaseStatus.NOT_STARTED
PhaseStatus.IN_PROGRESS
PhaseStatus.BLOCKED
PhaseStatus.COMPLETED
```

### AgentStatus

```python
from octalume.core.models import AgentStatus

AgentStatus.IDLE
AgentStatus.RUNNING
AgentStatus.COMPLETED
AgentStatus.FAILED
AgentStatus.TIMEOUT
```

### AgentType

```python
from octalume.core.models import AgentType

AgentType.VISION
AgentType.REQUIREMENTS
AgentType.ARCHITECTURE
AgentType.PLANNING
AgentType.DEVELOPMENT
AgentType.QUALITY
AgentType.DEPLOYMENT
AgentType.OPERATIONS
AgentType.ORCHESTRATOR
```

### ArtifactType

```python
from octalume.core.models import ArtifactType

ArtifactType.DOCUMENT
ArtifactType.CODE
ArtifactType.TEST
ArtifactType.CONFIGURATION
ArtifactType.DESIGN
ArtifactType.REPORT
ArtifactType.DECISION
```

### ComplianceStandard

```python
from octalume.core.models import ComplianceStandard

ComplianceStandard.HIPAA
ComplianceStandard.SOC2
ComplianceStandard.PCI_DSS
ComplianceStandard.GDPR
ComplianceStandard.SOX
ComplianceStandard.DOD_ITAR
```

## Compliance Scanners

```python
from octalume.compliance.scanner import ComplianceScanner
from octalume.core.models import ComplianceStandard

scanner = ComplianceScanner()

# Run scan
result = await scanner.scan(
    state=state,
    standards=[ComplianceStandard.HIPAA, ComplianceStandard.SOC2],
    scope="all"
)

# Generate report
report = await scanner.generate_report(
    state=state,
    standard=ComplianceStandard.HIPAA,
    format="markdown"
)
```

## Full Example

```python
import asyncio
from pathlib import Path
from octalume.core.state import ProjectStateManager
from octalume.core.engine import PhaseEngine
from octalume.core.gates import GateValidator
from octalume.core.orchestrator import AgentOrchestrator
from octalume.core.models import Artifact, ArtifactType, ComplianceStandard

async def main():
    # Setup
    manager = ProjectStateManager(state_dir=Path(".octalume"))
    gate_validator = GateValidator(manager)
    orchestrator = AgentOrchestrator(manager)
    engine = PhaseEngine(manager, gate_validator, orchestrator)

    # Create project
    state = await manager.create(
        name="healthcare-portal",
        description="Patient portal for healthcare",
        compliance_standards=["hipaa"]
    )
    print(f"Created project: {state.name}")

    # Start phase 1
    state = await engine.start_phase(state, 1)
    print(f"Started phase 1: {state.phases[1].name}")

    # Create artifact
    artifact = Artifact(
        id="P1-DOC-001",
        phase=1,
        name="Business Case",
        artifact_type=ArtifactType.DOCUMENT,
        content="...",
        compliance_tags=[ComplianceStandard.HIPAA]
    )
    state.artifacts[artifact.id] = artifact
    await manager.save(state)
    print(f"Created artifact: {artifact.id}")

    # Check gate
    result = await gate_validator.validate_exit(state, 1)
    print(f"Gate passed: {result.passed}")

    # Complete phase
    if result.passed:
        state, _ = await engine.complete_phase(state, 1)
        print(f"Phase 1 complete. Current phase: {state.current_phase}")

asyncio.run(main())
```
