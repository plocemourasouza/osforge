# AutoRefine v3 (Autonomous Iteration Loop)

**Trigger:** Improve skill, refine skill, optimize, autorefine, iterate on skill, autoresearch, improvement loop, self-improving, refine code, optimize performance, improve metric.

---

## Purpose

Autonomous iterative refinement loop inspired by Karpathy autoresearch. Generalized to any artifact with a measurable metric — skills, code, prompts, configs, docs.

---

## Core Concepts

### v2 Core Features
1. **Separation: verify + guard**
   - `verify` — measures the primary metric
   - `guard` — protects against regressions

2. **Cross-session memory**
   - Persists KEEP/DISCARD hypotheses via osforge-db
   - Queries before formulating new ones
   - Never repeats failures

3. **Generic mode**
   - Any file with a mechanical metric

### v3 Additions
4. **Meta-optimization**
   - After 10+ accumulated sessions
   - Analyzes aggregate success/failure patterns
   - Proposes adjustments to its own SKILL.md

5. **Cross-domain transfer**
   - KEEP hypotheses with delta ≥1.5%
   - Marked as transfer-candidate
   - Suggested in projects of the same domain

---

## Workflow

```
1. MEASURE baseline
   └── Run verify metric
   └── Record current state

2. HYPOTHESIZE
   └── Query osforge-db for failed attempts
   └── Generate new hypothesis (avoid repeats)

3. IMPLEMENT
   └── Make single, targeted change
   └── Document hypothesis

4. VERIFY
   └── Run verify metric
   └── Run guard checks

5. DECIDE
   └── If improvement: KEEP, record to osforge-db
   └── If regression: DISCARD, revert, record failure
   └── If neutral: DISCARD unless reduces complexity

6. ITERATE
   └── Return to step 2 until target met
```

---

## Maturity Levels

| Level | Symbol | Criteria |
|-------|--------|----------|
| Candidate | 🟡 | First success |
| Validated | 🟢 | 2+ confirmations |
| Proven | 🔵 | 3+ confirmations |

---

## Domain Transfer

```typescript
// When hypothesis succeeds with delta ≥1.5%
{
  hypothesis: "Use cursor-based pagination",
  delta: 0.023,  // 2.3% improvement
  domain: "api-backend",
  status: "transfer-candidate",
  confirmations: 1
}

// In future api-backend projects, suggest this first
```

---

## Commands

```bash
# Start autorefine loop
autorefine start --target skills/my-skill.md --metric accuracy

# Check status
autorefine status

# List hypotheses
osforge-db search "autorefine" --scope global

# View meta-analysis (after 10+ sessions)
autorefine meta-analyze
```

---

## Metrics Examples

| Artifact | Metric |
|----------|--------|
| Skill | Accuracy on test cases |
| Code | Test coverage %, bundle size |
| API | Response time p95, error rate |
| Prompt | Task success rate |
| Config | Build time, memory usage |

---

## Sources

- `karpathy/autoresearch`
- `uditgoenka/autoresearch`
- `alfonsograziano/auto-agent`
- `facebookresearch/HyperAgents` (Meta Research)
