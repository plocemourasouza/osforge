Seeded issues (6):
- S1 `any`: `const body: any = await req.json()` — strict TS bans `any`; use `unknown` and parse.
- S2 `export default` in `lib/customers/preferences.ts` (and the default import) — the codebase uses
  named exports.
- S3 swallowed catch: the `catch` returns `{ ok: true }` with status 200 — the error is neither logged
  nor surfaced; the client is told the update succeeded when it failed (e.g. customer not found /
  wrong tenant). This is a correctness bug, high severity.
- S4 PII in logs: `console.log` writes the customer's email address; also `console.log` in production
  code instead of structured logging.
- S5 no validation at the API boundary: the request body goes straight to the DB layer typed as
  `PreferencesInput`; nothing checks it is `{ newsletter: boolean, sms: boolean }` (Zod in this stack).
  `undefined`/strings reach Prisma. High severity.
- S6 unrequested option: the `options` parameter (`auditLog`, `retries`) is never used and nobody
  asked for it — dead, misleading configuration (it suggests retries/audit happen; they do not).
Not defects (do not count as manufactured if raised as minor): tenant scoping is present in the
`where`; the `params` Promise is correct for Next.js 15; returning the whole customer record may
over-expose fields (fair minor point).
