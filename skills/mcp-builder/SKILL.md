---
name: mcp-builder
description: "Constrói servidores MCP (Model Context Protocol) customizados em TypeScript ou Python. ACIONE quando: criar servidor MCP do zero, expor API interna como tool MCP, transformar banco de dados ou serviço em resource para Claude Code/Cursor, definir tools/resources/prompts com transporte stdio ou SSE, debugar integração de servidor MCP. Keywords: MCP, Model Context Protocol, servidor MCP, MCP server, tool, resource, stdio, SSE, integração, SDK. Não acione para: uso de servidores MCP já existentes, criação de skills ou plugins que não envolvem MCP."
metadata:
  author: osforge
  version: '1.0'
---

# MCP Server Builder

## Architecture
```
Claude Code/Cursor → MCP Client → stdio/SSE → Your MCP Server → Your API/DB/Service
```

An MCP server exposes **tools** (actions), **resources** (data), and **prompts** (templates) to AI agents.

## Minimal Server (TypeScript + stdio)
```typescript
// src/index.ts
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js'
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js'
import { z } from 'zod'

const server = new McpServer({
  name: 'my-project-mcp',
  version: '1.0.0',
})

// Tool: action the agent can invoke
server.tool(
  'search_projects',
  'Search projects by name or status',
  { query: z.string(), status: z.enum(['active', 'archived']).optional() },
  async ({ query, status }) => {
    const projects = await db.project.findMany({
      where: {
        name: { contains: query, mode: 'insensitive' },
        ...(status && { status }),
      },
      take: 10,
    })
    return {
      content: [{ type: 'text', text: JSON.stringify(projects, null, 2) }],
    }
  }
)

// Resource: data the agent can read
server.resource(
  'project/{id}',
  'Get project details by ID',
  async (uri) => {
    const id = uri.pathname.split('/').pop()
    const project = await db.project.findUnique({ where: { id } })
    return {
      contents: [{
        uri: uri.href,
        mimeType: 'application/json',
        text: JSON.stringify(project),
      }],
    }
  }
)

// Start
const transport = new StdioServerTransport()
await server.connect(transport)
```

## Project Structure
```
my-mcp-server/
├── src/
│   ├── index.ts          # Server entry
│   ├── tools/            # Tool definitions
│   │   ├── projects.ts
│   │   └── users.ts
│   └── resources/        # Resource definitions
│       └── docs.ts
├── package.json
└── tsconfig.json
```

## Registration in Claude Code
```jsonc
// ~/.claude/claude_desktop_config.json  OR  .claude/settings.json
{
  "mcpServers": {
    "my-project": {
      "command": "bun",
      "args": ["run", "/path/to/my-mcp-server/src/index.ts"],
      "env": {
        "DATABASE_URL": "..."
      }
    }
  }
}
```

## Registration in Cursor
```jsonc
// .cursor/mcp.json
{
  "mcpServers": {
    "my-project": {
      "command": "bun",
      "args": ["run", "/path/to/my-mcp-server/src/index.ts"]
    }
  }
}
```

## Tool Design Principles
- **Atomic**: One tool = one action. `search_projects` not `manage_projects`
- **Typed**: Use Zod schemas for all inputs — agent gets better type hints
- **Descriptive**: Tool description is the agent's only guide — be specific
- **Safe**: Read-only by default. Mutations require explicit confirmation flow
- **Paginated**: Return max 10-20 items. Provide cursor for more
- **Error-rich**: Return structured errors, not stack traces

## SSE Transport (for remote/web servers)
```typescript
import { SSEServerTransport } from '@modelcontextprotocol/sdk/server/sse.js'
import express from 'express'

const app = express()
app.get('/sse', async (req, res) => {
  const transport = new SSEServerTransport('/message', res)
  await server.connect(transport)
})
app.post('/message', async (req, res) => {
  await transport.handlePostMessage(req, res)
})
app.listen(3001)
```

## Testing
```typescript
import { Client } from '@modelcontextprotocol/sdk/client/index.js'
import { InMemoryTransport } from '@modelcontextprotocol/sdk/inMemory.js'

test('search_projects tool', async () => {
  const [clientTransport, serverTransport] = InMemoryTransport.createLinkedPair()
  await server.connect(serverTransport)
  
  const client = new Client({ name: 'test', version: '1.0' })
  await client.connect(clientTransport)
  
  const result = await client.callTool({ name: 'search_projects', arguments: { query: 'mira' } })
  expect(result.content[0].text).toContain('Mira Manager')
})
```
