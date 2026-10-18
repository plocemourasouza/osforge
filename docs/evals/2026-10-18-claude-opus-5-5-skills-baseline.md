# Eval · trigger · claude-opus-5-5

- **Data (UTC):** 2026-10-18T13:50:54Z · duração 1942 s
- **Modelo:** `claude-opus-5-5`
- **OSForge:** v5.2.1 · `badf4f9` · **árvore suja**
- **HOME usado:** `/private/tmp/claude-501/-Users-paulosouza-Development-osforge/5189ba77-8c14-4222-ae13-dacecc8e3fe1/scratchpad/home-baseline`
- **Execuções por caso:** 3
- **Comando:** `./scripts/test-skill-triggering.sh`
- **Tokens:** in 418 · out 1 443 · cache_read 7 653 156 · cache_create 3 520 279
- **Cota (B-026/B3):** início 5h 3% · fim 5h 34%

**Resultado:** 16/28 PASS (57 %) · ERROR 8 · FLAKY 4

Um caso só é PASS quando acerta nas N execuções. `0 < k < N` é **FLAKY**: instável,
não aprovado — é esta lista que o experimento E1 consome.

| Caso | k de N | Veredito | Detalhe |
|---|---|---|---|
| `aesthetic-boost` | 0/3 | ERROR | 3 error(s) (fora do k de N) |
| `asaas-integration` | 0/3 | ERROR | 3 error(s) (fora do k de N) |
| `asaas-integration` | 0/3 | ERROR | 3 error(s) (fora do k de N) |
| `better-auth` | 0/3 | ERROR | 3 error(s) (fora do k de N) |
| `better-auth` | 0/3 | ERROR | 3 error(s) (fora do k de N) |
| `frontend-ui-system` | 0/3 | ERROR | 3 error(s) (fora do k de N) |
| `llm-structured-output` | 0/3 | ERROR | 3 error(s) (fora do k de N) |
| `llm-structured-output` | 0/3 | ERROR | 3 error(s) (fora do k de N) |
| `nextjs-supabase-auth` | 1/3 | FLAKY | 2 error(s) (fora do k de N) |
| `prisma-expert` | 1/3 | FLAKY | 2 error(s) (fora do k de N) |
| `spec-builder` | 1/3 | FLAKY | 2 error(s) (fora do k de N) |
| `system-diagrams` | 2/3 | FLAKY | 1 error(s) (fora do k de N) |
| `adversarial-review` | 3/3 | PASS |  |
| `aws-deploy` | 3/3 | PASS |  |
| `aws-deploy` | 3/3 | PASS |  |
| `context-compact` | 3/3 | PASS |  |
| `epic-decomposer` | 3/3 | PASS |  |
| `finishing-a-development-branch` | 3/3 | PASS |  |
| `osforge-canvas` | 3/3 | PASS |  |
| `output-enforcement` | 3/3 | PASS |  |
| `security-best-practices` | 3/3 | PASS |  |
| `story-executor` | 3/3 | PASS |  |
| `stuck-recovery` | 3/3 | PASS |  |
| `system-diagrams` | 3/3 | PASS |  |
| `system-diagrams` | 3/3 | PASS |  |
| `systematic-debugging` | 3/3 | PASS |  |
| `tdd-workflow` | 3/3 | PASS |  |
| `verification-before-completion` | 3/3 | PASS |  |

## Casos instáveis (entrada do E1)

`spec-builder`, `nextjs-supabase-auth`, `prisma-expert`, `system-diagrams`
