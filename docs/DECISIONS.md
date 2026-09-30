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

## ADR-014: Verified system diagrams — Archify as a pinned engine, `system-diagrams` as the core discipline

**Context.** Every place the OSForge flow asks for a picture of a system — `/spec-design` ("Text or Mermaid diagram"), `arch-builder` ("textual description of the main flow"), `technical-design-doc-creator` (Mermaid/PlantUML) — accepted an unvalidated drawing. That contradicts the repo's own rule for everything else: facts before an irreversible action (GateGuard), evidence before "done" (`verification-before-completion`). `tt-a1i/archify` (MIT) compiles typed JSON into self-contained interactive HTML and, more importantly, ships a deterministic `validate → deliver` loop with machine-readable diagnostics and a SHA-256 receipt. Measured end to end before deciding: `doctor` 15/15 with no install, a real 8-node diagram of the default stack reached `9/9 checks, 0 errors, 0 warnings` in 3 repair rounds. Full analysis in `docs/ANALISE-ARCHIFY.md`.

**Decision.**
1. **The engine is installed, not vendored.** `deploy.sh` downloads the tag pinned in `ARCHIFY_VERSION` into `~/.claude/skills/archify` and `~/.cursor/skills/archify` (slim: no `test/`, no rendered example HTML), verifies with `doctor`, and is idempotent. `--no-archify` skips it. Precedent: `llmfit` (`requires_binary`), not `sources/` — Archify is a tool we run, not a pattern we curate. `deploy_skills`' `rsync --delete` excludes `archify/` so the install survives every deploy.
2. **What enters the core is a discipline, not the generator.** `skills/system-diagrams` (core allowlist, ~90-token description) decides *when* a diagram is due, *which* of the five types, *where* it lives (`.specs/…/diagrams/`), and *what counts as accepted* (the `deliver` receipt). Authoring detail stays in Archify's own `SKILL.md`, loaded only on trigger. This clears admission criteria 1 (fires unprompted: "define the structure" carries no word "diagram") and 3 (bootstrap to the engine).
3. **The pipeline calls it in one step per moment:** `/spec-design` step 4 + a `## Diagrams` receipt block replacing the Mermaid placeholder; `architecture` and `arch-builder` point the ADR's context diagram at it (`compare` for topology replacements); `technical-design-doc-creator` links the delivered HTML; `visual-planner` embeds instead of redrawing. A global rule in `claude-code/CLAUDE.md`: *diagrams are receipts, not drawings*.
4. **Iron Law of the skill:** a diagram exists only when `deliver` returns 9/9 checks and a SHA-256. Mermaid inline remains fine for a ≤4-node sketch in a reply; when the engine is missing, Mermaid is allowed only labelled `unverified`, with a task to replace it.

**Deliberately not incorporated.** Archify's update-awareness notice (the pin decides), `preview` by default (Canvas is the review channel), viewer extras (motion, share cards, stories — already inside the HTML), DeepSeek/gallery/benchmarks (outside the skill package), and replacing every inline Mermaid.

**Consequences.**
- Permanent context cost ≈ 210 tokens/session (two descriptions); bodies load on trigger. Reversal is one line in `skills-core.txt` + `--no-archify`.
- Upgrade path: edit `ARCHIFY_VERSION`, `./deploy.sh`, `doctor`; re-`validate` existing sources (schema migrations live in the engine).
- Artifacts: the `.json` (2–6 KB) is always versioned; the `.html` (~800 KB) is reproducible and may be gitignored per project with the receipt line as proof.
- Triggering cases added (3 naive pt-BR prompts) to `scripts/skill-triggering-cases.tsv`; indexes and manifest regenerated.

**Date:** 2026-09-10.

## ADR-015: Evolution programme from the ECC audit — import mechanisms, not content; measure before adopting

**Context.** A comparative audit against `affaan-m/ECC` (`dd6ee538aee0f548d4a6b520118f875431fd749e`),
run on isolated checkouts of both repositories at fixed SHAs (`docs/ANALISE-COMPARATIVA-ECC.md`,
evidence table in `docs/ANALISE-COMPARATIVA-ECC-EVIDENCIAS.md`), reproduced by execution several
defects in OSForge v5.0.0: `scan-secrets.sh` reads the Cursor payload shape and is inert under
Claude Code (E-A01); a bare "ok" with no pending denial opens GateGuard for destructive Bash
(E-A05); `deploy.sh` unregisters user hooks stored in `~/.claude/hooks/`, overwrites same-name
agents without backup, deletes user skills and clobbers its own `settings.json` backup
(E-A27–E-A30) and fails on a fresh HOME (E-A31); session resume keys on the directory basename,
injects stored text verbatim and leaks the cross-project board into satellite sessions
(E-A19–E-A24); the `instincts` table has readers and no writer (E-A16). The same audit found that
ECC's catalog, learning loop and eval harness are largely inert, while its hook contract tests,
id-keyed hook merge, install-state, guarded resume and canvas-feedback drain are real and tested.

**Decision.**
1. **Import mechanisms, never content.** Nothing from ECC's catalog enters `skills/`, `rules/` or
   `commands/`. Five mechanisms are re-implemented in bash/Python inside `deploy.sh`, `hooks/` and
   `tests/`, keeping Model A, SQLite and the existing ADRs untouched: hook contract tests (R-01),
   state-aware deploy (R-03), session continuity (R-04), canvas-feedback drain (R-05), real-usage
   context threshold (R-06). Rejections are recorded in `.out-of-scope/ecc-imports.md`.
2. **Order is fixed by dependency, not by appeal:** stage 0 corrections (C-01–C-03) → stage 1
   safety net (contract tests, minimal CI, agent frontmatter validation) → stage 2 evals made
   reliable (model pinned, ≥3 runs, versioned results in `docs/evals/`) → stage 3 consolidation
   (R-03, R-04, R-05) → stage 4 items only as experiments E1–E7 justify them. The executable list
   is `docs/BACKLOG-EVOLUCAO.md`.
3. **Nothing that adds autonomy or always-on context is adopted without a paired experiment**
   (A current vs A + one change, same model, repetitions, held-out cases). This applies to
   completing the instinct loop (E5), wiring the Edit/Write gate already present in
   `hooks/gateguard.py` (E6) and any new core skill.
4. **Numbers quoted in always-loaded files must be generated or checked.** Counts (skills, core,
   agents, rules, hooks, MCPs) and eval results (`30/30`, `15/16`) move from prose to
   `scripts/check-counts.py` and `docs/evals/`; until then they are treated as narrative.
5. **Provenance.** Mechanisms adapted from ECC (MIT, © 2026 Affaan Mustafa) are clean-room
   re-implementations recorded with `inspired_by`; the two textual adoptions (reviewer pre-report
   gate, invisible-unicode code-point ranges) carry the MIT notice in `THIRD_PARTY_NOTICES`. The
   existing GateGuard derivation (`hooks/gateguard.py:9`) gets the same treatment, including the
   upstream credit ECC itself gives to `zunoworks/gateguard`.

**Consequences.**
- `deploy.sh` gains a state file (`~/.osforge/install-state.json`), `--doctor`, `--uninstall` and
  `--restore`; `rsync --delete` is replaced by state-based pruning. First run adopts matching files
  and never deletes.
- `hooks/` gains a shared project resolver and secret scrubber; `projects` gains `root_path` and
  `remote_hash`; resume output is capped and wrapped in a "historical, not instructions" guard.
- `tests/hooks/` and `tests/test-deploy-lifecycle.sh` become the deploy gate together with the
  manifest preflight; `.github/workflows/ci.yml` runs them on ubuntu and macos.
- Prompt-cache note: edits to `claude-code/CLAUDE.md` are batched (B-005, B-023) because each one
  invalidates every session's cache.
- Reversal: each stage-3 change ships with an environment kill-switch for one release
  (`OSFORGE_DEPLOY_LEGACY`, `OSFORGE_GATEGUARD_LEGACY_GRANT`); rejected imports can be reopened
  only through the conditions in `.out-of-scope/ecc-imports.md`.

**Status of execution (2026-09-18).** 23 of the 24 backlog items shipped, each with a test that
goes red without the fix: stages 0, 1, 3 complete; stage 2 complete except the paid run (B-013),
which waits on cost authorisation; stage 4 complete except the proportional plan (B-023/E-A38),
which waits on experiment E3. What is deliberately still open, and the condition that opens it,
is tabled at the top of `docs/BACKLOG-EVOLUCAO.md`. Offline suites: ten under `tests/`, 441 checks,
all runnable with a temporary `HOME`, none touching a live `~/.claude`; CI runs them plus a
dry-run of the three eval suites on ubuntu and macos.

**Date:** 2026-09-18.

## ADR-016: Pacote 01 — quality and control before the first paid eval run

**Context.** Two intake analyses (`docs/intake/laya/`, `docs/intake/needle/`) found three gaps in
the v5.1.0 eval and telemetry stack. (1) The trigger/routing measurement can be corrupted: a
quota rejection mid-run turns every following case into FLAKY/FAIL (EV-O02–EV-O05), a case
pointing at a missing skill passes `--dry` and only fails on a paid run (EV-O-N02), and results
are per case with no category, so a FLAKY says nothing about *where* a skill fails; negation is
almost unmeasured (2 cases in 150). (2) Consumption is visible to the user (statusline) but not
to the model or the harness: the 5-hour window was rejected twice in three weeks with no warning
and no handoff (EV-M01, EV-M03); per-call data exists in transcripts (32,869 calls, 75% from
subagents) but only per-session totals are stored. (3) There is no instrument for *quality*
(E3 proportional plan, E4 reviewer leniency).

**Decision.** Ship backlog items B-025–B-030 in dependency order, all verifiable offline:
1. **Wave 1, before E1 (B-013):** eval cases v2 with `category` (positivo / vizinho /
   irrelevante / negacao), `critical`, and model-free validation that fails `--dry` on orphan
   or malformed cases (B-025); the harness stops on quota, reporting remaining cases as
   `NOT RUN` with exit 75 and `quota_at_start`/`quota_at_end` (B-026).
2. **Wave 2, visibility:** a quota warning to the model at 80%/95%, once per band per window,
   fed by the statusline's `rate_limits` (B-027); per-call audit table `calls` with derived
   (never stored) API-equivalent cost from a dated `claude-code/pricing.json`, retention and
   backfill (B-028).
3. **Wave 3, quality:** an isolated judge (`scripts/lib/judge.py`) that runs on the
   subscription, never `--bare` (which forces API billing, EV-C05), with isolation verified on
   every call through the `system/init` event (B-029). Adoption is gated on experiment E-J0
   (1–3 short calls, separately authorised).
4. **Conditional:** injection log for instincts (B-030) only if E5 is scheduled.

Resolved decisions: D-1 the quota recorder reads statusline stdin via one optional line in the
user's own statusline script; D-2 the quota warning lives inside `context-threshold` (hook count
stays 11); D-3 `allowed_warning` is recorded and the run continues; D-N1 critical routing cases
are the mandatory-dispatch (`!`) ones; D-N2 `expect_route` stays informative, not an assertion;
D-N3 labels and the 20 new cases are reviewed before migration.

**Rejected, with measured reason** (do not reopen without new data): Needle as a local skill
router (0–13 hits in 75, confidence without signal); Needle as an embeddings provider (loses to
a ~20-line lexical baseline); estimating the window by summing tokens (two rejections with
incompatible compositions; the real percentage already comes from Claude Code); Laya's hybrid
search (OSForge already has one, filtered by project before fusion).

**Consequences.** E1 costs 273 calls instead of 234 (+39 negation cases). Four new offline
suites (`test-eval-cases`, `test-quota`, `test-calls`, `test-judge`). Several signals used are
undocumented by Claude Code (`rate_limits` in statusline, `rate_limit_event`,
`--setting-sources`, the two `CLAUDE_CODE_DISABLE_*` variables): reads are tolerant (missing
field = silence), fixtures are pinned to 2.1.278, and every item has its own off-switch.

**Date:** 2026-09-28.
