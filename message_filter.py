#!/usr/bin/env python3
"""
Message Filter - Uses AI to decide if messages should be forwarded
"""
import json
import os
from datetime import datetime

# Store recent messages
MESSAGE_LOG = "/tmp/message_filter_log.json"
RECENT_FILE = "/tmp/recent_messages.json"

# Decision criteria
IMPORTANT_TRIGGERS = [
    "error", "failed", "critical", "urgent", "alert",
    "leads", "deal", "sale", "revenue", "pipeline",
    "completed", "success", "approved", "new"
]

def load_recent_messages():
    """Load recent messages from bots"""
    if os.path.exists(RECENT_FILE):
        with open(RECENT_FILE) as f:
            return json.load(f)
    return {"messages": []}

def should_forward(message):
    """Decide if message should be forwarded to main chat"""
    msg_lower = message.lower()
    
    # Check for important triggers
    for trigger in IMPORTANT_TRIGGERS:
        if trigger in msg_lower:
            return True, f"Contains: {trigger}"
    
    # Check message length (short = likely important)
    if len(message) < 100:
        return True, "Short message"
    
    # Default: don't forward (reduce noise)
    return False, "Routine message"

def log_decision(message, decision, reason):
    """Log the decision for learning"""
    log = {
        "timestamp": datetime.now().isoformat(),
        "message": message[:200],
        "forwarded": decision,
        "reason": reason
    }
    
    if os.path.exists(MESSAGE_LOG):
        with open(MESSAGE_LOG) as f:
            data = json.load(f)
    else:
        data = {"logs": []}
    
    data["logs"].append(log)
    data["logs"] = data["logs"][-100:]  # Keep last 100
    
    with open(MESSAGE_LOG, "w") as f:
        json.dump(data, f, indent=2)

def filter_messages():
    """Main filter function"""
    messages = load_recent_messages()
    
    to_forward = []
    
    for msg in messages.get("messages", []):
        content = msg.get("content", "")
        decision, reason = should_forward(content)
        
        log_decision(content, decision, reason)
        
        if decision:
            to_forward.append({
                "content": content,
                "source": msg.get("source", "unknown"),
                "reason": reason
            })
    
    return to_forward

def check_and_forward():
    """Check messages and return what should be forwarded"""
    to_forward = filter_messages()
    
    if to_forward:
        print(f"📬 Found {len(to_forward)} important messages to forward")
        for msg in to_forward:
            print(f"  - [{msg['source']}] {msg['reason']}")
    else:
        print("✅ No important messages to forward")
    
    return to_forward

if __name__ == "__main__":
    check_and_forward()