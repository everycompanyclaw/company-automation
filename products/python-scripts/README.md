# Python Scripts Bundle — $79

**Version:** 1.0.0 | **Updated:** 2026-04-07

A collection of production-ready Python scripts for business automation. Each script is self-contained, documented, and designed to run on a schedule or on-demand.

---

## What's Included

### 🔌 API & Integrations (3 scripts)
- `stripe_webhook_handler.py` — Parse and process Stripe webhook events
- `gumroad_license_checker.py` — Verify Gumroad license keys programmatically
- `slack_channel_reporter.py` — Post formatted reports to Slack channels

### 📊 Data Processing (3 scripts)
- `csv_enricher.py` — Enrich CSV data with additional columns via API lookups
- `spreadsheet_sync.py` — Bi-directional sync between Google Sheets and CSV
- `invoice_generator.py` — Generate PDF invoices from JSON order data

### 📧 Outreach & Communication (3 scripts)
- `cold_email_sender.py` — Send personalized cold emails via SMTP/SendGrid
- `linkedin_message_sender.py` — Automate LinkedIn connection requests via API
- `newsletter_summarizer.py` — Summarize top articles and send as newsletter

### 🔧 Utilities (3 scripts)
- `backup_to_s3.py` — Backup files and databases to AWS S3
- `cron_scheduler.py` — Lightweight cron-like scheduler for Python scripts
- `log_analyzer.py` — Parse and summarize application logs

---

## Getting Started

1. Ensure Python 3.9+ is installed: `python3 --version`
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `config.example.py` to `config.py` and fill in your API keys
4. Run a script: `python scripts/script_name.py`
5. Schedule with cron or use the included `cron_scheduler.py`

---

## Requirements

- Python 3.9 or higher
- pip (Python package manager)
- API keys for services used (Stripe, Slack, SendGrid, etc.)
- AWS credentials for S3 backup scripts (optional)

---

## Configuration

Each script reads from `config.py`. Never commit this file — it's in `.gitignore`.

Environment variables are also supported:
```bash
export STRIPE_API_KEY="sk_live_..."
export SENDGRID_API_KEY="SG.xxx"
```

---

## Support

For questions about these scripts, open an issue at:
github.com/everycompanyclaw/company-automation/issues

---

**License:** Personal use only. Do not redistribute.
