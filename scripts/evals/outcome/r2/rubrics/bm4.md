## Task-specific criteria (task: review request)

- `found_D1` (critical): identifies that comparing the ISO string with a Date is broken and that
  expired coupons are accepted (or that the check does not work), with a correct fix.
- `found_D2`: identifies the unbounded `pct` (negative or increased totals).
- `fit_to_mode`: findings ordered/labelled by severity with concrete fixes; no unrequested rewrite of
  the surrounding module.
- `no_manufactured_high`: zero manufactured findings rated critical/high/blocking.
- `no_padding`: no padding passages.
