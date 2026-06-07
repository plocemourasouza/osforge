---
name: smart-hooks
description: "Production-grade Python hooks for Claude Code quality gates, safety rails, and developer experience. TRIGGER when: setting up hooks for a project, configuring quality gates, implementing pre-commit checks, blocking dangerous commands, or improving Claude Code DX with notifications and backups. Install by copying hooks/ to .claude/hooks/ and updating settings.json."
metadata:
  author: osforge
  version: '1.0'
  inspired_by: darraghh1/my-claude-setup
---

# Smart Hooks for Claude Code

## Overview
Production-grade hooks that add safety rails, quality gates, and developer experience improvements to Claude Code sessions. All hooks are Python scripts designed for the `.claude/hooks/` directory.

## Available Hooks

### 1. pre_tool_use.py — Safety Rails
**Event:** PreToolUse (before Write, Edit, Bash)
**What it does:**
- Blocks dangerous commands (rm -rf /, DROP DATABASE, force push to main)
- Prevents writes to protected files (.env, .env.local, package-lock.json)
- Logs all tool calls to `.claude/audit.log` for traceability

**Example of a blocked command:**
```
$ rm -rf / --no-preserve-root
BLOCKED by pre_tool_use.py: command matches dangerous pattern "rm -rf /"
(see scripts/config/blocked_patterns.json → bash_blocked). Tool call denied
and logged to .claude/audit.log.
```

### 2. post_tool_use.py — Quality Gates
**Event:** PostToolUse (after Write, Edit on .ts/.tsx files)
**What it does:**
- Checks for `console.log` left in production code
- Warns about `any` type usage in TypeScript strict mode
- Detects missing error handling in async functions
- Flags hardcoded strings that should be i18n keys

### 3. pre_compact.py — Context Backup
**Event:** PreCompact (before context window compaction)
**What it does:**
- Saves full conversation transcript to `.claude/backups/`
- Timestamps the backup for recovery
- Prevents loss of important context during long sessions

### 4. session_end.py — Session Logging
**Event:** Stop (when session ends)
**What it does:**
- Logs session duration and token usage
- Plays system notification sound (macOS)
- Writes session summary to `.claude/sessions.log`

## Installation

### Step 1: Copy hooks to project
```bash
cp -r smart-hooks/scripts/*.py .claude/hooks/
chmod +x .claude/hooks/*.py
```

### Step 2: Configure settings.json
```jsonc
// .claude/settings.json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit|Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 .claude/hooks/pre_tool_use.py"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "python3 .claude/hooks/post_tool_use.py"
          }
        ]
      }
    ],
    "PreCompact": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 .claude/hooks/pre_compact.py"
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 .claude/hooks/session_end.py"
          }
        ]
      }
    ]
  }
}
```

## Design Principles

1. **Command hooks, not prompt hooks** — Command hooks run locally and don't consume API tokens. Prompt hooks make API calls. We use command hooks for everything except when we need Claude's judgment.
2. **Fail open** — If a hook errors, the operation continues. Hooks should never block legitimate work.
3. **Minimal overhead** — Each hook runs in <100ms. No network calls, no heavy dependencies.
4. **Audit trail** — All tool calls are logged for compliance and debugging.
5. **Unified validation** — One hook per event, not 5 separate hooks (learned from the TabNews optimization article).

## Customization

### Adding blocked commands
Edit `scripts/config/blocked_patterns.json`:
```json
{
  "bash_blocked": [
    "rm -rf /",
    "DROP DATABASE",
    "git push.*--force.*main",
    "chmod 777",
    "curl.*| sh"
  ],
  "file_protected": [
    ".env",
    ".env.local",
    "package-lock.json",
    "bun.lockb"
  ]
}
```

### Adding quality checks
Edit `scripts/config/quality_rules.json`:
```json
{
  "typescript_warnings": [
    { "pattern": "console\\.log", "message": "Remove console.log before commit", "severity": "warn" },
    { "pattern": ": any[^\\w]", "message": "Avoid 'any' type — use 'unknown' + narrowing", "severity": "error" },
    { "pattern": "// @ts-ignore", "message": "@ts-ignore without justification", "severity": "error" },
    { "pattern": "@ts-expect-error(?!.*TODO)", "message": "@ts-expect-error needs TODO comment", "severity": "warn" }
  ]
}
```
