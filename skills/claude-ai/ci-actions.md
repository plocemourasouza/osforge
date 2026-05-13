# Claude CI/CD Actions

**Trigger:** Setting up @claude in PRs/issues, automated PR review, CI/CD integration with Claude, GitHub Actions workflow, flaky test detection.

---

## Setup

```yaml
# .github/workflows/claude-review.yml
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
          mode: review
          max_turns: 10
```

---

## Modes

### Interactive Mode (@claude mentions)
```yaml
- uses: anthropics/claude-code-action@v1
  with:
    mode: interactive
    trigger: "@claude"
```

### Automated PR Review
```yaml
- uses: anthropics/claude-code-action@v1
  with:
    mode: review
    review_scope: changed_files
```

### Structured Output (CI Analysis)
```yaml
- uses: anthropics/claude-code-action@v1
  with:
    mode: analyze
    output_format: json
    analysis_type: flaky_tests
```

---

## MCP Integration in Actions

```yaml
- uses: anthropics/claude-code-action@v1
  with:
    mcp_servers: |
      github:
        command: npx
        args: ["-y", "@anthropic-ai/mcp-server-github"]
```

### CI Log Access Tools
- `mcp__github_ci__get_workflow_runs`
- `mcp__github_ci__get_job_logs`
- `mcp__github_ci__get_check_runs`

---

## Rules

1. **Never hardcode API key** — always use `${{ secrets.ANTHROPIC_API_KEY }}`
2. **Use `--max-turns`** to cap costs
3. **Sonnet 4 for reviews** — optimal cost/quality balance
4. **Limit scope** — review changed files only, not full repo

---

## Flaky Test Detection

```yaml
- uses: anthropics/claude-code-action@v1
  with:
    mode: analyze
    prompt: |
      Analyze test failures in this PR.
      Identify:
      1. Genuinely failing tests
      2. Flaky tests (random failures)
      3. Environment-dependent tests
      Output as JSON with confidence scores.
```

---

## Cost Control

```yaml
- uses: anthropics/claude-code-action@v1
  with:
    max_turns: 5           # Limit iterations
    model: claude-sonnet-4-20250514  # Not Opus unless needed
    timeout: 300           # 5 minute max
```
