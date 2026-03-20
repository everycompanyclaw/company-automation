#!/usr/bin/env python3
"""
Buffer MCP Server - Model Context Protocol Integration
"""
import json
import sys
import requests
import os

TOKEN = os.environ.get("BUFFER_TOKEN", "")

def handle_request(req):
    """Handle MCP request"""
    method = req.get("method")
    params = req.get("params", {})
    
    if method == "tools/list":
        return {
            "tools": [
                {
                    "name": "buffer_post",
                    "description": "Post to Instagram via Buffer",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "text": {"type": "string", "description": "Post text"}
                        },
                        "required": ["text"]
                    }
                }
            ]
        }
    
    if method == "tools/call":
        tool = params.get("name")
        args = params.get("arguments", {})
        
        if tool == "buffer_post":
            text = args.get("text", "")
            result = post_to_buffer(text)
            return {"content": [{"type": "text", "text": json.dumps(result)}]}
    
    return {"error": "Unknown method"}

def post_to_buffer(text):
    """Post to Buffer"""
    if not TOKEN:
        return {"error": "No token"}
    
    # Get profiles
    r = requests.get(f"https://api.bufferapp.com/1/profiles.json?access_token={TOKEN}")
    
    if r.status_code != 200:
        return {"error": f"API error: {r.status_code}"}
    
    profiles = r.json()
    
    # Find Instagram
    for p in profiles:
        if p.get("service") == "instagram":
            data = {
                "access_token": TOKEN,
                "text": text,
                "profile_ids[]": p["id"]
            }
            r = requests.post("https://api.bufferapp.com/1/updates/create.json", data=data)
            return {"success": True, "response": r.json()}
    
    return {"error": "No Instagram profile"}

# MCP stdio loop
if __name__ == "__main__":
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        try:
            req = json.loads(line)
            resp = handle_request(req)
            print(json.dumps(resp), flush=True)
        except Exception as e:
            print(json.dumps({"error": str(e)}), flush=True)
