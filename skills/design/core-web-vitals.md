# Core Web Vitals

**Trigger:** LCP, INP, CLS, Lighthouse, performance, page speed

---

## The Three Metrics

### LCP (Largest Contentful Paint)
**Target:** ≤ 2.5s
**What:** Time until largest content element is visible

**Optimize:**
- Use `next/image` with `priority` for hero images
- Preload critical resources
- Minimize render-blocking CSS/JS
- Use CDN for static assets
- Optimize server response time

```tsx
// Priority for above-fold images
<Image src="/hero.jpg" priority alt="Hero" />

// Preload critical fonts
<link rel="preload" href="/fonts/main.woff2" as="font" crossOrigin="anonymous" />

// Preconnect to external origins
<link rel="preconnect" href="https://fonts.googleapis.com" />
```

### INP (Interaction to Next Paint)
**Target:** ≤ 200ms
**What:** Responsiveness to user interactions

**Optimize:**
- Break long tasks into smaller chunks
- Use `requestIdleCallback` for non-urgent work
- Debounce/throttle event handlers
- Avoid synchronous layout (layout thrashing)
- Use Web Workers for heavy computation

```tsx
// Debounce search input
const debouncedSearch = useMemo(
  () => debounce((term: string) => search(term), 300),
  []
)

// Defer non-critical work
requestIdleCallback(() => {
  analytics.track('page_view')
})
```

### CLS (Cumulative Layout Shift)
**Target:** ≤ 0.1
**What:** Visual stability (unexpected layout shifts)

**Optimize:**
- Set explicit dimensions on images/videos
- Reserve space for dynamic content (ads, embeds)
- Avoid injecting content above existing content
- Use `transform` animations instead of layout properties

```tsx
// Always set dimensions
<Image src="/photo.jpg" width={800} height={600} alt="Photo" />

// Reserve space for async content
<div className="aspect-video bg-gray-100">
  <VideoEmbed />
</div>

// Skeleton placeholders
{isLoading ? <Skeleton className="h-20 w-full" /> : <Content />}
```

---

## Quick Wins Checklist

### Images
- [ ] Use `next/image` for all images
- [ ] Set `priority` on above-fold images
- [ ] Use `sizes` prop for responsive images
- [ ] Serve WebP/AVIF formats
- [ ] Lazy load below-fold images

### Fonts
- [ ] Use `next/font` (eliminates FOUT)
- [ ] Subset fonts to needed characters
- [ ] Preload critical fonts

### JavaScript
- [ ] Code split with `next/dynamic`
- [ ] Tree shake unused code
- [ ] Defer non-critical scripts
- [ ] Use `loading="lazy"` for iframes

### CSS
- [ ] Inline critical CSS
- [ ] Purge unused CSS
- [ ] Avoid large CSS files

### Server
- [ ] Use edge/CDN caching
- [ ] Compress responses (gzip/brotli)
- [ ] Optimize database queries

---

## Measurement

### Lighthouse
```bash
# CLI
npx lighthouse https://example.com --view

# In Chrome DevTools
# DevTools → Lighthouse tab → Generate report
```

### Web Vitals Library
```tsx
import { onCLS, onINP, onLCP } from 'web-vitals'

onCLS(console.log)
onINP(console.log)
onLCP(console.log)

// Send to analytics
function sendToAnalytics(metric) {
  const body = JSON.stringify(metric)
  navigator.sendBeacon('/api/analytics', body)
}

onCLS(sendToAnalytics)
onINP(sendToAnalytics)
onLCP(sendToAnalytics)
```

### Real User Monitoring (RUM)
```tsx
// pages/_app.tsx or layout.tsx
export function reportWebVitals(metric: NextWebVitalsMetric) {
  console.log(metric)
  // Send to your analytics service
}
```

---

## Common Issues & Fixes

| Issue | Metric | Fix |
|-------|--------|-----|
| Large hero image | LCP | Use `priority`, optimize size |
| Unoptimized fonts | LCP, CLS | Use `next/font` |
| Images without dimensions | CLS | Add `width`/`height` |
| Ads/embeds loading late | CLS | Reserve space with aspect ratio |
| Heavy JS on load | INP | Code split, defer |
| Long click handlers | INP | Debounce, use Web Workers |
| Third-party scripts | All | Load async, defer |

---

## Score Thresholds

| Metric | Good | Needs Improvement | Poor |
|--------|------|-------------------|------|
| LCP | ≤ 2.5s | 2.5s – 4s | > 4s |
| INP | ≤ 200ms | 200ms – 500ms | > 500ms |
| CLS | ≤ 0.1 | 0.1 – 0.25 | > 0.25 |
