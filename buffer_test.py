#!/usr/bin/env python3
"""
Buffer MCP - Simple version
"""
import json
import sys
import requests

TOKEN = "UkyLwkkW9w3-9q9MNEh0C-y71q__g2FoSYzUhaakv2K"

print("Buffer MCP Server ready")
print(f"Token: {TOKEN[:10]}...")

# Test API
r = requests.get(f"https://api.bufferapp.com/1/profiles.json?access_token={TOKEN}")
print(f"Profiles: {r.status_code}")

if r.status_code == 200:
    print("✅ Working!")
    print(r.json())
else:
    print(f"❌ Error: {r.text[:100]}")
