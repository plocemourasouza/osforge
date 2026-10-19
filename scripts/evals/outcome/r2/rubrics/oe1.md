## Task-specific criteria (task: ten complete CRUD handlers)

- `all_ten_complete` (critical): all 10 handlers are present and fully written; no placeholder or
  "similar for books".
- `requirements_met`: 404/400/201/204 rules, update rejects empty body, book `authorId` existence check
  on create and update, author delete 409 with books — all present (at most one minor slip).
- `zod_used`: Zod schemas validate create and update bodies.
- `compiles`: imports/exports coherent and plausibly type-checks (routers exported, types imported).
- `no_placeholders`: zero placeholder markers.
