#!/usr/bin/env python3
"""
Instagram API Poster — using IG Basic Display API
"""
import requests
import os
import sys
import json

IG_TOKEN = "IGAAU3w4V9XB5BZAFo5U1JLaF9kUTZAfRTE3S1dPRjJLVGlGWV83WWpKRXpscmJPcElnUDFTS3ZAXUndObTR4QWtqSDFaeTljTDlGXzVTWjN2dHZATdlJfQXZAlcjk3eXRzRlNjemVldEQwLWxBckYxeU5ZAS0dnSkI4R1IwRDdSdVp6bwZDZD"
IG_API = "https://graph.instagram.com"

def post_to_ig(caption, image_url):
    """Post image to Instagram via Basic Display API"""
    print(f"📸 Posting to Instagram (@everycompanyclaw)")
    
    # Create media container
    r1 = requests.post(
        f"{IG_API}/me/media",
        data={
            "access_token": IG_TOKEN,
            "image_url": image_url,
            "caption": caption
        },
        timeout=30
    )
    result1 = r1.json()
    print(f"Create media: {result1}")
    
    if "id" not in result1:
        print(f"❌ Failed: {result1}")
        return result1
    
    # Publish
    r2 = requests.post(
        f"{IG_API}/me/media_publish",
        data={
            "access_token": IG_TOKEN,
            "creation_id": result1["id"]
        },
        timeout=30
    )
    result2 = r2.json()
    print(f"✅ Posted! ID: {result2.get('id', 'unknown')}")
    return result2

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: ig_api_poster.py <caption_file> <image_url>")
        sys.exit(1)
    
    caption_file = sys.argv[1]
    image_url = sys.argv[2]
    
    with open(caption_file) as f:
        caption = f.read().strip()
    
    post_to_ig(caption, image_url)
