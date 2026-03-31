# COMPANY.md - EveryCompanyClaw

## Company Status: 🚀 Live Operations

**Last Updated:** 2026-03-31

## Vision

> "There's an AI company that runs completely by itself. It just... works."
> — EveryCompanyClaw

## Founding

**Founded:** 2026-03-17
**GitHub:** github.com/everycompanyclaw/company-automation

## Products & Services

| Product | Price | Status |
|---------|-------|--------|
| Python Scripts Bundle | $79 | ✅ Live |
| Zapier Templates | $49 | ✅ Live |
| AI Prompts Library | $29 | ✅ Live |

## Agent Team

| Agent | Role | Status |
|-------|------|--------|
| CEO (MK) | Strategy, approvals | Active |
| EveryCompanyClaw | CTO/Operator (OpenClaw) | Active |
| DevAgent | Engineer (gh issues poller) | Active |

## How Work Flows

```
MK (CEO) → creates GitHub issue
    → assigns to everycompanyclaw
    → DevAgent polls every 15 min (cron)
    → works the task
    → closes issue
    → reports back
```

## GitHub Issues

github.com/everycompanyclaw/company-automation/issues

DevAgent checks every 15 min for assigned open issues.

## Current Phase: Growth

- First 10 customers
- Product Hunt launch
- $1000 first revenue

## Social Pipeline (MiniMax-powered) ✅

- **MiniMax API key:** Configured ✅
- **content_generator.py:** AI generates Instagram (Cantonese) + Threads (English) posts
- **auto_post_to_social.py:** Playwright posts to IG + Threads every 6 hours
- **social_pipeline.sh:** generate → post, every 6 hours via cron
- **Cron:** `0 */6 * * *`

First real AI-generated post: Cantonese Instagram caption about AI automation for startups.

## Pending

- [ ] Set token budget
- [ ] Product Hunt launch
- [ ] First customers
- [ ] MiniMax API key

## Key Docs

- `memory/MEMORY.md` — long-term memory
- `memory/org-chart.md` — roles
- `memory/operations-handbook.md` — workflow (GitHub issues)
- `memory/heartbeat-rhythm.md` — daily cadence
- `memory/budget-tracking.md` — token budget
- `memory/daily/2026-03-31.md` — today log
