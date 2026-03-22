#!/usr/bin/env python3
"""
Agent Team System - Real Tech Company Structure
"""
import os
import json
from datetime import datetime

# Agent definitions
AGENTS = {
    "CEO": {
        "name": "CEO Agent",
        "role": "Strategy & Decision Making",
        "emoji": "👔",
        "color": "#FFD700",
        "current_task": "Company Vision & Strategy",
        "reports_to": "Board (You)",
        "team": []
    },
    "CTO": {
        "name": "CTO Agent",
        "role": "Technology & Architecture",
        "emoji": "🔧",
        "color": "#00FFFF",
        "current_task": "Tech Stack & Architecture",
        "reports_to": "CEO",
        "team": ["Tech Lead", "Senior Engineer", "DevOps"]
    },
    "CFO": {
        "name": "CFO Agent", 
        "role": "Finance & Analytics",
        "emoji": "📊",
        "color": "#00FF88",
        "current_task": "Financial Planning & Tracking",
        "reports_to": "CEO",
        "team": []
    },
    "VP_Engineering": {
        "name": "VP Engineering",
        "role": "Engineering Management",
        "emoji": "🤖",
        "color": "#7B2FF7",
        "current_task": "Project Management & Code Review",
        "reports_to": "CTO",
        "team": ["Backend Lead", "Frontend Lead", "QA Lead"]
    },
    "Tech_Lead": {
        "name": "Tech Lead",
        "role": "Technical Decisions",
        "emoji": "💻",
        "color": "#FF6B6B",
        "current_task": "Code Architecture & Best Practices",
        "reports_to": "VP_Engineering",
        "team": ["Senior Dev", "Junior Dev"]
    },
    "DevOps": {
        "name": "DevOps Engineer",
        "role": "Infrastructure & CI/CD",
        "emoji": "🚀",
        "color": "#4ECDC4",
        "current_task": "Docker, Deployments, Automation",
        "reports_to": "VP_Engineering",
        "team": []
    },
    "Sales": {
        "name": "Sales Agent",
        "role": "Lead Generation & Pipeline",
        "emoji": "💰",
        "color": "#00D4FF",
        "current_task": "Lead Gen & Outreach",
        "reports_to": "CEO",
        "team": ["SDR", "Account Executive", "Sales Development"]
    },
    "Marketing": {
        "name": "Marketing Agent",
        "role": "Content & Social Media",
        "emoji": "📢",
        "color": "#FF8800",
        "current_task": "Social Media & Content",
        "reports_to": "CEO",
        "team": ["Content Creator", "Social Media Manager", "SEO Specialist"]
    },
    "Operations": {
        "name": "Operations Agent",
        "role": "Daily Operations & Automation",
        "emoji": "🛠️",
        "color": "#7B2FF7",
        "current_task": "System Maintenance & Cron Jobs",
        "reports_to": "CEO",
        "team": ["System Admin", "Process Automation", "Data Manager"]
    },
    "Learning": {
        "name": "Learning Agent",
        "role": "Self-Improvement & Research",
        "emoji": "🎓",
        "color": "#FF0088",
        "current_task": "Research & Skill Building",
        "reports_to": "CTO",
        "team": ["Researcher", "Pattern Analyzer", "Strategy Learner"]
    }
}

def get_current_status():
    """Get current status from running systems"""
    
    # Learning stats
    learn_state = {"topics_done": [], "actions_done": []}
    try:
        with open("/tmp/learn_state.json", "r") as f:
            learn_state = json.load(f)
    except:
        pass
    
    # Lead/Pipeline stats
    leads = {"leads": []}
    pipeline = {"deals": []}
    try:
        with open("/tmp/leads.json", "r") as f:
            leads = json.load(f)
    except:
        pass
    try:
        with open("/tmp/sales_pipeline.json", "r") as f:
            pipeline = json.load(f)
    except:
        pass
    
    # Update agent statuses based on real data
    AGENTS["Learning"]["current_task"] = f"Learning: {learn_state.get('topics_done', [])[-1] if learn_state.get('topics_done') else 'None'}"
    AGENTS["Learning"]["stats"] = {
        "topics": len(learn_state.get("topics_done", [])),
        "actions": len(learn_state.get("actions_done", []))
    }
    
    AGENTS["Sales"]["current_task"] = f"Lead Gen: {len(leads.get('leads', []))} leads, {len(pipeline.get('deals', []))} deals"
    AGENTS["Sales"]["stats"] = {
        "leads": len(leads.get("leads", [])),
        "deals": len(pipeline.get("deals", []))
    }
    
    AGENTS["Marketing"]["current_task"] = "Social Media & Content Creation"
    AGENTS["Marketing"]["stats"] = {"posts": "Daily"}
    
    AGENTS["Operations"]["current_task"] = "Cron Jobs & System Maintenance"
    AGENTS["Operations"]["stats"] = {"jobs": "8 active"}
    
    AGENTS["CFO"]["current_task"] = "Financial Analytics"
    AGENTS["CFO"]["stats"] = {"revenue": "$0", "pipeline_value": "$0"}
    
    AGENTS["CTO"]["current_task"] = "Tech Stack & Architecture"
    AGENTS["CTO"]["stats"] = {"projects": 5, "team": 3}
    
    AGENTS["VP_Engineering"]["current_task"] = "Managing Engineering Projects"
    AGENTS["VP_Engineering"]["stats"] = {"open_prs": 0, "bugs": 0}
    
    AGENTS["Tech_Lead"]["current_task"] = "Code Reviews & Architecture"
    AGENTS["Tech_Lead"]["stats"] = {"code_quality": "Good"}
    
    AGENTS["DevOps"]["current_task"] = "CI/CD & Infrastructure"
    AGENTS["DevOps"]["stats"] = {"uptime": "99.9%", "deploys": "Auto"}
    
    AGENTS["CEO"]["current_task"] = "Company Strategy & Vision"
    AGENTS["CEO"]["stats"] = {"team_size": 10, "autonomy": "100%"}

def generate_org_chart():
    """Generate HTML org chart"""
    get_current_status()
    
    html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EveryCompanyClaw - Company Org Chart</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'SF Pro Display', -apple-system, sans-serif;
            background: #0a0a0f;
            min-height: 100vh;
            color: #fff;
            padding: 20px;
        }
        
        .header {
            text-align: center;
            padding: 30px;
            background: linear-gradient(135deg, #1a1a2e 0%, #0d0d12 100%);
            border-radius: 20px;
            margin-bottom: 30px;
        }
        
        h1 {
            font-size: 2.5em;
            background: linear-gradient(90deg, #00ff88, #00d4ff, #7b2ff7);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .subtitle { color: #666; margin-top: 10px; }
        
        .org-chart {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 40px;
        }
        
        .level {
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
            justify-content: center;
        }
        
        .agent-card {
            background: #151520;
            border-radius: 16px;
            padding: 20px;
            min-width: 200px;
            text-align: center;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
            transition: transform 0.3s, box-shadow 0.3s;
            border: 2px solid transparent;
        }
        
        .agent-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 30px rgba(0,0,0,0.5);
        }
        
        .emoji { font-size: 2.5em; margin-bottom: 10px; }
        
        .name { font-size: 1.2em; font-weight: bold; margin-bottom: 5px; }
        
        .role { color: #888; font-size: 0.9em; margin-bottom: 10px; }
        
        .task {
            background: #1a1a2e;
            padding: 8px 12px;
            border-radius: 8px;
            font-size: 0.85em;
            color: #aaa;
            margin-bottom: 10px;
        }
        
        .stats {
            display: flex;
            gap: 10px;
            justify-content: center;
            flex-wrap: wrap;
        }
        
        .stat {
            background: #252535;
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 0.8em;
            color: #00ff88;
        }
        
        .team-badge {
            margin-top: 10px;
            padding-top: 10px;
            border-top: 1px solid #333;
        }
        
        .team-label { color: #555; font-size: 0.75em; }
        
        .team-members {
            display: flex;
            gap: 5px;
            flex-wrap: wrap;
            justify-content: center;
            margin-top: 5px;
        }
        
        .team-member {
            background: #333;
            padding: 2px 8px;
            border-radius: 10px;
            font-size: 0.7em;
            color: #aaa;
        }
        
        .connector {
            width: 2px;
            height: 20px;
            background: #333;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🏢 EveryCompanyClaw</h1>
        <p class="subtitle">AI-Powered CompanyOrg Chart | ''' + datetime.now().strftime("%Y-%m-%d %H:%M") + '''</p>
    </div>
    
    <div class="org-chart">
'''
    
    # Level 1: CEO
    html += '        <div class="level">\n'
    for agent_id in ["CEO"]:
        a = AGENTS[agent_id]
        html += f'''        <div class="agent-card" style="border-color: {a['color']}">
            <div class="emoji">{a['emoji']}</div>
            <div class="name">{a['name']}</div>
            <div class="role">{a['role']}</div>
            <div class="task">{a['current_task']}</div>
            <div class="stats">
'''
        for stat, val in a.get("stats", {}).items():
            html += f'                <span class="stat">{stat}: {val}</span>\n'
        html += '''            </div>
        </div>
'''
    html += '        </div>\n'
    
    # Connector
    html += '        <div class="connector"></div>\n'
    
    # Level 2: CTO, CFO, Sales, Marketing, Operations
    html += '        <div class="level">\n'
    for agent_id in ["CTO", "CFO", "Sales", "Marketing", "Operations"]:
        a = AGENTS[agent_id]
        html += f'''        <div class="agent-card" style="border-color: {a['color']}">
            <div class="emoji">{a['emoji']}</div>
            <div class="name">{a['name']}</div>
            <div class="role">{a['role']}</div>
            <div class="task">{a['current_task']}</div>
            <div class="stats">
'''
        for stat, val in a.get("stats", {}).items():
            html += f'                <span class="stat">{stat}: {val}</span>\n'
        html += '''            </div>
        </div>
'''
    html += '        </div>\n'
    
    # Connector
    html += '        <div class="connector"></div>\n'
    
    # Level 3: More tech roles
    html += '        <div class="level">\n'
    for agent_id in ["VP_Engineering", "DevOps", "Learning"]:
        a = AGENTS[agent_id]
        html += f'''        <div class="agent-card" style="border-color: {a['color']}">
            <div class="emoji">{a['emoji']}</div>
            <div class="name">{a['name']}</div>
            <div class="role">{a['role']}</div>
            <div class="task">{a['current_task']}</div>
            <div class="stats">
'''
        for stat, val in a.get("stats", {}).items():
            html += f'                <span class="stat">{stat}: {val}</span>\n'
        
        if a.get("team"):
            html += '''            <div class="team-badge">
                <div class="team-label">Reports to: ''' + a['reports_to'] + '''</div>
                <div class="team-members">
'''
            for member in a["team"]:
                html += f'                    <span class="team-member">{member}</span>\n'
            html += '''                </div>
            </div>
'''
        
        html += '''        </div>
'''
    html += '        </div>\n'
    
    html += '''    </div>
</body>
</html>'''
    
    return html

if __name__ == "__main__":
    html = generate_org_chart()
    with open("/Users/macbookpro/.openclaw/workspace/company/org-chart.html", "w") as f:
        f.write(html)
    print("✅ Org chart updated with tech roles!")