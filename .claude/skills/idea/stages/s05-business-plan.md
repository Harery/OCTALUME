# Stage 5 — Business Plan
Layer: Micro | Output: docs/business-plan.md
⚠ After this stage is approved — trigger Compaction Checkpoint before Stage 6.

## Adaptive questions (3–5 — deepening into micro-layer specifics)

> 1. What is the pricing structure — specific numbers, not ranges? (if not yet defined)
> 2. What does the first 90 days look like operationally — what does the operator actually do each week?
> 3. Are there any partnership or distribution channels worth including at launch?
> 4. What does the free tier or trial look like — if applicable?
> 5. What is the one metric that, if it moves, tells you the business is working? (your "north star")

## Output — docs/business-plan.md

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BUSINESS PLAN
docs/business-plan.md
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## Executive summary
[3 sentences: what it is, who it's for, how it makes money]

## Revenue model (detailed)
  - Pricing tiers: [specific numbers from Q1]
  - Free tier / trial: [from Q4, or "none"]
  - Revenue at 90 days: [projection based on success criteria from BRD]
  - Revenue at 12 months: [projection]

## Go-to-market plan
  Phase 1 (0–30 days): [specific launch actions]
  Phase 2 (31–60 days): [growth actions]
  Phase 3 (61–90 days): [scale or pivot trigger]

## Primary acquisition channel
  [From S4 Q3 — with specific tactics, not generalities]
  [SEO: primary keyword targets from S1, pages to build for launch]

## Weekly operations (90-day plan)
  [From Q2 — what does the solo operator actually do week by week]

## North star metric
  [From Q5 — the one number that proves the business is working]

## Cost model (E6 ledger reference)
  [All fixed costs at launch — from S6 ledger, or placeholder for S6]
  [Break-even point: N users at $X/mo]

## Partnerships and distribution
  [From Q3, or "none at launch"]

## 12-month milestones
  Month 1: [milestone]
  Month 3: [milestone]
  Month 6: [milestone]
  Month 12: [milestone]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## ⚡ Compaction Checkpoint — Mandatory before Stage 6

After approval of this stage:
1. Write HANDOFF.md (E5) — see `references/enhancements.md`
2. Tell operator: "Run `/compact` in Claude Code now to clear context before Stage 6."
3. On resume, re-inject: project name, approved stage summaries (S1–S5), key decisions
4. Then load `stages/s06-tech-stack.md`

Gate → `stages/s06-tech-stack.md`
