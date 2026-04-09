#!/usr/bin/env python3
"""
Email Manager - EveryCompanyClaw
Clean, organized email system
"""

import smtplib
import json
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Config
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL = "everycompanyclaw@gmail.com"
PASSWORD = "ifwubwz pkqtievqh"

SENT_EMAILS_FILE = "/tmp/company-automation/sent_emails.json"
TEMPLATES_FILE = "/tmp/company-automation/email_templates.json"

DEFAULT_TEMPLATES = {
    "intro": {
        "subject": "👋 Automation tools for {company}?",
        "body": """Hi {name},

I came across {company} and thought our automation tools might help.

EveryCompanyClaw builds AI-powered tools for founders and small businesses:

🤖 Python Scripts Bundle — $79
50+ battle-tested scripts for automation

⚡ Zapier Templates — $49
25+ workflows to automate repetitive tasks

💡 AI Prompts Library — $29
200+ curated prompts for AI assistants

Used to run our own company 24/7.

Worth a look?

Best,
EveryCompanyClaw Team
🤖 AI-Powered Company"""
    },
    "followup": {
        "subject": "Following up — automation tools",
        "body": """Hi {name},

Just following up on our automation tools. Happy to answer any questions.

Cheers,
EveryCompanyClaw Team
🤖 AI-Powered Company"""
    },
    "launch": {
        "subject": "🚀 EveryCompanyClaw Launch — 40% Off Today Only",
        "body": """Hi {name},

We're LIVE today with 3 automation products:

🐍 Python Scripts Bundle
$79 (was $129) — 50+ production-ready scripts

⚡ Zapier Templates
$49 (was $79) — 25+ proven workflows

💡 AI Prompts Library
$29 (was $49) — 200+ curated prompts

Launch offer ends April 10.

🚀 Launch page: everycompanyclaw.com/launch

Cheers,
EveryCompanyClaw Team
🤖 AI-Powered Company"""
    }
}

def load_templates():
    if os.path.exists(TEMPLATES_FILE):
        with open(TEMPLATES_FILE) as f:
            return json.load(f)
    return DEFAULT_TEMPLATES

def load_sent():
    if os.path.exists(SENT_EMAILS_FILE):
        with open(SENT_EMAILS_FILE) as f:
            return json.load(f)
    return []

def save_sent(emails):
    with open(SENT_EMAILS_FILE, 'w') as f:
        json.dump(emails, f, indent=2)

def send_email(to, subject, body):
    """Send an email"""
    try:
        msg = MIMEMultipart()
        msg['From'] = f"EveryCompanyClaw <{EMAIL}>"
        msg['To'] = to
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL, PASSWORD)
        server.sendmail(EMAIL, to, msg.as_string())
        server.quit()
        
        # Log it
        emails = load_sent()
        emails.append({
            "to": to,
            "subject": subject,
            "date": datetime.now().isoformat(),
            "status": "sent"
        })
        save_sent(emails)
        
        print(f"✅ Sent to {to}")
        return True
    except Exception as e:
        print(f"❌ Failed to send to {to}: {e}")
        return False

def send_template(to, template_name, variables={}):
    """Send a template email"""
    templates = load_templates()
    if template_name not in templates:
        print(f"❌ Template '{template_name}' not found")
        return False
    
    t = templates[template_name]
    subject = t['subject'].format(**variables)
    body = t['body'].format(**variables)
    
    return send_email(to, subject, body)

def show_sent():
    """Show sent email log"""
    emails = load_sent()
    if not emails:
        print("No emails sent yet.")
        return
    
    print(f"\n📧 Sent Emails ({len(emails)} total)\n")
    for e in reversed(emails[-10:]):
        date = e['date'][:10]
        print(f"  {date} | {e['to']} | {e['subject'][:50]}...")

def show_templates():
    """Show available templates"""
    templates = load_templates()
    print("\n📝 Email Templates\n")
    for name, t in templates.items():
        print(f"  [{name}] {t['subject']}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("""
📧 Email Manager - EveryCompanyClaw

Usage:
  python3 email_manager.py send <to> <subject> <body>
  python3 email_manager.py template <to> <template_name> [var1=val1 var2=val2]
  python3 email_manager.py log
  python3 email_manager.py templates

Examples:
  python3 email_manager.py template john@gmail.com intro name=John company=TechCorp
  python3 email_manager.py send mary@startup.com "Subject" "Body text here"
  python3 email_manager.py log
        """)
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "send" and len(sys.argv) >= 5:
        send_email(sys.argv[2], sys.argv[3], sys.argv[4])
    elif cmd == "template" and len(sys.argv) >= 4:
        to = sys.argv[2]
        template_name = sys.argv[3]
        vars_dict = {}
        for arg in sys.argv[4:]:
            if '=' in arg:
                k, v = arg.split('=', 1)
                vars_dict[k] = v
        send_template(to, template_name, vars_dict)
    elif cmd == "log":
        show_sent()
    elif cmd == "templates":
        show_templates()
    else:
        print("Invalid command")
