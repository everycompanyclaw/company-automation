#!/usr/bin/env python3
"""
Instagram Poster - Longer posts about building the company
"""
import requests
import json
from datetime import datetime

IG_TOKEN = "IGAAU3w4V9XB5BZAGFqLWlKT2twUW5FSk45UGZABLTRnMllkZAlRQSkNsVE5GZATF5dlNwSUNJZA0FDVlRDOVF3bE5iUWtRd2hmQUpiRFBoX05GRkU2OXBuQWFlYW5DZAHdrV1ZAiekZArSU5DdmxuTWZAuYUFxVFk0Nk5xeWY1UkktS18zcwZDZD"

POSTS = [
    """🧵 How We Built an AI Company That Runs 24/7

Here's the story of how we built EveryCompanyClaw...

1/ We started with a simple idea: What if a company could run itself?

2/ First, we built AI agents for each role:
- CEO for strategy
- CTO for tech decisions  
- Sales for lead generation
- Marketing for content
- Operations for automation

3/ The key was connecting real APIs:
- GitHub API for leads
- Instagram API for posting
- Hacker News for content ideas

4/ Now we have 7 AI agents working together
- 47+ leads from real data
- Automated social media
- Self-improving systems

5/ The best part? It runs while we sleep.

The future of business is autonomous.

What do you think? 👇

#AI #Startup #Automation #Entrepreneur #Tech #Innovation""",

    """🚀 From Zero to 7 AI Agents - Our Journey

Building an AI-powered company isn't easy. Here's what we learned:

✦ Day 1: Started with one automation script
✦ Week 1: Added lead generation from GitHub API
✦ Week 2: Built 7 specialized AI agents
✦ Now: 47+ leads, automated posting, 24/7 operations

The secret sauce?
- Real data > Fake data
- Automation > Manual work
- AI agents > Single scripts

What's your biggest business challenge?
Drop a comment 👇

#Growth #StartupLife #AI #Automation""",

    """💡 We Built a Company That Runs Itself

Most businesses fail because they depend on humans working 24/7.

We solved this with AI agents.

Here's our stack:
▸ GitHub API → Real leads
▸ Instagram API → Auto posting  
▸ Hacker News → Content ideas
▸ OpenClaw → Agent orchestration

Results after 1 week:
✓ 47+ leads generated
✓ 2 Instagram posts published
✓ 7 AI agents running
✓ 500+ actions completed

The future is autonomous.

Are you ready? 🚀

#Startup #AI #FutureOfWork #Entrepreneur #TechStartup"""
]

def post_to_instagram():
    """Post a long-form content to Instagram"""
    
    caption = POSTS[0]  # First post
    
    # Create media container
    url = "https://graph.instagram.com/v21.0/me/media"
    image_url = "https://images.unsplash.com/photo-1551434678-e076c223a692?w=1080"
    
    data = {
        "image_url": image_url,
        "caption": caption,
        "access_token": IG_TOKEN
    }
    
    resp = requests.post(url, data=data, timeout=30)
    result = resp.json()
    print(f"Container: {result}")
    
    if "id" in result:
        # Wait and publish
        import time
        time.sleep(3)
        
        publish_url = "https://graph.instagram.com/v21.0/me/media_publish"
        pub_data = {
            "creation_id": result["id"],
            "access_token": IG_TOKEN
        }
        
        pub_resp = requests.post(publish_url, data=pub_data, timeout=30)
        pub_result = pub_resp.json()
        
        if "id" in pub_result:
            print(f"✅ Posted! ID: {pub_result['id']}")
            return True
    
    print(f"❌ Failed: {result}")
    return False

if __name__ == "__main__":
    post_to_instagram()