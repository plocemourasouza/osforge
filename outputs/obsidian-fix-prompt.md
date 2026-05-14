# Prompt — Aplicar fixes do audit no OBSIDIAN Studio

Cole esse bloco no Claude Code ou Cursor (com o projeto OBSIDIAN aberto):

---

## Contexto

Estou no projeto **OBSIDIAN — Studio of Considered Interfaces**, um site editorial premium em modo **EDITORIAL_MINIMALIST** (serif Fraunces sobre off-black, accent terracotta, tipografia cinemática). O servidor roda em `localhost:8000`.

Acabei de rodar um audit completo (performance + acessibilidade + anti-AI-slop) e o site ficou ótimo em qualidade visual (contraste 17:1, zero CLS, peso total 36KB), mas tem **3 problemas críticos** que precisam de fix cirúrgico **sem quebrar a estética**.

## Demanda

Aplique os fixes abaixo seguindo o padrão **redesign-audit** (auditar → fix mínimo → verificar). Mantenha integralmente a direção estética EDITORIAL_MINIMALIST. Acione automaticamente: `redesign-audit`, `taste-design-dials`, `core-web-vitals`, `accessibility`, `output-enforcement`, `verification-before-completion`.

---

## P0 — CRÍTICOS (fazer agora)

### Fix 1 · Reduzir loading sequence de 6.5s → 1.2s
**Arquivo:** `script.js` (ou onde estiver a animação do counter 0%→100%)

**Diagnóstico:** O First Contentful Paint mediu **6544ms** num site de 36KB total. A causa é o `duration` da animação do contador, não o peso de bytes. Tudo baixa em ~70ms.

**Critério de sucesso:**
- FCP ≤ 1800ms (Google "Good" threshold) — idealmente ≤ 1200ms
- Loading sequence dura ≤ 1.2s em desktop, ≤ 0.8s em mobile
- A estética (números crescendo grandes, mono labels) permanece intacta
- Verificar via `performance.getEntriesByType('paint')` no console após o fix

### Fix 2 · Implementar `prefers-reduced-motion`
**Arquivo:** `styles.css` (final do arquivo)

**Comportamento esperado:** Quando o usuário tem reduced-motion ativo no SO, o loader é pulado completamente e o conteúdo aparece imediatamente. Todas as animações de scroll, parallax e perpetual motion são desativadas.

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
  .loader, [data-loader] {
    display: none !important;
  }
  main, body > *:not(.loader) {
    opacity: 1 !important;
    transform: none !important;
  }
}
```

Adapte os seletores `.loader, [data-loader]` para o que o projeto realmente usa.

### Fix 3 · Corrigir `lang="pt-BR"` para `lang="en"`
**Arquivo:** `index.html` (linha 1-2)

```html
<!-- ❌ Antes -->
<html lang="pt-BR">

<!-- ✅ Depois -->
<html lang="en">
```

**Por quê:** Todo conteúdo do site está em inglês ("Designing the quiet luxury of tomorrow's interfaces…"). Screen readers em pt-BR vão ler o inglês com fonética portuguesa (ex: "Designing" vira "DEH-SIG-NING"). Quebra acessibilidade pra usuários assistivos e prejudica SEO multilíngue.

---

## P1 — ALTOS (mesma sessão)

### Fix 4 · Adicionar Open Graph + Twitter Card meta tags
**Arquivo:** `index.html` (dentro do `<head>`)

```html
<meta property="og:type" content="website">
<meta property="og:title" content="OBSIDIAN — Studio of Considered Interfaces">
<meta property="og:description" content="An independent design studio crafting considered digital experiences. Lisbon, MMXXVI.">
<meta property="og:image" content="https://obsidian.design/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:url" content="https://obsidian.design/">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="OBSIDIAN — Studio of Considered Interfaces">
<meta name="twitter:description" content="An independent design studio crafting considered digital experiences. Lisbon, MMXXVI.">
<meta name="twitter:image" content="https://obsidian.design/og-image.jpg">
<link rel="canonical" href="https://obsidian.design/">
```

**Importante:** Crie também um arquivo `og-image.jpg` (1200×630) com a identidade visual do studio. Pode ser o H1 "Designing the quiet luxury of tomorrow's interfaces" em Fraunces sobre off-black com o accent terracotta sutil.

### Fix 5 · Adicionar favicon SVG
**Arquivo:** `index.html`

```html
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
```

**Crie `favicon.svg`** com uma marca minimalista — sugestão: a letra "O" em Fraunces sobre fundo off-black, ou um pequeno círculo (referência ao dot que aparece como element separator no site). 32×32 viewBox.

### Fix 6 · Adicionar JSON-LD structured data
**Arquivo:** `index.html` (final do `<head>`)

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "OBSIDIAN Studio",
  "description": "An independent design studio crafting considered digital experiences.",
  "url": "https://obsidian.design",
  "email": "studio@obsidian.design",
  "telephone": "+351 21 0000 000",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "Rua das Janelas Verdes, 27",
    "postalCode": "1200-690",
    "addressLocality": "Lisbon",
    "addressCountry": "PT"
  },
  "foundingDate": "2025"
}
</script>
```

---

## P2 — MÉDIOS (próxima sprint)

### Fix 7 · Renderizar H1 no DOM inicial (mesmo escondido)
Hoje o H1 provavelmente é injetado via JS depois do loader. Mude para que ele já esteja no HTML estático com `opacity: 0` controlado por CSS — assim crawlers do Google e screen readers leem imediatamente.

### Fix 8 · Adicionar focus-visible explícito
**Arquivo:** `styles.css`

```css
*:focus-visible {
  outline: 2px solid var(--accent-terracotta);
  outline-offset: 4px;
  border-radius: 2px;
}
```

### Fix 9 · Skip link
**Arquivo:** `index.html` (logo após `<body>`)

```html
<a href="#main" class="skip-link">Skip to content</a>
```

```css
.skip-link {
  position: absolute;
  left: -9999px;
  top: 0;
  background: var(--bg);
  color: var(--fg);
  padding: 1rem 1.5rem;
  z-index: 999;
}
.skip-link:focus {
  left: 1rem;
  top: 1rem;
}
```

---

## Critérios de verificação (rodar antes de declarar pronto)

Aplique `verification-before-completion` ao final. **Não declare pronto sem provar:**

1. **Performance** — rodar no Chrome DevTools (modo Incognito, Network: Fast 3G simulado):
   ```js
   performance.getEntriesByType('paint')
   ```
   Expected: `first-contentful-paint < 1800`

2. **Acessibilidade** — instalar/rodar [axe DevTools](https://www.deque.com/axe/devtools/) e confirmar:
   - 0 violations critical
   - 0 violations serious
   - lang attribute correto
   - meta description presente

3. **SEO** — verificar Open Graph com [opengraph.xyz](https://www.opengraph.xyz/):
   - Preview do site mostra título, descrição e imagem corretamente
   - Twitter Card preview funciona

4. **Reduced-motion** — testar em macOS: System Settings → Accessibility → Display → "Reduce motion" → ON. Recarregar site. Confirmar que loader é pulado e conteúdo aparece imediatamente.

5. **Lang correto** — abrir VoiceOver (Cmd+F5 no Mac), navegar pela página, confirmar que o H1 é lido em inglês americano.

6. **Lighthouse score** (Chrome DevTools → Lighthouse → Mobile + Performance + Accessibility + Best Practices + SEO):
   - Performance ≥ 90
   - Accessibility ≥ 95
   - Best Practices ≥ 95
   - SEO ≥ 95

## Regras de execução

- **NÃO** mude a direção estética (mantenha Fraunces, off-black, terracotta accent, mono labels)
- **NÃO** rewrite — aplique fixes cirúrgicos
- **NÃO** adicione libs novas — todos os fixes são CSS/HTML inline ou JS mínimo
- **NÃO** corte código nem use placeholders (`// rest of code`, `// TODO`) — entregue tudo completo (skill `output-enforcement` ativa)
- Após cada P0 → faça um commit semântico antes de partir pro próximo
- Ao final, mostre `git diff --stat` e os screenshots before/after do Lighthouse

## Output esperado

1. Diff completo de `index.html`, `styles.css`, `script.js`
2. Conteúdo dos novos arquivos `favicon.svg` e (opcionalmente) `og-image.jpg` se conseguir gerar
3. Resultado do `performance.getEntriesByType('paint')` antes/depois
4. Lighthouse score antes/depois
5. Commit history com mensagens semânticas (feat/fix por categoria: perf, a11y, seo)
