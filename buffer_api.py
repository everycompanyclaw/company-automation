#!/usr/bin/env python3
"""
Buffer API - Using official docs
"""
import requests

# Based on Buffer docs
BASE = "https://api.bufferapp.com/1"

# User's token
TOKEN = "UkyLwkkW9w3-9q9MNEh0C-y71q__g2FoSYzUhaakv2K"

# Try different endpoints
endpoints = [
    "/profiles.json",
    "/profiles/owned.json", 
    "/user.json",
    "/updates.json",
]

print("Testing Buffer API endpoints...")

for ep in endpoints:
    url = f"{BASE}{ep}?access_token={TOKEN}"
    try:
        r = requests.get(url, timeout=10)
        print(f"{ep}: {r.status_code}")
        if r.status_code == 200:
            print(f"  ✓ {r.json()}")
    except Exception as e:
        print(f"{ep}: Error")

print("""
If all return 404:
- Token may be invalid
- Or need different authentication
""")
