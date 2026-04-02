#!/usr/bin/env python3
"""
EveryCompanyClaw Project Manager CLI
Usage:
  python3 project_manager.py new-project "Name" "Description" --value 500
  python3 project_manager.py list-projects
  python3 project_manager.py status <project_id>
  python3 project_manager.py complete <project_id>
  python3 project_manager.py add-sprint <project_id> "Sprint Name" "task1,task2,task3"
  python3 project_manager.py delete <project_id>
"""

import json
import os
import sys
import argparse
from datetime import datetime, timezone

PROJECTS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'projects.json')

def load_projects():
    if not os.path.exists(PROJECTS_FILE):
        return {"projects": [], "last_updated": datetime.now(timezone.utc).isoformat()}
    with open(PROJECTS_FILE, 'r') as f:
        return json.load(f)

def save_projects(data):
    data["last_updated"] = datetime.now(timezone.utc).isoformat()
    with open(PROJECTS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def new_project(name, description, value=0):
    data = load_projects()
    project_id = f"PRJ-{len(data['projects']) + 1:03d}"
    project = {
        "id": project_id,
        "name": name,
        "description": description,
        "value": value,
        "status": "scouting",
        "sprints": [],
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    data["projects"].append(project)
    save_projects(data)
    print(f"✅ Created project {project_id}: {name} (${value})")

def list_projects():
    data = load_projects()
    if not data["projects"]:
        print("📋 No projects yet.")
        return
    print(f"{'ID':<10} {'NAME':<25} {'STATUS':<12} {'VALUE':<10} {'SPRINTS'}")
    print("-" * 70)
    for p in data["projects"]:
        sprints = len(p.get("sprints", []))
        print(f"{p['id']:<10} {p['name'][:24]:<25} {p['status']:<12} ${p.get('value', 0):<9} {sprints}")

def status_project(project_id):
    data = load_projects()
    p = next((x for x in data["projects"] if x["id"] == project_id), None)
    if not p:
        print(f"❌ Project {project_id} not found.")
        return
    print(f"\n📊 {p['id']}: {p['name']}")
    print(f"   Description: {p['description']}")
    print(f"   Value:       ${p.get('value', 0)}")
    print(f"   Status:      {p['status']}")
    print(f"   Created:     {p['created_at']}")
    print(f"   Sprints:     {len(p.get('sprints', []))}")
    for i, s in enumerate(p.get("sprints", []), 1):
        print(f"     Sprint {i}: {s['name']} — {s.get('tasks', [])}")

def complete_project(project_id):
    data = load_projects()
    for p in data["projects"]:
        if p["id"] == project_id:
            old = p["status"]
            p["status"] = "completed"
            save_projects(data)
            print(f"✅ Project {project_id} marked as COMPLETED. Revenue: ${p.get('value', 0)}")
            return
    print(f"❌ Project {project_id} not found.")

def add_sprint(project_id, sprint_name, tasks):
    data = load_projects()
    for p in data["projects"]:
        if p["id"] == project_id:
            task_list = [t.strip() for t in tasks.split(",") if t.strip()]
            sprint = {"name": sprint_name, "tasks": task_list}
            if "sprints" not in p:
                p["sprints"] = []
            p["sprints"].append(sprint)
            if p["status"] == "scouting":
                p["status"] = "active"
            save_projects(data)
            print(f"🏃 Sprint '{sprint_name}' added to {project_id} ({len(task_list)} tasks). Project is now '{p['status']}'.")
            return
    print(f"❌ Project {project_id} not found.")

def delete_project(project_id):
    data = load_projects()
    original = len(data["projects"])
    data["projects"] = [p for p in data["projects"] if p["id"] != project_id]
    if len(data["projects"]) < original:
        save_projects(data)
        print(f"🗑️  Deleted project {project_id}.")
    else:
        print(f"❌ Project {project_id} not found.")

def main():
    parser = argparse.ArgumentParser(description="EveryCompanyClaw Project Manager")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # new-project
    np = subparsers.add_parser("new-project", help="Create a new project")
    np.add_argument("name", help="Project name")
    np.add_argument("description", help="Project description")
    np.add_argument("--value", type=int, default=0, help="Project value in dollars")

    # list-projects
    subparsers.add_parser("list-projects", help="List all projects")

    # status
    st = subparsers.add_parser("status", help="Show project status")
    st.add_argument("project_id", help="Project ID (e.g. PRJ-001)")

    # complete
    cp = subparsers.add_parser("complete", help="Mark project as completed")
    cp.add_argument("project_id", help="Project ID")

    # add-sprint
    sp = subparsers.add_parser("add-sprint", help="Add a sprint to a project")
    sp.add_argument("project_id", help="Project ID")
    sp.add_argument("sprint_name", help="Sprint name")
    sp.add_argument("tasks", help="Comma-separated task list")

    # delete
    dl = subparsers.add_parser("delete", help="Delete a project")
    dl.add_argument("project_id", help="Project ID")

    args = parser.parse_args()

    if args.command == "new-project":
        new_project(args.name, args.description, args.value)
    elif args.command == "list-projects":
        list_projects()
    elif args.command == "status":
        status_project(args.project_id)
    elif args.command == "complete":
        complete_project(args.project_id)
    elif args.command == "add-sprint":
        add_sprint(args.project_id, args.sprint_name, args.tasks)
    elif args.command == "delete":
        delete_project(args.project_id)

if __name__ == "__main__":
    main()
