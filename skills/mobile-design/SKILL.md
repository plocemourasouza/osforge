---
name: mobile-design
description: Mobile-first design thinking and decision-making for iOS and Android apps. Touch interaction, performance patterns, platform conventions. Teaches principles, not fixed values. Use when building React Native, Flutter, or native mobile apps.
metadata:
  author: antigravity-kit (adapted)
  version: "1.0.0"
  source: "antigravity-kit"
---

# Mobile Design System

> **Philosophy:** Touch-first. Battery-conscious. Platform-respectful. Offline-capable.
> **Core Principle:** Mobile is NOT a small desktop. THINK mobile constraints, ASK platform choice.

---

## 🔧 Runtime Scripts

**Execute these for validation (don't read, just run):**

| Script | Purpose | Usage |
|--------|---------|-------|
| `scripts/mobile_audit.py` | Mobile UX & Touch Audit | `python scripts/mobile_audit.py <project_path>` |

---

## 🔴 MANDATORY: Read Reference Files Before Working!

**⛔ DO NOT start development until you read the relevant files:**

### Universal (Always Read)

| File | Content | Status |
|------|---------|--------|
| **[mobile-design-thinking.md](mobile-design-thinking.md)** | **⚠️ ANTI-MEMORIZATION: Forces thinking, prevents AI defaults** | **⬜ CRITICAL FIRST** |
| **[touch-psychology.md](touch-psychology.md)** | **Fitts' Law, gestures, haptics, thumb zone** | **⬜ CRITICAL** |
| **[mobile-performance.md](mobile-performance.md)** | **RN/Flutter performance, 60fps, memory** | **⬜ CRITICAL** |
| **[mobile-backend.md](mobile-backend.md)** | **Push notifications, offline sync, mobile API** | **⬜ CRITICAL** |
| **[mobile-testing.md](mobile-testing.md)** | **Testing pyramid, E2E, platform-specific** | **⬜ CRITICAL** |
| **[mobile-debugging.md](mobile-debugging.md)** | **Native vs JS debugging, Flipper, Logcat** | **⬜ CRITICAL** |
| [mobile-navigation.md](mobile-navigation.md) | Tab/Stack/Drawer, deep linking | ⬜ Read |
| [mobile-typography.md](mobile-typography.md) | System fonts, Dynamic Type, a11y | ⬜ Read |
| [mobile-color-system.md](mobile-color-system.md) | OLED, dark mode, battery-aware | ⬜ Read |
| [decision-trees.md](decision-trees.md) | Framework/state/storage selection | ⬜ Read |

> 🧠 **mobile-design-thinking.md is PRIORITY!** This file ensures AI thinks instead of using memorized patterns.

### Platform-Specific (Read Based on Target)

| Platform | File | Content | When to Read |
|----------|------|---------|--------------|
| **iOS** | [platform-ios.md](platform-ios.md) | Human Interface Guidelines, SF Pro, SwiftUI patterns | Building for iPhone/iPad |
| **Android** | [platform-android.md](platform-android.md) | Material Design 3, Roboto, Compose patterns | Building for Android |
| **Cross-Platform** | Both above | Platform divergence points | React Native / Flutter |

> 🔴 **If building for iOS → Read platform-ios.md FIRST!**
> 🔴 **If building for Android → Read platform-android.md FIRST!**
> 🔴 **If cross-platform → Read BOTH and apply conditional platform logic!**

---

## ⚠️ CRITICAL: ASK BEFORE ASSUMING (MANDATORY)

> **STOP! If the user's request is open-ended, DO NOT default to your favorites.**

### You MUST Ask If Not Specified:

| Aspect | Ask | Why |
|--------|-----|-----|
| **Platform** | "iOS, Android, or both?" | Affects EVERY design decision |
| **Framework** | "React Native, Flutter, or native?" | Determines patterns and tools |
| **Navigation** | "Tab bar, drawer, or stack-based?" | Core UX decision |
| **State** | "What state management? (Zustand/Redux/Riverpod/BLoC?)" | Architecture foundation |
| **Offline** | "Does this need to work offline?" | Affects data strategy |
| **Target devices** | "Phone only, or tablet support?" | Layout complexity |

---

## 📋 Pre-Development Checklist

### Before Starting ANY Mobile Project

- [ ] **Platform confirmed?** (iOS / Android / Both)
- [ ] **Framework chosen?** (RN / Flutter / Native)
- [ ] **Navigation pattern decided?** (Tabs / Stack / Drawer)
- [ ] **State management selected?** (Zustand / Redux / Riverpod / BLoC)
- [ ] **Offline requirements known?**
- [ ] **Deep linking planned from day one?**
- [ ] **Target devices defined?** (Phone / Tablet / Both)

### Before Every Screen

- [ ] **Touch targets ≥ 44-48px?**
- [ ] **Primary CTA in thumb zone?**
- [ ] **Loading state exists?**
- [ ] **Error state with retry exists?**
- [ ] **Offline handling considered?**
- [ ] **Platform conventions followed?**

### Before Release

- [ ] **console.log removed?**
- [ ] **SecureStore for sensitive data?**
- [ ] **SSL pinning enabled?**
- [ ] **Lists optimized (memo, keyExtractor)?**
- [ ] **Memory cleanup on unmount?**
- [ ] **Tested on low-end devices?**
- [ ] **Accessibility labels on all interactive elements?**

---

## 📚 Reference Files

For deeper guidance on specific areas:

| File | When to Use |
|------|-------------|
| [mobile-design-thinking.md](mobile-design-thinking.md) | **FIRST! Anti-memorization, forces context-based thinking** |
| [touch-psychology.md](touch-psychology.md) | Understanding touch interaction, Fitts' Law, gesture design |
| [mobile-performance.md](mobile-performance.md) | Optimizing RN/Flutter, 60fps, memory/battery |
| [platform-ios.md](platform-ios.md) | iOS-specific design, HIG compliance |
| [platform-android.md](platform-android.md) | Android-specific design, Material Design 3 |
| [mobile-navigation.md](mobile-navigation.md) | Navigation patterns, deep linking |
| [mobile-typography.md](mobile-typography.md) | Type scale, system fonts, accessibility |
| [mobile-color-system.md](mobile-color-system.md) | OLED optimization, dark mode, battery |
| [decision-trees.md](decision-trees.md) | Framework, state, storage decisions |

---

> **Remember:** Mobile users are impatient, interrupted, and using imprecise fingers on small screens. Design for the WORST conditions: bad network, one hand, bright sun, low battery. If it works there, it works everywhere.
