# Stage 10 — Generate the Build
Layer: Build | Enhancement: E6 (update cost ledger)
Full detail: `references/build-handoff.md`

## Pre-build checklist
- [ ] Stage 6 stack approved
- [ ] Stage 7 constitution approved + CLAUDE.md generated
- [ ] Stage 8 all logic definitions complete
- [ ] Stage 9 diagrams approved
If any missing → return to that stage before proceeding.

## Build order (strict — never skip)
Present each section for review before proceeding to the next.

1. **The Filing Cabinet** — data model, schema, all relationships
   Reference: erDiagram from Stage 9
2. **The Engine Room** — core business logic, API layer, auth, AI automation hooks
   Reference: logic definitions from Stage 8
3. **The Showroom** — UI components, pages (SSR/SSG, SEO-first)
   Reference: constitution SEO standards from Stage 7
4. **The Deployment Kit** — Ubuntu server setup scripts, CI/CD, AI agent config
5. **The SEO Foundation** — sitemap.xml, robots.txt, meta tags, JSON-LD, Open Graph

## Every file generated must include
- Ubuntu LTS compatibility confirmed
- Zero paid dependencies (or flagged with pre-approval note)
- AI-operable: deployable via Claude Code CLI
- SEO requirements met for all public-facing routes

## E6 cost ledger update
Update the cost ledger from Stage 6 with any new components introduced.
Add scale estimates: @ launch / @ 1k users / @ 10k users.

Gate → `stages/s11-monitoring.md`
