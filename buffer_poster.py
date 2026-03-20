#!/usr/bin/env python3
"""
Buffer Auto-Poster - Schedule posts to Instagram
"""
import os
import requests
import json

BUFFER_API = "https://api.bufferapp.com/1"

# Get token from environment or user
BUFFER_TOKEN = os.environ.get('BUFFER_ACCESS_TOKEN', '')

def get_auth_url():
    """Get Buffer OAuth URL"""
    return "https://buffer.com/oauth2/authorize?client_id=YOUR_CLIENT_ID&redirect_uri=YOUR_REDIRECT_URI&response_type=code"

def save_token(token):
    """Save Buffer token"""
    with open("/Users/macbookpro/.openclaw/workspace/company/.buffer_token", "w") as f:
        f.write(token)

def load_token():
    """Load Buffer token"""
    path = "/Users/macbookpro/.openclaw/workspace/company/.buffer_token"
    if os.path.exists(path):
        with open(path) as f:
            return f.read().strip()
    return None

def get_profiles():
    """Get connected social profiles"""
    if not BUFFER_TOKEN:
        return None
    
    url = f"{BUFFER_API}/profiles.json?access_token={BUFFER_TOKEN}"
    r = requests.get(url)
    return r.json() if r.status_code == 200 else None

def create_post(text, profile_id=None):
    """Create a post via Buffer"""
    if not BUFFER_TOKEN:
        return {"error": "No Buffer token"}
    
    url = f"{BUFFER_API}/updates/create.json"
    
    data = {
        "access_token": BUFFER_TOKEN,
        "text": text,
    }
    
    if profile_id:
        data["profile_ids[]"] = profile_id
    
    r = requests.post(url, data=data)
    return r.json() if r.status_code == 200 else r.json()

def post_to_instagram(text):
    """Post text to Instagram via Buffer"""
    profiles = get_profiles()
    
    if not profiles:
        return {"error": "No Buffer profiles connected"}
    
    # Find Instagram profile
    ig_profile = None
    for p in profiles:
        if p.get("service") == "instagram":
            ig_profile = p
            break
    
    if not ig_profile:
        return {"error": "No Instagram profile connected"}
    
    # Post
    result = create_post(text, ig_profile["id"])
    return result

# Ready-to-post content
POSTS = [
    "🧵 20 Python自動化腳本｜幫你慳10+粒鐘\n\n💰 $79\n\n#python #automation #hkig",
    "🤖 Build in public - AI company running 24/7\n\n$79起\n\n#buildinpublic #automation",
    "💰 Python Scripts Bundle - $79\n\n20個自動化腳本\n\n#automation #python #香港",
]

def main():
    print("""
📅 Buffer Auto-Poster
==================

To use:
1. Go to https://buffer.com
2. Create free account
3. Connect Instagram
4. Get Access Token: https://buffer.com/developers
5. Set: export BUFFER_ACCESS_TOKEN='your_token'

Current: {}
""".format("✅ Connected" if BUFFER_TOKEN else "❌ Need Token"))
    
    if BUFFER_TOKEN:
        profiles = get_profiles()
        if profiles:
            print("✅ Connected profiles:")
            for p in profiles:
                print(f"  - {p['service']}: {p.get('formatted_username', 'Unknown')}")
            
            # Try posting
            print("\n🚀 Attempting to post...")
            result = post_to_instagram(POSTS[0])
            print(f"Result: {result}")

if __name__ == "__main__":
    main()
