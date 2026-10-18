# Memory recall eval (`osforge-db`)

Measures whether a natural-language question finds the decision it is about:
**hit@1** (the target is the first row) and **hit@5** (the target is in the top 5).

| File | What |
|---|---|
| `decisions.tsv` | 15 **synthetic** decisions (3 fictional projects, mixed pt-BR/en, pinned `created_at`). No real project data — keep it that way. |
| `questions.tsv` | 16 questions written the way an agent asks, not copied from the decision text; 3 are temporal (`since`/`until` columns → `--since`/`--until`). A gold of `D02\|D07` counts a hit on either. |
| `questions-expanded.tsv` | The same 16 questions rewritten the way an agent should query before searching: 4-8 keywords, English plus the pt-BR terms, code/file names. Same order and gold/since/until columns. |
| `run.py` | Builds a throwaway DB from the fixture through the real CLI and asks every question. |

Every run uses its own temp dir for `OSFORGE_DB`, `OSFORGE_CONFIG` and `HOME`; the live
`~/.osforge` is never opened.

```bash
# Lexical leg only (OSFORGE_EMBED=off, the default mode of the product) — fully offline;
# this is what CI runs, with a floor per set
python3 scripts/evals/memory/run.py --mode=fts --set=natural  --floor=0.8  [--verbose]
python3 scripts/evals/memory/run.py --mode=fts --set=expanded --floor=0.95 [--verbose]

# Hybrid (RRF of FTS5 + vector) — embeds the fixture with Ollama first.
# Ollama not reachable → prints SKIP and exits 0 (nothing is started for you).
python3 scripts/evals/memory/run.py --mode=hybrid

# Brain (ADR-017): `brain migrate` into a temp qdrant LOCAL store, then `recall`.
# Default embedder `fake` (deterministic, no model — what tests/test-brain.sh runs); with
# OSFORGE_BRAIN_EMBED=gemma it uses the real model if cached (~/.osforge/models or
# OSFORGE_BRAIN_MODELS) and the venv (~/.osforge/venv or OSFORGE_BRAIN_PYTHON); missing → SKIP.
python3 scripts/evals/memory/run.py --mode=brain [--recall=dense|keyword|hybrid] [--db=... --questions=...]

# Your own database: a COPY is queried (SQLite backup from a read-only handle);
# the questions file holds numeric decision ids in the gold column.
python3 scripts/evals/memory/run.py --mode=fts --db=/path/to/copy.db --questions=my-questions.tsv
```

Output: `mode=fts set=natural db=fixture n=16 hit@1=15/16 (94%) hit@5=15/16 (94%) miss=['D10']`.
Exit 1 when `--floor` is given and hit@5 is below it.

**Natural vs expanded.** The lexical leg matches words, so the agent acts as the semantic
layer when it searches FTS-only: it expands the question into keywords before it searches (guidance in the
`db-state-sync` skill). Fixture, FTS-only: natural hit@5 15/16 (94%), expanded 16/16 (100%).
Real data (14 private questions, not in the repo): natural 11/14, expanded 14/14. The
expansions were written knowing the target decision, so expanded is an optimistic bound, not a
forecast of what an agent achieves cold.

**Brain, measured (2026-10-18, embeddinggemma-300m, CPU).** Fixture: dense hit@1 15/16, hit@5
15/16 (miss: the category-only question "which security decisions…"), keyword 14/16, hybrid
15/16, expanded set dense 16/16. Real data (124 decisions, 14 private questions, gold via the
`migrate:sqlite#<id>` source key): dense hit@1 14/14, hit@5 14/14; keyword (BM25 only) 8/14,
11/14; hybrid (RRF) 14/14, 14/14. Median wall time per `recall` call ~1.3 s (fresh process,
model load included); migrate of 124 decisions ~7 s, ~1.0 GB peak RSS (`batch_size=1`).

**Floors.** `tests/test-memory-recall.sh` fails if FTS-only hit@5 on the fixture drops under
80% (natural) or 95% (expanded). The one known lexical miss (D10: "webhook keeps failing" vs "Webhooks … failures", no
stemming) is the kind of case the vector leg is there for; do not "fix" it by rewording the
question toward the decision text.

**Adding cases.** Add the decision to `decisions.tsv` (synthetic text only), then a question
that paraphrases it. Run `--verbose` before and after; a question that only passes because it
quotes the decision tests nothing.
