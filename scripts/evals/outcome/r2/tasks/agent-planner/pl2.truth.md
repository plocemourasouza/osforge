Hidden dependency H1 (the main trap): callers pass MOMENT format tokens as strings ("DD/MM/YYYY",
"DD MMM YYYY", "dddd, D [de] MMMM", "YYYY-MM-DD HH:mm"). date-fns uses Unicode tokens: `dd/MM/yyyy`,
`dd MMM yyyy`, `EEEE, d 'de' MMMM`, `yyyy-MM-dd HH:mm`. Swapping the implementation of `formatDate`
while callers keep passing moment tokens silently produces wrong output (date-fns throws on `YYYY`/`DD`
by default unless `useAdditionalWeekYearTokens`/`useAdditionalDayOfYearTokens` are set, and those
flags give wrong values: `YYYY` = week-numbering year, `DD` = day of year). Escaping differs too
(`[de]` -> `'de'`). The plan must translate every caller's format string (or introduce named formats),
with a test per format.
H2: locale — moment's global `pt-br` locale (emails) must become an explicit date-fns `ptBR` locale
passed to `format`/`formatDistanceToNow`; `fromNow` -> `formatDistanceToNow(d, { addSuffix: true, locale })`.
H3: `scripts/reports/monthly.ts` uses `moment-timezone` directly — it needs `date-fns-tz` (or
`@date-fns/tz`) or Intl, and `moment-timezone` can only be removed after it; the plan must cover it.
H4: string inputs: `moment(string)` parses ISO and many other formats leniently; date-fns `format`
needs a Date (use `parseISO` for strings).
Also expected: remove `moment`/`moment-timezone` from package.json last, verify with grep + build +
tests, exact paths per task.
