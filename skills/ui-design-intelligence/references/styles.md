# Styles Reference — UI Design Intelligence

67 estilos visuais curados. Para cada estilo: nome, atmosfera, quando usar, tokens CSS base, anti-patterns.

---

## Estilos Modernos

### Glassmorphism
**Atmosfera:** Translúcido, etéreo, futurista  
**Quando usar:** Apps premium, landing pages tech, dashboards dark  
**Tokens CSS:**
```css
--glass-bg: rgba(255, 255, 255, 0.1);
--glass-border: rgba(255, 255, 255, 0.2);
--glass-blur: blur(16px);
--glass-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
```
**Anti-pattern:** Usar em fundos claros sem contraste suficiente

### Claymorphism
**Atmosfera:** Suave, tridimensional, amigável, lúdico  
**Quando usar:** Apps infantis, produtos de saúde mental, onboarding  
**Tokens CSS:**
```css
--clay-shadow: 8px 8px 0px rgba(0, 0, 0, 0.15), -4px -4px 0px rgba(255, 255, 255, 0.6);
--clay-radius: 24px;
--clay-bg: #f0f4ff;
```
**Anti-pattern:** Usar em contextos financeiros/corporativos sérios

### Bento Grid
**Atmosfera:** Editorial, organizado, moderno, Apple-like  
**Quando usar:** Portfólios, landing pages de produto, apresentações de feature  
**Grid pattern:** `grid-cols-4`, células de tamanhos variados (1x1, 2x1, 1x2, 2x2)  
**Anti-pattern:** Usar quando o conteúdo não tem hierarquia visual clara

### Neumorphism
**Atmosfera:** Suave, monocromático, físico  
**Quando usar:** Apps de música, timers, controles deslizantes  
**Tokens CSS:**
```css
--neu-shadow-light: -6px -6px 12px rgba(255,255,255,0.8);
--neu-shadow-dark: 6px 6px 12px rgba(0,0,0,0.15);
--neu-bg: #e0e5ec;
```
**Anti-pattern:** Usar com acessibilidade como requisito — contraste é crítico

### Brutalism
**Atmosfera:** Raw, direto, anti-design, memorável  
**Quando usar:** Portfólios de devs, ferramentas para devs, projetos indie  
**Características:** Bordas 2-4px preto sólido, sombras offset, tipografia bold  
**Anti-pattern:** Usar em produtos enterprise ou healthcare

### AI-Native UI
**Atmosfera:** Futurista, inteligente, em movimento  
**Quando usar:** Produtos de IA, interfaces de chat, assistentes  
**Características:** Gradientes animados, bordas sutis pulsantes, tipografia mono para outputs  
**Anti-pattern:** Usar quando o produto não tem componente de IA real

---

## Estilos Corporativos

### Corporate Clean
**Atmosfera:** Profissional, confiável, neutro  
**Quando usar:** B2B SaaS, ERPs, sistemas de gestão, contabilidade  
**Paleta base:** Azul navy + cinza neutro + branco  
**Tokens:** Border-radius: 6px | Shadow: sutil | Tipografia: Inter/DM Sans

### Enterprise Dark
**Atmosfera:** Sério, técnico, premium B2B  
**Quando usar:** Dashboards analíticos, plataformas de trading, monitoramento  
**Paleta base:** #0f1117 fundo + #1e2330 superfície + azul/verde como accent

### Government / Legal
**Atmosfera:** Austero, formal, acessível  
**Quando usar:** Sistemas jurídicos, plataformas regulatórias, portais gov  
**Características:** Sem gradientes, tipografia serif para títulos, alto contraste WCAG AA

### Fintech Modern
**Atmosfera:** Confiável + moderno + premium  
**Quando usar:** Apps de banco, investimentos, carteiras digitais  
**Paleta base:** Azul escuro + verde como positivo + vermelho como negativo  
**Tokens:** Dados numéricos em fonte mono, verde #00c896 para ganho, vermelho #ff4757 para perda

---

## Estilos por Indústria

### Healthcare / Wellness
**Atmosfera:** Calmo, limpo, humanizado  
**Quando usar:** Apps médicos, telemedicina, bem-estar, nutrição  
**Paleta:** Verde suave + azul teal + branco + tons de areia  
**Regra:** Nunca usar vermelho para ações primárias — reservar para alertas médicos

### E-commerce Premium
**Atmosfera:** Aspiracional, limpo, produto em foco  
**Quando usar:** Fashion, luxo, produtos de alto valor  
**Características:** Muito espaço em branco, tipografia elegante, imagens em destaque

### E-commerce Popular
**Atmosfera:** Energético, urgente, conversão-focado  
**Quando usar:** Marketplaces, varejo, produtos de massa  
**Características:** CTAs grandes, badges de desconto, social proof visível

### EdTech
**Atmosfera:** Engajante, acessível, motivador  
**Quando usar:** Plataformas de ensino, cursos, quizzes  
**Paleta:** Roxo + laranja como accent + fundo neutro claro  
**Gamification tokens:** Badges, progress bars, streaks

### Gaming
**Atmosfera:** Imersivo, dark, enérgico  
**Quando usar:** Plataformas de gaming, eSports, comunidades  
**Paleta:** Muito escuro + neon (verde, roxo, azul) como accent

### Beauty / Lifestyle
**Atmosfera:** Elegante, feminino ou neutro, aspiracional  
**Quando usar:** Beleza, moda, lifestyle, bem-estar premium  
**Paleta:** Rosa/bege/dourado + muito branco  
**Tipografia:** Serif elegante para headings

### Tourism / Travel
**Atmosfera:** Aventureiro, colorido, inspirador  
**Quando usar:** Marketplaces de turismo, agências, apps de viagem  
**Paleta:** Azul oceano + verde natureza + laranja amanhecer

---

## Estilos por Abordagem

### Minimal / Swiss
**Atmosfera:** Máximo conteúdo, mínimo estilo  
**Quando usar:** Ferramentas de produtividade, editores, apps de foco  
**Regra:** Espaçamento generoso, tipografia é o design, sem decoração

### Dark Mode First
**Atmosfera:** Técnico, confortável para uso prolongado  
**Quando usar:** IDEs, dashboards de dev, monitoring, ferramentas CLI-adjacent  
**Tokens:** Fundo #0d1117 (GitHub-like) ou #1a1a2e ou #111827

### Warm Neutral
**Atmosfera:** Acolhedor, humano, artesanal  
**Quando usar:** Blogs, newsletters, produtos de criadores, comunidades  
**Paleta:** Creme/areia + marrom quente + verde musgo como accent

### Gradient Modern
**Atmosfera:** Vibrante, contemporâneo, energético  
**Quando usar:** Landing pages de startup, apps consumer, produtos criativos  
**Padrão:** Gradiente sutil no hero, flat no restante — nunca gradiente em todo o layout

### Skeuomorphic Subtle
**Atmosfera:** Tangível, familiar, confortável  
**Quando usar:** Apps de notas, calendários, ferramentas analógicas digitalizadas  
**Características:** Texturas sutis, sombras realistas, ícones tridimensionais leves

---

## Como selecionar o estilo certo

1. **Tipo de produto** → filtra metade dos estilos imediatamente
2. **Público-alvo** → B2B vs B2C, técnico vs leigo, jovem vs sênior
3. **Emoção desejada** → confiança, excitação, calma, urgência
4. **Keywords do usuário** → mapear para estilos compatíveis
5. **Restrições** → acessibilidade, conformidade regulatória, marca existente
