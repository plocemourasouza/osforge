---
name: game-art
description: "Princípios de arte para jogos: pipeline de assets, otimização de texturas, animação (sprite, skeletal, procedural), VFX e direção de arte. ACIONE quando: como organizar o pipeline de assets do Blender/Aseprite para a engine (FBX, glTF, PNG); minhas texturas estão pesadas e preciso de atlases, mipmaps ou compressão (KTX2, WebP); qual tipo de animação usar para personagens (frame-based vs skeletal); quero adicionar VFX (explosões, partículas, trails) sem matar a performance; estou definindo o estilo visual do jogo (realista, stylized, pixel art, minimalista). Keywords: game art, assets, texture, animation pipeline, VFX, partículas, sprite sheet, direção de arte, Blender, Aseprite. Não acione para: implementação de sistemas de sprite/tilemap em código (use 2d-games) ou shaders e rendering 3D (use 3d-games)."
metadata:
  author: antigravity-kit (adapted)
  version: "1.0.0"
  source: "antigravity-kit"
---

# Game Art & Visual Development

> Visual style, asset pipeline, animation, and visual effects principles.

---

## Asset Pipeline

### Asset Preparation

| Stage | Purpose |
|-------|---------|
| **Creation** | Art tools (Blender, Aseprite, etc.) |
| **Optimization** | Reduce poly count, compress textures |
| **Export** | Format selection (FBX, glTF, PNG) |
| **Integration** | Engine import, naming conventions |

### Texture Optimization

- Use atlases for 2D sprites
- Mipmaps for 3D models
- Compression formats (KTX2, WebP)
- Normal maps for detail

---

## Animation

### Animation Types

| Type | Use Case |
|------|----------|
| **Sprite** | 2D frame-based animation |
| **Skeletal** | Character articulation |
| **Particle** | Effects, weather |
| **Procedural** | Generated motion |

### Animation Principles

- Timing and spacing
- Overlapping action
- Anticipation
- Follow-through
- Arcs of motion

---

## Visual Effects

### VFX Categories

| Category | Examples |
|----------|----------|
| **Environmental** | Weather, dust, lighting |
| **Impact** | Explosions, hits |
| **Magic** | Spells, energy |
| **Movement** | Speed lines, trails |

### Performance Considerations

- Effect pooling
- Particle count limits
- GPU vs CPU particles
- LOD for distance

---

## Art Direction

### Visual Style Selection

| Style | Best For | Considerations |
|-------|----------|----------------|
| **Realistic** | Immersive, detailed | High performance cost |
| **Stylized** | Unique look, timeless | Consistent character design |
| **Pixel art** | Retro, charming | Requires careful scaling |
| **Minimalist** | Performance, clarity | Limited visual appeal |

### Consistent Asset Production

- Style guide documentation
- Consistent color palette
- Naming conventions
- Version control for assets

---

## Anti-Patterns

| ❌ Don't | ✅ Do |
|----------|-------|
| Mix art styles | Maintain visual consistency |
| Ignore performance budget | Profile VFX impact |
| Store uncompressed art | Optimize for target platform |
| Animate every property | Focus on key elements |

---

> **Remember:** Art serves gameplay. Beautiful graphics that obscure the game are a distraction.
