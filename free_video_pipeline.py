#!/usr/bin/env python3
"""
Free AI Video Pipeline
Uses free tools for video generation
"""
import os

FREE_TOOLS = {
    "image_generation": [
        {"name": "Leonardo.ai", "url": "leonardo.ai", "free": "150/day", "status": "ready"},
        {"name": "Midjourney", "url": "discord.com/invite/midjourney", "free": "Trial", "status": "ready"},
        {"name": "Playground AI", "url": "playgroundai.com", "free": "100/day", "status": "ready"},
        {"name": "Bing Image Creator", "url": "bing.com/create", "free": "100/day", "status": "ready"},
    ],
    "video_generation": [
        {"name": "Runway", "url": "runwayml.com", "free": "Trial", "status": "ready"},
        {"name": "Pika", "url": "pika.art", "free": "Trial", "status": "ready"},
        {"name": "Luma", "url": "lumalabs.ai", "free": "Trial", "status": "ready"},
    ],
    "voiceover": [
        {"name": "ElevenLabs", "url": "elevenlabs.io", "free": "10k chars", "status": "ready"},
        {"name": "Coqui", "url": "coqui.ai", "free": "Unlimited", "status": "ready"},
        {"name": "NaturalReader", "url": "naturalreaders.com", "free": "Free tier", "status": "ready"},
    ]
}

def show_free_tools():
    print("=" * 60)
    print("🎬 FREE AI VIDEO TOOLS")
    print("=" * 60)
    
    print("\n📷 IMAGE GENERATION (Free):")
    for t in FREE_TOOLS["image_generation"]:
        print(f"  • {t['name']} - {t['free']}")
        print(f"    {t['url']}")
    
    print("\n🎥 VIDEO GENERATION (Free):")
    for t in FREE_TOOLS["video_generation"]:
        print(f"  • {t['name']} - {t['free']}")
        print(f"    {t['url']}")
    
    print("\n🎤 VOICEOVER (Free):")
    for t in FREE_TOOLS["voiceover"]:
        print(f"  • {t['name']} - {t['free']}")
        print(f"    {t['url']}")

# Generate quick start guide
def create_quick_start():
    guide = """# 🎬 Quick Start - Free AI Video

## Step 1: Generate Images (Free)
Go to: **leonardo.ai** (150 free/day)

Copy & paste these prompts:

### Image 1: Robot Working
```
Robot working at modern desk, clock showing 10 hours saved, productivity concept, blue and green colors, futuristic office, 16:9
```

### Image 2: AI Brain
```
AI brain glowing with digital tools, ChatGPT and Python logos, tech concept, blue orange purple gradient, 16:9
```

### Image 3: Freelancer Success
```
Happy entrepreneur at laptop showing success, modern workspace, orange and white, professional lighting, 16:9
```

---

## Step 2: Generate Video (Free)
Go to: **pika.art** (free trial)

Upload images, select "animate" or "extend"

---

## Step 3: Voiceover (Free)
Go to: **elevenlabs.io** (free 10k chars)

Copy scripts from below and generate audio

---

## 📝 SCRIPTS

### Video 1: Save 10 Hours
```
Hey everyone! In this video, I'm going to show you how to save 10 hours every single week using Python automation.

First, think about all the repetitive tasks you do every day...

Second, here's the secret - Python can do all of this automatically.

Third, the best part? It runs while I sleep!

Imagine what you could do with 10 extra hours every week!
```

### Video 2: AI Tools
```
AI tools that actually work in 2026!

Number 1: ChatGPT for writing
Number 2: Claude for coding
Number 3: Python APIs

Which AI tool is your favorite?
```

### Video 3: Freelance Journey
```
Let me tell you how I built a freelance business from scratch...

It started when I realized I was spending 10 hours on manual tasks every week.

Then I learned Python. I built my first automation script.

Within 3 months, I had my first paying client. Within 6 months, I had a full pipeline.
```

---

## Step 4: Edit
Use **CapCut** (free) to combine:
- Video clips
- Voiceover
- Music
- Text overlay

---

## Step 5: Post
Upload to Instagram/TikTok and schedule!

---

## 🎯 Done!
"""
    
    with open("QUICK_START.md", "w") as f:
        f.write(guide)
    
    return guide

if __name__ == "__main__":
    show_free_tools()
    print("\n" + "="*60)
    guide = create_quick_start()
    print("\n✅ Created QUICK_START.md")
