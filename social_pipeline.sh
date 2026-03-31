#!/bin/bash
# MiniMax Social Pipeline — Generate content + post to IG + Threads
# Runs every 6 hours via cron

LOG="/tmp/social_pipeline.log"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Load env vars (MiniMax API key)
if [ -f "$SCRIPT_DIR/.env" ]; then
    export $(grep -v '^#' "$SCRIPT_DIR/.env" | xargs)
fi

echo "$(date): Starting social pipeline" >> $LOG

cd "$SCRIPT_DIR"

# Step 1: Generate fresh content with MiniMax
echo "$(date): Generating content with MiniMax..." >> $LOG
TOPICS=("AI automation business" "build in public startup" "indie hacker tools" "passive income automation" "AI company 24/7")
TOPIC=${TOPICS[$RANDOM % ${#TOPICS[@]}]}

python3 "$SCRIPT_DIR/content_generator.py" --topic "$TOPIC" >> $LOG 2>&1

# Step 2: Post to Instagram + Threads
echo "$(date): Posting to IG + Threads..." >> $LOG
/usr/bin/python3 "$SCRIPT_DIR/auto_post_to_social.py" --platform both >> $LOG 2>&1

echo "$(date): Done." >> $LOG
