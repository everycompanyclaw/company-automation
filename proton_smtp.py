#!/usr/bin/env python3
"""
Proton SMTP Connector
Note: Don't store passwords in files - use environment
"""
import os
import subprocess

# User provides these - don't save to file!
PROTON_EMAIL = "everycompanyclaw@proton.me"

def get_smtp_config():
    """Get Proton SMTP configuration"""
    return {
        "email": PROTON_EMAIL,
        "smtp_host": "127.0.0.1",
        "smtp_port": "1143",
        "instructions": "Proton Mail Bridge needed for SMTP"
    }

def open_bridge_download():
    """Open Proton Mail Bridge download"""
    subprocess.run(["open", "-a", "Google Chrome", 
                   "https://protonmail.com/bridge/"])

print("""
📧 Proton SMTP Setup
=================

Proton requires "Mail Bridge" for SMTP access.

Steps:
1. Download Proton Bridge: https://protonmail.com/bridge/
2. Install and log in
3. Get SMTP credentials from Bridge app

SMTP Details:
- Host: 127.0.0.1
- Port: 1143
- Username: your@proton.email
- Password: Bridge password (not your login)

Once Bridge is running, I can connect SMTP!

Download: https://protonmail.com/bridge/
""")
