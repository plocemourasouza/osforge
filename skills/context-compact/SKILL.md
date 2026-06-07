---
name: context-compact
description: >
  Compactação estruturada de conversação quando atinge ~70% da janela de contexto.
  ACIONE quando: usuário diz "comprimir contexto", "compactar", "summary", "perto
  do limite", "context full", "save state", "/compact", "/clear", ou quando o
  contador de tokens passar de 140k. Produz summary em 9 seções com analysis
  scratchpad. Substitui /clear destrutivo por preservation inteligente.
version: 1.0.0
inspired_by: Leonxlnx/agentic-ai-prompt-research (Prompt 21 — Compact Service)
metadata:
  source: "agentic-ai-prompt-research"
  category: "meta"
allowed-tools: Read
---

# Context Compact — Conversation Summarization

> Quando context > 70%, NÃO use `/clear` (destrutivo). Use este protocolo
> estruturado de 9 seções que preserva o essencial em ~5k tokens.

## Quick Start

**Exemplo 1 — pedido explícito:**
> Usuário: *"compactar contexto, estamos perto do limite"*
> A skill gera um summary estruturado de 9 seções (~5k tokens) que substitui a conversa inteira, preservando pedidos, decisões, arquivos tocados e o trabalho em andamento — sem perder o fio da execução.

**Exemplo 2 — proativo:**
> Contador de tokens passa de 140k no meio de uma refatoração.
> A skill sugere um **Partial Compact (Modo 3)**: resume as mensagens antigas e mantém as recentes intactas, liberando espaço sem tocar no "now".

**Mini-fluxo (3 passos):**
1. **Escolha o modo** — Full (tudo vira summary), Partial Recent (preserva o início) ou Partial Up-To (preserva o final). Veja "3 modos de operação".
2. **Execute o protocolo** — emita o NO_TOOLS_PREAMBLE, faça o scratchpad `<analysis>`, depois preencha o template de 9 seções (Passos 1–3 em "Protocolo de execução").
3. **Verifique e persista** — confira o checklist de "Verificação" e salve via `osforge-db set-resume` para recuperação cross-session.

## Quando ativar

| Trigger | Ação |
|---|---|
| Context > 70% (140k de 200k tokens) | Sugerir compact ao usuário ANTES de saturar |
| Context > 85% (170k) | Compact obrigatório — informar o usuário |
| Usuário diz "comprimir", "compactar", "perto do limite" | Compact imediato |
| Mudança grande de tópico no meio da sessão | Oferecer "compactar contexto antigo, manter recente" |

## 3 modos de operação

### Modo 1: Full Compact
Toda a conversa vira summary. Use quando vai começar uma fase totalmente nova.

### Modo 2: Partial Compact (Recent)
Mensagens recentes viram summary, mas contexto antigo é mantido intacto. Use quando o início da sessão tem informação crítica que NÃO pode virar resumo.

### Modo 3: Partial Compact (Up-To / Older)
Mensagens antigas viram summary, mensagens recentes ficam intactas. Use quando você está no meio de uma execução e precisa fazer espaço — preserva o "now".

## Protocolo de execução

### Passo 1: NO_TOOLS_PREAMBLE (CRÍTICO)

Inicie SEMPRE com este preamble pra evitar que o modelo chame ferramentas durante o summary:

```
CRITICAL: Respond with TEXT ONLY. Do NOT call any tools.

- Do NOT use Read, Bash, Grep, Glob, Edit, Write, or ANY other tool.
- You already have all the context you need in the conversation above.
- Tool calls will be REJECTED and will waste your only turn — you will fail the task.
- Your entire response must be plain text: an <analysis> block followed by a <summary> block.
```

### Passo 2: Analysis Scratchpad

Antes do summary final, faça uma análise cronológica em `<analysis>` tags:

```xml
<analysis>
1. Cronologicamente, analise cada mensagem e seção:
   - Pedidos explícitos do usuário e intenções
   - Sua abordagem para atender cada pedido
   - Decisões-chave, conceitos técnicos, padrões de código
   - Detalhes específicos: nomes de arquivos, code snippets completos,
     function signatures, file edits
   - Erros encontrados e como foram corrigidos
   - Feedback específico do usuário (atenção redobrada)
2. Double-check pra accuracy técnica e completude
</analysis>
```

O `<analysis>` é scratchpad — será descartado antes do summary chegar ao próximo contexto.

### Passo 3: Summary em 9 seções (template)

```markdown
<summary>

## 1. Primary Request and Intent
Todos os pedidos explícitos do usuário, com intent capturado integralmente.
Inclua TODOS, não só o último. Ex:
- "Integrar taste-skill ao OSForge" (turno 5)
- "Auditar OBSIDIAN para performance e a11y" (turno 23)
- "Aplicar fixes via prompt" (turno 31)

## 2. Key Technical Concepts
Tecnologias, frameworks, patterns discutidos:
- OSForge framework (122 skills, 26 agents, 12 rules)
- Anti-AI-slop directives (Inter ban, pure #000 ban, etc)
- Taste design dials (DESIGN_VARIANCE / MOTION_INTENSITY / VISUAL_DENSITY)
- Lighthouse Core Web Vitals (LCP, FCP, CLS)
- Chrome MCP for browser automation

## 3. Files and Code Sections
Arquivos examinados/modificados/criados, COM code snippets completos:

**Modified:**
- `claude-code/SKILLS.md` (added 8 design skills to Design & UX table)
- `rules/anti-ai-slop.mdc` (expanded from 9 to 40 rules)

**Created:**
- `skills/taste-design-dials/SKILL.md` (261 lines)
- `skills/aesthetic-modes/SKILL.md` (254 lines)
[etc — listar TODOS]

```typescript
// Snippets relevantes que vão ser necessários pra continuar
const decision = classifier.classify({...})
```

## 4. Errors and Fixes
Erros encontrados e resolução:
- `index.lock` no .git → resolvido com `rm -f .git/index.lock`
- Server localhost:4567 caiu → user reiniciou em :8000
- web_fetch URLs fora de provenance → solucionado clonando via bash

## 5. Problem Solving
Problemas resolvidos e troubleshooting em andamento:
- ✅ Integração taste-skill (5 skills + routing rules)
- ✅ Deploy em ~/.claude/ e ~/.cursor/
- ✅ Audit OBSIDIAN (gargalo FCP 6.5s identificado)
- 🔄 Em andamento: integração agentic-ai-prompt-research patterns

## 6. All User Messages
TODA mensagem não-tool-result do usuário (crítico pra tracking de intent drift):
- "Lembra do nosso projeto OSForge?"
- "temos no github..."
- "Quero adicionar esse conhecimento ao projeto..."
- "faça isso"
- "o comando /mcp não funcionou"
- "Quero que você rode os comandos..."
- "Aqui está o link do resultado gerado..."
- "Você não me convenceu por que o Auto Mode Critique (17) não..."
- "Perfeito, vamos avançar"
[continue listando TODAS — mesmo curtinhas]

## 7. Pending Tasks
Trabalho pendente:
- [ ] Implementar tool-safety-classifier skill
- [ ] Implementar config-critique skill
- [ ] Implementar context-compact skill (em progresso AGORA)
- [ ] Implementar stuck-recovery skill
- [ ] Criar memory-hierarchy.mdc rule
- [ ] Enrich orchestrator/AGENT.md com Coordinator patterns
- [ ] Update SKILLS.md router + README

## 8. Current Work
Descrição PRECISA do trabalho em progresso ANTES da compactação:
Estou criando 4 novas SKILL.md files no OSForge baseadas nos prompts do
agentic-ai-prompt-research (Leon Lin). Acabei de finalizar
`tool-safety-classifier` (Prompt 12), agora estou escrevendo
`context-compact` (este arquivo — Prompt 21). Próximos:
config-critique (P17), stuck-recovery (P26). Depois enrichments
no orchestrator e CLAUDE.md, depois commit + push.

## 9. Optional Next Step
Próximo passo IMEDIATO se alinhado com pedidos recentes:
Terminar de escrever context-compact/SKILL.md (este arquivo),
salvar com Write tool, depois partir para skills/config-critique/SKILL.md.

</summary>
```

## Modo 2 (Partial Recent) — adaptação

Trocar instrução inicial por:
```
Your task is to create a detailed summary of the RECENT portion of the conversation —
the messages that follow earlier retained context. The earlier messages are being kept
intact and do NOT need to be summarized. Focus your summary on what was discussed,
learned, and accomplished in the recent messages only.
```

## Modo 3 (Partial Up-To / Older) — adaptação

Trocar instrução inicial por:
```
Your task is to create a detailed summary of this conversation. This summary will be
placed at the start of a continuing session; newer messages that build on this context
will follow after your summary (you do not see them here). Summarize thoroughly so
that someone reading only your summary and then the newer messages can fully understand
what happened and continue the work.
```

E nas seções:
- Seção 8 vira "Work Completed" (não "Current Work")
- Seção 9 vira "Context for Continuing Work"

## Integração com osforge-db

O OSForge tem SQLite local (`~/.osforge/osforge.db`). Use-o para PERSISTIR o summary:

```bash
# Após gerar o summary, salvar persistente:
osforge-db set-resume <project-slug> "$(cat summary.md)"

# Sessão futura recupera em 50 tokens via:
osforge-db resume <project-slug>
```

Isso significa que **compactação não destrói** o contexto — ele continua disponível pra sessões futuras via osforge-db, mesmo quando saiu do context window atual.

## Custom instructions support

Se o projeto tem `compact-instructions.md` em `.osforge/`, incluir no prompt:

```
There may be additional summarization instructions provided in the included context.
If so, remember to follow these instructions when creating the above summary.
```

Útil pra projetos com terminologia específica que deve ser preservada literalmente.

## Anti-patterns

- ❌ Pular o `<analysis>` block — você vai esquecer algo
- ❌ Resumir só as últimas N mensagens "porque é mais fácil" — quebra intent tracking
- ❌ Omitir seção 6 (All User Messages) — é a defesa contra intent drift
- ❌ Usar Tool durante summarization — vai falhar com maxTurns: 1
- ❌ `<analysis>` no output final (deve ser stripped — só usuário precisa ver `<summary>`)

## Verificação

- [ ] 9 seções todas preenchidas (mesmo que algumas com "N/A")
- [ ] Section 3 inclui code snippets COMPLETOS (não placeholders)
- [ ] Section 6 lista TODA mensagem do usuário
- [ ] Sem chamada de ferramentas no output
- [ ] Total: 3-7k tokens (não < 1k, não > 10k)
- [ ] Resume restaurável: outra sessão consegue continuar lendo só o summary

---

## Related Skills

- `context-distillator` — sibling skill para destilação radical (~500 tokens)
- `osforge-db` — persistência cross-session (recovery via `osforge-db resume`)
- `project-context` — geração inicial de contexto de projeto
- `editorial-review` — limpeza pós-summary se necessário
