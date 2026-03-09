# 🧠 Síntese dos Repositórios de Agent Skills — Consolidado Local

> **Gerado em:** 05/02/2026  
> **Pasta local:** `/Users/paulosouza/Development/agent-skills-consolidado/`  
> **Total de skills:** 1.537 SKILL.md files | ~74MB de conteúdo  
> **Objetivo:** Referência centralizada de todas as skills pesquisadas, com paths locais para instalação e uso.

---

## 📂 Estrutura Local

```
agent-skills-consolidado/
├── 01-anthropic/            (17 skills)   — Skills oficiais Anthropic
├── 02-superpowers/          (14 skills)   — Workflow de dev completo (obra)
├── 03-claude-mem/           (plugin)      — Memória persistente para Claude Code
├── 04-vercel/               (5 skills)    — React, Next.js, Web Design
├── 05-context-engineering/  (18 skills)   — Context engineering (muratcankoylan)
├── 06-antigravity/          (634 skills)  — Coleção universal (sickn33)
├── 07-trailofbits/          (51 skills)   — Segurança e auditoria
├── 08-supabase/             (1 skill)     — PostgreSQL best practices
├── 09-expo/                 (9 skills)    — Mobile Expo/React Native
├── 10-cloudflare/           (8 skills)    — Workers, Agents SDK, Durable Objects
├── 11-sentry/               (13 skills)   — Code review, PRs, workflow dev
├── 12-curadoria/            (referências) — Awesome lists (VoltAgent + travisvn)
└── SINTESE-REPOSITORIOS.md  (este arquivo)
```

---

## 📊 Visão Geral Rápida

| # | Pasta Local | Repositório Original | ⭐ Stars | Licença | Foco |
|---|------------|---------------------|---------|---------|------|
| 1 | `01-anthropic/` | [anthropics/skills](https://github.com/anthropics/skills) | 63.9k | Apache 2.0 / Source-available | Doc, design, dev |
| 2 | `02-superpowers/` | [obra/superpowers](https://github.com/obra/superpowers) | 45.3k | MIT | Workflow TDD + subagents |
| 3 | `03-claude-mem/` | [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem) | 23.3k | AGPL-3.0 | Memória persistente |
| 4 | `04-vercel/` | [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) | 19.1k | MIT | React/Next.js/Deploy |
| 5 | `05-context-engineering/` | [muratcankoylan/Agent-Skills-for-Context-Engineering](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering) | 8.1k | MIT | Context engineering |
| 6 | `06-antigravity/` | [sickn33/antigravity-awesome-skills](https://github.com/sickn33/antigravity-awesome-skills) | 7.4k | MIT | 634+ skills universais |
| 7 | `07-trailofbits/` | [trailofbits/skills](https://github.com/trailofbits/skills) | 2.4k | CC-BY-SA-4.0 | Segurança enterprise |
| 8 | `08-supabase/` | [supabase/agent-skills](https://github.com/supabase/agent-skills) | 1.1k | MIT | PostgreSQL/Supabase |
| 9 | `09-expo/` | [expo/skills](https://github.com/expo/skills) | 878 | MIT | Expo/React Native |
| 10 | `10-cloudflare/` | [cloudflare/skills](https://github.com/cloudflare/skills) | 233 | Apache 2.0 | Cloudflare platform |
| 11 | `11-sentry/` | [getsentry/skills](https://github.com/getsentry/skills) | 173 | Apache 2.0 | Dev workflow interno |
| 12 | `12-curadoria/` | [VoltAgent](https://github.com/VoltAgent/awesome-agent-skills) / [travisvn](https://github.com/travisvn/awesome-claude-skills) | 6.2k / 6.6k | MIT | Listas curadas |
| — | — | [skills.sh](https://skills.sh) | — | — | Leaderboard/diretório |

---

## 🔍 Análise Detalhada por Repositório

---

### 1. 🟣 anthropics/skills — Skills Oficiais Anthropic

**Repo:** https://github.com/anthropics/skills  
**Local:** `01-anthropic/`  
**Stars:** 63.9k | **Licença:** Apache 2.0 (examples) / Source-available (doc skills)

**O que é:** Repositório oficial da Anthropic. Contém as skills de produção que o Claude usa internamente para manipulação de documentos, além de skills de demonstração para design, dev e comunicação.

**Skills disponíveis localmente:**

| Skill | Path Local | Descrição |
|-------|-----------|-----------|
| `docx` | `01-anthropic/docx/` | Criar, editar e analisar Word documents |
| `pdf` | `01-anthropic/pdf/` | Manipulação completa de PDFs |
| `pptx` | `01-anthropic/pptx/` | PowerPoint presentations |
| `xlsx` | `01-anthropic/xlsx/` | Excel spreadsheets |
| `frontend-design` | `01-anthropic/frontend-design/` | Design de UI anti-"AI slop" |
| `algorithmic-art` | `01-anthropic/algorithmic-art/` | Arte generativa com p5.js |
| `canvas-design` | `01-anthropic/canvas-design/` | Design visual em PNG/PDF |
| `web-artifacts-builder` | `01-anthropic/web-artifacts-builder/` | Artefatos HTML com React + Tailwind |
| `mcp-builder` | `01-anthropic/mcp-builder/` | Criar MCP servers |
| `webapp-testing` | `01-anthropic/webapp-testing/` | Testes com Playwright |
| `brand-guidelines` | `01-anthropic/brand-guidelines/` | Brand colors Anthropic |
| `internal-comms` | `01-anthropic/internal-comms/` | Status reports, newsletters |
| `doc-coauthoring` | `01-anthropic/doc-coauthoring/` | Co-autoria de documentos |
| `skill-creator` | `01-anthropic/skill-creator/` | Guia para criar novas skills |
| `theme-factory` | `01-anthropic/theme-factory/` | Temas profissionais |
| `slack-gif-creator` | `01-anthropic/slack-gif-creator/` | GIFs para Slack |

**Extras locais:**
- `01-anthropic/_template/` — Template para criar novas skills
- `01-anthropic/_spec/` — Especificação do Agent Skills standard

**Instalação via plugin (online):**
```bash
/plugin marketplace add anthropics/skills
/plugin install document-skills@anthropic-agent-skills
/plugin install example-skills@anthropic-agent-skills
```

**Instalação local (copiar para projeto):**
```bash
# Copiar skill específica para seu projeto
cp -R ~/Development/agent-skills-consolidado/01-anthropic/frontend-design .claude/skills/

# Ou copiar todas
cp -R ~/Development/agent-skills-consolidado/01-anthropic/* .claude/skills/
```

**Relevância:** ⭐⭐⭐⭐⭐

---

### 2. 🔵 obra/superpowers — Framework de Desenvolvimento

**Repo:** https://github.com/obra/superpowers  
**Local:** `02-superpowers/`  
**Stars:** 45.3k | **Licença:** MIT

**O que é:** Framework completo de workflow de software que transforma o coding agent num engenheiro senior com processos estruturados: brainstorming → planejamento → TDD → code review → merge.

**Skills disponíveis localmente:**

| Skill | Path Local | Fase | Descrição |
|-------|-----------|------|-----------|
| `brainstorming` | `02-superpowers/brainstorming/` | Design | Refinamento socrático de ideias |
| `writing-plans` | `02-superpowers/writing-plans/` | Planning | Tarefas de 2-5 min com paths exatos |
| `executing-plans` | `02-superpowers/executing-plans/` | Execution | Execução em batches com checkpoints |
| `subagent-driven-development` | `02-superpowers/subagent-driven-development/` | Execution | Subagente por tarefa com review 2-stage |
| `test-driven-development` | `02-superpowers/test-driven-development/` | Implementation | RED-GREEN-REFACTOR obrigatório |
| `systematic-debugging` | `02-superpowers/systematic-debugging/` | Debug | 4-phase root cause process |
| `verification-before-completion` | `02-superpowers/verification-before-completion/` | QA | Verificação antes de declarar pronto |
| `using-git-worktrees` | `02-superpowers/using-git-worktrees/` | Git | Workspace isolado em branch |
| `dispatching-parallel-agents` | `02-superpowers/dispatching-parallel-agents/` | Orchestration | Subagentes concorrentes |
| `requesting-code-review` | `02-superpowers/requesting-code-review/` | Review | Checklist pré-review |
| `receiving-code-review` | `02-superpowers/receiving-code-review/` | Review | Responder a feedback |
| `finishing-a-development-branch` | `02-superpowers/finishing-a-development-branch/` | Completion | Merge/PR/cleanup |
| `using-superpowers` | `02-superpowers/using-superpowers/` | Meta | Introdução ao sistema |
| `writing-skills` | `02-superpowers/writing-skills/` | Meta | Criar novas skills |

**Extras locais:**
- `02-superpowers/_commands/` — Slash commands
- `02-superpowers/_agents/` — Subagent definitions
- `02-superpowers/_hooks/` — Lifecycle hooks
- `02-superpowers/_docs/` — Documentação

**Instalação via plugin (online):**
```bash
/plugin marketplace add obra/superpowers-marketplace
/plugin install superpowers@superpowers-marketplace
```

**Instalação local:**
```bash
cp -R ~/Development/agent-skills-consolidado/02-superpowers/* .claude/skills/
```

**Relevância:** ⭐⭐⭐⭐⭐

---

### 3. 🧠 thedotmack/claude-mem — Memória Persistente

**Repo:** https://github.com/thedotmack/claude-mem  
**Local:** `03-claude-mem/`  
**Stars:** 23.3k | **Licença:** AGPL-3.0

**O que é:** Sistema de memória persistente e compressão de contexto. Captura automaticamente o que Claude faz, gera resumos semânticos e injeta contexto relevante em sessões futuras. **Não é uma skill convencional — é um plugin completo.**

**Conteúdo local:**
- `03-claude-mem/` — Plugin structure (commands, hooks, modes, scripts, ui)
- `03-claude-mem/_src/` — Source code do worker service
- `03-claude-mem/_docs/` — Documentação completa
- `03-claude-mem/_ragtime/` — RAG engine (licença separada: PolyForm Noncommercial)

**Features:**
- 🧠 Memória persistente entre sessões via SQLite + Chroma vector DB
- 📊 Progressive disclosure com custo de tokens visível
- 🔍 4 MCP tools: `search`, `timeline`, `get_observations`, `__IMPORTANT`
- 🖥️ Web Viewer em `http://localhost:37777`
- 🔒 Tags `<private>` para excluir conteúdo sensível

**Requisitos:** Node.js 18+, Bun (auto-install), uv (auto-install)

**Instalação (apenas online — requer npm):**
```bash
/plugin marketplace add thedotmack/claude-mem
/plugin install claude-mem
```

**Nota:** O conteúdo local serve como referência e estudo. A instalação funcional requer o plugin marketplace para registrar os hooks corretamente.

**Relevância:** ⭐⭐⭐⭐⭐

---

### 4. 🟢 vercel-labs/agent-skills — React & Next.js

**Repo:** https://github.com/vercel-labs/agent-skills  
**Local:** `04-vercel/`  
**Stars:** 19.1k | **Licença:** MIT

**O que é:** Skills oficiais da Vercel Engineering. A `react-best-practices` é a skill mais instalada do ecossistema (96.5k installs no skills.sh).

**Skills disponíveis localmente:**

| Skill | Path Local | Descrição |
|-------|-----------|-----------|
| `react-best-practices` | `04-vercel/react-best-practices/` | 40+ regras em 8 categorias (waterfalls, bundle, SSR, re-renders) |
| `web-design-guidelines` | `04-vercel/web-design-guidelines/` | 100+ regras de accessibility, performance, UX |
| `composition-patterns` | `04-vercel/composition-patterns/` | Compound components, state lifting |
| `react-native-skills` | `04-vercel/react-native-skills/` | 16 regras para mobile (FlashList, Reanimated) |
| `claude.ai` | `04-vercel/claude.ai/` | Deploy claimable para Vercel |

**Instalação local:**
```bash
cp -R ~/Development/agent-skills-consolidado/04-vercel/react-best-practices .claude/skills/
cp -R ~/Development/agent-skills-consolidado/04-vercel/web-design-guidelines .claude/skills/
```

**Instalação via npx (online):**
```bash
npx skills add vercel-labs/agent-skills
```

**Relevância:** ⭐⭐⭐⭐⭐

---

### 5. 📐 muratcankoylan/Agent-Skills-for-Context-Engineering

**Repo:** https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering  
**Local:** `05-context-engineering/`  
**Stars:** 8.1k | **Licença:** MIT

**O que é:** Skills focadas em context engineering — a disciplina de gerenciar o context window do LLM. Citado em pesquisa da Peking University.

**Skills disponíveis localmente:**

| Categoria | Skill | Path Local |
|-----------|-------|-----------|
| Fundamentos | `context-fundamentals` | `05-context-engineering/context-fundamentals/` |
| Fundamentos | `context-degradation` | `05-context-engineering/context-degradation/` |
| Fundamentos | `context-compression` | `05-context-engineering/context-compression/` |
| Arquitetura | `multi-agent-patterns` | `05-context-engineering/multi-agent-patterns/` |
| Arquitetura | `memory-systems` | `05-context-engineering/memory-systems/` |
| Arquitetura | `tool-design` | `05-context-engineering/tool-design/` |
| Arquitetura | `filesystem-context` | `05-context-engineering/filesystem-context/` |
| Arquitetura | `hosted-agents` | `05-context-engineering/hosted-agents/` |
| Operacional | `context-optimization` | `05-context-engineering/context-optimization/` |
| Operacional | `evaluation` | `05-context-engineering/evaluation/` |
| Operacional | `advanced-evaluation` | `05-context-engineering/advanced-evaluation/` |
| Metodologia | `project-development` | `05-context-engineering/project-development/` |
| Cognitivo | `bdi-mental-states` | `05-context-engineering/bdi-mental-states/` |

**Extras locais:**
- `05-context-engineering/_examples/` — digital-brain, x-to-book, llm-as-judge, book-sft-pipeline
- `05-context-engineering/_template/` — Template de skill
- `05-context-engineering/_researcher/` — Researcher agent

**Instalação local:**
```bash
cp -R ~/Development/agent-skills-consolidado/05-context-engineering/context-fundamentals .claude/skills/
```

**Instalação via plugin (online):**
```bash
/plugin marketplace add muratcankoylan/Agent-Skills-for-Context-Engineering
/plugin install context-engineering-fundamentals@context-engineering-marketplace
```

**Relevância:** ⭐⭐⭐⭐

---

### 6. 🌌 sickn33/antigravity-awesome-skills — Coleção Universal (634 skills)

**Repo:** https://github.com/sickn33/antigravity-awesome-skills  
**Local:** `06-antigravity/`  
**Stars:** 7.4k | **Licença:** MIT

**O que é:** A maior coleção agregada. 634 skills universais compatíveis com Claude Code, Gemini CLI, Codex CLI, Cursor, GitHub Copilot, OpenCode e AdaL. Inclui skills de repositórios oficiais como symlinks/cópias.

**Categorias (634 skills):**

| Categoria | Qtd | Exemplos |
|-----------|-----|----------|
| Security | 107 | api-security, sql-injection-testing, vulnerability-scanner |
| General | 95 | brainstorming, doc-coauthoring, writing-plans |
| Data & AI | 81 | rag-engineer, prompt-engineer, langgraph |
| Development | 72 | typescript-expert, python-patterns, react-patterns |
| Infrastructure | 72 | docker-expert, aws-serverless, vercel-deployment |
| Architecture | 52 | architecture, c4-context, senior-architect |
| Business | 35 | copywriting, pricing-strategy, seo-audit |
| Testing | 21 | TDD, testing-patterns, test-fixing |
| Workflow | 17 | workflow-automation, inngest, trigger-dev |

**Índice completo:** `06-antigravity/CATALOG.md` e `06-antigravity/skills_index.json`

**Instalação local (skill específica):**
```bash
# Consulte o CATALOG.md para encontrar a skill
cp -R ~/Development/agent-skills-consolidado/06-antigravity/typescript-expert .claude/skills/
```

**Instalação via npx (online — todas):**
```bash
npx antigravity-awesome-skills --claude
```

**⚠️ Nota:** Muitas skills aqui são cópias/derivações de repos oficiais (anthropic, vercel, trailofbits, etc.). Para skills que existem nas pastas 01-11, prefira usar a versão do repo original.

**Relevância:** ⭐⭐⭐⭐ (cherry-pick)

---

### 7. 🔒 trailofbits/skills — Segurança & Auditoria

**Repo:** https://github.com/trailofbits/skills  
**Local:** `07-trailofbits/`  
**Stars:** 2.4k | **Licença:** CC-BY-SA-4.0

**O que é:** Skills de segurança da Trail of Bits, uma das empresas de segurança mais respeitadas. Já encontrou bugs reais em produção.

**Skills por categoria:**

| Categoria | Skills Locais |
|-----------|--------------|
| **Smart Contracts** | `07-trailofbits/building-secure-contracts/`, `entry-point-analyzer/`, `algorand-vulnerability-scanner/`, `ton-vulnerability-scanner/`, `cairo-vulnerability-scanner/`, `solana-vulnerability-scanner/`, `cosmos-vulnerability-scanner/`, `substrate-vulnerability-scanner/`, `token-integration-analyzer/` |
| **Code Auditing** | `07-trailofbits/audit-context-building/`, `differential-review/`, `semgrep-rule-creator/`, `semgrep-rule-variant-creator/`, `static-analysis/` (CodeQL+Semgrep+SARIF), `variant-analysis/`, `sharp-edges/`, `insecure-defaults/`, `burpsuite-project-parser/` |
| **Testing** | `07-trailofbits/testing-handbook-*/` (fuzzers, sanitizers, coverage), `property-based-testing/`, `constant-time-analysis/` |
| **Compliance** | `07-trailofbits/spec-to-code-compliance/`, `fix-review/`, `audit-prep-assistant/`, `code-maturity-assessor/` |
| **Malware** | `07-trailofbits/yara-rule-authoring/` |
| **Mobile** | `07-trailofbits/firebase-apk-scanner/` |
| **Reverse Eng.** | `07-trailofbits/dwarf-expert/` |
| **Dev** | `07-trailofbits/modern-python/`, `ask-questions-if-underspecified/` |

**Instalação via plugin (online):**
```bash
/plugin marketplace add trailofbits/skills
```

**Instalação local:**
```bash
cp -R ~/Development/agent-skills-consolidado/07-trailofbits/static-analysis .claude/skills/
cp -R ~/Development/agent-skills-consolidado/07-trailofbits/insecure-defaults .claude/skills/
```

**Relevância:** ⭐⭐⭐⭐⭐

---

### 8. 🟩 supabase/agent-skills — PostgreSQL Best Practices

**Repo:** https://github.com/supabase/agent-skills  
**Local:** `08-supabase/`  
**Stars:** 1.1k | **Licença:** MIT

**O que é:** Skill oficial da Supabase para otimização de PostgreSQL.

**Skill disponível:**
| Skill | Path Local | Descrição |
|-------|-----------|-----------|
| `supabase-postgres-best-practices` | `08-supabase/supabase-postgres-best-practices/` | Query optimization, schema review, indexes |

**Instalação local:**
```bash
cp -R ~/Development/agent-skills-consolidado/08-supabase/supabase-postgres-best-practices .claude/skills/
```

**Instalação via npx (online):**
```bash
npx skills add supabase/agent-skills
```

**Relevância:** ⭐⭐⭐⭐ (essencial para o stack Supabase + Prisma)

---

### 9. 📱 expo/skills — Mobile Expo/React Native

**Repo:** https://github.com/expo/skills  
**Local:** `09-expo/`  
**Stars:** 878 | **Licença:** MIT

**O que é:** Skills oficiais do time Expo, otimizadas para modelos Opus.

**Skills disponíveis:**

| Skill | Path Local | Descrição |
|-------|-----------|-----------|
| `expo-app-design` | `09-expo/expo-app-design/` | Design e build de apps Expo |
| `expo-deployment` | `09-expo/expo-deployment/` | Deploy para produção |
| `upgrading-expo` | `09-expo/upgrading-expo/` | Upgrade de SDK |

**Instalação local:**
```bash
cp -R ~/Development/agent-skills-consolidado/09-expo/expo-app-design .claude/skills/
```

**Relevância:** ⭐⭐⭐

---

### 10. ☁️ cloudflare/skills — Cloudflare Platform

**Repo:** https://github.com/cloudflare/skills  
**Local:** `10-cloudflare/`  
**Stars:** 233 | **Licença:** Apache 2.0

**O que é:** Skills oficiais para desenvolvimento na plataforma Cloudflare.

**Skills disponíveis:**

| Skill | Path Local | Descrição |
|-------|-----------|-----------|
| `cloudflare` | `10-cloudflare/cloudflare/` | Platform-wide: Workers, Pages, KV, D1, R2, AI, WAF |
| `agents-sdk` | `10-cloudflare/agents-sdk/` | Agents com state, scheduling, RPC, MCP |
| `durable-objects` | `10-cloudflare/durable-objects/` | Coordenação stateful com SQLite |
| `sandbox-sdk` | `10-cloudflare/sandbox-sdk/` | Execução segura de código |
| `wrangler` | `10-cloudflare/wrangler/` | Deploy e gestão de Workers |
| `web-perf` | `10-cloudflare/web-perf/` | Core Web Vitals audit |
| `building-mcp-server-on-cloudflare` | `10-cloudflare/building-mcp-server-on-cloudflare/` | MCP servers com OAuth |
| `building-ai-agent-on-cloudflare` | `10-cloudflare/building-ai-agent-on-cloudflare/` | AI agents com WebSockets |

**Extras locais:**
- `10-cloudflare/_commands/` — Slash commands (`/cloudflare:build-agent`, `/cloudflare:build-mcp`)
- `10-cloudflare/_rules/` — Cursor rules

**Instalação local:**
```bash
cp -R ~/Development/agent-skills-consolidado/10-cloudflare/cloudflare .claude/skills/
```

**Relevância:** ⭐⭐⭐ (útil se usar Cloudflare R2/Workers)

---

### 11. 🔴 getsentry/skills — Dev Workflow da Sentry

**Repo:** https://github.com/getsentry/skills  
**Local:** `11-sentry/`  
**Stars:** 173 | **Licença:** Apache 2.0

**O que é:** Skills usadas internamente pelo time da Sentry. Bom referencial de como um time real organiza skills.

**Skills disponíveis:**

| Skill | Path Local | Descrição |
|-------|-----------|-----------|
| `code-review` | `11-sentry/code-review/` | Code review guidelines |
| `commit` | `11-sentry/commit/` | Commit message conventions |
| `create-pr` | `11-sentry/create-pr/` | PR creation workflow |
| `find-bugs` | `11-sentry/find-bugs/` | Bug + vulnerability detection |
| `iterate-pr` | `11-sentry/iterate-pr/` | Iterate até CI pass |
| `claude-settings-audit` | `11-sentry/claude-settings-audit/` | Audit de settings Claude Code |
| `agents-md` | `11-sentry/agents-md/` | Manter AGENTS.md |
| `brand-guidelines` | `11-sentry/brand-guidelines/` | Copy guidelines Sentry |
| `doc-coauthoring` | `11-sentry/doc-coauthoring/` | Co-autoria de docs |
| `security-review` | `11-sentry/security-review/` | Security review OWASP |
| `code-simplifier` | `11-sentry/code-simplifier/` | Simplificar código |
| `django-access-review` | `11-sentry/django-access-review/` | Django access patterns |
| `django-perf-review` | `11-sentry/django-perf-review/` | Django performance |

**Extras:** `11-sentry/_agents/` — Subagent definitions

**Instalação local:**
```bash
cp -R ~/Development/agent-skills-consolidado/11-sentry/code-review .claude/skills/
cp -R ~/Development/agent-skills-consolidado/11-sentry/security-review .claude/skills/
```

**Relevância:** ⭐⭐⭐

---

### 12. 📋 Curadoria — Awesome Lists

**Local:** `12-curadoria/`

Contém os READMEs das duas maiores listas curadas como referência:

| Arquivo | Origem | Descrição |
|---------|--------|-----------|
| `VOLTAGENT-awesome-agent-skills.md` | [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills) (6.2k ⭐) | Lista organizada por times oficiais (Google Labs, Hugging Face, Stripe, HashiCorp, WordPress, fal.ai, etc.) |
| `TRAVISVN-awesome-claude-skills.md` | [travisvn/awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills) (6.6k ⭐) | Guia completo com tutoriais, comparativos Skills vs MCP vs Prompts, timeline de updates |

**Uso:** Consulte estes arquivos para descobrir skills de times que não estão nos repos anteriores (ex: Stripe, Hugging Face, WordPress, HashiCorp).

---

### 🌐 skills.sh — Diretório Online

**URL:** https://skills.sh  
**CLI:** `npx skills add <owner/repo>`

Leaderboard de instalações. Top 5:
1. `find-skills` (Vercel) — 119.8k
2. `vercel-react-best-practices` — 96.5k
3. `web-design-guidelines` — 73.1k
4. `remotion-best-practices` — 68.2k
5. `frontend-design` (Anthropic) — 41.5k

---

## 🎯 Prioridades de Instalação para o Time

### Tier 1 — Instalar Imediatamente

| Pasta | Motivo | Comando Local |
|-------|--------|---------------|
| `01-anthropic/` | Document skills production-grade | `cp -R 01-anthropic/{frontend-design,docx,pdf,xlsx,pptx,mcp-builder} .claude/skills/` |
| `02-superpowers/` | Workflow de dev completo com TDD | `cp -R 02-superpowers/* .claude/skills/` |
| `03-claude-mem/` | Memória persistente (game-changer) | `/plugin marketplace add thedotmack/claude-mem` |
| `04-vercel/` | Stack do time é React/Next.js | `cp -R 04-vercel/{react-best-practices,web-design-guidelines} .claude/skills/` |
| `08-supabase/` | Stack do time usa Supabase | `cp -R 08-supabase/* .claude/skills/` |
| `07-trailofbits/` | Segurança nunca é opcional | `cp -R 07-trailofbits/{static-analysis,insecure-defaults,security-review} .claude/skills/` |

### Tier 2 — Avaliar e Instalar Seletivamente

| Pasta | Motivo | Skills Sugeridas |
|-------|--------|-----------------|
| `05-context-engineering/` | Otimizar como agents usam contexto | `context-fundamentals`, `context-optimization`, `multi-agent-patterns` |
| `10-cloudflare/` | Se usar Cloudflare R2/Workers | `cloudflare`, `wrangler` |
| `11-sentry/` | Referência de workflow de time | `code-review`, `commit`, `create-pr` |

### Tier 3 — Cherry-Pick da Antigravity

| Skills da `06-antigravity/` | Para quê |
|-----------------------------|----------|
| `typescript-expert` | Regras avançadas de TS |
| `prisma-patterns` | Patterns de Prisma ORM |
| `docker-expert` | Containerização |
| `aws-serverless` | Se usar AWS |
| `architecture` | Design de sistemas |
| `senior-architect` | Decisões arquiteturais |

**Consulte o catálogo completo em:** `06-antigravity/CATALOG.md`

---

## 🔧 Script de Instalação Rápida (Tier 1)

```bash
#!/bin/bash
# Instalar skills Tier 1 num projeto
# Uso: bash install-tier1.sh /caminho/do/projeto

PROJECT_DIR="${1:-.}"
SKILLS_BASE="$HOME/Development/agent-skills-consolidado"
TARGET="$PROJECT_DIR/.claude/skills"

mkdir -p "$TARGET"

echo "📦 Instalando Anthropic (core)..."
cp -R "$SKILLS_BASE/01-anthropic/frontend-design" "$TARGET/"
cp -R "$SKILLS_BASE/01-anthropic/docx" "$TARGET/"
cp -R "$SKILLS_BASE/01-anthropic/pdf" "$TARGET/"
cp -R "$SKILLS_BASE/01-anthropic/xlsx" "$TARGET/"
cp -R "$SKILLS_BASE/01-anthropic/pptx" "$TARGET/"
cp -R "$SKILLS_BASE/01-anthropic/mcp-builder" "$TARGET/"
cp -R "$SKILLS_BASE/01-anthropic/skill-creator" "$TARGET/"

echo "🔵 Instalando Superpowers (workflow)..."
for skill in brainstorming writing-plans executing-plans test-driven-development systematic-debugging subagent-driven-development requesting-code-review verification-before-completion using-git-worktrees; do
    cp -R "$SKILLS_BASE/02-superpowers/$skill" "$TARGET/" 2>/dev/null
done

echo "🟢 Instalando Vercel (React/Next.js)..."
cp -R "$SKILLS_BASE/04-vercel/react-best-practices" "$TARGET/"
cp -R "$SKILLS_BASE/04-vercel/web-design-guidelines" "$TARGET/"
cp -R "$SKILLS_BASE/04-vercel/composition-patterns" "$TARGET/"

echo "🟩 Instalando Supabase (PostgreSQL)..."
cp -R "$SKILLS_BASE/08-supabase/supabase-postgres-best-practices" "$TARGET/"

echo "🔒 Instalando Trail of Bits (segurança)..."
cp -R "$SKILLS_BASE/07-trailofbits/static-analysis" "$TARGET/" 2>/dev/null
cp -R "$SKILLS_BASE/07-trailofbits/insecure-defaults" "$TARGET/" 2>/dev/null
cp -R "$SKILLS_BASE/07-trailofbits/sharp-edges" "$TARGET/" 2>/dev/null

echo "✅ Instalação Tier 1 completa em $TARGET"
echo "📊 Skills instaladas:"
ls "$TARGET" | wc -l
```

---

## ⚠️ Notas Importantes

1. **Sobreposição:** A pasta `06-antigravity/` contém cópias de skills de outros repos (anthropic, vercel, trailofbits, etc.). Sempre prefira a versão do repo original (pastas 01-11).

2. **Licenças:** Respeite as licenças de cada repo ao usar em projetos comerciais:
   - MIT: livre para uso comercial (superpowers, vercel, muratcankoylan, antigravity, expo, sentry)
   - Apache 2.0: livre com atribuição (anthropic examples, cloudflare, sentry)
   - Source-available: as doc skills da Anthropic (docx/pdf/pptx/xlsx) são para referência
   - CC-BY-SA-4.0: Trail of Bits requer atribuição + share-alike
   - AGPL-3.0: Claude-mem requer código fonte aberto se deployar como serviço

3. **Claude-Mem:** Requer instalação via plugin marketplace (não funciona apenas copiando). O conteúdo local serve como documentação.

4. **Atualização:** Para atualizar as skills, basta re-clonar os repos ou usar `git pull` nos originais.

---

*Documento gerado por Claude Opus 4.6 — consolidação de 13 repositórios com 1.537 SKILL.md files.*
