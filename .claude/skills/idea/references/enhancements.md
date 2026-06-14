# Enhancements Reference — Full Detail

Seven enhancements active across the pipeline. Read when executing the relevant stage.

---

## E1 — CLAUDE.md + MEMORY.md + HANDOFF.md (generated at Stage 7, updated every session)

### Why it exists
AI agents start every session with amnesia. Without persistent memory files, the agent
forgets architectural decisions, operator preferences, and project state between sessions.
This causes contradictory decisions within weeks. These three files are the solution.

### CLAUDE.md rules (Anthropic best practice — 2025)
- Hard cap: **100 lines**. Claude ignores bloated CLAUDE.md files.
- Use `@path/to/file.md` import syntax to reference sub-files instead of inlining content.
- Only include instructions that are universally applicable to ALL sessions.
- No vague rules ("write clean code") — only specific, checkable instructions.
- The `<system-reminder>` wrapper Claude Code uses means irrelevant content gets ignored.
  The shorter and more focused CLAUDE.md is, the more reliably Claude follows it.

See `stages/s07-constitution.md` for the full CLAUDE.md template.

### MEMORY.md rules
- Hard cap: **200 lines**
- Location: `.claude/memory/MEMORY.md`
- Read at session start via `@.claude/memory/MEMORY.md` import in CLAUDE.md
- Prune at every Stage 12 maintenance pass — merge duplicates, delete stale entries

### Update protocol (every session end):
1. Update MEMORY.md: decisions made, corrections, state changes
2. If MEMORY.md > 200 lines: curate — merge similar entries, delete stale ones
3. If new "never do" rule found: add to CLAUDE.md (keep under 100 lines — use @ imports)
4. Write HANDOFF.md (E5) — always, no exceptions

---

## E2 — Product Type Classifier (Stage 1)

After identifying product type at Stage 1, activate the appropriate preset path.
This sharpens every downstream stage automatically.

| Product type | Stage 4 SEO focus | Stage 8 mandatory logic | Stage 10 schema |
|---|---|---|---|
| Marketplace | Provider + consumer keyword split | Payment split, provider onboarding, dispute flow | Product, Offer |
| SaaS | Feature comparison terms, "X alternative" | Subscription, trial, seat management | SoftwareApplication |
| Content platform | Topic clusters, article keywords | Content publishing workflow, author roles | Article, BlogPosting |
| Service portal | Local + service keywords | Booking/scheduling, availability, confirmation | LocalBusiness, Service |
| Education platform | Course + skill keywords | Teacher scheduling, student progress, parent supervision | Course, EducationalOrganization |
| Community/social | Community + niche keywords | Moderation queue, reporting, ban logic | Organization |

---

## E3 — Live Competitor Intelligence Search (Stage 4)

**Rule:** Stage 4 never asks the customer to name competitors. It finds them first.

**Search sequence:**
1. `[product domain] best platforms [current year]`
2. `[product domain] top alternatives`
3. `[product domain] [primary keyword] app`

**For each of top 3 competitors found:**
- What keywords do they rank for? (search: `site:[competitor.com] top pages` or use Ahrefs free)
- What does their homepage say they do?
- What are users saying they're missing? (search: `[competitor] alternatives` or Reddit)

**Output per competitor:**
```
Competitor: [name + URL]
What they do: [one sentence]
Top keywords they own: [list]
Gap they leave: [what this product could capture]
```

**Then map the SEO opportunity:**
```
Keyword gap analysis:
- [keyword] — competitor ranks #X, we can target with [page/content type]
- [keyword] — no strong competitor, high opportunity
```

Deliver findings → customer confirms or corrects.

---

## E4 — Per-Component Stack Freshness Check (Stage 6)

Replace a single general search with a structured per-component verification card.

**For each recommended tool, produce:**
```
Tool: [name]
Purpose: [one line]
Latest stable version: [X.Y.Z] (searched [date])
Last release: [date]
Ubuntu LTS compatible: yes / no / [caveats]
Free tier: [limits] / self-hosted: no cost
Paid trigger: [exact threshold]
Deprecation risk: none / low / [flag if successor tool found]
AI-operable: yes / [caveats]
Install command (Ubuntu): [apt/npm/pip/docker command]
```

**Red flags that trigger a replacement search:**
- Last release > 12 months ago
- GitHub repo archived or "no longer maintained"
- Critical CVEs unpatched > 30 days
- Free tier changed to paid since last recommendation

---

## E5 — HANDOFF.md (written at session end, stage pauses, and compaction checkpoint)

**Rule: Non-optional. Never skip. No exceptions under time pressure.**

**Trigger conditions — write HANDOFF.md when ANY of these occur:**
- Operator says anything signalling the session is ending ("ok thanks", "I'll come back to this", "let's stop here", "I'll continue later", or similar)
- Any stage approval gate is reached
- The compaction checkpoint after Stage 5
- Stage 12 completion (pipeline end)
- **Claude.ai users have no `/compact` CLI command** — in that environment, treat every stage gate as a mandatory E5 trigger. Do not wait to be asked.

**File:** `HANDOFF.md` (project root — overwrite on each trigger)
**Also copy the state block into MEMORY.md** to make the session resumable without re-reading HANDOFF.md

**Format:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
HANDOFF.md — [Project Name]
Session handoff — [YYYY-MM-DD HH:MM]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Status
- Last completed stage: [N] — [Name]
- Approval status: [approved / in revision]
- Next action: [exact next step — specific enough to act on without context]

# Decisions made this session
[YYYY-MM-DD | Stage | Decision | Rationale]

# Assumptions flagged
- [assumption] — awaiting operator confirmation
- [assumption] — assumed [X], correct if wrong

# Open questions
- [question requiring operator input]

# Files written this session
[path | status: written / updated / pending]

# Resume instructions
Load CLAUDE.md → read MEMORY.md → read this file → continue at Stage [N+1]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## E6 — Live Cost Ledger

Generated at Stage 6. Updated at Stage 10 (build) and Stage 12 (maintenance).

**Format:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
LIVE COST LEDGER — [project name]
Last updated: [date] | Verified via web search
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Component       | Tool              | Launch    | @ 1k users | @ 10k users | Paid trigger
----------------|-------------------|-----------|------------|-------------|------------------
Hosting         | Hetzner CX21      | ~$5/mo    | ~$5/mo     | ~$15/mo     | Traffic/RAM limit
Database        | Supabase free     | $0        | $0         | $25/mo      | >500MB or >50k MAU
Auth            | Supabase free     | $0        | $0         | $25/mo      | >50k MAU
File storage    | Supabase free     | $0        | $0         | $25/mo      | >1GB
Email           | Brevo free        | $0        | $0         | $25/mo      | >300/day
Analytics       | Umami self-hosted | $0        | $0         | $0          | Never (self-hosted)
Monitoring      | Uptime Kuma       | $0        | $0         | $0          | Never (self-hosted)
CDN             | Cloudflare free   | $0        | $0         | $0          | Enterprise needs
SSL             | Let's Encrypt     | $0        | $0         | $0          | Never
CI/CD           | GitHub Actions    | $0        | $0         | $0          | >2000 min/mo
----------------|-------------------|-----------|------------|-------------|------------------
TOTAL           |                   | ~$5/mo    | ~$5/mo     | ~$90/mo     |

Pre-approval threshold: operator signs off before any single line goes paid.
```

Always search for current pricing before filling in this table.

---

## E7 — Multi-Language Brain Dump Support (Stage 1)

**Step 1:** Detect language of incoming Brain Dump.
**Step 2:** If non-English, note language and process signal extraction in English.
**Step 3:** Prepend a single language-preference line to the top of the Q1–Q9 message:
> "Your idea is in [Arabic / French / German / Spanish / other] — should I deliver all outputs in [that language] or in English?"

This is sent in the SAME message as the 9 questions — not a separate round-trip.
Wait for all 9 answers + language preference together before producing Stage 1 output.

**Step 4:** Deliver all customer-facing pipeline outputs in the confirmed language.
Internal processing (logic definitions, code, stack decisions) stays in English.

**Language handling notes:**
- Arabic: use RTL layout recommendations in Stage 10 UI output
- French/German/Spanish: adjust SEO keyword research to target-language terms in Stage 4
- Any language: competitor search queries in Stage 4 should also run in the target language
