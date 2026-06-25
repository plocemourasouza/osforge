---
name: openui-genui-layout
description: "UI planning and generation in Next.js. Use when: creating any page, screen, dashboard, form, table, layout component, route scaffold. Produces an OpenUI Lang plan BEFORE any code. Keywords: create page, scaffold, layout, screen, dashboard, form, table, component, UI, create interface, generate UI, plan UI."
model: sonnet
context: fork
agent: general-purpose
allowed-tools: Read, Write, Glob
version: 1.1.0
stack: Next.js, TypeScript, shadcn/ui, Tailwind CSS, Zod, @openuidev/react-lang
---

## Project context
!`[ -f components.json ] && echo "shadcn/ui configured: $(cat components.json | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'style={d.get(\"style\",\"?\")} rsc={d.get(\"rsc\",\"?\")} tailwind={d.get(\"tailwind\",{}).get(\"config\",\"?\")}') 2>/dev/null || cat components.json | head -5)" || echo "components.json not found — shadcn/ui may not be configured"`
!`ls src/app 2>/dev/null | head -8 || ls app 2>/dev/null | head -8 || echo "app directory not found"`

# OpenUI GenUI Layout Skill

This skill provides structured UI planning and code generation using the **OpenUI Lang** open standard (MIT license). It works entirely without external APIs — the agent generates compact UI descriptions that are rendered by the free `@openuidev/react-lang` SDK using the project's native shadcn/ui components.

**Key principle:** OpenUI Lang is just a compact notation. The agent writes it; the open-source renderer reads it. No C1 API, no paid service, no network call at layout time.

---

## 1. When to Load This Skill

Load and follow this skill when any of these triggers appear:

- Creating, planning, or scaffolding a new page, screen, or route
- Designing a dashboard, CRUD table, form wizard, or data visualization layout
- Asked to "generate UI for [feature]" or "create components for [module]"
- Refactoring layout structure of an existing page
- Building a reusable component that requires props planning

**Do NOT load** for: purely styling changes (colors, spacing), logic-only tasks (API routes, hooks), or database schema work.

Concrete examples of when NOT to load:
- "Give this button a new style / change the button color" — styling only, no layout planning needed
- "Create a `useDebounce` / `useAuth` hook" — logic-only, no UI tree involved
- "Add an `orders` table to the database schema / create the migration" — database schema work, not UI

---

## 2. Mandatory Pre-Planning Step

**Before writing any code**, produce a layout plan in OpenUI Lang. This plan:

1. Makes layout structure explicit and reviewable
2. Guides component decomposition before implementation
3. Stays in sync with the shadcn/ui library (see `component-library.md`)
4. Can be rendered progressively as a skeleton UI while data loads

### OpenUI Lang Syntax Reference

```
# Core rules:
# - One statement per line: identifier = Expression
# - First statement MUST be: root = <RootComponent>(...)
# - Top-down order: Layout → Components → Data
# - Positional args map to Zod schema key order
# - Forward references (hoisting) are valid

root = Stack([header, kpi_row, main_content])
header = PageHeader("Revenue Dashboard", "Q4 2024")
kpi_row = Grid([card1, card2, card3])
card1 = StatCard("Total Revenue", "$1.2M", "up")
card2 = StatCard("Active Users", "3,450", "flat")
card3 = StatCard("Conversion", "4.8%", "up")
main_content = Tabs([tab1, tab2])
tab1 = TabItem("Overview", [overview_chart])
tab2 = TabItem("Details", [data_table])
overview_chart = BarChart(["Jan","Feb","Mar","Apr"], [series1])
series1 = Series("Revenue", [1200,1450,980,1600])
data_table = DataTable(columns, rows)
columns = ["Date","Amount","Status"]
rows = []
```

### Type System

| Type | Syntax | Example |
|------|--------|---------|
| Component call | `Type(arg1, arg2)` | `Button("Save", "default")` |
| String | `"text"` | `"Hello world"` |
| Number | `42`, `12.5`, `-5` | `100` |
| Boolean | `true` / `false` | `true` |
| Null | `null` | `null` |
| Array | `[a, b, c]` | `["Jan","Feb","Mar"]` |
| Object | `{key: val}` | `{variant: "destructive"}` |
| Reference | `identifier` | `myRows` |

---

## 3. Layout Planning Protocol

Follow this sequence for every UI task:

### Step 1 — Identify the layout pattern (see `layout-patterns.md`)

Select from: `dashboard`, `crud-list`, `form-wizard`, `detail-view`, `settings-page`, `auth-page`, `empty-state`, `onboarding`. Each has a canonical OpenUI Lang template.

### Step 2 — Write the OpenUI Lang plan

Output the plan as a fenced code block labeled `openui`:

````markdown
```openui
root = Stack([page_header, content_area])
page_header = PageHeader("User Management", "Manage system users")
content_area = Stack([toolbar, user_table, pagination])
toolbar = Toolbar([search_input, filter_select, add_button])
search_input = Input("Search users...", "search")
filter_select = Select("All Roles", role_options)
role_options = ["Admin","Editor","Viewer"]
add_button = Button("Add User", "default")
user_table = DataTable(user_cols, user_rows)
user_cols = ["Name","Email","Role","Status","Actions"]
user_rows = []
pagination = Pagination(1, 10, 150)
```
````

### Step 3 — Map to file structure

For each top-level component in the plan, identify or create the corresponding file:

```
src/
  app/users/
    page.tsx           ← root = Stack(...)
    _components/
      UserTable.tsx    ← user_table = DataTable(...)
      UserToolbar.tsx  ← toolbar = Toolbar(...)
      UserPagination.tsx ← pagination = Pagination(...)
```

### Step 4 — Generate the implementation code

Implement each component using shadcn/ui primitives. Reference `component-library.md` for the exact shadcn/ui imports and prop signatures for each OpenUI node.

---

## 4. Code Generation Rules

When generating implementation code from an OpenUI Lang plan:

1. **Server Components by default** — use `async` page components and pass data as props to Client Components
2. **Props from OpenUI schema** — each component's props interface mirrors its OpenUI Zod schema
3. **shadcn/ui primitives only** — never introduce new UI libraries; map to the component library
4. **TypeScript strict** — all props typed, no `any`, Zod schemas for external data
5. **Tailwind for spacing/layout** — use `cn()` utility for conditional classes
6. **No inline styles** — Tailwind classes only

### Component generation pattern:

```tsx
// From OpenUI plan: card1 = StatCard("Total Revenue", "$1.2M", "up")
// Maps to StatCard(label: string, value: string, trend: "up"|"down"|"flat")

import { TrendingUp, TrendingDown, Minus } from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { cn } from "@/lib/utils"

interface StatCardProps {
  label: string
  value: string
  trend: "up" | "down" | "flat"
}

export function StatCard({ label, value, trend }: StatCardProps) {
  const TrendIcon = trend === "up" ? TrendingUp : trend === "down" ? TrendingDown : Minus
  const trendColor = trend === "up" ? "text-green-600" : trend === "down" ? "text-red-600" : "text-muted-foreground"

  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between pb-2">
        <CardTitle className="text-sm font-medium text-muted-foreground">{label}</CardTitle>
        <TrendIcon className={cn("h-4 w-4", trendColor)} />
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold">{value}</div>
      </CardContent>
    </Card>
  )
}
```

---

## 5. OpenUI Lang → shadcn/ui Mapping (Quick Reference)

See `component-library.md` for full definitions. Key mappings:

| OpenUI Node | shadcn/ui Implementation |
|-------------|--------------------------|
| `Stack` | `<div className="flex flex-col gap-4">` |
| `Grid` | `<div className="grid grid-cols-N gap-4">` |
| `PageHeader` | `<div>` + `<h1>` + `<p>` |
| `StatCard` | `<Card>` + `<CardHeader>` + `<CardContent>` |
| `DataTable` | `<Table>` + `<TableHeader>` + `<TableRow>` |
| `Button` | `<Button variant={...}>` |
| `Input` | `<Input placeholder={...}>` |
| `Select` | `<Select>` + `<SelectContent>` |
| `Tabs` | `<Tabs>` + `<TabsList>` + `<TabsContent>` |
| `TabItem` | `<TabsTrigger>` + `<TabsContent>` |
| `Form` | `<Form>` + `react-hook-form` + Zod |
| `FormControl` | `<FormField>` + `<FormItem>` + `<FormLabel>` |
| `BarChart` | `recharts <BarChart>` wrapped in `<ResponsiveContainer>` |
| `LineChart` | `recharts <LineChart>` |
| `Alert` | `<Alert variant={...}>` |
| `Badge` | `<Badge variant={...}>` |
| `Dialog` | `<Dialog>` + `<DialogContent>` |
| `Sheet` | `<Sheet>` + `<SheetContent>` |
| `Pagination` | Custom pagination with `<Button>` |
| `Toolbar` | `<div className="flex items-center gap-2">` |
| `Breadcrumb` | `<Breadcrumb>` + `<BreadcrumbItem>` |
| `Sidebar` | `<aside>` using shadcn/ui sidebar primitive |

---

## 6. Integration with @openuidev/react-lang (Optional)

If the project uses progressive streaming UI (agent responses rendered as components):

```bash
bun add @openuidev/react-lang @openuidev/react-ui
```

```tsx
// src/lib/ui-library.ts
import { defineComponent, createLibrary } from "@openuidev/react-lang"
import { z } from "zod"
import { StatCard } from "@/components/stat-card"

const StatCardDef = defineComponent({
  name: "StatCard",
  description: "Displays a metric with label, value, and trend indicator.",
  props: z.object({
    label: z.string(),
    value: z.string(),
    trend: z.enum(["up", "down", "flat"]).optional(),
  }),
  component: ({ props }) => <StatCard {...props} trend={props.trend ?? "flat"} />,
})

export const appLibrary = createLibrary({
  root: "Stack",
  components: [StatCardDef],
})
```

```tsx
// app/api/chat/route.ts
import { appLibrary } from "@/lib/ui-library"

const systemPrompt = appLibrary.prompt({
  preamble: "You are a UI-aware assistant. Use OpenUI Lang for all structured responses.",
  additionalRules: [
    "Always use Stack as the root component.",
    "Prefer DataTable over manual lists for tabular data.",
    "Use StatCard for any numeric metric.",
  ],
})
```

**This integration is optional.** The skill works for UI planning and code generation without it.

---

## 7. Quality Checklist

Before finalizing any generated UI:

- [ ] OpenUI Lang plan written before any code
- [ ] Every component maps to a shadcn/ui primitive (no new libraries)
- [ ] Server/Client component split is correct (`"use client"` only where needed)
- [ ] All props typed with TypeScript interfaces
- [ ] Forms use `react-hook-form` + Zod validation
- [ ] Loading states (Suspense/skeleton) planned in the OpenUI tree
- [ ] Mobile responsive layout considered (`grid-cols-1 md:grid-cols-3`)
- [ ] Empty states handled for tables and lists

---

## 8. References

- OpenUI Lang spec: https://www.openui.com/docs/openui-lang/specification
- Defining components: https://www.openui.com/docs/openui-lang/defining-components
- Shadcn + OpenUI example: https://www.openui.com/docs/openui-lang/examples/shadcn-chat
- GitHub (MIT): https://github.com/thesysdev/openui
- See also: `component-library.md`, `layout-patterns.md`


## Gotchas

- **Forgetting the OpenUI plan before the code**: the skill has a clear contract — OpenUI Lang plan FIRST, code AFTER. Generating code directly without the plan violates the protocol and produces non-reviewable components.
- **Using libraries outside shadcn/ui**: the rule is to use only shadcn/ui native primitives (without installing new libraries). If the component doesn't exist in shadcn, compose it with the available primitives — don't install `react-beautiful-dnd`, `react-select`, etc. without explicit approval.
- **`"use client"` in Server Components**: components that use `useState`, `useEffect`, `onClick` need `"use client"`. Forgetting this causes a runtime error. Rule: Server Component by default, `"use client"` only when necessary.
- **Forms without `react-hook-form` + Zod**: never use manual `useState` to manage form state. The pattern is always `react-hook-form` + `zodResolver` + Zod schema — no exceptions.
- **Wrong layout pattern for the context**: always select the correct canonical pattern (`dashboard`, `crud-list`, `form-wizard`, `detail-view`, `settings-page`, `auth-page`, `empty-state`, `onboarding`) before generating the plan. Using `dashboard` for a settings screen is a category error.
- **Loading states not planned**: always include `Suspense` boundaries and skeleton loaders in the OpenUI Lang plan before implementing. Adding them later is much more work.
- **Mobile not considered in the plan**: the OpenUI plan must include breakpoints (`grid-cols-1 md:grid-cols-3`) from the start — responsiveness added later frequently breaks the layout.
