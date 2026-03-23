---
name: nextjs-static
description: Modern template for Next.js 16, React 19 & Tailwind v4. Optimized for Landing pages and Portfolios.
---

# Next.js Static Site Template (Modern Edition)

## Tech Stack

| Component | Technology | Notes |
|-----------|------------|-------|
| Framework | Next.js 16+ | App Router, Turbopack, Static Exports |
| Core | React 19 | Server Components, New Hooks, Compiler |
| Language | TypeScript | Strict Mode |
| Styling | Tailwind CSS v4 | CSS-first configuration (No js config), Oxide Engine |
| Animations | Framer Motion | Layout animations & gestures |
| Icons | Lucide React | Lightweight SVG icons |
| SEO | Metadata API | Native Next.js API (Replaces next-seo) |

---

## Directory Structure

```
project-name/
├── src/
│   ├── app/
│   │   ├── layout.tsx    # Contains root SEO Metadata
│   │   ├── page.tsx      # Landing Page
│   │   ├── globals.css   # Import Tailwind v4 & @theme config
│   │   ├── not-found.tsx # Custom 404 page
│   │   └── (routes)/     # Route groups (about, contact...)
│   ├── components/
│   │   ├── layout/       # Header, Footer
│   │   ├── sections/     # Hero, Features, Pricing, CTA
│   │   └── ui/           # Atomic components (Button, Card)
│   └── lib/
│       └── utils.ts      # Helper functions (cn, formatters)
├── content/              # Markdown/MDX content
├── public/               # Static assets (images, fonts)
├── next.config.ts        # Next.js Config (TypeScript)
└── package.json
```

---

## Static Export Config

```typescript
// next.config.ts
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: 'export',        // Required for Static Hosting
  images: {
    unoptimized: true      // Required if not using server image optimization
  },
  trailingSlash: true,     // Recommended for SEO
  reactStrictMode: true,
};

export default nextConfig;
```

---

## Deployment

| Platform | Method | Important Notes |
|----------|--------|-----------------|
| Vercel | Git Push | Auto-detects Next.js. Best for performance. |
| GitHub Pages | GitHub Actions | Need to set `basePath` if not using custom domain. |
| AWS S3 / CloudFront | Upload out folder | Ensure Error Document is configured to `404.html`. |
| Netlify | Git Push | Set build command to `npm run build`. |

---

## Best Practices (Modern)

- **React Server Components (RSC)**: Default all components to Server Components. Only add `'use client'` when you need state or events.
- **Image Optimization**: Use `<Image />` but remember `unoptimized: true` for static export.
- **Font Optimization**: Use `next/font` to automatically host fonts.
- **Responsive**: Mobile-first design using Tailwind prefixes.
