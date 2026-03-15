# 📖 OSForge — Guia de Uso

Instruções completas de instalação, configuração e uso do dia a dia.

---

## Índice

1. [Instalação](#1-instalação)
2. [Deploy automático](#2-deploy-automático)
3. [Skills — uso no dia a dia](#3-skills--uso-no-dia-a-dia)
4. [Agentes especializados](#4-agentes-especializados)
5. [Regras always-on (Cursor)](#5-regras-always-on-cursor)
6. [Spec Commands](#6-spec-commands)
7. [Python Hooks](#7-python-hooks)
8. [The Agency — 121 Especialistas](#8-the-agency--121-especialistas)
9. [llmfit Advisor — LLMs Locais](#9-llmfit-advisor--llms-locais)
10. [Smart Model Dispatch](#10-smart-model-dispatch)
11. [MCPs recomendados](#11-mcps-recomendados)
12. [Agentes de alto risco](#12-agentes-de-alto-risco)

---

## 1. Instalação

### Pré-requisitos

- Claude Code (`npm install -g @anthropic-ai/claude-code`) ou Cursor
- Bun (`curl -fsSL https://bun.sh/install | bash`)
- Git

### Clone

```bash
git clone https://github.com/plocemourasouza/osforge.git
cd osforge
```

### Dependências opcionais

```bash
# llmfit — recomendações de LLM local (macOS)
brew tap AlexsJones/llmfit && brew install llmfit

# llmfit — via Rust (qualquer plataforma)
cargo install llmfit
```

---

## 2. Deploy automático

O `deploy.sh` sincroniza tudo para `~/.claude/` e `~/.cursor/` com um único comando.

```bash
./deploy.sh                 # Deploy completo (Claude Code + Cursor)
./deploy.sh --claude-only   # Apenas Claude Code
./deploy.sh --cursor-only   # Apenas Cursor
./deploy.sh --dry-run       # Simula sem aplicar mudanças
```

### O que o deploy faz

**Claude Code (`~/.claude/`)**
- Copia `CLAUDE.md` e `SKILLS.md`
- Sincroniza 11 agentes para `~/.claude/agents/`
- Copia 9 commands `spec:*` para `~/.claude/commands/`
- Instala hooks Python em `~/.claude/hooks/`
- Merge não-destrutivo de MCPs em `~/.claude.json`

**Cursor (`~/.cursor/`)**
- Copia `SKILLS.md`
- Sincroniza agentes para `~/.cursor/agents/`
- Copia 8 rules `.mdc` para `~/.cursor/rules/`
- Copia hooks scripts

**Verificação de dependências**
O script avisa se `llmfit` não estiver instalado, com o comando de instalação.

### Deploy manual (sem script)

```bash
# Claude Code
cp claude-code/CLAUDE.md ~/.claude/CLAUDE.md
cp claude-code/SKILLS.md ~/.claude/SKILLS.md
cp -r agents/ ~/.claude/agents/
cp -r commands/ ~/.claude/commands/
cp hooks/*.py ~/.claude/hooks/

# Cursor
cp claude-code/SKILLS.md ~/.cursor/SKILLS.md
cp -r agents/ ~/.cursor/agents/
cp -r rules/ ~/.cursor/rules/
```

---

## 3. Skills — uso no dia a dia

Skills são carregadas sob demanda — apenas quando você precisa. O `SKILLS.md` mantém gatilhos condensados no contexto base (~6.9K tokens). O arquivo `SKILL.md` completo de cada skill só é lido quando ativada.

### Como ativar uma skill

Basta descrever o que você precisa. O Claude identifica e aplica a skill automaticamente pelos trigger phrases no `SKILLS.md`. Você também pode ativar explicitamente:

```
"Leia skills/tdd-workflow/SKILL.md"
"Use a skill de security best practices"
"Ativa o smart-model-dispatch"
```

### Referência de skills por categoria

**Core**
- `tdd-workflow` — Ciclo RED-GREEN-REFACTOR rigoroso
- `verification-before-completion` — Checklist antes de declarar tarefa concluída
- `coding-guidelines` — Regras Karpathy + convenções do stack
- `best-practices` — Padrões gerais de qualidade
- `git-workflow` — Branching, commits, PRs

**Stack**
- `prisma-expert` — Schema, migrations, queries otimizadas
- `nextjs-supabase-auth` — Auth SSR com Supabase
- `stripe-integration` — Webhooks, checkout, billing
- `bun-development` — Runtime Bun, scripts, workspaces
- `frontend-ui-system` — shadcn/ui, Tailwind, componentes
- `i18n-localization` — next-intl, mensagens, pluralização

**Performance**
- `react-performance` — Memoização, Suspense, lazy loading
- `postgres-optimization` — Índices, queries, explain analyze
- `core-web-vitals` — LCP, CLS, INP, métricas Vercel

**Security**
- `security-best-practices` — OWASP top 10, input validation
- `security-threat-model` — Threat modeling sistemático
- `insecure-defaults` — Detecta fail-open patterns
- `differential-review` — Review focado em segurança de PRs
- `gdpr-data-handling` — LGPD/GDPR compliance

**Meta / Agência**
- `smart-model-dispatch` — Roteamento Opus/Sonnet/Haiku
- `llmfit-advisor` — LLMs locais por hardware fit
- `dispatching-parallel-agents` — Orquestração paralela
- `agent-skills-search` — Busca de skills disponíveis
- `context7-docs-first` — Docs atualizadas via Context7 MCP
- `mcp-builder` — Criar servidores MCP
- `skill-creator` — Criar e avaliar novas skills
- `smart-hooks` — Hooks Python de qualidade

**API**
- `claude-api-typescript` — SDK Claude, tool use, streaming
- `claude-ci-actions` — GitHub Actions com Claude

**Testing**
- `e2e-testing-patterns` — Playwright, Page Object Model

**Docs**
- `docs-writer` — Documentação técnica clara
- `doc-sanitization` — Remoção de PII, sanitização
- `technical-design-doc-creator` — ADRs, design docs
- `tlc-spec-driven` — Spec-driven development completo

**Frontend**
- `accessibility` — WCAG 2.1, aria, screen readers
- `seo` — Meta tags, structured data, sitemap

**Optimization**
- `predictive-failure` — Análise antecipada de riscos
- `vercel-deploy` — Deploy, env vars, edge config

---

## 4. Agentes especializados

Agentes são personalidades com missão definida. Ativados explicitamente ou pelo campo `description` do frontmatter (Claude Code sugere automaticamente).

### Ativar um agente

```
"Use o planner para decompor esta feature"
"Ativa o security-auditor"
"Quero o debugger para investigar esse bug"
```

### Referência de agentes

| Agente | Quando usar |
|---|---|
| `planner` | Inicio de qualquer feature — decomposição, arquitetura, stories |
| `system-architect` | Design de sistemas, ADRs, decisões de arquitetura |
| `backend-engineer` | Prisma schema, Server Actions, APIs, Supabase |
| `frontend-engineer` | Componentes shadcn/ui, Server/Client Components, UX |
| `debugger` | Bug investigation em 10 passos estruturados |
| `code-reviewer` | Review de PR com output YAML estruturado |
| `code-refactorer` | Refactoring, clean code, redução de dívida técnica |
| `security-auditor` | Threat modeling, audit de segurança (metodologia Trail of Bits) |
| `validator` | Critica specs, valida acceptance criteria |
| `product-strategy-advisor` | Roadmap, priorização, decisões de produto |
| `git-commit-helper` | Conventional commits, changelogs, release notes |

### Padrão de uso combinado (feature completa)

```
1. planner        → Decompõe em stories e define arquitetura
2. validator      → Critica o plano, identifica gaps
3. backend-engineer → Implementa schema + Server Actions
4. frontend-engineer → Implementa UI
5. code-reviewer   → Review final
6. security-auditor → Audit se houver dados sensíveis
```

---

## 5. Regras always-on (Cursor)

As 8 regras `.mdc` ficam ativas em todas as sessões do Cursor automaticamente. Não precisam ser ativadas.

| Regra | Efeito |
|---|---|
| `typescript-strict` | Força `strict: true`, proíbe `any`, `enum`, `export default` |
| `tdd-enforcement` | Nenhum código de produção sem teste falhando primeiro |
| `code-style` | Naming conventions, import order, product thinking |
| `commit-conventions` | Conventional commits obrigatórios |
| `nextjs-patterns` | Server Components por padrão, `"use client"` só quando necessário |
| `product-thinking` | Decisão de usuário antes de decisão técnica |
| `security-mindset` | Zero-trust, fail-safe, sem secrets hardcoded |
| `agent-skills-reference` | Como carregar e usar skills OSForge |

---

## 6. Spec Commands

9 comandos `/spec:*` disponíveis no Claude Code para desenvolvimento orientado a spec.

```bash
# Fluxo completo de uma feature
/spec:discover    # Explorar o problema, coletar requisitos
/spec:specify     # Escrever especificação formal
/spec:design      # Design técnico + ADR
/spec:tasks       # Decompor em tarefas implementáveis
/spec:implement   # Executar implementação com guardrails
/spec:checklist   # Checklist pré-ship

# Utilitários
/spec:clarify     # Loop de clarificação para specs ambíguas
/spec:constitution # Definir princípios e restrições do projeto
/spec:measure     # Definir e rastrear métricas de sucesso
```

### Exemplo de uso

```
/spec:discover "Módulo de reconciliação OFX para o Tressen"
→ Claude explora requisitos, levanta dúvidas, mapeia o domínio

/spec:specify
→ Gera spec formal com casos de uso, regras de negócio, critérios de aceite

/spec:design
→ Prisma schema, Server Actions, fluxo de dados, ADR de decisões chave

/spec:tasks
→ Lista de tasks priorizadas prontas para implementação

/spec:implement
→ Implementa seguindo a spec, com verificação contínua

/spec:checklist
→ Valida que tudo foi feito antes do PR
```

---

## 7. Python Hooks

Hooks rodam como processos externos — **zero custo de tokens**. Configurados via `hooks/hooks-claude-code.json`.

### Instalação

```bash
# Via deploy.sh (automático)
./deploy.sh

# Manual
cp hooks/*.py ~/.claude/hooks/
chmod +x ~/.claude/hooks/*.py
```

### O que cada hook faz

**`pre_tool_use.py`** (antes de qualquer tool call)
- Bloqueia comandos shell perigosos (`rm -rf /`, `sudo`, etc.)
- Protege arquivos `.env` e `.env.local` de escrita acidental
- Gera audit log de todas as operações

**`post_tool_use.py`** (após Write/Edit)
- Detecta `console.log` em arquivos de produção
- Bloqueia `any` em TypeScript sem justificativa
- Avisa sobre `@ts-ignore` sem comentário explicativo
- Detecta `export default` (proibido pelo style guide)

**`pre_compact.py`** (antes de compactação de contexto)
- Faz backup da conversa atual em `~/.claude/backups/`
- Preserva contexto importante antes do truncamento

**`session_end.py`** (fim de sessão)
- Registra log resumido da sessão
- Envia notificação macOS via AppleScript

### Shell scripts auxiliares

```bash
hooks/scan-secrets.sh     # Detecta secrets/API keys em arquivos staged
hooks/protect-tests.sh    # Avisa ao modificar arquivos de teste críticos
hooks/notify-done.sh      # Notificação macOS de tarefa concluída
```

---

## 8. The Agency — 121 Especialistas

Biblioteca de 121 agentes de IA cobrindo todas as funções de negócio e técnica. Estrutura em 3 camadas para carregamento eficiente.

### Fluxo de ativação

```
Passo 1 — Identificar a divisão
"Leia skills/agency/SKILL.md"
→ Claude mostra as 10 divisões e quando usar cada uma

Passo 2 — Ver agentes da divisão
"Leia skills/agency/engineering/SKILL.md"
→ Lista os 23 agentes de engenharia com especialidades

Passo 3 — Ativar o agente
"Ative o Security Engineer"
→ Claude lê o .md completo e assume aquela especialidade
```

### Exemplo prático — construção de software

```
# Quando preciso de arquitetura para o sistema de pagamentos do Tressen:
"Leia skills/agency/engineering/SKILL.md"
→ "Ative o Backend Architect"
→ "Projeta a arquitetura de reconciliação OFX com suporte a múltiplos bancos"

# Quando preciso de UX para o LinkMeTur:
"Leia skills/agency/design/SKILL.md"
→ "Ative o UX Researcher"
→ "Analisa o fluxo de onboarding de prestadores de serviço turístico"

# Quando preciso de estratégia de vendas para a OSystems:
"Leia skills/agency/sales/SKILL.md"
→ "Ative o Outbound Strategist"
→ "Cria sequência de prospecção para micro empresas no RS"
```

### Divisões disponíveis

| Divisão | Agentes | Arquivo de índice |
|---|---|---|
| 💻 Engineering | 23 | `skills/agency/engineering/SKILL.md` |
| 🎨 Design | 8 | `skills/agency/design/SKILL.md` |
| 📢 Marketing | 26 | `skills/agency/marketing/SKILL.md` |
| 💰 Paid Media | 7 | `skills/agency/paid-media/SKILL.md` |
| 📊 Product | 5 | `skills/agency/product/SKILL.md` |
| 🎬 Project Management | 6 | `skills/agency/project-management/SKILL.md` |
| 💼 Sales | 8 | `skills/agency/sales/SKILL.md` |
| 🛟 Support & Ops | 6 | `skills/agency/support/SKILL.md` |
| 🧪 Testing | 8 | `skills/agency/testing/SKILL.md` |
| 🎯 Specialized | 24 | `skills/agency/specialized/SKILL.md` |

---

## 9. llmfit Advisor — LLMs Locais

Detecta o hardware real da máquina e recomenda quais modelos locais rodam bem, com quantização ideal e estimativa de velocidade.

### Instalação

```bash
# macOS (recomendado)
brew tap AlexsJones/llmfit && brew install llmfit

# Qualquer plataforma (requer Rust instalado)
cargo install llmfit

# Verificar
llmfit --version
llmfit system    # Ver specs detectadas
```

### Comandos essenciais

```bash
# Ver hardware detectado (JSON)
llmfit --json system

# Top 5 recomendações gerais
llmfit recommend --json --limit 5

# Filtrar por caso de uso
llmfit recommend --json --use-case coding    --limit 3
llmfit recommend --json --use-case reasoning --limit 3
llmfit recommend --json --use-case chat      --limit 3

# Apenas modelos com fit "perfect" ou "good"
llmfit recommend --json --min-fit good --limit 5

# Override de VRAM quando autodetect falhar
llmfit --memory=24G recommend --json --limit 5

# TUI interativa (padrão, sem flags)
llmfit
```

### Entendendo o output

| Campo | Significado |
|---|---|
| `fit_level` | `Perfect` (ideal) / `Good` (ok) / `Marginal` (apertado) / `TooTight` (não roda) |
| `run_mode` | `GPU` (rápido) / `CPU+GPU Offload` (misto) / `CPU` (lento) |
| `best_quant` | Melhor quantização para o hardware (Q8_0 = qualidade máxima, Q2_K = mais comprimido) |
| `estimated_tps` | Tokens por segundo estimados |
| `is_moe` | Mixture-of-Experts — VRAM real muito menor que parâmetros totais |

**Regra:** Nunca recomendar modelos com `fit_level: "TooTight"`.

### Quando usar local vs API

| Situação | Recomendação |
|---|---|
| Dados sensíveis — Tressen (contábil), Red Caveat (jurídico) | ✅ **Sempre local** — dados não saem do ambiente |
| Clientes OSystems sem budget de API | ✅ **Local** — llmfit identifica o melhor viável |
| Tarefas repetitivas em alto volume (boilerplate, i18n, stubs) | ✅ **Local** — Qwen2.5-Coder elimina custo acumulado |
| Raciocínio profundo, arquitetura, análise complexa | ❌ **API (Opus)** — sem equivalente local completo |
| Contexto >32K tokens | ❌ **API** — modelos locais têm janela limitada |
| Qualidade crítica em produção com latência controlada | ❌ **API** — mais consistente |

### Mapeamento HuggingFace → Ollama

| Modelo (llmfit) | Tag Ollama | Ideal para |
|---|---|---|
| `Qwen/Qwen2.5-Coder-7B-Instruct` | `qwen2.5-coder:7b` | Coding leve, boilerplate |
| `Qwen/Qwen2.5-Coder-14B-Instruct` | `qwen2.5-coder:14b` | Coding intermediário |
| `meta-llama/Llama-3.1-8B-Instruct` | `llama3.1:8b` | Chat geral |
| `meta-llama/Llama-3.3-70B-Instruct` | `llama3.3:70b` | Uso geral avançado |
| `deepseek-ai/DeepSeek-R1-Distill-Qwen-32B` | `deepseek-r1:32b` | Raciocínio |
| `google/gemma-2-9b-it` | `gemma2:9b` | Chat eficiente |
| `microsoft/Phi-4-mini-instruct` | `phi4-mini` | Tarefas leves, rápido |

### Instalar modelo via Ollama

```bash
ollama pull qwen2.5-coder:7b
ollama pull phi4-mini
ollama list   # ver instalados
```

### Ativar no OSForge

```
"Leia skills/llmfit-advisor/SKILL.md"
→ Detecta hardware, recomenda modelos, oferece configurar Ollama
```

---

## 10. Smart Model Dispatch

Roteia tarefas para o tier de modelo ideal — economizando ~65% de custo vs usar Opus para tudo.

```
"Leia skills/smart-model-dispatch/SKILL.md"
```

### Resumo de tiers

| Tier | Modelo | Custo | Quando usar |
|---|---|---|---|
| 🔴 Opus | `claude-opus-4-6` | $5/$25 por 1M | Arquitetura, raciocínio profundo, decisões críticas |
| 🟡 Sonnet | `claude-sonnet-4-6` | $3/$15 por 1M | Implementação, debugging, review, testes |
| 🟢 Haiku | `claude-haiku-4-5` | $1/$5 por 1M | Boilerplate, i18n, stubs, docs, CRUD simples |
| 🏠 Local | Ollama (via llmfit) | $0 | Tarefas Haiku com dados sensíveis ou alto volume |

### Padrão de feature completa com dispatch

```
[opus]   planner          → arquitetura + decomposição
[opus]   validator        → critica o plano
[sonnet] backend-engineer → Prisma + Server Actions
[sonnet] frontend-engineer → UI + componentes
[haiku]  → i18n keys, test stubs, seed data
[sonnet] code-reviewer    → review final
[local]  → tarefas mecânicas com dados sensíveis
```

---

## 11. MCPs recomendados

### Claude Code (global — `~/.claude.json`)

```jsonc
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"]
    },
    "supabase": {
      "command": "npx",
      "args": ["-y", "@supabase/mcp-server-supabase@latest", "--read-only"],
      "env": { "SUPABASE_ACCESS_TOKEN": "seu-token" }
    },
    "shadcn": {
      "command": "npx",
      "args": ["shadcn@latest", "mcp"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "seu-pat" }
    }
  }
}
```

> ⚠️ Nunca coloque tokens em chats ou arquivos versionados. Use variáveis de ambiente ou o arquivo `~/.claude.json` local.

### Cursor (projeto — `.cursor/mcp.json`)

Veja `mcp/cursor.json` no repositório.

---

## 12. Agentes de alto risco

Quatro agentes da The Agency podem executar ações autônomas com impacto real. Cada um tem um **bloco de checkpoint obrigatório** embutido no `.md` — eles nunca agem sem apresentar um plano e aguardar aprovação explícita.

| Agente | Risco | Arquivo |
|---|---|---|
| Accounts Payable | Pagamentos crypto/fiat/stablecoins | `skills/agency/specialized/accounts-payable-agent.md` |
| Carousel Growth Engine | Publicação autônoma em redes sociais | `skills/agency/marketing/marketing-carousel-growth-engine.md` |
| Report Distribution | Envio automático de e-mails/relatórios | `skills/agency/specialized/report-distribution-agent.md` |
| Agentic Identity & Trust | Configuração de trust inter-agentes | `skills/agency/specialized/agentic-identity-trust.md` |

### Protocolo de uso

1. O agente apresenta o plano completo antes de qualquer ação
2. Você responde explicitamente: `"confirmar"`, `"aprovar"` ou `"sim, prossiga"`
3. Sem resposta explícita = o agente para e pergunta de novo
4. Cada ação é registrada com timestamp para auditoria

Se precisar usar sem o checkpoint (contexto controlado), remova o bloco `---⚠️ AGENTE DE ALTO RISCO---` do início do arquivo `.md` correspondente.

---

*Dúvidas ou contribuições: abra uma issue em [github.com/plocemourasouza/osforge](https://github.com/plocemourasouza/osforge)*
