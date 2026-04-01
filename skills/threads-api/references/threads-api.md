# Threads API Reference

## Critical: Two-Step Publish Process

Threads API requires TWO API calls to publish:

### Step 1: Create Container
```
POST https://graph.threads.net/v1.0/{user-id}/threads
```
- Body: `{"media_type": "text", "text": "Your content"}`
- Response: `{"id": "<container_id>"}`

### Step 2: Publish Container
```
POST https://graph.threads.net/v1.0/{user-id}/threads_publish
```
- Body: `{"creation_id": "<container_id>"}`
- Response: `{"id": "<post_id>"}`

**Common Mistake:** Only calling Step 1 will create a container but NOT publish it.

## Required Credentials

### Config Files (workspace: ~/.openclaw/company/.config/)
- `threads-token.enc` - Access token (base64 encoded)
- `threads-user.json` - User info `{"id": "...", "name": "..."}`
- `threads-credentials.json` - App credentials

### Current Working Credentials
- **App ID:** `1506807204365399`
- **App Secret:** `2de8cc68bc3f4f9a75f17e6f9ae0dbfa`
- **User ID:** `26139168152370559`
- **Username:** `mick_my_ac`

## API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/v1.0/me` | GET | Get current user info |
| `/v1.0/{user-id}/threads` | POST | Create content container |
| `/v1.0/{user-id}/threads_publish` | POST | Publish container |
| `/v1.0/{user-id}/threads` | GET | List user's threads |

## Media Types

- `text` - Text-only post
- `image` - Image post (requires `image_url` field with HTTP URL)

**Note:** Base64 data URLs will fail. Only public HTTP URLs work for images.

## Token Refresh

Tokens expire and need refreshing every ~60 days.

Endpoint: `https://graph.threads.net/refresh_access_token`

Params:
- `grant_type=th_refresh_token`
- `access_token=<current_token>`
- `client_secret=<app_secret>`

Response: New token with `expires_in` (seconds)

## Error Codes

| Code | Message | Solution |
|------|---------|----------|
| 100 | Unsupported get request | Check permissions or token validity |
| 190 | Invalid OAuth token | Regenerate token |
| 33 | Object does not exist | Check ID or permissions |
| 2207052 | Media download failed | Use HTTP URL, not base64 |

## Permissions

Required for posting: `threads_content_publish` (privileged - needs app review or tester role)

For read-only: `threads_basic` (usually available by default)
