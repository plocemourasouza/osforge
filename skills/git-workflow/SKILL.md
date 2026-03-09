---
name: git-workflow
description: >
  Git workflow patterns for AI agent development: worktrees for parallel agents,
  branching strategy, commit discipline, and merge workflows.
  Use when creating branches, setting up parallel work, managing merges,
  resolving conflicts, or structuring git operations for agent-driven development.
  Triggers on: git workflow, create branch, parallel features, worktree,
  merge strategy, git setup, branching, git conflict.
metadata:
  author: paulo-cursor-setup
  version: "1.0.0"
---

# Git Workflow para Desenvolvimento com Agentes

## Branching Strategy

### Branch Naming (Conventional)
```
feature/descricao-curta
bugfix/descricao-do-bug
hotfix/correcao-critica
chore/manutencao
refactor/area-refatorada
```

### Workflow Básico
1. Sempre crie branch a partir de `main` (ou `develop` se o projeto usar)
2. Commits pequenos e frequentes (1 mudança lógica por commit)
3. Conventional Commits obrigatório (ver rule commit-conventions)
4. PR com squash merge para main
5. Delete branch após merge

## Git Worktrees — Paralelismo para Agentes

### Quando Usar Worktrees
- Múltiplas features independentes precisam ser implementadas
- Agentes paralelos trabalhando simultaneamente
- Features que tocam arquivos diferentes (sem conflito)

### Quando NÃO Usar Worktrees
- Features dependentes entre si (uma precisa da outra)
- Feature única que toca muitos arquivos
- Trabalho sequencial (uma feature por vez)

### Por Que Worktrees > Branches para Agentes
Branches compartilham o mesmo working directory. Se dois agentes tentam
trabalhar em branches diferentes do mesmo repo, eles pisam nos arquivos
um do outro. Worktrees criam diretórios separados, cada um com seu
working directory isolado.

### Setup de Worktrees

```bash
# 1. A partir do repo principal, criar worktrees
git worktree add ../project-feature-auth feature/auth
git worktree add ../project-feature-dashboard feature/dashboard
git worktree add ../project-feature-api feature/api

# 2. Verificar worktrees ativas
git worktree list

# 3. Cada agente trabalha em seu diretório
# Agente 1 → ../project-feature-auth/
# Agente 2 → ../project-feature-dashboard/
# Agente 3 → ../project-feature-api/

# 4. Após implementação, merge sequencial
cd /path/to/main-repo
git merge feature/auth
git merge feature/dashboard
git merge feature/api

# 5. Cleanup
git worktree remove ../project-feature-auth
git worktree remove ../project-feature-dashboard
git worktree remove ../project-feature-api
```

### Regras para Worktrees com Agentes
- SEMPRE faça commit no worktree antes de tentar merge
- NUNCA delete o worktree sem fazer merge ou confirmar abandono
- Cada worktree deve ter seus próprios `node_modules` (rode `npm install`)
- Resolva conflitos de merge um por vez, do mais simples ao mais complexo
- Após merge de todos, rode testes completos na branch principal

## Commit Discipline para Agentes

### Estrutura de Commits
```
tipo(escopo): descrição curta

- Detalhe 1
- Detalhe 2

Refs: #issue-number (se aplicável)
```

### Frequência
- Commit após cada unidade lógica de trabalho completa
- NUNCA acumule múltiplas features num único commit
- Se o agente implementou algo que funciona, commite imediatamente

### Pre-Commit Checklist
Antes de cada commit, verificar:
1. `npx tsc --noEmit` passa (TypeScript)
2. `npm run lint` passa (ESLint)
3. Nenhum `console.log` de debug
4. Nenhum arquivo `.env` ou secret no staging
5. Testes relevantes passam

O hook `scan-secrets.sh` faz verificação automática de secrets antes do commit.

## Merge & Conflict Resolution

### Estratégia de Merge
- **Feature → main**: Squash merge (histórico limpo)
- **Hotfix → main**: Regular merge (preserva contexto do fix)
- **Worktree merges**: Regular merge (preserva commits individuais)

### Resolução de Conflitos
1. Identifique os arquivos em conflito: `git diff --name-only --diff-filter=U`
2. Para cada arquivo, entenda a intenção de AMBOS os lados
3. Resolva preservando a funcionalidade de ambas as features
4. Rode testes após resolver cada arquivo
5. Commit do merge com mensagem descritiva

### Anti-patterns
- NUNCA use `git merge --strategy=ours` sem revisão (descarta trabalho)
- NUNCA force push em branches compartilhadas
- NUNCA resolva conflitos escolhendo cegamente um lado
- NUNCA faça merge sem rodar testes primeiro

## Integração com Outros Skills e Rules
- **commit-conventions rule**: Formato de commits é enforced globalmente
- **tdd-enforcement rule**: Testes são protegidos durante implementação
- **scan-secrets hook**: Verifica secrets antes de git commit/push
- **validator agent**: Valide contra spec antes de criar PR
- **tlc-spec-driven**: Use STATE.md para tracking entre sessões
