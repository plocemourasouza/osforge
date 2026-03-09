#!/usr/bin/env python3
"""Post-tool-use hook: Quality gates for TypeScript/TSX files.
Checks for common issues after Write/Edit operations.
Reads from stdin (JSON with tool_name, tool_input, tool_output).
Exit 0 = pass (warnings printed to stderr are shown to Claude).
"""
import json
import sys
import re
import os

QUALITY_RULES = [
    {
        "pattern": r"console\.log\(",
        "message": "⚠️ console.log detected — remove before commit",
        "severity": "warn",
        "extensions": [".ts", ".tsx", ".js", ".jsx"],
    },
    {
        "pattern": r":\s*any\b",
        "message": "⚠️ 'any' type used — prefer 'unknown' + narrowing (typescript-strict rule)",
        "severity": "warn",
        "extensions": [".ts", ".tsx"],
    },
    {
        "pattern": r"//\s*@ts-ignore(?!\s*—)",
        "message": "⚠️ @ts-ignore without justification — add reason after '—'",
        "severity": "warn",
        "extensions": [".ts", ".tsx"],
    },
    {
        "pattern": r"export\s+default\s+",
        "message": "⚠️ export default used — prefer named exports (coding-guidelines rule)",
        "severity": "warn",
        "extensions": [".ts", ".tsx"],
    },
    {
        "pattern": r"\bvar\s+",
        "message": "⚠️ 'var' keyword used — use 'const' or 'let'",
        "severity": "warn",
        "extensions": [".ts", ".tsx", ".js", ".jsx"],
    },
    {
        "pattern": r"TODO|FIXME|HACK|XXX",
        "message": "ℹ️ TODO/FIXME marker found — track or resolve",
        "severity": "info",
        "extensions": [".ts", ".tsx", ".js", ".jsx"],
    },
]

def check_file_quality(file_path: str, content: str) -> list[str]:
    """Run quality rules against file content."""
    warnings = []
    ext = os.path.splitext(file_path)[1]

    for rule in QUALITY_RULES:
        if ext not in rule["extensions"]:
            continue
        matches = re.findall(rule["pattern"], content)
        if matches:
            count = len(matches)
            warnings.append(f"{rule['message']} ({count}x in {os.path.basename(file_path)})")

    return warnings

def main():
    try:
        data = json.loads(sys.stdin.read())
    except (json.JSONDecodeError, EOFError):
        sys.exit(0)

    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input", {})

    if tool_name not in ("Write", "Edit"):
        sys.exit(0)

    file_path = tool_input.get("file_path", tool_input.get("path", ""))
    if not file_path:
        sys.exit(0)

    ext = os.path.splitext(file_path)[1]
    if ext not in (".ts", ".tsx", ".js", ".jsx"):
        sys.exit(0)

    # Read the file content after write/edit
    try:
        with open(file_path, "r") as f:
            content = f.read()
    except FileNotFoundError:
        sys.exit(0)

    warnings = check_file_quality(file_path, content)
    if warnings:
        print("\n".join(warnings), file=sys.stderr)

    sys.exit(0)  # Always pass — warnings are informational

if __name__ == "__main__":
    main()
