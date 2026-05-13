# Smart Model Dispatch

**Trigger:** Feature implementation with multiple subtasks, spawning subagents, parallel task dispatch, cost optimization, or when task complexity varies across work units.

---

## 3-Tier Routing

| Tier | Model | Use Cases |
|------|-------|-----------|
| **Opus** | `claude-opus-4-5-20251101` | Planning, security audits, architecture decisions |
| **Sonnet** | `claude-sonnet-4-20250514` | Implementation, debugging, code review |
| **Haiku** | `claude-3-5-haiku-20241022` | Boilerplate, i18n, tests, docs, simple tasks |

---

## Per-Agent Model Mapping

```typescript
const agentModels = {
  // Opus tier — high reasoning
  planner: 'claude-opus-4-5-20251101',
  architect: 'claude-opus-4-5-20251101',
  securityAuditor: 'claude-opus-4-5-20251101',

  // Sonnet tier — balanced
  debugger: 'claude-sonnet-4-20250514',
  codeReviewer: 'claude-sonnet-4-20250514',
  implementer: 'claude-sonnet-4-20250514',

  // Haiku tier — fast/cheap
  docWriter: 'claude-3-5-haiku-20241022',
  testWriter: 'claude-3-5-haiku-20241022',
  i18nTranslator: 'claude-3-5-haiku-20241022',
  boilerplate: 'claude-3-5-haiku-20241022',
}
```

---

## Dispatch Patterns

### Feature Implementation
```
1. Opus: Plan & decompose feature → tasks
2. Sonnet: Implement each task (parallel)
3. Haiku: Generate tests for each component
4. Sonnet: Review & integrate
5. Opus: Final security review
```

### Bug Fix Workflow
```
1. Sonnet: Reproduce & diagnose
2. Sonnet: Implement fix
3. Haiku: Add regression test
4. Sonnet: Review fix
```

### Security Audit
```
1. Opus: Threat modeling
2. Opus: Vulnerability analysis
3. Sonnet: Fix recommendations
4. Opus: Re-audit fixes
```

---

## Parallel Dispatch with Mixed Models

```typescript
// Launch parallel tasks with appropriate models
await Promise.all([
  // Heavy reasoning task
  runAgent({
    model: 'claude-opus-4-5-20251101',
    task: 'Analyze architecture implications'
  }),
  // Implementation tasks
  runAgent({
    model: 'claude-sonnet-4-20250514',
    task: 'Implement API endpoint'
  }),
  // Simple generation
  runAgent({
    model: 'claude-3-5-haiku-20241022',
    task: 'Generate i18n translations'
  }),
])
```

---

## Cost Estimation

| Model | Input $/1M | Output $/1M |
|-------|-----------|-------------|
| Opus 4.5 | $15.00 | $75.00 |
| Sonnet 4 | $3.00 | $15.00 |
| Haiku 3.5 | $0.80 | $4.00 |

**Savings:** Mixed-model dispatch achieves ~65% cost reduction vs all-Opus.

---

## Escalation Rules

```
Haiku fails → Escalate to Sonnet
Sonnet fails → Escalate to Opus
Opus fails → Human intervention
```

### Failure Signals
- Repeated incorrect outputs
- Task exceeds model capability
- Security-sensitive operation detected
- Complex reasoning required
