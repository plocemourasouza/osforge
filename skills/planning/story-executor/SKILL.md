---
name: story-executor
description: >
  Executa implementação de uma story seguindo suas tasks e ACs.
  Coordena invocação dos skills de execução corretos do OSForge.
  Use com "executar story", "implementar story", "dev story".
trigger: executar story|implementar story|dev story|run story
model-tier: sonnet
---

# Story Executor

## Papel
Desenvolvedor implementando a story. Foco em execução precisa das tasks,
respeitando project-context e patterns existentes do codebase.

## Inputs
- **story file** — Story com ACs e tasks (obrigatório)
- **project-context.md** — Stack e regras (carregar se existir)
- **Architecture** — Decisões técnicas relevantes

## Processo

### 1. Carregar Story
- Ler story file completo (ACs, tasks, dependências)
- Verificar que dependências estão completas (stories anteriores done)
- Carregar project-context.md para regras do codebase

### 2. Executar Tasks em Ordem
Para cada task na story:

**a) Identificar skill OSForge mais adequado:**
- Schema change → prisma skills
- UI component → shadcn/ui, nextjs skills
- API route → server-actions, api-routes skills
- Validação → zod-validation skill
- RLS → supabase-rls skill
- Teste → testing skills

**b) Executar task** usando o skill identificado

**c) Marcar task como done** no story file:
```markdown
- [x] `{file/path.ts}` — {ação} ✅
```

### 3. Self-Check — ACs Satisfeitos?
Após completar todas as tasks:
- Verificar cada AC contra o código produzido
- Rodar `skills/quality/edge-case-hunter` no diff produzido
- Se algum AC não satisfeito → identificar o gap e resolver

### 4. Atualizar Story
```markdown
---
status: in-review
completed_tasks: [{lista}]
files_changed: [{lista de arquivos}]
---
```

### 5. Handoff
Informar ao Orchestrator ou usuário:
"Story {id} implementada. {N} tasks completas, {N} arquivos modificados.
Todos ACs verificados. Pronto para code review."

## Regras Críticas
- NÃO parar por "milestone" ou "progresso significativo" — continuar até
  completar TODOS os ACs ou até um HALT condition
- NÃO agendar "próxima sessão" — executar em sequência contínua
- Se encontrar blocker técnico → HALT e informar o usuário com detalhes
- Se encontrar ambiguidade no AC → HALT e perguntar, não assumir
- Respeitar TODAS as regras de project-context.md (naming, patterns, etc.)
