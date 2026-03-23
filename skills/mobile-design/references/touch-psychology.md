---
name: touch-psychology
description: Mobile touch interaction psychology, Fitts' Law, thumb zone, gesture design, haptics
---

# Touch Psychology Reference

> Deep dive into mobile touch interaction, Fitts' Law for touch, thumb zone anatomy, gesture psychology, and haptic feedback.

---

## 1. Fitts' Law for Touch

### The Fundamental Difference

```
DESKTOP (Mouse/Trackpad):
├── Cursor size: 1 pixel (precision)
├── Visual feedback: Hover states
├── Error cost: Low (easy to retry)
└── Target acquisition: Fast, precise

MOBILE (Finger):
├── Contact area: ~7mm diameter (imprecise)
├── Visual feedback: No hover, only tap
├── Error cost: High (frustrating retries)
├── Occlusion: Finger covers the target
└── Target acquisition: Slower, needs larger targets
```

### Minimum Touch Target Sizes

| Platform | Minimum | Recommended | Use For |
|----------|---------|-------------|---------|
| **iOS (HIG)** | 44pt × 44pt | 48pt+ | All tappable elements |
| **Android (Material)** | 48dp × 48dp | 56dp+ | All tappable elements |
| **WCAG 2.2** | 44px × 44px | - | Accessibility compliance |
| **Critical Actions** | - | 56-64px | Primary CTAs, destructive actions |

---

## 2. Thumb Zone Anatomy

### One-Handed Phone Usage

```
Research shows: 49% of users hold phone one-handed.

┌─────────────────────────────────────┐
│                                     │
│  ┌─────────────────────────────┐    │
│  │       HARD TO REACH         │    │ ← Status bar, top nav
│  │      (requires stretch)     │    │    Put: Back, menu, settings
│  │                             │    │
│  ├─────────────────────────────┤    │
│  │                             │    │
│  │       OK TO REACH           │    │ ← Content area
│  │      (comfortable)          │    │    Put: Secondary actions, content
│  │                             │    │
│  ├─────────────────────────────┤    │
│  │                             │    │
│  │       EASY TO REACH         │    │ ← Tab bar, FAB zone
│  │      (thumb's arc)          │    │    Put: PRIMARY CTAs!
│  │                             │    │
│  └─────────────────────────────┘    │
│                                     │
│          [    HOME    ]             │
└─────────────────────────────────────┘
```

### Placement Guidelines

| Element Type | Ideal Position | Reason |
|--------------|----------------|--------|
| **Primary CTA** | Bottom center/right | Easy thumb reach |
| **Tab bar** | Bottom | Natural thumb position |
| **FAB** | Bottom right | Easy for right hand |
| **Navigation** | Top (stretch) | Less frequent use |
| **Destructive actions** | Top left | Hard to reach = harder to accidentally tap |

---

## 3. Touch Feedback Requirements

```
Tap → Immediate visual change (< 50ms)
├── Highlight state (background color change)
├── Scale down slightly (0.95-0.98)
├── Ripple effect (Android Material)
├── Haptic feedback for confirmation
└── Never nothing!

Loading → Show within 100ms
├── If action takes > 100ms
├── Show spinner/progress
├── Disable button (prevent double tap)
└── Optimistic UI when possible
```

---

## 4. Gesture Psychology

### Gesture Discoverability Problem

```
Problem: Gestures are INVISIBLE.
├── User must discover/remember them
├── No hover/visual hint
├── Different mental model than tap
└── Many users never discover gestures

Solution: Always provide visible alternative
├── Swipe to delete → Also show delete button or menu
├── Pull to refresh → Also show refresh button
├── Pinch to zoom → Also show zoom controls
└── Gestures as shortcuts, not only way
```

### Common Gesture Conventions

| Gesture | Universal Meaning | Usage |
|---------|-------------------|-------|
| **Tap** | Select, activate | Primary action |
| **Double tap** | Zoom in, like/favorite | Quick action |
| **Long press** | Context menu, selection mode | Secondary options |
| **Swipe horizontal** | Navigation, delete, actions | List actions |
| **Swipe down** | Refresh, dismiss | Pull to refresh |
| **Pinch** | Zoom in/out | Maps, images |

---

## 5. Haptic Feedback Patterns

### Why Haptics Matter

```
Haptics provide:
├── Confirmation without looking
├── Richer, more premium feel
├── Accessibility (blind users)
├── Reduced error rate
└── Emotional satisfaction
```

### iOS Haptic Types

| Type | Intensity | Use Case |
|------|-----------|----------|
| `selection` | Light | Picker scroll, toggle, selection |
| `light` | Light | Minor actions, hover equivalent |
| `medium` | Medium | Standard tap confirmation |
| `heavy` | Strong | Important completed, drop |
| `success` | Pattern | Task completed successfully |
| `warning` | Pattern | Warning, attention needed |
| `error` | Pattern | Error occurred |

### Haptic Usage Guidelines

```
✅ DO use haptics for:
├── Button taps
├── Toggle switches
├── Picker/slider values
├── Pull to refresh trigger
├── Successful action completion
├── Errors and warnings
├── Swipe action thresholds
└── Important state changes

❌ DON'T use haptics for:
├── Every scroll position
├── Every list item
├── Background events
├── Passive displays
└── Too frequently (haptic fatigue)
```

---

## 6. Mobile Cognitive Load

### How Mobile Differs from Desktop

| Factor | Desktop | Mobile | Implication |
|--------|---------|--------|-------------|
| **Attention** | Focused sessions | Interrupted constantly | Design for micro-sessions |
| **Context** | Controlled environment | Anywhere, any condition | Handle bad lighting, noise |
| **Multitasking** | Multiple windows | One app visible | Complete task in-app |
| **Input speed** | Fast (keyboard) | Slow (touch typing) | Minimize input, smart defaults |
| **Error recovery** | Easy (undo, back) | Harder (no keyboard shortcuts) | Prevent errors, easy recovery |

---

## 7. Touch Psychology Checklist

### Before Every Screen

- [ ] **All touch targets ≥ 44-48px?**
- [ ] **Primary CTA in thumb zone?**
- [ ] **Destructive actions require confirmation?**
- [ ] **Gesture alternatives exist (visible buttons)?**
- [ ] **Haptic feedback on important actions?**
- [ ] **Immediate visual feedback on tap?**
- [ ] **Loading states for actions > 100ms?**

---

> **Remember:** Every touch is a conversation between user and device. Make it feel natural, responsive, and respectful of human fingers—not precise cursor points.
