# Frontend Pipeline — Ordem de Invocação de Skills

> **Objetivo:** Eliminar ambiguidade sobre qual skill de frontend usar e quando.
> O OSForge tem 11+ skills de frontend/UI — este pipeline define a sequência correta.

---

## Pipeline Completo (Feature / Page Nova)

```
Phase 0 — IDENTIDADE (se não existe)
├── Skill: ui-design-intelligence
├── Input: tipo de produto + indústria + público-alvo
├── Output: design system spec (estilo + paleta + tipografia + UX guidelines)
└── Decisão: confirmar com usuário antes de prosseguir

Phase 1 — PLANEJAMENTO ESTRUTURAL
├── Skill: openui-genui-layout
├── Input: requisitos + design system spec (Phase 0)
├── Output: plano OpenUI Lang + componentes shadcn/ui mapeados
├── Padrões: dashboard | crud-list | form-wizard | detail-view |
│            settings-page | auth-page | empty-state | onboarding
└── Validação: usuário aprova estrutura antes de codificar

Phase 2 — COMPONENTES & LIBRARIES
├── Skill: frontend-ui-system
├── Decisão: quais registries usar:
│   ├── shadcn/ui (base — sempre)
│   ├── Magic UI (animações, efeitos, landing pages)
│   ├── Aceternity UI (efeitos avançados)
│   └── mapcn (mapas)
└── Instalação dos componentes necessários

Phase 3 — IMPLEMENTAÇÃO COM BOOST ESTÉTICO
├── Skills (carregadas em paralelo):
│   ├── frontend-design (princípios, UX psychology, decisão)
│   └── aesthetic-boost (kick anti-AI-slop, convergência, complexity matching)
├── Input: plano aprovado + componentes instalados + design system
├── Output: código production-grade com identidade visual
├── Rule always-on: anti-ai-slop.mdc (ativa automaticamente)
└── Referências opcionais (carregar se necessário):
    ├── tailwind-patterns (Tailwind v4, CSS-first config)
    ├── references/animation-guide.md
    └── references/motion-graphics.md

Phase 4 — AUDITORIA
├── Skill: web-design-guidelines (UX / accessibility review)
├── Skill: core-web-vitals (LCP, FID, CLS)
├── Skill: accessibility (WCAG 2.1)
└── Ciclo: findings → fix → re-audit até aprovação
```

---

## Pipeline Rápido (Componente / Fix Estético)

Para tasks menores que não precisam de planejamento completo:

```
1. aesthetic-boost (kick estético)
2. Implementar com anti-ai-slop rule ativa
3. Done
```

## Pipeline Landing Page

O caso de uso mais comum para design visual forte:

```
1. ui-design-intelligence (identidade / design system)
2. openui-genui-layout (estrutura em OpenUI Lang)
3. frontend-ui-system (Magic UI para hero, animações)
4. frontend-design + aesthetic-boost (implementação)
5. web-design-guidelines (auditoria final)
```

## Pipeline Mobile-First

Para interfaces mobile com touch psychology:

```
1. ui-design-intelligence (identidade)
2. mobile-design (touch psychology, platform-specific)
3. openui-genui-layout (estrutura)
4. frontend-design + aesthetic-boost (implementação)
5. accessibility + core-web-vitals (auditoria)
```

---

## Mapa de Skills por Fase

| Fase | Skills Envolvidas | Carregamento |
|------|-------------------|-------------|
| **Identidade** | ui-design-intelligence | On-demand |
| **Estrutura** | openui-genui-layout | On-demand |
| **Componentes** | frontend-ui-system | On-demand |
| **Implementação** | frontend-design, aesthetic-boost, tailwind-patterns | On-demand (paralelo) |
| **Auditoria** | web-design-guidelines, core-web-vitals, accessibility | On-demand |
| **Anti-Slop** | anti-ai-slop.mdc (rule) | Always-on |
| **SEO** | seo, seo-fundamentals | On-demand (pós-audit) |
| **i18n** | i18n-localization | On-demand (se multilíngue) |

---

## Quando NÃO Seguir o Pipeline Completo

- **Apenas ajuste de cores/spacing** → carregar só tailwind-patterns
- **Correção de bug visual** → nenhuma skill necessária
- **Componente isolado sem contexto visual** → frontend-ui-system é suficiente
- **Auditoria sem redesign** → pular direto para Phase 4

---

> **Referência teórica:** [Anthropic — Improving Frontend Design Through Skills](https://claude.com/blog/improving-frontend-design-through-skills)
> **Princípio:** Skills são prompts que ativam on-demand. O pipeline garante a sequência correta sem overhead desnecessário.
