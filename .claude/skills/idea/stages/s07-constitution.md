# Stage 7 — SpecKit Constitution + Bootstrap Files
Layer: Nano | Enhancement: E1 (all bootstrap files)
Note: "SpecKit constitution" refers to the custom declarative format defined in this stage — see output template below.

## Purpose

Generate the project's governing law and all AI agent bootstrap files.
Every Stage 10 implementation decision MUST comply with this constitution.

## Adaptive questions (3 max — ask only if unanswerable from prior stages)

- What code style conventions does the operator already follow? (formatter, linter, naming)
- Any regulatory compliance requirements not already stated? (GDPR, HIPAA, PCI-DSS)
- Any existing domain/VPS already provisioned that constrains infrastructure choices?

---

## Output 1 — constitution.md

**File path:** `.specify/memory/constitution.md`
**Format rules (spec-kit standard):**
- Each principle is one declarative line
- Use MUST / MUST NOT / SHOULD — never "should" without rationale
- No paragraphs, no prose, no explanations inside the constitution itself
- Principles must be testable — if you cannot write a check for it, rewrite it
- Version line in ISO date format: `v[N].[N] — YYYY-MM-DD`
- Prepend a Sync Impact Report as HTML comment after any update
- No vague language ("clean code", "best practices") — replace with specific rules

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SPECKIT CONSTITUTION — [Project Name]
.specify/memory/constitution.md
v1.0 — [YYYY-MM-DD]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Mission
[One sentence. What this system does and for whom.]

## Operating model
- Operator: 1 human (intent translation only)
- Execution: AI agent (Claude Code CLI — all else)
- Infrastructure: Ubuntu Server [current LTS version — search to verify]
- Budget: zero-cost until [operator-stated threshold from Q7]

## Code quality
- MUST use [search-verified linter] with [config] — no exceptions
- MUST use [search-verified formatter] — auto-run on save
- MUST use TypeScript strict mode (or equivalent for chosen language)
- MUST NOT commit commented-out code
- Comments explain intent — AI and operator must both understand without context

## Testing
- MUST have automated tests for all critical paths
- MUST NOT require manual steps to run test suite
- Tests MUST be executable via single command by AI agent

## SEO (public-facing pages only)
- MUST use SSR or SSG — never client-only SPA for indexable content
- MUST include <title>, <meta description>, OG tags, JSON-LD on every public page
- MUST generate sitemap.xml and robots.txt on deploy
- MUST achieve LCP < 2.5s, CLS < 0.1, INP < 200ms

## Performance
- MUST target 90+ Google PageSpeed score on mobile
- MUST use next-gen image formats (WebP/AVIF) with explicit dimensions

## Security
- MUST NOT hardcode secrets — environment variables only
- MUST use HTTPS — Let's Encrypt via Caddy or Certbot
- MUST sanitise all user input at the API boundary

## AI operability
- MUST be deployable by AI agent without manual SSH intervention
- MUST use infrastructure-as-code for all configuration
- MUST NOT require GUI-only configuration steps

## Cost governance
- MUST NOT introduce paid dependencies without operator pre-approval
- MUST document free-tier fallback for every external service
- Paid upgrade trigger: [specific metric from S6 cost ledger]

## Decision governance
- Rule 1: When in doubt → check BRD objectives (docs/BRD.md)
- Rule 2: Choose simpler, more AI-maintainable implementation
- Rule 3: Choose free option unless it genuinely blocks progress
- Rule 4: SEO is never optional on public-facing pages
- Rule 5: Flag to operator if rules conflict — do not self-resolve silently

## Definition of done (per feature)
- [ ] Tests pass
- [ ] SEO check passes (if public-facing)
- [ ] AI operability check passes
- [ ] Cost check passes (no new paid deps without approval)
- [ ] MEMORY.md updated with decision log entry
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**To generate the full constitution in Claude Code, run:**
```
/speckit.constitution [paste the 5–6 line seed below]
```

**5–6 line constitution seed (copy and paste into Claude Code):**
```
Project: [name]. Stack: [from Stage 6]. Operator: solo human + Claude Code CLI.
Infrastructure: Ubuntu Server LTS. Budget: zero-cost until [threshold].
Code: [linter] + [formatter], TypeScript strict. Tests: automated only, AI-executable.
SEO: SSR/SSG, Core Web Vitals targets. Security: no hardcoded secrets, HTTPS mandatory.
AI operability: all deploys scriptable, no manual SSH. Paid deps: operator approval required.
Definition of done: tests pass + SEO check + AI operability check + cost check + MEMORY.md updated.
```

---

## Output 2 — CLAUDE.md (E1)

**File path:** `CLAUDE.md` (project root)
**Hard cap: 100 lines**
**Best practices applied:**
- Short + human-readable — Claude ignores bloated CLAUDE.md files
- Bash commands for every common task (deploy, test, lint, build, dev)
- Use `@path/to/file.md` import syntax to reference sub-files instead of inlining
- Never inline the constitution — reference it
- Never add instructions that aren't universally applicable to all sessions
- No vague rules ("write clean code") — only specific, checkable instructions

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CLAUDE.md — [Project Name]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Project
[One-line description]

# Stack (search-verified versions)
- Frontend: [framework vX.X]
- Backend: [runtime + framework vX.X]
- Database: [db vX.X]
- Auth: [solution]
- Infra: Ubuntu [LTS version], Caddy, GitHub Actions

# Commands
- Dev:    [command]
- Test:   [command]
- Lint:   [command]
- Build:  [command]
- Deploy: [command]

# Memory files
@.claude/memory/MEMORY.md
@.specify/memory/constitution.md

# Never without operator approval
- Upgrade paid tier on any service
- Modify .specify/memory/constitution.md
- Delete or rename database tables
- Add a new external API integration
- Change deployment target or infrastructure provider

# Code rules
- [linter] + [formatter] — auto-run before every commit
- TypeScript strict (or equivalent) — no any types
- No hardcoded secrets — env vars only
- Comments explain intent — not what the code does

# When stuck
1. Check docs/BRD.md for objectives
2. Check .specify/memory/constitution.md for governing rules
3. Check docs/logic.md for workflow definitions
4. Flag to operator before self-resolving conflicts
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Output 3 — MEMORY.md (E1)

**File path:** `.claude/memory/MEMORY.md`
**Hard cap: 200 lines**
**Purpose:** Persistent architectural decisions log, readable by AI agent at session start

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MEMORY.md — [Project Name]
.claude/memory/MEMORY.md
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Pipeline state
- Current stage: 7 (approved)
- Next stage: 8 — Logic + workflow definitions
- Last compaction: [date or "not yet — due after S5"]

# Architectural decisions log
[YYYY-MM-DD] Stack: [choices] — Reason: [from S6]
[YYYY-MM-DD] Auth: [choice] — Reason: [from S6]
[YYYY-MM-DD] DB: [choice] — Reason: [from S6]
[YYYY-MM-DD] Hosting: [choice] — Reason: [from S6]

# Key decisions from stages 1–7
- Product type: [from S1 E2 classifier]
- Core job: [from S1]
- MVP scope: [from S3 — single core loop]
- Revenue model: [from S4]
- Budget threshold: [from Q7]
- Non-negotiable red line: [from Q5 — hard limit question]

# Open flags
[Any unresolved assumptions from stages 1–7]

# Cost ledger (E6 — current at S7)
[Component | Cost tier | Free-tier limit | Paid trigger]

# Known gotchas
[Project-specific issues discovered during pipeline — not generic]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Output 4 — HANDOFF.md (E5)

**File path:** `HANDOFF.md` (project root)
**Updated at:** every session end, every E5 trigger, and the compaction checkpoint

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
HANDOFF.md — [Project Name]
Session handoff — [YYYY-MM-DD HH:MM]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Status
- Last completed stage: [N] — [Name]
- Approval status: [approved / in revision]
- Next action: [exact next step]

# Decisions made this session
[Date | Stage | Decision | Rationale]

# Open questions
[Unresolved items needing operator input]

# Files written this session
[path | status: written / updated / pending]

# Resume instructions
To continue: load CLAUDE.md, read MEMORY.md, then run Stage [N+1]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Project scaffold output

```
/[project-name]/
├── CLAUDE.md                          ← < 100 lines
├── HANDOFF.md                         ← session state
├── .specify/
│   └── memory/
│       └── constitution.md            ← spec-kit format
├── .claude/
│   ├── memory/
│   │   └── MEMORY.md                  ← < 200 lines
│   └── rules/
├── docs/
│   ├── product-spec.md
│   ├── BRD.md
│   ├── MVP.md
│   ├── business-analyst-plan.md
│   ├── business-plan.md
│   ├── technical-analyst-plan.md
│   ├── tech-stack.md
│   ├── logic.md                       ← written at Stage 8
│   └── diagrams.md                    ← written at Stage 9
└── .gitignore
```

Gate → `stages/s08-logic.md`
