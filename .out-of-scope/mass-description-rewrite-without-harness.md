# Rewriting all skill descriptions in one pass

**Rejected: 2026-07-30** (SKILL-STANDARD §5.A)

Tempting every time an audit finds description debt (101 skills without "Do NOT use for" as of
this writing). Rejected because descriptions are the ACTIVATION surface: an unvalidated mass edit
can silently break triggering across the whole catalog, and the failure only shows up when a skill
stops firing in real use. Batches validated by `test-skill-triggering.sh` are the only sanctioned
route, which requires the harness run (consumes API) before and after each batch.

**Would reopen if:** never — this is a process guarantee, not a feature decision.
