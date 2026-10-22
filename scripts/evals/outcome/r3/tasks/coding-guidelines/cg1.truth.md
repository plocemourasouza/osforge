What a correct answer does (the solution ladder: house component first, then the platform):

- Renders the day field with the house `Input` from `@/components/ui/input` and `type="date"`
  (e.g. `<Input id="date" name="date" type="date" min={today} max={inSixtyDays} required />`), with a
  label (the house `Label` from `@/components/ui/label`, or a plain `<label>` like the existing
  service field, are both fine). The prompt shows `Input` and how the other forms use it; a raw
  `<input type="date" className="...">` that re-types the house styles, or a new
  `DatePicker`/calendar component, does not reuse the house component.
- Adds no dependency. Not needed: `react-day-picker`, the shadcn `Calendar` (it installs
  `react-day-picker`), `date-fns`, `dayjs`, `moment`, `luxon`, `date-fns-tz`. The native date input,
  `Intl` and plain string handling cover the whole task.
- Sets `min`/`max` on the input (today and today + 60 days, as `YYYY-MM-DD`).
- In the Server Action, validates `date` at the trust boundary with the Zod schema that already
  exists (e.g. `date: z.string().regex(/^\d{4}-\d{2}-\d{2}$/)`, `z.string().date()` or equivalent)
  AND enforces the range on the server (not before today, not after today + 60, computed in salon
  time or with a stated tolerance). Client-side `min`/`max` alone is not validation.
- Uses the existing `listSlotsForDay(service, date)` and books its first slot (or returns an error
  such as "No free slot on that day"), instead of re-implementing slot logic or filtering
  `nextFreeSlot`.
- Keeps the rest of the form and action as they are (service select, error/booked messages,
  `requireUser`), changing the submit label is fine.

Acceptable variations: computing "today" on the client with the local date
(`new Date().toLocaleDateString("en-CA")` or equivalent) is fine for `min`; a short note that
`toISOString().slice(0, 10)` would give the UTC date is a plus, not required. Passing the day
through a hidden field or controlled state is fine as long as the field is named `date`.

Over-builds (count as scope creep): a custom calendar/popover component, a time-of-day picker,
holiday/closed-day logic, a timezone library, i18n setup, new config options, refactoring the
select into the house components (not asked).
