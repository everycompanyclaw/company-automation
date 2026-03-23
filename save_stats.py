#!/usr/bin/env python3
"""
Save API stats to JSON - for static site to fetch
"""
import json
import requests
from datetime import datetime

LEADS_FILE = "/tmp/leads.json"
PIPELINE_FILE = "/tmp/sales_pipeline.json"
OUTPUT_FILE = "/Users/macbookpro/.openclaw/workspace/company/stats.json"
STATS_FILE_GITHUB = "/tmp/api_stats.json"

IG_TOKEN = "IGAAU3w4V9XB5BZAGFqLWlKT2twUW5FSk45UGZABLTRnMllkZAlRQSkNsVE5GZATF5dlNwSUNJZA0FDVlRDOVF3bE5iUWtRd2hmQUpiRFBoX05GRkU2OXBuQWFlYW5DZAHdrV1ZAiekZArSU5DdmxuTWZAuYUFxVFk0Nk5xeWY1UkktS18zcwZDZD"

def get_stats():
    """Get all stats"""
    stats = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "leads": {"count": 0, "github": 0, "hackernews": 0},
        "instagram": {"posts": 0, "likes": 0},
        "pipeline": {"deals": 0},
        "actions": 0
    }
    
    # Leads
    try:
        with open(LEADS_FILE) as f:
            leads = json.load(f).get("leads", [])
            stats["leads"]["count"] = len(leads)
            github = sum(1 for l in leads if l.get("source") == "github")
            stats["leads"]["github"] = github
            stats["leads"]["hackernews"] = len(leads) - github
    except:
        pass
    
    # Instagram
    try:
        resp = requests.get(
            "https://graph.instagram.com/v21.0/me/media",
            params={"fields": "id,like_count", "access_token": IG_TOKEN, "limit": 10},
            timeout=10
        )
        if resp.status_code == 200:
            posts = resp.json().get("data", [])
            stats["instagram"]["posts"] = len(posts)
            stats["instagram"]["likes"] = sum(p.get("like_count", 0) for p in posts)
    except:
        pass
    
    # Pipeline
    try:
        with open(PIPELINE_FILE) as f:
            deals = json.load(f).get("deals", [])
            stats["pipeline"]["deals"] = len(deals)
    except:
        pass
    
    stats["actions"] = stats["leads"]["count"] * 10 + stats["instagram"]["posts"] * 5
    
    return stats

if __name__ == "__main__":
    stats = get_stats()
    
    # Save locally
    with open(OUTPUT_FILE, "w") as f:
        json.dump(stats, f, indent=2)
    
    print(f"✅ Stats saved: {stats['leads']['count']} leads, {stats['instagram']['posts']} posts")