# Getting Started

This guide will help you get up and running with OCTALUME in minutes.

## Prerequisites

- Python 3.11 or higher
- pip or uv package manager
- Git (optional, for version control)

## Installation

### Using pip

```bash
pip install octalume
```

### Using uv (recommended)

```bash
uv pip install octalume
```

### From Source

```bash
git clone https://github.com/Harery/OCTALUME.git
cd OCTALUME
pip install -e ".[dev]"
```

## Your First Project

### 1. Initialize

Create a new OCTALUME project:

```bash
octalume init my-saas-app \
  --description "A SaaS application for task management" \
  --compliance soc2 gdpr
```

This creates:
- `.octalume/` directory with project state
- Initial configuration files
- Compliance configuration for SOC 2 and GDPR

### 2. Check Status

View your project status:

```bash
octalume status
```

Output:
```
Project: my-saas-app
Current Phase: 1 (Vision and Strategy)
Status: Not Started
Compliance: SOC2, GDPR

Phases:
  1. Vision and Strategy    [Not Started]
  2. Requirements and Scope [Not Started]
  3. Architecture and Design[Not Started]
  4. Development Planning   [Not Started]
  5. Development Execution  [Not Started]
  6. Quality and Security   [Not Started]
  7. Deployment and Release [Not Started]
  8. Operations and Maint.  [Not Started]

Artifacts: 0
Agents: 0
```

### 3. Start Phase 1

Begin the Vision and Strategy phase:

```bash
octalume start 1
```

### 4. Create Artifacts

Create your first artifact (e.g., Product Requirements Document):

```bash
octalume artifact create \
  --phase 1 \
  --type document \
  --name "Product Requirements Document" \
  --file docs/prd.md
```

### 5. Check Quality Gate

Validate phase completion:

```bash
octalume gate 1
```

### 6. Complete and Transition

Complete the phase and move to the next:

```bash
octalume complete 1
```

## MCP Integration with Claude Code

### Configure Claude Code

Add to your `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "octalume": {
      "command": "python",
      "args": ["-m", "octalume.mcp.server"],
      "env": {
        "OCTALUME_STATE_DIR": "/path/to/your/project/.octalume"
      }
    }
  }
}
```

### Available in Claude

Once configured, Claude Code can use all 30+ lifecycle tools:

```
You: Initialize a new project for my fintech startup

Claude: [Uses lifecycle_project_init tool]
        Created project "fintech-app" with SOC2 and PCI compliance.

You: Start phase 1 and create a business case document

Claude: [Uses lifecycle_phase_start]
        [Uses lifecycle_artifact_create]
        Started Vision phase. Created P1-DOC-001 Business Case.
```

## Web Dashboard

Start the web dashboard:

```bash
octalume dashboard
```

Opens at `http://localhost:8000` with:
- Project overview
- Phase progress visualization
- Artifact browser
- Agent status
- Compliance reports

## Python API

Use OCTALUME programmatically:

```python
import asyncio
from octalume import PhaseEngine, GateValidator, AgentOrchestrator
from octalume.core.state import ProjectStateManager

async def main():
    # Initialize
    manager = ProjectStateManager()
    state = await manager.create(
        name="my-project",
        description="Building with Python API",
        compliance_standards=["hipaa"]
    )

    # Start phase 1
    engine = PhaseEngine(manager)
    state = await engine.start_phase(state, 1)

    # Create an artifact
    from octalume.core.models import Artifact, ArtifactType
    artifact = Artifact(
        id="P1-DOC-001",
        phase=1,
        name="Business Case",
        artifact_type=ArtifactType.DOCUMENT,
        content="..."
    )
    state.artifacts[artifact.id] = artifact
    await manager.save(state)

    # Complete phase with quality gate
    state, gate_result = await engine.complete_phase(state, 1)
    if gate_result.passed:
        print("Phase 1 complete!")

asyncio.run(main())
```

## Next Steps

- [CLI Reference](./cli-reference.md) - All commands explained
- [MCP Tools](./mcp-tools.md) - Claude Code integration
- [Phases](./phases.md) - Deep dive into each phase
- [Compliance](./compliance.md) - Regulatory requirements
