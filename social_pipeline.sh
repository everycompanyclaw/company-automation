#!/bin/bash
# MiniMax Social Pipeline — Generate content + post to IG + Threads
# Runs daily at 7 PM via cron

LOG="/tmp/social_pipeline.log"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Load env vars
if [ -f "$SCRIPT_DIR/.env" ]; then
    set -a
    source "$SCRIPT_DIR/.env"
    set +a
fi

echo "$(date): Starting social pipeline" >> $LOG

cd "$SCRIPT_DIR"

# Step 1: Generate fresh content with MiniMax
echo "$(date): Generating content..." >> $LOG
TOPICS=("AI automation business" "build in public startup" "indie hacker tools" "passive income automation" "AI company 24/7")
TOPIC=${TOPICS[$RANDOM % ${#TOPICS[@]}]}
python3 "$SCRIPT_DIR/content_generator.py" --topic "$TOPIC" >> $LOG 2>&1

# Load generated posts
if [ -f "$SCRIPT_DIR/generated_posts.json" ]; then
    THREADS_POST=$(python3 -c "import json; print(json.load(open('$SCRIPT_DIR/generated_posts.json'))['threads'])")
    IG_POST=$(python3 -c "import json; print(json.load(open('$SCRIPT_DIR/generated_posts.json'))['instagram'])")
else
    echo "$(date): No generated posts found" >> $LOG
    exit 1
fi

# Step 2: Post to Instagram (Playwright) + Threads (API)
echo "$(date): Posting to Instagram (Playwright)..." >> $LOG
/usr/bin/python3 "$SCRIPT_DIR/auto_post_to_social.py" --platform instagram --content "$IG_POST" >> $LOG 2>&1

echo "$(date): Posting to Threads (API)..." >> $LOG
python3 "$SCRIPT_DIR/threads_api_poster.py" --post "$THREADS_POST" >> $LOG 2>&1

echo "$(date): Done." >> $LOG
