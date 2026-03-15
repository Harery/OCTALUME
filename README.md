# OCTALUME

**AI-Native Enterprise SDLC Framework**

8 Phases | Quality Gates | Multi-Agent Orchestration | Compliance Ready

---

## What is OCTALUME?

**Octa** = 8 phases | **Lume** = light/guidance

OCTALUME is an AI-native software development lifecycle framework that guides projects from initial vision through production operations with built-in quality gates, multi-agent orchestration, and compliance support.

## Features

- **8 Sequential Phases** - Clear progression from idea to production
- **30+ MCP Tools** - Full Claude Code integration via Model Context Protocol
- **Quality Gates** - Go/no-go decisions prevent problems from advancing
- **Multi-Agent Orchestration** - 9 specialized AI agents for each phase
- **Compliance Ready** - HIPAA, SOC 2, PCI DSS, GDPR, SOX support
- **Full Traceability** - Every decision and artifact tracked
- **Web Dashboard** - React-based dashboard for monitoring
- **CLI** - Complete command-line interface

## Quick Start

### Installation

```bash
pip install octalume
```

### Initialize a Project

```bash
octalume init my-project --description "My SaaS App" --compliance hipaa soc2
```

### Check Status

```bash
octalume status
```

### Start a Phase

```bash
octalume start 1
```

### Run Dashboard

```bash
octalume dashboard
```

## The 8 Phases

| Phase | Name | Owner | Duration |
|:-----:|------|-------|:--------:|
| 1 | Vision and Strategy | Product Owner | 1 week |
| 2 | Requirements and Scope | Product Owner | 2 weeks |
| 3 | Architecture and Design | CTA | 1 week |
| 4 | Development Planning | Project Manager | 1 week |
| 5 | Development Execution | Tech Lead | Variable |
| 6 | Quality and Security | QA Lead | 2 weeks |
| 7 | Deployment and Release | DevOps | 1 week |
| 8 | Operations and Maintenance | SRE | Ongoing |

## MCP Integration

OCTALUME provides 30+ MCP tools for Claude Code integration:

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

### Available Tools

| Category | Tools |
|----------|-------|
| Phase | `lifecycle_phase_start`, `lifecycle_phase_status`, `lifecycle_phase_validate`, `lifecycle_phase_transition`, `lifecycle_phase_rollback` |
| Agent | `lifecycle_agent_spawn`, `lifecycle_agent_delegate`, `lifecycle_agent_status`, `lifecycle_agent_list`, `lifecycle_agent_terminate` |
| Artifact | `lifecycle_artifact_create`, `lifecycle_artifact_get`, `lifecycle_artifact_search`, `lifecycle_artifact_link` |
| Gate | `lifecycle_gate_check`, `lifecycle_gate_bypass`, `lifecycle_gate_list`, `lifecycle_go_no_go` |
| Compliance | `lifecycle_compliance_scan`, `lifecycle_compliance_report`, `lifecycle_compliance_configure` |
| Memory | `lifecycle_memory_save`, `lifecycle_memory_load`, `lifecycle_memory_query` |
| Observability | `lifecycle_trace_add`, `lifecycle_trace_get`, `lifecycle_health_check` |

## CLI Reference

```bash
octalume init <name>           # Initialize project
octalume status                # Show project status
octalume start <phase>         # Start a phase
octalume complete <phase>      # Complete a phase
octalume gate <phase>          # Check quality gate
octalume agents                # List agents
octalume scan [--standard]     # Run compliance scan
octalume dashboard             # Start web dashboard
octalume memory                # View memory stats
```

## Python API

```python
from octalume import PhaseEngine, GateValidator, AgentOrchestrator, ProjectState
from octalume.core.state import ProjectStateManager

async def main():
    manager = ProjectStateManager()
    state = await manager.create(
        name="my-project",
        compliance_standards=["hipaa", "soc2"]
    )

    engine = PhaseEngine(manager)
    await engine.start_phase(state, 1)
    state, gate_result = await engine.complete_phase(state, 1)
```

## Compliance Standards

| Standard | Description |
|----------|-------------|
| HIPAA | Healthcare data protection |
| SOC 2 | Service organization controls |
| PCI DSS | Payment card security |
| GDPR | EU data protection |
| SOX | Financial controls |
| DoD/ITAR | Defense requirements |

## Architecture

```
octalume/
├── core/           # Phase engine, gates, orchestrator, state
├── mcp/            # MCP server with 30+ tools
├── agents/         # Phase-specific AI agents
├── compliance/     # Compliance scanners (HIPAA, SOC2, PCI, GDPR)
├── a2a/            # Agent-to-Agent protocol
└── utils/          # Logging, configuration
```

## License

MIT License

## Links

- Documentation: https://docs.octalume.dev
- Repository: https://github.com/Harery/OCTALUME
- Discord: https://discord.gg/octalume
