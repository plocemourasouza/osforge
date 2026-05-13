# Mobile Design

**Trigger:** mobile app, touch targets, iOS/Android, responsive mobile

---

## Touch Targets

### Minimum Sizes
- **iOS**: 44×44 points
- **Android**: 48×48 dp
- **Web**: 44×44 CSS pixels

```tsx
// Ensure adequate touch targets
<button className="min-h-[44px] min-w-[44px] p-3">
  <Icon size={24} />
</button>

// Spacing between targets
<div className="flex gap-2">
  <button className="p-3">Action 1</button>
  <button className="p-3">Action 2</button>
</div>
```

---

## Mobile-First Responsive

```tsx
// Start with mobile, expand up
<div className="
  p-4              /* Mobile base */
  sm:p-6           /* Tablet */
  lg:p-8           /* Desktop */
">
  <h1 className="
    text-xl         /* Mobile */
    sm:text-2xl     /* Tablet */
    lg:text-4xl     /* Desktop */
  ">
    Title
  </h1>
</div>
```

### Breakpoints
```
Mobile:  < 640px  (default)
sm:      ≥ 640px  (large phones, small tablets)
md:      ≥ 768px  (tablets)
lg:      ≥ 1024px (small laptops)
xl:      ≥ 1280px (desktops)
2xl:     ≥ 1536px (large screens)
```

---

## Navigation Patterns

### Bottom Navigation (Mobile)
```tsx
<nav className="fixed bottom-0 left-0 right-0 bg-white border-t md:hidden">
  <div className="flex justify-around py-2">
    <NavItem icon={<HomeIcon />} label="Home" href="/" />
    <NavItem icon={<SearchIcon />} label="Search" href="/search" />
    <NavItem icon={<ProfileIcon />} label="Profile" href="/profile" />
  </div>
</nav>
```

### Hamburger Menu
```tsx
// Show on mobile, hide on desktop
<button className="md:hidden" onClick={toggleMenu}>
  <MenuIcon />
</button>

// Desktop nav, hidden on mobile
<nav className="hidden md:flex gap-6">
  <NavLink href="/">Home</NavLink>
  <NavLink href="/about">About</NavLink>
</nav>
```

---

## Gestures & Interactions

### Swipe Actions
```tsx
// Use libraries like react-swipeable
import { useSwipeable } from 'react-swipeable'

function SwipeableCard({ onDelete }) {
  const handlers = useSwipeable({
    onSwipedLeft: onDelete,
    trackMouse: true,
  })

  return <div {...handlers}>Card content</div>
}
```

### Pull to Refresh
```tsx
// Built into many mobile frameworks
// For web, use libraries or native browser behavior
```

### Long Press
```tsx
function useLongPress(callback: () => void, ms = 500) {
  const timeout = useRef<NodeJS.Timeout>()

  const start = useCallback(() => {
    timeout.current = setTimeout(callback, ms)
  }, [callback, ms])

  const stop = useCallback(() => {
    clearTimeout(timeout.current)
  }, [])

  return {
    onMouseDown: start,
    onMouseUp: stop,
    onMouseLeave: stop,
    onTouchStart: start,
    onTouchEnd: stop,
  }
}
```

---

## Performance

### Optimize for Slow Connections
```tsx
// Lazy load images
<Image loading="lazy" src="/photo.jpg" alt="" />

// Skeleton loading
{isLoading ? (
  <Skeleton className="h-48 w-full" />
) : (
  <Content />
)}

// Prefetch critical resources
<link rel="prefetch" href="/next-page" />
```

### Reduce JavaScript
```tsx
// Code split routes
const HeavyComponent = dynamic(() => import('./HeavyComponent'), {
  loading: () => <Skeleton />,
})

// Defer non-critical scripts
<script src="/analytics.js" defer />
```

---

## Offline Support

### Service Worker
```typescript
// next.config.js with next-pwa
const withPWA = require('next-pwa')({
  dest: 'public',
  disable: process.env.NODE_ENV === 'development',
})

module.exports = withPWA({
  // Next.js config
})
```

### Offline Detection
```tsx
function useOnlineStatus() {
  const [isOnline, setIsOnline] = useState(navigator.onLine)

  useEffect(() => {
    const handleOnline = () => setIsOnline(true)
    const handleOffline = () => setIsOnline(false)

    window.addEventListener('online', handleOnline)
    window.addEventListener('offline', handleOffline)

    return () => {
      window.removeEventListener('online', handleOnline)
      window.removeEventListener('offline', handleOffline)
    }
  }, [])

  return isOnline
}

// Usage
const isOnline = useOnlineStatus()
if (!isOnline) {
  return <OfflineBanner />
}
```

---

## Platform Conventions

### iOS
- Safe areas for notch/home indicator
- Native-feeling animations (spring physics)
- Pull-to-refresh
- Swipe back navigation

### Android
- Material Design patterns
- Back button handling
- Status bar theming
- Bottom sheets

```tsx
// Safe area handling
<div className="pb-safe">
  {/* Content avoids home indicator */}
</div>

// Or with CSS
.safe-bottom {
  padding-bottom: env(safe-area-inset-bottom);
}
```

---

## Testing

### Device Emulation
```
Chrome DevTools → Device Toolbar → Select device
```

### Real Device Testing
- iOS: Safari on iPhone
- Android: Chrome on Android device
- Cross-browser: BrowserStack, Sauce Labs

### Checklist
- [ ] Touch targets ≥ 44px
- [ ] Text readable without zoom (16px+ base)
- [ ] Forms work with mobile keyboards
- [ ] Buttons/links have adequate spacing
- [ ] Works in portrait and landscape
- [ ] Fast on 3G connection
- [ ] Handles offline gracefully
