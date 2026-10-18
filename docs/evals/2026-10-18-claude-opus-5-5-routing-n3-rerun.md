# Eval · routing · claude-opus-5-5

- **Data (UTC):** 2026-10-18T14:26:32Z · duração 256 s
- **Modelo:** `claude-opus-5-5`
- **OSForge:** v5.2.1 · `badf4f9` · **árvore suja**
- **HOME usado:** `/private/tmp/claude-501/-Users-paulosouza-Development-osforge/5189ba77-8c14-4222-ae13-dacecc8e3fe1/scratchpad/home-cand2`
- **Execuções por caso:** 3
- **Comando:** `./scripts/test-orchestrator-routing.sh`
- **Tokens:** in 44 · out 169 · cache_read 920 190 · cache_create 288 808
- **Cota (B-026/B3):** início 5h 35% · fim 5h 38%

**Resultado:** 0/2 PASS (0 %) · FLAKY 2

Um caso só é PASS quando acerta nas N execuções. `0 < k < N` é **FLAKY**: instável,
não aprovado — é esta lista que o experimento E1 consome.

| Caso | k de N | Veredito | Detalhe |
|---|---|---|---|
| `r03` | 1/3 | FLAKY | agente:OK skill:X(esperado security-threat-model\|differential-review\|insecure-defaults\|vulnerability-scanner) |
| `r14` | 2/3 | FLAKY | agente:OK skill:X(esperado plan-writing\|osforge-canvas) tier:OK |

## Casos instáveis (entrada do E1)

`r03`, `r14`
