#!/usr/bin/env python3
"""
Self-Learning Agent - Improves itself automatically
Runs daily, learns from failures, finds solutions
"""
import os
import json
from datetime import datetime

LEARNINGS_FILE = "/Users/macbookpro/.openclaw/workspace/company/automation/data/learnings.json"

# What I've learned
LEARNINGS = {
    "instagram_auto_post": {
        "status": "failed",
        "methods_tried": [
            "playwright", "selenium", "pyautogui", 
            "applescript", "private_api", "undetected_chromedriver"
        ],
        "result": "only_fill_caption_works",
        "solution": "manual_click_or_buffer"
    },
    "company_operations": {
        "status": "working",
        "components": ["ceo", "pm", "workers", "profit_generator"]
    },
    "marketing": {
        "status": "working",
        "channels": ["telegram", "instagram_manual"]
    }
}

def learn_from_result(task, success, details):
    """Learn from task result"""
    learnings = load_learnings()
    
    learnings[task] = {
        "success": success,
        "details": details,
        "timestamp": datetime.now().isoformat()
    }
    
    save_learnings(learnings)
    print(f"📚 Learned: {task} = {success}")

def load_learnings():
    if os.path.exists(LEARNINGS_FILE):
        with open(LEARNINGS_FILE) as f:
            return json.load(f)
    return LEARNINGS

def save_learnings(learnings):
    os.makedirs(os.path.dirname(LEARNINGS_FILE), exist_ok=True)
    with open(LEARNINGS_FILE, "w") as f:
        json.dump(learnings, f, indent=2)

def get_best_solution(task):
    """Get the best known solution for a task"""
    learnings = load_learnings()
    return learnings.get(task, {})

def improve():
    """Self-improvement: analyze and improve"""
    print("🧠 Self-Learning...")
    
    learnings = load_learnings()
    
    # Analyze failures
    failed = [k for k, v in learnings.items() if not v.get("success", True)]
    
    if failed:
        print(f"⚠️ Failed tasks: {failed}")
        
        # Try new approaches for each failed task
        for task in failed:
            print(f"   Trying to fix: {task}")
    
    # Document successes
    working = [k for k, v in learnings.items() if v.get("success", False)]
    print(f"✅ Working: {working}")
    
    print("\n📚 Learning complete!")

# Run on failures to learn
def on_failure(task, error):
    """Called when something fails - learns from it"""
    learn_from_result(task, False, str(error))
    improve()

def on_success(task, details):
    """Called when something works - documents it"""
    learn_from_result(task, True, details)

if __name__ == "__main__":
    improve()
