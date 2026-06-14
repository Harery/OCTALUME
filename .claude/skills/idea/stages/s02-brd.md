# Stage 2 — Business Requirements Document (BRD)
Layer: Macro→Meso | Output: docs/BRD.md

## Adaptive questions (3 max — ask only if unanswerable from Stage 1 output)

> 1. What does success look like in 6 months — is there a revenue, user, or traffic number attached?
> 2. Any regulatory or legal constraints not captured in Q6/Q9 from the intake?
> 3. Any existing tools or platforms the product must integrate with — or can never replace?

Never ask questions already answered in the 9-question intake.
Infer from S1 output wherever possible. Flag assumptions in the output.

## Output — docs/BRD.md

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BUSINESS REQUIREMENTS DOCUMENT
docs/BRD.md
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## Problem statement
[Precise. References the user-perspective answer from Q1.]

## Business objectives (measurable)
[Numbers. No vague goals. Reference Q4 and the 6-month target.]

## Stakeholders
  - Primary users: [from Q2]
  - Secondary users: [inferred or stated]
  - Operators/admins: [from Q8]
  - Business owner: operator + AI agent — no dev team

## Success criteria
  [Include: organic search traffic target, SEO ranking goal, core metric from Q4]

## Constraints
  - Budget: [from Q7 — zero-cost / pre-seed / funded]
  - Operating model: AI-autonomous, Ubuntu Server LTS, OSS-first stack
  - Timeline: [from Q8, or "none stated"]
  - Regulatory: [from Q6 + Stage 2 Q2]
  - Integrations: [from Q9 + Stage 2 Q3]
  - Red lines: [from Q5 — the hard limit question]

## Risks and flags
  [Include: anything blocking AI-autonomous operation]
  [Include: assumptions made due to unanswered questions]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Gate → `stages/s03-mvp.md`
