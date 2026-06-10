---
name: agent-skills-search
description: Search and install Agent Skills from the local sources at ~/Development/osforge/sources/. Use when looking for specialized skills, best practices, or domain-specific patterns for security, React, PostgreSQL, testing, mobile, Cloudflare, or any technical domain. Triggers when the user asks about available skills, wants to install skills, or needs specialized knowledge for a new domain — frases concretas como "instala a skill de prisma", "procura um padrão de PostgreSQL", "tem alguma skill de testing?", "quais skills existem para mobile?", "instala a skill X no projeto".
---

# Agent Skills Repository Search

Local sources: `~/Development/osforge/sources/`

## Quick Search

```bash
# Search by keyword
python3 ~/Development/osforge/scripts/buscar-skill.py <term>

# Search by category
python3 ~/Development/osforge/scripts/buscar-skill.py --cat security
python3 ~/Development/osforge/scripts/buscar-skill.py --cat react
python3 ~/Development/osforge/scripts/buscar-skill.py --cat database
python3 ~/Development/osforge/scripts/buscar-skill.py --cat testing

# Install to current project
python3 ~/Development/osforge/scripts/buscar-skill.py --install prisma

# Repository stats
python3 ~/Development/osforge/scripts/buscar-skill.py --stats
```

## Install Skills

```bash
# Single skill — copy from sources to project
cp -R ~/Development/osforge/sources/<folder>/<skill> .claude/skills/

# Example: install Supabase best-practices
cp -R ~/Development/osforge/sources/08-supabase/supabase-postgres-best-practices .claude/skills/

# Example: install Trail of Bits insecure-defaults
cp -R ~/Development/osforge/sources/07-trailofbits/insecure-defaults .claude/skills/
```

## Tier Overview

### Tier 1 — Essential (install everywhere)
| Source | Focus | Key Skills |
|--------|-------|------------|
| `sources/01-anthropic/` | Design & docs | frontend-design, docx, pdf, xlsx, pptx, webapp-testing |
| `sources/02-superpowers/` | Workflow | brainstorming, writing-plans, executing-plans, tdd, debugging, verification |
| `sources/04-vercel/` | React/Next.js | react-best-practices (57 rules), web-design-guidelines (100+ rules) |
| `sources/07-trailofbits/` | Security | static-analysis, insecure-defaults, sharp-edges, audit-context |
| `sources/08-supabase/` | Database | supabase-postgres-best-practices |

### Tier 2 — Selective
| Source | When to Use |
|--------|-------------|
| `sources/05-context-engineering/` | Multi-agent context optimization |
| `sources/10-cloudflare/` | Workers, R2, Durable Objects, Agents SDK |
| `sources/11-sentry/` | Code review, commit conventions, PR workflow |

### Tier 3 — Cherry-pick
| Source | Content |
|--------|---------|
| `sources/06-antigravity/` | 634 universal skills (typescript, prisma, docker, architecture) |
| `sources/09-expo/` | Mobile (expo-app-design, expo-deployment) |
| `sources/12-curadoria/` | Awesome lists (Stripe, Hugging Face, HashiCorp) |
| `sources/13-claude-red/` | Offensive security (27 skills — uso autorizado apenas; versões curadas em skills/offensive-*) |

## Index Files
- JSON: `~/Development/osforge/INDICE-SKILLS.json`
- Markdown: `~/Development/osforge/docs/INDICE-SKILLS.md`
