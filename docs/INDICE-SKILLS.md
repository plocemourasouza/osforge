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
| 🔒 Security | 47 | 27.6% |
| 📱 Mobile | 25 | 14.7% |
| 🤖 AI / ML / Agents | 23 | 13.5% |
| 🔄 Workflow / Process | 22 | 12.9% |
| ⚛️ React / Frontend | 21 | 12.4% |
| 🧪 Testing | 16 | 9.4% |
| 🏗️ Architecture | 5 | 2.9% |
| 📝 Documentation / Writing | 4 | 2.4% |
| ☁️ Infrastructure / DevOps | 3 | 1.8% |
| 🗄️ Database / Backend | 3 | 1.8% |
| 💼 Business / Marketing | 1 | 0.6% |
| **TOTAL** | **170** | **100%** |

### Por Origem

| Origem | Repo | Qtd |
|--------|------|-----|
| skills | — | 170 |

---

## 🗂️ Sumário por Categoria

- [🔒 Security (47)](#)
- [📱 Mobile (25)](#)
- [🤖 AI / ML / Agents (23)](#)
- [🔄 Workflow / Process (22)](#)
- [⚛️ React / Frontend (21)](#)
- [🧪 Testing (16)](#)
- [🏗️ Architecture (5)](#)
- [📝 Documentation / Writing (4)](#)
- [☁️ Infrastructure / DevOps (3)](#)
- [🗄️ Database / Backend (3)](#)
- [💼 Business / Marketing (1)](#)

---

## 🔒 Security

**47 skills**

| Skill | Origem | Descrição | Path Local |
|-------|--------|-----------|-----------|
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
| **red-team-tactics** | 📦 skills | Táticas de red team baseadas em MITRE ATT&CK para simulação de adversário autorizada. ACIONE quando: planejar simulação de ataque/pentest autorizado, … | `skills/red-team-tactics/` |
| **redesign-audit** | 📦 skills | OSForge enhancement layer sobre redesign-existing-projects. Audita projeto existente, identifica padrões AI-genéricos, aplica upgrades cirúrgicos + re… | `skills/redesign-audit/` |
| **redesign-existing-projects** | 📦 skills | Eleva sites e apps existentes a qualidade premium: audita o design atual, identifica padrões genéricos de IA e aplica upgrades de tipografia, cor e la… | `skills/redesign-existing-projects/` |
| **security-best-practices** | 📦 skills | Perform language and framework specific security best-practice reviews and suggest improvements. Trigger only when the user explicitly requests securi… | `skills/security-best-practices/` |
| **security-threat-model** | 📦 skills | Repository-grounded threat modeling that enumerates trust boundaries, assets, attacker capabilities, abuse paths, and mitigations, and writes a concis… | `skills/security-threat-model/` |
| **ui-audit** | 📦 skills | Auditoria retroativa de qualidade visual em código frontend já implementado. ACIONE após qualquer fase de UI/UX, ou quando: | `skills/quality/ui-audit/` |
| **vulnerability-scanner** | 📦 skills | Análise avançada de vulnerabilidades com OWASP Top 10:2025, supply chain security e priorização de risco. ACIONE quando: mapear superfície de ataque d… | `skills/vulnerability-scanner/` |
| **web-design-guidelines** | 📦 skills | Review UI code for Web Interface Guidelines compliance. Use when asked to "review my UI", "check accessibility", "audit design", "review UX", or "chec… | `skills/web-design-guidelines/` |
| **webapp-testing** | 📦 skills | Testes E2E de aplicações web com Playwright, auditoria profunda de rotas/endpoints e testes visuais, com script runner de browser incluso. ACIONE quan… | `skills/webapp-testing/` |

## 📱 Mobile

**25 skills**

| Skill | Origem | Descrição | Path Local |
|-------|--------|-----------|-----------|
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

## 🤖 AI / ML / Agents

**23 skills**

| Skill | Origem | Descrição | Path Local |
|-------|--------|-----------|-----------|
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
| **humanizer** | 📦 skills | Remove signs of AI-generated writing from text. Use when editing or reviewing text to make it sound more natural and human-written. Based on Wikipedia… | `skills/humanizer/` |
| **llmfit-advisor** | 📦 skills | Detecta o hardware da máquina (RAM, CPU, GPU/VRAM) e recomenda os melhores LLMs locais com quantização ideal, estimativa de velocidade e scoring de fi… | `skills/llmfit-advisor/` |
| **phase-discussion** | 📦 skills | Captura decisões de implementação de uma fase ANTES do planejamento técnico. ACIONE antes de planejar qualquer fase com UI, API, sistema de conteúdo o… | `skills/planning/phase-discussion/` |
| **smart-model-dispatch** | 📦 skills | Roteador de modelos Claude. ACIONE quando: spawning de subagents via Agent tool, implementando feature com múltiplas subtasks de complexidade mista, o… | `skills/smart-model-dispatch/` |
| **stuck-recovery** | 📦 skills | Detecta agent stuck patterns (loops, repetições, drift do escopo, ferramenta falhando 3x+) e executa recovery cirúrgico: salva estado em osforge-db, i… | `skills/stuck-recovery/` |
| **tlc-spec-driven** | 📦 skills | Product-driven planning with 5 phases - Discover, Specify, Design, Tasks, Implement+Validate+Measure. Creates atomic tasks with verification criteria … | `skills/tlc-spec-driven/` |
| **tool-safety-classifier** | 📦 skills | Classifier LLM-powered de segurança pra auto-aprovação de tool calls em modos autônomos (CI, headless, agent-of-agents). ACIONE quando: usuário roda e… | `skills/tool-safety-classifier/` |

## 🔄 Workflow / Process

**22 skills**

| Skill | Origem | Descrição | Path Local |
|-------|--------|-----------|-----------|
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

**21 skills**

| Skill | Origem | Descrição | Path Local |
|-------|--------|-----------|-----------|
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

**16 skills**

| Skill | Origem | Descrição | Path Local |
|-------|--------|-----------|-----------|
| **bun-development** | 📦 skills | Bun runtime patterns, bundler configuration, and Bun-specific APIs. Trigger on Bun FFI, Bun.serve, Bun.file, Bun shell, workspace configuration, Bun-s… | `skills/bun-development/` |
| **context7-docs-first** | 📦 skills | Ground all platform and library answers in current official documentation by using Context7 MCP tools before responding. TRIGGER when: user asks about… | `skills/context7-docs-first/` |
| **e2e-testing-patterns** | 📦 skills | End-to-end testing with Playwright for Next.js applications. Trigger on E2E test setup, cross-page flow testing (checkout, onboarding, multi-step form… | `skills/e2e-testing-patterns/` |
| **epic-decomposer** | 📦 skills | Decompõe specs, PRDs ou requisitos em épicos e stories implementáveis. Cada story com ACs testáveis, tasks com file paths, e dependências mapeadas. | `skills/planning/epic-decomposer/` |
| **offensive-oauth** | 📦 skills | OAuth 2.0 attack checklist: authorization code interception, redirect_uri bypass, CSRF on OAuth flow, state parameter abuse, open redirector chaining,… | `skills/offensive-oauth/` |
| **offensive-reporting** | 📦 skills | Penetration test and red team report writing methodology. Covers executive summary structuring (risk-led narrative for non-technical readers), technic… | `skills/offensive-reporting/` |
| **offensive-ssrf** | 📦 skills | Server-Side Request Forgery testing checklist: SSRF discovery, blind SSRF with out-of-band, cloud metadata endpoints (AWS/GCP/Azure), SSRF filter bypa… | `skills/offensive-ssrf/` |
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

**5 skills**

| Skill | Origem | Descrição | Path Local |
|-------|--------|-----------|-----------|
| **architecture** | 📦 skills | Framework de decisão arquitetural com análise de requisitos, avaliação de trade-offs e documentação em ADRs. ACIONE quando: decidir entre X e Y (monol… | `skills/architecture/` |
| **bash-linux** | 📦 skills | Padrões de terminal Bash para Linux e macOS: comandos essenciais, pipes, processos, processamento de texto e scripts seguros. ACIONE quando: script ba… | `skills/bash-linux/` |
| **osforge-evolve** | 📦 skills | ACIONE quando: evolve, /evolve, osforge evolve, analisar observações, propor skills, clustering de padrões, instinct, promover instinct, aprendizado c… | `skills/evolve/` |
| **powershell-windows** | 📦 skills | Padrões e armadilhas críticas de PowerShell no Windows: sintaxe de operadores, null checks, JSON, paths e error handling. ACIONE quando: script PowerS… | `skills/powershell-windows/` |
| **readiness-gate** | 📦 skills | Quality gate pré-implementação. Valida que PRD, Architecture e Épicos estão alinhados e completos antes de iniciar o sprint loop. Use com: | `skills/quality/readiness-gate/` |

## 📝 Documentation / Writing

**4 skills**

| Skill | Origem | Descrição | Path Local |
|-------|--------|-----------|-----------|
| **brandkit** | 📦 skills | Gera imagens de brand-kit premium: boards de brand guidelines, sistemas de logo, identity decks e apresentações de universo visual com grids limpos, t… | `skills/brandkit/` |
| **doc-sanitization** | 📦 skills | Clean up, consolidate, and organize project documentation. Removes obsolete specs, merges duplicates, enforces lifecycle rules. Trigger on phrases lik… | `skills/doc-sanitization/` |
| **docs-writer** | 📦 skills | Escreve, revisa e edita documentação técnica verificando o código-fonte e seguindo style guide do projeto. ACIONE quando: documentar uma feature/coman… | `skills/docs-writer/` |
| **minimalist-ui** | 📦 skills | Gera interfaces ultra-minimalistas estilo editorial/documento (tipo Notion) com paleta monocromática quente, serifas editoriais, bento grids flat, pas… | `skills/minimalist-ui/` |

## ☁️ Infrastructure / DevOps

**3 skills**

| Skill | Origem | Descrição | Path Local |
|-------|--------|-----------|-----------|
| **agency-support** | 📦 skills | Índice dos 6 agentes de Suporte e Operações da Agency (Support Responder, Analytics Reporter, Executive Summary Generator, Finance Tracker, Legal Comp… | `skills/agency/support/` |
| **claude-ci-actions** | 📦 skills | Automate PR review, issue triage, and CI/CD tasks with Claude Code GitHub Actions. TRIGGER when: setting up @claude in PRs/issues, configuring automat… | `skills/claude-ci-actions/` |
| **deployment-procedures** | 📦 skills | Workflows seguros de deploy em produção com backup, verificação pós-deploy e rollback para Vercel, Railway, VPS+PM2, Docker e Kubernetes. ACIONE quand… | `skills/deployment-procedures/` |

## 🗄️ Database / Backend

**3 skills**

| Skill | Origem | Descrição | Path Local |
|-------|--------|-----------|-----------|
| **postgres-optimization** | 📦 skills | PostgreSQL and Supabase optimization best practices for queries, indexes, RLS policies, and connection management. Use when writing complex queries, c… | `skills/postgres-optimization/` |
| **prisma-expert** | 📦 skills | Padrões avançados de Prisma ORM. ACIONE quando: mudanças de schema com >3 models, estratégias de migration, queries lentas ou N+1, relações many-to-ma… | `skills/prisma-expert/` |
| **smart-hooks** | 📦 skills | Production-grade Python hooks for Claude Code quality gates, safety rails, and developer experience. TRIGGER when: setting up hooks for a project, con… | `skills/smart-hooks/` |

## 💼 Business / Marketing

**1 skills**

| Skill | Origem | Descrição | Path Local |
|-------|--------|-----------|-----------|
| **seo-fundamentals** | 📦 skills | Fundamentos de SEO para Google com E-E-A-T, Core Web Vitals e SEO técnico. ACIONE quando: melhorar ranking de página no Google, implementar schema mar… | `skills/seo-fundamentals/` |

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