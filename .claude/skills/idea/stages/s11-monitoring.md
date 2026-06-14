# Stage 11 — Observability + Monitoring Plan
Layer: Build (new)

## ⚠ CRITICAL PRE-CONDITION — READ BEFORE ANYTHING ELSE
**Uptime Kuma MUST be deployed on a SEPARATE Ubuntu VPS from the main app.**
If the app goes down and takes the monitor with it, alerts never fire.
The monitoring server must be independent of the infrastructure it monitors.
This is non-negotiable. Do not proceed if this constraint cannot be met.

## Purpose
Define the full observability stack before the project goes live.
AI-operated projects with no monitoring are blind. Silent failures are unfixable.
All components: self-hostable on Ubuntu, free, AI-configurable.

## Search before recommending
Verify current versions of all monitoring tools before output.

## Recommended stack (search-verified)
- **Uptime Kuma** — uptime monitoring, 90+ alert channels, status page
  ⚠ Deploy on a SEPARATE Ubuntu VPS from the main app.
  If app goes down and takes the monitor with it, alerts never fire.
- **Umami or Plausible (self-hosted)** — privacy-first analytics, zero cost
- **OpenTelemetry SDK** — instrumentation; pipes to any backend
- For larger projects: Grafana + Loki (logs + metrics)

## Adaptive questions (2 max — ask only if not answerable from prior stages)

```
Q1. How do you want to be alerted when something goes down?

  A. Telegram message  ← I'd go with this — instant, free, works on mobile
  B. Email
  C. Slack
  D. SMS (paid)
  E. Something else — tell me

Q2. What is the longest the product can be down before you need to know?

  A. 1 minute — critical, alert immediately
  B. 5 minutes  ← recommended default for most MVPs
  C. 15 minutes — lower priority, catch-up is fine
  D. Only alert if down more than 30 minutes
  E. Something else — tell me
```

Wait for answers before writing the monitoring plan. If already answered in prior stages, skip and proceed directly to output.

## Output
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OBSERVABILITY + MONITORING PLAN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## Uptime monitoring
  Tool: Uptime Kuma [search-verified version]
  Server: separate Ubuntu VPS (not same as app)
  Checks: [every endpoint, API, service]
  Alerts: [operator's channels]
  Interval: 60s default, 20s for critical

## Analytics
  Tool: [Umami/Plausible self-hosted — version verified]
  Events tracked: [key user actions beyond page views]

## Error tracking
  Tool: [Sentry self-hosted free OR OpenTelemetry → file logger]
  Captures: [unhandled exceptions, API errors, 5xx responses]
  Threshold: [>5 errors/min → notify operator]

## AI agent decision log
  Path: /var/log/agent-actions/YYYY-MM-DD.md
  Format: timestamp · action · outcome · cost-impact
  Review: operator reviews weekly summary

## Cost monitoring
  Trigger: service approaches paid tier → immediate operator notification
  Method: cron on Ubuntu checking usage APIs daily

## Incident response (AI-automated)
  IF uptime fails > 5min → AI agent auto-restart
  IF auto-restart fails → notify operator immediately
  IF SEO score drops > 10pts → AI agent runs audit + files issue
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Gate → `stages/s12-maintenance.md`
