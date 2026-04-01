---
name: threads-api
description: Post to Threads API (Instagram Threads/microblogging platform) for @mick_my_ac. Use when: (1) MK asks to post to Threads, (2) EveryCompanyClaw needs to post social media, (3) scheduling Threads posts, (4) testing Threads API connection. Requires two-step publish process (create container + publish). DO NOT use if token is expired - refresh first.
---

# Threads API Skill

## Overview

Post content to Threads (@mick_my_ac) via Meta's Threads Graph API. Handles authentication, two-step publishing, and error recovery.

## Critical: Two-Step Publishing

Threads API requires TWO API calls:

1. **Create container** → get container ID
2. **Publish container** → using container ID

Skipping step 2 creates a draft that never appears publicly.

## Quick Start

```python
import requests
import time

TOKEN = open('.config/threads-token.enc').read().strip()
USER_ID = "26139168152370559"

# Step 1: Create container
resp = requests.post(f'https://graph.threads.net/v1.0/{USER_ID}/threads',
    json={"access_token": TOKEN, "media_type": "text", "text": "Hello"})
container_id = resp.json().get('id')

# Step 2: Publish (wait 1 sec)
time.sleep(1)
publish = requests.post(f'https://graph.threads.net/v1.0/{USER_ID}/threads_publish',
    json={"access_token": TOKEN, "creation_id": container_id})
print(f"Posted: {publish.json()}")
```

## Workflow

1. **Check token validity** - GET `/v1.0/me` returns user info
2. **Create container** - POST to `/threads` with content
3. **Publish** - POST to `/threads_publish` with creation_id
4. **Verify** - Check `/threads` list for new post ID

## Error Handling

| Error | Meaning | Fix |
|-------|---------|-----|
| "Failed to decrypt" | Token corrupted/truncated | Regenerate token |
| 33 Object not found | Wrong ID or no permission | Check user ID |
| 2207052 Media failed | Image URL not accessible | Use HTTP URL only |
| "FINISHED" but not visible | Missing publish step | Add threads_publish call |

## Token Refresh

Tokens expire ~60 days. Refresh via:
```
GET https://graph.threads.net/refresh_access_token?grant_type=th_refresh_token&access_token=<TOKEN>&client_secret=<APP_SECRET>
```

Current credentials (workspace `~/.openclaw/company/.config/`):
- App ID: `1506807204365399`
- App Secret: `2de8cc68bc3f4f9a75f17e6f9ae0dbfa`
- User ID: `26139168152370559`
- Token file: `.config/threads-token.enc`

## Scripts

### threads-poster.py
Simple text posting: `python3 threads-poster.py "Your message"`

### threads-daily.py
AI-generated content + image posting for scheduled daily posts.

## References

See `references/threads-api.md` for complete API documentation, media types, and error codes.
