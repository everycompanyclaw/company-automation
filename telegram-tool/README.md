# 🏢🤖💼 EveryCompanyClaw Telegram Scraper

> A powerful, well-documented Python tool for scraping, monitoring, and analyzing public Telegram channels. Built for marketers, researchers, traders, and analysts who need structured data from Telegram.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.9+-green)
![License](https://img.shields.io/badge/license-MIT-orange)

---

## 🚀 Features

- **📥 Message Scraping** — Fetch messages from any public Telegram channel with configurable limits, date ranges, and text search filters
- **📊 Trend Analysis** — Detect trending topics and keywords using frequency analysis
- **🔔 Keyword Monitoring** — Real-time alerts when specified keywords appear
- **😊 Sentiment Analysis** — Basic sentiment scoring (positive/neutral/negative) per message
- **📁 Multi-Format Export** — Export to clean JSON or CSV for integration with your tools
- **📈 Activity Reports** — Visual activity breakdowns by hour, top messages by views/forwards
- **🔍 Channel Search** — Search through your joined dialogs for specific channels
- **⏱️ Scheduled Monitoring** — Continuously monitor channels at configurable intervals
- **🧩 Modular Design** — Use as a CLI tool or import as a Python library

---

## 💰 Pricing & Business Model

This tool is available in three tiers:

| Feature | Free | Pro ($49/mo) | Enterprise ($199/mo) |
|---------|------|--------------|----------------------|
| Channels | 3 | Unlimited | Unlimited |
| Messages/channel | 1,000 | 10,000 | Unlimited |
| History depth | 7 days | 30 days | Full |
| Keyword monitoring | ❌ | ✅ | ✅ |
| Trend detection | ✅ | ✅ | ✅ |
| Sentiment analysis | ✅ | ✅ | ✅ |
| CSV/JSON export | ✅ | ✅ | ✅ |
| Alert webhooks | ❌ | ✅ | ✅ |
| API access | ❌ | ✅ | ✅ |
| Priority support | ❌ | ❌ | ✅ |
| White-label | ❌ | ❌ | ✅ |

> **Note:** The code is open source. The paid tiers are for hosted/API access, priority support, and white-label licensing.

---

## 📋 Requirements

- Python 3.9 or higher
- A Telegram account (phone number)
- Telegram API credentials from [my.telegram.org](https://my.telegram.org/apps)

---

## ⚡ Quick Start

### 1. Install Dependencies

```bash
# Clone or download the tool
cd telegram-tool

# Install Python dependencies
pip install -r requirements.txt

# If you don't have Pandas for DataFrame support (optional)
pip install pandas
```

### 2. Get Telegram API Credentials

1. Go to [my.telegram.org](https://my.telegram.org)
2. Log in with your phone number
3. Click **"API development tools"**
4. Fill in the form (app name, platform, etc.)
5. Copy your `api_id` and `api_hash`

### 3. Configure the Tool

```bash
# Copy the example config
cp config.example.yaml config.yaml

# Edit with your credentials
nano config.yaml
```

```yaml
# config.yaml
telegram:
  api_id: "1234567"           # Your numeric API ID
  api_hash: "abcdef123456..."  # Your API hash string
  phone: "+1234567890"         # Your phone number with country code
```

### 4. Scrape Your First Channel

```bash
# Scrape a channel and save to JSON
python telegram_scraper.py scrape --channel t.me/example_channel --limit 100

# Export to CSV instead
python telegram_scraper.py scrape --channel t.me/news --format csv

# Scrape multiple channels at once
python telegram_scraper.py scrape --channels t.me/ch1 t.me/ch2 --format json
```

---

## 📖 Usage Examples

### Scrape Messages

```bash
# Basic scrape
python telegram_scraper.py scrape --channel t.me/techcrunch --limit 500

# With date filter
python telegram_scraper.py scrape --channel t.me/bitcoin --limit 1000 \
  --min-date 2024-01-01 --max-date 2024-12-31

# Search within messages
python telegram_scraper.py scrape --channel t.me/crypto_signals \
  --search "bitcoin" --limit 500

# Generate a summary report
python telegram_scraper.py scrape --channel t.me/your_channel \
  --limit 2000 --format both --summary --verbose
```

### Monitor Keywords

```bash
# Monitor for specific keywords (one-time check)
python telegram_scraper.py monitor \
  --channel t.me/crypto_signals \
  --keywords "bitcoin,buy,dump,alert" \
  --limit 100 --once

# Continuous monitoring every 5 minutes
python telegram_scraper.py monitor \
  --channel t.me/trading_signals \
  --keywords "long,short,tp,sl" \
  --interval 300

# Save matches to a file
python telegram_scraper.py monitor \
  --channel t.me/news \
  --keywords "AI,OpenAI,GPT" \
  --output ai_alerts.json
```

### Analyze Trends

```bash
# Detect trending keywords
python telegram_scraper.py trends --channel t.me/tech_news --limit 2000

# Include sentiment analysis
python telegram_scraper.py trends \
  --channel t.me/marketing_tips \
  --limit 1000 --sentiment

# Export messages for further analysis
python telegram_scraper.py trends \
  --channel t.me/industry_news \
  --export all_messages.json
```

### Search Channels

```bash
# Search for channels by name
python telegram_scraper.py search --query "crypto"

# Get more results
python telegram_scraper.py search --query "marketing" --limit 20
```

### Interactive Mode

```bash
# Start interactive shell
python telegram_scraper.py interactive
```

---

## 🔧 Configuration Reference

All configuration lives in `config.yaml`:

```yaml
telegram:
  api_id: "YOUR_API_ID"
  api_hash: "YOUR_API_HASH"
  phone: "+1234567890"
  session_name: "telegram_scraper"

scraper:
  max_messages: 10000          # Max messages per channel
  request_delay: 1.0           # Seconds between requests (rate limit protection)

monitoring:
  enabled: false
  keywords: ["bitcoin", "launch", "airdrop"]
  alert_threshold: 3            # Min matches before alert
  check_interval: 300           # Seconds between checks

output:
  default_format: "json"       # json or csv
  output_dir: "./output"

analysis:
  detect_trends: true
  top_trends: 20
  sentiment_analysis: true
  min_word_length: 4
  stopwords:
    - "the"
    - "and"
    # ... (see config.example.yaml for full list)
```

---

## 📤 Output Formats

### JSON Output

```json
[
  {
    "id": 12345,
    "date": "2024-03-15T10:30:00+00:00",
    "text": "Bitcoin just broke $70,000! 🚀",
    "raw_text": "Bitcoin just broke $70,000! 🚀",
    "urls": ["https://example.com/news"],
    "views": 15432,
    "forwards": 234,
    "replies": 45,
    "edit_date": null,
    "post_author": "crypto_analyst",
    "channel": "t.me/btc_signals",
    "channel_title": "BTC Signals"
  }
]
```

### CSV Output

| id | date | text | views | forwards | replies |
|----|------|------|-------|----------|---------|
| 12345 | 2024-03-15T10:30:00+00:00 | Bitcoin just broke... | 15432 | 234 | 45 |

---

## 🏗️ Architecture

```
telegram-tool/
├── telegram_scraper.py      # Main CLI entry point
├── config.example.yaml      # Example configuration
├── requirements.txt         # Python dependencies
├── README.md                # This file
└── LICENSE                  # MIT License

# Internal modules (all in telegram_scraper.py for simplicity):
# ├── TelegramScraperClient  — Telethon wrapper + message fetching
# ├── MessageAnalyzer        — Trends, keywords, sentiment
# └── MessageExporter        — JSON/CSV/Report generation
```

---

## 🔌 Using as a Library

You can import and use the scraper programmatically:

```python
import asyncio
from telegram_scraper import TelegramScraperClient, MessageAnalyzer, MessageExporter

async def main():
    # Connect
    client = TelegramScraperClient(
        api_id="1234567",
        api_hash="abcdef...",
        phone="+1234567890"
    )
    await client.connect()

    # Fetch messages
    messages = await client.get_messages("t.me/example_channel", limit=500)

    # Analyze
    analyzer = MessageAnalyzer()
    trends = analyzer.detect_trends(messages)
    sentiment = analyzer.sentiment_analysis(messages)

    # Export
    exporter = MessageExporter("./output")
    exporter.to_json(messages, "export.json")

    await client.disconnect()

asyncio.run(main())
```

---

## ⚠️ Legal & Ethical Notice

> **This tool is for legitimate research, monitoring, and content aggregation only.**

- Telegram's Terms of Service prohibit scraping. **You assume all risk and responsibility.**
- Public channels only — private groups/channels require membership and explicit permission.
- Do **not** use this tool for: spam, harassment, impersonation, doxxing, harassment, or illegal purposes.
- Rate limits and flood waits are enforced to minimize server impact.
- Respect user privacy. Data collected should be handled responsibly.
- EveryCompanyClaw is not responsible for how you use this tool.

---

## 🤔 Common Issues

### "FloodWaitError" / Rate Limiting

The tool automatically handles rate limiting with delays between requests. If you see frequent flood waits, increase `request_delay` in `config.yaml`.

### "Channel not found"

- Make sure you're using the correct username (with or without `@`)
- The channel must be public or you must be a member
- Check your API credentials are correct

### "SessionPasswordNeededError"

Two-factor authentication is enabled on your Telegram account. Either disable 2FA in Telegram settings, or use the `password` parameter when connecting.

### "Account banned"

Telegram occasionally bans accounts using third-party API clients. To avoid this:
- Don't scrape aggressively (use rate limits)
- Rotate between multiple accounts for heavy use
- Use official Telegram apps for your primary account

---

## 🛣️ Roadmap

- [ ] Web dashboard for viewing scraped data
- [ ] Scheduled scraping jobs (cron-like)
- [ ] Webhook alerts for keyword monitoring
- [ ] Media downloading (photos, videos, documents)
- [ ] Database storage (SQLite/PostgreSQL)
- [ ] REST API server mode
- [ ] Multi-language sentiment analysis
- [ ] Docker deployment
- [ ] Cloud-hosted scraping service (SaaS)

---

## 🤝 Contributing

Contributions welcome! Please read the code, follow the style, and submit a PR.

---

## 📄 License

MIT License — © 2026 EveryCompanyClaw 🏢🤖💼

---

## 🆘 Support

- **Documentation:** This README + `config.example.yaml`
- **Issues:** Open a GitHub issue
- **Email:** support@everycompanyclaw.com
- **Telegram:** @EveryCompanyClaw

---

*Built with ❤️ by EveryCompanyClaw — Your 24/7 AI Company*
