---
name: game-art
description: "Game art principles: asset pipeline, texture optimization, animation (sprite, skeletal, procedural), VFX, and art direction. Use when: how to organize the asset pipeline from Blender/Aseprite to the engine (FBX, glTF, PNG); my textures are heavy and I need atlases, mipmaps, or compression (KTX2, WebP); which type of animation to use for characters (frame-based vs skeletal); I want to add VFX (explosions, particles, trails) without killing performance; I'm defining the game's visual style (realistic, stylized, pixel art, minimalist). Keywords: game art, assets, texture, animation pipeline, VFX, particles, sprite sheet, art direction, Blender, Aseprite. Do NOT use for: implementing sprite/tilemap systems in code (use 2d-games) or 3D shaders and rendering (use 3d-games)."
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
