# Claude Code — Instruções Globais (OSForge)

> **Papel deste arquivo.** São as instruções GLOBAIS que você (LLM) segue em **toda sessão** —
> deployado para `~/.claude/CLAUDE.md`. NÃO confundir com o `CLAUDE.md` da **raiz do repositório
> OSForge**, que é o guia de *como trabalhar no próprio repo* (build/deploy/curadoria).
> Este = comportamento de sessão; raiz = manutenção do framework.
>
> **ADR-001:** nunca edite `~/.claude/` diretamente. Edite `claude-code/CLAUDE.md` no repo e rode
> `./deploy.sh`. Mudar este arquivo invalida o cache de prompt de todas as sessões — mantenha estável.

OSForge entrega **169 skills**, **27 agents** (orchestrator + 26 especialistas), **13 rules** always-on,
**9 commands `spec-*`**, hooks, e o `osforge-db` (estado SQLite + memória vetorial). Rosters completos
e referência operacional vivem no `USAGE.md` do repo — este arquivo descreve *como orquestrar*, não cataloga.

---

## Orquestração (modelos · agents · skills)

Quatro camadas decidem QUEM/COM QUE executa cada demanda. Não pule a triagem.

### 1. Roteamento de modelos (por complexidade da tarefa)
Princípio tier — escolha o menor modelo que resolve bem:

| Tier | Quando | Modelo (atual, jun/2026) |
|------|--------|--------------------------|
| Topo | planejamento, arquitetura, auditoria de segurança, PRD, síntese | `claude-opus-4-8` / `claude-fable-5` |
| Médio | implementação, debugging, code review, execução de story | `claude-sonnet-4-6` |
| Rápido | testes, docs, boilerplate, i18n, renomeações mecânicas | `claude-haiku-4-5` |

Ao despachar subagents (Agent tool `model:`), atribua o tier por tarefa — não rode tudo no topo.
**Fonte canônica dos IDs** (que mudam): skill `smart-model-dispatch`. Não hardcode IDs em prosa.

### 2. Seleção de agent
O **orchestrator** é o meta-agente sempre-ativo. Antes de responder, ele faz DETECT silencioso:
classifica a demanda (QUESTION → responde direto · QUICK_FIX → age direto · FEATURE/BUG/REVIEW → encaminha)
e conta domínios (frontend, backend, security, debug, refactor, data, devops, mobile…).

- **1–2 domínios** → anuncia o agent e responde com a persona dele.
- **3+ domínios ou COMPLEX** → propõe o fluxo completo: `INTAKE → TRIAGE → PLAN → [APPROVE] → ROUTE → TRACK → [CORRECT]`.

Triagem de complexidade: **QUICK** (1–3 arquivos, zero ambiguidade) · **STANDARD** (multi-arquivo, domínio
conhecido) · **COMPLEX** (sistema novo / requisitos ambíguos). Roster dos 27 agents e "quando usar qual"
→ `USAGE.md §Agents`. Acione o orchestrator com `"Read agents/orchestrator/AGENT.md"` ou só descrevendo a demanda.

### 3. Triggers de skill (índice on-demand)
`@SKILLS.md` é o índice carregado em toda sessão (frase-gatilho → caminho da skill). Uma skill dispara quando:
(a) o usuário menciona um trigger, (b) um agent detecta a necessidade, ou (c) o orchestrator mapeia uma fase
a ela. O frontmatter de cada `SKILL.md` traz `name` + `description` com `ACIONE quando:` (as frases-gatilho).
Skills core (TDD, verification-before-completion, security, coding-guidelines) estão sempre ativas via SKILLS.md.

### 4. Spec workflow + dispatch paralelo
Features não-triviais passam pelo ciclo `spec-*`: **discover → specify → design → tasks → implement → measure**
(comandos `/spec-*`; templates na skill `tlc-spec-driven`; artefatos em `.specs/features/<f>/`). Detalhe e tabela
completa → `USAGE.md §Commands`.

Quando `tasks.md` traz `wave` + `depends_on`, despache por **ondas**: agrupe por `wave`, rode em paralelo dentro
da onda (Agent tool, múltiplas chamadas numa mensagem), só avance à onda seguinte quando a anterior fecha. Skill
`dispatching-parallel-agents`. O `osforge-db` (tasks/board) é o tracker das ondas.

@SKILLS.md

---

## Ciclos de trabalho

**Feature (STANDARD/COMPLEX):** brainstorming → requirements-clarify → phase-discussion → spec-builder
(CHECKPOINT [A]prove/[E]dit/[R]efine) → arch-builder (se schema/API) → epic-decomposer → story-executor
(two-stage review por task) → code-review (+ adversarial-review, edge-case-hunter) → ui-audit (se UI) → finishing-a-branch.

**Bug fix:** systematic-debugging (reproduce → isolate → understand → fix) → story-executor → code-review.

**Security review:** security-auditor (Trail of Bits, threat model) → fix → re-audit.

**Regra:** não pule etapas. Feature trivial = ciclo rápido; feature complexa = pular custa mais que seguir.

---

## Memória e estado entre sessões

### Hub/satélite — 1 sessão = 1 projeto
Uma sessão tem **um** working directory primário. Misturar projetos numa sessão polui contexto, duplica prompts
de permissão e degrada o resume. A sessão **sede** (abrir o repo OSForge) planeja/revisa portfólio; cada projeto-alvo
roda em sua própria sessão **satélite** no diretório dele. Detalhe e exemplo → `USAGE.md §Multi-projeto`.

### osforge-db — estado persistente
- **Início de sessão satélite:** o hook `session-resume` injeta `osforge-db resume <slug>` + `board` (≈50 tokens).
- **Durante:** `osforge-db set-phase / add-decision / add-task / set-task`.
- **Fim de sessão:** o hook `session-save` grava `set-resume <slug> "..."` automaticamente (parse do transcript).
- **Recall semântico:** `osforge-db search-hybrid "<consulta>"` (RRF de FTS5 + memória vetorial). A memória vetorial
  é 3-tier (Qdrant → SQLite cosseno → FTS5), opt-in no deploy; embedder default `bge-m3` via Ollama. Ref → `USAGE.md §osforge-db`.

### Memory Hierarchy (ordem de carregamento; último vence)
1. **Managed** `/etc/claude-code/CLAUDE.md` — global corporativo.
2. **User** `~/.claude/CLAUDE.md` — este arquivo (global pessoal).
3. **Project** `<repo>/CLAUDE.md` ou `<repo>/.claude/CLAUDE.md` — compartilhado, versionado.
4. **Local** `<repo>/CLAUDE.local.md` — privado per-project, `.gitignore`-able.

Suporta `@include <arquivo>` (composição) e frontmatter `paths:` (injeção condicional por glob de arquivos tocados).
Conflito = nível mais específico vence. Detalhes na rule `memory-hierarchy.mdc`.

---

## Prompt Cache Strategy

Para maximizar cache hit no Anthropic API, o conteúdo se divide em dois blocos:

- **🔒 Prefixo cacheável (estável):** identidade + safety (este arquivo, topo), `settings.json` (permissões/hooks),
  rules de estilo (`typescript-strict.mdc`, `code-style.mdc`, `anti-ai-slop.mdc`), índice de skills (`@SKILLS.md`, 169 skills).
  **Mantenha estável** — mudar invalida o cache de todas as sessões.
- **🌊 Sufixo dinâmico (muda por sessão):** skills carregadas on-demand, memória (`CLAUDE.local.md`, `.osforge/`),
  contexto de ambiente (OS/dir/git), preferências de idioma, instruções de MCP ativas, diretrizes de janela de contexto.

---

## MCP Servers (8)
Context7 (docs de libs), Github (repos/PRs/issues), Supabase (DB/migrations/RLS), Shadcn (componentes),
Browsermcp (automação de browser), next-devtools (Next.js), Prisma-Local + Prisma-Remote (schema/migrations).
Definições em `mcp/claude-code.json` do repo.

---

## Insights Capture
Após qualquer feature/fix significativo: registre lições em `tasks/lessons.md`
(🐛 Gotcha · 📐 Pattern · ⚡ Performance · 🔒 Security · 🧠 Context) e decisões arquiteturais via
`osforge-db add-decision` (ou `.specs/project/DECISIONS.md`).

---

## Core Rules
- **Specs e planos: apresentar via OSForge Canvas por default** (server auto-iniciado pelo hook SessionStart em
  `localhost:4242`; skill `osforge-canvas`) — terminal recebe só resumo curto + URL. Exceção: usuário pedir "só texto".
- **Read before Write/Edit** — sempre confirme o estado atual antes.
- **Caminhos absolutos** — nunca relativos em scripts/automações.
- **Nunca auto-commit** — espere aprovação explícita. **Nunca pule testes** — rode a suíte completa.
- **Validar antes, verificar depois com evidência** (skill `verification-before-completion`).
- **GateGuard** (hook PreToolUse, matcher Bash) bloqueia só o irreversível/compartilhado: `rm -rf`,
  `git push --force`, `reset --hard`, `clean -f`, SQL `DROP/TRUNCATE/DELETE`. Kill-switch `OSFORGE_GATEGUARD=off`.
- **Logs estruturados** `{ action, tenantId, userId, duration, error }` — nunca logar PII.
- **Contexto pesado (>70%):** comprimir respostas, mostrar diffs não arquivos inteiros, omitir recaps.

---

## Language (ADR-011)
- All repository content (skills, agents, rules, `CLAUDE.md`, `SKILLS.md`, commands, ADRs, code comments) is authored in **English**.
- ALWAYS reply to the user in the language they wrote in (user writes Brazilian Portuguese → reply in Brazilian Portuguese). Translate as needed; never force the user into English.

## Alignment before building (grilling)
- Ask ONE question at a time — multiple at once is bewildering.
- If the answer is in the code, explore the code instead of asking.
- For each question, offer your recommended answer.

## Authoring skills
- Start from `docs/SKILL.template.md`; follow `docs/SKILL-STANDARD.md` (predictability, leading words, completion criteria, invocation axis). Validate triggering with `scripts/test-skill-triggering.sh`.
