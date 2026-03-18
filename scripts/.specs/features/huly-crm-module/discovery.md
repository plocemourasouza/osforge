# Discovery: Huly CRM Module
**Feature:** huly-crm-module | **Data:** 2026-03-15 | **Status:** Draft

## Problema do Usuário

- **Quem sofre:** Equipes de vendas e marketing de empresas que usam Huly como plataforma de produtividade, mas precisam gerenciar leads de forma estruturada
- **O que acontece:** O plugin `lead` atual do Huly é básico e não oferece funcionalidades completas de CRM (pipeline visual, scoring, automações, analytics, importação em massa, formulários de captura)
- **Evidência:** CRMs como HubSpot, Pipedrive e RD Station dominam o mercado justamente por oferecer gestão completa do ciclo de vida do lead — captura → qualificação → conversão
- **Frequência:** Diário — equipes de vendas interagem com leads múltiplas vezes por dia

## Hipótese

Acreditamos que **um módulo CRM nativo completo no Huly** vai **eliminar a necessidade de ferramentas externas e centralizar a gestão de leads** para **equipes de vendas e marketing de PMEs**
porque **a integração nativa com o ecossistema Huly (tasks, chat, calendário) cria um fluxo de trabalho unificado que ferramentas externas não conseguem replicar**.

## Métricas de Sucesso

| Métrica | Baseline (atual) | Target | Como medir | Prazo |
|---------|------------------|--------|------------|-------|
| Adoção do módulo CRM | 0% (não existe) | 30% dos workspaces ativos | % workspaces com CRM habilitado | 12 semanas |
| Leads gerenciados/workspace | 0 | 500+ leads médios | COUNT(leads) por workspace | 12 semanas |
| Taxa de conversão rastreada | N/A | 15%+ média | leads convertidos / leads totais | 16 semanas |
| NPS do módulo CRM | N/A | > 40 | Survey in-app | 16 semanas |

## Critério de Decisão

- **Sucesso:** > 25% dos workspaces ativos usando CRM com > 100 leads cada após 12 semanas
- **Pivotar:** Se adoção < 10% após 8 semanas, simplificar escopo para apenas pipeline + importação
- **Abandonar:** Se após 16 semanas NPS < 20, reavaliar proposta de valor vs. integrações externas

## MVP Scope

### Inclui (MVP)
1. **Modelo de dados Lead** completo (campos padrão + custom fields)
2. **Pipeline Kanban** visual com drag-and-drop (estágios configuráveis)
3. **API REST** para captura externa (POST/GET/PATCH /api/leads)
4. **Importação CSV/XLSX** com mapping de colunas e deduplicação
5. **Formulários embeddáveis** com captura automática de UTMs
6. **Lead Detail** com timeline de atividades e notas
7. **Dashboard básico** (total leads, por origem, por estágio, conversão)
8. **Automações básicas** (atribuição round-robin, notificações)
9. **Multi-tenancy** via workspace isolation (padrão Huly)
10. **Permissões** (Admin, Sales, Marketing)

### NÃO Inclui (v1)
- Integração direta com Meta Ads / Google Ads (webhook genérico apenas)
- Lead scoring com ML/AI
- Email marketing integrado (usar integrações existentes)
- Relatórios customizáveis (apenas dashboards fixos)
- Mobile app dedicado (usar PWA Huly)
- Integração com telefonia/VoIP

## Prioridade

| Dimensão | Score | Justificativa |
|----------|-------|---------------|
| **Impacto** | Alto (3) | CRM é funcionalidade core para empresas; diferencial competitivo |
| **Confiança** | Alta (3) | Padrão de mercado bem estabelecido; demanda comprovada |
| **Esforço** | Alto (3) | Módulo completo com múltiplos subsistemas |

**Score:** (3 × 3) / 3 = **3.0** — Alta prioridade, mas escopo grande requer faseamento

## Alternativas Consideradas

| Alternativa | Decisão | Razão |
|-------------|---------|-------|
| Não fazer nada | Descartada | Usuários continuam usando ferramentas externas, fragmentando workflow |
| Integrar HubSpot via API | Descartada | Dependência externa, custo para usuário, dados fora do Huly |
| Estender plugin lead existente | Descartada | Arquitetura limitada, melhor começar com design CRM-first |
| Criar apenas pipeline Kanban | Parcialmente considerada | Poderia ser MVP mínimo, mas sem captura/import perde valor |

## Arquitetura de Referência (Huly Platform)

### Stack Confirmado
- **Frontend:** Svelte + Design System Huly
- **Backend:** TypeScript + microserviços
- **Banco:** CockroachDB (dados), MinIO (arquivos), Redis (cache), Elasticsearch (busca)
- **Mensageria:** Redpanda (eventos assíncronos)
- **Monorepo:** Microsoft Rush

### Estrutura de Plugin (padrão Huly)
```
plugins/
  crm/                    # Core do módulo
  crm-assets/             # Assets visuais (ícones, themes)
  crm-resources/          # Recursos e traduções
server-plugins/
  crm/                    # Lógica servidor (API, workers)
```

### Multi-tenancy
- Workspace como unidade de isolamento
- Dados segregados por workspace_id em CockroachDB
- Permissões carregadas pelo Transactor ao conectar

## Entidades do Domínio (Preview)

```
Lead
├── Contact (1:1 opcional)
├── Company (N:1)
├── LeadSource (N:1)
├── Campaign (N:1)
├── LeadStatus/Stage (N:1)
├── LeadTag (N:N)
├── LeadActivity (1:N)
├── LeadNote (1:N)
└── Owner/User (N:1)

Pipeline
├── Stage (1:N ordenado)
└── Workspace (N:1)

ImportJob
├── ImportedLeads (1:N)
└── ErrorLog (1:N)

Form
├── FormField (1:N)
├── FormSubmission (1:N)
└── Campaign (N:1)
```

## Riscos Identificados

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| Complexidade de integração com core Huly | Média | Alto | Estudar plugins existentes (tracker, recruit) como referência |
| Performance com milhões de leads | Baixa | Alto | Índices compostos, paginação cursor-based, cache Redis |
| Curva de aprendizado do Rush/monorepo | Média | Médio | Documentar setup e usar CI existente |
| Conflito com plugin lead existente | Baixa | Médio | Namespace separado `crm:` vs `lead:` |

## Próximos Passos

1. `/spec:specify` — Detalhar requisitos funcionais e não-funcionais
2. `/spec:design` — Arquitetura técnica, modelo de dados, APIs
3. `/spec:tasks` — Decomposição em tasks atômicas com ordem de dependência

---

**Autor:** Claude (spec:discover)
**Revisão:** Pendente aprovação do stakeholder
