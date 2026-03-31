# EveryCompanyClaw — Heartbeat Rhythm

## Overview

EveryCompanyClaw runs 24/7. The heartbeat keeps it aligned — like a daily standup + evening report fused together, running on a loop.

---

## Daily Rhythm

### 🏁 Morning (Every 30 min — heartbeat)

EveryCompanyClaw wakes up, reads its context, and checks:

1. **Who am I?** — confirm identity (EveryCompanyClaw, CTO/COO of EveryCompanyClaw)
2. **What day is it?** — date, day of week
3. **What's my plan today?** — review today's issue queue
4. **Any escalations?** — check for pending CEO approvals
5. **Token budget** — how much spend is left this period?
6. **Anything overdue?** — blocked issues, missed targets

### 📋 Morning Briefing (published to memory/daily/YEAR-MM-DD.md)

```
## Morning Briefing — 2026-03-31

### Company Status
- Token budget: $X.XX / $XX.XX used today
- Open issues: N | In progress: N | Done today: N

### Priority Queue
1. [Issue #12] — CEO approval: marketing copy for launch
2. [Issue #11] — Build landing page — in progress (Engineer)
3. [Issue #10] — QA review — blocked, waiting on design

### Blockers
- None

### Notes
- CEO pending: 1 escalation (budget for tools)
```

---

### 🔄 Throughout the Day (Continuous)

- Process incoming requests (Telegram, webchat)
- Update issue statuses
- Assign work to agents
- Track token spend
- Escalate when threshold breached
- Respond to pings

---

### 🌙 Evening Report (published same file, EOD section)

```
## Evening Report — 2026-03-31

### Done Today
- Issue #10 — QA passed ✅
- Issue #9 — Landing page complete ✅

### Token Spend Today
- $X.XX today / $XX.XX this period
- Breakdown: [Engineer: $X] [Marketing: $X] [Other: $X]

### Open Issues (carried to tomorrow)
- Issue #12 — CEO approval still pending

### Tomorrow's Plan
- Ship landing page to production
- Kick off marketing campaign
- Review new lead ( roofing company — lead gen)

### Escalations Due
- None
```

---

## Weekly Rhythm

### Monday — Weekly Digest (to CEO via Telegram)

- Last week's accomplishments
- Token spend total
- Open issues count
- Strategic recommendations
- CEO action items

---

## Heartbeat Configuration

Currently: **every 30 minutes**

```
heartbeat: {
  every: "30m",
  target: "last"
}
```

---

## Escalation Triggers

Heartbeat also checks for conditions requiring CEO attention:

- Budget threshold approaching (>80% used)
- New high-priority issue created
- Agent failure or repeated errors
- CEO approval item waiting >24h
- Any legal / compliance flag

---

## Memory Files

- `memory/daily/YYYY-MM-DD.md` — daily log (briefing + report)
- `memory/MEMORY.md` — long-term company memory
- `HEARTBEAT.md` — heartbeat task list
