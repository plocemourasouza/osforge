---
name: agent-skills-search
description: Search and install Agent Skills from the local consolidated repository at ~/Development/agent-skills-consolidado/. Use when looking for specialized skills, best practices, or domain-specific patterns for security, React, PostgreSQL, testing, mobile, Cloudflare, or any technical domain. Triggers when the user asks about available skills, wants to install skills, or needs specialized knowledge for a new domain.
---

# Agent Skills Repository Search

Local repository: `~/Development/agent-skills-consolidado/`

## Quick Search

```bash
# Search by keyword
python3 ~/Development/agent-skills-consolidado/buscar-skill.py <term>

# Search by category
python3 ~/Development/agent-skills-consolidado/buscar-skill.py --cat security
python3 ~/Development/agent-skills-consolidado/buscar-skill.py --cat react
python3 ~/Development/agent-skills-consolidado/buscar-skill.py --cat database
python3 ~/Development/agent-skills-consolidado/buscar-skill.py --cat testing

# Install to current project
python3 ~/Development/agent-skills-consolidado/buscar-skill.py --install prisma

# Repository stats
python3 ~/Development/agent-skills-consolidado/buscar-skill.py --stats
```

## Install Skills

```bash
# Single skill
cp -R ~/Development/agent-skills-consolidado/<folder>/<skill> .claude/skills/

# Full Tier 1 (essential skills for any project)
bash ~/Development/agent-skills-consolidado/install-tier1.sh /path/to/project
```

## Tier Overview

### Tier 1 — Essential (install everywhere)
| Source | Focus | Key Skills |
|--------|-------|------------|
| `01-anthropic/` | Design & docs | frontend-design, docx, pdf, xlsx, pptx, webapp-testing |
| `02-superpowers/` | Workflow | brainstorming, writing-plans, executing-plans, tdd, debugging, verification |
| `04-vercel/` | React/Next.js | react-best-practices (57 rules), web-design-guidelines (100+ rules) |
| `07-trailofbits/` | Security | static-analysis, insecure-defaults, sharp-edges, audit-context |
| `08-supabase/` | Database | supabase-postgres-best-practices |

### Tier 2 — Selective
| Source | When to Use |
|--------|-------------|
| `05-context-engineering/` | Multi-agent context optimization |
| `10-cloudflare/` | Workers, R2, Durable Objects, Agents SDK |
| `11-sentry/` | Code review, commit conventions, PR workflow |

### Tier 3 — Cherry-pick
| Source | Content |
|--------|---------|
| `06-antigravity/` | 634 universal skills (typescript, prisma, docker, architecture) |
| `09-expo/` | Mobile (expo-app-design, expo-deployment) |
| `12-curadoria/` | Awesome lists (Stripe, Hugging Face, HashiCorp) |

## Index Files
- JSON: `~/Development/agent-skills-consolidado/INDICE-SKILLS.json`
- Markdown: `~/Development/agent-skills-consolidado/INDICE-SKILLS.md`
- Synthesis: `~/Development/agent-skills-consolidado/SINTESE-REPOSITORIOS.md`
