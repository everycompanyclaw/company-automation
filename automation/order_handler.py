#!/usr/bin/env python3
"""
Order Handler - Processes digital product orders automatically
Runs on cron: checks email for orders, sends products
"""
import os
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Config
SENDER = "everycompanyclaw@gmail.com"
APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD", "ifwubwz pkqtievqh")
ORDERS_FILE = "/Users/macbookpro/.openclaw/workspace/company/automation/data/orders.json"
INBOX_FILE = "/Users/macbookpro/.openclaw/workspace/company/automation/data/inbox.json"

PRODUCTS = {
    "python-scripts": {
        "name": "Python Automation Scripts Bundle",
        "price": 79,
        "files": [
            "/Users/macbookpro/.openclaw/workspace/company/products/python-scripts/bundle.py",
            "/Users/macbookpro/.openclaw/workspace/company/products/python-scripts/README.md"
        ]
    }
}

def load_orders():
    if os.path.exists(ORDERS_FILE):
        with open(ORDERS_FILE) as f:
            return json.load(f)
    return []

def save_orders(orders):
    with open(ORDERS_FILE, "w") as f:
        json.dump(orders, f, indent=2)

def send_product(email, product_id):
    """Send product files to customer"""
    product = PRODUCTS.get(product_id)
    if not product:
        return False
    
    # In production: attach files and send
    # For now: send download links
    body = f"""🎉 Thank you for your order!

Your Product: {product['name']}
Price: ${product['price']}

📥 Download your files:
https://github.com/everycompanyclaw/company-automation/raw/main/products/python-scripts/bundle.py
https://github.com/everycompanyclaw/company-automation/raw/main/products/python-scripts/README.md

Questions? Reply to this email!

Best,
MK Automation
everycompanyclaw@gmail.com"""
    
    msg = MIMEMultipart()
    msg['From'] = SENDER
    msg['To'] = email
    msg['Subject'] = f"🎉 Your {product['name']} - Download Link"
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER, APP_PASSWORD)
        server.sendmail(SENDER, email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def process_order(email, product_id):
    """Process a new order"""
    orders = load_orders()
    
    # Check if already ordered
    for order in orders:
        if order['email'] == email and order['product'] == product_id:
            return {"status": "duplicate", "message": "Already ordered"}
    
    # Send product
    success = send_product(email, product_id)
    
    if success:
        order = {
            "email": email,
            "product": product_id,
            "date": datetime.now().isoformat(),
            "status": "sent"
        }
        orders.append(order)
        save_orders(orders)
        return {"status": "success", "message": "Product sent"}
    
    return {"status": "error", "message": "Failed to send"}

# Manual trigger for testing
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        email = sys.argv[1]
        product = sys.argv[2]
        result = process_order(email, product)
        print(result)
    else:
        print("Usage: order_handler.py <email> <product_id>")
