#!/bin/bash
# Sync OpenClaw workspace docs to GitHub repo
# Run this whenever workspace docs change

OPENCLAW_DIR="$HOME/.openclaw/company"
REPO_DIR="$HOME/company-automation-sync"
TARGET_BRANCH="openclaw-integration"

echo "Syncing OpenClaw workspace → GitHub..."

# Pull latest from GitHub
git -C "$REPO_DIR" pull origin "$TARGET_BRANCH" 2>/dev/null

# Copy key docs
cp "$OPENCLAW_DIR/MEMORY.md" "$REPO_DIR/openclaw-workspace/"
cp "$OPENCLAW_DIR/COMPANY.md" "$REPO_DIR/openclaw-workspace/"
cp "$OPENCLAW_DIR/memory/daily/$(date +%Y-%m-%d).md" "$REPO_DIR/openclaw-workspace/daily-log-$(date +%Y-%m-%d).md" 2>/dev/null

# Commit and push
cd "$REPO_DIR"
git add openclaw-workspace/
git commit -m "OpenClaw workspace sync $(date '+%Y-%m-%d %H:%M')" 2>/dev/null
git push origin "$TARGET_BRANCH" 2>/dev/null

echo "Sync complete."
