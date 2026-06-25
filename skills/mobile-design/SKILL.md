---
name: mobile-design
description: "Mobile-first design principles for iOS and Android apps: touch interaction, thumb zone, 60fps performance, platform conventions (HIG, Material 3), offline-first, and native navigation. Use when: 'create an app in React Native or Flutter', 'native mobile screen design', 'this button is too small for touch', 'the app needs to work offline', 'tab bar, drawer, or stack for app navigation', 'OLED dark mode in the app'. Keywords: mobile, app, iOS, Android, React Native, Flutter, touch, gesture, HIG, Material Design. Do NOT use for: websites and responsive web (high-end-visual-design, minimalist-ui), Tailwind technical patterns (tailwind-patterns), generating app image mockups (imagegen-frontend-mobile)."
metadata:
  author: antigravity-kit (adapted)
  version: "1.0.0"
  source: "antigravity-kit"
---

# Mobile Design System

> **Philosophy:** Touch-first. Battery-conscious. Platform-respectful. Offline-capable.
> **Core Principle:** Mobile is NOT a small desktop. Design for the WORST conditions: bad network, one hand, bright sun, low battery. If it works there, it works everywhere.

This skill is self-contained: everything needed to design and review mobile screens is below. The files in `references/` are optional deep dives.

---

## Step 1 — Ask Before Assuming

If the user's request is open-ended, do NOT default to your favorite stack. Confirm these before writing any code:

| Aspect | Ask | Why it matters |
|--------|-----|----------------|
| **Platform** | "iOS, Android, or both?" | Affects every design decision (navigation, typography, feedback patterns) |
| **Framework** | "React Native, Flutter, or native?" | Determines component APIs and performance patterns |
| **Navigation** | "Tab bar, drawer, or stack-based?" | Core UX decision; hard to change later |
| **State** | "Zustand/Redux (RN) or Riverpod/BLoC (Flutter)?" | Architecture foundation |
| **Offline** | "Does this need to work offline?" | Changes the entire data strategy |
| **Target devices** | "Phone only, or tablet support?" | Layout complexity |

Also avoid memorized defaults: before picking a pattern "because that's how it's always done," check whether it actually fits THIS project's context, users, and constraints. (Full anti-default protocol: [references/mobile-design-thinking.md](references/mobile-design-thinking.md).)

---

## Step 2 — Touch Targets and Thumb Zone

### Minimum touch target sizes (memorize these)

| Standard | Minimum | Recommended | Notes |
|----------|---------|-------------|-------|
| iOS (HIG) | **44pt × 44pt** | 48pt+ | All tappable elements |
| Android (Material 3) | **48dp × 48dp** | 56dp+ | All tappable elements |
| WCAG 2.2 | 44px × 44px | — | Accessibility compliance |
| Primary CTAs / destructive | — | **56–64px** | Bigger = fewer mis-taps |

Spacing between adjacent targets: **≥ 8px**, or accidental taps will happen. A finger contact area is ~7mm and occludes the target — there is no hover state to save the user.

```jsx
// React Native — visual icon can be small, but the TAPPABLE area must be >= 44
<Pressable
  hitSlop={{ top: 12, bottom: 12, left: 12, right: 12 }} // expands touch area
  style={{ minWidth: 48, minHeight: 48, alignItems: 'center', justifyContent: 'center' }}
>
  <Icon name="close" size={20} />
</Pressable>
```

```dart
// Flutter — Material enforces 48x48 via materialTapTargetSize; don't shrink it
IconButton(
  iconSize: 20,
  constraints: const BoxConstraints(minWidth: 48, minHeight: 48),
  onPressed: close,
  icon: const Icon(Icons.close),
)
```

### Thumb zone (49% of users hold the phone one-handed)

| Screen region | Reachability | Put here |
|---------------|--------------|----------|
| **Bottom third** | Easy (thumb's natural arc) | Primary CTAs, tab bar, FAB (bottom-right) |
| **Middle** | OK | Content, secondary actions |
| **Top** | Hard (requires stretch/regrip) | Back, menu, settings — and **destructive actions** (hard to reach = hard to tap by accident) |

### Touch feedback — never nothing

- Visual change on tap in **< 50ms**: highlight, slight scale (0.95–0.98), or ripple (Android).
- Action taking **> 100ms** → show spinner/progress AND disable the button (prevents double tap); prefer optimistic UI.
- Haptics on important actions (button taps, toggles, success/error, swipe thresholds). Don't use haptics on every scroll or list item — haptic fatigue is real.

---

## Step 3 — Gestures

Gestures are **invisible** — many users never discover them. Rule: **gestures are shortcuts, never the only way.**

| Gesture | Meaning | Always pair with a visible alternative |
|---------|---------|----------------------------------------|
| Tap | Select / activate | — (primary) |
| Long press | Context menu, selection mode | Overflow/"..." menu |
| Swipe horizontal | Delete, list actions, navigation | Delete button or item menu |
| Swipe down | Pull to refresh, dismiss | Refresh button |
| Pinch | Zoom | Zoom controls (+/−) |
| Double tap | Zoom in, like/favorite | Visible like button |

More on gesture psychology, Fitts' Law and haptic types: [references/touch-psychology.md](references/touch-psychology.md).

---

## Step 4 — Performance and Battery

Target: **60fps** (16.6ms per frame). Test on low-end Android, not just the simulator.

### Lists (the #1 mobile performance killer)

```jsx
// React Native — never map() a long array inside ScrollView
<FlatList                       // or FlashList (Shopify) for long lists
  data={items}
  keyExtractor={(item) => item.id}
  renderItem={renderItem}        // renderItem memoized; item component wrapped in React.memo
  getItemLayout={(_, i) => ({ length: 72, offset: 72 * i, index: i })} // if fixed height
  windowSize={7}
  removeClippedSubviews
/>
```

```dart
// Flutter — lazy by default, but keep it that way
ListView.builder(               // never ListView(children: [...]) for long lists
  itemCount: items.length,
  itemExtent: 72,               // fixed height = cheaper layout
  itemBuilder: (context, i) => ItemTile(item: items[i]), // const constructors where possible
)
```

### Animation and rendering

- React Native: drive animations on the UI thread (`react-native-reanimated` or `useNativeDriver: true`); never animate layout via JS `setState` per frame.
- Flutter: use `RepaintBoundary` around expensive subtrees; avoid rebuilding whole screens (`const` widgets, granular `Consumer`/`select`).
- Images: request the size you render (resize on server/CDN); cache (`expo-image`, `cached_network_image`).

### Battery

- Dark mode with **pure black `#000`** saves real battery on OLED screens.
- Batch network calls; avoid polling — prefer push.
- Stop timers, location watchers and subscriptions when the app backgrounds; clean up on unmount/dispose.

---

## Step 5 — Platform Conventions (iOS vs Android)

Cross-platform code must still FEEL native. Key divergence points:

| Aspect | iOS (HIG) | Android (Material 3) |
|--------|-----------|----------------------|
| Touch target | 44pt min | 48dp min |
| System font | SF Pro | Roboto |
| Back navigation | Swipe-from-left-edge + back chevron top-left | System back button/gesture — must always work |
| Primary nav | Tab bar (bottom) | Bottom navigation bar ou navigation drawer |
| Prominent action | Buttons in context | FAB (floating action button) |
| Tap feedback | Highlight/opacity | Ripple effect |
| Confirmations | Action sheet (bottom) | Dialog or bottom sheet |
| Settings/share icons | iOS-style glyphs (SF Symbols) | Material icons |
| Type scaling | Dynamic Type — respect user setting | Font scale — respect user setting |

```jsx
// React Native — conditional platform logic
import { Platform } from 'react-native';
const styles = {
  shadow: Platform.select({
    ios: { shadowColor: '#000', shadowOpacity: 0.15, shadowRadius: 8, shadowOffset: { width: 0, height: 2 } },
    android: { elevation: 4 },
  }),
};
```

```dart
// Flutter — adaptive widgets pick the platform-correct look
Switch.adaptive(value: enabled, onChanged: toggle);
// Navigation transitions, dialogs: showAdaptiveDialog / platform-aware page routes
```

Never ship an Android app with iOS-style back chevrons only, or an iOS app with a FAB + ripple — users notice immediately.

---

## Step 6 — Offline and Resilience

- Decide per screen: must it work offline? If yes, define the cache strategy (stale-while-revalidate, queue-and-sync, read-only cache).
- Every screen needs **4 states**: loading (skeleton > spinner), success, **empty**, and **error with retry button**.
- Detect connectivity (`@react-native-community/netinfo`, `connectivity_plus`) and show a non-blocking offline banner — don't block the whole UI.
- Queue writes made offline and sync on reconnect; show pending state ("sending...").

---

## Checklists

### Before starting any mobile project
- [ ] Platform confirmed? (iOS / Android / Both)
- [ ] Framework chosen? (RN / Flutter / Native)
- [ ] Navigation pattern decided? (Tabs / Stack / Drawer)
- [ ] State management selected?
- [ ] Offline requirements known?
- [ ] Deep linking planned from day one?
- [ ] Target devices defined? (Phone / Tablet / Both)

### Before every screen
- [ ] Touch targets ≥ 44pt (iOS) / 48dp (Android), spacing ≥ 8px?
- [ ] Primary CTA in thumb zone (bottom third)?
- [ ] Destructive actions away from easy reach + confirmation?
- [ ] Every gesture has a visible alternative?
- [ ] Loading, empty, and error-with-retry states exist?
- [ ] Offline handling considered?
- [ ] Platform conventions followed (back nav, feedback, icons)?

### Before release
- [ ] console.log / debugPrint removed?
- [ ] SecureStore/Keychain/Keystore for sensitive data (never AsyncStorage/SharedPreferences)?
- [ ] SSL pinning enabled (if required)?
- [ ] Lists virtualized and memoized (FlatList/ListView.builder, keyExtractor, memo)?
- [ ] Memory cleanup on unmount/dispose (timers, listeners, subscriptions)?
- [ ] Tested on a low-end Android device?
- [ ] Accessibility labels on all interactive elements; respects Dynamic Type/font scale?

---

## Reference Files (Optional Deep Dives)

The skill works standalone; read these only when you need more depth:

| File | When to use |
|------|-------------|
| [references/mobile-design-thinking.md](references/mobile-design-thinking.md) | Anti-memorization protocol: component decomposition template, pattern questioning, design commitment — useful for complex/ambiguous projects |
| [references/touch-psychology.md](references/touch-psychology.md) | Fitts' Law details, full haptic type tables (iOS), gesture discoverability, cognitive load on mobile |

---

> **Remember:** Mobile users are impatient, interrupted, and using imprecise fingers on small screens. Every touch is a conversation — make it feel natural, responsive, and respectful of human fingers, not cursor points.
