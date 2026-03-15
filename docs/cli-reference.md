# CLI Reference

Complete reference for the OCTALUME command-line interface.

## Installation

```bash
pip install octalume
```

## Global Options

| Option | Description |
|--------|-------------|
| `--version` | Show version and exit |
| `--help` | Show help message |
| `--state-dir PATH` | Override state directory |
| `--verbose` | Enable verbose output |
| `--json` | Output as JSON |

## Commands

### `octalume init`

Initialize a new OCTALUME project.

```bash
octalume init <name> [OPTIONS]
```

**Arguments:**
- `name` - Project name (required)

**Options:**
| Option | Description |
|--------|-------------|
| `--description TEXT` | Project description |
| `--compliance STANDARDS` | Compliance standards (hipaa, soc2, pci, gdpr, sox) |
| `--template NAME` | Use a project template |

**Example:**
```bash
octalume init healthcare-app \
  --description "Healthcare patient portal" \
  --compliance hipaa soc2
```

---

### `octalume status`

Show current project status.

```bash
octalume status [OPTIONS]
```

**Options:**
| Option | Description |
|--------|-------------|
| `--phase NUMBER` | Show specific phase details |
| `--artifacts` | Include artifact list |
| `--agents` | Include agent list |

**Example:**
```bash
octalume status --artifacts --agents
```

---

### `octalume start`

Start a specific phase.

```bash
octalume start <phase_number>
```

**Arguments:**
- `phase_number` - Phase to start (1-8)

**Example:**
```bash
octalume start 1
```

---

### `octalume complete`

Complete a phase and run quality gate.

```bash
octalume complete <phase_number> [OPTIONS]
```

**Arguments:**
- `phase_number` - Phase to complete (1-8)

**Options:**
| Option | Description |
|--------|-------------|
| `--force` | Skip quality gate validation |
| `--notes TEXT` | Completion notes |

**Example:**
```bash
octalume complete 1 --notes "PRD approved by stakeholders"
```

---

### `octalume gate`

Check quality gate for a phase.

```bash
octalume gate <phase_number> [OPTIONS]
```

**Arguments:**
- `phase_number` - Phase to validate (1-8)

**Options:**
| Option | Description |
|--------|-------------|
| `--type TYPE` | Gate type: entry or exit (default: exit) |
| `--fix` | Suggest fixes for failures |

**Example:**
```bash
octalume gate 1 --fix
```

---

### `octalume rollback`

Rollback to a previous phase.

```bash
octalume rollback <to_phase> --reason TEXT
```

**Arguments:**
- `to_phase` - Target phase (1-7)

**Options:**
| Option | Description |
|--------|-------------|
| `--reason TEXT` | Reason for rollback (required) |

**Example:**
```bash
octalume rollback 3 --reason "Architecture review failed security audit"
```

---

### `octalume artifact`

Manage project artifacts.

#### `artifact create`

Create a new artifact.

```bash
octalume artifact create [OPTIONS]
```

**Options:**
| Option | Description |
|--------|-------------|
| `--phase NUMBER` | Phase number (required) |
| `--type TYPE` | Artifact type: document, code, test, config, design, report, decision |
| `--name TEXT` | Artifact name (required) |
| `--file PATH` | File path |
| `--content TEXT` | Inline content |
| `--tags TAGS` | Compliance tags |

**Example:**
```bash
octalume artifact create \
  --phase 3 \
  --type design \
  --name "System Architecture" \
  --file docs/architecture.md \
  --tags hipaa soc2
```

#### `artifact get`

Get artifact details.

```bash
octalume artifact get <artifact_id>
```

#### `artifact search`

Search artifacts.

```bash
octalume artifact search [OPTIONS]
```

**Options:**
| Option | Description |
|--------|-------------|
| `--phase NUMBER` | Filter by phase |
| `--type TYPE` | Filter by type |
| `--term TEXT` | Search term |
| `--limit NUMBER` | Max results (default: 50) |

---

### `octalume agents`

Manage AI agents.

#### `agents list`

List all agents.

```bash
octalume agents list [OPTIONS]
```

**Options:**
| Option | Description |
|--------|-------------|
| `--phase NUMBER` | Filter by phase |
| `--status STATUS` | Filter by status: idle, running, completed, failed |

#### `agents spawn`

Spawn a new agent.

```bash
octalume agents spawn <agent_type> --task TEXT
```

**Agent Types:** vision, requirements, architecture, planning, development, quality, deployment, operations, orchestrator

**Example:**
```bash
octalume agents spawn architecture --task "Design microservices architecture"
```

#### `agents status`

Get agent status.

```bash
octalume agents status <agent_id>
```

#### `agents terminate`

Terminate an agent.

```bash
octalume agents terminate <agent_id> --reason TEXT
```

---

### `octalume scan`

Run compliance scan.

```bash
octalume scan [OPTIONS]
```

**Options:**
| Option | Description |
|--------|-------------|
| `--standard STANDARDS` | Standards to scan (hipaa, soc2, pci, gdpr, sox) |
| `--scope SCOPE` | Scope: all, artifacts, processes, documentation |
| `--report FORMAT` | Output format: json, markdown, html |

**Example:**
```bash
octalume scan --standard hipaa soc2 --report markdown
```

---

### `octalume memory`

Manage project memory.

#### `memory stats`

Show memory statistics.

```bash
octalume memory stats
```

#### `memory save`

Save a memory entry.

```bash
octalume memory save --category CAT --key KEY --value VALUE
```

#### `memory load`

Load a memory entry.

```bash
octalume memory load --category CAT --key KEY
```

#### `memory query`

Query memory entries.

```bash
octalume memory query --category CAT --term SEARCH
```

---

### `octalume dashboard`

Start the web dashboard.

```bash
octalume dashboard [OPTIONS]
```

**Options:**
| Option | Description |
|--------|-------------|
| `--port PORT` | Port number (default: 8000) |
| `--host HOST` | Host (default: localhost) |
| `--no-browser` | Don't open browser |

---

### `octalume trace`

View execution traces.

```bash
octalume trace [OPTIONS]
```

**Options:**
| Option | Description |
|--------|-------------|
| `--phase NUMBER` | Filter by phase |
| `--limit NUMBER` | Max results (default: 100) |

---

### `octalume health`

Check system health.

```bash
octalume health
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Invalid arguments |
| 3 | Quality gate failed |
| 4 | Phase not ready |
| 5 | Configuration error |

## Environment Variables

| Variable | Description |
|----------|-------------|
| `OCTALUME_STATE_DIR` | Override state directory |
| `OCTALUME_LOG_LEVEL` | Log level (DEBUG, INFO, WARNING, ERROR) |
| `OCTALUME_NO_COLOR` | Disable colored output |
