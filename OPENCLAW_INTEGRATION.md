# OpenClaw Integration — EveryCompanyClaw

## Overview

As of 2026-03-31, EveryCompanyClaw has been integrated with OpenClaw for 24/7 autonomous operations.

## Architecture

```
MK (CEO / Board)
    │
    ├── OpenClaw (company operator agent — port 18789)
    │       │
    │       └── EveryCompanyClaw (CTO/COO)
    │               ├── Spawns DevAgent subagents
    │               ├── Runs 24/7 via heartbeat (every 30 min)
    │               └── Manages company memory and decisions
    │
    └── Paperclip (company orchestration — port 3100)
            ├── Issues: EVE-1, EVE-2, ...
            ├── EveryCompanyClaw (CTO agent) — connected via openclaw_gateway
            └── DevAgent (engineer) — connected via openclaw_gateway, polls every 15 min
```

## What's Running

| Component | Status | Location |
|----------|--------|----------|
| OpenClaw gateway | ✅ Active | ws://127.0.0.1:18789 |
| Paperclip server | ✅ Active | http://127.0.0.1:3100 |
| EveryCompanyClaw agent | ✅ Active | CTO role |
| DevAgent | ✅ Active | Engineer, cron-poll |
| GitHub sync | ✅ Ready | everycompanyclaw/company-automation |

## Issue System

Paperclip manages all company work as issues with IDs (EVE-1, EVE-2, etc.).

Issue states: `backlog` → `todo` → `in_progress` → `in_review` → `done`

DevAgent polls Paperclip every 15 minutes and picks up assigned issues automatically.

## Company Memory

All company memory, docs, and logs live in: `~/.openclaw/company/`

- `MEMORY.md` — long-term company memory
- `COMPANY.md` — current company state
- `memory/daily/YYYY-MM-DD.md` — daily logs
- `memory/org-chart.md` — roles
- `memory/operations-handbook.md` — workflow
- `memory/heartbeat-rhythm.md` — daily cadence
- `memory/budget-tracking.md` — token budget

## DevAgent Workflow

1. Paperclip issue created + assigned to DevAgent
2. Cron fires every 15 min → DevAgent subagent wakes
3. DevAgent checks: `GET /api/companies/{id}/issues?assigneeId={agentId}&status=todo`
4. Claims issue: `PATCH status=in_progress`
5. Does the work
6. Marks done: `PATCH status=done`
7. Reports back

## Next Steps

- [ ] Set token budget (MK to define monthly cap)
- [ ] Define first real project for DevAgent
- [ ] MiniMax API key for web_search + understand_image
- [ ] Push OpenClaw workspace docs to GitHub
- [ ] Product Hunt launch submission
