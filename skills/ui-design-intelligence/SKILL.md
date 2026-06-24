---
name: ui-design-intelligence
description: "Spec de design system adaptado ao produto e indústria. ACIONE quando: usuário menciona estilo visual, identidade, paleta, tipografia, tom visual, tipo de produto ou indústria (fintech, healthcare, saas, e-commerce, etc). Produz design system spec completo. Keywords: estilo visual, identidade visual, paleta, tipografia, design system, tom visual, landing page, fintech, healthcare, e-commerce, saas dashboard, aesthetic, brand, cores, fontes."
model: sonnet
context: fork
agent: general-purpose
allowed-tools: Read, Glob
metadata:
  inspired_by: nextlevelbuilder/ui-ux-pro-max-skill
---

# UI Design Intelligence

## Papel

Consultor de design com acesso a bases de conhecimento curadas: estilos visuais,
paletas por indústria, pares tipográficos, diretrizes UX e tipos de chart.
Agnóstico de stack — adapta as recomendações para qualquer framework ou biblioteca.

---

## Quando usar

- Ao iniciar qualquer feature com componente visual significativo
- Quando o usuário quer que a UI "pareça" algo específico (profissional, playful,
  premium, minimalista, dark tech, etc.)
- Antes de chamar `openui-genui-layout` — fornecer o design system como input
- Para alinhar múltiplas telas com identidade visual consistente
- Quando o tipo de produto implica expectativas visuais da indústria

---

## Processo: Geração de Design System

### 1. Coletar inputs

Do usuário ou do contexto existente:
- **Tipo de produto:** SaaS, e-commerce, fintech, healthcare, portfólio, landing page, dashboard, app mobile
- **Indústria/nicho:** contabilidade, jurídico, turismo, beleza, gaming, educação, etc.
- **Keywords de estilo:** palavras que o usuário usa ("clean", "premium", "playful", "dark", "corporate")
- **Stack alvo:** Next.js + shadcn/ui, React + Tailwind, Vue, HTML puro, React Native, Flutter
- **Modo:** light / dark / system

Se o usuário não forneceu estilo: inferir do tipo de produto via `references/reasoning-rules.md` (regra por indústria) e `references/styles.md`.

### 2. Busca multi-domínio em paralelo

Consultar simultaneamente (ler as seções relevantes de cada reference):

```
[Paralelo]
A → references/reasoning-rules.md  — regra por produto/indústria: pattern + estilo + cor + tipografia + anti-patterns (PONTO DE PARTIDA)
B → references/styles.md          — estilo visual + CSS tokens
C → references/color-palettes.md  — paleta por indústria/produto
D → references/typography-pairs.md — par tipográfico compatível
E → references/ux-guidelines.md   — diretrizes UX críticas para o contexto
F → references/chart-types.md     — tipos de chart se for dashboard/analytics
```

Quando o tipo de produto bate com uma regra em `reasoning-rules.md`, use-a como espinha dorsal e refine com os demais references.

### 3. Sintetizar o design system spec

Produzir um bloco estruturado:

```markdown
## Design System Spec — {Nome do Produto}

### Estilo Visual
Nome: {estilo} | Atmosfera: {descrição 1 frase}
Referências: {produtos conhecidos com esse estilo}

### Paleta de Cores
| Token          | Hex     | Uso |
|----------------|---------|-----|
| --primary      | #...    | CTAs, links, elementos de destaque |
| --primary-dark | #...    | Hover, pressed states |
| --background   | #...    | Fundo principal |
| --surface      | #...    | Cards, modais, sidebars |
| --text-primary | #...    | Textos principais |
| --text-muted   | #...    | Labels, placeholders, captions |
| --border       | #...    | Dividers, inputs |
| --success      | #...    | Feedback positivo |
| --warning      | #...    | Alertas |
| --error        | #...    | Erros, estados destrutivos |
| --accent       | #...    | Elementos secundários de destaque |

### Tipografia
Heading: {fonte} | Body: {fonte} | Mono: {fonte opcional}
Import: {CSS @import ou link Google Fonts}
Scale: xs(12) sm(14) base(16) lg(18) xl(20) 2xl(24) 3xl(30) 4xl(36)

### Spacing Scale
4px base — usar múltiplos: 4, 8, 12, 16, 24, 32, 48, 64, 96

### Radius System
sm: 4px | md: 8px | lg: 12px | xl: 16px | full: 9999px
Estilo geral: {sharp/rounded/very-rounded}

### Shadow System
{descrever 2-3 níveis de sombra compatíveis com o estilo}

### Diretrizes UX Prioritárias
{3-5 diretrizes mais críticas para este tipo de produto}

### Charts Recomendados (se aplicável)
{tipo de chart → quando usar → biblioteca sugerida}

### Adaptação por Stack
**Next.js + shadcn/ui:** aplicar tokens como CSS variables em globals.css;
usar variantes do shadcn mapeadas para a paleta
**React + Tailwind puro:** estender tailwind.config com os tokens
**Vue/Nuxt:** CSS variables no :root do app.vue
**React Native:** StyleSheet com os tokens; usar expo-font para tipografia
**HTML + Tailwind:** CDN + CSS variables inline no :root
```

#### Exemplo curto de output gerado

```markdown
## Design System Spec — PayFlow (fintech SaaS B2B)

### Estilo Visual
Nome: Corporate Trust Minimal | Atmosfera: sóbrio, preciso, confiável
Referências: Stripe Dashboard, Mercury, Brex

### Paleta de Cores
| Token          | Hex     | Uso |
|----------------|---------|-----|
| --primary      | #0F4C81 | CTAs, links |
| --background   | #FAFBFC | Fundo principal |
| --surface      | #FFFFFF | Cards, modais |
| --text-primary | #1A2330 | Textos principais |
| --success      | #1E7F4F | Transações confirmadas |
| --error        | #C0392B | Falhas de pagamento |

### Tipografia
Heading: Geist | Body: Geist | Mono: JetBrains Mono (valores monetários, tabular-nums)
Scale: xs(12) sm(14) base(16) lg(18) xl(20) 2xl(24) 3xl(30)

### Diretrizes UX Prioritárias
1. Valores monetários sempre em fonte mono com tabular-nums
2. Estados destrutivos exigem confirmação em duas etapas
3. Tabelas densas com zebra sutil, nunca cards para dados financeiros
```

### 4. Handoff para skills dependentes

Ao final, informar como o design system se conecta:

- **→ `openui-genui-layout`:** "Use esta paleta e tipografia ao gerar o plano OpenUI Lang e os componentes"
- **→ `ui-audit`:** "Este spec é a referência para o Pilar 2 (Consistência) e Pilar 6 (Alinhamento)"
- **→ `phase-discussion`:** "As decisões de estilo aqui substituem a discussão visual da fase"
- **→ `frontend-engineer`:** "Carregar este spec antes de implementar qualquer componente da feature"

---

## Referências

- `references/reasoning-rules.md` — 161 regras por produto/indústria (motor de design system v2.0)
- `references/styles.md` — 84 estilos visuais com tokens e quando usar
- `references/color-palettes.md` — 161 paletas por indústria e produto
- `references/typography-pairs.md` — 73 combinações tipográficas curadas
- `references/ux-guidelines.md` — 99 diretrizes UX com anti-patterns
- `references/chart-types.md` — 25 tipos de chart para dashboards e analytics


## Gotchas

- **Gerar design system sem coletar inputs**: nunca inferir o estilo apenas pelo nome do projeto. Sempre perguntar o tipo de produto, indústria e keywords de estilo antes de gerar — mesmo que pareça óbvio. "ContaFácil" pode querer ser sério e corporativo ou acessível e colorido.
- **Aplicar spec genérico de "SaaS"**: SaaS é uma categoria enorme — fintech SaaS, healthcare SaaS e gaming SaaS têm expectativas visuais completamente diferentes. Sempre refinar pela indústria/nicho, não só pelo modelo de negócio.
- **Não fazer handoff para `openui-genui-layout`**: o spec gerado aqui deve ser explicitamente passado como input para `openui-genui-layout` antes de qualquer geração de UI. Sem isso, os componentes gerados não vão seguir o design system.
- **Cores hard-coded no código**: o spec usa tokens CSS variables (`--primary`, `--background`, etc). Se o desenvolvedor implementar com valores hex diretos (`#2563EB`), o dark mode e theming dinâmico quebram. Sempre mapear para CSS variables do shadcn.
- **Tipografia sem `@import` correto**: ao usar Google Fonts, verificar que o `@import` está no `globals.css` antes de referenciar a família. Fontes não carregadas fazem fallback silencioso para o sistema.
- **Spec desatualizado após mudança de direção**: se o usuário mudar de "fintech premium" para "produto acessível para pequenos negócios" durante o desenvolvimento, o design system precisa ser regerado — não remendado. Specs parcialmente atualizados causam inconsistência visual.
