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
2. Commands `spec:*` — interface de execução, reescritos sem dependências bash

Os speckit foram renomeados para `spec:*` e reescritos para operar sobre `.specs/` (estrutura do tlc-spec-driven). A pasta `.specify/` e os scripts bash foram eliminados.

**Mapeamento:** speckit.specify→spec:discover, speckit.plan→spec:specify, speckit.tasks→spec:design, speckit.implement→spec:tasks, speckit.analyze→spec:implement, speckit.clarify→spec:clarify, speckit.checklist→spec:checklist, speckit.constitution→spec:constitution. Novo: `spec:measure` (fase 5, ausente nos speckit).

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
