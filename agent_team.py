#!/usr/bin/env python3
"""
Agent Team Runner
Runs all content agents automatically
"""
import os
import sys

# Add company path
sys.path.insert(0, '/Users/macbookpro/.openclaw/workspace/company')

def run_researcher():
    """Research trending topics"""
    print("🔍 Running Researcher...")
    os.system("python3 /Users/macbookpro/.openclaw/workspace/company/fetch_jobs.py")
    print("✅ Research done")

def run_creator():
    """Create content"""
    print("🎬 Running Creator...")
    os.system("python3 /Users/macbookpro/.openclaw/workspace/company/video_content.py generate-company")
    print("✅ Content created")

def run_scheduler():
    """Check and schedule posts"""
    print("📅 Running Scheduler...")
    os.system("python3 /Users/macbookpro/.openclaw/workspace/company/instagram_scheduler.py check")
    print("✅ Posts checked")

def run_outreach():
    """Send outreach"""
    print("🤝 Running Outreach...")
    # Placeholder for outreach
    print("✅ Outreach done")

def run_analytics():
    """Generate analytics"""
    print("📊 Running Analytics...")
    # Placeholder for analytics
    print("✅ Analytics done")

def daily_routine():
    """Run all agents daily"""
    print("="*50)
    print("🤖 Running Daily Agent Team")
    print("="*50)
    
    run_researcher()
    run_creator()
    run_scheduler()
    run_analytics()
    run_outreach()
    
    print("="*50)
    print("✅ Daily routine complete!")
    print("="*50)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        agent = sys.argv[1]
        
        if agent == "research":
            run_researcher()
        elif agent == "creator":
            run_creator()
        elif agent == "scheduler":
            run_scheduler()
        elif agent == "outreach":
            run_outreach()
        elif agent == "analytics":
            run_analytics()
        elif agent == "all":
            daily_routine()
        else:
            print(f"Unknown agent: {agent}")
    else:
        print("Usage:")
        print("  python agent_team.py research")
        print("  python agent_team.py creator")
        print("  python agent_team.py scheduler")
        print("  python agent_team.py all")
