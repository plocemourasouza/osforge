# Marketing Workflows — Routing Map

> Connects The Agency's agents (persona) with the marketingskills workflows (execution).
> Source: `coreyhaines31/marketingskills` v1.4.0, adapted for OSForge.

---

## How it works

1. The orchestrator detects a marketing/paid-media/sales demand
2. Activates the **agent** (persona with identity, rules, tone)
3. Loads the corresponding **workflow** (step-by-step execution framework)
4. The agent executes using the workflow as a playbook

**Rule:** The agent defines *who I am*. The workflow defines *what I do*.

---

## Prerequisite: Marketing Context

Before any workflow, check whether `.osforge/marketing-context.md` exists.
If it does not exist, use `workflows/product-marketing-context.md` to create it.
All workflows depend on this file as the source of truth about product, audience, and positioning.

---

## Division: 📢 Marketing (25 workflows)

### Conversion Rate Optimization (CRO)

| Workflow | When to use | Primary agent | Complementary agents |
|----------|-------------|-----------------|----------------------|
| `page-cro` | Optimize any marketing page | `marketing-growth-hacker` | `marketing-content-creator` |
| `signup-flow-cro` | Optimize the signup/registration flow | `marketing-growth-hacker` | — |
| `onboarding-cro` | Optimize post-signup activation | `marketing-growth-hacker` | — |
| `form-cro` | Optimize forms (except signup) | `marketing-growth-hacker` | — |
| `popup-cro` | Create/optimize popups and modals | `marketing-growth-hacker` | `marketing-content-creator` |
| `paywall-upgrade-cro` | Paywalls and in-app upgrade screens | `marketing-growth-hacker` | — |

### Content & Copy

| Workflow | When to use | Primary agent | Complementary agents |
|----------|-------------|-----------------|----------------------|
| `copywriting` | Write marketing copy for pages | `marketing-content-creator` | `marketing-growth-hacker` |
| `copy-editing` | Review and improve existing copy | `marketing-content-creator` | — |
| `content-strategy` | Plan a content strategy | `marketing-content-creator` | `marketing-seo-specialist` |
| `email-sequence` | Create automated email sequences | `marketing-content-creator` | `marketing-growth-hacker` |
| `lead-magnets` | Create lead magnets for lead capture | `marketing-content-creator` | `marketing-growth-hacker` |
| `social-content` | Content for social media | `marketing-social-media-strategist` | Platform agents* |

*Platform agents: `marketing-linkedin-content-creator`, `marketing-twitter-engager`, `marketing-instagram-curator`, `marketing-tiktok-strategist`, `marketing-reddit-community-builder`

### SEO & Discovery

| Workflow | When to use | Primary agent | Complementary agents |
|----------|-------------|-----------------|----------------------|
| `seo-audit` | Audit technical and on-page SEO | `marketing-seo-specialist` | — |
| `ai-seo` | Optimize for AI-driven search (AEO/GEO/LLMO) | `marketing-seo-specialist` | — |
| `programmatic-seo` | Create SEO pages at scale | `marketing-seo-specialist` | `marketing-growth-hacker` |
| `site-architecture` | Plan hierarchy, navigation, URLs | `marketing-seo-specialist` | — |
| `schema-markup` | Add/optimize structured data | `marketing-seo-specialist` | — |
| `competitor-alternatives` | Comparison pages with competitors | `marketing-seo-specialist` | `marketing-content-creator` |

### Retention & Growth

| Workflow | When to use | Primary agent | Complementary agents |
|----------|-------------|-----------------|----------------------|
| `churn-prevention` | Reduce churn, cancellation flows | `marketing-growth-hacker` | — |
| `free-tool-strategy` | Plan free marketing tools | `marketing-growth-hacker` | `marketing-seo-specialist` |
| `referral-program` | Create/optimize a referral program | `marketing-growth-hacker` | — |

### Strategy & Planning

| Workflow | When to use | Primary agent | Complementary agents |
|----------|-------------|-----------------|----------------------|
| `marketing-ideas` | Brainstorm marketing ideas | `marketing-growth-hacker` | `marketing-content-creator` |
| `marketing-psychology` | Apply psychology to marketing | `marketing-growth-hacker` | `marketing-content-creator` |
| `launch-strategy` | Plan a product/feature launch | `marketing-growth-hacker` | `marketing-content-creator`, `marketing-social-media-strategist` |
| `pricing-strategy` | Define pricing and packaging | `marketing-growth-hacker` | — |

---

## Division: 💰 Paid Media (4 workflows)

| Workflow | When to use | Primary agent | Complementary agents |
|----------|-------------|-----------------|----------------------|
| `paid-ads` | Google/Meta/LinkedIn Ads campaigns | `paid-media-ppc-strategist` | `paid-media-paid-social-strategist` |
| `ad-creative` | Generate ad creatives at scale | `paid-media-creative-strategist` | — |
| `analytics-tracking` | Set up tracking and measurement | `paid-media-tracking-specialist` | — |
| `ab-test-setup` | Plan and implement A/B tests | `paid-media-tracking-specialist` | `marketing-growth-hacker` |

---

## Division: 💼 Sales (3 workflows)

| Workflow | When to use | Primary agent | Complementary agents |
|----------|-------------|-----------------|----------------------|
| `cold-email` | B2B cold emails and follow-up sequences | `sales-outbound-strategist` | `sales-discovery-coach` |
| `sales-enablement` | Decks, one-pagers, objection docs | `sales-proposal-strategist` | `sales-deal-strategist` |
| `revops` | Lead lifecycle, scoring, MQL→SQL handoff | `sales-pipeline-analyst` | `sales-account-strategist` |

---

## Workflows without a direct agent (autonomous)

These workflows can be executed by the orchestrator without activating a specific agent.
The orchestrator takes on the appropriate persona based on context.

| Workflow | Description | Persona fallback |
|----------|-----------|-------------------|
| `product-marketing-context` | Create/update the project's marketing context | Orchestrator directly |

---

## Workflow Chaining

Workflows that naturally connect in sequence:

### Flow: New marketing page
```
product-marketing-context → copywriting → page-cro → schema-markup → analytics-tracking → ab-test-setup
```

### Flow: Complete SEO strategy
```
product-marketing-context → seo-audit → site-architecture → content-strategy → ai-seo → schema-markup → programmatic-seo
```

### Flow: Product launch
```
product-marketing-context → launch-strategy → copywriting → email-sequence → social-content → paid-ads → ad-creative → analytics-tracking
```

### Flow: Funnel optimization
```
page-cro → signup-flow-cro → onboarding-cro → email-sequence → churn-prevention → referral-program
```

### Flow: B2B outbound
```
product-marketing-context → competitor-alternatives → sales-enablement → cold-email → revops
```

---

## Cross-references across divisions

| Source | Destination | When |
|--------|---------|--------|
| Marketing → Paid Media | `copywriting` → `ad-creative` | Page copy becomes the base for creatives |
| Marketing → Paid Media | `page-cro` → `ab-test-setup` | CRO recommendations become test hypotheses |
| Marketing → Paid Media | `page-cro` → `analytics-tracking` | Optimizations need tracking |
| Marketing → Sales | `content-strategy` → `sales-enablement` | Marketing content feeds sales material |
| Marketing → Sales | `competitor-alternatives` → `cold-email` | Competitive differentiation enters the outreach |
| Paid Media → Marketing | `analytics-tracking` → `page-cro` | Tracking data reveals conversion problems |
| Sales → Marketing | `revops` → `email-sequence` | Lifecycle stages trigger email sequences |
