---
name: "lifecycle_orchestrator"
description: "Multi-agent orchestrator for Unified Enterprise Lifecycle. Coordinates phase-specific sub-agents, manages project state across context windows, and ensures incremental progress."
type: "orchestrator"
version: "1.0.0"
---

# LIFECYCLE ORCHESTRATOR - Multi-Agent System

**Orchestrator-Worker Pattern for Enterprise Development**

This orchestrator manages the complete Unified Enterprise Lifecycle by coordinating specialized sub-agents across 8 phases, following Anthropic's multi-agent architecture principles.

---

## ARCHITECTURE OVERVIEW

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    MULTI-AGENT ORCHESTRATION SYSTEM                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────┐                                                        │
│  │ ORCHESTRATOR    │  ← Lead Agent (Coordination)                          │
│  │ (This Agent)    │    - Analyzes project state                           │
│  └────────┬────────┘    - Spawns phase-specific sub-agents                  │
│           │              - Synthesizes results                               │
│           │              - Manages progress tracking                         │
│           │                                                               │
│           ├─────────────────────────────────────────────────────────────┐   │
│           │                                                             │   │
│           │  PHASE SUB-AGENTS (Spawn in Parallel as Needed)              │   │
│           │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │   │
│           │  │ Phase 1      │  │ Phase 2      │  │ Phase 3      │       │   │
│           │  │ Vision Agent │  │ Requirements │  │ Architecture  │       │   │
│           │  └──────────────┘  └──────────────┘  └──────────────┘       │   │
│           │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │   │
│           │  │ Phase 4      │  │ Phase 5      │  │ Phase 6      │       │   │
│           │  │ Planning     │  │ Development  │  │ Validation   │       │   │
│           │  └──────────────┘  └──────────────┘  └──────────────┘       │   │
│           │  ┌──────────────┐  ┌──────────────┐                     │   │
│           │  │ Phase 7      │  │ Phase 8      │                     │   │
│           │  │ Deployment   │  │ Operations   │                     │   │
│           │  └──────────────┘  └──────────────┘                     │   │
│           │                                                             │   │
│           └─────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  SHARED SERVICES (Cross-Cutting)                                           │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐          │
│  │ Security   │  │ Quality    │  │ Compliance │  │ Governance │          │
│  │ Agent      │  │ Agent      │  │ Agent      │  │ Agent      │          │
│  └────────────┘  └────────────┘  └────────────┘  └────────────┘          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## ORCHESTRATOR RESPONSIBILITIES

### 1. Project State Management

The orchestrator maintains project state across context windows:

```json
// .claude/project-state.json
{
  "project_name": "string",
  "current_phase": "phase_01_vision_strategy",
  "phase_status": "in_progress",
  "completed_phases": [],
  "blocked_phases": [],
  "artifacts": {
    "P1-VISION-001": "PRD document",
    "P1-BUSINESS-001": "Business case"
  },
  "traceability": {
    "last_commit": "abc123",
    "last_build": "build-456"
  }
}
```

### 2. Phase Coordination

**When to spawn sub-agents**:
- **Sequential phases**: Spawn next phase agent after current phase completes
- **Parallel phases**: Multiple sub-agents can work on independent tracks (e.g., security + quality testing in Phase 6)
- **Exception handling**: Spawn escalation agent when blockers occur

**Sub-agent communication pattern**:
```
Orchestrator → [Spawn Phase Agent] → Phase Agent returns results → Orchestrator synthesizes → Update project state → Proceed
```

### 3. Progress Tracking

- Read `claude-progress.txt` at start of each session
- Update progress incrementally
- Commit progress to git with descriptive messages
- Never mark features as complete without testing

---

## ORCHESTRATOR WORKFLOW

### Session Start (Every New Context Window)

```bash
# 1. Get bearings
pwd

# 2. Read project state
read .claude/project-state.json
read claude-progress.txt

# 3. Read git history for recent work
git log --oneline -20

# 4. Verify environment is working
source init.sh  # if exists

# 5. Determine next action
# - If project-state.json doesn't exist: run initializer agent
# - If phase in progress: continue that phase
# - If phase complete: spawn next phase agent
# - If blocked: diagnose and resolve
```

### Decision Tree

```
┌─────────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR DECISION TREE                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  START SESSION                                              │
│       │                                                     │
│       ▼                                                     │
│  Does .claude/project-state.json exist?                     │
│       │                                                     │
│       ├── NO ──► RUN INITIALIZER AGENT                      │
│       │         - Set up project structure                  │
│       │         - Create feature_list.json                  │
│       │         - Initialize git repo                       │
│       │         - Create init.sh                            │
│       │                                                     │
│       └── YES ──► READ PROJECT STATE                        │
│                 │                                           │
│                 ▼                                           │
│          What is current_phase status?                      │
│                 │                                           │
│                 ├── "not_started" ──► SPAWN PHASE AGENT     │
│                 ├── "in_progress"  ──► CONTINUE PHASE       │
│                 ├── "blocked"       ──► DIAGNOSE BLOCKER    │
│                 ├── "complete"      ──► GOTO NEXT PHASE     │
│                 └── "failed"        ──► ASSESS & RETRY      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## SPAWNING SUB-AGENTS

### Phase Agents

Each phase has a dedicated sub-agent with its own prompt and tools:

```bash
# Spawn phase agent syntax
spawn_agent --phase=phase_01_vision_strategy --context="project requirements gathering"

# The orchestrator provides:
# 1. Phase-specific prompt from skills/phase_XX/SKILL.md
# 2. Relevant project state
# 3. Entry criteria validation
# 4. Expected outputs
```

### Parallel Agent Execution

**When multiple agents can run in parallel**:

```
Phase 6: Quality & Security Validation
├── Quality Agent (functional testing)
├── Security Agent (penetration testing)
├── Performance Agent (load testing)
└── Compliance Agent (audit validation)

All four agents run in parallel, then orchestrator synthesizes results.
```

---

## ORCHESTRATOR PROMPTING PRINCIPLES

Based on Anthropic's multi-agent research:

### 1. Think Like Your Agents

Understand what each sub-agent needs:
- Clear objective
- Output format
- Tools and sources to use
- Task boundaries

### 2. Scale Effort to Query Complexity

```
Simple fact-finding     → 1 agent, 3-10 tool calls
Direct comparisons      → 2-4 agents, 10-15 calls each
Complex research        → 10+ agents with divided responsibilities
```

### 3. Guide the Thinking Process

Use extended thinking mode for:
- Planning phase transitions
- Assessing blockers
- Synthesizing multi-agent results
- Making go/no-go decisions

### 4. Parallel Tool Calling

Always spawn multiple agents in parallel when possible:
```
# Instead of:
spawn_agent phase_1
wait
spawn_agent phase_2
wait

# Do:
spawn_agent phase_1, phase_2, phase_3  # Parallel
wait for all
synthesize results
```

---

## SUB-AGENT OUTPUT HANDLING

### Acceptable Output Formats

```json
// Standard sub-agent result
{
  "agent": "phase_01_vision_strategy",
  "status": "complete",
  "outputs": {
    "artifacts": ["P1-VISION-001", "P1-BUSINESS-001"],
    "deliverables": ["PRD.md", "business_case.md"],
    "next_phase": "phase_02_requirements_scope",
    "blockers": [],
    "recommendations": []
  },
  "traceability": {
    "commit": "abc123",
    "timestamp": "2025-01-11T00:00:00Z"
  }
}
```

### Output Directly to Filesystem

To avoid "game of telephone" (information loss through coordinator):

```
Sub-agent ──► Create artifact file ──► Pass reference to orchestrator
```

Example:
```bash
# Phase 3 agent creates architecture document
# Instead of returning full content to orchestrator:
echo '{"artifact": "P3-ARCH-001", "path": "docs/architecture/system.md"}' > /tmp/agent_result.json

# Orchestrator reads only the reference
```

---

## ERROR HANDLING AND RECOVERY

### Sub-Agent Failure Modes

| Failure | Symptom | Orchestrator Response |
|---------|---------|----------------------|
| **Timeout** | Agent doesn't respond | Spawn retry agent with time budget |
| **Context Overflow** | Agent hits token limit | Compact and retry with summary |
| **Tool Failure** | Required tool unavailable | Diagnose and provide alternative |
| **Blocker** | Agent can't proceed | Spawn escalation agent |
| **Contradiction** | Agents disagree | Synthesize and resolve |

### Recovery Strategies

```python
# Pseudo-code for orchestrator recovery
def handle_subagent_failure(agent, error):
    if error.type == "timeout":
        # Compact context and retry
        compact_agent_context(agent)
        return spawn_agent(agent.phase, retry=True)
    elif error.type == "blocker":
        # Spawn escalation agent
        return spawn_agent("escalation", context=error.context)
    elif error.type == "contradiction":
        # Synthesis agent to resolve
        return spawn_agent("synthesis", inputs=agent.outputs)
```

---

## QUALITY GATES (Orchestrator Level)

The orchestrator enforces quality gates between phases:

```python
def can_transition_to_next_phase(current_phase, next_phase):
    # Check exit criteria
    if not current_phase.exit_criteria_met():
        return False, "Exit criteria not met"

    # Check entry criteria for next phase
    if not next_phase.entry_criteria_met():
        return False, "Entry criteria not met"

    # Check artifacts
    required_artifacts = get_required_artifacts(current_phase)
    if not all_artifacts_exist(required_artifacts):
        return False, "Missing artifacts"

    # Check approvals
    required_approvals = get_required_approvals(current_phase)
    if not all_approvals_obtained(required_approvals):
        return False, "Missing approvals"

    return True, "Ready to proceed"
```

---

## MEMORY AND STATE MANAGEMENT

### Progressive Disclosure

The orchestrator uses progressive disclosure for context:

```
Level 1: Phase metadata (name, description, entry/exit criteria)
Level 2: Phase SKILL.md body
Level 3: Referenced files and artifacts
```

### Compaction Strategy

When approaching context limit:

```bash
# Summarize completed work
cat > claude-progress-summary.md <<EOF
# Session Summary - $(date)

## Completed
- Phase X deliverables completed
- Artifacts: P{X}-*

## In Progress
- Phase Y currently working on Z

## Next Steps
1. Continue Phase Y
2. Complete deliverable D
3. Move to Phase Z
EOF

# Clear tool results from history (safest compaction)
clear_tool_results --older-than 50

# Keep recent 5 files accessible
keep_recent_files 5
```

---

## ORCHESTRATOR TOOLS

### Built-in Orchestrator Tools

```yaml
tools:
  - name: spawn_agent
    description: "Spawn a phase-specific sub-agent"
    input_schema:
      type: object
      properties:
        phase:
          type: string
          enum: ["phase_01", "phase_02", "phase_03", "phase_04", "phase_05", "phase_06", "phase_07", "phase_08"]
        context:
          type: string
        parallel:
          type: boolean
          default: false

  - name: read_project_state
    description: "Read the current project state"

  - name: update_project_state
    description: "Update project state after agent completes"

  - name: validate_quality_gate
    description: "Check if phase can transition to next"

  - name: synthesize_results
    description: "Synthesize outputs from multiple parallel agents"

  - name: diagnose_blocker
    description: "Analyze and resolve project blockers"
```

---

## BEST PRACTICES

### For Orchestrator Prompting

1. **Be Specific About Objectives**
   - "Spawn phase_01 agent to create PRD for e-commerce platform"
   - NOT: "Work on phase 1"

2. **Provide Clear Output Format**
   - "Return JSON with artifacts, blockers, next_phase"
   - NOT: "Tell me what you did"

3. **Set Task Boundaries**
   - "Focus only on requirements gathering. Do NOT start design."
   - NOT: "Work on the project"

4. **Give Effort Budgets**
   - "Use 3-5 searches, max 10 tool calls"
   - NOT: "Research this"

### For Sub-Agent Coordination

1. **Start Wide, Then Narrow**
   - Spawn multiple agents in parallel
   - Synthesize their results
   - Then drill into specifics

2. **Let Agents Improve Themselves**
   - Ask agents to diagnose their own failures
   - Use agent feedback to improve prompts

3. **Use Extended Thinking**
   - For complex orchestration decisions
   - When synthesizing multi-agent results
   - When making go/no-go decisions

---

## EVALUATION AND TESTING

### Orchestrator Success Metrics

| Metric | Target | Purpose |
|--------|--------|---------|
| Phase Transition Accuracy | 100% | Correct phase sequencing |
| Sub-Agent Success Rate | >95% | Reliable agent spawning |
| Artifact Traceability | 100% | All artifacts tracked |
| Blocker Resolution | <24h | Quick unblocking |
| Context Efficiency | <100K tokens/session | Efficient context use |

### Testing the Orchestrator

```bash
# Test orchestrator decision making
test_orchestrator --scenario=new_project
test_orchestrator --scenario=mid_phase
test_orchestrator --scenario=blocked_project
test_orchestrator --scenario=phase_transition

# Test sub-agent spawning
test_spawn_agent --phase=phase_01 --expect_success
test_spawn_agent --phase=phase_02 --parallel_with=phase_03
```

---

## SEE ALSO

- **Initializer Agent**: `../skills/agents/INITIALIZER.md` - Project setup agent
- **Phase Agents**: `../skills/phase_*/SKILL.md` - Individual phase agents
- **Shared Services**: `../skills/shared/` - Cross-cutting agents
- **Tools**: `../.claude/tools/` - Orchestrator tool definitions

---

**This orchestrator implements Anthropic's multi-agent research principles for enterprise development.**

---

**Review Completed By:** OCTALUME TEAM
**Date:** 2026-01-13
**Next Review Recommended:** After major framework updates or every 6 months
