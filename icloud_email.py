#!/usr/bin/env python3
"""
iCloud Hide My Email - Alternative to Proton
Uses AppleScript to open System Settings
"""
import subprocess
import time

def open_icloud_settings():
    """Open iCloud settings for Hide My Email"""
    print("🚀 Opening iCloud Settings...")
    
    # Open System Settings directly to iCloud section
    subprocess.run(["open", "x-apple.systempreferences:com.apple.Preferences、AppleIDSettings"])
    time.sleep(3)
    
    print("""
🍎 iCloud Hide My Email
=====================

Manual steps needed:

1. Click your name (Apple ID)
2. Click "iCloud" 
3. Click "Hide My Email" (or "Manage")
4. Click "+" to create new email
5. Choose:
   - Share new email: Yes
   - Forward to: your real email
   
6. Use the generated email for company

This gives unlimited email aliases!

After creating, give me the email and I'll connect SMTP!
""")

def main():
    open_icloud_settings()

if __name__ == "__main__":
    main()
