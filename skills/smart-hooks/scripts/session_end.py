#!/usr/bin/env python3
"""Session end hook: Log session and notify.
Logs session end to .claude/sessions.log and plays notification (macOS).
"""
import json
import sys
import os
import subprocess
from datetime import datetime

def play_notification():
    """Play system sound on macOS."""
    try:
        subprocess.run(
            ["afplay", "/System/Library/Sounds/Glass.aiff"],
            timeout=3,
            capture_output=True,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass  # Not macOS or sound not available

def log_session_end():
    """Write session end entry."""
    log_dir = os.path.join(os.getcwd(), ".claude")
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, "sessions.log")

    entry = {
        "timestamp": datetime.now().isoformat(),
        "event": "session_end",
        "cwd": os.getcwd(),
    }

    with open(log_path, "a") as f:
        f.write(json.dumps(entry) + "\n")

def main():
    log_session_end()
    play_notification()
    print("ℹ️ Session logged and notification sent.", file=sys.stderr)
    sys.exit(0)

if __name__ == "__main__":
    main()
