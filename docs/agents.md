# Multi-Agent Orchestration

OCTALUME uses 9 specialized AI agents for phase-specific tasks.

## Agent Types

| Type | Phase | Focus |
|------|-------|-------|
| Vision | 1 | Business case, market analysis |
| Requirements | 2 | Requirements elicitation |
| Architecture | 3 | System design |
| Planning | 4 | Project planning |
| Development | 5 | Code implementation |
| Quality | 6 | Testing, security |
| Deployment | 7 | Release management |
| Operations | 8 | Monitoring, incidents |
| Orchestrator | All | Coordination |

---

## Agent Lifecycle

### Spawning

```python
from octalume.core.orchestrator import AgentOrchestrator

orchestrator = AgentOrchestrator(manager)

agent_id = await orchestrator.spawn_agent(
    state=state,
    agent_type="architecture",
    task="Design microservices architecture for payment system",
    config={
        "max_iterations": 10,
        "compliance_tags": ["pci"],
        "timeout_minutes": 60
    }
)
```

### Delegation

```python
task_id = await orchestrator.delegate_task(
    state=state,
    agent_id=agent_id,
    task="Create API gateway design",
    context={
        "priority": "high",
        "dependencies": ["P3-DSN-001"]
    }
)
```

### Monitoring

```python
status = await orchestrator.get_agent_status(state, agent_id)

# Response:
{
    "agent_id": "agent-arch-001",
    "type": "architecture",
    "status": "running",
    "current_task": "Designing payment service",
    "progress": 0.65,
    "artifacts_created": ["P3-DSN-001", "P3-DSN-002"],
    "started_at": "2026-03-15T09:00:00Z",
    "estimated_completion": "2026-03-15T12:00:00Z"
}
```

### Termination

```python
success = await orchestrator.terminate_agent(
    state=state,
    agent_id=agent_id,
    reason="Task completed successfully"
)
```

---

## Agent Communication

### Direct Messaging

```python
message_id = await orchestrator.send_agent_message(
    state=state,
    from_agent="agent-arch-001",
    to_agent="agent-dev-001",
    message_type="handoff",
    payload={
        "design_doc": "P3-DSN-001",
        "instructions": "Implement according to spec"
    }
)
```

### Broadcast

```python
message_ids = await orchestrator.broadcast_message(
    state=state,
    from_agent="orchestrator",
    message_type="phase_transition",
    payload={
        "from_phase": 3,
        "to_phase": 4,
        "artifacts": ["P3-DSN-001"]
    },
    phase_filter=3  # Only agents in phase 3
)
```

---

## Agent Capabilities by Type

### Vision Agent (Phase 1)

**Responsibilities:**
- Market research and analysis
- Business case creation
- ROI projections
- Competitive analysis
- PRD drafting

**Example Task:**
```
"Research the healthcare SaaS market and create a business case
for a patient portal with HIPAA compliance"
```

---

### Requirements Agent (Phase 2)

**Responsibilities:**
- Requirements elicitation
- User story creation
- Acceptance criteria definition
- Traceability matrix maintenance
- MVP scope definition

**Example Task:**
```
"Elicit requirements for the appointment scheduling feature
and create user stories with acceptance criteria"
```

---

### Architecture Agent (Phase 3)

**Responsibilities:**
- System architecture design
- Security architecture
- Data architecture
- Threat modeling
- API specification

**Example Task:**
```
"Design a microservices architecture for the payment processing
system with PCI DSS compliance"
```

---

### Planning Agent (Phase 4)

**Responsibilities:**
- Work breakdown structure
- Resource planning
- Sprint planning
- Risk assessment
- Timeline creation

**Example Task:**
```
"Create a sprint plan for the MVP features with 5 developers
over 6 sprints"
```

---

### Development Agent (Phase 5)

**Responsibilities:**
- Code implementation
- Unit testing
- Code review
- Technical documentation
- Bug fixes

**Example Task:**
```
"Implement the authentication service with OAuth2 and JWT
according to the architecture spec P3-DSN-001"
```

---

### Quality Agent (Phase 6)

**Responsibilities:**
- Test execution
- Security testing
- Performance testing
- Compliance validation
- UAT coordination

**Example Task:**
```
"Run security tests for HIPAA compliance on the patient
data module"
```

---

### Deployment Agent (Phase 7)

**Responsibilities:**
- Deployment planning
- Infrastructure setup
- Release coordination
- Smoke testing
- Rollback procedures

**Example Task:**
```
"Create deployment plan for production release with zero
downtime strategy"
```

---

### Operations Agent (Phase 8)

**Responsibilities:**
- System monitoring
- Incident response
- Root cause analysis
- Performance optimization
- Capacity planning

**Example Task:**
```
"Set up monitoring alerts for the payment service with
PagerDuty integration"
```

---

### Orchestrator Agent

**Responsibilities:**
- Agent coordination
- Phase transitions
- Resource allocation
- Cross-agent communication
- Workflow management

**Example Task:**
```
"Coordinate the transition from Phase 3 to Phase 4,
ensuring all artifacts are ready"
```

---

## Health Monitoring

```python
health = await orchestrator.health_check(state)

# Response:
{
    "status": "healthy",
    "agents": {
        "total": 5,
        "running": 3,
        "idle": 1,
        "completed": 1,
        "failed": 0
    },
    "resources": {
        "memory_mb": 512,
        "cpu_percent": 25
    },
    "last_activity": "2026-03-15T10:30:00Z"
}
```

---

## CLI Usage

```bash
# List agents
octalume agents list --phase 3 --status running

# Spawn agent
octalume agents spawn architecture --task "Design data layer"

# Check status
octalume agents status agent-arch-001

# Terminate
octalume agents terminate agent-arch-001 --reason "Completed"
```

---

## MCP Integration

```json
{
  "name": "lifecycle_agent_spawn",
  "arguments": {
    "agent_type": "quality",
    "task": "Run HIPAA compliance scan",
    "config": {
      "compliance_tags": ["hipaa"],
      "scope": "artifacts"
    }
  }
}
```
