#!/bin/bash
# Social Pipeline — Different content for Threads vs IG
# Threads: @milo_chen018 (personal) — different CN content
# Instagram: @everycompanyclaw (company) — different content
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
MINIMAX_API_KEY="$MINIMAX_API_KEY" python3 "$SCRIPT_DIR/content_generator.py" --topic "$TOPIC" >> $LOG 2>&1

# Load generated posts
if [ -f "$SCRIPT_DIR/generated_posts.json" ]; then
    THREADS_POST=$(python3 -c "import json; print(json.load(open('$SCRIPT_DIR/generated_posts.json'))['threads'])")
    IG_POST=$(python3 -c "import json; print(json.load(open('$SCRIPT_DIR/generated_posts.json'))['instagram'])")
else
    echo "$(date): No generated posts found, using fallback" >> $LOG
    exit 1
fi

# Step 2: Post to Instagram (company @everycompanyclaw) — IG API
echo "$(date): Posting to Instagram (@everycompanyclaw)..." >> $LOG
IG_IMAGE_URL="https://raw.githubusercontent.com/everycompanyclaw/company-automation/openclaw-integration/pixel-cat-pixar.png"
python3 "$SCRIPT_DIR/ig_api_poster.py" "/tmp/ig_caption.txt" "$IG_IMAGE_URL" 2>&1 || echo "IG post failed" >> $LOG

# Step 3: Post to Threads (@milo_chen018) — different CN content
echo "$(date): Posting to Threads (@milo_chen018)..." >> $LOG
TOKEN=$(cat "$SCRIPT_DIR/.threads_token" 2>/dev/null)
if [ -n "$TOKEN" ]; then
    echo "$THREADS_POST" > /tmp/threads_caption.txt
    RESULT=$(curl -s -X POST "https://graph.threads.net/me/threads" \
        -d "access_token=$TOKEN" \
        -d "media_type=text" \
        -d "text=$THREADS_POST")
    echo "Threads result: $RESULT" >> $LOG
else
    echo "No Threads token found" >> $LOG
fi

# Send notification to MK
python3 "$SCRIPT_DIR/daily_report.py" >> $LOG 2>&1

echo "$(date): Done." >> $LOG
