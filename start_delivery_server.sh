#!/bin/bash
# Start Delivery Pipeline Webhook Server
# Run via launchd, pm2, or cron @reboot

export PATH="/usr/local/bin:$PATH"
WORKDIR="/Users/macbookpro/.openclaw/company"
LOG="$WORKDIR/delivery_server.log"

echo "[$(date)] Starting delivery pipeline webhook server..." >> "$LOG"
cd "$WORKDIR"
exec python3 delivery_pipeline.py serve --port 8080 >> "$LOG" 2>&1
