# Compression Rules

## STRIP — Remove completely
- Transitions: "As mentioned", "Worth noting", "Furthermore", "As discussed"
- Rhetoric: "This is revolutionary", "What's most interesting is", "It's important to highlight"
- Hedging: "We believe", "Probably", "Maybe", "It seems that"
- Self-reference: "This document describes", "As above", "As we will see"
- Common knowledge: "Vercel is a cloud platform", "MIT is an open-source license", "TypeScript is a superset of JavaScript"
- Repeated introductions of the same concept
- Transition paragraphs between sections
- Decorative formatting (bold for emphasis, horizontal rules, emojis)
- Filler: "In order to", "It should be noted that", "The fact that", "It is necessary that"
- Formal greetings and closings
- Generic disclaimers

## PRESERVE — Always keep
- Specific numbers, dates, versions, percentages
- Named entities (products, companies, people, technologies)
- Decisions + rationale (compressed: "Decision: X. Reason: Y")
- Rejected alternatives + reason (compressed: "Rejected: X. Reason: Y")
- Explicit and non-negotiable constraints
- Dependencies and ordering relationships
- Open questions and unresolved items
- Scope boundaries (in/out/deferred)
- Success criteria and how they are validated
- User segments and what success means for each
- Risks with severity signals
- Conflicts between source documents
- Environment variables and configurations
- URLs, endpoints, connection strings
- Business rules with conditionals

## TRANSFORM — Change form for efficiency
- Long prose → dense bullet with the same information
- "We decided to use X because Y and Z" → "X (rationale: Y, Z)"
- Repeated category labels → group under a single heading
- "Risk: ... Severity: high" → "HIGH RISK: ..."
- Conditionals → "If X → Y" form
- Multi-sentence explanations → compressed with semicolons
- Lists of short related items → single bullet with semicolons
- "X is used for Y" → "X: Y" (when context is clear)
- Verbose enumerations → parenthesized lists: "platforms (Cursor, Claude Code, Windsurf)"
- Tables with many columns → bullets with key:value
- Code blocks with comments → code without comments (the bullet above explains)

## DEDUPLICATION
- Same fact in multiple docs → keep the version with the most context
- Same concept at different levels of detail → keep the detailed one
- Overlapping lists → merge into a single list without duplicates
- Conflicting docs → note the conflict: "Doc A: X; Doc B: Y — unresolved"
- Executive summary + later expansion → keep only the expansion
- Repeated introductory framing → capture once under the most relevant theme
