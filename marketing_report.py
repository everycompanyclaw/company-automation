#!/usr/bin/env python3
"""
Detailed Marketing Report - Specific Targets
Sends daily to Telegram
"""
import os
import json
from datetime import datetime

BOTS = {
    "company": "8689117372:AAHWWbJqpIazdy1TxCOxFbJs1YrofmAGfVw",
    "notify": "8677779317:AAEaxRQmEpymFeer0sVPXe1YNMUqcURZACg"
}

STATE_FILE = "/tmp/learn_state.json"

def send_msg(bot, chat_id, text):
    import requests
    try:
        requests.post(f"https://api.telegram.org/bot{BOTS[bot]}/sendMessage",
                      json={"chat_id": chat_id, "text": text, "parse_mode": "HTML"}, timeout=10)
    except:
        pass

def get_marketing_report():
    """Generate detailed marketing report with specific targets"""
    try:
        with open(STATE_FILE, "r") as f:
            state = json.load(f)
    except:
        state = {"topics_done": [], "actions_done": []}
    
    topics = state.get("topics_done", [])
    actions = state.get("actions_done", [])
    
    # SPECIFIC TARGETS - Who exactly to reach
    targets = """
🎯 <b>SPECIFIC TARGETS - WHO TO REACH</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

<b>By Platform:</b>

<b>LinkedIn:</b>
• Startup founders in automation groups
• CTOs needing AI solutions
• Marketing managers
• Operations leads
Search: "automation startup", "AI integration", "workflow"

<b>Twitter/X:</b>
• @indiehackers members
• @producthunt makers
• Tech founders
• Solopreneurs
Engage with: automation, no-code, tools

<b>Reddit:</b>
• r/automation
• r/python
• r/indiehackers
• r/smallbusiness
• r/freelance

<b>Upwork/Fiverr:</b>
• Post "I help automate workflows"
• Bid on: Python automation, Zapier, n8n
• Keywords: workflow automation, API integration

<b>Facebook Groups:</b>
• Small Business Owners
• Startup Founders
• Digital Marketing

<b>Specific Companies to Research:</b>
• Small agencies needing automation
• Local businesses (dentists, restaurants, shops)
• E-commerce stores
• Consultants

<b>Ideal Customer Profile:</b>
• Revenue: $50K-$2M/year
• Team: 2-20 people
• Problem: Manual processes waste 5+ hours/week
• Budget: Can afford $29-$79 for automation tools
"""
    
    # HOW TO REACH - Specific actions
    how_to = """
📣 <b>HOW TO REACH THEM</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

<b>LinkedIn:</b>
1. Connect with 10 people/day in target group
2. Comment on their posts (valuable insights)
3. Send DM: "Saw your post about X, I help automate that"
4. Share case studies as posts

<b>Twitter:</b>
1. Reply to relevant tweets with tips
2. Quote tweet with tool mentions
3. DM founders offering free audit
4. Join Twitter Spaces

<b>Reddit:</b>
1. Answer questions in automation subreddits
2. Include case study in answers
3. No spam - be genuinely helpful

<b>Email:</b>
1. Find contact info via Apollo.io
2. Cold email: "Help companies like yours save 10 hours/week"
3. Follow up 3 times

<b>Outreach Script:</b>
"Hi [Name], I noticed [specific thing about their business] and thought you might be spending time on [manual task]. We help [similar companies] automate this and save 10+ hours/week. Would you be open to a 5-min chat?"
"""
    
    # CONTENT TO CREATE
    content = """
📝 <b>CONTENT TO CREATE</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

<b>This Week:</b>
1. LinkedIn post: "3 automations that saved me 10 hours"
2. Twitter thread: How to automate X
3. Blog: Python vs Zapier for small business
4. Case study: How [client] saved $X

<b>Topics That Work:</b>
• "I built a bot that does X"
• "How to automate Y in 10 minutes"
• "Stop doing Z manually"
• "Before/after automation"

<b>Hashtags:</b>
#automation #python #startup #indiehackers #buildinpublic #productivity #AI #nocode
"""
    
    # Funnel
    funnel = """
🔻 <b>CONVERSION PATH</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Step 1: Follow on social
↓ (free)
Step 2: Download free guide
↓ (email capture)
Step 3: Newsletter signup
↓ (nurture)
Step 4: Buy $29 product
↓ (trust)
Step 5: Buy $79 bundle
↓ (upsell)
Step 6: Refer others
"""
    
    # Products
    products = """
💰 <b>PRODUCTS TO SELL</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

<b>Entry: $29</b>
• AI Prompts Library
• Quick wins, low commitment

<b>Core: $49</b>
• Zapier Templates
• Ready-to-use workflows

<b>Premium: $79</b>
• Python Scripts Bundle
• Custom automation solutions
"""
    
    # Today's learning
    recent_topics = topics[-5:] if topics else ["None yet"]
    recent_actions = actions[-10:] if actions else ["None yet"]
    
    actions_today = f"""
⚡ <b>ACTIONS TAKEN</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    for t in recent_topics:
        actions_today += f"• Learn: {t}\n"
    for a in recent_actions:
        actions_today += f"• Do: {a}\n"
    
    report = f"""📊 <b>MARKETING REPORT - {datetime.now().strftime('%Y-%m-%d')}</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{targets}

{how_to}

{content}

{funnel}

{products}

{actions_today}

<b>Website:</b> everycompanyclaw.github.io/company-automation/

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    
    return report

def main():
    report = get_marketing_report()
    print(report)
    send_msg("company", "96691420", report)
    print("\nReport sent!")

if __name__ == "__main__":
    main()
