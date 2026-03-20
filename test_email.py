#!/usr/bin/env python3
"""
Email Sender - Uses Gmail App Password
"""
import smtplib
from email.mime.text import MIMEText
import sys

EMAIL = "everycompanyclaw@gmail.com"
PASSWORD = "ifwubwz pkqtievqh"  # App Password
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

def send_email(to, subject, body):
    """Send email"""
    msg = MIMEText(body, 'plain')
    msg['From'] = EMAIL
    msg['To'] = to
    msg['Subject'] = subject
    
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL, PASSWORD)
        server.sendmail(EMAIL, to, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

# Test
if __name__ == "__main__":
    print("Testing email...")
    
    # Test send to self
    test_result = send_email(
        to="everycompanyclaw@gmail.com",
        subject="Test from Company",
        body="Testing email system!"
    )
    
    if test_result:
        print("✅ Email sent successfully!")
    else:
        print("❌ Email failed")
        sys.exit(1)
