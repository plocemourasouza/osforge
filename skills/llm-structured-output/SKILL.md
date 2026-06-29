---
name: llm-structured-output
description: "Decision discipline for getting structured, validated data out of LLMs in product features. Use when: building an LLM feature that must return typed data (extraction, classification, parsing), choosing between Instructor / PydanticAI / Zod, adding retries+validation to model output, or streaming partial structured results. Keywords: structured output, Instructor, PydanticAI, Zod, schema, extraction, validation, retries, LLM JSON, typed output. Do NOT use for: free-form text generation (no schema), prompt wording (prompt-engineering), the Claude SDK API surface (claude-api-typescript)."
model: sonnet
allowed-tools: Read, Grep, Glob, Edit
metadata:
  version: "1.0.0"
  note: "Discipline only — for each library's current API use Context7 (context7-docs-first)."
---

# LLM Structured Output (extraction · validation · retries)

**Iron Law:** `NEVER TRUST RAW LLM TEXT — DEFINE A SCHEMA, VALIDATE, AND RETRY ON FAILURE`

> **Current API:** Instructor / PydanticAI / Zod evolve fast. For exact methods, decorators, and options, **use Context7** (`context7-docs-first`) — this skill is the decision tree and the gotchas, not the API reference.

## When NOT to use
- Free-form prose generation with no schema → just call the model
- A single trivial field → a schema/library is overkill
- Prompt wording / few-shot design → `prompting` / `prompt-engineering`
- The Claude SDK call surface itself → `claude-api-typescript`

## Decision tree (pick the tool)
1. **Extraction / classification / parsing → typed data**
   - **Python** → **Instructor** (Pydantic `BaseModel` + `from_provider`, auto-retry/validation/streaming).
   - **TypeScript** → **Zod** schema + the provider's structured-output mode, or **Instructor-JS**.
   **Done when:** the output is a validated typed object, not a string you parse by hand.
2. **A typed agent runtime** (tools, multi-step, observability, dataset replays) → **PydanticAI** (Python). *"Instructor for extraction, PydanticAI for agents."*
   **Done when:** the agent's tools and outputs are typed and the run is observable.
3. **App-boundary validation of any external/LLM input** (TS) → **Zod** (already the stack default).
   **Done when:** every external input crosses a Zod schema before use.

## Discipline (applies to any of them)
- **Schema first.** Model the output as a typed schema (Pydantic/Zod); let the library coerce + validate.
- **Retry on validation failure** (Instructor `max_retries`; Tenacity). Validation errors are re-asked, not swallowed.
- **Stream partials** for UX when the object is large (`create_partial` / iterable).
- **Keep schemas shallow.** Deep nesting raises failure + retry cost. Flatten where you can.
- **Provider-agnostic.** `from_provider("anthropic/...")` etc. — don't hardcode one vendor's call shape.

## Anti-patterns
| WRONG | RIGHT |
|---|---|
| `JSON.parse(llmText)` and hope | Schema + validate (Instructor/Zod), retry on fail |
| Swallowing a validation error | Re-ask the model (bounded retries) then surface |
| One giant deeply-nested schema | Flatten; split into smaller validated pieces |
| Hardcoding one provider's JSON-mode quirks | Provider-agnostic client (`from_provider`) |
| Baking library API from memory | Confirm current API via Context7 |

## References
- Current API → **Context7** (`context7-docs-first`): `instructor`, `pydantic`, `pydantic-ai`, `zod`
- TS validation default → `Zod` (see `docs/STACK-COVERAGE.md`)
- Input safety → `skills/security-best-practices` (validate all external input)
