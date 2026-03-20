#!/usr/bin/env python3
"""
Postiz Instagram Auto-Post
Uses Postiz API to schedule posts to Instagram
"""
import requests
import json
import os
from datetime import datetime

# Postiz API config
# User needs to set: POSTIZ_API_KEY and POSTIZ_WORKSPACE_ID
POSTIZ_API_KEY = os.environ.get("POSTIZ_API_KEY", "")
POSTIZ_WORKSPACE_ID = os.environ.get("POSTIZ_WORKSPACE_ID", "")
BASE_URL = "https://api.postiz.com/v1"

def get_headers():
    return {
        "Authorization": f"Bearer {POSTIZ_API_KEY}",
        "Content-Type": "application/json"
    }

def get_social_accounts():
    """Get connected social accounts"""
    url = f"{BASE_URL}/socialaccount?workspaceId={POSTIZ_WORKSPACE_ID}"
    r = requests.get(url, headers=get_headers())
    return r.json()

def create_post(content, image_url=None):
    """Create and schedule a post"""
    
    post_data = {
        "content": content,
        "workspaceId": POSTIZ_WORKSPACE_ID,
        "scheduledAt": datetime.now().isoformat(),
        "socialMediaIds": []  # Will be filled with Instagram account ID
    }
    
    if image_url:
        post_data["media"] = [{"url": image_url, "type": "image"}]
    
    url = f"{BASE_URL}/post"
    r = requests.post(url, json=post_data, headers=get_headers())
    return r.json()

def post_to_instagram(text, image_url=None):
    """Main function to post to Instagram via Postiz"""
    
    print("📸 Postiz Instagram Auto-Post")
    print("=" * 40)
    
    if not POSTIZ_API_KEY:
        print("❌ No API key configured")
        print("\nSetup:")
        print("1. Sign up at https://postiz.com")
        print("2. Connect your Instagram account")
        print("3. Get API key from settings")
        print("4. Set environment variables:")
        print("   POSTIZ_API_KEY=your_key")
        print("   POSTIZ_WORKSPACE_ID=your_workspace_id")
        return {"error": "no_api_key"}
    
    # Get accounts
    accounts = get_social_accounts()
    print(f"Accounts: {json.dumps(accounts, indent=2)[:200]}...")
    
    # Create post
    result = create_post(text, image_url)
    print(f"Result: {result}")
    
    return result

if __name__ == "__main__":
    # Test post
    result = post_to_instagram("🧠 Test post from AI Company #automation")
    print(json.dumps(result, indent=2))
