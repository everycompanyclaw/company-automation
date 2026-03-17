#!/usr/bin/env python3
"""
Gmail Sender for Company
"""
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SENDER = "everycompanyclaw@gmail.com"
APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD", "")

def send_email(recipient, subject, body):
    if not APP_PASSWORD:
        return {"error": "No GMAIL_APP_PASSWORD set"}
    
    msg = MIMEMultipart()
    msg['From'] = SENDER
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER, APP_PASSWORD)
        server.sendmail(SENDER, recipient, msg.as_string())
        server.quit()
        return {"success": True}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 4:
        print("Usage: gmail_send.py <to> <subject> <body>")
        sys.exit(1)
    
    result = send_email(sys.argv[1], sys.argv[2], sys.argv[3])
    print(result)
