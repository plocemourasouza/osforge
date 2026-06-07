---
name: using-git-worktrees
description: "Setup e uso de git worktrees para desenvolvimento paralelo. ACIONE quando: trabalhar em múltiplas features simultaneamente, precisar de branches isoladas para cada agente paralelo, testar hotfix sem interromper desenvolvimento de feature. Keywords: git worktree, worktrees, parallel development, multiple branches, isolated workspace, branch paralela."
model: sonnet
allowed-tools: Read, Bash, Glob
metadata:
  author: osforge
  version: '1.0'
  source: obra/superpowers (MIT)
  adapted_by: osforge
---

## Estado atual de worktrees
!`git worktree list 2>/dev/null || echo "Git worktrees não disponível ou repositório não inicializado"`
!`git branch -a 2>/dev/null | head -10 || echo "Branches não disponível"`

# Using Git Worktrees

## O que são worktrees?

Git worktrees permitem ter múltiplos checkouts do mesmo repositório em
diretórios diferentes, cada um em uma branch diferente. Ideal para:

- Agents paralelos trabalhando em features independentes ao mesmo tempo
- Testar um hotfix sem commitar/stash o trabalho em progresso
- Code review de uma branch enquanto implementa outra

---

## Setup inicial

### Criar worktree para nova feature

```bash
# Criar branch + worktree em um passo
git worktree add ../meu-projeto-feature-A feature/feature-A

# Ou criar a partir de branch existente
git worktree add ../meu-projeto-hotfix hotfix/bug-123

# Verificar worktrees ativos
git worktree list
```

O diretório `../meu-projeto-feature-A` fica completamente isolado — mudanças lá não afetam o diretório principal.

> ⚠️ **WARNING: uma branch checked-out em um worktree NÃO pode ser usada em outro.** O git bloqueia `git checkout`/`git worktree add` de uma branch que já está ativa em qualquer outro worktree (erro: `fatal: '<branch>' is already checked out at '<path>'`). Planeje uma branch exclusiva por worktree; se precisar da branch em outro lugar, remova o worktree que a está usando primeiro.

### Estrutura recomendada para OSForge + agents paralelos

```
/Users/paulosouza/Development/
├── meu-projeto/               ← main (worktree principal)
├── meu-projeto-feature-A/     ← worktree para Agent 1
├── meu-projeto-feature-B/     ← worktree para Agent 2
└── meu-projeto-hotfix/        ← worktree para hotfix urgente
```

---

## Fluxo com dispatching-parallel-agents

Quando `dispatching-parallel-agents` identifica tasks paralelas:

```bash
# 1. Criar um worktree por task paralela
git worktree add ../projeto-task-api feature/task-api
git worktree add ../projeto-task-ui feature/task-ui
git worktree add ../projeto-task-tests feature/task-tests

# 2. Cada agent trabalha no seu diretório isolado
# Agent 1: cd ../projeto-task-api && implementar
# Agent 2: cd ../projeto-task-ui && implementar
# Agent 3: cd ../projeto-task-tests && implementar

# 3. Após conclusão, fazer merge de cada branch
git checkout main
git merge feature/task-api --no-ff
git merge feature/task-ui --no-ff
git merge feature/task-tests --no-ff

# 4. Limpar worktrees
git worktree remove ../projeto-task-api
git worktree remove ../projeto-task-ui
git worktree remove ../projeto-task-tests
```

---

## Comandos essenciais

```bash
# Listar todos os worktrees
git worktree list

# Criar worktree + nova branch
git worktree add <path> <nova-branch>

# Criar worktree em branch existente
git worktree add <path> <branch-existente>

# Remover worktree (após merge)
git worktree remove <path>

# Forçar remoção (se path já não existe)
git worktree prune

# Mover worktree para outro diretório
git worktree move <path-atual> <novo-path>
```

---

## Setup em cada worktree

Cada worktree é um diretório de projeto completo mas compartilha o `.git` com o principal. O que NÃO é compartilhado:

- `node_modules/` — rodar `bun install` em cada worktree
- `.env` — copiar ou criar `.env.local` em cada worktree
- Processos rodando (dev server, etc.)

```bash
# Em cada novo worktree:
cd ../meu-projeto-feature-A
bun install                    # instalar dependências
cp ..meu-projeto/.env.local .  # copiar variáveis de ambiente
bun dev --port 3001            # porta diferente para não conflitar
```

---

## Gotchas

- **Usar o mesmo porto em múltiplos worktrees**: cada `bun dev` precisa de uma porta diferente (`--port 3001`, `--port 3002`, etc). Portas conflitantes causam erro ao iniciar.
- **Esquecer de rodar `bun install` no worktree novo**: `node_modules` não é compartilhado. Sem instalar, imports falham com erros confusos.
- **Deixar worktrees órfãos**: worktrees não removidos acumulam espaço e confundem `git worktree list`. Sempre remover após merge com `git worktree remove`.
- **Checkout de branch em uso por outro worktree**: git não permite. Se Agent 1 está usando `feature/A`, não é possível fazer `git checkout feature/A` no worktree principal. Solução: criar novo worktree ou remover o existente.
- **Modificar `.git/config` em worktree**: worktrees compartilham configuração git. Mudanças no `.git/config` em um worktree afetam todos. Usar `.git/config.worktree` para configurações locais ao worktree.
- **Não fazer `git worktree prune` após deletar diretório manualmente**: se o diretório do worktree foi deletado sem `git worktree remove`, o git mantém a referência morta. Rodar `git worktree prune` para limpar.
