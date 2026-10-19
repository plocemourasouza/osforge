# Eval · routing · claude-opus-5-5

- **Data (UTC):** 2026-10-18T14:26:40Z · duração 447 s
- **Modelo:** `claude-opus-5-5`
- **OSForge:** v5.2.1 · `badf4f9` · **árvore suja**
- **HOME usado:** `/private/tmp/claude-501/-Users-paulosouza-Development-osforge/5189ba77-8c14-4222-ae13-dacecc8e3fe1/scratchpad/home-baseline`
- **Execuções por caso:** 3
- **Comando:** `./scripts/test-orchestrator-routing.sh`
- **Tokens:** in 64 · out 1 084 · cache_read 1 624 333 · cache_create 361 101
- **Cota (B-026/B3):** início 5h 35% · fim 5h 38%

**Resultado:** 1/2 PASS (50 %) · FAIL 1

Um caso só é PASS quando acerta nas N execuções. `0 < k < N` é **FLAKY**: instável,
não aprovado — é esta lista que o experimento E1 consome.

| Caso | k de N | Veredito | Detalhe |
|---|---|---|---|
| `r03` | 0/3 | FAIL | agente:OK skill:X(esperado security-threat-model\|differential-review\|insecure-defaults\|vulnerability-scanner) |
| `r14` | 3/3 | PASS |  |
