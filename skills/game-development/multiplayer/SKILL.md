---
name: multiplayer
description: "Multiplayer game principles: network architecture (dedicated server, P2P, host-based), synchronization, lag compensation, anti-cheat, and matchmaking. Use when: I want to add multiplayer to my game and don't know which architecture to use; remote players keep teleporting or lagging (prediction, interpolation, reconciliation); how to reduce netcode bandwidth (delta compression, area of interest); players are cheating (speed hack, aimbot) and I need server authority; how to design matchmaking by skill and latency. Keywords: multiplayer, netcode, networking, latency, synchronization, lag compensation, dedicated server, anti-cheat, matchmaking, P2P. Do NOT use for: single-player games or general game architecture questions without networking (use game-development)."
metadata:
  author: antigravity-kit (adapted)
  version: "1.0.0"
  source: "antigravity-kit"
---

# Multiplayer Game Development

> Networking architecture and synchronization principles.

---

## 1. Architecture Selection

### Decision Tree

```
What type of multiplayer?
│
├── Competitive / Real-time
│   └── Dedicated Server (authoritative)
│
├── Cooperative / Casual
│   └── Host-based (one player is server)
│
├── Turn-based
│   └── Client-server (simple)
│
└── Massive (MMO)
    └── Distributed servers
```

### Comparison

| Architecture | Latency | Cost | Security |
|--------------|---------|------|----------|
| **Dedicated** | Low | High | Strong |
| **P2P** | Variable | Low | Weak |
| **Host-based** | Medium | Low | Medium |

---

## 2. Synchronization Principles

### State vs Input

| Approach | Sync What | Best For |
|----------|-----------|----------|
| **State Sync** | Game state | Simple, few objects |
| **Input Sync** | Player inputs | Action games |
| **Hybrid** | Both | Most games |

### Lag Compensation

| Technique | Purpose |
|-----------|---------|
| **Prediction** | Client predicts server |
| **Interpolation** | Smooth remote players |
| **Reconciliation** | Fix mispredictions |
| **Lag compensation** | Rewind for hit detection |

---

## 3. Network Optimization

### Bandwidth Reduction

| Technique | Savings |
|-----------|---------|
| **Delta compression** | Send only changes |
| **Quantization** | Reduce precision |
| **Priority** | Important data first |
| **Area of interest** | Only nearby entities |

### Update Rates

| Type | Rate |
|------|------|
| Position | 20-60 Hz |
| Health | On change |
| Inventory | On change |
| Chat | On send |

---

## 4. Security Principles

### Server Authority

```
Client: "I hit the enemy"
Server: Validate → did projectile actually hit?
         → was player in valid state?
         → was timing possible?
```

### Anti-Cheat

| Cheat | Prevention |
|-------|------------|
| Speed hack | Server validates movement |
| Aimbot | Server validates sight line |
| Item dupe | Server owns inventory |
| Wall hack | Don't send hidden data |

---

## 5. Matchmaking

### Considerations

| Factor | Impact |
|--------|--------|
| **Skill** | Fair matches |
| **Latency** | Playable connection |
| **Wait time** | Player patience |
| **Party size** | Group play |

---

## 6. Anti-Patterns

| ❌ Don't | ✅ Do |
|----------|-------|
| Trust the client | Server is authority |
| Send everything | Send only necessary |
| Ignore latency | Design for 100-200ms |
| Sync exact positions | Interpolate/predict |

---

> **Remember:** Never trust the client. The server is the source of truth.
