Seeded issues: none. This is a clean change; the correct verdict is APPROVE.

Why it is correct (what a careful reviewer verifies):
- Authorization: `requireUser()` plus `userId: user.id` in the `where` of the update, so a client cannot
  cancel another client's booking by posting its id (covered by a test).
- Atomicity: a single conditional `updateMany` checks ownership, `status: "CONFIRMED"` and the 24 h
  window in the database; double clicks or two tabs cannot both cancel, and there is no read-then-write
  race (covered by the idempotency test).
- The 24 h rule compares `startsAt` (`timestamptz`) with an absolute instant (`Date.now() + 24 h`);
  time zones do not matter for a duration-based window.
- Input validated with Zod (`cuid`), malformed ids rejected (tested); the error message does not reveal
  whether a booking id exists (same message for "not yours", "too late" and "already cancelled"),
  which is the safer choice.
- `revalidatePath("/bookings")` refreshes the list; the button handles pending, error (`role="alert"`)
  and success states; `confirm()` before submitting is an acceptable, simple guard.
- No payment to refund (paid at the salon) and freed slots reappear (unchanged slot search), per the context.

Things a reviewer might raise that are NOT defects here (raising them as blocking/must-fix is
manufactured): "use `findUnique` + check first" (would introduce the race the `updateMany` avoids);
"race condition on cancel" (there is none); "time-zone bug in the 24 h window"; "missing auth" (it is
there); "missing refund"; "use a transaction" (one statement is already atomic); "a generic error
message is bad UX" (deliberate; a one-line suggestion to distinguish "too late" is acceptable as a
non-blocking suggestion); "replace `confirm()` with a dialog component" (taste).

Acceptable non-blocking suggestions (count as real, not manufactured, if presented as optional):
notifying the salon of the cancellation, an audit field for who cancelled, a test at exactly the 24 h
boundary, using `useFormStatus`.
