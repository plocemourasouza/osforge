# Eval · routing · claude-sonnet-5

- **Data (UTC):** 2026-09-29T03:41:01Z · duração 223 s
- **Modelo:** `claude-sonnet-5`
- **OSForge:** v5.1.0 · `9a13750` · **árvore suja**
- **HOME usado:** `/Users/paulosouza`
- **Execuções por caso:** 3
- **Comando:** `./scripts/test-orchestrator-routing.sh`
- **Tokens:** in 28 · out 36 · cache_read 727 950 · cache_create 422 076
- **Cota (B-026/B3):** início 5h 42% · fim 5h 42%

## Críticos reprovados

- `r12` — FAIL (0/3): despacho:X(esperado penetration-tester) skill:X(esperado offensive-jwt\|offensive-idor)

**Resultado:** 0/2 PASS (0 %) · FAIL 1 · FLAKY 1

Um caso só é PASS quando acerta nas N execuções. `0 < k < N` é **FLAKY**: instável,
não aprovado — é esta lista que o experimento E1 consome.

| Caso | k de N | Veredito | Detalhe |
|---|---|---|---|
| `r12` | 0/3 | FAIL | despacho:X(esperado penetration-tester) skill:X(esperado offensive-jwt\|offensive-idor) |
| `r01` | 2/3 | FLAKY | agente:OK skill:X(esperado systematic-debugging) |

## Casos instáveis (entrada do E1)

`r01`
