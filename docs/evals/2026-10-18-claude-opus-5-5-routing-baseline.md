# Eval · routing · claude-opus-5-5

- **Data (UTC):** 2026-10-18T13:47:26Z · duração 2508 s
- **Modelo:** `claude-opus-5-5`
- **OSForge:** v5.2.1 · `badf4f9` · **árvore suja**
- **HOME usado:** `/private/tmp/claude-501/-Users-paulosouza-Development-osforge/5189ba77-8c14-4222-ae13-dacecc8e3fe1/scratchpad/home-baseline`
- **Execuções por caso:** 3
- **Comando:** `./scripts/test-orchestrator-routing.sh`
- **Tokens:** in 404 · out 2 952 · cache_read 9 811 420 · cache_create 2 856 522
- **Cota (B-026/B3):** início 5h 2% · fim 5h 37%

## Críticos reprovados

- `r12` — FAIL (0/3): despacho:X(esperado penetration-tester) skill:OK

**Resultado:** 10/16 PASS (62 %) · ERROR 1 · FAIL 1 · FLAKY 4

Um caso só é PASS quando acerta nas N execuções. `0 < k < N` é **FLAKY**: instável,
não aprovado — é esta lista que o experimento E1 consome.

| Caso | k de N | Veredito | Detalhe |
|---|---|---|---|
| `r12` | 0/3 | FAIL | despacho:X(esperado penetration-tester) skill:OK |
| `r02` | 0/3 | ERROR | 3 error(s) (fora do k de N) |
| `r03` | 2/3 | FLAKY | agente:OK skill:X(esperado security-threat-model\|differential-review\|insecure-defaults\|vulnerability-scanner) |
| `r04` | 2/3 | FLAKY | 1 error(s) (fora do k de N) |
| `r14` | 1/3 | FLAKY | 2 error(s) (fora do k de N) |
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

`r03`, `r04`, `r14`, `r16`
