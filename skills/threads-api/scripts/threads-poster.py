#!/usr/bin/env python3
"""Threads API Auto-Poster for EveryCompanyClaw - v2 with publish step"""

import json
import sys
import requests
import time
from pathlib import Path

CONFIG_DIR = Path("/Users/macbookpro/.openclaw/company/.config")
TOKEN_FILE = CONFIG_DIR / "threads-token.enc"
USER_FILE = CONFIG_DIR / "threads-user.json"

def load_token():
    with open(TOKEN_FILE) as f:
        return f.read().strip()

def load_user():
    if USER_FILE.exists():
        with open(USER_FILE) as f:
            return json.load(f)
    return None

def save_user(user_id, name):
    with open(USER_FILE, 'w') as f:
        json.dump({"id": user_id, "name": name}, f)

def get_user(token):
    """Get Threads user info"""
    url = f"https://graph.threads.net/v1.0/me"
    params = {"fields": "id,name", "access_token": token}
    resp = requests.get(url, params=params)
    data = resp.json()
    if 'id' in data:
        save_user(data['id'], data.get('name', ''))
    return data

def post_thread(token, user_id, text):
    """Post a text thread to Threads API - Two step process"""
    # Step 1: Create container
    create_url = f"https://graph.threads.net/v1.0/{user_id}/threads"
    create_data = {
        "access_token": token,
        "media_type": "text",
        "text": text
    }
    create_resp = requests.post(create_url, json=create_data)
    create_result = create_resp.json()
    
    if 'id' not in create_result:
        return create_result
    
    container_id = create_result['id']
    
    # Step 2: Publish the container
    time.sleep(1)  # Brief pause for processing
    publish_url = f"https://graph.threads.net/v1.0/{user_id}/threads_publish"
    publish_data = {
        "access_token": token,
        "creation_id": container_id
    }
    publish_resp = requests.post(publish_url, json=publish_data)
    return publish_resp.json()

def main():
    if len(sys.argv) < 2:
        print("Usage: threads-poster.py <message>")
        sys.exit(1)
    
    text = sys.argv[1]
    token = load_token()
    
    # Get or load user
    user = load_user()
    if not user:
        print("📋 Fetching user info...")
        user = get_user(token)
        if 'id' not in user:
            print(f"❌ Failed to get user: {user}")
            sys.exit(1)
        print(f"👤 User: {user['name']} ({user['id']})")
    
    print(f"📤 Posting: {text[:50]}...")
    result = post_thread(token, user['id'], text)
    
    if 'id' in result:
        print(f"✅ Posted! ID: {result['id']}")
    else:
        print(f"❌ Error: {result}")

if __name__ == "__main__":
    main()
