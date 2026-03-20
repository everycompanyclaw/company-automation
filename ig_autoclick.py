#!/usr/bin/env python3
"""
Instagram Auto-Click Share - Uses pyautogui with multiple methods
"""
import subprocess
import time
import pyautogui

pyautogui.FAILSAFE = False

def open_instagram():
    """Open Instagram"""
    subprocess.run(["open", "-a", "Google Chrome", "https://www.instagram.com/"])
    time.sleep(5)

def wait_for_post():
    """Wait for user to create post"""
    print("Waiting for post creation...")
    time.sleep(30)

def fill_caption():
    """Fill caption"""
    pyautogui.click(x=500, y=500)  # Click on caption area
    time.sleep(1)
    pyautogui.typewrite("🧵 20 Python自動化腳本｜幫你慳10+粒鐘\n\n💰 $79\n#python #automation #hkig", interval=0.01)
    print("Caption filled!")

def click_share_exact():
    """Click Share button at exact coordinates"""
    print("Attempting to click Share...")
    
    # Method 1: Try approximate location (center-right of screen)
    # Instagram Share button is usually in the right side
    for attempt in range(5):
        # Move to approximate Share button location
        pyautogui.moveTo(x=850, y=500, duration=0.3)
        time.sleep(0.2)
        pyautogui.click()
        print(f"Click attempt {attempt + 1}")
        time.sleep(0.5)
    
    # Method 2: Tab through to find Share button
    for _ in range(10):
        pyautogui.press('tab')
        time.sleep(0.3)
        pyautogui.press('enter')
        time.sleep(0.5)
    
    # Method 3: Click at different coordinates
    pyautogui.click(x=900, y=520)
    time.sleep(0.5)
    pyautogui.click(x=880, y=550)
    time.sleep(0.5)
    pyautogui.click(x=850, y=580)

def main():
    print("🚀 Instagram Auto-Click Share")
    print("=" * 40)
    
    # Open Instagram
    print("1. Opening Instagram...")
    open_instagram()
    
    # Wait for user to create post
    print("2. Creating post...")
    wait_for_post()
    
    # Fill caption
    print("3. Filling caption...")
    fill_caption()
    
    # Click Share
    print("4. Clicking Share...")
    click_share_exact()
    
    print("\n✅ Done! Check if posted!")

if __name__ == "__main__":
    main()
