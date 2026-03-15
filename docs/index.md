# OCTALUME Documentation

**AI-Native Enterprise SDLC Framework**

---

## Overview

OCTALUME (Octa = 8 phases, Lume = light/guidance) is an AI-native software development lifecycle framework that guides projects from initial vision through production operations with:

- **8 Sequential Phases** with clear quality gates
- **30+ MCP Tools** for Claude Code integration
- **Multi-Agent Orchestration** with 9 specialized agents
- **Compliance Ready** - HIPAA, SOC 2, PCI DSS, GDPR, SOX support
- **Full Traceability** from requirements to deployment

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

## Documentation Sections

| Section | Description |
|---------|-------------|
| [Getting Started](./getting-started.md) | Installation and first project |
| [CLI Reference](./cli-reference.md) | Complete command-line interface |
| [MCP Tools](./mcp-tools.md) | 30+ Model Context Protocol tools |
| [Python API](./python-api.md) | Programmatic usage |
| [Phases](./phases.md) | The 8 SDLC phases |
| [Agents](./agents.md) | Multi-agent orchestration |
| [Compliance](./compliance.md) | Regulatory compliance support |
| [Architecture](./architecture.md) | System design |

## The 8 Phases

| Phase | Name | Owner | Focus |
|:-----:|------|-------|-------|
| 1 | Vision and Strategy | Product Owner | Business case, market opportunity |
| 2 | Requirements and Scope | Product Owner | Functional, non-functional, security requirements |
| 3 | Architecture and Design | CTA | System, security, data architecture |
| 4 | Development Planning | Project Manager | WBS, resource plan, sprint plan |
| 5 | Development Execution | Tech Lead | Agile sprints, feature implementation |
| 6 | Quality and Security | QA Lead | Testing, security validation |
| 7 | Deployment and Release | DevOps | Production deployment |
| 8 | Operations and Maintenance | SRE | Monitoring, incidents, improvements |

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Claude Code / IDE                         │
│                         (MCP)                                │
├─────────────────────────────────────────────────────────────┤
│                   MCP Server (30+ Tools)                     │
├─────────────────────────────────────────────────────────────┤
│                      Phase Engine                            │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────────────────┐  │    │
│  │  │  Gates  │  │ Agents  │  │ State Manager       │  │    │
│  │  └─────────┘  └─────────┘  └─────────────────────┘  │    │
│  └─────────────────────────────────────────────────────┘    │
├─────────────────────────────────────────────────────────────┤
│              Compliance Layer (HIPAA, SOC2, etc.)            │
├─────────────────────────────────────────────────────────────┤
│                   Memory & Trace Layer                       │
└─────────────────────────────────────────────────────────────┘
```

## License

MIT License
