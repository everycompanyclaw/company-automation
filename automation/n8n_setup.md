# n8n Setup Guide

## Option 1: Run n8n Locally

```bash
# Install n8n
npm install -g n8n

# Start n8n
n8n start
```

Then open http://localhost:5678

## Option 2: n8n.cloud (Easier)

1. Go to https://n8n.io/
2. Sign up for free account
3. Create new workflow

## Option 3: Make.com (No-Code)

1. Go to https://make.com
2. Sign up free
3. Create scenario: Schedule → Telegram

---

## Quick: Telegram Auto-Post (Already Working!)

Since we're on Telegram, I can auto-send posts here:

**Every 6 hours → Post content to Telegram → You copy to IG/Threads**

```json
{
  "name": "Social Content Scheduler",
  "nodes": [
    {
      "name": "Schedule",
      "type": "scheduleTrigger",
      "parameters": {"interval": {"hours": 6}}
    },
    {
      "name": "Send to Telegram",
      "type": "telegram",
      "parameters": {"chatId": "96691420", "text": "{{$json.post}}"}
    }
  ]
}
```

---

## Want Me To:

1. Set up n8n on your machine?
2. Create a Make.com scenario?
3. Keep auto-sending content to Telegram here?
