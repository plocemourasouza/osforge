# OSForge Agent Flow

Referência visual da arquitetura de fluxo do OSForge.
Leitura rápida — sem precisar abrir o AGENT.md completo.

---

## Fluxo Completo

```
┌─────────────────────────────────────────────────────────────────┐
│  QUALQUER MENSAGEM DO USUÁRIO                                   │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│  0. DETECT (Intelligent Routing — silencioso)                   │
│  ├─ Classificar: QUESTION / QUICK_FIX / FEATURE / BUG / DESIGN │
│  ├─ Detectar domínios: Frontend · Backend · Security · Debug…  │
│  └─ Selecionar agente(s) → anunciar se relevante               │
│                                                                 │
│  QUESTION / QUICK_FIX trivial → responder direto               │
│  1-2 domínios → persona do agente selecionado                  │
│  3+ domínios / COMPLEX → sugerir Orchestrator ↓                │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│  1. INTAKE                                                      │
│  ├─ osforge-db list-projects --status=active (work in progress?)│
│  ├─ osforge-db resume <slug>  (fase atual + resume point)       │
│  │   fallback: .osforge/status.yaml + STATE.md (markdown)       │
│  ├─ Carregar project-context.md                                 │
│  └─ Clarificar (máx 5 perguntas) → loop até clareza            │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│  2. TRIAGE                                                      │
│  ├─ QUICK   → 1-3 arquivos, zero ambiguidade                   │
│  ├─ STANDARD → multi-arquivo, domínio conhecido                 │
│  └─ COMPLEX  → novo sistema, requisitos ambíguos               │
│                                                                 │
│  STANDARD / COMPLEX: declarar na 1ª linha da resposta:         │
│  "Triage: STANDARD — <justificativa 1-2 frases>"               │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│  3. PLAN                                                        │
│  └─ Gerar plano multi-fase com skills mapeados                 │
│     → [A] Aprovar / [E] Editar / [S] Simplificar              │
│                                                                 │
│  APRESENTAÇÃO (Canvas default):                                 │
│  └─ Emitir artefato skills/osforge-canvas (localhost:4242,     │
│     auto-start via SessionStart hook) + resumo curto terminal  │
│     Exceção: usuário pediu "só texto" → texto no terminal      │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│  4. ROUTE — execução fase por fase                              │
│                                                                 │
│  QUICK              STANDARD                COMPLEX             │
│  ┌──────────┐       ┌────────────────┐      ┌───────────────┐  │
│  │spec-     │       │phase-discussion│      │prd-builder    │  │
│  │builder   │       │spec-builder    │      │arch-builder   │  │
│  │(skills   │       │arch-builder*   │      │phase-discuss. │  │
│  │execução) │       │epic-decomp.    │      │epic-decomp.   │  │
│  │code-rev. │       │story-executor  │      │readiness-gate │  │
│  └──────────┘       │code-review     │      │story-executor │  │
│                     │adv-review      │      │code-review    │  │
│                     └────────────────┘      │adv-review     │  │
│                      *se schema/API         └───────────────┘  │
│                                                                 │
│  Tasks com bloco YAML (id/depends_on/wave/parallel_ok):        │
│  waves montadas automaticamente por dispatching-parallel-agents │
│                                                                 │
│  Cada worker despachado via delegation-brief.md:               │
│  objetivo / skills / escopo / critério de pronto / modelo      │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│  5. TRACK (osforge-db — SQLite primário)                        │
│  ├─ osforge-db set-phase <slug> <fase> complete <skill> <art>   │
│  ├─ osforge-db add-task / set-task / list-tasks / board         │
│  ├─ osforge-db add-decision <slug> "<decisão>" --category=arch  │
│  └─ osforge-db set-resume <slug> "Próximo: <fase> — <detalhe>" │
│     (OBRIGATÓRIO ao encerrar sessão com work in progress)       │
│                                                                 │
│  Fallback markdown: .osforge/status.yaml + STATE.md            │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│  6. CORRECT (se mudança de direção)                             │
│  └─ Analisar impacto → propor ajuste → aguardar aprovação      │
└─────────────────────────────────────────────────────────────────┘
```

---

## Mapeamento de Skills por Domínio

```
Request detectado           →  Agente/Skill invocado
────────────────────────────────────────────────────────────────────
Frontend (UI, componente)   →  frontend-engineer
                               + ui-design-intelligence (estilo)
                               + openui-genui-layout (estrutura)
                               + ui-audit (verificação pós)

Backend (API, Prisma)       →  backend-engineer
                               + prisma-expert
                               + postgres-optimization

Auth / Segurança            →  security-auditor
                               + insecure-defaults
                               + nextjs-supabase-auth

Bug / Erro                  →  debugger (10 steps)

Review de código            →  code-reviewer
                               + adversarial-review
                               + edge-case-hunter

Nova feature complexa       →  orchestrator → fluxo completo

UI com intenção visual      →  ui-design-intelligence (primeiro)
                               → openui-genui-layout (estrutura)
                               → frontend-engineer (implementação)
                               → ui-audit (verificação)
```

---

## Exemplo: "Build a Next.js dashboard with authentication"

```
Triage: COMPLEX — novo sistema com Frontend + Backend + Auth

1. INTAKE    → entender escopo, osforge-db resume / carregar project-context.md
2. TRIAGE    → COMPLEX (novo sistema, múltiplos domínios)
3. PLAN      → 5 fases: PRD → Arch → Stories → Impl → Review
               → Canvas: http://localhost:4242/?a=<slug>  +  resumo terminal
4. ROUTE:
   Fase 1: prd-builder         → REQUIREMENTS.md
   Fase 2: arch-builder        → ADR (auth strategy, schema)
   Fase 3: phase-discussion    → CONTEXT.md (decisões UI/UX)
            ui-design-intelligence → design system spec
   Fase 4: epic-decomposer     → 3 épicos, 12 stories (YAML: id/wave/parallel_ok)
            story-executor (waves via dispatching-parallel-agents):
              Wave 1 || User schema + Product schema  (parallel_ok: true)
              Wave 2 || Auth API  + Dashboard API     (parallel_ok: true)
              Wave 3 →  Checkout UI (depende das APIs)
            Cada worker: delegation-brief.md completo
   Fase 5: code-reviewer + adversarial-review + ui-audit
5. TRACK     → osforge-db set-phase / add-task / add-decision / set-resume
               fallback: .osforge/status.yaml + STATE.md atualizados
```

---

## Skills de Suporte (qualquer triage)

| Necessidade | Skill |
|---|---|
| Comprimir contexto | `context/context-distillator` |
| Gerar project-context | `context/project-context-generator` |
| Refinar output | `quality/elicitation-engine` |
| Especialista de área | `agency/` (The Agency — 121 especialistas) |
| Modelo local (LGPD) | `llmfit-advisor` |
| Otimizar custo | `smart-model-dispatch` |
| Iterar sobre skill | `autorefine-skill` |
| Validação do projeto | `python3 .scripts/validate.py --quick` |
| Design system spec | `ui-design-intelligence` |
| Routing automático | `rules/intelligent-routing.mdc` (always-on) |
| Multi-projeto (sede/satélite) | `USAGE.md §10` |

---

*Ver `agents/orchestrator/AGENT.md` para especificação completa.*
*Ver `~/.claude/SKILLS.md` para lista de todos os skills disponíveis.*
