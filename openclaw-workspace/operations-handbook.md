# Operations — Without Paperclip

## Issue System: GitHub Issues

All work tracked as GitHub Issues in `everycompanyclaw/company-automation`.

**Issue workflow:**
1. CEO/MK creates issue → assigns to DevAgent (or labels)
2. DevAgent polls GitHub issues every 15 min
3. DevAgent claims issue, works it, closes it

## DevAgent Workflow

**Polling cadence:** every 15 min via cron (isolated subagent)

**Check command:**
```bash
gh issue list --repo everycompanyclaw/company-automation --state open --assignee @me --limit 10
```

**Claim an issue:**
```bash
gh issue edit NUMBER --add-assignee everycompanyclaw
gh issue comment NUMBER --body "Working on it..."
```

**Mark done:**
```bash
gh issue close NUMBER --comment "Completed: [description]"
```

## Status Labels Used

- `todo` — work queued (via label or just open state)
- `in-progress` — DevAgent is working
- `done` — closed
- `high` / `medium` / `low` — priority

## Issue Creation

Create issues via:
- GitHub web UI
- `gh issue create --repo everycompanyclaw/company-automation --title "..." --body "..."`
- OpenClaw exec

## Cron: DevAgent Poller

Every 15 minutes: `devagent-poller` cron job wakes → checks GitHub → works tasks
