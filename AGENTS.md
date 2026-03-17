# MK's AI Company - Agent Team

## Company Structure

Each agent has a specific role and can be spawned when needed.

---

## 🤖 Agent Roles

### 1. CEO Agent (Strategy)
- **Task:** High-level planning, business decisions
- **When:** Long-term strategy, major decisions
- **Model:** Opus

### 2. Sales Agent (Lead Generation)
- **Task:** Find leads, outreach, follow-ups
- **When:** Lead generation, cold outreach
- **Model:** Claude Code

### 3. Developer Agent (Build)
- **Task:** Code, automation, technical work
- **When:** Building, coding, technical tasks
- **Model:** Claude Code

### 4. Support Agent (Customer Service)
- **Task:** Respond to inquiries, FAQ
- **When:** Customer questions, basic support
- **Model:** MiniMax (fast, cheap)

### 5. Analyst Agent (Research)
- **Task:** Research, data analysis, reports
- **When:** Market research, financial analysis
- **Model:** Opus

### 6. Operations Agent (Admin)
- **Task:** Scheduling, reminders, routine tasks
- **When:** Automation, cron jobs, reminders
- **Model:** MiniMax

---

## How to Use

| Task Type | Spawn Agent |
|-----------|-----------|
| Strategy decisions | CEO Agent |
| Find customers | Sales Agent |
| Build something | Developer Agent |
| Answer questions | Support Agent |
| Research/Analysis | Analyst Agent |
| Routine tasks | Operations Agent |

---

## Automation Flow

1. **Lead comes in** → Support Agent responds
2. **Qualified** → Sales Agent follows up
3. **Deal closed** → Developer Agent builds
4. **Ongoing** → Operations Agent manages

---

## Files

- `agents.py` - Agent spawning system
- `workflows.py` - Automation flows
- `skills/` - Each agent's skills
