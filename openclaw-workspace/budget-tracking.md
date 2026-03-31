# EveryCompanyClaw — Budget & Token Tracking

## Philosophy

Token spend = company fuel. Track it like cash flow. Every dollar should have a purpose.

---

## Budget Structure

| Budget Item | Monthly Cap | Current Spend | Status |
|-------------|-------------|---------------|--------|
| **Total Company** | TBD (MK to set) | — | ⏳ Awaiting budget |
| Inference / Model calls | — | tracked per-agent | tracked |
| Tools / APIs | — | per service | tracked |
| External services | — | per vendor | tracked |

---

## Tracking Approach

### Per-Period Budget
- **Period:** Monthly (reset on 1st of each month)
- **Cap:** Set by CEO before operations begin
- **Alert threshold:** 80% — notify CEO
- **Hard limit:** 100% — pause non-essential work

### Per-Agent Spend
Each agent tracks its own token consumption:
- CTO / EveryCompanyClaw — internal reasoning
- Engineer agents — coding tasks
- Marketing agents — content generation
- QA agents — testing / browsing

---

## Token Spend Dashboard

```
┌─────────────────────────────────────────────┐
│ EveryCompanyClaw — Token Budget Dashboard  │
├─────────────────────────────────────────────┤
│ Period: 2026-03 (March)                   │
│ Total budget: $TBD                          │
│ Spent: $0.00                                │
│ Remaining: $TBD                             │
│ Status: 🟡 Not yet active                  │
└─────────────────────────────────────────────┘
```

---

## Spend Categories

| Category | Examples | Typical Model |
|----------|----------|---------------|
| Coding | Code generation, debugging, PRs | Claude Opus / Cursor |
| Content | Blog posts, copy, social | MiniMax / GPT |
| Research | Web search, data gathering | MiniMax web search |
| QA | Browser testing, screenshots | Claude + browser skill |
| Planning | Strategy, roadmapping, docs | EveryCompanyClaw |

---

## Cost Optimization Rules

1. **Use the right model for the task** — don't use Opus for simple copy
2. **Batch where possible** — group similar tasks to reduce context overhead
3. **Free first** — check if free-tier models can handle a task
4. **Review before spend** — ask "is this worth the tokens?"
5. **Set per-task limits** — max tokens per issue to prevent runaway spend

---

## Budget Decisions (Escalation Required)

- Any single purchase > $X (MK to define threshold)
- New external service subscription
- Increase to monthly cap
- Spending on behalf of company (contracts, tools)

---

## Reporting

- Daily token spend logged in `memory/daily/YYYY-MM-DD.md`
- Weekly token report in Monday digest
- Monthly close-out report

---

## Next Steps

1. MK sets initial monthly token budget
2. Configure OpenClaw to track spend (if available)
3. Set up alert at 80% threshold
