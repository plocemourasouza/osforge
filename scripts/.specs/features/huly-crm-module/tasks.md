# Tasks: Huly CRM Module (v2 - Arquitetura Nativa)
**Feature:** huly-crm-module | **Data:** 2026-03-16 | **Status:** Ready
**Referências:** [spec.md](./spec.md) | [design.md](./design.md) (v2)

---

## Resumo

| Métrica | Valor |
|---------|-------|
| Total de tasks | 72 |
| Épicos | 7 |
| Estimativa | ~32 horas |
| Complexidade | Alta |

### Mudanças vs tasks.md v1
- **Removido**: Migrations SQL (Huly usa document system)
- **Removido**: Repository pattern (usa TxOperations)
- **Adicionado**: @Model/@Mixin decorators
- **Adicionado**: SpaceType definitions
- **Adicionado**: Viewlet registration
- **Alterado**: Svelte components (não React)

### Dependências Externas
- [x] Repositório hcengineering/platform clonado em ~/Development/huly-platform
- [ ] Node v22 instalado (Huly requirement)
- [ ] Rush instalado globalmente (`npm install -g @microsoft/rush`)
- [ ] Docker rodando (MongoDB, MinIO, Redpanda)

### Ordem de Implementação

```
Épico 1: Setup ──────────────────────────────────┐
                                                 ▼
Épico 2: Plugin Namespace + Types ───────────────┤
                                                 ▼
Épico 3: Model Classes + SpaceType ──────────────┤
                                                 ▼
Épico 4: Viewlets + Application ─────────────────┤
                                                 ▼
Épico 5: Svelte Components ──────────────────────┤
           │                                     │
           ▼                                     ▼
Épico 6: Server Plugin (API)       Épico 7: Dashboard & Import
```

---

## Épico 1: Setup & Environment
**Estimativa:** 2h | **Prioridade:** P0 (bloqueante)

### 1.1 Ambiente de Desenvolvimento

- [ ] **T-001**: Instalar Node v22 via nvm
  - Comando: `nvm install 22 && nvm use 22`
  - Critério: `node --version` retorna v22.x
  - Estimativa: 5min

- [ ] **T-002**: Instalar Rush globalmente
  - Comando: `npm install -g @microsoft/rush`
  - Critério: `rush --version` funciona
  - Estimativa: 5min

- [ ] **T-003**: Rodar rush update no repositório Huly
  - Comando: `cd ~/Development/huly-platform && rush update`
  - Critério: Sem erros, node_modules instalados
  - Estimativa: 10min

- [ ] **T-004**: Verificar build inicial do Huly
  - Comando: `rush build`
  - Critério: Build completo sem erros
  - Estimativa: 15min

### 1.2 Estrutura do Plugin CRM

- [ ] **T-005**: Criar diretório `plugins/crm`
  - Arquivos:
    - `plugins/crm/package.json`
    - `plugins/crm/tsconfig.json`
    - `plugins/crm/src/index.ts`
  - Template: copiar de `plugins/lead` e adaptar
  - Critério: `rush build -t @hcengineering/crm` executa
  - Estimativa: 15min

- [ ] **T-006**: Criar diretório `plugins/crm-assets`
  - Arquivos:
    - `plugins/crm-assets/package.json`
    - `plugins/crm-assets/tsconfig.json`
    - `plugins/crm-assets/src/index.ts`
    - `plugins/crm-assets/assets/icons/` (SVGs)
  - Critério: Assets exportados corretamente
  - Estimativa: 20min

- [ ] **T-007**: Criar diretório `plugins/crm-resources`
  - Arquivos:
    - `plugins/crm-resources/package.json`
    - `plugins/crm-resources/tsconfig.json`
    - `plugins/crm-resources/src/index.ts`
    - `plugins/crm-resources/src/plugin.ts`
  - Critério: Plugin resources registrado
  - Estimativa: 15min

- [ ] **T-008**: Criar diretório `models/crm`
  - Arquivos:
    - `models/crm/package.json`
    - `models/crm/tsconfig.json`
    - `models/crm/src/index.ts`
    - `models/crm/src/plugin.ts`
  - Critério: Model package compila
  - Estimativa: 15min

- [ ] **T-009**: Criar diretório `server-plugins/crm`
  - Arquivos:
    - `server-plugins/crm/package.json`
    - `server-plugins/crm/tsconfig.json`
    - `server-plugins/crm/src/index.ts`
  - Critério: Server plugin carrega sem erros
  - Estimativa: 15min

- [ ] **T-010**: Registrar plugins no rush.json
  - Arquivo: `rush.json` — adicionar entradas para crm, crm-assets, crm-resources, models/crm
  - Comando: `rush update`
  - Critério: `rush list` mostra os novos plugins
  - Estimativa: 10min

---

## Épico 2: Plugin Namespace + Domain Types
**Estimativa:** 3h | **Prioridade:** P0

### 2.1 Plugin Namespace (plugins/crm/src/index.ts)

- [ ] **T-011**: Definir interface CrmLead
  - Arquivo: `plugins/crm/src/index.ts`
  - Conteúdo: Interface que extends Task com campos CRM
  - Campos: email, phone, companyName, jobTitle, city, state, country, score, value, source, campaign, UTMs, convertedAt, lostReason
  - Critério: Interface exportada corretamente
  - Estimativa: 20min

- [ ] **T-012**: Definir interface CrmPipeline
  - Arquivo: `plugins/crm/src/index.ts`
  - Conteúdo: Interface que extends Project
  - Campos: description, defaultOwner
  - Estimativa: 10min

- [ ] **T-013**: Definir interface CrmCustomer (mixin)
  - Arquivo: `plugins/crm/src/index.ts`
  - Conteúdo: Interface que extends Contact
  - Campos: leads, totalValue, customerSince, notes
  - Estimativa: 10min

- [ ] **T-014**: Definir interfaces CrmSource, CrmCampaign, CrmForm
  - Arquivo: `plugins/crm/src/index.ts`
  - Conteúdo: Entidades auxiliares
  - Estimativa: 25min

- [ ] **T-015**: Criar plugin namespace com plugin()
  - Arquivo: `plugins/crm/src/index.ts`
  - Conteúdo: crmId, objeto crm com app, class, mixin, component, string, icon, etc.
  - Referência: `plugins/lead/src/index.ts`
  - Critério: `import crm from '@hcengineering/crm'` funciona
  - Estimativa: 30min

### 2.2 Internacionalização

- [ ] **T-016**: Criar strings em inglês
  - Arquivo: `plugins/crm-resources/src/lang/en.json`
  - Conteúdo: Todas as strings do namespace crm.string.*
  - Estimativa: 20min

- [ ] **T-017**: Criar strings em português
  - Arquivo: `plugins/crm-resources/src/lang/pt-BR.json`
  - Conteúdo: Traduções de todas as strings
  - Estimativa: 20min

- [ ] **T-018**: Registrar i18n no plugin resources
  - Arquivo: `plugins/crm-resources/src/plugin.ts`
  - Conteúdo: Loader de traduções
  - Estimativa: 10min

---

## Épico 3: Model Classes + SpaceType
**Estimativa:** 4h | **Prioridade:** P0

### 3.1 Model Classes (models/crm/src/types.ts)

- [ ] **T-019**: Criar classe TCrmPipeline
  - Arquivo: `models/crm/src/types.ts`
  - Decorators: @Model(crm.class.CrmPipeline, task.class.Project), @UX
  - Propriedades: description, defaultOwner, attachments, comments
  - Referência: `models/lead/src/types.ts` (TFunnel)
  - Estimativa: 25min

- [ ] **T-020**: Criar classe TCrmLead
  - Arquivo: `models/crm/src/types.ts`
  - Decorators: @Model(crm.class.CrmLead, task.class.Task), @UX
  - Propriedades: Todos os campos do design.md com @Prop, @Index, @TypeRef
  - Referência: `models/lead/src/types.ts` (TLead)
  - Estimativa: 45min

- [ ] **T-021**: Criar classe TCrmCustomer (mixin)
  - Arquivo: `models/crm/src/types.ts`
  - Decorator: @Mixin(crm.mixin.CrmCustomer, contact.class.Contact)
  - Propriedades: leads, totalValue, customerSince, notes
  - Estimativa: 20min

- [ ] **T-022**: Criar classes TCrmSource, TCrmCampaign, TCrmForm
  - Arquivo: `models/crm/src/types.ts`
  - Decorators: @Model com @Prop para cada campo
  - Estimativa: 35min

### 3.2 SpaceType (Pipeline Stages)

- [ ] **T-023**: Definir defaultCrmStatuses array
  - Arquivo: `models/crm/src/spaceType.ts`
  - Conteúdo: Array com New, Contacted, Qualified, Proposal, Negotiation, Won, Lost
  - Cada status com id, name, color (PaletteColorIndexes), category
  - Estimativa: 20min

- [ ] **T-024**: Criar TaskTypeDescriptor para Lead
  - Arquivo: `models/crm/src/spaceType.ts`
  - Função: defineSpaceType(builder)
  - Conteúdo: builder.createDoc(task.class.TaskTypeDescriptor, ...)
  - Estimativa: 20min

- [ ] **T-025**: Criar ProjectTypeDescriptor para Pipeline
  - Arquivo: `models/crm/src/spaceType.ts`
  - Conteúdo: builder.createDoc(task.class.ProjectTypeDescriptor, ...)
  - Estimativa: 15min

- [ ] **T-026**: Criar Status docs para cada estágio
  - Arquivo: `models/crm/src/spaceType.ts`
  - Loop: Criar Status para cada item em defaultCrmStatuses
  - Estimativa: 15min

- [ ] **T-027**: Criar TaskType (Lead)
  - Arquivo: `models/crm/src/spaceType.ts`
  - Conteúdo: builder.createDoc(task.class.TaskType, ...)
  - Associar statuses e statusCategories
  - Estimativa: 20min

- [ ] **T-028**: Criar ProjectType (Default Pipeline)
  - Arquivo: `models/crm/src/spaceType.ts`
  - Conteúdo: builder.createDoc(task.class.ProjectType, ...)
  - Template de pipeline padrão
  - Estimativa: 20min

### 3.3 Index e Migration

- [ ] **T-029**: Criar createModel function
  - Arquivo: `models/crm/src/index.ts`
  - Conteúdo: Registra model classes, chama defineSpaceType
  - Estimativa: 25min

- [ ] **T-030**: Criar migration.ts (se necessário)
  - Arquivo: `models/crm/src/migration.ts`
  - Conteúdo: crmOperation com migrate e upgrade
  - Dados default: sources (Website, LinkedIn, etc.)
  - Estimativa: 20min

- [ ] **T-031**: Testar build do model
  - Comando: `rush build -t @hcengineering/model-crm`
  - Critério: Build sem erros TypeScript
  - Estimativa: 10min

---

## Épico 4: Viewlets + Application
**Estimativa:** 3h | **Prioridade:** P1

### 4.1 Viewlets

- [ ] **T-032**: Criar Kanban Viewlet para Lead
  - Arquivo: `models/crm/src/index.ts` (dentro de createModel)
  - Conteúdo: builder.createDoc(view.class.Viewlet, ...) com descriptor: task.viewlet.Kanban
  - Config: attachedTo, companyName, value, assignee, dueDate
  - Estimativa: 25min

- [ ] **T-033**: Criar Table Viewlet para Lead
  - Arquivo: `models/crm/src/index.ts`
  - Conteúdo: Viewlet com descriptor: task.viewlet.StatusTable
  - Config: title, email, phone, status, assignee, score, source, modifiedOn
  - Estimativa: 20min

- [ ] **T-034**: Criar List Viewlet para Lead
  - Arquivo: `models/crm/src/index.ts`
  - Conteúdo: Viewlet com descriptor: view.viewlet.List
  - Estimativa: 15min

### 4.2 Presenters e Mixins

- [ ] **T-035**: Criar mixin ObjectPresenter para Lead
  - Arquivo: `models/crm/src/index.ts`
  - Conteúdo: builder.mixin(..., view.mixin.ObjectPresenter, { presenter: crm.component.LeadPresenter })
  - Estimativa: 10min

- [ ] **T-036**: Criar mixin ObjectEditor para Lead
  - Arquivo: `models/crm/src/index.ts`
  - Conteúdo: builder.mixin(..., view.mixin.ObjectEditor, { editor: crm.component.EditLead })
  - Estimativa: 10min

- [ ] **T-037**: Criar mixin ObjectTitle e ObjectIdentifier
  - Arquivo: `models/crm/src/index.ts`
  - Conteúdo: providers para título e ID do lead
  - Estimativa: 15min

### 4.3 Application (Sidebar)

- [ ] **T-038**: Registrar Application no Workbench
  - Arquivo: `models/crm/src/index.ts`
  - Conteúdo: builder.createDoc(workbench.class.Application, ...)
  - Configurar: label, icon, alias, position, navigatorModel
  - Estimativa: 30min

- [ ] **T-039**: Configurar specials (My Leads, Customers, Dashboard)
  - Arquivo: `models/crm/src/index.ts`
  - Conteúdo: specials array no navigatorModel
  - Estimativa: 20min

- [ ] **T-040**: Configurar spaces (Pipelines)
  - Arquivo: `models/crm/src/index.ts`
  - Conteúdo: spaces array com CrmPipeline
  - Estimativa: 15min

---

## Épico 5: Svelte Components
**Estimativa:** 8h | **Prioridade:** P1

### 5.1 Componentes de Lead

- [ ] **T-041**: Criar CreateLead.svelte
  - Arquivo: `plugins/crm-resources/src/components/CreateLead.svelte`
  - Conteúdo: Modal com campos do lead, SpaceSelector, StatusSelector
  - Referência: `plugins/lead-resources/src/components/CreateLead.svelte`
  - Critério: Modal abre e cria lead corretamente
  - Estimativa: 60min

- [ ] **T-042**: Criar EditLead.svelte
  - Arquivo: `plugins/crm-resources/src/components/EditLead.svelte`
  - Conteúdo: Painel lateral com todos os campos editáveis
  - Referência: `plugins/lead-resources/src/components/EditLead.svelte`
  - Estimativa: 45min

- [ ] **T-043**: Criar LeadPresenter.svelte
  - Arquivo: `plugins/crm-resources/src/components/LeadPresenter.svelte`
  - Conteúdo: Renderização inline do lead (nome + empresa)
  - Estimativa: 20min

- [ ] **T-044**: Criar KanbanCard.svelte
  - Arquivo: `plugins/crm-resources/src/components/KanbanCard.svelte`
  - Conteúdo: Card para Kanban com nome, empresa, owner, valor, tempo no estágio
  - Estimativa: 30min

- [ ] **T-045**: Criar MyLeads.svelte
  - Arquivo: `plugins/crm-resources/src/components/MyLeads.svelte`
  - Conteúdo: Lista filtrada por assignee = currentUser
  - Estimativa: 35min

### 5.2 Componentes de Pipeline

- [ ] **T-046**: Criar CreatePipeline.svelte
  - Arquivo: `plugins/crm-resources/src/components/CreatePipeline.svelte`
  - Conteúdo: Modal para criar novo pipeline
  - Estimativa: 30min

- [ ] **T-047**: Criar Pipeline.svelte (view principal)
  - Arquivo: `plugins/crm-resources/src/components/Pipeline.svelte`
  - Conteúdo: View que utiliza Kanban nativo do task system
  - Estimativa: 40min

### 5.3 Componentes de Customer

- [ ] **T-048**: Criar Customers.svelte
  - Arquivo: `plugins/crm-resources/src/components/Customers.svelte`
  - Conteúdo: Lista de Contacts com mixin CrmCustomer
  - Estimativa: 35min

- [ ] **T-049**: Criar CustomerPresenter.svelte
  - Arquivo: `plugins/crm-resources/src/components/CustomerPresenter.svelte`
  - Conteúdo: Card de customer com leads count e total value
  - Estimativa: 25min

### 5.4 Registrar Components

- [ ] **T-050**: Registrar todos os componentes no plugin
  - Arquivo: `plugins/crm-resources/src/index.ts`
  - Conteúdo: Export map de component ID -> Svelte component
  - Critério: Todos os crm.component.* resolvem
  - Estimativa: 20min

- [ ] **T-051**: Testar renderização dos componentes
  - Comando: `rush dev`
  - Critério: Aplicação CRM aparece no sidebar, componentes renderizam
  - Estimativa: 30min

---

## Épico 6: Server Plugin (API REST)
**Estimativa:** 5h | **Prioridade:** P1

### 6.1 Setup Server Plugin

- [ ] **T-052**: Configurar Express router no server plugin
  - Arquivo: `server-plugins/crm/src/index.ts`
  - Conteúdo: Router para /api/v1/crm/*
  - Estimativa: 20min

- [ ] **T-053**: Criar middleware de autenticação API key
  - Arquivo: `server-plugins/crm/src/middleware/auth.ts`
  - Lógica: Valida X-API-Key header, resolve workspace
  - Critério: Requests sem key retornam 401
  - Estimativa: 30min

- [ ] **T-054**: Criar middleware de rate limiting
  - Arquivo: `server-plugins/crm/src/middleware/rateLimit.ts`
  - Lógica: 100 req/min por API key
  - Estimativa: 25min

### 6.2 Endpoints de Lead

- [ ] **T-055**: Implementar POST /api/v1/crm/leads
  - Arquivo: `server-plugins/crm/src/routes/leads.ts`
  - Lógica: Valida com Zod, verifica duplicidade, cria via TxOperations
  - Critério: AC-10 (201 com lead_id)
  - Estimativa: 40min

- [ ] **T-056**: Implementar GET /api/v1/crm/leads
  - Lógica: Filtros, paginação via client.findAll
  - Critério: Retorna lista paginada
  - Estimativa: 30min

- [ ] **T-057**: Implementar GET /api/v1/crm/leads/:id
  - Lógica: client.findOne com workspace isolation
  - Critério: 404 se não encontrado
  - Estimativa: 15min

- [ ] **T-058**: Implementar PATCH /api/v1/crm/leads/:id
  - Lógica: client.update com campos parciais
  - Critério: Retorna lead atualizado
  - Estimativa: 25min

- [ ] **T-059**: Implementar DELETE /api/v1/crm/leads/:id
  - Lógica: client.remove
  - Critério: 204 No Content
  - Estimativa: 15min

### 6.3 Endpoints de Form (público)

- [ ] **T-060**: Implementar POST /api/v1/crm/forms/:slug/submit
  - Arquivo: `server-plugins/crm/src/routes/forms.ts`
  - Lógica: Valida captcha (opcional), mapeia campos, cria lead
  - Critério: AC-13 (lead criado com UTMs)
  - Estimativa: 45min

- [ ] **T-061**: Implementar GET /api/v1/crm/forms/:slug/embed.js
  - Lógica: Retorna script de embed que captura UTMs
  - Estimativa: 35min

---

## Épico 7: Dashboard & Import
**Estimativa:** 7h | **Prioridade:** P2

### 7.1 Dashboard

- [ ] **T-062**: Criar Dashboard.svelte
  - Arquivo: `plugins/crm-resources/src/components/Dashboard.svelte`
  - Conteúdo: Layout com filtro de período e cards de KPI
  - Estimativa: 45min

- [ ] **T-063**: Criar KPICard.svelte
  - Arquivo: `plugins/crm-resources/src/components/dashboard/KPICard.svelte`
  - Props: title, value, change, trend
  - Estimativa: 20min

- [ ] **T-064**: Criar FunnelChart.svelte
  - Arquivo: `plugins/crm-resources/src/components/dashboard/FunnelChart.svelte`
  - Conteúdo: Gráfico de funil com conversão por estágio
  - Estimativa: 40min

- [ ] **T-065**: Criar TrendChart.svelte
  - Arquivo: `plugins/crm-resources/src/components/dashboard/TrendChart.svelte`
  - Conteúdo: Line chart de leads ao longo do tempo
  - Estimativa: 35min

- [ ] **T-066**: Implementar queries de métricas
  - Arquivo: `plugins/crm-resources/src/utils/analytics.ts`
  - Lógica: client.findAll com agregações para métricas
  - Critério: AC-18, AC-19
  - Estimativa: 40min

### 7.2 Importação

- [ ] **T-067**: Criar ImportWizard.svelte
  - Arquivo: `plugins/crm-resources/src/components/import/ImportWizard.svelte`
  - Conteúdo: Wizard multi-step (Upload → Mapping → Preview → Import)
  - Estimativa: 60min

- [ ] **T-068**: Criar FileUpload.svelte
  - Arquivo: `plugins/crm-resources/src/components/import/FileUpload.svelte`
  - Conteúdo: Drag & drop zone para CSV/XLSX
  - Estimativa: 30min

- [ ] **T-069**: Criar ColumnMapping.svelte
  - Arquivo: `plugins/crm-resources/src/components/import/ColumnMapping.svelte`
  - Conteúdo: Mapeamento de colunas do arquivo para campos do lead
  - Estimativa: 40min

- [ ] **T-070**: Implementar parser de CSV/XLSX
  - Arquivo: `plugins/crm-resources/src/utils/import-parser.ts`
  - Dependências: papaparse, xlsx
  - Critério: Retorna preview e valida dados
  - Estimativa: 45min

- [ ] **T-071**: Implementar importação em batch
  - Arquivo: `plugins/crm-resources/src/utils/import-processor.ts`
  - Lógica: Cria leads em chunks, reporta progresso
  - Critério: AC-14, AC-15, AC-16
  - Estimativa: 50min

---

## Validação Final

- [ ] **T-072**: Build de produção completo
  - Comando: `rush build`
  - Critério: exit 0, sem erros TypeScript
  - Estimativa: 15min

---

## Mapeamento AC → Tasks

| Acceptance Criteria | Tasks que validam |
|---------------------|-------------------|
| AC-01: Criar lead válido | T-041, T-055 |
| AC-02: Duplicidade de lead | T-055 |
| AC-03: Marketing não pode criar | T-053 (permissões) |
| AC-04: Paginação de lista | T-056 |
| AC-05: Filtro por estágio | T-045, T-056 |
| AC-06: Pipeline com colunas | T-032, T-047 |
| AC-07: Drag & drop muda estágio | T-032 (Kanban nativo) |
| AC-08: Bloqueio de não-owner | T-042 (EditLead) |
| AC-09: Modal de conversão | T-042 |
| AC-10: API POST leads | T-055 |
| AC-11: API key inválida | T-053 |
| AC-12: Payload inválido | T-055 (Zod) |
| AC-13: Form submit com UTMs | T-060 |
| AC-14: Preview importação | T-067, T-070 |
| AC-15: Progresso importação | T-071 |
| AC-16: Ignorar duplicados | T-071 |
| AC-17: Relatório de erros | T-071 |
| AC-18: Dashboard com métricas | T-062, T-066 |
| AC-19: Filtro de período | T-062, T-066 |
| AC-20: Click em gráfico filtra | T-064, T-065 |
| AC-21: Round-robin | T-041 (CreateLead com auto-assign) |
| AC-22: Notificação de novo lead | Herda de task system |
| AC-23: Admin edita qualquer lead | T-042 |
| AC-24: Sales vê mas não edita | T-042 |
| AC-25: Marketing sem criar lead | T-053 |
| AC-ERROR-01: API indisponível | T-055 (error handling) |
| AC-ERROR-02: Lead convertido não exclui | T-042, T-059 |
| AC-ERROR-03: Sessão expira | T-053 |

---

## Próximos Passos

1. **Setup**: Executar T-001 a T-010 para preparar ambiente
2. **Plugin**: Executar T-011 a T-018 para namespace e types
3. **Model**: Executar T-019 a T-031 para classes e SpaceType
4. **Verificar**: `rush build` deve passar sem erros
5. **UI**: Começar componentes Svelte (T-041+)

---

**Autor:** Claude (spec:tasks v2)
**Atualizado:** 2026-03-16 — Adaptado para arquitetura Huly nativa
