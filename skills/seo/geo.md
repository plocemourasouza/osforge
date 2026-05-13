# GEO (Generative Engine Optimization)

**Trigger:** GEO, AI search, LLM visibility, ChatGPT ranking, Perplexity

---

## What is GEO?

Optimization for AI-powered search engines:
- ChatGPT with browsing
- Perplexity
- Claude
- Google AI Overviews
- Bing Copilot

Unlike traditional SEO (ranking in a list), GEO aims to be **cited** and **quoted** by AI systems.

---

## Key Differences from SEO

| SEO | GEO |
|-----|-----|
| Rank #1 in list | Be cited in AI response |
| Keywords in title | Clear, definitive statements |
| Link building | Being a primary source |
| Click-through rate | Quote-worthiness |

---

## Content Principles

### Be Definitive
```markdown
// BAD - Vague
"There are several ways to optimize React performance."

// GOOD - Definitive, quotable
"The three most effective React performance optimizations are:
1. Memoization with useMemo and useCallback
2. Code splitting with React.lazy
3. Virtualization for long lists"
```

### Use Clear Structure
```markdown
## How to [Task]

### Prerequisites
- Item 1
- Item 2

### Step 1: [Action]
[Clear instruction]

### Step 2: [Action]
[Clear instruction]

### Common Issues
| Problem | Solution |
|---------|----------|
| Issue 1 | Fix 1 |
```

### Include Statistics & Data
```markdown
// BAD
"Next.js is faster than Create React App."

// GOOD
"Next.js Server Components reduce JavaScript bundle size by 40-60%
compared to client-side rendering, according to Vercel benchmarks."
```

---

## Structured Data for AI

### FAQ Schema
```tsx
const faqJsonLd = {
  '@context': 'https://schema.org',
  '@type': 'FAQPage',
  mainEntity: [
    {
      '@type': 'Question',
      name: 'What is the best way to optimize React performance?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: 'The most effective React performance optimizations include...',
      },
    },
  ],
}
```

### HowTo Schema
```tsx
const howToJsonLd = {
  '@context': 'https://schema.org',
  '@type': 'HowTo',
  name: 'How to Set Up Next.js with TypeScript',
  step: [
    {
      '@type': 'HowToStep',
      name: 'Create project',
      text: 'Run npx create-next-app@latest --typescript',
    },
    // ...
  ],
}
```

---

## Citation Optimization

### Be the Primary Source
- Original research and data
- Unique case studies
- First-party benchmarks
- Expert interviews

### Clear Attribution
```markdown
**Author:** Dr. Jane Smith, Senior Software Engineer at BigTech
**Published:** January 15, 2024
**Last Updated:** March 1, 2024
**Methodology:** [Link to methodology]
```

### Quote-Ready Paragraphs
```markdown
// Easy for AI to quote
"Server Components in Next.js 14 reduce client-side JavaScript
by up to 60%, resulting in faster page loads and better Core Web
Vitals scores. This is achieved by rendering components entirely
on the server and sending only the HTML to the client."
```

---

## Content Formats

### Comparison Tables
```markdown
| Feature | Next.js | Remix | Astro |
|---------|---------|-------|-------|
| SSR | Yes | Yes | Optional |
| SSG | Yes | No | Yes |
| Partial Hydration | Yes | No | Yes |
| Learning Curve | Medium | Medium | Low |
```

### Decision Trees
```markdown
### Choosing a Framework

**Do you need a full-stack solution?**
- Yes → Next.js or Remix
- No → Continue

**Is content mostly static?**
- Yes → Astro
- No → Continue

**Do you need real-time features?**
- Yes → Remix
- No → Next.js
```

### Definitive Lists
```markdown
## The 5 Essential TypeScript Compiler Options

1. **strict: true** — Enables all strict type checking
2. **noUncheckedIndexedAccess** — Safer array/object access
3. **noImplicitReturns** — Ensures all code paths return
4. **forceConsistentCasingInFileNames** — Prevents case issues
5. **esModuleInterop** — Better CommonJS compatibility
```

---

## Technical Implementation

### Fast Response Times
AI crawlers have timeouts. Ensure:
- TTFB < 200ms
- Full page load < 2s
- Edge deployment when possible

### Clean HTML
```html
<!-- Clear semantic structure -->
<article>
  <h1>Main Topic</h1>
  <p class="summary">Key takeaway in first paragraph...</p>
  <section>
    <h2>Subtopic 1</h2>
    <p>Detailed explanation...</p>
  </section>
</article>

<!-- Avoid -->
<div class="content">
  <div class="title">...</div>
  <div class="body">...</div>
</div>
```

### Accessible Content
- Alt text on images
- Transcripts for videos
- Readable font sizes
- No content behind interactions

---

## Monitoring

### Track AI Citations
- Set up alerts for brand mentions
- Monitor Perplexity/ChatGPT responses
- Check AI Overviews in Google

### Content Freshness
- Update statistics regularly
- Add "Last Updated" dates
- Archive outdated content

---

## Checklist

- [ ] Clear, definitive statements
- [ ] Structured with headings
- [ ] Comparison tables where applicable
- [ ] Statistics with sources
- [ ] Author credentials
- [ ] Last updated date
- [ ] FAQ schema for Q&A content
- [ ] HowTo schema for tutorials
- [ ] Fast page load
- [ ] Clean semantic HTML
