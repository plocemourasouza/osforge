This is task cg1 with the house component's file left OUT of the prompt. The repository (not
shown to the assistant) has `components/ui/input.tsx` exporting `Input` (a `forwardRef` wrapper
over `<input>` with the house Tailwind classes, accepting every native input prop including
`type="date"`) and `components/ui/label.tsx` exporting `Label`; the other forms of the app use them.
Nothing in the prompt itself names them: the assistant can only know they exist if its context
lists them (arm C's repository map has the line `components/ui/: Badge, ..., IconButton, Input, Label`).

What a correct answer does:

- Renders the day field with the house `Input` (`import { Input } from "@/components/ui/input"`)
  and `type="date"`, `min`/`max` set to today and today + 60 days. An answer whose context did not
  reveal `Input` and that writes a raw `<input type="date">` matching the select's classes is a
  reasonable answer, but it does NOT reuse the house component and fails that criterion; the
  criterion grades the outcome, not the excuse.
- Adds no dependency (no `react-day-picker`, shadcn `Calendar`, `date-fns`, `dayjs`, `moment`,
  `luxon`, `date-fns-tz`).
- Validates `date` in the Server Action with the existing Zod schema (format) and enforces the
  today..+60 range on the server.
- Books via the existing `listSlotsForDay(service, date)` (its signature is in the prompt).
- Keeps the rest of the form and action as they are.

Over-builds (scope creep): a custom calendar/popover, a time picker, closed-day logic, a timezone
library, i18n, new options, rewriting the select into new components.

The map names folders, not files: an import from a guessed module inside the right folder
(e.g. `@/lib/utils` instead of `@/lib/format`) still counts as reuse; the exact path is not graded.
