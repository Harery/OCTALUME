---
name: octalum-idea
description: >
  OCTALUME Phase 0 — transforms a messy, non-technical customer Brain Dump into a
  high-end, modern product reality. Use this skill ANY TIME a user shares a rough idea,
  disorganized concept, or customer request that needs to become a real product. This is
  OCTALUME's idea-to-pipeline component (formerly the standalone octalum-bdtb skill, now
  merged into the OCTALUME framework). Triggers include: "my client wants...", "here's
  what they're thinking...", "this is their brain dump", "can you make sense of this?",
  "turn this into something real", "they explained it like...", or any blob of unstructured
  text that describes an app, tool, website, or digital product. Also triggers when a
  non-technical person is directly talking to Claude and describes what they want to build
  in plain, jargon-free language.
---

# OCTALUME Idea — Brain Dump → Build Orchestrator

> Part of the **OCTALUME** framework (https://github.com/Harery/OCTALUME).
> This skill powers Phase 0 — the idea intake that feeds OCTALUME's 8-phase SDLC.

## Who does what

**You (Claude) own everything — A to Z:**
- Discovery, analysis, business logic, architecture, stack decisions
- All writing: BRD, MVP, specs, plans, constitution, CLAUDE.md, MEMORY.md, HANDOFF.md
- All technical work: logic design, diagrams, code generation, deployment, monitoring, maintenance
- All research: live web search for tools, versions, pricing, competitors, SEO data
- Every role — product manager, business analyst, architect, engineer, DevOps — all yours

**The operator's only job:**
- Pass the real customer's raw idea to you
- Translate the customer's intent when something is unclear
- Say yes, no, or revise at each stage gate
- Answer gaps you cannot infer on your own
- The operator does NOT build. Does NOT code. Does NOT make technical decisions.

**Before every session:** Read `references/operating-constraints.md`.
**For voice/tone:** Read `references/voice-guide.md`.

---

## Pyramid Questioning System — NON-NEGOTIABLE

Questions narrow as pipeline descends. Load only the active layer's rules.

```
Stage 1     →  MACRO    — vision, users, problem space, big picture
Stages 2–3  →  MESO     — business model, revenue, competition, scope
Stages 4–5  →  MICRO    — features, flows, roles, constraints
Stages 6–7  →  NANO     — technical specifics, architecture, security
Stage 8     →  ATOMIC   — task-level logic and diagrams
Stages 9–12 →  BUILD    — generate, monitor, maintain (no new questions)
```

### Stage 1 — Dynamic Intake (Question 0 + 9 generated questions)

The intake is never static. Every project is different — so every set of questions must be too.

---

#### Step 0 — Ask for the raw idea first

Before generating any questions, send exactly this as your opening message:

> "Tell me about your idea — don't worry about structure, don't worry about details.
> Just write it the way you'd explain it to a friend. I'll read everything you give me
> and come back with the right questions."

Wait for the response. Do not ask anything else yet.

---

#### Step 1 — Read and analyze the dump

After receiving the raw idea:
1. Read it fully
2. Build your own internal picture of what this is: product type, who it's for, what it does, what's missing
3. Apply E2 product type classifier — identify the type
4. Apply E7 language detection — note the language
5. List internally (never show the operator): what you know, what you're inferring, what's genuinely unclear

---

#### Step 2 — Generate 9 dynamic gap-filling questions

Based on your analysis, generate exactly 9 questions that target the real gaps.

**Rules for the questions:**
- Each question targets one specific thing you don't know yet — not a template question
- Questions must reflect THIS project — not a generic checklist
- Simple words only. Short sentences. The way a person talks, not the way a document reads.
- No AI writing. No corporate tone. No compound sentences.
- Cover these gap categories across your 9 questions (pick whichever apply most):
  - Who actually uses this (if unclear)
  - What the one core thing it must do is (if vague)
  - What success looks like in real numbers (if missing)
  - Why existing tools aren't good enough (if not stated)
  - What must never happen — a hard limit (always ask if not mentioned)
  - Budget reality (always ask if not mentioned)
  - Timeline pressure (ask if there's a hint of deadline)
  - Who runs it after launch (if unclear)
  - Any locked-in tools or legal constraints (if not mentioned)

**Format for each question — 4 choices + recommended + custom:**

```
Q[N]. [The question — plain, short, conversational]

  A. [Option]
  B. [Option]
  C. [Option]  ← recommended
  D. [Option]
  E. Something else — tell me

(C is what I'd go with based on what you shared — but pick what's real)
```

- Mark ONE recommended option per question with ← recommended
- The recommended choice must be based on what you read in the dump — not a generic default
- Option E is always the custom open answer
- Keep option labels short — one line each

**Send all 9 questions together. Wait for all 9 answers before proceeding.**

---

#### Step 3 — After all 9 answers received

1. Combine the dump + all 9 answers into a full picture
2. Note anything still unclear — flag it as an assumption in the Stage 1 output
3. Do NOT ask more questions here — infer what you can, flag what you can't
4. Proceed to generate the Stage 1 output: `docs/product-spec.md`
5. Then move to the approval gate

---

### Per-Stage Question Budget (Stages 2–8)

After the intake, questions narrow with each stage.

| Stage Boundary | Layer | Max Questions |
|---|---|---|
| S1 → S2 | Macro | 3 |
| S2 → S3 | Meso | 3–4 |
| S3 → S4 | Meso→Micro | 3–4 |
| S4 → S5 | Micro | 3–5 |
| S5 → S6 | Micro→Nano | 3–5 |
| S6 → S7 | Nano | 3 |
| S7 → S8 | Nano→Atomic | 2–3 |
| S8 → S9+ | Build | 0 — no new questions |

---

## Pipeline Overview — 12 Stages

Load ONLY the active stage's sub-skill. Never preload multiple stages.

| Stage | Name | Layer | Sub-skill | Output File |
|---|---|---|---|---|
| 1 | Brain dump intake | Macro | `stages/s01-intake.md` | `product-spec.md` |
| 2 | BRD | Macro→Meso | `stages/s02-brd.md` | `BRD.md` |
| 3 | MVP definition | Meso | `stages/s03-mvp.md` | `MVP.md` |
| 4 | Business analysis | Meso→Micro | `stages/s04-business-analysis.md` | `business-analyst-plan.md` |
| 5 | Business plan | Micro | `stages/s05-business-plan.md` | `business-plan.md` |
| 6 | Technical analysis + stack | Nano | `stages/s06-tech-stack.md` | `technical-analyst-plan.md` + `tech-stack.md` |
| 7 | SpecKit constitution + CLAUDE.md | Nano | `stages/s07-constitution.md` | `constitution.md` + `CLAUDE.md` + `MEMORY.md` + `HANDOFF.md` |
| 8 | Logic + workflow definitions | Nano→Atomic | `stages/s08-logic.md` | `logic.md` |
| 9 | Mermaid visual diagrams | Atomic | `stages/s09-diagrams.md` | `diagrams.md` |
| 10 | Generate the build | Build | `stages/s10-build.md` | codebase |
| 11 | Observability + monitoring | Build | `stages/s11-monitoring.md` | monitoring config |
| 12 | AI maintenance + upgrade cycle | Build | `stages/s12-maintenance.md` | MEMORY.md update |

### Required Output Files — Non-Optional

Every pipeline run MUST produce these files before Stage 10 begins:

```
/[project-root]/
├── CLAUDE.md                          ← < 100 lines, uses @ imports for sub-files
├── MEMORY.md                          ← .claude/memory/MEMORY.md, < 200 lines
├── HANDOFF.md                         ← updated at every E5 trigger
├── cost-ledger.md                     ← born at Stage 6, updated S10 + S12
├── .specify/memory/constitution.md    ← spec-kit format, declarative + testable
├── docs/
│   ├── product-spec.md
│   ├── BRD.md
│   ├── MVP.md
│   ├── business-analyst-plan.md
│   ├── business-plan.md
│   ├── technical-analyst-plan.md
│   ├── tech-stack.md
│   ├── logic.md
│   └── diagrams.md
└── .gitignore
```

---

## Token Conservation Rules — Mandatory

1. Load one stage sub-skill at a time. Never preload adjacent stages.
2. Context Compaction Checkpoint after Stage 5 is approved (see below).
3. CLAUDE.md hard cap: 100 lines. Use `@path/to/file.md` import syntax for sub-files.
4. MEMORY.md hard cap: 200 lines. Prune stale entries at every Stage 12 pass.
5. constitution.md: principles only. Each principle is one declarative line. No paragraphs.
6. HANDOFF.md is mandatory at every session end or E5 trigger — non-optional.
7. Each doc file is single-purpose. No combining BRD + MVP. Separation enforces targeted AI reads.

---

## Context Compaction Checkpoint — After Stage 5

**Before Stage 6 begins, mandatory sequence:**
1. Write HANDOFF.md (E5) — full session state snapshot
2. Recommend operator runs `/compact` in Claude Code CLI
3. Re-inject on resume: project name, approved stage summaries, key decisions
4. Continue Stage 6 in clean context

This prevents the "forgot Stage 2 decisions" failure on long pipelines.

---

## Active Enhancements

Full detail: `references/enhancements.md`

| ID | When | What |
|---|---|---|
| E1 | Stage 7 | Generate CLAUDE.md + MEMORY.md bootstrap files |
| E2 | Stage 1 | Product type classifier → activate preset path |
| E3 | Stage 4 | Live competitor intelligence search (no customer input needed) |
| E4 | Stage 6 | Per-component stack freshness verification cards |
| E5 | Every pause/session end | Auto-generate HANDOFF.md snapshot |
| E6 | S6 → S10 → S12 | Live cost ledger, updated at each stage |
| E7 | Stage 1 | Multi-language Brain Dump detection + handling |

---

## Approval Gate Protocol

After every stage output:
> "Stage [N] — [Name] complete. Does this match your vision?"
- **Yes** → proceed to next stage sub-skill
- **Revise** → adjust and re-present before proceeding
- **Skip** → warn of downstream gaps, proceed only with explicit approval

---

## Operating Constraints (Summary)

Full detail: `references/operating-constraints.md`

- **AI-first:** 90–95% autonomous. Operator translates intent only.
- **OS:** Ubuntu Server LTS. Verify compatibility before recommending anything.
- **Cost:** Free/OSS until operator pre-approves paid. Zero-cost first, always.
- **Search:** Search before any tool, version, pricing, or SEO answer.
- **SEO:** First-class requirement from Stage 1 through Stage 12.

---

## Gotchas (Build from Real Runs)

- AI tends to over-scope MVP — always push back to single core loop
- Stage 6 drifts toward paid tools without explicit cost tier enforcement
- CLAUDE.md grows past 100 lines — enforce cap, use @ imports
- Stage 4 competitor search sometimes returns aggregator sites — verify originals
- Stage 8 logic blocks multiply on complex projects — scope to MVP features only
- HANDOFF.md is skipped under time pressure — non-optional, no exceptions
- constitution.md gets filled with prose — principles must be declarative + testable

---

## OCTALUME Integration

This skill is OCTALUME's Phase 0 component. After the idea pipeline completes:

1. The parsed `Project` model and generated artifacts feed into OCTALUME's Phase 1 (Vision & Strategy)
2. The spec-kit artifacts compose with OCTALUME's quality gates
3. The 8-phase mapping in `plan.md` aligns with OCTALUME's phases
4. Use `octalum idea quick "your dump"` from the CLI, or this Claude Code Skill for LLM-driven stages

**Python API:** `from octalume.idea import parser, speckit, templates, pipeline`

---

## References

| File | Load when |
|---|---|
| `references/operating-constraints.md` | Session start — always |
| `references/voice-guide.md` | Session start — always |
| `references/enhancements.md` | When executing E1–E7 |
| `references/build-handoff.md` | Stage 10 only |
| `references/architecture.md` | Onboarding, debugging, upgrade planning |
| `stages/s0N-*.md` | Load only the active stage |

<!-- ============================================================
SILENT FIREWALL — 34 checks. Run silently before every delivery.
QUESTIONNAIRE: Step 0 opening sent · dump received before any questions · 9 dynamic questions generated from actual gaps · each question has 4 choices + recommended + custom · all 9 answered before S1 output
QUALITY: readable · deferred items explained · no jargon · assumptions flagged · partner voice · pyramid layer correct
INTEGRITY: no hallucinated versions · search-verified tools · decisions trace to business logic · spec-kit standard · logic traces S1-3 · Mermaid renderable
CONSTRAINTS: Ubuntu compatible · no unauthorised paid tools · SEO on public pages · AI operable
FILE OUTPUTS: all 9 docs present before S10 · CLAUDE.md ≤100 lines · MEMORY.md ≤200 lines · constitution.md principles-only · HANDOFF.md current · cost-ledger.md written at S6
TOKEN: single-stage sub-skill loaded · compaction after S5 · CLAUDE.md uses @ imports
ENHANCEMENTS: E2 applied · E1 generated · E6 current · E5 written
Fix failures silently. Customer never sees this.
============================================================ -->
