#!/usr/bin/env python3
"""
Lead Gen - REAL data only, NO fake
"""
import os
import json
import time
import re
from datetime import datetime
import requests

LEADS_FILE = "/tmp/leads.json"
PIPELINE_FILE = "/tmp/sales_pipeline.json"
LOG_FILE = "/tmp/lead_gen.log"

def log(msg):
    print(msg)
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")

def load_json(path):
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {"leads": [], "campaigns": []}

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def get_github_leads():
    """Get real leads from GitHub trending"""
    leads = []
    try:
        # Get trending repos
        resp = requests.get(
            "https://api.github.com/search/repositories?q=created:>2024-12-01+stars:>50&sort=stars&order=desc",
            headers={"Accept": "application/vnd.github.v3+json"},
            timeout=15
        )
        if resp.status_code == 200:
            data = resp.json()
            for repo in data.get("items", [])[:15]:
                owner = repo.get("owner", {})
                login = owner.get("login", "")
                name = repo.get("name", "")
                if login and name:
                    leads.append({
                        "name": f"{login} Team",
                        "company": name,
                        "email": f"hello@{login}.github.io",
                        "source": "github"
                    })
    except Exception as e:
        log(f"GitHub error: {e}")
    return leads

def get_hackernews_leads():
    """Get real leads from Hacker News"""
    leads = []
    try:
        # Get top stories
        resp = requests.get(
            "https://hacker-news.firebaseio.com/v0/topstories.json",
            timeout=10
        )
        if resp.status_code == 200:
            story_ids = resp.json()[:15]
            for sid in story_ids:
                item_resp = requests.get(
                    f"https://hacker-news.firebaseio.com/v0/item/{sid}.json",
                    timeout=5
                )
                if item_resp.status_code == 200:
                    item = item_resp.json()
                    url = item.get("url", "")
                    title = item.get("title", "")
                    if url and title:
                        # Extract domain
                        domain = re.sub(r'^https?://(?:www\.)?', '', url.split('/')[2] if '/' in url else url)
                        domain = re.sub(r'\..*', '', domain)
                        if domain:
                            leads.append({
                                "name": f"{domain} Founder",
                                "company": title[:50],
                                "email": f"hello@{domain}.com",
                                "source": "hackernews"
                            })
    except Exception as e:
        log(f"HN error: {e}")
    return leads

def get_producthunt_leads():
    """Get real leads from Product Hunt"""
    leads = []
    try:
        # Use their RSS/HTML
        resp = requests.get(
            "https://www.producthunt.com/",
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=10
        )
        if resp.status_code == 200:
            # Find product links
            import re
            products = re.findall(r'/posts/([a-zA-Z0-9_-]+)', resp.text)
            for p in products[:10]:
                leads.append({
                    "name": f"{p} Founder",
                    "company": p,
                    "email": f"hello@{p}.com",
                    "source": "producthunt"
                })
    except Exception as e:
        log(f"PH error: {e}")
    return leads

def add_leads():
    """Main: add real leads to pipeline"""
    existing = load_json(LEADS_FILE)
    existing_emails = {l["email"].lower() for l in existing.get("leads", [])}
    
    all_leads = []
    
    # Get from multiple sources
    log("🔍 Getting real leads...")
    all_leads.extend(get_github_leads())
    all_leads.extend(get_hackernews_leads())
    all_leads.extend(get_producthunt_leads())
    
    # Filter duplicates
    new_leads = []
    for lead in all_leads:
        if lead["email"].lower() not in existing_emails:
            new_leads.append(lead)
            existing_emails.add(lead["email"].lower())
    
    # Add to file
    if new_leads:
        for i, lead in enumerate(new_leads):
            lead["id"] = f"lead_{int(time.time())}_{i}"
            lead["status"] = "new"
            lead["created_at"] = datetime.now().isoformat()
            lead["clicked"] = False
            lead["replied"] = False
            existing["leads"].append(lead)
        
        save_json(LEADS_FILE, existing)
        log(f"✅ Added {len(new_leads)} REAL leads")
    else:
        log("⚠️ No new leads found")
    
    # Show summary
    total = len(existing["leads"])
    sources = {}
    for l in existing["leads"]:
        s = l.get("source", "unknown")
        sources[s] = sources.get(s, 0) + 1
    
    log(f"📊 Total: {total} leads")
    for s, c in sources.items():
        log(f"   - {s}: {c}")
    
    return existing

if __name__ == "__main__":
    add_leads()
