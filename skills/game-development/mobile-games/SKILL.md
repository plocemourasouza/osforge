---
name: mobile-games
description: "Princípios de jogos mobile: touch input, bateria e thermal, requisitos de App Store e Google Play, monetização. ACIONE quando: estou portando ou criando um jogo para iOS/Android e os controles de touch estão ruins; meu jogo mobile esquenta o aparelho ou drena bateria (thermal throttling, 30 vs 60 FPS); quais requisitos preciso cumprir para publicar na App Store ou Google Play (privacy labels, 64-bit, target API); qual modelo de monetização usar (premium, IAP, ads, assinatura); como lidar com interrupções, tamanhos de tela e portrait/landscape. Keywords: mobile, iOS, Android, touch, gestos, bateria, App Store, Google Play, IAP, monetização. Não acione para: jogos que rodam no navegador mobile (use web-games) ou AR com ARKit/ARCore (use vr-ar)."
metadata:
  author: antigravity-kit (adapted)
  version: "1.0.0"
  source: "antigravity-kit"
---

# Mobile Game Development

> Platform constraints and optimization principles.

---

## 1. Platform Considerations

### Key Constraints

| Constraint | Strategy |
|------------|----------|
| **Touch input** | Large hit areas, gestures |
| **Battery** | Limit CPU/GPU usage |
| **Thermal** | Throttle when hot |
| **Screen size** | Responsive UI |
| **Interruptions** | Pause on background |

---

## 2. Touch Input Principles

### Touch vs Controller

| Touch | Desktop/Console |
|-------|-----------------|
| Imprecise | Precise |
| Occludes screen | No occlusion |
| Limited buttons | Many buttons |
| Gestures available | Buttons/sticks |

### Best Practices

- Minimum touch target: 44x44 points
- Visual feedback on touch
- Avoid precise timing requirements
- Support both portrait and landscape

---

## 3. Performance Targets

### Thermal Management

| Action | Trigger |
|--------|---------|
| Reduce quality | Device warm |
| Limit FPS | Device hot |
| Pause effects | Critical temp |

### Battery Optimization

- 30 FPS often sufficient
- Sleep when paused
- Minimize GPS/network
- Dark mode saves OLED battery

---

## 4. App Store Requirements

### iOS (App Store)

| Requirement | Note |
|-------------|------|
| Privacy labels | Required |
| Account deletion | If account creation exists |
| Screenshots | For all device sizes |

### Android (Google Play)

| Requirement | Note |
|-------------|------|
| Target API | Current year's SDK |
| 64-bit | Required |
| App bundles | Recommended |

---

## 5. Monetization Models

| Model | Best For |
|-------|----------|
| **Premium** | Quality games, loyal audience |
| **Free + IAP** | Casual, progression-based |
| **Ads** | Hyper-casual, high volume |
| **Subscription** | Content updates, multiplayer |

---

## 6. Anti-Patterns

| ❌ Don't | ✅ Do |
|----------|-------|
| Desktop controls on mobile | Design for touch |
| Ignore battery drain | Monitor thermals |
| Force landscape | Support player preference |
| Always-on network | Cache and sync |

---

> **Remember:** Mobile is the most constrained platform. Respect battery and attention.
