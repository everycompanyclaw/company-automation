#!/usr/bin/env python3
"""
Resend Email - No installation needed
Just needs API key
"""
import requests

API_KEY = ""  # Set your Resend API key

def send_email(to, subject, body):
    """Send email via Resend"""
    global API_KEY
    
    if not API_KEY:
        return {"error": "No API key. Get free at resend.com"}
    
    response = requests.post(
        "https://api.resend.com/emails",
        {
            "from": "EveryCompanyClaw <onboarding@resend.dev>",
            "to": [to],
            "subject": subject,
            "text": body
        },
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
    )
    
    return response.json()

# Test
print("Resend Email Setup")
print("=" * 40)
print("Get free API key: https://resend.com/api-keys")
print("")
print("Set API key and run:")
print('  RESEND_API_KEY=re_123... python3 send_resend.py')
