# Typography Pairs — UI Design Intelligence

57 combinações tipográficas curadas. Organizadas por atmosfera. Todas usam Google Fonts (gratuito).

---

## Como usar

```html
<!-- Exemplo de import -->
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:wght@700&display=swap" rel="stylesheet">
```

```css
/* Aplicação dos tokens */
:root {
  --font-heading: 'Playfair Display', serif;
  --font-body: 'Inter', sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
}
```

---

## Corporativo / Profissional

| Par | Heading | Body | Mono | Quando usar |
|---|---|---|---|---|
| **Corporate Standard** | Inter 700 | Inter 400 | JetBrains Mono | SaaS B2B, ERPs, dashboards |
| **Corporate Refined** | DM Sans 700 | DM Sans 400 | — | Plataformas B2B modernas |
| **Professional Serif** | Merriweather 700 | Source Sans Pro | — | Jurídico, relatórios, governo |
| **Executive** | Fraunces 700 | Inter 400 | — | Consultoria, premium B2B |
| **Clean Authority** | Space Grotesk 700 | Space Grotesk 400 | Space Mono | Fintech, analytics |

---

## Moderno / Tech

| Par | Heading | Body | Mono | Quando usar |
|---|---|---|---|---|
| **Tech Default** | Inter 800 | Inter 400 | Fira Code | Dev tools, dashboards tech |
| **Modern SaaS** | Outfit 700 | Outfit 400 | — | SaaS consumer, apps modernos |
| **Dark Tech** | JetBrains Mono | Inter | JetBrains Mono | IDEs, CLI tools, dev products |
| **AI Native** | Syne 700 | Inter 400 | IBM Plex Mono | Produtos de IA, interfaces futuristas |
| **Startup Bold** | Manrope 800 | Manrope 400 | — | Landing pages de startup |
| **Digital Agency** | Bebas Neue | Karla 400 | — | Agências, portfólios criativos |
| **Geometric** | Nunito Sans 700 | Nunito Sans 400 | — | Apps consumer, onboarding |

---

## Elegante / Premium

| Par | Heading | Body | Mono | Quando usar |
|---|---|---|---|---|
| **Luxury Classic** | Playfair Display 700 | Lato 400 | — | Moda, beleza premium, lifestyle |
| **Editorial** | Cormorant Garamond 700 | Source Serif Pro | — | Publicações, revistas, blogs premium |
| **Refined Modern** | DM Serif Display 700 | DM Sans 400 | — | Fashion, portfólios elegantes |
| **Premium Serif** | Libre Baskerville 700 | Libre Baskerville 400 | — | Jurídico premium, consultoria |
| **Art Deco** | Josefin Sans 700 | Josefin Sans 300 | — | Beleza, estética, eventos |
| **Contemporary** | Raleway 700 | Raleway 400 | — | Portfólios, marcas criativas |

---

## Amigável / Consumer

| Par | Heading | Body | Mono | Quando usar |
|---|---|---|---|---|
| **Friendly Default** | Poppins 700 | Poppins 400 | — | Apps consumer, edtech, wellness |
| **Playful** | Nunito 800 | Nunito 400 | — | Apps infantis, games, onboarding |
| **Warm** | Quicksand 700 | Quicksand 400 | — | Saúde mental, wellness, nutrição |
| **Approachable** | Rubik 700 | Rubik 400 | — | Apps de comunidade, social |
| **Energetic** | Exo 2 700 | Exo 2 400 | — | Fitness, esportes, gaming |
| **Creative** | Pacifico 400 | Lato 400 | — | Artesanato, culinária, lifestyle |

---

## Editorial / Blog

| Par | Heading | Body | Quando usar |
|---|---|---|---|
| **Blog Classic** | Playfair Display | Georgia (system) | Blog pessoal, newsletter |
| **Medium Style** | Slab Serif (Zilla Slab) | Charter (system) | Publicações longas |
| **News** | Libre Baskerville | Source Serif 4 | Portais de notícias |
| **Modern Editorial** | DM Serif Display | DM Sans | Revistas digitais modernas |
| **Minimal Blog** | Inter | Georgia (system) | Blogs técnicos, documentação |

---

## Dashboards / Analytics

| Par | Heading | Body | Mono | Quando usar |
|---|---|---|---|---|
| **Data Dense** | Inter 600 | Inter 400 | Roboto Mono | Dashboards com muitos dados |
| **Analytics Clear** | DM Sans 600 | DM Sans 400 | DM Mono | Analytics, KPI boards |
| **Trading** | IBM Plex Sans 600 | IBM Plex Sans 400 | IBM Plex Mono | Fintech, trading, crypto |
| **Monitoring** | Space Grotesk 600 | Inter 400 | Space Mono | Monitoramento, DevOps |

---

## Mobile / App

| Par | Heading | Body | Quando usar |
|---|---|---|---|
| **iOS Style** | SF Pro (system) | SF Pro (system) | Apps iOS nativos |
| **Android Style** | Roboto (system) | Roboto (system) | Apps Android nativos |
| **Cross-platform Warm** | Nunito 700 | Nunito 400 | React Native, Flutter |
| **Cross-platform Pro** | Inter 700 | Inter 400 | Apps profissionais cross-platform |

---

## E-commerce

| Par | Heading | Body | Quando usar |
|---|---|---|---|
| **Marketplace** | Barlow 700 | Barlow 400 | Marketplaces, catálogos |
| **Fashion** | Cormorant Garamond | Jost | Moda, acessórios premium |
| **Sports** | Oswald 700 | Roboto 400 | Esportes, fitness, outdoor |
| **Food** | Lobster | Raleway 400 | Restaurantes, delivery, culinária |

---

## Regras de tipografia

1. **Nunca misturar mais de 2 famílias** (+ 1 mono opcional)
2. **Contraste de peso** — heading precisa ser notavelmente mais pesado que body
3. **Contraste de estilo** — serif heading + sans body funciona bem; o inverso também
4. **Hierarquia de tamanhos** — heading mínimo 1.5x o tamanho do body
5. **Line-height** — body: 1.5–1.7 | heading: 1.1–1.3
6. **Letter-spacing** — headings grandes: -0.02em a -0.04em | body: 0 | labels: 0.05em
7. **Loading** — sempre usar `display=swap` e `font-display: swap` para performance
