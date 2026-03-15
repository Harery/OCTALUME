# MCP Tools Reference

OCTALUME provides 30+ MCP (Model Context Protocol) tools for seamless integration with Claude Code and other AI assistants.

## Configuration

Add to your Claude Code settings (`~/.claude/settings.json`):

```json
{
  "mcpServers": {
    "octalume": {
      "command": "python",
      "args": ["-m", "octalume.mcp.server"],
      "env": {
        "OCTALUME_STATE_DIR": "/path/to/project/.octalume"
      }
    }
  }
}
```

## Tool Categories

| Category | Tools | Description |
|----------|-------|-------------|
| Phase | 5 | Phase lifecycle management |
| Agent | 5 | AI agent orchestration |
| Artifact | 4 | Artifact tracking |
| Gate | 4 | Quality gate management |
| Compliance | 3 | Regulatory compliance |
| Project | 3 | Project state |
| Memory | 3 | Long-term context |
| Observability | 3 | Tracing and health |
| A2A | 2 | Agent-to-agent messaging |

---

## Phase Orchestration

### `lifecycle_phase_start`

Start a specific phase in the SDLC lifecycle.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| phase_number | integer | Yes | Phase number (1-8) |

**Example:**
```json
{
  "name": "lifecycle_phase_start",
  "arguments": {
    "phase_number": 1
  }
}
```

**Response:**
```json
{
  "success": true,
  "phase": {
    "number": 1,
    "name": "Vision and Strategy",
    "status": "in_progress",
    "started_at": "2026-03-15T10:00:00Z"
  }
}
```

---

### `lifecycle_phase_status`

Get detailed status of a specific phase.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| phase_number | integer | Yes | Phase number (1-8) |

**Response:**
```json
{
  "phase_number": 1,
  "status": "in_progress",
  "started_at": "2026-03-15T10:00:00Z",
  "artifacts": ["P1-DOC-001", "P1-DOC-002"],
  "agents": ["agent-vision-001"],
  "progress_percentage": 45,
  "exit_criteria": {
    "passed": ["business_case_created"],
    "failed": ["prd_completed"]
  }
}
```

---

### `lifecycle_phase_validate`

Validate exit criteria for a phase.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| phase_number | integer | Yes | Phase number (1-8) |

**Response:**
```json
{
  "passed": false,
  "missing_artifacts": ["P1-DOC-003"],
  "failed_criteria": ["prd_approved"],
  "warnings": ["business_case_needs_review"],
  "recommendations": ["Add stakeholder approval to PRD"]
}
```

---

### `lifecycle_phase_transition`

Transition from current phase to the next.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| artifacts | array | No | Artifacts to include |

**Response:**
```json
{
  "success": true,
  "previous_phase": 1,
  "current_phase": 2,
  "gate_result": {
    "passed": true
  }
}
```

---

### `lifecycle_phase_rollback`

Rollback to a previous phase.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| to_phase | integer | Yes | Target phase (1-7) |
| reason | string | Yes | Reason for rollback |

**Response:**
```json
{
  "success": true,
  "current_phase": 3,
  "rollback_log_id": "rb-20260315-001"
}
```

---

## Agent Management

### `lifecycle_agent_spawn`

Spawn a new AI agent for a phase-specific task.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| agent_type | string | Yes | Agent type (vision, requirements, architecture, planning, development, quality, deployment, operations, orchestrator) |
| task | string | Yes | Task description |
| config | object | No | Agent configuration |

**Example:**
```json
{
  "name": "lifecycle_agent_spawn",
  "arguments": {
    "agent_type": "architecture",
    "task": "Design microservices architecture for payment processing",
    "config": {
      "compliance_tags": ["pci"],
      "max_iterations": 10
    }
  }
}
```

---

### `lifecycle_agent_delegate`

Delegate a task to an existing agent.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| agent_id | string | Yes | Agent ID |
| task | string | Yes | Task description |
| context | object | No | Additional context |

---

### `lifecycle_agent_status`

Get status of a specific agent.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| agent_id | string | Yes | Agent ID |

**Response:**
```json
{
  "agent_id": "agent-arch-001",
  "type": "architecture",
  "status": "running",
  "current_task": "Designing API gateway",
  "progress": 0.6,
  "artifacts_created": ["P3-DSN-001"],
  "started_at": "2026-03-15T09:00:00Z",
  "estimated_completion": "2026-03-15T12:00:00Z"
}
```

---

### `lifecycle_agent_list`

List all agents, optionally filtered.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| phase | integer | No | Filter by phase |
| status | string | No | Filter by status (idle, running, completed, failed, timeout) |

---

### `lifecycle_agent_terminate`

Terminate a running agent.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| agent_id | string | Yes | Agent ID |
| reason | string | No | Termination reason |

---

## Artifact Tracking

### `lifecycle_artifact_create`

Create a new artifact with traceability ID.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| phase | integer | Yes | Phase number (1-8) |
| artifact_type | string | Yes | Type (document, code, test, configuration, design, report, decision) |
| name | string | Yes | Artifact name |
| content | string/object | No | Content |
| file_path | string | No | File path |
| compliance_tags | array | No | Compliance tags |

**Response:**
```json
{
  "success": true,
  "artifact": {
    "id": "P1-DOC-001",
    "phase": 1,
    "name": "Product Requirements Document",
    "artifact_type": "document",
    "created_at": "2026-03-15T10:00:00Z",
    "compliance_tags": ["hipaa", "soc2"]
  }
}
```

---

### `lifecycle_artifact_get`

Get an artifact by its ID.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| artifact_id | string | Yes | Artifact ID (e.g., P1-DOC-001) |

---

### `lifecycle_artifact_search`

Search artifacts by phase, type, or content.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| phase | integer | No | Filter by phase |
| artifact_type | string | No | Filter by type |
| search_term | string | No | Search in name/content |
| limit | integer | No | Max results (default: 50) |

---

### `lifecycle_artifact_link`

Link two artifacts for traceability.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| source_artifact_id | string | Yes | Source artifact ID |
| target_artifact_id | string | Yes | Target artifact ID |

---

## Quality Gates

### `lifecycle_gate_check`

Check if a quality gate passes.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| phase_number | integer | Yes | Phase number (1-8) |
| gate_type | string | No | Gate type (entry, exit) |

**Response:**
```json
{
  "passed": false,
  "phase": 1,
  "gate_type": "exit",
  "criteria": [
    {"id": "business_case", "name": "Business Case Created", "passed": true},
    {"id": "prd", "name": "PRD Completed", "passed": false},
    {"id": "stakeholder_approval", "name": "Stakeholder Approval", "passed": false}
  ],
  "missing_artifacts": ["P1-DOC-002"],
  "recommendations": ["Complete the Product Requirements Document"]
}
```

---

### `lifecycle_gate_bypass`

Bypass a quality gate (requires approval).

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| phase_number | integer | Yes | Phase number |
| reason | string | Yes | Bypass reason |
| approver | string | Yes | Approver name/ID |

---

### `lifecycle_gate_list`

List all quality gate definitions.

**Response:**
```json
{
  "gates": [
    {
      "phase": 1,
      "type": "exit",
      "criteria": [
        {"id": "business_case", "name": "Business Case", "required": true},
        {"id": "prd", "name": "Product Requirements", "required": true}
      ]
    }
  ]
}
```

---

### `lifecycle_go_no_go`

Execute a go/no-go decision for phase transition.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| phase_number | integer | Yes | Phase number |

**Response:**
```json
{
  "decision": "no-go",
  "phase": 1,
  "blockers": [
    "Missing: Product Requirements Document",
    "Missing: Stakeholder Approval"
  ],
  "risks": [
    "Business case not reviewed by finance"
  ],
  "recommendations": [
    "Complete PRD before proceeding",
    "Schedule stakeholder review meeting"
  ]
}
```

---

## Compliance

### `lifecycle_compliance_scan`

Run a compliance scan.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| standards | array | No | Standards to scan (hipaa, soc2, pci_dss, gdpr, sox, dod_itar) |
| scope | string | No | Scope (all, artifacts, processes, documentation) |

**Response:**
```json
{
  "scan_id": "scan-20260315-001",
  "standards": ["hipaa", "soc2"],
  "results": {
    "hipaa": {
      "compliant": false,
      "score": 0.75,
      "findings": [
        {"control": "164.312(a)", "status": "pass", "description": "Access control"},
        {"control": "164.312(b)", "status": "fail", "description": "Audit controls missing"}
      ]
    },
    "soc2": {
      "compliant": true,
      "score": 0.92
    }
  }
}
```

---

### `lifecycle_compliance_report`

Generate a compliance report.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| standard | string | Yes | Standard name |
| format | string | No | Format (json, markdown, html) |

---

### `lifecycle_compliance_configure`

Configure compliance standards.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| standards | array | Yes | Standards to enable |

---

## Project State

### `lifecycle_project_init`

Initialize a new project.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| name | string | Yes | Project name |
| description | string | No | Description |
| compliance_standards | array | No | Compliance standards |

---

### `lifecycle_project_status`

Get complete project status.

**Response:**
```json
{
  "id": "proj-001",
  "name": "my-project",
  "current_phase": 3,
  "status": "in_progress",
  "phases": {...},
  "artifacts": {...},
  "agents": {...},
  "compliance_standards": ["hipaa", "soc2"]
}
```

---

### `lifecycle_project_summary`

Get human-readable summary.

---

## Memory & Context

### `lifecycle_memory_save`

Save a memory entry.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| category | string | Yes | Category (decisions, progress, blockers, notes, context) |
| key | string | Yes | Entry key |
| value | string/object | Yes | Entry value |
| metadata | object | No | Additional metadata |

---

### `lifecycle_memory_load`

Load a memory entry.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| category | string | Yes | Category |
| key | string | Yes | Entry key |

---

### `lifecycle_memory_query`

Query memory entries.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| category | string | No | Filter by category |
| search_term | string | No | Search term |
| limit | integer | No | Max results (default: 50) |

---

## Observability

### `lifecycle_trace_add`

Add a trace entry.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| phase | integer | Yes | Phase number |
| action | string | Yes | Action name |
| artifact_id | string | No | Related artifact |
| agent_id | string | No | Related agent |
| duration_ms | number | No | Duration in milliseconds |
| metadata | object | No | Additional metadata |

---

### `lifecycle_trace_get`

Get trace entries.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| phase | integer | No | Filter by phase |
| limit | integer | No | Max results (default: 100) |

---

### `lifecycle_health_check`

Perform health check on all agents.

**Response:**
```json
{
  "status": "healthy",
  "agents": {
    "total": 5,
    "running": 3,
    "idle": 2,
    "failed": 0
  },
  "memory": {
    "entries": 42,
    "size_mb": 2.1
  },
  "artifacts": {
    "total": 15,
    "by_phase": {1: 5, 2: 3, 3: 7}
  }
}
```

---

## A2A Communication

### `lifecycle_agent_message`

Send message between agents.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| from_agent | string | Yes | Sender agent ID |
| to_agent | string | Yes | Receiver agent ID |
| message_type | string | Yes | Message type |
| payload | object | Yes | Message payload |

---

### `lifecycle_agent_broadcast`

Broadcast message to agents.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| from_agent | string | Yes | Sender agent ID |
| message_type | string | Yes | Message type |
| payload | object | Yes | Message payload |
| phase_filter | integer | No | Only agents in this phase |
