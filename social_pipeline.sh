#!/bin/bash
# MiniMax Social Pipeline — Generate content + post to IG + Threads
# Runs every 6 hours via cron

LOG="/tmp/social_pipeline.log"
echo "$(date): Starting social pipeline" >> $LOG

cd /tmp/company-automation

# Step 1: Generate fresh content with MiniMax
echo "$(date): Generating content..." >> $LOG
TOPICS=("AI automation" "build in public startup" "indie hacker tools" "passive income automation" "AI company")
TOPIC=${TOPICS[$RANDOM % ${#TOPICS[@]}]}

python3 /tmp/company-automation/content_generator.py --topic "$TOPIC" >> $LOG 2>&1

# Step 2: Post to Instagram + Threads
echo "$(date): Posting to IG + Threads..." >> $LOG
/usr/bin/python3 /tmp/company-automation/auto_post_to_social.py --platform both >> $LOG 2>&1

echo "$(date): Done." >> $LOG
