---
name: receiving-code-review
description: "Como responder ao feedback de um code review. ACIONE quando: recebeu feedback de review, PR tem comments, revisor pediu mudanças, CHANGES_REQUESTED. Keywords: responder review, feedback de review, changes requested, responder PR, tratar comments, resolver feedback, revisor pediu mudanças."
model: sonnet
allowed-tools: Read, Bash, Glob, Grep, Write, Edit
metadata:
  author: osforge
  version: '1.0'
  source: obra/superpowers (MIT)
  adapted_by: osforge
---

## Estado do PR
!`git log --oneline -3 2>/dev/null || echo "Git não disponível"`
!`git diff --stat HEAD~1 2>/dev/null | tail -5 || echo "Diff não disponível"`

# Receiving Code Review

## Papel

Agente de resposta a review. Processa feedback de forma sistemática,
distingue entre mudanças obrigatórias e sugestões opcionais, e implementa
as correções necessárias sem perder rastreabilidade.

Inspirado no padrão `receiving-code-review` do obra/superpowers.

---

## Processo

### 1. Catalogar o feedback

Estruturar todos os comments recebidos:

```markdown
## Feedback Catalogado

### Bloqueantes (MUST fix antes do merge)
1. **{arquivo}:{linha}** — {problema} → {ação necessária}
2. **{arquivo}:{linha}** — {problema} → {ação necessária}

### Importantes (SHOULD fix — melhora qualidade)
3. **{arquivo}:{linha}** — {sugestão} → {ação sugerida}

### Opcionais (NICE to have — considerar)
4. **{arquivo}:{linha}** — {observação} → {ação opcional}

### Questões (revisor perguntou, precisa responder)
5. **{pergunta}** → {resposta}
```

### 2. Classificar cada item

Para cada feedback, classificar:
- **Concordo → implementar**: o revisor está certo, fazer a mudança
- **Concordo parcialmente → discutir**: entendo o ponto mas há nuance, responder no PR explicando
- **Discordo → justificar**: tenho boa razão para manter o código como está, explicar por quê
- **Dúvida → perguntar**: não entendi o comment, pedir esclarecimento

### 3. Implementar correções

Para cada item "implementar":

```markdown
## Implementando: {descrição do item}

Arquivo: {path}
Problema: {o que o revisor identificou}
Solução: {o que vou fazer}
```

Após implementar, verificar:
- `bun tsc --noEmit` — TypeScript ainda limpo?
- `bun test` — testes ainda passando?
- A correção resolve o problema apontado?

### 4. Responder no PR

Para cada item tratado, formular resposta:

```markdown
**Bloqueantes resolvidos:**
- ✅ {item 1}: {o que fiz}
- ✅ {item 2}: {o que fiz}

**Importantes resolvidos:**
- ✅ {item 3}: {o que fiz}

**Discordâncias justificadas:**
- 💬 {item N}: Mantive como estava porque {razão técnica específica}.
  Se você ainda vê problema, me ajude a entender o caso de uso que isso quebraria.

**Opcionais — deixei para depois:**
- 📋 {item N}: Concordo que seria melhor. Criei issue #{N} para endereçar em outra branch.
```

### 5. Solicitar re-review

Após commit das correções:
```bash
git add -A
git commit -m "fix(review): address code review feedback

- {resumo do que foi corrigido}
- {outro item}

Co-reviewed-by: {nome do revisor}"
git push origin {branch}
```

Notificar o revisor que as mudanças foram aplicadas.

---

## Gotchas

- **Implementar todos os "opcionais" por ansiedade de agradar**: opcionais são opcionais. Implementar tudo aumenta o diff, prolonga o review e pode introduzir mudanças que o revisor não pediu. Priorizar bloqueantes e importantes.
- **Não justificar discordâncias**: se discorda de um comment, silêncio não é uma estratégia. Explicar o raciocínio técnico de forma respeitosa — o revisor pode não ter visto o contexto completo.
- **Commit "address review" monolítico**: commits de review devem ser atômicos por item, não um grande commit de tudo. Facilita re-review e bisect se algo quebrar.
- **Não verificar testes após cada correção**: cada correção pode quebrar testes que passavam antes. Rodar `bun test` após cada mudança significativa, não só no final.
- **Responder defensivamente**: reviews são para melhorar o código, não para atacar o autor. Tom respeitoso e factual — mesmo para discordâncias.
- **Resolver todos os comments mas não re-solicitar review**: após aplicar todas as correções, sempre solicitar explicitamente o re-review. O revisor não monitora o PR automaticamente.
