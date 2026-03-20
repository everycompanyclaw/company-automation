#!/usr/bin/env python3
"""
Full Video Script Generator
Creates complete scripts for all videos
"""
import json

videos = [
    {
        "id": 1,
        "title": "Save 10 Hours/Week with Python Automation",
        "style": "educational",
        "script": """INTRO (5s):
Hey everyone! In this video, I'm going to show you how to save 10 hours every single week using Python automation.

BODY (60s):
First, think about all the repetitive tasks you do every day. Checking emails, updating spreadsheets, generating reports... These take hours!

Second, here's the secret - Python can do all of this automatically. For example, I wrote a simple script that:
- Checks my emails every morning
- Categorizes important messages
- Sends me a summary

Third, the best part? It runs while I sleep! I set it up once, and now it works 24/7.

OUTRO (10s):
Imagine what you could do with 10 extra hours every week! Subscribe and hit the bell to learn more about Python automation.

#Python #Automation #Productivity #Tech""",
        "hashtags": ["#Python", "#Automation", "#Productivity", "#Tech", "#TimeSaving"]
    },
    {
        "id": 2,
        "title": "AI Tools That Actually Work",
        "style": "short",
        "script": """INTRO (3s):
AI tools that actually work in 2026!

BODY (45s):
Number 1: ChatGPT for writing - fastest drafts ever
Number 2: Claude for coding - it understands your whole project
Number 3: Python + APIs for automation - your personal assistant

These 3 changed my workflow completely.

OUTRO (7s):
Which AI tool is your favorite? Comment below!

#AI #ChatGPT #Claude #Productivity #AIFTools""",
        "hashtags": ["#AI", "#ChatGPT", "#Claude", "#Productivity", "#TechTools"]
    },
    {
        "id": 3,
        "title": "How I Built a Freelance Business",
        "style": "story",
        "script": """INTRO (5s):
Let me tell you how I built a freelance business from scratch...

BODY (60s):
It started when I realized I was spending 10 hours on manual tasks every week.

Then I learned Python. I built my first automation script - it took 2 hours.

The result? I had an extra 8 hours per week to find clients!

Within 3 months, I had my first paying client. Within 6 months, I had a full pipeline.

OUTRO (10s):
The secret is simple: learn one skill, automate your work, use the time to grow. Start today!

#Freelance #Python #SideHustle #Business""",
        "hashtags": ["#Freelance", "#Python", "#SideHustle", "#Business", "#Entrepreneur"]
    },
    {
        "id": 4,
        "title": "Python Script in 60 Seconds",
        "style": "short",
        "script": """INTRO (3s):
Python script in 60 seconds!

BODY (50s):
Here's a script that saves me 1 hour every day:
(Show code)
Import, define, run - that's it!

Now every morning I get my daily report automatically.

Less work, more results.

OUTRO (7s):
Want the code? Comment "CODE"!

#Python #Coding #Automation #Shorts""",
        "hashtags": ["#Python", "#Coding", "#Automation", "#Tech", "#Shorts"]
    },
    {
        "id": 5,
        "title": "The Future of Work is Remote",
        "style": "educational",
        "script": """INTRO (5s):
The future of work is remote. Here's why it matters...

BODY (60s):
First, geography doesn't matter anymore. You can work with anyone, anywhere.

Second, automation handles the boring stuff. Humans do creative work.

Third, AI amplifies your skills. One person + AI = 10x output.

The companies embracing this? They're winning.

OUTRO (10s):
Are you ready for the future of work? Follow for more!

#RemoteWork #FutureOfWork #AI #Productivity #WorkFromHome""",
        "hashtags": ["#RemoteWork", "#FutureOfWork", "#AI", "#Productivity", "#WorkFromHome"]
    }
]

# Save all scripts
with open("full_video_scripts.json", "w") as f:
    json.dump(videos, f, indent=2)

print("✅ Created 5 full video scripts!")

for v in videos:
    print(f"\n{'='*50}")
    print(f"VIDEO {v['id']}: {v['title']}")
    print(f"{'='*50}")
    print(v['script'][:200] + "...")
    print(f"\nHashtags: {', '.join(v['hashtags'])}")
