---
name: marketing-context
description: "Create or update the project's marketing context. Use before any marketing workflow. Generates `.osforge/marketing-context.md`, which all workflows consult as the source of truth about product, audience, positioning, and voice."
metadata:
  version: 2.0.0
  origin: coreyhaines31/marketingskills (product-marketing-context v1.1.0)
  adapted-for: osforge
---

# Project Marketing Context

You help the user create and maintain the marketing context document.
This document captures positioning and messaging information that ALL
marketing, paid media, and sales workflows reference as the single source of truth.

**Output file:** `.osforge/marketing-context.md`

---

## OSForge Integration

### Existing context sources

Before asking the user anything, check these sources in this order:

1. **`.osforge/marketing-context.md`** — If it exists, read it and offer to update
2. **`project-context.md`** (root or `docs/`) — Extract stack, product, and audience
3. **`.osforge/STATE.md`** — Check prior product decisions
4. **`README.md`** of the project — Name, description, features

### No-duplication rule

If `project-context.md` already has information about the product (name, stack, features),
do NOT duplicate it. Reference it: "Stack and features covered in project-context.md."
The marketing-context focuses on what project-context does NOT cover: positioning,
audience, voice, customer pains, differentiation, and social proof.

---

## Workflow

### Step 1: Check existing context

Check whether `.osforge/marketing-context.md` exists.
Also check `.agents/product-marketing-context.md` and
`.claude/product-marketing-context.md` as migration fallbacks.

**If found in an old location:** offer automatic migration:
```
I found marketing context in .agents/product-marketing-context.md.
I'll migrate it to .osforge/marketing-context.md to integrate with OSForge.
```

**If marketing-context.md exists:**
- Read it and summarize what is captured
- Ask which sections you want to update
- Only collect info for the chosen sections

**If it does not exist, offer two options:**
1. **Auto-draft from the codebase** (recommended): Study the repo, README,
   landing pages, copy, package.json, and generate a V1
2. **Start from scratch**: Walk through each section conversationally

### Step 2: Collect information

**If auto-drafting:**
1. Read: README, landing pages, marketing copy, about pages, meta descriptions,
   package.json, project-context.md
2. Generate a draft of all sections
3. Present it and ask what needs correcting
4. Iterate until the user is satisfied

**If from scratch:**
Walk through one section at a time. Do not dump all the questions at once.
Insist on real customer language — exact phrases are worth more than
polished descriptions.

---

## Sections to Capture

### 1. Product Vision
- One-sentence description
- What it does (2-3 sentences)
- Product category (which "shelf" the customer looks for you on)
- Type (SaaS, marketplace, e-commerce, service, etc.)
- Business model and pricing

### 2. Target Audience
- Company type (industry, size, stage)
- Target decision-makers (titles, departments)
- Primary use case
- Jobs to be done (2-3 things the customer "hires" you for)
- Specific usage scenarios

### 3. Personas (B2B)
For each stakeholder in the buying process:
- User, Champion, Decision-Maker, Economic Buyer, Technical Influencer
- What each one values, their challenge, and the value promise

### 4. Problems & Pains
- Core challenge before finding your solution
- Why current solutions fail
- Cost of inaction (time, money, opportunities)
- Emotional tension (stress, fear, doubt)

### 5. Differentiation
- Direct alternatives (competitors) and indirect ones (spreadsheets, manual, etc.)
- What makes you different (not "better" — different)
- One-sentence positioning: "[Product] is the only [category] that [differentiator]"

### 6. Social Proof
- Metrics (users, revenue, growth, time saved)
- Notable customers or logos
- Documented results
- Reviews and ratings

### 7. Voice & Tone
- How the brand sounds (formal/informal, technical/accessible)
- Words and phrases the brand USES
- Words and phrases the brand AVOIDS
- Tone references (e.g., "like a technical colleague explaining")

### 8. Channel Strategy
- Current acquisition channels (organic, paid, email, social, partnerships)
- Most effective channel
- Planned or in-testing channels

---

## Output Format

Generate `.osforge/marketing-context.md` with this template:

```markdown
# Marketing Context — [Product Name]

> Generated on [date]. Source of truth for all marketing workflows.
> Stack and features: see project-context.md

## Product
[content from section 1]

## Audience
[content from section 2]

## Personas
[content from section 3 — omit if B2C]

## Problems & Pains
[content from section 4]

## Differentiation
[content from section 5]

## Social Proof
[content from section 6]

## Voice & Tone
[content from section 7]

## Channels
[content from section 8]
```

---

## Related Skills

- **After creating context:** use `copywriting` to write copy, `page-cro` to optimize pages
- **For SEO:** `seo-audit` and `content-strategy` use the audience and positioning from here
- **For sales:** `sales-enablement` and `cold-email` use the pains and differentiation from here
- **For ads:** `paid-ads` and `ad-creative` use the voice, audience, and social proof from here
