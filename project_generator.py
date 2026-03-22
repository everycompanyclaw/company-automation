#!/usr/bin/env python3
"""
Project Generator - Research leads and create projects
Uses tech roles to evaluate each lead
"""
import os
import json
import re
from datetime import datetime

LEADS_FILE = "/tmp/leads.json"
PROJECTS_DIR = "/Users/macbookpro/.openclaw/workspace/company/projects"

# Tech roles definitions
TECHS = {
    "CTO": {
        "role": "Technology & Architecture",
        "emoji": "🔧",
        "focus": ["Technical feasibility", "Architecture design", "Tech stack decisions"]
    },
    "VP_Engineering": {
        "role": "Engineering Management",
        "emoji": "🤖",
        "focus": ["Project planning", "Code reviews", "Team coordination"]
    },
    "Tech_Lead": {
        "role": "Technical Decisions",
        "emoji": "💻",
        "focus": ["Code quality", "Best practices", "API design"]
    },
    "DevOps": {
        "role": "Infrastructure & CI/CD",
        "emoji": "🚀",
        "focus": ["Deployment", "Monitoring", "Automation"]
    },
    "Learning": {
        "role": "Research & Study",
        "emoji": "🎓",
        "focus": ["Learn tech", "Document findings", "Identify opportunities"]
    }
}

def load_leads():
    with open(LEADS_FILE) as f:
        return json.load(f)

def generate_project(lead, index):
    """Generate a project research doc for a lead"""
    company = lead.get("company", "Unknown")[:50]
    source = lead.get("source", "unknown")
    email = lead.get("email", "")
    
    # Generate research description based on source
    if source == "github":
        desc = f"GitHub project: {company}. Research their tech stack and find integration opportunities."
        opportunity = "Build integration, create plugins, or offer consulting services."
    elif source == "hackernews":
        desc = f"Hacker News trending: {company}. Research the technology and business potential."
        opportunity = "Identify partnerships or replication opportunities."
    else:
        desc = f"Lead from {source}: {company}"
        opportunity = "Explore business opportunity."
    
    # Build tech role assignments
    tech_assignments = []
    for role, info in TECHS.items():
        focus = info["focus"][index % len(info["focus"])]
        tech_assignments.append(f"## {info['emoji']} {role} - {info['role']}\n- Focus: {focus}")
    
    project = f"""# Project Research: {company}

## Lead Info
- **Company/Project**: {company}
- **Source**: {source}
- **Email**: {email}
- **Research Date**: {datetime.now().strftime("%Y-%m-%d %H:%M")}

## Research
{desc}

## Business Opportunity
{opportunity}

## Tech Role Assignments

{chr(10).join(tech_assignments)}

## Next Steps
- [ ] CTO: Evaluate technical feasibility
- [ ] Tech Lead: Research tech stack
- [ ] Learning: Study their technology
- [ ] VP Engineering: Plan project scope
- [ ] DevOps: Design deployment strategy
"""
    return project

def main():
    # Ensure projects dir exists
    os.makedirs(PROJECTS_DIR, exist_ok=True)
    
    # Load leads
    leads = load_leads()
    lead_list = leads.get("leads", [])
    
    print(f"🎯 Generating projects for {len(lead_list)} leads...")
    
    # Generate project for each lead
    for i, lead in enumerate(lead_list):
        company = lead.get("company", "unknown")[:30].replace(" ", "-")
        
        # Clean filename
        company = re.sub(r'[^a-zA-Z0-9_-]', '', company)
        
        project_file = os.path.join(PROJECTS_DIR, f"{company}.md")
        
        # Generate if not exists
        if not os.path.exists(project_file):
            project = generate_project(lead, i)
            with open(project_file, "w") as f:
                f.write(project)
            print(f"✅ Created: {company}.md")
        else:
            print(f"⏭️  Skipped: {company}.md (exists)")
    
    print(f"\n📊 Generated projects in {PROJECTS_DIR}")

if __name__ == "__main__":
    main()