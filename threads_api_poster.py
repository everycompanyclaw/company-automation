#!/usr/bin/env python3
"""
Threads API Poster — Direct Graph API posting
No browser needed once token is obtained.

Usage:
    python3 threads_api_poster.py --setup    # Get access token via OAuth
    python3 threads_api_poster.py --post "Your post content"
    python3 threads_api_poster.py --dry-run  # Test with sample post
"""

import os
import sys
import json
import requests
import argparse
import webbrowser
from datetime import datetime
from pathlib import Path

# ===== CONFIG =====
SCRIPT_DIR = Path(__file__).parent.resolve()
ENV_FILE = SCRIPT_DIR / ".env"
TOKEN_FILE = SCRIPT_DIR / ".threads_token"
CONFIG_FILE = SCRIPT_DIR / ".threads_config"

def load_env():
    env = {}
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip()
    return env

def save_token(token):
    TOKEN_FILE.write_text(token)
    os.chmod(TOKEN_FILE, 0o600)

def load_token():
    if TOKEN_FILE.exists():
        return TOKEN_FILE.read_text().strip()
    return None

def get_access_token(app_id, app_secret, code):
    """Exchange authorization code for access token."""
    url = "https://graph.facebook.com/v19.0/oauth/access_token"
    params = {
        "client_id": app_id,
        "client_secret": app_secret,
        "redirect_uri": "https://developers.facebook.com/tools/explorer",
        "code": code,
    }
    resp = requests.get(url, params=params, timeout=15)
    data = resp.json()
    if "access_token" in data:
        return data["access_token"]
    else:
        raise Exception(f"Token exchange failed: {data}")

def get_long_lived_token(short_token, app_id, app_secret):
    """Convert short-lived token to long-lived."""
    url = "https://graph.facebook.com/v19.0/oauth/access_token"
    params = {
        "grant_type": "fb_exchange_token",
        "client_id": app_id,
        "client_secret": app_secret,
        "fb_exchange_token": short_token,
    }
    resp = requests.get(url, params=params, timeout=15)
    return resp.json()

def get_threads_user_id(token):
    """Get Threads user ID from Instagram account."""
    url = "https://graph.facebook.com/v19.0/me/accounts"
    params = {"access_token": token}
    resp = requests.get(url, params=params, timeout=15)
    data = resp.json()
    if "data" in data and len(data["data"]) > 0:
        return data["data"][0].get("id")
    # Try Instagram business account linked to Threads
    url2 = "https://graph.facebook.com/v19.0/me"
    params2 = {"access_token": token, "fields": "instagram_business_account"}
    resp2 = requests.get(url2, params=params2, timeout=15)
    data2 = resp2.json()
    return data2.get("instagram_business_account", {}).get("id")

def post_to_threads(token, thread_id, content):
    """Post text content to Threads via Graph API."""
    url = f"https://graph.facebook.com/v19.0/{thread_id}/threads"
    params = {"access_token": token}
    data = {"message": content}
    resp = requests.post(url, params=params, json=data, timeout=30)
    return resp.json()

def setup(app_id, app_secret):
    """Interactive OAuth setup — get initial token."""
    auth_url = (
        f"https://www.facebook.com/v19.0/dialog/oauth"
        f"?client_id={app_id}"
        f"&redirect_uri=https%3A%2F%2Fdevelopers.facebook.com%2Ftools%2Fexplorer"
        f"&scope=threads_content_publish%2Cthreads_basic%2Cinstagram_basic"
        f"&response_type=code"
    )
    print(f"\n🔗 Open this URL in your browser to authorize:")
    print(f"   {auth_url}")
    print(f"\n   After authorizing, you'll be redirected to the Graph API Explorer.")
    print(f"   Copy the Authorization Code from the URL in your browser.")
    code = input("\nPaste the authorization code here: ").strip()
    
    print("\n🔄 Exchanging code for access token...")
    token = get_access_token(app_id, app_secret, code)
    
    print("🔄 Getting long-lived token...")
    long_lived = get_long_lived_token(token, app_id, app_secret)
    if "access_token" in long_lived:
        token = long_lived["access_token"]
    
    save_token(token)
    print(f"✅ Token saved!")
    
    # Get thread ID
    print("🔍 Finding your Threads account...")
    thread_id = get_threads_user_id(token)
    if thread_id:
        CONFIG_FILE.write_text(json.dumps({"thread_id": thread_id, "app_id": app_id}))
        print(f"✅ Threads account ID: {thread_id}")
    else:
        print("⚠️ Could not find Threads account ID automatically.")
        print("   You may need to provide it manually.")
    
    return token

def main():
    env = load_env()
    app_id = env.get("THREADS_APP_ID", "")
    app_secret = env.get("THREADS_APP_SECRET", "")
    token = load_token()
    
    parser = argparse.ArgumentParser(description="Threads API Poster")
    parser.add_argument("--setup", action="store_true", help="Run OAuth setup flow")
    parser.add_argument("--post", "-p", help="Post content to Threads")
    parser.add_argument("--dry-run", action="store_true", help="Show post content without publishing")
    parser.add_argument("--token", help="Provide access token directly")
    args = parser.parse_args()
    
    if args.setup:
        if not app_id or not app_secret:
            print("❌ THREADS_APP_ID and THREADS_APP_SECRET required in .env")
            sys.exit(1)
        token = setup(app_id, app_secret)
        return
    
    if args.token:
        save_token(args.token)
        print("✅ Token saved")
        return
    
    if not token:
        print("❌ No token found. Run with --setup first.")
        print("   Or provide token: threads_api_poster.py --token YOUR_TOKEN")
        sys.exit(1)
    
    if not app_id or not app_secret:
        print("❌ THREADS_APP_ID and THREADS_APP_SECRET required in .env")
        sys.exit(1)
    
    # Load thread config
    thread_id = None
    if CONFIG_FILE.exists():
        config = json.loads(CONFIG_FILE.read_text())
        thread_id = config.get("thread_id")
    
    if not thread_id:
        print("⚠️ Thread ID not found. Setting up...")
        thread_id = get_threads_user_id(token)
        if thread_id:
            CONFIG_FILE.write_text(json.dumps({"thread_id": thread_id, "app_id": app_id}))
    
    if not thread_id:
        print("❌ Could not determine Threads account ID.")
        print("   Create an app in Meta Developer Portal and link to Threads.")
        sys.exit(1)
    
    if args.dry_run:
        print(f"[DRY RUN] Would post to Threads:")
        print(f"  Thread ID: {thread_id}")
        print(f"  Token: {token[:20]}...")
        return
    
    if not args.post:
        print("Usage:")
        print("  --setup     : First-time OAuth setup")
        print("  --post TEXT : Post to Threads")
        print("  --dry-run   : Test configuration")
        print("  --token KEY : Save token directly")
        return
    
    print(f"📤 Posting to Threads...")
    result = post_to_threads(token, thread_id, args.post)
    
    if "id" in result:
        print(f"✅ Posted! ID: {result['id']}")
    else:
        print(f"❌ Posting failed: {result}")

if __name__ == "__main__":
    main()
