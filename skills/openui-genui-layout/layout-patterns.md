# Layout Patterns

Templates canônicos em OpenUI Lang para os padrões de tela mais comuns.
Selecione o padrão mais próximo e adapte — não invente estrutura do zero.

---

## 1. dashboard

**Quando usar:** Visão geral com KPIs, gráficos e atividade recente.

```openui
root = Stack([header, kpi_row, charts_row, recent_section])
header = PageHeader("Dashboard", "Visão geral do sistema")

kpi_row = Grid([kpi1, kpi2, kpi3, kpi4])
kpi1 = StatCard("Total Receita", "$0", "flat")
kpi2 = StatCard("Usuários Ativos", "0", "flat")
kpi3 = StatCard("Conversão", "0%", "flat")
kpi4 = StatCard("Pendências", "0", "flat")

charts_row = Grid([revenue_chart, dist_chart])
revenue_chart = Card("Receita Mensal", [line_chart])
line_chart = LineChart(["Jan","Fev","Mar","Abr","Mai","Jun"], [series1])
series1 = Series("Receita", [0,0,0,0,0,0])
dist_chart = Card("Distribuição", [pie])
pie = PieChart([])

recent_section = Card("Atividade Recente", [recent_table])
recent_table = DataTable(["Data","Descrição","Valor","Status"], [])
```

---

## 2. crud-list

**Quando usar:** Listagem com busca, filtro, paginação e ações por linha.

```openui
root = Stack([header, toolbar, data_table, pager])
header = PageHeader("Usuários", "Gerencie os usuários do sistema")

toolbar = Toolbar([search, role_filter, add_btn])
search = Input("Buscar usuários...", "search")
role_filter = Select("Todos os papéis", ["Admin","Editor","Visualizador"])
add_btn = Button("Adicionar Usuário", "default")

data_table = DataTable(["Nome","Email","Papel","Status","Ações"], [])
pager = Pagination(1, 10, 0)
```

---

## 3. form-wizard

**Quando usar:** Cadastro ou processo em etapas com validação por passo.

```openui
root = Stack([header, steps_indicator, step_content])
header = PageHeader("Novo Cadastro", "Preencha os dados em 3 etapas")

steps_indicator = Breadcrumb([
  {label: "Dados Básicos", href: null},
  {label: "Endereço", href: null},
  {label: "Confirmação", href: null}
])

step_content = Form("step-1", step_buttons, [name_field, email_field, phone_field])
name_field = FormControl("Nome completo", name_input, null, true)
name_input = Input("João Silva", "text")
email_field = FormControl("E-mail", email_input, null, true)
email_input = Input("joao@exemplo.com", "email")
phone_field = FormControl("Telefone", phone_input)
phone_input = Input("(11) 90000-0000", "tel")

step_buttons = Buttons([back_btn, next_btn])
back_btn = Button("Voltar", "outline")
next_btn = Button("Próximo", "default")
```

---

## 4. detail-view

**Quando usar:** Visualização de detalhes de uma entidade com seções e abas.

```openui
root = Stack([breadcrumb, header, info_grid, tabs_section])

breadcrumb = Breadcrumb([
  {label: "Usuários", href: "/users"},
  {label: "João Silva", href: null}
])

header = PageHeader("João Silva", "Visualizando perfil")

info_grid = Grid([basic_card, contact_card])
basic_card = Card("Informações Básicas", [info_list])
info_list = UnorderedList([
  {label: "Papel", description: "Administrador"},
  {label: "Status", description: "Ativo"},
  {label: "Criado em", description: "01/01/2024"}
])
contact_card = Card("Contato", [contact_list])
contact_list = UnorderedList([
  {label: "E-mail", description: "joao@exemplo.com"},
  {label: "Telefone", description: "(11) 90000-0000"}
])

tabs_section = Tabs([activity_tab, permissions_tab])
activity_tab = TabItem("Atividade", [activity_table])
activity_table = DataTable(["Data","Ação","Detalhes"], [])
permissions_tab = TabItem("Permissões", [permissions_list])
permissions_list = UnorderedList([])
```

---

## 5. settings-page

**Quando usar:** Configurações agrupadas por categoria em abas.

```openui
root = Stack([header, settings_tabs])
header = PageHeader("Configurações", "Gerencie as preferências do sistema")

settings_tabs = Tabs([general_tab, notifications_tab, security_tab])

general_tab = TabItem("Geral", [general_form])
general_form = Form("general-settings", save_buttons, [org_field, tz_field, lang_field])
org_field = FormControl("Nome da organização", org_input, null, true)
org_input = Input("Minha Empresa")
tz_field = FormControl("Fuso horário", tz_select)
tz_select = Select("America/Sao_Paulo", ["America/Sao_Paulo","America/Fortaleza","America/Manaus"])
lang_field = FormControl("Idioma", lang_select)
lang_select = Select("Português (BR)", ["Português (BR)","English"])
save_buttons = Buttons([save_btn])
save_btn = Button("Salvar Alterações", "default")

notifications_tab = TabItem("Notificações", [notif_form])
notif_form = Form("notif-settings", notif_buttons, [email_notif, sms_notif])
email_notif = FormControl("Notificações por e-mail", email_check)
email_check = Checkbox("Receber alertas por e-mail", true)
sms_notif = FormControl("Notificações por SMS", sms_check)
sms_check = Checkbox("Receber alertas por SMS", false)
notif_buttons = Buttons([notif_save_btn])
notif_save_btn = Button("Salvar", "default")

security_tab = TabItem("Segurança", [pwd_card])
pwd_card = Card("Alterar Senha", [pwd_form])
pwd_form = Form("password", pwd_buttons, [current_pwd, new_pwd, confirm_pwd])
current_pwd = FormControl("Senha atual", current_input, null, true)
current_input = Input("••••••••", "password")
new_pwd = FormControl("Nova senha", new_input, "Mínimo 8 caracteres", true)
new_input = Input("••••••••", "password")
confirm_pwd = FormControl("Confirmar nova senha", confirm_input, null, true)
confirm_input = Input("••••••••", "password")
pwd_buttons = Buttons([update_pwd_btn])
update_pwd_btn = Button("Atualizar Senha", "default")
```

---

## 6. auth-page

**Quando usar:** Login, cadastro, reset de senha.

```openui
root = Stack([auth_card])
auth_card = Card("Entrar na plataforma", [auth_form])

auth_form = Form("login", login_buttons, [email_field, password_field])
email_field = FormControl("E-mail", email_input, null, true)
email_input = Input("seu@email.com", "email")
password_field = FormControl("Senha", pwd_input, null, true)
pwd_input = Input("••••••••", "password")

login_buttons = Buttons([login_btn, forgot_btn])
login_btn = Button("Entrar", "default")
forgot_btn = Button("Esqueci minha senha", "ghost")
```

---

## 7. empty-state

**Quando usar:** Estado inicial sem dados, busca vazia, ou feature não configurada.

```openui
root = Stack([header, empty_card])
header = PageHeader("Documentos", "Gerencie seus arquivos")

empty_card = Card(null, [empty_title, empty_desc, empty_actions])
empty_title = TextContent("Nenhum documento ainda", "h3")
empty_desc = TextContent("Faça o upload do seu primeiro documento para começar.", "muted")
empty_actions = Buttons([upload_btn])
upload_btn = Button("Fazer Upload", "default")
```

---

## 8. onboarding

**Quando usar:** Guia de primeiros passos após cadastro ou configuração inicial.

```openui
root = Stack([welcome_header, progress_alert, steps_grid])

welcome_header = PageHeader("Bem-vindo! Vamos começar.", "Complete estas etapas para configurar sua conta")
progress_alert = Alert("default", "2 de 4 etapas concluídas", "Você está indo bem!")

steps_grid = Grid([step1, step2, step3, step4])
step1 = Card("Perfil configurado", [step1_desc, step1_badge])
step1_desc = TextContent("Adicione sua foto e informações básicas", "small")
step1_badge = Badge("Concluído", "default")
step2 = Card("Convide sua equipe", [step2_desc, step2_btn])
step2_desc = TextContent("Adicione membros para colaborar", "small")
step2_btn = Button("Convidar", "outline")
step3 = Card("Conecte integrações", [step3_desc, step3_btn])
step3_desc = TextContent("Conecte suas ferramentas favoritas", "small")
step3_btn = Button("Explorar", "outline")
step4 = Card("Configure notificações", [step4_desc, step4_btn])
step4_desc = TextContent("Escolha como receber alertas", "small")
step4_btn = Button("Configurar", "outline")
```

---

## Variações Comuns

### Dashboard com Sidebar
```openui
root = SidebarLayout(nav_sidebar, [header, kpi_row, charts_row])
nav_sidebar = Sidebar([
  {label: "Dashboard", href: "/"},
  {label: "Usuários", href: "/users"},
  {label: "Relatórios", href: "/reports"},
  {label: "Configurações", href: "/settings"}
])
# ... continua com padrão dashboard
```

### CRUD com Sheet (sem modal)
```openui
root = Stack([header, toolbar, data_table, pager, edit_sheet])
edit_sheet = Sheet("right", "Editar Registro", [edit_form])
edit_form = Form("edit-record", edit_buttons, [name_field, email_field])
# ...
```

### Detail View com ações no header
```openui
root = Stack([breadcrumb, header_with_actions, info_section])
header_with_actions = PageHeader("João Silva", null, [edit_btn, delete_btn])
edit_btn = Button("Editar", "outline")
delete_btn = Button("Excluir", "destructive")
# ...
```

---

## Tabela de Seleção Rápida

| Situação | Padrão |
|----------|--------|
| Tela inicial com números | `dashboard` |
| Listar/buscar/filtrar entidades | `crud-list` |
| Criar entidade com muitos campos | `form-wizard` |
| Ver detalhes de uma entidade | `detail-view` |
| Configurar sistema/usuário | `settings-page` |
| Login/cadastro/reset | `auth-page` |
| Feature vazia ou sem dados | `empty-state` |
| Primeiros passos pós-cadastro | `onboarding` |
