# Stage 8 — Logic + Workflow Definitions
Layer: Nano→Atomic | Output: docs/logic.md
⚠ Questions stop after this stage. Stages 9–12 are build-only.

## Adaptive questions (2–3 max — final clarifications before implementation)

> 1. Are there any user roles with different permissions that haven't been fully defined? (e.g. admin vs standard user vs guest)
> 2. What happens when the core loop fails — what is the error state and recovery path?
> 3. Are there any time-based triggers or scheduled tasks in the MVP? (e.g. reminders, billing cycles, expiry)

These are the last questions in the pipeline. After this stage, no new questions.

## Scope constraint

Define logic only for MVP features from docs/MVP.md.
Do NOT define logic for deferred features — this inflates token cost with no build value.
If a feature is on the deferred list, note "deferred — see docs/MVP.md" and stop.

## Output — docs/logic.md

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
LOGIC + WORKFLOW DEFINITIONS
docs/logic.md
[Scope: MVP features only — see docs/MVP.md]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## User roles and permissions
  [Role | What they can do | What they cannot do]

## Core user flows (one per MVP feature)

### [Feature name]
  Entry point: [where the flow starts]
  Happy path:
    1. [step]
    2. [step]
    3. [step — terminal state / success condition]
  Error states:
    - [condition] → [what happens] → [recovery path]
  Business rules:
    - [rule 1 — testable]
    - [rule 2 — testable]

## Data entities (MVP only)
  [Entity | Fields | Relationships | Constraints]

## API surface (MVP only)
  [Endpoint | Method | Auth required | Input | Output | Error codes]

## Scheduled tasks (if any)
  [Task | Trigger | What it does | Failure behaviour]

## State machine (if applicable)
  [Entity | States | Transitions | Guards]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Gate → `stages/s09-diagrams.md`
