---
name: aesthetic-boost
description: >
  Boost estético anti-AI-slop. Invoque junto com qualquer skill de frontend para
  elevar a qualidade visual. Ative quando o usuário pedir "design bonito",
  "visual marcante", "landing page", "hero section", "melhorar design",
  "identidade visual forte", ou qualquer task que exija output visualmente
  distinto. Compacto (~500 tokens) para mínimo overhead de contexto.
version: 1.0.0
inspired_by: anthropics/claude-code frontend-design plugin (MIT, 277K+ installs)
---

# Aesthetic Boost — Anti-AI-Slop Directive

> Modelos convergem para designs genéricos por causa de **convergência distribucional**:
> tokens de alta probabilidade dominam o sampling, e escolhas de design "seguras"
> (Inter, gradientes roxos, layouts previsíveis) são overrepresented nos dados de treinamento.
> Esta skill é uma **perturbação intencional** que desloca a geração do centro da distribuição.

## Antes de Codificar

Commit to a BOLD aesthetic direction:
- **Purpose**: Que problema essa interface resolve? Quem usa?
- **Tone**: Pick an extreme — brutally minimal, maximalist chaos, retro-futuristic,
  organic/natural, luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw,
  art deco/geometric, soft/pastel, industrial/utilitarian
- **Differentiation**: O que torna INESQUECÍVEL? Qual é a *one thing* que vão lembrar?

**CRITICAL**: Intencionalidade, não intensidade. Bold maximalism e refined minimalism
ambos funcionam — o que importa é executar a visão com precisão.

## 5 Eixos Estéticos

1. **Typography**: Fontes bonitas, únicas, interessantes. PROIBIDO: Inter, Roboto, Arial,
   system fonts. Pair display font + body font com alto contraste. Extremos de peso
   (100/200 vs 800/900). Scale jumps 3x+, não 1.5x. Google Fonts ou fontes locais.

2. **Color & Theme**: CSS variables para consistência. Cores dominantes com acentos afiados
   superam paletas tímidas e uniformes. PROIBIDO: gradientes roxos em fundo branco.

3. **Motion**: CSS-only para HTML. Motion library (framer-motion) para React.
   Um page load orquestrado com staggered reveals (animation-delay) > micro-interações
   espalhadas. Scroll-triggering e hover states que surpreendem.

4. **Spatial Composition**: Assimetria. Sobreposição. Flow diagonal. Grid-breaking.
   Espaço negativo generoso OU densidade controlada. Não: bento grids genéricos.

5. **Backgrounds & Depth**: Gradient meshes, noise textures, geometric patterns,
   transparências em camada, sombras dramáticas, bordas decorativas, grain overlays.
   Crie atmosfera — nunca defaulte para cores sólidas planas.

## Anti-Convergência

NUNCA use as mesmas escolhas entre projetos. Varie entre light/dark, fontes diferentes,
estéticas diferentes. NUNCA convirja para escolhas comuns de "segunda ordem" (Space Grotesk,
deep cyan, glassmorphism padrão) — ao escapar dos defaults óbvios, o modelo tende a cair
em um NOVO set de defaults igualmente genéricos. Quebre esse ciclo.

Se perceber repetição de padrões dentro da mesma sessão → mude radicalmente.

## Complexity Matching (OBRIGATÓRIO)

A complexidade do código DEVE espelhar a visão estética:
- **Maximalist** → código elaborado, animações extensas, efeitos em camada
- **Minimalist** → restraint extremo, precisão milimétrica em spacing/tipografia, detalhes sutis
- **NUNCA:** design minimalista com código complexo desnecessário, ou design ambicioso com código lazy
- Elegância vem de executar a visão com precisão

## Identidade da Marca (Se Disponível)

Se o projeto tem brand assets (logo dark/light, paleta hex, fontes definidas, conceito visual):
- USE-OS como fundação — a skill potencializa a identidade existente
- Mencione os assets no prompt: "Use assets em /public/brand"
- Fontes da marca > fontes da skill

Sem brand assets → crie uma direção estética original e consistente para o contexto.

> **Lembre:** Claude é capaz de trabalho criativo extraordinário. Não segure — mostre o que
> pode ser criado quando se pensa fora da caixa e se compromete totalmente com uma visão distinta.
