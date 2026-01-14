# OCTALUME Framework - Directory Structure

**Complete directory and file listing for the OCTALUME (Enterprise Lifecycle) Framework**

---

<!-- SEO Metadata -->
**Keywords:** OCTALUME directory structure, framework files, project organization, SDLC framework structure, enterprise framework files, agent configuration, skills directory, phase skills, shared skills
**Description:** Complete directory structure and file listing for OCTALUME framework - all files, folders, agents, skills, templates, and configuration documentation
**Tags:** #OCTALUME #DirectoryStructure #FrameworkFiles #ProjectOrganization #EnterpriseFramework
**Author:** Mohamed ElHarery
**Version:** 1.0.0
**LastUpdated:** 2026

---

**Copyright (c) 2026 Mohamed ElHarery**
**Email:** mohamed@harery.com
**Website:** https://www.harery.com/
**GitHub:** https://github.com/Harery
**License:** MIT License - See LICENSE file for details

---

## ROOT DIRECTORY

```
OCTALUME/
├── SETUP_GUIDE.md                 # How to set up and use Claude Code with this framework
├── FRAMEWORK_VISUALIZATION.md     # Mermaid diagrams showing workflow and flows
├── DIRECTORY_STRUCTURE.md         # This file - complete directory listing
├── CLAUDE.md                      # Auto-loaded by Claude Code (main framework context)
├── .gitignore                     # Git ignore patterns
├── .claude/                       # Claude Code configuration and agent systems
└── skills/                        # All phase and shared skills
```

---

## .CLAUDE/ DIRECTORY

```
.claude/
├── ORCHESTRATOR.md                # Multi-agent orchestration system
├── CONTEXT_ENGINEERING.md         # Context management utilities
├── MEMORY_BANK.md                 # Memory system documentation
├── HOOKS.md                       # Hook system documentation
├── settings.json                  # Claude Code settings
│
├── agents/                        # Agent harnesses
│   ├── INITIALIZER.md             # First-run setup agent
│   ├── CODING.md                  # Incremental development agent
│   └── agent-spawner.js           # Agent spawning mechanism
│
├── validators/                    # Quality gate enforcement
│   └── phase-gate-validator.js    # Phase gate validation (entry/exit criteria)
│
├── escalation/                    # Go/no-go enforcement
│   └── escalation-manager.js      # Escalation and go/no-go decisions
│
├── bindings/                      # Task-skill binding
│   └── task-skill-binder.js       # Binds tasks to skills with execution tracking
│
├── handoff/                       # Phase handoff verification
│   └── handoff-verify.js          # Phase transition verification
│
├── memory/                        # Memory management system
│   ├── memory-lock.js             # File-based locking for concurrent access
│   ├── state-sync.js              # Bidirectional state synchronization
│   ├── memory.json                # Active memory store
│   ├── load.sh                    # Memory load script
│   ├── save.sh                    # Memory save script
│   ├── search.sh                  # Memory search script
│   ├── list.sh                    # Memory list script
│   └── delete.sh                  # Memory delete script
│
├── commands/                      # Claude Code commands
│   ├── lifecycle-init.md          # Initialize new project command
│   ├── lifecycle-phase.md         # Work on specific phase command
│   ├── lifecycle-feature.md       # Work on specific feature command
│   └── lifecycle-scan.md          # Security/compliance scan command
│
├── hooks/                         # Event hooks
│   ├── user-prompt-submit.sh      # Pre-prompt validation
│   ├── pre-tool-use.sh            # Pre-tool validation
│   └── post-tool-response.sh      # Post-tool validation
│
├── tools/                         # Tool definitions
│   └── TOOL_SEARCH.md             # Tool discovery system
│
├── templates/                     # Example templates
│   ├── example-project-state.json # Example project state
│   └── example-feature-list.json  # Example 50-feature list
│
├── mcp-server/                    # MCP server for lifecycle tools
│   ├── index.js                   # MCP server entry point
│   ├── package.json               # NPM package configuration
│   ├── package-lock.json          # NPM lock file
│   └── README.md                  # MCP server documentation
│
└── local/                         # Local settings
    └── settings.json              # Local Claude settings
```

---

## SKILLS/ DIRECTORY

```
skills/
├── phase_01_vision_strategy/
│   ├── SKILL.md                   # Phase 1 skill definition
│   ├── templates/
│   │   ├── business-case-template.md
│   │   └── prd-template.md
│   └── examples/
│       └── sample-business-case.md
│
├── phase_02_requirements_scope/
│   └── SKILL.md                   # Phase 2 skill definition
│
├── phase_03_architecture_design/
│   └── SKILL.md                   # Phase 3 skill definition
│
├── phase_04_development_planning/
│   └── SKILL.md                   # Phase 4 skill definition
│
├── phase_05_development_execution/
│   └── SKILL.md                   # Phase 5 skill definition
│
├── phase_06_quality_security/
│   └── SKILL.md                   # Phase 6 skill definition
│
├── phase_07_deployment_release/
│   └── SKILL.md                   # Phase 7 skill definition
│
├── phase_08_operations_maintenance/
│   └── SKILL.md                   # Phase 8 skill definition
│
└── shared/                        # Cross-cutting shared skills
    ├── roles/
    │   └── SKILL.md               # All 16 role definitions
    ├── security/
    │   └── SKILL.md               # Security framework
    ├── quality/
    │   └── SKILL.md               # Quality framework
    ├── compliance/
    │   └── SKILL.md               # Compliance framework
    └── governance/
        └── SKILL.md               # Decision-making framework
```

---

## FILE DESCRIPTIONS

### Root Files

| File | Description |
|------|-------------|
| `SETUP_GUIDE.md` | Complete guide to set up and use Claude Code with this framework |
| `FRAMEWORK_VISUALIZATION.md` | Mermaid diagrams showing workflow, flows, and phase transitions |
| `DIRECTORY_STRUCTURE.md` | This file - complete directory and file listing |
| `CLAUDE.md` | Auto-loaded by Claude Code - contains main framework context |
| `.gitignore` | Git ignore patterns for the project |

### .claude/ Configuration Files

| File | Description |
|------|-------------|
| `ORCHESTRATOR.md` | Multi-agent orchestration system documentation |
| `CONTEXT_ENGINEERING.md` | Context management utilities and best practices |
| `MEMORY_BANK.md` | Memory bank system documentation |
| `HOOKS.md` | Hook system for event-driven actions |
| `settings.json` | Claude Code settings (permissions, MCP, agents) |

### Agent Harnesses

| File | Description |
|------|-------------|
| `INITIALIZER.md` | First-run setup agent - creates project structure, generates features |
| `CODING.md` | Incremental development agent - works on features one at a time |
| `agent-spawner.js` | JavaScript module for spawning agents with timeout detection |

### Enforcement Systems

| File | Description |
|------|-------------|
| `phase-gate-validator.js` | Validates entry/exit criteria for phase transitions |
| `escalation-manager.js` | Manages go/no-go decisions and escalation procedures |
| `task-skill-binder.js` | Binds tasks to skills and tracks execution |
| `handoff-verify.js` | Verifies phase handoff completeness |

### Memory Management

| File | Description |
|------|-------------|
| `memory-lock.js` | File-based locking for concurrent memory access |
| `state-sync.js` | Bidirectional state synchronization between JSON files |
| `memory.json` | Active memory store for project state |
| `load.sh` | Shell script to load memory |
| `save.sh` | Shell script to save memory |
| `search.sh` | Shell script to search memory |
| `list.sh` | Shell script to list memory contents |
| `delete.sh` | Shell script to delete memory entries |

### Commands

| File | Description |
|------|-------------|
| `lifecycle-init.md` | Command to initialize a new lifecycle project |
| `lifecycle-phase.md` | Command to work on a specific phase |
| `lifecycle-feature.md` | Command to work on a specific feature |
| `lifecycle-scan.md` | Command for security/compliance scanning |

### Hooks

| File | Description |
|------|-------------|
| `user-prompt-submit.sh` | Executed before user prompt is submitted |
| `pre-tool-use.sh` | Executed before any tool is used |
| `post-tool-response.sh` | Executed after tool response is received |

### MCP Server

| File | Description |
|------|-------------|
| `index.js` | MCP server entry point |
| `package.json` | NPM package configuration |
| `package-lock.json` | NPM dependency lock file |
| `README.md` | MCP server documentation |

### Phase Skills

| Skill | Phase | Owner | Description |
|-------|-------|-------|-------------|
| `phase_01_vision_strategy/SKILL.md` | 1 | Product Owner | PRD, Business Case, Market Analysis |
| `phase_02_requirements_scope/SKILL.md` | 2 | Product Owner | Requirements, NFRs, Traceability |
| `phase_03_architecture_design/SKILL.md` | 3 | CTA | System Architecture, Security Design |
| `phase_04_development_planning/SKILL.md` | 4 | Project Manager | WBS, Resource Plan, Sprint Plan |
| `phase_05_development_execution/SKILL.md` | 5 | Tech Lead | Code, Reviews, Unit Tests |
| `phase_06_quality_security/SKILL.md` | 6 | QA Lead | QA Testing, Security, UAT |
| `phase_07_deployment_release/SKILL.md` | 7 | DevOps | Deployment, Release, Rollback |
| `phase_08_operations_maintenance/SKILL.md` | 8 | SRE | Monitoring, Incidents, Maintenance |

### Shared Skills

| Skill | Description |
|-------|-------------|
| `shared/roles/SKILL.md` | All 16 role definitions with responsibilities |
| `shared/security/SKILL.md` | Security framework and processes |
| `shared/quality/SKILL.md` | Quality standards and testing framework |
| `shared/compliance/SKILL.md` | Compliance and audit requirements |
| `shared/governance/SKILL.md` | Decision-making and RACI matrix |

---

## TRACEABILITY NAMING CONVENTION

All artifacts follow the format: `P{N}-{SECTION}-###`

- `P1-VISION-###` - Phase 1: Vision documents
- `P2-REQ-###` - Phase 2: Requirements
- `P3-ARCH-###` - Phase 3: Architecture
- `P4-PLAN-###` - Phase 4: Planning documents
- `P5-CODE-###` - Phase 5: Code commits
- `P6-TEST-###` - Phase 6: Test artifacts
- `P7-DEPLOY-###` - Phase 7: Deployment artifacts
- `P8-OPS-###` - Phase 8: Operations artifacts

---

## STATISTICS

| Category | Count |
|----------|-------|
| Root Files | 5 |
| .claude/ Documentation | 4 |
| Agent Harnesses | 3 |
| Enforcement Systems | 4 |
| Memory Scripts | 8 |
| Commands | 4 |
| Hooks | 3 |
| Phase Skills | 8 |
| Shared Skills | 5 |
| Phase 1 Templates | 2 |
| Phase 1 Examples | 1 |

**Total: ~47 operational files**

---

**For more details, see:**
- `SETUP_GUIDE.md` - How to set up and use Claude Code
- `FRAMEWORK_VISUALIZATION.md` - Visual diagrams of workflow
- `CLAUDE.md` - Auto-loaded framework context

---

**Version**: 1.0.0
**Last Updated**: 2026-01-13
