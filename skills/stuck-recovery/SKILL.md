---
name: stuck-recovery
description: >
  Detecta agent stuck patterns (loops, repetições, drift do escopo, ferramenta
  falhando 3x+) e executa recovery cirúrgico: salva estado em osforge-db, identifica
  causa raiz, propõe reset com contexto mínimo preservado. ACIONE quando: usuário
  diz "stuck", "travado", "loop", "não está funcionando", "tenta de novo", "isso
  não está progredindo", "esquece o que estava fazendo", ou quando o agente
  detecta sinais internos de saturação (mesma ferramenta 3x com falha, sem
  progresso em N turnos).
version: 1.0.0
inspired_by: Leonxlnx/agentic-ai-prompt-research (Prompt 26 — Stuck Skill, reframed)
metadata:
  source: "agentic-ai-prompt-research"
  category: "meta"
allowed-tools: Read, Bash, Glob, Grep
---

# Stuck Recovery — Agent Loop Detection + State Save + Reset

> O Stuck Skill original do Claude Code é diagnóstico de processo (CPU, zombies, FDs).
> Este skill é diagnóstico de **agente** — detecta loops semânticos e propõe recovery
> sem perder o trabalho feito.

## Pré-requisitos

Esta skill depende de duas peças externas (via Bash, listado em `allowed-tools`):

- **`osforge-db`** (CLI) — persistência de estado/blockers/resume nas Fases 2 e 4. Verificar com `osforge-db --version`. Sem ele, o SAVE degrada para WIP commit + arquivo de notas local.
- **`context-compact`** (skill OSForge) — usada na Opção B (compact reset). Sem ela, pular direto para Opção A ou C.

## Signs of being stuck (detection)

### Sinais externos (usuário fala)
- "Não está funcionando"
- "Você está travado"
- "Tenta de novo de outro jeito"
- "Você está em loop"
- "Esquece, vamos voltar"
- "Isso não está progredindo"

### Sinais internos (auto-detecção)
| Sinal | Threshold |
|---|---|
| Mesma ferramenta falhando consecutivamente | ≥ 3 vezes |
| Mesmo arquivo sendo lido sem ação | ≥ 5 vezes em 10 turnos |
| Sem progresso mensurável | 10+ turnos sem completar tarefa atômica |
| Context > 85% sem fechamento de fase | saturação iminente |
| Loop de "verify → fail → retry" sem mudança de approach | ≥ 2 ciclos |
| Drift do escopo original | tópico diverge sem aprovação do usuário |
| Tool errors crescendo (não diminuindo) | erro rate > 30% nos últimos 10 calls |

## Protocolo de recovery (4 fases)

### Fase 1: STOP — Pare antes de piorar

Quando detecta stuck:

```
🛑 STUCK DETECTED

Sinal: <qual sinal disparou>
Contexto: <X% / 200k>
Última tarefa atômica completa: <há quantos turnos>
Padrão observado: <descrição em 1 linha>

Vou pausar e propor recovery antes de gastar mais contexto.
```

**NÃO**:
- Tentar mais uma vez "só pra ver"
- Pular pra próxima sub-tarefa
- Pretender que está progredindo

### Fase 2: SAVE — Preserve o trabalho

Salvar estado COMPLETO em `osforge-db` antes do reset:

```bash
osforge-db set-phase <project-slug> "<current-phase>" in_progress \
  --resume "<descrição precisa do ponto de parada>" \
  --artifacts "<arquivos modificados, paths>"

osforge-db add-blocker <project-slug> "<descrição do que está bloqueando>"

# Persistir o summary atual via context-compact se aplicável
```

Garantir que TODOS os arquivos modificados estão commitados (mesmo em WIP commit):
```bash
git add -A && git commit -m "wip: stuck recovery checkpoint at <task>"
```

### Fase 3: DIAGNOSE — Identifique a causa raiz

Aplicar systematic-debugging skill (4 fases) **na própria sessão**:

#### Phase 1: Reproduce
Liste exatamente o que estava acontecendo nos últimos 5-10 turnos:
- Quais ferramentas foram chamadas
- Quais erros retornaram
- O que o agente tentou fazer
- O que o agente DEVERIA ter feito

#### Phase 2: Isolate
Identifique o turn EXATO onde o agente começou a descarrilar:
- Foi uma decisão errada em qual ponto?
- Foi uma assumption falsa sobre quê?
- Foi falta de contexto sobre quê?

#### Phase 3: Understand
Categorize a causa raiz:

| Causa | Sintoma | Fix |
|---|---|---|
| **Context saturation** | Loops + esquecimento | `context-compact` → resume |
| **Wrong approach** | Mesmo erro insiste mesmo após retry | Mudar approach completamente, não tentar variações |
| **Missing context** | Decisões erradas por falta de info | Spawn `explorer-agent` para mapear |
| **Tool misuse** | Ferramenta certa, parâmetros errados | Re-read tool description |
| **Spec drift** | Agente saiu do escopo original | Voltar ao spec, descartar trabalho off-scope |
| **External blocker** | Server down, API quebrada, dep ausente | Avisar usuário, parar até resolver |

#### Phase 4: Fix
Definir explicitamente o que vai ser DIFERENTE na próxima tentativa:
- Approach: <X em vez de Y>
- Context: <vou carregar Z primeiro>
- Verification: <vou checar W antes de declarar pronto>

### Fase 4: RECOVER — Reset cirúrgico com contexto mínimo

3 opções, escolha baseada em diagnóstico:

#### Opção A: Soft reset (mesma sessão)
Se context não está saturado e a causa é diagnosticável:
- Anuncie o reset ao usuário
- Limpe assumptions ruins do contexto mental
- Reformule o approach
- Continue

#### Opção B: Compact reset (mesma sessão, contexto compactado)
Se context > 70% mas você quer continuar:
1. Acione `context-compact` skill
2. Compacte tudo até o ponto do stuck
3. Reinicie com summary + new approach

#### Opção C: Hard reset (nova sessão)
Se context > 90% ou approach é fundamentalmente errado:
1. `osforge-db set-resume <slug> "<próximo passo específico>"`
2. Avise o usuário: "vou pedir pra você abrir nova sessão"
3. Nova sessão começa com `osforge-db resume <slug>` → 50 tokens

## Decision tree

```
Detected stuck
    │
    ├─ Context < 70%?
    │   ├─ YES → Opção A (soft reset)
    │   └─ NO  ↓
    │
    ├─ Context 70-90%?
    │   ├─ YES → Opção B (compact reset)
    │   └─ NO  ↓
    │
    └─ Context > 90% OR approach fundamentalmente errado?
        └─ Opção C (hard reset via osforge-db)
```

## Comunicação ao usuário

**SEMPRE** seja transparente:
```
🛑 Detectei que estamos em loop nas últimas 6 mensagens (tentando rodar `tsc` que falha por causa de import que não existe).

Diagnóstico: missing context — não verifiquei o `package.json` antes de assumir que a dep estava instalada.

Recovery proposto:
1. Salvar estado atual (in progress: fix do TS error em validate.ts:42)
2. Acionar `explorer-agent` pra mapear deps reais
3. Continuar com approach corrigido (instalar dep OR ajustar import)

Pode aprovar? Senão, você prefere: (a) eu tento com outro approach agora, ou (b) salvamos e você abre nova sessão fresh?
```

## Anti-patterns

- ❌ Continuar tentando depois de 3 falhas consecutivas
- ❌ Reset silencioso (usuário fica perdido)
- ❌ Reset sem salvar estado (perde trabalho)
- ❌ Diagnosticar errado e re-aplicar mesma solução
- ❌ Esconder que está stuck pra "parecer competente"
- ❌ Tentar mais ferramentas como solução pra falta de approach

## Verificação pós-recovery

Após o reset, o próximo turno deve produzir:
- [ ] Outcome diferente do loop original
- [ ] Approach mudou (não só os parâmetros)
- [ ] Estado pré-recovery está acessível via `osforge-db resume`
- [ ] Usuário sabe o que mudou e por quê

## Integration com OSForge

O `stuck-recovery` complementa skills existentes:
- `systematic-debugging` (4 fases) — usado dentro da Fase 3 (Diagnose)
- `context-compact` — usado na Opção B (compact reset)
- `osforge-db` — persistência de estado em todas as opções
- `verification-before-completion` — gate antes de declarar recovery successful

## Frequência esperada

Em sessão saudável: **0-1 invocação por 2-3 horas de trabalho intenso**.

Mais que isso indica:
- Spec mal definido (precisa `spec:clarify`)
- Codebase mal mapeada (precisa `explorer-agent`)
- Approach fundamentalmente errado (precisa `brainstorming`)

---

## Related Skills

- `systematic-debugging` — usada internamente na Fase Diagnose
- `context-compact` — opção B do recovery
- `osforge-db` — persistência cross-session
- `verification-before-completion` — gate pós-recovery
- `predictive-failure` — antecipa stuck antes de acontecer
