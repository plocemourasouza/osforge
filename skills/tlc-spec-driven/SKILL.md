---
name: tlc-spec-driven
description: Product-driven planning with 5 phases - Discover, Specify, Design, Tasks, Implement+Validate+Measure. Creates atomic tasks with verification criteria and maintains persistent memory across sessions. Stack-agnostic. Use when starting projects, planning features, implementing with verification, tracking decisions across sessions. Triggers on "initialize project", "map codebase", "discover", "specify feature", "design", "tasks", "implement", "validate", "measure", "pause work", "resume work".
metadata:
  author: github.com/felipfr (extended with PDD integration)
  version: "2.0.0"
---

# Tech Lead's Club - Product-Driven Spec Development

Plan and implement products with precision. User problems first. Granular tasks. Clear dependencies. Measurable outcomes.

```
┌──────────┐   ┌──────────┐   ┌──────────┐   ┌─────────┐   ┌───────────────────┐   ┌──────────┐
│ DISCOVER │ → │ SPECIFY  │ → │  DESIGN  │ → │  TASKS  │ → │ IMPLEMENT+VALIDATE│ → │ MEASURE  │
└──────────┘   └──────────┘   └──────────┘   └─────────┘   └───────────────────┘   └──────────┘
 Problema do    Requisitos     Arquitetura    Tarefas        Código + Testes         Métricas de
 usuário +      técnicos +     + decisões     atômicas +     + evidência de          sucesso +
 hipótese +     acceptance     + trade-offs   priorização    verificação             feedback loop
 métricas       criteria                      por impacto
```

## Princípio PDD (Product Driven Development)

Antes de resolver tecnicamente, pergunte:
- **Isso resolve o problema do USUÁRIO ou o problema TÉCNICO?**
- Existe uma solução mais simples que entrega 80% do valor?
- Como o usuário vai perceber essa mudança?
- Se ninguém usar esse feature, foi tempo bem gasto?

PDD não substitui rigor técnico — ele DIRECIONA o rigor técnico para onde importa.

## Project Structure

```
.specs/
├── project/
│   ├── PROJECT.md      # Vision & goals
│   ├── ROADMAP.md      # Features & milestones
│   ├── STATE.md        # Memory between sessions
│   └── DECISIONS.md    # ADR log (architectural decisions)
├── codebase/           # Brownfield analysis (existing projects)
│   ├── STACK.md
│   ├── ARCHITECTURE.md
│   ├── CONVENTIONS.md
│   ├── STRUCTURE.md
│   ├── TESTING.md
│   └── INTEGRATIONS.md
└── features/           # Feature specifications
    └── [feature]/
        ├── discovery.md    # ← NOVO: Problema, hipótese, métricas
        ├── spec.md
        ├── design.md
        ├── tasks.md
        └── stories/
```

## Workflow

**New project:**
1. Initialize project → PROJECT.md
2. Create roadmap → ROADMAP.md
3. **Discover** → discovery.md (problema + hipótese + métricas)
4. Specify features → spec.md
5. Design → design.md
6. Tasks → tasks.md
7. Implement + Validate
8. **Measure** → verificar métricas pós-deploy

**Existing codebase:**
1. Map codebase → 6 brownfield docs
2. Initialize project → PROJECT.md + ROADMAP.md
3. **Discover** → discovery.md
4. Specify features → existing workflow
5. Implement + Validate + **Measure**

---

## Phase 0: DISCOVER (PDD)

**Trigger:** "discover", "qual problema resolver", "por que construir", "validate hypothesis"

**Propósito:** Garantir que estamos construindo a coisa certa ANTES de especificar a solução.

**Saída:** `.specs/features/[feature]/discovery.md`

### Discovery Template

```markdown
# Discovery: [Feature Name]

## Problema do Usuário
- **Quem sofre:** [persona específica, não "o usuário"]
- **O que acontece:** [situação atual — dor concreta, observável]
- **Evidência:** [dados, feedback, métricas, observações que comprovam o problema]
- **Frequência:** [diário / semanal / ocasional]

## Hipótese
Acreditamos que [solução proposta] vai [resultado esperado] para [persona]
porque [razão baseada em evidência].

## Métricas de Sucesso
| Métrica | Baseline (atual) | Target | Como medir | Prazo |
|---------|------------------|--------|------------|-------|
| [primária] | [valor atual] | [meta] | [ferramenta/evento] | [semanas] |
| [secundária] | [valor atual] | [meta] | [ferramenta/evento] | [semanas] |

## Critério de Sucesso/Falha
- **Sucesso:** [métrica primária atinge target em prazo]
- **Pivotar:** [se métrica < X% do target, mudar abordagem]
- **Abandonar:** [se após Y semanas sem melhora, não prosseguir]

## MVP Scope (menor experimento que valida hipótese)
- Inclui: [funcionalidades mínimas para testar hipótese]
- NÃO inclui: [o que pode esperar para depois da validação]

## Alternativas Consideradas
- [Opção A]: descartada porque [razão]
- [Opção B]: descartada porque [razão]
- Não fazer nada: [risco se não implementarmos]

## Prioridade de Produto
Impacto: [Alto/Médio/Baixo] × Confiança: [Alta/Média/Baixa] / Esforço: [Alto/Médio/Baixo]
Score: [H×H/L = muito alta ... L×L/H = muito baixa]
```

### Regras do Discover
- NUNCA pule esta fase para features que tocam o usuário final
- Para tasks puramente técnicas (refactoring, infra, CI/CD), Discover é opcional
- Se não há evidência do problema, busque antes de especificar
- Se não consegue definir métrica de sucesso, o escopo está vago demais

---

## Phase 1-3: SPECIFY → DESIGN → TASKS

(Mantém workflow existente — ver references/)

### Impact-First Prioritization (na fase TASKS)

Quando múltiplas tasks existem, priorize por impacto no usuário:

```
Prioridade = (Impacto no Usuário × Confiança) / Esforço Técnico
```

| Fator | Alto (3) | Médio (2) | Baixo (1) |
|-------|----------|-----------|-----------|
| **Impacto** | Afeta todos os usuários ou fluxo crítico | Afeta segmento relevante | Afeta poucos ou edge case |
| **Confiança** | Dados/feedback confirmam | Evidência indireta | Intuição / suposição |
| **Esforço** | > 1 semana | 2-5 dias | < 2 dias |

**Score > 4:** Fazer primeiro
**Score 2-4:** Fazer neste ciclo
**Score < 2:** Backlog (reavaliar depois)

**Anti-pattern:** NÃO priorize pelo que é tecnicamente interessante. Priorize pelo que entrega mais valor ao usuário com maior confiança.

---

## Phase 4: IMPLEMENT + VALIDATE

(Mantém workflow existente — ver references/)

---

## Phase 5: MEASURE (PDD)

**Trigger:** "measure", "post-deploy", "verificar métricas", "feature funcionou?"

**Propósito:** Fechar o loop — verificar se a hipótese do Discover se confirmou.

### Post-Deploy Checklist

```markdown
## Post-Deploy: [Feature Name]
Data do deploy: [YYYY-MM-DD]

### Rollout
- [ ] Feature flag configurada (canary/% rollout)
- [ ] Plano de rollback documentado
- [ ] Monitoramento de erros ativo (Sentry/logs)

### Analytics
- [ ] Eventos de analytics implementados para métricas de sucesso
- [ ] Dashboard/query criada para acompanhar métricas
- [ ] Baseline registrada antes do deploy

### Revisão Agendada
- [ ] Data de revisão: [YYYY-MM-DD] (conforme prazo do Discovery)
- [ ] Responsável: [nome/role]

### Resultado (preencher na data de revisão)
- Métrica primária: [baseline] → [atual] (target era [X])
- Métrica secundária: [baseline] → [atual]
- Veredicto: [ ] Sucesso [ ] Pivotar [ ] Abandonar
- Aprendizados: [o que descobrimos]
- Próximos passos: [iterar / escalar / remover]
```

### Regras do Measure
- NUNCA declare feature "entregue" sem métricas configuradas
- Se não é possível medir (infra, refactoring), registre pelo menos: build time, error rate, deploy frequency
- Revisão de métricas é tão importante quanto code review
- Features sem evidência de impacto são candidatas a remoção

---

## Context Loading Strategy

**Base load (~15k tokens):**
- PROJECT.md (if exists)
- ROADMAP.md (when planning/working on features)
- STATE.md (persistent memory)

**On-demand load:**
- discovery.md (when planning new feature — Phase 0)
- Codebase docs (when working in existing project)
- spec.md (when working on specific feature)
- design.md (when implementing from design)
- tasks.md (when executing tasks)

**Never load simultaneously:**
- Multiple feature specs
- Multiple architecture docs
- Archived documents

**Target:** <40k tokens total context
**Reserve:** 160k+ tokens for work, reasoning, outputs

### Context Budget — Regra dos 70%

Acima de 70% do context window, o modelo degrada silenciosamente: ignora tools,
alucina mais, para no meio de tasks, perde adherência a rules. Não há erro
explícito — apenas degradação progressiva.

**Sinais de saturação (auto-diagnóstico):**
- Respostas ficam genéricas ou repetitivas
- Agent "esquece" de rodar testes ou verificações
- Tasks param abruptamente sem explicação
- Rules documentadas são ignoradas
- Agent começa a cortar caminho em processos definidos

**Ações obrigatórias ao detectar saturação:**

1. **PARE** a task atual — não continue em contexto degradado
2. **Salve estado** no STATE.md:
   ```
   ## Context Reset — [YYYY-MM-DD HH:MM]
   - Task em andamento: [descrição]
   - Último checkpoint: [o que foi completado]
   - Próximo passo: [o que falta]
   - Arquivos modificados: [lista]
   - Testes passando: [sim/não/parcial]
   ```
3. **Compact** ou inicie nova sessão
4. **Retome** carregando apenas: STATE.md + task específica

**Prevenção (antes de saturar):**
- Antes de tasks complexas: descarregue contexto desnecessário
- Uma feature por sessão — não misture features no mesmo contexto
- Após completar fase (Specify, Design, Tasks), salve em arquivo e limpe
- Sub-agents para research, code-review e debugging (contexto isolado)
- Se uma task precisa de mais de 3 specs, divida a task

**Estimativa de consumo:**

| Item | Tokens (~) | Notas |
|------|-----------|-------|
| CLAUDE.md + SKILLS.md | ~5k | Base fixa |
| 1 skill ativado | ~2-4k | Sob demanda |
| 1 spec.md típico | ~1-3k | Sob demanda |
| 1 agent completo | ~3-5k | Contexto isolado (não conta) |
| MCP call + response | ~1-2k | Cada chamada |
| Arquivo de código lido | ~0.5-2k | Por arquivo |
| Histórico de mensagens | acumula | Principal vilão |

**Budget prático (200k window):**
- 🟢 < 80k (~40%): zona confortável, modelo opera bem
- 🟡 80-120k (~40-60%): atenção, evitar carregar mais contexto
- 🔴 120-140k (~60-70%): salvar estado, preparar compaction
- ⛔ > 140k (~70%+): PARAR, compactar AGORA, degradação ativa

### Compression Mode (zonas 🟡 e 🔴)

Quando o contexto entra na zona amarela ou vermelha, adote automaticamente:
- Respostas concisas sem preâmbulos ou recapitulações
- Mostrar apenas diffs, nunca re-listar arquivos inteiros
- Não repetir contexto já estabelecido na conversa
- Omitir explicações de "por que" quando o usuário já tem o contexto
- Priorizar ação sobre documentação inline

### Story Loading por Fase

User stories têm ~725 tokens. Cada fase precisa apenas de seções específicas:

| Fase | Seções necessárias da story | Ignorar |
|------|----------------------------|--------|
| **Discover/Specify** | Story completa | — |
| **Design** | Acceptance criteria + edge cases + dependências | Contexto de produto, prioridade, métricas |
| **Implement** | Acceptance criteria + happy path + edge cases | Contexto de produto, prioridade, métricas |
| **Measure** | Métricas de sucesso + critério de completude | Acceptance criteria, edge cases, happy path |

Isso reduz o consumo de ~725 → ~350 tokens por story nas fases de implementação.

## Attempts Log (quando implementação falha)

Quando uma task falha após tentativa genuína, registre em STATE.md:

```markdown
## Attempts — STORY-{N}: [título]

### Attempt 1 — [YYYY-MM-DD HH:MM]
- Abordagem: [o que foi tentado]
- Resultado: [o que aconteceu]
- Root cause: [por que falhou]
- Arquivos tocados: [lista]
- Rollback: [git stash / git checkout -- files]

### Attempt 2 — [YYYY-MM-DD HH:MM]
- Abordagem: [diferente da anterior]
- ...

### Decisão
- [ ] Tentar abordagem diferente: [descrição]
- [ ] Escalar complexidade para architect review
- [ ] Simplificar escopo (remover edge cases)
```

### Regras de Attempts
- Após 3 tentativas falhadas na mesma task: PARE e revise a spec/design
- Cada tentativa DEVE usar abordagem diferente (repetir = desperdício)
- SEMPRE faça rollback limpo antes de nova tentativa (não acumule fixes)

## Commands

**Project-level:**

| Trigger Pattern | Reference |
|----------------|-----------|
| Initialize project, setup project | [project-init.md](references/project-init.md) |
| Create roadmap, plan features | [roadmap.md](references/roadmap.md) |
| Map codebase, analyze existing code | [brownfield-mapping.md](references/brownfield-mapping.md) |
| Record decision, log blocker | [state-management.md](references/state-management.md) |
| Pause work, end session | [session-handoff.md](references/session-handoff.md) |
| Resume work, continue | [session-handoff.md](references/session-handoff.md) |

**Feature-level:**

| Trigger Pattern | Reference |
|----------------|-----------|
| Discover, validate problem, why build | (inline — Phase 0 above) |
| Specify feature, define requirements | [specify.md](references/specify.md) |
| Design feature, architecture | [design.md](references/design.md) |
| Break into tasks, create tasks | [tasks.md](references/tasks.md) |
| Implement task, build | [implement.md](references/implement.md) |
| Validate, verify, test | [validate.md](references/validate.md) |
| Measure, post-deploy, check metrics | (inline — Phase 5 above) |

**Tools:**

| Trigger Pattern | Reference |
|----------------|-----------|
| Code analysis, search patterns | [code-analysis.md](references/code-analysis.md) |

## Output Behavior

**Model guidance:** After completing lightweight tasks (validation, state updates, session handoff), naturally mention once that such tasks work well with faster/cheaper models. Track in STATE.md under `Preferences` to avoid repeating. For heavy tasks (brownfield mapping, complex design), briefly note the reasoning requirements before starting.

Be conversational, not robotic. Don't interrupt workflow—add as a natural closing note. Skip if user seems experienced or has already acknowledged the tip.

## Code Analysis

Use available tools with graceful degradation. See [code-analysis.md](references/code-analysis.md).

## Templates

### User Stories
Antes de implementar features, crie user stories usando o template:
- Template: [templates/user-story.md](templates/user-story.md)
- Local: `.specs/features/[feature]/stories/`
- Criar ANTES da implementação para guiar acceptance testing
- DEVE incluir Contexto de Produto e Métricas de Sucesso (PDD)

### Decision Log (ADR)
Registre decisões arquiteturais importantes:
- Template: [templates/decisions.md](templates/decisions.md)
- Local: `.specs/project/DECISIONS.md`
- Toda decisão com trade-offs deve ser registrada
