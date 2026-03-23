---
name: react-native-app
description: React Native mobile app template principles. Expo, TypeScript, navigation.
---

# React Native App Template (2026 Edition)

Modern mobile app template, optimized for New Architecture and React 19.

## Tech Stack

| Component | Technology | Version / Notes |
|-----------|------------|-----------------|
| Core | React Native + Expo | SDK 52+ (New Architecture Enabled) |
| Language | TypeScript | v5+ (Strict Mode) |
| UI Logic | React | v19 (React Compiler, auto-memoization) |
| Navigation | Expo Router | v4+ (File-based, Universal Links) |
| Styling | NativeWind | v4.0 (Tailwind v4, CSS-first config) |
| State | Zustand + React Query | v5+ (Async State Management) |
| Storage | Expo SecureStore | Encrypted local storage |

---

## Directory Structure

```
project-name/
├── app/                 # Expo Router (File-based routing)
│   ├── _layout.tsx      # Root Layout (Stack/Tabs config)
│   ├── index.tsx        # Main Screen
│   ├── (tabs)/          # Route Group for Tab Bar
│   │   ├── _layout.tsx
│   │   ├── home.tsx
│   │   └── profile.tsx
│   ├── +not-found.tsx   # 404 Page
│   └── [id].tsx         # Dynamic Route (Typed)
├── components/
│   ├── ui/              # Primitive Components (Button, Text)
│   └── features/        # Complex Components
├── hooks/               # Custom Hooks
├── lib/
│   ├── api.ts           # Axios/Fetch client
│   └── storage.ts       # SecureStore wrapper
├── store/               # Zustand stores
├── constants/           # Colors, Theme config
├── assets/              # Fonts, Images
├── global.css           # Entry point for NativeWind v4
├── tailwind.config.ts   # Tailwind Config (if custom theme)
├── babel.config.js      # NativeWind Babel Plugin
└── app.json             # Expo Config
```

---

## Best Practices (2026 Standard)

- **New Architecture**: Ensure `newArchEnabled: true` in `app.json`
- **Typed Routes**: Use Expo Router's "Typed Routes" feature
- **React 19**: Reduce usage of `useMemo`/`useCallback` thanks to React Compiler
- **Components**: Build UI primitives with NativeWind className
- **Assets**: Use `expo-image` instead of default `<Image />`
- **API**: Always wrap with TanStack Query, avoid direct calls in `useEffect`
