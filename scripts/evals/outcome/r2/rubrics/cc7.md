## Task-specific criteria (task: review a PR with six seeded convention violations)

- `found_swallowed_catch` (critical): identifies S3: the catch hides the failure AND reports success to
  the client.
- `found_missing_validation` (critical): identifies S5: the body is not validated/parsed at the API
  boundary (schema validation such as Zod, or equivalent explicit checks).
- `found_pii_log`: identifies S4 specifically as logging personal data (the email), not only as
  "remove console.log".
- `found_any`: identifies S1 (`any`).
- `found_default_export`: identifies S2 (`export default` / default import) as a convention issue.
- `found_unrequested_option`: identifies S6 (the unused `options` / `retries` / `auditLog` parameter).
- `no_manufactured_high` (critical): zero manufactured findings rated blocking/critical/high.
- `actionable`: each finding names the line/file and a concrete fix.
