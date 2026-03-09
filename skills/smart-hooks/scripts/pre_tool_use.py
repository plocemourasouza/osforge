#!/usr/bin/env python3
"""Pre-tool-use hook: Safety rails for Claude Code.
Blocks dangerous commands and logs all tool calls.
Reads from stdin (JSON with tool_name, tool_input).
Exit 0 = allow, Exit 2 = block with message to stderr.
"""
import json
import sys
import os
import re
from datetime import datetime

BLOCKED_BASH_PATTERNS = [
    r"rm\s+-rf\s+/(?!\w)",
    r"rm\s+-rf\s+~",
    r"DROP\s+DATABASE",
    r"DROP\s+SCHEMA",
    r"TRUNCATE\s+TABLE",
    r"git\s+push.*--force.*main",
    r"git\s+push.*--force.*master",
    r"chmod\s+777",
    r"curl.*\|\s*sh",
    r"curl.*\|\s*bash",
    r"wget.*\|\s*sh",
    r":(){ :\|:& };:",  # fork bomb
    r"mkfs\.",
    r"dd\s+if=.*of=/dev/",
    r">\s*/dev/sd",
]

PROTECTED_FILES = [
    ".env",
    ".env.local",
    ".env.production",
    "package-lock.json",
    "bun.lockb",
    "yarn.lock",
]

def log_tool_call(tool_name: str, tool_input: dict):
    """Append tool call to audit log."""
    log_dir = os.path.join(os.getcwd(), ".claude")
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, "audit.log")
    entry = {
        "timestamp": datetime.now().isoformat(),
        "tool": tool_name,
        "input_summary": str(tool_input)[:200],
    }
    with open(log_path, "a") as f:
        f.write(json.dumps(entry) + "\n")

def check_bash_safety(command: str) -> str | None:
    """Check if a bash command matches blocked patterns."""
    for pattern in BLOCKED_BASH_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            return f"BLOCKED: Dangerous command pattern detected: {pattern}"
    return None

def check_file_protection(file_path: str) -> str | None:
    """Check if a file is in the protected list."""
    basename = os.path.basename(file_path)
    for protected in PROTECTED_FILES:
        if basename == protected:
            return f"BLOCKED: Cannot modify protected file: {protected}"
    return None

def main():
    try:
        data = json.loads(sys.stdin.read())
    except (json.JSONDecodeError, EOFError):
        sys.exit(0)  # Fail open

    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input", {})

    # Log every tool call
    log_tool_call(tool_name, tool_input)

    # Check Bash commands
    if tool_name == "Bash":
        command = tool_input.get("command", "")
        violation = check_bash_safety(command)
        if violation:
            print(violation, file=sys.stderr)
            sys.exit(2)

    # Check file writes
    if tool_name in ("Write", "Edit"):
        file_path = tool_input.get("file_path", tool_input.get("path", ""))
        violation = check_file_protection(file_path)
        if violation:
            print(violation, file=sys.stderr)
            sys.exit(2)

    sys.exit(0)  # Allow

if __name__ == "__main__":
    main()
