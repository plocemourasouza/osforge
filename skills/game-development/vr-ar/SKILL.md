---
name: vr-ar
description: "Princípios de jogos VR/AR: conforto e prevenção de motion sickness, locomoção, hand tracking, anchoring AR e metas de performance por headset. ACIONE quando: jogadores estão passando mal no meu jogo VR (motion sickness, locomoção teleport vs smooth); estou desenvolvendo para Meta Quest, PSVR2 ou SteamVR e preciso das metas de FPS/latência (90+ FPS, <20ms); como desenhar interação com as mãos (controllers vs hand tracking, haptics); estou fazendo um app AR com ARKit/ARCore e preciso de anchors (plane, image, cloud); como dimensionar UI legível em VR. Keywords: VR, AR, realidade virtual, realidade aumentada, Quest, motion sickness, hand tracking, ARKit, ARCore, locomoção. Não acione para: jogos 3D de tela plana (use 3d-games) ou netcode de multiplayer VR (use multiplayer)."
metadata:
  author: antigravity-kit (adapted)
  version: "1.0.0"
  source: "antigravity-kit"
---

# VR/AR Game Development

> Comfort, immersion, and platform-specific principles for VR and AR.

---

## 1. VR Comfort Principles

### Motion Sickness Prevention

| Factor | Mitigation |
|--------|-----------|
| **Latency** | Target <20ms motion-to-photon |
| **Frame rate** | 90+ FPS minimum (120+ preferred) |
| **Acceleration** | Smooth acceleration, avoid instant movement |
| **FOV mismatch** | Maintain game world sense of scale |

### Movement Types

| Type | Impact | Usage |
|------|--------|-------|
| **Teleport** | No sickness | Static navigation |
| **Smooth locomotion** | Medium sickness | Continuous movement |
| **Room-scale** | No sickness | Small play spaces |
| **Artificial acceleration** | High sickness | Avoid if possible |

---

## 2. VR Interaction Design

### Hand Tracking

| Method | Pros | Cons |
|--------|------|------|
| **Controller** | Precise, familiar | Requires hardware |
| **Hand tracking** | Natural, immersive | Less precise |
| **Hybrid** | Best of both | Complex switching |

### Interaction Distance

- Arm's reach (~2 meters)
- Natural reaching motion
- Grip/trigger feedback
- Haptic confirmation

---

## 3. VR Hardware Targets

| Platform | Resolution | Refresh | Tracking |
|----------|-----------|---------|----------|
| **Meta Quest 3** | 2064×2208 | 120Hz | Inside-out |
| **PlayStation VR2** | 2000×2040 | 120Hz | External cameras |
| **SteamVR (PC)** | Varies | 144Hz | External sensors |

---

## 4. AR Interaction Design

### Real-World Anchoring

| Anchor Type | Use Case |
|-------------|----------|
| **Plane** | Object surfaces |
| **Face** | Face filters, makeup |
| **Image** | Marker-based tracking |
| **Cloud** | Persistent anchors |

### Overlay Types

| Type | Example |
|------|---------|
| **Screen-space** | HUD elements |
| **World-space** | Objects in environment |
| **Occlusion** | Virtual objects behind real |

---

## 5. Cross-Platform Considerations

### VR Platforms

| Platform | Input | Focus |
|----------|-------|-------|
| **Meta Quest** | Hand tracking | Accessibility |
| **PlayStation VR2** | DualSense haptics | Console experience |
| **SteamVR** | Multiple controllers | PC enthusiasts |

### AR Platforms

| Platform | Tracking | Strength |
|----------|----------|----------|
| **ARKit (iOS)** | LiDAR+Visual | Precise planes |
| **ARCore (Android)** | Visual tracking | Widespread |
| **Magic Leap** | Spatial computing | Enterprise |

---

## 6. Performance Targets

### VR Requirements

- 90 FPS minimum
- <20ms latency
- 16.7ms per frame budget
- GPU-bound optimization priority

### AR Requirements

- 60 FPS minimum
- Real-time camera processing
- Battery efficiency critical
- CPU-bound optimization

---

## 7. Anti-Patterns

| ❌ Don't | ✅ Do |
|----------|-------|
| Optimize for console specs | Target VR headsets specifically |
| Ignore comfort guidelines | Design for VR comfort |
| Rapid acceleration | Smooth, natural movement |
| Small UI elements | Large, readable interfaces |
| Ignore latency | Every frame matters |

---

> **Remember:** VR is immersive presence. Any flaw breaks immersion. AR is understanding space. Anchors must be reliable.
