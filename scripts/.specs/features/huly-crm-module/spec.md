# Spec: Huly CRM Module
**Feature:** huly-crm-module | **Data:** 2026-03-15 | **Status:** Draft
**Referência:** [discovery.md](./discovery.md)

## Contexto

Equipes de vendas e marketing que usam Huly precisam gerenciar leads de forma estruturada, mas o plugin `lead` atual é básico. Este módulo CRM nativo oferecerá gestão completa do ciclo de vida do lead (captura → qualificação → conversão) integrada ao ecossistema Huly, eliminando a necessidade de ferramentas externas.

---

## Requisitos Funcionais

### RF-01: Criar Lead Manualmente
- **Descrição:** Usuário cria um novo lead preenchendo formulário no sistema
- **Usuário:** Sales, Admin
- **Fluxo principal:**
  1. Usuário acessa módulo CRM > Leads
  2. Clica em "Novo Lead"
  3. Preenche campos obrigatórios (nome, email ou telefone)
  4. Preenche campos opcionais (empresa, cargo, origem, campanha, tags)
  5. Seleciona estágio inicial do pipeline
  6. Confirma criação
  7. Sistema valida dados, gera ID, atribui owner (usuário atual ou round-robin)
  8. Lead aparece no pipeline e lista
- **Fluxos alternativos:**
  - FA-01: Usuário cancela → dados descartados, retorna à lista
  - FA-02: Usuário salva como rascunho → lead com status "draft", não aparece no pipeline
- **Erros e exceções:**
  - E-01: Email inválido → mensagem inline, bloqueia submit
  - E-02: Lead duplicado (mesmo email) → modal de confirmação: "Lead existente. Mesclar ou criar novo?"
  - E-03: Campos obrigatórios vazios → highlight campos, mensagem de erro

### RF-02: Visualizar Lista de Leads
- **Descrição:** Usuário visualiza todos os leads do workspace em formato de tabela
- **Usuário:** Sales, Marketing, Admin
- **Fluxo principal:**
  1. Usuário acessa módulo CRM > Leads
  2. Sistema carrega lista paginada (50 itens/página)
  3. Exibe colunas: Nome, Email, Empresa, Estágio, Owner, Origem, Criado em
  4. Usuário pode ordenar por qualquer coluna
  5. Usuário pode buscar por texto (nome, email, empresa)
  6. Usuário pode filtrar por: estágio, owner, origem, tags, período
- **Fluxos alternativos:**
  - FA-01: Lista vazia → exibe empty state com CTA "Criar primeiro lead" ou "Importar leads"
  - FA-02: Filtros ativos → badge com contagem de filtros, botão "Limpar filtros"
- **Erros e exceções:**
  - E-01: Timeout na busca → mensagem "Busca demorou. Tente filtros mais específicos"

### RF-03: Visualizar Pipeline Kanban
- **Descrição:** Usuário visualiza leads organizados em colunas por estágio (Kanban)
- **Usuário:** Sales, Admin
- **Fluxo principal:**
  1. Usuário acessa CRM > Pipeline
  2. Sistema exibe colunas ordenadas por posição dos estágios
  3. Cada coluna mostra cards de leads naquele estágio
  4. Card exibe: nome, empresa, valor (se houver), owner avatar, tempo no estágio
  5. Contador de leads por coluna no header
- **Fluxos alternativos:**
  - FA-01: Muitos leads por estágio → scroll vertical dentro da coluna
  - FA-02: Usuário filtra por owner → apenas leads do owner selecionado
- **Erros e exceções:**
  - E-01: Estágio sem leads → coluna vazia com placeholder "Arraste leads aqui"

### RF-04: Mover Lead entre Estágios (Drag & Drop)
- **Descrição:** Usuário arrasta card de lead para outro estágio no pipeline
- **Usuário:** Sales, Admin
- **Fluxo principal:**
  1. Usuário clica e segura card do lead
  2. Arrasta para coluna de destino
  3. Solta o card
  4. Sistema atualiza estágio do lead
  5. Registra atividade "Movido de [origem] para [destino]"
  6. Dispara evento `lead_stage_changed`
- **Fluxos alternativos:**
  - FA-01: Drop na mesma coluna → reordena posição dentro do estágio
  - FA-02: Mover para "Convertido" → modal solicita dados de conversão (valor, data)
  - FA-03: Mover para "Perdido" → modal solicita motivo da perda
- **Erros e exceções:**
  - E-01: Sem permissão para editar lead → toast "Você não pode mover leads de outros owners"
  - E-02: Estágio bloqueado → visual feedback, card retorna à posição original

### RF-05: Visualizar Detalhes do Lead
- **Descrição:** Usuário acessa página completa de um lead específico
- **Usuário:** Sales, Marketing, Admin
- **Fluxo principal:**
  1. Usuário clica no lead (lista ou pipeline)
  2. Sistema abre painel lateral ou página dedicada
  3. Exibe seções:
     - Header: nome, empresa, estágio atual, owner
     - Dados de contato: email, telefone, endereço
     - Informações: cargo, origem, campanha, UTMs, score
     - Timeline: atividades em ordem cronológica reversa
     - Notas: lista de notas com autor e data
     - Tags: tags atribuídas com opção de editar
  4. Ações disponíveis: Editar, Converter, Marcar como Perdido, Excluir
- **Fluxos alternativos:**
  - FA-01: Lead convertido → exibe badge "Convertido" e link para Contact/Deal criado
  - FA-02: Lead perdido → exibe badge "Perdido" e motivo
- **Erros e exceções:**
  - E-01: Lead não encontrado (deletado) → redirect para lista com toast "Lead não existe"

### RF-06: Editar Lead
- **Descrição:** Usuário altera dados de um lead existente
- **Usuário:** Sales, Admin (owner do lead ou Admin)
- **Fluxo principal:**
  1. Usuário acessa detalhes do lead
  2. Clica em "Editar" ou edita inline
  3. Altera campos desejados
  4. Salva alterações
  5. Sistema valida e persiste
  6. Registra atividade "Lead atualizado: [campos alterados]"
  7. Dispara evento `lead_updated`
- **Fluxos alternativos:**
  - FA-01: Edição inline → salva ao perder foco do campo
  - FA-02: Cancelar edição → restaura valores anteriores
- **Erros e exceções:**
  - E-01: Conflito de edição (outro usuário editou) → modal "Dados foram alterados. Recarregar ou sobrescrever?"
  - E-02: Sem permissão → campos desabilitados, tooltip "Apenas o owner pode editar"

### RF-07: Adicionar Nota ao Lead
- **Descrição:** Usuário registra anotação textual no lead
- **Usuário:** Sales, Marketing, Admin
- **Fluxo principal:**
  1. Usuário acessa detalhes do lead
  2. Clica em "Adicionar nota"
  3. Digita texto da nota (suporta markdown básico)
  4. Opcionalmente menciona outros usuários (@usuario)
  5. Salva nota
  6. Nota aparece na timeline com autor e timestamp
  7. Se mencionou usuários, notifica-os
- **Fluxos alternativos:**
  - FA-01: Nota privada → checkbox "Apenas eu posso ver"
- **Erros e exceções:**
  - E-01: Nota vazia → botão salvar desabilitado

### RF-08: Registrar Atividade no Lead
- **Descrição:** Usuário registra interação com o lead (ligação, email, reunião)
- **Usuário:** Sales, Admin
- **Fluxo principal:**
  1. Usuário acessa detalhes do lead
  2. Clica em "Registrar atividade"
  3. Seleciona tipo: Ligação, Email, Reunião, WhatsApp, Outro
  4. Preenche descrição e resultado
  5. Opcionalmente agenda follow-up (cria task no Huly)
  6. Salva atividade
  7. Atividade aparece na timeline
  8. Dispara evento `lead_activity_created`
- **Fluxos alternativos:**
  - FA-01: Agendar follow-up → abre modal de criação de task integrado
- **Erros e exceções:**
  - E-01: Tipo obrigatório não selecionado → highlight campo

### RF-09: Capturar Lead via API REST
- **Descrição:** Sistema externo envia lead via endpoint autenticado
- **Usuário:** Sistema externo (API key)
- **Fluxo principal:**
  1. Sistema externo envia POST `/api/v1/crm/leads` com payload JSON
  2. API valida autenticação (API key no header)
  3. API valida payload (schema Zod)
  4. API verifica duplicidade por email
  5. Se único, cria lead com status "new"
  6. Atribui owner via round-robin ou owner especificado
  7. Retorna 201 com ID do lead criado
  8. Dispara evento `lead_created`
- **Fluxos alternativos:**
  - FA-01: Lead duplicado → retorna 200 com ID existente e flag `duplicate: true`
  - FA-02: Payload inclui `ownerId` → atribui ao owner especificado
- **Erros e exceções:**
  - E-01: API key inválida → 401 Unauthorized
  - E-02: Payload inválido → 400 Bad Request com detalhes de validação
  - E-03: Workspace não encontrado → 404 Not Found
  - E-04: Rate limit excedido → 429 Too Many Requests

### RF-10: Capturar Lead via Formulário Embeddável
- **Descrição:** Visitante preenche formulário em site externo e lead é criado
- **Usuário:** Visitante anônimo (site externo)
- **Fluxo principal:**
  1. Visitante acessa página com formulário embeddado
  2. Script captura UTMs da URL automaticamente
  3. Visitante preenche campos do formulário
  4. Clica em submit
  5. Script envia dados para endpoint público `/api/v1/crm/forms/{formId}/submit`
  6. API valida reCAPTCHA/hCaptcha
  7. API cria lead associado ao formulário/campanha
  8. Retorna sucesso
  9. Script exibe mensagem de confirmação ou redireciona
- **Fluxos alternativos:**
  - FA-01: Campos customizados → formulário renderiza campos definidos no builder
  - FA-02: Redirect URL configurado → redireciona após sucesso
- **Erros e exceções:**
  - E-01: Captcha inválido → não cria lead, exibe erro
  - E-02: Formulário desativado → 410 Gone
  - E-03: Campos obrigatórios faltando → 400 com lista de campos

### RF-11: Criar Formulário de Captura
- **Descrição:** Usuário cria formulário para captura de leads em sites externos
- **Usuário:** Marketing, Admin
- **Fluxo principal:**
  1. Usuário acessa CRM > Formulários > Novo
  2. Define nome do formulário
  3. Adiciona campos (drag & drop): Nome, Email, Telefone, Empresa, Custom
  4. Configura campos obrigatórios
  5. Associa a uma campanha (opcional)
  6. Define página de sucesso ou redirect URL
  7. Configura captcha (hCaptcha recomendado)
  8. Salva formulário
  9. Sistema gera código de embed (script + HTML)
- **Fluxos alternativos:**
  - FA-01: Preview do formulário → visualiza como aparecerá no site
  - FA-02: Duplicar formulário existente → copia configurações
- **Erros e exceções:**
  - E-01: Nome duplicado → "Já existe formulário com este nome"

### RF-12: Importar Leads via CSV/XLSX
- **Descrição:** Usuário importa leads em massa a partir de arquivo
- **Usuário:** Sales, Marketing, Admin
- **Fluxo principal:**
  1. Usuário acessa CRM > Importar
  2. Faz upload do arquivo (.csv ou .xlsx)
  3. Sistema faz parsing e exibe preview (primeiras 10 linhas)
  4. Usuário mapeia colunas do arquivo para campos do lead
  5. Sistema valida dados e identifica:
     - Leads válidos
     - Leads com erros (email inválido, campos obrigatórios faltando)
     - Leads duplicados (por email)
  6. Usuário escolhe ação para duplicados: ignorar, atualizar, criar novo
  7. Usuário confirma importação
  8. Sistema cria job de importação em background
  9. Exibe progresso em tempo real
  10. Ao concluir, exibe relatório: X criados, Y atualizados, Z erros
- **Fluxos alternativos:**
  - FA-01: Arquivo muito grande (>10MB) → upload chunked
  - FA-02: Salvar mapeamento → reutilizar em futuras importações
- **Erros e exceções:**
  - E-01: Arquivo inválido → "Formato não suportado. Use CSV ou XLSX"
  - E-02: Arquivo vazio → "Arquivo não contém dados"
  - E-03: Job falha → notifica usuário, permite retry

### RF-13: Configurar Pipeline e Estágios
- **Descrição:** Usuário configura estágios do pipeline de vendas
- **Usuário:** Admin
- **Fluxo principal:**
  1. Usuário acessa CRM > Configurações > Pipeline
  2. Visualiza estágios atuais em ordem
  3. Pode:
     - Adicionar novo estágio (nome, cor, posição)
     - Editar estágio existente
     - Reordenar estágios (drag & drop)
     - Excluir estágio (se não houver leads)
     - Definir estágio padrão para novos leads
  4. Salva configuração
- **Fluxos alternativos:**
  - FA-01: Excluir estágio com leads → "Mova os leads antes de excluir"
  - FA-02: Estágios "Convertido" e "Perdido" → não podem ser excluídos (sistema)
- **Erros e exceções:**
  - E-01: Nome de estágio duplicado → "Já existe estágio com este nome"
  - E-02: Menos de 2 estágios → "Pipeline precisa de pelo menos 2 estágios"

### RF-14: Visualizar Dashboard de Analytics
- **Descrição:** Usuário visualiza métricas e gráficos do CRM
- **Usuário:** Sales, Marketing, Admin
- **Fluxo principal:**
  1. Usuário acessa CRM > Dashboard
  2. Sistema exibe cards de KPIs:
     - Total de leads (período)
     - Leads por estágio
     - Taxa de conversão
     - Tempo médio de conversão
     - Leads por origem
     - Leads por owner
  3. Usuário pode filtrar por período (7d, 30d, 90d, custom)
  4. Gráficos:
     - Funil de conversão (bar chart)
     - Leads ao longo do tempo (line chart)
     - Distribuição por origem (pie chart)
     - Performance por vendedor (bar chart)
- **Fluxos alternativos:**
  - FA-01: Sem leads no período → exibe zeros com empty state
  - FA-02: Clique em segmento do gráfico → filtra lista de leads
- **Erros e exceções:**
  - E-01: Erro ao carregar métricas → retry automático, fallback para "Dados indisponíveis"

### RF-15: Configurar Automações Básicas
- **Descrição:** Usuário configura regras automáticas para leads
- **Usuário:** Admin
- **Fluxo principal:**
  1. Usuário acessa CRM > Configurações > Automações
  2. Visualiza automações disponíveis:
     - Atribuição round-robin de novos leads
     - Notificação ao owner quando lead criado
     - Notificação quando lead fica X dias sem atividade
     - Auto-mover para estágio quando condição atendida
  3. Ativa/desativa automações
  4. Configura parâmetros (ex: dias sem atividade = 7)
  5. Salva configuração
- **Fluxos alternativos:**
  - FA-01: Round-robin → seleciona quais usuários participam da rotação
- **Erros e exceções:**
  - E-01: Nenhum usuário no round-robin → "Selecione pelo menos um usuário"

### RF-16: Converter Lead em Contato/Oportunidade
- **Descrição:** Usuário converte lead qualificado em contato ou oportunidade
- **Usuário:** Sales, Admin
- **Fluxo principal:**
  1. Usuário acessa detalhes do lead
  2. Clica em "Converter"
  3. Modal exibe opções:
     - Criar Contato (com dados do lead)
     - Criar Empresa (se não existir)
     - Valor da oportunidade (opcional)
  4. Usuário confirma
  5. Sistema:
     - Cria Contact com dados do lead
     - Cria Company se selecionado
     - Move lead para estágio "Convertido"
     - Registra atividade de conversão
  6. Dispara evento `lead_converted`
- **Fluxos alternativos:**
  - FA-01: Contato já existe (mesmo email) → vincula ao existente
- **Erros e exceções:**
  - E-01: Lead já convertido → botão desabilitado

### RF-17: Gerenciar Permissões do CRM
- **Descrição:** Admin configura quem pode fazer o quê no CRM
- **Usuário:** Admin
- **Fluxo principal:**
  1. Admin acessa CRM > Configurações > Permissões
  2. Visualiza matriz de permissões por papel:
     - Admin: todas as permissões
     - Sales: CRUD leads próprios, visualizar todos, mover no pipeline
     - Marketing: visualizar leads, criar formulários, ver dashboard
  3. Pode criar papéis customizados
  4. Atribui papéis a usuários do workspace
  5. Salva configuração
- **Fluxos alternativos:**
  - FA-01: Papel customizado → seleciona permissões granulares
- **Erros e exceções:**
  - E-01: Remover último Admin → "Deve haver pelo menos um Admin"

### RF-18: Busca Global de Leads
- **Descrição:** Usuário busca leads por qualquer campo indexado
- **Usuário:** Sales, Marketing, Admin
- **Fluxo principal:**
  1. Usuário digita no campo de busca global
  2. Sistema busca em: nome, email, telefone, empresa, notas
  3. Exibe resultados em tempo real (debounce 300ms)
  4. Usuário clica no resultado para abrir lead
- **Fluxos alternativos:**
  - FA-01: Busca avançada → filtros combinados (AND/OR)
- **Erros e exceções:**
  - E-01: Nenhum resultado → "Nenhum lead encontrado. Tente outros termos"

### RF-19: Bulk Actions em Leads
- **Descrição:** Usuário executa ações em múltiplos leads simultaneamente
- **Usuário:** Sales, Admin
- **Fluxo principal:**
  1. Usuário seleciona múltiplos leads (checkbox) na lista
  2. Barra de ações aparece com opções:
     - Mover para estágio
     - Atribuir a owner
     - Adicionar tag
     - Remover tag
     - Excluir
  3. Usuário seleciona ação
  4. Confirma (para ações destrutivas)
  5. Sistema executa em batch
  6. Exibe resultado: "X leads atualizados"
- **Fluxos alternativos:**
  - FA-01: Selecionar todos da página → checkbox no header
  - FA-02: Selecionar todos do filtro → link "Selecionar todos os X leads"
- **Erros e exceções:**
  - E-01: Alguns falharam → "X atualizados, Y falharam. Ver detalhes"

### RF-20: Receber Webhook de Lead
- **Descrição:** Sistema recebe leads de integrações externas via webhook genérico
- **Usuário:** Sistema externo
- **Fluxo principal:**
  1. Admin configura webhook em CRM > Integrações > Webhooks
  2. Sistema gera URL única e secret
  3. Sistema externo envia POST para URL do webhook
  4. API valida signature (HMAC)
  5. API mapeia payload para campos do lead (mapeamento configurado)
  6. Cria lead
  7. Retorna 200 OK
- **Fluxos alternativos:**
  - FA-01: Payload não mapeado → armazena em campo `raw_data` para review
- **Erros e exceções:**
  - E-01: Signature inválida → 401 Unauthorized
  - E-02: Webhook desativado → 410 Gone

---

## Requisitos Não-Funcionais

### RNF-01: Performance
- **Response time:** < 200ms para 95% das requests de leitura
- **Response time:** < 500ms para 95% das requests de escrita
- **Pipeline Kanban:** Renderização < 1s para até 500 leads
- **Busca:** Resultados em < 300ms para índices de até 1M leads
- **Dashboard:** Métricas pré-agregadas, refresh < 2s
- **Importação:** 1000 leads/minuto em background job

### RNF-02: Escalabilidade
- Suportar até 10M leads por workspace
- Suportar até 1000 workspaces concorrentes
- API rate limit: 100 requests/minuto por API key
- Importação: arquivos até 100MB (500k linhas)

### RNF-03: Segurança
- **Autenticação:** JWT via Huly core para UI, API keys para integrações
- **Autorização:** RBAC com 3 papéis padrão (Admin, Sales, Marketing)
- **Multi-tenancy:** Isolamento total por workspace_id em todas as queries
- **Validação:** Zod schemas em todos os inputs
- **Sanitização:** XSS prevention em campos de texto
- **API:** Rate limiting, CORS configurável, HTTPS obrigatório
- **Dados sensíveis:** Emails e telefones mascarados em logs
- **Audit log:** Todas as ações de escrita registradas

### RNF-04: Disponibilidade
- **Uptime:** 99.9% (alinhado com SLA Huly)
- **Degradação:** Dashboard pode falhar sem afetar CRUD de leads
- **Retry:** Jobs de importação com retry exponencial (3 tentativas)

### RNF-05: Acessibilidade
- **WCAG:** Nível AA
- **Keyboard:** Todas as ações acessíveis via teclado
- **Screen reader:** Labels e ARIA attributes em todos os componentes
- **Contraste:** Mínimo 4.5:1 para texto

### RNF-06: Internacionalização
- **Idiomas:** pt-BR, en-US (MVP)
- **Formato:** Datas e números localizados
- **Timezone:** Respeitar timezone do workspace

### RNF-07: Observabilidade
- **Logs:** Structured JSON com correlation_id
- **Métricas:** Prometheus-compatible (leads created, conversion rate, API latency)
- **Tracing:** OpenTelemetry spans para requests
- **Alertas:** Erros 5xx > 1%, latência p95 > 1s

---

## Acceptance Criteria

### Gestão de Leads
- [ ] AC-01: Dado que sou Sales, quando crio lead com nome e email válidos, então lead aparece na lista e pipeline com status "new"
- [ ] AC-02: Dado que sou Sales, quando crio lead com email já existente, então sistema exibe modal de duplicidade com opções
- [ ] AC-03: Dado que sou Marketing, quando tento criar lead, então recebo erro de permissão
- [ ] AC-04: Dado que existem 100 leads, quando acesso a lista, então vejo paginação com 50 leads por página
- [ ] AC-05: Dado que filtro por estágio "Qualified", quando aplico filtro, então vejo apenas leads nesse estágio

### Pipeline Kanban
- [ ] AC-06: Dado que existem leads em múltiplos estágios, quando acesso Pipeline, então vejo colunas ordenadas com cards de leads
- [ ] AC-07: Dado que sou owner do lead, quando arrasto card para outro estágio, então lead é atualizado e atividade registrada
- [ ] AC-08: Dado que NÃO sou owner do lead, quando tento arrastar card, então recebo feedback visual de bloqueio
- [ ] AC-09: Dado que movo lead para "Convertido", quando solto o card, então modal de conversão é exibido

### Captura de Leads
- [ ] AC-10: Dado que tenho API key válida, quando envio POST /api/v1/crm/leads com payload correto, então recebo 201 com lead_id
- [ ] AC-11: Dado que envio API key inválida, quando faço request, então recebo 401 Unauthorized
- [ ] AC-12: Dado que envio payload sem email, quando faço POST, então recebo 400 com detalhes de validação
- [ ] AC-13: Dado que formulário está embeddado em site, quando visitante preenche e submete, então lead é criado com UTMs capturados

### Importação
- [ ] AC-14: Dado que faço upload de CSV válido, quando mapeio colunas, então vejo preview com 10 primeiros registros
- [ ] AC-15: Dado que confirmo importação de 1000 leads, quando job executa, então vejo progresso em tempo real
- [ ] AC-16: Dado que CSV tem leads duplicados, quando escolho "ignorar", então apenas leads únicos são criados
- [ ] AC-17: Dado que importação falha parcialmente, quando conclui, então vejo relatório com sucessos e erros detalhados

### Dashboard
- [ ] AC-18: Dado que existem leads no período, quando acesso Dashboard, então vejo KPIs corretos (total, conversão, etc.)
- [ ] AC-19: Dado que filtro por últimos 7 dias, quando mudo para 30 dias, então métricas atualizam em < 2s
- [ ] AC-20: Dado que clico em segmento do gráfico de origem, quando clico, então sou redirecionado para lista filtrada

### Automações
- [ ] AC-21: Dado que round-robin está ativo com 3 vendedores, quando 3 leads são criados via API, então cada vendedor recebe 1 lead
- [ ] AC-22: Dado que notificação de novo lead está ativa, quando lead é criado, então owner recebe notificação in-app

### Permissões
- [ ] AC-23: Dado que sou Admin, quando acesso qualquer lead, então posso editar independente do owner
- [ ] AC-24: Dado que sou Sales, quando acesso lead de outro owner, então vejo dados mas campos de edição estão desabilitados
- [ ] AC-25: Dado que sou Marketing, quando acesso CRM, então não vejo opção de criar lead manual

### Erros
- [ ] AC-ERROR-01: Dado que API está indisponível, quando acesso lista de leads, então vejo mensagem de erro com opção de retry
- [ ] AC-ERROR-02: Dado que tento excluir lead convertido, quando confirmo, então recebo erro "Leads convertidos não podem ser excluídos"
- [ ] AC-ERROR-03: Dado que sessão expira, quando faço ação, então sou redirecionado para login

---

## Fora do Escopo

- **Integração direta Meta/Google Ads:** Usar webhook genérico; integração nativa em versão futura
- **Lead scoring com ML:** Pontuação manual apenas; ML requer dados históricos
- **Email marketing:** Usar integrações existentes do Huly ou ferramentas externas
- **Relatórios customizáveis:** Dashboards fixos; builder de relatórios em versão futura
- **App mobile dedicado:** Usar PWA responsivo do Huly
- **Telefonia/VoIP:** Registro manual de ligações; integração em versão futura
- **Múltiplos pipelines:** Um pipeline por workspace; múltiplos em versão futura

---

## Dependências

### Internas (Huly Platform)
- **Auth service:** Autenticação e gestão de sessão
- **Workspace service:** Isolamento multi-tenant
- **User service:** Gestão de usuários e papéis
- **Notification service:** Envio de notificações in-app
- **Task service:** Integração para follow-ups (opcional)
- **Contact/Company plugins:** Para conversão de leads (se existirem)

### Externas
- **CockroachDB:** Persistência principal
- **Redis:** Cache de sessão e métricas agregadas
- **Elasticsearch:** Índice de busca full-text
- **MinIO:** Armazenamento de arquivos de importação
- **Redpanda:** Eventos assíncronos entre serviços

### Bibliotecas (sugeridas)
- **Zod:** Validação de schemas
- **date-fns:** Manipulação de datas
- **papaparse:** Parsing de CSV
- **xlsx:** Parsing de Excel
- **chart.js ou similar:** Gráficos do dashboard

---

## Constitution Check

> Não existe `.specs/memory/constitution.md` — nenhuma verificação de princípios necessária.
> Recomendação: Criar constitution antes de prosseguir para garantir consistência arquitetural.

---

## Notas de Implementação

### Priorização Sugerida para MVP
1. **Core:** Modelo de dados + CRUD de Lead (RF-01 a RF-08)
2. **Pipeline:** Kanban visual com drag & drop (RF-03, RF-04)
3. **Captura:** API REST (RF-09) — habilita integrações desde o início
4. **Importação:** CSV básico (RF-12) — onboarding de dados existentes
5. **Dashboard:** KPIs básicos (RF-14)
6. **Formulários:** Embed básico (RF-10, RF-11)
7. **Automações:** Round-robin + notificações (RF-15)
8. **Permissões:** RBAC básico (RF-17)

### Riscos Técnicos a Monitorar
- Integração com sistema de permissões existente do Huly
- Performance do Kanban com muitos leads (virtualização necessária)
- Complexidade do mapeamento de importação

---

**Autor:** Claude (spec:specify)
**Próximo passo:** `/spec-design huly-crm-module`
