# Marketing Workflows — Mapa de Roteamento

> Conecta agentes do The Agency (persona) com workflows do marketingskills (execução).
> Fonte: `coreyhaines31/marketingskills` v1.4.0, adaptado para OSForge.

---

## Como funciona

1. O orchestrator detecta uma demanda de marketing/paid-media/vendas
2. Ativa o **agente** (persona com identidade, regras, tom)
3. Carrega o **workflow** correspondente (framework de execução passo-a-passo)
4. O agente executa usando o workflow como roteiro

**Regra:** O agente define *quem eu sou*. O workflow define *o que eu faço*.

---

## Pré-requisito: Contexto de Marketing

Antes de qualquer workflow, verificar se `.osforge/marketing-context.md` existe.
Se não existir, usar `workflows/product-marketing-context.md` para criá-lo.
Todos os workflows dependem desse arquivo como fonte de verdade sobre produto, audiência e posicionamento.

---

## Divisão: 📢 Marketing (25 workflows)

### Otimização de Conversão (CRO)

| Workflow | Quando usar | Agente primário | Agentes complementares |
|----------|-------------|-----------------|----------------------|
| `page-cro` | Otimizar qualquer página de marketing | `marketing-growth-hacker` | `marketing-content-creator` |
| `signup-flow-cro` | Otimizar fluxo de cadastro/registro | `marketing-growth-hacker` | — |
| `onboarding-cro` | Otimizar ativação pós-cadastro | `marketing-growth-hacker` | — |
| `form-cro` | Otimizar formulários (exceto signup) | `marketing-growth-hacker` | — |
| `popup-cro` | Criar/otimizar popups e modais | `marketing-growth-hacker` | `marketing-content-creator` |
| `paywall-upgrade-cro` | Paywalls e telas de upgrade in-app | `marketing-growth-hacker` | — |

### Conteúdo & Copy

| Workflow | Quando usar | Agente primário | Agentes complementares |
|----------|-------------|-----------------|----------------------|
| `copywriting` | Escrever copy de marketing para páginas | `marketing-content-creator` | `marketing-growth-hacker` |
| `copy-editing` | Revisar e melhorar copy existente | `marketing-content-creator` | — |
| `content-strategy` | Planejar estratégia de conteúdo | `marketing-content-creator` | `marketing-seo-specialist` |
| `email-sequence` | Criar sequências de email automatizadas | `marketing-content-creator` | `marketing-growth-hacker` |
| `lead-magnets` | Criar lead magnets para captura de leads | `marketing-content-creator` | `marketing-growth-hacker` |
| `social-content` | Conteúdo para redes sociais | `marketing-social-media-strategist` | Agentes de plataforma* |

*Agentes de plataforma: `marketing-linkedin-content-creator`, `marketing-twitter-engager`, `marketing-instagram-curator`, `marketing-tiktok-strategist`, `marketing-reddit-community-builder`

### SEO & Discovery

| Workflow | Quando usar | Agente primário | Agentes complementares |
|----------|-------------|-----------------|----------------------|
| `seo-audit` | Auditar SEO técnico e on-page | `marketing-seo-specialist` | — |
| `ai-seo` | Otimizar para buscas via IA (AEO/GEO/LLMO) | `marketing-seo-specialist` | — |
| `programmatic-seo` | Criar páginas SEO em escala | `marketing-seo-specialist` | `marketing-growth-hacker` |
| `site-architecture` | Planejar hierarquia, navegação, URLs | `marketing-seo-specialist` | — |
| `schema-markup` | Adicionar/otimizar dados estruturados | `marketing-seo-specialist` | — |
| `competitor-alternatives` | Páginas de comparação com concorrentes | `marketing-seo-specialist` | `marketing-content-creator` |

### Retenção & Crescimento

| Workflow | Quando usar | Agente primário | Agentes complementares |
|----------|-------------|-----------------|----------------------|
| `churn-prevention` | Reduzir churn, fluxos de cancelamento | `marketing-growth-hacker` | — |
| `free-tool-strategy` | Planejar ferramentas gratuitas de marketing | `marketing-growth-hacker` | `marketing-seo-specialist` |
| `referral-program` | Criar/otimizar programa de indicação | `marketing-growth-hacker` | — |

### Estratégia & Planejamento

| Workflow | Quando usar | Agente primário | Agentes complementares |
|----------|-------------|-----------------|----------------------|
| `marketing-ideas` | Brainstorm de ideias de marketing | `marketing-growth-hacker` | `marketing-content-creator` |
| `marketing-psychology` | Aplicar psicologia ao marketing | `marketing-growth-hacker` | `marketing-content-creator` |
| `launch-strategy` | Planejar lançamento de produto/feature | `marketing-growth-hacker` | `marketing-content-creator`, `marketing-social-media-strategist` |
| `pricing-strategy` | Definir precificação e empacotamento | `marketing-growth-hacker` | — |

---

## Divisão: 💰 Mídia Paga (4 workflows)

| Workflow | Quando usar | Agente primário | Agentes complementares |
|----------|-------------|-----------------|----------------------|
| `paid-ads` | Campanhas Google/Meta/LinkedIn Ads | `paid-media-ppc-strategist` | `paid-media-paid-social-strategist` |
| `ad-creative` | Gerar criativos de anúncios em escala | `paid-media-creative-strategist` | — |
| `analytics-tracking` | Configurar tracking e medição | `paid-media-tracking-specialist` | — |
| `ab-test-setup` | Planejar e implementar testes A/B | `paid-media-tracking-specialist` | `marketing-growth-hacker` |

---

## Divisão: 💼 Vendas (3 workflows)

| Workflow | Quando usar | Agente primário | Agentes complementares |
|----------|-------------|-----------------|----------------------|
| `cold-email` | Emails frios B2B e sequências de follow-up | `sales-outbound-strategist` | `sales-discovery-coach` |
| `sales-enablement` | Decks, one-pagers, docs de objeções | `sales-proposal-strategist` | `sales-deal-strategist` |
| `revops` | Lifecycle de leads, scoring, handoff MQL→SQL | `sales-pipeline-analyst` | `sales-account-strategist` |

---

## Workflows sem agente direto (autônomos)

Estes workflows podem ser executados pelo orchestrator sem ativar um agente específico.
O orchestrator assume a persona adequada baseado no contexto.

| Workflow | Descrição | Fallback de persona |
|----------|-----------|-------------------|
| `product-marketing-context` | Criar/atualizar contexto de marketing do projeto | Orchestrator direto |

---

## Encadeamento de Workflows

Workflows que naturalmente se conectam em sequência:

### Fluxo: Página nova de marketing
```
product-marketing-context → copywriting → page-cro → schema-markup → analytics-tracking → ab-test-setup
```

### Fluxo: Estratégia SEO completa
```
product-marketing-context → seo-audit → site-architecture → content-strategy → ai-seo → schema-markup → programmatic-seo
```

### Fluxo: Lançamento de produto
```
product-marketing-context → launch-strategy → copywriting → email-sequence → social-content → paid-ads → ad-creative → analytics-tracking
```

### Fluxo: Otimização de funil
```
page-cro → signup-flow-cro → onboarding-cro → email-sequence → churn-prevention → referral-program
```

### Fluxo: Outbound B2B
```
product-marketing-context → competitor-alternatives → sales-enablement → cold-email → revops
```

---

## Cross-references entre divisões

| Origem | Destino | Quando |
|--------|---------|--------|
| Marketing → Paid Media | `copywriting` → `ad-creative` | Copy de página vira base para criativos |
| Marketing → Paid Media | `page-cro` → `ab-test-setup` | Recomendações de CRO viram hipóteses de teste |
| Marketing → Paid Media | `page-cro` → `analytics-tracking` | Otimizações precisam de tracking |
| Marketing → Sales | `content-strategy` → `sales-enablement` | Conteúdo de marketing alimenta material de vendas |
| Marketing → Sales | `competitor-alternatives` → `cold-email` | Diferenciação competitiva entra no outreach |
| Paid Media → Marketing | `analytics-tracking` → `page-cro` | Dados de tracking revelam problemas de conversão |
| Sales → Marketing | `revops` → `email-sequence` | Lifecycle stages disparam sequências de email |
