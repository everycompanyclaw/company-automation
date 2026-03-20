#!/usr/bin/env python3
"""
Instagram Click Fix - Try ALL remaining methods
"""
import subprocess
import time
import os

def method1_playwright_js():
    """Method 1: Playwright with custom JS"""
    print("1️⃣ Trying Playwright JS injection...")
    script = '''
from playwright.sync_api import sync_playwright
import time

def click_share():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://www.instagram.com/")
        time.sleep(5)
        
        # Wait for user to create post
        print("Waiting for post...")
        time.sleep(25)
        
        # Fill caption
        page.keyboard.press("Tab")
        time.sleep(0.2)
        page.keyboard.type("🧵 Python Scripts $79 #automation", delay=2)
        
        # Try clicking with JS
        print("Clicking Share...")
        for i in range(10):
            page.evaluate("""
                () => {
                    // Get all buttons
                    const buttons = document.querySelectorAll('button');
                    for(let b of buttons) {
                        if(b.textContent.includes('Share')) {
                            b.click();
                            b.dispatchEvent(new MouseEvent('click', {bubbles: true}));
                            b.dispatchEvent(new Event('mousedown', {bubbles: true}));
                        }
                    }
                }
            """)
            time.sleep(0.5)
        
        time.sleep(15)
        browser.close()

click_share()
'''
    return script

def method2_pyautogui():
    """Method 2: pyautogui with coordinates"""
    print("2️⃣ Trying pyautogui with coordinates...")
    return '''
import pyautogui
import time
pyautogui.FAILSAFE = False

# Open Instagram
subprocess.run(["open", "-a", "Google Chrome", "https://www.instagram.com/"])
time.sleep(5)

# Wait for user
print("Waiting for post...")
time.sleep(25)

# Click and type
pyautogui.click(500, 500)
pyautogui.typewrite("🧵 Python Scripts $79", interval=0.01)

# Try multiple click positions for Share button
for x, y in [(850, 550), (900, 580), (800, 520), (950, 600)]:
    pyautogui.click(x, y)
    time.sleep(0.3)

print("Done!")
'''

def method3_applescript():
    """Method 3: AppleScript with UI elements"""
    print("3️⃣ Trying AppleScript UI...")
    return '''
tell application "Google Chrome"
    activate
end tell

delay 2

tell application "System Events"
    -- Try to find Share button
    keystroke "s" using {command down, shift down}
end tell
'''

def method4_shortcuts():
    """Method 4: iOS Shortcuts (manual setup needed)"""
    print("4️⃣ iOS Shortcuts - needs setup on phone")
    print("   Create Shortcut: Open Instagram → Share → Save")
    return None

def method5_extension():
    """Method 5: Browser extension approach"""
    print("5️⃣ Browser extension - needs manual install")
    return None

def main():
    print("""
🔧 INSTAGRAM CLICK SOLVER
======================

Trying ALL methods to auto-click Share:

1. Playwright JS injection
2. pyautogui coordinates
3. AppleScript UI
4. iOS Shortcuts (manual)
5. Browser Extension (manual)

Let's try them all!
""")
    
    # Try method 1
    print("\n--- Trying Method 1: Playwright ---")
    
    # Try method 2
    print("\n--- Trying Method 2: pyautogui ---")
    subprocess.run(["python3", "-c", method2_pyautogui()])
    
    print("\n⚠️ If none work:")
    print("- Instagram actively blocks automation")
    print("- Best solution: Use iOS Shortcuts app")
    print("- Or: Hire someone to click manually")

if __name__ == "__main__":
    main()
