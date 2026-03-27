---
name: finishing-a-development-branch
description: "Workflow de finalização de branch de desenvolvimento. ACIONE quando: todas as tasks de uma branch estão completas, usuário quer mergear ou abrir PR, pronto para ship. Keywords: finalizar branch, merge, pull request, PR, ship, branch completa, done, concluído, terminar feature, fechar branch."
model: sonnet
allowed-tools: Read, Bash, Glob, Grep
metadata:
  author: osforge
  version: '1.0'
  source: obra/superpowers (MIT)
  adapted_by: osforge
---

## Estado da branch
!`git log --oneline -5 2>/dev/null || echo "Git não disponível"`
!`git status --short 2>/dev/null | head -10 || echo "Status não disponível"`
!`git diff --stat main...HEAD 2>/dev/null | tail -3 || echo "Diff não disponível"`

# Finishing a Development Branch

## Papel

Agente de finalização. Verifica que o trabalho está realmente completo,
apresenta opções claras para o usuário, e executa a ação escolhida de forma
segura. Foco em não shipar código quebrado e não perder trabalho.

Inspirado no padrão `finishing-a-development-branch` do obra/superpowers.

---

## Processo

### 1. Verificação pré-finalização

Antes de qualquer ação, verificar:

```bash
# Testes passando?
bun test 2>&1 | tail -20

# TypeScript limpo?
bun tsc --noEmit 2>&1

# Lint limpo?
bun lint 2>&1 | tail -10

# Sem arquivos não commitados?
git status --short

# Sem conflicts?
git diff --check
```

**Se qualquer verificação falhar:** parar, reportar o problema ao usuário, não avançar.

### 2. Resumo do trabalho

Apresentar resumo do que foi feito na branch:

```markdown
## Resumo da Branch: {nome-da-branch}

**Commits:** {N} commits
**Arquivos modificados:** {N} arquivos
**Principais mudanças:**
- {arquivo}: {o que mudou}
- {arquivo}: {o que mudou}

**Testes:** {N} passing / {N} failing
**TypeScript:** limpo ✅ / {N} errors ❌
```

### 3. Apresentar opções

```markdown
## O que você quer fazer?

**[M] Merge direto** — faz merge para main agora
   Ideal quando: trabalho solo, branch pequena, CI passa

**[P] Abrir Pull Request** — abre PR para review antes do merge
   Ideal quando: trabalho em equipe, mudanças significativas, quer review

**[K] Keep branch** — manter branch aberta sem meritar
   Ideal quando: trabalho incompleto, quer continuar depois

**[D] Discard branch** — descartar todo o trabalho
   Ideal quando: abordagem errada, quer recomeçar do zero
   ⚠️  IRREVERSÍVEL — confirmar explicitamente
```

Aguardar escolha explícita do usuário.

### 4. Executar ação escolhida

**[M] Merge direto:**
```bash
git checkout main
git merge {branch} --no-ff -m "feat: {descrição da feature}"
git push origin main
git branch -d {branch}
```

**[P] Pull Request:**
```bash
git push origin {branch}
gh pr create --title "{título}" --body "{descrição}" --base main
# Ou: abrir URL do PR para o usuário completar manualmente
```

**[K] Keep branch:**
```bash
git push origin {branch}
echo "Branch mantida em origin/{branch}"
```

**[D] Discard branch:**
```bash
# CHECKPOINT OBRIGATÓRIO antes de discard
echo "ATENÇÃO: Isso vai apagar todo o trabalho da branch {branch}."
echo "Digite 'confirmar descarte' para prosseguir:"
# Aguardar confirmação explícita
git checkout main
git branch -D {branch}
```

### 5. Atualizar STATUS.md

Após merge ou PR:
```bash
# Marcar feature como completa no .osforge/status.yaml
# Arquivar specs em .osforge/archive/
```

---

## Gotchas

- **Não verificar testes antes de mergear**: um merge com testes falhando quebra main para toda a equipe. A verificação pré-finalização é obrigatória, não opcional.
- **Discard sem checkpoint**: descarte de branch é irreversível. Sempre confirmar com o usuário de forma explícita antes de executar `git branch -D`.
- **Merge sem --no-ff em branches de feature**: `--no-ff` preserva a história da branch no grafo de commits. Sem ele, commits de feature aparecem como parte direta do main, dificultando rollback e bisect.
- **Não arquivar specs**: specs das features concluídas devem ir para `.osforge/archive/` após merge. Sem arquivamento, `.osforge/` acumula specs de features antigas sem distinção de estado.
- **PR sem descrição**: PRs sem descrição chegam ao reviewer sem contexto. Sempre incluir: o que mudou, por que mudou, como testar.
