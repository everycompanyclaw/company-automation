#!/usr/bin/env python3
"""
Alternative Email Solutions - No Proton Bridge Needed
"""
import subprocess

# Option 1: Gmail with App Password (free)
GMAIL_SMTP = {
    "host": "smtp.gmail.com",
    "port": 587,
    "user": "everycompanyclaw@gmail.com",
    "note": "Use App Password instead of login password"
}

# Option 2: SendGrid (free tier)
SENDGRID = {
    "host": "smtp.sendgrid.net",
    "port": 587,
    "user": "apikey",
    "note": "Get free API key from sendgrid.com"
}

# Option 3: Mailgun (free tier)
MAILGUN = {
    "host": "smtp.mailgun.org",
    "port": 587,
    "user": "postmaster@yourdomain.com",
    "note": "Need domain for Mailgun"
}

# Option 4: Ethereal (testing)
ETHEREAL = {
    "host": "smtp.ethereal.email",
    "port": 587,
    "user": "generate@ethereal.email",
    "note": "Free testing emails"
}

def setup_gmail():
    """Use Gmail with existing credentials"""
    print("""
📧 Option: Gmail SMTP
====================

Current: everycompanyclaw@gmail.com

To use:
1. Enable 2-Factor Authentication on Gmail
2. Go to: https://myaccount.google.com/apppasswords
3. Create app password for "Mail"
4. Use that 16-char password as SMTP password

SMTP Settings:
- Host: smtp.gmail.com
- Port: 587 (TLS) or 465 (SSL)
- Username: everycompanyclaw@gmail.com
- Password: [App Password]

We have credentials ready in the system!
""")

def setup_sendgrid():
    """Set up SendGrid"""
    print("""
📧 Option: SendGrid (Free)
=======================

1. Go to: https://sendgrid.com/free/
2. Sign up free
3. Go to: Settings → API Keys
4. Create API Key
5. Use as SMTP password

SMTP:
- Host: smtp.sendgrid.net
- Port: 587
- Username: apikey
- Password: [Your API Key]
""")

def test_current_email():
    """Test current Gmail setup"""
    print("Testing current email setup...")
    
    import smtplib
    from email.mime.text import MIMEText
    
    # Current settings
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    username = "everycompanyclaw@gmail.com"
    password = "ifwubwz pkqtievqh"  # From earlier
    
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(username, password)
        print("✅ Gmail SMTP works!")
        server.quit()
        return True
    except Exception as e:
        print(f"❌ Gmail SMTP failed: {e}")
        return False

print("""
📧 Email Options for Company
=========================

1. Gmail (current) - Already configured!
2. SendGrid - Free tier
3. Proton - Needs Bridge

Let me test Gmail...
""")

test_current_email()
