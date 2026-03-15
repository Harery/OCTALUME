# CLAUDE.md - OCTALUME Framework Context

This file is auto-loaded when Claude Code starts. It provides context for working with OCTALUME.

---

## Framework Overview

OCTALUME (Octa = 8 phases, Lume = light/guidance) is an AI-native enterprise SDLC framework built in Python with 30+ MCP tools for Claude Code integration.

### Core Principles

1. Sequential phase progression with quality gates
2. 30+ MCP tools for Claude Code integration
3. Multi-agent orchestration (9 specialized agents)
4. Compliance ready (HIPAA, SOC 2, PCI DSS, GDPR, SOX)
5. Complete traceability from requirements to deployment

---

## Directory Structure

```
OCTALUME/
├── octalume/                 # Main Python package
│   ├── core/                 # Engine, gates, orchestrator, state, memory
│   ├── mcp/                  # MCP server with 30+ tools
│   ├── agents/               # 9 phase-specific AI agents
│   ├── compliance/           # Compliance scanners
│   ├── a2a/                  # Agent-to-agent protocol
│   ├── utils/                # Logging, configuration
│   └── cli.py                # Click-based CLI
├── web/                      # FastAPI backend + React frontend
├── tests/                    # pytest tests
├── docs/                     # Documentation
├── schemas/                  # JSON schemas
├── pyproject.toml            # Package configuration
└── pytest.ini                # Test configuration
```

---

## The 8 Phases

| Phase | Name | Owner | Key Deliverables |
|:-----:|------|-------|------------------|
| 1 | Vision and Strategy | Product Owner | PRD, Business Case |
| 2 | Requirements and Scope | Product Owner | Requirements, Traceability Matrix |
| 3 | Architecture and Design | CTA | System Architecture, Threat Models |
| 4 | Development Planning | Project Manager | WBS, Sprint Plan |
| 5 | Development Execution | Tech Lead | Working Software |
| 6 | Quality and Security | QA Lead | Test Results, Security Sign-off |
| 7 | Deployment and Release | DevOps | Production Deployment |
| 8 | Operations and Maintenance | SRE | Monitoring, Incidents |

---

## Quality Gates

Each phase has entry and exit criteria with go/no-go decisions.

| Phase | Exit Criteria |
|:-----:|---------------|
| 1 | Business case approved, PRD completed |
| 2 | Requirements approved, traceability matrix created |
| 3 | Architecture approved, threat models completed |
| 4 | WBS approved, sprints planned |
| 5 | Features complete, unit tests passing |
| 6 | All tests passing, security validated, UAT signed off |
| 7 | Deployed to production, smoke tests passing |
| 8 | Monitoring active, SLAs met |

---

## Quick Start

```bash
# Install
pip install octalume

# Initialize a project
octalume init my-project --compliance hipaa soc2

# Check status
octalume status

# Start a phase
octalume start 1

# Run dashboard
octalume dashboard
```

---

## MCP Integration

Add to `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "octalume": {
      "command": "python",
      "args": ["-m", "octalume.mcp.server"]
    }
  }
}
```

### Available MCP Tools (30+)

| Category | Tools |
|----------|-------|
| Phase | `lifecycle_phase_start`, `lifecycle_phase_status`, `lifecycle_phase_validate`, `lifecycle_phase_transition`, `lifecycle_phase_rollback` |
| Agent | `lifecycle_agent_spawn`, `lifecycle_agent_delegate`, `lifecycle_agent_status`, `lifecycle_agent_list`, `lifecycle_agent_terminate` |
| Artifact | `lifecycle_artifact_create`, `lifecycle_artifact_get`, `lifecycle_artifact_search`, `lifecycle_artifact_link` |
| Gate | `lifecycle_gate_check`, `lifecycle_gate_bypass`, `lifecycle_gate_list`, `lifecycle_go_no_go` |
| Compliance | `lifecycle_compliance_scan`, `lifecycle_compliance_report`, `lifecycle_compliance_configure` |
| Memory | `lifecycle_memory_save`, `lifecycle_memory_load`, `lifecycle_memory_query` |

---

## The 9 Agents

| Agent | Phase | Focus |
|-------|-------|-------|
| VisionAgent | 1 | Business case, market analysis |
| RequirementsAgent | 2 | Requirements, user stories |
| ArchitectureAgent | 3 | System design, threat modeling |
| PlanningAgent | 4 | WBS, sprint planning |
| DevelopmentAgent | 5 | Code implementation |
| QualityAgent | 6 | Testing, security validation |
| DeploymentAgent | 7 | Release management |
| OperationsAgent | 8 | Monitoring, incidents |
| OrchestratorAgent | All | Coordination |

---

## Artifact Naming

All artifacts follow: `P{N}-{SECTION}-{###}`

Examples:
- `P1-DOC-001` - Phase 1, Document, item 1
- `P3-DSN-042` - Phase 3, Design, item 42
- `P5-CODE-789` - Phase 5, Code, item 789

Sections: DOC, CODE, TEST, CFG, DSN, RPT, DEC

---

## Compliance Standards

| Standard | Description |
|----------|-------------|
| HIPAA | Healthcare data protection |
| SOC 2 | Service organization controls |
| PCI DSS | Payment card security |
| GDPR | EU data protection |
| SOX | Financial controls |

---

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/

# Run linting
ruff check octalume tests
black --check octalume tests

# Run type checking
mypy octalume
```

---

## Reference Files

| Topic | Location |
|-------|----------|
| Getting Started | docs/getting-started.md |
| CLI Reference | docs/cli-reference.md |
| MCP Tools | docs/mcp-tools.md |
| Python API | docs/python-api.md |
| Phases | docs/phases.md |
| Agents | docs/agents.md |
| Compliance | docs/compliance.md |
| Architecture | docs/architecture.md |

---

Version 2.0.0 | OCTALUME AI-Native Enterprise SDLC Framework
