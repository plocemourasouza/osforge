# Smart Hooks (Python)

**Trigger:** Setting up quality gates, safety rails, or developer experience hooks for Claude Code. Also trigger when configuring pre-commit checks, blocking dangerous commands, or adding audit logging to a project.

---

## Hook Types

| Hook | When | Purpose |
|------|------|---------|
| `pre_tool_use` | Before tool execution | Block dangerous commands |
| `post_tool_use` | After tool execution | Quality gates |
| `pre_compact` | Before context compaction | Backup conversation |
| `session_end` | When session ends | Logging, notifications |

---

## pre_tool_use.py

Blocks dangerous bash commands + protected file writes + audit log.

```python
#!/usr/bin/env python3
import json
import sys

DANGEROUS_COMMANDS = [
    'rm -rf /',
    'git push --force',
    'DROP TABLE',
    'DELETE FROM',
]

PROTECTED_FILES = [
    '.env',
    '.env.local',
    'secrets.json',
]

def main():
    hook_data = json.loads(sys.stdin.read())
    tool_name = hook_data.get('tool_name')
    tool_input = hook_data.get('tool_input', {})

    # Block dangerous bash commands
    if tool_name == 'bash':
        command = tool_input.get('command', '')
        for dangerous in DANGEROUS_COMMANDS:
            if dangerous in command:
                print(json.dumps({
                    'decision': 'block',
                    'reason': f'Blocked dangerous command: {dangerous}'
                }))
                return

    # Block writes to protected files
    if tool_name in ('write', 'edit'):
        file_path = tool_input.get('file_path', '')
        for protected in PROTECTED_FILES:
            if protected in file_path:
                print(json.dumps({
                    'decision': 'block',
                    'reason': f'Cannot modify protected file: {protected}'
                }))
                return

    print(json.dumps({'decision': 'allow'}))

if __name__ == '__main__':
    main()
```

---

## post_tool_use.py

TypeScript quality gates: console.log, any type, @ts-ignore, export default.

```python
#!/usr/bin/env python3
import json
import sys
import re

VIOLATIONS = [
    (r'console\.log\(', 'Remove console.log'),
    (r': any\b', 'Replace any with proper type'),
    (r'@ts-ignore', 'Remove @ts-ignore'),
    (r'export default', 'Use named exports'),
]

def main():
    hook_data = json.loads(sys.stdin.read())
    tool_name = hook_data.get('tool_name')
    tool_output = hook_data.get('tool_output', {})

    if tool_name in ('write', 'edit'):
        content = tool_output.get('content', '')
        warnings = []

        for pattern, message in VIOLATIONS:
            if re.search(pattern, content):
                warnings.append(message)

        if warnings:
            print(json.dumps({
                'warnings': warnings,
                'action': 'continue'  # Warn but don't block
            }))
            return

    print(json.dumps({'action': 'continue'}))

if __name__ == '__main__':
    main()
```

---

## Configuration

```json
// ~/.claude/settings.json
{
  "hooks": {
    "pre_tool_use": ["python3", "~/.claude/hooks/pre_tool_use.py"],
    "post_tool_use": ["python3", "~/.claude/hooks/post_tool_use.py"],
    "pre_compact": ["python3", "~/.claude/hooks/pre_compact.py"],
    "session_end": ["python3", "~/.claude/hooks/session_end.py"]
  }
}
```

---

## Design Principles

1. **Command hooks, not prompt** — zero token cost
2. **Fail-open** — if hook crashes, allow operation
3. **<100ms each** — hooks must be fast
4. **Configurable via JSON** — easy to adjust rules
