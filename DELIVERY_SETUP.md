# Product Delivery Pipeline — Setup Guide

## Overview

Automated delivery system that receives Stripe payment events and emails product download links to customers within minutes.

## Components

- **`delivery_pipeline.py`** — Main delivery engine + Stripe webhook server
- **`automation/order_handler.py`** — Legacy email-based order processor (still works)
- **`automation/data/delivery_log.json`** — Audit log of all deliveries

## Quick Setup

### 1. Set Environment Variables

```bash
export STRIPE_WEBHOOK_SECRET="whsec_..."        # From Stripe Dashboard
export GMAIL_APP_PASSWORD="xxxx xxxx xxxx xxxx" # Gmail app password
export LINK_SECRET="your-secret-key"            # HMAC signing key for download links
export ALERT_EMAIL="everycompanyclaw@gmail.com" # Address for failure alerts
```

### 2. Start Webhook Server

```bash
# Option A: Direct
python3 delivery_pipeline.py serve --port 8080

# Option B: pm2 (production)
pm2 start delivery_pipeline.py --name delivery -- python3 serve --port 8080

# Option C: macOS launchd
# Copy com.company.delivery.plist to ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.company.delivery.plist
```

### 3. Configure Stripe Webhook

1. Go to https://dashboard.stripe.com/webhooks
2. Add endpoint: `https://YOUR_PUBLIC_URL/webhook/stripe`
3. Select events:
   - `checkout.session.completed` ✅
   - `payment_intent.succeeded` ✅
4. Copy the webhook signing secret → set as `STRIPE_WEBHOOK_SECRET`

### 4. Expose Webhook to Internet

For local dev / testing:
```bash
ngrok http 8080
# Use the https:// URL from ngrok output in Stripe webhook config
```

For production: point a subdomain DNS A record to your server.

## Local Testing

```bash
# Manually trigger a delivery
python3 delivery_pipeline.py deliver --email test@example.com --product python-scripts

# Check delivery log
python3 delivery_pipeline.py log

# View raw log file
cat automation/data/delivery_log.json
```

## Map Stripe Price IDs to Products

After creating products in Stripe, update `PRICE_TO_PRODUCT` in `delivery_pipeline.py`:

```python
PRICE_TO_PRODUCT = {
    "price_xxxxxxxxxxxx": "python-scripts",
    "price_yyyyyyyyyyyy": "zapier-templates",
    "price_zzzzzzzzzzzz": "ai-prompts",
}
```

Find Price IDs: Stripe Dashboard → Products → click a product → Prices section.

## File Versioning

- Products live in `products/{product-id}/`
- Each product has a `base_version` field (e.g., `"v1"`)
- Customers receive links to the version available at purchase time
- Product updates go into new version directories; old links remain valid for existing customers

## Acceptance Criteria — Status

| Criteria | Status |
|----------|--------|
| Customer receives product link within minutes | ✅ Webhook triggers email instantly |
| Delivery log maintained for audit | ✅ `automation/data/delivery_log.json` |
| Failed deliveries trigger alert | ✅ Sends alert email to ALERT_EMAIL |
| Product updates propagate correctly | ✅ Versioned paths protect existing customers |

## Monitoring

```bash
# Watch real-time logs
tail -f delivery_pipeline.log

# Health check
curl -X POST http://localhost:8080/webhook/stripe
# Returns {"error": "Invalid JSON"} if server is up (good!)

# Restart if needed
pm2 restart delivery
```
