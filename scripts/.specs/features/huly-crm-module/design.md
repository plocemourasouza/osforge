# Design: Huly CRM Module (Adaptado)
**Feature:** huly-crm-module | **Data:** 2026-03-16 | **Status:** Draft v2
**Referência:** [spec.md](./spec.md) | Arquitetura Huly Platform

---

## Arquitetura Adaptada

### Visão Geral

O módulo CRM segue a **arquitetura real do Huly Platform**:
- **Models com Decorators** (`@Model`, `@Mixin`, `@Prop`)
- **Herança de Classes** (TTask, TProject, TContact)
- **Sistema de SpaceType** para pipeline/stages
- **Viewlets** para diferentes visualizações (Kanban, Table, List)
- **Componentes Svelte** para UI

```
┌─────────────────────────────────────────────────────────────────────┐
│                         HULY PLATFORM                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  models/                        plugins/                             │
│  ├── crm/                       ├── crm/           (namespace)       │
│  │   ├── types.ts               ├── crm-assets/    (icons)           │
│  │   ├── index.ts               └── crm-resources/ (components)      │
│  │   ├── spaceType.ts                                                │
│  │   ├── migration.ts           server-plugins/                      │
│  │   └── permissions.ts         └── crm/           (triggers, api)   │
│  └── server-crm/                                                     │
│                                                                      │
├─────────────────────────────────────────────────────────────────────┤
│  Core Platform Services                                              │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐               │
│  │ Contact  │ │  Task    │ │ Activity │ │  View    │               │
│  │ (people) │ │ (tasks)  │ │ (logs)   │ │ (UI)     │               │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘               │
└─────────────────────────────────────────────────────────────────────┘
```

### Estrutura de Diretórios

```
huly-platform/
├── models/
│   ├── crm/                              # Model definitions
│   │   ├── src/
│   │   │   ├── index.ts                  # createModel() + viewlets + actions
│   │   │   ├── types.ts                  # @Model, @Mixin classes
│   │   │   ├── plugin.ts                 # IDs namespace
│   │   │   ├── spaceType.ts              # Pipeline stages
│   │   │   ├── migration.ts              # Schema versioning
│   │   │   └── permissions.ts            # Access control
│   │   └── package.json
│   │
│   └── server-crm/                       # Server-side model config
│       └── src/
│           └── index.ts                  # Triggers, presenters
│
├── plugins/
│   ├── crm/                              # Plugin namespace
│   │   └── src/
│   │       ├── index.ts                  # plugin() definition
│   │       └── analytics.ts
│   │
│   ├── crm-assets/                       # Visual assets
│   │   └── src/
│   │       ├── index.ts
│   │       └── icons.ts
│   │
│   └── crm-resources/                    # UI Components
│       └── src/
│           ├── index.ts                  # Export resources
│           ├── plugin.ts
│           └── components/
│               ├── CreateLead.svelte
│               ├── EditLead.svelte
│               ├── LeadPresenter.svelte
│               ├── KanbanCard.svelte
│               ├── Pipeline.svelte
│               ├── Dashboard.svelte
│               ├── ImportWizard.svelte
│               └── FormBuilder.svelte
│
└── server-plugins/
    └── crm/                              # Backend services
        └── src/
            ├── index.ts
            ├── api/                      # REST endpoints
            ├── triggers/                 # Event handlers
            └── functions/                # Server functions
```

---

## Modelo de Dados

### Domain Types (plugins/crm/src/index.ts)

```typescript
import type { Contact } from '@hcengineering/contact'
import type { Task, Project, TaskType } from '@hcengineering/task'
import type {
  Ref, Doc, Class, Mixin, Status, Timestamp,
  Markup, MarkupBlobRef, Permission, Attribute
} from '@hcengineering/core'
import type { Asset, IntlString, Plugin } from '@hcengineering/platform'
import { plugin } from '@hcengineering/platform'

/**
 * CRM Lead - extends Task for workflow capabilities
 */
export interface CrmLead extends Task {
  space: Ref<CrmPipeline>
  attachedTo: Ref<CrmCustomer>
  status: Ref<Status>

  // Contact info
  email?: string
  phone?: string

  // Company
  companyName?: string
  jobTitle?: string

  // Location
  city?: string
  state?: string
  country?: string

  // CRM fields
  score: number
  value?: number

  // Source tracking
  source?: Ref<CrmSource>
  campaign?: Ref<CrmCampaign>
  utmSource?: string
  utmMedium?: string
  utmCampaign?: string

  // Conversion
  convertedAt?: Timestamp
  lostReason?: string
}

/**
 * CRM Pipeline - extends Project (like Funnel in lead plugin)
 */
export interface CrmPipeline extends Project {
  description?: Markup
  defaultOwner?: Ref<Employee>
}

/**
 * CRM Customer - mixin on Contact
 */
export interface CrmCustomer extends Contact {
  leads?: number
  totalValue?: number
  customerSince?: Timestamp
  notes?: MarkupBlobRef
}

/**
 * CRM Source - lead origin
 */
export interface CrmSource extends Doc {
  name: string
  isActive: boolean
}

/**
 * CRM Campaign
 */
export interface CrmCampaign extends Doc {
  name: string
  source?: Ref<CrmSource>
  startDate?: Timestamp
  endDate?: Timestamp
  budget?: number
  isActive: boolean
}

/**
 * CRM Form - capture form definition
 */
export interface CrmForm extends Doc {
  name: string
  slug: string
  campaign?: Ref<CrmCampaign>
  defaultPipeline?: Ref<CrmPipeline>
  captchaEnabled: boolean
  successMessage: string
  redirectUrl?: string
  isActive: boolean
  submissionsCount: number
  fields: CrmFormField[]
}

export interface CrmFormField {
  name: string
  label: string
  type: 'text' | 'email' | 'phone' | 'select' | 'textarea'
  required: boolean
  position: number
  leadField?: string
}

/**
 * Plugin ID
 */
export const crmId = 'crm' as Plugin

/**
 * Plugin namespace
 */
const crm = plugin(crmId, {
  app: {
    CRM: '' as Ref<Doc>
  },
  class: {
    CrmLead: '' as Ref<Class<CrmLead>>,
    CrmPipeline: '' as Ref<Class<CrmPipeline>>,
    CrmSource: '' as Ref<Class<CrmSource>>,
    CrmCampaign: '' as Ref<Class<CrmCampaign>>,
    CrmForm: '' as Ref<Class<CrmForm>>
  },
  mixin: {
    CrmCustomer: '' as Ref<Mixin<CrmCustomer>>
  },
  component: {
    CreateLead: '' as AnyComponent,
    EditLead: '' as AnyComponent,
    LeadPresenter: '' as AnyComponent,
    KanbanCard: '' as AnyComponent,
    Pipeline: '' as AnyComponent,
    Dashboard: '' as AnyComponent,
    ImportWizard: '' as AnyComponent,
    CreatePipeline: '' as AnyComponent,
    FormBuilder: '' as AnyComponent,
    MyLeads: '' as AnyComponent,
    Customers: '' as AnyComponent
  },
  function: {
    LeadTitleProvider: '' as Resource<TitleProvider>,
    LeadIdProvider: '' as Resource<IdProvider>
  },
  string: {
    CRM: '' as IntlString,
    Lead: '' as IntlString,
    Leads: '' as IntlString,
    Pipeline: '' as IntlString,
    Pipelines: '' as IntlString,
    Customer: '' as IntlString,
    Customers: '' as IntlString,
    CreateLead: '' as IntlString,
    MyLeads: '' as IntlString,
    Dashboard: '' as IntlString,
    Import: '' as IntlString,
    Forms: '' as IntlString,
    Source: '' as IntlString,
    Campaign: '' as IntlString,
    Score: '' as IntlString,
    Value: '' as IntlString
  },
  icon: {
    CRM: '' as Asset,
    Lead: '' as Asset,
    Pipeline: '' as Asset,
    Customer: '' as Asset,
    Dashboard: '' as Asset,
    Import: '' as Asset,
    Form: '' as Asset
  },
  attribute: {
    State: '' as Ref<Attribute<Status>>
  },
  descriptors: {
    PipelineType: '' as Ref<ProjectTypeDescriptor>,
    LeadType: '' as Ref<TaskTypeDescriptor>
  },
  taskType: {
    Lead: '' as Ref<TaskType>
  },
  template: {
    DefaultPipeline: '' as Ref<ProjectType>
  },
  space: {
    DefaultPipeline: '' as Ref<CrmPipeline>
  },
  permission: {
    CreatePipeline: '' as Ref<Permission>,
    ImportLeads: '' as Ref<Permission>,
    ManageForms: '' as Ref<Permission>,
    ViewDashboard: '' as Ref<Permission>
  },
  viewlet: {
    KanbanLead: '' as Ref<Viewlet>,
    TableLead: '' as Ref<Viewlet>,
    ListLead: '' as Ref<Viewlet>
  },
  ids: {
    LeadNotificationGroup: '' as Ref<NotificationGroup>
  }
})

export default crm
```

### Model Classes (models/crm/src/types.ts)

```typescript
import {
  IndexKind,
  type Ref,
  type Status,
  type Timestamp,
  type MarkupBlobRef
} from '@hcengineering/core'
import { type Employee } from '@hcengineering/contact'
import { type CrmLead, type CrmPipeline, type CrmCustomer, type CrmSource, type CrmCampaign, type CrmForm } from '@hcengineering/crm'
import {
  Collection,
  Index,
  Mixin,
  Model,
  Prop,
  ReadOnly,
  TypeDate,
  TypeMarkup,
  TypeNumber,
  TypeRef,
  TypeString,
  TypeBoolean,
  UX
} from '@hcengineering/model'
import contact, { TContact } from '@hcengineering/model-contact'
import core, { TDoc } from '@hcengineering/model-core'
import task, { TProject, TTask } from '@hcengineering/model-task'
import attachment from '@hcengineering/model-attachment'
import chunter from '@hcengineering/model-chunter'

import crm from './plugin'

// ============================================
// CRM PIPELINE (extends Project)
// ============================================

@Model(crm.class.CrmPipeline, task.class.Project)
@UX(crm.string.Pipeline, crm.icon.Pipeline)
export class TCrmPipeline extends TProject implements CrmPipeline {
  @Prop(TypeMarkup(), crm.string.Description)
  @Index(IndexKind.FullText)
    description?: string

  @Prop(TypeRef(contact.mixin.Employee), crm.string.DefaultOwner)
    defaultOwner?: Ref<Employee>

  @Prop(Collection(attachment.class.Attachment), attachment.string.Attachments)
    attachments?: number

  @Prop(Collection(chunter.class.ChatMessage), chunter.string.Comments)
    comments?: number
}

// ============================================
// CRM LEAD (extends Task)
// ============================================

@Model(crm.class.CrmLead, task.class.Task)
@UX(crm.string.Lead, crm.icon.Lead, 'CRM', 'title', undefined, crm.string.Leads)
export class TCrmLead extends TTask implements CrmLead {
  @Prop(TypeRef(contact.class.Contact), crm.string.Customer)
  @ReadOnly()
  declare attachedTo: Ref<CrmCustomer>

  declare space: Ref<CrmPipeline>

  @Prop(TypeRef(core.class.Status), task.string.TaskState, { _id: crm.attribute.State })
  declare status: Ref<Status>

  @Prop(TypeString(), crm.string.Title)
  @Index(IndexKind.FullText)
    title!: string

  // Contact info
  @Prop(TypeString(), crm.string.Email)
  @Index(IndexKind.FullText)
    email?: string

  @Prop(TypeString(), crm.string.Phone)
    phone?: string

  // Company
  @Prop(TypeString(), crm.string.Company)
  @Index(IndexKind.FullText)
    companyName?: string

  @Prop(TypeString(), crm.string.JobTitle)
    jobTitle?: string

  // Location
  @Prop(TypeString(), crm.string.City)
    city?: string

  @Prop(TypeString(), crm.string.State)
    state?: string

  @Prop(TypeString(), crm.string.Country)
    country?: string

  // CRM fields
  @Prop(TypeNumber(), crm.string.Score)
    score!: number

  @Prop(TypeNumber(), crm.string.Value)
    value?: number

  // Source tracking
  @Prop(TypeRef(crm.class.CrmSource), crm.string.Source)
    source?: Ref<CrmSource>

  @Prop(TypeRef(crm.class.CrmCampaign), crm.string.Campaign)
    campaign?: Ref<CrmCampaign>

  @Prop(TypeString(), crm.string.UTMSource)
    utmSource?: string

  @Prop(TypeString(), crm.string.UTMMedium)
    utmMedium?: string

  @Prop(TypeString(), crm.string.UTMCampaign)
    utmCampaign?: string

  // Assignee
  @Prop(TypeRef(contact.mixin.Employee), crm.string.Assignee)
  declare assignee: Ref<Employee> | null

  // Dates
  @Prop(TypeDate(), task.string.StartDate)
    startDate!: Timestamp | null

  @Prop(TypeDate(), crm.string.ConvertedAt)
    convertedAt?: Timestamp

  @Prop(TypeString(), crm.string.LostReason)
    lostReason?: string
}

// ============================================
// CRM CUSTOMER (Mixin on Contact)
// ============================================

@Mixin(crm.mixin.CrmCustomer, contact.class.Contact)
@UX(crm.string.Customer, crm.icon.Customer, undefined, undefined, undefined, crm.string.Customers)
export class TCrmCustomer extends TContact implements CrmCustomer {
  @Prop(Collection(crm.class.CrmLead), crm.string.Leads)
    leads?: number

  @Prop(TypeNumber(), crm.string.TotalValue)
    totalValue?: number

  @Prop(TypeDate(), crm.string.CustomerSince)
    customerSince?: Timestamp

  @Prop(TypeMarkup(), crm.string.Notes)
  @Index(IndexKind.FullText)
    notes?: MarkupBlobRef
}

// ============================================
// CRM SOURCE
// ============================================

@Model(crm.class.CrmSource, core.class.Doc)
@UX(crm.string.Source, crm.icon.Source)
export class TCrmSource extends TDoc implements CrmSource {
  @Prop(TypeString(), crm.string.Name)
  @Index(IndexKind.FullText)
    name!: string

  @Prop(TypeBoolean(), crm.string.Active)
    isActive!: boolean
}

// ============================================
// CRM CAMPAIGN
// ============================================

@Model(crm.class.CrmCampaign, core.class.Doc)
@UX(crm.string.Campaign, crm.icon.Campaign)
export class TCrmCampaign extends TDoc implements CrmCampaign {
  @Prop(TypeString(), crm.string.Name)
  @Index(IndexKind.FullText)
    name!: string

  @Prop(TypeRef(crm.class.CrmSource), crm.string.Source)
    source?: Ref<CrmSource>

  @Prop(TypeDate(), crm.string.StartDate)
    startDate?: Timestamp

  @Prop(TypeDate(), crm.string.EndDate)
    endDate?: Timestamp

  @Prop(TypeNumber(), crm.string.Budget)
    budget?: number

  @Prop(TypeBoolean(), crm.string.Active)
    isActive!: boolean
}

// ============================================
// CRM FORM (for lead capture)
// ============================================

@Model(crm.class.CrmForm, core.class.Doc)
@UX(crm.string.Form, crm.icon.Form)
export class TCrmForm extends TDoc implements CrmForm {
  @Prop(TypeString(), crm.string.Name)
  @Index(IndexKind.FullText)
    name!: string

  @Prop(TypeString(), crm.string.Slug)
    slug!: string

  @Prop(TypeRef(crm.class.CrmCampaign), crm.string.Campaign)
    campaign?: Ref<CrmCampaign>

  @Prop(TypeRef(crm.class.CrmPipeline), crm.string.DefaultPipeline)
    defaultPipeline?: Ref<CrmPipeline>

  @Prop(TypeBoolean(), crm.string.CaptchaEnabled)
    captchaEnabled!: boolean

  @Prop(TypeString(), crm.string.SuccessMessage)
    successMessage!: string

  @Prop(TypeString(), crm.string.RedirectUrl)
    redirectUrl?: string

  @Prop(TypeBoolean(), crm.string.Active)
    isActive!: boolean

  @Prop(TypeNumber(), crm.string.Submissions)
    submissionsCount!: number

  // Fields stored as embedded array
  fields!: CrmFormField[]
}
```

### Pipeline Stages (models/crm/src/spaceType.ts)

```typescript
import { type Builder } from '@hcengineering/model'
import core from '@hcengineering/model-core'
import task from '@hcengineering/model-task'
import { PaletteColorIndexes } from '@hcengineering/ui'

import crm from './plugin'

/**
 * Default CRM Pipeline Stages
 */
export const defaultCrmStatuses = [
  {
    id: crm.taskTypeStatus.New,
    name: 'New',
    color: PaletteColorIndexes.Coin,
    category: task.statusCategory.UnStarted
  },
  {
    id: crm.taskTypeStatus.Contacted,
    name: 'Contacted',
    color: PaletteColorIndexes.Arctic,
    category: task.statusCategory.Active
  },
  {
    id: crm.taskTypeStatus.Qualified,
    name: 'Qualified',
    color: PaletteColorIndexes.Cerulean,
    category: task.statusCategory.Active
  },
  {
    id: crm.taskTypeStatus.Proposal,
    name: 'Proposal',
    color: PaletteColorIndexes.Waterway,
    category: task.statusCategory.Active
  },
  {
    id: crm.taskTypeStatus.Negotiation,
    name: 'Negotiation',
    color: PaletteColorIndexes.Sunshine,
    category: task.statusCategory.Active
  },
  {
    id: crm.taskTypeStatus.Won,
    name: 'Won',
    color: PaletteColorIndexes.Grass,
    category: task.statusCategory.Won
  },
  {
    id: crm.taskTypeStatus.Lost,
    name: 'Lost',
    color: PaletteColorIndexes.Firework,
    category: task.statusCategory.Lost
  }
]

export function defineSpaceType (builder: Builder): void {
  // Task Type Descriptor (Lead)
  builder.createDoc(task.class.TaskTypeDescriptor, core.space.Model, {
    baseClass: crm.class.CrmLead,
    name: crm.string.Lead,
    description: crm.string.LeadDescription,
    icon: crm.icon.Lead,
    allowCreate: true
  }, crm.descriptors.LeadType)

  // Project Type Descriptor (Pipeline)
  builder.createDoc(task.class.ProjectTypeDescriptor, core.space.Model, {
    name: crm.string.CRM,
    description: crm.string.PipelineDescription,
    icon: crm.icon.Pipeline,
    baseClass: crm.class.CrmPipeline,
    allowedTaskTypeDescriptors: [crm.descriptors.LeadType]
  }, crm.descriptors.PipelineType)

  // Create default statuses
  for (const status of defaultCrmStatuses) {
    builder.createDoc(core.class.Status, core.space.Model, {
      name: status.name,
      color: status.color,
      category: status.category,
      ofAttribute: crm.attribute.State
    }, status.id)
  }

  // Task Type (Lead)
  builder.createDoc(task.class.TaskType, core.space.Model, {
    name: 'Lead',
    descriptor: crm.descriptors.LeadType,
    ofClass: crm.class.CrmLead,
    targetClass: crm.class.CrmLead,
    statuses: defaultCrmStatuses.map(s => s.id),
    statusCategories: [
      task.statusCategory.UnStarted,
      task.statusCategory.Active,
      task.statusCategory.Won,
      task.statusCategory.Lost
    ],
    kind: 'both'
  }, crm.taskType.Lead)

  // Project Type (Default Pipeline)
  builder.createDoc(task.class.ProjectType, core.space.Model, {
    name: 'Sales Pipeline',
    description: 'Default sales pipeline template',
    descriptor: crm.descriptors.PipelineType,
    tasks: [crm.taskType.Lead],
    statuses: defaultCrmStatuses.map(s => ({
      _id: s.id,
      taskType: crm.taskType.Lead
    })),
    classic: true
  }, crm.template.DefaultPipeline)
}
```

---

## Viewlets (Visualizações)

```typescript
// models/crm/src/index.ts (excerpt)

export function createModel (builder: Builder): void {
  // Register model classes
  builder.createModel(TCrmPipeline, TCrmLead, TCrmCustomer, TCrmSource, TCrmCampaign, TCrmForm)

  // ============================================
  // KANBAN VIEWLET
  // ============================================
  builder.createDoc(view.class.Viewlet, core.space.Model, {
    attachTo: crm.class.CrmLead,
    descriptor: task.viewlet.Kanban,
    config: [
      'attachedTo',
      'companyName',
      'value',
      'assignee',
      'dueDate'
    ],
    viewOptions: {
      groupBy: ['status'],
      orderBy: [['modifiedOn', SortingOrder.Descending]],
      other: [
        {
          key: 'shouldShowAll',
          type: 'toggle',
          defaultValue: false,
          label: view.string.ShowAll
        }
      ]
    }
  }, crm.viewlet.KanbanLead)

  // ============================================
  // TABLE VIEWLET
  // ============================================
  builder.createDoc(view.class.Viewlet, core.space.Model, {
    attachTo: crm.class.CrmLead,
    descriptor: task.viewlet.StatusTable,
    config: [
      '',
      'title',
      'attachedTo',
      'companyName',
      'email',
      'phone',
      'status',
      'assignee',
      'score',
      'value',
      'source',
      'modifiedOn'
    ],
    configOptions: {
      sortable: true
    }
  }, crm.viewlet.TableLead)

  // ============================================
  // LIST VIEWLET
  // ============================================
  builder.createDoc(view.class.Viewlet, core.space.Model, {
    attachTo: crm.class.CrmLead,
    descriptor: view.viewlet.List,
    config: [
      { key: 'status', props: { kind: 'list', size: 'small' } },
      { key: '', displayProps: { grow: true } },
      { key: 'companyName' },
      { key: 'assignee', displayProps: { fixed: 'right' } },
      { key: 'score', props: { kind: 'list' } },
      { key: 'modifiedOn', displayProps: { fixed: 'right' } }
    ]
  }, crm.viewlet.ListLead)

  // ============================================
  // PRESENTERS
  // ============================================
  builder.mixin(crm.class.CrmLead, core.class.Class, view.mixin.ObjectPresenter, {
    presenter: crm.component.LeadPresenter
  })

  builder.mixin(crm.class.CrmLead, core.class.Class, view.mixin.ObjectEditor, {
    editor: crm.component.EditLead
  })

  builder.mixin(crm.class.CrmLead, core.class.Class, view.mixin.ObjectTitle, {
    titleProvider: crm.function.LeadTitleProvider
  })

  builder.mixin(crm.class.CrmLead, core.class.Class, view.mixin.ObjectIdentifier, {
    provider: crm.function.LeadIdProvider
  })

  // ============================================
  // APPLICATION (Sidebar)
  // ============================================
  builder.createDoc(
    workbench.class.Application,
    core.space.Model,
    {
      label: crm.string.CRM,
      icon: crm.icon.CRM,
      alias: crmId,
      hidden: false,
      position: 'top',
      navigatorModel: {
        specials: [
          {
            id: 'my-leads',
            label: crm.string.MyLeads,
            icon: crm.icon.Lead,
            component: crm.component.MyLeads,
            position: 'top'
          },
          {
            id: 'customers',
            label: crm.string.Customers,
            icon: crm.icon.Customer,
            component: crm.component.Customers,
            position: 'top'
          },
          {
            id: 'dashboard',
            label: crm.string.Dashboard,
            icon: crm.icon.Dashboard,
            component: crm.component.Dashboard,
            position: 'bottom'
          }
        ],
        spaces: [
          {
            label: crm.string.Pipelines,
            spaceClass: crm.class.CrmPipeline,
            addSpaceLabel: crm.string.CreatePipeline,
            createComponent: crm.component.CreatePipeline,
            visibleIf: crm.function.CanCreatePipeline
          }
        ]
      }
    },
    crm.app.CRM
  )

  // SpaceType, Permissions, Notifications...
  defineSpaceType(builder)
  definePermissions(builder)
  defineNotifications(builder)
}
```

---

## Decisões Técnicas (ADRs Atualizadas)

### ADR-001: Estender Task System do Huly
**Decisão:** CrmLead estende TTask, CrmPipeline estende TProject.

**Razão:** Aproveita todo o sistema de workflow, status, assignee, notificações e viewlets do Huly.

**Consequências:**
- Herda campos: status, assignee, dueDate, number, identifier
- Integração automática com Kanban do task system
- Notificações de assignment funcionam out-of-box

### ADR-002: Customer como Mixin
**Decisão:** CrmCustomer é um @Mixin de Contact, não uma entidade separada.

**Razão:** Permite que qualquer Contact seja "promovido" a Customer sem duplicar dados.

**Consequências:**
- Lead.attachedTo aponta para Contact (que pode ter mixin Customer)
- Preserva todas as features de Contact (avatar, channels, etc.)

### ADR-003: Pipeline Stages via SpaceType
**Decisão:** Usar o sistema de TaskType/ProjectType do Huly para definir estágios.

**Razão:** Consistência com outros módulos (tracker, lead), suporte nativo a customização.

**Consequências:**
- Estágios definidos em spaceType.ts
- Categorias: UnStarted, Active, Won, Lost
- Kanban agrupa automaticamente por status

### ADR-004: REST API via Server Plugin
**Decisão:** Criar endpoints REST em server-plugins/crm para integrações externas.

**Razão:** O sistema interno do Huly usa WebSocket/Transactor, mas integrações externas precisam de REST.

**Consequências:**
- Endpoints: POST/GET/PATCH /api/v1/crm/leads
- Autenticação via API keys separadas
- Rate limiting no middleware

### ADR-005: Forms como Doc Separado
**Decisão:** CrmForm é uma entidade Doc independente, não um mixin.

**Razão:** Forms precisam de configuração complexa (campos, captcha, redirect) e slug único.

**Consequências:**
- Endpoint público para submit (sem auth, com captcha)
- Slug único por workspace para URLs estáveis

---

## Componentes UI (Svelte)

### Estrutura de Componentes

```
plugins/crm-resources/src/components/
├── leads/
│   ├── CreateLead.svelte         # Modal de criação
│   ├── EditLead.svelte           # Painel de edição
│   ├── LeadPresenter.svelte      # Renderização inline
│   ├── KanbanCard.svelte         # Card no Kanban
│   ├── MyLeads.svelte            # Lista "Meus Leads"
│   └── LeadFilters.svelte        # Filtros da lista
├── pipeline/
│   ├── CreatePipeline.svelte     # Modal de criação
│   ├── Pipeline.svelte           # View principal do pipeline
│   └── StageConfig.svelte        # Config de estágios
├── customers/
│   ├── Customers.svelte          # Lista de customers
│   ├── CustomerPresenter.svelte  # Card de customer
│   └── CustomerDetail.svelte     # Detalhes
├── dashboard/
│   ├── Dashboard.svelte          # Dashboard principal
│   ├── KPICard.svelte            # Card de métrica
│   ├── FunnelChart.svelte        # Gráfico de funil
│   └── TrendChart.svelte         # Gráfico de tendência
├── import/
│   ├── ImportWizard.svelte       # Wizard de importação
│   ├── ColumnMapping.svelte      # Mapeamento de colunas
│   └── ImportProgress.svelte     # Progresso
└── forms/
    ├── FormBuilder.svelte        # Builder de formulários
    ├── FormPreview.svelte        # Preview
    └── EmbedCode.svelte          # Código de embed
```

### Exemplo: CreateLead.svelte

```svelte
<script lang="ts">
  import { createEventDispatcher } from 'svelte'
  import { getClient, SpaceSelector, UserBox } from '@hcengineering/presentation'
  import { Card, EditBox, Label, NumberInput } from '@hcengineering/ui'
  import { StatusSelector } from '@hcengineering/task-resources'
  import contact from '@hcengineering/contact'
  import crm, { CrmLead, CrmPipeline, CrmCustomer } from '@hcengineering/crm'

  export let space: Ref<CrmPipeline> | undefined = undefined

  let title = ''
  let email = ''
  let phone = ''
  let companyName = ''
  let customer: Ref<CrmCustomer> | null = null
  let status: Ref<Status> | undefined

  const client = getClient()
  const dispatch = createEventDispatcher()

  $: canSave = title.trim().length > 0 && (email.trim().length > 0 || phone.trim().length > 0)

  async function createLead () {
    if (space === undefined || status === undefined) return

    // Get next sequence number
    const sequence = await client.findOne(core.class.Sequence, {
      attachedTo: crm.class.CrmLead
    })
    const number = sequence ? sequence.sequence + 1 : 1
    await client.update(sequence, { $inc: { sequence: 1 } })

    // Ensure customer has CrmCustomer mixin
    if (customer !== null) {
      const customerDoc = await client.findOne(contact.class.Contact, { _id: customer })
      if (customerDoc && !client.getHierarchy().hasMixin(customerDoc, crm.mixin.CrmCustomer)) {
        await client.createMixin(
          customerDoc._id,
          customerDoc._class,
          customerDoc.space,
          crm.mixin.CrmCustomer,
          { totalValue: 0 }
        )
      }
    }

    const leadData: AttachedData<CrmLead> = {
      status,
      number,
      identifier: `CRM-${number}`,
      title,
      email: email || undefined,
      phone: phone || undefined,
      companyName: companyName || undefined,
      score: 0,
      startDate: Date.now(),
      rank: ''
    }

    await client.addCollection(
      crm.class.CrmLead,
      space,
      customer ?? ('' as Ref<CrmCustomer>),
      crm.mixin.CrmCustomer,
      'leads',
      leadData
    )

    dispatch('close')
  }
</script>

<Card
  label={crm.string.CreateLead}
  okAction={createLead}
  canSave={canSave}
  on:close
>
  <svelte:fragment slot="header">
    <SpaceSelector
      _class={crm.class.CrmPipeline}
      label={crm.string.Pipeline}
      bind:space
    />
  </svelte:fragment>

  <div class="flex-col gap-4">
    <EditBox
      label={crm.string.Title}
      bind:value={title}
      placeholder="Nome do lead"
      focus
    />

    <div class="flex-row gap-4">
      <EditBox
        label={crm.string.Email}
        bind:value={email}
        placeholder="email@example.com"
      />
      <EditBox
        label={crm.string.Phone}
        bind:value={phone}
        placeholder="+55 11 99999-9999"
      />
    </div>

    <EditBox
      label={crm.string.Company}
      bind:value={companyName}
      placeholder="Empresa"
    />

    <UserBox
      _class={contact.class.Contact}
      label={crm.string.Customer}
      bind:value={customer}
      allowDeselect
    />

    {#if space}
      <StatusSelector
        space={space}
        _class={crm.class.CrmLead}
        bind:value={status}
      />
    {/if}
  </div>
</Card>
```

---

## API REST (server-plugins/crm)

```typescript
// server-plugins/crm/src/api/leads.ts

import { Router } from 'express'
import { z } from 'zod'
import { TxOperations } from '@hcengineering/core'
import crm from '@hcengineering/crm'

const CreateLeadSchema = z.object({
  title: z.string().min(1).max(200),
  email: z.string().email().optional(),
  phone: z.string().max(30).optional(),
  companyName: z.string().max(200).optional(),
  pipelineId: z.string(),
  statusId: z.string().optional(),
  ownerId: z.string().optional(),
  utmSource: z.string().optional(),
  utmMedium: z.string().optional(),
  utmCampaign: z.string().optional()
}).refine(data => data.email || data.phone, {
  message: 'Email ou telefone é obrigatório'
})

export function createLeadRoutes (getClient: () => Promise<TxOperations>): Router {
  const router = Router()

  /**
   * POST /api/v1/crm/leads
   */
  router.post('/leads', async (req, res) => {
    try {
      const data = CreateLeadSchema.parse(req.body)
      const client = await getClient()

      // Check duplicate
      if (data.email) {
        const existing = await client.findOne(crm.class.CrmLead, { email: data.email })
        if (existing) {
          return res.status(200).json({ id: existing._id, duplicate: true })
        }
      }

      // Get sequence
      const sequence = await client.findOne(core.class.Sequence, {
        attachedTo: crm.class.CrmLead
      })
      const number = sequence ? sequence.sequence + 1 : 1
      await client.update(sequence, { $inc: { sequence: 1 } })

      // Create lead
      const lead = await client.createDoc(crm.class.CrmLead, data.pipelineId, {
        title: data.title,
        email: data.email,
        phone: data.phone,
        companyName: data.companyName,
        status: data.statusId || crm.taskTypeStatus.New,
        assignee: data.ownerId || null,
        utmSource: data.utmSource,
        utmMedium: data.utmMedium,
        utmCampaign: data.utmCampaign,
        number,
        identifier: `CRM-${number}`,
        score: 0,
        startDate: Date.now(),
        rank: ''
      })

      res.status(201).json({ id: lead, duplicate: false })
    } catch (error) {
      if (error instanceof z.ZodError) {
        return res.status(400).json({ errors: error.errors })
      }
      res.status(500).json({ error: 'Internal server error' })
    }
  })

  /**
   * GET /api/v1/crm/leads
   */
  router.get('/leads', async (req, res) => {
    const client = await getClient()
    const { page = 1, pageSize = 50, status, search } = req.query

    const query: any = {}
    if (status) query.status = status
    if (search) query.title = { $regex: search, $options: 'i' }

    const leads = await client.findAll(crm.class.CrmLead, query, {
      limit: Number(pageSize),
      skip: (Number(page) - 1) * Number(pageSize)
    })

    const total = await client.findAll(crm.class.CrmLead, query, { projection: { _id: 1 } })

    res.json({
      leads,
      total: total.length,
      page: Number(page),
      pageSize: Number(pageSize)
    })
  })

  return router
}
```

---

## Migrations

```typescript
// models/crm/src/migration.ts

import { type MigrateOperation } from '@hcengineering/model'
import { crmId } from '@hcengineering/crm'

export const crmOperation: MigrateOperation = {
  async migrate (client, mode): Promise<void> {
    // Initial migration - nothing to migrate yet
  },

  async upgrade (state, client, mode): Promise<void> {
    await tryUpgrade(mode, state, client, crmId, [
      {
        state: 'create-default-pipeline',
        func: async (client) => {
          const ops = new TxOperations(client, core.account.System)

          // Create default sources
          const sources = ['Website', 'Indicação', 'LinkedIn', 'Google Ads', 'Facebook Ads', 'Evento', 'Outro']
          for (const name of sources) {
            await ops.createDoc(crm.class.CrmSource, core.space.Model, {
              name,
              isActive: true
            })
          }
        }
      }
    ])
  }
}
```

---

## Resumo das Mudanças

| Aspecto | Design Original | Design Adaptado |
|---------|-----------------|-----------------|
| **Modelo de dados** | SQL/CockroachDB | @Model/@Mixin decorators |
| **Persistência** | Migrations SQL | Huly document system |
| **Lead** | Entidade independente | Estende TTask |
| **Pipeline** | Entidade independente | Estende TProject |
| **Customer** | Tabela separada | Mixin de Contact |
| **Stages** | Tabela crm_stage | SpaceType + StatusCategory |
| **Viewlets** | Componentes custom | Kanban/Table/List nativos |
| **Permissões** | RBAC próprio | Sistema de Permission do Huly |

---

**Autor:** Claude (spec:design v2)
**Próximo passo:** Atualizar tasks.md e iniciar implementação
