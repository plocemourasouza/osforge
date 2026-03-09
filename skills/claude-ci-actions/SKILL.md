---
name: claude-ci-actions
description: "Automate PR review, issue triage, and CI/CD tasks with Claude Code GitHub Actions. TRIGGER when: setting up @claude in PRs/issues, configuring automated code review, CI/CD integration with Claude, GitHub Actions workflow with Claude, or debugging Claude-powered automation pipelines."
metadata:
  author: osforge
  version: '1.0'
  source: anthropics/claude-code-action
---

# Claude CI/CD Actions (GitHub Actions)

## Overview
`anthropics/claude-code-action@v1` integrates Claude Code into GitHub Actions for automated PR review, @claude mentions in issues, and CI/CD automation.

## Quick Setup
```bash
# In Claude Code terminal — installs GitHub App + secrets automatically
/install-github-app
```

## Workflow — Interactive (@claude mentions)
```yaml
# .github/workflows/claude.yml
name: Claude Code
on:
  issue_comment:
    types: [created]
  pull_request_review_comment:
    types: [created]
  issues:
    types: [opened, assigned]

permissions:
  contents: write
  pull-requests: write
  issues: write
  actions: read

jobs:
  claude:
    if: |
      (github.event_name == 'issue_comment' && contains(github.event.comment.body, '@claude')) ||
      (github.event_name == 'pull_request_review_comment' && contains(github.event.comment.body, '@claude')) ||
      (github.event_name == 'issues' && contains(github.event.issue.body, '@claude'))
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 1
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          additional_permissions: |
            actions: read
```

## Workflow — Automated PR Review
```yaml
name: Claude PR Review
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: |
            Review this PR focusing on:
            1. Security vulnerabilities (auth, injection, data exposure)
            2. Type safety (TypeScript strict mode compliance)
            3. Test coverage gaps
            4. Performance issues (N+1 queries, missing indexes)
          claude_args: |
            --max-turns 10
            --model claude-sonnet-4-6
```

## Workflow — Structured Output (Flaky Test Detection)
```yaml
- name: Detect flaky tests
  id: analyze
  uses: anthropics/claude-code-action@v1
  with:
    anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
    prompt: |
      Check the CI logs and determine if this is a flaky test.
    claude_args: |
      --json-schema '{"type":"object","properties":{"is_flaky":{"type":"boolean"},"confidence":{"type":"number"},"summary":{"type":"string"}},"required":["is_flaky"]}'

- name: Retry if flaky
  if: fromJSON(steps.analyze.outputs.structured_output).is_flaky == true
  run: gh workflow run CI
```

## Key Inputs

| Input | Description |
|---|---|
| `anthropic_api_key` | API key (use `${{ secrets.ANTHROPIC_API_KEY }}`) |
| `prompt` | Direct prompt for automation mode |
| `claude_args` | CLI args: `--max-turns`, `--model`, `--system-prompt`, `--json-schema` |
| `trigger_phrase` | Custom trigger (default: `@claude`) |
| `assignee_trigger` | Trigger on issue assignment (e.g., `claude-bot`) |
| `additional_permissions` | Extra perms (e.g., `actions: read` for CI logs) |
| `plugins` | Install plugins: `code-review@claude-code-plugins` |

## CI Access Tools (when `actions: read` enabled)
- `mcp__github_ci__get_ci_status` — View workflow run statuses
- `mcp__github_ci__get_workflow_run_details` — Detailed workflow info
- `mcp__github_ci__download_job_log` — Download and analyze job logs

## MCP Integration in Actions
```yaml
claude_args: |
  --mcp-config '{"mcpServers": {"supabase": {"command": "npx", "args": ["supabase-mcp-server"]}}}'
```

## Automation Patterns

### Issue → PR Creation
Comment `@claude create pull request` on an issue — Claude generates the PR with all changes.

### Auto-Documentation on Merge
```yaml
on:
  push:
    branches: [main]
jobs:
  docs:
    runs-on: ubuntu-latest
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          prompt: "Update the API documentation based on recent code changes"
```

## Security Rules
- NEVER hardcode `ANTHROPIC_API_KEY` — always use `${{ secrets.* }}`
- Limit `allowed_tools` to only what's needed: `"Bash(bun run test),Read,Edit"`
- Set `--max-turns` to prevent runaway costs
- Use `claude-sonnet-4-6` for review tasks (cheaper, fast enough)
- Review Claude's suggestions before merging — don't auto-merge
- CLAUDE.md in repo root guides Claude's behavior in Actions

## Cost Awareness
- GitHub Actions minutes consumed per run
- API tokens per interaction (proportional to prompt + context)
- Use `--max-turns 10` to cap costs
- Sonnet 4.6 ($3/$15 per 1M tokens) for review, Opus 4.6 ($5/$25) for complex tasks
