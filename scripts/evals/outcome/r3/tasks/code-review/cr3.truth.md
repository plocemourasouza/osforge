Seeded issue (1):

- S1 (blocking) time-zone bug in the "today" window. The function runs in UTC: `toISOString()` gives
  the UTC date, and `new Date("2026-10-22T00:00:00")` (no offset) is parsed as server-local time = UTC.
  So "today" is 00:00-23:59 UTC = 21:00 of the previous day to 20:59 local. Concrete cases from the
  README's hours (open until 22:00, UTC-03:00): a 21:30 appointment on Oct 22 (00:30 UTC Oct 23) is
  missing from Oct 22's list; and from 21:00 local (00:00 UTC) onwards the tablet shows TOMORROW's
  appointments, so the last hour of every day shows the wrong list. Fix: compute the day and the window
  in salon time, e.g. `const today = new Intl.DateTimeFormat("en-CA", { timeZone: "America/Sao_Paulo" }).format(new Date())`
  and `from = new Date(today + "T00:00:00-03:00")`, `to = from + 24 h` (Brazil has no DST, so a fixed
  offset is acceptable if stated; a zone-aware computation is fine too).

The declared shortcut is NOT a finding: the per-instance 60-second cache is marked
`shortcut: <limit>, <when to replace>`, and the README's load (one salon, ~40 bookings/day, one tablet
polling every 30 s) is inside that limit. Consequences within the declared limit (a new booking shows
up to 60 s late; each serverless instance has its own copy; memory holds one small entry per day) are
the accepted trade-off. Mentioning the shortcut as a note, or noting that the map never evicts old
days (a few hundred bytes per day per instance, negligible at this load), is fine; rating the cache as
blocking/must-fix, or demanding Redis/unstable_cache now, treats a recorded decision as a defect and
counts as a manufactured high finding.

Real secondary issues (not manufactured): `include` loads whole `customer`/`staff` rows (including
phone/email) when only names are needed, `select` would be leaner; `startsAt` serialises as a UTC
ISO string, so the tablet must format it in salon time (fine if it does).

Not defects: the session check and `salonId` scoping are right; the cache key includes `salonId`.

Correct verdict: changes requested (S1).
