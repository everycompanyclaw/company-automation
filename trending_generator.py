#!/usr/bin/env python3
"""
Trending Topics Generator
Creates content based on current trends
"""
import json

TRENDING = {
    "hong_kong": [
        "Hong Kong 2026 Events",
        "Travel Trends Hong Kong",
        "Digital Transformation HK",
        "Tech Hub Asia",
        "Business Opportunities"
    ],
    "tech": [
        "AI Automation",
        "Python for Business",
        "No-Code Tools",
        "Remote Work",
        "Productivity Hacks"
    ],
    "lifestyle": [
        "Work Life Balance",
        "Side Hustle",
        "Financial Freedom",
        "Passive Income",
        "Career Growth"
    ]
}

def generate_trending_content():
    """Generate content ideas from trending topics"""
    content = []
    
    for category, topics in TRENDING.items():
        for topic in topics:
            content.append({
                "topic": topic,
                "category": category,
                "hashtags": generate_hashtags(topic),
                "script": generate_script(topic)
            })
    
    with open("trending_content.json", "w") as f:
        json.dump(content, f, indent=2)
    
    return content

def generate_hashtags(topic):
    """Generate hashtags for topic"""
    base = topic.lower().replace(" ", "")
    return f"#{base} #HongKong #2026 #Trending"

def generate_script(topic):
    """Generate short script for topic"""
    return f"""Did you know about {topic}?

This is changing everything in Hong Kong in 2026!

Here's what you need to know...

#HongKong #Trending #2026"""

# Run
content = generate_trending_content()

print(f"✅ Generated {len(content)} trending content ideas!")

for c in content:
    print(f"  📌 {c['topic']} ({c['category']})")
