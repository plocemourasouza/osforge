# Eval · routing · claude-opus-5-5

- **Data (UTC):** 2026-10-18T14:34:57Z · duração 497 s
- **Modelo:** `claude-opus-5-5`
- **OSForge:** v5.2.1 · `badf4f9` · **árvore suja**
- **HOME usado:** `/private/tmp/claude-501/-Users-paulosouza-Development-osforge/5189ba77-8c14-4222-ae13-dacecc8e3fe1/scratchpad/home-cand3`
- **Execuções por caso:** 3
- **Comando:** `./scripts/test-orchestrator-routing.sh`
- **Tokens:** in 66 · out 1 118 · cache_read 1 718 703 · cache_create 364 911
- **Cota (B-026/B3):** início 5h 38% · fim 5h 40%

**Resultado:** 1/2 PASS (50 %) · FLAKY 1

Um caso só é PASS quando acerta nas N execuções. `0 < k < N` é **FLAKY**: instável,
não aprovado — é esta lista que o experimento E1 consome.

| Caso | k de N | Veredito | Detalhe |
|---|---|---|---|
| `r14` | 1/3 | FLAKY | 2 error(s) (fora do k de N) |
| `r03` | 3/3 | PASS |  |

## Casos instáveis (entrada do E1)

`r14`
