---
name: systematic-debugging
description: "Debugging sistemático em 4 fases com análise de causa raiz. ACIONE quando: bug difícil de reproduzir, crash sem stacktrace claro, comportamento intermitente, regressão sem causa óbvia, investigação profunda de root cause. Keywords: debug, bug, error, crash, fix, issue, not working, broken, regression, investigate."
model: sonnet
context: fork
agent: general-purpose
allowed-tools: Read, Bash, Glob, Grep
metadata:
  author: antigravity-kit (adapted)
  version: "1.1"
  source: "antigravity-kit"
---

# Systematic Debugging

> Source: obra/superpowers

## Overview
This skill provides a structured approach to debugging that prevents random guessing and ensures problems are properly understood before solving.

## 4-Phase Debugging Process

### Phase 1: Reproduce
Before fixing, reliably reproduce the issue.

```markdown
## Reproduction Steps
1. [Exact step to reproduce]
2. [Next step]
3. [Expected vs actual result]

## Reproduction Rate
- [ ] Always (100%)
- [ ] Often (50-90%)
- [ ] Sometimes (10-50%)
- [ ] Rare (<10%)
```

### Phase 2: Isolate
Narrow down the source.

```markdown
## Isolation Questions
- When did this start happening?
- What changed recently?
- Does it happen in all environments?
- Can we reproduce with minimal code?
- What's the smallest change that triggers it?
```

### Phase 3: Understand
Find the root cause, not just symptoms.

```markdown
## Root Cause Analysis
### The 5 Whys
1. Why: [First observation]
2. Why: [Deeper reason]
3. Why: [Still deeper]
4. Why: [Getting closer]
5. Why: [Root cause]
```

### Phase 4: Fix & Verify
Fix and verify it's truly fixed.

```markdown
## Fix Verification
- [ ] Bug no longer reproduces
- [ ] Related functionality still works
- [ ] No new issues introduced
- [ ] Test added to prevent regression
```

## Debugging Checklist

```markdown
## Before Starting
- [ ] Can reproduce consistently
- [ ] Have minimal reproduction case
- [ ] Understand expected behavior

## During Investigation
- [ ] Check recent changes (git log)
- [ ] Check logs for errors
- [ ] Add logging if needed
- [ ] Use debugger/breakpoints

## After Fix
- [ ] Root cause documented
- [ ] Fix verified
- [ ] Regression test added
- [ ] Similar code checked
```

## Common Debugging Commands

```bash
# Recent changes
git log --oneline -20
git diff HEAD~5

# Search for pattern
grep -r "errorPattern" --include="*.ts"

# Check logs
pm2 logs app-name --err --lines 100
```

## Anti-Patterns

❌ **Random changes** - "Maybe if I change this..."
❌ **Ignoring evidence** - "That can't be the cause"
❌ **Assuming** - "It must be X" without proof
❌ **Not reproducing first** - Fixing blindly
❌ **Stopping at symptoms** - Not finding root cause

---

## Gotchas

- **Começar a corrigir antes de reproduzir**: a causa mais comum de fix errado. Sempre reproduza de forma confiável antes de qualquer mudança — se não consegue reproduzir, não sabe o que está corrigindo.
- **Parar nos sintomas**: "o botão não funciona" é sintoma, não causa. Sempre aprofundar com os 5 Whys até chegar a uma causa que faz sentido mecanicamente. Parar na primeira explicação plausível é o erro mais frequente.
- **Não checar `git log` primeiro**: a maioria dos bugs tem correlação temporal com uma mudança recente. `git log --oneline -20` deve ser a primeira ação, não a última.
- **Múltiplas mudanças simultâneas**: ao testar uma hipótese, faça UMA mudança por vez. Múltiplas mudanças simultâneas tornam impossível identificar o que corrigiu o problema — ou introduziu outro.
- **Assumir ambiente idêntico**: comportamentos diferentes entre dev/staging/prod geralmente indicam variáveis de ambiente, dados de seed ou versões de dependência diferentes. Sempre verificar com `node -e "require('./package.json').dependencies"` ou equivalente.
- **Não adicionar regression test**: depois de corrigir, sempre adicionar um teste que falha sem o fix e passa com ele. Sem isso, o bug voltará em 3 meses.
