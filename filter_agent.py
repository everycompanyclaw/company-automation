#!/usr/bin/env python3
"""
Subagent: Message Filter Agent
Determines if messages should be forwarded to main chat
Only forwards IMPORTANT messages
"""
import json
import sys

def analyze_message(message_data):
    """Use AI reasoning to decide if message is important"""
    
    content = message_data.get("content", "").lower()
    source = message_data.get("source", "unknown")
    
    # HIGH priority - ALWAYS forward these
    high_priority_triggers = [
        "error", "failed", "critical", "alert",
        "approved", "deal closed", "revenue",
        "security", "breach", "down"
    ]
    
    # FILTER OUT - Routine noise patterns
    noise_patterns = [
        "heartbeat", "all systems running", "batch processing",
        "cron completed", "running normally", "check complete",
        "no action needed", "nothing new", "dashboard updated",
        "generated successfully", "✅", "completed successfully",
        "check complete", "all good"
    ]
    
    # Check if it's noise first
    is_noise = False
    for pattern in noise_patterns:
        if pattern in content:
            is_noise = True
            break
    
    if is_noise:
        return {
            "forward": False,
            "priority": "NONE",
            "reason": "Routine bot message - filtered out",
            "message": ""
        }
    
    # Check high priority triggers
    for trigger in high_priority_triggers:
        if trigger in content:
            return {
                "forward": True,
                "priority": "HIGH",
                "reason": f"Important: {trigger}",
                "message": message_data.get("content", "")[:200]
            }
    
    # Check for significant business updates
    important_context = ["new lead", "leads generated", "posted to", "sale", "pipeline", "revenue", "deal"]
    for trigger in important_context:
        if trigger in content:
            return {
                "forward": True,
                "priority": "MEDIUM",
                "reason": f"Business update: {trigger}",
                "message": message_data.get("content", "")[:200]
            }
    
    # Default: don't forward (reduce noise)
    return {
        "forward": False,
        "priority": "NONE",
        "reason": "Routine update - filtered",
        "message": ""
    }

if __name__ == "__main__":
    # Read message from args
    if len(sys.argv) > 1:
        message = {"content": sys.argv[1], "source": "cli"}
    else:
        message = {"content": "No message provided", "source": "unknown"}
    
    result = analyze_message(message)
    
    if result["forward"]:
        print(f"✅ FORWARD: {result['reason']}")
        print(f"   Message: {result['message'][:100]}")
    else:
        print(f"🚫 FILTERED: {result['reason']}")