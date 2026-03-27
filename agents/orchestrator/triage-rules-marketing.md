# Regras de Triage — Marketing, Mídia Paga & Vendas

> Extensão de `agents/orchestrator/triage-rules.md` para demandas de marketing.
> Adicionar ao final do triage-rules.md existente.

---

## Detecção de Demanda de Marketing

### Sinais de ativação

O orchestrator deve detectar demandas de marketing por estas palavras-chave e contextos:

**CRO / Conversão:**
- "conversão", "CRO", "landing page", "bounce rate", "signup", "onboarding"
- "ninguém converte", "taxa de conversão", "formulário", "popup", "paywall"
- "otimizar página", "melhorar conversões", "page isn't converting"

**Copy / Conteúdo:**
- "escrever copy", "headline", "CTA", "reescrever", "copy fraca"
- "email sequence", "drip campaign", "welcome email", "newsletter"
- "conteúdo para", "estratégia de conteúdo", "lead magnet"
- "post para LinkedIn/Twitter/Instagram"

**SEO:**
- "SEO", "audit SEO", "ranking", "Google", "tráfego orgânico"
- "schema", "sitemap", "core web vitals", "indexação"
- "AI search", "AEO", "GEO", "aparecer no ChatGPT/Perplexity"
- "pSEO", "programmatic SEO", "páginas em escala"

**Paid Media:**
- "Google Ads", "Meta Ads", "LinkedIn Ads", "Facebook Ads"
- "campanha paga", "PPC", "ROAS", "CPA", "ad creative"
- "tracking", "GA4", "GTM", "pixel", "conversão tracking"
- "A/B test", "experimento", "teste A/B"

**Vendas:**
- "cold email", "outbound", "prospecção"
- "sales deck", "proposta", "one-pager", "objeções"
- "pipeline", "MQL", "SQL", "lead scoring", "RevOps"

**Estratégia:**
- "lançamento", "launch", "pricing", "precificação"
- "churn", "retenção", "cancelamento", "referral"
- "ideias de marketing", "growth", "viral"

---

## Classificação de Complexidade para Marketing

### QUICK — Execução direta

**Critérios (TODOS devem aplicar):**
- Uma tarefa isolada com contexto claro
- Produto/audiência já conhecidos (marketing-context existe)
- Não requer pesquisa competitiva ou análise de dados
- Output é um único artefato (copy, audit, email, etc.)

**Exemplos:**
- "Reescreve essa headline" → `copywriting`
- "Adiciona schema markup nessa página" → `schema-markup`
- "Escreve um cold email para CTOs" → `cold-email`
- "Revisa essa copy" → `copy-editing`
- "Cria um popup de exit-intent" → `popup-cro`

**Pipeline:** contexto → workflow → output → review

### STANDARD — Tarefa com planejamento

**Critérios (ALGUM se aplica):**
- Múltiplos outputs interconectados
- Precisa de análise antes de agir (audit, review)
- Envolve sequência de passos (funil, email sequence)
- Requer decisões estratégicas com trade-offs

**Exemplos:**
- "Faz um audit de SEO do meu site" → `seo-audit` (análise + recomendações)
- "Cria uma sequência de 5 emails" → `email-sequence` (estratégia + copy)
- "Otimiza minha landing page" → `page-cro` (análise + recomendações + copy)
- "Monta uma campanha no Google Ads" → `paid-ads` (estratégia + setup + criativos)
- "Configura tracking de conversão" → `analytics-tracking` (plano + implementação)

**Pipeline:** contexto → análise → plano → execução por fase → review

### COMPLEX — Estratégia completa

**Critérios (ALGUM se aplica):**
- Estratégia completa de canal ou funil
- Envolve múltiplos workflows encadeados
- Requer criação de marketing-context do zero
- Impacta múltiplos canais ou times

**Exemplos:**
- "Monta minha estratégia de SEO completa" → `seo-audit` + `site-architecture` + `content-strategy` + `ai-seo` + `schema-markup`
- "Prepara o lançamento do meu produto" → `launch-strategy` + `copywriting` + `email-sequence` + `social-content` + `paid-ads`
- "Otimiza todo meu funil" → `page-cro` + `signup-flow-cro` + `onboarding-cro` + `email-sequence` + `churn-prevention`
- "Monta minha operação de RevOps" → `revops` + `analytics-tracking` + `sales-enablement` + `cold-email`

**Pipeline:** contexto → plano multi-fase → execução workflow por workflow → review integrado

---

## Routing para Skills por Domínio (extensão da tabela existente)

| Tipo de Projeto | Skills/Workflows Primários | Agente Principal |
|---|---|---|
| CRO | `page-cro`, `signup-flow-cro`, `form-cro`, `popup-cro` | `marketing-growth-hacker` |
| Copywriting | `copywriting`, `copy-editing`, `lead-magnets` | `marketing-content-creator` |
| SEO | `seo-audit`, `ai-seo`, `schema-markup`, `site-architecture` | `marketing-seo-specialist` |
| Conteúdo | `content-strategy`, `email-sequence`, `social-content` | `marketing-content-creator` |
| Paid | `paid-ads`, `ad-creative`, `analytics-tracking`, `ab-test-setup` | `paid-media-ppc-strategist` |
| Vendas | `cold-email`, `sales-enablement`, `revops` | `sales-outbound-strategist` |
| Growth | `churn-prevention`, `referral-program`, `free-tool-strategy` | `marketing-growth-hacker` |
| Estratégia | `marketing-ideas`, `launch-strategy`, `pricing-strategy` | `marketing-growth-hacker` |

---

## Regra: Verificar marketing-context

**ANTES de executar qualquer workflow de marketing/paid/vendas:**

```
Se .osforge/marketing-context.md NÃO existe:
  → Informar o usuário: "Para executar este workflow com qualidade,
    preciso do contexto de marketing do projeto. Posso criar agora
    (leva ~5 min) ou prosseguir com as informações que você me der."
  → Se aceitar: executar marketing-context-adapter primeiro
  → Se recusar: prosseguir pedindo contexto inline
```

---

## Regra: Combo Agente + Workflow

Quando ativar um agente de marketing/paid/vendas para uma tarefa:

```
1. Identificar o workflow correspondente (ver ROUTING.md)
2. Anunciar: "🤖 Ativando @{agente} com workflow {workflow}..."
3. Carregar o arquivo do agente (identidade)
4. Carregar o arquivo do workflow (execução)
5. Executar o workflow usando a persona do agente
```

Se o workflow gerar recomendações que dependem de OUTRO workflow:
```
Ao final: "Recomendações implementadas. Próximo passo sugerido:
executar {workflow-seguinte} para {motivo}. Prosseguir?"
```
