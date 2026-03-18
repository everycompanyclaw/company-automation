#!/usr/bin/env python3
"""
Instagram Auto-Poster - macOS Shortcuts Integration
Uses Apple Shortcuts for automation
"""
import subprocess
import time

IG_CAPTION = """🧵 20 Python自動化腳本｜幫你慳10+粒鐘

由Email提取器、檔案整理器、發票生成器...
全部已經寫好，等你去用！

💰 $79 = 永久使用

#python #automation #hkig #香港 #startup #indiehacker"""

def create_shortcut():
    """Create a macOS Shortcut for Instagram posting"""
    # This would create a Shortcut that can be triggered
    # For now, we'll use AppleScript directly
    
    script = '''
    tell application "Google Chrome"
        activate
    end tell
    
    delay 2
    
    tell application "System Events"
        -- Try to find Share button and click
        keystroke "s" using {command down, shift down}
    end tell
    '''
    
    return script

def main():
    print("🚀 Opening Instagram via Chrome...")
    
    # Open Instagram
    subprocess.run(["open", "-a", "Google Chrome", "https://www.instagram.com/"])
    
    print("""
📱 Instagram opened!

Please do:
1. Log in (if not)
2. Click + → Upload image → Click Next

I'll try to:
- Paste caption
- Press keyboard shortcut for Share
""")
    
    time.sleep(25)
    
    # Try to paste
    print("📝 Pasting caption...")
    subprocess.run([
        "osascript", "-e", '''
        tell application "Google Chrome"
            activate
        end tell
        delay 1
        tell application "System Events"
            keystroke "v" using command down
        end tell
        '''])
    print("   ✅ Pasted!")
    
    time.sleep(2)
    
    # Try Cmd+Shift+S or other shortcuts
    print("🔄 Trying keyboard shortcuts...")
    subprocess.run([
        "osascript", "-e", '''
        tell application "System Events"
            keystroke return using command down
        end tell
        '''])
    
    print("""
⏳ Waiting 25 seconds...
If posted → Done!
If not → Click Share manually
""")
    
    time.sleep(25)
    
    print("✅ Done!")

if __name__ == "__main__":
    main()
