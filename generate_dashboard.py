#!/usr/bin/env python3
"""
Generate Live CRM Dashboard HTML with real-time data
Shows company flow like an actual business
"""
import os
import json
from datetime import datetime
from collections import Counter

CRM_FILE = "/tmp/company_crm.json"
LEARN_STATE = "/tmp/learn_state.json"
LEADS_FILE = "/tmp/leads.json"
PIPELINE_FILE = "/tmp/sales_pipeline.json"
OUTPUT_FILE = "/Users/macbookpro/.openclaw/workspace/company/crm-dashboard.html"

def load_json(path, default):
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return default

def get_pipeline_by_stage(pipeline):
    """Group deals by stage"""
    stages = {}
    for deal in pipeline.get("deals", []):
        stage = deal.get("stage", "lead")
        if stage not in stages:
            stages[stage] = []
        stages[stage].append(deal)
    return stages

def generate_dashboard():
    # Load all data
    crm = load_json(CRM_FILE, {"leads": [], "activities": [], "pipeline": [], "tasks": []})
    learn = load_json(LEARN_STATE, {"topics_done": [], "actions_done": []})
    leads = load_json(LEADS_FILE, {"leads": []})
    pipeline = load_json(PIPELINE_FILE, {"deals": []})
    
    topics = learn.get("topics_done", [])
    actions = learn.get("actions_done", [])
    activities = crm.get("activities", [])
    
    current_topic = topics[-1] if topics else "None"
    current_action = actions[-1] if actions else "None"
    
    # Pipeline stats
    pipeline_by_stage = get_pipeline_stage(pipeline)
    pipeline_value = sum(d.get("value", 0) for d in pipeline.get("deals", []))
    total_deals = len(pipeline.get("deals", []))
    
    # Lead stats
    total_leads = len(leads.get("leads", []))
    leads_clicked = sum(1 for l in leads.get("leads", []) if l.get("clicked"))
    leads_replied = sum(1 for l in leads.get("leads", []) if l.get("replied"))
    
    # Recent activities (today)
    today = datetime.now().strftime("%Y-%m-%d")
    today_activities = [a for a in activities if a.get("time", "").startswith(today)][-15:][::-1]
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EveryCompanyClaw - Live Company Dashboard</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
            background: #0a0a0f;
            min-height: 100vh;
            color: #fff;
            padding: 20px;
        }}
        
        .header {{
            text-align: center;
            padding: 30px 0;
            border-bottom: 1px solid #1a1a2e;
            margin-bottom: 30px;
        }}
        
        h1 {{
            font-size: 2.5em;
            background: linear-gradient(90deg, #00ff88, #00d4ff, #7b2ff7);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }}
        
        .subtitle {{
            color: #666;
            font-size: 1.1em;
        }}
        
        .live-badge {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: rgba(0,255,136,0.1);
            padding: 8px 16px;
            border-radius: 20px;
            margin-top: 15px;
        }}
        
        .live-dot {{
            width: 10px;
            height: 10px;
            background: #00ff88;
            border-radius: 50%;
            animation: pulse 1.5s infinite;
        }}
        
        @keyframes pulse {{
            0%, 100% {{ opacity: 1; transform: scale(1); }}
            50% {{ opacity: 0.5; transform: scale(0.9); }}
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }}
        
        .full-width {{
            grid-column: 1 / -1;
        }}
        
        .card {{
            background: linear-gradient(145deg, #12121a 0%, #0d0d12 100%);
            border-radius: 16px;
            padding: 24px;
            border: 1px solid #1a1a2e;
        }}
        
        .card h2 {{
            color: #00d4ff;
            margin-bottom: 20px;
            font-size: 1.1em;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .card h2 span {{
            font-size: 1.3em;
        }}
        
        /* Stats Grid */
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 15px;
        }}
        
        .stat {{
            text-align: center;
            padding: 20px;
            background: rgba(255,255,255,0.03);
            border-radius: 12px;
        }}
        
        .stat-number {{
            font-size: 2.2em;
            font-weight: 700;
            color: #00ff88;
        }}
        
        .stat-number.purple {{ color: #7b2ff7; }}
        .stat-number.blue {{ color: #00d4ff; }}
        .stat-number.orange {{ color: #ff8800; }}
        
        .stat-label {{
            color: #666;
            font-size: 0.85em;
            margin-top: 5px;
        }}
        
        /* Pipeline Flow */
        .pipeline-flow {{
            display: flex;
            gap: 10px;
            overflow-x: auto;
            padding: 10px 0;
        }}
        
        .pipeline-stage {{
            min-width: 120px;
            padding: 15px;
            background: rgba(255,255,255,0.03);
            border-radius: 12px;
            text-align: center;
        }}
        
        .pipeline-stage h4 {{
            color: #888;
            font-size: 0.8em;
            margin-bottom: 10px;
            text-transform: uppercase;
        }}
        
        .pipeline-stage .count {{
            font-size: 1.8em;
            font-weight: 700;
        }}
        
        .pipeline-stage .value {{
            color: #00ff88;
            font-size: 0.9em;
            margin-top: 5px;
        }}
        
        .stage-lead {{ border-left: 3px solid #666; }}
        .stage-contacted {{ border-left: 3px solid #00d4ff; }}
        .stage-interested {{ border-left: 3px solid #7b2ff7; }}
        .stage-proposal {{ border-left: 3px solid #ff8800; }}
        .stage-negotiation {{ border-left: 3px solid #ff0088; }}
        .stage-closed_won {{ border-left: 3px solid #00ff88; }}
        
        /* Agent Flow */
        .agent-flow {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 15px;
        }}
        
        .agent {{
            padding: 20px;
            background: rgba(255,255,255,0.03);
            border-radius: 12px;
            border-left: 4px solid;
        }}
        
        .agent-learning {{ border-color: #7b2ff7; }}
        .agent-sales {{ border-color: #00d4ff; }}
        .agent-marketing {{ border-color: #ff8800; }}
        
        .agent h3 {{
            font-size: 1em;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        .agent-status {{
            padding: 8px 12px;
            background: rgba(0,255,136,0.1);
            border-radius: 8px;
            margin-bottom: 10px;
        }}
        
        .agent-status .label {{
            color: #666;
            font-size: 0.75em;
        }}
        
        .agent-status .value {{
            color: #00ff88;
            font-weight: 600;
        }}
        
        .agent-activity {{
            color: #888;
            font-size: 0.85em;
            margin-top: 10px;
        }}
        
        /* Activity Timeline */
        .timeline {{
            list-style: none;
        }}
        
        .timeline li {{
            padding: 12px 0;
            border-bottom: 1px solid #1a1a2e;
            display: flex;
            gap: 15px;
        }}
        
        .timeline li:last-child {{ border-bottom: none; }}
        
        .time {{
            color: #666;
            font-size: 0.85em;
            min-width: 60px;
        }}
        
        .type {{
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 0.75em;
            min-width: 70px;
            text-align: center;
        }}
        
        .type-learning {{
            background: rgba(123,47,247,0.2);
            color: #7b2ff7;
        }}
        
        .type-action {{
            background: rgba(0,255,136,0.2);
            color: #00ff88;
        }}
        
        .details {{
            color: #aaa;
        }}
        
        /* Footer */
        .footer {{
            text-align: center;
            color: #444;
            margin-top: 30px;
            padding: 20px;
            font-size: 0.85em;
        }}
        
        .auto-refresh {{
            color: #00ff88;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🏢 EveryCompanyClaw</h1>
        <p class="subtitle">AI-Powered Autonomous Company</p>
        <div class="live-badge">
            <span class="live-dot"></span>
            <span>LIVE - Running 24/7</span>
        </div>
    </div>
    
    <div class="container">
        <!-- Stats Overview -->
        <div class="card full-width">
            <h2><span>📊</span> Company Performance</h2>
            <div class="stats-grid">
                <div class="stat">
                    <div class="stat-number">{len(topics)}</div>
                    <div class="stat-label">Topics Learned</div>
                </div>
                <div class="stat">
                    <div class="stat-number purple">{len(actions)}</div>
                    <div class="stat-label">Actions Done</div>
                </div>
                <div class="stat">
                    <div class="stat-number blue">{total_leads}</div>
                    <div class="stat-label">Leads Generated</div>
                </div>
                <div class="stat">
                    <div class="stat-number orange">{leads_clicked}</div>
                    <div class="stat-label">Leads Clicked</div>
                </div>
                <div class="stat">
                    <div class="stat-number">{total_deals}</div>
                    <div class="stat-label">Pipeline Deals</div>
                </div>
            </div>
        </div>
        
        <!-- Pipeline Flow -->
        <div class="card full-width">
            <h2><span>💼</span> Sales Pipeline</h2>
            <div class="pipeline-flow">
                <div class="pipeline-stage stage-lead">
                    <h4>Lead</h4>
                    <div class="count">{pipeline_by_stage.get('lead', 0)}</div>
                </div>
                <div class="pipeline-stage stage-contacted">
                    <h4>Contacted</h4>
                    <div class="count">{pipeline_by_stage.get('contacted', 0)}</div>
                </div>
                <div class="pipeline-stage stage-interested">
                    <h4>Interested</h4>
                    <div class="count">{pipeline_by_stage.get('interested', 0)}</div>
                </div>
                <div class="pipeline-stage stage-proposal">
                    <h4>Proposal</h4>
                    <div class="count">{pipeline_by_stage.get('proposal', 0)}</div>
                </div>
                <div class="pipeline-stage stage-negotiation">
                    <h4>Negotiation</h4>
                    <div class="count">{pipeline_by_stage.get('negotiation', 0)}</div>
                </div>
                <div class="pipeline-stage stage-closed_won">
                    <h4>Closed Won</h4>
                    <div class="count">{pipeline_by_stage.get('closed_won', 0)}</div>
                </div>
            </div>
            <p style="color:#666; margin-top:15px;">Total Pipeline Value: <span style="color:#00ff88">${pipeline_value}</span></p>
        </div>
        
        <!-- Agent Flow -->
        <div class="card full-width">
            <h2><span>🤖</span> Live Agent Operations</h2>
            <div class="agent-flow">
                <div class="agent agent-learning">
                    <h3>🧠 Learning Agent</h3>
                    <div class="agent-status">
                        <div class="label">Currently Learning</div>
                        <div class="value">{current_topic}</div>
                    </div>
                    <div class="agent-status">
                        <div class="label">Frequency</div>
                        <div class="value">Every 5 min</div>
                    </div>
                    <div class="agent-activity">
                        Topics: {len(topics)} | Latest: {topics[-1] if topics else 'N/A'}
                    </div>
                </div>
                
                <div class="agent agent-sales">
                    <h3>💰 Sales Agent</h3>
                    <div class="agent-status">
                        <div class="label">Currently Doing</div>
                        <div class="value">{current_action}</div>
                    </div>
                    <div class="agent-status">
                        <div class="label">Frequency</div>
                        <div class="value">Every 15 min</div>
                    </div>
                    <div class="agent-activity">
                        Leads: {total_leads} | Replied: {leads_replied} | Pipeline: {total_deals}
                    </div>
                </div>
                
                <div class="agent agent-marketing">
                    <h3>📢 Marketing Agent</h3>
                    <div class="agent-status">
                        <div class="label">Content Focus</div>
                        <div class="value">Social Media</div>
                    </div>
                    <div class="agent-status">
                        <div class="label">Frequency</div>
                        <div class="value">Every 30 min</div>
                    </div>
                    <div class="agent-activity">
                        Posts: Daily | Engagement: {leads_clicked} clicks
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Recent Activity -->
        <div class="card">
            <h2><span>⚡</span> Today's Activity</h2>
            <ul class="timeline">
'''
    
    for a in today_activities:
        type_class = "type-learning" if a.get("action") == "learning" else "type-action"
        html += f'''                <li>
                    <span class="time">{a.get('time', '')[11:16]}</span>
                    <span class="type {type_class}">{a.get('action', '')}</span>
                    <span class="details">{a.get('details', '')}</span>
                </li>
'''
    
    html += '''            </ul>
        </div>
        
        <!-- Lead Stats -->
        <div class="card">
            <h2><span>🎯</span> Lead Performance</h2>
            <div class="stats-grid" style="grid-template-columns: 1fr 1fr;">
                <div class="stat">
                    <div class="stat-number blue">''' + str(total_leads) + '''</div>
                    <div class="stat-label">Total Leads</div>
                </div>
                <div class="stat">
                    <div class="stat-number">''' + str(leads_replied) + '''</div>
                    <div class="stat-label">Replied</div>
                </div>
            </div>
            <div style="margin-top: 20px;">
                <p style="color:#666; margin-bottom:10px;">Conversion Rate:</p>
                <div style="background: #1a1a2e; border-radius: 10px; height: 20px; overflow: hidden;">
                    <div style="background: linear-gradient(90deg, #00ff88, #00d4ff); height: 100%; width: ''' + str(int(leads_replied/total_leads*100) if total_leads > 0 else 0) + '''%;"></div>
                </div>
                <p style="color:#00ff88; text-align:right; margin-top:5px;">''' + str(int(leads_replied/total_leads*100) if total_leads > 0 else 0) + '''% response rate</p>
            </div>
        </div>
    </div>
    
    <div class="footer">
        <p>Auto-refresh every 30 seconds | Last updated: ''' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '''</p>
        <p class="auto-refresh">🏢 EveryCompanyClaw - Autonomous AI Company Running 24/7</p>
    </div>
    
    <script>
        setInterval(() => {
            location.reload();
        }, 30000);
    </script>
</body>
</html>'''
    
    with open(OUTPUT_FILE, "w") as f:
        f.write(html)
    
    print(f"✅ Dashboard updated: {OUTPUT_FILE}")

def get_pipeline_stage(pipeline):
    """Get count by stage"""
    stages = {"lead": 0, "contacted": 0, "interested": 0, "proposal": 0, "negotiation": 0, "closed_won": 0, "closed_lost": 0}
    for deal in pipeline.get("deals", []):
        stage = deal.get("stage", "lead")
        if stage in stages:
            stages[stage] += 1
    return stages

if __name__ == "__main__":
    generate_dashboard()
