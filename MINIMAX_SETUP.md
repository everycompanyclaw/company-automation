# MiniMax API Key Setup

## Board — Action Required

The social pipeline is ready but needs your MiniMax API key to generate fresh AI content.

**Subscribe here:** https://platform.minimaxi.com/subscribe/token-plan

## After you get the API key:

### Option 1: Set as environment variable
```bash
export MINIMAX_API_KEY="your_key_here"
```

### Option 2: Add to config
Edit `/Users/macbookpro/.mcporter/mcporter.json`:
```json
{
  "mcpServers": {
    "MiniMax": {
      "command": "uvx",
      "args": ["minimax-coding-plan-mcp", "-y"],
      "env": {
        "MINIMAX_API_KEY": "YOUR_KEY_HERE",
        "MINIMAX_API_HOST": "https://api.minimaxi.com"
      }
    }
  }
}
```

## What's powered by MiniMax

`content_generator.py` uses MiniMax for:
1. **web_search** — finds trending topics relevant to the company
2. **text generation** — creates unique Instagram + Threads posts

Without the key, it uses pre-written fallback posts.

## Test with API key
```bash
export MINIMAX_API_KEY="your_key"
python3 /tmp/company-automation/content_generator.py --topic "AI automation" --dry-run
```
