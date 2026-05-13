# Bun Development

**Trigger:** Bun.file, Bun.serve, Bun.$, bun:sqlite, Bun runtime

---

## Bun.file — Fast I/O

```typescript
// Read file
const file = Bun.file('data.json')
const content = await file.text()
const json = await file.json()
const buffer = await file.arrayBuffer()

// Write file
await Bun.write('output.txt', 'Hello, Bun!')
await Bun.write('data.json', JSON.stringify(data))

// File metadata
console.log(file.size)  // bytes
console.log(file.type)  // MIME type
```

---

## Bun.serve — Native HTTP

```typescript
Bun.serve({
  port: 3000,
  fetch(request) {
    const url = new URL(request.url)

    if (url.pathname === '/api/health') {
      return Response.json({ status: 'ok' })
    }

    if (url.pathname === '/api/data' && request.method === 'POST') {
      const body = await request.json()
      return Response.json({ received: body })
    }

    return new Response('Not Found', { status: 404 })
  },
  error(error) {
    return new Response(`Error: ${error.message}`, { status: 500 })
  },
})
```

---

## Bun.$ — Shell Tagged Templates

```typescript
import { $ } from 'bun'

// Simple command
await $`echo "Hello"`

// With variables (auto-escaped)
const name = 'my-project'
await $`mkdir -p ${name}`

// Capture output
const result = await $`ls -la`.text()
console.log(result)

// Check exit code
const { exitCode } = await $`git status`.nothrow()
if (exitCode !== 0) {
  console.log('Not a git repo')
}

// Pipe commands
await $`cat file.txt | grep "pattern" | wc -l`
```

---

## bun:sqlite — Built-in SQLite

```typescript
import { Database } from 'bun:sqlite'

const db = new Database('app.db')

// Create table
db.run(`
  CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE
  )
`)

// Prepared statements (recommended)
const insert = db.prepare('INSERT INTO users (name, email) VALUES ($name, $email)')
insert.run({ $name: 'John', $email: 'john@example.com' })

// Query
const query = db.prepare('SELECT * FROM users WHERE id = ?')
const user = query.get(1)

// All results
const allUsers = db.prepare('SELECT * FROM users').all()

// Transaction
const insertMany = db.transaction((users) => {
  for (const user of users) {
    insert.run(user)
  }
})
insertMany([
  { $name: 'Alice', $email: 'alice@example.com' },
  { $name: 'Bob', $email: 'bob@example.com' },
])
```

---

## Workspace Config

```json
// package.json
{
  "workspaces": ["packages/*", "apps/*"]
}
```

```bash
# Install all workspaces
bun install

# Run script in specific workspace
bun run --filter @myorg/api start

# Add dependency to workspace
bun add zod --filter @myorg/shared
```

---

## Bun Test

```typescript
// example.test.ts
import { describe, it, expect, mock, beforeEach } from 'bun:test'

describe('Calculator', () => {
  it('adds numbers', () => {
    expect(1 + 2).toBe(3)
  })

  it('handles async', async () => {
    const result = await Promise.resolve(42)
    expect(result).toBe(42)
  })
})

// Mocking
const mockFn = mock(() => 'mocked')
mockFn()
expect(mockFn).toHaveBeenCalled()

// Mocking modules
mock.module('./api', () => ({
  fetchData: mock(() => Promise.resolve({ data: 'test' })),
}))
```

```bash
# Run tests
bun test

# Watch mode
bun test --watch

# Coverage
bun test --coverage
```

---

## Gotchas

### Binary Lockfile
Bun uses `bun.lockb` (binary) instead of `package-lock.json`. Commit it to git.

### Native Addon Compatibility
Some Node.js native addons may not work. Check compatibility or use Bun-native alternatives.

### Snapshot Format
Bun snapshots differ from Jest. Don't mix snapshot files between runners.

### process.env
Works like Node.js, but `Bun.env` is slightly faster for direct access.

```typescript
// Both work
process.env.API_KEY
Bun.env.API_KEY  // Slightly faster
```
