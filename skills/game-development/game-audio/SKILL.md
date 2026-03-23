---
name: game-audio
description: Game audio and sound design principles. Music, SFX, adaptive audio.
metadata:
  author: antigravity-kit (adapted)
  version: "1.0.0"
  source: "antigravity-kit"
---

# Game Audio & Sound Design

> Sound design, music, and adaptive audio principles.

---

## Sound Categories

### SFX (Sound Effects)

| Category | Purpose |
|----------|---------|
| **UI** | Feedback for interactions |
| **Gameplay** | Player actions, impacts |
| **Environmental** | Ambient, weather, ambience |
| **Impact** | Hits, explosions, events |

### Music

| Type | Use Case |
|------|----------|
| **Exploration** | Calm, atmospheric |
| **Combat** | Energetic, intense |
| **Boss** | Memorable, climactic |
| **Menu** | Inviting, brand-setting |

---

## Audio Implementation

### File Formats

| Format | Best For | Trade-offs |
|--------|----------|------------|
| **WAV** | SFX | Large file size |
| **OGG** | Music, loops | Compression, seek issues |
| **MP3** | Streaming | Compatibility |
| **FLAC** | Lossless audio | Large files |

### Audio Compression

- Lossy vs lossless
- Bitrate selection (128-320 kbps)
- Sample rate (44.1kHz typical)
- Mono vs stereo considerations

---

## Adaptive Audio

### Context-Based Audio

| Context | Adaptation |
|---------|------------|
| **Health** | Intensity increases as damage taken |
| **Intensity** | Music layers add as danger increases |
| **Time of day** | Different ambient tracks |
| **Location** | Environmental audio changes |

### Implementation

- Audio parameter control
- Music layer systems
- Real-time mixing
- Distance attenuation

---

## Audio Performance

### Optimization Strategies

| Technique | Benefit |
|-----------|---------|
| **Pooling** | Reuse audio sources |
| **LOD** | Reduce distant audio quality |
| **Compression** | Reduce file size |
| **Streaming** | Load large files gradually |

### Budget Considerations

- Voice count limits
- Memory for loaded audio
- CPU processing for effects
- Latency for UI feedback

---

## Audio Accessibility

### Considerations

| Accessibility | Implementation |
|---------------|-----------------|
| **Deaf players** | Visual feedback for audio cues |
| **Hard of hearing** | Haptic alternatives |
| **Volume control** | Per-category audio mixing |
| **Clarity** | Clear dialogue, no muddy audio |

---

## Anti-Patterns

| ❌ Don't | ✅ Do |
|----------|-------|
| Use same SFX for everything | Vary sound effects |
| Loop silence awkwardly | Use audio transitions |
| Ignore volume balancing | Mix to consistent levels |
| Audio always at full volume | Implement proper attenuation |

---

> **Remember:** Audio is 50% of the player experience. A game sounds as good as it plays.
