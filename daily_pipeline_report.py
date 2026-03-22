#!/usr/bin/env python3
"""
Enhanced Pipeline Report with Full Details
"""
import json
import os
from datetime import datetime

LEADS_FILE = "/tmp/leads.json"
PIPELINE_FILE = "/tmp/sales_pipeline.json"

def load_json(path, default):
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return default

def generate_report():
    leads = load_json(LEADS_FILE, {"leads": []})
    pipeline = load_json(PIPELINE_FILE, {"deals": []})
    
    total = len(leads.get("leads", []))
    contacted = sum(1 for l in leads.get("leads", []) if l.get("status") in ["contacted", "interested", "proposal"])
    replied = sum(1 for l in leads.get("leads", []) if l.get("replied"))
    clicked = sum(1 for l in leads.get("leads", []) if l.get("clicked"))
    
    # Pipeline stages
    stages = {}
    for deal in pipeline.get("deals", []):
        stage = deal.get("stage", "lead")
        stages[stage] = stages.get(stage, 0) + 1
    
    # Lead sources
    sources = {}
    for lead in leads.get("leads", []):
        src = lead.get("source", "unknown")
        sources[src] = sources.get(src, 0) + 1
    
    report = f"""
╔═══════════════════════════════════════════════════════════════╗
║          EVERYCOMPANYCLAW - PIPELINE REPORT                   ║
║                 {datetime.now().strftime('%Y-%m-%d %H:%M')}                             ║
╚═══════════════════════════════════════════════════════════════╝

┌───────────────────────────────────────────────────────────────┐
│                    📊 FUNNEL METRICS                         │
├───────────────────────────────────────────────────────────────┤
│  Total Leads:      ████████████████████████  {total:>3}           │
│  Contacted:       ████████████████░░░░░░░░  {contacted:>3} ({int(contacted/total*100) if total else 0}%)      │
│  Clicked:         █████████░░░░░░░░░░░░░  {clicked:>3} ({int(clicked/total*100) if total else 0}%)      │
│  Replied:         ████░░░░░░░░░░░░░░░░░░  {replied:>3} ({int(replied/total*100) if total else 0}%)      │
└───────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────┐
│                    📱 LEAD SOURCES                            │
├───────────────────────────────────────────────────────────────┤
"""
    for src, count in sources.items():
        pct = int(count/total*100) if total else 0
        bar = "█" * (pct // 5) + "░" * (20 - pct // 5)
        report += f"│  {src:<12} {bar} {count:>3} ({pct:>2}%)\n"
    
    report += """└───────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────┐
│                    💰 PIPELINE STAGES                         │
├───────────────────────────────────────────────────────────────┤
│  📋 Lead:          ░░░░░░░░░░░░░░░░░░░  {:>2} deals           │
│  📨 Contacted:     ██████████████░░░░░░  {:>2} deals           │
│  🤔 Interested:    ████░░░░░░░░░░░░░░░  {:>2} deals           │
│  📄 Proposal:      ██░░░░░░░░░░░░░░░░░  {:>2} deals           │
│  🎉 Closed Won:    ░░░░░░░░░░░░░░░░░░░  {:>2} deals           │
└───────────────────────────────────────────────────────────────┘
""".format(
        stages.get('lead', 0),
        stages.get('contacted', 0),
        stages.get('interested', 0),
        stages.get('proposal', 0),
        stages.get('closed_won', 0)
    )
    
    # Replied leads with details
    replied_leads = [l for l in leads.get("leads", []) if l.get("replied")]
    if replied_leads:
        report += """
┌───────────────────────────────────────────────────────────────┐
│                 ✅ HOT LEADS (REPLIED)                       │
│                    (Ready for sales call)                    │
├───────────────────────────────────────────────────────────────┤
│  NAME                   COMPANY              SOURCE    DATE  │
├───────────────────────────────────────────────────────────────┤
"""
        for lead in replied_leads:
            name = (lead.get('name', 'Unknown')[:18]).ljust(18)
            company = (lead.get('company', 'N/A')[:17]).ljust(17)
            source = (lead.get('source', '-')[:8]).ljust(8)
            date = (lead.get('created_at', '')[:10])[-5:]
            report += f"│  {name}  {company}  {source}  {date}\n"
        report += "└───────────────────────────────────────────────────────────────┘\n"
    
    # Clicked but not replied
    clicked_not_replied = [l for l in leads.get("leads", []) if l.get("clicked") and not l.get("replied")]
    if clicked_not_replied:
        report += """
┌───────────────────────────────────────────────────────────────┐
│                 👀 WARM LEADS (CLICKED, NOT REPLIED)         │
│                    (Need follow-up)                          │
├───────────────────────────────────────────────────────────────┤
"""
        for lead in clicked_not_replied[:5]:
            name = (lead.get('name', 'Unknown')[:18]).ljust(18)
            company = (lead.get('company', 'N/A')[:17]).ljust(17)
            source = (lead.get('source', '-')[:8]).ljust(8)
            report += f"│  {name}  {company}  {source}\n"
        report += "└───────────────────────────────────────────────────────────────┘\n"
    
    report += f"""
╚═══════════════════════════════════════════════════════════════╝
                    🤖 Autonomous AI Company
"""
    
    print(report)
    with open("/tmp/daily_pipeline_report.txt", "w") as f:
        f.write(report)

if __name__ == "__main__":
    generate_report()
