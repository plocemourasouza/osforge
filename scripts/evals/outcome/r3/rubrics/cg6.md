## Task-specific criteria (task: simplify a clickable-div icon button; unused props, a11y and caller-specific behaviour)

- `keeps_accessibility` (critical): the result keeps the accessible name, `aria-pressed` for toggles,
  focusability, Enter and Space activation, an exposed disabled state, and a visible focus indicator.
- `no_behavior_lost` (critical): `stopPropagation` kept; inside the cart form the button does not
  submit (`type="button"` if it became a `<button>`); disabled blocks `onPress`; 36 px size and
  `className` merge kept. Any one lost fails.
- `removes_unused_props`: `variant`, `legacySize`, `trackingId` (and the tracking and `isFocused` state) are gone.
- `native_element`: the component uses a native `<button>` instead of `div` + `role` + key handling.
- `callers_ok`: the three callers work without changes (or the answer updates them consistently).
- `proportionate`: no unrequested features or abstractions; the explanation is short relative to the change.
