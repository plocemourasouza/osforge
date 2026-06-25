---
name: pc-games
description: "PC game principles (Windows, Mac, Linux): publishing on Steam, graphics settings, control rebinding, modding, and desktop accessibility. Use when: I'm launching my game on Steam (or Epic, GOG, itch.io) and need to prepare the store page; how to structure graphics options in tiers (resolution, shadows, ray tracing, FPS); I need to support keyboard+mouse and controller with full rebinding; I want to add mod support and Steam Workshop; which minimum/recommended specs to set for the target hardware. Keywords: PC, Steam, desktop, resolutions, graphics settings, rebinding, modding, Steam Workshop, itch.io, GOG. Do NOT use for: browser games (use web-games), mobile (use mobile-games), or VR headsets via SteamVR (use vr-ar)."
metadata:
  author: antigravity-kit (adapted)
  version: "1.0.0"
  source: "antigravity-kit"
---

# PC Game Development

> Platform-specific principles for PC gaming (Windows, Mac, Linux).

---

## 1. Platform Capabilities

### PC Advantages

| Advantage | Opportunity |
|-----------|-------------|
| **Performance** | High-fidelity graphics, complex logic |
| **Input** | Keyboard, mouse, controller combination |
| **Hardware** | Utilize GPU for computation |
| **Mods** | Community content creation |

### Target Hardware Ranges

| Category | Specs |
|----------|-------|
| **Min** | GTX 1060, i5-8400, 8GB RAM |
| **Recommended** | RTX 2070, i7-10700, 16GB RAM |
| **Ultra** | RTX 4070, i9-13900K, 32GB RAM |

---

## 2. Input Systems

### Input Complexity

| Input Type | Use Case |
|-----------|----------|
| **Keyboard** | Menu navigation, text input |
| **Mouse** | Precise aiming, UI interaction |
| **Controller** | Console-style gameplay |
| **Hybrid** | Keyboard + mouse for strategy |

### Input Rebinding

- Always support full rebinding
- Save user preferences
- Preset profiles (WASD, ESDF, controller)
- Conflict detection

---

## 3. Platform Distribution

### Steam Considerations

| Factor | Consideration |
|--------|----------------|
| **Release notes** | Detailed changelog |
| **Screenshots** | 5+ representative images |
| **Trailer** | 30-60 second gameplay video |
| **Pricing** | Consider regional pricing |
| **Store page** | Compelling description, tags |

### Other Platforms

- Epic Games Store
- GOG
- itch.io
- Direct distribution

---

## 4. Performance Optimization

### Settings Tiers

| Setting | Low | Medium | High |
|---------|-----|--------|------|
| Resolution | 1080p | 1440p | 4K |
| Shadows | Off | Medium | High |
| Ray tracing | Off | On (low) | On (high) |
| FPS target | 60 | 144 | Unlimited |

### GPU Scaling

- VRAM usage (texture resolution)
- Draw distance (LOD changes)
- Particle count
- Shadow quality and distance

---

## 5. Accessibility for PC

### Controller Support

- Full gamepad support
- Button remapping
- Analog stick curves
- Trigger sensitivity

### Keyboard/Mouse

- Remappable controls
- Mouse sensitivity settings
- No forced gamepad-only sections

### Display Options

- Colorblind modes
- Text size adjustments
- Subtitle options
- High contrast modes

---

## 6. Modding Support

### Tools Provided

- Map editor
- Asset importers
- SDK documentation
- Community guidelines

### Workshop Integration

- Steam Workshop support
- Easy mod installation
- Rating/review system
- Automatic updates

---

## Anti-Patterns

| ❌ Don't | ✅ Do |
|----------|-------|
| Fixed resolution only | Support multiple resolutions |
| Gamepad only | Support mouse/keyboard |
| No graphics settings | Provide quality/performance options |
| Fixed controls | Allow full rebinding |

---

> **Remember:** PC players expect choice - resolution, quality, controls, and customization.
