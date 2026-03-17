#!/bin/bash
# Spawn the right agent for a task

TASK="$1"

# Auto-select agent based on task
if [[ "$TASK" == *"lead"* || "$TASK" == *"sales"* || "$TASK" == *"customer"* ]]; then
    MODEL="opus"
    echo "💼 Spawning Sales Agent..."
elif [[ "$TASK" == *"build"* || "$TASK" == *"code"* || "$TASK" == *"develop"* || "$TASK" == *"create"* ]]; then
    MODEL="opus"
    echo "💻 Spawning Developer Agent..."
elif [[ "$TASK" == *"plan"* || "$TASK" == *"strategy"* || "$TASK" == *"decision"* ]]; then
    MODEL="opus"
    echo "🤖 Spawning CEO Agent..."
elif [[ "$TASK" == *"research"* || "$TASK" == *"analyze"* || "$TASK" == *"report"* ]]; then
    MODEL="opus"
    echo "📊 Spawning Analyst Agent..."
elif [[ "$TASK" == *"help"* || "$TASK" == *"support"* || "$TASK" == *"question"* ]]; then
    MODEL="minimax"
    echo "🎧 Spawning Support Agent..."
else
    MODEL="minimax"
    echo "⚙️ Spawning Operations Agent..."
fi

# Spawn with Claude Code
/Users/macbookpro/.local/bin/claude -p --model $MODEL "$TASK"
