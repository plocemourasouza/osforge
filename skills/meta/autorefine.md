# AutoRefine v3 (Autonomous Iteration Loop)

**Trigger:** Melhorar skill, refinar skill, otimizar, autorefine, iterar sobre skill, autoresearch, loop de melhoria, self-improving, refinar código, otimizar performance, melhorar métrica.

---

## Purpose

Loop autônomo de refinamento iterativo inspirado no Karpathy autoresearch. Generalizado para qualquer artefato com métrica mensurável — skills, código, prompts, configs, docs.

---

## Core Concepts

### v2 Core Features
1. **Separation: verify + guard**
   - `verify` — mede a métrica principal
   - `guard` — protege contra regressões

2. **Cross-session memory**
   - Persiste hipóteses KEEP/DISCARD via osforge-db
   - Consulta antes de formular novas
   - Nunca repete falhas

3. **Generic mode**
   - Qualquer arquivo com métrica mecânica

### v3 Additions
4. **Meta-optimization**
   - Após 10+ sessões acumuladas
   - Analisa padrões agregados de sucesso/falha
   - Propõe ajustes ao próprio SKILL.md

5. **Cross-domain transfer**
   - Hipóteses KEEP com delta ≥1.5%
   - Marcadas como transfer-candidate
   - Sugeridas em projetos do mesmo domínio

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

| Artefato | Métrica |
|----------|---------|
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
