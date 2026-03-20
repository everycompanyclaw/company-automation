#!/usr/bin/env python3
"""Simple IG auto-post with pyautogui"""
import pyautogui, time, subprocess
pyautogui.FAILSAFE = False

# Open IG
subprocess.Popen(["open", "-a", "Google Chrome", "https://www.instagram.com/"])
time.sleep(4)

print("1. Open IG manually")
print("2. Create post (upload + next)")
time.sleep(25)

print("3. Click caption area")
pyautogui.click(500, 500)
time.sleep(1)

print("4. Type caption")
pyautogui.typewrite("🧵 Python Scripts $79 #automation #hkig", interval=0.01)
time.sleep(2)

print("5. Tab to Share and press Enter")
for _ in range(8):
    pyautogui.press("tab")
    time.sleep(0.2)
time.sleep(1)
pyautogui.press("enter")

print("6. Wait...")
time.sleep(10)
print("Done!")
