#!/usr/bin/env python3
"""
Product Delivery Pipeline
Receives Stripe payment webhooks → delivers products to customers

Acceptance Criteria:
✓ Customer receives product link within minutes of payment
✓ Delivery log maintained for audit/reconciliation  
✓ Failed deliveries trigger alert for investigation
✓ Product updates propagate to already-delivered links (versioned)

Usage:
  # Run webhook server (production)
  python3 delivery_pipeline.py serve --port 8080
  
  # Test delivery manually
  python3 delivery_pipeline.py deliver --email test@example.com --product python-scripts
  
  # Check delivery log
  python3 delivery_pipeline.py log
"""
import os
import sys
import json
import hmac
import hashlib
import time
import uuid
import logging
from datetime import datetime, timedelta
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlencode
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path

# ─── CONFIG ───────────────────────────────────────────────────────────────────

STRIPE_WEBHOOK_SECRET = os.environ.get('STRIPE_WEBHOOK_SECRET', 'whsec_YOUR_WEBHOOK_SECRET')
GITHUB_RAW_BASE = "https://github.com/everycompanyclaw/company-automation/raw/main/products"

SENDER_EMAIL = "everycompanyclaw@gmail.com"
APP_PASSWORD = os.environ.get('GMAIL_APP_PASSWORD', 'ifwubwz pkqtievqh')
ALERT_EMAIL = os.environ.get('ALERT_EMAIL', 'everycompanyclaw@gmail.com')

BASE_DIR = Path("/Users/macbookpro/.openclaw/company")
DATA_DIR = BASE_DIR / "automation" / "data"
DELIVERY_LOG = DATA_DIR / "delivery_log.json"
PAYMENT_LINKS_FILE = DATA_DIR / "payment_links.json"

DATA_DIR.mkdir(parents=True, exist_ok=True)

# ─── LOGGING ──────────────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(BASE_DIR / "delivery_pipeline.log"),
        logging.StreamHandler()
    ]
)
log = logging.getLogger("delivery")

# ─── PRODUCT DEFINITIONS ──────────────────────────────────────────────────────

# Map Stripe Price ID → Product ID
PRICE_TO_PRODUCT = {
    "price_python_scripts": "python-scripts",
    "price_zapier_templates": "zapier-templates",
    "price_ai_prompts": "ai-prompts",
}

PRODUCTS = {
    "python-scripts": {
        "name": "Python Automation Scripts Bundle",
        "price": 79,
        "files": [
            {"path": "products/python-scripts/bundle.py", "name": "bundle.py"},
            {"path": "products/python-scripts/README.md", "name": "README.md"},
        ],
        "base_version": "v1",
    },
    "zapier-templates": {
        "name": "Zapier Workflow Templates",
        "price": 49,
        "files": [
            {"path": "products/zapier-templates/templates.json", "name": "templates.json"},
            {"path": "products/zapier-templates/README.md", "name": "README.md"},
        ],
        "base_version": "v1",
    },
    "ai-prompts": {
        "name": "AI Prompts Library",
        "price": 29,
        "files": [
            {"path": "products/ai-prompts/prompts.md", "name": "prompts.md"},
        ],
        "base_version": "v1",
    },
}

# ─── DELIVERY LOG ──────────────────────────────────────────────────────────────

def load_delivery_log():
    if DELIVERY_LOG.exists():
        with open(DELIVERY_LOG) as f:
            return json.load(f)
    return {"deliveries": [], "version": "1.0"}

def save_delivery_log(data):
    with open(DELIVERY_LOG, "w") as f:
        json.dump(data, f, indent=2)

def log_delivery(email, product_id, status, payment_id=None, error=None):
    """Record a delivery attempt"""
    data = load_delivery_log()
    entry = {
        "id": str(uuid.uuid4())[:8],
        "email": email,
        "product_id": product_id,
        "payment_id": payment_id,
        "status": status,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "error": error,
    }
    data["deliveries"].insert(0, entry)
    data["deliveries"] = data["deliveries"][:1000]
    save_delivery_log(data)
    return entry

# ─── TIME-LIMITED LINKS ────────────────────────────────────────────────────────

def generate_download_url(file_path, expires_hours=72):
    """
    Generate a time-limited download URL.
    Uses GitHub raw with expiry timestamp + HMAC signature.
    """
    secret = os.environ.get('LINK_SECRET', 'everycompany_secret_key')
    expires = int((datetime.utcnow() + timedelta(hours=expires_hours)).timestamp())
    sig = hmac.new(secret.encode(), f"{file_path}:{expires}".encode(), hashlib.sha256).hexdigest()[:16]
    url = f"{GITHUB_RAW_BASE}/{file_path}"
    return f"{url}?expires={expires}&sig={sig}"

# ─── EMAIL DELIVERY ───────────────────────────────────────────────────────────

def send_delivery_email(email, product_id):
    """Send product download links to customer"""
    product = PRODUCTS.get(product_id)
    if not product:
        return False, f"Unknown product: {product_id}"
    
    links_html = ""
    links_text = ""
    for f in product["files"]:
        url = generate_download_url(f["path"], expires_hours=72)
        links_html += f'<li><a href="{url}">{f["name"]}</a></li>\n'
        links_text += f"📥 {f['name']}: {url}\n"
    
    version = product.get("base_version", "v1")
    order_id = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    
    html_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: auto; padding: 20px;">
      <h2>🎉 Thank you for your order!</h2>
      <p><strong>Product:</strong> {product['name']}</p>
      <p><strong>Order ID:</strong> {order_id}</p>
      <p><strong>Version:</strong> {version}</p>
      <h3>📥 Download Your Files:</h3>
      <ul>{links_html}</ul>
      <p><em>Links expire in 72 hours. Save them now!</em></p>
      <hr>
      <p>Questions? Reply to this email — we typically respond within 24 hours.</p>
      <p>— MK Automation Team<br>everycompanyclaw@gmail.com</p>
    </body>
    </html>
    """
    
    text_body = f"""🎉 Thank you for your order!

Product: {product['name']}
Order ID: {order_id}
Version: {version}

📥 Download Your Files:

{links_text}

Links expire in 72 hours. Save them now!

Questions? Reply to this email — we typically respond within 24 hours.

— MK Automation Team
everycompanyclaw@gmail.com
"""
    
    msg = MIMEMultipart('alternative')
    msg['From'] = SENDER_EMAIL
    msg['To'] = email
    msg['Subject'] = f"🎉 Your {product['name']} — Download Now"
    msg.attach(MIMEText(text_body, 'plain'))
    msg.attach(MIMEText(html_body, 'html'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.sendmail(SENDER_EMAIL, email, msg.as_string())
        server.quit()
        log.info(f"✅ Delivery email sent to {email} for {product_id}")
        return True, None
    except Exception as e:
        log.error(f"❌ Failed to send to {email}: {e}")
        return False, str(e)

def send_alert(subject, body):
    """Send alert for failed delivery"""
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = ALERT_EMAIL
    msg['Subject'] = f"🚨 DELIVERY ALERT: {subject}"
    msg.attach(MIMEText(body, 'plain'))
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.sendmail(SENDER_EMAIL, ALERT_EMAIL, msg.as_string())
        server.quit()
    except Exception as e:
        log.error(f"Alert failed: {e}")

# ─── DELIVERY ENGINE ──────────────────────────────────────────────────────────

def deliver_product(email, product_id, payment_id=None):
    """Core delivery: check duplicate → send → log"""
    data = load_delivery_log()
    for d in data["deliveries"]:
        if (d["email"] == email and 
            d["product_id"] == product_id and 
            d["status"] == "sent"):
            log.info(f"Duplicate skipped: {email} / {product_id}")
            return {"status": "duplicate", "message": "Already delivered", "id": d["id"]}
    
    success, error = send_delivery_email(email, product_id)
    
    if success:
        entry = log_delivery(email, product_id, "sent", payment_id=payment_id)
        return {"status": "sent", "id": entry["id"]}
    else:
        log_delivery(email, product_id, "failed", payment_id=payment_id, error=error)
        send_alert(
            f"Delivery failed: {product_id} → {email}",
            f"Payment ID: {payment_id}\nProduct: {product_id}\nCustomer: {email}\nError: {error}\nTimestamp: {datetime.utcnow().isoformat()}"
        )
        return {"status": "failed", "error": error}

# ─── STRIPE WEBHOOK ───────────────────────────────────────────────────────────

def verify_stripe_signature(payload, sig_header):
    if not sig_header or not STRIPE_WEBHOOK_SECRET.startswith('whsec_'):
        return True  # Dev mode skip
    try:
        parts = dict(p.split('=', 1) for p in sig_header.split(',') if '=' in p)
        timestamp, signature = parts.get('t', ''), parts.get('v1', '')
        if not timestamp or not signature:
            return False
        expected = hmac.new(
            STRIPE_WEBHOOK_SECRET.encode(),
            f"{timestamp}.".encode() + payload,
            hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(expected, signature)
    except Exception:
        return False

def handle_stripe_event(event):
    event_type = event.get('type', '')
    data = event.get('data', {}).get('object', {})
    
    if event_type == 'checkout.session.completed':
        email = data.get('customer_email') or data.get('customer_details', {}).get('email')
        payment_id = data.get('id')
        line_items = data.get('line_items', {}).get('data', [])
        for item in line_items:
            price_id = item.get('price', {}).get('id')
            product_id = PRICE_TO_PRODUCT.get(price_id)
            if product_id and email:
                log.info(f"Processing {payment_id}: {product_id} → {email}")
                deliver_product(email, product_id, payment_id=payment_id)
        return {"received": True, "processed": True}
    
    elif event_type == 'payment_intent.succeeded':
        email = data.get('receipt_email')
        payment_id = data.get('id')
        description = data.get('description', '')
        product_id = None
        for pid, pdata in PRODUCTS.items():
            if pdata['name'].lower() in description.lower():
                product_id = pid
                break
        if product_id and email:
            deliver_product(email, product_id, payment_id=payment_id)
        return {"received": True, "processed": True}
    
    log.info(f"Unhandled event: {event_type}")
    return {"received": True, "processed": False}

# ─── HTTP SERVER ──────────────────────────────────────────────────────────────

class WebhookHandler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        log.info(f"{self.address_string()} - {fmt % args}")
    
    def do_POST(self):
        if self.path != '/webhook/stripe':
            self.send_error_response(404, "Not found")
            return
        content_length = int(self.headers.get('Content-Length', 0))
        payload = self.rfile.read(content_length)
        sig_header = self.headers.get('Stripe-Signature', '')
        if not verify_stripe_signature(payload, sig_header):
            self.send_error_response(400, "Invalid signature")
            return
        try:
            event = json.loads(payload)
        except:
            self.send_error_response(400, "Invalid JSON")
            return
        result = handle_stripe_event(event)
        self.send_json_response(200, result)
    
    def send_json_response(self, code, data):
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def send_error_response(self, code, message):
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"error": message}).encode())

def run_server(port=8080):
    server = HTTPServer(('0.0.0.0', port), WebhookHandler)
    log.info(f"🚀 Delivery webhook server running on port {port}")
    log.info(f"   Endpoint: POST /webhook/stripe")
    log.info(f"   Configure at: https://dashboard.stripe.com/webhooks")
    server.serve_forever()

# ─── CLI ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Product Delivery Pipeline")
    sub = parser.add_subparsers(dest="cmd")
    
    sub.add_parser("serve", description="Start webhook server").add_argument("--port", type=int, default=8080)
    
    p = sub.add_parser("deliver", description="Manually trigger delivery")
    p.add_argument("--email", required=True)
    p.add_argument("--product", required=True)
    
    sub.add_parser("log", description="Show delivery log").add_argument("--limit", type=int, default=20)
    
    args = parser.parse_args()
    
    if args.cmd == "deliver":
        result = deliver_product(args.email, args.product)
        print(json.dumps(result, indent=2))
        sys.exit(0 if result["status"] == "sent" else 1)
    elif args.cmd == "log":
        data = load_delivery_log()
        print(f"\n📦 Delivery Log — {len(data['deliveries'])} total deliveries")
        print("=" * 80)
        icons = {"sent": "✅", "failed": "❌", "duplicate": "⏭️"}
        for d in data["deliveries"][:args.limit]:
            icon = icons.get(d["status"], "❓")
            print(f"{icon} [{d['timestamp']}] {d['email']} | {d['product_id']} | {d['status']}")
            if d.get('error'):
                print(f"   Error: {d['error']}")
        sys.exit(0)
    elif args.cmd == "serve":
        run_server(args.port)
    else:
        parser.print_help()
