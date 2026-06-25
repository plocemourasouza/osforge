# Triage Rules — Marketing, Paid Media & Sales

> Extension of `agents/orchestrator/triage-rules.md` for marketing requests.
> Append to the end of the existing triage-rules.md.

---

## Marketing Request Detection

### Activation signals

The orchestrator should detect marketing requests by these keywords and contexts:

**CRO / Conversion:**
- "conversion", "CRO", "landing page", "bounce rate", "signup", "onboarding"
- "no one converts", "conversion rate", "form", "popup", "paywall"
- "optimize page", "improve conversions", "page isn't converting"

**Copy / Content:**
- "write copy", "headline", "CTA", "rewrite", "weak copy"
- "email sequence", "drip campaign", "welcome email", "newsletter"
- "content for", "content strategy", "lead magnet"
- "post for LinkedIn/Twitter/Instagram"

**SEO:**
- "SEO", "SEO audit", "ranking", "Google", "organic traffic"
- "schema", "sitemap", "core web vitals", "indexing"
- "AI search", "AEO", "GEO", "show up in ChatGPT/Perplexity"
- "pSEO", "programmatic SEO", "pages at scale"

**Paid Media:**
- "Google Ads", "Meta Ads", "LinkedIn Ads", "Facebook Ads"
- "paid campaign", "PPC", "ROAS", "CPA", "ad creative"
- "tracking", "GA4", "GTM", "pixel", "conversion tracking"
- "A/B test", "experiment", "A/B test"

**Sales:**
- "cold email", "outbound", "prospecting"
- "sales deck", "proposal", "one-pager", "objections"
- "pipeline", "MQL", "SQL", "lead scoring", "RevOps"

**Strategy:**
- "launch", "launch", "pricing", "pricing"
- "churn", "retention", "cancellation", "referral"
- "marketing ideas", "growth", "viral"

---

## Complexity Classification for Marketing

### QUICK — Direct execution

**Criteria (ALL must apply):**
- A single isolated task with clear context
- Product/audience already known (marketing-context exists)
- Does not require competitive research or data analysis
- Output is a single artifact (copy, audit, email, etc.)

**Examples:**
- "Rewrite this headline" → `copywriting`
- "Add schema markup to this page" → `schema-markup`
- "Write a cold email for CTOs" → `cold-email`
- "Review this copy" → `copy-editing`
- "Create an exit-intent popup" → `popup-cro`

**Pipeline:** context → workflow → output → review

### STANDARD — Task with planning

**Criteria (SOME apply):**
- Multiple interconnected outputs
- Needs analysis before acting (audit, review)
- Involves a sequence of steps (funnel, email sequence)
- Requires strategic decisions with trade-offs

**Examples:**
- "Do an SEO audit of my site" → `seo-audit` (analysis + recommendations)
- "Create a sequence of 5 emails" → `email-sequence` (strategy + copy)
- "Optimize my landing page" → `page-cro` (analysis + recommendations + copy)
- "Set up a Google Ads campaign" → `paid-ads` (strategy + setup + creatives)
- "Configure conversion tracking" → `analytics-tracking` (plan + implementation)

**Pipeline:** context → analysis → plan → phased execution → review

### COMPLEX — Complete strategy

**Criteria (SOME apply):**
- Complete channel or funnel strategy
- Involves multiple chained workflows
- Requires creating marketing-context from scratch
- Impacts multiple channels or teams

**Examples:**
- "Build my complete SEO strategy" → `seo-audit` + `site-architecture` + `content-strategy` + `ai-seo` + `schema-markup`
- "Prepare my product launch" → `launch-strategy` + `copywriting` + `email-sequence` + `social-content` + `paid-ads`
- "Optimize my entire funnel" → `page-cro` + `signup-flow-cro` + `onboarding-cro` + `email-sequence` + `churn-prevention`
- "Set up my RevOps operation" → `revops` + `analytics-tracking` + `sales-enablement` + `cold-email`

**Pipeline:** context → multi-phase plan → workflow-by-workflow execution → integrated review

---

## Routing to Skills by Domain (extension of the existing table)

| Project Type | Primary Skills/Workflows | Main Agent |
|---|---|---|
| CRO | `page-cro`, `signup-flow-cro`, `form-cro`, `popup-cro` | `marketing-growth-hacker` |
| Copywriting | `copywriting`, `copy-editing`, `lead-magnets` | `marketing-content-creator` |
| SEO | `seo-audit`, `ai-seo`, `schema-markup`, `site-architecture` | `marketing-seo-specialist` |
| Content | `content-strategy`, `email-sequence`, `social-content` | `marketing-content-creator` |
| Paid | `paid-ads`, `ad-creative`, `analytics-tracking`, `ab-test-setup` | `paid-media-ppc-strategist` |
| Sales | `cold-email`, `sales-enablement`, `revops` | `sales-outbound-strategist` |
| Growth | `churn-prevention`, `referral-program`, `free-tool-strategy` | `marketing-growth-hacker` |
| Strategy | `marketing-ideas`, `launch-strategy`, `pricing-strategy` | `marketing-growth-hacker` |

---

## Rule: Check marketing-context

**BEFORE executing any marketing/paid/sales workflow:**

```
If .osforge/marketing-context.md does NOT exist:
  → Inform the user: "To execute this workflow with quality,
    I need the project's marketing context. I can create it now
    (takes ~5 min) or proceed with the information you give me."
  → If accepted: run marketing-context-adapter first
  → If declined: proceed by asking for context inline
```

---

## Rule: Agent + Workflow Combo

When activating a marketing/paid/sales agent for a task:

```
1. Identify the corresponding workflow (see ROUTING.md)
2. Announce: "🤖 Activating @{agent} with workflow {workflow}..."
3. Load the agent file (identity)
4. Load the workflow file (execution)
5. Execute the workflow using the agent's persona
```

If the workflow generates recommendations that depend on ANOTHER workflow:
```
At the end: "Recommendations implemented. Suggested next step:
run {next-workflow} for {reason}. Proceed?"
```
