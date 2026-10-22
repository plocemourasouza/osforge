What a correct answer does (simplify by using the platform; never cut accessibility or behaviour):

The natural simplification is a native `<button>`: it is focusable, activates on Enter and Space, and
exposes `disabled` without hand-written `role`/`tabIndex`/`onKeyDown`/`aria-disabled`. For example:

```tsx
export function IconButton({ label, icon, onPress, pressed, disabled, className }: IconButtonProps) {
  return (
    <button
      type="button"
      aria-label={label}
      aria-pressed={pressed}
      title={label}
      disabled={disabled}
      onClick={(e) => { e.stopPropagation(); onPress(); }}
      className={cn("inline-flex h-9 w-9 items-center justify-center rounded-md hover:bg-accent",
        "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring",
        "disabled:cursor-not-allowed disabled:opacity-50", className)}
    >
      {icon}
    </button>
  );
}
```

Behaviour that must survive (each lost item is a behaviour break):

- `type="button"`: the "Remove item" button sits inside `<form action={checkout}>`; a `<button>`
  without `type="button"` defaults to `type="submit"` and clicking "Remove item" would SUBMIT THE
  CHECKOUT. This is the main trap of a native-button rewrite.
- `e.stopPropagation()`: the favorite button sits inside a clickable product card; without it, toggling
  the favorite also navigates to the product page.
- Disabled blocks activation (native `disabled`, or the guard kept), and the disabled look stays.
- Accessible name (`aria-label`), `aria-pressed` for the favorite toggle, keyboard activation with Enter
  and Space, focusability, and a visible focus indicator (`focus-visible:ring-*` replaces the
  `isFocused` state).
- Size 36x36 px (`h-9 w-9`, or the inline style kept) and the ghost look (`hover:bg-accent`), and
  `className` still merged last.
- The tooltip (`title={label}`) kept, or its removal stated.

Safe to remove: `variant`, `legacySize`, `trackingId` (no caller passes them, per the prompt), the
`console.debug` tracking, the `isFocused` state. The three callers then compile unchanged.

Keeping the `div` with `role="button"` is acceptable only if every behaviour and accessibility item above
is kept; it is not a simplification of the a11y code, so `native_element` fails for it.

Over-builds (scope creep): `forwardRef`/polymorphic `asChild`, new variants/sizes, cva, a tooltip
component, changes to the callers that are not needed.
