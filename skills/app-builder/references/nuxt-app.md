---
name: nuxt-app
description: Nuxt 4 full-stack template. Vue 3 (Vapor), Pinia, Tailwind v4, Prisma.
---

# Nuxt 4 Full-Stack Template (2026 Edition)

## Tech Stack

| Component | Technology | Version / Notes |
|-----------|------------|-----------------|
| Framework | Nuxt | v4.0+ (App Directory structure) |
| UI Engine | Vue | v3.6+ (Vapor Mode enabled) |
| Language | TypeScript | v5+ (Strict Mode) |
| State | Pinia | v3+ (Store syntax) |
| Database | PostgreSQL | Prisma ORM |
| Styling | Tailwind CSS | v4.0 (Vite Plugin, Zero-config) |
| UI Lib | Nuxt UI | v3 (Tailwind v4 native) |
| Validation | Zod | Schema validation |

---

## Directory Structure (Nuxt 4 Standard)

```
project-name/
├── app/                  # Application Source
│   ├── assets/
│   │   └── css/
│   │       └── main.css  # Tailwind v4 imports
│   ├── components/       # Auto-imported components
│   ├── composables/      # Auto-imported logic
│   ├── layouts/
│   ├── pages/            # File-based routing
│   ├── app.vue           # Root component
│   └── router.options.ts
├── server/               # Nitro Server Engine
│   ├── api/              # API Routes (e.g. /api/users)
│   ├── routes/           # Server Routes
│   └── utils/            # Server-only helpers (Prisma)
├── prisma/
│   └── schema.prisma
├── public/
├── nuxt.config.ts        # Main Config
└── package.json
```

---

## Key Concepts (2026)

| Concept | Description |
|---------|-------------|
| **App Directory** | Tách biệt mã nguồn ứng dụng và file cấu hình root. |
| **Vapor Mode** | Render không cần Virtual DOM (như SolidJS). Bật trong `nuxt.config`. |
| **Server Functions** | Gọi hàm server trực tiếp từ client (thay thế dần API routes). |
| **Tailwind v4** | Cấu hình theme trực tiếp trong CSS, không cần `tailwind.config.js`. |
| **Nuxt Islands** | Render component cô lập trên server (`<NuxtIsland name="..." />`). |

---

## Best Practices

- **Vapor Mode**: Kích hoạt cho các component nặng về render
- **Data Fetching**: Sử dụng `useFetch` hoặc Server Functions
- **State**: Dùng `defineStore` (Pinia) cho global state
- **Type Safety**: Tự động tạo type cho API routes
