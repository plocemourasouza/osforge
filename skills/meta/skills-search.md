# Agent Skills Search

**Trigger:** Need specialized skills, best practices, or domain patterns.

---

## Commands

```bash
# Search by term
python3 ~/Development/osforge/scripts/buscar-skill.py <term>

# Search by category
python3 ~/Development/osforge/scripts/buscar-skill.py --cat security

# Show statistics
python3 ~/Development/osforge/scripts/buscar-skill.py --stats
```

---

## Tiers

| Tier | Sources | Quality |
|------|---------|---------|
| **Tier 1** | Anthropic, Superpowers, Vercel, Trail of Bits, Supabase | Production-grade |
| **Tier 2** | Context Engineering, Cloudflare, Sentry | High quality |
| **Tier 3** | Antigravity (634 skills), Expo, Curadoria | Community |

---

## Categories

- `security` — Security patterns, audits, threat modeling
- `nextjs` — Next.js patterns, App Router, Server Components
- `react` — React patterns, hooks, optimization
- `testing` — Testing strategies, Playwright, Vitest
- `database` — PostgreSQL, Prisma, Supabase
- `deployment` — CI/CD, Vercel, production ops
- `api` — REST, GraphQL, tRPC patterns

---

## Usage Examples

```bash
# Find authentication patterns
python3 ~/Development/osforge/scripts/buscar-skill.py auth

# Find all security skills
python3 ~/Development/osforge/scripts/buscar-skill.py --cat security

# Find Supabase-specific skills
python3 ~/Development/osforge/scripts/buscar-skill.py supabase
```

---

## Output Format

```
[Tier 1] anthropic/security-best-practices
  Path: ~/.claude/skills/security-best-practices/SKILL.md
  Tags: security, auth, validation

[Tier 2] cloudflare/edge-caching
  Path: ~/.claude/skills/edge-caching/SKILL.md
  Tags: performance, edge, caching
```
