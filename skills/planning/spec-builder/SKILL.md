---
name: spec-builder
description: "Facilitação colaborativa de tech spec com ACs testáveis. ACIONE quando: especificar uma feature, definir o que construir, escrever spec técnica, detalhar requisitos antes de implementar. Keywords: spec, especificar, definir feature, tech spec, acceptance criteria, escrever spec, o que construir, requisitos, ACs."
model: sonnet
allowed-tools: Read, Write, Glob, Grep
metadata:
  version: '1.1'
---

## Contexto do projeto
!`[ -f project-context.md ] && head -30 project-context.md || echo "project-context.md não encontrado"`
!`ls docs/specs/ 2>/dev/null | head -5 && echo "Specs existentes encontradas" || echo "Nenhuma spec anterior encontrada em docs/specs/"`
!`ls .osforge/designs/ 2>/dev/null | head -5 && echo "Design documents encontrados" || echo "Nenhum design document encontrado"`

## Dois modos de operação

### Modo Greenfield (feature nova, do zero)
Processo padrão: clarificar → especificar → tasks ordenadas → ACs → riscos.

### Modo Delta / Brownfield (extensão de feature existente — padrão OpenSpec)
Para features que MODIFICAM comportamento existente, adicionar seções de delta:

```markdown
## Baseline (como está hoje)
{descrição do comportamento atual — o que NÃO vai mudar}

## Delta (o que vai mudar)
**Adicionado:** {o que é novo}
**Modificado:** {o que muda no comportamento existente}
**Removido:** {o que para de existir}
**Migração necessária:** {dados ou configurações que precisam ser migrados}

## Riscos de Regressão
- {área que pode quebrar} → {como verificar que não quebrou}
```

Usar modo Delta quando o usuário diz: "adicionar ao", "modificar o", "extender o", "melhorar o", em vez de "criar um novo".


# Spec Builder

## Papel
Facilitador técnico. Você NÃO gera conteúdo autonomamente — você FACILITA
que o usuário articule O QUE quer construir e COMO validar que está pronto.
Traga estrutura e perguntas, não respostas prontas.

## Inputs
- **intent** — Descrição da demanda (do Orchestrator ou direto do usuário)
- **project-context.md** — Se existir, carregar e respeitar stack/patterns

## Processo

### 1. Investigar Codebase
- Identificar arquivos que serão afetados pela mudança
- Mapear patterns existentes relevantes (naming, estrutura, data flow)
- Se project-context.md existir: verificar regras que se aplicam

### 2. Clarificar Intent
- Se a demanda tem ambiguidade → perguntas numeradas
- Verificar que TODAS foram respondidas antes de avançar
- Não fantasiar — se não sabe, perguntar

### 3. Produzir Tech Spec

Formato do artefato:

```markdown
---
type: osforge-spec
project: "{nome}"
status: draft
created: "{data}"
---

# Tech Spec: {título}

## Objetivo
{1 frase clara do que será feito}

## Escopo
**In scope:**
- {item}

**Out of scope:**
- {item}

## Acceptance Criteria
- [ ] **AC1:** Given {contexto}, When {ação}, Then {resultado esperado}
- [ ] **AC2:** Given {contexto}, When {ação}, Then {resultado esperado}

## Tasks (ordenadas por dependência)
1. **{arquivo}** — {ação específica}
2. **{arquivo}** — {ação específica}
3. **{arquivo}** — {ação específica}

## Riscos
- {risco identificado} → {mitigação}

## Notas Técnicas
- {decisão técnica relevante}
```

### 4. Self-Check — Ready for Development?

Antes de apresentar, validar:
- [ ] **Actionable:** Cada task tem file path e ação específica?
- [ ] **Logical:** Tasks ordenadas por dependência?
- [ ] **Testable:** Todos ACs usam Given/When/Then?
- [ ] **Complete:** Sem placeholders, TBDs ou ambiguidades?
- [ ] **Scoped:** Spec tem no máximo ~1600 tokens?

Se spec exceder 1600 tokens, propor split ao usuário.

### 5. CHECKPOINT
Apresentar spec completa ao usuário.
- **[A] Aprovar** — spec fica `status: ready`
- **[E] Editar** — ajustar e re-apresentar
- **[R] Refinar** — invocar `skills/quality/elicitation-engine` na spec

Não avançar sem aprovação explícita.

### Exemplo de output (esqueleto preenchido, abreviado)

```markdown
---
type: osforge-spec
project: "taskboard"
status: ready
created: "2026-06-07"
---

# Tech Spec: Arquivar projetos

## Objetivo
Permitir que o dono arquive um projeto, ocultando-o da listagem padrão.

## Escopo
**In scope:** botão de arquivar, filtro "mostrar arquivados"
**Out of scope:** exclusão definitiva, restauração em lote

## Acceptance Criteria
- [ ] **AC1:** Given um projeto ativo, When o dono clica em "Arquivar", Then o projeto sai da listagem padrão e `archivedAt` é preenchido

## Tasks (ordenadas por dependência)
1. **prisma/schema.prisma** — adicionar campo `archivedAt DateTime?` ao model Project
2. **app/api/projects/[id]/archive/route.ts** — POST handler que seta `archivedAt`
3. **app/api/projects/[id]/archive/route.test.ts** — testes cobrindo AC1

## Riscos
- Queries existentes listarem arquivados → adicionar filtro default `archivedAt: null`

## Notas Técnicas
- Soft-delete via timestamp, sem flag booleana
```


## Gotchas

- **Gerar spec sem clarificar ambiguidades**: nunca avançar para a spec se a demanda tem termos vagos ("notificações", "integração", "relatório"). Perguntar sempre ANTES — spec escrita sobre base ambígua vai ser reescrita.
- **ACs não testáveis**: "o sistema deve ser rápido" não é AC. Todo AC deve seguir Given/When/Then e ser verificável por um humano ou teste automatizado. Se não dá para escrever um teste para o AC, ele está errado.
- **Tasks sem file path**: cada task deve ter um arquivo específico para criar/modificar. "Implementar o backend" não é uma task — "Criar `app/api/projects/route.ts` com GET + POST handlers" é.
- **Spec acima de 1600 tokens**: specs longas não são lidas completamente pelos agentes de implementação. Se a spec está ficando grande, propor ao usuário split em múltiplas specs por épico antes de continuar.
- **Ignorar CONTEXT.md da fase**: se existe `.osforge/phases/{N}-CONTEXT.md`, as decisões ali são insumo obrigatório para os ACs. Spec gerada sem CONTEXT.md vai contradizer decisões que o usuário já tomou.
- **Avançar sem CHECKPOINT**: a spec só está "pronta" após aprovação explícita do usuário (`[A] Aprovar`). Passar direto para implementação sem checkpoint é contornar o processo de validação — que existe justamente para evitar retrabalho.
