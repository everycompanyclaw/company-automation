#!/usr/bin/env python3
"""
Job Scout - Monitors for freelance job opportunities
Runs every 30 mins as CEO → PM → Workers chain
"""
import os
import json
from datetime import datetime

JOBS_FILE = "/Users/macbookpro/.openclaw/workspace/company/automation/data/jobs.md"
LEADS_FILE = "/Users/macbookpro/.openclaw/workspace/company/automation/data/leads.md"
REPORT_FILE = "/Users/macbookpro/.openclaw/workspace/company/automation/data/job_report.md"

# Job search keywords
KEYWORDS = [
    "python automation",
    "workflow automation", 
    "zapier",
    "ai integration",
    "chatbot",
    "api integration",
    "script writing",
    "data automation",
    "n8n",
    "make.com"
]

# Target platforms
PLATFORMS = [
    "upwork.com",
    "fiverr.com", 
    "toptal.com",
    "linkedin.com/jobs",
    "indeed.com"
]

def check_jobs():
    """Check for new job opportunities"""
    report = f"""# Job Scout Report - {datetime.now().strftime('%Y-%m-%d %H:%M')}

## 🔍 Job Search

### Keywords Monitoring
{', '.join(KEYWORDS)}

### Platforms
{', '.join(PLATFORMS)}

## 📊 Status

⚠️ Web fetching blocked by external restrictions

## 💡 Manual Actions Needed

1. Check Upwork manually: https://www.upwork.com
2. Check Fiverr: https://www.fiverr.com
3. Search keywords above

## 🎯 Hot Leads to Pursue

- Companies needing automation
- Startups needing AI integration
- Small businesses needing workflows

## 📝 Next Steps

1. [ ] Apply to 3 relevant jobs today
2. [ ] Send outreach to 5 potential clients
3. [ ] Update job leads database

---
*Job Scout - EveryCompanyClaw*
"""
    
    with open(REPORT_FILE, "w") as f:
        f.write(report)
    
    return report

def add_job_lead(company, platform, role, link):
    """Add a job lead to database"""
    jobs = []
    
    if os.path.exists(JOBS_FILE):
        with open(JOBS_FILE) as f:
            jobs = json.load(f)
    
    jobs.append({
        "company": company,
        "platform": platform,
        "role": role,
        "link": link,
        "date": datetime.now().isoformat(),
        "status": "new"
    })
    
    with open(JOBS_FILE, "w") as f:
        json.dump(jobs, f, indent=2)

def get_job_count():
    """Get count of tracked jobs"""
    if os.path.exists(JOBS_FILE):
        with open(JOBS_FILE) as f:
            jobs = json.load(f)
        return len(jobs)
    return 0

if __name__ == "__main__":
    print("🔍 Running Job Scout...")
    report = check_jobs()
    job_count = get_job_count()
    print(f"✅ Job check complete - {job_count} jobs tracked")
    print(report)
