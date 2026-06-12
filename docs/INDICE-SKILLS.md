# 📚 Índice Completo de Agent Skills

> **Total:** 966 skills indexadas de 12 repositórios
> **Pasta local:** `~/Development/osforge/sources/` (fontes) e `~/Development/osforge/skills/` (curadas)
>
> 💡 **Dica de busca:** Use `Ctrl+F` / `Cmd+F` para pesquisar por palavra-chave.
> Para instalar uma skill: `cp -R ~/Development/osforge/<path_local> .claude/skills/`

---

## 📊 Estatísticas

### Por Categoria

| Categoria | Qtd | % |
|-----------|-----|---|
| 🔒 Security | 205 | 21.2% |
| 🤖 AI / ML / Agents | 142 | 14.7% |
| 🔄 Workflow / Process | 135 | 14.0% |
| ⚛️ React / Frontend | 96 | 9.9% |
| 🧪 Testing | 84 | 8.7% |
| 🏗️ Architecture | 63 | 6.5% |
| 📝 Documentation / Writing | 59 | 6.1% |
| ☁️ Infrastructure / DevOps | 48 | 5.0% |
| 📱 Mobile | 39 | 4.0% |
| 🗄️ Database / Backend | 38 | 3.9% |
| 📦 General | 38 | 3.9% |
| 🎨 Design / Creative | 12 | 1.2% |
| 💼 Business / Marketing | 6 | 0.6% |
| 🐍 Languages / Frameworks | 1 | 0.1% |
| **TOTAL** | **966** | **100%** |

### Por Origem

| Origem | Repo | Qtd |
|--------|------|-----|
| Antigravity (634+) | [Link](https://github.com/sickn33/antigravity-awesome-skills) | 634 |
| skills | — | 169 |
| Trail of Bits | [Link](https://github.com/trailofbits/skills) | 51 |
| Claude-Red (Offensive Security) | [Link](https://github.com/SnailSploit/Claude-Red) | 27 |
| Context Engineering | [Link](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering) | 18 |
| Anthropic (Oficial) | [Link](https://github.com/anthropics/skills) | 17 |
| Superpowers (obra) | [Link](https://github.com/obra/superpowers) | 14 |
| Sentry | [Link](https://github.com/getsentry/skills) | 13 |
| Expo | [Link](https://github.com/expo/skills) | 9 |
| Cloudflare | [Link](https://github.com/cloudflare/skills) | 8 |
| Vercel Labs | [Link](https://github.com/vercel-labs/agent-skills) | 5 |
| Supabase | [Link](https://github.com/supabase/agent-skills) | 1 |

---

## 🗂️ Sumário por Categoria

- [🔒 Security (205)](#)
- [🤖 AI / ML / Agents (142)](#)
- [🔄 Workflow / Process (135)](#)
- [⚛️ React / Frontend (96)](#)
- [🧪 Testing (84)](#)
- [🏗️ Architecture (63)](#)
- [📝 Documentation / Writing (59)](#)
- [☁️ Infrastructure / DevOps (48)](#)
- [📱 Mobile (39)](#)
- [🗄️ Database / Backend (38)](#)
- [📦 General (38)](#)
- [🎨 Design / Creative (12)](#)
- [💼 Business / Marketing (6)](#)
- [🐍 Languages / Frameworks (1)](#)

---

## 🔒 Security

**205 skills**

| Skill | Origem | Descrição | Path Local |
|-------|--------|-----------|-----------|
| **web-design-guidelines** | 🟢 Vercel Labs | Review UI code for Web Interface Guidelines compliance. Use when asked to "review my UI", "check accessibility", "audit design", "review UX", or "chec… | `sources/04-vercel/web-design-guidelines/` |
| **address-sanitizer** | 🔒 Trail of Bits | AddressSanitizer detects memory errors during fuzzing. Use when fuzzing C/C++ code to find buffer overflows and use-after-free bugs. | `sources/07-trailofbits/testing-handbook-skills/skills/address-sanitizer/` |
| **aflpp** | 🔒 Trail of Bits | AFL++ is a fork of AFL with better fuzzing performance and advanced features. Use for multi-core fuzzing of C/C++ projects. | `sources/07-trailofbits/testing-handbook-skills/skills/aflpp/` |
| **algorand-vulnerability-scanner** | 🔒 Trail of Bits | Scans Algorand smart contracts for 11 common vulnerabilities including rekeying attacks, unchecked transaction fees, missing field validations, and ac… | `sources/07-trailofbits/building-secure-contracts/skills/algorand-vulnerability-scanner/` |
| **atheris** | 🔒 Trail of Bits | Atheris is a coverage-guided Python fuzzer based on libFuzzer. Use for fuzzing pure Python code and Python C extensions. | `sources/07-trailofbits/testing-handbook-skills/skills/atheris/` |
| **audit-context-building** | 🔒 Trail of Bits | Enables ultra-granular, line-by-line code analysis to build deep architectural context before vulnerability or bug finding. | `sources/07-trailofbits/audit-context-building/skills/audit-context-building/` |
| **audit-prep-assistant** | 🔒 Trail of Bits | Prepares codebases for security review using Trail of Bits' checklist. Helps set review goals, runs static analysis tools, increases test coverage, re… | `sources/07-trailofbits/building-secure-contracts/skills/audit-prep-assistant/` |
| **burpsuite-project-parser** | 🔒 Trail of Bits | Searches and explores Burp Suite project files (.burp) from the command line. Use when searching response headers or bodies with regex patterns, extra… | `sources/07-trailofbits/burpsuite-project-parser/skills/` |
| **cairo-vulnerability-scanner** | 🔒 Trail of Bits | Scans Cairo/StarkNet smart contracts for 6 critical vulnerabilities including felt252 arithmetic overflow, L1-L2 messaging issues, address conversion … | `sources/07-trailofbits/building-secure-contracts/skills/cairo-vulnerability-scanner/` |
| **cargo-fuzz** | 🔒 Trail of Bits | cargo-fuzz is the de facto fuzzing tool for Rust projects using Cargo. Use for fuzzing Rust code with libFuzzer backend. | `sources/07-trailofbits/testing-handbook-skills/skills/cargo-fuzz/` |
| **code-maturity-assessor** | 🔒 Trail of Bits | Systematic code maturity assessment using Trail of Bits' 9-category framework. Analyzes codebase for arithmetic safety, auditing practices, access con… | `sources/07-trailofbits/building-secure-contracts/skills/code-maturity-assessor/` |
| **codeql** | 🔒 Trail of Bits | Run CodeQL static analysis for security vulnerability detection, taint tracking, and data flow analysis. Use when asked to analyze code with CodeQL, c… | `sources/07-trailofbits/static-analysis/skills/codeql/` |
| **codeql** | 🔒 Trail of Bits | CodeQL is a static analysis framework that queries code as a database. Use when you need interprocedural analysis or complex data flow tracking. | `sources/07-trailofbits/testing-handbook-skills/skills/codeql/` |
| **constant-time-analysis** | 🔒 Trail of Bits | Detects timing side-channel vulnerabilities in cryptographic code. Use when implementing or reviewing crypto code, encountering division on secrets, s… | `sources/07-trailofbits/constant-time-analysis/skills/constant-time-analysis/` |
| **constant-time-testing** | 🔒 Trail of Bits | Constant-time testing detects timing side channels in cryptographic code. Use when auditing crypto implementations for timing vulnerabilities. | `sources/07-trailofbits/testing-handbook-skills/skills/constant-time-testing/` |
| **cosmos-vulnerability-scanner** | 🔒 Trail of Bits | Scans Cosmos SDK blockchains for 9 consensus-critical vulnerabilities including non-determinism, incorrect signers, ABCI panics, and rounding errors. … | `sources/07-trailofbits/building-secure-contracts/skills/cosmos-vulnerability-scanner/` |
| **coverage-analysis** | 🔒 Trail of Bits | Coverage analysis measures code exercised during fuzzing. Use when assessing harness effectiveness or identifying fuzzing blockers. | `sources/07-trailofbits/testing-handbook-skills/skills/coverage-analysis/` |
| **differential-review** | 🔒 Trail of Bits | Performs security-focused differential review of code changes (PRs, commits, diffs). Adapts analysis depth to codebase size, uses git history for cont… | `sources/07-trailofbits/differential-review/skills/differential-review/` |
| **entry-point-analyzer** | 🔒 Trail of Bits | Analyzes smart contract codebases to identify state-changing entry points for security auditing. Detects externally callable functions that modify sta… | `sources/07-trailofbits/entry-point-analyzer/skills/entry-point-analyzer/` |
| **firebase-apk-scanner** | 🔒 Trail of Bits | Scans Android APKs for Firebase security misconfigurations including open databases, storage buckets, authentication issues, and exposed cloud functio… | `sources/07-trailofbits/firebase-apk-scanner/skills/firebase-apk-scanner/` |
| **fix-review** | 🔒 Trail of Bits | Verifies that git commits address security audit findings without introducing bugs. This skill should be used when the user asks to "verify these comm… | `sources/07-trailofbits/fix-review/skills/fix-review/` |
| **fuzzing-dictionary** | 🔒 Trail of Bits | Fuzzing dictionaries guide fuzzers with domain-specific tokens. Use when fuzzing parsers, protocols, or format-specific code. | `sources/07-trailofbits/testing-handbook-skills/skills/fuzzing-dictionary/` |
| **fuzzing-obstacles** | 🔒 Trail of Bits | Techniques for patching code to overcome fuzzing obstacles. Use when checksums, global state, or other barriers block fuzzer progress. | `sources/07-trailofbits/testing-handbook-skills/skills/fuzzing-obstacles/` |
| **guidelines-advisor** | 🔒 Trail of Bits | Smart contract development advisor based on Trail of Bits' best practices. Analyzes codebase to generate documentation/specifications, review architec… | `sources/07-trailofbits/building-secure-contracts/skills/guidelines-advisor/` |
| **harness-writing** | 🔒 Trail of Bits | Techniques for writing effective fuzzing harnesses across languages. Use when creating new fuzz targets or improving existing harness code. | `sources/07-trailofbits/testing-handbook-skills/skills/harness-writing/` |
| **insecure-defaults** | 🔒 Trail of Bits | Detects fail-open insecure defaults (hardcoded secrets, weak auth, permissive security) that allow apps to run insecurely in production. Use when audi… | `sources/07-trailofbits/insecure-defaults/skills/insecure-defaults/` |
| **libafl** | 🔒 Trail of Bits | LibAFL is a modular fuzzing library for building custom fuzzers. Use for advanced fuzzing needs, custom mutators, or non-standard fuzzing targets. | `sources/07-trailofbits/testing-handbook-skills/skills/libafl/` |
| **libfuzzer** | 🔒 Trail of Bits | Coverage-guided fuzzer built into LLVM for C/C++ projects. Use for fuzzing C/C++ code that can be compiled with Clang. | `sources/07-trailofbits/testing-handbook-skills/skills/libfuzzer/` |
| **ossfuzz** | 🔒 Trail of Bits | OSS-Fuzz provides free continuous fuzzing for open source projects. Use when setting up continuous fuzzing infrastructure or enrolling projects. | `sources/07-trailofbits/testing-handbook-skills/skills/ossfuzz/` |
| **ruzzy** | 🔒 Trail of Bits | Ruzzy is a coverage-guided Ruby fuzzer by Trail of Bits. Use for fuzzing pure Ruby code and Ruby C extensions. | `sources/07-trailofbits/testing-handbook-skills/skills/ruzzy/` |
| **sarif-parsing** | 🔒 Trail of Bits | Parse, analyze, and process SARIF (Static Analysis Results Interchange Format) files. Use when reading security scan results, aggregating findings fro… | `sources/07-trailofbits/static-analysis/skills/sarif-parsing/` |
| **secure-workflow-guide** | 🔒 Trail of Bits | Guides through Trail of Bits' 5-step secure development workflow. Runs Slither scans, checks special features (upgradeability/ERC conformance/token in… | `sources/07-trailofbits/building-secure-contracts/skills/secure-workflow-guide/` |
| **semgrep** | 🔒 Trail of Bits | Run Semgrep static analysis for fast security scanning and pattern matching. Use when asked to scan code with Semgrep, write custom YAML rules, find v… | `sources/07-trailofbits/static-analysis/skills/semgrep/` |
| **semgrep** | 🔒 Trail of Bits | Semgrep is a fast static analysis tool for finding bugs and enforcing code standards. Use when scanning code for security issues or integrating into C… | `sources/07-trailofbits/testing-handbook-skills/skills/semgrep/` |
| **semgrep-rule-creator** | 🔒 Trail of Bits | Creates custom Semgrep rules for detecting security vulnerabilities, bug patterns, and code patterns. Use when writing Semgrep rules or building custo… | `sources/07-trailofbits/semgrep-rule-creator/skills/semgrep-rule-creator/` |
| **semgrep-rule-variant-creator** | 🔒 Trail of Bits | Creates language variants of existing Semgrep rules. Use when porting a Semgrep rule to specified target languages. Takes an existing rule and target … | `sources/07-trailofbits/semgrep-rule-variant-creator/skills/semgrep-rule-variant-creator/` |
| **sharp-edges** | 🔒 Trail of Bits | Identifies error-prone APIs, dangerous configurations, and footgun designs that enable security mistakes. Use when reviewing API designs, configuratio… | `sources/07-trailofbits/sharp-edges/skills/sharp-edges/` |
| **solana-vulnerability-scanner** | 🔒 Trail of Bits | Scans Solana programs for 6 critical vulnerabilities including arbitrary CPI, improper PDA validation, missing signer/ownership checks, and sysvar spo… | `sources/07-trailofbits/building-secure-contracts/skills/solana-vulnerability-scanner/` |
| **spec-to-code-compliance** | 🔒 Trail of Bits | Verifies code implements exactly what documentation specifies for blockchain audits. Use when comparing code against whitepapers, finding gaps between… | `sources/07-trailofbits/spec-to-code-compliance/skills/spec-to-code-compliance/` |
| **substrate-vulnerability-scanner** | 🔒 Trail of Bits | Scans Substrate/Polkadot pallets for 7 critical vulnerabilities including arithmetic overflow, panic DoS, incorrect weights, and bad origin checks. Us… | `sources/07-trailofbits/building-secure-contracts/skills/substrate-vulnerability-scanner/` |
| **testing-handbook-generator** | 🔒 Trail of Bits | Meta-skill that analyzes the Trail of Bits Testing Handbook (appsec.guide) and generates Claude Code skills for security testing tools and techniques.… | `sources/07-trailofbits/testing-handbook-skills/skills/testing-handbook-generator/` |
| **token-integration-analyzer** | 🔒 Trail of Bits | Token integration and implementation analyzer based on Trail of Bits' token integration checklist. Analyzes token implementations for ERC20/ERC721 con… | `sources/07-trailofbits/building-secure-contracts/skills/token-integration-analyzer/` |
| **ton-vulnerability-scanner** | 🔒 Trail of Bits | Scans TON (The Open Network) smart contracts for 3 critical vulnerabilities including integer-as-boolean misuse, fake Jetton contracts, and forward TO… | `sources/07-trailofbits/building-secure-contracts/skills/ton-vulnerability-scanner/` |
| **variant-analysis** | 🔒 Trail of Bits | Find similar vulnerabilities and bugs across codebases using pattern-based analysis. Use when hunting bug variants, building CodeQL/Semgrep queries, a… | `sources/07-trailofbits/variant-analysis/skills/variant-analysis/` |
| **yara-rule-authoring** | 🔒 Trail of Bits | Guides authoring of high-quality YARA-X detection rules for malware identification. Use when writing, reviewing, or optimizing YARA rules. Covers nami… | `sources/07-trailofbits/yara-authoring/skills/yara-rule-authoring/` |
| **cloudflare** | ☁️ Cloudflare | Comprehensive Cloudflare platform skill covering Workers, Pages, storage (KV, D1, R2), AI (Workers AI, Vectorize, Agents SDK), networking (Tunnel, Spe… | `sources/10-cloudflare/cloudflare/` |
| **durable-objects** | ☁️ Cloudflare | Create and review Cloudflare Durable Objects. Use when building stateful coordination (chat rooms, multiplayer games, booking systems), implementing R… | `sources/10-cloudflare/durable-objects/` |
| **web-perf** | ☁️ Cloudflare | Analyzes web performance using Chrome DevTools MCP. Measures Core Web Vitals (FCP, LCP, TBT, CLS, Speed Index), identifies render-blocking resources, … | `sources/10-cloudflare/web-perf/` |
| **claude-settings-audit** | 🔴 Sentry | Analyze a repository to generate recommended Claude Code settings.json permissions. Use when setting up a new project, auditing existing settings, or … | `sources/11-sentry/claude-settings-audit/` |
| **code-review** | 🔴 Sentry | Perform code reviews following Sentry engineering practices. Use when reviewing pull requests, examining code changes, or providing feedback on code q… | `sources/11-sentry/code-review/` |
| **django-access-review** | 🔴 Sentry | Django access control and IDOR security review. Use when reviewing Django views, DRF viewsets, ORM queries, or any Python/Django code handling user au… | `sources/11-sentry/django-access-review/` |
| **django-perf-review** | 🔴 Sentry | Django performance code review. Use when asked to "review Django performance", "find N+1 queries", "optimize Django", "check queryset performance", "d… | `sources/11-sentry/django-perf-review/` |
| **find-bugs** | 🔴 Sentry | Find bugs, security vulnerabilities, and code quality issues in local branch changes. Use when asked to review changes, find bugs, security review, or… | `sources/11-sentry/find-bugs/` |
| **security-review** | 🔴 Sentry | Security code review for vulnerabilities. Use when asked to "security review", "find vulnerabilities", "check for security issues", "audit security", … | `sources/11-sentry/security-review/` |
| **accessibility-compliance-accessibility-audit** | 🌌 Antigravity (634+) | You are an accessibility expert specializing in WCAG compliance, inclusive design, and assistive technology compatibility. Conduct audits, identify ba… | `sources/06-antigravity/accessibility-compliance-accessibility-audit/` |
| **Active Directory Attacks** | 🌌 Antigravity (634+) | This skill should be used when the user asks to "attack Active Directory", "exploit AD", "Kerberoasting", "DCSync", "pass-the-hash", "BloodHound enume… | `sources/06-antigravity/active-directory-attacks/` |
| **analytics-tracking** | 🌌 Antigravity (634+) | Design, audit, and improve analytics tracking systems that produce reliable, decision-ready data. Use when the user wants to set up, fix, or evaluate … | `sources/06-antigravity/analytics-tracking/` |
| **angular-migration** | 🌌 Antigravity (634+) | Migrate from AngularJS to Angular using hybrid mode, incremental component rewriting, and dependency injection updates. Use when upgrading AngularJS a… | `sources/06-antigravity/angular-migration/` |
| **API Fuzzing for Bug Bounty** | 🌌 Antigravity (634+) | This skill should be used when the user asks to "test API security", "fuzz APIs", "find IDOR vulnerabilities", "test REST API", "test GraphQL", "API p… | `sources/06-antigravity/api-fuzzing-bug-bounty/` |
| **api-security-best-practices** | 🌌 Antigravity (634+) | Implement secure API design patterns including authentication, authorization, input validation, rate limiting, and protection against common API vulne… | `sources/06-antigravity/api-security-best-practices/` |
| **attack-tree-construction** | 🌌 Antigravity (634+) | Build comprehensive attack trees to visualize threat paths. Use when mapping attack scenarios, identifying defense gaps, or communicating security ris… | `sources/06-antigravity/attack-tree-construction/` |
| **auth-implementation-patterns** | 🌌 Antigravity (634+) | Master authentication and authorization patterns including JWT, OAuth2, session management, and RBAC to build secure, scalable access control systems.… | `sources/06-antigravity/auth-implementation-patterns/` |
| **AWS Penetration Testing** | 🌌 Antigravity (634+) | This skill should be used when the user asks to "pentest AWS", "test AWS security", "enumerate IAM", "exploit cloud infrastructure", "AWS privilege es… | `sources/06-antigravity/aws-penetration-testing/` |
| **backend-dev-guidelines** | 🌌 Antigravity (634+) | Opinionated backend development standards for Node.js + Express + TypeScript microservices. Covers layered architecture, BaseController pattern, depen… | `sources/06-antigravity/backend-dev-guidelines/` |
| **backend-security-coder** | 🌌 Antigravity (634+) | Expert in secure backend coding practices specializing in input | `sources/06-antigravity/backend-security-coder/` |
| **Broken Authentication Testing** | 🌌 Antigravity (634+) | This skill should be used when the user asks to "test for broken authentication vulnerabilities", "assess session management security", "perform crede… | `sources/06-antigravity/broken-authentication/` |
| **Burp Suite Web Application Testing** | 🌌 Antigravity (634+) | This skill should be used when the user asks to "intercept HTTP traffic", "modify web requests", "use Burp Suite for testing", "perform web vulnerabil… | `sources/06-antigravity/burp-suite-testing/` |
| **cicd-automation-workflow-automate** | 🌌 Antigravity (634+) | You are a workflow automation expert specializing in creating efficient CI/CD pipelines, GitHub Actions workflows, and automated development processes… | `sources/06-antigravity/cicd-automation-workflow-automate/` |
| **Cloud Penetration Testing** | 🌌 Antigravity (634+) | This skill should be used when the user asks to "perform cloud penetration testing", "assess Azure or AWS or GCP security", "enumerate cloud resources… | `sources/06-antigravity/cloud-penetration-testing/` |
| **code-review-checklist** | 🌌 Antigravity (634+) | Comprehensive checklist for conducting thorough code reviews covering functionality, security, performance, and maintainability | `sources/06-antigravity/code-review-checklist/` |
| **codebase-cleanup-deps-audit** | 🌌 Antigravity (634+) | You are a dependency security expert specializing in vulnerability scanning, license compliance, and supply chain security. Analyze project dependenci… | `sources/06-antigravity/codebase-cleanup-deps-audit/` |
| **Cross-Site Scripting and HTML Injection Testing** | 🌌 Antigravity (634+) | This skill should be used when the user asks to "test for XSS vulnerabilities", "perform cross-site scripting attacks", "identify HTML injection flaws… | `sources/06-antigravity/xss-html-injection/` |
| **dependency-management-deps-audit** | 🌌 Antigravity (634+) | You are a dependency security expert specializing in vulnerability scanning, license compliance, and supply chain security. Analyze project dependenci… | `sources/06-antigravity/dependency-management-deps-audit/` |
| **deployment-pipeline-design** | 🌌 Antigravity (634+) | Design multi-stage CI/CD pipelines with approval gates, security checks, and deployment orchestration. Use when architecting deployment workflows, set… | `sources/06-antigravity/deployment-pipeline-design/` |
| **docker-expert** | 🌌 Antigravity (634+) | Docker containerization expert with deep knowledge of multi-stage builds, image optimization, container security, Docker Compose orchestration, and pr… | `sources/06-antigravity/docker-expert/` |
| **dotnet-backend-patterns** | 🌌 Antigravity (634+) | Master C#/.NET backend development patterns for building robust APIs, MCP servers, and enterprise applications. Covers async/await, dependency injecti… | `sources/06-antigravity/dotnet-backend-patterns/` |
| **Ethical Hacking Methodology** | 🌌 Antigravity (634+) | This skill should be used when the user asks to "learn ethical hacking", "understand penetration testing lifecycle", "perform reconnaissance", "conduc… | `sources/06-antigravity/ethical-hacking-methodology/` |
| **event-sourcing-architect** | 🌌 Antigravity (634+) | Expert in event sourcing, CQRS, and event-driven architecture patterns. Masters event store design, projection building, saga orchestration, and event… | `sources/06-antigravity/event-sourcing-architect/` |
| **fastapi-templates** | 🌌 Antigravity (634+) | Create production-ready FastAPI projects with async patterns, dependency injection, and comprehensive error handling. Use when building new FastAPI ap… | `sources/06-antigravity/fastapi-templates/` |
| **ffuf-claude-skill** | 🌌 Antigravity (634+) | Web fuzzing with ffuf | `sources/06-antigravity/ffuf-claude-skill/` |
| **File Path Traversal Testing** | 🌌 Antigravity (634+) | This skill should be used when the user asks to "test for directory traversal", "exploit path traversal vulnerabilities", "read arbitrary files throug… | `sources/06-antigravity/file-path-traversal/` |
| **find-bugs** | 🌌 Antigravity (634+) | Find bugs, security vulnerabilities, and code quality issues in local branch changes. Use when asked to review changes, find bugs, security review, or… | `sources/06-antigravity/find-bugs/` |
| **firebase** | 🌌 Antigravity (634+) | Firebase gives you a complete backend in minutes - auth, database, storage, functions, hosting. But the ease of setup hides real complexity. Security … | `sources/06-antigravity/firebase/` |
| **fix-review** | 🌌 Antigravity (634+) | Verify fix commits address audit findings without new bugs | `sources/06-antigravity/fix-review/` |
| **frontend-mobile-security-xss-scan** | 🌌 Antigravity (634+) | You are a frontend security specialist focusing on Cross-Site Scripting (XSS) vulnerability detection and prevention. Analyze React, Vue, Angular, and… | `sources/06-antigravity/frontend-mobile-security-xss-scan/` |
| **frontend-security-coder** | 🌌 Antigravity (634+) | Expert in secure frontend coding practices specializing in XSS | `sources/06-antigravity/frontend-security-coder/` |
| **HTML Injection Testing** | 🌌 Antigravity (634+) | This skill should be used when the user asks to "test for HTML injection", "inject HTML into web pages", "perform HTML injection attacks", "deface web… | `sources/06-antigravity/html-injection-testing/` |
| **IDOR Vulnerability Testing** | 🌌 Antigravity (634+) | This skill should be used when the user asks to "test for insecure direct object references," "find IDOR vulnerabilities," "exploit broken access cont… | `sources/06-antigravity/idor-testing/` |
| **k8s-manifest-generator** | 🌌 Antigravity (634+) | Create production-ready Kubernetes manifests for Deployments, Services, ConfigMaps, and Secrets following best practices and security standards. Use w… | `sources/06-antigravity/k8s-manifest-generator/` |
| **k8s-security-policies** | 🌌 Antigravity (634+) | Implement Kubernetes security policies including NetworkPolicy, PodSecurityPolicy, and RBAC for production-grade security. Use when securing Kubernete… | `sources/06-antigravity/k8s-security-policies/` |
| **linkerd-patterns** | 🌌 Antigravity (634+) | Implement Linkerd service mesh patterns for lightweight, security-focused service mesh deployments. Use when setting up Linkerd, configuring traffic p… | `sources/06-antigravity/linkerd-patterns/` |
| **Linux Privilege Escalation** | 🌌 Antigravity (634+) | This skill should be used when the user asks to "escalate privileges on Linux", "find privesc vectors on Linux systems", "exploit sudo misconfiguratio… | `sources/06-antigravity/linux-privilege-escalation/` |
| **loki-mode** | 🌌 Antigravity (634+) | Multi-agent autonomous startup system for Claude Code. Triggers on "Loki Mode". Orchestrates 100+ specialized agents across engineering, QA, DevOps, s… | `sources/06-antigravity/loki-mode/` |
| **malware-analyst** | 🌌 Antigravity (634+) | Expert malware analyst specializing in defensive malware research, | `sources/06-antigravity/malware-analyst/` |
| **memory-forensics** | 🌌 Antigravity (634+) | Master memory forensics techniques including memory acquisition, process analysis, and artifact extraction using Volatility and related tools. Use whe… | `sources/06-antigravity/memory-forensics/` |
| **Metasploit Framework** | 🌌 Antigravity (634+) | This skill should be used when the user asks to "use Metasploit for penetration testing", "exploit vulnerabilities with msfconsole", "create payloads … | `sources/06-antigravity/metasploit-framework/` |
| **mobile-security-coder** | 🌌 Antigravity (634+) | Expert in secure mobile coding practices specializing in input | `sources/06-antigravity/mobile-security-coder/` |
| **nestjs-expert** | 🌌 Antigravity (634+) | Nest.js framework expert specializing in module architecture, dependency injection, middleware, guards, interceptors, testing with Jest/Supertest, Typ… | `sources/06-antigravity/nestjs-expert/` |
| **nodejs-best-practices** | 🌌 Antigravity (634+) | Node.js development principles and decision-making. Framework selection, async patterns, security, and architecture. Teaches thinking, not copying. | `sources/06-antigravity/nodejs-best-practices/` |
| **pci-compliance** | 🌌 Antigravity (634+) | Implement PCI DSS compliance requirements for secure handling of payment card data and payment systems. Use when securing payment processing, achievin… | `sources/06-antigravity/pci-compliance/` |
| **Pentest Checklist** | 🌌 Antigravity (634+) | This skill should be used when the user asks to "plan a penetration test", "create a security assessment checklist", "prepare for penetration testing"… | `sources/06-antigravity/pentest-checklist/` |
| **Pentest Commands** | 🌌 Antigravity (634+) | This skill should be used when the user asks to "run pentest commands", "scan with nmap", "use metasploit exploits", "crack passwords with hydra or jo… | `sources/06-antigravity/pentest-commands/` |
| **Privilege Escalation Methods** | 🌌 Antigravity (634+) | This skill should be used when the user asks to "escalate privileges", "get root access", "become administrator", "privesc techniques", "abuse sudo", … | `sources/06-antigravity/privilege-escalation-methods/` |
| **production-code-audit** | 🌌 Antigravity (634+) | Autonomously deep-scan entire codebase line-by-line, understand architecture and patterns, then systematically transform it to production-grade, corpo… | `sources/06-antigravity/production-code-audit/` |
| **Red Team Tools and Methodology** | 🌌 Antigravity (634+) | This skill should be used when the user asks to "follow red team methodology", "perform bug bounty hunting", "automate reconnaissance", "hunt for XSS … | `sources/06-antigravity/red-team-tools/` |
| **sast-configuration** | 🌌 Antigravity (634+) | Configure Static Application Security Testing (SAST) tools for automated vulnerability detection in application code. Use when setting up security sca… | `sources/06-antigravity/sast-configuration/` |
| **schema-markup** | 🌌 Antigravity (634+) | Design, validate, and optimize schema.org structured data for eligibility, correctness, and measurable SEO impact. Use when the user wants to add, fix… | `sources/06-antigravity/schema-markup/` |
| **Security Scanning Tools** | 🌌 Antigravity (634+) | This skill should be used when the user asks to "perform vulnerability scanning", "scan networks for open ports", "assess web application security", "… | `sources/06-antigravity/scanning-tools/` |
| **security-auditor** | 🌌 Antigravity (634+) | Expert security auditor specializing in DevSecOps, comprehensive | `sources/06-antigravity/security-auditor/` |
| **security-bluebook-builder** | 🌌 Antigravity (634+) | Build security Blue Books for sensitive apps | `sources/06-antigravity/security-bluebook-builder/` |
| **security-compliance-compliance-check** | 🌌 Antigravity (634+) | You are a compliance expert specializing in regulatory requirements for software systems including GDPR, HIPAA, SOC2, PCI-DSS, and other industry stan… | `sources/06-antigravity/security-compliance-compliance-check/` |
| **security-requirement-extraction** | 🌌 Antigravity (634+) | Derive security requirements from threat models and business context. Use when translating threats into actionable requirements, creating security use… | `sources/06-antigravity/security-requirement-extraction/` |
| **security-review** | 🌌 Antigravity (634+) | Use this skill when adding authentication, handling user input, working with secrets, creating API endpoints, or implementing payment/sensitive featur… | `sources/06-antigravity/cc-skill-security-review/` |
| **security-scanning-security-dependencies** | 🌌 Antigravity (634+) | You are a security expert specializing in dependency vulnerability analysis, SBOM generation, and supply chain security. Scan project dependencies acr… | `sources/06-antigravity/security-scanning-security-dependencies/` |
| **security-scanning-security-hardening** | 🌌 Antigravity (634+) | Coordinate multi-layer security scanning and hardening across application, infrastructure, and compliance controls. | `sources/06-antigravity/security-scanning-security-hardening/` |
| **security-scanning-security-sast** | 🌌 Antigravity (634+) | Static Application Security Testing (SAST) for code vulnerability | `sources/06-antigravity/security-scanning-security-sast/` |
| **seo-audit** | 🌌 Antigravity (634+) | Diagnose and audit SEO issues affecting crawlability, indexation, rankings, and organic performance. Use when the user asks for an SEO audit, technica… | `sources/06-antigravity/seo-audit/` |
| **seo-content-auditor** | 🌌 Antigravity (634+) | Analyzes provided content for quality, E-E-A-T signals, and SEO | `sources/06-antigravity/seo-content-auditor/` |
| **service-mesh-expert** | 🌌 Antigravity (634+) | Expert service mesh architect specializing in Istio, Linkerd, and cloud-native networking patterns. Masters traffic management, security policies, obs… | `sources/06-antigravity/service-mesh-expert/` |
| **Shodan Reconnaissance and Pentesting** | 🌌 Antigravity (634+) | This skill should be used when the user asks to "search for exposed devices on the internet," "perform Shodan reconnaissance," "find vulnerable servic… | `sources/06-antigravity/shodan-reconnaissance/` |
| **SMTP Penetration Testing** | 🌌 Antigravity (634+) | This skill should be used when the user asks to "perform SMTP penetration testing", "enumerate email users", "test for open mail relays", "grab SMTP b… | `sources/06-antigravity/smtp-penetration-testing/` |
| **solidity-security** | 🌌 Antigravity (634+) | Master smart contract security best practices to prevent common vulnerabilities and implement secure Solidity patterns. Use when writing smart contrac… | `sources/06-antigravity/solidity-security/` |
| **SQL Injection Testing** | 🌌 Antigravity (634+) | This skill should be used when the user asks to "test for SQL injection vulnerabilities", "perform SQLi attacks", "bypass authentication using SQL inj… | `sources/06-antigravity/sql-injection-testing/` |
| **SQLMap Database Penetration Testing** | 🌌 Antigravity (634+) | This skill should be used when the user asks to "automate SQL injection testing," "enumerate database structure," "extract database credentials using … | `sources/06-antigravity/sqlmap-database-pentesting/` |
| **SSH Penetration Testing** | 🌌 Antigravity (634+) | This skill should be used when the user asks to "pentest SSH services", "enumerate SSH configurations", "brute force SSH credentials", "exploit SSH vu… | `sources/06-antigravity/ssh-penetration-testing/` |
| **stride-analysis-patterns** | 🌌 Antigravity (634+) | Apply STRIDE methodology to systematically identify threats. Use when analyzing system security, conducting threat modeling sessions, or creating secu… | `sources/06-antigravity/stride-analysis-patterns/` |
| **threat-mitigation-mapping** | 🌌 Antigravity (634+) | Map identified threats to appropriate security controls and mitigations. Use when prioritizing security investments, creating remediation plans, or va… | `sources/06-antigravity/threat-mitigation-mapping/` |
| **threat-modeling-expert** | 🌌 Antigravity (634+) | Expert in threat modeling methodologies, security architecture review, and risk assessment. Masters STRIDE, PASTA, attack trees, and security requirem… | `sources/06-antigravity/threat-modeling-expert/` |
| **Top 100 Web Vulnerabilities Reference** | 🌌 Antigravity (634+) | This skill should be used when the user asks to "identify web application vulnerabilities", "explain common security flaws", "understand vulnerability… | `sources/06-antigravity/top-web-vulnerabilities/` |
| **vulnerability-scanner** | 🌌 Antigravity (634+) | Advanced vulnerability analysis principles. OWASP 2025, Supply Chain Security, attack surface mapping, risk prioritization. | `sources/06-antigravity/vulnerability-scanner/` |
| **wcag-audit-patterns** | 🌌 Antigravity (634+) | Conduct WCAG 2.2 accessibility audits with automated testing, manual verification, and remediation guidance. Use when auditing websites for accessibil… | `sources/06-antigravity/wcag-audit-patterns/` |
| **web-design-guidelines** | 🌌 Antigravity (634+) | Review UI code for Web Interface Guidelines compliance. Use when asked to "review my UI", "check accessibility", "audit design", "review UX", or "chec… | `sources/06-antigravity/web-design-guidelines/` |
| **Windows Privilege Escalation** | 🌌 Antigravity (634+) | This skill should be used when the user asks to "escalate privileges on Windows," "find Windows privesc vectors," "enumerate Windows for privilege esc… | `sources/06-antigravity/windows-privilege-escalation/` |
| **WordPress Penetration Testing** | 🌌 Antigravity (634+) | This skill should be used when the user asks to "pentest WordPress sites", "scan WordPress for vulnerabilities", "enumerate WordPress users, themes, o… | `sources/06-antigravity/wordpress-penetration-testing/` |
| **accessibility** | 📦 skills | Audit and improve web accessibility following WCAG 2.1 guidelines. Use when asked to "improve accessibility", "a11y audit", "WCAG compliance", "screen… | `skills/accessibility/` |
| **agency-engineering** | 📦 skills | Índice dos 23 agentes de Engenharia da Agency (Backend Architect, Code Reviewer, Security Engineer, SRE, DevOps Automator, AI Engineer, Database Optim… | `skills/agency/engineering/` |
| **agency-paid-media** | 📦 skills | Índice dos 7 agentes e 4 workflows de Mídia Paga da Agency (PPC Strategist, Paid Social Strategist, Creative Strategist, Tracking Specialist, Programm… | `skills/agency/paid-media/` |
| **agency-specialized** | 📦 skills | Índice dos 24 agentes Especialistas da Agency (Agents Orchestrator, Compliance Auditor, Blockchain Security Auditor, MCP Builder, Document Generator, … | `skills/agency/specialized/` |
| **agency-testing** | 📦 skills | Índice dos 8 agentes de Qualidade e Testes da Agency (Accessibility Auditor, API Tester, Performance Benchmarker, Reality Checker, Evidence Collector,… | `skills/agency/testing/` |
| **agent-skills-search** | 📦 skills | Search and install Agent Skills from the local sources at ~/Development/osforge/sources/. Use when looking for specialized skills, best practices, or … | `skills/agent-skills-search/` |
| **best-practices** | 📦 skills | Apply modern web development best practices for security, compatibility, and code quality. Use when asked to "apply best practices", "security audit",… | `skills/best-practices/` |
| **code-review-checklist** | 📦 skills | Checklist de code review cobrindo correção, segurança, performance, qualidade, testes e padrões específicos de código gerado por IA. ACIONE quando: pe… | `skills/code-review-checklist/` |
| **database-design** | 📦 skills | Princípios de design de banco de dados: escolha de banco e ORM, schema, índices, otimização e migrations. ACIONE quando: query lenta ou N+1 em produçã… | `skills/database-design/` |
| **db-state-sync** | 📦 skills | Gerencia estado de projetos no banco SQLite local do OSForge (~/.osforge/osforge.db). ACIONE quando: salvar progresso de uma fase, registrar decisão a… | `skills/context/db-state-sync/` |
| **differential-review** | 📦 skills | Security-focused code review of diffs and PRs. Trigger on PR security review, git diff analysis, change impact assessment, or when reviewing commits t… | `skills/differential-review/` |
| **gdpr-data-handling** | 📦 skills | GDPR/LGPD compliance patterns for data handling. Trigger on consent management, data subject rights (access, deletion, portability), privacy policies,… | `skills/gdpr-data-handling/` |
| **insecure-defaults** | 📦 skills | Detect fail-open patterns and insecure default configurations. Trigger on security hardening, env variable audit, default config review, permission ch… | `skills/insecure-defaults/` |
| **lint-and-validate** | 📦 skills | Controle de qualidade automático após cada modificação de código: lint, type-check e análise estática (eslint, tsc, ruff, mypy, bandit, npm audit). AC… | `skills/lint-and-validate/` |
| **offensive-ai-security** | 📦 skills | AI/LLM security offensive checklist: prompt injection, jailbreaking, model extraction, training data poisoning, adversarial inputs, LLM-assisted attac… | `skills/offensive-ai-security/` |
| **offensive-ai-security** | 🛡️ Claude-Red (Offensive Security) | AI/LLM security offensive checklist: prompt injection, jailbreaking, model extraction, training data poisoning, adversarial inputs, LLM-assisted attac… | `sources/13-claude-red/offensive-ai-security/` |
| **offensive-bug-identification** | 📦 skills | Systematic bug identification methodology: source code review patterns, black-box testing strategies, taint analysis, dangerous function hunting, data… | `skills/offensive-bug-identification/` |
| **offensive-bug-identification** | 🛡️ Claude-Red (Offensive Security) | Systematic bug identification methodology: source code review patterns, black-box testing strategies, taint analysis, dangerous function hunting, data… | `sources/13-claude-red/offensive-bug-identification/` |
| **offensive-business-logic** | 📦 skills | Business logic vulnerability testing for web/mobile/API engagements. Covers workflow bypass, state machine violations, multi-step process abuse, price… | `skills/offensive-business-logic/` |
| **offensive-business-logic** | 🛡️ Claude-Red (Offensive Security) | Business logic vulnerability testing for web/mobile/API engagements. Covers workflow bypass, state machine violations, multi-step process abuse, price… | `sources/13-claude-red/offensive-business-logic/` |
| **offensive-cloud** | 📦 skills | Cloud security attack methodology across AWS, Azure, and GCP. Covers credential harvesting (IMDS, ~/.aws, env vars, leaked CI secrets, instance roles)… | `skills/offensive-cloud/` |
| **offensive-cloud** | 🛡️ Claude-Red (Offensive Security) | Cloud security attack methodology across AWS, Azure, and GCP. Covers credential harvesting (IMDS, ~/.aws, env vars, leaked CI secrets, instance roles)… | `sources/13-claude-red/offensive-cloud/` |
| **offensive-deserialization** | 📦 skills | Insecure deserialization attack checklist: identifying deserialization sinks, Java/PHP/.NET/Python deserialization exploitation, ysoserial gadget chai… | `skills/offensive-deserialization/` |
| **offensive-deserialization** | 🛡️ Claude-Red (Offensive Security) | Insecure deserialization attack checklist: identifying deserialization sinks, Java/PHP/.NET/Python deserialization exploitation, ysoserial gadget chai… | `sources/13-claude-red/offensive-deserialization/` |
| **offensive-fast-checking** | 📦 skills | Speed-optimized offensive checklist for rapid assessment: quick-win vulnerability patterns, fast recon shortcuts, automated scanner configurations, an… | `skills/offensive-fast-checking/` |
| **offensive-fast-checking** | 🛡️ Claude-Red (Offensive Security) | Speed-optimized offensive checklist for rapid assessment: quick-win vulnerability patterns, fast recon shortcuts, automated scanner configurations, an… | `sources/13-claude-red/offensive-fast-checking/` |
| **offensive-file-upload** | 📦 skills | File upload vulnerability checklist: MIME type bypass, extension bypass, magic byte manipulation, path traversal in filenames, stored XSS via SVG/HTML… | `skills/offensive-file-upload/` |
| **offensive-file-upload** | 🛡️ Claude-Red (Offensive Security) | File upload vulnerability checklist: MIME type bypass, extension bypass, magic byte manipulation, path traversal in filenames, stored XSS via SVG/HTML… | `sources/13-claude-red/offensive-file-upload/` |
| **offensive-fuzzing** | 📦 skills | Practical offensive fuzzing methodology covering target identification, fuzzer selection (AFL++, libFuzzer, Honggfuzz, Boofuzz, syzkaller), harness wr… | `skills/offensive-fuzzing/` |
| **offensive-fuzzing** | 🛡️ Claude-Red (Offensive Security) | Practical offensive fuzzing methodology covering target identification, fuzzer selection (AFL++, libFuzzer, Honggfuzz, Boofuzz, syzkaller), harness wr… | `sources/13-claude-red/offensive-fuzzing/` |
| **offensive-graphql** | 📦 skills | GraphQL security testing checklist: introspection abuse, batching attacks, query depth/complexity DoS, field suggestion enumeration, IDOR via GraphQL,… | `skills/offensive-graphql/` |
| **offensive-graphql** | 🛡️ Claude-Red (Offensive Security) | GraphQL security testing checklist: introspection abuse, batching attacks, query depth/complexity DoS, field suggestion enumeration, IDOR via GraphQL,… | `sources/13-claude-red/offensive-graphql/` |
| **offensive-idor** | 📦 skills | IDOR (Insecure Direct Object Reference) testing checklist: object ID enumeration, horizontal/vertical privilege escalation, GUID predictability, indir… | `skills/offensive-idor/` |
| **offensive-idor** | 🛡️ Claude-Red (Offensive Security) | IDOR (Insecure Direct Object Reference) testing checklist: object ID enumeration, horizontal/vertical privilege escalation, GUID predictability, indir… | `sources/13-claude-red/offensive-idor/` |
| **offensive-jwt** | 📦 skills | JWT attack methodology for penetration testers. Covers algorithm confusion (alg:none, RS256→HS256), weak HMAC secret brute force, kid parameter inject… | `skills/offensive-jwt/` |
| **offensive-jwt** | 🛡️ Claude-Red (Offensive Security) | JWT attack methodology for penetration testers. Covers algorithm confusion (alg:none, RS256→HS256), weak HMAC secret brute force, kid parameter inject… | `sources/13-claude-red/offensive-jwt/` |
| **offensive-mobile** | 📦 skills | Mobile (Android + iOS) application penetration testing methodology. Covers static analysis (apktool/jadx for Android, class-dump/Hopper/IDA for iOS), … | `skills/offensive-mobile/` |
| **offensive-mobile** | 🛡️ Claude-Red (Offensive Security) | Mobile (Android + iOS) application penetration testing methodology. Covers static analysis (apktool/jadx for Android, class-dump/Hopper/IDA for iOS), … | `sources/13-claude-red/offensive-mobile/` |
| **offensive-open-redirect** | 📦 skills | Open redirect vulnerability checklist: parameter identification, bypass techniques (URL encoding, double slashes, CRLF injection, protocol handlers), … | `skills/offensive-open-redirect/` |
| **offensive-open-redirect** | 🛡️ Claude-Red (Offensive Security) | Open redirect vulnerability checklist: parameter identification, bypass techniques (URL encoding, double slashes, CRLF injection, protocol handlers), … | `sources/13-claude-red/offensive-open-redirect/` |
| **offensive-osint** | 📦 skills | Comprehensive OSINT methodology skill for offensive security, red team intelligence gathering, and bug bounty reconnaissance. Covers domain recon, ema… | `skills/offensive-osint/` |
| **offensive-osint** | 🛡️ Claude-Red (Offensive Security) | Comprehensive OSINT methodology skill for offensive security, red team intelligence gathering, and bug bounty reconnaissance. Covers domain recon, ema… | `sources/13-claude-red/offensive-osint/` |
| **offensive-parameter-pollution** | 📦 skills | HTTP parameter pollution (HPP) checklist: duplicate parameter injection, backend vs frontend parsing differences, WAF bypass via HPP, server-side vs c… | `skills/offensive-parameter-pollution/` |
| **offensive-parameter-pollution** | 🛡️ Claude-Red (Offensive Security) | HTTP parameter pollution (HPP) checklist: duplicate parameter injection, backend vs frontend parsing differences, WAF bypass via HPP, server-side vs c… | `sources/13-claude-red/offensive-parameter-pollution/` |
| **offensive-race-condition** | 📦 skills | Race condition (TOCTOU) testing checklist: identifying timing windows, Burp Suite Turbo Intruder, Last-Byte sync technique, rate limit bypass, double-… | `skills/offensive-race-condition/` |
| **offensive-race-condition** | 🛡️ Claude-Red (Offensive Security) | Race condition (TOCTOU) testing checklist: identifying timing windows, Burp Suite Turbo Intruder, Last-Byte sync technique, rate limit bypass, double-… | `sources/13-claude-red/offensive-race-condition/` |
| **offensive-rce** | 📦 skills | Remote Code Execution testing checklist: OS command injection, SSTI-to-RCE, deserialization RCE, file upload RCE, XXE with SSRF to RCE, RCE via depend… | `skills/offensive-rce/` |
| **offensive-rce** | 🛡️ Claude-Red (Offensive Security) | Remote Code Execution testing checklist: OS command injection, SSTI-to-RCE, deserialization RCE, file upload RCE, XXE with SSRF to RCE, RCE via depend… | `sources/13-claude-red/offensive-rce/` |
| **offensive-request-smuggling** | 📦 skills | HTTP request smuggling checklist: CL.TE, TE.CL, TE.TE variants, detection with timing and differential responses, WAF bypass, cache poisoning, credent… | `skills/offensive-request-smuggling/` |
| **offensive-request-smuggling** | 🛡️ Claude-Red (Offensive Security) | HTTP request smuggling checklist: CL.TE, TE.CL, TE.TE variants, detection with timing and differential responses, WAF bypass, cache poisoning, credent… | `sources/13-claude-red/offensive-request-smuggling/` |
| **offensive-sqli** | 📦 skills | SQL injection testing skill for offensive security assessments and bug bounty hunting. Covers error-based, UNION-based, boolean/time-based blind, out-… | `skills/offensive-sqli/` |
| **offensive-sqli** | 🛡️ Claude-Red (Offensive Security) | SQL injection testing skill for offensive security assessments and bug bounty hunting. Covers error-based, UNION-based, boolean/time-based blind, out-… | `sources/13-claude-red/offensive-sqli/` |
| **offensive-ssti** | 📦 skills | Server-Side Template Injection testing checklist: template engine identification (Jinja2, Twig, Freemarker, Pebble, Velocity), polyglot detection payl… | `skills/offensive-ssti/` |
| **offensive-ssti** | 🛡️ Claude-Red (Offensive Security) | Server-Side Template Injection testing checklist: template engine identification (Jinja2, Twig, Freemarker, Pebble, Velocity), polyglot detection payl… | `sources/13-claude-red/offensive-ssti/` |
| **offensive-toctou** | 📦 skills | Time-of-Check / Time-of-Use (TOCTOU) race condition exploitation methodology across binary, kernel, filesystem, web, and container layers. Covers symb… | `skills/offensive-toctou/` |
| **offensive-toctou** | 🛡️ Claude-Red (Offensive Security) | Time-of-Check / Time-of-Use (TOCTOU) race condition exploitation methodology across binary, kernel, filesystem, web, and container layers. Covers symb… | `sources/13-claude-red/offensive-toctou/` |
| **offensive-waf-bypass** | 📦 skills | WAF bypass techniques checklist: encoding bypass (URL/HTML/Unicode/double encoding), case variation, comment injection, HTTP header manipulation, chun… | `skills/offensive-waf-bypass/` |
| **offensive-waf-bypass** | 🛡️ Claude-Red (Offensive Security) | WAF bypass techniques checklist: encoding bypass (URL/HTML/Unicode/double encoding), case variation, comment injection, HTTP header manipulation, chun… | `sources/13-claude-red/offensive-waf-bypass/` |
| **offensive-xss** | 📦 skills | Cross-Site Scripting testing checklist: stored/reflected/DOM/blind XSS discovery, polyglot payloads, CSP bypass, XSS filter bypass, event handler inje… | `skills/offensive-xss/` |
| **offensive-xss** | 🛡️ Claude-Red (Offensive Security) | Cross-Site Scripting testing checklist: stored/reflected/DOM/blind XSS discovery, polyglot payloads, CSP bypass, XSS filter bypass, event handler inje… | `sources/13-claude-red/offensive-xss/` |
| **offensive-xxe** | 📦 skills | XML External Entity injection testing checklist: classic XXE, blind XXE (out-of-band), XXE via file upload (SVG/docx), XXE in SOAP/REST, error-based X… | `skills/offensive-xxe/` |
| **offensive-xxe** | 🛡️ Claude-Red (Offensive Security) | XML External Entity injection testing checklist: classic XXE, blind XXE (out-of-band), XXE via file upload (SVG/docx), XXE in SOAP/REST, error-based X… | `sources/13-claude-red/offensive-xxe/` |
| **red-team-tactics** | 📦 skills | Táticas de red team baseadas em MITRE ATT&CK para simulação de adversário autorizada. ACIONE quando: planejar simulação de ataque/pentest autorizado, … | `skills/red-team-tactics/` |
| **redesign-audit** | 📦 skills | OSForge enhancement layer sobre redesign-existing-projects. Audita projeto existente, identifica padrões AI-genéricos, aplica upgrades cirúrgicos + re… | `skills/redesign-audit/` |
| **redesign-existing-projects** | 📦 skills | Eleva sites e apps existentes a qualidade premium: audita o design atual, identifica padrões genéricos de IA e aplica upgrades de tipografia, cor e la… | `skills/redesign-existing-projects/` |
| **security-best-practices** | 📦 skills | Perform language and framework specific security best-practice reviews and suggest improvements. Trigger only when the user explicitly requests securi… | `skills/security-best-practices/` |
| **security-threat-model** | 📦 skills | Repository-grounded threat modeling that enumerates trust boundaries, assets, attacker capabilities, abuse paths, and mitigations, and writes a concis… | `skills/security-threat-model/` |
| **ui-audit** | 📦 skills | Auditoria retroativa de qualidade visual em código frontend já implementado. ACIONE após qualquer fase de UI/UX, ou quando: | `skills/quality/ui-audit/` |
| **vulnerability-scanner** | 📦 skills | Análise avançada de vulnerabilidades com OWASP Top 10:2025, supply chain security e priorização de risco. ACIONE quando: mapear superfície de ataque d… | `skills/vulnerability-scanner/` |
| **web-design-guidelines** | 📦 skills | Review UI code for Web Interface Guidelines compliance. Use when asked to "review my UI", "check accessibility", "audit design", "review UX", or "chec… | `skills/web-design-guidelines/` |
| **webapp-testing** | 📦 skills | Testes E2E de aplicações web com Playwright, auditoria profunda de rotas/endpoints e testes visuais, com script runner de browser incluso. ACIONE quan… | `skills/webapp-testing/` |

## 🤖 AI / ML / Agents

**142 skills**

| Skill | Origem | Descrição | Path Local |
|-------|--------|-----------|-----------|
| **doc-coauthoring** | 🟣 Anthropic (Oficial) | Guide users through a structured workflow for co-authoring documentation. Use when user wants to write documentation, proposals, technical specs, deci… | `sources/01-anthropic/doc-coauthoring/` |
| **mcp-builder** | 🟣 Anthropic (Oficial) | Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. … | `sources/01-anthropic/mcp-builder/` |
| **dispatching-parallel-agents** | 🔵 Superpowers (obra) | Use when facing 2+ independent tasks that can be worked on without shared state or sequential dependencies | `sources/02-superpowers/dispatching-parallel-agents/` |
| **subagent-driven-development** | 🔵 Superpowers (obra) | Use when executing implementation plans with independent tasks in the current session | `sources/02-superpowers/subagent-driven-development/` |
| **agents-md** | 🔴 Sentry | This skill should be used when the user asks to "create AGENTS.md", "update AGENTS.md", "maintain agent docs", "set up CLAUDE.md", or needs to keep ag… | `sources/11-sentry/agents-md/` |
| **doc-coauthoring** | 🔴 Sentry | Guide users through a structured workflow for co-authoring documentation. Use when user wants to write documentation, proposals, technical specs, deci… | `sources/11-sentry/doc-coauthoring/` |
| **advanced-evaluation** | 📐 Context Engineering | This skill should be used when the user asks to "implement LLM-as-judge", "compare model outputs", "create evaluation rubrics", "mitigate evaluation b… | `sources/05-context-engineering/advanced-evaluation/` |
| **bdi-mental-states** | 📐 Context Engineering | This skill should be used when the user asks to "model agent mental states", "implement BDI architecture", "create belief-desire-intention models", "t… | `sources/05-context-engineering/bdi-mental-states/` |
| **book-sft-pipeline** | 📐 Context Engineering | This skill should be used when the user asks to "fine-tune on books", "create SFT dataset", "train style model", "extract ePub text", or mentions styl… | `sources/05-context-engineering/_examples/book-sft-pipeline/` |
| **comprehensive-research-agent** | 📐 Context Engineering | Ensure thorough validation, error recovery, and transparent reasoning in research tasks with multiple tool calls | `sources/05-context-engineering/_examples/interleaved_thinking/generated_skills/comprehensive-research-agent/` |
| **context-compression** | 📐 Context Engineering | This skill should be used when the user asks to "compress context", "summarize conversation history", "implement compaction", "reduce token usage", or… | `sources/05-context-engineering/context-compression/` |
| **context-degradation** | 📐 Context Engineering | This skill should be used when the user asks to "diagnose context problems", "fix lost-in-middle issues", "debug agent failures", "understand context … | `sources/05-context-engineering/context-degradation/` |
| **context-optimization** | 📐 Context Engineering | This skill should be used when the user asks to "optimize context", "reduce token costs", "improve context efficiency", "implement KV-cache optimizati… | `sources/05-context-engineering/context-optimization/` |
| **digital-brain** | 📐 Context Engineering | This skill should be used when the user asks to "write a post", "check my voice", "look up contact", "prepare for meeting", "weekly review", "track go… | `sources/05-context-engineering/_examples/digital-brain-skill/` |
| **filesystem-context** | 📐 Context Engineering | This skill should be used when the user asks to "offload context to files", "implement dynamic context discovery", "use filesystem for agent memory", … | `sources/05-context-engineering/filesystem-context/` |
| **memory-systems** | 📐 Context Engineering | This skill should be used when the user asks to "implement agent memory", "persist state across sessions", "build knowledge graph", "track entities", … | `sources/05-context-engineering/memory-systems/` |
| **multi-agent-patterns** | 📐 Context Engineering | This skill should be used when the user asks to "design multi-agent system", "implement supervisor pattern", "create swarm architecture", "coordinate … | `sources/05-context-engineering/multi-agent-patterns/` |
| **project-development** | 📐 Context Engineering | This skill should be used when the user asks to "start an LLM project", "design batch pipeline", "evaluate task-model fit", "structure agent project",… | `sources/05-context-engineering/project-development/` |
| **reasoning-trace-optimizer** | 📐 Context Engineering | Debug and optimize AI agents by analyzing reasoning traces. Activates on | `sources/05-context-engineering/_examples/interleaved_thinking/` |
| **skill-template** | 📐 Context Engineering | Template for creating new Agent Skills for context engineering. Use this template when adding new skills to the collection. | `sources/05-context-engineering/_template/` |
| **tool-design** | 📐 Context Engineering | This skill should be used when the user asks to "design agent tools", "create tool descriptions", "reduce tool complexity", "implement MCP tools", or … | `sources/05-context-engineering/tool-design/` |
| **agent-manager-skill** | 🌌 Antigravity (634+) | Manage multiple local CLI agents via tmux sessions (start/stop/monitor/assign) with cron-friendly scheduling. | `sources/06-antigravity/agent-manager-skill/` |
| **agent-memory-mcp** | 🌌 Antigravity (634+) | A hybrid memory system that provides persistent, searchable knowledge management for AI agents (Architecture, Patterns, Decisions). | `sources/06-antigravity/agent-memory-mcp/` |
| **agent-memory-systems** | 🌌 Antigravity (634+) | Memory is the cornerstone of intelligent agents. Without it, every interaction starts from zero. This skill covers the architecture of agent memory: s… | `sources/06-antigravity/agent-memory-systems/` |
| **agent-orchestration-improve-agent** | 🌌 Antigravity (634+) | Systematic improvement of existing agents through performance analysis, prompt engineering, and continuous iteration. | `sources/06-antigravity/agent-orchestration-improve-agent/` |
| **agent-orchestration-multi-agent-optimize** | 🌌 Antigravity (634+) | Optimize multi-agent systems with coordinated profiling, workload distribution, and cost-aware orchestration. Use when improving agent performance, th… | `sources/06-antigravity/agent-orchestration-multi-agent-optimize/` |
| **agent-tool-builder** | 🌌 Antigravity (634+) | Tools are how AI agents interact with the world. A well-designed tool is the difference between an agent that works and one that hallucinates, fails s… | `sources/06-antigravity/agent-tool-builder/` |
| **ai-agents-architect** | 🌌 Antigravity (634+) | Expert in designing and building autonomous AI agents. Masters tool use, memory systems, planning strategies, and multi-agent orchestration. Use when:… | `sources/06-antigravity/ai-agents-architect/` |
| **ai-engineer** | 🌌 Antigravity (634+) | Build production-ready LLM applications, advanced RAG systems, and | `sources/06-antigravity/ai-engineer/` |
| **ai-product** | 🌌 Antigravity (634+) | Every product will be AI-powered. The question is whether you | `sources/06-antigravity/ai-product/` |
| **ai-wrapper-product** | 🌌 Antigravity (634+) | Expert in building products that wrap AI APIs (OpenAI, Anthropic, etc.) into focused tools people will pay for. Not just | `sources/06-antigravity/ai-wrapper-product/` |
| **api-documenter** | 🌌 Antigravity (634+) | Master API documentation with OpenAPI 3.1, AI-powered tools, and | `sources/06-antigravity/api-documenter/` |
| **app-builder** | 🌌 Antigravity (634+) | Main application building orchestrator. Creates full-stack applications from natural language requests. Determines project type, selects tech stack, c… | `sources/06-antigravity/app-builder/` |
| **architecture** | 🌌 Antigravity (634+) | Architectural decision-making framework. Requirements analysis, trade-off evaluation, ADR documentation. Use when making architecture decisions or ana… | `sources/06-antigravity/architecture/` |
| **arm-cortex-expert** | 🌌 Antigravity (634+) | Senior embedded software engineer specializing in firmware and driver development for ARM Cortex-M microcontrollers (Teensy, STM32, nRF52, SAMD). Deca… | `sources/06-antigravity/arm-cortex-expert/` |
| **audio-transcriber** | 🌌 Antigravity (634+) | Transform audio recordings into professional Markdown documentation with intelligent summaries using LLM integration | `sources/06-antigravity/audio-transcriber/` |
| **autonomous-agent-patterns** | 🌌 Antigravity (634+) | Design patterns for building autonomous coding agents. Covers tool integration, permission systems, browser automation, and human-in-the-loop workflow… | `sources/06-antigravity/autonomous-agent-patterns/` |
| **autonomous-agents** | 🌌 Antigravity (634+) | Autonomous agents are AI systems that can independently decompose goals, plan actions, execute tools, and self-correct without constant human guidance… | `sources/06-antigravity/autonomous-agents/` |
| **blockrun** | 🌌 Antigravity (634+) | Use when user needs capabilities Claude lacks (image generation, real-time X/Twitter data) or explicitly requests external models ("blockrun", "use gr… | `sources/06-antigravity/blockrun/` |
| **bullmq-specialist** | 🌌 Antigravity (634+) | BullMQ expert for Redis-backed job queues, background processing, and reliable async execution in Node.js/TypeScript applications. Use when: bullmq, b… | `sources/06-antigravity/bullmq-specialist/` |
| **business-analyst** | 🌌 Antigravity (634+) | Master modern business analysis with AI-powered analytics, | `sources/06-antigravity/business-analyst/` |
| **c-pro** | 🌌 Antigravity (634+) | Write efficient C code with proper memory management, pointer | `sources/06-antigravity/c-pro/` |
| **c4-context** | 🌌 Antigravity (634+) | Expert C4 Context-level documentation specialist. Creates | `sources/06-antigravity/c4-context/` |
| **clarity-gate** | 🌌 Antigravity (634+) | Pre-ingestion verification for epistemic quality in RAG systems with 9-point verification and Two-Round HITL workflow | `sources/06-antigravity/clarity-gate/` |
| **Claude Code Guide** | 🌌 Antigravity (634+) | Master guide for using Claude Code effectively. Includes configuration templates, prompting strategies "Thinking" keywords, debugging techniques, and … | `sources/06-antigravity/claude-code-guide/` |
| **clean-code** | 🌌 Antigravity (634+) | Pragmatic coding standards - concise, direct, no over-engineering, no unnecessary comments | `sources/06-antigravity/clean-code/` |
| **code-documentation-doc-generate** | 🌌 Antigravity (634+) | You are a documentation expert specializing in creating comprehensive, maintainable documentation from code. Generate API docs, architecture diagrams,… | `sources/06-antigravity/code-documentation-doc-generate/` |
| **code-refactoring-context-restore** | 🌌 Antigravity (634+) | Use when working with code refactoring context restore | `sources/06-antigravity/code-refactoring-context-restore/` |
| **code-review-ai-ai-review** | 🌌 Antigravity (634+) | You are an expert AI-powered code review specialist combining automated static analysis, intelligent pattern recognition, and modern DevOps practices.… | `sources/06-antigravity/code-review-ai-ai-review/` |
| **code-reviewer** | 🌌 Antigravity (634+) | Elite code review expert specializing in modern AI-powered code | `sources/06-antigravity/code-reviewer/` |
| **computer-use-agents** | 🌌 Antigravity (634+) | Build AI agents that interact with computers like humans do - viewing screens, moving cursors, clicking buttons, and typing text. Covers Anthropic | `sources/06-antigravity/computer-use-agents/` |
| **computer-vision-expert** | 🌌 Antigravity (634+) | SOTA Computer Vision Expert (2026). Specialized in YOLO26, Segment Anything 3 (SAM 3), Vision Language Models, and real-time spatial analysis. | `sources/06-antigravity/computer-vision-expert/` |
| **content-marketer** | 🌌 Antigravity (634+) | Elite content marketing strategist specializing in AI-powered | `sources/06-antigravity/content-marketer/` |
| **context-compression** | 🌌 Antigravity (634+) | Design and evaluate compression strategies for long-running sessions | `sources/06-antigravity/context-compression/` |
| **context-degradation** | 🌌 Antigravity (634+) | Recognize patterns of context failure: lost-in-middle, poisoning, distraction, and clash | `sources/06-antigravity/context-degradation/` |
| **context-driven-development** | 🌌 Antigravity (634+) | Use this skill when working with Conductor's context-driven | `sources/06-antigravity/context-driven-development/` |
| **context-fundamentals** | 🌌 Antigravity (634+) | Understand what context is, why it matters, and the anatomy of context in agent systems | `sources/06-antigravity/context-fundamentals/` |
| **context-management-context-restore** | 🌌 Antigravity (634+) | Use when working with context management context restore | `sources/06-antigravity/context-management-context-restore/` |
| **context-management-context-save** | 🌌 Antigravity (634+) | Use when working with context management context save | `sources/06-antigravity/context-management-context-save/` |
| **context-manager** | 🌌 Antigravity (634+) | Elite AI context engineering specialist mastering dynamic context | `sources/06-antigravity/context-manager/` |
| **context-optimization** | 🌌 Antigravity (634+) | Apply compaction, masking, and caching strategies | `sources/06-antigravity/context-optimization/` |
| **context-window-management** | 🌌 Antigravity (634+) | Strategies for managing LLM context windows including summarization, trimming, routing, and avoiding context rot Use when: context window, token limit… | `sources/06-antigravity/context-window-management/` |
| **conversation-memory** | 🌌 Antigravity (634+) | Persistent memory systems for LLM conversations including short-term, long-term, and entity-based memory Use when: conversation memory, remember, memo… | `sources/06-antigravity/conversation-memory/` |
| **cqrs-implementation** | 🌌 Antigravity (634+) | Implement Command Query Responsibility Segregation for scalable architectures. Use when separating read and write models, optimizing query performance… | `sources/06-antigravity/cqrs-implementation/` |
| **crewai** | 🌌 Antigravity (634+) | Expert in CrewAI - the leading role-based multi-agent framework used by 60% of Fortune 500 companies. Covers agent design with roles and goals, task d… | `sources/06-antigravity/crewai/` |
| **customer-support** | 🌌 Antigravity (634+) | Elite AI-powered customer support specialist mastering | `sources/06-antigravity/customer-support/` |
| **data-storytelling** | 🌌 Antigravity (634+) | Transform data into compelling narratives using visualization, context, and persuasive structure. Use when presenting analytics to stakeholders, creat… | `sources/06-antigravity/data-storytelling/` |
| **deep-research** | 🌌 Antigravity (634+) | Execute autonomous multi-step research using Google Gemini Deep Research Agent. Use for: market analysis, competitive landscaping, literature reviews,… | `sources/06-antigravity/deep-research/` |
| **design-orchestration** | 🌌 Antigravity (634+) | Orchestrates design workflows by routing work through brainstorming, multi-agent review, and execution readiness in the correct order. Prevents premat… | `sources/06-antigravity/design-orchestration/` |
| **dispatching-parallel-agents** | 🌌 Antigravity (634+) | Use when facing 2+ independent tasks that can be worked on without shared state or sequential dependencies | `sources/06-antigravity/dispatching-parallel-agents/` |
| **doc-coauthoring** | 🌌 Antigravity (634+) | Guide users through a structured workflow for co-authoring documentation. Use when user wants to write documentation, proposals, technical specs, deci… | `sources/06-antigravity/doc-coauthoring/` |
| **documentation-generation-doc-generate** | 🌌 Antigravity (634+) | You are a documentation expert specializing in creating comprehensive, maintainable documentation from code. Generate API docs, architecture diagrams,… | `sources/06-antigravity/documentation-generation-doc-generate/` |
| **documentation-templates** | 🌌 Antigravity (634+) | Documentation templates and structure guidelines. README, API docs, code comments, and AI-friendly documentation. | `sources/06-antigravity/documentation-templates/` |
| **error-debugging-multi-agent-review** | 🌌 Antigravity (634+) | Use when working with error debugging multi agent review | `sources/06-antigravity/error-debugging-multi-agent-review/` |
| **evaluation** | 🌌 Antigravity (634+) | Build evaluation frameworks for agent systems | `sources/06-antigravity/evaluation/` |
| **fal-audio** | 🌌 Antigravity (634+) | Text-to-speech and speech-to-text using fal.ai audio models | `sources/06-antigravity/fal-audio/` |
| **fal-generate** | 🌌 Antigravity (634+) | Generate images and videos using fal.ai AI models | `sources/06-antigravity/fal-generate/` |
| **fal-image-edit** | 🌌 Antigravity (634+) | AI-powered image editing with style transfer and object removal | `sources/06-antigravity/fal-image-edit/` |
| **fal-platform** | 🌌 Antigravity (634+) | Platform APIs for model management, pricing, and usage tracking | `sources/06-antigravity/fal-platform/` |
| **fal-workflow** | 🌌 Antigravity (634+) | Generate workflow JSON files for chaining AI models | `sources/06-antigravity/fal-workflow/` |
| **file-organizer** | 🌌 Antigravity (634+) | Intelligently organizes files and folders by understanding context, finding duplicates, and suggesting better organizational structures. Use when user… | `sources/06-antigravity/file-organizer/` |
| **fp-ts-pragmatic** | 🌌 Antigravity (634+) | A practical, jargon-free guide to fp-ts functional programming - the 80/20 approach that gets results without the academic overhead. Use when writing … | `sources/06-antigravity/fp-ts-pragmatic/` |
| **hybrid-search-implementation** | 🌌 Antigravity (634+) | Combine vector and keyword search for improved retrieval. Use when implementing RAG systems, building search engines, or when neither approach alone p… | `sources/06-antigravity/hybrid-search-implementation/` |
| **incident-response-smart-fix** | 🌌 Antigravity (634+) | [Extended thinking: This workflow implements a sophisticated debugging and resolution pipeline that leverages AI-assisted debugging tools and observab… | `sources/06-antigravity/incident-response-smart-fix/` |
| **langchain-architecture** | 🌌 Antigravity (634+) | Design LLM applications using the LangChain framework with agents, memory, and tool integration patterns. Use when building LangChain applications, im… | `sources/06-antigravity/langchain-architecture/` |
| **langfuse** | 🌌 Antigravity (634+) | Expert in Langfuse - the open-source LLM observability platform. Covers tracing, prompt management, evaluation, datasets, and integration with LangCha… | `sources/06-antigravity/langfuse/` |
| **last30days** | 🌌 Antigravity (634+) | Research a topic from the last 30 days on Reddit + X + Web, become an expert, and write copy-paste-ready prompts for the user's target tool. | `sources/06-antigravity/last30days/` |
| **llm-app-patterns** | 🌌 Antigravity (634+) | Production-ready patterns for building LLM applications. Covers RAG pipelines, agent architectures, prompt IDEs, and LLMOps monitoring. Use when desig… | `sources/06-antigravity/llm-app-patterns/` |
| **llm-application-dev-ai-assistant** | 🌌 Antigravity (634+) | You are an AI assistant development expert specializing in creating intelligent conversational interfaces, chatbots, and AI-powered applications. Desi… | `sources/06-antigravity/llm-application-dev-ai-assistant/` |
| **llm-application-dev-langchain-agent** | 🌌 Antigravity (634+) | You are an expert LangChain agent developer specializing in production-grade AI systems using LangChain 0.1+ and LangGraph. | `sources/06-antigravity/llm-application-dev-langchain-agent/` |
| **llm-application-dev-prompt-optimize** | 🌌 Antigravity (634+) | You are an expert prompt engineer specializing in crafting effective prompts for LLMs through advanced techniques including constitutional AI, chain-o… | `sources/06-antigravity/llm-application-dev-prompt-optimize/` |
| **machine-learning-ops-ml-pipeline** | 🌌 Antigravity (634+) | Design and implement a complete ML pipeline for: $ARGUMENTS | `sources/06-antigravity/machine-learning-ops-ml-pipeline/` |
| **marketing-psychology** | 🌌 Antigravity (634+) | Apply behavioral science and mental models to marketing decisions, prioritized using a psychological leverage and feasibility scoring system. | `sources/06-antigravity/marketing-psychology/` |
| **mcp-builder** | 🌌 Antigravity (634+) | Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. … | `sources/06-antigravity/mcp-builder/` |
| **memory-safety-patterns** | 🌌 Antigravity (634+) | Implement memory-safe programming with RAII, ownership, smart pointers, and resource management across Rust, C++, and C. Use when writing safe systems… | `sources/06-antigravity/memory-safety-patterns/` |
| **memory-systems** | 🌌 Antigravity (634+) | Design short-term, long-term, and graph-based memory architectures | `sources/06-antigravity/memory-systems/` |
| **ml-engineer** | 🌌 Antigravity (634+) | Build production ML systems with PyTorch 2.x, TensorFlow, and | `sources/06-antigravity/ml-engineer/` |
| **mlops-engineer** | 🌌 Antigravity (634+) | Build comprehensive ML pipelines, experiment tracking, and model | `sources/06-antigravity/mlops-engineer/` |
| **multi-agent-brainstorming** | 🌌 Antigravity (634+) | Use this skill when a design or idea requires higher confidence, risk reduction, or formal review. This skill orchestrates a structured, sequential mu… | `sources/06-antigravity/multi-agent-brainstorming/` |
| **multi-agent-patterns** | 🌌 Antigravity (634+) | Master orchestrator, peer-to-peer, and hierarchical multi-agent architectures | `sources/06-antigravity/multi-agent-patterns/` |
| **nanobanana-ppt-skills** | 🌌 Antigravity (634+) | AI-powered PPT generation with document analysis and styled images | `sources/06-antigravity/nanobanana-ppt-skills/` |
| **on-call-handoff-patterns** | 🌌 Antigravity (634+) | Master on-call shift handoffs with context transfer, escalation procedures, and documentation. Use when transitioning on-call responsibilities, docume… | `sources/06-antigravity/on-call-handoff-patterns/` |
| **projection-patterns** | 🌌 Antigravity (634+) | Build read models and projections from event streams. Use when implementing CQRS read sides, building materialized views, or optimizing query performa… | `sources/06-antigravity/projection-patterns/` |
| **prompt-caching** | 🌌 Antigravity (634+) | Caching strategies for LLM prompts including Anthropic prompt caching, response caching, and CAG (Cache Augmented Generation) Use when: prompt caching… | `sources/06-antigravity/prompt-caching/` |
| **prompt-engineer** | 🌌 Antigravity (634+) | Transforms user prompts into optimized prompts using frameworks (RTF, RISEN, Chain of Thought, RODES, Chain of Density, RACE, RISE, STAR, SOAP, CLEAR,… | `sources/06-antigravity/prompt-engineer/` |
| **prompt-engineering** | 🌌 Antigravity (634+) | Expert guide on prompt engineering patterns, best practices, and optimization techniques. Use when user wants to improve prompts, learn prompting stra… | `sources/06-antigravity/prompt-engineering/` |
| **prompt-engineering-patterns** | 🌌 Antigravity (634+) | Master advanced prompt engineering techniques to maximize LLM performance, reliability, and controllability in production. Use when optimizing prompts… | `sources/06-antigravity/prompt-engineering-patterns/` |
| **prompt-library** | 🌌 Antigravity (634+) | Curated collection of high-quality prompts for various use cases. Includes role-based prompts, task-specific templates, and prompt refinement techniqu… | `sources/06-antigravity/prompt-library/` |
| **python-performance-optimization** | 🌌 Antigravity (634+) | Profile and optimize Python code using cProfile, memory profilers, and performance best practices. Use when debugging slow Python code, optimizing bot… | `sources/06-antigravity/python-performance-optimization/` |
| **spark-optimization** | 🌌 Antigravity (634+) | Optimize Apache Spark jobs with partitioning, caching, shuffle optimization, and memory tuning. Use when improving Spark performance, debugging slow j… | `sources/06-antigravity/spark-optimization/` |
| **startup-business-analyst-financial-projections** | 🌌 Antigravity (634+) | Create detailed 3-5 year financial model with revenue, costs, cash | `sources/06-antigravity/startup-business-analyst-financial-projections/` |
| **startup-financial-modeling** | 🌌 Antigravity (634+) | This skill should be used when the user asks to "create financial | `sources/06-antigravity/startup-financial-modeling/` |
| **subagent-driven-development** | 🌌 Antigravity (634+) | Use when executing implementation plans with independent tasks in the current session | `sources/06-antigravity/subagent-driven-development/` |
| **team-collaboration-standup-notes** | 🌌 Antigravity (634+) | You are an expert team communication specialist focused on async-first standup practices, AI-assisted note generation from commit history, and effecti… | `sources/06-antigravity/team-collaboration-standup-notes/` |
| **telegram-bot-builder** | 🌌 Antigravity (634+) | Expert in building Telegram bots that solve real problems - from simple automation to complex AI-powered bots. Covers bot architecture, the Telegram B… | `sources/06-antigravity/telegram-bot-builder/` |
| **tool-design** | 🌌 Antigravity (634+) | Build tools that agents can use effectively, including architectural reduction patterns | `sources/06-antigravity/tool-design/` |
| **ui-skills** | 🌌 Antigravity (634+) | Opinionated, evolving constraints to guide agents when building interfaces | `sources/06-antigravity/ui-skills/` |
| **vexor** | 🌌 Antigravity (634+) | Vector-powered CLI for semantic file search with a Claude/Codex skill | `sources/06-antigravity/vexor/` |
| **voice-agents** | 🌌 Antigravity (634+) | Voice agents represent the frontier of AI interaction - humans speaking naturally with AI systems. The challenge isn | `sources/06-antigravity/voice-agents/` |
| **writing-skills** | 🌌 Antigravity (634+) | Use when creating, updating, or improving agent skills. | `sources/06-antigravity/writing-skills/` |
| **agency** | 📦 skills | Índice geral dos 121 agentes especialistas da The Agency, organizado em 10 divisões com roteamento on-demand. ACIONE quando: | `skills/agency/` |
| **agency-design** | 📦 skills | Índice dos 8 agentes de Design da Agency (Brand Guardian, UI Designer, UX Architect, UX Researcher, Image Prompt Engineer, Visual Storyteller, Whimsy … | `skills/agency/design/` |
| **agency-marketing** | 📦 skills | Índice dos 26 agentes e 25 workflows de Marketing da Agency (Growth Hacker, Content Creator, SEO Specialist, estrategistas por plataforma, CRO, mercad… | `skills/agency/marketing/` |
| **agency-product** | 📦 skills | Índice dos 5 agentes de Produto da Agency (Product Manager, Sprint Prioritizer, Feedback Synthesizer, Trend Researcher, Behavioral Nudge Engine). ACIO… | `skills/agency/product/` |
| **agency-project-management** | 📦 skills | Índice dos 6 agentes de Gestão de Projetos da Agency (Project Shepherd, Studio Producer, Studio Operations, Jira Workflow Steward, Experiment Tracker,… | `skills/agency/project-management/` |
| **agency-sales** | 📦 skills | Índice dos 8 agentes e 3 workflows de Vendas da Agency (Outbound Strategist, Discovery Coach, Deal Strategist, Proposal Strategist, Pipeline Analyst, … | `skills/agency/sales/` |
| **claude-api-typescript** | 📦 skills | Build apps with the Claude API, Anthropic TypeScript SDK, and Agent SDK. TRIGGER when: code imports `@anthropic-ai/sdk` or `@anthropic-ai/claude-agent… | `skills/claude-api-typescript/` |
| **coding-guidelines** | 📦 skills | Apply when writing, modifying, or reviewing code. Behavioral guidelines to reduce common LLM coding mistakes. Triggers on implementation tasks, code c… | `skills/coding-guidelines/` |
| **config-critique** | 📦 skills | Lint LLM-powered de customizações do usuário no OSForge — valida novas SKILL.md, rules .mdc, hooks customizados, agents adicionais, e overrides de CLA… | `skills/config-critique/` |
| **context-compact** | 📦 skills | Compactação estruturada de conversação quando atinge ~70% da janela de contexto. ACIONE quando: usuário diz "comprimir contexto", "compactar", "summar… | `skills/context-compact/` |
| **context-distillator** | 📦 skills | Compressão lossless de documentos longos para consumo otimizado por LLMs, preservando 100% da informação factual e eliminando overhead textual. ACIONE… | `skills/context/context-distillator/` |
| **dispatching-parallel-agents** | 📦 skills | Orquestra tasks paralelas em subagents independentes. ACIONE quando: 2+ tasks sem estado compartilhado, refatoração em múltiplos arquivos não relacion… | `skills/dispatching-parallel-agents/` |
| **doc-shard** | 📦 skills | Divide documentos markdown grandes em arquivos menores organizados com index. Use quando documento exceder context window ou para organizar docs exten… | `skills/context/doc-shard/` |
| **editorial-review** | 📦 skills | Revisão editorial de documentos técnicos em 2 modos: prose (copy-editing clínico) e structure (reorganização e simplificação). Use com "editorial revi… | `skills/context/editorial-review/` |
| **genai-optimization** | 📦 skills | Generative Engine Optimization (GEO) para conteúdo ser citado por motores de busca com IA. ACIONE quando: fazer conteúdo ser citado pelo ChatGPT/Perpl… | `skills/genai-optimization/` |
| **git-workflow** | 📦 skills | Git workflow patterns for AI agent development: worktrees for parallel agents, branching strategy, commit discipline, and merge workflows. Use when cr… | `skills/git-workflow/` |
| **llmfit-advisor** | 📦 skills | Detecta o hardware da máquina (RAM, CPU, GPU/VRAM) e recomenda os melhores LLMs locais com quantização ideal, estimativa de velocidade e scoring de fi… | `skills/llmfit-advisor/` |
| **phase-discussion** | 📦 skills | Captura decisões de implementação de uma fase ANTES do planejamento técnico. ACIONE antes de planejar qualquer fase com UI, API, sistema de conteúdo o… | `skills/planning/phase-discussion/` |
| **smart-model-dispatch** | 📦 skills | Roteador de modelos Claude. ACIONE quando: spawning de subagents via Agent tool, implementando feature com múltiplas subtasks de complexidade mista, o… | `skills/smart-model-dispatch/` |
| **stuck-recovery** | 📦 skills | Detecta agent stuck patterns (loops, repetições, drift do escopo, ferramenta falhando 3x+) e executa recovery cirúrgico: salva estado em osforge-db, i… | `skills/stuck-recovery/` |
| **tlc-spec-driven** | 📦 skills | Product-driven planning with 5 phases - Discover, Specify, Design, Tasks, Implement+Validate+Measure. Creates atomic tasks with verification criteria … | `skills/tlc-spec-driven/` |
| **tool-safety-classifier** | 📦 skills | Classifier LLM-powered de segurança pra auto-aprovação de tool calls em modos autônomos (CI, headless, agent-of-agents). ACIONE quando: usuário roda e… | `skills/tool-safety-classifier/` |

## 🔄 Workflow / Process

**135 skills**

| Skill | Origem | Descrição | Path Local |
|-------|--------|-----------|-----------|
| **xlsx** | 🟣 Anthropic (Oficial) | Use this skill any time a spreadsheet file is the primary input or output. This means any task where the user wants to: open, read, edit, or fix an ex… | `sources/01-anthropic/xlsx/` |
| **executing-plans** | 🔵 Superpowers (obra) | Use when you have a written implementation plan to execute in a separate session with review checkpoints | `sources/02-superpowers/executing-plans/` |
| **receiving-code-review** | 🔵 Superpowers (obra) | Use when receiving code review feedback, before implementing suggestions, especially if feedback seems unclear or technically questionable - requires … | `sources/02-superpowers/receiving-code-review/` |
| **requesting-code-review** | 🔵 Superpowers (obra) | Use when completing tasks, implementing major features, or before merging to verify work meets requirements | `sources/02-superpowers/requesting-code-review/` |
| **using-git-worktrees** | 🔵 Superpowers (obra) | Use when starting feature work that needs isolation from current workspace or before executing implementation plans - creates isolated git worktrees w… | `sources/02-superpowers/using-git-worktrees/` |
| **verification-before-completion** | 🔵 Superpowers (obra) | Use when about to claim work is complete, fixed, or passing, before committing or creating PRs - requires running verification commands and confirming… | `sources/02-superpowers/verification-before-completion/` |
| **dwarf-expert** | 🔒 Trail of Bits | Provides expertise for analyzing DWARF debug files and understanding the DWARF debug format/standard (v3-v5). Triggers when understanding DWARF inform… | `sources/07-trailofbits/dwarf-expert/skills/dwarf-expert/` |
| **code-simplifier** | 🔴 Sentry | Simplifies and refines code for clarity, consistency, and maintainability while preserving all functionality. Use when asked to "simplify code", "clea… | `sources/11-sentry/code-simplifier/` |
| **iterate-pr** | 🔴 Sentry | Iterate on a PR until CI passes. Use when you need to fix CI failures, address review feedback, or continuously push fixes until all checks are green.… | `sources/11-sentry/iterate-pr/` |
| **2d-games** | 🌌 Antigravity (634+) | 2D game development principles. Sprites, tilemaps, physics, camera. | `sources/06-antigravity/game-development/2d-games/` |
| **3d-games** | 🌌 Antigravity (634+) | 3D game development principles. Rendering, shaders, physics, cameras. | `sources/06-antigravity/game-development/3d-games/` |
| **address-github-comments** | 🌌 Antigravity (634+) | Use when you need to address review or issue comments on an open GitHub Pull Request using the gh CLI. | `sources/06-antigravity/address-github-comments/` |
| **anti-reversing-techniques** | 🌌 Antigravity (634+) | Understand anti-reversing, obfuscation, and protection techniques encountered during software analysis. Use when analyzing protected binaries, bypassi… | `sources/06-antigravity/anti-reversing-techniques/` |
| **behavioral-modes** | 🌌 Antigravity (634+) | AI operational modes (brainstorm, implement, debug, review, teach, ship, orchestrate). Use to adapt behavior based on task type. | `sources/06-antigravity/behavioral-modes/` |
| **blockchain-developer** | 🌌 Antigravity (634+) | Build production-ready Web3 applications, smart contracts, and | `sources/06-antigravity/blockchain-developer/` |
| **cc-skill-project-guidelines-example** | 🌌 Antigravity (634+) | Project Guidelines Skill (Example) | `sources/06-antigravity/cc-skill-project-guidelines-example/` |
| **code-refactoring-tech-debt** | 🌌 Antigravity (634+) | You are a technical debt expert specializing in identifying, quantifying, and prioritizing technical debt in software projects. Analyze the codebase t… | `sources/06-antigravity/code-refactoring-tech-debt/` |
| **code-review-excellence** | 🌌 Antigravity (634+) | Master effective code review practices to provide constructive feedback, catch bugs early, and foster knowledge sharing while maintaining team morale.… | `sources/06-antigravity/code-review-excellence/` |
| **codebase-cleanup-tech-debt** | 🌌 Antigravity (634+) | You are a technical debt expert specializing in identifying, quantifying, and prioritizing technical debt in software projects. Analyze the codebase t… | `sources/06-antigravity/codebase-cleanup-tech-debt/` |
| **comprehensive-review-full-review** | 🌌 Antigravity (634+) | Use when working with comprehensive review full review | `sources/06-antigravity/comprehensive-review-full-review/` |
| **comprehensive-review-pr-enhance** | 🌌 Antigravity (634+) | You are a PR optimization expert specializing in creating high-quality pull requests that facilitate efficient code reviews. Generate comprehensive PR… | `sources/06-antigravity/comprehensive-review-pr-enhance/` |
| **concise-planning** | 🌌 Antigravity (634+) | Use when a user asks for a plan for a coding task, to generate a clear, actionable, and atomic checklist. | `sources/06-antigravity/concise-planning/` |
| **conductor-new-track** | 🌌 Antigravity (634+) | Create a new track with specification and phased implementation plan | `sources/06-antigravity/conductor-new-track/` |
| **conductor-revert** | 🌌 Antigravity (634+) | Git-aware undo by logical work unit (track, phase, or task) | `sources/06-antigravity/conductor-revert/` |
| **conductor-setup** | 🌌 Antigravity (634+) | Initialize project with Conductor artifacts (product definition, | `sources/06-antigravity/conductor-setup/` |
| **conductor-status** | 🌌 Antigravity (634+) | Display project status, active tracks, and next actions | `sources/06-antigravity/conductor-status/` |
| **conductor-validator** | 🌌 Antigravity (634+) | Validates Conductor project artifacts for completeness, | `sources/06-antigravity/conductor-validator/` |
| **copy-editing** | 🌌 Antigravity (634+) | When the user wants to edit, review, or improve existing marketing copy. Also use when the user mentions | `sources/06-antigravity/copy-editing/` |
| **cpp-pro** | 🌌 Antigravity (634+) | Write idiomatic C++ code with modern features, RAII, smart | `sources/06-antigravity/cpp-pro/` |
| **debugging-strategies** | 🌌 Antigravity (634+) | Master systematic debugging techniques, profiling tools, and root cause analysis to efficiently track down bugs across any codebase or technology stac… | `sources/06-antigravity/debugging-strategies/` |
| **defi-protocol-templates** | 🌌 Antigravity (634+) | Implement DeFi protocols with production-ready templates for staking, AMMs, governance, and lending systems. Use when building decentralized finance a… | `sources/06-antigravity/defi-protocol-templates/` |
| **design-md** | 🌌 Antigravity (634+) | Analyze Stitch projects and synthesize a semantic design system into DESIGN.md files | `sources/06-antigravity/design-md/` |
| **distributed-debugging-debug-trace** | 🌌 Antigravity (634+) | You are a debugging expert specializing in setting up comprehensive debugging environments, distributed tracing, and diagnostic tools. Configure debug… | `sources/06-antigravity/distributed-debugging-debug-trace/` |
| **dx-optimizer** | 🌌 Antigravity (634+) | Developer Experience specialist. Improves tooling, setup, and | `sources/06-antigravity/dx-optimizer/` |
| **email-sequence** | 🌌 Antigravity (634+) | When the user wants to create or optimize an email sequence, drip campaign, automated email flow, or lifecycle email program. Also use when the user m… | `sources/06-antigravity/email-sequence/` |
| **environment-setup-guide** | 🌌 Antigravity (634+) | Guide developers through setting up development environments with proper tools, dependencies, and configurations | `sources/06-antigravity/environment-setup-guide/` |
| **error-debugging-error-analysis** | 🌌 Antigravity (634+) | You are an expert error analysis specialist with deep expertise in debugging distributed systems, analyzing production incidents, and implementing com… | `sources/06-antigravity/error-debugging-error-analysis/` |
| **error-debugging-error-trace** | 🌌 Antigravity (634+) | You are an error tracking and observability expert specializing in implementing comprehensive error monitoring solutions. Set up error tracking system… | `sources/06-antigravity/error-debugging-error-trace/` |
| **error-diagnostics-error-analysis** | 🌌 Antigravity (634+) | You are an expert error analysis specialist with deep expertise in debugging distributed systems, analyzing production incidents, and implementing com… | `sources/06-antigravity/error-diagnostics-error-analysis/` |
| **error-diagnostics-error-trace** | 🌌 Antigravity (634+) | You are an error tracking and observability expert specializing in implementing comprehensive error monitoring solutions. Set up error tracking system… | `sources/06-antigravity/error-diagnostics-error-trace/` |
| **executing-plans** | 🌌 Antigravity (634+) | Use when you have a written implementation plan to execute in a separate session with review checkpoints | `sources/06-antigravity/executing-plans/` |
| **form-cro** | 🌌 Antigravity (634+) | Optimize any form that is NOT signup or account registration — including lead capture, contact, demo request, application, survey, quote, and checkout… | `sources/06-antigravity/form-cro/` |
| **framework-migration-code-migrate** | 🌌 Antigravity (634+) | You are a code migration expert specializing in transitioning codebases between frameworks, languages, versions, and platforms. Generate comprehensive… | `sources/06-antigravity/framework-migration-code-migrate/` |
| **game-audio** | 🌌 Antigravity (634+) | Game audio principles. Sound design, music integration, adaptive audio systems. | `sources/06-antigravity/game-development/game-audio/` |
| **game-design** | 🌌 Antigravity (634+) | Game design principles. GDD structure, balancing, player psychology, progression. | `sources/06-antigravity/game-development/game-design/` |
| **game-development** | 🌌 Antigravity (634+) | Game development orchestrator. Routes to platform-specific skills based on project needs. | `sources/06-antigravity/game-development/` |
| **gdpr-data-handling** | 🌌 Antigravity (634+) | Implement GDPR-compliant data handling with consent management, data subject rights, and privacy by design. Use when building systems that process EU … | `sources/06-antigravity/gdpr-data-handling/` |
| **git-advanced-workflows** | 🌌 Antigravity (634+) | Master advanced Git workflows including rebasing, cherry-picking, bisect, worktrees, and reflog to maintain clean history and recover from any situati… | `sources/06-antigravity/git-advanced-workflows/` |
| **git-pr-workflows-pr-enhance** | 🌌 Antigravity (634+) | You are a PR optimization expert specializing in creating high-quality pull requests that facilitate efficient code reviews. Generate comprehensive PR… | `sources/06-antigravity/git-pr-workflows-pr-enhance/` |
| **git-pushing** | 🌌 Antigravity (634+) | Stage, commit, and push git changes with conventional commit messages. Use when user wants to commit and push changes, mentions pushing to remote, or … | `sources/06-antigravity/git-pushing/` |
| **grafana-dashboards** | 🌌 Antigravity (634+) | Create and manage production Grafana dashboards for real-time visualization of system and application metrics. Use when building monitoring dashboards… | `sources/06-antigravity/grafana-dashboards/` |
| **haskell-pro** | 🌌 Antigravity (634+) | Expert Haskell engineer specializing in advanced type systems, pure | `sources/06-antigravity/haskell-pro/` |
| **hr-pro** | 🌌 Antigravity (634+) | Professional, ethical HR partner for hiring, | `sources/06-antigravity/hr-pro/` |
| **incident-responder** | 🌌 Antigravity (634+) | Expert SRE incident responder specializing in rapid problem | `sources/06-antigravity/incident-responder/` |
| **incident-runbook-templates** | 🌌 Antigravity (634+) | Create structured incident response runbooks with step-by-step procedures, escalation paths, and recovery actions. Use when building runbooks, respond… | `sources/06-antigravity/incident-runbook-templates/` |
| **iterate-pr** | 🌌 Antigravity (634+) | Iterate on a PR until CI passes. Use when you need to fix CI failures, address review feedback, or continuously push fixes until all checks are green.… | `sources/06-antigravity/iterate-pr/` |
| **julia-pro** | 🌌 Antigravity (634+) | Master Julia 1.10+ with modern features, performance optimization, | `sources/06-antigravity/julia-pro/` |
| **kaizen** | 🌌 Antigravity (634+) | Guide for continuous improvement, error proofing, and standardization. Use this skill when the user wants to improve code quality, refactor, or discus… | `sources/06-antigravity/kaizen/` |
| **launch-strategy** | 🌌 Antigravity (634+) | When the user wants to plan a product launch, feature announcement, or release strategy. Also use when the user mentions | `sources/06-antigravity/launch-strategy/` |
| **legal-advisor** | 🌌 Antigravity (634+) | Draft privacy policies, terms of service, disclaimers, and legal | `sources/06-antigravity/legal-advisor/` |
| **linear-claude-skill** | 🌌 Antigravity (634+) | Manage Linear issues, projects, and teams | `sources/06-antigravity/linear-claude-skill/` |
| **lint-and-validate** | 🌌 Antigravity (634+) | Automatic quality control, linting, and static analysis procedures. Use after every code modification to ensure syntax correctness and project standar… | `sources/06-antigravity/lint-and-validate/` |
| **Linux Production Shell Scripts** | 🌌 Antigravity (634+) | This skill should be used when the user asks to "create bash scripts", "automate Linux tasks", "monitor system resources", "backup files", "manage use… | `sources/06-antigravity/linux-shell-scripting/` |
| **marketing-ideas** | 🌌 Antigravity (634+) | Provide proven marketing strategies and growth ideas for SaaS and software products, prioritized using a marketing feasibility scoring system. | `sources/06-antigravity/marketing-ideas/` |
| **micro-saas-launcher** | 🌌 Antigravity (634+) | Expert in launching small, focused SaaS products fast - the indie hacker approach to building profitable software. Covers idea validation, MVP develop… | `sources/06-antigravity/micro-saas-launcher/` |
| **minecraft-bukkit-pro** | 🌌 Antigravity (634+) | Master Minecraft server plugin development with Bukkit, Spigot, and | `sources/06-antigravity/minecraft-bukkit-pro/` |
| **nft-standards** | 🌌 Antigravity (634+) | Implement NFT standards (ERC-721, ERC-1155) with proper metadata handling, minting strategies, and marketplace integration. Use when creating NFT cont… | `sources/06-antigravity/nft-standards/` |
| **notion-template-business** | 🌌 Antigravity (634+) | Expert in building and selling Notion templates as a business - not just making templates, but building a sustainable digital product business. Covers… | `sources/06-antigravity/notion-template-business/` |
| **observability-engineer** | 🌌 Antigravity (634+) | Build production-ready monitoring, logging, and tracing systems. | `sources/06-antigravity/observability-engineer/` |
| **observability-monitoring-monitor-setup** | 🌌 Antigravity (634+) | You are a monitoring and observability expert specializing in implementing comprehensive monitoring solutions. Set up metrics collection, distributed … | `sources/06-antigravity/observability-monitoring-monitor-setup/` |
| **observability-monitoring-slo-implement** | 🌌 Antigravity (634+) | You are an SLO (Service Level Objective) expert specializing in implementing reliability standards and error budget-based practices. Design SLO framew… | `sources/06-antigravity/observability-monitoring-slo-implement/` |
| **observe-whatsapp** | 🌌 Antigravity (634+) | Observe and troubleshoot WhatsApp in Kapso: debug message delivery, inspect webhook deliveries/retries, triage API errors, and run health checks. Use … | `sources/06-antigravity/observe-whatsapp/` |
| **page-cro** | 🌌 Antigravity (634+) | Analyze and optimize individual pages for conversion performance. Use when the user wants to improve conversion rates, diagnose why a page is underper… | `sources/06-antigravity/page-cro/` |
| **payment-integration** | 🌌 Antigravity (634+) | Integrate Stripe, PayPal, and payment processors. Handles checkout | `sources/06-antigravity/payment-integration/` |
| **paypal-integration** | 🌌 Antigravity (634+) | Integrate PayPal payment processing with support for express checkout, subscriptions, and refund management. Use when implementing PayPal payments, pr… | `sources/06-antigravity/paypal-integration/` |
| **pc-games** | 🌌 Antigravity (634+) | PC and console game development principles. Engine selection, platform features, optimization strategies. | `sources/06-antigravity/game-development/pc-games/` |
| **performance-profiling** | 🌌 Antigravity (634+) | Performance profiling principles. Measurement, analysis, and optimization techniques. | `sources/06-antigravity/performance-profiling/` |
| **personal-tool-builder** | 🌌 Antigravity (634+) | Expert in building custom tools that solve your own problems first. The best products often start as personal tools - scratch your own itch, build for… | `sources/06-antigravity/personal-tool-builder/` |
| **php-pro** | 🌌 Antigravity (634+) | Write idiomatic PHP code with generators, iterators, SPL data | `sources/06-antigravity/php-pro/` |
| **planning-with-files** | 🌌 Antigravity (634+) | Implements Manus-style file-based planning for complex tasks. Creates task_plan.md, findings.md, and progress.md. Use when starting complex multi-step… | `sources/06-antigravity/planning-with-files/` |
| **posix-shell-pro** | 🌌 Antigravity (634+) | Expert in strict POSIX sh scripting for maximum portability across | `sources/06-antigravity/posix-shell-pro/` |
| **pricing-strategy** | 🌌 Antigravity (634+) | Design pricing, packaging, and monetization strategies based on value, customer willingness to pay, and growth objectives. | `sources/06-antigravity/pricing-strategy/` |
| **python-packaging** | 🌌 Antigravity (634+) | Create distributable Python packages with proper project structure, setup.py/pyproject.toml, and publishing to PyPI. Use when packaging Python librari… | `sources/06-antigravity/python-packaging/` |
| **python-pro** | 🌌 Antigravity (634+) | Master Python 3.12+ with modern features, async programming, | `sources/06-antigravity/python-pro/` |
| **receiving-code-review** | 🌌 Antigravity (634+) | Use when receiving code review feedback, before implementing suggestions, especially if feedback seems unclear or technically questionable - requires … | `sources/06-antigravity/receiving-code-review/` |
| **red-team-tactics** | 🌌 Antigravity (634+) | Red team tactics principles based on MITRE ATT&CK. Attack phases, detection evasion, reporting. | `sources/06-antigravity/red-team-tactics/` |
| **referral-program** | 🌌 Antigravity (634+) | When the user wants to create, optimize, or analyze a referral program, affiliate program, or word-of-mouth strategy. Also use when the user mentions | `sources/06-antigravity/referral-program/` |
| **requesting-code-review** | 🌌 Antigravity (634+) | Use when completing tasks, implementing major features, or before merging to verify work meets requirements | `sources/06-antigravity/requesting-code-review/` |
| **research-engineer** | 🌌 Antigravity (634+) | An uncompromising Academic Research Engineer. Operates with absolute scientific rigor, objective criticism, and zero flair. Focuses on theoretical cor… | `sources/06-antigravity/research-engineer/` |
| **sales-automator** | 🌌 Antigravity (634+) | Draft cold emails, follow-ups, and proposal templates. Creates | `sources/06-antigravity/sales-automator/` |
| **scala-pro** | 🌌 Antigravity (634+) | Master enterprise-grade Scala development with functional | `sources/06-antigravity/scala-pro/` |
| **seo-cannibalization-detector** | 🌌 Antigravity (634+) | Analyzes multiple provided pages to identify keyword overlap and | `sources/06-antigravity/seo-cannibalization-detector/` |
| **server-management** | 🌌 Antigravity (634+) | Server management principles and decision-making. Process management, monitoring strategy, and scaling decisions. Teaches thinking, not commands. | `sources/06-antigravity/server-management/` |
| **service-mesh-observability** | 🌌 Antigravity (634+) | Implement comprehensive observability for service meshes including distributed tracing, metrics, and visualization. Use when setting up mesh monitorin… | `sources/06-antigravity/service-mesh-observability/` |
| **sharp-edges** | 🌌 Antigravity (634+) | Identify error-prone APIs and dangerous configurations | `sources/06-antigravity/sharp-edges/` |
| **skill-creator** | 🌌 Antigravity (634+) | This skill should be used when the user asks to create a new skill, build a skill, make a custom skill, develop a CLI skill, or wants to extend the CL… | `sources/06-antigravity/skill-creator/` |
| **slo-implementation** | 🌌 Antigravity (634+) | Define and implement Service Level Indicators (SLIs) and Service Level Objectives (SLOs) with error budgets and alerting. Use when establishing reliab… | `sources/06-antigravity/slo-implementation/` |
| **startup-business-analyst-market-opportunity** | 🌌 Antigravity (634+) | Generate comprehensive market opportunity analysis with TAM/SAM/SOM | `sources/06-antigravity/startup-business-analyst-market-opportunity/` |
| **stripe-integration** | 🌌 Antigravity (634+) | Implement Stripe payment processing for robust, PCI-compliant payment flows including checkout, subscriptions, and webhooks. Use when integrating Stri… | `sources/06-antigravity/stripe-integration/` |
| **team-collaboration-issue** | 🌌 Antigravity (634+) | You are a GitHub issue resolution expert specializing in systematic bug investigation, feature implementation, and collaborative development workflows… | `sources/06-antigravity/team-collaboration-issue/` |
| **templates** | 🌌 Antigravity (634+) | Project scaffolding templates for new applications. Use when creating new projects from scratch. Contains 12 templates for various tech stacks. | `sources/06-antigravity/app-builder/templates/` |
| **temporal-python-pro** | 🌌 Antigravity (634+) | Master Temporal workflow orchestration with Python SDK. Implements | `sources/06-antigravity/temporal-python-pro/` |
| **trigger-dev** | 🌌 Antigravity (634+) | Trigger.dev expert for background jobs, AI workflows, and reliable async execution with excellent developer experience and TypeScript-first design. Us… | `sources/06-antigravity/trigger-dev/` |
| **typescript-advanced-types** | 🌌 Antigravity (634+) | Master TypeScript's advanced type system including generics, conditional types, mapped types, template literals, and utility types for building type-s… | `sources/06-antigravity/typescript-advanced-types/` |
| **typescript-pro** | 🌌 Antigravity (634+) | Master TypeScript with advanced types, generics, and strict type | `sources/06-antigravity/typescript-pro/` |
| **using-git-worktrees** | 🌌 Antigravity (634+) | Use when starting feature work that needs isolation from current workspace or before executing implementation plans - creates isolated git worktrees w… | `sources/06-antigravity/using-git-worktrees/` |
| **uv-package-manager** | 🌌 Antigravity (634+) | Master the uv package manager for fast Python dependency management, virtual environments, and modern Python project workflows. Use when setting up Py… | `sources/06-antigravity/uv-package-manager/` |
| **verification-before-completion** | 🌌 Antigravity (634+) | Use when about to claim work is complete, fixed, or passing, before committing or creating PRs - requires running verification commands and confirming… | `sources/06-antigravity/verification-before-completion/` |
| **vr-ar** | 🌌 Antigravity (634+) | VR/AR development principles. Comfort, interaction, performance requirements. | `sources/06-antigravity/game-development/vr-ar/` |
| **web-games** | 🌌 Antigravity (634+) | Web browser game development principles. Framework selection, WebGPU, optimization, PWA. | `sources/06-antigravity/game-development/web-games/` |
| **Wireshark Network Traffic Analysis** | 🌌 Antigravity (634+) | This skill should be used when the user asks to "analyze network traffic with Wireshark", "capture packets for troubleshooting", "filter PCAP files", … | `sources/06-antigravity/wireshark-analysis/` |
| **xlsx** | 🌌 Antigravity (634+) | Comprehensive spreadsheet creation, editing, and analysis with support for formulas, formatting, data analysis, and visualization. When Claude needs t… | `sources/06-antigravity/xlsx-official/` |
| **youtube-summarizer** | 🌌 Antigravity (634+) | Extract transcripts from YouTube videos and generate comprehensive, detailed summaries using intelligent analysis frameworks | `sources/06-antigravity/youtube-summarizer/` |
| **adversarial-review** | 📦 skills | Revisão cínica e adversarial de qualquer artefato. ACIONE quando: revisar spec antes de implementar, validar PRD, criticar schema, revisar código com … | `skills/quality/adversarial-review/` |
| **aesthetic-modes** | 📦 skills | Três modos visuais distintos para projetos com identidade forte: EDITORIAL_MINIMALIST (Notion/Linear, warm monochrome), INDUSTRIAL_BRUTALIST (Swiss + … | `skills/aesthetic-modes/` |
| **behavioral-modes** | 📦 skills | AI operational modes (brainstorm, implement, debug, review, teach, ship, orchestrate). Use to adapt behavior based on task type. | `skills/behavioral-modes/` |
| **brainstorming** | 📦 skills | Refinamento socrático de ideia ANTES de qualquer código ou spec técnica. ACIONE quando: usuário descreve uma ideia vaga, quer explorar alternativas an… | `skills/brainstorming/` |
| **code-review** | 📦 skills | Review estruturado de código com checklist adaptado ao stack OSForge. ACIONE quando: code review, revisar código, review PR, CR. Integra adversarial-r… | `skills/quality/code-review/` |
| **core-web-vitals** | 📦 skills | Optimize Core Web Vitals (LCP, INP, CLS) for better page experience and search ranking. Use when asked to "improve Core Web Vitals", "fix LCP", "reduc… | `skills/core-web-vitals/` |
| **elicitation-engine** | 📦 skills | Refinamento iterativo de outputs (specs, PRDs, decisões arquiteturais, qualquer artefato) via menu interativo de técnicas de elicitação estruturadas. … | `skills/quality/elicitation-engine/` |
| **finishing-a-development-branch** | 📦 skills | Workflow de finalização de branch de desenvolvimento. ACIONE quando: todas as tasks de uma branch estão completas, usuário quer mergear ou abrir PR, p… | `skills/finishing-a-development-branch/` |
| **full-output-enforcement** | 📦 skills | Regra base anti-truncamento: proíbe placeholders e omissões, exige geração completa de cada deliverable e gerencia splits por limite de token com marc… | `skills/full-output-enforcement/` |
| **high-end-visual-design** | 📦 skills | Faz o site parecer caro nível agência: fontes premium, cards double-bezel, sombras ultra-difusas, nav em pílula de vidro flutuante e coreografia de mo… | `skills/high-end-visual-design/` |
| **image-to-code** | 📦 skills | Elite website image-to-code skill for Codex. Trigger on requests like "design a stunning hero section", "build a premium landing page", or "redesign t… | `skills/image-to-code/` |
| **industrial-brutalist-ui** | 📦 skills | Gera interfaces brutalistas industriais que fundem print tipográfico suíço com terminais militares/CRT: grids rígidos, monospace, tipografia gigante, … | `skills/industrial-brutalist-ui/` |
| **osforge-canvas** | 📦 skills | UI generativa local para revisão interativa de planos, specs e breakdowns no browser, com feedback estruturado nativo. CANAL DEFAULT para apresentação… | `skills/osforge-canvas/` |
| **receiving-code-review** | 📦 skills | Como responder ao feedback de um code review. ACIONE quando: recebeu feedback de review, PR tem comments, revisor pediu mudanças, CHANGES_REQUESTED. K… | `skills/receiving-code-review/` |
| **requirements-clarify** | 📦 skills | Clarificação estruturada de requisitos ANTES do plano técnico. ACIONE quando: spec tem áreas vagas ou underspecificadas, usuário disse | `skills/planning/requirements-clarify/` |
| **rust-pro** | 📦 skills | Especialista em Rust 1.75+ para sistemas de alta performance: async com Tokio, ownership, lifetimes, traits avançados, unsafe/FFI e web services com a… | `skills/rust-pro/` |
| **seo** | 📦 skills | Optimize for search engine visibility and ranking. Use when asked to "improve SEO", "optimize for search", "fix meta tags", "add structured data", "si… | `skills/seo/` |
| **story-executor** | 📦 skills | Executa implementação de uma story seguindo suas tasks e ACs. ACIONE quando: executar story, implementar story, dev story, run story. Coordena invocaç… | `skills/planning/story-executor/` |
| **stripe-integration** | 📦 skills | Stripe payment processing for SaaS applications. Trigger on checkout implementation, subscription billing, webhook handling, pricing page, payment for… | `skills/stripe-integration/` |
| **systematic-debugging** | 📦 skills | Debugging sistemático em 4 fases com análise de causa raiz. ACIONE quando: bug difícil de reproduzir, crash sem stacktrace claro, comportamento interm… | `skills/systematic-debugging/` |
| **ui-design-intelligence** | 📦 skills | Spec de design system adaptado ao produto e indústria. ACIONE quando: usuário menciona estilo visual, identidade, paleta, tipografia, tom visual, tipo… | `skills/ui-design-intelligence/` |
| **verification-before-completion** | 📦 skills | Requires running verification commands and confirming output before making any success claims. Use when about to claim work is complete, fixed, passin… | `skills/verification-before-completion/` |

## ⚛️ React / Frontend

**96 skills**

| Skill | Origem | Descrição | Path Local |
|-------|--------|-----------|-----------|
| **algorithmic-art** | 🟣 Anthropic (Oficial) | Creating algorithmic art using p5.js with seeded randomness and interactive parameter exploration. Use this when users request creating art using code… | `sources/01-anthropic/algorithmic-art/` |
| **frontend-design** | 🟣 Anthropic (Oficial) | Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when the user asks to build web components, pages, a… | `sources/01-anthropic/frontend-design/` |
| **slack-gif-creator** | 🟣 Anthropic (Oficial) | Knowledge and utilities for creating animated GIFs optimized for Slack. Provides constraints, validation tools, and animation concepts. Use when users… | `sources/01-anthropic/slack-gif-creator/` |
| **theme-factory** | 🟣 Anthropic (Oficial) | Toolkit for styling artifacts with a theme. These artifacts can be slides, docs, reportings, HTML landing pages, etc. There are 10 pre-set themes with… | `sources/01-anthropic/theme-factory/` |
| **web-artifacts-builder** | 🟣 Anthropic (Oficial) | Suite of tools for creating elaborate, multi-component claude.ai HTML artifacts using modern frontend web technologies (React, Tailwind CSS, shadcn/ui… | `sources/01-anthropic/web-artifacts-builder/` |
| **brainstorming** | 🔵 Superpowers (obra) | You MUST use this before any creative work - creating features, building components, adding functionality, or modifying behavior. Explores user intent… | `sources/02-superpowers/brainstorming/` |
| **vercel-composition-patterns** | 🟢 Vercel Labs | React composition patterns that scale. Use when refactoring components with | `sources/04-vercel/composition-patterns/` |
| **vercel-react-best-practices** | 🟢 Vercel Labs | React and Next.js performance optimization guidelines from Vercel Engineering. This skill should be used when writing, reviewing, or refactoring React… | `sources/04-vercel/react-best-practices/` |
| **vercel-react-native-skills** | 🟢 Vercel Labs | React Native and Expo best practices for building performant mobile apps. Use | `sources/04-vercel/react-native-skills/` |
| **interpreting-culture-index** | 🔒 Trail of Bits | Use when interpreting Culture Index surveys, CI profiles, behavioral assessments, or personality data. Supports individual interpretation, team compos… | `sources/07-trailofbits/culture-index/skills/interpreting-culture-index/` |
| **agents-sdk** | ☁️ Cloudflare | Build AI agents on Cloudflare Workers using the Agents SDK. Load when creating stateful agents, durable workflows, real-time WebSocket apps, scheduled… | `sources/10-cloudflare/agents-sdk/` |
| **building-native-ui** | 📱 Expo | Complete guide for building beautiful apps with Expo Router. Covers fundamentals, styling, components, navigation, animations, patterns, and native ta… | `sources/09-expo/expo-app-design/skills/building-native-ui/` |
| **expo-tailwind-setup** | 📱 Expo | Set up Tailwind CSS v4 in Expo with react-native-css and NativeWind v5 for universal styling | `sources/09-expo/expo-app-design/skills/expo-tailwind-setup/` |
| **native-data-fetching** | 📱 Expo | Use when implementing or debugging ANY network request, API call, or data fetching. Covers fetch API, axios, React Query, SWR, error handling, caching… | `sources/09-expo/expo-app-design/skills/native-data-fetching/` |
| **use-dom** | 📱 Expo | Use Expo DOM components to run web code in a webview on native and as-is on web. Migrate web code to native incrementally. | `sources/09-expo/expo-app-design/skills/use-dom/` |
| **context-fundamentals** | 📐 Context Engineering | This skill should be used when the user asks to "understand context", "explain context windows", "design agent architecture", "debug context issues", … | `sources/05-context-engineering/context-fundamentals/` |
| **3d-web-experience** | 🌌 Antigravity (634+) | Expert in building 3D experiences for the web - Three.js, React Three Fiber, Spline, WebGL, and interactive 3D scenes. Covers product configurators, 3… | `sources/06-antigravity/3d-web-experience/` |
| **algolia-search** | 🌌 Antigravity (634+) | Expert patterns for Algolia search implementation, indexing strategies, React InstantSearch, and relevance tuning Use when: adding search to, algolia,… | `sources/06-antigravity/algolia-search/` |
| **algorithmic-art** | 🌌 Antigravity (634+) | Creating algorithmic art using p5.js with seeded randomness and interactive parameter exploration. Use this when users request creating art using code… | `sources/06-antigravity/algorithmic-art/` |
| **angular** | 🌌 Antigravity (634+) | Modern Angular (v20+) expert with deep knowledge of Signals, Standalone Components, Zoneless applications, SSR/Hydration, and reactive patterns. Use P… | `sources/06-antigravity/angular/` |
| **angular-state-management** | 🌌 Antigravity (634+) | Master modern Angular state management with Signals, NgRx, and RxJS. Use when setting up global state, managing component stores, choosing between sta… | `sources/06-antigravity/angular-state-management/` |
| **angular-ui-patterns** | 🌌 Antigravity (634+) | Modern Angular UI patterns for loading states, error handling, and data display. Use when building UI components, handling async data, or managing com… | `sources/06-antigravity/angular-ui-patterns/` |
| **application-performance-performance-optimization** | 🌌 Antigravity (634+) | Optimize end-to-end application performance with profiling, observability, and backend/frontend tuning. Use when coordinating performance optimization… | `sources/06-antigravity/application-performance-performance-optimization/` |
| **architecture-patterns** | 🌌 Antigravity (634+) | Implement proven backend architecture patterns including Clean Architecture, Hexagonal Architecture, and Domain-Driven Design. Use when architecting c… | `sources/06-antigravity/architecture-patterns/` |
| **avalonia-layout-zafiro** | 🌌 Antigravity (634+) | Guidelines for modern Avalonia UI layout using Zafiro.Avalonia, emphasizing shared styles, generic components, and avoiding XAML redundancy. | `sources/06-antigravity/avalonia-layout-zafiro/` |
| **avalonia-viewmodels-zafiro** | 🌌 Antigravity (634+) | Optimal ViewModel and Wizard creation patterns for Avalonia using Zafiro and ReactiveUI. | `sources/06-antigravity/avalonia-viewmodels-zafiro/` |
| **backend-patterns** | 🌌 Antigravity (634+) | Backend architecture patterns, API design, database optimization, and server-side best practices for Node.js, Express, and Next.js API routes. | `sources/06-antigravity/cc-skill-backend-patterns/` |
| **brainstorming** | 🌌 Antigravity (634+) | Use this skill before any creative or constructive work (features, components, architecture, behavior changes, or functionality). This skill transform… | `sources/06-antigravity/brainstorming/` |
| **c4-component** | 🌌 Antigravity (634+) | Expert C4 Component-level documentation specialist. Synthesizes C4 | `sources/06-antigravity/c4-component/` |
| **coding-standards** | 🌌 Antigravity (634+) | Universal coding standards, best practices, and patterns for TypeScript, JavaScript, React, and Node.js development. | `sources/06-antigravity/cc-skill-coding-standards/` |
| **core-components** | 🌌 Antigravity (634+) | Core component library and design system patterns. Use when building UI, using design tokens, or working with the component library. | `sources/06-antigravity/core-components/` |
| **discord-bot-architect** | 🌌 Antigravity (634+) | Specialized skill for building production-ready Discord bots. Covers Discord.js (JavaScript) and Pycord (Python), gateway intents, slash commands, int… | `sources/06-antigravity/discord-bot-architect/` |
| **embedding-strategies** | 🌌 Antigravity (634+) | Select and optimize embedding models for semantic search and RAG applications. Use when choosing embedding models, implementing chunking strategies, o… | `sources/06-antigravity/embedding-strategies/` |
| **fp-ts-react** | 🌌 Antigravity (634+) | Practical patterns for using fp-ts with React - hooks, state, forms, data fetching. Use when building React apps with functional programming patterns.… | `sources/06-antigravity/fp-ts-react/` |
| **framework-migration-legacy-modernize** | 🌌 Antigravity (634+) | Orchestrate a comprehensive legacy system modernization using the strangler fig pattern, enabling gradual replacement of outdated components while mai… | `sources/06-antigravity/framework-migration-legacy-modernize/` |
| **frontend-design** | 🌌 Antigravity (634+) | Create distinctive, production-grade frontend interfaces with intentional aesthetics, high craft, and non-generic visual identity. Use when building o… | `sources/06-antigravity/frontend-design/` |
| **frontend-dev-guidelines** | 🌌 Antigravity (634+) | Opinionated frontend development standards for modern React + TypeScript applications. Covers Suspense-first data fetching, lazy loading, feature-base… | `sources/06-antigravity/frontend-dev-guidelines/` |
| **frontend-developer** | 🌌 Antigravity (634+) | Build React components, implement responsive layouts, and handle | `sources/06-antigravity/frontend-developer/` |
| **frontend-patterns** | 🌌 Antigravity (634+) | Frontend development patterns for React, Next.js, state management, performance optimization, and UI best practices. | `sources/06-antigravity/cc-skill-frontend-patterns/` |
| **frontend-slides** | 🌌 Antigravity (634+) | Create stunning, animation-rich HTML presentations from scratch or by converting PowerPoint files. Use when the user wants to build a presentation, co… | `sources/06-antigravity/frontend-slides/` |
| **game-art** | 🌌 Antigravity (634+) | Game art principles. Visual style selection, asset pipeline, animation workflow. | `sources/06-antigravity/game-development/game-art/` |
| **imagen** | 🌌 Antigravity (634+) | This skill generates images using Google Gemini's image generation model (gemini-3-pro-image-preview). It enables seamless image creation during any C… | `sources/06-antigravity/imagen/` |
| **javascript-typescript-typescript-scaffold** | 🌌 Antigravity (634+) | You are a TypeScript project architecture expert specializing in scaffolding production-ready Node.js and frontend applications. Generate complete pro… | `sources/06-antigravity/javascript-typescript-typescript-scaffold/` |
| **langgraph** | 🌌 Antigravity (634+) | Expert in LangGraph - the production-grade framework for building stateful, multi-actor AI applications. Covers graph construction, state management, … | `sources/06-antigravity/langgraph/` |
| **mobile-design** | 🌌 Antigravity (634+) | Mobile-first design and engineering doctrine for iOS and Android apps. Covers touch interaction, performance, platform conventions, offline behavior, … | `sources/06-antigravity/mobile-design/` |
| **mobile-developer** | 🌌 Antigravity (634+) | Develop React Native, Flutter, or native mobile apps with modern | `sources/06-antigravity/mobile-developer/` |
| **nextjs-app-router-patterns** | 🌌 Antigravity (634+) | Master Next.js 14+ App Router with Server Components, streaming, parallel routes, and advanced data fetching. Use when building Next.js applications, … | `sources/06-antigravity/nextjs-app-router-patterns/` |
| **nextjs-best-practices** | 🌌 Antigravity (634+) | Next.js App Router principles. Server Components, data fetching, routing patterns. | `sources/06-antigravity/nextjs-best-practices/` |
| **nextjs-supabase-auth** | 🌌 Antigravity (634+) | Expert integration of Supabase Auth with Next.js App Router Use when: supabase auth next, authentication next.js, login supabase, auth middleware, pro… | `sources/06-antigravity/nextjs-supabase-auth/` |
| **parallel-agents** | 🌌 Antigravity (634+) | Multi-agent orchestration patterns. Use when multiple independent tasks can run with different domain expertise or when comprehensive analysis require… | `sources/06-antigravity/parallel-agents/` |
| **radix-ui-design-system** | 🌌 Antigravity (634+) | Build accessible design systems with Radix UI primitives. Headless component customization, theming strategies, and compound component patterns for pr… | `sources/06-antigravity/radix-ui-design-system/` |
| **react-native-architecture** | 🌌 Antigravity (634+) | Build production React Native apps with Expo, navigation, native modules, offline sync, and cross-platform patterns. Use when developing mobile apps, … | `sources/06-antigravity/react-native-architecture/` |
| **react-patterns** | 🌌 Antigravity (634+) | Modern React patterns and principles. Hooks, composition, performance, TypeScript best practices. | `sources/06-antigravity/react-patterns/` |
| **react-state-management** | 🌌 Antigravity (634+) | Master modern React state management with Redux Toolkit, Zustand, Jotai, and React Query. Use when setting up global state, managing server state, or … | `sources/06-antigravity/react-state-management/` |
| **react-ui-patterns** | 🌌 Antigravity (634+) | Modern React UI patterns for loading states, error handling, and data fetching. Use when building UI components, handling async data, or managing UI s… | `sources/06-antigravity/react-ui-patterns/` |
| **remotion-best-practices** | 🌌 Antigravity (634+) | Best practices for Remotion - Video creation in React | `sources/06-antigravity/remotion-best-practices/` |
| **salesforce-development** | 🌌 Antigravity (634+) | Expert patterns for Salesforce platform development including Lightning Web Components (LWC), Apex triggers and classes, REST/Bulk APIs, Connected App… | `sources/06-antigravity/salesforce-development/` |
| **scroll-experience** | 🌌 Antigravity (634+) | Expert in building immersive scroll-driven experiences - parallax storytelling, scroll animations, interactive narratives, and cinematic web experienc… | `sources/06-antigravity/scroll-experience/` |
| **senior-architect** | 🌌 Antigravity (634+) | Comprehensive software architecture skill for designing scalable, maintainable systems using ReactJS, NextJS, NodeJS, Express, React Native, Swift, Ko… | `sources/06-antigravity/senior-architect/` |
| **senior-fullstack** | 🌌 Antigravity (634+) | Comprehensive fullstack development skill for building complete web applications with React, Next.js, Node.js, GraphQL, and PostgreSQL. Includes proje… | `sources/06-antigravity/senior-fullstack/` |
| **shopify-apps** | 🌌 Antigravity (634+) | Expert patterns for Shopify app development including Remix/React Router apps, embedded apps with App Bridge, webhook handling, GraphQL Admin API, Pol… | `sources/06-antigravity/shopify-apps/` |
| **slack-bot-builder** | 🌌 Antigravity (634+) | Build Slack apps using the Bolt framework across Python, JavaScript, and Java. Covers Block Kit for rich UIs, interactive components, slash commands, … | `sources/06-antigravity/slack-bot-builder/` |
| **slack-gif-creator** | 🌌 Antigravity (634+) | Knowledge and utilities for creating animated GIFs optimized for Slack. Provides constraints, validation tools, and animation concepts. Use when users… | `sources/06-antigravity/slack-gif-creator/` |
| **swiftui-expert-skill** | 🌌 Antigravity (634+) | Write, review, or improve SwiftUI code following best practices for state management, view composition, performance, modern APIs, Swift concurrency, a… | `sources/06-antigravity/swiftui-expert-skill/` |
| **tailwind-design-system** | 🌌 Antigravity (634+) | Build scalable design systems with Tailwind CSS, design tokens, component libraries, and responsive patterns. Use when creating component libraries, i… | `sources/06-antigravity/tailwind-design-system/` |
| **tailwind-patterns** | 🌌 Antigravity (634+) | Tailwind CSS v4 principles. CSS-first configuration, container queries, modern patterns, design token architecture. | `sources/06-antigravity/tailwind-patterns/` |
| **team-composition-analysis** | 🌌 Antigravity (634+) | This skill should be used when the user asks to "plan team | `sources/06-antigravity/team-composition-analysis/` |
| **terraform-module-library** | 🌌 Antigravity (634+) | Build reusable Terraform modules for AWS, Azure, and GCP infrastructure following infrastructure-as-code best practices. Use when creating infrastruct… | `sources/06-antigravity/terraform-module-library/` |
| **theme-factory** | 🌌 Antigravity (634+) | Toolkit for styling artifacts with a theme. These artifacts can be slides, docs, reportings, HTML landing pages, etc. There are 10 pre-set themes with… | `sources/06-antigravity/theme-factory/` |
| **ui-ux-designer** | 🌌 Antigravity (634+) | Create interface designs, wireframes, and design systems. Masters | `sources/06-antigravity/ui-ux-designer/` |
| **ui-ux-pro-max** | 🌌 Antigravity (634+) | UI/UX design intelligence. 50 styles, 21 palettes, 50 font pairings, 20 charts, 9 stacks (React, Next.js, Vue, Svelte, SwiftUI, React Native, Flutter,… | `sources/06-antigravity/ui-ux-pro-max/` |
| **unity-ecs-patterns** | 🌌 Antigravity (634+) | Master Unity ECS (Entity Component System) with DOTS, Jobs, and Burst for high-performance game development. Use when building data-oriented games, op… | `sources/06-antigravity/unity-ecs-patterns/` |
| **vercel-deployment** | 🌌 Antigravity (634+) | Expert knowledge for deploying to Vercel with Next.js Use when: vercel, deploy, deployment, hosting, production. | `sources/06-antigravity/vercel-deployment/` |
| **vercel-react-best-practices** | 🌌 Antigravity (634+) | React and Next.js performance optimization guidelines from Vercel Engineering. This skill should be used when writing, reviewing, or refactoring React… | `sources/06-antigravity/react-best-practices/` |
| **web-artifacts-builder** | 🌌 Antigravity (634+) | Suite of tools for creating elaborate, multi-component claude.ai HTML artifacts using modern frontend web technologies (React, Tailwind CSS, shadcn/ui… | `sources/06-antigravity/web-artifacts-builder/` |
| **aesthetic-boost** | 📦 skills | Boost estético anti-AI-slop. Invoque junto com qualquer skill de frontend para elevar a qualidade visual. Ative quando o usuário pedir "design bonito"… | `skills/aesthetic-boost/` |
| **app-builder** | 📦 skills | Orquestrador de criação de aplicações full-stack a partir de pedidos em linguagem natural, com 13 templates de scaffolding e coordenação de agentes. A… | `skills/app-builder/` |
| **arch-builder** | 📦 skills | Facilitação de decisões arquiteturais com ADRs. Stack-aware — respeita project-context.md e otimiza para Next.js/Prisma/Supabase. ACIONE com frases co… | `skills/planning/arch-builder/` |
| **autorefine-skill** | 📦 skills | Refinamento autônomo iterativo com loop autoresearch + meta-otimização + transferência cross-domínio. ACIONE quando (ex.: | `skills/autorefine-skill/` |
| **design-md** | 📦 skills | Contrato de identidade de marca POR PROJETO em um arquivo DESIGN.md — o documento de 9 seções (Visual Theme, Color, Typography, Spacing, Layout, Compo… | `skills/design-md/` |
| **design-taste-frontend** | 📦 skills | Anti-slop frontend skill for landing pages, portfolios, and redesigns. Trigger on phrases like "build a landing page", "create my portfolio site", "re… | `skills/design-taste-frontend/` |
| **design-taste-frontend-v1** | 📦 skills | Versão legada v1 da taste-skill de frontend premium com dials fixos (variance 8, motion 6, density 4), anti-slop, ban de Inter e roxo-AI, e micro-físi… | `skills/design-taste-frontend-v1/` |
| **frontend-design** | 📦 skills | Design thinking and decision-making for web UI. ACTIVATE whenever the user asks to design or style UI components, build page layouts, choose color pal… | `skills/frontend-design/` |
| **frontend-ui-system** | 📦 skills | Frontend UI development using shadcn/ui ecosystem with extended registries (Magic UI, Aceternity UI, mapcn). Leverages shadcn MCP and shadcn Studio ex… | `skills/frontend-ui-system/` |
| **gpt-taste** | 📦 skills | Engenharia de design award-winning com motion GSAP avançado: randomização de layouts, estrutura AIDA, hero de no máximo 2-3 linhas, bento grids sem cé… | `skills/gpt-taste/` |
| **i18n-localization** | 📦 skills | Internationalization for Next.js applications. Trigger on multi-language support ("set up multiple languages", "add English/Spanish support", "transla… | `skills/i18n-localization/` |
| **imagegen-frontend-mobile** | 📦 skills | Elite mobile app image-generation skill for creating premium, app-native screen concepts and flows. Keywords - mobile UI design, iOS app design, Andro… | `skills/imagegen-frontend-mobile/` |
| **imagegen-frontend-web** | 📦 skills | Direção de arte para gerar mockups de sites premium via geração de imagem: uma imagem horizontal separada por seção, variedade de composição de hero e… | `skills/imagegen-frontend-web/` |
| **nextjs-react-expert** | 📦 skills | React and Next.js performance optimization from Vercel Engineering. Use when building React components, optimizing performance, eliminating waterfalls… | `skills/nextjs-react-expert/` |
| **nextjs-supabase-auth** | 📦 skills | Padrões de autenticação Next.js App Router + Supabase Auth. ACIONE quando: configurando middleware de auth, RBAC multi-org, gerenciamento de sessão, r… | `skills/nextjs-supabase-auth/` |
| **openui-genui-layout** | 📦 skills | Planejamento e geração de UI em Next.js. ACIONE quando: criando qualquer página, tela, dashboard, formulário, tabela, componente com layout, scaffold … | `skills/openui-genui-layout/` |
| **react-performance** | 📦 skills | React and Next.js performance optimization rules from Vercel Engineering. Use when writing, reviewing, or refactoring React components, Next.js pages,… | `skills/react-performance/` |
| **stitch-design-taste** | 📦 skills | Gera arquivos DESIGN.md semânticos para o Google Stitch, codificando atmosfera, paleta calibrada, tipografia, componentes e anti-padrões em linguagem … | `skills/stitch-design-taste/` |
| **tailwind-patterns** | 📦 skills | Padrões técnicos de Tailwind CSS v4: configuração CSS-first com @theme, engine Oxide, container queries nativas, design tokens como CSS variables e mi… | `skills/tailwind-patterns/` |
| **taste-design-dials** | 📦 skills | Camada de enhancement OSForge sobre a taste-skill com 3 dials ajustáveis (DESIGN_VARIANCE, MOTION_INTENSITY, VISUAL_DENSITY) mais regras Next.js App R… | `skills/taste-design-dials/` |
| **visual-planner** | 📦 skills | Transforma documentos de planejamento em breakdowns HTML visuais e interativos. ACIONE quando: visualizar um plano, transformar spec em HTML, criar br… | `skills/visual-planner/` |

## 🧪 Testing

**84 skills**

| Skill | Origem | Descrição | Path Local |
|-------|--------|-----------|-----------|
| **skill-creator** | 🟣 Anthropic (Oficial) | Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from scratch, update or op… | `sources/01-anthropic/skill-creator/` |
| **webapp-testing** | 🟣 Anthropic (Oficial) | Toolkit for interacting with and testing local web applications using Playwright. Supports verifying frontend functionality, debugging UI behavior, ca… | `sources/01-anthropic/webapp-testing/` |
| **finishing-a-development-branch** | 🔵 Superpowers (obra) | Use when implementation is complete, all tests pass, and you need to decide how to integrate the work - guides completion of development work by prese… | `sources/02-superpowers/finishing-a-development-branch/` |
| **systematic-debugging** | 🔵 Superpowers (obra) | Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes | `sources/02-superpowers/systematic-debugging/` |
| **test-driven-development** | 🔵 Superpowers (obra) | Use when implementing any feature or bugfix, before writing implementation code | `sources/02-superpowers/test-driven-development/` |
| **property-based-testing** | 🔒 Trail of Bits | Provides guidance for property-based testing across multiple languages and smart contracts. Use when writing tests, reviewing code with serialization/… | `sources/07-trailofbits/property-based-testing/skills/property-based-testing/` |
| **wycheproof** | 🔒 Trail of Bits | Wycheproof provides test vectors for validating cryptographic implementations. Use when testing crypto code for known attacks and edge cases. | `sources/07-trailofbits/testing-handbook-skills/skills/wycheproof/` |
| **expo-dev-client** | 📱 Expo | Build and distribute Expo development clients locally or via TestFlight | `sources/09-expo/expo-app-design/skills/expo-dev-client/` |
| **evaluation** | 📐 Context Engineering | This skill should be used when the user asks to "evaluate agent performance", "build test framework", "measure agent quality", "create evaluation rubr… | `sources/05-context-engineering/evaluation/` |
| **ab-test-setup** | 🌌 Antigravity (634+) | Structured guide for setting up A/B tests with mandatory gates for hypothesis, metrics, and execution readiness. | `sources/06-antigravity/ab-test-setup/` |
| **agent-evaluation** | 🌌 Antigravity (634+) | Testing and benchmarking LLM agents including behavioral testing, capability assessment, reliability metrics, and production monitoring—where even top… | `sources/06-antigravity/agent-evaluation/` |
| **airflow-dag-patterns** | 🌌 Antigravity (634+) | Build production Apache Airflow DAGs with best practices for operators, sensors, testing, and deployment. Use when creating data pipelines, orchestrat… | `sources/06-antigravity/airflow-dag-patterns/` |
| **api-testing-observability-api-mock** | 🌌 Antigravity (634+) | You are an API mocking expert specializing in realistic mock services for development, testing, and demos. Design mocks that simulate real API behavio… | `sources/06-antigravity/api-testing-observability-api-mock/` |
| **backtesting-frameworks** | 🌌 Antigravity (634+) | Build robust backtesting systems for trading strategies with proper handling of look-ahead bias, survivorship bias, and transaction costs. Use when de… | `sources/06-antigravity/backtesting-frameworks/` |
| **bats-testing-patterns** | 🌌 Antigravity (634+) | Master Bash Automated Testing System (Bats) for comprehensive shell script testing. Use when writing tests for shell scripts, CI/CD pipelines, or requ… | `sources/06-antigravity/bats-testing-patterns/` |
| **browser-automation** | 🌌 Antigravity (634+) | Browser automation powers web testing, scraping, and AI agent interactions. The difference between a flaky script and a reliable system comes down to … | `sources/06-antigravity/browser-automation/` |
| **bun-development** | 🌌 Antigravity (634+) | Modern JavaScript/TypeScript development with Bun runtime. Covers package management, bundling, testing, and migration from Node.js. Use when working … | `sources/06-antigravity/bun-development/` |
| **conductor-implement** | 🌌 Antigravity (634+) | Execute tasks from a track's implementation plan following TDD workflow | `sources/06-antigravity/conductor-implement/` |
| **context7-auto-research** | 🌌 Antigravity (634+) | Automatically fetch latest library/framework documentation for Claude Code via Context7 API | `sources/06-antigravity/context7-auto-research/` |
| **copywriting** | 🌌 Antigravity (634+) | Use this skill when writing, rewriting, or improving marketing copy for any page (homepage, landing page, pricing, feature, product, or about page). T… | `sources/06-antigravity/copywriting/` |
| **data-engineering-data-driven-feature** | 🌌 Antigravity (634+) | Build features guided by data insights, A/B testing, and continuous measurement using specialized agents for analysis, implementation, and experimenta… | `sources/06-antigravity/data-engineering-data-driven-feature/` |
| **data-quality-frameworks** | 🌌 Antigravity (634+) | Implement data quality validation with Great Expectations, dbt tests, and data contracts. Use when building data quality pipelines, implementing valid… | `sources/06-antigravity/data-quality-frameworks/` |
| **dbt-transformation-patterns** | 🌌 Antigravity (634+) | Master dbt (data build tool) for analytics engineering with model organization, testing, documentation, and incremental strategies. Use when building … | `sources/06-antigravity/dbt-transformation-patterns/` |
| **debugger** | 🌌 Antigravity (634+) | Debugging specialist for errors, test failures, and unexpected | `sources/06-antigravity/debugger/` |
| **dependency-upgrade** | 🌌 Antigravity (634+) | Manage major dependency version upgrades with compatibility analysis, staged rollout, and comprehensive testing. Use when upgrading framework versions… | `sources/06-antigravity/dependency-upgrade/` |
| **deployment-validation-config-validate** | 🌌 Antigravity (634+) | You are a configuration management expert specializing in validating, testing, and ensuring the correctness of application configurations. Create comp… | `sources/06-antigravity/deployment-validation-config-validate/` |
| **e2e-testing-patterns** | 🌌 Antigravity (634+) | Master end-to-end testing with Playwright and Cypress to build reliable test suites that catch bugs, improve confidence, and enable fast deployment. U… | `sources/06-antigravity/e2e-testing-patterns/` |
| **finishing-a-development-branch** | 🌌 Antigravity (634+) | Use when implementation is complete, all tests pass, and you need to decide how to integrate the work - guides completion of development work by prese… | `sources/06-antigravity/finishing-a-development-branch/` |
| **framework-migration-deps-upgrade** | 🌌 Antigravity (634+) | You are a dependency management expert specializing in safe, incremental upgrades of project dependencies. Plan and execute dependency updates with mi… | `sources/06-antigravity/framework-migration-deps-upgrade/` |
| **frontend-mobile-development-component-scaffold** | 🌌 Antigravity (634+) | You are a React component architecture expert specializing in scaffolding production-ready, accessible, and performant components. Generate complete c… | `sources/06-antigravity/frontend-mobile-development-component-scaffold/` |
| **git-pr-workflows-git-workflow** | 🌌 Antigravity (634+) | Orchestrate a comprehensive git workflow from code review through PR creation, leveraging specialized agents for quality assurance, testing, and deplo… | `sources/06-antigravity/git-pr-workflows-git-workflow/` |
| **github-actions-templates** | 🌌 Antigravity (634+) | Create production-ready GitHub Actions workflows for automated testing, building, and deploying applications. Use when setting up CI/CD with GitHub Ac… | `sources/06-antigravity/github-actions-templates/` |
| **gitlab-ci-patterns** | 🌌 Antigravity (634+) | Build GitLab CI/CD pipelines with multi-stage workflows, caching, and distributed runners for scalable automation. Use when implementing GitLab CI/CD,… | `sources/06-antigravity/gitlab-ci-patterns/` |
| **Infinite Gratitude** | 🌌 Antigravity (634+) | Multi-agent research skill for parallel research execution (10 agents, battle-tested with real case studies). | `sources/06-antigravity/infinite-gratitude/` |
| **javascript-testing-patterns** | 🌌 Antigravity (634+) | Implement comprehensive testing strategies using Jest, Vitest, and Testing Library for unit tests, integration tests, and end-to-end testing with mock… | `sources/06-antigravity/javascript-testing-patterns/` |
| **llm-evaluation** | 🌌 Antigravity (634+) | Implement comprehensive evaluation strategies for LLM applications using automated metrics, human feedback, and benchmarking. Use when testing LLM per… | `sources/06-antigravity/llm-evaluation/` |
| **Network 101** | 🌌 Antigravity (634+) | This skill should be used when the user asks to "set up a web server", "configure HTTP or HTTPS", "perform SNMP enumeration", "configure SMB shares", … | `sources/06-antigravity/network-101/` |
| **performance-testing-review-ai-review** | 🌌 Antigravity (634+) | You are an expert AI-powered code review specialist combining automated static analysis, intelligent pattern recognition, and modern DevOps practices.… | `sources/06-antigravity/performance-testing-review-ai-review/` |
| **performance-testing-review-multi-agent-review** | 🌌 Antigravity (634+) | Use when working with performance testing review multi agent review | `sources/06-antigravity/performance-testing-review-multi-agent-review/` |
| **playwright-skill** | 🌌 Antigravity (634+) | Complete browser automation with Playwright. Auto-detects dev servers, writes clean test scripts to /tmp. Test pages, fill forms, take screenshots, ch… | `sources/06-antigravity/playwright-skill/` |
| **pypict-skill** | 🌌 Antigravity (634+) | Pairwise test generation | `sources/06-antigravity/pypict-skill/` |
| **python-testing-patterns** | 🌌 Antigravity (634+) | Implement comprehensive testing strategies with pytest, fixtures, mocking, and test-driven development. Use when writing Python tests, setting up test… | `sources/06-antigravity/python-testing-patterns/` |
| **quant-analyst** | 🌌 Antigravity (634+) | Build financial models, backtest trading strategies, and analyze | `sources/06-antigravity/quant-analyst/` |
| **react-modernization** | 🌌 Antigravity (634+) | Upgrade React applications to latest versions, migrate from class components to hooks, and adopt concurrent features. Use when modernizing React codeb… | `sources/06-antigravity/react-modernization/` |
| **screen-reader-testing** | 🌌 Antigravity (634+) | Test web applications with screen readers including VoiceOver, NVDA, and JAWS. Use when validating screen reader compatibility, debugging accessibilit… | `sources/06-antigravity/screen-reader-testing/` |
| **screenshots** | 🌌 Antigravity (634+) | Generate marketing screenshots of your app using Playwright. Use when the user wants to create screenshots for Product Hunt, social media, landing pag… | `sources/06-antigravity/screenshots/` |
| **systematic-debugging** | 🌌 Antigravity (634+) | Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes | `sources/06-antigravity/systematic-debugging/` |
| **systems-programming-rust-project** | 🌌 Antigravity (634+) | You are a Rust project architecture expert specializing in scaffolding production-ready Rust applications. Generate complete project structures with c… | `sources/06-antigravity/systems-programming-rust-project/` |
| **tdd-orchestrator** | 🌌 Antigravity (634+) | Master TDD orchestrator specializing in red-green-refactor | `sources/06-antigravity/tdd-orchestrator/` |
| **tdd-workflow** | 🌌 Antigravity (634+) | Test-Driven Development workflow principles. RED-GREEN-REFACTOR cycle. | `sources/06-antigravity/tdd-workflow/` |
| **tdd-workflows-tdd-cycle** | 🌌 Antigravity (634+) | Use when working with tdd workflows tdd cycle | `sources/06-antigravity/tdd-workflows-tdd-cycle/` |
| **tdd-workflows-tdd-green** | 🌌 Antigravity (634+) | Implement the minimal code needed to make failing tests pass in the TDD green phase. | `sources/06-antigravity/tdd-workflows-tdd-green/` |
| **tdd-workflows-tdd-red** | 🌌 Antigravity (634+) | Generate failing tests for the TDD red phase to define expected behavior and edge cases. | `sources/06-antigravity/tdd-workflows-tdd-red/` |
| **tdd-workflows-tdd-refactor** | 🌌 Antigravity (634+) | Use when working with tdd workflows tdd refactor | `sources/06-antigravity/tdd-workflows-tdd-refactor/` |
| **temporal-python-testing** | 🌌 Antigravity (634+) | Test Temporal workflows with pytest, time-skipping, and mocking strategies. Covers unit testing, integration testing, replay testing, and local develo… | `sources/06-antigravity/temporal-python-testing/` |
| **test-automator** | 🌌 Antigravity (634+) | Master AI-powered test automation with modern frameworks, | `sources/06-antigravity/test-automator/` |
| **test-driven-development** | 🌌 Antigravity (634+) | Use when implementing any feature or bugfix, before writing implementation code | `sources/06-antigravity/test-driven-development/` |
| **test-fixing** | 🌌 Antigravity (634+) | Run tests and systematically fix all failing tests using smart error grouping. Use when user asks to fix failing tests, mentions test failures, runs t… | `sources/06-antigravity/test-fixing/` |
| **testing-patterns** | 🌌 Antigravity (634+) | Jest testing patterns, factory functions, mocking strategies, and TDD workflow. Use when writing unit tests, creating test factories, or following TDD… | `sources/06-antigravity/testing-patterns/` |
| **ui-visual-validator** | 🌌 Antigravity (634+) | Rigorous visual validation expert specializing in UI testing, | `sources/06-antigravity/ui-visual-validator/` |
| **unit-testing-test-generate** | 🌌 Antigravity (634+) | Generate comprehensive, maintainable unit tests across languages with strong coverage and edge case focus. | `sources/06-antigravity/unit-testing-test-generate/` |
| **viral-generator-builder** | 🌌 Antigravity (634+) | Expert in building shareable generator tools that go viral - name generators, quiz makers, avatar creators, personality tests, and calculator tools. C… | `sources/06-antigravity/viral-generator-builder/` |
| **web3-testing** | 🌌 Antigravity (634+) | Test smart contracts comprehensively using Hardhat and Foundry with unit tests, integration tests, and mainnet forking. Use when testing Solidity cont… | `sources/06-antigravity/web3-testing/` |
| **webapp-testing** | 🌌 Antigravity (634+) | Toolkit for interacting with and testing local web applications using Playwright. Supports verifying frontend functionality, debugging UI behavior, ca… | `sources/06-antigravity/webapp-testing/` |
| **workflow-patterns** | 🌌 Antigravity (634+) | Use this skill when implementing tasks according to Conductor's TDD | `sources/06-antigravity/workflow-patterns/` |
| **bun-development** | 📦 skills | Bun runtime patterns, bundler configuration, and Bun-specific APIs. Trigger on Bun FFI, Bun.serve, Bun.file, Bun shell, workspace configuration, Bun-s… | `skills/bun-development/` |
| **context7-docs-first** | 📦 skills | Ground all platform and library answers in current official documentation by using Context7 MCP tools before responding. TRIGGER when: user asks about… | `skills/context7-docs-first/` |
| **e2e-testing-patterns** | 📦 skills | End-to-end testing with Playwright for Next.js applications. Trigger on E2E test setup, cross-page flow testing (checkout, onboarding, multi-step form… | `skills/e2e-testing-patterns/` |
| **epic-decomposer** | 📦 skills | Decompõe specs, PRDs ou requisitos em épicos e stories implementáveis. Cada story com ACs testáveis, tasks com file paths, e dependências mapeadas. | `skills/planning/epic-decomposer/` |
| **offensive-oauth** | 📦 skills | OAuth 2.0 attack checklist: authorization code interception, redirect_uri bypass, CSRF on OAuth flow, state parameter abuse, open redirector chaining,… | `skills/offensive-oauth/` |
| **offensive-oauth** | 🛡️ Claude-Red (Offensive Security) | OAuth 2.0 attack checklist: authorization code interception, redirect_uri bypass, CSRF on OAuth flow, state parameter abuse, open redirector chaining,… | `sources/13-claude-red/offensive-oauth/` |
| **offensive-reporting** | 📦 skills | Penetration test and red team report writing methodology. Covers executive summary structuring (risk-led narrative for non-technical readers), technic… | `skills/offensive-reporting/` |
| **offensive-reporting** | 🛡️ Claude-Red (Offensive Security) | Penetration test and red team report writing methodology. Covers executive summary structuring (risk-led narrative for non-technical readers), technic… | `sources/13-claude-red/offensive-reporting/` |
| **offensive-ssrf** | 📦 skills | Server-Side Request Forgery testing checklist: SSRF discovery, blind SSRF with out-of-band, cloud metadata endpoints (AWS/GCP/Azure), SSRF filter bypa… | `skills/offensive-ssrf/` |
| **offensive-ssrf** | 🛡️ Claude-Red (Offensive Security) | Server-Side Request Forgery testing checklist: SSRF discovery, blind SSRF with out-of-band, cloud metadata endpoints (AWS/GCP/Azure), SSRF filter bypa… | `sources/13-claude-red/offensive-ssrf/` |
| **output-enforcement** | 📦 skills | Camada de enhancement OSForge sobre full-output-enforcement: além do output completo, exige verification gate antes de declarar done e proteção TDD (n… | `skills/output-enforcement/` |
| **predictive-failure** | 📦 skills | Analyze implemented code to predict potential failure points that tests may not catch. Uses pattern matching against common production failure modes. … | `skills/predictive-failure/` |
| **skill-creator** | 📦 skills | Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from scratch, update or op… | `skills/skill-creator/` |
| **spec-builder** | 📦 skills | Facilitação colaborativa de tech spec com ACs testáveis. ACIONE quando: especificar uma feature, definir o que construir, escrever spec técnica, detal… | `skills/planning/spec-builder/` |
| **tdd-workflow** | 📦 skills | Enforces Test-Driven Development (RED-GREEN-REFACTOR) workflow. Use when implementing any feature, bugfix, or behavior change. Ensures tests are writt… | `skills/tdd-workflow/` |
| **technical-design-doc-creator** | 📦 skills | Creates comprehensive Technical Design Documents (TDD) following industry standards with mandatory sections, optional sections, and interactive gather… | `skills/technical-design-doc-creator/` |
| **testing-patterns** | 📦 skills | Padrões e princípios de testes unitários e de integração: pirâmide de testes, padrão AAA, estratégias de mocking, organização e dados de teste. ACIONE… | `skills/testing-patterns/` |
| **using-git-worktrees** | 📦 skills | Setup e uso de git worktrees para desenvolvimento paralelo. ACIONE quando: trabalhar em múltiplas features simultaneamente, precisar de branches isola… | `skills/using-git-worktrees/` |
| **vercel-deploy** | 📦 skills | Deploy applications and websites to Vercel. Use when the user requests deployment actions like "deploy my app", "deploy and give me the link", "push t… | `skills/vercel-deploy/` |

## 🏗️ Architecture

**63 skills**

| Skill | Origem | Descrição | Path Local |
|-------|--------|-----------|-----------|
| **architect-review** | 🌌 Antigravity (634+) | Master software architect specializing in modern architecture | `sources/06-antigravity/architect-review/` |
| **architecture-decision-records** | 🌌 Antigravity (634+) | Write and maintain Architecture Decision Records (ADRs) following best practices for technical decision documentation. Use when documenting significan… | `sources/06-antigravity/architecture-decision-records/` |
| **async-python-patterns** | 🌌 Antigravity (634+) | Master Python asyncio, concurrent programming, and async/await patterns for high-performance applications. Use when building async APIs, concurrent sy… | `sources/06-antigravity/async-python-patterns/` |
| **backend-architect** | 🌌 Antigravity (634+) | Expert backend architect specializing in scalable API design, | `sources/06-antigravity/backend-architect/` |
| **bash-linux** | 🌌 Antigravity (634+) | Bash/Linux terminal patterns. Critical commands, piping, error handling, scripting. Use when working on macOS or Linux systems. | `sources/06-antigravity/bash-linux/` |
| **bazel-build-optimization** | 🌌 Antigravity (634+) | Optimize Bazel builds for large-scale monorepos. Use when configuring Bazel, implementing remote execution, or optimizing build performance for enterp… | `sources/06-antigravity/bazel-build-optimization/` |
| **binary-analysis-patterns** | 🌌 Antigravity (634+) | Master binary analysis patterns including disassembly, decompilation, control flow analysis, and code pattern recognition. Use when analyzing executab… | `sources/06-antigravity/binary-analysis-patterns/` |
| **browser-extension-builder** | 🌌 Antigravity (634+) | Expert in building browser extensions that solve real problems - Chrome, Firefox, and cross-browser extensions. Covers extension architecture, manifes… | `sources/06-antigravity/browser-extension-builder/` |
| **c4-architecture-c4-architecture** | 🌌 Antigravity (634+) | Generate comprehensive C4 architecture documentation for an existing repository/codebase using a bottom-up analysis approach. | `sources/06-antigravity/c4-architecture-c4-architecture/` |
| **c4-code** | 🌌 Antigravity (634+) | Expert C4 Code-level documentation specialist. Analyzes code | `sources/06-antigravity/c4-code/` |
| **c4-container** | 🌌 Antigravity (634+) | Expert C4 Container-level documentation specialist. Synthesizes | `sources/06-antigravity/c4-container/` |
| **clerk-auth** | 🌌 Antigravity (634+) | Expert patterns for Clerk auth implementation, middleware, organizations, webhooks, and user sync Use when: adding authentication, clerk auth, user au… | `sources/06-antigravity/clerk-auth/` |
| **code-refactoring-refactor-clean** | 🌌 Antigravity (634+) | You are a code refactoring expert specializing in clean code principles, SOLID design patterns, and modern software engineering best practices. Analyz… | `sources/06-antigravity/code-refactoring-refactor-clean/` |
| **codebase-cleanup-refactor-clean** | 🌌 Antigravity (634+) | You are a code refactoring expert specializing in clean code principles, SOLID design patterns, and modern software engineering best practices. Analyz… | `sources/06-antigravity/codebase-cleanup-refactor-clean/` |
| **csharp-pro** | 🌌 Antigravity (634+) | Write modern C# code with advanced features like records, pattern | `sources/06-antigravity/csharp-pro/` |
| **data-engineering-data-pipeline** | 🌌 Antigravity (634+) | You are a data pipeline architecture expert specializing in scalable, reliable, and cost-effective data pipelines for batch and streaming data process… | `sources/06-antigravity/data-engineering-data-pipeline/` |
| **distributed-tracing** | 🌌 Antigravity (634+) | Implement distributed tracing with Jaeger and Tempo to track requests across microservices and identify performance bottlenecks. Use when debugging mi… | `sources/06-antigravity/distributed-tracing/` |
| **docs-architect** | 🌌 Antigravity (634+) | Creates comprehensive technical documentation from existing | `sources/06-antigravity/docs-architect/` |
| **dotnet-architect** | 🌌 Antigravity (634+) | Expert .NET backend architect specializing in C#, ASP.NET Core, | `sources/06-antigravity/dotnet-architect/` |
| **elixir-pro** | 🌌 Antigravity (634+) | Write idiomatic Elixir code with OTP patterns, supervision trees, | `sources/06-antigravity/elixir-pro/` |
| **error-detective** | 🌌 Antigravity (634+) | Search logs and codebases for error patterns, stack traces, and | `sources/06-antigravity/error-detective/` |
| **error-handling-patterns** | 🌌 Antigravity (634+) | Master error handling patterns across languages including exceptions, Result types, error propagation, and graceful degradation to build resilient app… | `sources/06-antigravity/error-handling-patterns/` |
| **fp-ts-errors** | 🌌 Antigravity (634+) | Handle errors as values using fp-ts Either and TaskEither for cleaner, more predictable TypeScript code. Use when implementing error handling patterns… | `sources/06-antigravity/fp-ts-errors/` |
| **git-pr-workflows-onboard** | 🌌 Antigravity (634+) | You are an **expert onboarding specialist and knowledge transfer architect** with deep experience in remote-first organizations, technical team integr… | `sources/06-antigravity/git-pr-workflows-onboard/` |
| **godot-gdscript-patterns** | 🌌 Antigravity (634+) | Master Godot 4 GDScript patterns including signals, scenes, state machines, and optimization. Use when building Godot games, implementing game systems… | `sources/06-antigravity/godot-gdscript-patterns/` |
| **golang-pro** | 🌌 Antigravity (634+) | Master Go 1.21+ with modern patterns, advanced concurrency, | `sources/06-antigravity/golang-pro/` |
| **hubspot-integration** | 🌌 Antigravity (634+) | Expert patterns for HubSpot CRM integration including OAuth authentication, CRM objects, associations, batch operations, webhooks, and custom objects.… | `sources/06-antigravity/hubspot-integration/` |
| **i18n-localization** | 🌌 Antigravity (634+) | Internationalization and localization patterns. Detecting hardcoded strings, managing translations, locale files, RTL support. | `sources/06-antigravity/i18n-localization/` |
| **java-pro** | 🌌 Antigravity (634+) | Master Java 21+ with modern features like virtual threads, pattern | `sources/06-antigravity/java-pro/` |
| **javascript-mastery** | 🌌 Antigravity (634+) | Comprehensive JavaScript reference covering 33+ essential concepts every developer should know. From fundamentals like primitives and closures to adva… | `sources/06-antigravity/javascript-mastery/` |
| **javascript-pro** | 🌌 Antigravity (634+) | Master modern JavaScript with ES6+, async patterns, and Node.js | `sources/06-antigravity/javascript-pro/` |
| **kpi-dashboard-design** | 🌌 Antigravity (634+) | Design effective KPI dashboards with metrics selection, visualization best practices, and real-time monitoring patterns. Use when building business da… | `sources/06-antigravity/kpi-dashboard-design/` |
| **makepad-skills** | 🌌 Antigravity (634+) | Makepad UI development skills for Rust apps: setup, patterns, shaders, packaging, and troubleshooting. | `sources/06-antigravity/makepad-skills/` |
| **microservices-patterns** | 🌌 Antigravity (634+) | Design microservices architectures with service boundaries, event-driven communication, and resilience patterns. Use when building distributed systems… | `sources/06-antigravity/microservices-patterns/` |
| **modern-javascript-patterns** | 🌌 Antigravity (634+) | Master ES6+ features including async/await, destructuring, spread operators, arrow functions, promises, modules, iterators, generators, and functional… | `sources/06-antigravity/modern-javascript-patterns/` |
| **monorepo-architect** | 🌌 Antigravity (634+) | Expert in monorepo architecture, build systems, and dependency management at scale. Masters Nx, Turborepo, Bazel, and Lerna for efficient multi-projec… | `sources/06-antigravity/monorepo-architect/` |
| **monorepo-management** | 🌌 Antigravity (634+) | Master monorepo management with Turborepo, Nx, and pnpm workspaces to build efficient, scalable multi-package repositories with optimized builds and d… | `sources/06-antigravity/monorepo-management/` |
| **multiplayer** | 🌌 Antigravity (634+) | Multiplayer game development principles. Architecture, networking, synchronization. | `sources/06-antigravity/game-development/multiplayer/` |
| **n8n-mcp-tools-expert** | 🌌 Antigravity (634+) | Expert guide for using n8n-mcp MCP tools effectively. Use when searching for nodes, validating configurations, accessing templates, managing workflows… | `sources/06-antigravity/n8n-mcp-tools-expert/` |
| **n8n-node-configuration** | 🌌 Antigravity (634+) | Operation-aware node configuration guidance. Use when configuring nodes, understanding property dependencies, determining required fields, choosing be… | `sources/06-antigravity/n8n-node-configuration/` |
| **nx-workspace-patterns** | 🌌 Antigravity (634+) | Configure and optimize Nx monorepo workspaces. Use when setting up Nx, configuring project boundaries, optimizing build caching, or implementing affec… | `sources/06-antigravity/nx-workspace-patterns/` |
| **openapi-spec-generation** | 🌌 Antigravity (634+) | Generate and maintain OpenAPI 3.1 specifications from code, design-first specs, and validation patterns. Use when creating API documentation, generati… | `sources/06-antigravity/openapi-spec-generation/` |
| **plaid-fintech** | 🌌 Antigravity (634+) | Expert patterns for Plaid API integration including Link token flows, transactions sync, identity verification, Auth for ACH, balance checks, webhook … | `sources/06-antigravity/plaid-fintech/` |
| **powershell-windows** | 🌌 Antigravity (634+) | PowerShell Windows patterns. Critical pitfalls, operator syntax, error handling. | `sources/06-antigravity/powershell-windows/` |
| **programmatic-seo** | 🌌 Antigravity (634+) | Design and evaluate programmatic SEO strategies for creating SEO-driven pages at scale using templates and structured data. Use when the user mentions… | `sources/06-antigravity/programmatic-seo/` |
| **python-patterns** | 🌌 Antigravity (634+) | Python development principles and decision-making. Framework selection, async patterns, type hints, project structure. Teaches thinking, not copying. | `sources/06-antigravity/python-patterns/` |
| **rust-async-patterns** | 🌌 Antigravity (634+) | Master Rust async programming with Tokio, async traits, error handling, and concurrent patterns. Use when building async Rust applications, implementi… | `sources/06-antigravity/rust-async-patterns/` |
| **rust-pro** | 🌌 Antigravity (634+) | Master Rust 1.75+ with modern async patterns, advanced type system | `sources/06-antigravity/rust-pro/` |
| **saga-orchestration** | 🌌 Antigravity (634+) | Implement saga patterns for distributed transactions and cross-aggregate workflows. Use when coordinating multi-step business processes, handling comp… | `sources/06-antigravity/saga-orchestration/` |
| **segment-cdp** | 🌌 Antigravity (634+) | Expert patterns for Segment Customer Data Platform including Analytics.js, server-side tracking, tracking plans with Protocols, identity resolution, d… | `sources/06-antigravity/segment-cdp/` |
| **seo-structure-architect** | 🌌 Antigravity (634+) | Analyzes and optimizes content structure including header | `sources/06-antigravity/seo-structure-architect/` |
| **skill-developer** | 🌌 Antigravity (634+) | Create and manage Claude Code skills following Anthropic best practices. Use when creating new skills, modifying skill-rules.json, understanding trigg… | `sources/06-antigravity/skill-developer/` |
| **software-architecture** | 🌌 Antigravity (634+) | Guide for quality focused software architecture. This skill should be used when users want to write code, design architecture, analyze code, in any ca… | `sources/06-antigravity/software-architecture/` |
| **turborepo-caching** | 🌌 Antigravity (634+) | Configure Turborepo for efficient monorepo builds with local and remote caching. Use when setting up Turborepo, optimizing build pipelines, or impleme… | `sources/06-antigravity/turborepo-caching/` |
| **typescript-expert** | 🌌 Antigravity (634+) | TypeScript and JavaScript expert with deep knowledge of type-level programming, performance optimization, monorepo management, migration strategies, a… | `sources/06-antigravity/typescript-expert/` |
| **unreal-engine-cpp-pro** | 🌌 Antigravity (634+) | Expert guide for Unreal Engine 5.x C++ development, covering UObject hygiene, performance patterns, and best practices. | `sources/06-antigravity/unreal-engine-cpp-pro/` |
| **workflow-orchestration-patterns** | 🌌 Antigravity (634+) | Design durable workflows with Temporal for distributed systems. Covers workflow vs activity separation, saga patterns, state management, and determini… | `sources/06-antigravity/workflow-orchestration-patterns/` |
| **zapier-make-patterns** | 🌌 Antigravity (634+) | No-code automation democratizes workflow building. Zapier and Make (formerly Integromat) let non-developers automate business processes without writin… | `sources/06-antigravity/zapier-make-patterns/` |
| **architecture** | 📦 skills | Framework de decisão arquitetural com análise de requisitos, avaliação de trade-offs e documentação em ADRs. ACIONE quando: decidir entre X e Y (monol… | `skills/architecture/` |
| **bash-linux** | 📦 skills | Padrões de terminal Bash para Linux e macOS: comandos essenciais, pipes, processos, processamento de texto e scripts seguros. ACIONE quando: script ba… | `skills/bash-linux/` |
| **osforge-evolve** | 📦 skills | ACIONE quando: evolve, /evolve, osforge evolve, analisar observações, propor skills, clustering de padrões, instinct, promover instinct, aprendizado c… | `skills/evolve/` |
| **powershell-windows** | 📦 skills | Padrões e armadilhas críticas de PowerShell no Windows: sintaxe de operadores, null checks, JSON, paths e error handling. ACIONE quando: script PowerS… | `skills/powershell-windows/` |
| **readiness-gate** | 📦 skills | Quality gate pré-implementação. Valida que PRD, Architecture e Épicos estão alinhados e completos antes de iniciar o sprint loop. Use com: | `skills/quality/readiness-gate/` |

## 📝 Documentation / Writing

**59 skills**

| Skill | Origem | Descrição | Path Local |
|-------|--------|-----------|-----------|
| **brand-guidelines** | 🟣 Anthropic (Oficial) | Applies Anthropic's official brand colors and typography to any sort of artifact that may benefit from having Anthropic's look-and-feel. Use it when b… | `sources/01-anthropic/brand-guidelines/` |
| **canvas-design** | 🟣 Anthropic (Oficial) | Create beautiful visual art in .png and .pdf documents using design philosophy. You should use this skill when the user asks to create a poster, piece… | `sources/01-anthropic/canvas-design/` |
| **docx** | 🟣 Anthropic (Oficial) | Use this skill whenever the user wants to create, read, edit, or manipulate Word documents (.docx files). Triggers include: any mention of \ | `sources/01-anthropic/docx/` |
| **internal-comms** | 🟣 Anthropic (Oficial) | A set of resources to help me write all kinds of internal communications, using the formats that my company likes to use. Claude should use this skill… | `sources/01-anthropic/internal-comms/` |
| **pptx** | 🟣 Anthropic (Oficial) | Use this skill any time a .pptx file is involved in any way — as input, output, or both. This includes: creating slide decks, pitch decks, or presenta… | `sources/01-anthropic/pptx/` |
| **writing-plans** | 🔵 Superpowers (obra) | Use when you have a spec or requirements for a multi-step task, before touching code | `sources/02-superpowers/writing-plans/` |
| **modern-python** | 🔒 Trail of Bits | Configures Python projects with modern tooling (uv, ruff, ty). Use when creating projects, writing standalone scripts, or migrating from pip/Poetry/my… | `sources/07-trailofbits/modern-python/skills/modern-python/` |
| **brand-guidelines** | 🔴 Sentry | Write copy following Sentry brand guidelines. Use when writing UI text, error messages, empty states, onboarding flows, 404 pages, documentation, mark… | `sources/11-sentry/brand-guidelines/` |
| **commit** | 🔴 Sentry | Create commit messages following Sentry conventions. Use when committing code changes, writing commit messages, or formatting git history. Follows con… | `sources/11-sentry/commit/` |
| **create-pr** | 🔴 Sentry | Create pull requests following Sentry conventions. Use when opening PRs, writing PR descriptions, or preparing changes for review. Follows Sentry's co… | `sources/11-sentry/create-pr/` |
| **angular-best-practices** | 🌌 Antigravity (634+) | Angular performance optimization and best practices guide. Use when writing, reviewing, or refactoring Angular code for optimal performance, bundle si… | `sources/06-antigravity/angular-best-practices/` |
| **api-documentation-generator** | 🌌 Antigravity (634+) | Generate comprehensive, developer-friendly API documentation from code, including endpoints, parameters, examples, and best practices | `sources/06-antigravity/api-documentation-generator/` |
| **beautiful-prose** | 🌌 Antigravity (634+) | Hard-edged writing style contract for timeless, forceful English prose without AI tics | `sources/06-antigravity/beautiful-prose/` |
| **brand-guidelines** | 🌌 Antigravity (634+) | Applies Anthropic's official brand colors and typography to any sort of artifact that may benefit from having Anthropic's look-and-feel. Use it when b… | `sources/06-antigravity/brand-guidelines-anthropic/` |
| **brand-guidelines** | 🌌 Antigravity (634+) | Applies Anthropic's official brand colors and typography to any sort of artifact that may benefit from having Anthropic's look-and-feel. Use it when b… | `sources/06-antigravity/brand-guidelines-community/` |
| **canvas-design** | 🌌 Antigravity (634+) | Create beautiful visual art in .png and .pdf documents using design philosophy. You should use this skill when the user asks to create a poster, piece… | `sources/06-antigravity/canvas-design/` |
| **changelog-automation** | 🌌 Antigravity (634+) | Automate changelog generation from commits, PRs, and releases following Keep a Changelog format. Use when setting up release workflows, generating rel… | `sources/06-antigravity/changelog-automation/` |
| **code-documentation-code-explain** | 🌌 Antigravity (634+) | You are a code education expert specializing in explaining complex code through clear narratives, visual diagrams, and step-by-step breakdowns. Transf… | `sources/06-antigravity/code-documentation-code-explain/` |
| **codex-review** | 🌌 Antigravity (634+) | Professional code review with auto CHANGELOG generation, integrated with Codex AI | `sources/06-antigravity/codex-review/` |
| **commit** | 🌌 Antigravity (634+) | Create commit messages following Sentry conventions. Use when committing code changes, writing commit messages, or formatting git history. Follows con… | `sources/06-antigravity/commit/` |
| **content-creator** | 🌌 Antigravity (634+) | Create SEO-optimized marketing content with consistent brand voice. Includes brand voice analyzer, SEO optimizer, content frameworks, and social media… | `sources/06-antigravity/content-creator/` |
| **create-pr** | 🌌 Antigravity (634+) | Create pull requests following Sentry conventions. Use when opening PRs, writing PR descriptions, or preparing changes for review. Follows Sentry | `sources/06-antigravity/create-pr/` |
| **culture-index** | 🌌 Antigravity (634+) | Index and search culture documentation | `sources/06-antigravity/culture-index/` |
| **daily-news-report** | 🌌 Antigravity (634+) | Scrapes content based on a preset URL list, filters high-quality technical information, and generates daily Markdown reports. | `sources/06-antigravity/daily-news-report/` |
| **docx** | 🌌 Antigravity (634+) | Comprehensive document creation, editing, and analysis with support for tracked changes, comments, formatting preservation, and text extraction. When … | `sources/06-antigravity/docx-official/` |
| **employment-contract-templates** | 🌌 Antigravity (634+) | Create employment contracts, offer letters, and HR policy documents following legal best practices. Use when drafting employment agreements, creating … | `sources/06-antigravity/employment-contract-templates/` |
| **exa-search** | 🌌 Antigravity (634+) | Semantic search, similar content discovery, and structured research using Exa API | `sources/06-antigravity/exa-search/` |
| **free-tool-strategy** | 🌌 Antigravity (634+) | When the user wants to plan, evaluate, or build a free tool for marketing purposes — lead generation, SEO value, or brand awareness. Also use when the… | `sources/06-antigravity/free-tool-strategy/` |
| **internal-comms** | 🌌 Antigravity (634+) | A set of resources to help me write all kinds of internal communications, using the formats that my company likes to use. Claude should use this skill… | `sources/06-antigravity/internal-comms-anthropic/` |
| **internal-comms** | 🌌 Antigravity (634+) | A set of resources to help me write all kinds of internal communications, using the formats that my company likes to use. Claude should use this skill… | `sources/06-antigravity/internal-comms-community/` |
| **n8n-code-python** | 🌌 Antigravity (634+) | Write Python code in n8n Code nodes. Use when writing Python in n8n, using _input/_json/_node syntax, working with standard library, or need to unders… | `sources/06-antigravity/n8n-code-python/` |
| **notebooklm** | 🌌 Antigravity (634+) | Use this skill to query your Google NotebookLM notebooks directly from Claude Code for source-grounded, citation-backed answers from Gemini. Browser a… | `sources/06-antigravity/notebooklm/` |
| **obsidian-clipper-template-creator** | 🌌 Antigravity (634+) | Guide for creating templates for the Obsidian Web Clipper. Use when you want to create a new clipping template, understand available variables, or for… | `sources/06-antigravity/obsidian-clipper-template-creator/` |
| **pdf** | 🌌 Antigravity (634+) | Comprehensive PDF manipulation toolkit for extracting text and tables, creating new PDFs, merging/splitting documents, and handling forms. When Claude… | `sources/06-antigravity/pdf-official/` |
| **plan-writing** | 🌌 Antigravity (634+) | Structured task planning with clear breakdowns, dependencies, and verification criteria. Use when implementing features, refactoring, or any multi-ste… | `sources/06-antigravity/plan-writing/` |
| **popup-cro** | 🌌 Antigravity (634+) | Create and optimize popups, modals, overlays, slide-ins, and banners to increase conversions without harming user experience or brand trust. | `sources/06-antigravity/popup-cro/` |
| **postmortem-writing** | 🌌 Antigravity (634+) | Write effective blameless postmortems with root cause analysis, timelines, and action items. Use when conducting incident reviews, writing postmortem … | `sources/06-antigravity/postmortem-writing/` |
| **pptx** | 🌌 Antigravity (634+) | Presentation creation, editing, and analysis. When Claude needs to work with presentations (.pptx files) for: (1) Creating new presentations, (2) Modi… | `sources/06-antigravity/pptx-official/` |
| **product-manager-toolkit** | 🌌 Antigravity (634+) | Comprehensive toolkit for product managers including RICE prioritization, customer interview analysis, PRD templates, discovery frameworks, and go-to-… | `sources/06-antigravity/product-manager-toolkit/` |
| **protocol-reverse-engineering** | 🌌 Antigravity (634+) | Master network protocol reverse engineering including packet analysis, protocol dissection, and custom protocol documentation. Use when analyzing netw… | `sources/06-antigravity/protocol-reverse-engineering/` |
| **readme** | 🌌 Antigravity (634+) | When the user wants to create or update a README.md file for a project. Also use when the user says | `sources/06-antigravity/readme/` |
| **reference-builder** | 🌌 Antigravity (634+) | Creates exhaustive technical references and API documentation. | `sources/06-antigravity/reference-builder/` |
| **seo-authority-builder** | 🌌 Antigravity (634+) | Analyzes content for E-E-A-T signals and suggests improvements to | `sources/06-antigravity/seo-authority-builder/` |
| **seo-content-planner** | 🌌 Antigravity (634+) | Creates comprehensive content outlines and topic clusters for SEO. | `sources/06-antigravity/seo-content-planner/` |
| **seo-content-refresher** | 🌌 Antigravity (634+) | Identifies outdated elements in provided content and suggests | `sources/06-antigravity/seo-content-refresher/` |
| **seo-content-writer** | 🌌 Antigravity (634+) | Writes SEO-optimized content based on provided keywords and topic | `sources/06-antigravity/seo-content-writer/` |
| **seo-fundamentals** | 🌌 Antigravity (634+) | Core principles of SEO including E-E-A-T, Core Web Vitals, technical foundations, content quality, and how modern search engines evaluate pages. This … | `sources/06-antigravity/seo-fundamentals/` |
| **seo-keyword-strategist** | 🌌 Antigravity (634+) | Analyzes keyword usage in provided content, calculates density, | `sources/06-antigravity/seo-keyword-strategist/` |
| **seo-snippet-hunter** | 🌌 Antigravity (634+) | Formats content to be eligible for featured snippets and SERP | `sources/06-antigravity/seo-snippet-hunter/` |
| **skill-seekers** | 🌌 Antigravity (634+) | -Automatically convert documentation websites, GitHub repositories, and PDFs into Claude AI skills in minutes. | `sources/06-antigravity/skill-seekers/` |
| **social-content** | 🌌 Antigravity (634+) | When the user wants help creating, scheduling, or optimizing social media content for LinkedIn, Twitter/X, Instagram, TikTok, Facebook, or other platf… | `sources/06-antigravity/social-content/` |
| **startup-business-analyst-business-case** | 🌌 Antigravity (634+) | Generate comprehensive investor-ready business case document with | `sources/06-antigravity/startup-business-analyst-business-case/` |
| **tavily-web** | 🌌 Antigravity (634+) | Web search, content extraction, crawling, and research capabilities using Tavily API | `sources/06-antigravity/tavily-web/` |
| **tutorial-engineer** | 🌌 Antigravity (634+) | Creates step-by-step tutorials and educational content from code. | `sources/06-antigravity/tutorial-engineer/` |
| **writing-plans** | 🌌 Antigravity (634+) | Use when you have a spec or requirements for a multi-step task, before touching code | `sources/06-antigravity/writing-plans/` |
| **brandkit** | 📦 skills | Gera imagens de brand-kit premium: boards de brand guidelines, sistemas de logo, identity decks e apresentações de universo visual com grids limpos, t… | `skills/brandkit/` |
| **doc-sanitization** | 📦 skills | Clean up, consolidate, and organize project documentation. Removes obsolete specs, merges duplicates, enforces lifecycle rules. Trigger on phrases lik… | `skills/doc-sanitization/` |
| **docs-writer** | 📦 skills | Escreve, revisa e edita documentação técnica verificando o código-fonte e seguindo style guide do projeto. ACIONE quando: documentar uma feature/coman… | `skills/docs-writer/` |
| **minimalist-ui** | 📦 skills | Gera interfaces ultra-minimalistas estilo editorial/documento (tipo Notion) com paleta monocromática quente, serifas editoriais, bento grids flat, pas… | `skills/minimalist-ui/` |

## ☁️ Infrastructure / DevOps

**48 skills**

| Skill | Origem | Descrição | Path Local |
|-------|--------|-----------|-----------|
| **writing-skills** | 🔵 Superpowers (obra) | Use when creating new skills, editing existing skills, or verifying skills work before deployment | `sources/02-superpowers/writing-skills/` |
| **vercel-deploy** | 🟢 Vercel Labs | Deploy applications and websites to Vercel. Use this skill when the user requests deployment actions such as "Deploy my app", "Deploy this to producti… | `sources/04-vercel/claude.ai/vercel-deploy-claimable/` |
| **building-ai-agent-on-cloudflare** | ☁️ Cloudflare | Builds AI agents on Cloudflare using the Agents SDK with state management, real-time WebSockets, scheduled tasks, tool integration, and chat capabilit… | `sources/10-cloudflare/building-ai-agent-on-cloudflare/` |
| **building-mcp-server-on-cloudflare** | ☁️ Cloudflare | Builds remote MCP (Model Context Protocol) servers on Cloudflare Workers with tools, OAuth authentication, and production deployment. Generates server… | `sources/10-cloudflare/building-mcp-server-on-cloudflare/` |
| **sandbox-sdk** | ☁️ Cloudflare | Build sandboxed applications for secure code execution. Load when building AI code execution, code interpreters, CI/CD systems, interactive dev enviro… | `sources/10-cloudflare/sandbox-sdk/` |
| **wrangler** | ☁️ Cloudflare | Cloudflare Workers CLI for deploying, developing, and managing Workers, KV, R2, D1, Vectorize, Hyperdrive, Workers AI, Containers, Queues, Workflows, … | `sources/10-cloudflare/wrangler/` |
| **hosted-agents** | 📐 Context Engineering | This skill should be used when the user asks to "build background agent", "create hosted coding agent", "set up sandboxed execution", "implement multi… | `sources/05-context-engineering/hosted-agents/` |
| **aws-serverless** | 🌌 Antigravity (634+) | Specialized skill for building production-ready serverless applications on AWS. Covers Lambda functions, API Gateway, DynamoDB, SQS/SNS event-driven p… | `sources/06-antigravity/aws-serverless/` |
| **aws-skills** | 🌌 Antigravity (634+) | AWS development with infrastructure automation and cloud architecture patterns | `sources/06-antigravity/aws-skills/` |
| **azure-functions** | 🌌 Antigravity (634+) | Expert patterns for Azure Functions development including isolated worker model, Durable Functions orchestration, cold start optimization, and product… | `sources/06-antigravity/azure-functions/` |
| **backend-development-feature-development** | 🌌 Antigravity (634+) | Orchestrate end-to-end backend feature development from requirements to deployment. Use when coordinating multi-phase feature delivery across teams an… | `sources/06-antigravity/backend-development-feature-development/` |
| **bash-defensive-patterns** | 🌌 Antigravity (634+) | Master defensive Bash programming techniques for production-grade scripts. Use when writing robust shell scripts, CI/CD pipelines, or system utilities… | `sources/06-antigravity/bash-defensive-patterns/` |
| **bash-pro** | 🌌 Antigravity (634+) | Master of defensive Bash scripting for production automation, CI/CD | `sources/06-antigravity/bash-pro/` |
| **cloud-architect** | 🌌 Antigravity (634+) | Expert cloud architect specializing in AWS/Azure/GCP multi-cloud | `sources/06-antigravity/cloud-architect/` |
| **cost-optimization** | 🌌 Antigravity (634+) | Optimize cloud costs through resource rightsizing, tagging strategies, reserved instances, and spending analysis. Use when reducing cloud expenses, an… | `sources/06-antigravity/cost-optimization/` |
| **deployment-engineer** | 🌌 Antigravity (634+) | Expert deployment engineer specializing in modern CI/CD pipelines, | `sources/06-antigravity/deployment-engineer/` |
| **deployment-procedures** | 🌌 Antigravity (634+) | Production deployment principles and decision-making. Safe deployment workflows, rollback strategies, and verification. Teaches thinking, not scripts. | `sources/06-antigravity/deployment-procedures/` |
| **event-store-design** | 🌌 Antigravity (634+) | Design and implement event stores for event-sourced systems. Use when building event sourcing infrastructure, choosing event store technologies, or im… | `sources/06-antigravity/event-store-design/` |
| **file-uploads** | 🌌 Antigravity (634+) | Expert at handling file uploads and cloud storage. Covers S3, Cloudflare R2, presigned URLs, multipart uploads, and image optimization. Knows how to h… | `sources/06-antigravity/file-uploads/` |
| **gcp-cloud-run** | 🌌 Antigravity (634+) | Specialized skill for building production-ready serverless applications on GCP. Covers Cloud Run services (containerized), Cloud Run Functions (event-… | `sources/06-antigravity/gcp-cloud-run/` |
| **github-workflow-automation** | 🌌 Antigravity (634+) | Automate GitHub workflows with AI assistance. Includes PR reviews, issue triage, CI/CD integration, and Git operations. Use when automating GitHub wor… | `sources/06-antigravity/github-workflow-automation/` |
| **gitops-workflow** | 🌌 Antigravity (634+) | Implement GitOps workflows with ArgoCD and Flux for automated, declarative Kubernetes deployments with continuous reconciliation. Use when implementin… | `sources/06-antigravity/gitops-workflow/` |
| **go-concurrency-patterns** | 🌌 Antigravity (634+) | Master Go concurrency with goroutines, channels, sync primitives, and context. Use when building concurrent Go applications, implementing worker pools… | `sources/06-antigravity/go-concurrency-patterns/` |
| **helm-chart-scaffolding** | 🌌 Antigravity (634+) | Design, organize, and manage Helm charts for templating and packaging Kubernetes applications with reusable configurations. Use when creating Helm cha… | `sources/06-antigravity/helm-chart-scaffolding/` |
| **hugging-face-cli** | 🌌 Antigravity (634+) | Execute Hugging Face Hub operations using the `hf` CLI. Use when the user needs to download models/datasets/spaces, upload files to Hub repositories, … | `sources/06-antigravity/hugging-face-cli/` |
| **hugging-face-jobs** | 🌌 Antigravity (634+) | This skill should be used when users want to run any workload on Hugging Face Jobs infrastructure. Covers UV scripts, Docker-based jobs, hardware sele… | `sources/06-antigravity/hugging-face-jobs/` |
| **hybrid-cloud-architect** | 🌌 Antigravity (634+) | Expert hybrid cloud architect specializing in complex multi-cloud | `sources/06-antigravity/hybrid-cloud-architect/` |
| **hybrid-cloud-networking** | 🌌 Antigravity (634+) | Configure secure, high-performance connectivity between on-premises infrastructure and cloud platforms using VPN and dedicated connections. Use when b… | `sources/06-antigravity/hybrid-cloud-networking/` |
| **inngest** | 🌌 Antigravity (634+) | Inngest expert for serverless-first background jobs, event-driven workflows, and durable execution without managing queues or workers. Use when: innge… | `sources/06-antigravity/inngest/` |
| **istio-traffic-management** | 🌌 Antigravity (634+) | Configure Istio traffic management including routing, load balancing, circuit breakers, and canary deployments. Use when implementing service mesh tra… | `sources/06-antigravity/istio-traffic-management/` |
| **kubernetes-architect** | 🌌 Antigravity (634+) | Expert Kubernetes architect specializing in cloud-native | `sources/06-antigravity/kubernetes-architect/` |
| **ml-pipeline-workflow** | 🌌 Antigravity (634+) | Build end-to-end MLOps pipelines from data preparation through model training, validation, and production deployment. Use when creating ML pipelines, … | `sources/06-antigravity/ml-pipeline-workflow/` |
| **multi-cloud-architecture** | 🌌 Antigravity (634+) | Design multi-cloud architectures using a decision framework to select and integrate services across AWS, Azure, and GCP. Use when building multi-cloud… | `sources/06-antigravity/multi-cloud-architecture/` |
| **network-engineer** | 🌌 Antigravity (634+) | Expert network engineer specializing in modern cloud networking, | `sources/06-antigravity/network-engineer/` |
| **prometheus-configuration** | 🌌 Antigravity (634+) | Set up Prometheus for comprehensive metric collection, storage, and monitoring of infrastructure and applications. Use when implementing metrics colle… | `sources/06-antigravity/prometheus-configuration/` |
| **secrets-management** | 🌌 Antigravity (634+) | Implement secure secrets management for CI/CD pipelines using Vault, AWS Secrets Manager, or native platform solutions. Use when handling sensitive cr… | `sources/06-antigravity/secrets-management/` |
| **shellcheck-configuration** | 🌌 Antigravity (634+) | Master ShellCheck static analysis configuration and usage for shell script quality. Use when setting up linting infrastructure, fixing code issues, or… | `sources/06-antigravity/shellcheck-configuration/` |
| **terraform-skill** | 🌌 Antigravity (634+) | Terraform infrastructure as code best practices | `sources/06-antigravity/terraform-skill/` |
| **terraform-specialist** | 🌌 Antigravity (634+) | Expert Terraform/OpenTofu specialist mastering advanced IaC | `sources/06-antigravity/terraform-specialist/` |
| **upstash-qstash** | 🌌 Antigravity (634+) | Upstash QStash expert for serverless message queues, scheduled jobs, and reliable HTTP-based task delivery without managing infrastructure. Use when: … | `sources/06-antigravity/upstash-qstash/` |
| **vector-index-tuning** | 🌌 Antigravity (634+) | Optimize vector index performance for latency, recall, and memory. Use when tuning HNSW parameters, selecting quantization strategies, or scaling vect… | `sources/06-antigravity/vector-index-tuning/` |
| **vercel-deploy-claimable** | 🌌 Antigravity (634+) | Deploy applications and websites to Vercel. Use this skill when the user requests deployment actions such as | `sources/06-antigravity/vercel-deploy-claimable/` |
| **voice-ai-development** | 🌌 Antigravity (634+) | Expert in building voice AI applications - from real-time voice agents to voice-enabled apps. Covers OpenAI Realtime API, Vapi for voice agents, Deepg… | `sources/06-antigravity/voice-ai-development/` |
| **voice-ai-engine-development** | 🌌 Antigravity (634+) | Build real-time conversational AI voice engines using async worker pipelines, streaming transcription, LLM agents, and TTS synthesis with interrupt ha… | `sources/06-antigravity/voice-ai-engine-development/` |
| **workflow-automation** | 🌌 Antigravity (634+) | Workflow automation is the infrastructure that makes AI agents reliable. Without durable execution, a network hiccup during a 10-step payment flow mea… | `sources/06-antigravity/workflow-automation/` |
| **agency-support** | 📦 skills | Índice dos 6 agentes de Suporte e Operações da Agency (Support Responder, Analytics Reporter, Executive Summary Generator, Finance Tracker, Legal Comp… | `skills/agency/support/` |
| **claude-ci-actions** | 📦 skills | Automate PR review, issue triage, and CI/CD tasks with Claude Code GitHub Actions. TRIGGER when: setting up @claude in PRs/issues, configuring automat… | `skills/claude-ci-actions/` |
| **deployment-procedures** | 📦 skills | Workflows seguros de deploy em produção com backup, verificação pós-deploy e rollback para Vercel, Railway, VPS+PM2, Docker e Kubernetes. ACIONE quand… | `skills/deployment-procedures/` |

## 📱 Mobile

**39 skills**

| Skill | Origem | Descrição | Path Local |
|-------|--------|-----------|-----------|
| **expo-api-routes** | 📱 Expo | Guidelines for creating API routes in Expo Router with EAS Hosting | `sources/09-expo/expo-app-design/skills/expo-api-routes/` |
| **expo-cicd-workflows** | 📱 Expo | Helps understand and write EAS workflow YAML files for Expo projects. Use this skill when the user asks about CI/CD or workflows in an Expo or EAS con… | `sources/09-expo/expo-deployment/skills/expo-cicd-workflows/` |
| **expo-deployment** | 📱 Expo | Deploying Expo apps to iOS App Store, Android Play Store, web hosting, and API routes | `sources/09-expo/expo-deployment/skills/expo-deployment/` |
| **upgrading-expo** | 📱 Expo | Guidelines for upgrading Expo SDK versions and fixing dependency issues | `sources/09-expo/upgrading-expo/skills/upgrading-expo/` |
| **app-store-optimization** | 🌌 Antigravity (634+) | Complete App Store Optimization (ASO) toolkit for researching, optimizing, and tracking mobile app performance on Apple App Store and Google Play Stor… | `sources/06-antigravity/app-store-optimization/` |
| **expo-deployment** | 🌌 Antigravity (634+) | Deploy Expo apps to production | `sources/06-antigravity/expo-deployment/` |
| **flutter-expert** | 🌌 Antigravity (634+) | Master Flutter development with Dart 3, advanced widgets, and | `sources/06-antigravity/flutter-expert/` |
| **interactive-portfolio** | 🌌 Antigravity (634+) | Expert in building portfolios that actually land jobs and clients - not just showing work, but creating memorable experiences. Covers developer portfo… | `sources/06-antigravity/interactive-portfolio/` |
| **ios-developer** | 🌌 Antigravity (634+) | Develop native iOS applications with Swift/SwiftUI. Masters iOS 18, | `sources/06-antigravity/ios-developer/` |
| **mobile-games** | 🌌 Antigravity (634+) | Mobile game development principles. Touch input, battery, performance, app stores. | `sources/06-antigravity/game-development/mobile-games/` |
| **multi-platform-apps-multi-platform** | 🌌 Antigravity (634+) | Build and deploy the same feature consistently across web, mobile, and desktop platforms using API-first architecture and parallel implementation stra… | `sources/06-antigravity/multi-platform-apps-multi-platform/` |
| **stitch-ui-design** | 🌌 Antigravity (634+) | Expert guide for creating effective prompts for Google Stitch AI UI design tool. Use when user wants to design UI/UX in Stitch, create app interfaces,… | `sources/06-antigravity/stitch-ui-design/` |
| **upgrading-expo** | 🌌 Antigravity (634+) | Upgrade Expo SDK versions | `sources/06-antigravity/upgrading-expo/` |
| **varlock-claude-skill** | 🌌 Antigravity (634+) | Secure environment variable management ensuring secrets are never exposed in Claude sessions, terminals, logs, or git commits | `sources/06-antigravity/varlock-claude-skill/` |
| **2d-games** | 📦 skills | Princípios de jogos 2D: sprites, atlases, tilemaps, física 2D, câmeras e padrões de gênero (platformer, top-down). ACIONE quando: estou fazendo um pla… | `skills/game-development/2d-games/` |
| **3d-games** | 📦 skills | Princípios de jogos 3D: pipeline de rendering, shaders, física e colisão 3D, câmeras, iluminação e LOD. ACIONE quando: meu jogo 3D está com draw calls… | `skills/game-development/3d-games/` |
| **api-patterns** | 📦 skills | Princípios de design de APIs: escolha de estilo, formato de resposta, versionamento, paginação, autenticação e rate limiting. ACIONE quando: escolher … | `skills/api-patterns/` |
| **clean-code** | 📦 skills | Padrões pragmáticos de código limpo: conciso, direto, sem over-engineering e sem comentários desnecessários. ACIONE quando: código over-engineered ou … | `skills/clean-code/` |
| **documentation-templates** | 📦 skills | Templates prontos e guias de estrutura para documentação: README, API docs, comentários de código e docs AI-friendly. ACIONE quando: criar README do z… | `skills/documentation-templates/` |
| **edge-case-hunter** | 📦 skills | Caça exaustiva de edge cases por enumeração sistemática de branches e boundaries, reportando em JSON apenas caminhos sem handling. ACIONE quando: pedi… | `skills/quality/edge-case-hunter/` |
| **game-art** | 📦 skills | Princípios de arte para jogos: pipeline de assets, otimização de texturas, animação (sprite, skeletal, procedural), VFX e direção de arte. ACIONE quan… | `skills/game-development/game-art/` |
| **game-audio** | 📦 skills | Princípios de áudio para jogos: SFX, música, formatos e compressão, áudio adaptativo, performance e acessibilidade sonora. ACIONE quando: quero adicio… | `skills/game-development/game-audio/` |
| **game-design** | 📦 skills | Princípios de game design: core loop, estrutura de GDD, psicologia do jogador, balanceamento de dificuldade e progressão. ACIONE quando: meu jogo não … | `skills/game-development/game-design/` |
| **game-development** | 📦 skills | Orquestrador de desenvolvimento de jogos que ensina princípios universais (game loop, padrões, performance, IA, colisão) e roteia para sub-skills de p… | `skills/game-development/` |
| **mcp-builder** | 📦 skills | Constrói servidores MCP (Model Context Protocol) customizados em TypeScript ou Python. ACIONE quando: criar servidor MCP do zero, expor API interna co… | `skills/mcp-builder/` |
| **mobile-design** | 📦 skills | Princípios de design mobile-first para apps iOS e Android: interação touch, thumb zone, performance 60fps, convenções de plataforma (HIG, Material 3),… | `skills/mobile-design/` |
| **mobile-games** | 📦 skills | Princípios de jogos mobile: touch input, bateria e thermal, requisitos de App Store e Google Play, monetização. ACIONE quando: estou portando ou crian… | `skills/game-development/mobile-games/` |
| **multiplayer** | 📦 skills | Princípios de jogos multiplayer: arquitetura de rede (dedicated server, P2P, host-based), sincronização, lag compensation, anti-cheat e matchmaking. A… | `skills/game-development/multiplayer/` |
| **nodejs-best-practices** | 📦 skills | Princípios de desenvolvimento Node.js: escolha de framework, padrões async, arquitetura em camadas, validação, error handling e segurança. ACIONE quan… | `skills/nodejs-best-practices/` |
| **pc-games** | 📦 skills | Princípios de jogos para PC (Windows, Mac, Linux): publicação na Steam, configurações gráficas, rebinding de controles, modding e acessibilidade deskt… | `skills/game-development/pc-games/` |
| **performance-profiling** | 📦 skills | Princípios de profiling de performance: medir, analisar e otimizar usando Core Web Vitals, Lighthouse e ferramentas de profiling. ACIONE quando: págin… | `skills/performance-profiling/` |
| **plan-writing** | 📦 skills | Planejamento estruturado de trabalho com breakdown em tarefas pequenas, dependências e critérios de verificação. ACIONE quando: planeja a implementaçã… | `skills/plan-writing/` |
| **prd-builder** | 📦 skills | Facilitação colaborativa de Product Requirements Document. Guia o usuário por definição de problema, usuários, requisitos, métricas e escopo MVP. Use … | `skills/planning/prd-builder/` |
| **project-context-generator** | 📦 skills | Analisa codebase e gera project-context.md + constitution.md — os documentos governantes do projeto. ACIONE quando: iniciar em projeto novo, projeto n… | `skills/context/project-context-generator/` |
| **python-patterns** | 📦 skills | Princípios de desenvolvimento Python: escolha de framework, async vs sync, type hints, Pydantic, estrutura de projeto e background tasks. ACIONE quand… | `skills/python-patterns/` |
| **server-management** | 📦 skills | Princípios de operação de servidores: gerenciamento de processos (PM2, systemd, Docker), monitoramento, logs, scaling, health checks e troubleshooting… | `skills/server-management/` |
| **stitch-design-export** | 📦 skills | OSForge enhancement layer sobre stitch-design-taste. Gera DESIGN.md para Google Stitch com tokens de osforge.config.json + Impeccable. ACIONE com stit… | `skills/stitch-design-export/` |
| **vr-ar** | 📦 skills | Princípios de jogos VR/AR: conforto e prevenção de motion sickness, locomoção, hand tracking, anchoring AR e metas de performance por headset. ACIONE … | `skills/game-development/vr-ar/` |
| **web-games** | 📦 skills | Princípios de jogos para navegador: escolha de framework (Phaser, PixiJS, Three.js, Babylon.js), WebGPU vs WebGL, compressão de assets, PWA e áudio no… | `skills/game-development/web-games/` |

## 🗄️ Database / Backend

**38 skills**

| Skill | Origem | Descrição | Path Local |
|-------|--------|-----------|-----------|
| **supabase-postgres-best-practices** | 🟩 Supabase | Postgres performance optimization and best practices from Supabase. Use this skill when writing, reviewing, or optimizing Postgres queries, schema des… | `sources/08-supabase/supabase-postgres-best-practices/` |
| **api-design-principles** | 🌌 Antigravity (634+) | Master REST and GraphQL API design principles to build intuitive, scalable, and maintainable APIs that delight developers. Use when designing new APIs… | `sources/06-antigravity/api-design-principles/` |
| **api-patterns** | 🌌 Antigravity (634+) | API design principles and decision-making. REST vs GraphQL vs tRPC selection, response formats, versioning, pagination. | `sources/06-antigravity/api-patterns/` |
| **automate-whatsapp** | 🌌 Antigravity (634+) | Build WhatsApp automations with Kapso workflows: configure WhatsApp triggers, edit workflow graphs, manage executions, deploy functions, and use datab… | `sources/06-antigravity/automate-whatsapp/` |
| **clickhouse-io** | 🌌 Antigravity (634+) | ClickHouse database patterns, query optimization, analytics, and data engineering best practices for high-performance analytical workloads. | `sources/06-antigravity/cc-skill-clickhouse-io/` |
| **database-admin** | 🌌 Antigravity (634+) | Expert database administrator specializing in modern cloud | `sources/06-antigravity/database-admin/` |
| **database-architect** | 🌌 Antigravity (634+) | Expert database architect specializing in data layer design from | `sources/06-antigravity/database-architect/` |
| **database-cloud-optimization-cost-optimize** | 🌌 Antigravity (634+) | You are a cloud cost optimization expert specializing in reducing infrastructure expenses while maintaining performance and reliability. Analyze cloud… | `sources/06-antigravity/database-cloud-optimization-cost-optimize/` |
| **database-design** | 🌌 Antigravity (634+) | Database design principles and decision-making. Schema design, indexing strategy, ORM selection, serverless databases. | `sources/06-antigravity/database-design/` |
| **database-migration** | 🌌 Antigravity (634+) | Execute database migrations across ORMs and platforms with zero-downtime strategies, data transformation, and rollback procedures. Use when migrating … | `sources/06-antigravity/database-migration/` |
| **database-migrations-migration-observability** | 🌌 Antigravity (634+) | Migration monitoring, CDC, and observability infrastructure | `sources/06-antigravity/database-migrations-migration-observability/` |
| **database-migrations-sql-migrations** | 🌌 Antigravity (634+) | SQL database migrations with zero-downtime strategies for | `sources/06-antigravity/database-migrations-sql-migrations/` |
| **database-optimizer** | 🌌 Antigravity (634+) | Expert database optimizer specializing in modern performance | `sources/06-antigravity/database-optimizer/` |
| **django-pro** | 🌌 Antigravity (634+) | Master Django 5.x with async views, DRF, Celery, and Django | `sources/06-antigravity/django-pro/` |
| **fastapi-pro** | 🌌 Antigravity (634+) | Build high-performance async APIs with FastAPI, SQLAlchemy 2.0, and | `sources/06-antigravity/fastapi-pro/` |
| **graphql** | 🌌 Antigravity (634+) | GraphQL gives clients exactly the data they need - no more, no less. One endpoint, typed schema, introspection. But the flexibility that makes it powe… | `sources/06-antigravity/graphql/` |
| **graphql-architect** | 🌌 Antigravity (634+) | Master modern GraphQL with federation, performance optimization, | `sources/06-antigravity/graphql-architect/` |
| **moodle-external-api-development** | 🌌 Antigravity (634+) | Create custom external web service APIs for Moodle LMS. Use when implementing web services for course management, user tracking, quiz operations, or c… | `sources/06-antigravity/moodle-external-api-development/` |
| **neon-postgres** | 🌌 Antigravity (634+) | Expert patterns for Neon serverless Postgres, branching, connection pooling, and Prisma/Drizzle integration Use when: neon database, serverless postgr… | `sources/06-antigravity/neon-postgres/` |
| **nodejs-backend-patterns** | 🌌 Antigravity (634+) | Build production-ready Node.js backend services with Express/Fastify, implementing middleware patterns, error handling, authentication, database integ… | `sources/06-antigravity/nodejs-backend-patterns/` |
| **nosql-expert** | 🌌 Antigravity (634+) | Expert guidance for distributed NoSQL databases (Cassandra, DynamoDB). Focuses on mental models, query-first modeling, single-table design, and avoidi… | `sources/06-antigravity/nosql-expert/` |
| **postgresql** | 🌌 Antigravity (634+) | Design a PostgreSQL-specific schema. Covers best-practices, data types, indexing, constraints, performance patterns, and advanced features | `sources/06-antigravity/postgresql/` |
| **prisma-expert** | 🌌 Antigravity (634+) | Prisma ORM expert for schema design, migrations, query optimization, relations modeling, and database operations. Use PROACTIVELY for Prisma schema is… | `sources/06-antigravity/prisma-expert/` |
| **python-development-python-scaffold** | 🌌 Antigravity (634+) | You are a Python project architecture expert specializing in scaffolding production-ready Python applications. Generate complete project structures wi… | `sources/06-antigravity/python-development-python-scaffold/` |
| **rag-engineer** | 🌌 Antigravity (634+) | Expert in building Retrieval-Augmented Generation systems. Masters embedding models, vector databases, chunking strategies, and retrieval optimization… | `sources/06-antigravity/rag-engineer/` |
| **rag-implementation** | 🌌 Antigravity (634+) | Build Retrieval-Augmented Generation (RAG) systems for LLM applications with vector databases and semantic search. Use when implementing knowledge-gro… | `sources/06-antigravity/rag-implementation/` |
| **ruby-pro** | 🌌 Antigravity (634+) | Write idiomatic Ruby code with metaprogramming, Rails patterns, and | `sources/06-antigravity/ruby-pro/` |
| **shopify-development** | 🌌 Antigravity (634+) | Build Shopify apps, extensions, themes using GraphQL Admin API, Shopify CLI, Polaris UI, and Liquid. TRIGGER: "shopify", "shopify app", "checkout exte… | `sources/06-antigravity/shopify-development/` |
| **similarity-search-patterns** | 🌌 Antigravity (634+) | Implement efficient similarity search with vector databases. Use when building semantic search, implementing nearest neighbor queries, or optimizing r… | `sources/06-antigravity/similarity-search-patterns/` |
| **skill-rails-upgrade** | 🌌 Antigravity (634+) | Analyze Rails apps and provide upgrade assessments | `sources/06-antigravity/skill-rails-upgrade/` |
| **sql-optimization-patterns** | 🌌 Antigravity (634+) | Master SQL query optimization, indexing strategies, and EXPLAIN analysis to dramatically improve database performance and eliminate slow queries. Use … | `sources/06-antigravity/sql-optimization-patterns/` |
| **sql-pro** | 🌌 Antigravity (634+) | Master modern SQL with cloud-native databases, OLTP/OLAP | `sources/06-antigravity/sql-pro/` |
| **supabase-postgres-best-practices** | 🌌 Antigravity (634+) | Postgres performance optimization and best practices from Supabase. Use this skill when writing, reviewing, or optimizing Postgres queries, schema des… | `sources/06-antigravity/postgres-best-practices/` |
| **using-neon** | 🌌 Antigravity (634+) | Guides and best practices for working with Neon Serverless Postgres. Covers getting started, local development with Neon, choosing a connection method… | `sources/06-antigravity/using-neon/` |
| **vector-database-engineer** | 🌌 Antigravity (634+) | Expert in vector databases, embedding strategies, and semantic search implementation. Masters Pinecone, Weaviate, Qdrant, Milvus, and pgvector for RAG… | `sources/06-antigravity/vector-database-engineer/` |
| **postgres-optimization** | 📦 skills | PostgreSQL and Supabase optimization best practices for queries, indexes, RLS policies, and connection management. Use when writing complex queries, c… | `skills/postgres-optimization/` |
| **prisma-expert** | 📦 skills | Padrões avançados de Prisma ORM. ACIONE quando: mudanças de schema com >3 models, estratégias de migration, queries lentas ou N+1, relações many-to-ma… | `skills/prisma-expert/` |
| **smart-hooks** | 📦 skills | Production-grade Python hooks for Claude Code quality gates, safety rails, and developer experience. TRIGGER when: setting up hooks for a project, con… | `skills/smart-hooks/` |

## 📦 General

**38 skills**

| Skill | Origem | Descrição | Path Local |
|-------|--------|-----------|-----------|
| **template-skill** | 🟣 Anthropic (Oficial) | Replace with description of the skill and when Claude should use it. | `sources/01-anthropic/_template/` |
| **ask-questions-if-underspecified** | 🔒 Trail of Bits | Clarify requirements before implementing. Use when serious doubts arise. | `sources/07-trailofbits/ask-questions-if-underspecified/skills/ask-questions-if-underspecified/` |
| **claude-in-chrome-troubleshooting** | 🔒 Trail of Bits | Diagnose and fix Claude in Chrome MCP extension connectivity issues. Use when mcp__claude-in-chrome__* tools fail, return "Browser extension is not co… | `sources/07-trailofbits/claude-in-chrome-troubleshooting/skills/claude-in-chrome-troubleshooting/` |
| **avalonia-zafiro-development** | 🌌 Antigravity (634+) | Mandatory skills, conventions, and behavioral rules for Avalonia UI development using the Zafiro toolkit. | `sources/06-antigravity/avalonia-zafiro-development/` |
| **billing-automation** | 🌌 Antigravity (634+) | Build automated billing systems for recurring payments, invoicing, subscription lifecycle, and dunning management. Use when implementing subscription … | `sources/06-antigravity/billing-automation/` |
| **busybox-on-windows** | 🌌 Antigravity (634+) | How to use a Win32 build of BusyBox to run many of the standard UNIX command line tools on Windows. | `sources/06-antigravity/busybox-on-windows/` |
| **cc-skill-continuous-learning** | 🌌 Antigravity (634+) | Development skill from everything-claude-code | `sources/06-antigravity/cc-skill-continuous-learning/` |
| **cc-skill-strategic-compact** | 🌌 Antigravity (634+) | Development skill from everything-claude-code | `sources/06-antigravity/cc-skill-strategic-compact/` |
| **claude-ally-health** | 🌌 Antigravity (634+) | A health assistant skill for medical information analysis, symptom tracking, and wellness guidance. | `sources/06-antigravity/claude-ally-health/` |
| **claude-scientific-skills** | 🌌 Antigravity (634+) | Scientific research and analysis skills | `sources/06-antigravity/claude-scientific-skills/` |
| **claude-speed-reader** | 🌌 Antigravity (634+) | -Speed read Claude | `sources/06-antigravity/claude-speed-reader/` |
| **claude-win11-speckit-update-skill** | 🌌 Antigravity (634+) | Windows 11 system management | `sources/06-antigravity/claude-win11-speckit-update-skill/` |
| **competitive-landscape** | 🌌 Antigravity (634+) | This skill should be used when the user asks to "analyze | `sources/06-antigravity/competitive-landscape/` |
| **conductor-manage** | 🌌 Antigravity (634+) | Manage track lifecycle: archive, restore, delete, rename, and cleanup | `sources/06-antigravity/conductor-manage/` |
| **data-engineer** | 🌌 Antigravity (634+) | Build scalable data pipelines, modern data warehouses, and | `sources/06-antigravity/data-engineer/` |
| **devops-troubleshooter** | 🌌 Antigravity (634+) | Expert DevOps troubleshooter specializing in rapid incident | `sources/06-antigravity/devops-troubleshooter/` |
| **firecrawl-scraper** | 🌌 Antigravity (634+) | Deep web scraping, screenshots, PDF parsing, and website crawling using Firecrawl API | `sources/06-antigravity/firecrawl-scraper/` |
| **firmware-analyst** | 🌌 Antigravity (634+) | Expert firmware analyst specializing in embedded systems, IoT | `sources/06-antigravity/firmware-analyst/` |
| **full-stack-orchestration-full-stack-feature** | 🌌 Antigravity (634+) | Use when working with full stack orchestration full stack feature | `sources/06-antigravity/full-stack-orchestration-full-stack-feature/` |
| **geo-fundamentals** | 🌌 Antigravity (634+) | Generative Engine Optimization for AI search engines (ChatGPT, Claude, Perplexity). | `sources/06-antigravity/geo-fundamentals/` |
| **incident-response-incident-response** | 🌌 Antigravity (634+) | Use when working with incident response incident response | `sources/06-antigravity/incident-response-incident-response/` |
| **legacy-modernizer** | 🌌 Antigravity (634+) | Refactor legacy codebases, migrate outdated frameworks, and | `sources/06-antigravity/legacy-modernizer/` |
| **market-sizing-analysis** | 🌌 Antigravity (634+) | This skill should be used when the user asks to "calculate TAM", | `sources/06-antigravity/market-sizing-analysis/` |
| **onboarding-cro** | 🌌 Antigravity (634+) | When the user wants to optimize post-signup onboarding, user activation, first-run experience, or time-to-value. Also use when the user mentions "onbo… | `sources/06-antigravity/onboarding-cro/` |
| **oss-hunter** | 🌌 Antigravity (634+) | Automatically hunt for high-impact OSS contribution opportunities in trending repositories. | `sources/06-antigravity/oss-hunter/` |
| **paywall-upgrade-cro** | 🌌 Antigravity (634+) | When the user wants to create or optimize in-app paywalls, upgrade screens, upsell modals, or feature gates. Also use when the user mentions "paywall,… | `sources/06-antigravity/paywall-upgrade-cro/` |
| **performance-engineer** | 🌌 Antigravity (634+) | Expert performance engineer specializing in modern observability, | `sources/06-antigravity/performance-engineer/` |
| **reverse-engineer** | 🌌 Antigravity (634+) | Expert reverse engineer specializing in binary analysis, | `sources/06-antigravity/reverse-engineer/` |
| **risk-manager** | 🌌 Antigravity (634+) | Monitor portfolio risk, R-multiples, and position limits. Creates | `sources/06-antigravity/risk-manager/` |
| **risk-metrics-calculation** | 🌌 Antigravity (634+) | Calculate portfolio risk metrics including VaR, CVaR, Sharpe, Sortino, and drawdown analysis. Use when measuring portfolio risk, implementing risk lim… | `sources/06-antigravity/risk-metrics-calculation/` |
| **search-specialist** | 🌌 Antigravity (634+) | Expert web researcher using advanced search techniques and | `sources/06-antigravity/search-specialist/` |
| **signup-flow-cro** | 🌌 Antigravity (634+) | When the user wants to optimize signup, registration, account creation, or trial activation flows. Also use when the user mentions "signup conversions… | `sources/06-antigravity/signup-flow-cro/` |
| **superpowers-lab** | 🌌 Antigravity (634+) | Lab environment for Claude superpowers | `sources/06-antigravity/superpowers-lab/` |
| **telegram-mini-app** | 🌌 Antigravity (634+) | Expert in building Telegram Mini Apps (TWA) - web apps that run inside Telegram with native-like experience. Covers the TON ecosystem, Telegram Web Ap… | `sources/06-antigravity/telegram-mini-app/` |
| **track-management** | 🌌 Antigravity (634+) | Use this skill when creating, managing, or working with Conductor | `sources/06-antigravity/track-management/` |
| **twilio-communications** | 🌌 Antigravity (634+) | Build communication features with Twilio: SMS messaging, voice calls, WhatsApp Business API, and user verification (2FA). Covers the full spectrum fro… | `sources/06-antigravity/twilio-communications/` |
| **unity-developer** | 🌌 Antigravity (634+) | Build Unity games with optimized C# scripts, efficient rendering, | `sources/06-antigravity/unity-developer/` |
| **web-performance-optimization** | 🌌 Antigravity (634+) | Optimize website and web application performance including loading speed, Core Web Vitals, bundle size, caching strategies, and runtime performance | `sources/06-antigravity/web-performance-optimization/` |

## 🎨 Design / Creative

**12 skills**

| Skill | Origem | Descrição | Path Local |
|-------|--------|-----------|-----------|
| **pdf** | 🟣 Anthropic (Oficial) | Use this skill whenever the user wants to do anything with PDF files. This includes reading or extracting text/tables from PDFs, combining or merging … | `sources/01-anthropic/pdf/` |
| **using-superpowers** | 🔵 Superpowers (obra) | Use when starting any conversation - establishes how to find and use skills, requiring Skill tool invocation before ANY response including clarifying … | `sources/02-superpowers/using-superpowers/` |
| **d3-viz** | 🌌 Antigravity (634+) | Creating interactive data visualisations using d3.js. This skill should be used when creating custom charts, graphs, network diagrams, geographic visu… | `sources/06-antigravity/claude-d3js-skill/` |
| **debugging-toolkit-smart-debug** | 🌌 Antigravity (634+) | Use when working with debugging toolkit smart debug | `sources/06-antigravity/debugging-toolkit-smart-debug/` |
| **error-diagnostics-smart-debug** | 🌌 Antigravity (634+) | Use when working with error diagnostics smart debug | `sources/06-antigravity/error-diagnostics-smart-debug/` |
| **fal-upscale** | 🌌 Antigravity (634+) | Upscale and enhance image and video resolution using AI | `sources/06-antigravity/fal-upscale/` |
| **mermaid-expert** | 🌌 Antigravity (634+) | Create Mermaid diagrams for flowcharts, sequences, ERDs, and | `sources/06-antigravity/mermaid-expert/` |
| **startup-analyst** | 🌌 Antigravity (634+) | Expert startup business analyst specializing in market sizing, | `sources/06-antigravity/startup-analyst/` |
| **startup-metrics-framework** | 🌌 Antigravity (634+) | This skill should be used when the user asks about "key startup | `sources/06-antigravity/startup-metrics-framework/` |
| **threejs-skills** | 🌌 Antigravity (634+) | Three.js skills for creating 3D elements and interactive experiences | `sources/06-antigravity/threejs-skills/` |
| **using-superpowers** | 🌌 Antigravity (634+) | Use when starting any conversation - establishes how to find and use skills, requiring Skill tool invocation before ANY response including clarifying … | `sources/06-antigravity/using-superpowers/` |
| **x-article-publisher-skill** | 🌌 Antigravity (634+) | Publish articles to X/Twitter | `sources/06-antigravity/x-article-publisher-skill/` |

## 💼 Business / Marketing

**6 skills**

| Skill | Origem | Descrição | Path Local |
|-------|--------|-----------|-----------|
| **competitor-alternatives** | 🌌 Antigravity (634+) | When the user wants to create competitor comparison or alternative pages for SEO and sales enablement. Also use when the user mentions | `sources/06-antigravity/competitor-alternatives/` |
| **data-scientist** | 🌌 Antigravity (634+) | Expert data scientist for advanced analytics, machine learning, and | `sources/06-antigravity/data-scientist/` |
| **email-systems** | 🌌 Antigravity (634+) | Email has the highest ROI of any marketing channel. $36 for every $1 spent. Yet most startups treat it as an afterthought - bulk blasts, no personaliz… | `sources/06-antigravity/email-systems/` |
| **paid-ads** | 🌌 Antigravity (634+) | When the user wants help with paid advertising campaigns on Google Ads, Meta (Facebook/Instagram), LinkedIn, Twitter/X, or other ad platforms. Also us… | `sources/06-antigravity/paid-ads/` |
| **seo-meta-optimizer** | 🌌 Antigravity (634+) | Creates optimized meta titles, descriptions, and URL suggestions | `sources/06-antigravity/seo-meta-optimizer/` |
| **seo-fundamentals** | 📦 skills | Fundamentos de SEO para Google com E-E-A-T, Core Web Vitals e SEO técnico. ACIONE quando: melhorar ranking de página no Google, implementar schema mar… | `skills/seo-fundamentals/` |

## 🐍 Languages / Frameworks

**1 skills**

| Skill | Origem | Descrição | Path Local |
|-------|--------|-----------|-----------|
| **mtls-configuration** | 🌌 Antigravity (634+) | Configure mutual TLS (mTLS) for zero-trust service-to-service communication. Use when implementing zero-trust networking, certificate management, or s… | `sources/06-antigravity/mtls-configuration/` |

---

## 🔤 Índice Alfabético Rápido

Lista compacta para busca rápida com `Ctrl+F`:


**#**
- `2d-games` — skills — `skills/game-development/2d-games/`
- `2d-games` — Antigravity — `sources/06-antigravity/game-development/2d-games/`
- `3d-games` — skills — `skills/game-development/3d-games/`
- `3d-games` — Antigravity — `sources/06-antigravity/game-development/3d-games/`
- `3d-web-experience` — Antigravity — `sources/06-antigravity/3d-web-experience/`

**A**
- `ab-test-setup` — Antigravity — `sources/06-antigravity/ab-test-setup/`
- `accessibility` — skills — `skills/accessibility/`
- `accessibility-compliance-accessibility-audit` — Antigravity — `sources/06-antigravity/accessibility-compliance-accessibility-audit/`
- `Active Directory Attacks` — Antigravity — `sources/06-antigravity/active-directory-attacks/`
- `address-github-comments` — Antigravity — `sources/06-antigravity/address-github-comments/`
- `address-sanitizer` — Trail of Bits — `sources/07-trailofbits/testing-handbook-skills/skills/address-sanitizer/`
- `advanced-evaluation` — Context Enginee — `sources/05-context-engineering/advanced-evaluation/`
- `adversarial-review` — skills — `skills/quality/adversarial-review/`
- `aesthetic-boost` — skills — `skills/aesthetic-boost/`
- `aesthetic-modes` — skills — `skills/aesthetic-modes/`
- `aflpp` — Trail of Bits — `sources/07-trailofbits/testing-handbook-skills/skills/aflpp/`
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
- `agent-evaluation` — Antigravity — `sources/06-antigravity/agent-evaluation/`
- `agent-manager-skill` — Antigravity — `sources/06-antigravity/agent-manager-skill/`
- `agent-memory-mcp` — Antigravity — `sources/06-antigravity/agent-memory-mcp/`
- `agent-memory-systems` — Antigravity — `sources/06-antigravity/agent-memory-systems/`
- `agent-orchestration-improve-agent` — Antigravity — `sources/06-antigravity/agent-orchestration-improve-agent/`
- `agent-orchestration-multi-agent-optimize` — Antigravity — `sources/06-antigravity/agent-orchestration-multi-agent-optimize/`
- `agent-skills-search` — skills — `skills/agent-skills-search/`
- `agent-tool-builder` — Antigravity — `sources/06-antigravity/agent-tool-builder/`
- `agents-md` — Sentry — `sources/11-sentry/agents-md/`
- `agents-sdk` — Cloudflare — `sources/10-cloudflare/agents-sdk/`
- `ai-agents-architect` — Antigravity — `sources/06-antigravity/ai-agents-architect/`
- `ai-engineer` — Antigravity — `sources/06-antigravity/ai-engineer/`
- `ai-product` — Antigravity — `sources/06-antigravity/ai-product/`
- `ai-wrapper-product` — Antigravity — `sources/06-antigravity/ai-wrapper-product/`
- `airflow-dag-patterns` — Antigravity — `sources/06-antigravity/airflow-dag-patterns/`
- `algolia-search` — Antigravity — `sources/06-antigravity/algolia-search/`
- `algorand-vulnerability-scanner` — Trail of Bits — `sources/07-trailofbits/building-secure-contracts/skills/algorand-vulnerability-scanner/`
- `algorithmic-art` — Anthropic — `sources/01-anthropic/algorithmic-art/`
- `algorithmic-art` — Antigravity — `sources/06-antigravity/algorithmic-art/`
- `analytics-tracking` — Antigravity — `sources/06-antigravity/analytics-tracking/`
- `angular` — Antigravity — `sources/06-antigravity/angular/`
- `angular-best-practices` — Antigravity — `sources/06-antigravity/angular-best-practices/`
- `angular-migration` — Antigravity — `sources/06-antigravity/angular-migration/`
- `angular-state-management` — Antigravity — `sources/06-antigravity/angular-state-management/`
- `angular-ui-patterns` — Antigravity — `sources/06-antigravity/angular-ui-patterns/`
- `anti-reversing-techniques` — Antigravity — `sources/06-antigravity/anti-reversing-techniques/`
- `API Fuzzing for Bug Bounty` — Antigravity — `sources/06-antigravity/api-fuzzing-bug-bounty/`
- `api-design-principles` — Antigravity — `sources/06-antigravity/api-design-principles/`
- `api-documentation-generator` — Antigravity — `sources/06-antigravity/api-documentation-generator/`
- `api-documenter` — Antigravity — `sources/06-antigravity/api-documenter/`
- `api-patterns` — skills — `skills/api-patterns/`
- `api-patterns` — Antigravity — `sources/06-antigravity/api-patterns/`
- `api-security-best-practices` — Antigravity — `sources/06-antigravity/api-security-best-practices/`
- `api-testing-observability-api-mock` — Antigravity — `sources/06-antigravity/api-testing-observability-api-mock/`
- `app-builder` — skills — `skills/app-builder/`
- `app-builder` — Antigravity — `sources/06-antigravity/app-builder/`
- `app-store-optimization` — Antigravity — `sources/06-antigravity/app-store-optimization/`
- `application-performance-performance-optimization` — Antigravity — `sources/06-antigravity/application-performance-performance-optimization/`
- `arch-builder` — skills — `skills/planning/arch-builder/`
- `architect-review` — Antigravity — `sources/06-antigravity/architect-review/`
- `architecture` — skills — `skills/architecture/`
- `architecture` — Antigravity — `sources/06-antigravity/architecture/`
- `architecture-decision-records` — Antigravity — `sources/06-antigravity/architecture-decision-records/`
- `architecture-patterns` — Antigravity — `sources/06-antigravity/architecture-patterns/`
- `arm-cortex-expert` — Antigravity — `sources/06-antigravity/arm-cortex-expert/`
- `ask-questions-if-underspecified` — Trail of Bits — `sources/07-trailofbits/ask-questions-if-underspecified/skills/ask-questions-if-underspecified/`
- `async-python-patterns` — Antigravity — `sources/06-antigravity/async-python-patterns/`
- `atheris` — Trail of Bits — `sources/07-trailofbits/testing-handbook-skills/skills/atheris/`
- `attack-tree-construction` — Antigravity — `sources/06-antigravity/attack-tree-construction/`
- `audio-transcriber` — Antigravity — `sources/06-antigravity/audio-transcriber/`
- `audit-context-building` — Trail of Bits — `sources/07-trailofbits/audit-context-building/skills/audit-context-building/`
- `audit-prep-assistant` — Trail of Bits — `sources/07-trailofbits/building-secure-contracts/skills/audit-prep-assistant/`
- `auth-implementation-patterns` — Antigravity — `sources/06-antigravity/auth-implementation-patterns/`
- `automate-whatsapp` — Antigravity — `sources/06-antigravity/automate-whatsapp/`
- `autonomous-agent-patterns` — Antigravity — `sources/06-antigravity/autonomous-agent-patterns/`
- `autonomous-agents` — Antigravity — `sources/06-antigravity/autonomous-agents/`
- `autorefine-skill` — skills — `skills/autorefine-skill/`
- `avalonia-layout-zafiro` — Antigravity — `sources/06-antigravity/avalonia-layout-zafiro/`
- `avalonia-viewmodels-zafiro` — Antigravity — `sources/06-antigravity/avalonia-viewmodels-zafiro/`
- `avalonia-zafiro-development` — Antigravity — `sources/06-antigravity/avalonia-zafiro-development/`
- `AWS Penetration Testing` — Antigravity — `sources/06-antigravity/aws-penetration-testing/`
- `aws-serverless` — Antigravity — `sources/06-antigravity/aws-serverless/`
- `aws-skills` — Antigravity — `sources/06-antigravity/aws-skills/`
- `azure-functions` — Antigravity — `sources/06-antigravity/azure-functions/`

**B**
- `backend-architect` — Antigravity — `sources/06-antigravity/backend-architect/`
- `backend-dev-guidelines` — Antigravity — `sources/06-antigravity/backend-dev-guidelines/`
- `backend-development-feature-development` — Antigravity — `sources/06-antigravity/backend-development-feature-development/`
- `backend-patterns` — Antigravity — `sources/06-antigravity/cc-skill-backend-patterns/`
- `backend-security-coder` — Antigravity — `sources/06-antigravity/backend-security-coder/`
- `backtesting-frameworks` — Antigravity — `sources/06-antigravity/backtesting-frameworks/`
- `bash-defensive-patterns` — Antigravity — `sources/06-antigravity/bash-defensive-patterns/`
- `bash-linux` — skills — `skills/bash-linux/`
- `bash-linux` — Antigravity — `sources/06-antigravity/bash-linux/`
- `bash-pro` — Antigravity — `sources/06-antigravity/bash-pro/`
- `bats-testing-patterns` — Antigravity — `sources/06-antigravity/bats-testing-patterns/`
- `bazel-build-optimization` — Antigravity — `sources/06-antigravity/bazel-build-optimization/`
- `bdi-mental-states` — Context Enginee — `sources/05-context-engineering/bdi-mental-states/`
- `beautiful-prose` — Antigravity — `sources/06-antigravity/beautiful-prose/`
- `behavioral-modes` — skills — `skills/behavioral-modes/`
- `behavioral-modes` — Antigravity — `sources/06-antigravity/behavioral-modes/`
- `best-practices` — skills — `skills/best-practices/`
- `billing-automation` — Antigravity — `sources/06-antigravity/billing-automation/`
- `binary-analysis-patterns` — Antigravity — `sources/06-antigravity/binary-analysis-patterns/`
- `blockchain-developer` — Antigravity — `sources/06-antigravity/blockchain-developer/`
- `blockrun` — Antigravity — `sources/06-antigravity/blockrun/`
- `book-sft-pipeline` — Context Enginee — `sources/05-context-engineering/_examples/book-sft-pipeline/`
- `brainstorming` — skills — `skills/brainstorming/`
- `brainstorming` — Superpowers — `sources/02-superpowers/brainstorming/`
- `brainstorming` — Antigravity — `sources/06-antigravity/brainstorming/`
- `brand-guidelines` — Anthropic — `sources/01-anthropic/brand-guidelines/`
- `brand-guidelines` — Antigravity — `sources/06-antigravity/brand-guidelines-anthropic/`
- `brand-guidelines` — Antigravity — `sources/06-antigravity/brand-guidelines-community/`
- `brand-guidelines` — Sentry — `sources/11-sentry/brand-guidelines/`
- `brandkit` — skills — `skills/brandkit/`
- `Broken Authentication Testing` — Antigravity — `sources/06-antigravity/broken-authentication/`
- `browser-automation` — Antigravity — `sources/06-antigravity/browser-automation/`
- `browser-extension-builder` — Antigravity — `sources/06-antigravity/browser-extension-builder/`
- `building-ai-agent-on-cloudflare` — Cloudflare — `sources/10-cloudflare/building-ai-agent-on-cloudflare/`
- `building-mcp-server-on-cloudflare` — Cloudflare — `sources/10-cloudflare/building-mcp-server-on-cloudflare/`
- `building-native-ui` — Expo — `sources/09-expo/expo-app-design/skills/building-native-ui/`
- `bullmq-specialist` — Antigravity — `sources/06-antigravity/bullmq-specialist/`
- `bun-development` — skills — `skills/bun-development/`
- `bun-development` — Antigravity — `sources/06-antigravity/bun-development/`
- `Burp Suite Web Application Testing` — Antigravity — `sources/06-antigravity/burp-suite-testing/`
- `burpsuite-project-parser` — Trail of Bits — `sources/07-trailofbits/burpsuite-project-parser/skills/`
- `business-analyst` — Antigravity — `sources/06-antigravity/business-analyst/`
- `busybox-on-windows` — Antigravity — `sources/06-antigravity/busybox-on-windows/`

**C**
- `c-pro` — Antigravity — `sources/06-antigravity/c-pro/`
- `c4-architecture-c4-architecture` — Antigravity — `sources/06-antigravity/c4-architecture-c4-architecture/`
- `c4-code` — Antigravity — `sources/06-antigravity/c4-code/`
- `c4-component` — Antigravity — `sources/06-antigravity/c4-component/`
- `c4-container` — Antigravity — `sources/06-antigravity/c4-container/`
- `c4-context` — Antigravity — `sources/06-antigravity/c4-context/`
- `cairo-vulnerability-scanner` — Trail of Bits — `sources/07-trailofbits/building-secure-contracts/skills/cairo-vulnerability-scanner/`
- `canvas-design` — Anthropic — `sources/01-anthropic/canvas-design/`
- `canvas-design` — Antigravity — `sources/06-antigravity/canvas-design/`
- `cargo-fuzz` — Trail of Bits — `sources/07-trailofbits/testing-handbook-skills/skills/cargo-fuzz/`
- `cc-skill-continuous-learning` — Antigravity — `sources/06-antigravity/cc-skill-continuous-learning/`
- `cc-skill-project-guidelines-example` — Antigravity — `sources/06-antigravity/cc-skill-project-guidelines-example/`
- `cc-skill-strategic-compact` — Antigravity — `sources/06-antigravity/cc-skill-strategic-compact/`
- `changelog-automation` — Antigravity — `sources/06-antigravity/changelog-automation/`
- `cicd-automation-workflow-automate` — Antigravity — `sources/06-antigravity/cicd-automation-workflow-automate/`
- `clarity-gate` — Antigravity — `sources/06-antigravity/clarity-gate/`
- `Claude Code Guide` — Antigravity — `sources/06-antigravity/claude-code-guide/`
- `claude-ally-health` — Antigravity — `sources/06-antigravity/claude-ally-health/`
- `claude-api-typescript` — skills — `skills/claude-api-typescript/`
- `claude-ci-actions` — skills — `skills/claude-ci-actions/`
- `claude-in-chrome-troubleshooting` — Trail of Bits — `sources/07-trailofbits/claude-in-chrome-troubleshooting/skills/claude-in-chrome-troubleshooting/`
- `claude-scientific-skills` — Antigravity — `sources/06-antigravity/claude-scientific-skills/`
- `claude-settings-audit` — Sentry — `sources/11-sentry/claude-settings-audit/`
- `claude-speed-reader` — Antigravity — `sources/06-antigravity/claude-speed-reader/`
- `claude-win11-speckit-update-skill` — Antigravity — `sources/06-antigravity/claude-win11-speckit-update-skill/`
- `clean-code` — skills — `skills/clean-code/`
- `clean-code` — Antigravity — `sources/06-antigravity/clean-code/`
- `clerk-auth` — Antigravity — `sources/06-antigravity/clerk-auth/`
- `clickhouse-io` — Antigravity — `sources/06-antigravity/cc-skill-clickhouse-io/`
- `Cloud Penetration Testing` — Antigravity — `sources/06-antigravity/cloud-penetration-testing/`
- `cloud-architect` — Antigravity — `sources/06-antigravity/cloud-architect/`
- `cloudflare` — Cloudflare — `sources/10-cloudflare/cloudflare/`
- `code-documentation-code-explain` — Antigravity — `sources/06-antigravity/code-documentation-code-explain/`
- `code-documentation-doc-generate` — Antigravity — `sources/06-antigravity/code-documentation-doc-generate/`
- `code-maturity-assessor` — Trail of Bits — `sources/07-trailofbits/building-secure-contracts/skills/code-maturity-assessor/`
- `code-refactoring-context-restore` — Antigravity — `sources/06-antigravity/code-refactoring-context-restore/`
- `code-refactoring-refactor-clean` — Antigravity — `sources/06-antigravity/code-refactoring-refactor-clean/`
- `code-refactoring-tech-debt` — Antigravity — `sources/06-antigravity/code-refactoring-tech-debt/`
- `code-review` — skills — `skills/quality/code-review/`
- `code-review` — Sentry — `sources/11-sentry/code-review/`
- `code-review-ai-ai-review` — Antigravity — `sources/06-antigravity/code-review-ai-ai-review/`
- `code-review-checklist` — skills — `skills/code-review-checklist/`
- `code-review-checklist` — Antigravity — `sources/06-antigravity/code-review-checklist/`
- `code-review-excellence` — Antigravity — `sources/06-antigravity/code-review-excellence/`
- `code-reviewer` — Antigravity — `sources/06-antigravity/code-reviewer/`
- `code-simplifier` — Sentry — `sources/11-sentry/code-simplifier/`
- `codebase-cleanup-deps-audit` — Antigravity — `sources/06-antigravity/codebase-cleanup-deps-audit/`
- `codebase-cleanup-refactor-clean` — Antigravity — `sources/06-antigravity/codebase-cleanup-refactor-clean/`
- `codebase-cleanup-tech-debt` — Antigravity — `sources/06-antigravity/codebase-cleanup-tech-debt/`
- `codeql` — Trail of Bits — `sources/07-trailofbits/static-analysis/skills/codeql/`
- `codeql` — Trail of Bits — `sources/07-trailofbits/testing-handbook-skills/skills/codeql/`
- `codex-review` — Antigravity — `sources/06-antigravity/codex-review/`
- `coding-guidelines` — skills — `skills/coding-guidelines/`
- `coding-standards` — Antigravity — `sources/06-antigravity/cc-skill-coding-standards/`
- `commit` — Antigravity — `sources/06-antigravity/commit/`
- `commit` — Sentry — `sources/11-sentry/commit/`
- `competitive-landscape` — Antigravity — `sources/06-antigravity/competitive-landscape/`
- `competitor-alternatives` — Antigravity — `sources/06-antigravity/competitor-alternatives/`
- `comprehensive-research-agent` — Context Enginee — `sources/05-context-engineering/_examples/interleaved_thinking/generated_skills/comprehensive-research-agent/`
- `comprehensive-review-full-review` — Antigravity — `sources/06-antigravity/comprehensive-review-full-review/`
- `comprehensive-review-pr-enhance` — Antigravity — `sources/06-antigravity/comprehensive-review-pr-enhance/`
- `computer-use-agents` — Antigravity — `sources/06-antigravity/computer-use-agents/`
- `computer-vision-expert` — Antigravity — `sources/06-antigravity/computer-vision-expert/`
- `concise-planning` — Antigravity — `sources/06-antigravity/concise-planning/`
- `conductor-implement` — Antigravity — `sources/06-antigravity/conductor-implement/`
- `conductor-manage` — Antigravity — `sources/06-antigravity/conductor-manage/`
- `conductor-new-track` — Antigravity — `sources/06-antigravity/conductor-new-track/`
- `conductor-revert` — Antigravity — `sources/06-antigravity/conductor-revert/`
- `conductor-setup` — Antigravity — `sources/06-antigravity/conductor-setup/`
- `conductor-status` — Antigravity — `sources/06-antigravity/conductor-status/`
- `conductor-validator` — Antigravity — `sources/06-antigravity/conductor-validator/`
- `config-critique` — skills — `skills/config-critique/`
- `constant-time-analysis` — Trail of Bits — `sources/07-trailofbits/constant-time-analysis/skills/constant-time-analysis/`
- `constant-time-testing` — Trail of Bits — `sources/07-trailofbits/testing-handbook-skills/skills/constant-time-testing/`
- `content-creator` — Antigravity — `sources/06-antigravity/content-creator/`
- `content-marketer` — Antigravity — `sources/06-antigravity/content-marketer/`
- `context-compact` — skills — `skills/context-compact/`
- `context-compression` — Context Enginee — `sources/05-context-engineering/context-compression/`
- `context-compression` — Antigravity — `sources/06-antigravity/context-compression/`
- `context-degradation` — Context Enginee — `sources/05-context-engineering/context-degradation/`
- `context-degradation` — Antigravity — `sources/06-antigravity/context-degradation/`
- `context-distillator` — skills — `skills/context/context-distillator/`
- `context-driven-development` — Antigravity — `sources/06-antigravity/context-driven-development/`
- `context-fundamentals` — Context Enginee — `sources/05-context-engineering/context-fundamentals/`
- `context-fundamentals` — Antigravity — `sources/06-antigravity/context-fundamentals/`
- `context-management-context-restore` — Antigravity — `sources/06-antigravity/context-management-context-restore/`
- `context-management-context-save` — Antigravity — `sources/06-antigravity/context-management-context-save/`
- `context-manager` — Antigravity — `sources/06-antigravity/context-manager/`
- `context-optimization` — Context Enginee — `sources/05-context-engineering/context-optimization/`
- `context-optimization` — Antigravity — `sources/06-antigravity/context-optimization/`
- `context-window-management` — Antigravity — `sources/06-antigravity/context-window-management/`
- `context7-auto-research` — Antigravity — `sources/06-antigravity/context7-auto-research/`
- `context7-docs-first` — skills — `skills/context7-docs-first/`
- `conversation-memory` — Antigravity — `sources/06-antigravity/conversation-memory/`
- `copy-editing` — Antigravity — `sources/06-antigravity/copy-editing/`
- `copywriting` — Antigravity — `sources/06-antigravity/copywriting/`
- `core-components` — Antigravity — `sources/06-antigravity/core-components/`
- `core-web-vitals` — skills — `skills/core-web-vitals/`
- `cosmos-vulnerability-scanner` — Trail of Bits — `sources/07-trailofbits/building-secure-contracts/skills/cosmos-vulnerability-scanner/`
- `cost-optimization` — Antigravity — `sources/06-antigravity/cost-optimization/`
- `coverage-analysis` — Trail of Bits — `sources/07-trailofbits/testing-handbook-skills/skills/coverage-analysis/`
- `cpp-pro` — Antigravity — `sources/06-antigravity/cpp-pro/`
- `cqrs-implementation` — Antigravity — `sources/06-antigravity/cqrs-implementation/`
- `create-pr` — Antigravity — `sources/06-antigravity/create-pr/`
- `create-pr` — Sentry — `sources/11-sentry/create-pr/`
- `crewai` — Antigravity — `sources/06-antigravity/crewai/`
- `Cross-Site Scripting and HTML Injection Testing` — Antigravity — `sources/06-antigravity/xss-html-injection/`
- `csharp-pro` — Antigravity — `sources/06-antigravity/csharp-pro/`
- `culture-index` — Antigravity — `sources/06-antigravity/culture-index/`
- `customer-support` — Antigravity — `sources/06-antigravity/customer-support/`

**D**
- `d3-viz` — Antigravity — `sources/06-antigravity/claude-d3js-skill/`
- `daily-news-report` — Antigravity — `sources/06-antigravity/daily-news-report/`
- `data-engineer` — Antigravity — `sources/06-antigravity/data-engineer/`
- `data-engineering-data-driven-feature` — Antigravity — `sources/06-antigravity/data-engineering-data-driven-feature/`
- `data-engineering-data-pipeline` — Antigravity — `sources/06-antigravity/data-engineering-data-pipeline/`
- `data-quality-frameworks` — Antigravity — `sources/06-antigravity/data-quality-frameworks/`
- `data-scientist` — Antigravity — `sources/06-antigravity/data-scientist/`
- `data-storytelling` — Antigravity — `sources/06-antigravity/data-storytelling/`
- `database-admin` — Antigravity — `sources/06-antigravity/database-admin/`
- `database-architect` — Antigravity — `sources/06-antigravity/database-architect/`
- `database-cloud-optimization-cost-optimize` — Antigravity — `sources/06-antigravity/database-cloud-optimization-cost-optimize/`
- `database-design` — skills — `skills/database-design/`
- `database-design` — Antigravity — `sources/06-antigravity/database-design/`
- `database-migration` — Antigravity — `sources/06-antigravity/database-migration/`
- `database-migrations-migration-observability` — Antigravity — `sources/06-antigravity/database-migrations-migration-observability/`
- `database-migrations-sql-migrations` — Antigravity — `sources/06-antigravity/database-migrations-sql-migrations/`
- `database-optimizer` — Antigravity — `sources/06-antigravity/database-optimizer/`
- `db-state-sync` — skills — `skills/context/db-state-sync/`
- `dbt-transformation-patterns` — Antigravity — `sources/06-antigravity/dbt-transformation-patterns/`
- `debugger` — Antigravity — `sources/06-antigravity/debugger/`
- `debugging-strategies` — Antigravity — `sources/06-antigravity/debugging-strategies/`
- `debugging-toolkit-smart-debug` — Antigravity — `sources/06-antigravity/debugging-toolkit-smart-debug/`
- `deep-research` — Antigravity — `sources/06-antigravity/deep-research/`
- `defi-protocol-templates` — Antigravity — `sources/06-antigravity/defi-protocol-templates/`
- `dependency-management-deps-audit` — Antigravity — `sources/06-antigravity/dependency-management-deps-audit/`
- `dependency-upgrade` — Antigravity — `sources/06-antigravity/dependency-upgrade/`
- `deployment-engineer` — Antigravity — `sources/06-antigravity/deployment-engineer/`
- `deployment-pipeline-design` — Antigravity — `sources/06-antigravity/deployment-pipeline-design/`
- `deployment-procedures` — skills — `skills/deployment-procedures/`
- `deployment-procedures` — Antigravity — `sources/06-antigravity/deployment-procedures/`
- `deployment-validation-config-validate` — Antigravity — `sources/06-antigravity/deployment-validation-config-validate/`
- `design-md` — skills — `skills/design-md/`
- `design-md` — Antigravity — `sources/06-antigravity/design-md/`
- `design-orchestration` — Antigravity — `sources/06-antigravity/design-orchestration/`
- `design-taste-frontend` — skills — `skills/design-taste-frontend/`
- `design-taste-frontend-v1` — skills — `skills/design-taste-frontend-v1/`
- `devops-troubleshooter` — Antigravity — `sources/06-antigravity/devops-troubleshooter/`
- `differential-review` — skills — `skills/differential-review/`
- `differential-review` — Trail of Bits — `sources/07-trailofbits/differential-review/skills/differential-review/`
- `digital-brain` — Context Enginee — `sources/05-context-engineering/_examples/digital-brain-skill/`
- `discord-bot-architect` — Antigravity — `sources/06-antigravity/discord-bot-architect/`
- `dispatching-parallel-agents` — skills — `skills/dispatching-parallel-agents/`
- `dispatching-parallel-agents` — Superpowers — `sources/02-superpowers/dispatching-parallel-agents/`
- `dispatching-parallel-agents` — Antigravity — `sources/06-antigravity/dispatching-parallel-agents/`
- `distributed-debugging-debug-trace` — Antigravity — `sources/06-antigravity/distributed-debugging-debug-trace/`
- `distributed-tracing` — Antigravity — `sources/06-antigravity/distributed-tracing/`
- `django-access-review` — Sentry — `sources/11-sentry/django-access-review/`
- `django-perf-review` — Sentry — `sources/11-sentry/django-perf-review/`
- `django-pro` — Antigravity — `sources/06-antigravity/django-pro/`
- `doc-coauthoring` — Anthropic — `sources/01-anthropic/doc-coauthoring/`
- `doc-coauthoring` — Antigravity — `sources/06-antigravity/doc-coauthoring/`
- `doc-coauthoring` — Sentry — `sources/11-sentry/doc-coauthoring/`
- `doc-sanitization` — skills — `skills/doc-sanitization/`
- `doc-shard` — skills — `skills/context/doc-shard/`
- `docker-expert` — Antigravity — `sources/06-antigravity/docker-expert/`
- `docs-architect` — Antigravity — `sources/06-antigravity/docs-architect/`
- `docs-writer` — skills — `skills/docs-writer/`
- `documentation-generation-doc-generate` — Antigravity — `sources/06-antigravity/documentation-generation-doc-generate/`
- `documentation-templates` — skills — `skills/documentation-templates/`
- `documentation-templates` — Antigravity — `sources/06-antigravity/documentation-templates/`
- `docx` — Anthropic — `sources/01-anthropic/docx/`
- `docx` — Antigravity — `sources/06-antigravity/docx-official/`
- `dotnet-architect` — Antigravity — `sources/06-antigravity/dotnet-architect/`
- `dotnet-backend-patterns` — Antigravity — `sources/06-antigravity/dotnet-backend-patterns/`
- `durable-objects` — Cloudflare — `sources/10-cloudflare/durable-objects/`
- `dwarf-expert` — Trail of Bits — `sources/07-trailofbits/dwarf-expert/skills/dwarf-expert/`
- `dx-optimizer` — Antigravity — `sources/06-antigravity/dx-optimizer/`

**E**
- `e2e-testing-patterns` — skills — `skills/e2e-testing-patterns/`
- `e2e-testing-patterns` — Antigravity — `sources/06-antigravity/e2e-testing-patterns/`
- `edge-case-hunter` — skills — `skills/quality/edge-case-hunter/`
- `editorial-review` — skills — `skills/context/editorial-review/`
- `elicitation-engine` — skills — `skills/quality/elicitation-engine/`
- `elixir-pro` — Antigravity — `sources/06-antigravity/elixir-pro/`
- `email-sequence` — Antigravity — `sources/06-antigravity/email-sequence/`
- `email-systems` — Antigravity — `sources/06-antigravity/email-systems/`
- `embedding-strategies` — Antigravity — `sources/06-antigravity/embedding-strategies/`
- `employment-contract-templates` — Antigravity — `sources/06-antigravity/employment-contract-templates/`
- `entry-point-analyzer` — Trail of Bits — `sources/07-trailofbits/entry-point-analyzer/skills/entry-point-analyzer/`
- `environment-setup-guide` — Antigravity — `sources/06-antigravity/environment-setup-guide/`
- `epic-decomposer` — skills — `skills/planning/epic-decomposer/`
- `error-debugging-error-analysis` — Antigravity — `sources/06-antigravity/error-debugging-error-analysis/`
- `error-debugging-error-trace` — Antigravity — `sources/06-antigravity/error-debugging-error-trace/`
- `error-debugging-multi-agent-review` — Antigravity — `sources/06-antigravity/error-debugging-multi-agent-review/`
- `error-detective` — Antigravity — `sources/06-antigravity/error-detective/`
- `error-diagnostics-error-analysis` — Antigravity — `sources/06-antigravity/error-diagnostics-error-analysis/`
- `error-diagnostics-error-trace` — Antigravity — `sources/06-antigravity/error-diagnostics-error-trace/`
- `error-diagnostics-smart-debug` — Antigravity — `sources/06-antigravity/error-diagnostics-smart-debug/`
- `error-handling-patterns` — Antigravity — `sources/06-antigravity/error-handling-patterns/`
- `Ethical Hacking Methodology` — Antigravity — `sources/06-antigravity/ethical-hacking-methodology/`
- `evaluation` — Context Enginee — `sources/05-context-engineering/evaluation/`
- `evaluation` — Antigravity — `sources/06-antigravity/evaluation/`
- `event-sourcing-architect` — Antigravity — `sources/06-antigravity/event-sourcing-architect/`
- `event-store-design` — Antigravity — `sources/06-antigravity/event-store-design/`
- `exa-search` — Antigravity — `sources/06-antigravity/exa-search/`
- `executing-plans` — Superpowers — `sources/02-superpowers/executing-plans/`
- `executing-plans` — Antigravity — `sources/06-antigravity/executing-plans/`
- `expo-api-routes` — Expo — `sources/09-expo/expo-app-design/skills/expo-api-routes/`
- `expo-cicd-workflows` — Expo — `sources/09-expo/expo-deployment/skills/expo-cicd-workflows/`
- `expo-deployment` — Antigravity — `sources/06-antigravity/expo-deployment/`
- `expo-deployment` — Expo — `sources/09-expo/expo-deployment/skills/expo-deployment/`
- `expo-dev-client` — Expo — `sources/09-expo/expo-app-design/skills/expo-dev-client/`
- `expo-tailwind-setup` — Expo — `sources/09-expo/expo-app-design/skills/expo-tailwind-setup/`

**F**
- `fal-audio` — Antigravity — `sources/06-antigravity/fal-audio/`
- `fal-generate` — Antigravity — `sources/06-antigravity/fal-generate/`
- `fal-image-edit` — Antigravity — `sources/06-antigravity/fal-image-edit/`
- `fal-platform` — Antigravity — `sources/06-antigravity/fal-platform/`
- `fal-upscale` — Antigravity — `sources/06-antigravity/fal-upscale/`
- `fal-workflow` — Antigravity — `sources/06-antigravity/fal-workflow/`
- `fastapi-pro` — Antigravity — `sources/06-antigravity/fastapi-pro/`
- `fastapi-templates` — Antigravity — `sources/06-antigravity/fastapi-templates/`
- `ffuf-claude-skill` — Antigravity — `sources/06-antigravity/ffuf-claude-skill/`
- `File Path Traversal Testing` — Antigravity — `sources/06-antigravity/file-path-traversal/`
- `file-organizer` — Antigravity — `sources/06-antigravity/file-organizer/`
- `file-uploads` — Antigravity — `sources/06-antigravity/file-uploads/`
- `filesystem-context` — Context Enginee — `sources/05-context-engineering/filesystem-context/`
- `find-bugs` — Antigravity — `sources/06-antigravity/find-bugs/`
- `find-bugs` — Sentry — `sources/11-sentry/find-bugs/`
- `finishing-a-development-branch` — skills — `skills/finishing-a-development-branch/`
- `finishing-a-development-branch` — Superpowers — `sources/02-superpowers/finishing-a-development-branch/`
- `finishing-a-development-branch` — Antigravity — `sources/06-antigravity/finishing-a-development-branch/`
- `firebase` — Antigravity — `sources/06-antigravity/firebase/`
- `firebase-apk-scanner` — Trail of Bits — `sources/07-trailofbits/firebase-apk-scanner/skills/firebase-apk-scanner/`
- `firecrawl-scraper` — Antigravity — `sources/06-antigravity/firecrawl-scraper/`
- `firmware-analyst` — Antigravity — `sources/06-antigravity/firmware-analyst/`
- `fix-review` — Antigravity — `sources/06-antigravity/fix-review/`
- `fix-review` — Trail of Bits — `sources/07-trailofbits/fix-review/skills/fix-review/`
- `flutter-expert` — Antigravity — `sources/06-antigravity/flutter-expert/`
- `form-cro` — Antigravity — `sources/06-antigravity/form-cro/`
- `fp-ts-errors` — Antigravity — `sources/06-antigravity/fp-ts-errors/`
- `fp-ts-pragmatic` — Antigravity — `sources/06-antigravity/fp-ts-pragmatic/`
- `fp-ts-react` — Antigravity — `sources/06-antigravity/fp-ts-react/`
- `framework-migration-code-migrate` — Antigravity — `sources/06-antigravity/framework-migration-code-migrate/`
- `framework-migration-deps-upgrade` — Antigravity — `sources/06-antigravity/framework-migration-deps-upgrade/`
- `framework-migration-legacy-modernize` — Antigravity — `sources/06-antigravity/framework-migration-legacy-modernize/`
- `free-tool-strategy` — Antigravity — `sources/06-antigravity/free-tool-strategy/`
- `frontend-design` — skills — `skills/frontend-design/`
- `frontend-design` — Anthropic — `sources/01-anthropic/frontend-design/`
- `frontend-design` — Antigravity — `sources/06-antigravity/frontend-design/`
- `frontend-dev-guidelines` — Antigravity — `sources/06-antigravity/frontend-dev-guidelines/`
- `frontend-developer` — Antigravity — `sources/06-antigravity/frontend-developer/`
- `frontend-mobile-development-component-scaffold` — Antigravity — `sources/06-antigravity/frontend-mobile-development-component-scaffold/`
- `frontend-mobile-security-xss-scan` — Antigravity — `sources/06-antigravity/frontend-mobile-security-xss-scan/`
- `frontend-patterns` — Antigravity — `sources/06-antigravity/cc-skill-frontend-patterns/`
- `frontend-security-coder` — Antigravity — `sources/06-antigravity/frontend-security-coder/`
- `frontend-slides` — Antigravity — `sources/06-antigravity/frontend-slides/`
- `frontend-ui-system` — skills — `skills/frontend-ui-system/`
- `full-output-enforcement` — skills — `skills/full-output-enforcement/`
- `full-stack-orchestration-full-stack-feature` — Antigravity — `sources/06-antigravity/full-stack-orchestration-full-stack-feature/`
- `fuzzing-dictionary` — Trail of Bits — `sources/07-trailofbits/testing-handbook-skills/skills/fuzzing-dictionary/`
- `fuzzing-obstacles` — Trail of Bits — `sources/07-trailofbits/testing-handbook-skills/skills/fuzzing-obstacles/`

**G**
- `game-art` — skills — `skills/game-development/game-art/`
- `game-art` — Antigravity — `sources/06-antigravity/game-development/game-art/`
- `game-audio` — skills — `skills/game-development/game-audio/`
- `game-audio` — Antigravity — `sources/06-antigravity/game-development/game-audio/`
- `game-design` — skills — `skills/game-development/game-design/`
- `game-design` — Antigravity — `sources/06-antigravity/game-development/game-design/`
- `game-development` — skills — `skills/game-development/`
- `game-development` — Antigravity — `sources/06-antigravity/game-development/`
- `gcp-cloud-run` — Antigravity — `sources/06-antigravity/gcp-cloud-run/`
- `gdpr-data-handling` — skills — `skills/gdpr-data-handling/`
- `gdpr-data-handling` — Antigravity — `sources/06-antigravity/gdpr-data-handling/`
- `genai-optimization` — skills — `skills/genai-optimization/`
- `geo-fundamentals` — Antigravity — `sources/06-antigravity/geo-fundamentals/`
- `git-advanced-workflows` — Antigravity — `sources/06-antigravity/git-advanced-workflows/`
- `git-pr-workflows-git-workflow` — Antigravity — `sources/06-antigravity/git-pr-workflows-git-workflow/`
- `git-pr-workflows-onboard` — Antigravity — `sources/06-antigravity/git-pr-workflows-onboard/`
- `git-pr-workflows-pr-enhance` — Antigravity — `sources/06-antigravity/git-pr-workflows-pr-enhance/`
- `git-pushing` — Antigravity — `sources/06-antigravity/git-pushing/`
- `git-workflow` — skills — `skills/git-workflow/`
- `github-actions-templates` — Antigravity — `sources/06-antigravity/github-actions-templates/`
- `github-workflow-automation` — Antigravity — `sources/06-antigravity/github-workflow-automation/`
- `gitlab-ci-patterns` — Antigravity — `sources/06-antigravity/gitlab-ci-patterns/`
- `gitops-workflow` — Antigravity — `sources/06-antigravity/gitops-workflow/`
- `go-concurrency-patterns` — Antigravity — `sources/06-antigravity/go-concurrency-patterns/`
- `godot-gdscript-patterns` — Antigravity — `sources/06-antigravity/godot-gdscript-patterns/`
- `golang-pro` — Antigravity — `sources/06-antigravity/golang-pro/`
- `gpt-taste` — skills — `skills/gpt-taste/`
- `grafana-dashboards` — Antigravity — `sources/06-antigravity/grafana-dashboards/`
- `graphql` — Antigravity — `sources/06-antigravity/graphql/`
- `graphql-architect` — Antigravity — `sources/06-antigravity/graphql-architect/`
- `guidelines-advisor` — Trail of Bits — `sources/07-trailofbits/building-secure-contracts/skills/guidelines-advisor/`

**H**
- `harness-writing` — Trail of Bits — `sources/07-trailofbits/testing-handbook-skills/skills/harness-writing/`
- `haskell-pro` — Antigravity — `sources/06-antigravity/haskell-pro/`
- `helm-chart-scaffolding` — Antigravity — `sources/06-antigravity/helm-chart-scaffolding/`
- `high-end-visual-design` — skills — `skills/high-end-visual-design/`
- `hosted-agents` — Context Enginee — `sources/05-context-engineering/hosted-agents/`
- `hr-pro` — Antigravity — `sources/06-antigravity/hr-pro/`
- `HTML Injection Testing` — Antigravity — `sources/06-antigravity/html-injection-testing/`
- `hubspot-integration` — Antigravity — `sources/06-antigravity/hubspot-integration/`
- `hugging-face-cli` — Antigravity — `sources/06-antigravity/hugging-face-cli/`
- `hugging-face-jobs` — Antigravity — `sources/06-antigravity/hugging-face-jobs/`
- `hybrid-cloud-architect` — Antigravity — `sources/06-antigravity/hybrid-cloud-architect/`
- `hybrid-cloud-networking` — Antigravity — `sources/06-antigravity/hybrid-cloud-networking/`
- `hybrid-search-implementation` — Antigravity — `sources/06-antigravity/hybrid-search-implementation/`

**I**
- `i18n-localization` — skills — `skills/i18n-localization/`
- `i18n-localization` — Antigravity — `sources/06-antigravity/i18n-localization/`
- `IDOR Vulnerability Testing` — Antigravity — `sources/06-antigravity/idor-testing/`
- `image-to-code` — skills — `skills/image-to-code/`
- `imagegen-frontend-mobile` — skills — `skills/imagegen-frontend-mobile/`
- `imagegen-frontend-web` — skills — `skills/imagegen-frontend-web/`
- `imagen` — Antigravity — `sources/06-antigravity/imagen/`
- `incident-responder` — Antigravity — `sources/06-antigravity/incident-responder/`
- `incident-response-incident-response` — Antigravity — `sources/06-antigravity/incident-response-incident-response/`
- `incident-response-smart-fix` — Antigravity — `sources/06-antigravity/incident-response-smart-fix/`
- `incident-runbook-templates` — Antigravity — `sources/06-antigravity/incident-runbook-templates/`
- `industrial-brutalist-ui` — skills — `skills/industrial-brutalist-ui/`
- `Infinite Gratitude` — Antigravity — `sources/06-antigravity/infinite-gratitude/`
- `inngest` — Antigravity — `sources/06-antigravity/inngest/`
- `insecure-defaults` — skills — `skills/insecure-defaults/`
- `insecure-defaults` — Trail of Bits — `sources/07-trailofbits/insecure-defaults/skills/insecure-defaults/`
- `interactive-portfolio` — Antigravity — `sources/06-antigravity/interactive-portfolio/`
- `internal-comms` — Anthropic — `sources/01-anthropic/internal-comms/`
- `internal-comms` — Antigravity — `sources/06-antigravity/internal-comms-anthropic/`
- `internal-comms` — Antigravity — `sources/06-antigravity/internal-comms-community/`
- `interpreting-culture-index` — Trail of Bits — `sources/07-trailofbits/culture-index/skills/interpreting-culture-index/`
- `ios-developer` — Antigravity — `sources/06-antigravity/ios-developer/`
- `istio-traffic-management` — Antigravity — `sources/06-antigravity/istio-traffic-management/`
- `iterate-pr` — Antigravity — `sources/06-antigravity/iterate-pr/`
- `iterate-pr` — Sentry — `sources/11-sentry/iterate-pr/`

**J**
- `java-pro` — Antigravity — `sources/06-antigravity/java-pro/`
- `javascript-mastery` — Antigravity — `sources/06-antigravity/javascript-mastery/`
- `javascript-pro` — Antigravity — `sources/06-antigravity/javascript-pro/`
- `javascript-testing-patterns` — Antigravity — `sources/06-antigravity/javascript-testing-patterns/`
- `javascript-typescript-typescript-scaffold` — Antigravity — `sources/06-antigravity/javascript-typescript-typescript-scaffold/`
- `julia-pro` — Antigravity — `sources/06-antigravity/julia-pro/`

**K**
- `k8s-manifest-generator` — Antigravity — `sources/06-antigravity/k8s-manifest-generator/`
- `k8s-security-policies` — Antigravity — `sources/06-antigravity/k8s-security-policies/`
- `kaizen` — Antigravity — `sources/06-antigravity/kaizen/`
- `kpi-dashboard-design` — Antigravity — `sources/06-antigravity/kpi-dashboard-design/`
- `kubernetes-architect` — Antigravity — `sources/06-antigravity/kubernetes-architect/`

**L**
- `langchain-architecture` — Antigravity — `sources/06-antigravity/langchain-architecture/`
- `langfuse` — Antigravity — `sources/06-antigravity/langfuse/`
- `langgraph` — Antigravity — `sources/06-antigravity/langgraph/`
- `last30days` — Antigravity — `sources/06-antigravity/last30days/`
- `launch-strategy` — Antigravity — `sources/06-antigravity/launch-strategy/`
- `legacy-modernizer` — Antigravity — `sources/06-antigravity/legacy-modernizer/`
- `legal-advisor` — Antigravity — `sources/06-antigravity/legal-advisor/`
- `libafl` — Trail of Bits — `sources/07-trailofbits/testing-handbook-skills/skills/libafl/`
- `libfuzzer` — Trail of Bits — `sources/07-trailofbits/testing-handbook-skills/skills/libfuzzer/`
- `linear-claude-skill` — Antigravity — `sources/06-antigravity/linear-claude-skill/`
- `linkerd-patterns` — Antigravity — `sources/06-antigravity/linkerd-patterns/`
- `lint-and-validate` — skills — `skills/lint-and-validate/`
- `lint-and-validate` — Antigravity — `sources/06-antigravity/lint-and-validate/`
- `Linux Privilege Escalation` — Antigravity — `sources/06-antigravity/linux-privilege-escalation/`
- `Linux Production Shell Scripts` — Antigravity — `sources/06-antigravity/linux-shell-scripting/`
- `llm-app-patterns` — Antigravity — `sources/06-antigravity/llm-app-patterns/`
- `llm-application-dev-ai-assistant` — Antigravity — `sources/06-antigravity/llm-application-dev-ai-assistant/`
- `llm-application-dev-langchain-agent` — Antigravity — `sources/06-antigravity/llm-application-dev-langchain-agent/`
- `llm-application-dev-prompt-optimize` — Antigravity — `sources/06-antigravity/llm-application-dev-prompt-optimize/`
- `llm-evaluation` — Antigravity — `sources/06-antigravity/llm-evaluation/`
- `llmfit-advisor` — skills — `skills/llmfit-advisor/`
- `loki-mode` — Antigravity — `sources/06-antigravity/loki-mode/`

**M**
- `machine-learning-ops-ml-pipeline` — Antigravity — `sources/06-antigravity/machine-learning-ops-ml-pipeline/`
- `makepad-skills` — Antigravity — `sources/06-antigravity/makepad-skills/`
- `malware-analyst` — Antigravity — `sources/06-antigravity/malware-analyst/`
- `market-sizing-analysis` — Antigravity — `sources/06-antigravity/market-sizing-analysis/`
- `marketing-ideas` — Antigravity — `sources/06-antigravity/marketing-ideas/`
- `marketing-psychology` — Antigravity — `sources/06-antigravity/marketing-psychology/`
- `mcp-builder` — skills — `skills/mcp-builder/`
- `mcp-builder` — Anthropic — `sources/01-anthropic/mcp-builder/`
- `mcp-builder` — Antigravity — `sources/06-antigravity/mcp-builder/`
- `memory-forensics` — Antigravity — `sources/06-antigravity/memory-forensics/`
- `memory-safety-patterns` — Antigravity — `sources/06-antigravity/memory-safety-patterns/`
- `memory-systems` — Context Enginee — `sources/05-context-engineering/memory-systems/`
- `memory-systems` — Antigravity — `sources/06-antigravity/memory-systems/`
- `mermaid-expert` — Antigravity — `sources/06-antigravity/mermaid-expert/`
- `Metasploit Framework` — Antigravity — `sources/06-antigravity/metasploit-framework/`
- `micro-saas-launcher` — Antigravity — `sources/06-antigravity/micro-saas-launcher/`
- `microservices-patterns` — Antigravity — `sources/06-antigravity/microservices-patterns/`
- `minecraft-bukkit-pro` — Antigravity — `sources/06-antigravity/minecraft-bukkit-pro/`
- `minimalist-ui` — skills — `skills/minimalist-ui/`
- `ml-engineer` — Antigravity — `sources/06-antigravity/ml-engineer/`
- `ml-pipeline-workflow` — Antigravity — `sources/06-antigravity/ml-pipeline-workflow/`
- `mlops-engineer` — Antigravity — `sources/06-antigravity/mlops-engineer/`
- `mobile-design` — skills — `skills/mobile-design/`
- `mobile-design` — Antigravity — `sources/06-antigravity/mobile-design/`
- `mobile-developer` — Antigravity — `sources/06-antigravity/mobile-developer/`
- `mobile-games` — skills — `skills/game-development/mobile-games/`
- `mobile-games` — Antigravity — `sources/06-antigravity/game-development/mobile-games/`
- `mobile-security-coder` — Antigravity — `sources/06-antigravity/mobile-security-coder/`
- `modern-javascript-patterns` — Antigravity — `sources/06-antigravity/modern-javascript-patterns/`
- `modern-python` — Trail of Bits — `sources/07-trailofbits/modern-python/skills/modern-python/`
- `monorepo-architect` — Antigravity — `sources/06-antigravity/monorepo-architect/`
- `monorepo-management` — Antigravity — `sources/06-antigravity/monorepo-management/`
- `moodle-external-api-development` — Antigravity — `sources/06-antigravity/moodle-external-api-development/`
- `mtls-configuration` — Antigravity — `sources/06-antigravity/mtls-configuration/`
- `multi-agent-brainstorming` — Antigravity — `sources/06-antigravity/multi-agent-brainstorming/`
- `multi-agent-patterns` — Context Enginee — `sources/05-context-engineering/multi-agent-patterns/`
- `multi-agent-patterns` — Antigravity — `sources/06-antigravity/multi-agent-patterns/`
- `multi-cloud-architecture` — Antigravity — `sources/06-antigravity/multi-cloud-architecture/`
- `multi-platform-apps-multi-platform` — Antigravity — `sources/06-antigravity/multi-platform-apps-multi-platform/`
- `multiplayer` — skills — `skills/game-development/multiplayer/`
- `multiplayer` — Antigravity — `sources/06-antigravity/game-development/multiplayer/`

**N**
- `n8n-code-python` — Antigravity — `sources/06-antigravity/n8n-code-python/`
- `n8n-mcp-tools-expert` — Antigravity — `sources/06-antigravity/n8n-mcp-tools-expert/`
- `n8n-node-configuration` — Antigravity — `sources/06-antigravity/n8n-node-configuration/`
- `nanobanana-ppt-skills` — Antigravity — `sources/06-antigravity/nanobanana-ppt-skills/`
- `native-data-fetching` — Expo — `sources/09-expo/expo-app-design/skills/native-data-fetching/`
- `neon-postgres` — Antigravity — `sources/06-antigravity/neon-postgres/`
- `nestjs-expert` — Antigravity — `sources/06-antigravity/nestjs-expert/`
- `Network 101` — Antigravity — `sources/06-antigravity/network-101/`
- `network-engineer` — Antigravity — `sources/06-antigravity/network-engineer/`
- `nextjs-app-router-patterns` — Antigravity — `sources/06-antigravity/nextjs-app-router-patterns/`
- `nextjs-best-practices` — Antigravity — `sources/06-antigravity/nextjs-best-practices/`
- `nextjs-react-expert` — skills — `skills/nextjs-react-expert/`
- `nextjs-supabase-auth` — skills — `skills/nextjs-supabase-auth/`
- `nextjs-supabase-auth` — Antigravity — `sources/06-antigravity/nextjs-supabase-auth/`
- `nft-standards` — Antigravity — `sources/06-antigravity/nft-standards/`
- `nodejs-backend-patterns` — Antigravity — `sources/06-antigravity/nodejs-backend-patterns/`
- `nodejs-best-practices` — skills — `skills/nodejs-best-practices/`
- `nodejs-best-practices` — Antigravity — `sources/06-antigravity/nodejs-best-practices/`
- `nosql-expert` — Antigravity — `sources/06-antigravity/nosql-expert/`
- `notebooklm` — Antigravity — `sources/06-antigravity/notebooklm/`
- `notion-template-business` — Antigravity — `sources/06-antigravity/notion-template-business/`
- `nx-workspace-patterns` — Antigravity — `sources/06-antigravity/nx-workspace-patterns/`

**O**
- `observability-engineer` — Antigravity — `sources/06-antigravity/observability-engineer/`
- `observability-monitoring-monitor-setup` — Antigravity — `sources/06-antigravity/observability-monitoring-monitor-setup/`
- `observability-monitoring-slo-implement` — Antigravity — `sources/06-antigravity/observability-monitoring-slo-implement/`
- `observe-whatsapp` — Antigravity — `sources/06-antigravity/observe-whatsapp/`
- `obsidian-clipper-template-creator` — Antigravity — `sources/06-antigravity/obsidian-clipper-template-creator/`
- `offensive-ai-security` — skills — `skills/offensive-ai-security/`
- `offensive-ai-security` — Claude-Red — `sources/13-claude-red/offensive-ai-security/`
- `offensive-bug-identification` — skills — `skills/offensive-bug-identification/`
- `offensive-bug-identification` — Claude-Red — `sources/13-claude-red/offensive-bug-identification/`
- `offensive-business-logic` — skills — `skills/offensive-business-logic/`
- `offensive-business-logic` — Claude-Red — `sources/13-claude-red/offensive-business-logic/`
- `offensive-cloud` — skills — `skills/offensive-cloud/`
- `offensive-cloud` — Claude-Red — `sources/13-claude-red/offensive-cloud/`
- `offensive-deserialization` — skills — `skills/offensive-deserialization/`
- `offensive-deserialization` — Claude-Red — `sources/13-claude-red/offensive-deserialization/`
- `offensive-fast-checking` — skills — `skills/offensive-fast-checking/`
- `offensive-fast-checking` — Claude-Red — `sources/13-claude-red/offensive-fast-checking/`
- `offensive-file-upload` — skills — `skills/offensive-file-upload/`
- `offensive-file-upload` — Claude-Red — `sources/13-claude-red/offensive-file-upload/`
- `offensive-fuzzing` — skills — `skills/offensive-fuzzing/`
- `offensive-fuzzing` — Claude-Red — `sources/13-claude-red/offensive-fuzzing/`
- `offensive-graphql` — skills — `skills/offensive-graphql/`
- `offensive-graphql` — Claude-Red — `sources/13-claude-red/offensive-graphql/`
- `offensive-idor` — skills — `skills/offensive-idor/`
- `offensive-idor` — Claude-Red — `sources/13-claude-red/offensive-idor/`
- `offensive-jwt` — skills — `skills/offensive-jwt/`
- `offensive-jwt` — Claude-Red — `sources/13-claude-red/offensive-jwt/`
- `offensive-mobile` — skills — `skills/offensive-mobile/`
- `offensive-mobile` — Claude-Red — `sources/13-claude-red/offensive-mobile/`
- `offensive-oauth` — skills — `skills/offensive-oauth/`
- `offensive-oauth` — Claude-Red — `sources/13-claude-red/offensive-oauth/`
- `offensive-open-redirect` — skills — `skills/offensive-open-redirect/`
- `offensive-open-redirect` — Claude-Red — `sources/13-claude-red/offensive-open-redirect/`
- `offensive-osint` — skills — `skills/offensive-osint/`
- `offensive-osint` — Claude-Red — `sources/13-claude-red/offensive-osint/`
- `offensive-parameter-pollution` — skills — `skills/offensive-parameter-pollution/`
- `offensive-parameter-pollution` — Claude-Red — `sources/13-claude-red/offensive-parameter-pollution/`
- `offensive-race-condition` — skills — `skills/offensive-race-condition/`
- `offensive-race-condition` — Claude-Red — `sources/13-claude-red/offensive-race-condition/`
- `offensive-rce` — skills — `skills/offensive-rce/`
- `offensive-rce` — Claude-Red — `sources/13-claude-red/offensive-rce/`
- `offensive-reporting` — skills — `skills/offensive-reporting/`
- `offensive-reporting` — Claude-Red — `sources/13-claude-red/offensive-reporting/`
- `offensive-request-smuggling` — skills — `skills/offensive-request-smuggling/`
- `offensive-request-smuggling` — Claude-Red — `sources/13-claude-red/offensive-request-smuggling/`
- `offensive-sqli` — skills — `skills/offensive-sqli/`
- `offensive-sqli` — Claude-Red — `sources/13-claude-red/offensive-sqli/`
- `offensive-ssrf` — skills — `skills/offensive-ssrf/`
- `offensive-ssrf` — Claude-Red — `sources/13-claude-red/offensive-ssrf/`
- `offensive-ssti` — skills — `skills/offensive-ssti/`
- `offensive-ssti` — Claude-Red — `sources/13-claude-red/offensive-ssti/`
- `offensive-toctou` — skills — `skills/offensive-toctou/`
- `offensive-toctou` — Claude-Red — `sources/13-claude-red/offensive-toctou/`
- `offensive-waf-bypass` — skills — `skills/offensive-waf-bypass/`
- `offensive-waf-bypass` — Claude-Red — `sources/13-claude-red/offensive-waf-bypass/`
- `offensive-xss` — skills — `skills/offensive-xss/`
- `offensive-xss` — Claude-Red — `sources/13-claude-red/offensive-xss/`
- `offensive-xxe` — skills — `skills/offensive-xxe/`
- `offensive-xxe` — Claude-Red — `sources/13-claude-red/offensive-xxe/`
- `on-call-handoff-patterns` — Antigravity — `sources/06-antigravity/on-call-handoff-patterns/`
- `onboarding-cro` — Antigravity — `sources/06-antigravity/onboarding-cro/`
- `openapi-spec-generation` — Antigravity — `sources/06-antigravity/openapi-spec-generation/`
- `openui-genui-layout` — skills — `skills/openui-genui-layout/`
- `osforge-canvas` — skills — `skills/osforge-canvas/`
- `osforge-evolve` — skills — `skills/evolve/`
- `oss-hunter` — Antigravity — `sources/06-antigravity/oss-hunter/`
- `ossfuzz` — Trail of Bits — `sources/07-trailofbits/testing-handbook-skills/skills/ossfuzz/`
- `output-enforcement` — skills — `skills/output-enforcement/`

**P**
- `page-cro` — Antigravity — `sources/06-antigravity/page-cro/`
- `paid-ads` — Antigravity — `sources/06-antigravity/paid-ads/`
- `parallel-agents` — Antigravity — `sources/06-antigravity/parallel-agents/`
- `payment-integration` — Antigravity — `sources/06-antigravity/payment-integration/`
- `paypal-integration` — Antigravity — `sources/06-antigravity/paypal-integration/`
- `paywall-upgrade-cro` — Antigravity — `sources/06-antigravity/paywall-upgrade-cro/`
- `pc-games` — skills — `skills/game-development/pc-games/`
- `pc-games` — Antigravity — `sources/06-antigravity/game-development/pc-games/`
- `pci-compliance` — Antigravity — `sources/06-antigravity/pci-compliance/`
- `pdf` — Anthropic — `sources/01-anthropic/pdf/`
- `pdf` — Antigravity — `sources/06-antigravity/pdf-official/`
- `Pentest Checklist` — Antigravity — `sources/06-antigravity/pentest-checklist/`
- `Pentest Commands` — Antigravity — `sources/06-antigravity/pentest-commands/`
- `performance-engineer` — Antigravity — `sources/06-antigravity/performance-engineer/`
- `performance-profiling` — skills — `skills/performance-profiling/`
- `performance-profiling` — Antigravity — `sources/06-antigravity/performance-profiling/`
- `performance-testing-review-ai-review` — Antigravity — `sources/06-antigravity/performance-testing-review-ai-review/`
- `performance-testing-review-multi-agent-review` — Antigravity — `sources/06-antigravity/performance-testing-review-multi-agent-review/`
- `personal-tool-builder` — Antigravity — `sources/06-antigravity/personal-tool-builder/`
- `phase-discussion` — skills — `skills/planning/phase-discussion/`
- `php-pro` — Antigravity — `sources/06-antigravity/php-pro/`
- `plaid-fintech` — Antigravity — `sources/06-antigravity/plaid-fintech/`
- `plan-writing` — skills — `skills/plan-writing/`
- `plan-writing` — Antigravity — `sources/06-antigravity/plan-writing/`
- `planning-with-files` — Antigravity — `sources/06-antigravity/planning-with-files/`
- `playwright-skill` — Antigravity — `sources/06-antigravity/playwright-skill/`
- `popup-cro` — Antigravity — `sources/06-antigravity/popup-cro/`
- `posix-shell-pro` — Antigravity — `sources/06-antigravity/posix-shell-pro/`
- `postgres-optimization` — skills — `skills/postgres-optimization/`
- `postgresql` — Antigravity — `sources/06-antigravity/postgresql/`
- `postmortem-writing` — Antigravity — `sources/06-antigravity/postmortem-writing/`
- `powershell-windows` — skills — `skills/powershell-windows/`
- `powershell-windows` — Antigravity — `sources/06-antigravity/powershell-windows/`
- `pptx` — Anthropic — `sources/01-anthropic/pptx/`
- `pptx` — Antigravity — `sources/06-antigravity/pptx-official/`
- `prd-builder` — skills — `skills/planning/prd-builder/`
- `predictive-failure` — skills — `skills/predictive-failure/`
- `pricing-strategy` — Antigravity — `sources/06-antigravity/pricing-strategy/`
- `prisma-expert` — skills — `skills/prisma-expert/`
- `prisma-expert` — Antigravity — `sources/06-antigravity/prisma-expert/`
- `Privilege Escalation Methods` — Antigravity — `sources/06-antigravity/privilege-escalation-methods/`
- `product-manager-toolkit` — Antigravity — `sources/06-antigravity/product-manager-toolkit/`
- `production-code-audit` — Antigravity — `sources/06-antigravity/production-code-audit/`
- `programmatic-seo` — Antigravity — `sources/06-antigravity/programmatic-seo/`
- `project-context-generator` — skills — `skills/context/project-context-generator/`
- `project-development` — Context Enginee — `sources/05-context-engineering/project-development/`
- `projection-patterns` — Antigravity — `sources/06-antigravity/projection-patterns/`
- `prometheus-configuration` — Antigravity — `sources/06-antigravity/prometheus-configuration/`
- `prompt-caching` — Antigravity — `sources/06-antigravity/prompt-caching/`
- `prompt-engineer` — Antigravity — `sources/06-antigravity/prompt-engineer/`
- `prompt-engineering` — Antigravity — `sources/06-antigravity/prompt-engineering/`
- `prompt-engineering-patterns` — Antigravity — `sources/06-antigravity/prompt-engineering-patterns/`
- `prompt-library` — Antigravity — `sources/06-antigravity/prompt-library/`
- `property-based-testing` — Trail of Bits — `sources/07-trailofbits/property-based-testing/skills/property-based-testing/`
- `protocol-reverse-engineering` — Antigravity — `sources/06-antigravity/protocol-reverse-engineering/`
- `pypict-skill` — Antigravity — `sources/06-antigravity/pypict-skill/`
- `python-development-python-scaffold` — Antigravity — `sources/06-antigravity/python-development-python-scaffold/`
- `python-packaging` — Antigravity — `sources/06-antigravity/python-packaging/`
- `python-patterns` — skills — `skills/python-patterns/`
- `python-patterns` — Antigravity — `sources/06-antigravity/python-patterns/`
- `python-performance-optimization` — Antigravity — `sources/06-antigravity/python-performance-optimization/`
- `python-pro` — Antigravity — `sources/06-antigravity/python-pro/`
- `python-testing-patterns` — Antigravity — `sources/06-antigravity/python-testing-patterns/`

**Q**
- `quant-analyst` — Antigravity — `sources/06-antigravity/quant-analyst/`

**R**
- `radix-ui-design-system` — Antigravity — `sources/06-antigravity/radix-ui-design-system/`
- `rag-engineer` — Antigravity — `sources/06-antigravity/rag-engineer/`
- `rag-implementation` — Antigravity — `sources/06-antigravity/rag-implementation/`
- `react-modernization` — Antigravity — `sources/06-antigravity/react-modernization/`
- `react-native-architecture` — Antigravity — `sources/06-antigravity/react-native-architecture/`
- `react-patterns` — Antigravity — `sources/06-antigravity/react-patterns/`
- `react-performance` — skills — `skills/react-performance/`
- `react-state-management` — Antigravity — `sources/06-antigravity/react-state-management/`
- `react-ui-patterns` — Antigravity — `sources/06-antigravity/react-ui-patterns/`
- `readiness-gate` — skills — `skills/quality/readiness-gate/`
- `readme` — Antigravity — `sources/06-antigravity/readme/`
- `reasoning-trace-optimizer` — Context Enginee — `sources/05-context-engineering/_examples/interleaved_thinking/`
- `receiving-code-review` — skills — `skills/receiving-code-review/`
- `receiving-code-review` — Superpowers — `sources/02-superpowers/receiving-code-review/`
- `receiving-code-review` — Antigravity — `sources/06-antigravity/receiving-code-review/`
- `Red Team Tools and Methodology` — Antigravity — `sources/06-antigravity/red-team-tools/`
- `red-team-tactics` — skills — `skills/red-team-tactics/`
- `red-team-tactics` — Antigravity — `sources/06-antigravity/red-team-tactics/`
- `redesign-audit` — skills — `skills/redesign-audit/`
- `redesign-existing-projects` — skills — `skills/redesign-existing-projects/`
- `reference-builder` — Antigravity — `sources/06-antigravity/reference-builder/`
- `referral-program` — Antigravity — `sources/06-antigravity/referral-program/`
- `remotion-best-practices` — Antigravity — `sources/06-antigravity/remotion-best-practices/`
- `requesting-code-review` — Superpowers — `sources/02-superpowers/requesting-code-review/`
- `requesting-code-review` — Antigravity — `sources/06-antigravity/requesting-code-review/`
- `requirements-clarify` — skills — `skills/planning/requirements-clarify/`
- `research-engineer` — Antigravity — `sources/06-antigravity/research-engineer/`
- `reverse-engineer` — Antigravity — `sources/06-antigravity/reverse-engineer/`
- `risk-manager` — Antigravity — `sources/06-antigravity/risk-manager/`
- `risk-metrics-calculation` — Antigravity — `sources/06-antigravity/risk-metrics-calculation/`
- `ruby-pro` — Antigravity — `sources/06-antigravity/ruby-pro/`
- `rust-async-patterns` — Antigravity — `sources/06-antigravity/rust-async-patterns/`
- `rust-pro` — skills — `skills/rust-pro/`
- `rust-pro` — Antigravity — `sources/06-antigravity/rust-pro/`
- `ruzzy` — Trail of Bits — `sources/07-trailofbits/testing-handbook-skills/skills/ruzzy/`

**S**
- `saga-orchestration` — Antigravity — `sources/06-antigravity/saga-orchestration/`
- `sales-automator` — Antigravity — `sources/06-antigravity/sales-automator/`
- `salesforce-development` — Antigravity — `sources/06-antigravity/salesforce-development/`
- `sandbox-sdk` — Cloudflare — `sources/10-cloudflare/sandbox-sdk/`
- `sarif-parsing` — Trail of Bits — `sources/07-trailofbits/static-analysis/skills/sarif-parsing/`
- `sast-configuration` — Antigravity — `sources/06-antigravity/sast-configuration/`
- `scala-pro` — Antigravity — `sources/06-antigravity/scala-pro/`
- `schema-markup` — Antigravity — `sources/06-antigravity/schema-markup/`
- `screen-reader-testing` — Antigravity — `sources/06-antigravity/screen-reader-testing/`
- `screenshots` — Antigravity — `sources/06-antigravity/screenshots/`
- `scroll-experience` — Antigravity — `sources/06-antigravity/scroll-experience/`
- `search-specialist` — Antigravity — `sources/06-antigravity/search-specialist/`
- `secrets-management` — Antigravity — `sources/06-antigravity/secrets-management/`
- `secure-workflow-guide` — Trail of Bits — `sources/07-trailofbits/building-secure-contracts/skills/secure-workflow-guide/`
- `Security Scanning Tools` — Antigravity — `sources/06-antigravity/scanning-tools/`
- `security-auditor` — Antigravity — `sources/06-antigravity/security-auditor/`
- `security-best-practices` — skills — `skills/security-best-practices/`
- `security-bluebook-builder` — Antigravity — `sources/06-antigravity/security-bluebook-builder/`
- `security-compliance-compliance-check` — Antigravity — `sources/06-antigravity/security-compliance-compliance-check/`
- `security-requirement-extraction` — Antigravity — `sources/06-antigravity/security-requirement-extraction/`
- `security-review` — Antigravity — `sources/06-antigravity/cc-skill-security-review/`
- `security-review` — Sentry — `sources/11-sentry/security-review/`
- `security-scanning-security-dependencies` — Antigravity — `sources/06-antigravity/security-scanning-security-dependencies/`
- `security-scanning-security-hardening` — Antigravity — `sources/06-antigravity/security-scanning-security-hardening/`
- `security-scanning-security-sast` — Antigravity — `sources/06-antigravity/security-scanning-security-sast/`
- `security-threat-model` — skills — `skills/security-threat-model/`
- `segment-cdp` — Antigravity — `sources/06-antigravity/segment-cdp/`
- `semgrep` — Trail of Bits — `sources/07-trailofbits/static-analysis/skills/semgrep/`
- `semgrep` — Trail of Bits — `sources/07-trailofbits/testing-handbook-skills/skills/semgrep/`
- `semgrep-rule-creator` — Trail of Bits — `sources/07-trailofbits/semgrep-rule-creator/skills/semgrep-rule-creator/`
- `semgrep-rule-variant-creator` — Trail of Bits — `sources/07-trailofbits/semgrep-rule-variant-creator/skills/semgrep-rule-variant-creator/`
- `senior-architect` — Antigravity — `sources/06-antigravity/senior-architect/`
- `senior-fullstack` — Antigravity — `sources/06-antigravity/senior-fullstack/`
- `seo` — skills — `skills/seo/`
- `seo-audit` — Antigravity — `sources/06-antigravity/seo-audit/`
- `seo-authority-builder` — Antigravity — `sources/06-antigravity/seo-authority-builder/`
- `seo-cannibalization-detector` — Antigravity — `sources/06-antigravity/seo-cannibalization-detector/`
- `seo-content-auditor` — Antigravity — `sources/06-antigravity/seo-content-auditor/`
- `seo-content-planner` — Antigravity — `sources/06-antigravity/seo-content-planner/`
- `seo-content-refresher` — Antigravity — `sources/06-antigravity/seo-content-refresher/`
- `seo-content-writer` — Antigravity — `sources/06-antigravity/seo-content-writer/`
- `seo-fundamentals` — skills — `skills/seo-fundamentals/`
- `seo-fundamentals` — Antigravity — `sources/06-antigravity/seo-fundamentals/`
- `seo-keyword-strategist` — Antigravity — `sources/06-antigravity/seo-keyword-strategist/`
- `seo-meta-optimizer` — Antigravity — `sources/06-antigravity/seo-meta-optimizer/`
- `seo-snippet-hunter` — Antigravity — `sources/06-antigravity/seo-snippet-hunter/`
- `seo-structure-architect` — Antigravity — `sources/06-antigravity/seo-structure-architect/`
- `server-management` — skills — `skills/server-management/`
- `server-management` — Antigravity — `sources/06-antigravity/server-management/`
- `service-mesh-expert` — Antigravity — `sources/06-antigravity/service-mesh-expert/`
- `service-mesh-observability` — Antigravity — `sources/06-antigravity/service-mesh-observability/`
- `sharp-edges` — Antigravity — `sources/06-antigravity/sharp-edges/`
- `sharp-edges` — Trail of Bits — `sources/07-trailofbits/sharp-edges/skills/sharp-edges/`
- `shellcheck-configuration` — Antigravity — `sources/06-antigravity/shellcheck-configuration/`
- `Shodan Reconnaissance and Pentesting` — Antigravity — `sources/06-antigravity/shodan-reconnaissance/`
- `shopify-apps` — Antigravity — `sources/06-antigravity/shopify-apps/`
- `shopify-development` — Antigravity — `sources/06-antigravity/shopify-development/`
- `signup-flow-cro` — Antigravity — `sources/06-antigravity/signup-flow-cro/`
- `similarity-search-patterns` — Antigravity — `sources/06-antigravity/similarity-search-patterns/`
- `skill-creator` — skills — `skills/skill-creator/`
- `skill-creator` — Anthropic — `sources/01-anthropic/skill-creator/`
- `skill-creator` — Antigravity — `sources/06-antigravity/skill-creator/`
- `skill-developer` — Antigravity — `sources/06-antigravity/skill-developer/`
- `skill-rails-upgrade` — Antigravity — `sources/06-antigravity/skill-rails-upgrade/`
- `skill-seekers` — Antigravity — `sources/06-antigravity/skill-seekers/`
- `skill-template` — Context Enginee — `sources/05-context-engineering/_template/`
- `slack-bot-builder` — Antigravity — `sources/06-antigravity/slack-bot-builder/`
- `slack-gif-creator` — Anthropic — `sources/01-anthropic/slack-gif-creator/`
- `slack-gif-creator` — Antigravity — `sources/06-antigravity/slack-gif-creator/`
- `slo-implementation` — Antigravity — `sources/06-antigravity/slo-implementation/`
- `smart-hooks` — skills — `skills/smart-hooks/`
- `smart-model-dispatch` — skills — `skills/smart-model-dispatch/`
- `SMTP Penetration Testing` — Antigravity — `sources/06-antigravity/smtp-penetration-testing/`
- `social-content` — Antigravity — `sources/06-antigravity/social-content/`
- `software-architecture` — Antigravity — `sources/06-antigravity/software-architecture/`
- `solana-vulnerability-scanner` — Trail of Bits — `sources/07-trailofbits/building-secure-contracts/skills/solana-vulnerability-scanner/`
- `solidity-security` — Antigravity — `sources/06-antigravity/solidity-security/`
- `spark-optimization` — Antigravity — `sources/06-antigravity/spark-optimization/`
- `spec-builder` — skills — `skills/planning/spec-builder/`
- `spec-to-code-compliance` — Trail of Bits — `sources/07-trailofbits/spec-to-code-compliance/skills/spec-to-code-compliance/`
- `SQL Injection Testing` — Antigravity — `sources/06-antigravity/sql-injection-testing/`
- `sql-optimization-patterns` — Antigravity — `sources/06-antigravity/sql-optimization-patterns/`
- `sql-pro` — Antigravity — `sources/06-antigravity/sql-pro/`
- `SQLMap Database Penetration Testing` — Antigravity — `sources/06-antigravity/sqlmap-database-pentesting/`
- `SSH Penetration Testing` — Antigravity — `sources/06-antigravity/ssh-penetration-testing/`
- `startup-analyst` — Antigravity — `sources/06-antigravity/startup-analyst/`
- `startup-business-analyst-business-case` — Antigravity — `sources/06-antigravity/startup-business-analyst-business-case/`
- `startup-business-analyst-financial-projections` — Antigravity — `sources/06-antigravity/startup-business-analyst-financial-projections/`
- `startup-business-analyst-market-opportunity` — Antigravity — `sources/06-antigravity/startup-business-analyst-market-opportunity/`
- `startup-financial-modeling` — Antigravity — `sources/06-antigravity/startup-financial-modeling/`
- `startup-metrics-framework` — Antigravity — `sources/06-antigravity/startup-metrics-framework/`
- `stitch-design-export` — skills — `skills/stitch-design-export/`
- `stitch-design-taste` — skills — `skills/stitch-design-taste/`
- `stitch-ui-design` — Antigravity — `sources/06-antigravity/stitch-ui-design/`
- `story-executor` — skills — `skills/planning/story-executor/`
- `stride-analysis-patterns` — Antigravity — `sources/06-antigravity/stride-analysis-patterns/`
- `stripe-integration` — skills — `skills/stripe-integration/`
- `stripe-integration` — Antigravity — `sources/06-antigravity/stripe-integration/`
- `stuck-recovery` — skills — `skills/stuck-recovery/`
- `subagent-driven-development` — Superpowers — `sources/02-superpowers/subagent-driven-development/`
- `subagent-driven-development` — Antigravity — `sources/06-antigravity/subagent-driven-development/`
- `substrate-vulnerability-scanner` — Trail of Bits — `sources/07-trailofbits/building-secure-contracts/skills/substrate-vulnerability-scanner/`
- `supabase-postgres-best-practices` — Antigravity — `sources/06-antigravity/postgres-best-practices/`
- `supabase-postgres-best-practices` — Supabase — `sources/08-supabase/supabase-postgres-best-practices/`
- `superpowers-lab` — Antigravity — `sources/06-antigravity/superpowers-lab/`
- `swiftui-expert-skill` — Antigravity — `sources/06-antigravity/swiftui-expert-skill/`
- `systematic-debugging` — skills — `skills/systematic-debugging/`
- `systematic-debugging` — Superpowers — `sources/02-superpowers/systematic-debugging/`
- `systematic-debugging` — Antigravity — `sources/06-antigravity/systematic-debugging/`
- `systems-programming-rust-project` — Antigravity — `sources/06-antigravity/systems-programming-rust-project/`

**T**
- `tailwind-design-system` — Antigravity — `sources/06-antigravity/tailwind-design-system/`
- `tailwind-patterns` — skills — `skills/tailwind-patterns/`
- `tailwind-patterns` — Antigravity — `sources/06-antigravity/tailwind-patterns/`
- `taste-design-dials` — skills — `skills/taste-design-dials/`
- `tavily-web` — Antigravity — `sources/06-antigravity/tavily-web/`
- `tdd-orchestrator` — Antigravity — `sources/06-antigravity/tdd-orchestrator/`
- `tdd-workflow` — skills — `skills/tdd-workflow/`
- `tdd-workflow` — Antigravity — `sources/06-antigravity/tdd-workflow/`
- `tdd-workflows-tdd-cycle` — Antigravity — `sources/06-antigravity/tdd-workflows-tdd-cycle/`
- `tdd-workflows-tdd-green` — Antigravity — `sources/06-antigravity/tdd-workflows-tdd-green/`
- `tdd-workflows-tdd-red` — Antigravity — `sources/06-antigravity/tdd-workflows-tdd-red/`
- `tdd-workflows-tdd-refactor` — Antigravity — `sources/06-antigravity/tdd-workflows-tdd-refactor/`
- `team-collaboration-issue` — Antigravity — `sources/06-antigravity/team-collaboration-issue/`
- `team-collaboration-standup-notes` — Antigravity — `sources/06-antigravity/team-collaboration-standup-notes/`
- `team-composition-analysis` — Antigravity — `sources/06-antigravity/team-composition-analysis/`
- `technical-design-doc-creator` — skills — `skills/technical-design-doc-creator/`
- `telegram-bot-builder` — Antigravity — `sources/06-antigravity/telegram-bot-builder/`
- `telegram-mini-app` — Antigravity — `sources/06-antigravity/telegram-mini-app/`
- `template-skill` — Anthropic — `sources/01-anthropic/_template/`
- `templates` — Antigravity — `sources/06-antigravity/app-builder/templates/`
- `temporal-python-pro` — Antigravity — `sources/06-antigravity/temporal-python-pro/`
- `temporal-python-testing` — Antigravity — `sources/06-antigravity/temporal-python-testing/`
- `terraform-module-library` — Antigravity — `sources/06-antigravity/terraform-module-library/`
- `terraform-skill` — Antigravity — `sources/06-antigravity/terraform-skill/`
- `terraform-specialist` — Antigravity — `sources/06-antigravity/terraform-specialist/`
- `test-automator` — Antigravity — `sources/06-antigravity/test-automator/`
- `test-driven-development` — Superpowers — `sources/02-superpowers/test-driven-development/`
- `test-driven-development` — Antigravity — `sources/06-antigravity/test-driven-development/`
- `test-fixing` — Antigravity — `sources/06-antigravity/test-fixing/`
- `testing-handbook-generator` — Trail of Bits — `sources/07-trailofbits/testing-handbook-skills/skills/testing-handbook-generator/`
- `testing-patterns` — skills — `skills/testing-patterns/`
- `testing-patterns` — Antigravity — `sources/06-antigravity/testing-patterns/`
- `theme-factory` — Anthropic — `sources/01-anthropic/theme-factory/`
- `theme-factory` — Antigravity — `sources/06-antigravity/theme-factory/`
- `threat-mitigation-mapping` — Antigravity — `sources/06-antigravity/threat-mitigation-mapping/`
- `threat-modeling-expert` — Antigravity — `sources/06-antigravity/threat-modeling-expert/`
- `threejs-skills` — Antigravity — `sources/06-antigravity/threejs-skills/`
- `tlc-spec-driven` — skills — `skills/tlc-spec-driven/`
- `token-integration-analyzer` — Trail of Bits — `sources/07-trailofbits/building-secure-contracts/skills/token-integration-analyzer/`
- `ton-vulnerability-scanner` — Trail of Bits — `sources/07-trailofbits/building-secure-contracts/skills/ton-vulnerability-scanner/`
- `tool-design` — Context Enginee — `sources/05-context-engineering/tool-design/`
- `tool-design` — Antigravity — `sources/06-antigravity/tool-design/`
- `tool-safety-classifier` — skills — `skills/tool-safety-classifier/`
- `Top 100 Web Vulnerabilities Reference` — Antigravity — `sources/06-antigravity/top-web-vulnerabilities/`
- `track-management` — Antigravity — `sources/06-antigravity/track-management/`
- `trigger-dev` — Antigravity — `sources/06-antigravity/trigger-dev/`
- `turborepo-caching` — Antigravity — `sources/06-antigravity/turborepo-caching/`
- `tutorial-engineer` — Antigravity — `sources/06-antigravity/tutorial-engineer/`
- `twilio-communications` — Antigravity — `sources/06-antigravity/twilio-communications/`
- `typescript-advanced-types` — Antigravity — `sources/06-antigravity/typescript-advanced-types/`
- `typescript-expert` — Antigravity — `sources/06-antigravity/typescript-expert/`
- `typescript-pro` — Antigravity — `sources/06-antigravity/typescript-pro/`

**U**
- `ui-audit` — skills — `skills/quality/ui-audit/`
- `ui-design-intelligence` — skills — `skills/ui-design-intelligence/`
- `ui-skills` — Antigravity — `sources/06-antigravity/ui-skills/`
- `ui-ux-designer` — Antigravity — `sources/06-antigravity/ui-ux-designer/`
- `ui-ux-pro-max` — Antigravity — `sources/06-antigravity/ui-ux-pro-max/`
- `ui-visual-validator` — Antigravity — `sources/06-antigravity/ui-visual-validator/`
- `unit-testing-test-generate` — Antigravity — `sources/06-antigravity/unit-testing-test-generate/`
- `unity-developer` — Antigravity — `sources/06-antigravity/unity-developer/`
- `unity-ecs-patterns` — Antigravity — `sources/06-antigravity/unity-ecs-patterns/`
- `unreal-engine-cpp-pro` — Antigravity — `sources/06-antigravity/unreal-engine-cpp-pro/`
- `upgrading-expo` — Antigravity — `sources/06-antigravity/upgrading-expo/`
- `upgrading-expo` — Expo — `sources/09-expo/upgrading-expo/skills/upgrading-expo/`
- `upstash-qstash` — Antigravity — `sources/06-antigravity/upstash-qstash/`
- `use-dom` — Expo — `sources/09-expo/expo-app-design/skills/use-dom/`
- `using-git-worktrees` — skills — `skills/using-git-worktrees/`
- `using-git-worktrees` — Superpowers — `sources/02-superpowers/using-git-worktrees/`
- `using-git-worktrees` — Antigravity — `sources/06-antigravity/using-git-worktrees/`
- `using-neon` — Antigravity — `sources/06-antigravity/using-neon/`
- `using-superpowers` — Superpowers — `sources/02-superpowers/using-superpowers/`
- `using-superpowers` — Antigravity — `sources/06-antigravity/using-superpowers/`
- `uv-package-manager` — Antigravity — `sources/06-antigravity/uv-package-manager/`

**V**
- `variant-analysis` — Trail of Bits — `sources/07-trailofbits/variant-analysis/skills/variant-analysis/`
- `varlock-claude-skill` — Antigravity — `sources/06-antigravity/varlock-claude-skill/`
- `vector-database-engineer` — Antigravity — `sources/06-antigravity/vector-database-engineer/`
- `vector-index-tuning` — Antigravity — `sources/06-antigravity/vector-index-tuning/`
- `vercel-composition-patterns` — Vercel Labs — `sources/04-vercel/composition-patterns/`
- `vercel-deploy` — skills — `skills/vercel-deploy/`
- `vercel-deploy` — Vercel Labs — `sources/04-vercel/claude.ai/vercel-deploy-claimable/`
- `vercel-deploy-claimable` — Antigravity — `sources/06-antigravity/vercel-deploy-claimable/`
- `vercel-deployment` — Antigravity — `sources/06-antigravity/vercel-deployment/`
- `vercel-react-best-practices` — Vercel Labs — `sources/04-vercel/react-best-practices/`
- `vercel-react-best-practices` — Antigravity — `sources/06-antigravity/react-best-practices/`
- `vercel-react-native-skills` — Vercel Labs — `sources/04-vercel/react-native-skills/`
- `verification-before-completion` — skills — `skills/verification-before-completion/`
- `verification-before-completion` — Superpowers — `sources/02-superpowers/verification-before-completion/`
- `verification-before-completion` — Antigravity — `sources/06-antigravity/verification-before-completion/`
- `vexor` — Antigravity — `sources/06-antigravity/vexor/`
- `viral-generator-builder` — Antigravity — `sources/06-antigravity/viral-generator-builder/`
- `visual-planner` — skills — `skills/visual-planner/`
- `voice-agents` — Antigravity — `sources/06-antigravity/voice-agents/`
- `voice-ai-development` — Antigravity — `sources/06-antigravity/voice-ai-development/`
- `voice-ai-engine-development` — Antigravity — `sources/06-antigravity/voice-ai-engine-development/`
- `vr-ar` — skills — `skills/game-development/vr-ar/`
- `vr-ar` — Antigravity — `sources/06-antigravity/game-development/vr-ar/`
- `vulnerability-scanner` — skills — `skills/vulnerability-scanner/`
- `vulnerability-scanner` — Antigravity — `sources/06-antigravity/vulnerability-scanner/`

**W**
- `wcag-audit-patterns` — Antigravity — `sources/06-antigravity/wcag-audit-patterns/`
- `web-artifacts-builder` — Anthropic — `sources/01-anthropic/web-artifacts-builder/`
- `web-artifacts-builder` — Antigravity — `sources/06-antigravity/web-artifacts-builder/`
- `web-design-guidelines` — skills — `skills/web-design-guidelines/`
- `web-design-guidelines` — Vercel Labs — `sources/04-vercel/web-design-guidelines/`
- `web-design-guidelines` — Antigravity — `sources/06-antigravity/web-design-guidelines/`
- `web-games` — skills — `skills/game-development/web-games/`
- `web-games` — Antigravity — `sources/06-antigravity/game-development/web-games/`
- `web-perf` — Cloudflare — `sources/10-cloudflare/web-perf/`
- `web-performance-optimization` — Antigravity — `sources/06-antigravity/web-performance-optimization/`
- `web3-testing` — Antigravity — `sources/06-antigravity/web3-testing/`
- `webapp-testing` — skills — `skills/webapp-testing/`
- `webapp-testing` — Anthropic — `sources/01-anthropic/webapp-testing/`
- `webapp-testing` — Antigravity — `sources/06-antigravity/webapp-testing/`
- `Windows Privilege Escalation` — Antigravity — `sources/06-antigravity/windows-privilege-escalation/`
- `Wireshark Network Traffic Analysis` — Antigravity — `sources/06-antigravity/wireshark-analysis/`
- `WordPress Penetration Testing` — Antigravity — `sources/06-antigravity/wordpress-penetration-testing/`
- `workflow-automation` — Antigravity — `sources/06-antigravity/workflow-automation/`
- `workflow-orchestration-patterns` — Antigravity — `sources/06-antigravity/workflow-orchestration-patterns/`
- `workflow-patterns` — Antigravity — `sources/06-antigravity/workflow-patterns/`
- `wrangler` — Cloudflare — `sources/10-cloudflare/wrangler/`
- `writing-plans` — Superpowers — `sources/02-superpowers/writing-plans/`
- `writing-plans` — Antigravity — `sources/06-antigravity/writing-plans/`
- `writing-skills` — Superpowers — `sources/02-superpowers/writing-skills/`
- `writing-skills` — Antigravity — `sources/06-antigravity/writing-skills/`
- `wycheproof` — Trail of Bits — `sources/07-trailofbits/testing-handbook-skills/skills/wycheproof/`

**X**
- `x-article-publisher-skill` — Antigravity — `sources/06-antigravity/x-article-publisher-skill/`
- `xlsx` — Anthropic — `sources/01-anthropic/xlsx/`
- `xlsx` — Antigravity — `sources/06-antigravity/xlsx-official/`

**Y**
- `yara-rule-authoring` — Trail of Bits — `sources/07-trailofbits/yara-authoring/skills/yara-rule-authoring/`
- `youtube-summarizer` — Antigravity — `sources/06-antigravity/youtube-summarizer/`

**Z**
- `zapier-make-patterns` — Antigravity — `sources/06-antigravity/zapier-make-patterns/`

---

*Índice gerado automaticamente por Claude Opus 4.6 a partir de 770 SKILL.md files.*