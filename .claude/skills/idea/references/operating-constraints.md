# Operating Constraints — Full Reference

Read this file at the start of every session before any stage output.
These are hard rules. Not preferences. Every violation is a Silent Firewall failure.

---

## 1. AI-First Operating Model

**The setup:** One human operator + AI. That's the entire team.
- Operator role: translate customer intent into the pipeline. Nothing else.
- AI role: everything else — build, deploy, configure, test, maintain, upgrade, monitor.
- No human developer. No external team. No freelancers.

**What this means for every recommendation:**
- Every tool must be operable by AI agent (Claude Code CLI, agentic workflows, MCP)
- Every deployment must be scriptable and AI-executable without manual SSH
- Every configuration must be infrastructure-as-code, not manual UI clicks
- Every maintenance task must be automatable via scheduled AI agent runs
- Flag any recommendation that requires a human developer to operate

**Preferred AI tooling:**
- Claude Code CLI for primary development and deployment
- MCP servers for external service integration
- GitHub Actions (free tier) for CI/CD automation
- Shell scripts on Ubuntu for system-level automation

---

## 2. Infrastructure: Linux Ubuntu Server LTS

**The only server environment: Ubuntu Server LTS.**

- No Windows Server. No macOS. No other Linux distros unless explicitly required.
- Current LTS: search for latest Ubuntu LTS version before recommending
- Package management: `apt` for system packages, `npm`/`pip`/`cargo` for language packages
- Containerisation: Docker on Ubuntu when isolation is needed
- All shell scripts: bash, targeting Ubuntu LTS
- Systemd for service management

**VPS providers (search for current pricing before recommending):**
- Hetzner Cloud — typically cheapest in Europe
- Contabo — typically cheapest globally for raw specs
- OVH — good EU option
- DigitalOcean / Linode — slightly more expensive but excellent documentation
- Never recommend a VPS without searching for current pricing first

**Always verify:** Ubuntu LTS compatibility before recommending any tool, package,
or service. If uncertain — search first.

---

## 3. Zero-Cost-First Rule

**The law:** Every component must be free until operator explicitly approves paid.

### Cost tier priority (strict order):
1. **Free & open-source, self-hosted on Ubuntu** — always first choice
2. **Free tier of managed service** — when self-hosting is genuinely impractical
3. **Cheapest paid tier** — only when free tier is a genuine blocker, with operator approval
4. **Standard paid** — only after traction is proven and operator pre-approves

### Rules:
- Never recommend paid when a free equivalent performs adequately
- Every Stage 6 stack component must show its cost tier explicitly
- Define the exact trigger that would justify upgrading to paid:
  - User count threshold (e.g. "free tier sufficient until 1,000 active users")
  - Traffic threshold (e.g. "Cloudflare free handles up to 100k requests/day")
  - Revenue threshold (e.g. "introduce Stripe fees only when first booking is made")
- If a free tier has meaningful limitations, document them explicitly

### Common free tier reference (always search to verify current limits):
- **Supabase free:** PostgreSQL + Auth + Storage + Realtime
- **Cloudflare free:** CDN, DNS, DDoS protection, Pages, Workers (limited)
- **GitHub free:** Repos, Actions (2000 min/month), Pages
- **Vercel free:** Deployments (limited bandwidth) — but prefer self-hosted on Ubuntu
- **Plausible / Umami (self-hosted):** Free analytics on own Ubuntu server
- **Caddy / Nginx:** Free reverse proxy + SSL on Ubuntu
- **Let's Encrypt:** Free SSL certificates
- **Resend free / Mailgun free / Brevo free:** Email sending (verify current limits)

---

## 4. Live Internet Search — Mandatory

**The rule:** Search before answering anything that could have changed.

### Always search for:
- Any tool, package, or library recommendation (check for deprecations, successors)
- Any version number (never state a version from training memory alone)
- Any pricing or free-tier information (these change frequently)
- Any SEO best practice (Google algorithm changes constantly)
- Any AI model or agent capability (capabilities change rapidly)
- Any Ubuntu LTS compatibility question
- Any "current best practice" in web development, security, or DevOps
- Competitor landscape for any product domain
- Keyword volumes and SEO data for the product domain

### Search cadence:
- At every stage boundary before producing output
- Before every tool recommendation in Stage 6
- Before every SEO recommendation in any stage
- Before stating any version number anywhere

**If search returns no result or result is ambiguous:**
- State uncertainty explicitly
- Do not guess
- Provide the closest verified answer and flag the gap

---

## 5. SEO — First-Class Requirement

SEO is not a Phase 2 task. It is built in from the first line of code.

### Per-stage SEO responsibilities:

**Stage 1:** Identify primary keyword universe (5–10 terms real users search)
**Stage 2:** SEO as a measurable BRD success criterion
**Stage 3:** Core pages SEO-indexable from day one in launch criteria
**Stage 4:** Competitive SEO gap — what keywords competitors own vs what's available
**Stage 5:** SEO as primary zero-cost acquisition channel in GTM plan
**Stage 6:** SSR/SSG stack required; sitemap, robots.txt, meta tags in architecture
**Stage 7:** SEO standards in constitution — semantic HTML, Core Web Vitals as quality rules
**Stage 8:** URL slug logic, canonical rules, sitemap update triggers defined
**Stage 9:** Site architecture / URL map diagram; crawl path diagram
**Stage 10:** Full SEO-first build implementation

### Non-negotiables in every build:
- **Rendering:** SSR or SSG only for public-facing pages. Never client-only SPA for indexable content.
- **HTML semantics:** h1→h2→h3 hierarchy. Correct landmark elements (`<main>`, `<nav>`, `<article>`, etc.)
- **Meta tags:** `<title>` (50–60 chars) + `<meta name="description">` (150–160 chars) on every page
- **Open Graph:** `og:title`, `og:description`, `og:image`, `og:url` on every page
- **Twitter/X Card:** `twitter:card`, `twitter:title`, `twitter:description`, `twitter:image`
- **Structured data:** JSON-LD schema appropriate to content type
  - LocalBusiness for location-based services
  - Course / EducationalOrganization for education platforms
  - FAQPage for FAQ sections
  - BreadcrumbList for multi-level navigation
  - Person / Organization as appropriate
- **sitemap.xml:** Auto-generated, includes all public URLs, submitted to Google Search Console
- **robots.txt:** Configured, never blocking indexable pages
- **Canonical URLs:** `<link rel="canonical">` on every page
- **Core Web Vitals targets:**
  - LCP (Largest Contentful Paint) < 2.5s
  - CLS (Cumulative Layout Shift) < 0.1
  - INP (Interaction to Next Paint) < 200ms
- **Mobile-first:** All pages responsive at 320px minimum (Google mobile-first indexing)
- **HTTPS:** Mandatory. Let's Encrypt via Caddy or Certbot on Ubuntu.
- **Image optimisation:** Next-gen formats (WebP/AVIF), explicit width/height attributes
- **Internal linking:** Logical site structure, key pages within 3 clicks of homepage
- **Page speed:** Aim for 90+ Google PageSpeed score on mobile

### SEO tools (free, self-hostable where possible):
- **Google Search Console:** Free. Required. Submit sitemap on launch.
- **Google Analytics 4:** Free. Or self-hosted Umami/Plausible for privacy.
- **Ahrefs Webmaster Tools free tier:** For backlink monitoring
- **Screaming Frog free (up to 500 URLs):** For crawl audits
