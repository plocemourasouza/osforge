---
name: orchestrator-awareness
description: >
  Rule always-on que garante ativação do Orchestrator quando necessário
  e respeito ao sistema de artefatos progressivos.
type: always-on
version: 1.0.0
---

# Rule: Orchestrator Awareness

## Ativação do Orchestrator

- Quando o usuário iniciar conversa sobre desenvolvimento (novo projeto, feature,
  bug, melhoria), verificar se o Orchestrator deve ser ativado.
- Se existe `.osforge/status.yaml` com work in-progress: SEMPRE informar ao
  usuário antes de qualquer ação: "Há trabalho em progresso: {projeto} — fase
  {current_phase}. Retomar ou iniciar novo?"
- Para demandas de desenvolvimento que envolvam mais de 1 arquivo ou decisões
  de design: sugerir ativação do Orchestrator para planejamento estruturado.
- Para quick fixes triviais (1 arquivo, zero ambiguidade): não impor o Orchestrator
  a menos que o usuário peça.

## Sistema de Artefatos

- Nunca iniciar implementação de feature STANDARD ou COMPLEX sem spec/story
  aprovada (exceto se o usuário fizer override explícito).
- Artefatos de planning devem ter frontmatter com `type`, `status` e `created`.
- Quando um artefato referenciar outro, usar caminhos relativos ao projeto.
- Status de artefatos: draft → ready → in-progress → complete.
- Nunca alterar artefato com status `complete` sem aprovação do usuário.

## Tracking

- Se `.osforge/status.yaml` existe, manter atualizado a cada mudança de fase.
- Se não existe e o trabalho justifica (STANDARD+), sugerir criação.
- Nunca apagar entries do status — marcar como `skipped` ou `cancelled`.
