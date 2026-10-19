## Task-specific criteria (task: plan a small feature)

- `reuses_filters` (critical): the plan reuses the list's filter parsing and `where` construction (or
  extracts a shared builder) so the export matches what is shown; it does not re-implement filters.
- `tenant_scoped` (critical): the export route authenticates and scopes by the session's `tenantId`.
- `volume_handled`: addresses the ~180k-row case (streaming / batching / cap) rather than loading all
  rows in memory.
- `ambiguity_handled`: asks, or states the assumption, whether "currently shown" means the current page
  or all matching rows.
- `csv_correctness`: covers escaping and at least one of CSV-formula injection or Excel encoding/BOM.
- `granular_paths`: tasks name exact file paths and a done/verify criterion; tests are planned.
- `proportionate`: about 5–12 tasks, no unjustified new infrastructure, no code bodies.
