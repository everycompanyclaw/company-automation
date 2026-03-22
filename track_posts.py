#!/usr/bin/env python3
"""
Track real posts from company activities
"""
import json
import os

CRM_FILE = "/tmp/company_crm.json"
POSTS_FILE = "/tmp/real_posts.json"

def load_json(path, default):
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return default

def get_posts():
    """Extract real posts from CRM activities"""
    crm = load_json(CRM_FILE, {"activities": []})
    
    posts = []
    for act in crm.get("activities", []):
        details = act.get("details", "")
        action = act.get("action", "")
        
        if "post_to_instagram" in details or "post_to_twitter" in details or "instagram" in details.lower():
            posts.append({
                "platform": "Instagram" if "instagram" in details.lower() else "Twitter",
                "content": details,
                "time": act.get("time", ""),
                "action": action
            })
    
    return posts

if __name__ == "__main__":
    posts = get_posts()
    print(f"Found {len(posts)} real posts")
    for p in posts:
        print(f"  - {p['platform']}: {p['time']}")
