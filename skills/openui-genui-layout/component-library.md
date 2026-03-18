# Component Library Reference

Definições canônicas dos componentes OpenUI Lang mapeados para shadcn/ui.
Para cada nó: nome OpenUI, schema Zod (ordem define posição dos argumentos), e implementação React.

---

## Layout

### Stack
Container flexível vertical. Root padrão para a maioria das páginas.

```ts
// OpenUI: root = Stack([child1, child2])
z.object({
  children: z.array(ChildUnion),
  gap: z.enum(["sm","md","lg"]).optional(), // default: "md"
})
// shadcn/ui:
<div className="flex flex-col gap-4">{children}</div>
// gap-sm=gap-2, gap-md=gap-4, gap-lg=gap-6
```

### Grid
Grid responsivo. Determina número de colunas pelo `cols`.

```ts
// OpenUI: kpi_row = Grid([card1, card2, card3])
z.object({
  children: z.array(ChildUnion),
  cols: z.number().min(1).max(6).optional(), // default: children.length, max 4
})
// shadcn/ui:
<div className="grid grid-cols-1 md:grid-cols-{cols} gap-4">{children}</div>
```

### Tabs
Container de abas. Usa shadcn Tabs primitivo.

```ts
// OpenUI: main = Tabs([tab1, tab2])
z.object({
  items: z.array(TabItem.ref),
  defaultValue: z.string().optional(),
})
// shadcn/ui: <Tabs><TabsList><TabsTrigger/></TabsList><TabsContent/></Tabs>
```

### TabItem
Item de aba. Sempre filho de Tabs.

```ts
// OpenUI: tab1 = TabItem("Overview", [chart])
z.object({
  label: z.string(),
  content: z.array(ChildUnion),
  value: z.string().optional(), // default: slugify(label)
})
```

### SidebarLayout
Layout com sidebar lateral. Para dashboards com navegação.

```ts
// OpenUI: root = SidebarLayout(sidebar, [children])
z.object({
  sidebar: Sidebar.ref,
  content: z.array(ChildUnion),
})
// shadcn/ui: SidebarProvider + Sidebar + SidebarContent + SidebarMenu
```

---

## Typography & Header

### PageHeader
Cabeçalho padrão de página com título, subtítulo e ações opcionais.

```ts
// OpenUI: header = PageHeader("User Management", "Manage system users")
z.object({
  title: z.string(),
  subtitle: z.string().optional(),
  actions: z.array(Button.ref).optional(),
})
// shadcn/ui:
<div className="flex items-center justify-between">
  <div>
    <h1 className="text-2xl font-bold tracking-tight">{title}</h1>
    {subtitle && <p className="text-muted-foreground">{subtitle}</p>}
  </div>
  {actions && <div className="flex gap-2">{actions}</div>}
</div>
```

### TextContent
Bloco de texto com variante tipográfica.

```ts
// OpenUI: desc = TextContent("Some description", "body")
z.object({
  text: z.string(),
  variant: z.enum(["h1","h2","h3","h4","body","small","muted","code"]).optional(),
})
```

---

## Cards & Metrics

### StatCard
Card de métrica com label, valor e indicador de tendência.

```ts
// OpenUI: c1 = StatCard("Total Revenue", "$1.2M", "up")
z.object({
  label: z.string(),
  value: z.string(),
  trend: z.enum(["up","down","flat"]).optional(),
  description: z.string().optional(),
})
// shadcn/ui: Card + CardHeader + CardContent + TrendingUp/Down (lucide-react)
```

### Card
Card genérico com título e corpo livre.

```ts
// OpenUI: info = Card("Title", [child1, child2])
z.object({
  title: z.string().optional(),
  children: z.array(ChildUnion),
  description: z.string().optional(),
})
// shadcn/ui: <Card><CardHeader><CardTitle/></CardHeader><CardContent/></Card>
```

### Alert
Mensagem de alerta contextual.

```ts
// OpenUI: warn = Alert("default", "Heads up!", "You have unsaved changes.")
z.object({
  variant: z.enum(["default","destructive","warning","success"]),
  title: z.string(),
  description: z.string().optional(),
})
// shadcn/ui: <Alert variant={...}><AlertTitle/><AlertDescription/></Alert>
```

### Badge
Badge inline com variante.

```ts
// OpenUI: status = Badge("Active", "default")
z.object({
  label: z.string(),
  variant: z.enum(["default","secondary","destructive","outline"]).optional(),
})
// shadcn/ui: <Badge variant={...}>{label}</Badge>
```

---

## Tables & Lists

### DataTable
Tabela de dados com colunas e linhas. `rows = []` renderiza skeleton.

```ts
// OpenUI: tbl = DataTable(cols, rows)
z.object({
  columns: z.array(z.string()),
  rows: z.array(z.array(z.any())),
  selectable: z.boolean().optional(),
  actions: z.array(z.string()).optional(),
})
// shadcn/ui: Table + TableHeader + TableBody + TableRow + TableCell
// Para tabelas complexas com sorting: @tanstack/react-table
```

### UnorderedList / ListItem

```ts
// OpenUI: list = UnorderedList([item1, item2])
z.object({ items: z.array(ListItem.ref) })

// ListItem:
z.object({ label: z.string(), description: z.string().optional() })
```

### Pagination

```ts
// OpenUI: pager = Pagination(1, 10, 150)
z.object({ page: z.number(), pageSize: z.number(), total: z.number() })
// shadcn/ui: Pagination + PaginationContent + PaginationItem + PaginationLink
```

---

## Forms

### Form
Container de formulário. Integra react-hook-form + Zod.

```ts
// OpenUI: frm = Form("user-form", buttons, [field1, field2])
z.object({
  id: z.string(),
  buttons: Buttons.ref,
  controls: z.array(FormControl.ref),
})
// SEMPRE defina cada FormControl como referência separada para streaming progressivo
// NUNCA aninhe Form dentro de Form
```

### FormControl

```ts
// OpenUI: name_field = FormControl("Full Name", name_input)
z.object({
  label: z.string(),
  field: z.union([Input.ref, Textarea.ref, Select.ref, Checkbox.ref, DatePicker.ref]),
  description: z.string().optional(),
  required: z.boolean().optional(),
})
// shadcn/ui: FormField + FormItem + FormLabel + FormControl + FormMessage
```

### Input

```ts
// OpenUI: email_input = Input("Email address", "email")
z.object({
  placeholder: z.string().optional(),
  type: z.enum(["text","email","password","number","url","tel","search"]).optional(),
  disabled: z.boolean().optional(),
})
// shadcn/ui: <Input type={...} placeholder={...} />
```

### Textarea

```ts
// OpenUI: desc_input = Textarea("Description...", 4)
z.object({ placeholder: z.string().optional(), rows: z.number().optional() })
```

### Select

```ts
// OpenUI: role_select = Select("Select role", role_opts)
z.object({ placeholder: z.string(), options: z.array(z.string()), value: z.string().optional() })
// shadcn/ui: Select + SelectTrigger + SelectContent + SelectItem
```

### Checkbox

```ts
// OpenUI: agree = Checkbox("I agree to terms", false)
z.object({ label: z.string(), checked: z.boolean().optional() })
```

### DatePicker

```ts
// OpenUI: due_date = DatePicker("Due date", null)
z.object({ placeholder: z.string().optional(), value: z.string().optional() })
// shadcn/ui: Calendar + Popover (date picker pattern)
```

### Button / Buttons

```ts
// OpenUI: save_btn = Button("Save", "default")
z.object({
  label: z.string(),
  variant: z.enum(["default","secondary","destructive","outline","ghost","link"]).optional(),
  size: z.enum(["default","sm","lg","icon"]).optional(),
  disabled: z.boolean().optional(),
})

// Buttons (grupo):
// OpenUI: actions = Buttons([save_btn, cancel_btn])
z.object({ items: z.array(Button.ref) })
// shadcn/ui: <div className="flex gap-2">{items}</div>
```

---

## Navigation

### Toolbar

```ts
// OpenUI: bar = Toolbar([search_input, add_btn])
z.object({ children: z.array(ChildUnion) })
// shadcn/ui: <div className="flex items-center gap-2 flex-wrap">{children}</div>
```

### Breadcrumb

```ts
// OpenUI: crumb = Breadcrumb([{label:"Home",href:"/"},{label:"Users",href:null}])
z.object({ items: z.array(z.object({ label: z.string(), href: z.string().nullable() })) })
// shadcn/ui: Breadcrumb + BreadcrumbList + BreadcrumbItem + BreadcrumbLink
```

---

## Charts (via recharts)

### BarChart / LineChart

```ts
// OpenUI: chart = BarChart(["Jan","Feb","Mar"], [series1])
z.object({
  labels: z.array(z.string()),
  series: z.array(Series.ref),
  height: z.number().optional(), // default: 300
})
// impl: recharts BarChart/LineChart wrapped in ResponsiveContainer
```

### PieChart

```ts
// OpenUI: dist = PieChart(pie_data)
z.object({
  data: z.array(z.object({ name: z.string(), value: z.number() })),
  height: z.number().optional(),
})
```

### Series

```ts
// OpenUI: s1 = Series("Revenue", [100,200,150])
z.object({ name: z.string(), data: z.array(z.number()), color: z.string().optional() })
```

---

## Overlays

### Dialog

```ts
// OpenUI: confirm = Dialog("Delete User", [warn_msg, action_btns])
z.object({ title: z.string(), children: z.array(ChildUnion), description: z.string().optional() })
// shadcn/ui: Dialog + DialogContent + DialogHeader + DialogTitle
```

### Sheet

```ts
// OpenUI: drawer = Sheet("right", "Edit User", [edit_form])
z.object({ side: z.enum(["left","right","top","bottom"]).optional(), title: z.string(), children: z.array(ChildUnion) })
// shadcn/ui: Sheet + SheetContent + SheetHeader + SheetTitle
```

---

## Notas

- `rows = []` no DataTable → estado skeleton automático
- Charts requerem `recharts` no package.json
- Formulários sempre com `react-hook-form` + Zod
- `ChildUnion` aceita qualquer componente da lista acima em posições de children
