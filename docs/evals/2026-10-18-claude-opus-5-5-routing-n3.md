# Eval · routing · claude-opus-5-5

- **Data (UTC):** 2026-10-18T13:50:37Z · duração 2431 s
- **Modelo:** `claude-opus-5-5`
- **OSForge:** v5.2.1 · `badf4f9` · **árvore suja**
- **HOME usado:** `/private/tmp/claude-501/-Users-paulosouza-Development-osforge/5189ba77-8c14-4222-ae13-dacecc8e3fe1/scratchpad/home-cand`
- **Execuções por caso:** 3
- **Comando:** `./scripts/test-orchestrator-routing.sh`
- **Tokens:** in 394 · out 1 794 · cache_read 9 135 089 · cache_create 2 528 581
- **Cota (B-026/B3):** início 5h 3% · fim 5h 38%

## Críticos reprovados

- `r12` — FAIL (0/3): despacho:X(esperado penetration-tester) skill:X(esperado offensive-jwt\|offensive-idor)

**Resultado:** 10/16 PASS (62 %) · ERROR 1 · FAIL 3 · FLAKY 2

Um caso só é PASS quando acerta nas N execuções. `0 < k < N` é **FLAKY**: instável,
não aprovado — é esta lista que o experimento E1 consome.

| Caso | k de N | Veredito | Detalhe |
|---|---|---|---|
| `r03` | 0/3 | FAIL | agente:OK skill:X(esperado security-threat-model\|differential-review\|insecure-defaults\|vulnerability-scanner) |
| `r12` | 0/3 | FAIL | despacho:X(esperado penetration-tester) skill:X(esperado offensive-jwt\|offensive-idor) |
| `r14` | 0/3 | FAIL | agente:OK skill:X(esperado plan-writing\|osforge-canvas) tier:OK, 1 error(s) (fora do k de N) |
| `r02` | 0/3 | ERROR | 3 error(s) (fora do k de N) |
| `r04` | 1/3 | FLAKY | 2 error(s) (fora do k de N) |
| `r16` | 2/3 | FLAKY | 1 error(s) (fora do k de N) |
| `r01` | 3/3 | PASS |  |
| `r05` | 3/3 | PASS |  |
| `r06` | 3/3 | PASS |  |
| `r07` | 3/3 | PASS |  |
| `r08` | 3/3 | PASS |  |
| `r09` | 3/3 | PASS |  |
| `r10` | 3/3 | PASS |  |
| `r11` | 3/3 | PASS |  |
| `r13` | 3/3 | PASS |  |
| `r15` | 3/3 | PASS |  |

## Casos instáveis (entrada do E1)

`r04`, `r16`
