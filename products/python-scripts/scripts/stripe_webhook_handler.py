#!/usr/bin/env python3
"""
Stripe Webhook Handler
Version: 1.0.0

Receives Stripe webhook events, verifies signature, and processes:
- payment_intent.succeeded
- payment_intent.failed
- customer.subscription.created
- customer.subscription.deleted
- invoice.payment_failed

Usage:
    python stripe_webhook_handler.py [--port 4242]

Requirements:
    pip install stripe flask
"""

import json
import os
import sys
import logging
from datetime import datetime
from flask import Flask, request, abort

import stripe

# ─── Configuration ────────────────────────────────────────────────────────────
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY", "")
STRIPE_WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET", "")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "webhooks")

# ─── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(OUTPUT_DIR, "webhook.log")),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)

# ─── Setup ────────────────────────────────────────────────────────────────────
os.makedirs(OUTPUT_DIR, exist_ok=True)
stripe.api_key = STRIPE_SECRET_KEY

app = Flask(__name__)

# ─── Event Handlers ───────────────────────────────────────────────────────────
EVENT_HANDLERS = {
    "payment_intent.succeeded": "handle_payment_succeeded",
    "payment_intent.failed": "handle_payment_failed",
    "customer.subscription.created": "handle_subscription_created",
    "customer.subscription.deleted": "handle_subscription_deleted",
    "invoice.payment_failed": "handle_invoice_failed",
}


def handle_payment_succeeded(event):
    """Log successful payment and save to file."""
    data = event["data"]["object"]
    record = {
        "event": "payment_succeeded",
        "payment_id": data["id"],
        "customer_email": data.get("receipt_email", "unknown"),
        "amount": data["amount"] / 100,  # Stripe amounts are in cents
        "currency": data["currency"].upper(),
        "timestamp": datetime.utcnow().isoformat(),
    }
    _save_event("payments", record)
    logger.info(f"Payment succeeded: {record['payment_id']} — ${record['amount']} {record['currency']}")


def handle_payment_failed(event):
    """Log failed payment for review."""
    data = event["data"]["object"]
    record = {
        "event": "payment_failed",
        "payment_id": data["id"],
        "customer_email": data.get("receipt_email", "unknown"),
        "amount": data["amount"] / 100,
        "currency": data["currency"].upper(),
        "failure_message": data.get("last_payment_error", {}).get("message", ""),
        "timestamp": datetime.utcnow().isoformat(),
    }
    _save_event("failed_payments", record)
    logger.warning(f"Payment failed: {record['payment_id']} — {record['failure_message']}")


def handle_subscription_created(event):
    """Log new subscription."""
    data = event["data"]["object"]
    record = {
        "event": "subscription_created",
        "subscription_id": data["id"],
        "customer_id": data["customer"],
        "status": data["status"],
        "amount": (data.get("items", {}).get("data", [{}])[0].get("price", {}).get("unit_amount", 0)) / 100,
        "timestamp": datetime.utcnow().isoformat(),
    }
    _save_event("subscriptions", record)
    logger.info(f"Subscription created: {record['subscription_id']} — {record['status']}")


def handle_subscription_deleted(event):
    """Log cancelled subscription."""
    data = event["data"]["object"]
    record = {
        "event": "subscription_deleted",
        "subscription_id": data["id"],
        "customer_id": data["customer"],
        "status": data["status"],
        "timestamp": datetime.utcnow().isoformat(),
    }
    _save_event("subscriptions", record)
    logger.info(f"Subscription cancelled: {record['subscription_id']}")


def handle_invoice_failed(event):
    """Log failed invoice payment."""
    data = event["data"]["object"]
    record = {
        "event": "invoice_failed",
        "invoice_id": data["id"],
        "customer_id": data["customer"],
        "amount_due": data["amount_due"] / 100,
        "attempt_count": data["attempt_count"],
        "timestamp": datetime.utcnow().isoformat(),
    }
    _save_event("invoices", record)
    logger.warning(f"Invoice payment failed: {record['invoice_id']} — attempt {record['attempt_count']}")


def _save_event(category: str, record: dict):
    """Append event record to a JSON file."""
    category_dir = os.path.join(OUTPUT_DIR, category)
    os.makedirs(category_dir, exist_ok=True)
    filename = f"{datetime.utcnow().strftime('%Y-%m-%d')}.jsonl"
    filepath = os.path.join(category_dir, filename)
    with open(filepath, "a") as f:
        f.write(json.dumps(record) + "\n")


# ─── Flask Route ───────────────────────────────────────────────────────────────
@app.route("/webhook", methods=["POST"])
def webhook():
    """Main webhook endpoint — receives events from Stripe."""
    if not STRIPE_SECRET_KEY:
        logger.error("STRIPE_SECRET_KEY not set")
        return {"error": "Server misconfigured"}, 500

    payload = request.get_data(as_text=True)
    sig_header = request.headers.get("Stripe-Signature")
    event = None

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, STRIPE_WEBHOOK_SECRET)
    except stripe.error.SignatureVerificationError:
        logger.error("Webhook signature verification failed")
        abort(400, "Invalid signature")
    except Exception as e:
        logger.error(f"Error parsing webhook: {e}")
        abort(400, str(e))

    event_type = event["type"]
    handler_name = EVENT_HANDLERS.get(event_type)

    if handler_name:
        handler = globals().get(handler_name)
        if handler:
            try:
                handler(event)
            except Exception as e:
                logger.error(f"Error in handler {handler_name}: {e}")
                return {"error": f"Handler error: {e}"}, 500
        else:
            logger.warning(f"No handler found for {event_type}")
    else:
        logger.debug(f"Unhandled event type: {event_type}")

    return {"received": True}, 200


# ─── CLI Mode ─────────────────────────────────────────────────────────────────
@app.route("/health", methods=["GET"])
def health():
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Stripe Webhook Handler")
    parser.add_argument("--port", type=int, default=4242, help="Port to run on")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    args = parser.parse_args()

    logger.info(f"Starting Stripe webhook handler on {args.host}:{args.port}")
    app.run(host=args.host, port=args.port, debug=os.environ.get("DEBUG", "false").lower() == "true")
