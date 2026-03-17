#!/usr/bin/env python3
"""
Worker Agents - Execute tasks
Sales, Support, Operations
"""
import os
import json
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Config
STRIPE_KEY = os.environ.get('STRIPE_SECRET_KEY')
SENDER = "everycompanyclaw@gmail.com"
APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD", "ifwubwz pkqtievqh")

class SalesWorker:
    """Handles sales and outreach"""
    
    def run(self):
        print("💼 Sales worker: Checking leads...")
        # In production: send outreach emails
        return "Sales: Ready to contact leads"

class SupportWorker:
    """Handles customer support"""
    
    def run(self):
        print("💬 Support worker: Checking messages...")
        # In production: check and respond to messages
        return "Support: Ready to help customers"

class OperationsWorker:
    """Handles order processing"""
    
    def run(self):
        print("⚙️ Operations worker: Checking orders...")
        
        if STRIPE_KEY:
            import stripe
            stripe.api_key = STRIPE_KEY
            try:
                charges = stripe.Charge.list(limit=5)
                print(f"   Found {len(charges.data)} recent charges")
            except:
                print("   Stripe check failed")
        
        return "Operations: Order check complete"

def run_worker(role):
    workers = {
        "sales": SalesWorker(),
        "support": SupportWorker(),
        "operations": OperationsWorker()
    }
    
    worker = workers.get(role)
    if worker:
        return worker.run()
    return f"Unknown role: {role}"

if __name__ == "__main__":
    import sys
    role = sys.argv[1] if len(sys.argv) > 1 else "operations"
    result = run_worker(role)
    print(result)
