# MCP Builder

**Trigger:** Creating MCP servers for internal services, exposing APIs as MCP tools/resources, MCP architecture.

---

## Setup

```bash
bun add @modelcontextprotocol/sdk zod
```

---

## Basic MCP Server

```typescript
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js'
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js'
import { z } from 'zod'

const server = new McpServer({
  name: 'my-service',
  version: '1.0.0',
})

// Define a tool
server.tool(
  'get_user',
  'Get user by ID',
  {
    userId: z.string().describe('The user ID'),
  },
  async ({ userId }) => {
    const user = await db.users.findUnique({ where: { id: userId } })
    return { content: [{ type: 'text', text: JSON.stringify(user) }] }
  }
)

// Define a resource
server.resource(
  'users://list',
  'List all users',
  async () => {
    const users = await db.users.findMany()
    return { content: [{ type: 'text', text: JSON.stringify(users) }] }
  }
)

// Start server
const transport = new StdioServerTransport()
await server.connect(transport)
```

---

## Tool Definition with Zod

```typescript
const searchSchema = z.object({
  query: z.string().describe('Search query'),
  limit: z.number().default(10).describe('Max results'),
  filters: z.object({
    status: z.enum(['active', 'inactive']).optional(),
    createdAfter: z.string().datetime().optional(),
  }).optional(),
})

server.tool('search', 'Search records', searchSchema, async (input) => {
  // input is fully typed from Zod schema
  const results = await search(input)
  return { content: [{ type: 'text', text: JSON.stringify(results) }] }
})
```

---

## Transports

### Stdio (default)
```typescript
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js'
const transport = new StdioServerTransport()
```

### SSE (Server-Sent Events)
```typescript
import { SSEServerTransport } from '@modelcontextprotocol/sdk/server/sse.js'
const transport = new SSEServerTransport('/sse', response)
```

---

## Registration

### Claude Code
```json
// ~/.claude/settings.json
{
  "mcpServers": {
    "my-service": {
      "command": "bun",
      "args": ["run", "/path/to/server.ts"]
    }
  }
}
```

### Cursor
```json
// ~/.cursor/mcp.json
{
  "mcpServers": {
    "my-service": {
      "command": "bun",
      "args": ["run", "/path/to/server.ts"]
    }
  }
}
```

---

## Testing

```typescript
import { InMemoryTransport } from '@modelcontextprotocol/sdk/inMemory.js'
import { Client } from '@modelcontextprotocol/sdk/client/index.js'

const [clientTransport, serverTransport] = InMemoryTransport.createLinkedPair()

await server.connect(serverTransport)
const client = new Client({ name: 'test', version: '1.0.0' })
await client.connect(clientTransport)

// Call tools
const result = await client.callTool('get_user', { userId: '123' })
```

---

## Principles

1. **Atomic tools** — Each tool does one thing well
2. **Typed inputs** — Use Zod for validation
3. **Safe by default** — Read-only unless explicitly write
4. **Paginated responses** — Large datasets need pagination
