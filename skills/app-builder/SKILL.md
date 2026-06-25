---
name: app-builder
description: "Orchestrator for building full-stack applications from natural-language requests, with 13 scaffolding templates and agent coordination. Use when: creating a new app from scratch, deciding which stack to use for a project, scaffolding Next.js/FastAPI/Expo/Electron/Astro, building a SaaS, landing page, or CLI from scratch, coordinating agents to build a complete project. Keywords: app builder, create app, new project, scaffold, tech stack, full-stack, template, boilerplate, greenfield, monorepo. Do NOT use for: small tweaks to existing projects, debugging, or refactoring already-built code."
metadata:
  author: antigravity-kit (adapted)
  version: "1.0.0"
  source: "antigravity-kit"
---

# App Builder - Application Building Orchestrator

> Analyzes user's requests, determines tech stack, plans structure, and coordinates agents.

## 🎯 Selective Reading Rule

**Read ONLY files relevant to the request!** Check the content map, find what you need.

| File | Description | When to Read |
|------|-------------|--------------|
| `project-detection.md` | Keyword matrix, project type detection | Starting new project |
| `tech-stack.md` | 2026 default stack, alternatives | Choosing technologies |
| `agent-coordination.md` | Agent pipeline, execution order | Coordinating multi-agent work |
| `scaffolding.md` | Directory structure, core files | Creating project structure |
| `feature-building.md` | Feature analysis, error handling | Adding features to existing project |
| `templates/SKILL.md` | **Project templates** | Scaffolding new project |

---

## 📦 Templates (13 Total)

Quick-start scaffolding for new projects. **Read the matching template only!**

| Template | Tech Stack | When to Use |
|----------|------------|-------------|
| [nextjs-fullstack](references/nextjs-fullstack.md) | Next.js + Prisma | Full-stack web app |
| [nextjs-saas](references/nextjs-saas.md) | Next.js + Stripe | SaaS product |
| [nextjs-static](references/nextjs-static.md) | Next.js + Framer | Landing page |
| [nuxt-app](references/nuxt-app.md) | Nuxt 3 + Pinia | Vue full-stack app |
| [express-api](references/express-api.md) | Express + JWT | REST API |
| [python-fastapi](references/python-fastapi.md) | FastAPI | Python API |
| [react-native-app](references/react-native-app.md) | Expo + Zustand | Mobile app |
| [flutter-app](references/flutter-app.md) | Flutter + Riverpod | Cross-platform mobile |
| [electron-desktop](references/electron-desktop.md) | Electron + React | Desktop app |
| [chrome-extension](references/chrome-extension.md) | Chrome MV3 | Browser extension |
| [cli-tool](references/cli-tool.md) | Node.js + Commander | CLI app |
| [monorepo-turborepo](references/monorepo-turborepo.md) | Turborepo + pnpm | Monorepo |
| [astro-static](references/astro-static.md) | Astro + MDX | Blog / Docs |

---

## 🔗 Related Agents

| Agent | Role |
|-------|------|
| `project-planner` | Task breakdown, dependency graph |
| `frontend-specialist` | UI components, pages |
| `backend-specialist` | API, business logic |
| `database-architect` | Schema, migrations |
| `devops-engineer` | Deployment, preview |

---

## Usage Example

```
User: "Make an Instagram clone with photo sharing and likes"

App Builder Process:
1. Project type: Social Media App
2. Tech stack: Next.js + Prisma + Cloudinary + Clerk
3. Create plan:
   ├─ Database schema (users, posts, likes, follows)
   ├─ API routes (12 endpoints)
   ├─ Pages (feed, profile, upload)
   └─ Components (PostCard, Feed, LikeButton)
4. Coordinate agents
5. Report progress
6. Start preview
```

---

## 📖 Full Documentation References

For detailed information on each aspect, see the references folder.
