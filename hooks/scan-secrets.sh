#!/bin/bash
# Hook: beforeShellExecution (CAN BLOCK via JSON output)
# Scans for secrets before git commit and blocks dangerous commands

input=$(cat)
command=$(echo "$input" | python3 -c "import sys,json; print(json.load(sys.stdin).get('command',''))" 2>/dev/null)

# Block dangerous destructive commands
if echo "$command" | grep -qE 'rm\s+-rf\s+(/|\$HOME|~|\.\./)'; then
  echo '{"continue": false, "permission": "deny", "userMessage": "⛔ Comando destrutivo bloqueado", "agentMessage": "This destructive command was blocked by a safety hook. Never run rm -rf on root, home, or parent directories."}'
  exit 0
fi

# Scan for secrets before git commit
if echo "$command" | grep -qE 'git\s+(commit|push)'; then
  workspace=$(echo "$input" | python3 -c "import sys,json; roots=json.load(sys.stdin).get('workspace_roots',[]); print(roots[0] if roots else '.')" 2>/dev/null)
  
  # Check staged files for secrets patterns
  secrets_found=$(cd "$workspace" 2>/dev/null && git diff --cached --name-only 2>/dev/null | xargs grep -lE '(PRIVATE_KEY|SECRET_KEY|API_SECRET|aws_secret|password\s*=\s*["'\'']).{8,}' 2>/dev/null | head -5)
  
  if [ -n "$secrets_found" ]; then
    echo "{\"continue\": false, \"permission\": \"deny\", \"userMessage\": \"⛔ Possíveis secrets detectados nos arquivos staged: $secrets_found\", \"agentMessage\": \"BLOCKED: Potential secrets/credentials found in staged files. Review and remove sensitive data before committing. Files: $secrets_found\"}"
    exit 0
  fi
fi

# Allow everything else
echo '{"continue": true, "permission": "allow"}'
