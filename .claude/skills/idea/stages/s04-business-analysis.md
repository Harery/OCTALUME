# Stage 4 — Business Analysis
Layer: Meso→Micro | Enhancement: E3 (live competitor search) | Output: docs/business-analyst-plan.md

## Execute on load

Apply E3 immediately — do NOT ask the operator about competitors.
Search the product domain for current competitors before writing any questions.
Use product type from S1 E2 classifier to target the search correctly.

Search queries to run (adapt to the product domain):
- "[product domain] top competitors [current year]"
- "[product domain] market size [current year]"
- "[product domain] pricing models"
- "[primary keyword from S1] site:g2.com OR site:capterra.com OR site:producthunt.com"

## Adaptive questions (3–5 — moving from Meso to Micro)

Ask only after E3 search is complete.

> 1. Who is your target customer segment most precisely — demographics, job role, or situation?
> 2. What is the revenue model: subscription / one-time / usage-based / freemium / marketplace fee / other?
> 3. What is the primary acquisition channel at launch — SEO / paid / referral / community / direct sales?
> 4. Are there any regulatory or compliance requirements specific to this market segment? (if not covered in S2)
> 5. What is the unit economics target — what does one converted user need to generate to be viable? (ask only if revenue model was stated)

## Output — docs/business-analyst-plan.md

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BUSINESS ANALYST PLAN
docs/business-analyst-plan.md
[Competitor research completed: YYYY-MM-DD]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## Market landscape (E3 — search-verified)
  [Top 3–5 competitors | their positioning | pricing | key weakness]
  [Market size estimate if available — cite source]

## Competitive SEO gap (E3)
  [Keywords competitors rank for vs available opportunities]
  [One SEO angle this product can own that competitors don't]

## Target segment
  [From Q1 this stage — specific, not a persona template]

## Revenue model
  [From Q2 this stage — with unit economics if stated]

## Acquisition strategy
  [From Q3 this stage — primary channel at launch]

## Stakeholder map
  - Decision maker: [who approves the purchase/signup]
  - Primary user: [who uses it daily]
  - Admin/operator: [who configures it]

## Compliance and regulatory
  [From S2 + S4 Q4 — what must be designed around from day one]

## Business risks
  [Market, competitive, and execution risks specific to this product]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Gate → `stages/s05-business-plan.md`
