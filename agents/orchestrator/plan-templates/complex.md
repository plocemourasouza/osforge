# Plan Template: COMPLEX

## Plano: {título}
**Complexidade:** COMPLEX
**Fases:** 7+ (adaptar conforme necessidade)

### Fase 1: Definição de Requisitos (PRD)
- **Objetivo:** Definir problema, usuários, requisitos funcionais e não-funcionais, escopo MVP
- **Skill:** `skills/planning/prd-builder`
- **Artefato:** `{output_dir}/prd-{slug}.md`
- **Tamanho:** Médio a Grande
- **Facilitação:** Colaborativa — perguntas guiadas, não geração autônoma

### Fase 2: Arquitetura
- **Objetivo:** Decisões técnicas, data model, API design, integrações
- **Skill:** `skills/planning/arch-builder`
- **Artefato:** `{output_dir}/architecture-{slug}.md` (com ADRs)
- **Tamanho:** Médio
- **Input:** PRD da Fase 1 + project-context.md

### Fase 3: Decomposição em Épicos e Stories
- **Objetivo:** Transformar requisitos em work items implementáveis
- **Skill:** `skills/planning/epic-decomposer`
- **Artefato:** `{output_dir}/epics/{slug}/` (1 arquivo por épico com stories)
- **Tamanho:** Médio a Grande
- **Input:** PRD + Architecture

### Fase 4: Quality Gate — Readiness Check
- **Objetivo:** Validar que PRD, Architecture e Épicos estão alinhados e completos
- **Skill:** `skills/quality/readiness-gate`
- **Artefato:** Readiness report (PASS / CONCERNS / FAIL)
- **Tamanho:** Pequeno
- **Decisão:**
  - PASS → avançar para implementação
  - CONCERNS → resolver concerns e re-check
  - FAIL → voltar para fase que falhou

### Fase 5: Sprint Planning
- **Objetivo:** Sequenciar stories por dependência e prioridade
- **Skill:** Orchestrator (inline — não precisa de skill separado)
- **Artefato:** Atualizar `.osforge/status.yaml` com sequência de stories
- **Tamanho:** Pequeno

### Fase 6-N: Implementação (sprint loop)
- **Objetivo:** Implementar stories em sequência
- **Skill:** `skills/planning/story-executor` → skills de execução
- **Artefato:** Código + testes por story

Para cada story:
1. Criar/refinar story context (`skills/planning/story-executor`)
2. Implementar tasks
3. Code review (`skills/quality/code-review`)
4. Se aprovado → atualizar status → próxima story
5. Se changes requested → corrigir e re-review

### Fase Final: Review de Qualidade
- **Objetivo:** Revisão adversarial completa + edge case analysis
- **Skill:** `skills/quality/adversarial-review` + `skills/quality/edge-case-hunter`
- **Artefato:** Review report consolidado + lista de edge cases
- **Tamanho:** Médio a Grande

### Checkpoints
- Após Fase 1: aprovar PRD (todos os requisitos cobertos?)
- Após Fase 2: aprovar arquitetura (decisões fazem sentido?)
- Após Fase 3: aprovar decomposição (stories são implementáveis?)
- Após Fase 4: readiness gate deve PASS
- Após cada story: code review
- Após Fase Final: aprovar para merge/deploy

### Notas
- Se PRD for muito grande (>5000 tokens), usar `context-distillator` para comprimir
- Se docs grandes surgirem, usar `doc-shard` para dividir
- Course correction pode acontecer em qualquer ponto — voltar ao Orchestrator
- Para projetos com compliance (LGPD, TSE), incluir review de compliance como sub-fase
- Para projetos multi-tenant, incluir review de RLS como sub-fase
