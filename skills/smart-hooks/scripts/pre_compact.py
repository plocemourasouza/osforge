#!/usr/bin/env python3
"""Pre-compact hook: Backup conversation before context compaction.
Saves transcript to .claude/backups/ with timestamp.
"""
import json
import sys
import os
from datetime import datetime

def main():
    backup_dir = os.path.join(os.getcwd(), ".claude", "backups")
    os.makedirs(backup_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_path = os.path.join(backup_dir, f"pre-compact-{timestamp}.json")

    try:
        data = json.loads(sys.stdin.read())
    except (json.JSONDecodeError, EOFError):
        data = {"note": "No input data available"}

    backup = {
        "timestamp": datetime.now().isoformat(),
        "event": "pre_compact",
        "data": data,
    }

    with open(backup_path, "w") as f:
        json.dump(backup, f, indent=2, default=str)

    print(f"ℹ️ Context backup saved: {backup_path}", file=sys.stderr)
    sys.exit(0)

if __name__ == "__main__":
    main()
