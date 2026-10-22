## Task-specific criteria (task: add a date picker to the booking form; house `Input` and `listSlotsForDay` exist)

- `reuses_house_input` (critical): the day field is the house `Input` (`@/components/ui/input`) with
  `type="date"`; a raw `<input>` re-styled by hand, or a new picker/calendar component, fails.
- `no_new_dependency` (critical): no new npm package is added or suggested as part of the solution
  (no date library, no day-picker, no shadcn Calendar).
- `native_date_input`: uses the platform's `type="date"` input (not a hand-made calendar or three selects).
- `range_on_client`: sets `min` and `max` on the field (today and today + 60 days).
- `server_validates_date`: the Server Action validates `date` (format with Zod or equivalent) and
  enforces the today..+60 range on the server; client-only limits fail.
- `uses_day_helper`: books via the existing `listSlotsForDay(service, date)` rather than new slot logic.
- `proportionate`: no unrequested features or abstractions (see the ground truth's over-builds);
  the explanation is short relative to the change.
