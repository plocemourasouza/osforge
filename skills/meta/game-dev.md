# Game Development

**Trigger:** Game, game loop, sprites, 2D/3D, multiplayer, game engine.

---

## Purpose

Game development orchestrator providing core principles and routing to platform-specific sub-skills.

---

## Platform Selection

| Platform | Engine | Use Case |
|----------|--------|----------|
| **Web** | Phaser, Three.js, Babylon.js | Browser games, WebGL |
| **Mobile** | Unity, Godot, React Native | iOS/Android games |
| **PC** | Unity, Unreal, Godot | Desktop games |
| **VR/AR** | Unity, Unreal | Immersive experiences |

---

## Dimensional Specialties

### 2D Games
- Phaser (web)
- Unity 2D
- Godot 2D
- Pygame (prototypes)

### 3D Games
- Three.js (web)
- Unity 3D
- Unreal Engine
- Godot 3D

---

## Core Game Loop

```typescript
class Game {
  private lastTime = 0

  start() {
    requestAnimationFrame(this.loop.bind(this))
  }

  loop(currentTime: number) {
    const deltaTime = (currentTime - this.lastTime) / 1000
    this.lastTime = currentTime

    this.update(deltaTime)
    this.render()

    requestAnimationFrame(this.loop.bind(this))
  }

  update(dt: number) {
    // Physics, input, AI
  }

  render() {
    // Draw everything
  }
}
```

---

## Web Games with Phaser

```typescript
import Phaser from 'phaser'

const config: Phaser.Types.Core.GameConfig = {
  type: Phaser.AUTO,
  width: 800,
  height: 600,
  physics: {
    default: 'arcade',
    arcade: { gravity: { y: 300 } }
  },
  scene: {
    preload,
    create,
    update,
  }
}

function preload(this: Phaser.Scene) {
  this.load.image('player', 'player.png')
}

function create(this: Phaser.Scene) {
  this.player = this.physics.add.sprite(100, 450, 'player')
}

function update(this: Phaser.Scene) {
  // Game logic
}

new Phaser.Game(config)
```

---

## 3D Web with Three.js

```typescript
import * as THREE from 'three'

const scene = new THREE.Scene()
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight)
const renderer = new THREE.WebGLRenderer()

renderer.setSize(window.innerWidth, window.innerHeight)
document.body.appendChild(renderer.domElement)

const geometry = new THREE.BoxGeometry()
const material = new THREE.MeshBasicMaterial({ color: 0x00ff00 })
const cube = new THREE.Mesh(geometry, material)
scene.add(cube)

camera.position.z = 5

function animate() {
  requestAnimationFrame(animate)
  cube.rotation.x += 0.01
  cube.rotation.y += 0.01
  renderer.render(scene, camera)
}

animate()
```

---

## OSForge Integration

For multiplayer games with Next.js backend:

```typescript
// Leaderboard API
// app/api/leaderboard/route.ts
export async function GET() {
  const scores = await prisma.score.findMany({
    orderBy: { points: 'desc' },
    take: 100,
    include: { user: { select: { name: true } } }
  })
  return Response.json({ data: scores })
}

export async function POST(request: Request) {
  const { userId, points } = await request.json()
  const score = await prisma.score.create({
    data: { userId, points }
  })
  return Response.json({ data: score })
}
```
