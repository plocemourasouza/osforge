# SEO

**Trigger:** SEO, meta tags, sitemap, E-E-A-T, search ranking, structured data

---

## Meta Tags

### Basic Meta
```tsx
// app/layout.tsx or page.tsx
export const metadata: Metadata = {
  title: 'Page Title | Brand',
  description: 'Compelling description under 160 characters that summarizes the page content.',
  keywords: ['keyword1', 'keyword2'],  // Less important now
}
```

### Dynamic Meta
```tsx
// app/blog/[slug]/page.tsx
export async function generateMetadata({ params }): Promise<Metadata> {
  const post = await getPost(params.slug)

  return {
    title: post.title,
    description: post.excerpt,
    openGraph: {
      title: post.title,
      description: post.excerpt,
      images: [post.coverImage],
    },
  }
}
```

---

## Open Graph & Twitter Cards

```tsx
export const metadata: Metadata = {
  title: 'My Page',
  description: 'Description here',

  openGraph: {
    title: 'My Page',
    description: 'Description here',
    url: 'https://example.com/page',
    siteName: 'My Site',
    images: [
      {
        url: 'https://example.com/og-image.jpg',
        width: 1200,
        height: 630,
        alt: 'Description of image',
      },
    ],
    locale: 'en_US',
    type: 'website',
  },

  twitter: {
    card: 'summary_large_image',
    title: 'My Page',
    description: 'Description here',
    images: ['https://example.com/twitter-image.jpg'],
    creator: '@username',
  },
}
```

---

## Canonical URLs

```tsx
export const metadata: Metadata = {
  alternates: {
    canonical: 'https://example.com/page',
    languages: {
      'en-US': 'https://example.com/en-US/page',
      'pt-BR': 'https://example.com/pt-BR/page',
    },
  },
}
```

---

## Structured Data (JSON-LD)

```tsx
// app/blog/[slug]/page.tsx
export default async function BlogPost({ params }) {
  const post = await getPost(params.slug)

  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'BlogPosting',
    headline: post.title,
    datePublished: post.publishedAt,
    dateModified: post.updatedAt,
    author: {
      '@type': 'Person',
      name: post.author.name,
    },
    image: post.coverImage,
    description: post.excerpt,
  }

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />
      <article>...</article>
    </>
  )
}
```

### Common Schema Types
- `Article` / `BlogPosting`
- `Product`
- `Organization`
- `Person`
- `FAQPage`
- `BreadcrumbList`
- `LocalBusiness`

---

## Sitemap

### next-sitemap
```bash
bun add next-sitemap
```

```javascript
// next-sitemap.config.js
module.exports = {
  siteUrl: 'https://example.com',
  generateRobotsTxt: true,
  sitemapSize: 7000,
  exclude: ['/admin/*', '/api/*'],
  robotsTxtOptions: {
    additionalSitemaps: [
      'https://example.com/server-sitemap.xml',
    ],
  },
}
```

### Dynamic Sitemap
```tsx
// app/sitemap.ts
export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const posts = await getPosts()

  const postUrls = posts.map((post) => ({
    url: `https://example.com/blog/${post.slug}`,
    lastModified: post.updatedAt,
    changeFrequency: 'weekly',
    priority: 0.8,
  }))

  return [
    {
      url: 'https://example.com',
      lastModified: new Date(),
      changeFrequency: 'daily',
      priority: 1,
    },
    ...postUrls,
  ]
}
```

---

## robots.txt

```tsx
// app/robots.ts
export default function robots(): MetadataRoute.Robots {
  return {
    rules: {
      userAgent: '*',
      allow: '/',
      disallow: ['/admin/', '/api/', '/private/'],
    },
    sitemap: 'https://example.com/sitemap.xml',
  }
}
```

---

## Semantic HTML

```tsx
// One h1 per page
<h1>Main Page Title</h1>

// Hierarchical headings
<h2>Section</h2>
<h3>Subsection</h3>

// Semantic structure
<header>...</header>
<nav>...</nav>
<main>
  <article>
    <header>...</header>
    <section>...</section>
  </article>
  <aside>...</aside>
</main>
<footer>...</footer>
```

---

## E-E-A-T

**E**xperience, **E**xpertise, **A**uthoritativeness, **T**rustworthiness

### Signals
- Author bios with credentials
- Clear contact information
- Privacy policy, terms of service
- SSL certificate
- Reviews and testimonials
- Backlinks from authoritative sources
- Accurate, well-researched content
- Regular content updates

---

## Performance (Core Web Vitals)

SEO ranking factor:
- **LCP** ≤ 2.5s
- **INP** ≤ 200ms
- **CLS** ≤ 0.1

See: `~/.claude/skills/design/core-web-vitals.md`

---

## Checklist

### Every Page
- [ ] Unique, descriptive `<title>` (50-60 chars)
- [ ] Meta description (150-160 chars)
- [ ] Canonical URL
- [ ] One `<h1>` tag
- [ ] Semantic heading hierarchy

### Site-wide
- [ ] robots.txt configured
- [ ] sitemap.xml generated
- [ ] SSL certificate
- [ ] Mobile-friendly
- [ ] Fast loading (Core Web Vitals)
- [ ] Structured data where applicable
- [ ] Open Graph tags
- [ ] Analytics tracking
