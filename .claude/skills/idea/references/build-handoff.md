# Build Handoff — Stage 10 Reference
Updated to align with 12-stage pipeline and 5-step build order.

## Pre-Build Checklist
Before writing a single line of code, confirm all approved:
- [ ] Stage 6: Stack decision locked + cost ledger (E6) initialised
- [ ] Stage 7: Constitution approved + CLAUDE.md + MEMORY.md generated (E1)
- [ ] Stage 8: All logic definitions complete + scope limited to MVP
- [ ] Stage 9: All diagrams approved (erDiagram required for Step 1)
- [ ] E6 cost ledger: all components documented, no unauthorised paid tools

If any missing → return to that stage. Do not proceed.

## Build Order (Strict — 5 Steps)
Present each step for operator review before proceeding to the next.

### Step 1 — The Filing Cabinet (Data Model)
Everything depends on this. Build first.

Deliver:
- Full schema — all tables/collections, relationships, field types, constraints
- Plain-language description of each table
- Reference the erDiagram from Stage 9 exactly
- Migrations or seed scripts where needed
- Ubuntu LTS compatible, zero paid dependencies

### Step 2 — The Engine Room (Business Logic + API)
The brain of the app. Built to Stage 8 logic definitions exactly.

Deliver:
- Core business logic matching every Stage 8 function definition
- API routes / server actions for every user flow
- Auth system (approved solution from Stage 6)
- Permission rules as defined in Stage 8
- AI automation hooks (deployment trigger, monitoring response, cost alert)
- Error handling for every edge case in Stage 8

### Step 3 — The Showroom (UI — SSR/SSG, SEO-first)
What users see. Built to constitution SEO standards.

Deliver:
- All MVP pages (SSR or SSG — never client-only SPA for public pages)
- Semantic HTML: correct h1→h2→h3 hierarchy, landmark elements
- Meta title + description on every page
- Open Graph tags (og:title, og:description, og:image, og:url)
- Mobile-first responsive at 320px minimum
- Loading states, error states, form validation

### Step 4 — The Deployment Kit (Ubuntu → Production)
The machine that ships it and keeps it running.

Deliver:
- Ubuntu LTS server setup script (apt installs, user creation, firewall)
- Caddy or Nginx config + Let's Encrypt SSL automation
- Systemd service file for the app
- GitHub Actions CI/CD pipeline (free tier)
- Environment variables template (.env.example — never commit real values)
- Claude Code CLI config for AI-autonomous deployment

### Step 5 — The SEO Foundation
The signal layer that brings organic traffic. Built last so it wraps the real content.

Deliver:
- sitemap.xml (auto-generated, covers all public routes)
- robots.txt (configured, never blocking indexable pages)
- JSON-LD structured data (type determined by product — Course, LocalBusiness, etc.)
- Open Graph image (og:image) for all key pages
- Google Search Console verification file
- Core Web Vitals baseline check (target: LCP <2.5s, CLS <0.1, INP <200ms)

## Code Standards
All code must comply with the Stage 7 constitution. Non-negotiable.
Every file: Ubuntu LTS compatible · zero unauthorised paid deps · AI-operable.

## E6 Cost Ledger Update
After Step 4, update the cost ledger with any new components introduced in the build.
Add scale estimates: @ launch / @ 1k users / @ 10k users.

## Handoff Message to Customer (plain language)

> "The plan is locked and approved across all 12 stages. Now we build.
>
> I'll do it in 5 steps:
> 1. The Filing Cabinet — how all your data is organised
> 2. The Engine Room — the logic that makes everything work
> 3. The Showroom — what your users actually see and touch
> 4. The Deployment Kit — the machine that ships it automatically
> 5. The SEO Foundation — the signal layer that brings you organic traffic
>
> I'll show you each piece as it's done. You don't need to read the
> code — just tell me if the result does what you imagined."

## Stack Translation Reminder

| Tech term | Customer name |
|---|---|
| Database schema | The Filing Cabinet |
| API routes + logic | The Engine Room |
| Authentication | The Front Door |
| UI components | The Showroom |
| Server setup scripts | The Building Blueprint |
| CI/CD pipeline | The Automatic Safety Checklist |
| Environment config | The Secret Keys Drawer |
| SSL certificate | The Security Lock |
| sitemap.xml | The Map Google Uses to Find You |
| JSON-LD structured data | The Label That Tells Google What This Page Is |
