#!/usr/bin/env python3
"""
Simple SMTP Server - Fixed for Python 3.11
"""
import smtpd
import asyncore

class EmailServer(smtpd.SMTPServer):
    def process_message(self, peer, mailfrom, rcpttos, data):
        print(f"📧 Email: {mailfrom} → {rcpttos}")

print("Starting SMTP server on port 1025...")
server = EmailServer(('0.0.0.0', 1025), None)
asyncore.loop()
