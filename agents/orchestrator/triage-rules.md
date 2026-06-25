# Triage Rules

## Complexity Classification

### QUICK — Direct execution

**ALL criteria must apply:**
- Clear and limited scope (1-3 files)
- Zero ambiguity about what to do
- No new architectural decisions
- No new Prisma models/schemas
- No new external integrations
- Zero blast radius (no unintended consequences)

**Typical user signals:**
- "corrigir", "fix", "adjust", "bug"
- "add field", "change color", "rename"
- "refactor function", "extract component"
- "add validation in X"
- "run lint", "format code", "update dependency"
- "improve SEO of page X", "fix meta tags"
- "write documentation for X", "create README"

**Pipeline:** spec → implement → review
**Artifacts:** tech-spec.md only

---

### STANDARD — Feature with planning

**SOME of the criteria apply:**
- Feature with defined but multi-file scope (4-10 files)
- Needs new models or schema changes in Prisma
- Impacts existing API routes or Server Actions
- Creates a new UI flow (but a known domain)
- Integration with an already-configured service (e.g., Stripe already exists, add a new webhook)

**BUT the domain is known and the stack is the project default.**

**Typical user signals:**
- "create feature for", "add module for"
- "implement flow for", "integrate with"
- "new CRUD for", "add authentication in"
- "create API for", "endpoint for", "GraphQL schema for"
- "mobile app for", "mobile screen for"
- "game with", "game of", "multiplayer"
- "deploy with Docker", "configure CI/CD"
- "optimize performance of", "profiling of"

**Pipeline:** spec → arch-check (if schema) → stories → implement loop → review
**Artifacts:** spec.md, stories/

---

### COMPLEX — System with full planning

**SOME of the criteria apply:**
- An entire new system or module
- Ambiguous requirements that need to be distilled
- Multiple new external integrations
- Significant architectural decisions (new infra, new pattern)
- Cross-cutting impact across several existing modules
- Compliance requirements (LGPD, TSE, ICP-Brasil)
- Multi-tenant or multi-role with complex rules

**Typical user signals:**
- "build a system for", "new product", "new platform"
- "migrate from X to Y", "redesign module"
- "complete system with", "I want it to have"
- Long descriptions with multiple interconnected features
- "create a complete game", "mobile app from scratch", "SaaS for"
- "new project with" (→ use `skills/app-builder` for scaffolding)
- "microservices architecture", "complete redesign"
- "multi-tenant platform", "marketplace"

**Pipeline:** prd → architecture → epics → readiness-gate → sprint loop
**Artifacts:** prd.md, architecture.md, epics/, sprint-status.yaml

---

## Decision When in Doubt

When the classification is not clear:

1. **In doubt between QUICK and STANDARD** → STANDARD
   (it is better to plan a bit more than to discover mid-way that something was missing)

2. **In doubt between STANDARD and COMPLEX** → Ask the user:
   "This looks to me like it's between STANDARD and COMPLEX. If you already have clarity
   about what to build and it is an isolated module, STANDARD is enough. If the requirements
   are still forming or there are many interconnected pieces, COMPLEX
   ensures nothing gets lost. What do you think?"

3. **User override** always prevails:
   "I want to treat it as QUICK" → respect it, even if it is technically STANDARD
   "Do the full planning" → COMPLEX regardless of the classification

---

## Specialized Skills by Project Type

When the request involves a specific domain, load the corresponding skills:

| Project Type | Primary Skills | Main Agent |
|---|---|---|
| Next.js web app | `nextjs-react-expert`, `frontend-ui-system`, `tailwind-patterns` | `frontend-engineer` |
| Landing / Hero / Marketing site | `frontend-design`, `aesthetic-boost`, `taste-design-dials`, `aesthetic-modes` (mood-dependent), `frontend-ui-system` | `frontend-engineer` |
| Premium / Awwwards / Agency-tier | `taste-design-dials`, `aesthetic-modes` → `SOFT_PREMIUM`, `aesthetic-boost`, `ui-audit` (post) | `frontend-engineer` |
| Editorial / Minimalist (Notion/Linear) | `aesthetic-modes` → `EDITORIAL_MINIMALIST`, `frontend-design`, `taste-design-dials` (low motion/density) | `frontend-engineer` |
| Brutalist / Industrial / Terminal | `aesthetic-modes` → `INDUSTRIAL_BRUTALIST`, `frontend-design`, `taste-design-dials` (high density) | `frontend-engineer` |
| Redesign / Modernize existing UI | `redesign-audit` → `ui-audit` → fix loop | `frontend-engineer` |
| Google Stitch export | `stitch-design-export`, `ui-design-intelligence` | (no dedicated agent) |
| Long / multi-file output | + `output-enforcement` (modifier, always) | (any agent) |
| API/Backend | `api-patterns`, `nodejs-best-practices`, `database-design` | `backend-engineer` |
| Mobile app | `mobile-design`, `app-builder` (react-native/flutter template) | `mobile-developer` |
| Game | `game-development` + relevant sub-skills | `game-developer` |
| Security/Audit | `security-best-practices`, `red-team-tactics`, `vulnerability-scanner` | `security-auditor` + `penetration-tester` |
| Performance | `performance-profiling`, `react-performance`, `core-web-vitals` | `performance-optimizer` |
| DevOps/Deploy | `deployment-procedures`, `server-management`, `claude-ci-actions` | `devops-engineer` |
| SEO/GEO | `seo-fundamentals`, `seo`, `genai-optimization` | `seo-specialist` |
| Documentation | `documentation-templates`, `docs-writer`, `technical-design-doc-creator` | `documentation-writer` |
| Legacy/Refactor | `clean-code`, `coding-guidelines` | `code-archaeologist` + `code-refactorer` |
| Rust | `rust-pro` | (no dedicated agent, use inline expertise) |
| Python | `python-patterns` | (no dedicated agent, use inline expertise) |
| Scaffolding | `app-builder` (13 templates available) | (app-builder workflow) |
| Brainstorm | `brainstorming` | (Socratic workflow) |
| Testing | `tdd-workflow`, `testing-patterns`, `e2e-testing-patterns`, `webapp-testing` | `test-engineer` + `qa-automation-engineer` |
| Database | `database-design`, `prisma-expert`, `postgres-optimization` | `database-architect` |
| Marketing/CRO | See `./triage-rules-marketing.md` | `marketing-growth-hacker` (The Agency) |
| Paid Media | See `./triage-rules-marketing.md` | `paid-media-ppc-strategist` (The Agency) |
| Sales/RevOps | See `./triage-rules-marketing.md` | `sales-outbound-strategist` (The Agency) |
