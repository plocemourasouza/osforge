# Styles Reference — UI Design Intelligence

84 estilos visuais curados. Para cada estilo: atmosfera, quando usar, tokens CSS base, anti-pattern.

---

## General

### Minimalism & Swiss Style
**Atmosfera:** Clean, simple, spacious, functional, white space, high contrast, geometric, sans-serif, grid-based, essential  
**Quando usar:** Enterprise apps, dashboards, documentation sites, SaaS platforms, professional tools  
**Tokens CSS:**
```css
--spacing: 2rem;
--border-radius: 0px;
--font-weight: 400-700;
--shadow: none;
--accent-color: single primary only;
```
**Anti-pattern:** Creative portfolios, entertainment, playful brands, artistic experiments

### Neumorphism
**Atmosfera:** Soft UI, embossed, debossed, convex, concave, light source, subtle depth, rounded (12-16px), monochromatic  
**Quando usar:** Health/wellness apps, meditation platforms, fitness trackers, minimal interaction UIs  
**Tokens CSS:**
```css
--border-radius: 14px;
--shadow-soft-1: -5px -5px 15px;
--shadow-soft-2: 5px 5px 15px;
--color-light: #F5F5F5;
--color-primary: single pastel;
```
**Anti-pattern:** Complex apps, critical accessibility, data-heavy dashboards, high-contrast required

### Glassmorphism
**Atmosfera:** Frosted glass, transparent, blurred background, layered, vibrant background, light source, depth, multi-layer  
**Quando usar:** Modern SaaS, financial dashboards, high-end corporate, lifestyle apps, modal overlays, navigation  
**Tokens CSS:**
```css
--blur-amount: 15px;
--glass-opacity: 0.15;
--border-color: rgba(255,255,255,0.2);
--background: vibrant color;
--text-color: light/dark based on BG;
```
**Anti-pattern:** Low-contrast backgrounds, critical accessibility, performance-limited, dark text on dark

### Brutalism
**Atmosfera:** Raw, unpolished, stark, high contrast, plain text, default fonts, visible borders, asymmetric, anti-design  
**Quando usar:** Design portfolios, artistic projects, counter-culture brands, editorial/media sites, tech blogs  
**Tokens CSS:**
```css
--border-radius: 0px;
--transition-duration: 0s;
--font-weight: 700-900;
--colors: primary only;
--border-style: visible;
--grid-visible: true;
```
**Anti-pattern:** Corporate environments, conservative industries, critical accessibility, customer-facing professional

### 3D & Hyperrealism
**Atmosfera:** Depth, realistic textures, 3D models, spatial navigation, tactile, skeuomorphic elements, rich detail, immersive  
**Quando usar:** Gaming, product showcase, immersive experiences, high-end e-commerce, architectural viz, VR/AR  
**Tokens CSS:**
```css
--perspective: 1000px;
--parallax-layers: 5;
--lighting-intensity: realistic;
--shadow-depth: 20-40%;
--animation-duration: 300-400ms;
```
**Anti-pattern:** Low-end mobile, performance-limited, critical accessibility, data tables/forms

### Vibrant & Block-based
**Atmosfera:** Bold, energetic, playful, block layout, geometric shapes, high color contrast, duotone, modern, energetic  
**Quando usar:** Startups, creative agencies, gaming, social media, youth-focused, entertainment, consumer  
**Tokens CSS:**
```css
--block-gap: 48px;
--typography-size: 32px+;
--color-palette: 4-6 vibrant colors;
--animation: continuous pattern;
--contrast-ratio: 7:1+;
```
**Anti-pattern:** Financial institutions, healthcare, formal business, government, conservative, elderly

### Dark Mode (OLED)
**Atmosfera:** Dark theme, low light, high contrast, deep black, midnight blue, eye-friendly, OLED, night mode, power efficient  
**Quando usar:** Night-mode apps, coding platforms, entertainment, eye-strain prevention, OLED devices, low-light  
**Tokens CSS:**
```css
--bg-black: #000000;
--bg-dark-grey: #121212;
--text-primary: #FFFFFF;
--accent-neon: neon colors;
--glow-effect: minimal;
--oled-optimized: true;
```
**Anti-pattern:** Print-first content, high-brightness outdoor, color-accuracy-critical

### Accessible & Ethical
**Atmosfera:** High contrast, large text (16px+), keyboard navigation, screen reader friendly, WCAG compliant, focus state, semantic  
**Quando usar:** Government, healthcare, education, inclusive products, large audience, legal compliance, public  
**Tokens CSS:**
```css
--contrast-ratio: 7:1;
--font-size-min: 16px;
--focus-ring: 3-4px;
--touch-target: 44x44px;
--wcag-level: AAA;
--keyboard-accessible: true;
--sr-tested: true;
```
**Anti-pattern:** None - accessibility universal

### Claymorphism
**Atmosfera:** Soft 3D, chunky, playful, toy-like, bubbly, thick borders (3-4px), double shadows, rounded (16-24px)  
**Quando usar:** Educational apps, children's apps, SaaS platforms, creative tools, fun-focused, onboarding, casual games  
**Tokens CSS:**
```css
--border-radius: 20px;
--border-width: 3-4px;
--shadow-inner: inset -2px -2px 8px;
--shadow-outer: 4px 4px 8px;
--color-palette: pastels;
--animation: bounce;
```
**Anti-pattern:** Formal corporate, professional services, data-critical, serious/medical, legal apps, finance

### Aurora UI
**Atmosfera:** Vibrant gradients, smooth blend, Northern Lights effect, mesh gradient, luminous, atmospheric, abstract  
**Quando usar:** Modern SaaS, creative agencies, branding, music platforms, lifestyle, premium products, hero sections  
**Tokens CSS:**
```css
--gradient-colors: complementary pairs;
--animation-duration: 8-12s;
--blend-mode: screen;
--color-saturation: 1.2;
--effect: iridescent;
--loop-smooth: true;
```
**Anti-pattern:** Data-heavy dashboards, critical accessibility, content-heavy where distraction issues

### Retro-Futurism
**Atmosfera:** Vintage sci-fi, 80s aesthetic, neon glow, geometric patterns, CRT scanlines, pixel art, cyberpunk, synthwave  
**Quando usar:** Gaming, entertainment, music platforms, tech brands, artistic projects, nostalgic, cyberpunk  
**Tokens CSS:**
```css
--neon-colors: #0080FF #FF006E #00FFFF;
--background: #000000;
--font-family: monospace;
--effect: glitch+glow;
--scanline-opacity: 0.3;
--crt-effect: true;
```
**Anti-pattern:** Conservative industries, critical accessibility, professional/corporate, elderly, legal/finance

### Flat Design
**Atmosfera:** 2D, minimalist, bold colors, no shadows, clean lines, simple shapes, typography-focused, modern, icon-heavy  
**Quando usar:** Web apps, mobile apps, cross-platform, startup MVPs, user-friendly, SaaS, dashboards, corporate  
**Tokens CSS:**
```css
--shadow: none;
--color-palette: 4-6 solid;
--border-radius: 2px;
--gradient: none;
--icons: simplified SVG;
--animation: minimal 150-200ms;
```
**Anti-pattern:** Complex 3D, premium/luxury, artistic portfolios, immersive experiences, high-detail

### Skeuomorphism
**Atmosfera:** Realistic, texture, depth, 3D appearance, real-world metaphors, shadows, gradients, tactile, detailed, material  
**Quando usar:** Legacy apps, gaming, immersive storytelling, premium products, luxury, realistic simulations, education  
**Tokens CSS:**
```css
--gradient-stops: 8-12;
--texture-overlay: noise+grain;
--shadow-layers: 3+;
--animation-duration: 300-500ms;
--depth-effect: pronounced;
--tactile: true;
```
**Anti-pattern:** Modern enterprise, critical accessibility, low-performance, web (use Flat/Modern)

### Liquid Glass
**Atmosfera:** Flowing glass, morphing, smooth transitions, fluid effects, translucent, animated blur, iridescent, chromatic aberration  
**Quando usar:** Premium SaaS, high-end e-commerce, creative platforms, branding experiences, luxury portfolios  
**Tokens CSS:**
```css
--morph-duration: 400-600ms;
--blur-amount: 15px;
--chromatic-aberration: true;
--iridescent: true;
--blend-mode: screen;
--smooth-transitions: true;
```
**Anti-pattern:** Performance-limited, critical accessibility, complex data, budget projects

### Motion-Driven
**Atmosfera:** Animation-heavy, microinteractions, smooth transitions, scroll effects, parallax, entrance anim, page transitions  
**Quando usar:** Portfolio sites, storytelling platforms, interactive experiences, entertainment apps, creative, SaaS  
**Tokens CSS:**
```css
--animation-duration: 300-400ms;
--parallax-layers: 5;
--scroll-behavior: smooth;
--gpu-accelerated: true;
--entrance-animation: true;
--page-transition: smooth;
```
**Anti-pattern:** Data dashboards, critical accessibility, low-power devices, content-heavy, motion-sensitive

### Micro-interactions
**Atmosfera:** Small animations, gesture-based, tactile feedback, subtle animations, contextual interactions, responsive  
**Quando usar:** Mobile apps, touchscreen UIs, productivity tools, user-friendly, consumer apps, interactive components  
**Tokens CSS:**
```css
--micro-animation-duration: 50-100ms;
--gesture-responsive: true;
--haptic-feedback: true;
--loading-animation: smooth;
--state-feedback: success+error;
```
**Anti-pattern:** Desktop-only, critical performance, accessibility-first (alternatives needed)

### Inclusive Design
**Atmosfera:** Accessible, color-blind friendly, high contrast, haptic feedback, voice interaction, screen reader, WCAG AAA, universal  
**Quando usar:** Public services, education, healthcare, finance, government, accessible consumer, inclusive  
**Tokens CSS:**
```css
--contrast-ratio: 7:1;
--font-size: 16px+;
--keyboard-accessible: true;
--sr-compatible: true;
--wcag-level: AAA;
--color-symbols: true;
--haptic: enabled;
```
**Anti-pattern:** None - accessibility universal

### Zero Interface
**Atmosfera:** Minimal visible UI, voice-first, gesture-based, AI-driven, invisible controls, predictive, context-aware, ambient  
**Quando usar:** Voice assistants, AI platforms, future-forward UX, smart home, contextual computing, ambient experiences  
**Tokens CSS:**
```css
--voice-ui: enabled;
--gesture-detection: active;
--ai-predictions: smart;
--progressive-disclosure: true;
--visible-ui: minimal;
--context-aware: true;
```
**Anti-pattern:** Complex workflows, data-entry heavy, traditional systems, legacy support, explicit control

### Soft UI Evolution
**Atmosfera:** Evolved soft UI, better contrast, modern aesthetics, subtle depth, accessibility-focused, improved shadows, hybrid  
**Quando usar:** Modern enterprise apps, SaaS platforms, health/wellness, modern business tools, professional, hybrid  
**Tokens CSS:**
```css
--shadow-soft: modern blend;
--border-radius: 10px;
--animation-duration: 200-300ms;
--contrast-ratio: 4.5:1+;
--color-hierarchy: improved;
--wcag-level: AA+;
```
**Anti-pattern:** Extreme minimalism, critical performance, systems without modern OS

### Neubrutalism
**Atmosfera:** Bold borders, black outlines, primary colors, thick shadows, no gradients, flat colors, 45° shadows, playful, Gen Z  
**Quando usar:** Gen Z brands, startups, creative agencies, Figma-style apps, Notion-style interfaces, tech blogs  
**Tokens CSS:**
```css
--border-width: 3px;
--shadow-offset: 4px;
--shadow-color: #000;
--colors: high saturation;
--font: bold sans;
```
**Anti-pattern:** Luxury brands, finance, healthcare, conservative industries (too playful)

### Bento Box Grid
**Atmosfera:** Modular cards, asymmetric grid, varied sizes, Apple-style, dashboard tiles, negative space, clean hierarchy, cards  
**Quando usar:** Dashboards, product pages, portfolios, Apple-style marketing, feature showcases, SaaS  
**Tokens CSS:**
```css
--grid-gap: 16px;
--card-radius: 24px;
--card-bg: #FFFFFF;
--page-bg: #F5F5F7;
--shadow: 0 4px 6px rgba(0,0,0,0.05);
--hover-scale: 1.02;
```
**Anti-pattern:** Dense data tables, text-heavy content, real-time monitoring

### Y2K Aesthetic
**Atmosfera:** Neon pink, chrome, metallic, bubblegum, iridescent, glossy, retro-futurism, 2000s, futuristic nostalgia  
**Quando usar:** Fashion brands, music platforms, Gen Z brands, nostalgia marketing, entertainment, youth-focused  
**Tokens CSS:**
```css
--neon-pink: #FF69B4;
--neon-cyan: #00FFFF;
--chrome-silver: #C0C0C0;
--glossy-gradient: linear-gradient(180deg, white 0%, transparent 50%);
--glow-blur: 10px;
```
**Anti-pattern:** B2B enterprise, healthcare, finance, conservative industries, elderly users

### Cyberpunk UI
**Atmosfera:** Neon, dark mode, terminal, HUD, sci-fi, glitch, dystopian, futuristic, matrix, tech noir  
**Quando usar:** Gaming platforms, tech products, crypto apps, sci-fi applications, developer tools, entertainment  
**Tokens CSS:**
```css
--bg-dark: #0D0D0D;
--neon-green: #00FF00;
--neon-magenta: #FF00FF;
--neon-cyan: #00FFFF;
--scanline-opacity: 0.1;
--glitch-duration: 0.3s;
```
**Anti-pattern:** Corporate enterprise, healthcare, family apps, conservative brands, elderly users

### Organic Biophilic
**Atmosfera:** Nature, organic shapes, green, sustainable, rounded, flowing, wellness, earthy, natural textures  
**Quando usar:** Wellness apps, sustainability brands, eco products, health apps, meditation, organic food brands  
**Tokens CSS:**
```css
--forest-green: #228B22;
--earth-brown: #8B4513;
--sky-blue: #87CEEB;
--cream-bg: #F5F5DC;
--organic-radius: 24px;
--shadow-soft: 0 8px 32px rgba(0,0,0,0.08);
```
**Anti-pattern:** Tech-focused products, gaming, industrial, urban brands

### AI-Native UI
**Atmosfera:** Chatbot, conversational, voice, assistant, agentic, ambient, minimal chrome, streaming text, AI interactions  
**Quando usar:** AI products, chatbots, voice assistants, copilots, AI-powered tools, conversational interfaces  
**Tokens CSS:**
```css
--ai-accent: #6366F1;
--user-bubble-bg: #E0E7FF;
--ai-bubble-bg: #F9FAFB;
--input-height: 48px;
--typing-dot-size: 8px;
--message-gap: 16px;
```
**Anti-pattern:** Traditional forms, data-heavy dashboards, print-first content

### Memphis Design
**Atmosfera:** 80s, geometric, playful, postmodern, shapes, patterns, squiggles, triangles, neon, abstract, bold  
**Quando usar:** Creative agencies, music sites, youth brands, event promotion, artistic portfolios, entertainment  
**Tokens CSS:**
```css
--memphis-pink: #FF71CE;
--memphis-yellow: #FFCE5C;
--memphis-teal: #86CCCA;
--memphis-purple: #6A7BB4;
--pattern-size: 20px;
--shape-rotation: 15deg;
```
**Anti-pattern:** Corporate finance, healthcare, legal, elderly users, conservative brands

### Vaporwave
**Atmosfera:** Synthwave, retro-futuristic, 80s-90s, neon, glitch, nostalgic, sunset gradient, dreamy, aesthetic  
**Quando usar:** Music platforms, gaming, creative portfolios, tech startups, entertainment, artistic projects  
**Tokens CSS:**
```css
--vapor-pink: #FF71CE;
--vapor-cyan: #01CDFE;
--vapor-mint: #05FFA1;
--vapor-purple: #B967FF;
--grid-color: rgba(255,255,255,0.1);
--glow-intensity: 15px;
```
**Anti-pattern:** Business apps, e-commerce, education, healthcare, enterprise software

### Dimensional Layering
**Atmosfera:** Depth, overlapping, z-index, layers, 3D, shadows, elevation, floating, cards, spatial hierarchy  
**Quando usar:** Dashboards, card layouts, modals, navigation, product showcases, SaaS interfaces  
**Tokens CSS:**
```css
--elevation-1: 0 1px 3px rgba(0,0,0,0.1);
--elevation-2: 0 4px 6px rgba(0,0,0,0.1);
--elevation-3: 0 10px 20px rgba(0,0,0,0.1);
--elevation-4: 0 20px 40px rgba(0,0,0,0.15);
--blur-amount: 8px;
```
**Anti-pattern:** Print-style layouts, simple blogs, low-end devices, flat design requirements

### Exaggerated Minimalism
**Atmosfera:** Bold minimalism, oversized typography, high contrast, negative space, loud minimal, statement design  
**Quando usar:** Fashion, architecture, portfolios, agency landing pages, luxury brands, editorial  
**Tokens CSS:**
```css
--type-giant: clamp(3rem, 10vw, 12rem);
--type-weight: 900;
--spacing-huge: 8rem;
--color-primary: #000000;
--color-bg: #FFFFFF;
--accent: single color only;
```
**Anti-pattern:** E-commerce catalogs, dashboards, forms, data-heavy, elderly users, complex apps

### Kinetic Typography
**Atmosfera:** Motion text, animated type, moving letters, dynamic, typing effect, morphing, scroll-triggered text  
**Quando usar:** Hero sections, marketing sites, video platforms, storytelling, creative portfolios, landing pages  
**Tokens CSS:**
```css
--text-animation-duration: 1s;
--letter-delay: 0.05s;
--typing-speed: 100ms;
--gradient-text: linear-gradient(90deg, #color1, #color2);
--morph-duration: 0.5s;
```
**Anti-pattern:** Long-form content, accessibility-critical, data interfaces, forms, elderly users

### Parallax Storytelling
**Atmosfera:** Scroll-driven, narrative, layered scrolling, immersive, progressive disclosure, cinematic, scroll-triggered  
**Quando usar:** Brand storytelling, product launches, case studies, portfolios, annual reports, marketing campaigns  
**Tokens CSS:**
```css
--parallax-speed-bg: 0.3;
--parallax-speed-mid: 0.6;
--parallax-speed-fg: 1;
--section-height: 100vh;
--transition-duration: 600ms;
--perspective: 1px;
```
**Anti-pattern:** E-commerce, dashboards, mobile-first, SEO-critical, accessibility-required

### Swiss Modernism 2.0
**Atmosfera:** Grid system, Helvetica, modular, asymmetric, international style, rational, clean, mathematical spacing  
**Quando usar:** Corporate sites, architecture, editorial, SaaS, museums, professional services, documentation  
**Tokens CSS:**
```css
--grid-columns: 12;
--grid-gap: 1rem;
--base-unit: 8px;
--font-primary: Inter;
--color-text: #000000;
--color-bg: #FFFFFF;
--accent: single vibrant;
```
**Anti-pattern:** Playful brands, children's sites, entertainment, gaming, emotional storytelling

### HUD / Sci-Fi FUI
**Atmosfera:** Futuristic, technical, wireframe, neon, data, transparency, iron man, sci-fi, interface  
**Quando usar:** Sci-fi games, space tech, cybersecurity, movie props, immersive dashboards  
**Tokens CSS:**
```css
--hud-color: #00FFFF;
--bg-color: rgba(0,10,20,0.9);
--line-width: 1px;
--glow: 0 0 5px;
--font: monospace;
```
**Anti-pattern:** Standard corporate, reading heavy content, accessible public services

### Pixel Art
**Atmosfera:** Retro, 8-bit, 16-bit, gaming, blocky, nostalgic, pixelated, arcade  
**Quando usar:** Indie games, retro tools, creative portfolios, nostalgia marketing, Web3/NFT  
**Tokens CSS:**
```css
--pixel-size: 4px;
--font: pixel font;
--border-style: pixel-shadow;
--anti-alias: none;
```
**Anti-pattern:** Professional corporate, modern SaaS, high-res photography sites

### Bento Grids
**Atmosfera:** Apple-style, modular, cards, organized, clean, hierarchy, grid, rounded, soft  
**Quando usar:** Product features, dashboards, personal sites, marketing summaries, galleries  
**Tokens CSS:**
```css
--grid-gap: 20px;
--card-radius: 24px;
--card-bg: #FFFFFF;
--page-bg: #F5F5F7;
--shadow: soft;
```
**Anti-pattern:** Long-form reading, data tables, complex forms

### Spatial UI (VisionOS)
**Atmosfera:** Glass, depth, immersion, spatial, translucent, gaze, gesture, apple, vision-pro  
**Quando usar:** Spatial computing apps, VR/AR interfaces, immersive media, futuristic dashboards  
**Tokens CSS:**
```css
--glass-bg: rgba(255,255,255,0.2);
--glass-blur: 40px;
--glass-saturate: 180%;
--window-radius: 24px;
--depth-shadow: 0 8px 32px rgba(0,0,0,0.1);
--focus-scale: 1.02;
```
**Anti-pattern:** Text-heavy documents, high-contrast requirements, non-3D capable devices

### E-Ink / Paper
**Atmosfera:** Paper-like, matte, high contrast, texture, reading, calm, slow tech, monochrome  
**Quando usar:** Reading apps, digital newspapers, minimal journals, distraction-free writing, slow-living brands  
**Tokens CSS:**
```css
--paper-bg: #FDFBF7;
--ink-color: #1A1A1A;
--pencil-grey: #4A4A4A;
--border-color: #E0E0E0;
--font-reading: Georgia;
--transition: none;
```
**Anti-pattern:** Gaming, video platforms, high-energy marketing, dark mode dependent apps

### Gen Z Chaos / Maximalism
**Atmosfera:** Chaos, clutter, stickers, raw, collage, mixed media, loud, internet culture, ironic  
**Quando usar:** Gen Z lifestyle brands, music artists, creative portfolios, viral marketing, fashion  
**Tokens CSS:**
```css
--chaos-pink: #FF00FF;
--chaos-green: #00FF00;
--chaos-yellow: #FFFF00;
--chaos-blue: #0000FF;
--jitter-amount: 5deg;
--saturate: 150%;
```
**Anti-pattern:** Corporate, government, healthcare, banking, serious tools

### Biomimetic / Organic 2.0
**Atmosfera:** Nature-inspired, cellular, fluid, breathing, generative, algorithms, life-like  
**Quando usar:** Sustainability tech, biotech, advanced health, meditation, generative art platforms  
**Tokens CSS:**
```css
--cellular-pink: #FF9999;
--chlorophyll: #00FF41;
--bioluminescent: #00FFFF;
--breathing-duration: 4s;
--morph-ease: cubic-bezier(0.4, 0, 0.2, 1);
--organic-blur: 20px;
```
**Anti-pattern:** Standard SaaS, data grids, strict corporate, accounting

### Anti-Polish / Raw Aesthetic
**Atmosfera:** Hand-drawn, collage, scanned textures, unfinished, imperfect, authentic, human, sketch, raw marks, creative process  
**Quando usar:** Creative portfolios, artist sites, indie brands, handmade products, authentic storytelling, editorial  
**Tokens CSS:**
```css
--paper-bg: #FAFAF8;
--pencil-color: #4A4A4A;
--marker-black: #1A1A1A;
--kraft-brown: #C4A77D;
--sketch-rotation: random(-3deg, 3deg);
--texture-opacity: 0.3;
```
**Anti-pattern:** Corporate enterprise, fintech, healthcare, government, polished SaaS

### Tactile Digital / Deformable UI
**Atmosfera:** Jelly buttons, chrome, clay, squishy, deformable, bouncy, physical, tactile feedback, press response  
**Quando usar:** Modern mobile apps, playful brands, entertainment, gaming UI, consumer products, interactive demos  
**Tokens CSS:**
```css
--press-scale: 0.95;
--bounce-duration: 400ms;
--spring-stiffness: 300;
--spring-damping: 20;
--material-glossy: linear-gradient(135deg, white 0%, transparent 60%);
--depth-shadow: 0 10px 30px rgba(0,0,0,0.2);
```
**Anti-pattern:** Enterprise software, data dashboards, accessibility-critical, professional tools

### Nature Distilled
**Atmosfera:** Muted earthy, skin tones, wood, soil, sand, terracotta, warmth, organic materials, handmade warmth  
**Quando usar:** Wellness brands, sustainable products, artisan goods, organic food, spa/beauty, home decor  
**Tokens CSS:**
```css
--terracotta: #C67B5C;
--sand-beige: #D4C4A8;
--warm-clay: #B5651D;
--soft-cream: #F5F0E1;
--olive-green: #6B7B3C;
--grain-opacity: 0.1;
```
**Anti-pattern:** Tech startups, gaming, nightlife, corporate finance, high-energy brands

### Interactive Cursor Design
**Atmosfera:** Custom cursor, cursor as tool, hover effects, cursor feedback, pointer transformation, cursor trail, magnetic cursor  
**Quando usar:** Creative portfolios, interactive experiences, agency sites, product showcases, gaming, entertainment  
**Tokens CSS:**
```css
--cursor-size: 20px;
--cursor-hover-scale: 1.5;
--magnetic-distance: 100px;
--trail-length: 10;
--trail-fade: 0.1;
--blend-mode: difference;
```
**Anti-pattern:** Mobile-first (no cursor), accessibility-critical, data-heavy dashboards, forms

### Voice-First Multimodal
**Atmosfera:** Voice UI, multimodal, audio feedback, conversational, hands-free, ambient, contextual, speech recognition  
**Quando usar:** Voice assistants, accessibility apps, hands-free tools, smart home, automotive UI, cooking apps  
**Tokens CSS:**
```css
--listening-color: #6B8FAF;
--speaking-color: #22C55E;
--waveform-height: 60px;
--pulse-duration: 1.5s;
--indicator-size: 24px;
--voice-accent: #9B8FBB;
```
**Anti-pattern:** Visual-heavy content, data entry, complex forms, noisy environments

### 3D Product Preview
**Atmosfera:** 360 product view, rotatable, zoomable, touch-to-spin, AR preview, product configurator, interactive 3D model  
**Quando usar:** E-commerce, furniture, fashion, automotive, electronics, jewelry, product configurators  
**Tokens CSS:**
```css
--canvas-bg: #F5F5F5;
--hotspot-color: #3B82F6;
--loading-spinner: primary;
--rotation-speed: 0.5;
--zoom-min: 0.5;
--zoom-max: 2;
```
**Anti-pattern:** Content-heavy sites, blogs, dashboards, low-bandwidth, accessibility-critical

### Gradient Mesh / Aurora Evolved
**Atmosfera:** Complex gradients, mesh gradients, multi-color blend, aurora effect, flowing colors, iridescent, holographic, prismatic  
**Quando usar:** Hero sections, backgrounds, creative brands, music platforms, fashion, lifestyle, premium products  
**Tokens CSS:**
```css
--mesh-color-1: #00FFFF;
--mesh-color-2: #FF00FF;
--mesh-color-3: #FFFF00;
--mesh-color-4: #00FF66;
--flow-duration: 10s;
--shimmer-intensity: 0.3;
```
**Anti-pattern:** Data interfaces, text-heavy content, accessibility-critical, conservative brands

### Editorial Grid / Magazine
**Atmosfera:** Magazine layout, asymmetric grid, editorial typography, pull quotes, drop caps, column layout, print-inspired  
**Quando usar:** News sites, blogs, magazines, editorial content, long-form articles, journalism, publishing  
**Tokens CSS:**
```css
--grid-cols: asymmetric;
--body-font: Georgia/Merriweather;
--heading-font: bold sans;
--drop-cap-size: 4em;
--pull-quote-size: 1.5em;
--column-gap: 2rem;
```
**Anti-pattern:** Dashboards, apps, e-commerce catalogs, real-time data, short-form content

### Chromatic Aberration / RGB Split
**Atmosfera:** RGB split, color fringing, glitch, retro tech, VHS, analog error, distortion, lens effect  
**Quando usar:** Music platforms, gaming, tech brands, creative portfolios, nightlife, entertainment, video platforms  
**Tokens CSS:**
```css
--rgb-offset: 2px;
--red-channel: #FF0000;
--green-channel: #00FF00;
--blue-channel: #0000FF;
--glitch-duration: 0.3s;
--scanline-opacity: 0.1;
```
**Anti-pattern:** Corporate, healthcare, finance, accessibility-critical, elderly users

### Vintage Analog / Retro Film
**Atmosfera:** Film grain, VHS, cassette tape, polaroid, analog warmth, faded colors, light leaks, vintage photography  
**Quando usar:** Photography portfolios, music/vinyl brands, vintage fashion, nostalgia marketing, film industry, cafes  
**Tokens CSS:**
```css
--sepia-amount: 20%;
--contrast: 1.1;
--saturation: 0.8;
--grain-opacity: 0.15;
--light-leak-color: rgba(255,200,100,0.2);
--warm-tint: #F5E6C8;
```
**Anti-pattern:** Modern tech, SaaS, healthcare, children's apps, corporate enterprise

## Landing Page

### Hero-Centric Design
**Atmosfera:** Large hero section, compelling headline, high-contrast CTA, product showcase, value proposition, hero image/video, dramatic visual  
**Quando usar:** SaaS landing pages, product launches, service landing pages, B2B platforms, tech companies  
**Tokens CSS:**
```css
--hero-min-height: 100vh;
--headline-size: clamp(2rem, 5vw, 4rem);
--cta-padding: 1rem 2rem;
--overlay-opacity: 0.5;
--text-shadow: 0 2px 4px rgba(0,0,0,0.3);
```
**Anti-pattern:** Complex navigation, multi-page experiences, data-heavy applications

### Conversion-Optimized
**Atmosfera:** Form-focused, minimalist design, single CTA focus, high contrast, urgency elements, trust signals, social proof, clear value  
**Quando usar:** E-commerce product pages, free trial signups, lead generation, SaaS pricing pages, limited-time offers  
**Tokens CSS:**
```css
--cta-color: high contrast primary;
--form-max-width: 600px;
--input-height: 48px;
--focus-ring: 3px solid accent;
--success-color: #22C55E;
--error-color: #EF4444;
```
**Anti-pattern:** Complex feature explanations, multi-product showcases, technical documentation

### Feature-Rich Showcase
**Atmosfera:** Multiple feature sections, grid layout, benefit cards, visual feature demonstrations, interactive elements, problem-solution pairs  
**Quando usar:** Enterprise SaaS, software tools landing pages, platform services, complex product explanations, B2B products  
**Tokens CSS:**
```css
--card-padding: 2rem;
--card-radius: 12px;
--icon-size: 48px;
--grid-gap: 2rem;
--section-padding: 4rem 0;
--hover-transform: translateY(-4px);
```
**Anti-pattern:** Simple product pages, early-stage startups with few features, entertainment landing pages

### Minimal & Direct
**Atmosfera:** Minimal text, white space heavy, single column layout, direct messaging, clean typography, visual-centric, fast-loading  
**Quando usar:** Simple service landing pages, indie products, consulting services, micro SaaS, freelancer portfolios  
**Tokens CSS:**
```css
--content-max-width: 680px;
--spacing-large: 4rem;
--font-size-body: 18px;
--line-height: 1.6;
--color-text: #1a1a1a;
--color-bg: #ffffff;
```
**Anti-pattern:** Feature-heavy products, complex explanations, multi-product showcases

### Social Proof-Focused
**Atmosfera:** Testimonials prominent, client logos displayed, case studies sections, reviews/ratings, user avatars, success metrics, credibility markers  
**Quando usar:** B2B SaaS, professional services, premium products, e-commerce conversion pages, established brands  
**Tokens CSS:**
```css
--avatar-size: 64px;
--logo-height: 40px;
--star-color: #FBBF24;
--metric-font-size: 3rem;
--testimonial-bg: #F9FAFB;
--blockquote-border: 4px solid accent;
```
**Anti-pattern:** Startup MVPs, products without users, niche/experimental products

### Interactive Product Demo
**Atmosfera:** Embedded product mockup/video, interactive elements, product walkthrough, step-by-step guides, hover-to-reveal features, embedded demos  
**Quando usar:** SaaS platforms, tool/software products, productivity apps landing pages, developer tools, productivity software  
**Tokens CSS:**
```css
--video-aspect-ratio: 16/9;
--overlay-bg: rgba(0,0,0,0.7);
--step-indicator-size: 32px;
--play-button-size: 80px;
--transition-duration: 300ms;
```
**Anti-pattern:** Simple services, consulting, non-digital products, complexity-averse audiences

### Trust & Authority
**Atmosfera:** Certificates/badges displayed, expert credentials, case studies with metrics, before/after comparisons, industry recognition, security badges  
**Quando usar:** Healthcare/medical landing pages, financial services, enterprise software, premium/luxury products, legal services  
**Tokens CSS:**
```css
--badge-height: 48px;
--trust-color: #1E40AF;
--security-green: #059669;
--card-shadow: 0 4px 6px rgba(0,0,0,0.1);
--metric-highlight: #F59E0B;
```
**Anti-pattern:** Casual products, entertainment, viral/social-first products

### Storytelling-Driven
**Atmosfera:** Narrative flow, visual story progression, section transitions, consistent character/brand voice, emotional messaging, journey visualization  
**Quando usar:** Brand/startup stories, mission-driven products, premium/lifestyle brands, documentary-style products, educational  
**Tokens CSS:**
```css
--section-min-height: 100vh;
--reveal-duration: 600ms;
--narrative-font: serif;
--chapter-spacing: 8rem;
--timeline-color: accent;
--parallax-speed: 0.5;
```
**Anti-pattern:** Technical/complex products (unless narrative-driven), traditional enterprise software

## BI/Analytics

### Data-Dense Dashboard
**Atmosfera:** Multiple charts/widgets, data tables, KPI cards, minimal padding, grid layout, space-efficient, maximum data visibility  
**Quando usar:** Business intelligence dashboards, financial analytics, enterprise reporting, operational dashboards, data warehousing  
**Tokens CSS:**
```css
--grid-gap: 8px;
--card-padding: 12px;
--font-size-small: 12px;
--table-row-height: 36px;
--sidebar-width: 240px;
--header-height: 56px;
```
**Anti-pattern:** Marketing dashboards, consumer-facing analytics, simple reporting

### Heat Map & Heatmap Style
**Atmosfera:** Color-coded grid/matrix, data intensity visualization, geographical heat maps, correlation matrices, cell-based representation, gradient coloring  
**Quando usar:** Geographical analysis, performance matrices, correlation analysis, user behavior heatmaps, temperature/intensity data  
**Tokens CSS:**
```css
--heatmap-cool: #0080FF;
--heatmap-neutral: #FFFFFF;
--heatmap-hot: #FF0000;
--cell-size: 24px;
--legend-width: 200px;
--tooltip-bg: rgba(0,0,0,0.9);
```
**Anti-pattern:** Linear data representation, categorical comparisons (use bar charts), small datasets

### Executive Dashboard
**Atmosfera:** High-level KPIs, large key metrics, minimal detail, summary view, trend indicators, at-a-glance insights, executive summary  
**Quando usar:** C-suite dashboards, business summary reports, decision-maker dashboards, strategic planning views  
**Tokens CSS:**
```css
--kpi-font-size: 48px;
--sparkline-height: 32px;
--status-green: #22C55E;
--status-yellow: #F59E0B;
--status-red: #EF4444;
--card-min-width: 280px;
```
**Anti-pattern:** Detailed analyst dashboards, technical deep-dives, operational monitoring

### Real-Time Monitoring
**Atmosfera:** Live data updates, status indicators, alert notifications, streaming data visualization, active monitoring, streaming charts  
**Quando usar:** System monitoring dashboards, DevOps dashboards, real-time analytics, stock market dashboards, live event tracking  
**Tokens CSS:**
```css
--pulse-animation: pulse 2s infinite;
--alert-z-index: 1000;
--live-indicator: #22C55E;
--critical-color: #DC2626;
--update-interval: 5s;
--toast-duration: 5s;
```
**Anti-pattern:** Historical analysis, long-term trend reports, archived data dashboards

### Drill-Down Analytics
**Atmosfera:** Hierarchical data exploration, expandable sections, interactive drill-down paths, summary-to-detail flow, context preservation  
**Quando usar:** Sales analytics, product analytics, funnel analysis, multi-dimensional data exploration, business intelligence  
**Tokens CSS:**
```css
--breadcrumb-separator: /;
--expand-duration: 300ms;
--level-indent: 24px;
--back-button-size: 40px;
--context-bar-height: 48px;
--drill-transition: 300ms ease;
```
**Anti-pattern:** Simple linear data, single-metric dashboards, streaming real-time dashboards

### Comparative Analysis Dashboard
**Atmosfera:** Side-by-side comparisons, period-over-period metrics, A/B test results, regional comparisons, performance benchmarks  
**Quando usar:** Period-over-period reporting, A/B test dashboards, market comparison, competitive analysis, regional performance  
**Tokens CSS:**
```css
--positive-color: #22C55E;
--negative-color: #EF4444;
--neutral-color: #6B7280;
--comparison-gap: 2rem;
--arrow-size: 16px;
--badge-padding: 4px 8px;
```
**Anti-pattern:** Single metric dashboards, future projections (use forecasting), real-time only (no historical)

### Predictive Analytics
**Atmosfera:** Forecast lines, confidence intervals, trend projections, scenario modeling, AI-driven insights, anomaly detection visualization  
**Quando usar:** Forecasting dashboards, anomaly detection systems, trend prediction dashboards, AI-powered analytics, budget planning  
**Tokens CSS:**
```css
--forecast-dash: 5 5;
--confidence-opacity: 0.2;
--anomaly-color: #F59E0B;
--prediction-color: #8B5CF6;
--scenario-toggle-width: 48px;
--ai-accent: #6366F1;
```
**Anti-pattern:** Historical-only dashboards, simple reporting, real-time operational dashboards

### User Behavior Analytics
**Atmosfera:** Funnel visualization, user flow diagrams, conversion tracking, engagement metrics, user journey mapping, cohort analysis  
**Quando usar:** Conversion funnel analysis, user journey tracking, engagement analytics, cohort analysis, retention tracking  
**Tokens CSS:**
```css
--funnel-width: 100%;
--stage-colors: gradient;
--flow-opacity: 0.6;
--cohort-cell-size: 40px;
--retention-line-color: #3B82F6;
--engagement-scale: 5 levels;
```
**Anti-pattern:** Real-time operational metrics, technical system monitoring, financial transactions

### Financial Dashboard
**Atmosfera:** Revenue metrics, profit/loss visualization, budget tracking, financial ratios, portfolio performance, cash flow, audit trail  
**Quando usar:** Financial reporting, accounting dashboards, portfolio tracking, budget monitoring, banking analytics  
**Tokens CSS:**
```css
--currency-symbol: $;
--decimal-places: 2;
--profit-color: #22C55E;
--loss-color: #EF4444;
--variance-threshold: 10%;
--table-header-bg: #F3F4F6;
```
**Anti-pattern:** Simple business dashboards, entertainment/social metrics, non-financial data

### Sales Intelligence Dashboard
**Atmosfera:** Deal pipeline, sales metrics, territory performance, sales rep leaderboard, win-loss analysis, quota tracking, forecast accuracy  
**Quando usar:** CRM dashboards, sales management, opportunity tracking, performance management, quota planning  
**Tokens CSS:**
```css
--pipeline-colors: stage gradient;
--gauge-track: #E5E7EB;
--gauge-fill: primary;
--rank-1-color: #FFD700;
--rank-2-color: #C0C0C0;
--rank-3-color: #CD7F32;
```
**Anti-pattern:** Marketing analytics, customer support metrics, HR dashboards

## Mobile

### Bauhaus (包豪斯)
**Atmosfera:** bauhaus, geometric, constructivist, primary colors, hard shadow, bold, tactile, functional, poster, mechanical, architectural  
**Quando usar:** Mobile-first apps needing high personality, onboarding flows, branding-forward product screens, artisan/design brands, editorial mobile experiences  
**Tokens CSS:**
```css
--color-red: #D02020;
--color-blue: #1040C0;
--color-yellow: #F0C020;
--color-bg: #F0F0F0;
--color-fg: #121212;
--border-width: 2px;
--shadow-hard: 4px 4px 0px 0px #121212;
--radius-block: 0px;
--radius-pill: 9999px;
--font-display: Outfit;
--font-weight-hero: 900;
```
**Anti-pattern:** Enterprise dashboards, accessibility-critical contexts (requires extra a11y work), data-heavy screens, conservative industries

### Minimalist Monochrome
**Atmosfera:** monochrome, black white, editorial, austere, typographic, sharp, zero radius, high contrast, brutalist, pocket editorial, serif, mechanical  
**Quando usar:** Luxury fashion e-commerce mobile, editorial publications, high-end portfolio apps, experimental/avant-garde brands, digital exhibitions  
**Tokens CSS:**
```css
--color-bg: #FFFFFF;
--color-fg: #000000;
--color-muted: #F5F5F5;
--color-muted-fg: #525252;
--color-border: #000000;
--color-border-light: #E5E5E5;
--radius: 0px;
--shadow: none;
--border-hairline: 1px solid #E5E5E5;
--border-thin: 1px solid #000000;
--border-thick: 2px solid #000000;
--border-heavy: 4px solid #000000;
--font-display: Playfair Display;
--font-body: Source Serif 4;
--font-mono: JetBrains Mono;
```
**Anti-pattern:** Entertainment, colorful brands, friendly consumer apps, anything requiring visual warmth or gradient

### Modern Dark (Cinema Mobile)
**Atmosfera:** dark mode, cinematic, ambient light, glassmorphism, deep black, indigo, glow, blur, atmospheric, reanimated, haptic, premium, layered, frosted glass, linear gradient  
**Quando usar:** Developer tools, pro productivity apps, fintech/trading dashboards, media/streaming platforms, AI tool interfaces, high-end gaming companion apps  
**Tokens CSS:**
```css
--bg-deep: #020203;
--bg-base: #050506;
--bg-elevated: #0a0a0c;
--surface: rgba(255 255 255/0.05);
--foreground: #EDEDEF;
--foreground-muted: #8A8F98;
--accent: #5E6AD2;
--accent-glow: rgba(94 106 210/0.2);
--border: rgba(255 255 255/0.08);
--radius: 16px;
--easing: cubic-bezier(0.16 1 0.3 1);
--font: Inter;
```
**Anti-pattern:** Consumer apps needing warmth, children's apps, health/medical contexts where dark feels harsh, high-accessibility contexts needing maximum contrast

### SaaS Mobile (High-Tech Boutique)
**Atmosfera:** saas, electric blue, gradient, fintech, spring animation, dual font, glassmorphism, boutique, premium, calistoga, inter, mono, tactile, haptic, bento  
**Quando usar:** B2B SaaS mobile dashboards, fintech apps, developer tool mobile companions, marketing analytics apps, HR/operations apps, modern business productivity  
**Tokens CSS:**
```css
--bg: #FAFAFA;
--fg: #0F172A;
--muted: #F1F5F9;
--accent: #0052FF;
--accent-sec: #4D7CFF;
--card: #FFFFFF;
--border: #E2E8F0;
--radius: 16px;
--shadow: shadowOpacity 0.1 shadowRadius 10;
--spring: mass 1 damping 15 stiffness 120;
--font-display: Calistoga;
--font-body: Inter;
--font-mono: JetBrains Mono;
```
**Anti-pattern:** Pure consumer entertainment, children's apps, highly decorative lifestyle apps, contexts where Electric Blue feels too corporate

### Terminal CLI (Mobile)
**Atmosfera:** terminal, cli, matrix green, monospace, hacker, ascii, command line, developer, web3, crypto, sci-fi, OLED, retro-future, field operative  
**Quando usar:** Developer tools, Web3/blockchain apps, geek-culture apps, ARG games, sci-fi/noir gaming companions, hacker/security tools, creative studio portfolios  
**Tokens CSS:**
```css
--bg: #050505;
--fg-primary: #33FF00;
--fg-amber: #FFB000;
--fg-muted: #1A3D1A;
--fg-error: #FF3333;
--border: #33FF00;
--radius: 0px;
--font: SpaceMono-Regular or JetBrains Mono;
--font-sizes: 12 14 16 only;
--blink-duration: 500ms;
--scanline-opacity: 0.05;
```
**Anti-pattern:** Consumer products, health apps, anything requiring approachability or warmth, children's apps, standard enterprise contexts

### Kinetic Brutalism (Mobile)
**Atmosfera:** kinetic, brutalism, motion, marquee, acid yellow, uppercase, oversized, aggressive typography, street, zine, high contrast, scroll-driven, haptic, reanimated  
**Quando usar:** Immersive storytelling apps, brand flagship mobile, music/culture platforms, sports apps, underground zines, limited-edition product drops, performance dashboards  
**Tokens CSS:**
```css
--bg: #09090B;
--fg: #FAFAFA;
--muted: #27272A;
--muted-fg: #A1A1AA;
--accent: #DFE104;
--accent-fg: #000000;
--border: #3F3F46;
--radius: 0px;
--border-width: 2px;
--shadow: none;
--marquee-speed: 5000ms;
--press-duration: 100ms;
--font: Space Grotesk or Inter;
```
**Anti-pattern:** Calm informational apps, healthcare, finance contexts needing trust, children's, any context where aggressive typography feels inappropriate

### Flat Design Mobile (Touch-First)
**Atmosfera:** flat, 2D, no shadow, color blocking, geometric, bold, poster, icon, touch-first, minimal, clean, tailored, cross-platform  
**Quando usar:** Cross-platform apps (iOS+Android parity), information-dense dashboards, system UI, brand illustration, onboarding flows, marketing pages, icon design  
**Tokens CSS:**
```css
--bg: #FFFFFF;
--surface: #F3F4F6;
--fg: #111827;
--primary: #3B82F6;
--secondary: #10B981;
--accent: #F59E0B;
--border: #E5E7EB;
--radius-sm: 6px;
--radius-md: 12px;
--radius-pill: 999px;
--shadow: none;
--elevation: 0;
--touch-target: 48px;
--spacing: 4 8 16 24 32 48;
```
**Anti-pattern:** Ultra-premium contexts needing depth/shadow, dark-mode-first products, contexts where flat design reads as unfinished or sterile

### Material You (MD3 Mobile)
**Atmosfera:** material design 3, md3, tonal surfaces, pills, soft curves, android, md3 easing, state layers, haptic, fab, google  
**Quando usar:** Android ecosystem apps, cross-platform productivity tools, MD3-based admin panels, data-heavy back-office UI with Material UI  
**Tokens CSS:**
```css
--md3-bg: #FFFBFE;
--md3-on-surface: #1C1B1F;
--md3-primary: #6750A4;
--md3-on-primary: #FFFFFF;
--md3-secondary-container: #E8DEF8;
--md3-on-secondary-container: #1D192B;
--md3-tertiary: #7D5260;
--md3-surface-container: #F3EDF7;
--md3-outline: #79747E;
--radius-pill: 999px;
--easing-emphasized: cubic-bezier(0.2,0,0,1);
```
**Anti-pattern:** Ultra-minimal brutalist brands, terminal/hacker aesthetics, monochrome editorial apps

### Neo Brutalism (Mobile)
**Atmosfera:** neo brutalism, pop art, stickers, thick borders, cream background, hot red, vivid yellow, soft violet, hard offset shadow, mechanical press, collage  
**Quando usar:** Creative tools, collab platforms, Gen Z marketing & e-commerce, portfolio sites, sticker-book style content apps  
**Tokens CSS:**
```css
☐ Mechanical press hides shadow;
```
**Anti-pattern:** Serious enterprise apps, conservative industries, sober fintech, accessibility-first contexts (must tune contrast)

### Bold Typography (Mobile Poster)
**Atmosfera:** bold typography, editorial, poster, broadsheet, vermillion, negative space, edge-to-edge type, underline CTA, near-black, warm white  
**Quando usar:** Creative brand heroes, reading-focused apps, event/exhibition pages, editorial mobile experiences, landing hero sections  
**Tokens CSS:**
```css
--bg: #0A0A0A;
--fg: #FAFAFA;
--muted: #1A1A1A;
--muted-fg: #737373;
--accent: #FF3D00;
--accent-fg: #0A0A0A;
--border: #262626;
--font-primary: Inter Tight;
--font-display: Playfair Display Italic;
--font-mono: JetBrains Mono;
```
**Anti-pattern:** Utility dashboards, kids apps, playful consumer products, contexts needing many icons or heavy imagery

### Academia (Scholarly Mobile)
**Atmosfera:** academia, library, mahogany, parchment, brass, crimson, serif, drop cap, arch-top, vignette, leather, scholarly, tactile  
**Quando usar:** Knowledge management apps, deep reading tools, ritual-heavy personal brands, lore-heavy RPG/roleplay apps, culture-specific community platforms  
**Tokens CSS:**
```css
--bg: #1C1714;
--bg-alt: #251E19;
--fg: #E8DFD4;
--muted: #3D332B;
--muted-fg: #9C8B7A;
--border: #4A3F35;
--accent-brass: #C9A962;
--accent-crimson: #8B2635;
--radius: 4px;
--arch-radius: 100px;
--shadow-card: 0 4px 6px rgba(0,0,0,0.4);
--font-heading: Cormorant Garamond;
--font-body: Crimson Pro;
--font-label: Cinzel;
```
**Anti-pattern:** Hyper-modern tech dashboards, neon/glassmorphism, playful Gen Z branding

### Cyberpunk Mobile HUD
**Atmosfera:** cyberpunk, neon, glitch, chamfered, orbitron, jetbrains, scanlines, crt, hud, matrix, military, decker  
**Quando usar:** Gaming dashboards, crypto/cyberpunk apps, sci-fi companion tools, hacker OS skins, data-heavy monitoring HUDs  
**Tokens CSS:**
```css
--bg: #0A0A0F;
--card: #12121A;
--fg: #E0E0E0;
--muted: #1C1C2E;
--accent: #00FF88;
--accent2: #FF00FF;
--accent3: #00D4FF;
--border: #2A2A3A;
--destructive: #FF3366;
--radius: 0px;
--font-heading: Orbitron;
--font-body: JetBrains Mono;
```
**Anti-pattern:** Serious enterprise, health/finance requiring calm trust, minimal editorial apps

### Bitcoin DeFi (Mobile)
**Atmosfera:** web3, bitcoin, defi, digital gold, fintech, wallet, orange, glassmorphism, gradient, blur, holographic, trust, precision  
**Quando usar:** DeFi dashboards, wallets, NFT marketplaces, Web3 social, metaverse utilities, high-tech fintech brands  
**Tokens CSS:**
```css
--bg-void: #030304;
--bg-surface: #0F1115;
--fg: #FFFFFF;
--fg-muted: #94A3B8;
--border-dim: rgba(30,41,59,0.2);
--accent-bitcoin: #F7931A;
--accent-burnt: #EA580C;
--accent-gold: #FFD600;
--radius-card: 24px;
--radius-pill: 999px;
--blur-intensity: 20;
--font-heading: Space Grotesk;
--font-body: Inter;
--font-mono: JetBrains Mono;
```
**Anti-pattern:** Playful casual apps, low-tech brands, ultra-minimal editorial apps

### Claymorphism (Mobile)
**Atmosfera:** claymorphism, clay, 3d, soft, bubbly, candy, playful, rounded, squish, tactile, inflate, silicone, haptic, spring  
**Quando usar:** Children education apps, teen social products, crypto gamification, creative tools, brand mascot-led apps  
**Tokens CSS:**
```css
--bg: #F4F1FA;
--card-bg: rgba(255,255,255,0.7);
--text: #332F3A;
--muted: #635F69;
--accent: #7C3AED;
--accent2: #DB2777;
--success: #10B981;
--warning: #F59E0B;
--radius-outer: 50px;
--radius-card: 32px;
--radius-button: 20px;
--font-heading: Nunito Black;
--font-body: DM Sans;
```
**Anti-pattern:** Serious enterprise, high-density data, editorial reading apps, fintech trust signals

### Enterprise SaaS (Mobile)
**Atmosfera:** enterprise, saas, b2b, professional, indigo, violet, gradient, polished, trustworthy, clean, approachable, spring, haptic  
**Quando usar:** B2B backend management, productivity tools, government and finance mobile apps, SaaS companion apps, enterprise dashboards  
**Tokens CSS:**
```css
--bg: #F8FAFC;
--surface: #FFFFFF;
--text: #0F172A;
--muted: #64748B;
--primary: #4F46E5;
--secondary: #7C3AED;
--success: #10B981;
--border: #E2E8F0;
--radius-card: 16px;
--radius-pill: 999px;
--radius-input: 8px;
--shadow-card: rgba(79,70,229,0.08);
--font: Plus Jakarta Sans;
```
**Anti-pattern:** Pure consumer entertainment, Gen-Z youth apps, gaming UI, ultra-minimal editorial

### Sketch Hand-Drawn (Mobile)
**Atmosfera:** sketch, hand-drawn, handwriting, wobbly, imperfect, paper, kalam, organic, collage, post-it, tape, offset shadow, scribble  
**Quando usar:** Low-fidelity prototyping, creative brands, children/picturebook apps, education tools, journaling apps, gamified puzzles  
**Tokens CSS:**
```css
--bg: #FDFBF7;
--text: #2D2D2D;
--accent-red: #FF4D4D;
--accent-blue: #2D5DA1;
--postit: #FFF9C4;
--border-width: 3px;
--shadow-offset: 4px 4px;
--font-heading: Kalam Bold;
--font-body: Patrick Hand;
--rotation-card: -1deg to 1deg;
```
**Anti-pattern:** Enterprise dashboards, high-density data tables, fintech precision tools, medical or legal apps

### Neumorphism (Mobile)
**Atmosfera:** neumorphism, soft ui, dual shadow, extruded, inset, clay surface, monochromatic, cool grey, haptic, ceramic, physical, depth  
**Quando usar:** Minimal hardware controls, smart home apps, aesthetic utility tools, health monitors, brand showcase pages  
**Tokens CSS:**
```css
--bg: #E0E5EC;
--text: #3D4852;
--muted: #6B7280;
--accent: #6C63FF;
--shadow-light: rgba(255,255,255,0.6);
--shadow-dark: rgba(163,177,198,0.7);
--inset-bg: #D1D9E6;
--radius-card: 32px;
--radius-button: 16px;
--font: Plus Jakarta Sans or System;
```
**Anti-pattern:** High-density data, bright multi-color apps, apps needing strong visual hierarchy via color, dark-mode-only products
