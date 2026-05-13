# Claude API & Agent SDK

**Trigger:** @anthropic-ai/sdk, Claude API, tool use, streaming, Agent SDK

---

## Setup

```bash
bun add @anthropic-ai/sdk
```

```typescript
import Anthropic from '@anthropic-ai/sdk'

const client = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
})
```

---

## Basic Message

```typescript
const message = await client.messages.create({
  model: 'claude-sonnet-4-20250514',
  max_tokens: 1024,
  messages: [
    { role: 'user', content: 'Hello, Claude!' }
  ],
})

console.log(message.content[0].text)
```

---

## Streaming

```typescript
const stream = await client.messages.stream({
  model: 'claude-sonnet-4-20250514',
  max_tokens: 1024,
  messages: [
    { role: 'user', content: 'Write a short story.' }
  ],
})

for await (const event of stream) {
  if (event.type === 'content_block_delta' && event.delta.type === 'text_delta') {
    process.stdout.write(event.delta.text)
  }
}

const finalMessage = await stream.finalMessage()
```

---

## Tool Use

```typescript
import { z } from 'zod'

const weatherSchema = z.object({
  location: z.string().describe('City name'),
  unit: z.enum(['celsius', 'fahrenheit']).optional(),
})

const tools = [
  {
    name: 'get_weather',
    description: 'Get current weather for a location',
    input_schema: {
      type: 'object',
      properties: {
        location: { type: 'string', description: 'City name' },
        unit: { type: 'string', enum: ['celsius', 'fahrenheit'] },
      },
      required: ['location'],
    },
  },
]

const message = await client.messages.create({
  model: 'claude-sonnet-4-20250514',
  max_tokens: 1024,
  tools,
  messages: [
    { role: 'user', content: 'What is the weather in Tokyo?' }
  ],
})

// Check if Claude wants to use a tool
if (message.stop_reason === 'tool_use') {
  const toolUse = message.content.find(c => c.type === 'tool_use')

  // Execute the tool
  const result = await getWeather(toolUse.input)

  // Send result back
  const response = await client.messages.create({
    model: 'claude-sonnet-4-20250514',
    max_tokens: 1024,
    tools,
    messages: [
      { role: 'user', content: 'What is the weather in Tokyo?' },
      { role: 'assistant', content: message.content },
      {
        role: 'user',
        content: [{
          type: 'tool_result',
          tool_use_id: toolUse.id,
          content: JSON.stringify(result),
        }],
      },
    ],
  })
}
```

---

## Structured Output

```typescript
const response = await client.messages.create({
  model: 'claude-sonnet-4-20250514',
  max_tokens: 1024,
  messages: [
    { role: 'user', content: 'Extract info from: John Doe, 30 years old, engineer' }
  ],
  // Force JSON output
  response_format: { type: 'json_object' },
})
```

---

## Vision (Images)

```typescript
const message = await client.messages.create({
  model: 'claude-sonnet-4-20250514',
  max_tokens: 1024,
  messages: [
    {
      role: 'user',
      content: [
        {
          type: 'image',
          source: {
            type: 'base64',
            media_type: 'image/png',
            data: base64ImageData,
          },
        },
        {
          type: 'text',
          text: 'What is in this image?',
        },
      ],
    },
  ],
})
```

---

## Batch API (50% Cost Reduction)

```typescript
// Create batch
const batch = await client.batches.create({
  requests: [
    {
      custom_id: 'req-1',
      params: {
        model: 'claude-sonnet-4-20250514',
        max_tokens: 1024,
        messages: [{ role: 'user', content: 'Hello' }],
      },
    },
    // ... more requests
  ],
})

// Check status
const status = await client.batches.retrieve(batch.id)

// Get results when complete
if (status.status === 'completed') {
  const results = await client.batches.results(batch.id)
}
```

---

## Current Models

| Model | ID | Best For |
|-------|-----|----------|
| Opus 4.5 | `claude-opus-4-5-20251101` | Complex reasoning, planning |
| Sonnet 4 | `claude-sonnet-4-20250514` | Balanced performance/cost |
| Haiku 3.5 | `claude-3-5-haiku-20241022` | Fast, simple tasks |

---

## Extended Thinking

```typescript
const message = await client.messages.create({
  model: 'claude-sonnet-4-20250514',
  max_tokens: 16000,
  thinking: {
    type: 'enabled',
    budget_tokens: 10000,  // Tokens for internal reasoning
  },
  messages: [
    { role: 'user', content: 'Solve this complex math problem...' }
  ],
})

// Access thinking
const thinking = message.content.find(c => c.type === 'thinking')
console.log('Reasoning:', thinking?.thinking)

const answer = message.content.find(c => c.type === 'text')
console.log('Answer:', answer?.text)
```

---

## Agent SDK

```bash
bun add @anthropic-ai/claude-agent-sdk
```

```typescript
import { Agent, Tool } from '@anthropic-ai/claude-agent-sdk'

const agent = new Agent({
  model: 'claude-sonnet-4-20250514',
  tools: [
    new Tool({
      name: 'search',
      description: 'Search the web',
      schema: z.object({ query: z.string() }),
      execute: async ({ query }) => {
        return await searchWeb(query)
      },
    }),
  ],
})

const result = await agent.run('Find information about Next.js 15')
```

### Subagents

```typescript
const researchAgent = new Agent({
  name: 'researcher',
  model: 'claude-sonnet-4-20250514',
  tools: [searchTool],
})

const writerAgent = new Agent({
  name: 'writer',
  model: 'claude-sonnet-4-20250514',
  subagents: [researchAgent],
})

await writerAgent.run('Write an article about AI trends')
```

---

## Error Handling

```typescript
import { APIError, RateLimitError } from '@anthropic-ai/sdk'

try {
  const message = await client.messages.create({...})
} catch (error) {
  if (error instanceof RateLimitError) {
    // Wait and retry
    await sleep(error.retryAfter * 1000)
    // Retry...
  } else if (error instanceof APIError) {
    console.error('API Error:', error.message, error.status)
  }
}
```

---

## Best Practices

1. **Use streaming** for better UX in interactive apps
2. **Batch requests** for bulk processing (50% cheaper)
3. **Cache responses** where appropriate
4. **Handle rate limits** with exponential backoff
5. **Use Haiku** for simple tasks to reduce costs
6. **Enable thinking** for complex reasoning tasks
7. **Validate tool inputs** with Zod schemas
