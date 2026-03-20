#!/usr/bin/env python3
"""
Proton Bridge Auto-Setup
Downloads and configures Proton Bridge
"""
import subprocess
import time
import os

def download_bridge():
    """Download Proton Bridge"""
    url = "https://protonmail.com/download/bridge/ProtonMailBridge-1.8.5.dmg"
    dest = os.path.expanduser("~/Downloads/ProtonMailBridge.dmg")
    
    print(f"📥 Downloading Proton Bridge to {dest}...")
    
    result = subprocess.run(
        ["curl", "-L", "-o", dest, url],
        capture_output=True
    )
    
    if os.path.exists(dest):
        print("✅ Downloaded!")
        # Open DMG
        subprocess.run(["open", dest])
        return True
    else:
        print("❌ Download failed")
        return False

def check_bridge_running():
    """Check if Proton Bridge is running"""
    result = subprocess.run(
        ["ps", "aux"],
        capture_output=True,
        text=True
    )
    
    if "Proton Bridge" in result.stdout or "protonbridge" in result.stdout:
        return True
    return False

def get_smtp_from_bridge():
    """Try to get SMTP config from Bridge"""
    # Bridge runs locally on port 1143
    print("🔌 Checking Bridge on localhost:1143...")
    
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex(('127.0.0.1', 1143))
        sock.close()
        
        if result == 0:
            print("✅ Bridge is running!")
            return True
    except:
        pass
    
    print("❌ Bridge not running")
    return False

print("""
🔧 Proton Bridge Setup
====================
""")

# Check if already running
if check_bridge_running():
    print("✅ Proton Bridge is already running!")
    get_smtp_from_bridge()
else:
    print("⚠️ Bridge not running")
    print("Please:")
    print("1. Download Bridge from the opened window")
    print("2. Install it")
    print("3. Log in with: everycompanyclaw@proton.me")
    print("4. Get SMTP credentials from Settings → Show Credentials")
    print("5. Give me the credentials and I'll connect!")
