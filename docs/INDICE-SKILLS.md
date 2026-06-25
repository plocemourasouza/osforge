# 📚 Índice Completo de Agent Skills

> **Total:** 170 skills indexadas de 1 repositórios
> **Pasta local:** `~/Development/osforge/sources/` (fontes) e `~/Development/osforge/skills/` (curadas)
>
> 💡 **Dica de busca:** Use `Ctrl+F` / `Cmd+F` para pesquisar por palavra-chave.
> Para instalar uma skill: `cp -R ~/Development/osforge/<path_local> .claude/skills/`

---

## 📊 Estatísticas

### Por Categoria

| Categoria | Qtd | % |
|-----------|-----|---|
| 🔒 Security | 44 | 25.9% |
| 🔄 Workflow / Process | 28 | 16.5% |
| ⚛️ React / Frontend | 24 | 14.1% |
| 🤖 AI / ML / Agents | 21 | 12.4% |
| 🧪 Testing | 17 | 10.0% |
| 🏗️ Architecture | 8 | 4.7% |
| 📦 General | 7 | 4.1% |
| 📝 Documentation / Writing | 6 | 3.5% |
| 🗄️ Database / Backend | 5 | 2.9% |
| 📱 Mobile | 4 | 2.4% |
| ☁️ Infrastructure / DevOps | 3 | 1.8% |
| 💼 Business / Marketing | 2 | 1.2% |
| 🎨 Design / Creative | 1 | 0.6% |
| **TOTAL** | **170** | **100%** |

### Por Origem

| Origem | Repo | Qtd |
|--------|------|-----|
| skills | — | 170 |

---

## 🗂️ Sumário por Categoria

- [🔒 Security (44)](#)
- [🔄 Workflow / Process (28)](#)
- [⚛️ React / Frontend (24)](#)
- [🤖 AI / ML / Agents (21)](#)
- [🧪 Testing (17)](#)
- [🏗️ Architecture (8)](#)
- [📦 General (7)](#)
- [📝 Documentation / Writing (6)](#)
- [🗄️ Database / Backend (5)](#)
- [📱 Mobile (4)](#)
- [☁️ Infrastructure / DevOps (3)](#)
- [💼 Business / Marketing (2)](#)
- [🎨 Design / Creative (1)](#)

---

## 🔒 Security

**44 skills**

| Skill | Origem | Descrição | Path Local |
|-------|--------|-----------|-----------|
| **accessibility** | 📦 skills | Audit and improve web accessibility following WCAG 2.1 guidelines. Use when asked to "improve accessibility", "a11y audit", "WCAG compliance", "screen… | `skills/accessibility/` |
| **agent-skills-search** | 📦 skills | Search and install Agent Skills from the local sources at ~/Development/osforge/sources/. Use when looking for specialized skills, best practices, or … | `skills/agent-skills-search/` |
| **best-practices** | 📦 skills | Apply modern web development best practices for security, compatibility, and code quality. Use when asked to "apply best practices", "security audit",… | `skills/best-practices/` |
| **code-review-checklist** | 📦 skills | Code review checklist covering correctness, security, performance, quality, testing, and patterns specific to AI-generated code. Use when: asked to re… | `skills/code-review-checklist/` |
| **database-design** | 📦 skills | Database design principles: database and ORM choice, schema, indexes, optimization, and migrations. Use when: a slow query or N+1 in production, choos… | `skills/database-design/` |
| **differential-review** | 📦 skills | Security-focused code review of diffs and PRs. Trigger on PR security review, git diff analysis, change impact assessment, or when reviewing commits t… | `skills/differential-review/` |
| **gdpr-data-handling** | 📦 skills | GDPR/LGPD compliance patterns for data handling. Trigger on consent management, data subject rights (access, deletion, portability), privacy policies,… | `skills/gdpr-data-handling/` |
| **insecure-defaults** | 📦 skills | Detect fail-open patterns and insecure default configurations. Trigger on security hardening, env variable audit, default config review, permission ch… | `skills/insecure-defaults/` |
| **lint-and-validate** | 📦 skills | Automatic quality control after every code change: lint, type-check, and static analysis (eslint, tsc, ruff, mypy, bandit, npm audit). Use when: you j… | `skills/lint-and-validate/` |
| **nodejs-best-practices** | 📦 skills | Node.js development principles: framework choice, async patterns, layered architecture, validation, error handling, and security. Use when: choosing b… | `skills/nodejs-best-practices/` |
| **offensive-ai-security** | 📦 skills | AI/LLM security offensive checklist: prompt injection, jailbreaking, model extraction, training data poisoning, adversarial inputs, LLM-assisted attac… | `skills/offensive-ai-security/` |
| **offensive-bug-identification** | 📦 skills | Systematic bug identification methodology: source code review patterns, black-box testing strategies, taint analysis, dangerous function hunting, data… | `skills/offensive-bug-identification/` |
| **offensive-business-logic** | 📦 skills | Business logic vulnerability testing for web/mobile/API engagements. Covers workflow bypass, state machine violations, multi-step process abuse, price… | `skills/offensive-business-logic/` |
| **offensive-cloud** | 📦 skills | Cloud security attack methodology across AWS, Azure, and GCP. Covers credential harvesting (IMDS, ~/.aws, env vars, leaked CI secrets, instance roles)… | `skills/offensive-cloud/` |
| **offensive-deserialization** | 📦 skills | Insecure deserialization attack checklist: identifying deserialization sinks, Java/PHP/.NET/Python deserialization exploitation, ysoserial gadget chai… | `skills/offensive-deserialization/` |
| **offensive-fast-checking** | 📦 skills | Speed-optimized offensive checklist for rapid assessment: quick-win vulnerability patterns, fast recon shortcuts, automated scanner configurations, an… | `skills/offensive-fast-checking/` |
| **offensive-file-upload** | 📦 skills | File upload vulnerability checklist: MIME type bypass, extension bypass, magic byte manipulation, path traversal in filenames, stored XSS via SVG/HTML… | `skills/offensive-file-upload/` |
| **offensive-fuzzing** | 📦 skills | Practical offensive fuzzing methodology covering target identification, fuzzer selection (AFL++, libFuzzer, Honggfuzz, Boofuzz, syzkaller), harness wr… | `skills/offensive-fuzzing/` |
| **offensive-graphql** | 📦 skills | GraphQL security testing checklist: introspection abuse, batching attacks, query depth/complexity DoS, field suggestion enumeration, IDOR via GraphQL,… | `skills/offensive-graphql/` |
| **offensive-idor** | 📦 skills | IDOR (Insecure Direct Object Reference) testing checklist: object ID enumeration, horizontal/vertical privilege escalation, GUID predictability, indir… | `skills/offensive-idor/` |
| **offensive-jwt** | 📦 skills | JWT attack methodology for penetration testers. Covers algorithm confusion (alg:none, RS256→HS256), weak HMAC secret brute force, kid parameter inject… | `skills/offensive-jwt/` |
| **offensive-mobile** | 📦 skills | Mobile (Android + iOS) application penetration testing methodology. Covers static analysis (apktool/jadx for Android, class-dump/Hopper/IDA for iOS), … | `skills/offensive-mobile/` |
| **offensive-open-redirect** | 📦 skills | Open redirect vulnerability checklist: parameter identification, bypass techniques (URL encoding, double slashes, CRLF injection, protocol handlers), … | `skills/offensive-open-redirect/` |
| **offensive-osint** | 📦 skills | Comprehensive OSINT methodology skill for offensive security, red team intelligence gathering, and bug bounty reconnaissance. Covers domain recon, ema… | `skills/offensive-osint/` |
| **offensive-parameter-pollution** | 📦 skills | HTTP parameter pollution (HPP) checklist: duplicate parameter injection, backend vs frontend parsing differences, WAF bypass via HPP, server-side vs c… | `skills/offensive-parameter-pollution/` |
| **offensive-race-condition** | 📦 skills | Race condition (TOCTOU) testing checklist: identifying timing windows, Burp Suite Turbo Intruder, Last-Byte sync technique, rate limit bypass, double-… | `skills/offensive-race-condition/` |
| **offensive-rce** | 📦 skills | Remote Code Execution testing checklist: OS command injection, SSTI-to-RCE, deserialization RCE, file upload RCE, XXE with SSRF to RCE, RCE via depend… | `skills/offensive-rce/` |
| **offensive-request-smuggling** | 📦 skills | HTTP request smuggling checklist: CL.TE, TE.CL, TE.TE variants, detection with timing and differential responses, WAF bypass, cache poisoning, credent… | `skills/offensive-request-smuggling/` |
| **offensive-sqli** | 📦 skills | SQL injection testing skill for offensive security assessments and bug bounty hunting. Covers error-based, UNION-based, boolean/time-based blind, out-… | `skills/offensive-sqli/` |
| **offensive-ssti** | 📦 skills | Server-Side Template Injection testing checklist: template engine identification (Jinja2, Twig, Freemarker, Pebble, Velocity), polyglot detection payl… | `skills/offensive-ssti/` |
| **offensive-toctou** | 📦 skills | Time-of-Check / Time-of-Use (TOCTOU) race condition exploitation methodology across binary, kernel, filesystem, web, and container layers. Covers symb… | `skills/offensive-toctou/` |
| **offensive-waf-bypass** | 📦 skills | WAF bypass techniques checklist: encoding bypass (URL/HTML/Unicode/double encoding), case variation, comment injection, HTTP header manipulation, chun… | `skills/offensive-waf-bypass/` |
| **offensive-xss** | 📦 skills | Cross-Site Scripting testing checklist: stored/reflected/DOM/blind XSS discovery, polyglot payloads, CSP bypass, XSS filter bypass, event handler inje… | `skills/offensive-xss/` |
| **offensive-xxe** | 📦 skills | XML External Entity injection testing checklist: classic XXE, blind XXE (out-of-band), XXE via file upload (SVG/docx), XXE in SOAP/REST, error-based X… | `skills/offensive-xxe/` |
| **red-team-tactics** | 📦 skills | Red team tactics based on MITRE ATT&CK for authorized adversary simulation. Use when: planning an authorized attack simulation/pentest, structuring a … | `skills/red-team-tactics/` |
| **redesign-audit** | 📦 skills | OSForge enhancement layer sobre redesign-existing-projects. Audita projeto existente, identifica padrões AI-genéricos, aplica upgrades cirúrgicos + re… | `skills/redesign-audit/` |
| **redesign-existing-projects** | 📦 skills | Elevates existing sites and apps to premium quality: audits the current design, identifies generic AI patterns, and applies typography, color, and lay… | `skills/redesign-existing-projects/` |
| **security-best-practices** | 📦 skills | Perform language and framework specific security best-practice reviews and suggest improvements. Trigger only when the user explicitly requests securi… | `skills/security-best-practices/` |
| **security-threat-model** | 📦 skills | Repository-grounded threat modeling that enumerates trust boundaries, assets, attacker capabilities, abuse paths, and mitigations, and writes a concis… | `skills/security-threat-model/` |
| **tool-safety-classifier** | 📦 skills | LLM-powered security classifier for auto-approval of tool calls in autonomous modes (CI, headless, agent-of-agents). Use when: the user runs in "autom… | `skills/tool-safety-classifier/` |
| **ui-audit** | 📦 skills | Retroactive visual quality audit of already-implemented frontend code. Use after any UI/UX phase, or when: | `skills/quality/ui-audit/` |
| **vulnerability-scanner** | 📦 skills | Advanced vulnerability analysis with OWASP Top 10:2025, supply chain security, and risk prioritization. Use when: mapping a project | `skills/vulnerability-scanner/` |
| **web-design-guidelines** | 📦 skills | Review UI code for Web Interface Guidelines compliance. Use when asked to "review my UI", "check accessibility", "audit design", "review UX", or "chec… | `skills/web-design-guidelines/` |
| **webapp-testing** | 📦 skills | E2E testing of web applications with Playwright, deep route/endpoint auditing, and visual testing, with a browser runner script included. Use when: te… | `skills/webapp-testing/` |

## 🔄 Workflow / Process

**28 skills**

| Skill | Origem | Descrição | Path Local |
|-------|--------|-----------|-----------|
| **3d-games** | 📦 skills | 3D game principles: rendering pipeline, shaders, 3D physics and collision, cameras, lighting, and LOD. Use when: my 3D game has too many draw calls an… | `skills/game-development/3d-games/` |
| **adversarial-review** | 📦 skills | Cynical, adversarial review of any artifact. Use when: reviewing a spec before implementing, validating a PRD, critiquing a schema, reviewing code wit… | `skills/quality/adversarial-review/` |
| **aesthetic-modes** | 📦 skills | Three distinct visual modes for projects with a strong identity: EDITORIAL_MINIMALIST (Notion/Linear, warm monochrome), INDUSTRIAL_BRUTALIST (Swiss + … | `skills/aesthetic-modes/` |
| **agency-product** | 📦 skills | Index of the Agency | `skills/agency/product/` |
| **agency-project-management** | 📦 skills | Index of the Agency | `skills/agency/project-management/` |
| **behavioral-modes** | 📦 skills | AI operational modes (brainstorm, implement, debug, review, teach, ship, orchestrate). Use to adapt behavior based on task type. | `skills/behavioral-modes/` |
| **brainstorming** | 📦 skills | Socratic refinement of an idea BEFORE any code or technical spec. Use when: the user describes a vague idea, wants to explore alternatives before comm… | `skills/brainstorming/` |
| **code-review** | 📦 skills | Structured code review with a checklist adapted to the OSForge stack. Use when: code review, review code, review PR, CR. Integrates adversarial-review… | `skills/quality/code-review/` |
| **core-web-vitals** | 📦 skills | Optimize Core Web Vitals (LCP, INP, CLS) for better page experience and search ranking. Use when asked to "improve Core Web Vitals", "fix LCP", "reduc… | `skills/core-web-vitals/` |
| **finishing-a-development-branch** | 📦 skills | Development branch finalization workflow. Use when: all tasks on a branch are complete, the user wants to merge or open a PR, ready to ship. Keywords:… | `skills/finishing-a-development-branch/` |
| **game-audio** | 📦 skills | Game audio principles: SFX, music, formats and compression, adaptive audio, performance, and audio accessibility. Use when: I want to add sounds and m… | `skills/game-development/game-audio/` |
| **game-design** | 📦 skills | Game design principles: core loop, GDD structure, player psychology, difficulty balancing, and progression. Use when: my game isn | `skills/game-development/game-design/` |
| **high-end-visual-design** | 📦 skills | Makes the site look expensive at agency level: premium fonts, double-bezel cards, ultra-diffused shadows, floating glass pill nav, and motion choreogr… | `skills/high-end-visual-design/` |
| **image-to-code** | 📦 skills | Elite website image-to-code skill for Codex. Trigger on requests like "design a stunning hero section", "build a premium landing page", or "redesign t… | `skills/image-to-code/` |
| **industrial-brutalist-ui** | 📦 skills | Generates industrial brutalist interfaces that fuse Swiss typographic print with military/CRT terminals: rigid grids, monospace, giant typography, haz… | `skills/industrial-brutalist-ui/` |
| **osforge-canvas** | 📦 skills | Local generative UI for interactive review of plans, specs, and breakdowns in the browser, with native structured feedback. DEFAULT CHANNEL for presen… | `skills/osforge-canvas/` |
| **pc-games** | 📦 skills | PC game principles (Windows, Mac, Linux): publishing on Steam, graphics settings, control rebinding, modding, and desktop accessibility. Use when: I | `skills/game-development/pc-games/` |
| **receiving-code-review** | 📦 skills | How to respond to code review feedback. Use when: received review feedback, PR has comments, reviewer requested changes, CHANGES_REQUESTED. Keywords: … | `skills/receiving-code-review/` |
| **requirements-clarify** | 📦 skills | Structured requirements clarification BEFORE the technical plan. Use when: a spec has vague or underspecified areas, the user said | `skills/planning/requirements-clarify/` |
| **seo** | 📦 skills | Optimize for search engine visibility and ranking. Use when asked to "improve SEO", "optimize for search", "fix meta tags", "add structured data", "si… | `skills/seo/` |
| **seo-fundamentals** | 📦 skills | SEO fundamentals for Google with E-E-A-T, Core Web Vitals, and technical SEO. Use when: improving a page | `skills/seo-fundamentals/` |
| **story-executor** | 📦 skills | Executes implementation of a story following its tasks and ACs. Use when: execute story, implement story, dev story, run story. Coordinates invocation… | `skills/planning/story-executor/` |
| **stripe-integration** | 📦 skills | Stripe payment processing for SaaS applications. Trigger on checkout implementation, subscription billing, webhook handling, pricing page, payment for… | `skills/stripe-integration/` |
| **systematic-debugging** | 📦 skills | Systematic 4-phase debugging with root-cause analysis. Use when: a bug is hard to reproduce, a crash has no clear stacktrace, intermittent behavior, a… | `skills/systematic-debugging/` |
| **ui-design-intelligence** | 📦 skills | Design system spec adapted to the product and industry. Use when: the user mentions visual style, identity, palette, typography, visual tone, product … | `skills/ui-design-intelligence/` |
| **verification-before-completion** | 📦 skills | Requires running verification commands and confirming output before making any success claims. Use when about to claim work is complete, fixed, passin… | `skills/verification-before-completion/` |
| **vr-ar** | 📦 skills | VR/AR game principles: comfort and motion sickness prevention, locomotion, hand tracking, AR anchoring, and per-headset performance targets. Use when:… | `skills/game-development/vr-ar/` |
| **web-games** | 📦 skills | Browser game principles: framework selection (Phaser, PixiJS, Three.js, Babylon.js), WebGPU vs WebGL, asset compression, PWA, and browser audio. Use w… | `skills/game-development/web-games/` |

## ⚛️ React / Frontend

**24 skills**

| Skill | Origem | Descrição | Path Local |
|-------|--------|-----------|-----------|
| **aesthetic-boost** | 📦 skills | Anti-AI-slop aesthetic boost. Invoke alongside any frontend skill to elevate visual quality. Activate when the user asks for "beautiful design", "stri… | `skills/aesthetic-boost/` |
| **app-builder** | 📦 skills | Orchestrator for building full-stack applications from natural-language requests, with 13 scaffolding templates and agent coordination. Use when: crea… | `skills/app-builder/` |
| **arch-builder** | 📦 skills | Facilitation of architectural decisions with ADRs. Stack-aware — respects project-context.md and optimizes for Next.js/Prisma/Supabase. Use with phras… | `skills/planning/arch-builder/` |
| **autorefine-skill** | 📦 skills | Iterative autonomous refinement with autoresearch loop + meta-optimization + cross-domain transfer. Use when (e.g. | `skills/autorefine-skill/` |
| **design-md** | 📦 skills | PER-PROJECT brand identity contract in a DESIGN.md file — the 9-section document (Visual Theme, Color, Typography, Spacing, Layout, Components, Motion… | `skills/design-md/` |
| **design-taste-frontend** | 📦 skills | Anti-slop frontend skill for landing pages, portfolios, and redesigns. Trigger on phrases like "build a landing page", "create my portfolio site", "re… | `skills/design-taste-frontend/` |
| **design-taste-frontend-v1** | 📦 skills | Legacy v1 of the premium frontend taste-skill with fixed dials (variance 8, motion 6, density 4), anti-slop, Inter and AI-purple bans, and magnetic mi… | `skills/design-taste-frontend-v1/` |
| **dispatching-parallel-agents** | 📦 skills | Orchestrates parallel tasks across independent subagents. Use when: 2+ tasks with no shared state, refactoring across multiple unrelated files, decomp… | `skills/dispatching-parallel-agents/` |
| **frontend-design** | 📦 skills | Design thinking and decision-making for web UI. ACTIVATE whenever the user asks to design or style UI components, build page layouts, choose color pal… | `skills/frontend-design/` |
| **frontend-ui-system** | 📦 skills | Frontend UI development using shadcn/ui ecosystem with extended registries (Magic UI, Aceternity UI, mapcn). Leverages shadcn MCP and shadcn Studio ex… | `skills/frontend-ui-system/` |
| **game-art** | 📦 skills | Game art principles: asset pipeline, texture optimization, animation (sprite, skeletal, procedural), VFX, and art direction. Use when: how to organize… | `skills/game-development/game-art/` |
| **gpt-taste** | 📦 skills | Award-winning design engineering with advanced GSAP motion: layout randomization, AIDA structure, hero of at most 2-3 lines, bento grids with no empty… | `skills/gpt-taste/` |
| **i18n-localization** | 📦 skills | Internationalization for Next.js applications. Trigger on multi-language support ("set up multiple languages", "add English/Spanish support", "transla… | `skills/i18n-localization/` |
| **imagegen-frontend-mobile** | 📦 skills | Elite mobile app image-generation skill for creating premium, app-native screen concepts and flows. Keywords - mobile UI design, iOS app design, Andro… | `skills/imagegen-frontend-mobile/` |
| **imagegen-frontend-web** | 📦 skills | Art direction for generating premium site mockups via image generation: one separate horizontal image per section, hero composition variety, and a sin… | `skills/imagegen-frontend-web/` |
| **nextjs-react-expert** | 📦 skills | React and Next.js performance optimization from Vercel Engineering. Use when building React components, optimizing performance, eliminating waterfalls… | `skills/nextjs-react-expert/` |
| **nextjs-supabase-auth** | 📦 skills | Next.js App Router + Supabase Auth authentication patterns. Use when: configuring auth middleware, multi-org RBAC, session management, token refresh, … | `skills/nextjs-supabase-auth/` |
| **openui-genui-layout** | 📦 skills | UI planning and generation in Next.js. Use when: creating any page, screen, dashboard, form, table, layout component, route scaffold. Produces an Open… | `skills/openui-genui-layout/` |
| **performance-profiling** | 📦 skills | Performance profiling principles: measure, analyze, and optimize using Core Web Vitals, Lighthouse, and profiling tools. Use when: slow page or poor L… | `skills/performance-profiling/` |
| **react-performance** | 📦 skills | React and Next.js performance optimization rules from Vercel Engineering. Use when writing, reviewing, or refactoring React components, Next.js pages,… | `skills/react-performance/` |
| **stitch-design-taste** | 📦 skills | Generates semantic DESIGN.md files for Google Stitch, encoding atmosphere, calibrated palette, typography, components, and anti-patterns in natural la… | `skills/stitch-design-taste/` |
| **tailwind-patterns** | 📦 skills | Technical Tailwind CSS v4 patterns: CSS-first configuration with @theme, the Oxide engine, native container queries, design tokens as CSS variables, a… | `skills/tailwind-patterns/` |
| **taste-design-dials** | 📦 skills | OSForge enhancement layer on top of the taste-skill with 3 adjustable dials (DESIGN_VARIANCE, MOTION_INTENSITY, VISUAL_DENSITY) plus Next.js App Route… | `skills/taste-design-dials/` |
| **visual-planner** | 📦 skills | Transforms planning documents into visual, interactive HTML breakdowns. Use when: visualizing a plan, turning a spec into HTML, creating a visual brea… | `skills/visual-planner/` |

## 🤖 AI / ML / Agents

**21 skills**

| Skill | Origem | Descrição | Path Local |
|-------|--------|-----------|-----------|
| **architecture** | 📦 skills | Architectural decision framework with requirements analysis, trade-off evaluation, and documentation in ADRs. Use when: deciding between X and Y (mono… | `skills/architecture/` |
| **claude-api-typescript** | 📦 skills | Build apps with the Claude API, Anthropic TypeScript SDK, and Agent SDK. TRIGGER when: code imports `@anthropic-ai/sdk` or `@anthropic-ai/claude-agent… | `skills/claude-api-typescript/` |
| **clean-code** | 📦 skills | Pragmatic clean-code standards: concise, direct, no over-engineering, and no unnecessary comments. Use when: code is over-engineered or has premature … | `skills/clean-code/` |
| **coding-guidelines** | 📦 skills | Apply when writing, modifying, or reviewing code. Behavioral guidelines to reduce common LLM coding mistakes. Triggers on implementation tasks, code c… | `skills/coding-guidelines/` |
| **config-critique** | 📦 skills | LLM-powered lint of user customizations in OSForge — validates new SKILL.md, .mdc rules, custom hooks, additional agents, and CLAUDE.md overrides acro… | `skills/config-critique/` |
| **context-compact** | 📦 skills | Structured conversation compaction when reaching ~70% of the context window. Use when: user says "compress context", "compact", "summary", "near the l… | `skills/context-compact/` |
| **context-distillator** | 📦 skills | Lossless compression of long documents for optimized LLM consumption, preserving 100% of the factual information and eliminating textual overhead. Use… | `skills/context/context-distillator/` |
| **db-state-sync** | 📦 skills | Manages project state in OSForge | `skills/context/db-state-sync/` |
| **doc-shard** | 📦 skills | Split large markdown documents into smaller organized files with an index. Use when a document exceeds the context window or to organize extensive doc… | `skills/context/doc-shard/` |
| **documentation-templates** | 📦 skills | Ready-made templates and structure guides for documentation: README, API docs, code comments, and AI-friendly docs. Use when: creating a README from s… | `skills/documentation-templates/` |
| **editorial-review** | 📦 skills | Editorial review of technical documents in 2 modes: prose (clinical copy-editing) and structure (reorganization and simplification). Use with "editori… | `skills/context/editorial-review/` |
| **genai-optimization** | 📦 skills | Generative Engine Optimization (GEO) for content to be cited by AI-powered search engines. Use when: making content get cited by ChatGPT/Perplexity/Cl… | `skills/genai-optimization/` |
| **git-workflow** | 📦 skills | Git workflow patterns for AI agent development: worktrees for parallel agents, branching strategy, commit discipline, and merge workflows. Use when cr… | `skills/git-workflow/` |
| **humanizer** | 📦 skills | Remove signs of AI-generated writing from text. Use when editing or reviewing text to make it sound more natural and human-written. Based on Wikipedia… | `skills/humanizer/` |
| **llmfit-advisor** | 📦 skills | Detects the machine | `skills/llmfit-advisor/` |
| **phase-discussion** | 📦 skills | Captures implementation decisions for a phase BEFORE technical planning. Use when planning any phase with UI, API, content system, or data reorganizat… | `skills/planning/phase-discussion/` |
| **project-context-generator** | 📦 skills | Analyzes a codebase and generates project-context.md + constitution.md — the project | `skills/context/project-context-generator/` |
| **rust-pro** | 📦 skills | Rust 1.75+ expert for high-performance systems: async with Tokio, ownership, lifetimes, advanced traits, unsafe/FFI, and web services with axum. Use w… | `skills/rust-pro/` |
| **smart-model-dispatch** | 📦 skills | Claude model router. Use when: spawning subagents via Agent tool, implementing a feature with multiple mixed-complexity subtasks, optimizing API cost,… | `skills/smart-model-dispatch/` |
| **stuck-recovery** | 📦 skills | Detects agent stuck patterns (loops, repetitions, scope drift, a tool failing 3x+) and runs surgical recovery: saves state to osforge-db, identifies r… | `skills/stuck-recovery/` |
| **tlc-spec-driven** | 📦 skills | Product-driven planning with 5 phases - Discover, Specify, Design, Tasks, Implement+Validate+Measure. Creates atomic tasks with verification criteria … | `skills/tlc-spec-driven/` |

## 🧪 Testing

**17 skills**

| Skill | Origem | Descrição | Path Local |
|-------|--------|-----------|-----------|
| **agency-testing** | 📦 skills | Index of the Agency | `skills/agency/testing/` |
| **bun-development** | 📦 skills | Bun runtime patterns, bundler configuration, and Bun-specific APIs. Trigger on Bun FFI, Bun.serve, Bun.file, Bun shell, workspace configuration, Bun-s… | `skills/bun-development/` |
| **context7-docs-first** | 📦 skills | Ground all platform and library answers in current official documentation by using Context7 MCP tools before responding. TRIGGER when: user asks about… | `skills/context7-docs-first/` |
| **e2e-testing-patterns** | 📦 skills | End-to-end testing with Playwright for Next.js applications. Trigger on E2E test setup, cross-page flow testing (checkout, onboarding, multi-step form… | `skills/e2e-testing-patterns/` |
| **epic-decomposer** | 📦 skills | Decomposes specs, PRDs, or requirements into implementable epics and stories. Each story with testable ACs, tasks with file paths, and mapped dependen… | `skills/planning/epic-decomposer/` |
| **offensive-oauth** | 📦 skills | OAuth 2.0 attack checklist: authorization code interception, redirect_uri bypass, CSRF on OAuth flow, state parameter abuse, open redirector chaining,… | `skills/offensive-oauth/` |
| **offensive-reporting** | 📦 skills | Penetration test and red team report writing methodology. Covers executive summary structuring (risk-led narrative for non-technical readers), technic… | `skills/offensive-reporting/` |
| **offensive-ssrf** | 📦 skills | Server-Side Request Forgery testing checklist: SSRF discovery, blind SSRF with out-of-band, cloud metadata endpoints (AWS/GCP/Azure), SSRF filter bypa… | `skills/offensive-ssrf/` |
| **output-enforcement** | 📦 skills | OSForge enhancement layer over full-output-enforcement: beyond complete output, requires a verification gate before declaring done and TDD protection … | `skills/output-enforcement/` |
| **predictive-failure** | 📦 skills | Analyze implemented code to predict potential failure points that tests may not catch. Uses pattern matching against common production failure modes. … | `skills/predictive-failure/` |
| **skill-creator** | 📦 skills | Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from scratch, update or op… | `skills/skill-creator/` |
| **spec-builder** | 📦 skills | Collaborative facilitation of a tech spec with testable ACs. Use when: specifying a feature, defining what to build, writing a technical spec, detaili… | `skills/planning/spec-builder/` |
| **tdd-workflow** | 📦 skills | Enforces Test-Driven Development (RED-GREEN-REFACTOR) workflow. Use when implementing any feature, bugfix, or behavior change. Ensures tests are writt… | `skills/tdd-workflow/` |
| **technical-design-doc-creator** | 📦 skills | Creates comprehensive Technical Design Documents (TDD) following industry standards with mandatory sections, optional sections, and interactive gather… | `skills/technical-design-doc-creator/` |
| **testing-patterns** | 📦 skills | Unit and integration testing patterns and principles: testing pyramid, AAA pattern, mocking strategies, test organization and data. Use when: writing … | `skills/testing-patterns/` |
| **using-git-worktrees** | 📦 skills | Setup and use of git worktrees for parallel development. Use when: working on multiple features simultaneously, needing isolated branches for each par… | `skills/using-git-worktrees/` |
| **vercel-deploy** | 📦 skills | Deploy applications and websites to Vercel. Use when the user requests deployment actions like "deploy my app", "deploy and give me the link", "push t… | `skills/vercel-deploy/` |

## 🏗️ Architecture

**8 skills**

| Skill | Origem | Descrição | Path Local |
|-------|--------|-----------|-----------|
| **2d-games** | 📦 skills | 2D game principles: sprites, atlases, tilemaps, 2D physics, cameras, and genre patterns (platformer, top-down). Use when: I | `skills/game-development/2d-games/` |
| **bash-linux** | 📦 skills | Bash terminal patterns for Linux and macOS: essential commands, pipes, processes, text processing, and safe scripts. Use when: a bash script errors or… | `skills/bash-linux/` |
| **elicitation-engine** | 📦 skills | Iterative refinement of outputs (specs, PRDs, architectural decisions, any artifact) via an interactive menu of structured elicitation techniques. Use… | `skills/quality/elicitation-engine/` |
| **game-development** | 📦 skills | Game development orchestrator that teaches universal principles (game loop, patterns, performance, AI, collision) and routes to platform and specialty… | `skills/game-development/` |
| **multiplayer** | 📦 skills | Multiplayer game principles: network architecture (dedicated server, P2P, host-based), synchronization, lag compensation, anti-cheat, and matchmaking.… | `skills/game-development/multiplayer/` |
| **osforge-evolve** | 📦 skills | Use when: evolve, /evolve, osforge evolve, analyze observations, propose skills, pattern clustering, instinct, promote instinct, continuous learning, … | `skills/evolve/` |
| **powershell-windows** | 📦 skills | Critical PowerShell patterns and pitfalls on Windows: operator syntax, null checks, JSON, paths, and error handling. Use when: a PowerShell script fai… | `skills/powershell-windows/` |
| **readiness-gate** | 📦 skills | Pre-implementation quality gate. Validates that the PRD, Architecture and Epics are aligned and complete before starting the sprint loop. Use with: | `skills/quality/readiness-gate/` |

## 📦 General

**7 skills**

| Skill | Origem | Descrição | Path Local |
|-------|--------|-----------|-----------|
| **agency** | 📦 skills | General index of The Agency | `skills/agency/` |
| **agency-engineering** | 📦 skills | Index of the Agency | `skills/agency/engineering/` |
| **agency-paid-media** | 📦 skills | Index of the Agency | `skills/agency/paid-media/` |
| **agency-specialized** | 📦 skills | Index of the Agency | `skills/agency/specialized/` |
| **agency-support** | 📦 skills | Index of the Agency | `skills/agency/support/` |
| **edge-case-hunter** | 📦 skills | Exhaustive edge-case hunt via systematic enumeration of branches and boundaries, reporting in JSON only the paths without handling. Use when: asked fo… | `skills/quality/edge-case-hunter/` |
| **full-output-enforcement** | 📦 skills | Anti-truncation base rule: forbids placeholders and omissions, requires complete generation of every deliverable, and manages token-limit splits with … | `skills/full-output-enforcement/` |

## 📝 Documentation / Writing

**6 skills**

| Skill | Origem | Descrição | Path Local |
|-------|--------|-----------|-----------|
| **brandkit** | 📦 skills | Generates premium brand-kit images: brand guideline boards, logo systems, identity decks, and visual-universe presentations with clean grids, sparse t… | `skills/brandkit/` |
| **doc-sanitization** | 📦 skills | Clean up, consolidate, and organize project documentation. Removes obsolete specs, merges duplicates, enforces lifecycle rules. Trigger on phrases lik… | `skills/doc-sanitization/` |
| **docs-writer** | 📦 skills | Writes, reviews, and edits technical documentation by checking the source code and following the project | `skills/docs-writer/` |
| **minimalist-ui** | 📦 skills | Generates ultra-minimalist editorial/document-style interfaces (Notion-like) with a warm monochrome palette, editorial serifs, flat bento grids, washe… | `skills/minimalist-ui/` |
| **plan-writing** | 📦 skills | Structured work planning with breakdown into small tasks, dependencies, and verification criteria. Use when: planning a feature implementation, breaki… | `skills/plan-writing/` |
| **prd-builder** | 📦 skills | Collaborative facilitation of a Product Requirements Document. Guides the user through problem definition, users, requirements, metrics, and MVP scope… | `skills/planning/prd-builder/` |

## 🗄️ Database / Backend

**5 skills**

| Skill | Origem | Descrição | Path Local |
|-------|--------|-----------|-----------|
| **api-patterns** | 📦 skills | API design principles: style choice, response format, versioning, pagination, authentication, and rate limiting. Use when: choosing between REST, Grap… | `skills/api-patterns/` |
| **postgres-optimization** | 📦 skills | PostgreSQL and Supabase optimization best practices for queries, indexes, RLS policies, and connection management. Use when writing complex queries, c… | `skills/postgres-optimization/` |
| **prisma-expert** | 📦 skills | Advanced Prisma ORM patterns. Use when: schema changes with >3 models, migration strategies, slow queries or N+1, many-to-many or polymorphic relation… | `skills/prisma-expert/` |
| **python-patterns** | 📦 skills | Python development principles: framework selection, async vs sync, type hints, Pydantic, project structure, and background tasks. Use when: choosing b… | `skills/python-patterns/` |
| **smart-hooks** | 📦 skills | Production-grade Python hooks for Claude Code quality gates, safety rails, and developer experience. TRIGGER when: setting up hooks for a project, con… | `skills/smart-hooks/` |

## 📱 Mobile

**4 skills**

| Skill | Origem | Descrição | Path Local |
|-------|--------|-----------|-----------|
| **mcp-builder** | 📦 skills | Builds custom MCP (Model Context Protocol) servers in TypeScript or Python. Use when: creating an MCP server from scratch, exposing an internal API as… | `skills/mcp-builder/` |
| **mobile-design** | 📦 skills | Mobile-first design principles for iOS and Android apps: touch interaction, thumb zone, 60fps performance, platform conventions (HIG, Material 3), off… | `skills/mobile-design/` |
| **mobile-games** | 📦 skills | Mobile game principles: touch input, battery and thermal, App Store and Google Play requirements, monetization. Use when: I | `skills/game-development/mobile-games/` |
| **stitch-design-export** | 📦 skills | OSForge enhancement layer sobre stitch-design-taste. Gera DESIGN.md para Google Stitch com tokens de osforge.config.json + Impeccable. ACIONE com stit… | `skills/stitch-design-export/` |

## ☁️ Infrastructure / DevOps

**3 skills**

| Skill | Origem | Descrição | Path Local |
|-------|--------|-----------|-----------|
| **claude-ci-actions** | 📦 skills | Automate PR review, issue triage, and CI/CD tasks with Claude Code GitHub Actions. TRIGGER when: setting up @claude in PRs/issues, configuring automat… | `skills/claude-ci-actions/` |
| **deployment-procedures** | 📦 skills | Safe production deployment workflows with backup, post-deploy verification, and rollback for Vercel, Railway, VPS+PM2, Docker, and Kubernetes. Use whe… | `skills/deployment-procedures/` |
| **server-management** | 📦 skills | Server operations principles: process management (PM2, systemd, Docker), monitoring, logs, scaling, health checks, and troubleshooting. Use when: app … | `skills/server-management/` |

## 💼 Business / Marketing

**2 skills**

| Skill | Origem | Descrição | Path Local |
|-------|--------|-----------|-----------|
| **agency-marketing** | 📦 skills | Index of the Agency | `skills/agency/marketing/` |
| **agency-sales** | 📦 skills | Index of the Agency | `skills/agency/sales/` |

## 🎨 Design / Creative

**1 skills**

| Skill | Origem | Descrição | Path Local |
|-------|--------|-----------|-----------|
| **agency-design** | 📦 skills | Index of the Agency | `skills/agency/design/` |

---

## 🔤 Índice Alfabético Rápido

Lista compacta para busca rápida com `Ctrl+F`:


**#**
- `2d-games` — skills — `skills/game-development/2d-games/`
- `3d-games` — skills — `skills/game-development/3d-games/`

**A**
- `accessibility` — skills — `skills/accessibility/`
- `adversarial-review` — skills — `skills/quality/adversarial-review/`
- `aesthetic-boost` — skills — `skills/aesthetic-boost/`
- `aesthetic-modes` — skills — `skills/aesthetic-modes/`
- `agency` — skills — `skills/agency/`
- `agency-design` — skills — `skills/agency/design/`
- `agency-engineering` — skills — `skills/agency/engineering/`
- `agency-marketing` — skills — `skills/agency/marketing/`
- `agency-paid-media` — skills — `skills/agency/paid-media/`
- `agency-product` — skills — `skills/agency/product/`
- `agency-project-management` — skills — `skills/agency/project-management/`
- `agency-sales` — skills — `skills/agency/sales/`
- `agency-specialized` — skills — `skills/agency/specialized/`
- `agency-support` — skills — `skills/agency/support/`
- `agency-testing` — skills — `skills/agency/testing/`
- `agent-skills-search` — skills — `skills/agent-skills-search/`
- `api-patterns` — skills — `skills/api-patterns/`
- `app-builder` — skills — `skills/app-builder/`
- `arch-builder` — skills — `skills/planning/arch-builder/`
- `architecture` — skills — `skills/architecture/`
- `autorefine-skill` — skills — `skills/autorefine-skill/`

**B**
- `bash-linux` — skills — `skills/bash-linux/`
- `behavioral-modes` — skills — `skills/behavioral-modes/`
- `best-practices` — skills — `skills/best-practices/`
- `brainstorming` — skills — `skills/brainstorming/`
- `brandkit` — skills — `skills/brandkit/`
- `bun-development` — skills — `skills/bun-development/`

**C**
- `claude-api-typescript` — skills — `skills/claude-api-typescript/`
- `claude-ci-actions` — skills — `skills/claude-ci-actions/`
- `clean-code` — skills — `skills/clean-code/`
- `code-review` — skills — `skills/quality/code-review/`
- `code-review-checklist` — skills — `skills/code-review-checklist/`
- `coding-guidelines` — skills — `skills/coding-guidelines/`
- `config-critique` — skills — `skills/config-critique/`
- `context-compact` — skills — `skills/context-compact/`
- `context-distillator` — skills — `skills/context/context-distillator/`
- `context7-docs-first` — skills — `skills/context7-docs-first/`
- `core-web-vitals` — skills — `skills/core-web-vitals/`

**D**
- `database-design` — skills — `skills/database-design/`
- `db-state-sync` — skills — `skills/context/db-state-sync/`
- `deployment-procedures` — skills — `skills/deployment-procedures/`
- `design-md` — skills — `skills/design-md/`
- `design-taste-frontend` — skills — `skills/design-taste-frontend/`
- `design-taste-frontend-v1` — skills — `skills/design-taste-frontend-v1/`
- `differential-review` — skills — `skills/differential-review/`
- `dispatching-parallel-agents` — skills — `skills/dispatching-parallel-agents/`
- `doc-sanitization` — skills — `skills/doc-sanitization/`
- `doc-shard` — skills — `skills/context/doc-shard/`
- `docs-writer` — skills — `skills/docs-writer/`
- `documentation-templates` — skills — `skills/documentation-templates/`

**E**
- `e2e-testing-patterns` — skills — `skills/e2e-testing-patterns/`
- `edge-case-hunter` — skills — `skills/quality/edge-case-hunter/`
- `editorial-review` — skills — `skills/context/editorial-review/`
- `elicitation-engine` — skills — `skills/quality/elicitation-engine/`
- `epic-decomposer` — skills — `skills/planning/epic-decomposer/`

**F**
- `finishing-a-development-branch` — skills — `skills/finishing-a-development-branch/`
- `frontend-design` — skills — `skills/frontend-design/`
- `frontend-ui-system` — skills — `skills/frontend-ui-system/`
- `full-output-enforcement` — skills — `skills/full-output-enforcement/`

**G**
- `game-art` — skills — `skills/game-development/game-art/`
- `game-audio` — skills — `skills/game-development/game-audio/`
- `game-design` — skills — `skills/game-development/game-design/`
- `game-development` — skills — `skills/game-development/`
- `gdpr-data-handling` — skills — `skills/gdpr-data-handling/`
- `genai-optimization` — skills — `skills/genai-optimization/`
- `git-workflow` — skills — `skills/git-workflow/`
- `gpt-taste` — skills — `skills/gpt-taste/`

**H**
- `high-end-visual-design` — skills — `skills/high-end-visual-design/`
- `humanizer` — skills — `skills/humanizer/`

**I**
- `i18n-localization` — skills — `skills/i18n-localization/`
- `image-to-code` — skills — `skills/image-to-code/`
- `imagegen-frontend-mobile` — skills — `skills/imagegen-frontend-mobile/`
- `imagegen-frontend-web` — skills — `skills/imagegen-frontend-web/`
- `industrial-brutalist-ui` — skills — `skills/industrial-brutalist-ui/`
- `insecure-defaults` — skills — `skills/insecure-defaults/`

**L**
- `lint-and-validate` — skills — `skills/lint-and-validate/`
- `llmfit-advisor` — skills — `skills/llmfit-advisor/`

**M**
- `mcp-builder` — skills — `skills/mcp-builder/`
- `minimalist-ui` — skills — `skills/minimalist-ui/`
- `mobile-design` — skills — `skills/mobile-design/`
- `mobile-games` — skills — `skills/game-development/mobile-games/`
- `multiplayer` — skills — `skills/game-development/multiplayer/`

**N**
- `nextjs-react-expert` — skills — `skills/nextjs-react-expert/`
- `nextjs-supabase-auth` — skills — `skills/nextjs-supabase-auth/`
- `nodejs-best-practices` — skills — `skills/nodejs-best-practices/`

**O**
- `offensive-ai-security` — skills — `skills/offensive-ai-security/`
- `offensive-bug-identification` — skills — `skills/offensive-bug-identification/`
- `offensive-business-logic` — skills — `skills/offensive-business-logic/`
- `offensive-cloud` — skills — `skills/offensive-cloud/`
- `offensive-deserialization` — skills — `skills/offensive-deserialization/`
- `offensive-fast-checking` — skills — `skills/offensive-fast-checking/`
- `offensive-file-upload` — skills — `skills/offensive-file-upload/`
- `offensive-fuzzing` — skills — `skills/offensive-fuzzing/`
- `offensive-graphql` — skills — `skills/offensive-graphql/`
- `offensive-idor` — skills — `skills/offensive-idor/`
- `offensive-jwt` — skills — `skills/offensive-jwt/`
- `offensive-mobile` — skills — `skills/offensive-mobile/`
- `offensive-oauth` — skills — `skills/offensive-oauth/`
- `offensive-open-redirect` — skills — `skills/offensive-open-redirect/`
- `offensive-osint` — skills — `skills/offensive-osint/`
- `offensive-parameter-pollution` — skills — `skills/offensive-parameter-pollution/`
- `offensive-race-condition` — skills — `skills/offensive-race-condition/`
- `offensive-rce` — skills — `skills/offensive-rce/`
- `offensive-reporting` — skills — `skills/offensive-reporting/`
- `offensive-request-smuggling` — skills — `skills/offensive-request-smuggling/`
- `offensive-sqli` — skills — `skills/offensive-sqli/`
- `offensive-ssrf` — skills — `skills/offensive-ssrf/`
- `offensive-ssti` — skills — `skills/offensive-ssti/`
- `offensive-toctou` — skills — `skills/offensive-toctou/`
- `offensive-waf-bypass` — skills — `skills/offensive-waf-bypass/`
- `offensive-xss` — skills — `skills/offensive-xss/`
- `offensive-xxe` — skills — `skills/offensive-xxe/`
- `openui-genui-layout` — skills — `skills/openui-genui-layout/`
- `osforge-canvas` — skills — `skills/osforge-canvas/`
- `osforge-evolve` — skills — `skills/evolve/`
- `output-enforcement` — skills — `skills/output-enforcement/`

**P**
- `pc-games` — skills — `skills/game-development/pc-games/`
- `performance-profiling` — skills — `skills/performance-profiling/`
- `phase-discussion` — skills — `skills/planning/phase-discussion/`
- `plan-writing` — skills — `skills/plan-writing/`
- `postgres-optimization` — skills — `skills/postgres-optimization/`
- `powershell-windows` — skills — `skills/powershell-windows/`
- `prd-builder` — skills — `skills/planning/prd-builder/`
- `predictive-failure` — skills — `skills/predictive-failure/`
- `prisma-expert` — skills — `skills/prisma-expert/`
- `project-context-generator` — skills — `skills/context/project-context-generator/`
- `python-patterns` — skills — `skills/python-patterns/`

**R**
- `react-performance` — skills — `skills/react-performance/`
- `readiness-gate` — skills — `skills/quality/readiness-gate/`
- `receiving-code-review` — skills — `skills/receiving-code-review/`
- `red-team-tactics` — skills — `skills/red-team-tactics/`
- `redesign-audit` — skills — `skills/redesign-audit/`
- `redesign-existing-projects` — skills — `skills/redesign-existing-projects/`
- `requirements-clarify` — skills — `skills/planning/requirements-clarify/`
- `rust-pro` — skills — `skills/rust-pro/`

**S**
- `security-best-practices` — skills — `skills/security-best-practices/`
- `security-threat-model` — skills — `skills/security-threat-model/`
- `seo` — skills — `skills/seo/`
- `seo-fundamentals` — skills — `skills/seo-fundamentals/`
- `server-management` — skills — `skills/server-management/`
- `skill-creator` — skills — `skills/skill-creator/`
- `smart-hooks` — skills — `skills/smart-hooks/`
- `smart-model-dispatch` — skills — `skills/smart-model-dispatch/`
- `spec-builder` — skills — `skills/planning/spec-builder/`
- `stitch-design-export` — skills — `skills/stitch-design-export/`
- `stitch-design-taste` — skills — `skills/stitch-design-taste/`
- `story-executor` — skills — `skills/planning/story-executor/`
- `stripe-integration` — skills — `skills/stripe-integration/`
- `stuck-recovery` — skills — `skills/stuck-recovery/`
- `systematic-debugging` — skills — `skills/systematic-debugging/`

**T**
- `tailwind-patterns` — skills — `skills/tailwind-patterns/`
- `taste-design-dials` — skills — `skills/taste-design-dials/`
- `tdd-workflow` — skills — `skills/tdd-workflow/`
- `technical-design-doc-creator` — skills — `skills/technical-design-doc-creator/`
- `testing-patterns` — skills — `skills/testing-patterns/`
- `tlc-spec-driven` — skills — `skills/tlc-spec-driven/`
- `tool-safety-classifier` — skills — `skills/tool-safety-classifier/`

**U**
- `ui-audit` — skills — `skills/quality/ui-audit/`
- `ui-design-intelligence` — skills — `skills/ui-design-intelligence/`
- `using-git-worktrees` — skills — `skills/using-git-worktrees/`

**V**
- `vercel-deploy` — skills — `skills/vercel-deploy/`
- `verification-before-completion` — skills — `skills/verification-before-completion/`
- `visual-planner` — skills — `skills/visual-planner/`
- `vr-ar` — skills — `skills/game-development/vr-ar/`
- `vulnerability-scanner` — skills — `skills/vulnerability-scanner/`

**W**
- `web-design-guidelines` — skills — `skills/web-design-guidelines/`
- `web-games` — skills — `skills/game-development/web-games/`
- `webapp-testing` — skills — `skills/webapp-testing/`

---

*Índice gerado automaticamente por Claude Opus 4.6 a partir de 770 SKILL.md files.*