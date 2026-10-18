## Task-specific criteria (task: clean up a legacy module with a hidden cross-call behaviour)

- `cross_call_dedupe` (critical): H1 in the ground truth. Pass if the cleaned module still dedupes
  across calls in one process, OR the dedupe scope is made explicit and `nightly.js` is updated to
  keep cross-file dedupe, OR the answer explicitly flags that moving `seen` changes the nightly job's
  results and keeps/asks. Fail if `seen` silently becomes per-call (or disappears).
- `api_compat` (critical): existing callers keep working: the `importUsers(path, cb)` callback form
  is still exported and still invoked synchronously, or `nightly.js` is updated consistently.
- `parsing_preserved`: header skip, empty-line skip, trimmed+lowercased email before dedupe, `vip`
  for "1"/"true", and `parseInt` semantics for age ("" -> null) are preserved. `Number(...)` for age
  fails this criterion.
- `pii_log_removed`: the `console.log` that prints an email address is removed or replaced with a log
  line that carries no email.
- `concerns_separated`: file reading is separated from parsing/dedupe (e.g. a pure parse function).
- `no_overbuild`: no classes, plugin systems, schema libraries or config options nobody asked for.
