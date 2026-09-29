# Eval · routing · claude-sonnet-5

- **Data (UTC):** 2026-09-29T03:45:03Z · duração 2197 s
- **Modelo:** `claude-sonnet-5`
- **OSForge:** v5.1.0 · `9a13750` · **árvore suja**
- **HOME usado:** `/Users/paulosouza`
- **Execuções por caso:** 3
- **Comando:** `./scripts/test-orchestrator-routing.sh`
- **Tokens:** in 354 · out 834 · cache_read 12 615 354 · cache_create 2 973 173

## Críticos reprovados

- `r12` — FAIL (0/3): despacho:X(esperado penetration-tester) skill:OK

**Resultado:** 1/16 PASS (6 %) · ERROR 1 · FAIL 8 · FLAKY 6

Um caso só é PASS quando acerta nas N execuções. `0 < k < N` é **FLAKY**: instável,
não aprovado — é esta lista que o experimento E1 consome.

| Caso | k de N | Veredito | Detalhe |
|---|---|---|---|
| `r03` | 0/3 | FAIL | agente:OK skill:X(esperado security-threat-model\|differential-review\|insecure-defaults\|vulnerability-scanner) |
| `r06` | 0/3 | FAIL | agente:OK skill:X(esperado aws-deploy\|deployment-procedures) |
| `r07` | 0/3 | FAIL | agente:OK skill:X(esperado mobile-design\|app-builder) |
| `r09` | 0/3 | FAIL | agente:OK skill:X(esperado seo-fundamentals\|genai-optimization) |
| `r11` | 0/3 | FAIL | agente:X(esperado code-refactorer\|code-archaeologist) skill:X(esperado clean-code\|codebase-design\|plan-writing) |
| `r12` | 0/3 | FAIL | despacho:X(esperado penetration-tester) skill:OK |
| `r14` | 0/3 | FAIL | agente:OK skill:X(esperado plan-writing\|osforge-canvas) tier:OK |
| `r15` | 0/3 | FAIL | agente:X(esperado git-commit-helper) |
| `r16` | 0/3 | ERROR | agente:OK skill:X(esperado docs-writer\|documentation-templates), 1 error(s) (fora do k de N) |
| `r01` | 2/3 | FLAKY | agente:OK skill:X(esperado systematic-debugging) |
| `r02` | 1/3 | FLAKY | 2 error(s) (fora do k de N) |
| `r04` | 1/3 | FLAKY | agente:OK skill:X(esperado database-design\|postgres-optimization), 1 error(s) (fora do k de N) |
| `r05` | 1/3 | FLAKY | agente:OK skill:X(esperado tdd-workflow\|webapp-testing\|e2e-testing-patterns), 1 error(s) (fora do k de N) |
| `r08` | 1/3 | FLAKY | agente:OK skill:X(esperado game-development\|web-games\|2d-games\|brainstorming) |
| `r10` | 1/3 | FLAKY | agente:OK skill:X(esperado performance-profiling\|react-performance\|nextjs-react-expert\|core-web-vitals) |
| `r13` | 3/3 | PASS |  |

## Casos instáveis (entrada do E1)

`r01`, `r02`, `r04`, `r05`, `r08`, `r10`
