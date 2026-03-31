# MEMORY.md - EveryCompanyClaw Long-Term Memory

## Company Overview

- **Name:** EveryCompanyClaw 🏢🤖💼
- **Founded:** 2026-03-17
- **Mission:** Build the first fully autonomous AI company that runs itself, generates profit, and becomes known globally
- **Status:** 🚀 Live Operations
- **Website:** everycompanyclaw.github.io/company-automation
- **GitHub:** github.com/everycompanyclaw

## Company Vision

**"The AI Company That Runs Itself"**

## Products & Services

| Product | Price | Status |
|---------|-------|--------|
| Python Scripts Bundle | $79 | ✅ Live |
| Zapier Templates | $49 | ✅ Live |
| AI Prompts Library | $29 | ✅ Live |

## GitHub Repo

**Repo:** `everycompanyclaw/company-automation`
**Issues:** github.com/everycompanyclaw/company-automation/issues

## Architecture

```
MK (CEO / Board)
    │
    └── OpenClaw (gateway — port 18789)
            └── EveryCompanyClaw (CTO/COO)
                    ├── Spawns DevAgent subagents
                    ├── Runs 24/7 via heartbeat (every 30 min)
                    └── DevAgent polls GitHub every 15 min
```

## Issue System: GitHub Issues

All work tracked as GitHub Issues in `everycompanyclaw/company-automation`.

DevAgent workflow:
1. Polls every 15 min via cron (isolated subagent)
2. Checks: `gh issue list --repo everycompanyclaw/company-automation --state open --assignee everycompanyclaw`
3. Claims issue (comments + sets in-progress)
4. Does the work
5. Closes with completion comment

## Active Agents

| Agent | Role | Status |
|-------|------|--------|
| EveryCompanyClaw | CTO/COO (OpenClaw main) | Active |
| DevAgent | Engineer (gh issues poller) | Active |

## Company Stats (as of 2026-03-23)

- Leads: 48 | Pipeline deals: 78 | Actions: 495 | Posts: 3

## Board (MK)

MK provides:
- API keys (when needed)
- Budget decisions
- Strategic direction
- Final approval on major expenditures

MK does NOT run day-to-day operations — that's EveryCompanyClaw's job.

## Pending Items (from Board)

- [ ] Provide MiniMax API key (for web_search + understand_image)
- [ ] Set token budget (monthly cap for AI spend)
- [ ] Approve first major expenditure (if > threshold)
