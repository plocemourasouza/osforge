# The Agency — AI Specialist Library

**Trigger:** Needing a specialist in any area not covered by the technical skills above.

---

## Load

```
Leia skills/agency/SKILL.md
```

---

## Divisions (10)

| Division | Specialists | Focus |
|----------|-------------|-------|
| **Engineering** | 15+ | Security, SRE, DevOps, mobile, blockchain |
| **Design** | 10+ | UI/UX, design systems, identity, image prompts |
| **Marketing** | 12+ | SEO, content, social media, growth, ASO |
| **Paid Media** | 8+ | Google/Meta Ads, PPC, analytics |
| **Product** | 10+ | Roadmap, prioritization, market research |
| **Project Management** | 8+ | Planning, Jira, scrum |
| **Sales** | 10+ | Outbound, discovery, MEDDPICC, pipeline |
| **Support** | 8+ | Customer service, compliance, operations |
| **Quality** | 10+ | QA, API testing, WCAG, performance |
| **Advanced** | 10+ | Agent orchestration, SOC2/ISO, supply chain |

---

## Hierarchical Loading

```
1. Router (this file) → identifies division
2. Division index → lists available agents
3. Agent file → loads the specific specialist
```

**Zero context cost** until activated.

---

## Usage Examples

### Engineering
```
"I need help with API security"
→ Load: skills/agency/engineering/engineering-security-architect.md
```

### Design
```
"Create a prompt to generate a product image"
→ Load: skills/agency/design/design-image-prompt-engineer.md
```

### Marketing
```
"ASO strategy for a mobile app"
→ Load: skills/agency/marketing/marketing-aso-specialist.md
```

---

## Total: 121 Specialists

Each specialist has:
- Optimized system prompt
- Defined area of expertise
- Usage examples
- Documented limitations
