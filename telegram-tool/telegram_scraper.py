#!/usr/bin/env python3
"""
EveryCompanyClaw Telegram Scraper
=================================
A powerful, well-documented Telegram scraping tool for:
  - Scraping public channel messages
  - Keyword monitoring with alerts
  - Trending topic detection
  - Content aggregation
  - Clean JSON/CSV export

Requirements:
  - Python 3.9+
  - Telegram API credentials (https://my.telegram.org/apps)
  - Telethon library

Installation:
  pip install -r requirements.txt
  cp config.example.yaml config.yaml
  # Edit config.yaml with your API credentials
  python telegram_scraper.py --help

Usage Examples:
  # Scrape a single channel
  python telegram_scraper.py scrape --channel t.me/example_channel

  # Scrape multiple channels and export to JSON
  python telegram_scraper.py scrape --channels t.me/ch1 t.me/ch2 --format json

  # Search for keywords across messages
  python telegram_scraper.py monitor --keywords "bitcoin launch" --channel t.me/crypto_signals

  # Detect trending topics in a channel
  python telegram_scraper.py trends --channel t.me/tech_news

  # Export messages to CSV
  python telegram_scraper.py scrape --channel t.me/news --format csv --output news_export.csv

  # Interactive mode
  python telegram_scraper.py interactive

Legal Notice:
  This tool is for legitimate research, monitoring, and content aggregation only.
  Do not use for spam, harassment, or illegal purposes. Scraping Telegram may
  violate their Terms of Service. You assume all risk and responsibility.

Author: EveryCompanyClaw 🏢🤖💼
Version: 1.0.0
"""

import argparse
import csv
import datetime
import io
import json
import logging
import os
import re
import sys
import time
import unicodedata
from collections import Counter
from pathlib import Path
from typing import Any

import yaml
from rich.console import Console
from rich.logging import RichHandler
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.tree import Tree

# Optional dependencies
try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

try:
    from telethon import TelegramClient
    from telethon.errors import FloodWaitError, SessionPasswordNeededError
    from telethon.tl.functions.messages import GetHistoryRequest
    from telethon.tl.types import Message, MessageEntityTextUrl
    TELETHON_AVAILABLE = True
except ImportError:
    TELETHON_AVAILABLE = False

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(console=Console(), rich_tracebacks=True)]
)
log = logging.getLogger("telegram_scraper")


# =============================================================================
# CONFIGURATION
# =============================================================================

def load_config(config_path: str = "config.yaml") -> dict:
    """Load configuration from YAML file."""
    config_file = Path(config_path)
    if not config_file.exists():
        log.warning(f"Config file '{config_path}' not found. Using defaults.")
        return {}
    with open(config_file, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def save_config(config: dict, config_path: str = "config.yaml") -> None:
    """Save configuration to YAML file."""
    with open(config_path, "w", encoding="utf-8") as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)
    log.info(f"Configuration saved to '{config_path}'")


# =============================================================================
# TELETHON CLIENT
# =============================================================================

class TelegramScraperClient:
    """Wrapper around Telethon client with convenience methods."""

    def __init__(self, api_id: str, api_hash: str, phone: str,
                 session_name: str = "telegram_scraper", config: dict = None):
        if not TELETHON_AVAILABLE:
            raise ImportError(
                "Telethon is not installed. Run: pip install telethon"
            )

        self.api_id = api_id
        self.api_hash = api_hash
        self.phone = phone
        self.session_name = session_name
        self.config = config or {}
        self.client = None
        self._me = None

    async def connect(self) -> None:
        """Connect to Telegram."""
        log.info("Connecting to Telegram...")
        self.client = TelegramClient(
            self.session_name,
            self.api_id,
            self.api_hash,
            sequential_updates=True
        )

        await self.client.start(phone=self.phone)

        # Verify connection
        self._me = await self.client.get_me()
        log.info(f"Connected as: {self._me.first_name} (@{self._me.username})")

    async def disconnect(self) -> None:
        """Disconnect from Telegram."""
        if self.client:
            await self.client.disconnect()
            log.info("Disconnected from Telegram.")

    async def get_messages(
        self,
        channel: str,
        limit: int = 100,
        offset_id: int = 0,
        min_date: datetime.datetime = None,
        max_date: datetime.datetime = None,
        search_query: str = None,
        filter_type: str = None
    ) -> list[dict]:
        """
        Fetch messages from a channel.

        Args:
            channel: Channel username or t.me link
            limit: Maximum number of messages to fetch
            offset_id: Start from this message ID (for pagination)
            min_date: Only return messages after this date
            max_date: Only return messages before this date
            search_query: Filter messages by text search
            filter_type: Filter type ('photo', 'video', 'document', etc.)

        Returns:
            List of message dictionaries
        """
        # Normalize channel username
        channel = self._normalize_channel(channel)

        try:
            entity = await self.client.get_entity(channel)
        except ValueError:
            log.error(f"Channel not found: {channel}")
            return []

        messages = []
        total_fetched = 0
        request_delay = self.config.get("scraper", {}).get("request_delay", 1.0)

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=Console()
        ) as progress:
            task = progress.add_task(
                f"Fetching messages from {channel}...",
                total=None
            )

            while total_fetched < limit:
                try:
                    history = await self.client(GetHistoryRequest(
                        peer=entity,
                        limit=min(100, limit - total_fetched),
                        offset_id=offset_id,
                        offset_date=None,
                        add_offset=0,
                        max_id=0,
                        min_id=0,
                        hash=0
                    ))

                    if not history.messages:
                        break

                    for message in history.messages:
                        msg_dict = self._parse_message(message)

                        # Apply date filters
                        if min_date and msg_dict["date"] < min_date:
                            continue
                        if max_date and msg_dict["date"] > max_date:
                            continue

                        # Apply search filter
                        if search_query:
                            if search_query.lower() not in (msg_dict.get("text") or "").lower():
                                continue

                        messages.append(msg_dict)
                        total_fetched += 1

                        if total_fetched >= limit:
                            break

                    # Update offset for next batch
                    offset_id = history.messages[-1].id

                    if total_fetched >= limit:
                        break

                    self._rate_limit(request_delay)

                except FloodWaitError as e:
                    log.warning(f"Flood wait: sleeping for {e.seconds}s")
                    time.sleep(min(e.seconds, 30))
                except Exception as e:
                    log.error(f"Error fetching messages: {e}")
                    break

            progress.update(task, completed=True)

        log.info(f"Fetched {len(messages)} messages from {channel}")
        return messages

    async def get_channel_info(self, channel: str) -> dict:
        """Get information about a channel."""
        channel = self._normalize_channel(channel)
        try:
            entity = await self.client.get_entity(channel)
            info = {
                "id": entity.id,
                "title": getattr(entity, "title", None),
                "username": getattr(entity, "username", None),
                "about": getattr(entity, "about", None),
                "members_count": getattr(entity, "participants_count", None),
                "date": getattr(entity, "date", None),
                "verified": getattr(entity, "verified", False),
                "megagroup": getattr(entity, "megagroup", False),
                "type": type(entity).__name__
            }
            return info
        except Exception as e:
            log.error(f"Error getting channel info: {e}")
            return {}

    async def search_channels(self, query: str, limit: int = 10) -> list[dict]:
        """Search for public channels by name."""
        try:
            results = await self.client.get_dialogs(limit=limit * 2)
            channels = []
            for dialog in results:
                entity = dialog.entity
                title = getattr(entity, "title", "") or ""
                username = getattr(entity, "username", "") or ""
                if query.lower() in title.lower() or query.lower() in username.lower():
                    channels.append({
                        "title": title,
                        "username": username,
                        "id": entity.id,
                        "type": type(entity).__name__
                    })
                    if len(channels) >= limit:
                        break
            return channels
        except Exception as e:
            log.error(f"Error searching channels: {e}")
            return []

    # ---- Internal helpers ----

    def _normalize_channel(self, channel: str) -> str:
        """Normalize channel input to username or t.me link."""
        if channel.startswith("https://t.me/"):
            return channel
        if channel.startswith("t.me/"):
            return f"https://{channel}"
        return channel

    def _parse_message(self, message: Message) -> dict:
        """Parse a Telethon Message object into a dictionary."""
        text = ""
        if message.message:
            text = message.message

        # Extract URLs from entities
        urls = []
        if message.entities:
            for entity in message.entities:
                if isinstance(entity, MessageEntityTextUrl):
                    urls.append(entity.url)

        return {
            "id": message.id,
            "date": message.date.isoformat() if message.date else None,
            "text": text,
            "raw_text": message.message or "",
            "urls": urls,
            "views": message.views,
            "forwards": message.forwards,
            "replies": message.replies,
            "is_reply": message.is_reply,
            "reply_to_msg_id": message.reply_to_msg_id,
            "edit_date": message.edit_date.isoformat() if message.edit_date else None,
            "post_author": message.post_author,
            "channel_id": message.peer_id.channel_id if hasattr(message.peer_id, 'channel_id') else None,
            "from_id": message.from_id,
        }

    def _rate_limit(self, delay: float) -> None:
        """Apply rate limiting delay."""
        time.sleep(delay)


# =============================================================================
# ANALYZER
# =============================================================================

class MessageAnalyzer:
    """Analyze scraped messages for trends, keywords, and sentiment."""

    def __init__(self, config: dict = None):
        self.config = config or {}
        self.stopwords = set(
            self.config.get("analysis", {}).get("stopwords", []) +
            self._default_stopwords()
        )
        self.min_word_len = self.config.get("analysis", {}).get("min_word_length", 4)
        self.top_trends = self.config.get("analysis", {}).get("top_trends", 20)

    def _default_stopwords(self) -> list:
        """Default English stopwords."""
        return [
            "the", "and", "is", "are", "for", "that", "this", "with", "you",
            "your", "from", "have", "has", "was", "were", "been", "but",
            "not", "they", "their", "what", "which", "who", "when", "where",
            "how", "all", "can", "will", "just", "about", "would", "could",
            "should", "into", "than", "then", "some", "only", "more", "also",
            "very", "after", "back", "out", "over", "new", "now", "get",
            "got", "even", "much", "any", "most", "very", "well", "down",
            "up", "our", "we", "he", "she", "it", "my", "me", "him", "her",
            "its", "am", "do", "did", "done", "does", "been", "being",
            "say", "said", "says", "make", "made", "take", "took", "see",
            "saw", "know", "knew", "go", "went", "come", "came", "want",
            "think", "use", "find", "give", "tell", "ask", "need", "feel",
            "became", "leave", "call", "keep", "let", "begin", "seem",
            "help", "show", "hear", "play", "run", "move", "live", "believe",
            "hold", "bring", "happen", "write", "provide", "sit", "stand",
            "lose", "pay", "meet", "include", "continue", "set", "learn",
            "change", "lead", "understand", "watch", "follow", "stop",
            "create", "speak", "read", "spend", "grow", "open", "walk",
            "win", "offer", "remember", "love", "consider", "appear",
            "buy", "wait", "serve", "die", "send", "expect", "build",
            "stay", "fall", "cut", "reach", "kill", "remain", "suggest",
            "raise", "pass", "sell", "require", "report", "decide",
            "pull", "don't", "i'm", "you're", "they're", "we're", "it's",
            "that's", "what's", "there", "here", "because", "while"
        ]

    def extract_keywords(self, messages: list[dict]) -> list[tuple[str, int]]:
        """Extract most frequent meaningful words from messages."""
        word_counts = Counter()

        for msg in messages:
            text = msg.get("text", "") or ""
            # Normalize text
            text = self._normalize_text(text)
            words = text.split()
            for word in words:
                if len(word) >= self.min_word_len and word not in self.stopwords:
                    word_counts[word] += 1

        return word_counts.most_common(self.top_trends)

    def detect_trends(self, messages: list[dict]) -> list[dict]:
        """Detect trending topics using keyword frequency analysis."""
        keywords = self.extract_keywords(messages)

        trends = []
        for keyword, count in keywords:
            # Count how many messages contain this keyword
            matching_messages = [
                m for m in messages
                if keyword.lower() in (m.get("text", "") or "").lower()
            ]
            trends.append({
                "keyword": keyword,
                "total_mentions": count,
                "message_count": len(matching_messages),
                "latest_message_id": (
                    max(m["id"] for m in matching_messages)
                    if matching_messages else None
                )
            })

        # Sort by total mentions descending
        trends.sort(key=lambda x: x["total_mentions"], reverse=True)
        return trends[:self.top_trends]

    def keyword_monitoring(
        self,
        messages: list[dict],
        keywords: list[str]
    ) -> list[dict]:
        """Monitor messages for specific keywords."""
        results = []
        keywords_lower = [k.lower() for k in keywords]

        for msg in messages:
            text = (msg.get("text", "") or "").lower()
            matched = [kw for kw in keywords_lower if kw in text]
            if matched:
                results.append({
                    **msg,
                    "matched_keywords": matched
                })

        return results

    def sentiment_analysis(self, messages: list[dict]) -> list[dict]:
        """
        Perform basic sentiment analysis using a lexicon approach.
        Returns messages with sentiment scores and labels.
        """
        positive_words = {
            "good", "great", "excellent", "amazing", "love", "best",
            "awesome", "wonderful", "fantastic", "happy", "joy", "excited",
            "win", "winner", "profit", "gains", "bullish", "moon", "pump",
            "success", "successful", "breakthrough", "incredible", "perfect",
            "beautiful", "outstanding", "brilliant", "superb", "nice"
        }
        negative_words = {
            "bad", "terrible", "awful", "hate", "worst", "scam", "fail",
            "failure", "loss", "losses", "bearish", "dump", "crash", "drop",
            "risk", "warning", "alert", "danger", "problem", "issue",
            "broken", "fake", "fraud", "suspicious", "hack", "exploit"
        }

        results = []
        for msg in messages:
            text = (msg.get("text", "") or "").lower()
            words = set(text.split())

            pos_count = len(words & positive_words)
            neg_count = len(words & negative_words)

            if pos_count > neg_count:
                sentiment = "positive"
                score = (pos_count - neg_count) / max(len(words), 1)
            elif neg_count > pos_count:
                sentiment = "negative"
                score = -(neg_count - pos_count) / max(len(words), 1)
            else:
                sentiment = "neutral"
                score = 0.0

            results.append({
                **msg,
                "sentiment": sentiment,
                "sentiment_score": round(score, 4),
                "positive_words": pos_count,
                "negative_words": neg_count
            })

        return results

    def activity_by_hour(self, messages: list[dict]) -> list[dict]:
        """Analyze posting activity by hour of day."""
        hour_counts = Counter()
        for msg in messages:
            date_str = msg.get("date")
            if date_str:
                try:
                    dt = datetime.datetime.fromisoformat(date_str.replace("Z", "+00:00"))
                    hour_counts[dt.hour] += 1
                except (ValueError, TypeError):
                    pass

        return [
            {"hour": h, "count": c}
            for h, c in sorted(hour_counts.items())
        ]

    def top_messages(self, messages: list[dict], by: str = "views", limit: int = 10) -> list[dict]:
        """Get top messages by views, forwards, or replies."""
        if by == "views":
            return sorted(messages, key=lambda m: m.get("views") or 0, reverse=True)[:limit]
        elif by == "forwards":
            return sorted(messages, key=lambda m: m.get("forwards") or 0, reverse=True)[:limit]
        elif by == "replies":
            return sorted(messages, key=lambda m: m.get("replies") or 0, reverse=True)[:limit]
        return messages[:limit]

    def _normalize_text(self, text: str) -> str:
        """Normalize text for keyword extraction."""
        # Remove URLs
        text = re.sub(r'https?://\S+', '', text)
        # Remove @mentions
        text = re.sub(r'@\w+', '', text)
        # Remove #hashtags
        text = re.sub(r'#\w+', '', text)
        # Remove special characters but keep spaces
        text = re.sub(r'[^\w\s]', ' ', text)
        # Lowercase
        text = text.lower()
        # Normalize unicode
        text = unicodedata.normalize("NFKD", text)
        # Remove extra whitespace
        text = ' '.join(text.split())
        return text


# =============================================================================
# EXPORTER
# =============================================================================

class MessageExporter:
    """Export messages to various formats."""

    def __init__(self, output_dir: str = "./output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def to_json(self, messages: list[dict], output_path: str = None) -> str:
        """Export messages to JSON file."""
        if output_path is None:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = self.output_dir / f"messages_{timestamp}.json"

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(messages, f, ensure_ascii=False, indent=2)

        log.info(f"Exported {len(messages)} messages to {output_path}")
        return str(output_path)

    def to_csv(self, messages: list[dict], output_path: str = None) -> str:
        """Export messages to CSV file."""
        if output_path is None:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = self.output_dir / f"messages_{timestamp}.csv"

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Flatten messages for CSV
        flat_messages = []
        for msg in messages:
            flat = {
                "id": msg.get("id"),
                "date": msg.get("date"),
                "text": msg.get("text", ""),
                "views": msg.get("views"),
                "forwards": msg.get("forwards"),
                "replies": msg.get("replies"),
                "edit_date": msg.get("edit_date"),
                "post_author": msg.get("post_author"),
                "urls": ", ".join(msg.get("urls", [])),
            }
            flat_messages.append(flat)

        if flat_messages:
            fieldnames = list(flat_messages[0].keys())
            with open(output_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(flat_messages)

        log.info(f"Exported {len(messages)} messages to {output_path}")
        return str(output_path)

    def to_dataframe(self, messages: list[dict]) -> Any:
        """Convert messages to a Pandas DataFrame."""
        if not PANDAS_AVAILABLE:
            log.warning("Pandas not available. Install with: pip install pandas")
            return None
        return pd.DataFrame(messages)

    def generate_report(self, messages: list[dict], channel: str, analyzer: MessageAnalyzer) -> str:
        """Generate a text summary report."""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = self.output_dir / f"report_{timestamp}.txt"

        trends = analyzer.detect_trends(messages)
        top_views = analyzer.top_messages(messages, by="views", limit=5)
        activity = analyzer.activity_by_hour(messages)

        lines = [
            "=" * 60,
            "TELEGRAM SCRAPER — SUMMARY REPORT",
            "=" * 60,
            f"Channel: {channel}",
            f"Total Messages: {len(messages)}",
            f"Generated: {datetime.datetime.now().isoformat()}",
            "-" * 60,
            "TOP TRENDING KEYWORDS",
            "-" * 60,
        ]

        for i, trend in enumerate(trends[:10], 1):
            lines.append(
                f"  {i:2}. {trend['keyword']:<20} "
                f"({trend['total_mentions']} mentions, "
                f"{trend['message_count']} messages)"
            )

        lines += [
            "",
            "-" * 60,
            "TOP MESSAGES BY VIEWS",
            "-" * 60,
        ]
        for i, msg in enumerate(top_views, 1):
            text_preview = (msg.get("text", "") or "")[:80].replace("\n", " ")
            lines.append(f"  {i}. [{msg.get('views', 0):>8} views] {text_preview}")

        lines += [
            "",
            "-" * 60,
            "ACTIVITY BY HOUR (UTC)",
            "-" * 60,
        ]
        for act in activity:
            bar = "█" * min(act["count"], 50)
            lines.append(f"  {act['hour']:02d}:00 — {act['count']:>5} messages  {bar}")

        lines += [
            "-" * 60,
            "=" * 60,
        ]

        report_text = "\n".join(lines)
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report_text)

        log.info(f"Report saved to {report_path}")
        return str(report_path)


# =============================================================================
# MAIN CLI
# =============================================================================

def print_banner():
    """Print the tool banner."""
    banner = r"""
     _                                 _   _
    (_)                               (_) | |
     |  _   _  ___   ___  _ __  _ __  | | | |  ___
     | | | | |/ __| / _ \| '__|| '_ \ | | | | / _ \
     | | |_| |\__ \|  __/| |   | | | || | | ||  __/
     |__\__, ||___/ \___||_|   |_| |_||_| |_| \___|
        __/ |
       |___/    Telegram Scraper  v1.0.0
              by EveryCompanyClaw 🏢🤖💼
    """
    print(banner)


def cmd_scrape(args, config: dict):
    """Handle the scrape command."""
    if not TELETHON_AVAILABLE:
        log.error("Telethon is not installed. Run: pip install telethon")
        return

    api_id = config.get("telegram", {}).get("api_id") or args.api_id
    api_hash = config.get("telegram", {}).get("api_hash") or args.api_hash
    phone = config.get("telegram", {}).get("phone") or args.phone

    if not api_id or not api_hash or not phone:
        log.error(
            "Missing credentials. Provide them in config.yaml or as CLI arguments:\n"
            "  --api-id, --api-hash, --phone\n"
            "Get credentials at: https://my.telegram.org/apps"
        )
        return

    async def run():
        client = TelegramScraperClient(
            api_id=api_id,
            api_hash=api_hash,
            phone=phone,
            config=config
        )

        try:
            await client.connect()

            # Build list of channels
            channels = args.channels or [args.channel] if args.channel else []
            if not channels and not args.all_dialogs:
                log.error("No channels specified. Use --channel or --channels.")
                return

            all_messages = []
            channel_info = {}

            for ch in channels:
                log.info(f"Scraping channel: {ch}")

                # Get channel info
                info = await client.get_channel_info(ch)
                channel_info[ch] = info

                # Fetch messages
                messages = await client.get_messages(
                    ch,
                    limit=args.limit,
                    min_date=(
                        datetime.datetime.fromisoformat(args.min_date)
                        if args.min_date else None
                    ),
                    max_date=(
                        datetime.datetime.fromisoformat(args.max_date)
                        if args.max_date else None
                    ),
                    search_query=args.search
                )

                # Add channel metadata
                for msg in messages:
                    msg["channel"] = ch
                    msg["channel_title"] = info.get("title", ch)

                all_messages.extend(messages)

            log.info(f"Total messages scraped: {len(all_messages)}")

            # Export
            exporter = MessageExporter(
                output_dir=args.output_dir or config.get("output", {}).get("output_dir", "./output")
            )

            output_path = args.output

            if args.format == "json" or args.format == "both":
                p = exporter.to_json(all_messages, output_path)
                print(f"\n✅ JSON saved: {p}")

            if args.format == "csv" or args.format == "both":
                ext = "csv" if args.format == "csv" else "csv"
                if output_path:
                    csv_path = str(Path(output_path).with_suffix(".csv"))
                else:
                    csv_path = None
                p = exporter.to_csv(all_messages, csv_path)
                print(f"\n✅ CSV saved: {p}")

            # Optional summary
            if args.summary:
                analyzer = MessageAnalyzer(config)
                report_path = exporter.generate_report(all_messages, channels[0] if channels else "unknown", analyzer)
                print(f"\n📊 Report saved: {report_path}")

            # Print channel info
            if args.verbose:
                for ch, info in channel_info.items():
                    print(f"\nChannel: {ch}")
                    print(f"  Title: {info.get('title', 'N/A')}")
                    print(f"  Username: {info.get('username', 'N/A')}")
                    print(f"  Members: {info.get('members_count', 'N/A')}")
                    print(f"  Verified: {info.get('verified', False)}")

        finally:
            await client.disconnect()

    import asyncio
    asyncio.run(run())


def cmd_monitor(args, config: dict):
    """Handle the monitor command."""
    if not TELETHON_AVAILABLE:
        log.error("Telethon is not installed.")
        return

    api_id = config.get("telegram", {}).get("api_id") or args.api_id
    api_hash = config.get("telegram", {}).get("api_hash") or args.api_hash
    phone = config.get("telegram", {}).get("phone") or args.phone

    keywords = args.keywords.split(",") if args.keywords else \
               config.get("monitoring", {}).get("keywords", [])

    if not keywords:
        log.error("No keywords specified. Use --keywords or set them in config.yaml")
        return

    async def run():
        client = TelegramScraperClient(
            api_id=api_id,
            api_hash=api_hash,
            phone=phone,
            config=config
        )

        try:
            await client.connect()

            channel = args.channel
            log.info(f"Monitoring '{channel}' for keywords: {keywords}")

            while True:
                messages = await client.get_messages(
                    channel,
                    limit=args.limit,
                    search_query=None  # We filter manually for all keywords
                )

                analyzer = MessageAnalyzer(config)
                matches = analyzer.keyword_monitoring(messages, keywords)

                if matches:
                    log.info(f"🎯 Found {len(matches)} matching messages!")
                    print(f"\n{'='*60}")
                    print(f"KEYWORD ALERT — {len(matches)} matches")
                    print(f"Channel: {channel}")
                    print(f"Keywords: {keywords}")
                    print(f"{'='*60}")

                    for msg in matches[-5:]:  # Show last 5
                        print(f"\n[{msg['date']}] (Views: {msg.get('views', 0)})")
                        text = (msg.get("text", "") or "")[:200]
                        print(f"  {text}")
                        print(f"  → Matched: {msg.get('matched_keywords', [])}")

                    if args.output:
                        exporter = MessageExporter()
                        exporter.to_json(matches, args.output)
                        log.info(f"Saved matches to {args.output}")

                else:
                    log.info(f"No keyword matches in {len(messages)} messages scanned.")

                if args.once:
                    break

                interval = args.interval or config.get("monitoring", {}).get("check_interval", 300)
                log.info(f"Next check in {interval}s...")
                time.sleep(interval)

        finally:
            await client.disconnect()

    import asyncio
    asyncio.run(run())


def cmd_trends(args, config: dict):
    """Handle the trends command."""
    if not TELETHON_AVAILABLE:
        log.error("Telethon is not installed.")
        return

    api_id = config.get("telegram", {}).get("api_id") or args.api_id
    api_hash = config.get("telegram", {}).get("api_hash") or args.api_hash
    phone = config.get("telegram", {}).get("phone") or args.phone

    async def run():
        client = TelegramScraperClient(
            api_id=api_id,
            api_hash=api_hash,
            phone=phone,
            config=config
        )

        try:
            await client.connect()

            channel = args.channel
            log.info(f"Analyzing trends in: {channel}")

            messages = await client.get_messages(channel, limit=args.limit)

            if not messages:
                log.warning("No messages found.")
                return

            analyzer = MessageAnalyzer(config)

            print(f"\n{'='*60}")
            print(f"TREND ANALYSIS — {channel}")
            print(f"Total messages analyzed: {len(messages)}")
            print(f"{'='*60}\n")

            # Trending keywords
            print("📈 TOP TRENDING KEYWORDS\n")
            trends = analyzer.detect_trends(messages)
            for i, trend in enumerate(trends, 1):
                bar_len = min(trend["total_mentions"], 40)
                bar = "█" * bar_len
                print(
                    f"  {i:2}. {trend['keyword']:<22} "
                    f"{trend['total_mentions']:>4} mentions  "
                    f"({trend['message_count']} msgs) {bar}"
                )

            # Sentiment distribution
            if args.sentiment:
                print(f"\n😊 SENTIMENT ANALYSIS\n")
                analyzed = analyzer.sentiment_analysis(messages)
                sentiments = Counter(m["sentiment"] for m in analyzed)
                total = sum(sentiments.values()) or 1
                for s, count in sentiments.most_common():
                    pct = count / total * 100
                    bar = "█" * int(pct / 2)
                    print(f"  {s.capitalize():<10} {count:>5} ({pct:5.1f}%)  {bar}")

            # Top messages
            print(f"\n🔥 TOP MESSAGES BY VIEWS\n")
            top = analyzer.top_messages(messages, by="views", limit=5)
            for i, msg in enumerate(top, 1):
                text = (msg.get("text", "") or "")[:60].replace("\n", " ")
                print(f"  {i}. [{msg.get('views', 0):>8} views] {text}")

            # Activity by hour
            print(f"\n⏰ ACTIVITY BY HOUR (UTC)\n")
            activity = analyzer.activity_by_hour(messages)
            if activity:
                max_count = max(a["count"] for a in activity)
                for act in activity:
                    bar_len = int(act["count"] / max_count * 30) if max_count else 0
                    bar = "█" * bar_len
                    print(f"  {act['hour']:02d}:00  {act['count']:>5}  {bar}")

            print()

            # Export if requested
            if args.export:
                exporter = MessageExporter()
                exporter.to_json(messages, args.export)
                log.info(f"Exported to {args.export}")

        finally:
            await client.disconnect()

    import asyncio
    asyncio.run(run())


def cmd_search(args, config: dict):
    """Handle the search command."""
    if not TELETHON_AVAILABLE:
        log.error("Telethon is not installed.")
        return

    api_id = config.get("telegram", {}).get("api_id") or args.api_id
    api_hash = config.get("telegram", {}).get("api_hash") or args.api_hash
    phone = config.get("telegram", {}).get("phone") or args.phone

    async def run():
        client = TelegramScraperClient(
            api_id=api_id,
            api_hash=api_hash,
            phone=phone,
            config=config
        )

        try:
            await client.connect()

            log.info(f"Searching for: {args.query}")
            results = await client.search_channels(args.query, limit=args.limit)

            if not results:
                log.info("No channels found.")
                return

            print(f"\n{'='*60}")
            print(f"CHANNEL SEARCH RESULTS — '{args.query}'")
            print(f"{'='*60}\n")

            table = Table(show_header=True, header_style="bold")
            table.add_column("#", style="dim", width=4)
            table.add_column("Title")
            table.add_column("Username")
            table.add_column("Type")

            for i, ch in enumerate(results, 1):
                table.add_row(
                    str(i),
                    ch.get("title", "N/A"),
                    f"@{ch.get('username', 'N/A')}",
                    ch.get("type", "N/A")
                )

            console = Console()
            console.print(table)

        finally:
            await client.disconnect()

    import asyncio
    asyncio.run(run())


def cmd_interactive(args, config: dict):
    """Interactive mode."""
    print_banner()
    print("Interactive Mode — EveryCompanyClaw Telegram Scraper")
    print("Type 'help' for commands, 'exit' to quit.\n")

    console = Console()

    while True:
        try:
            cmd = console.input("\n📬 > ")
            cmd = cmd.strip()
            if not cmd:
                continue

            if cmd.lower() in ("exit", "quit", "q"):
                print("Goodbye!")
                break

            if cmd.lower() == "help":
                print(HELP_TEXT)
                continue

            print(f"[yellow]Running: {cmd}[/yellow]")
            # Parse and run as CLI command
            # (In a full implementation, would route to appropriate handler)
            print("[yellow]Use the CLI commands for actual operations.[/yellow]")
            print("[yellow]Example: python telegram_scraper.py scrape --channel t.me/example[/yellow]")

        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break


HELP_TEXT = """
EveryCompanyClaw Telegram Scraper — Commands
---------------------------------------------
help              Show this help message
exit / quit       Exit interactive mode

Scrape Commands:
  python telegram_scraper.py scrape --channel t.me/channel_name
  python telegram_scraper.py scrape --channels t.me/ch1 t.me/ch2 --format json
  python telegram_scraper.py scrape --channel t.me/news --limit 5000 --format csv

Monitor Commands:
  python telegram_scraper.py monitor --channel t.me/channel --keywords "bitcoin,launch"
  python telegram_scraper.py monitor --channel t.me/signal --keywords "buy,alert" --interval 60

Trend Analysis:
  python telegram_scraper.py trends --channel t.me/tech_news --limit 1000
  python telegram_scraper.py trends --channel t.me/crypto --sentiment --export trends.json

Channel Search:
  python telegram_scraper.py search --query "crypto"

Setup:
  1. Get API credentials: https://my.telegram.org/apps
  2. Copy config.example.yaml to config.yaml
  3. Fill in your api_id, api_hash, and phone number
"""


# =============================================================================
# ARGUMENT PARSER
# =============================================================================

def build_parser():
    parser = argparse.ArgumentParser(
        description="EveryCompanyClaw Telegram Scraper v1.0.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=HELP_TEXT
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # ---- Scrape ----
    scrape_parser = subparsers.add_parser("scrape", help="Scrape messages from a channel")
    scrape_parser.add_argument("--channel", type=str, help="Single channel (username or t.me link)")
    scrape_parser.add_argument("--channels", nargs="+", type=str, help="Multiple channels")
    scrape_parser.add_argument("--all-dialogs", action="store_true", help="Scrape all joined dialogs")
    scrape_parser.add_argument("--limit", type=int, default=100, help="Max messages per channel (default: 100)")
    scrape_parser.add_argument("--format", type=str, choices=["json", "csv", "both"], default="json", help="Output format")
    scrape_parser.add_argument("--output", type=str, help="Output file path")
    scrape_parser.add_argument("--output-dir", type=str, help="Output directory")
    scrape_parser.add_argument("--search", type=str, help="Filter messages by text search")
    scrape_parser.add_argument("--min-date", type=str, help="Minimum date (ISO format: YYYY-MM-DD)")
    scrape_parser.add_argument("--max-date", type=str, help="Maximum date (ISO format: YYYY-MM-DD)")
    scrape_parser.add_argument("--summary", action="store_true", help="Generate summary report")
    scrape_parser.add_argument("--verbose", action="store_true", help="Show channel info")
    scrape_parser.add_argument("--api-id", type=str, help="Telegram API ID (overrides config)")
    scrape_parser.add_argument("--api-hash", type=str, help="Telegram API Hash (overrides config)")
    scrape_parser.add_argument("--phone", type=str, help="Phone number (overrides config)")

    # ---- Monitor ----
    monitor_parser = subparsers.add_parser("monitor", help="Monitor a channel for keywords")
    monitor_parser.add_argument("--channel", type=str, required=True, help="Channel to monitor")
    monitor_parser.add_argument("--keywords", type=str, help="Comma-separated keywords")
    monitor_parser.add_argument("--limit", type=int, default=100, help="Messages per check (default: 100)")
    monitor_parser.add_argument("--interval", type=int, help="Check interval in seconds (default: 300)")
    monitor_parser.add_argument("--once", action="store_true", help="Run once and exit")
    monitor_parser.add_argument("--output", type=str, help="Save matches to JSON file")
    monitor_parser.add_argument("--api-id", type=str, help="Telegram API ID")
    monitor_parser.add_argument("--api-hash", type=str, help="Telegram API Hash")
    monitor_parser.add_argument("--phone", type=str, help="Phone number")

    # ---- Trends ----
    trends_parser = subparsers.add_parser("trends", help="Analyze trending topics in a channel")
    trends_parser.add_argument("--channel", type=str, required=True, help="Channel to analyze")
    trends_parser.add_argument("--limit", type=int, default=1000, help="Messages to analyze (default: 1000)")
    trends_parser.add_argument("--sentiment", action="store_true", help="Include sentiment analysis")
    trends_parser.add_argument("--export", type=str, help="Export all messages to JSON")
    trends_parser.add_argument("--api-id", type=str, help="Telegram API ID")
    trends_parser.add_argument("--api-hash", type=str, help="Telegram API Hash")
    trends_parser.add_argument("--phone", type=str, help="Phone number")

    # ---- Search ----
    search_parser = subparsers.add_parser("search", help="Search for channels")
    search_parser.add_argument("--query", type=str, required=True, help="Search query")
    search_parser.add_argument("--limit", type=int, default=10, help="Results limit (default: 10)")
    search_parser.add_argument("--api-id", type=str, help="Telegram API ID")
    search_parser.add_argument("--api-hash", type=str, help="Telegram API Hash")
    search_parser.add_argument("--phone", type=str, help="Phone number")

    # ---- Interactive ----
    subparsers.add_parser("interactive", help="Interactive mode")

    return parser


# =============================================================================
# ENTRY POINT
# =============================================================================

def main():
    print_banner()

    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        print("\n" + HELP_TEXT)
        sys.exit(1)

    # Load config
    config = load_config(args.config if hasattr(args, "config") else "config.yaml")

    # Route to command handler
    if args.command == "scrape":
        cmd_scrape(args, config)
    elif args.command == "monitor":
        cmd_monitor(args, config)
    elif args.command == "trends":
        cmd_trends(args, config)
    elif args.command == "search":
        cmd_search(args, config)
    elif args.command == "interactive":
        cmd_interactive(args, config)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
