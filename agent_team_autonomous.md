# 🤖 AI Agent Team - Self-Operating

## Mission
Autonomously run the company 24/7 with minimal human intervention.

---

## Agent Roles

### 1. Sales Agent 🤖
**Job:** Find leads, send outreach, follow up
**Trigger:** Daily at 9am
**Tools:** Email, outreach scripts

### 2. Support Agent 💬
**Job:** Answer questions, qualify leads
**Trigger:** When someone messages
**Tools:** Auto-responder, knowledge base

### 3. Operations Agent ⚙️
**Job:** Run cron jobs, process orders
**Trigger:** Scheduled + events
**Tools:** Order handler, cron

### 4. Marketing Agent 📢
**Job:** Post content, engage on social
**Trigger:** Daily at 10am
**Tools:** Social scripts

---

## Daily Schedule (Autonomous)

| Time | Agent | Task |
|------|-------|------|
| 8:00 | Operations | Check for new orders |
| 9:00 | Sales | Send outreach emails |
| 10:00 | Marketing | Post to social |
| 12:00 | Support | Check & respond to messages |
| 14:00 | Operations | Check for new orders |
| 17:00 | Sales | Follow up with leads |
| 20:00 | Operations | Daily report |

---

## Current Status

### Active Agents
- ✅ Sales Agent (ready)
- ✅ Support Agent (ready)
- ✅ Operations Agent (ready)
- 🔄 Marketing Agent (need social accounts)

### What's Working
- Auto-responder answers FAQs
- Order handler processes orders
- Outreach scripts ready

### Need Setup
- [ ] Social media accounts to post from
- [ ] Payment links (waiting on MK)

---

## Commands to Run Agents

```bash
# Run sales agent
python company/outreach_v2.py

# Run operations
python company/automation/order_handler.py

# Check orders
cat company/automation/data/orders.json
```
