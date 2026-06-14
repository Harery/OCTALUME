# Stage 12 — AI Maintenance + Upgrade Cycle
Layer: Build (new) | Enhancement: E6 (final cost ledger update)

## Purpose
Define how the AI agent maintains the project post-launch.
Without this, the project becomes unmaintainable within 3–6 months.

## Gotcha
CLAUDE.md tends to grow past 100 lines by this stage.
Enforce curation: delete stale entries, merge similar rules. Hard cap is 100 lines.

## Output
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AI MAINTENANCE + UPGRADE CYCLE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Daily (fully automated)
  - Uptime checks via Uptime Kuma
  - Error log review — flag anomalies
  - AI agent decision log written
  - SEO: check Google Search Console (GSC) for crawl errors

## Weekly (AI executes, operator reviews summary)
  - Dependency vulnerability scan (npm audit / pip-audit)
  - Core Web Vitals check via PageSpeed API
  - SEO ranking check vs prior week
  - Cost ledger review — verify zero-cost baseline
  - CLAUDE.md + MEMORY.md updated with new decisions

## Monthly (AI proposes, operator approves)
  - Dependency upgrades (minor + patch)
  - SEO content gap analysis
  - Analytics review — behaviour patterns, drop-off
  - Stack freshness check — search for successors to any deprecated component

## On trigger (event-driven, AI-autonomous)
  - Security patch released → patch within 24h
  - Uptime incident → auto-restart → escalate if unresolved in 5min
  - SEO rank drop > 10% → audit + action plan to operator
  - Paid tier threshold reached → immediate notification, NO auto-upgrade

## CLAUDE.md / MEMORY.md update protocol (every session end)
  1. Update MEMORY.md with decisions, corrections, patterns
  2. Curate if > 200 lines — merge similar, delete stale
  3. Add new "never do" rules to CLAUDE.md if discovered
  4. Write: /var/log/agent-actions/YYYY-MM-DD.md
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## E6 final cost ledger update
Finalise the cost ledger with all 12 stages' components.
Include scale tiers: @ launch / @ 1k users / @ 10k users.

## Pipeline complete
After approval: generate the final Session Handoff Summary:
```
SESSION HANDOFF — [YYYY-MM-DD]
Project: [name] | Type: [product type]
Last approved: Stage 12 — AI Maintenance + Upgrade Cycle
Pipeline status: COMPLETE — all 12 stages approved
Key decisions log: see MEMORY.md
Cost ledger final: [launch cost / 1k users / 10k users]
Next action: Hand off to Claude Code CLI for build execution
Files ready: CLAUDE.md · MEMORY.md · constitution.md · cost-ledger.md
```
All files ready for Claude Code CLI handoff.
