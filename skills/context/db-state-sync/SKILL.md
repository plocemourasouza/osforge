---
name: db-state-sync
description: "Gerencia estado de projetos no banco SQLite local do OSForge (~/.osforge/osforge.db). ACIONE quando: salvar progresso de uma fase, registrar decisão arquitetural, adicionar/resolver blocker, rastrear tasks, ver board cross-project, retomar sessão anterior, buscar decisões passadas. Keywords: salvar estado, registrar decisão, add-decision, set-phase, add-task, set-task, list-tasks, board, resumir sessão, buscar decisão, osforge-db, estado do projeto."
model: haiku
allowed-tools: Bash
metadata:
  author: osforge
  version: '1.1'
---

## Banco disponível
!`osforge-db stats 2>/dev/null || echo "banco não inicializado — rode: osforge-db init"`

# DB State Sync

## Papel

Interface entre o orchestrator e o banco SQLite local do OSForge.
Executa queries via `osforge-db` CLI sem token overhead — toda leitura
de estado retorna apenas o que é necessário.

---

## Banco de dados

Localização padrão: `~/.osforge/osforge.db` (global, cross-project)
Localização local: `.osforge/osforge.db` (por projeto, via `--scope=local`)

`osforge-db` usa Python built-in `sqlite3` — zero dependências externas.

---

## Comandos por situação

### INTAKE — retomar sessão

```bash
# Retorna fase atual + resume point (shell injection compacta, ~50 tokens)
osforge-db resume <slug>

# Retorna estado completo (todas as fases, blockers, decisões recentes)
osforge-db status <slug>

# Listar todos os projetos ativos
osforge-db list-projects
```

**Shell injection no SKILL.md** (usar dentro de qualquer skill de planning):
```
!`osforge-db resume SLUG_DO_PROJETO`
```

### TRACK — atualizar progresso

```bash
# Criar/atualizar projeto
osforge-db upsert-project <slug> "<descrição>" <triage> <status>

# Mudar status de uma fase
osforge-db set-phase <slug> "<nome da fase>" in-progress skills/planning/spec-builder
osforge-db set-phase <slug> "<nome da fase>" complete skills/planning/spec-builder docs/specs/feature.md

# Salvar ponto de retomada (encerrar sessão)
osforge-db set-resume <slug> "<onde parou e próximo passo exato>"
```

### DECISÕES — registrar e buscar

```bash
# Registrar decisão
osforge-db add-decision <slug> "<decisão>" --category=arch
osforge-db add-decision <slug> "<decisão>" --category=product
osforge-db add-decision <slug> "<decisão>" --category=ux
osforge-db add-decision <slug> "<decisão>" --category=data
osforge-db add-decision <slug> "<decisão>" --category=security

# Listar decisões recentes
osforge-db list-decisions <slug> --category=arch --limit=10

# Busca FTS5 cross-project (retorna decisões semanticamente relacionadas)
osforge-db search "Prisma RLS multi-tenant"
osforge-db search "autenticação OAuth" --project=<slug>
```

### TASKS — rastrear tarefas + board cross-project

```bash
# Criar task (status inicial: pending). Flags todas opcionais.
osforge-db add-task <slug> "<título>"
osforge-db add-task <slug> "<título>" --phase="<nome da fase>" --wave=1 --depends=1,2 --priority=p0
# → imprime o id da task criada (ex.: "Task #5 criada")
# --phase resolve por nome (a fase deve existir; crie com set-phase antes)
# --depends é CSV de task ids (texto livre, não validado contra FK)
# --priority: p0 (crítica) | p1 (padrão) | p2

# Atualizar status de uma task
osforge-db set-task <slug> <task_id> in-progress
osforge-db set-task <slug> <task_id> done
# status válidos: pending | in-progress | done | blocked | cancelled

# Listar tasks de um projeto (compacto)
osforge-db list-tasks <slug>
osforge-db list-tasks <slug> --status=in-progress
# formato: [id] status priority wave:N title (deps: ...)

# Board cross-project: tasks de todos os projetos agrupadas por status
osforge-db board                 # default: só projetos status=active
osforge-db board --status=all    # inclui projetos arquivados/inativos
# ordem dos grupos: in-progress → blocked → pending → done (só as 3 últimas)
# projetos sem tasks aparecem como "<slug>: sem tasks"
```

### BLOCKERS — rastrear impedimentos

```bash
# Adicionar blocker
osforge-db add-blocker <slug> "<descrição>" --waiting="<o que está esperando>"

# Listar blockers ativos
osforge-db list-blockers <slug>

# Resolver blocker
osforge-db resolve-blocker <slug> <id>
```

### MIGRAÇÃO — importar status.yaml existente

```bash
# Migra .osforge/status.yaml para o banco
osforge-db import-yaml .osforge/status.yaml <slug>
```

---

## Categorias de decisão

| Categoria | Quando usar |
|---|---|
| `arch` | Decisões de arquitetura e stack (padrão) |
| `product` | Decisões de produto, escopo, prioridade |
| `ux` | Decisões de interface e experiência |
| `data` | Decisões de schema, migrations, dados |
| `security` | Decisões de segurança, auth, LGPD |

---

## Integração com o orchestrator

O orchestrator usa `osforge-db` em dois momentos:

**INTAKE** — ao iniciar sessão:
```bash
# Verificar se há trabalho em progresso
osforge-db list-projects --status=active

# Carregar estado do projeto atual
osforge-db status <slug>
```

**TRACK** — ao completar cada fase:
```bash
osforge-db set-phase <slug> "<fase>" complete <skill-path> <artifact-path>
osforge-db add-decision <slug> "<decisão tomada nessa fase>"
osforge-db set-resume <slug> "Próximo: <fase> via <skill>"
```

---

## Gotchas

- **Slug do projeto**: usar kebab-case consistente. O slug é a chave primária de tudo — `linkme-tur`, `essent-billing`, `rede-essent-portal`. Nunca mudar após criar.
- **FTS5 e hifens**: a busca já sanitiza hifens automaticamente. Não é necessário escapar.
- **Banco global vs local**: para projetos com dados sensíveis (Essent, Rede Essent Jus), usar `--scope=local` — o banco fica no projeto e pode ser `.gitignore`d. O banco global guarda apenas estado e decisões não-sensíveis.
- **set-resume é obrigatório ao encerrar**: sem um `set-resume` atualizado, a próxima sessão não sabe onde parou. Tratar como um commit git — sempre executar antes de fechar o editor.
- **import-yaml é idempotente**: pode ser executado múltiplas vezes no mesmo projeto sem duplicar fases (usa `ON CONFLICT DO NOTHING`).
