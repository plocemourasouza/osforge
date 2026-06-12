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
