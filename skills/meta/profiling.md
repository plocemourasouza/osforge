# Performance Profiling

**Trigger:** Performance profiling, Lighthouse, Web Vitals profiling, bundle analysis.

---

## Core Web Vitals Targets

| Metric | Good | Needs Improvement | Poor |
|--------|------|-------------------|------|
| **LCP** | ≤2.5s | 2.5s-4s | >4s |
| **INP** | ≤200ms | 200ms-500ms | >500ms |
| **CLS** | ≤0.1 | 0.1-0.25 | >0.25 |

---

## Measurement Tools

### Lighthouse
```bash
# CLI
npx lighthouse https://example.com --output=json --output-path=./report.json

# Chrome DevTools
# Open DevTools → Lighthouse tab → Generate report
```

### Web Vitals
```typescript
import { onCLS, onINP, onLCP } from 'web-vitals'

onCLS(console.log)
onINP(console.log)
onLCP(console.log)
```

---

## Bundle Analysis

### Next.js
```bash
# Enable bundle analyzer
ANALYZE=true bun run build
```

```typescript
// next.config.js
const withBundleAnalyzer = require('@next/bundle-analyzer')({
  enabled: process.env.ANALYZE === 'true',
})
module.exports = withBundleAnalyzer({})
```

### Vite
```bash
bunx vite-bundle-visualizer
```

---

## React Profiler

```typescript
import { Profiler } from 'react'

function onRenderCallback(
  id: string,
  phase: 'mount' | 'update',
  actualDuration: number,
  baseDuration: number,
  startTime: number,
  commitTime: number
) {
  console.log({ id, phase, actualDuration, baseDuration })
}

<Profiler id="App" onRender={onRenderCallback}>
  <App />
</Profiler>
```

---

## Chrome DevTools Performance

### Recording
1. Open DevTools → Performance tab
2. Click Record
3. Perform action
4. Stop recording
5. Analyze flame graph

### Key Metrics
- **Scripting** — JavaScript execution time
- **Rendering** — Style, layout, paint
- **Loading** — Network requests

---

## Bottleneck Identification

### Long Tasks (>50ms)
```typescript
const observer = new PerformanceObserver((list) => {
  for (const entry of list.getEntries()) {
    if (entry.duration > 50) {
      console.warn('Long task detected:', entry)
    }
  }
})
observer.observe({ entryTypes: ['longtask'] })
```

### Memory Leaks
```typescript
// Take heap snapshot in DevTools
// Memory tab → Take snapshot
// Compare snapshots to find leaks
```

---

## Optimization Strategies

### By Metric

| Issue | Strategy |
|-------|----------|
| High LCP | Optimize images, preload critical resources |
| High INP | Break long tasks, use web workers |
| High CLS | Set explicit dimensions, reserve space |
| Large bundle | Code splitting, tree shaking |
| Slow API | Caching, pagination, CDN |
