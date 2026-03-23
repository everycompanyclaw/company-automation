#!/usr/bin/env python3
"""
Startup Automation MVP
AI-powered automation for startups
"""
import os
import json
from datetime import datetime

CONFIG_FILE = "/tmp/startup_automation_config.json"

# Core features for startups
FEATURES = {
    "lead_gen": {
        "name": "Lead Generation",
        "description": "Automated lead scraping from GitHub, HN, etc.",
        "status": "active",
        "leads_collected": 0
    },
    "email_outreach": {
        "name": "Email Outreach", 
        "description": "Automated cold email campaigns",
        "status": "active",
        "emails_sent": 0
    },
    "social_posting": {
        "name": "Social Media Posting",
        "description": "Auto-post to Instagram, LinkedIn, Twitter",
        "status": "active",
        "posts_published": 0
    },
    "crm": {
        "name": "CRM",
        "description": "Track leads and deals pipeline",
        "status": "active",
        "deals": 0
    },
    "analytics": {
        "name": "Analytics",
        "description": "Track performance and ROI",
        "status": "active"
    }
}

def initialize_startup_config():
    """Initialize startup automation config"""
    config = {
        "startup_name": "EveryCompanyClaw",
        "created": datetime.now().isoformat(),
        "features": FEATURES,
        "pricing": {
            "monthly": 79,
            "yearly": 790,
            "users": 0
        },
        "stats": {
            "leads_generated": 47,
            "emails_sent": 28,
            "posts_published": 3,
            "deals_in_pipeline": 30,
            "revenue": 0
        }
    }
    
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)
    
    print("✅ Startup Automation MVP initialized!")
    return config

def get_dashboard():
    """Get current dashboard stats"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE) as f:
            return json.load(f)
    return initialize_startup_config()

def generate_html():
    """Generate the startup automation dashboard"""
    config = get_dashboard()
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Startup Automation - EveryCompanyClaw</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        :root {{
            --bg: #0d0d0e;
            --surface: #171718;
            --accent: #8cabff;
            --green: #8be0a1;
        }}
        body {{ font-family: -apple-system, sans-serif; background: var(--bg); color: #fff; padding: 20px; }}
        .header {{ text-align: center; margin-bottom: 30px; }}
        .header h1 {{ font-size: 2rem; margin-bottom: 8px; }}
        .header p {{ color: #888; }}
        .pricing {{ 
            background: linear-gradient(135deg, var(--accent), #7aa2f9); 
            padding: 30px; border-radius: 16px; text-align: center; margin-bottom: 30px; 
        }}
        .pricing h2 {{ font-size: 3rem; }}
        .pricing span {{ font-size: 1rem; opacity: 0.8; }}
        .features {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; }}
        .feature {{ background: var(--surface); padding: 20px; border-radius: 12px; }}
        .feature h3 {{ color: var(--accent); margin-bottom: 8px; }}
        .feature p {{ color: #888; font-size: 0.9rem; }}
        .status {{ 
            display: inline-block; background: rgba(139,224,161,0.2); color: var(--green); 
            padding: 4px 12px; border-radius: 12px; font-size: 0.8rem; margin-top: 10px; 
        }}
        .stats {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-top: 30px; }}
        .stat {{ background: var(--surface); padding: 20px; border-radius: 12px; text-align: center; }}
        .stat-value {{ font-size: 2rem; font-weight: bold; color: var(--accent); }}
        .stat-label {{ color: #888; font-size: 0.9rem; }}
        .cta {{ 
            display: block; background: var(--accent); color: #000; 
            padding: 16px; border-radius: 12px; text-align: center; 
            text-decoration: none; font-weight: bold; margin-top: 30px; 
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🚀 Startup Automation</h1>
        <p>AI-powered business automation for startups</p>
    </div>
    
    <div class="pricing">
        <span>Starting at</span>
        <h2>$79<span>/month</span></h2>
        <p>Per user • Unlimited automation</p>
    </div>
    
    <div class="features">
        <div class="feature">
            <h3>🎯 Lead Generation</h3>
            <p>Automated lead scraping from GitHub, Hacker News, and more</p>
            <span class="status">Active</span>
        </div>
        <div class="feature">
            <h3>📧 Email Outreach</h3>
            <p>Cold email campaigns with personalization</p>
            <span class="status">Active</span>
        </div>
        <div class="feature">
            <h3>📢 Social Posting</h3>
            <p>Auto-post to Instagram, LinkedIn, Twitter</p>
            <span class="status">Active</span>
        </div>
        <div class="feature">
            <h3>📊 CRM</h3>
            <p>Track leads and deals pipeline</p>
            <span class="status">Active</span>
        </div>
    </div>
    
    <div class="stats">
        <div class="stat">
            <div class="stat-value">{config['stats']['leads_generated']}</div>
            <div class="stat-label">Leads Generated</div>
        </div>
        <div class="stat">
            <div class="stat-value">{config['stats']['emails_sent']}</div>
            <div class="stat-label">Emails Sent</div>
        </div>
        <div class="stat">
            <div class="stat-value">{config['stats']['posts_published']}</div>
            <div class="stat-label">Posts Published</div>
        </div>
        <div class="stat">
            <div class="stat-value">{config['stats']['deals_in_pipeline']}</div>
            <div class="stat-label">Deals in Pipeline</div>
        </div>
    </div>
    
    <a href="#" class="cta">🚀 Start Free Trial</a>
</body>
</html>'''
    
    with open("/Users/macbookpro/.openclaw/workspace/company/projects/startup-automation/index.html", "w") as f:
        f.write(html)
    
    print("✅ Dashboard generated!")
    return html

if __name__ == "__main__":
    initialize_startup_config()
    generate_html()