# DECISIONS.md — Architecture Decision Records
## Agent Skills Framework — Reestruturação v2.0 (2026-02-26)

---

## ADR-001: Repositório como Única Fonte de Verdade

**Status:** Aceito

**Contexto:** Agentes e configurações eram editados diretamente em `~/.claude/` e `~/.cursor/`, causando drift silencioso entre ferramentas e impossibilitando rastreamento de mudanças.

**Decisão:** `agent-skills-consolidado/` é a única fonte de verdade. Nenhum arquivo de configuração é editado diretamente nas ferramentas. Todo deploy ocorre via `deploy.sh`.

**Consequências:** Qualquer mudança em agentes, rules, hooks ou skills exige commit no repositório seguido de `./deploy.sh`. Ganho: rastreabilidade total via git, rollback simples, paridade garantida entre ferramentas.

---

## ADR-002: Eliminação da Camada 3 (Agentes/Skills/Commands Locais em Projetos)

**Status:** Aceito

**Contexto:** Projetos como `proc-perfil`, `linkmetur-webapp` e `mira-manager` tinham agentes, skills e commands locais em `.claude/agents/`, `.claude/skills/` e `.claude/commands/`. Estes duplicavam ou divergiam do global sem ciclo de vida definido.

**Decisão:** Projetos não terão mais Camada 3. O que for valioso sobe para o global. Contexto projeto-específico vai para o `CLAUDE.md` do projeto como texto, não como artefato de framework.

**Exceções:** `settings.local.json` é mantido (configuração do Cursor, fora do escopo). `.specs/` é mantido (artefatos de features, gerados pelo sistema spec).

---

## ADR-003: Unificação do Sistema Spec

**Status:** Aceito

**Contexto:** Dois sistemas coexistiam sem integração: `tlc-spec-driven` (SKILL com templates, estrutura `.specs/`) e `speckit.*` (commands com dependência de scripts bash, estrutura `.specify/`). Ambiguidade sobre qual usar e qual era a fonte de verdade.

**Decisão:** Sistema unificado com dois componentes complementares:
1. `tlc-spec-driven` SKILL — especificação de comportamento e templates canônicos
2. Commands `spec-*` — interface de execução, reescritos sem dependências bash

Os speckit foram renomeados para `spec-*` e reescritos para operar sobre `.specs/` (estrutura do tlc-spec-driven). A pasta `.specify/` e os scripts bash foram eliminados.

**Mapeamento:** speckit.specify→spec-discover, speckit.plan→spec-specify, speckit.tasks→spec-design, speckit.implement→spec-tasks, speckit.analyze→spec-implement, speckit.clarify→spec-clarify, speckit.checklist→spec-checklist, speckit.constitution→spec-constitution. Novo: `spec-measure` (fase 5, ausente nos speckit).

---

## ADR-004: CURSOR-GLOBAL-RULES Migrado para Arquivos .mdc

**Status:** Aceito

**Contexto:** `CURSOR-GLOBAL-RULES-v2.md` (1.341 linhas) continha diretrizes técnicas valiosas mas nunca era carregado pelo Cursor — existia apenas como documento de referência no repositório.

**Decisão:** Conteúdo migrado para 4 arquivos `.mdc` temáticos em `rules/`, que o Cursor carrega automaticamente como global rules. Arquivos originais movidos para `archive/`.

**Arquivos criados:** `nextjs-patterns.mdc`, `security-mindset.mdc`, `agent-skills-reference.mdc`, `product-thinking.mdc`.

---

## ADR-005: Promoção de 4 Agentes da Camada 3 para Global

**Status:** Aceito

**Contexto:** 9 agentes existiam apenas em projetos locais. 5 eram shadcn-específicos (cobertos por `frontend-engineer` + Shadcn MCP). 4 tinham valor genuíno não coberto pelos 7 agentes globais existentes.

**Decisão:** Promover ao global: `code-refactorer`, `git-commit-helper`, `product-strategy-advisor`, `system-architect`. Descartar: os 5 shadcn-específicos e `premium-ux-designer`.

**Critério de promoção:** Valor claro + domínio não coberto pelo global existente + sem referências projeto-específicas.

---

## ADR-006: Hooks com Paths Absolutos

**Status:** Aceito

**Contexto:** `hooks.json` do Cursor usava paths relativos (`hooks/protect-tests.sh`), dependendo do CWD do projeto. Projetos sem pasta `hooks/` local causavam falha silenciosa em todos os hooks.

**Decisão:** `hooks.json` usa `$HOME/.cursor/hooks/` como prefixo absoluto. Scripts são deployados em `~/.cursor/hooks/` pelo `deploy.sh`. Claude Code recebe hooks próprios em `~/.claude/hooks/` via `hooks-claude-code.json` merged em `settings.json`.

---

## ADR-007: Conversão de .cursorrules para CLAUDE.md em Projetos

**Status:** Aceito

**Contexto:** Projetos `members` e `members-app` tinham `.cursorrules` com contexto projeto-específico valiosos (stack, padrões, arquitetura). `.cursorrules` é lido apenas pelo Cursor; `CLAUDE.md` é lido por ambas as ferramentas.

**Decisão:** Converter `.cursorrules` para `CLAUDE.md` estruturado em cada projeto. Remover `.cursorrules` após conversão. Manter toda informação contextual relevante.

---

## ADR-008: Rename spec:* → spec-* (Windows filename compatibility)

**Status:** Aceito

**Contexto:** O caractere `:` é ilegal em nomes de arquivo no sistema de arquivos NTFS (Windows); `git clone` em Windows falhava ao tentar criar os 9 arquivos `commands/spec:*.md`. Adicionalmente, Claude Code reserva `:` como separador de namespace de plugins (e.g. `caveman:cavecrew`) — um arquivo chamado `spec:discover.md` não é acessível via `/spec:discover` como comando slash; o frontmatter `name` não altera a invocação, que é sempre derivada do filename. Subdiretórios com `:` no nome também não são suportados.

**Decisão:** Renomear os 9 arquivos `commands/spec:*.md` para `commands/spec-*.md`. A invocação passa de `/spec:X` para `/spec-X` em todos os documentos, tabelas de comandos e referências textuais. O `deploy.sh` inclui passo idempotente de remoção dos legados (arquivos com `:` no nome) antes do copy, garantindo que instâncias já deployadas fiquem limpas na próxima execução.

**Data:** 2026-06-10.

---

## ADR-009: Reorganização Estrutural — sources/ e Remoção de Peso Morto

**Status:** Aceito

**Contexto:** A raiz do repositório acumulava 30+ entradas misturando produto deployável com material de curadoria: 13 diretórios de fontes upstream (75MB), `_skills/` (73MB de snapshot desatualizado das mesmas fontes), `_taste-skill-source/`, e ~560KB de material morto versionado (`archive/` e `superclaude-backup/` aposentados desde o ADR-004, spec abandonada `scripts/.specs/huly-crm-module/`, `mcp.json` legacy supersedido por `mcp/claude-code.json`, backups e scripts órfãos). `13-claude-red/` estava trackeado no git, inconsistente com a política de fontes gitignored.

**Decisão:**
1. Todas as fontes de curadoria (`01-anthropic` … `13-claude-red`, `_taste-skill-source`) movidas para `sources/` (gitignored — entrada única no `.gitignore`). `13-claude-red` untracked para alinhar com a política.
2. `_skills/` deletado (duplicação pura; regenerável das fontes).
3. Peso morto removido via `git rm` — o histórico git preserva tudo (incl. o conteúdo de `archive/` referenciado pelo ADR-004): `archive/`, `superclaude-backup/`, `scripts/.specs/`, `mcp.json`, `claude-code/SKILLS.md.backup`, `docs/SETUP-REPORT.md`, `outputs/obsidian-fix-prompt.md`, `scripts/hooks-dashboard.sh`, `scripts/install-tier1.sh`.
4. `AGENT_FLOW.md` movido para `docs/`.
5. `scripts/_extract_index.py` ajustado para resolver a coleção-fonte sob o prefixo `sources/`.
6. `.nojekyll` e `osforge-architecture.html` permanecem na raiz (possível GitHub Pages; README linka o HTML).

**Consequência:** Raiz com ~15 entradas — produto (`skills/ agents/ rules/ commands/ hooks/ mcp/ claude-code/ scripts/`), docs, runtime (`outputs/ .osforge/ tests/`) e `sources/`. Os 14 paths lidos pelo `deploy.sh` não mudaram.

**Data:** 2026-06-10.

---

## ADR-010: Backend Vetorial — Qdrant via Docker (3-tier graceful fallback)

**Status:** Aceito

**Contexto:** O `osforge-db` original usava SQLite cosine brute-force para busca vetorial (`vec_memory` table). Com crescimento do banco, brute-force escala O(n). Busca semântica de alta qualidade requer HNSW indexado — padrão da indústria.

**Decisão:** Introduzir Qdrant como tier primário do store vetorial, mantendo SQLite como cache/fallback e FTS5 como tier lexical permanente. Três tiers:

| Tier | Backend | Quando |
|------|---------|--------|
| 1 | **Qdrant** (Docker, HNSW) | `OSFORGE_VECTOR=qdrant` ou `config.json.vector_backend=qdrant` |
| 2 | **SQLite** (cosine brute-force) | default; ou fallback se Qdrant vazio/inalcançável |
| 3 | **off** | `OSFORGE_EMBED=off`; busca degrada para FTS5 lexical |

Regras de fallback:
- Qdrant inalcançável (ConnectionError, timeout): warning para stderr, retorna resultado SQLite — NUNCA crasha.
- Qdrant vazio (0 pontos): transparentemente usa SQLite.
- `vstore_upsert` sempre escreve para AMBOS Qdrant + SQLite (SQLite = cache garantido).

**Primeira dependência de runtime externa** do OSForge (Docker). Por isso:
- Opt-in explícito: `deploy.sh --with-qdrant` ou prompt interativo.
- `deploy.sh --no-qdrant` configura sqlite e imprime aviso de degradação.
- Nenhum arquivo Python novo — Qdrant REST via `urllib` stdlib (zero dependências pip adicionais).
- Imagem pinada: `qdrant/qdrant:v1.18.2`.
- Volume em `~/.osforge/qdrant/storage` (fora do repo, persistente entre deploys).

**Isolamento de config:**
- `OSFORGE_CONFIG` env aponta para config alternativo — testes usam `/tmp`, nunca tocam `~/.osforge/config.json` real.
- Precedência: env vars > `~/.osforge/config.json` > defaults hardcoded.

**Consequências:**
- `osforge-db vec-init` deve ser executado uma vez após Qdrant subir (descobre dim embedando probe string, cria/valida coleção).
- `embed-backfill` popula Qdrant a partir dos registros SQLite existentes.
- Ambientes sem Docker continuam funcionando com SQLite (tier 2) transparentemente.
- Ollama continua sendo o embedder padrão (`embed_provider=ollama`); Qdrant é apenas o store.

**Modelo de embedding padrão — `bge-m3` (revisado após avaliação):**
A primeira escolha (`nomic-embed-text`, 768d) falhou em avaliação empírica com texto técnico curto em PT-BR — 1/3 de acerto top-1, com um documento dominando todas as queries (embeddings anisotrópicos, modelo inglês-cêntrico). `bge-m3` (multilíngue, 1024d) acertou 3/3 com separação saudável. Default do provider ollama passou a `bge-m3`; `nomic-embed-text` fica como alternativa leve (274MB vs 1.2GB) via `OSFORGE_EMBED_MODEL`. A dim é descoberta por `vec-init` (não hardcoded), então trocar de modelo só exige re-`vec-init` + `embed-backfill`.

**Data:** 2026-06-12.

## ADR-011: English Authoring + Reply-in-User-Language + Unified Skill Standard

> From this ADR onward, DECISIONS.md entries are written in English (per the decision below).

**Context.** OSForge content was historically authored largely in pt-BR, with inconsistent skill descriptions — some used `ACIONE quando / Keywords / Não acione para`, others terse English `Use when…` with no negative triggers. Mixed language and inconsistent activation specs hurt **predictability**: how reliably Claude Code picks and executes the right skill in any situation. A review of `mattpocock/skills` (MIT) surfaced complementary strengths worth merging.

**Decision.**
1. **Authoring = English.** All repo content (skills, agents, rules, `CLAUDE.md`, `SKILLS.md`, commands, ADRs, comments) is authored in English. Supersedes the prior "prose largely pt-BR — match that" convention.
2. **Runtime = user's language, via a translation boundary.** The orchestrator (or top-level agent) is the single language boundary: it understands the user's input in their language, transcribes the intent to English, coordinates the entire internal pipeline in English (plans, specs, artifacts, sub-agent/worker prompts, inter-agent messages), and replies to the user in the user's language. Internal scope = English; only the user-facing layer uses the user's language. Encoded in `claude-code/CLAUDE.md` and `agents/orchestrator/AGENT.md`.
3. **Unified skill standard.** Adopt `docs/SKILL-STANDARD.md` + `docs/SKILL.template.md` as single source of truth: activation via `Use when / Keywords / Do NOT use for`; explicit invocation axis (`disable-model-invocation`); execution-routing frontmatter (`model/context/agent/allowed-tools`); canonical body (Iron Law → When NOT to use → numbered steps with checkable "Done when" → anti-patterns → progressive-disclosure references); leading words; failure-mode audit. Merges OSForge's activation/routing strengths with mattpocock/skills' predictability theory (`inspired_by`, MIT).

**Consequences.**
- The pt-BR→English migration of ~142 skills + agents + rules runs in **harness-validated batches** (`scripts/test-skill-triggering.sh`), never a single mega-diff. Order: pilot 3 → engineering/stack → agency → rest.
- **Cross-lingual activation risk:** English descriptions must still fire on pt-BR user prompts (semantic, not lexical, match). Mitigation: triggering test cases MUST include pt-BR prompts.
- `skill-creator` points to the standard; new skills start from the template.
- Third-party adaptations keep `inspired_by`/`source` frontmatter.

**Date:** 2026-06-24.

## ADR-012: Stack Coverage Policy — Context7 for facts, skills for discipline

**Context.** Expanding the supported stack (Better Auth, ASAAS, AWS, Rails, Astro, Vite, etc.) raised the question: do we create a skill/agent per technology, or rely on the Context7 docs MCP? Reflexively creating one skill per tech bloats an already large library (170 skills) and bakes volatile API docs into files that go stale (the `sediment` failure mode).

**Decision.** Context7 and skills are **complementary**, split by what they hold:
1. **Volatile facts (current API, syntax, version-specific behavior) → Context7**, never a skill. Enforced by the existing `context7-docs-first` rule. Skills MUST NOT duplicate API documentation.
2. **Durable discipline (patterns, anti-patterns, gotchas, OSForge conventions, when-to-use) → a lean skill** that explicitly points to Context7 for the API surface.
3. **A whole multi-step role → an agent** (rare; the roster is considered complete).

**Priority rule (coverage):** create a skill only when (a) there is durable opinion/gotchas to encode, OR (b) Context7/model coverage is weak — typically **new or regional** tech (e.g., ASAAS, Better Auth). Well-documented popular libs (Vite, Astro, Express, Jest, Zod) rely on Context7 + existing language skills; no dedicated skill.

**Consequences.**
- A verifiable coverage contract lives in `docs/STACK-COVERAGE.md`: each stack tech → `{skill | Context7 docs-first}`.
- First skills created under this policy: `asaas-integration`, `better-auth`, `aws-deploy` — each lean, each with a "current API → Context7" pointer.
- Triggering for new skills is validated by `scripts/test-skill-triggering.sh`, including pt-BR prompts (cross-lingual, per ADR-011).
- Express stays under `nodejs-best-practices`; pytest/Django/FastAPI/Flask stay under `python-patterns`.

**Date:** 2026-06-25.

## ADR-013: Plan Mode Standard — read-only plan as a parallel-dispatch manifest

**Context.** Claude Code's Plan Mode had no defined standard in OSForge. Plans risked being free-form prose that the agent (or the user) could not turn into autonomous, parallel execution. The goal: a single plan — small or large — that multiple agents can execute in parallel without the user mediating each step.

**Decision.** Plan Mode is the **read-only** half of the orchestrator flow (`DETECT → INTAKE → TRIAGE → PLAN`), stopping at an approval HALT. Its output is a **dispatch manifest**, authored from `docs/PLAN.template.md`, containing: Objective · Feature structure (modules/seams, data model, API) · User stories (US-xx + acceptance criteria) · Roster (models/agents/skills declared up front) · Task manifest · Waves · Risks/rollback · Out of scope · Verification. **Every task carries full metadata** — `story · wave · depends_on · model · agent · skills · files · done-when · verify` — so each is a self-contained worker prompt.

- **Grilling on intake** (one question at a time); triage scales plan depth.
- **Language boundary (ADR-011):** plan authored in English; reply in the user's language.
- **Presentation:** OSForge Canvas by default.
- **Default autonomy: checkpoint per wave** — on approval, dispatch each wave in parallel (`dispatching-parallel-agents`), then stop for review before the next wave. (User may opt into full auto-run or per-task checkpoints.)

**Consequences.**
- Encoded in `rules/plan-mode.mdc` (Cursor) + a Plan Mode section in `claude-code/CLAUDE.md` (Claude Code); template in `docs/PLAN.template.md`.
- The task manifest maps 1:1 to `osforge-db` (`add-task` with existing `wave`/`depends_on` columns) and to `.specs/` artifacts — plan → tracked execution with no re-modeling.
- Rule count rises 13 → 14.

**Date:** 2026-06-25.
