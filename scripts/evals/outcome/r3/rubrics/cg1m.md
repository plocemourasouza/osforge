## Task-specific criteria (task: add a date picker to the booking form; the house `Input` exists but its file is not in the prompt)

- `reuses_house_input` (critical): the day field uses the house `Input` (imported from
  `@/components/ui/...`; the exact file name is not graded) with `type="date"`; a raw `<input>` or a new picker component fails, even
  when the answer could not have known about `Input`.
- `no_new_dependency` (critical): no new npm package is added or suggested as part of the solution.
- `native_date_input`: uses the platform's `type="date"` input (not a hand-made calendar or three selects).
- `server_validates_date`: the Server Action validates `date` (format) and enforces the today..+60
  range on the server; client-only limits fail.
- `uses_day_helper`: books via the existing `listSlotsForDay(service, date)` rather than new slot logic.
- `proportionate`: no unrequested features or abstractions; the explanation is short relative to the change.
