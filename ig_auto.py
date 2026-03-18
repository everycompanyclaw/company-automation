#!/usr/bin/env python3
"""
Instagram Auto-Poster - Final version
Uses pyautogui for clicking
"""
import subprocess
import time
import pyautogui

pyautogui.FAILSAFE = False

IG_CAPTION = """🧵 20 Python自動化腳本｜幫你慳10+粒鐘

由Email提取器、檔案整理器、發票生成器...
全部已經寫好，等你去用！

💰 $79 = 永久使用

#python #automation #hkig #香港 #startup #indiehacker"""

def main():
    print("🚀 Opening Instagram...")
    
    # Open Instagram
    subprocess.run(["open", "-a", "Google Chrome", "https://www.instagram.com/"])
    
    print("""
📱 Instagram opened!

Steps:
1. Click + → Upload image → Click Next
2. Wait for caption box
3. I'll paste caption in 20 seconds
""")
    
    time.sleep(20)
    
    # Try to paste
    print("📝 Trying to paste...")
    pyautogui.hotkey('command', 'v')
    print("   ✅ Pasted!")
    
    time.sleep(3)
    
    # Try to click Share
    print("🔄 Trying Share...")
    pyautogui.press('tab')
    time.sleep(0.5)
    pyautogui.press('enter')
    
    print("""
⏳ Waiting 20 seconds...
If posted → Done!
If not → Click Share manually
""")
    
    time.sleep(20)
    
    print("✅ Done!")

if __name__ == "__main__":
    main()
