#!/usr/bin/env python3
"""
Log Analyzer
Version: 1.0.0

Parses application logs and generates a summary report with:
- Error frequency by type
- Request counts and response times (if applicable)
- Top errors with stack traces
- Time-based distribution

Usage:
    python log_analyzer.py --input app.log --output report.md
    python log_analyzer.py --input /var/log/app/ --output report.md --since "2026-04-01"

Requirements:
    pip install regex (optional, uses built-in re)

Input log format (auto-detected):
    - Standard: [TIMESTAMP] [LEVEL] message
    - JSON: {"timestamp": "...", "level": "...", "message": "..."}
    - Apache/Nginx: standard access log format
"""

import argparse
import gzip
import json
import os
import re
import sys
from collections import defaultdict, Counter
from datetime import datetime
from pathlib import Path
from typing import Optional


LOG_LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

LOG_PATTERN_STANDARD = re.compile(r"\[?(\d{4}-\d{2}-\d{2}[T\s]\d{2}:\d{2}:\d{2}[^\]]*)\]?\s*\[?(\w+)\]?\s*(.*)")
LOG_PATTERN_JSON = re.compile(r"^\s*\{.*\}\s*$")


def parse_log_line(line: str) -> Optional[dict]:
    """Parse a single log line. Returns None if unparseable."""
    line = line.strip()
    if not line:
        return None

    # Try JSON first
    if LOG_PATTERN_JSON.match(line):
        try:
            obj = json.loads(line)
            return {
                "timestamp": obj.get("timestamp") or obj.get("time") or obj.get("@timestamp"),
                "level": (obj.get("level") or obj.get("severity") or "INFO").upper(),
                "message": obj.get("message") or obj.get("msg", ""),
                "raw": line,
            }
        except json.JSONDecodeError:
            pass

    # Try standard format
    match = LOG_PATTERN_STANDARD.search(line)
    if match:
        return {
            "timestamp": match.group(1),
            "level": match.group(2).upper(),
            "message": match.group(3).strip(),
            "raw": line,
        }

    # Fallback: plain text
    return {"timestamp": None, "level": "INFO", "message": line, "raw": line}


def read_logs(path: str) -> list:
    """Read all log lines from a file or directory."""
    lines = []
    path_obj = Path(path)

    if path_obj.is_dir():
        files = sorted(path_obj.glob("*.log")) + sorted(path_obj.glob("*.log.gz"))
    else:
        files = [path_obj]

    for f in files:
        try:
            if f.suffix == ".gz":
                with gzip.open(f, "rt") as fh:
                    lines.extend(fh.readlines())
            else:
                with open(f, "r") as fh:
                    lines.extend(fh.readlines())
        except Exception as e:
            print(f"⚠️  Could not read {f}: {e}", file=sys.stderr)

    return lines


def analyze_logs(lines: list, since: Optional[str] = None) -> dict:
    """Analyze log lines and return statistics."""
    entries = []
    level_counts = Counter()
    error_messages = Counter()
    hourly_counts = defaultdict(int)

    since_dt = None
    if since:
        try:
            since_dt = datetime.fromisoformat(since)
        except ValueError:
            pass

    for line in lines:
        parsed = parse_log_line(line)
        if not parsed:
            continue

        # Filter by date if specified
        if since_dt and parsed["timestamp"]:
            try:
                ts_str = re.sub(r"[Z+-]\d{2}:?\d{2}$", "", parsed["timestamp"])
                ts_dt = datetime.fromisoformat(ts_str[:19])
                if ts_dt < since_dt:
                    continue
            except (ValueError, TypeError):
                pass

        entries.append(parsed)
        level_counts[parsed["level"]] += 1

        # Hour extraction for hourly stats
        if parsed["timestamp"]:
            try:
                hour = parsed["timestamp"][11:13]
                if hour.isdigit():
                    hourly_counts[hour] += 1
            except (IndexError, TypeError):
                pass

        if parsed["level"] in ("ERROR", "CRITICAL"):
            # Normalize error message (remove dynamic values)
            msg = re.sub(r"\d{4,}", "N", parsed["message"])
            msg = re.sub(r"[a-f0-9]{8,}", "ID", msg)
            msg = re.sub(r"['\"].*?['\"]", '"V"', msg)
            error_messages[msg[:120]] += 1

    return {
        "total_lines": len(lines),
        "parsed_entries": len(entries),
        "level_counts": dict(level_counts),
        "error_messages": dict(error_messages.most_common(20)),
        "hourly_counts": dict(sorted(hourly_counts.items())),
    }


def generate_report(stats: dict, output_path: str, title: str = "Log Analysis Report"):
    """Generate a markdown report from statistics."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        f"# {title}",
        f"",
        f"**Generated:** {now}",
        f"",
        "## Summary",
        f"",
        f"- Total log lines: **{stats['total_lines']:,}**",
        f"- Successfully parsed: **{stats['parsed_entries']:,}**",
        f"",
        "## Log Level Distribution",
        f"",
    ]

    for level in LOG_LEVELS:
        count = stats["level_counts"].get(level, 0)
        pct = (count / stats["parsed_entries"] * 100) if stats["parsed_entries"] else 0
        bar = "█" * int(pct / 2) + "░" * (50 - int(pct / 2))
        lines.append(f"- **{level}:** {count:,} ({pct:.1f}%) `{bar}`")

    lines.extend(["", "## Errors", ""])

    error_msgs = stats.get("error_messages", {})
    if error_msgs:
        lines.append("| Count | Error Message |")
        lines.append("|-------|----------------|")
        for msg, count in list(error_msgs.items())[:20]:
            escaped = msg.replace("|", "\\|").replace("\n", " ")
            lines.append(f"| {count} | {escaped[:100]} |")
    else:
        lines.append("No errors found ✅")

    hourly = stats.get("hourly_counts", {})
    if hourly:
        lines.extend(["", "## Activity by Hour (UTC)", ""])
        for hour in sorted(hourly.keys()):
            count = hourly[hour]
            bar = "█" * int(count / max(hourly.values()) * 30)
            lines.append(f"- **{hour}:00** {bar} ({count:,})")

    with open(output_path, "w") as f:
        f.write("\n".join(lines))

    return output_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze application logs and generate report")
    parser.add_argument("--input", required=True, help="Log file or directory")
    parser.add_argument("--output", default="log-report.md", help="Output markdown report")
    parser.add_argument("--title", default="Log Analysis Report", help="Report title")
    parser.add_argument("--since", help="Filter logs since date (YYYY-MM-DD)")
    args = parser.parse_args()

    print(f"📖 Reading logs from {args.input}...")
    lines = read_logs(args.input)
    print(f"   Read {len(lines):,} lines")

    print(f"🔍 Analyzing logs...")
    stats = analyze_logs(lines, since=args.since)

    print(f"📝 Generating report...")
    report_path = generate_report(stats, args.output, title=args.title)
    print(f"✅ Report saved to {report_path}")

    error_count = sum(stats["level_counts"].get(l, 0) for l in ("ERROR", "CRITICAL"))
    print(f"\n📊 Summary:")
    print(f"   Total lines: {stats['total_lines']:,}")
    print(f"   Errors: {error_count:,}")
    print(f"   Warnings: {stats['level_counts'].get('WARNING', 0):,}")
