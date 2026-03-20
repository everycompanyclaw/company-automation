#!/usr/bin/env python3
"""
PinchTab Controller
Control browser via PinchTab API
"""
import requests
import json

PORT = 8765

def control(command):
    """Send command to PinchTab"""
    try:
        r = requests.post(f"http://localhost:{PORT}/execute", 
                         json={"command": command}, timeout=10)
        return r.json()
    except Exception as e:
        return {"error": str(e)}

# Example commands
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        cmd = " ".join(sys.argv[1:])
        result = control(cmd)
        print(json.dumps(result, indent=2))
    else:
        print("Usage: pinchtab.py [command]")
        print("Examples:")
        print("  pinchtab.py open https://google.com")
        print("  pinchtab.py click .button")
        print("  pinchtab.py screenshot")
