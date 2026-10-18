# Eval · trigger · claude-opus-5-5

- **Data (UTC):** 2026-10-18T14:24:10Z · duração 62 s
- **Modelo:** `claude-opus-5-5`
- **OSForge:** v5.2.1 · `badf4f9` · **árvore suja**
- **HOME usado:** `/private/tmp/claude-501/-Users-paulosouza-Development-osforge/5189ba77-8c14-4222-ae13-dacecc8e3fe1/scratchpad/home-cand`
- **Execuções por caso:** 3
- **Comando:** `./scripts/test-skill-triggering.sh`
- **Tokens:** in 24 · out 48 · cache_read 396 271 · cache_create 141 833
- **Cota (B-026/B3):** início 5h 34% · fim 5h 35%

**Resultado:** 1/1 PASS (100 %)

Um caso só é PASS quando acerta nas N execuções. `0 < k < N` é **FLAKY**: instável,
não aprovado — é esta lista que o experimento E1 consome.

| Caso | k de N | Veredito | Detalhe |
|---|---|---|---|
| `stuck-recovery` | 3/3 | PASS |  |
