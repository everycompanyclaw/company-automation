#!/usr/bin/env python3
"""
Outreach Sender - Sends emails to potential clients
"""
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SENDER = "everycompanyclaw@gmail.com"
APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD", "ifwubwz pkqtievqh")

# Sample leads (in production, these would come from research)
LEADS = [
    {"name": "John", "email": "john@startup.com", "company": "TechStartup"},
    {"name": "Sarah", "email": "sarah@smallbiz.com", "company": "SmallBiz Solutions"},
]

def send_outreach(lead):
    subject = f"Save 10+ hours/week with automation - {lead['company']}"
    body = f"""Hi {lead['name']},

I help small businesses save time through automation.

Quick question: How many hours do you spend on repetitive tasks each week?

I specialize in:
- Workflow automation
- Python scripts
- API integrations
- AI assistance

Most clients save 10+ hours per week. Would love to chat about how I can help {lead['company']}.

Best,
MK
everycompanyclaw@gmail.com"""
    
    msg = MIMEMultipart()
    msg['From'] = SENDER
    msg['To'] = lead['email']
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER, APP_PASSWORD)
        server.sendmail(SENDER, lead['email'], msg.as_string())
        server.quit()
        return {"success": True, "email": lead['email']}
    except Exception as e:
        return {"success": False, "email": lead['email'], "error": str(e)}

if __name__ == "__main__":
    for lead in LEADS:
        result = send_outreach(lead)
        print(result)
