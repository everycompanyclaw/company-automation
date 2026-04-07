#!/usr/bin/env python3
"""
Cold Email Sender
Version: 1.0.0

Send personalized cold emails via SMTP (Gmail, Outlook) or SendGrid API.
Supports CSV input, template variables, and rate limiting.

Usage:
    # SMTP mode
    python cold_email_sender.py --config config.py --template template.txt --recipients leads.csv --dry-run

    # SendGrid mode
    python cold_email_sender.py --config config.py --template template.txt --recipients leads.csv --provider sendgrid --dry-run

Requirements:
    pip install sendgrid  # For SendGrid mode

Input CSV format (recipients.csv):
    email,name,company,title,custom_var
    john@acme.com,John Smith,Acme Corp,CEO,something

Template format (template.txt):
    Subject: Quick intro — {{company}}

    Hi {{name}},

    I noticed {{company}} is doing interesting work in [industry].
    I'd love to show you how we're helping similar companies [outcome].

    Would you be open to a 15-min call this week?

    Best,
    {{sender_name}}
"""

import argparse
import csv
import os
import re
import smtplib
import sys
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import Optional

# ─── SendGrid Support ─────────────────────────────────────────────────────────
try:
    from sendgrid import SendGridAPIClient
    from sendgrid.helpers.mail import Mail

    SENDGRID_AVAILABLE = True
except ImportError:
    SENDGRID_AVAILABLE = False


# ─── Template Engine ─────────────────────────────────────────────────────────
def interpolate_template(template: str, variables: dict) -> tuple:
    """Replace {{var}} placeholders in template. Returns (subject, body)."""
    subject = ""
    body = template

    # Extract subject from first line if it's "Subject: ..."
    lines = template.split("\n", 1)
    if lines[0].lower().startswith("subject:"):
        subject = lines[0][8:].strip()
        body = lines[1] if len(lines) > 1 else ""

    def replace(match):
        key = match.group(1).strip()
        return str(variables.get(key, match.group(0)))

    subject = re.sub(r"\{\{(\w+)\}\}", replace, subject)
    body = re.sub(r"\{\{(\w+)\}\}", replace, body)
    return subject, body


def load_template(path: str) -> str:
    with open(path, "r") as f:
        return f.read()


def load_recipients(path: str) -> list:
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


# ─── Email Sending ────────────────────────────────────────────────────────────
def send_via_smtp(
    subject: str,
    body: str,
    to_email: str,
    from_email: str,
    smtp_host: str,
    smtp_port: int,
    username: str,
    password: str,
    use_tls: bool = True,
) -> bool:
    """Send email via SMTP."""
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email

    msg.attach(MIMEText(body, "plain"))
    msg.attach(MIMEText(body, "html"))

    try:
        with smtplib.SMTP(smtp_host, smtp_port, timeout=30) as server:
            if use_tls:
                server.starttls()
            server.login(username, password)
            server.sendmail(from_email, [to_email], msg.as_string())
        return True
    except Exception as e:
        print(f"    ❌ SMTP error: {e}")
        return False


def send_via_sendgrid(
    subject: str,
    body: str,
    to_email: str,
    from_email: str,
    api_key: str,
) -> bool:
    """Send email via SendGrid API."""
    if not SENDGRID_AVAILABLE:
        print("❌ SendGrid not installed. Run: pip install sendgrid")
        return False

    message = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject=subject,
        html_content=body,
        plain_text_content=body,
    )

    try:
        sg = SendGridAPIClient(api_key)
        response = sg.send(message)
        return 200 <= response.status_code < 300
    except Exception as e:
        print(f"    ❌ SendGrid error: {e}")
        return False


def send_emails(
    template_path: str,
    recipients_path: str,
    config: dict,
    dry_run: bool = True,
    delay: float = 3.0,
):
    """Main sending function."""
    template = load_template(template_path)
    recipients = load_recipients(recipients_path)

    provider = config.get("provider", "smtp").lower()
    sender_name = config.get("sender_name", "Your Name")
    from_email = config.get("from_email")
    print(f"\n📤 Starting {provider.upper()} email campaign")
    print(f"   Recipients: {len(recipients)}")
    print(f"   Dry run: {dry_run}")
    print(f"   Delay between emails: {delay}s\n")

    for i, row in enumerate(recipients, 1):
        variables = {**row, "sender_name": sender_name}
        subject, body = interpolate_template(template, variables)

        print(f"[{i}/{len(recipients)}] {row['email']} — {row.get('name', 'N/A')}")
        if dry_run:
            print(f"    Subject: {subject}")
            print(f"    Body preview: {body[:80]}...")
        else:
            success = False
            if provider == "sendgrid":
                success = send_via_sendgrid(
                    subject=subject,
                    body=body,
                    to_email=row["email"],
                    from_email=from_email,
                    api_key=config["sendgrid_api_key"],
                )
            else:
                success = send_via_smtp(
                    subject=subject,
                    body=body,
                    to_email=row["email"],
                    from_email=from_email,
                    smtp_host=config["smtp_host"],
                    smtp_port=config.get("smtp_port", 587),
                    username=config["smtp_username"],
                    password=config["smtp_password"],
                    use_tls=config.get("smtp_use_tls", True),
                )

            if success:
                print(f"    ✅ Sent")
            else:
                print(f"    ❌ Failed")

        if i < len(recipients) and not dry_run:
            time.sleep(delay)

    print(f"\n✅ Campaign complete. {len(recipients)} emails processed.")


# ─── CLI ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cold Email Sender")
    parser.add_argument("--config", required=True, help="Python config file (see config.example.py)")
    parser.add_argument("--template", required=True, help="Email template file (.txt)")
    parser.add_argument("--recipients", required=True, help="Recipients CSV file")
    parser.add_argument("--dry-run", action="store_true", default=True, help="Dry run (no emails sent)")
    parser.add_argument("--live", action="store_false", dest="dry_run", help="Send actual emails (requires --dry-run removed)")
    parser.add_argument("--delay", type=float, default=3.0, help="Seconds between emails (rate limit)")
    args = parser.parse_args()

    # Load config
    config_path = Path(args.config)
    if not config_path.exists():
        print(f"Config file not found: {args.config}")
        sys.exit(1)

    import importlib.util

    spec = importlib.util.spec_from_file_location("config", args.config)
    config_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config_module)
    config = {k: v for k, v in vars(config_module).items() if not k.startswith("_")}

    send_emails(
        template_path=args.template,
        recipients_path=args.recipients,
        config=config,
        dry_run=args.dry_run,
        delay=args.delay,
    )
