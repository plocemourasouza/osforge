---
name: claude-api-typescript
description: "Build apps with the Claude API, Anthropic TypeScript SDK, and Agent SDK. TRIGGER when: code imports `@anthropic-ai/sdk` or `@anthropic-ai/claude-agent-sdk`, user asks to use Claude API, build AI-powered features, create agents programmatically, implement tool use, streaming, batches, or structured outputs. Also trigger for Agent SDK patterns: subagents, hooks, MCP integration, permissions."
metadata:
  author: anthropic (adapted for osforge stack)
  version: '1.0'
  source: anthropics/skills/claude-api
---

# Claude API & Agent SDK — TypeScript

## Defaults
- Model: `claude-opus-4-6` (always, unless user explicitly requests another)
- Thinking: `thinking: { type: "adaptive" }` (Opus 4.6 / Sonnet 4.6 — do NOT use `budget_tokens`, it's deprecated)
- Streaming: default for any request with long input/output — use `.finalMessage()` to get complete response
- Effort: `output_config: { effort: "high" }` (default). Use `"low"` for subagents, `"max"` for deep reasoning (Opus only)

## Current Models (2026-02)

| Model | ID | Context | Input $/1M | Output $/1M |
|---|---|---|---|---|
| Claude Opus 4.6 | `claude-opus-4-6` | 200K (1M beta) | $5.00 | $25.00 |
| Claude Sonnet 4.6 | `claude-sonnet-4-6` | 200K (1M beta) | $3.00 | $15.00 |
| Claude Haiku 4.5 | `claude-haiku-4-5` | 200K | $1.00 | $5.00 |

## Which Surface?

```
1. Single LLM call (classification, summarization, extraction)
   → Claude API — one request, one response

2. Does Claude need file/web/shell access autonomously?
   → Yes → Agent SDK — built-in tools, don't reimplement

3. Multi-step workflow with YOUR tools (code-orchestrated)
   → Claude API + tool use — you control the loop

4. Open-ended agent with your own tools
   → Claude API agentic loop (maximum flexibility)
```

## Quick Start — Claude API

```typescript
import Anthropic from "@anthropic-ai/sdk"
const client = new Anthropic() // uses ANTHROPIC_API_KEY env var

const response = await client.messages.create({
  model: "claude-opus-4-6",
  max_tokens: 1024,
  thinking: { type: "adaptive" },
  messages: [{ role: "user", content: "What is the capital of France?" }],
})
```

## Quick Start — Agent SDK

```typescript
import { query } from "@anthropic-ai/claude-agent-sdk"

for await (const message of query({
  prompt: "Explain this codebase",
  options: { allowedTools: ["Read", "Glob", "Grep"] },
})) {
  if ("result" in message) console.log(message.result)
}
```

## Quick Start — Subagents (Agent SDK)

```typescript
import { query } from "@anthropic-ai/claude-agent-sdk"

// Define subagents via options.agents — the main agent delegates with the Agent tool
for await (const message of query({
  prompt: "Audit this repo: review code quality and check test coverage",
  options: {
    allowedTools: ["Read", "Glob", "Grep", "Agent"],
    agents: {
      "code-reviewer": {
        description: "Reviews code for quality and best practices",
        prompt: "You are a senior code reviewer. Be concise and actionable.",
        tools: ["Read", "Glob", "Grep"],
        model: "sonnet", // cheaper model for subagent work
      },
      "test-auditor": {
        description: "Audits test coverage and test quality",
        prompt: "Find untested code paths and weak assertions.",
        tools: ["Read", "Glob", "Grep"],
      },
    },
  },
})) {
  if ("result" in message) console.log(message.result)
}
```

## Reference Files (read on demand)

### Claude API
1. **`typescript/claude-api/README.md`** — Installation, basic usage, vision, multi-turn, system prompts, error handling
2. **`typescript/claude-api/tool-use.md`** — Tool Runner (betaZodTool + Zod), manual agentic loop, code execution, memory tool, structured outputs
3. **`typescript/claude-api/streaming.md`** — Streaming patterns, event handling, tool use with streaming
4. **`typescript/claude-api/batches.md`** — Batch processing (50% cost, async)
5. **`typescript/claude-api/files-api.md`** — File upload/reuse across requests

### Agent SDK
6. **`typescript/agent-sdk/README.md`** — Built-in tools, permissions, MCP support, subagents
7. **`typescript/agent-sdk/patterns.md`** — Hooks (PostToolUse), custom tools, session forking, CI/CD patterns

### Shared
8. **`shared/tool-use-concepts.md`** — Tool definition structure, tool choice, server-side tools, tool runner vs manual loop
9. **`shared/models.md`** — Complete model catalog with exact IDs and aliases
10. **`shared/error-codes.md`** — HTTP error codes, rate limits, retry strategies

## Key Patterns (Inline)

### Tool Runner (Recommended)
```typescript
import { betaZodTool } from "@anthropic-ai/sdk/helpers/beta/zod"
import { z } from "zod"

const searchProjects = betaZodTool({
  name: "search_projects",
  description: "Search projects by name or status",
  inputSchema: z.object({
    query: z.string(),
    status: z.enum(["active", "archived"]).optional(),
  }),
  run: async (input) => {
    const projects = await prisma.project.findMany({
      where: { name: { contains: input.query, mode: "insensitive" } },
    })
    return JSON.stringify(projects)
  },
})

const result = await client.beta.messages.toolRunner({
  model: "claude-opus-4-6",
  max_tokens: 4096,
  tools: [searchProjects],
  messages: [{ role: "user", content: "Find active projects about billing" }],
})
```

### Structured Outputs
```typescript
const response = await client.messages.create({
  model: "claude-opus-4-6",
  max_tokens: 1024,
  output_config: {
    format: {
      type: "json_schema",
      json_schema: {
        name: "analysis",
        schema: {
          type: "object",
          properties: {
            sentiment: { type: "string", enum: ["positive", "negative", "neutral"] },
            confidence: { type: "number" },
            summary: { type: "string" },
          },
          required: ["sentiment", "confidence", "summary"],
        },
      },
    },
  },
  messages: [{ role: "user", content: "Analyze: The product exceeded expectations" }],
})
```

### Agent SDK Subagents
```typescript
for await (const message of query({
  prompt: "Review this codebase for security issues",
  options: {
    allowedTools: ["Read", "Glob", "Grep", "Agent"],
    agents: {
      "security-reviewer": {
        description: "Expert security code reviewer",
        prompt: "Analyze code for vulnerabilities following OWASP guidelines",
        tools: ["Read", "Glob", "Grep"],
      },
    },
  },
})) {
  if ("result" in message) console.log(message.result)
}
```

### Agent SDK Hooks
```typescript
import { query, HookCallback } from "@anthropic-ai/claude-agent-sdk"
import { appendFileSync } from "fs"

const logFileChange: HookCallback = async (input) => {
  const filePath = (input as any).tool_input?.file_path ?? "unknown"
  appendFileSync("./audit.log", `${new Date().toISOString()}: modified ${filePath}\n`)
  return {}
}

for await (const message of query({
  prompt: "Refactor utils.ts",
  options: {
    allowedTools: ["Read", "Edit", "Write"],
    permissionMode: "acceptEdits",
    hooks: {
      PostToolUse: [{ matcher: "Edit|Write", hooks: [logFileChange] }],
    },
  },
})) { /* ... */ }
```

## Common Pitfalls
- **Opus 4.6:** `budget_tokens` is deprecated — use `thinking: { type: "adaptive" }`
- **Opus 4.6:** Assistant message prefills return 400 error — use structured outputs instead
- **128K output:** Requires streaming — use `.stream()` with `.finalMessage()`
- **Structured outputs:** Use `output_config: { format: {...} }` (not deprecated `output_format`)
- **Don't redefine SDK types:** Use `Anthropic.MessageParam`, `Anthropic.Tool`, etc.
- **Tool inputs:** Always `JSON.parse()` — never string-match on serialized input
