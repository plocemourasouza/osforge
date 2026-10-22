This component in our Next.js 15 / React 19 / TypeScript / Tailwind app has grown messy. Simplify it.
A search of the repository shows that no caller passes `variant`, `legacySize` or `trackingId`.
Show me the new version.

`components/ui/icon-button.tsx`:

```tsx
"use client";
import * as React from "react";
import { cn } from "@/lib/utils";

type IconButtonProps = {
  label: string; // accessible name, also shown as the tooltip
  icon: React.ReactNode;
  onPress: () => void;
  pressed?: boolean; // toggles, e.g. favorite
  disabled?: boolean;
  variant?: "ghost" | "solid";
  legacySize?: number;
  trackingId?: string;
  className?: string;
};

export function IconButton({
  label,
  icon,
  onPress,
  pressed,
  disabled,
  variant = "ghost",
  legacySize,
  trackingId,
  className,
}: IconButtonProps) {
  const [isFocused, setIsFocused] = React.useState(false);
  const size = legacySize ?? 36;

  const activate = (e: React.SyntheticEvent) => {
    e.stopPropagation(); // these sit inside clickable product cards
    if (disabled) return;
    if (trackingId) console.debug("track", trackingId);
    onPress();
  };

  return (
    <div
      role="button"
      tabIndex={disabled ? -1 : 0}
      aria-label={label}
      aria-pressed={pressed}
      aria-disabled={disabled || undefined}
      title={label}
      onClick={activate}
      onKeyDown={(e) => {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          activate(e);
        }
      }}
      onFocus={() => setIsFocused(true)}
      onBlur={() => setIsFocused(false)}
      style={{ width: size, height: size }}
      className={cn(
        "inline-flex items-center justify-center rounded-md",
        variant === "solid" ? "bg-primary text-primary-foreground" : "hover:bg-accent",
        isFocused && "ring-2 ring-ring",
        disabled && "cursor-not-allowed opacity-50",
        className,
      )}
    >
      {icon}
    </div>
  );
}
```

Its three callers:

```tsx
// components/shop/product-card.tsx -- the whole card is clickable (onClick={() => router.push(...)})
<IconButton label={isFav ? "Remove from favorites" : "Add to favorites"} icon={<Heart />} pressed={isFav} onPress={toggleFav} />

// app/(shop)/cart/cart-form.tsx -- inside <form action={checkout}>
<IconButton label="Remove item" icon={<Trash2 />} onPress={() => removeLine(line.id)} disabled={pending} />

// components/booking/staff-picker.tsx
<IconButton label="Next week" icon={<ChevronRight />} onPress={nextWeek} className="ml-auto" />
```
