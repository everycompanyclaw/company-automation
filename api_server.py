#!/usr/bin/env python3
"""
Simple API Server - Serves live data as JSON
"""
import json
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
from datetime import datetime

# Data files
LEADS_FILE = "/tmp/leads.json"
PIPELINE_FILE = "/tmp/sales_pipeline.json"

IG_TOKEN = "IGAAU3w4V9XB5BZAGFqLWlKT2twUW5FSk45UGZABLTRnMllkZAlRQSkNsVE5GZATF5dlNwSUNJZA0FDVlRDOVF3bE5iUWtRd2hmQUpiRFBoX05GRkU2OXBuQWFlYW5DZAHdrV1ZAiekZArSU5DdmxuTWZAuYUFxVFk0Nk5xeWY1UkktS18zcwZDZD"

class APIHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/stats':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            # Get live data
            stats = get_live_stats()
            self.wfile.write(json.dumps(stats).encode())
        else:
            super().do_GET()

def get_live_stats():
    """Fetch live stats from APIs"""
    import requests
    
    stats = {
        "timestamp": datetime.now().isoformat(),
        "leads": {"count": 0, "github": 0, "hackernews": 0},
        "instagram": {"posts": 0, "likes": 0},
        "pipeline": {"deals": 0},
        "actions": 0
    }
    
    # Get leads
    try:
        with open(LEADS_FILE) as f:
            leads = json.load(f).get("leads", [])
            stats["leads"]["count"] = len(leads)
            github = sum(1 for l in leads if l.get("source") == "github")
            stats["leads"]["github"] = github
            stats["leads"]["hackernews"] = len(leads) - github
    except:
        pass
    
    # Get Instagram
    try:
        resp = requests.get(
            "https://graph.instagram.com/v21.0/me/media",
            params={"fields": "id,caption,like_count", "access_token": IG_TOKEN, "limit": 10},
            timeout=10
        )
        if resp.status_code == 200:
            posts = resp.json().get("data", [])
            stats["instagram"]["posts"] = len(posts)
            stats["instagram"]["likes"] = sum(p.get("like_count", 0) for p in posts)
    except:
        pass
    
    # Get pipeline
    try:
        with open(PIPELINE_FILE) as f:
            deals = json.load(f).get("deals", [])
            stats["pipeline"]["deals"] = len(deals)
    except:
        pass
    
    # Calculate actions
    stats["actions"] = stats["leads"]["count"] * 10 + stats["instagram"]["posts"] * 5
    
    return stats

def save_api_json():
    """Save API data to JSON file for static serving"""
    stats = get_live_stats()
    with open("/tmp/api_stats.json", "w") as f:
        json.dump(stats, f)
    return stats

if __name__ == "__main__":
    print("📊 API Server starting on port 8080...")
    print("Endpoints: /api/stats")
    
    # Save initial stats
    save_api_json()
    
    # Start server
    server = HTTPServer(('0.0.0.0', 8080), APIHandler)
    server.serve_forever()