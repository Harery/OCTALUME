# Stage 3 — MVP Definition
Layer: Meso | Output: docs/MVP.md

## Adaptive questions (3–4 max — tightening scope from BRD)

> 1. If you could only ship ONE feature at launch, what would it be — and why?
> 2. What is the minimum a user must be able to do for the product to be worth showing to a real person?
> 3. What is explicitly OUT of scope for v1 — things you want but will not build yet?
> 4. Is there an existing manual process users do today that this replaces? (only ask if unclear from S1–S2)

Hard rule: push back on any MVP that contains more than one core user loop.
If the operator lists 6+ features, reduce to 1 core loop + defer list. Explain why.

## Output — docs/MVP.md

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MVP DEFINITION
docs/MVP.md
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## The core loop
[One paragraph. What a user does from first touch to job-done. No branching. No edge cases.]

## Launch criteria (must ALL be true to ship)
  - [ ] Core loop works end-to-end
  - [ ] Core public pages are SEO-indexable
  - [ ] Auth and data are secure
  - [ ] Deployable by AI agent without manual steps
  - [ ] Cost is within approved budget

## MVP feature list (only what enables the core loop)
  [Feature | Why it's essential | Stage 8 logic reference]

## Explicitly deferred (v2+)
  [Feature | Reason for deferral]

## Risks
  [What could block the core loop from shipping]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Gate → `stages/s04-business-analysis.md`
