#!/usr/bin/env python3
"""
Instagram Auto-Poster - macOS AppleScript version
"""
import subprocess
import time

IG_CAPTION = """🧵 20 Python自動化腳本｜幫你慳10+粒鐘

由Email提取器、檔案整理器、發票生成器...
全部已經寫好，等你去用！

💰 $79 = 永久使用

#python #automation #hkig #香港 #startup #indiehacker"""

def main():
    print("🚀 Opening Instagram in Chrome...")
    
    # Open Instagram in Chrome
    subprocess.run(["open", "-a", "Google Chrome", "https://www.instagram.com/"])
    
    print("""
📱 Instagram opened in Chrome!

Please:
1. Log in (if not)
2. Click + to create post
3. Upload image
4. Click Next

I'll wait and try to help...
""")
    
    # Wait for user to get to caption screen
    print("⏳ Waiting 30 seconds...")
    time.sleep(30)
    
    # Try AppleScript to simulate Cmd+V to paste caption
    print("📝 Trying to paste caption...")
    subprocess.run(["osascript", "-e", """
        tell application "Google Chrome"
            activate
        end tell
        delay 1
        tell application "System Events"
            keystroke "v" using command down
        end tell
    """])
    
    print("""
⏳ Waiting 20 more seconds for you to click Share...
""")
    
    time.sleep(20)
    
    print("✅ Done! Did it post?")

if __name__ == "__main__":
    main()
