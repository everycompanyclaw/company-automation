#!/usr/bin/env python3
# Email Auto-Responder Script
# Price: $49

import imaplib
import email
import smtplib
from email.mime.text import MIMEText

# Configuration
IMAP_SERVER = "imap.gmail.com"
SMTP_SERVER = "smtp.gmail.com"

def check_and_respond():
    # Connect to email
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login("your-email@gmail.com", "your-app-password")
    mail.select("inbox")
    
    # Search for unread emails
    typ, msgs = mail.search(None, 'UNSEEN')
    
    for num in msgs[0].split():
        typ, msg_data = mail.fetch(num, '(RFC822)')
        email_msg = email.message_from_bytes(msg_data[0][1])
        
        # Auto-respond
        subject = email_msg['subject']
        sender = email_msg['from']
        
        response = f"Thanks for your email! I'll get back to you soon."
        
        # Send response
        msg = MIMEText(response)
        msg['To'] = sender
        msg['Subject'] = f"Re: {subject}"
        
        s = smtplib.SMTP(SMTP_SERVER, 587)
        s.starttls()
        s.login("your-email@gmail.com", "your-app-password")
        s.sendmail("your-email@gmail.com", sender, msg.as_string())
        s.quit()
        
        print(f"Auto-responded to {sender}")

if __name__ == "__main__":
    check_and_respond()
