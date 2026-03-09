# TOOLS-CONFIG.md
## O que cada ferramenta carrega — Fonte única: agent-skills-consolidado/

**Atualizado automaticamente pelo `deploy.sh`. Não edite manualmente.**

---

## Claude Code (`~/.claude/`)

| Artefato | Origem no Repo | Destino |
|----------|---------------|---------|
| CLAUDE.md | `claude-code/CLAUDE.md` | `~/.claude/CLAUDE.md` |
| SKILLS.md | `claude-code/SKILLS.md` | `~/.claude/SKILLS.md` |
| 11 agentes | `agents/*.md` | `~/.claude/agents/` |
| 9 commands spec:* | `commands/*.md` | `~/.claude/commands/` |
| 3 hook scripts | `hooks/*.sh` | `~/.claude/hooks/` |
| Hooks config | `hooks/hooks-claude-code.json` | merged em `~/.claude/settings.json` |

**MCPs** (configurados em `~/.claude.json`, bloco `mcpServers`):
- Context7, Github, Supabase, Prisma-Local, Prisma-Remote, Shadcn, Browsermcp

**Cadeia de carregamento:**
1. Claude Code lê `~/.claude/CLAUDE.md` ao iniciar sessão global
2. `@SKILLS.md` no CLAUDE.md injeta 26 skills inline (inclui tlc-spec-driven)
3. Agentes são sugeridos proativamente via campo `description` do frontmatter
4. Commands `spec:*` ficam disponíveis via `/` prefix em qualquer sessão
5. Hooks disparam em `PostToolUse` (Write/Edit) e `PreToolUse` (Bash)

---

## Cursor (`~/.cursor/`)

| Artefato | Origem no Repo | Destino |
|----------|---------------|---------|
| SKILLS.md | `claude-code/SKILLS.md` | `~/.cursor/SKILLS.md` |
| 11 agentes | `agents/*.md` | `~/.cursor/agents/` |
| 8 rules .mdc | `rules/*.mdc` | `~/.cursor/rules/` |
| 3 hook scripts | `hooks/*.sh` | `~/.cursor/hooks/` |
| Hooks config | `hooks/hooks.json` | `~/.cursor/hooks.json` |

**MCPs** (configurados no Cursor UI → Settings → MCP):
- Context7, Github, Supabase, Shadcn, Browsermcp

**Rules .mdc carregadas:**
- `typescript-strict.mdc` — TypeScript strict mode (alwaysApply: true)
- `tdd-enforcement.mdc` — Proteção de arquivos de teste (alwaysApply: true)
- `code-style.mdc` — Convenções de código TS/React (alwaysApply: true)
- `commit-conventions.mdc` — Conventional Commits (alwaysApply: true)
- `nextjs-patterns.mdc` — Stack técnica, Next.js 15+, Prisma, shadcn (alwaysApply: true)
- `security-mindset.mdc` — Fail-secure defaults, checklist segurança (alwaysApply: true)
- `agent-skills-reference.mdc` — Referência ao repositório de skills (alwaysApply: true)
- `product-thinking.mdc` — Princípios fundamentais, PDD, planejamento (alwaysApply: true)

**Cadeia de carregamento:**
1. Rules .mdc são injetadas automaticamente no contexto de toda sessão
2. Agentes ficam disponíveis via `@agentname` ou menção explícita
3. Hooks disparam via `hooks.json` com paths absolutos `$HOME/.cursor/hooks/`

---

## Projetos (sem Camada 3)

Projetos **não têm** `.claude/agents/`, `.claude/skills/` ou `.claude/commands/`.

O que projetos **podem ter**:
- `CLAUDE.md` — Contexto específico do projeto (stack, padrões, comandos úteis)
- `settings.local.json` — Configuração do Cursor (model, features)
- `.specs/` — Artefatos de features (gerados pelo sistema spec:*)
- `tasks/todo.md` e `tasks/lessons.md` — Gestão de tarefas e aprendizados

---

## Como Fazer Deploy

```bash
# Sincronizar tudo (repositório → ~/.claude/ e ~/.cursor/)
cd ~/Development/agent-skills-consolidado
./deploy.sh

# Apenas Claude Code
./deploy.sh --claude-only

# Apenas Cursor
./deploy.sh --cursor-only

# Dry run (sem alterações)
./deploy.sh --dry-run
```

---

## Sistema Spec Unificado

```
Interface de execução:  /spec:discover, /spec:specify, /spec:design,
                        /spec:tasks, /spec:implement, /spec:clarify,
                        /spec:checklist, /spec:constitution, /spec:measure

Especificação:          skills/tlc-spec-driven/SKILL.md (via @SKILLS.md)

Estrutura de pastas:    .specs/
                        ├── memory/
                        │   └── constitution.md   (spec:constitution)
                        ├── project/
                        │   ├── PROJECT.md
                        │   ├── STATE.md           (gerenciado manualmente)
                        │   └── DECISIONS.md
                        └── features/
                            └── [feature-name]/
                                ├── discovery.md   (spec:discover)
                                ├── spec.md        (spec:specify)
                                ├── design.md      (spec:design)
                                ├── tasks.md       (spec:tasks)
                                ├── validation.md  (spec:implement)
                                ├── measure.md     (spec:measure)
                                └── checklist.md   (spec:checklist)
```

> **Nota:** `$HOME` em `hooks.json` e `settings.json` é literal intencional.
> Claude Code e Cursor passam o `command` para `/bin/sh -c`, que expande `$HOME`.
> Ferramentas que leiam o JSON diretamente verão o path não expandido — isso é esperado.
