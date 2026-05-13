# Regras de Triage

## Classificação de Complexidade

### QUICK — Execução direta

**TODOS os critérios devem se aplicar:**
- Escopo claro e limitado (1-3 arquivos)
- Zero ambiguidade no que fazer
- Sem decisões arquiteturais novas
- Sem novos models/schemas no Prisma
- Sem integrações externas novas
- Zero blast radius (sem consequências não-intencionais)

**Sinais típicos do usuário:**
- "corrigir", "fix", "ajustar", "bug"
- "adicionar campo", "mudar cor", "renomear"
- "refatorar função", "extrair componente"
- "adicionar validação em X"
- "rodar lint", "formatar código", "atualizar dependência"
- "melhorar SEO da página X", "corrigir meta tags"
- "escrever documentação de X", "criar README"

**Pipeline:** spec → implement → review
**Artefatos:** tech-spec.md apenas

---

### STANDARD — Feature com planejamento

**ALGUM dos critérios se aplica:**
- Feature com escopo definido mas multi-arquivo (4-10 arquivos)
- Precisa de novos models ou schema changes no Prisma
- Impacta API routes ou Server Actions existentes
- Cria novo fluxo de UI (mas domínio conhecido)
- Integração com serviço já configurado (ex: Stripe já existe, adicionar novo webhook)

**MAS domínio é conhecido e stack é o padrão do projeto.**

**Sinais típicos do usuário:**
- "criar feature de", "adicionar módulo de"
- "implementar fluxo de", "integrar com"
- "novo CRUD de", "adicionar autenticação em"
- "criar API de", "endpoint para", "GraphQL schema para"
- "app mobile para", "tela mobile de"
- "game com", "jogo de", "multiplayer"
- "deploy com Docker", "configurar CI/CD"
- "otimizar performance de", "profiling de"

**Pipeline:** spec → arch-check (se schema) → stories → implement loop → review
**Artefatos:** spec.md, stories/

---

### COMPLEX — Sistema com planejamento completo

**ALGUM dos critérios se aplica:**
- Sistema ou módulo inteiro novo
- Requisitos ambíguos que precisam ser destilados
- Múltiplas integrações externas novas
- Decisões arquiteturais significativas (nova infra, novo padrão)
- Impacto cross-cutting em vários módulos existentes
- Requisitos de compliance (LGPD, TSE, ICP-Brasil)
- Multi-tenant ou multi-role com regras complexas

**Sinais típicos do usuário:**
- "construir sistema de", "novo produto", "nova plataforma"
- "migrar de X para Y", "redesenhar módulo"
- "sistema completo com", "quero que tenha"
- Descrições longas com múltiplas features interconectadas
- "criar jogo completo", "app mobile do zero", "SaaS de"
- "novo projeto com" (→ usar `skills/app-builder` para scaffolding)
- "arquitetura de microsserviços", "redesign completo"
- "plataforma multi-tenant", "marketplace"

**Pipeline:** prd → architecture → epics → readiness-gate → sprint loop
**Artefatos:** prd.md, architecture.md, epics/, sprint-status.yaml

---

## Decisão em Caso de Dúvida

Quando a classificação não é clara:

1. **Na dúvida entre QUICK e STANDARD** → STANDARD
   (é melhor planejar um pouco mais do que descobrir no meio que faltou)

2. **Na dúvida entre STANDARD e COMPLEX** → Perguntar ao usuário:
   "Isso me parece entre STANDARD e COMPLEX. Se você já tem clareza do
   que construir e é um módulo isolado, STANDARD basta. Se os requisitos
   ainda estão se formando ou há muitas peças interconectadas, COMPLEX
   garante que nada se perca. O que você acha?"

3. **Override do usuário** sempre prevalece:
   "Quero tratar como QUICK" → respeitar, mesmo que tecnicamente seja STANDARD
   "Faz o planejamento completo" → COMPLEX independente da classificação

---

## Skills Especializados por Tipo de Projeto

Quando a demanda envolve um domínio específico, carregar os skills correspondentes:

| Tipo de Projeto | Skills Primários | Agente Principal |
|---|---|---|
| App web Next.js | `nextjs-react-expert`, `frontend-ui-system`, `tailwind-patterns` | `frontend-engineer` |
| Landing / Hero / Marketing site | `frontend-design`, `aesthetic-boost`, `taste-design-dials`, `aesthetic-modes` (mood-dependent), `frontend-ui-system` | `frontend-engineer` |
| Premium / Awwwards / Agency-tier | `taste-design-dials`, `aesthetic-modes` → `SOFT_PREMIUM`, `aesthetic-boost`, `ui-audit` (post) | `frontend-engineer` |
| Editorial / Minimalist (Notion/Linear) | `aesthetic-modes` → `EDITORIAL_MINIMALIST`, `frontend-design`, `taste-design-dials` (low motion/density) | `frontend-engineer` |
| Brutalist / Industrial / Terminal | `aesthetic-modes` → `INDUSTRIAL_BRUTALIST`, `frontend-design`, `taste-design-dials` (high density) | `frontend-engineer` |
| Redesign / Modernize existing UI | `redesign-audit` → `ui-audit` → fix loop | `frontend-engineer` |
| Google Stitch export | `stitch-design-export`, `ui-design-intelligence` | (sem agente dedicado) |
| Output longo / multi-arquivo | + `output-enforcement` (modifier, sempre) | (qualquer agente) |
| API/Backend | `api-patterns`, `nodejs-best-practices`, `database-design` | `backend-engineer` |
| App mobile | `mobile-design`, `app-builder` (react-native/flutter template) | `mobile-developer` |
| Game | `game-development` + sub-skills relevantes | `game-developer` |
| Segurança/Audit | `security-best-practices`, `red-team-tactics`, `vulnerability-scanner` | `security-auditor` + `penetration-tester` |
| Performance | `performance-profiling`, `react-performance`, `core-web-vitals` | `performance-optimizer` |
| DevOps/Deploy | `deployment-procedures`, `server-management`, `claude-ci-actions` | `devops-engineer` |
| SEO/GEO | `seo-fundamentals`, `seo`, `genai-optimization` | `seo-specialist` |
| Documentação | `documentation-templates`, `docs-writer`, `technical-design-doc-creator` | `documentation-writer` |
| Legacy/Refactor | `clean-code`, `coding-guidelines` | `code-archaeologist` + `code-refactorer` |
| Rust | `rust-pro` | (sem agente dedicado, usar expertise inline) |
| Python | `python-patterns` | (sem agente dedicado, usar expertise inline) |
| Scaffolding | `app-builder` (13 templates disponíveis) | (workflow do app-builder) |
| Brainstorm | `brainstorming` | (workflow socrático) |
| Testing | `tdd-workflow`, `testing-patterns`, `e2e-testing-patterns`, `webapp-testing` | `test-engineer` + `qa-automation-engineer` |
| Database | `database-design`, `prisma-expert`, `postgres-optimization` | `database-architect` |
| Marketing/CRO | Ver `./triage-rules-marketing.md` | `marketing-growth-hacker` (The Agency) |
| Mídia Paga | Ver `./triage-rules-marketing.md` | `paid-media-ppc-strategist` (The Agency) |
| Vendas/RevOps | Ver `./triage-rules-marketing.md` | `sales-outbound-strategist` (The Agency) |
