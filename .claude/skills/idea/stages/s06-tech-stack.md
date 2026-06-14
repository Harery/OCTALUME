# Stage 6 — Technical Analysis + Stack Decision
Layer: Nano | Enhancements: E4 (freshness cards), E6 (cost ledger)
Output: docs/technical-analyst-plan.md + docs/tech-stack.md

## Execute on load

Apply E4 immediately: for each recommended tool, run a structured freshness check.
Search pattern: "[tool] latest stable release [current year]"
Never write a version number without searching for it first.

Freshness card format per component:
```
Tool: [name]
Latest stable: [vX.X.X — search-verified YYYY-MM-DD]
Ubuntu LTS compatible: yes / no / [condition]
Free tier: [limits — search-verified]
Deprecation risk: none / low / flag ([reason])
AI operable: yes / no / [condition]
```

Stack selection rules:
- SSR/SSG frameworks only for SEO (Next.js, Nuxt, SvelteKit, Astro — search for current leader)
- Prefer self-hostable over managed SaaS
- Every component must be configurable by AI agent (Claude Code CLI / MCP)
- Monolith preferred at launch for AI maintainability
- No paid dependency without operator pre-approval from Q7

## Adaptive questions (3–5 — deep technical constraints)

> 1. Any hard platform constraints — VPS already purchased, domain already registered?
> 2. Any AI agent tools or MCP servers already in use that must be preserved?
> 3. What is the operator's comfort level with infrastructure? (none / basic / intermediate — determines how much IaC scaffolding to generate)
> 4. Any performance or scale requirements beyond standard MVP? (e.g. "must handle 10k concurrent users at launch")
> 5. Any preference between relational vs document database — or is this fully open?

## Output 1 — docs/technical-analyst-plan.md

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TECHNICAL ANALYST PLAN
docs/technical-analyst-plan.md
[All components search-verified: YYYY-MM-DD]
[OS: Ubuntu Server LTS | Model: AI-autonomous | Budget: zero-cost]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## Architecture pattern
[Monolith — justified for AI maintainability at launch]
[Exceptions: state the specific reason if not monolith]

## Technical constraints
[From S6 Q1–Q5 + S1 Q6]

## SEO technical approach
[SSR/SSG choice and reason, sitemap strategy, Core Web Vitals plan]

## AI operability confirmation
[Each component: deployable/configurable by AI agent — confirmed or flagged]

## Security approach
[HTTPS, env vars, input sanitisation, auth model]

## Scalability path
[What breaks first at scale, and what the upgrade path looks like]

## Integration map
[External services → how they connect → what happens if they go down]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Output 2 — docs/tech-stack.md

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TECH STACK
docs/tech-stack.md
[All components search-verified: YYYY-MM-DD]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## Stack (E4 freshness card per component)
  Frontend:    [framework vX.X — Ubuntu ✓ — Cost: OSS]
  Backend:     [runtime + framework vX.X — Ubuntu ✓ — Cost: OSS]
  Database:    [db vX.X — self-hosted — Ubuntu ✓ — Cost: OSS]
  Auth:        [solution — Ubuntu ✓ — Cost: $0]
  File storage:[solution — Cost: $0 / free tier limit: X]
  Email:       [provider — Cost: $0 until N/day — search-verified]
  Payments:    [provider — Cost: % per transaction only — no monthly fee]
  Reverse proxy:[Caddy or Nginx — Ubuntu ✓ — Cost: OSS]
  SSL:         [Let's Encrypt — Cost: $0]
  CI/CD:       [GitHub Actions free tier — Cost: $0]
  Hosting:     [Ubuntu VPS — provider — search-verified ~$X/mo]
  Analytics:   [Umami or Plausible self-hosted — Cost: $0]
  AI tooling:  [Claude Code CLI + MCP servers]

## Why this stack
  [One sentence per component — plain language, no jargon]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Output 3 — cost-ledger.md (E6 — born here, updated S10 + S12)

**File path:** `cost-ledger.md` (project root)
Write this as a standalone file. It is referenced at Stage 12 completion and must exist.

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
LIVE COST LEDGER — [Project Name]
cost-ledger.md
Last updated: [YYYY-MM-DD] | Verified via web search
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Component       | Tool              | Launch    | @ 1k users | @ 10k users | Paid trigger
----------------|-------------------|-----------|------------|-------------|------------------
Hosting         | [VPS + provider]  | ~$X/mo    | ~$X/mo     | ~$X/mo      | [RAM/traffic]
Database        | [solution]        | $0        | $0         | $X/mo       | [threshold]
Auth            | [solution]        | $0        | $0         | $X/mo       | [threshold]
File storage    | [solution]        | $0        | $0         | $X/mo       | [threshold]
Email           | [provider]        | $0        | $0         | $X/mo       | [daily limit]
Analytics       | [self-hosted]     | $0        | $0         | $0          | Never
Monitoring      | [self-hosted]     | $0        | $0         | $0          | Never
CDN             | Cloudflare free   | $0        | $0         | $0          | Enterprise
SSL             | Let's Encrypt     | $0        | $0         | $0          | Never
CI/CD           | GitHub Actions    | $0        | $0         | $0          | >2000 min/mo
----------------|-------------------|-----------|------------|-------------|------------------
TOTAL           |                   | ~$X/mo    | ~$X/mo     | ~$X/mo      |

Pre-approval threshold: operator signs off before any single line goes paid.
Scale notes added at Stage 10. Final figures confirmed at Stage 12.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Gate → `stages/s07-constitution.md`
