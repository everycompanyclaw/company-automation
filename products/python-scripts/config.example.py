"""
Configuration Example — Python Scripts Bundle
Copy this file to config.py and fill in your values.
NEVER commit config.py to version control.
"""

# ─── Stripe Webhook Handler ───────────────────────────────────────────────────
STRIPE_SECRET_KEY = "sk_test_..."
STRIPE_WEBHOOK_SECRET = "whsec_..."

# ─── Invoice Generator ────────────────────────────────────────────────────────
INVOICE_COMPANY_NAME = "Your Company Name"
INVOICE_COMPANY_ADDRESS = "123 Business St, City, Country"
INVOICE_COMPANY_EMAIL = "billing@yourcompany.com"
# INVOICE_LOGO_PATH = "/path/to/logo.png"  # Optional

# ─── Cold Email Sender ─────────────────────────────────────────────────────────
# Provider: "smtp" or "sendgrid"
EMAIL_PROVIDER = "smtp"

# SMTP Configuration (Gmail / Outlook / custom)
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "your@email.com"
SMTP_PASSWORD = "your-app-password"  # Use Gmail App Password, not login password
SMTP_USE_TLS = True

# SendGrid Configuration (alternative to SMTP)
SENDGRID_API_KEY = "SG.xxx"

# Email sender identity
FROM_EMAIL = "your@email.com"
SENDER_NAME = "Your Name"

# ─── S3 Backup ────────────────────────────────────────────────────────────────
AWS_ACCESS_KEY_ID = "AKIA..."
AWS_SECRET_ACCESS_KEY = "..."
AWS_DEFAULT_REGION = "us-east-1"
S3_BUCKET = "my-company-backups"
S3_PREFIX = "backups/"

# Sources to back up (relative to script location or absolute)
BACKUP_SOURCES = [
    "../data",
    "../database",
]

# Compression (gzip)
COMPRESS = True

# Retention: keep this many backups, delete older ones
KEEP_BACKUPS = 10

# ─── Slack Reporter ───────────────────────────────────────────────────────────
SLACK_BOT_TOKEN = "xoxb-..."
SLACK_DEFAULT_CHANNEL = "#alerts"

# ─── Google Sheets Sync ───────────────────────────────────────────────────────
GOOGLE_SERVICE_ACCOUNT_KEY = "../config/google-service-account.json"
SPREADSHEET_ID = "your-spreadsheet-id-here"
