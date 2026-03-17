#!/usr/bin/env python3
"""
Company Workflows
How agents work together
"""

WORKFLOWS = {
    "lead_capture": {
        "name": "New Lead Flow",
        "steps": [
            {"agent": "support", "action": "Respond to inquiry"},
            {"agent": "support", "action": "Qualify lead"},
            {"agent": "sales", "action": "Follow up"},
            {"agent": "ceo", "action": "Approve deal"},
            {"agent": "developer", "action": "Deliver project"},
            {"agent": "operations", "action": "Ongoing support"}
        ]
    },
    
    "project_delivery": {
        "name": "Project Delivery",
        "steps": [
            {"agent": "sales", "action": "Close deal"},
            {"agent": "developer", "action": "Build solution"},
            {"agent": "analyst", "action": "Test and verify"},
            {"agent": "support", "action": "Deliver to client"},
            {"agent": "operations", "action": "Set up maintenance"}
        ]
    },
    
    "research": {
        "name": "Market Research",
        "steps": [
            {"agent": "analyst", "action": "Gather data"},
            {"agent": "analyst", "action": "Analyze market"},
            {"agent": "ceo", "action": "Make decision"},
            {"agent": "sales", "action": "Execute strategy"}
        ]
    }
}

def run_workflow(workflow_name: str):
    """Run a workflow"""
    if workflow_name not in WORKFLOWS:
        print(f"Unknown workflow: {workflow_name}")
        return
    
    workflow = WORKFLOWS[workflow_name]
    print(f"\n{'='*50}")
    print(f"📋 Running: {workflow['name']}")
    print(f"{'='*50}\n")
    
    for i, step in enumerate(workflow["steps"], 1):
        print(f"{i}. 🤖 {step['agent'].title()} Agent → {step['action']}")
    
    print(f"\n✅ Workflow complete!\n")

if __name__ == "__main__":
    # Example
    run_workflow("lead_capture")
    run_workflow("project_delivery")
    run_workflow("research")
