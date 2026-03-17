#!/usr/bin/env python3
"""
Agent Team System
Auto-spawn the right agent for each task
"""

from typing import Dict, Any, Callable
import json

class AgentTeam:
    def __init__(self):
        self.agents = {}
        self.current_task = None
    
    def register_agent(self, name: str, config: Dict):
        """Register an agent"""
        self.agents[name] = config
    
    def get_agent_for_task(self, task: str) -> str:
        """Auto-select best agent"""
        task_lower = task.lower()
        
        # Strategy/Planning
        if any(w in task_lower for w in ["plan", "strategy", "goal", "decision", "vision"]):
            return "ceo"
        
        # Sales/Lead Gen
        elif any(w in task_lower for w in ["lead", "sales", "customer", "outreach", "close", "sell"]):
            return "sales"
        
        # Building/Coding
        elif any(w in task_lower for w in ["build", "code", "develop", "create", "make", "fix", "debug"]):
            return "developer"
        
        # Support/Service
        elif any(w in task_lower for w in ["help", "support", "question", "respond", "answer"]):
            return "support"
        
        # Research/Analysis
        elif any(w in task_lower for w in ["research", "analyze", "report", "data", "find", "search"]):
            return "analyst"
        
        # Operations/Routine
        else:
            return "operations"
    
    def spawn_agent(self, task: str) -> Dict:
        """Spawn the right agent for task"""
        agent_name = self.get_agent_for_task(task)
        agent = self.agents.get(agent_name, {})
        
        return {
            "agent": agent_name,
            "task": task,
            "model": agent.get("model", "minimax"),
            "prompt": agent.get("prompt", "")
        }

# Default team
TEAM = AgentTeam()

TEAM.register_agent("ceo", {
    "name": "CEO Agent",
    "model": "opus",
    "prompt": "You are MK's CEO. Think strategically, make decisions, plan growth."
})

TEAM.register_agent("sales", {
    "name": "Sales Agent",
    "model": "opus", 
    "prompt": "You are MK's Sales Agent. Find leads, write outreach, close deals."
})

TEAM.register_agent("developer", {
    "name": "Developer Agent",
    "model": "opus",
    "prompt": "You are MK's Developer. Build, code, create technical solutions."
})

TEAM.register_agent("support", {
    "name": "Support Agent",
    "model": "minimax",
    "prompt": "You are MK's Support. Respond helpfully to customer questions."
})

TEAM.register_agent("analyst", {
    "name": "Analyst Agent",
    "model": "opus",
    "prompt": "You are MK's Analyst. Research markets, analyze data, provide insights."
})

TEAM.register_agent("operations", {
    "name": "Operations Agent",
    "model": "minimax",
    "prompt": "You are MK's Operations. Handle routine tasks efficiently."
})

if __name__ == "__main__":
    # Test
    test_tasks = [
        "Find leads for automation business",
        "Build a website for my client",
        "Help a customer with their question",
        "Create a business plan",
        "Analyze the stock market",
        "Schedule a meeting"
    ]
    
    print("🤖 Agent Team - Auto Selection\n")
    for task in test_tasks:
        agent = TEAM.get_agent_for_task(task)
        print(f"Task: {task}")
        print(f"→ Agent: {agent}\n")
