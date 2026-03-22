#!/usr/bin/env python3
"""
Live CRM with Tech Roles & Projects
Tracks leads, projects, and tech role assignments
"""
import os
import json
from datetime import datetime

CRM_FILE = "/tmp/company_crm.json"
PROJECTS_DIR = "/Users/macbookpro/.openclaw/workspace/company/projects"

# Tech roles
TECHS = {
    "CTO": {"role": "Technology & Architecture", "emoji": "🔧", "color": "#00FFFF"},
    "VP_Engineering": {"role": "Engineering Management", "emoji": "🤖", "color": "#7B2FF7"},
    "Tech_Lead": {"role": "Technical Decisions", "emoji": "💻", "color": "#FF6B6B"},
    "DevOps": {"role": "Infrastructure & CI/CD", "emoji": "🚀", "color": "#4ECDC4"},
    "Learning": {"role": "Research & Study", "emoji": "🎓", "color": "#FF0088"},
    "CEO": {"role": "Strategy & Decisions", "emoji": "👔", "color": "#FFD700"},
    "Sales": {"role": "Lead Generation", "emoji": "💰", "color": "#00D4FF"},
    "Marketing": {"role": "Content & Social", "emoji": "📢", "color": "#FF8800"},
}

def load_crm():
    if os.path.exists(CRM_FILE):
        with open(CRM_FILE, "r") as f:
            data = json.load(f)
            # Ensure all keys exist
            data.setdefault("leads", [])
            data.setdefault("activities", [])
            data.setdefault("pipeline", [])
            data.setdefault("tasks", [])
            data.setdefault("projects", [])
            data.setdefault("tech_tasks", [])
            return data
    return {"leads": [], "activities": [], "pipeline": [], "tasks": [], "projects": [], "tech_tasks": []}

def save_crm(data):
    with open(CRM_FILE, "w") as f:
        json.dump(data, f, indent=2)

def load_leads():
    if os.path.exists("/tmp/leads.json"):
        with open("/tmp/leads.json") as f:
            return json.load(f)
    return {"leads": []}

def load_projects():
    """Load all project files"""
    projects = []
    if os.path.exists(PROJECTS_DIR):
        for f in os.listdir(PROJECTS_DIR):
            if f.endswith(".md"):
                with open(os.path.join(PROJECTS_DIR, f)) as fp:
                    content = fp.read()
                    # Extract company name
                    name = f.replace(".md", "").replace("-", " ")
                    projects.append({"name": name, "file": f, "content": content[:500]})
    return projects

def add_activity(action, details):
    crm = load_crm()
    activity = {
        "id": len(crm["activities"]) + 1,
        "action": action,
        "details": details,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    crm["activities"].append(activity)
    crm["activities"] = crm["activities"][-50:]
    save_crm(crm)
    return activity

def assign_tech_task(project, tech_role, task, due=""):
    """Assign a task to a tech role"""
    crm = load_crm()
    task_item = {
        "id": len(crm["tech_tasks"]) + 1,
        "project": project,
        "tech_role": tech_role,
        "task": task,
        "status": "pending",
        "assigned": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "due": due
    }
    crm["tech_tasks"].append(task_item)
    save_crm(crm)
    return task_item

def get_dashboard():
    """Full dashboard with tech roles"""
    crm = load_crm()
    leads_data = load_leads()
    projects = load_projects()
    
    # Assignments by tech role
    tech_task_counts = {}
    for task in crm.get("tech_tasks", []):
        role = task.get("tech_role", "unknown")
        tech_task_counts[role] = tech_task_counts.get(role, 0) + 1
    
    return {
        "leads": len(leads_data.get("leads", [])),
        "projects": len(projects),
        "tech_roles": list(TECHS.keys()),
        "tech_task_counts": tech_task_counts,
        "recent_activities": crm["activities"][-10:],
        "pending_tasks": crm.get("tech_tasks", [])[-10:],
        "pipeline": crm.get("pipeline", [])
    }

def generate_crm_html():
    """Generate HTML dashboard with tech roles"""
    crm = load_crm()
    leads_data = load_leads()
    projects = load_projects()
    dashboard = get_dashboard()
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>EveryCompanyClaw CRM - Tech Roles Edition</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'SF Pro', sans-serif; background: #0a0a0f; color: #fff; padding: 20px; }}
        .header {{ text-align: center; padding: 20px; background: linear-gradient(135deg, #1a1a2e, #0d0d12); border-radius: 15px; margin-bottom: 20px; }}
        h1 {{ background: linear-gradient(90deg, #00ff88, #00d4ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
        .stats {{ display: flex; gap: 15px; justify-content: center; flex-wrap: wrap; margin-bottom: 20px; }}
        .stat-card {{ background: #151520; padding: 20px 30px; border-radius: 12px; text-align: center; min-width: 150px; }}
        .stat-num {{ font-size: 2em; font-weight: bold; color: #00ff88; }}
        .stat-label {{ color: #888; font-size: 0.9em; }}
        .section {{ background: #151520; border-radius: 12px; padding: 20px; margin-bottom: 20px; }}
        .section h2 {{ color: #00d4ff; margin-bottom: 15px; }}
        .tech-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; }}
        .tech-card {{ background: #1a1a2e; padding: 15px; border-radius: 10px; border-left: 4px solid; }}
        .tech-card.cto {{ border-color: #00FFFF; }}
        .tech-card.vp {{ border-color: #7B2FF7; }}
        .tech-card.lead {{ border-color: #FF6B6B; }}
        .tech-card.devops {{ border-color: #4ECDC4; }}
        .tech-card.learn {{ border-color: #FF0088; }}
        .tech-emoji {{ font-size: 1.5em; }}
        .tech-name {{ font-weight: bold; margin: 5px 0; }}
        .tech-role {{ color: #888; font-size: 0.8em; }}
        .tech-tasks {{ margin-top: 10px; padding-top: 10px; border-top: 1px solid #333; }}
        .task {{ background: #252535; padding: 5px 10px; border-radius: 5px; margin: 3px 0; font-size: 0.85em; }}
        .project-list {{ display: flex; flex-wrap: wrap; gap: 10px; }}
        .project {{ background: #252535; padding: 8px 15px; border-radius: 8px; font-size: 0.9em; }}
        .activity {{ background: #1a1a2e; padding: 10px; margin: 5px 0; border-radius: 8px; }}
        .activity-time {{ color: #666; font-size: 0.8em; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🏢 EveryCompanyClaw CRM</h1>
        <p>Tech Roles & Project Management | {datetime.now().strftime("%Y-%m-%d %H:%M")}</p>
    </div>
    
    <div class="stats">
        <div class="stat-card">
            <div class="stat-num">{len(leads_data.get("leads", []))}</div>
            <div class="stat-label">Real Leads</div>
        </div>
        <div class="stat-card">
            <div class="stat-num">{len(projects)}</div>
            <div class="stat-label">Projects</div>
        </div>
        <div class="stat-card">
            <div class="stat-num">{len(TECHS)}</div>
            <div class="stat-label">Tech Roles</div>
        </div>
        <div class="stat-card">
            <div class="stat-num">{len(crm.get("tech_tasks", []))}</div>
            <div class="stat-label">Tasks Assigned</div>
        </div>
    </div>
    
    <div class="section">
        <h2>🔧 Tech Roles Team</h2>
        <div class="tech-grid">
'''
    
    for role, info in TECHS.items():
        task_count = dashboard.get("tech_task_counts", {}).get(role, 0)
        html += f'''            <div class="tech-card {role.lower()[:2]}">
                <div class="tech-emoji">{info['emoji']}</div>
                <div class="tech-name">{role}</div>
                <div class="tech-role">{info['role']}</div>
                <div class="tech-tasks">
                    <div class="task">{task_count} tasks assigned</div>
                </div>
            </div>
'''
    
    html += '''        </div>
    </div>
    
    <div class="section">
        <h2>📁 Active Projects</h2>
        <div class="project-list">
'''
    
    for p in projects[:15]:
        html += f'            <div class="project">{p["name"][:30]}</div>\n'
    
    html += '''        </div>
    </div>
    
    <div class="section">
        <h2>⚡ Recent Activities</h2>
'''
    
    for act in crm.get("activities", [])[-10:]:
        html += f'''        <div class="activity">
            <div class="activity-time">[{act.get("time", "")}]</div>
            <div>{act.get("action", "")}: {act.get("details", "")[:50]}</div>
        </div>
'''
    
    html += '''    </div>
</body>
</html>'''
    
    with open("/Users/macbookpro/.openclaw/workspace/company/crm-dashboard.html", "w") as f:
        f.write(html)
    return html

if __name__ == "__main__":
    # Initialize
    crm = load_crm()
    
    # Add tech role tasks from projects
    projects = load_projects()
    
    if not crm.get("tech_tasks"):
        print("🎯 Assigning tech role tasks to projects...")
        
        for project in projects[:10]:
            name = project["name"]
            # Assign tasks to different tech roles
            assign_tech_task(name, "CTO", f"Evaluate technical feasibility for {name}")
            assign_tech_task(name, "Tech_lead", f"Research tech stack for {name}")
            assign_tech_task(name, "Learning", f"Study {name} technology")
            assign_tech_task(name, "DevOps", f"Design deployment strategy for {name}")
        
        print(f"✅ Assigned tasks to {len(projects[:10])} projects")
    
    # Generate HTML
    generate_crm_html()
    print("✅ CRM Dashboard updated with tech roles!")
    print(f"📊 {get_dashboard()}")