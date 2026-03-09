---
name: bun-development
description: Bun runtime patterns, bundler configuration, and Bun-specific APIs. Trigger on Bun FFI, Bun.serve, Bun.file, Bun shell, workspace configuration, Bun-specific test patterns, or runtime edge cases that differ from Node.js.
metadata:
  author: osforge
  version: '1.0'
---

# Bun Development Patterns

## Where Bun Differs from Node.js

| Area | Node.js | Bun | Impact |
|------|---------|-----|--------|
| Package install | `npm install` (slow) | `bun install` (10x faster) | Drop-in |
| Test runner | Jest/Vitest | `bun test` (built-in) | Config change |
| Bundler | webpack/esbuild | `bun build` (built-in) | Config change |
| File I/O | `fs.readFile` | `Bun.file()` (faster) | API difference |
| HTTP server | Express/Fastify | `Bun.serve()` (native) | API difference |
| Shell scripts | child_process | `Bun.$` (shell tagged template) | New API |
| SQLite | better-sqlite3 | `bun:sqlite` (built-in) | Built-in |
| FFI | node-ffi-napi | `bun:ffi` (built-in, faster) | New API |

## Bun-Specific APIs

### Bun.file (Fast File I/O)
```typescript
// Read file (returns Blob-like BunFile)
const file = Bun.file('data.json')
const content = await file.json() // or .text(), .arrayBuffer()
console.log(file.size, file.type) // metadata without reading

// Write file
await Bun.write('output.txt', 'content')
await Bun.write('copy.json', Bun.file('source.json')) // zero-copy
```

### Bun.serve (HTTP Server)
```typescript
Bun.serve({
  port: 3000,
  async fetch(req) {
    const url = new URL(req.url)
    if (url.pathname === '/api/health') {
      return Response.json({ status: 'ok' })
    }
    return new Response('Not Found', { status: 404 })
  },
  error(error) {
    return new Response(`Error: ${error.message}`, { status: 500 })
  },
})
```

### Bun Shell ($)
```typescript
import { $ } from 'bun'

// Run shell commands with tagged templates
const result = await $`ls -la`.text()
const branch = await $`git branch --show-current`.text()

// Pipe and combine
await $`cat file.txt | grep "pattern" > output.txt`

// With variables (auto-escaped)
const dir = '/path/to/dir'
await $`find ${dir} -name "*.ts" -type f`
```

### bun:sqlite (Built-in SQLite)
```typescript
import { Database } from 'bun:sqlite'

const db = new Database('app.db')
db.run('CREATE TABLE IF NOT EXISTS cache (key TEXT PRIMARY KEY, value TEXT, expires INTEGER)')

// Prepared statements (fast)
const get = db.prepare('SELECT value FROM cache WHERE key = ? AND expires > ?')
const cached = get.get(key, Date.now())
```

## Workspace Configuration
```jsonc
// package.json
{
  "workspaces": ["packages/*", "apps/*"],
  "scripts": {
    "dev": "bun --filter './apps/web' dev",
    "test": "bun test --recursive",
    "build": "bun --filter '*' build"
  }
}
```

## Bun Test Patterns
```typescript
import { test, expect, describe, mock } from 'bun:test'

describe('UserService', () => {
  test('creates user', async () => {
    const result = await service.create({ name: 'Test' })
    expect(result.id).toBeDefined()
  })

  test('mocking', () => {
    const fn = mock(() => 42)
    expect(fn()).toBe(42)
    expect(fn).toHaveBeenCalledTimes(1)
  })
})
```

## Gotchas
- `bun install` uses binary lockfile (`bun.lockb`) — commit it
- Some Node.js native addons don't work in Bun yet — check compatibility
- `bun test` snapshot format differs from Jest — don't mix
- Bun's `fetch` is built-in, no need for `node-fetch`
- For Next.js: Bun runs the dev server, but Next.js still uses its own bundler
