#!/usr/bin/env python3
"""
Postiz Agent - Instagram Auto-Post
"""
import os
import sys

# Check for API key
API_KEY = os.environ.get("POSTIZ_API_KEY", "")
WORKSPACE_ID = os.environ.get("POSTIZ_WORKSPACE_ID", "")

def main():
    print("📸 Postiz Agent - Instagram Auto-Post")
    print("=" * 40)
    
    if not API_KEY or not WORKSPACE_ID:
        print("❌ Missing configuration!")
        print("\nSet these environment variables:")
        print("  export POSTIZ_API_KEY='your_api_key'")
        print("  export POSTIZ_WORKSPACE_ID='your_workspace_id'")
        print("\nGet them from: https://postiz.com/settings")
        return
    
    print(f"✅ Configured with workspace: {WORKSPACE_ID}")
    print("\nReady to post!")
    print("\nUsage:")
    print("  python3 postiz_agent.py post 'Your caption #hashtag'")

if __name__ == "__main__":
    main()
