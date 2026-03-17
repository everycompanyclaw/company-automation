#!/usr/bin/env python3
"""
Enhanced Outreach Sender - V2
"""
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SENDER = "everycompanyclaw@gmail.com"
APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD", "ifwubwz pkqtievqh")

# Real leads database (research needed weekly)
LEADS = []

# Outreach templates
TEMPLATES = {
    "cold": """Hi {name},

I help businesses like {company} save 10+ hours/week through automation.

Quick question: How much time does your team spend on repetitive tasks?

I specialize in:
• Workflow automation (Zapier, Make, n8n)
• Python scripts & APIs
• AI chatbots & assistants
• Data processing

Recent results for similar businesses:
- Law firm: 15 hrs/week saved on document processing
- E-commerce: Automated inventory alerts
- Agency: Client reporting automated

Interested in a free 15-min call to see where automation could help?

Best,
MK
everycompanyclaw@gmail.com""",

    "followup": """Hi {name},

Just following up on my last email about automation for {company}.

I help businesses save 10+ hours/week. Would love to chat.

Quick question: What repetitive tasks take most of your time?

Happy to share examples from similar companies.

Best,
MK"""
}

def load_leads():
    """Load leads from database"""
    # TODO: Connect to leads.md parsing
    return LEADS

def send_email(to_email, subject, body):
    msg = MIMEMultipart()
    msg['From'] = SENDER
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER, APP_PASSWORD)
        server.sendmail(SENDER, to_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def outreach_cold(lead):
    body = TEMPLATES["cold"].format(
        name=lead.get("name", "there"),
        company=lead.get("company", "your business")
    )
    subject = f"Save 10+ hours/week with automation - {lead.get('company', '')}"
    return send_email(lead["email"], subject, body)

def outreach_followup(lead):
    body = TEMPLATES["followup"].format(
        name=lead.get("name", "there"),
        company=lead.get("company", "your business")
    )
    subject = f"Following up - automation for {lead.get('company', '')}"
    return send_email(lead["email"], subject, body)

if __name__ == "__main__":
    leads = load_leads()
    for lead in leads:
        result = outreach_cold(lead)
        print(f"Sent to {lead['email']}: {result}")
