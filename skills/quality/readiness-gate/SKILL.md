---
name: readiness-gate
description: "Quality gate pré-implementação. Valida que PRD, Architecture e Épicos estão alinhados e completos antes de iniciar o sprint loop. Use com: 'readiness check', 'pronto para implementar?', 'quality gate', 'o PRD está alinhado com a arquitetura?', 'validar cobertura de requisitos', 'todos os requisitos têm story?', 'checar rastreabilidade antes do sprint'."
trigger: readiness|pronto para implementar|quality gate|gate check|alinhamento PRD|cobertura de requisitos|rastreabilidade
model-tier: sonnet
---

# Readiness Gate

## Papel
Product Manager + Scrum Master especialista em rastreabilidade de requisitos.
Sucesso é medido por encontrar falhas no planejamento ANTES de implementar.

## Inputs
- **PRD** — Requisitos do produto
- **Architecture** — Decisões técnicas (se existir)
- **Épicos/Stories** — Work items a serem implementados
- **project-context.md** — Stack e regras do projeto

## Execução

### 1. Carregar Todos os Artefatos de Planning
- Buscar PRD, Architecture, Épicos nos diretórios de output do projeto
- Se algum obrigatório faltar → FAIL imediato com indicação do que falta

### 2. Cross-Check de Rastreabilidade

**Requisitos → Stories:**
- [ ] Cada requisito funcional do PRD tem pelo menos 1 story?
- [ ] Requisitos not covered sinalizados
- [ ] Prioridades do PRD (must/should/nice) refletidas na ordem dos épicos?

**Stories → Architecture:**
- [ ] Cada story que toca data model referencia ADR de schema?
- [ ] Cada story que toca API referencia ADR de API design?
- [ ] Stack nas stories bate com architecture doc?

**Stories → Implementabilidade:**
- [ ] Todas stories têm ACs com Given/When/Then?
- [ ] Todas tasks têm file paths explícitos?
- [ ] Sem placeholders ou TBDs?
- [ ] Dependências entre stories são consistentes (sem ciclos)?
- [ ] Complexidade L não deveria ser split?

**Architecture → project-context:**
- [ ] Stack definido na architecture bate com project-context.md?
- [ ] Padrões de architecture não conflitam com rules existentes?

**Segurança e Compliance:**
- [ ] RLS policies planejadas para novos data models?
- [ ] LGPD considerado para dados pessoais?
- [ ] Auth flows cobrem todos os roles?

### 3. Produzir Relatório

```markdown
## Readiness Gate: {projeto}

**Resultado:** PASS | CONCERNS | FAIL

### Sumário
- Requisitos cobertos: {N}/{total} ({%})
- Stories com ACs completos: {N}/{total}
- ADRs referenciados: {N}
- Gaps encontrados: {N}

### PASS Items
- {item que passou}

### CONCERNS (deve resolver, mas não bloqueia)
- {concern com sugestão de resolução}

### FAIL Items (bloqueia implementação)
- {fail item com indicação de como resolver}

### Recomendação
{PASS: avançar para sprint planning}
{CONCERNS: resolver concerns e re-check}
{FAIL: voltar para {fase} e resolver {items}}
```

### 4. Decisão
- **PASS** → Orchestrator pode avançar para implementação
- **CONCERNS** → Listar concerns, perguntar se quer resolver agora ou aceitar risco
- **FAIL** → Bloqueia avanço, indicar exatamente o que falta e qual skill usar
