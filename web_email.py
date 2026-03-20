#!/usr/bin/env python3
"""
Email via Web API - No installation needed
Uses web-based email APIs
"""
import requests

# Option 1: Resend (free tier) - No install needed
RESEND_API_KEY = ""  # User needs to get from resend.com

# Option 2: Create mailto links (works instantly)
def create_mailto_link(to, subject, body):
    import urllib.parse
    subject = urllib.parse.quote(subject)
    body = urllib.parse.quote(body)
    return f"mailto:{to}?subject={subject}&body={body}"

# Option 3: Use Gmail web via automation
def send_via_gmail_web():
    """Opens Gmail with compose window"""
    import subprocess
    
    # Create mailto link and open
    link = create_mailto_link(
        to="customer@example.com",
        subject="Your Order",
        body="Thank you for your purchase!"
    )
    
    # Open Gmail with compose
    subprocess.run(["open", f"https://mail.google.com/mail/?view=cm&fs=1&to=customer@example.com&su=Subject&body=Body"])

# Test with Resend (need API key)
def send_resend(to_email, subject, body):
    """Send email via Resend API - no SMTP needed"""
    api_key = os.environ.get("RESEND_API_KEY", "")
    
    if not api_key:
        return {"error": "Need RESEND_API_KEY"}
    
    response = requests.post(
        "https://api.resend.com/emails",
        {
            "from": "EveryCompanyClaw <onboarding@resend.dev>",
            "to": [to_email],
            "subject": subject,
            "text": body
        },
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    )
    
    return response.json()

print("""
📧 Email Solutions (No Installation)
====================================

1. ✅ Gmail - Already configured (need App Password)
2. ✅ Resend - Free API (need API key from resend.com)
3. ✅ mailto: links - Work instantly!

For Resend:
1. Go to: https://resend.com
2. Sign up free
3. Get API key: https://resend.com/api-keys
4. Give me the API key

For Gmail:
1. Use App Password (no 2FA needed on company account)

Or use mailto: links instantly!
""")
