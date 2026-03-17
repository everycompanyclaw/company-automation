#!/usr/bin/env python3
"""
MK's Company - Agent Spawner
Each agent has a specific role
"""

from enum import Enum
from typing import Optional

class AgentRole(Enum):
    CEO = "ceo"
    SALES = "sales"
    DEVELOPER = "developer"
    SUPPORT = "support"
    ANALYST = "analyst"
    OPERATIONS = "operations"

AGENT_CONFIGS = {
    AgentRole.CEO: {
        "name": "CEO Agent",
        "description": "Strategic planning and business decisions",
        "model": "opus",
        "system_prompt": "You are MK's CEO. Think strategically about long-term goals, business decisions, and growth."
    },
    AgentRole.SALES: {
        "name": "Sales Agent", 
        "description": "Lead generation and outreach",
        "model": "opus",
        "system_prompt": "You are MK's Sales Agent. Find leads, write outreach messages, and close deals."
    },
    AgentRole.DEVELOPER: {
        "name": "Developer Agent",
        "description": "Building and coding",
        "model": "opus", 
        "system_prompt": "You are MK's Developer. Build, code, and create technical solutions."
    },
    AgentRole.SUPPORT: {
        "name": "Support Agent",
        "description": "Customer service and FAQs",
        "model": "minimax",
        "system_prompt": "You are MK's Support Agent. Respond to customer questions helpfully and professionally."
    },
    AgentRole.ANALYST: {
        "name": "Analyst Agent",
        "description": "Research and analysis",
        "model": "opus",
        "system_prompt": "You are MK's Analyst. Research markets, analyze data, and provide insights."
    },
    AgentRole.OPERATIONS: {
        "name": "Operations Agent",
        "description": "Routine tasks and automation",
        "model": "minimax",
        "system_prompt": "You are MK's Operations Agent. Handle routine tasks, scheduling, and automation."
    }
}

def spawn_agent(role: AgentRole, task: str) -> dict:
    """Spawn an agent for a specific role"""
    config = AGENT_CONFIGS[role]
    return {
        "role": role.value,
        "name": config["name"],
        "model": config["model"],
        "task": task,
        "system_prompt": config["system_prompt"]
    }

def get_agent_for_task(task_type: str) -> AgentRole:
    """Auto-select the right agent for a task"""
    task_lower = task_type.lower()
    
    if any(word in task_lower for word in ["strategy", "plan", "goal", "decision"]):
        return AgentRole.CEO
    elif any(word in task_lower for word in ["lead", "sales", "outreach", "customer"]):
        return AgentRole.SALES
    elif any(word in task_lower for word in ["build", "code", "develop", "create"]):
        return AgentRole.DEVELOPER
    elif any(word in task_lower for word in ["help", "question", "support", "faq"]):
        return AgentRole.SUPPORT
    elif any(word in task_lower for word in ["research", "analyze", "report", "data"]):
        return AgentRole.ANALYST
    else:
        return AgentRole.OPERATIONS

if __name__ == "__main__":
    # Example
    task = "Find potential clients for automation services"
    agent_role = get_agent_for_task(task)
    agent = spawn_agent(agent_role, task)
    print(f"Selected: {agent['name']}")
    print(f"Model: {agent['model']}")
    print(f"Task: {agent['task']}")
