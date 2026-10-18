---
name: claude-api-typescript
description: "Build apps with the Claude API (Anthropic TypeScript SDK) and the Claude Agent SDK. Use when: code imports `@anthropic-ai/sdk` or `@anthropic-ai/claude-agent-sdk`, building AI-powered features, tool use, streaming, batches, structured outputs, prompt caching, Managed Agents, or migrating to a newer Claude model. Keywords: anthropic, claude api, messages.create, tool runner, betaZodTool, streaming, adaptive thinking, effort, structured output, model migration, agent sdk, subagents, hooks. Do NOT use for: non-Anthropic providers (OpenAI, Gemini), Python/Go/Java SDKs, or Claude Code CI workflows (claude-ci-actions)."
metadata:
  author: anthropic (adapted for osforge stack)
  version: '2.0'
  source: anthropics/skills/claude-api (bundled claude-api skill, TypeScript subset)
---

# Claude API & Agent SDK - TypeScript

TypeScript-only subset of Anthropic's bundled `claude-api` skill. The files under `shared/` and `typescript/claude-api/` are copied verbatim from upstream and are the authority; `typescript/agent-sdk/` is OSForge-authored (the upstream skill does not cover the Agent SDK). Refresh by re-copying from upstream, never by hand-editing.

## Output requirement

Call Claude through the official SDK (`@anthropic-ai/sdk`). Use raw `fetch` only when the user explicitly asks for REST/raw HTTP. Never mix the two, and never use OpenAI-compatible shims.

**Never guess SDK usage.** Method names, types and import paths must come from the `typescript/` files here or the repositories in `shared/live-sources.md`. If a binding is not documented here, fetch the SDK repo listed in `shared/live-sources.md` before writing code.

If the project already uses another provider (`openai`, `langchain_openai`, `gpt-*`), stop and ask whether to switch it to Claude before editing.

## Defaults

Unless the user requests otherwise:
- Model: `claude-opus-5-5` (exact string, never add date suffixes). Use another model only when the user names it. "sonnet" with no version means `claude-sonnet-5-5`; "haiku" means `claude-haiku-5-5`; "fable" / "most capable" means `claude-fable-5-1`.
- Thinking: `thinking: { type: "adaptive" }` for anything non-trivial. `budget_tokens` is removed (400) on current models.
- Effort: `output_config: { effort: ... }`, set explicitly (Opus 5.5 and Haiku 5.5 default to `medium`, the rest to `high`). `low` for subagents, `max` when correctness beats cost.
- Streaming: default for long input/output or high `max_tokens`; use `.finalMessage()` when you do not need individual events. With user-defined tools on a streaming request set `eager_input_streaming: true` and validate parsed tool inputs (see `shared/tool-use-concepts.md`).
- `max_tokens`: about 16000 non-streaming, about 64000 streaming; low only for classification or cache pre-warming.
- Handle `stop_reason: "refusal"` before reading `content`, and include the server-side `fallbacks` parameter by default on `claude-fable-5-1`, `claude-opus-5-5`, `claude-opus-5` and `claude-sonnet-5-5` code (`typescript/claude-api/README.md` Refusal Fallbacks, `shared/model-migration.md`).

## API drift - your training prior may be stale

| Area | Stale prior | Current API |
|---|---|---|
| Extended thinking | `thinking: {type: "enabled", budget_tokens: N}` | `thinking: {type: "adaptive"}`. `budget_tokens` is rejected (400) on Fable 5/5.1, Sonnet 5/5.5, Opus 4.7/4.8/5/5.5 and Haiku 5.5; deprecated on Opus/Sonnet 4.6; only Haiku 4.5 and older still use it. |
| Disabling thinking | `thinking: {type: "disabled"}` | 400 on Fable 5/5.1 and Opus 5.5 at every effort; on Sonnet 5.5 send `{type: "between_tools"}` at effort `high` or below. Lower `effort` instead. |
| Forced tool use | `tool_choice: {type: "any" \| "tool"}` | 400 on Fable 5.1, Opus 5.5 and Sonnet 5.5. Use `auto` + `strict: true` + a prompt instruction, or structured outputs. |
| Prefill | Last assistant turn as prefill | 400 on the 4.6+ families. Use structured outputs or system-prompt instructions. |
| Sampling | `temperature` / `top_p` / `top_k` | Removed/rejected on current models (see `shared/models.md`). |
| Structured outputs | `output_format` | `output_config: { format: {...} }`; prefer `client.messages.parse()`. |
| Web search / fetch | `web_search_20250305`, `web_fetch_20250910` | `web_search_20260209`, `web_fetch_20260209` on current models; older models keep the basic variants. |
| Code execution | `code_execution_20250522` | `code_execution_20260521` (result block `bash_code_execution_tool_result`). |
| Computer use | `computer_20251124` | `computer_toolset_20260801` on the Claude API and Google Cloud for Opus 5.5 / Sonnet 5.5 / Haiku 5.5. |
| Thinking display | `summarized` by default | `omitted` by default on current models; set `display: "summarized"` to show reasoning. |
| Files API / Skills | `client.beta.files.*` with beta header | Out of beta: `client.files.*`, no header (`shared/live-sources.md`). |
| Preserved thinking | Edit or reorder earlier turns freely | Thinking blocks are bound to the model and conversation; keep histories append-only (`shared/model-migration.md`). |

The `typescript/` files are authoritative over recalled patterns.

## Which surface?

```
1. Single LLM call (classification, summarization, extraction, Q&A)
   -> Claude API: one request, one response

2. Multi-step workflow with code-controlled logic, or a custom agent with YOUR tools
   -> Claude API + tool use (Tool Runner, or the manual loop for full control)

3. Anthropic-hosted agent loop + sandbox (persisted, versioned, scheduled, long-running)
   -> Managed Agents (beta)

4. Batteries-included coding/filesystem agent on your own infra
   -> Claude Agent SDK (a separate package; see typescript/agent-sdk/)
```

Start with the simplest tier that works. Tool Runner (`client.beta.messages.toolRunner`) is a harness over tools you define; the Agent SDK is Claude Code as a library with built-in tools. They are different packages.

## Current models (cached 2026-10-06; verify with `shared/models.md` or `client.models.retrieve`)

| Model | ID | Context | Input $/1M | Output $/1M |
|---|---|---|---|---|
| Claude Fable 5.1 | `claude-fable-5-1` | 1M | $10.00 | $50.00 |
| Claude Opus 5.5 (default) | `claude-opus-5-5` | 1M | $4.00 | $20.00 |
| Claude Opus 5 | `claude-opus-5` | 1M | $5.00 | $25.00 |
| Claude Sonnet 5.5 | `claude-sonnet-5-5` | 1M | $2.00 | $10.00 |
| Claude Haiku 5.5 | `claude-haiku-5-5` | 1M | $0.10 | $0.50 |

Older generations (Fable 5, Mythos, Opus 4.x, Sonnet 5 / 4.x, Haiku 4.5) are still served; their IDs, legacy and retired lists live in `shared/models.md`. Use only exact IDs from that file.

## Quick start

```typescript
import Anthropic from "@anthropic-ai/sdk"
const client = new Anthropic() // ANTHROPIC_API_KEY, or an `ant auth login` profile

const response = await client.messages.create({
  model: "claude-opus-5-5",
  max_tokens: 16000,
  thinking: { type: "adaptive" },
  output_config: { effort: "high" },
  messages: [{ role: "user", content: "What is the capital of France?" }],
})
```

Tool Runner:

```typescript
import { betaZodTool } from "@anthropic-ai/sdk/helpers/beta/zod"
import { z } from "zod"

const searchProjects = betaZodTool({
  name: "search_projects",
  description: "Search projects by name or status",
  inputSchema: z.object({ query: z.string(), status: z.enum(["active", "archived"]).optional() }),
  run: async (input) => JSON.stringify(await findProjects(input)),
})

const finalMessage = await client.beta.messages.toolRunner({
  model: "claude-opus-5-5",
  max_tokens: 16000,
  tools: [searchProjects],
  messages: [{ role: "user", content: "Find active projects about billing" }],
})
```

Agent SDK (see `typescript/agent-sdk/README.md` for options and `patterns.md` for hooks, custom tools, forking):

```typescript
import { query } from "@anthropic-ai/claude-agent-sdk"

for await (const message of query({
  prompt: "Explain this codebase",
  options: { allowedTools: ["Read", "Glob", "Grep"] },
})) {
  if ("result" in message) console.log(message.result)
}
```

## Reading guide (read on demand; all paths relative to this directory)

Always start with `typescript/claude-api/README.md` for any Claude API task.

| Task | Read |
|---|---|
| Single call, chat, vision, multi-turn, caching, compaction, refusal fallbacks | `typescript/claude-api/README.md` |
| Real-time UI / streaming | + `typescript/claude-api/streaming.md` |
| Function calling, agents, structured outputs, code execution, memory | + `shared/tool-use-concepts.md` + `typescript/claude-api/tool-use.md` |
| Batch processing (50% cost) | + `typescript/claude-api/batches.md` |
| File upload / reuse | + `typescript/claude-api/files-api.md` |
| Tracing and observability | `shared/opentelemetry.md` + `typescript/claude-api/opentelemetry.md` |
| Move code to a newer model, replace `budget_tokens` / prefill | `shared/model-migration.md` |
| Which model, IDs, capabilities | `shared/models.md` |
| Prompt caching, low hit rate | `shared/prompt-caching.md` |
| HTTP errors, retries, typed exceptions | `shared/error-codes.md` |
| Per-feature availability on AWS / Bedrock / Vertex / Foundry | `shared/platform-availability.md`, `shared/claude-platform-on-aws.md` |
| Cost, agent design, token counting | `shared/cost-optimization.md`, `shared/agent-design.md`, `shared/token-counting.md` |
| Auditing prompts for dated patterns | `shared/prompt-audit.md` |
| Evals and hill-climbing | `shared/evals/build-eval.md`, `shared/evals/eval-audit.md`, `shared/evals/eval-hillclimb.md` |
| Managed Agents (beta) | `shared/managed-agents-overview.md`, then the topical `shared/managed-agents-*.md`, plus `typescript/managed-agents/README.md` |
| Admin API, CLI, auth | `shared/admin-api.md`, `shared/anthropic-cli.md` |
| Agent SDK (built-in tools, permissions, MCP, subagents, hooks) | `typescript/agent-sdk/README.md`, `typescript/agent-sdk/patterns.md` |
| Latest official docs, SDK repos | `shared/live-sources.md` (fetch the URLs) |

The eval guides mention an optional full report builder (`build-report.mjs`) that may exist in some installs; this copy ships only `shared/evals/report/build-report-lite.mjs`, which the guides use as the fallback.

## Common pitfalls

- Do not truncate inputs silently; if content exceeds the context window, tell the user and discuss chunking or summarization.
- Parse tool inputs with `JSON.parse()`; never string-match serialized input.
- Do not redefine SDK types: use `Anthropic.MessageParam`, `Anthropic.Tool`, `Anthropic.Message`, `Anthropic.ToolUseBlock`.
- Use the SDK's typed errors (`Anthropic.RateLimitError`, `Anthropic.APIError`, ...) in a most-specific-first chain; do not string-match messages.
- Use `stream.finalMessage()` instead of wrapping `.on()` events in a Promise.
- 128K output requires streaming.
- Bash and text-editor tools are Anthropic-defined and schema-less; a custom tool named `bash` is a different tool.
- Server-tool errors (web search / fetch) return HTTP 200 with an error object in the result block; branch on it.
- Advisor tool: the advisor model must be at least as capable as the executor (pairing table in `shared/tool-use-concepts.md`).
- MCP connector needs both `mcp_servers` and a matching `mcp_toolset` entry in `tools`.
