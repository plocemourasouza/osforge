---
name: verification-before-completion
description: Requires running verification commands and confirming output before making any success claims. Use when about to claim work is complete, fixed, passing, or done. Ensures evidence before assertions. Triggers before commits, PRs, or any completion statement.
---

# Verification Before Completion

Claiming work is complete without verification is dishonesty, not efficiency.

**Core principle:** Evidence before claims, always.

## The Iron Law

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

If you haven't run the verification command in this message, you cannot claim it passes.

## The Gate Function

Before claiming any status or expressing satisfaction:

1. **IDENTIFY**: What command proves this claim?
2. **RUN**: Execute the FULL command (fresh, complete — not from cache)
3. **READ**: Full output, check exit code, count failures
4. **VERIFY**: Does output actually confirm the claim?
   - If NO → State actual status with evidence
   - If YES → State claim WITH evidence
5. **ONLY THEN**: Make the claim

Skip any step = lying, not verifying.

## Evidence Requirements

| Claim | Requires | NOT Sufficient |
|-------|----------|----------------|
| "Tests pass" | Test command output: 0 failures | Previous run, "should pass" |
| "Lint clean" | Linter output: 0 errors | Partial check, extrapolation |
| "Build succeeds" | Build command: exit 0 | Linter passing, "looks good" |
| "Bug fixed" | Test original symptom: passes | Code changed, assumed fixed |
| "No regressions" | Full suite: all pass | Only new tests pass |
| "Types correct" | `tsc --noEmit`: exit 0 | No red squiggles in editor |

## Red Flags — STOP Immediately

You are about to violate this skill if you catch yourself:

- Using **"should"**, "probably", "seems to", "likely works"
- Expressing satisfaction before verification: "Great!", "Perfect!", "Done!"
- About to commit or push without running the test suite
- Trusting a previous run as evidence for current state
- Relying on partial verification ("lint passes so types must be fine")
- Thinking "just this once" or "it's a small change"
- Feeling tired and wanting to wrap up

## Verification Commands Reference

```bash
# TypeScript types
bun tsc --noEmit

# Lint
bun run lint

# Unit + Integration tests
bun run test

# E2E tests
bun run test:e2e

# Full build
bun run build

# Prisma (after schema changes)
bun prisma generate && bun tsc --noEmit
```

---

## Project-level Validation Scripts

Para projetos que precisam de verificações sistemáticas além do pipeline do Claude Code,
o OSForge fornece um template de script invocável diretamente.

### Instalar no projeto

```bash
cp ~/.claude/hooks/validate.py .scripts/validate.py
chmod +x .scripts/validate.py
```

### Executar

```bash
# Checklist rápido durante desenvolvimento
python3 .scripts/validate.py --quick

# Verificação completa antes de deploy
python3 .scripts/validate.py --full

# Verificar domínio específico
python3 .scripts/validate.py --domain types
python3 .scripts/validate.py --domain tests
python3 .scripts/validate.py --domain build
python3 .scripts/validate.py --domain security
```

### Personalizar para o projeto

O script lê `.scripts/validate.config.json` se existir:

```json
{
  "commands": {
    "types": "bun tsc --noEmit",
    "lint": "bun run lint",
    "tests": "bun run test",
    "build": "bun run build",
    "prisma": "bun prisma validate"
  },
  "quick": ["types", "lint"],
  "full": ["types", "lint", "tests", "build"],
  "pre_deploy": ["types", "lint", "tests", "build", "prisma"]
}
```

O template base está em `hooks/validate.py` no repositório OSForge.

### Integração com o Orchestrator

O Orchestrator pode invocar o script no step de ROUTE ao completar cada fase:
```
"Fase N concluída. Executando validação..."
→ python3 .scripts/validate.py --quick
→ Reportar resultado antes de avançar para a próxima fase
```

## Correct Completion Format

```
✅ Verified:
- `bun run lint` → 0 errors, 0 warnings
- `bun run test` → 14 tests passed, 0 failed
- `bun tsc --noEmit` → exit 0

The feature is complete and ready for review.
```

## Incorrect Completion Format

```
❌ WRONG:
"I've implemented the feature and it should work correctly.
The tests should pass since the logic is straightforward."
```
