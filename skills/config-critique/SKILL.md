---
name: config-critique
description: >
  Lint LLM-powered de customizações do usuário no OSForge — valida novas SKILL.md,
  rules .mdc, hooks customizados, agents adicionais, e overrides de CLAUDE.md em
  4 eixos (Clarity / Completeness / Conflicts / Actionability). ACIONE quando:
  "revisar minha skill", "validar minha rule", "verificar conflito de hooks",
  "lint config", "minha skill está boa?", "este agent vai funcionar?", "PR review
  de skill", ou quando o usuário adiciona/edita config no ~/.claude/ ou ~/.cursor/.
version: 1.0.0
inspired_by: Leonxlnx/agentic-ai-prompt-research (Prompt 17 — Auto Mode Critique)
metadata:
  source: "agentic-ai-prompt-research"
  category: "meta-quality"
allowed-tools: Read, Glob, Grep
---

# Config Critique — LLM-Powered Linter for OSForge Customizations

> Expert reviewer que avalia configurações customizadas do usuário antes
> de virarem source of truth. 4 eixos. Construtivo. Conciso.

## Quando usar

| Trigger | O que critica |
|---|---|
| Usuário criou nova SKILL.md | Frontmatter, description triggers, conflitos com skills existentes |
| Usuário escreveu rule `.mdc` | Globs, `alwaysApply`, conflitos com rules base |
| Usuário customizou hooks `settings.json` | Pattern matching, false positives, edge cases |
| Usuário adicionou agent `.md` | Reality Check + QC Loop presentes, persona conflita com outros |
| Usuário sobrescreveu seção do CLAUDE.md | Conflito com SKILLS.md, com rules |
| Antes de PR no OSForge upstream | Gate de qualidade pra PR review |

## Quando NÃO usar

- Configs auto-geradas pelo `deploy.sh` (já validadas)
- Edits triviais (corrigir typo, mudar 1 linha)
- Skills imutáveis built-in do OSForge core

## Os 4 eixos

### 1. Clarity
> A regra/skill é inequívoca? Algum LLM pode misinterpretar?

Procurar:
- Descriptions vagas ("útil para coisas de design")
- Triggers ambíguos (palavras que aparecem em qualquer prompt)
- Verbos passivos ("pode ser usado") em vez de imperativos ("ACIONE quando")
- Referências sem contexto ("usar o pattern padrão" — qual?)
- Frontmatter campos vazios ou inconsistentes

**Bom:**
```yaml
description: >
  ACIONE quando: "criar landing page premium", "estilo Awwwards",
  "hero magnético". Carrega 3-dial system (VARIANCE/MOTION/DENSITY).
```

**Ruim:**
```yaml
description: Bom para design bonito
```

### 2. Completeness
> Há gaps ou edge cases não cobertos?

Procurar:
- Skills sem "Quando NÃO usar"
- Rules sem fallback quando o pattern não casa
- Hooks sem tratamento de erro
- Agents sem "What this agent does NOT do"
- Falta de exemplos negativos
- Triggers que cobrem só português OU só inglês (deveria cobrir ambos no OSForge)

**Pergunta-teste:** *Se eu der esse SKILL.md pra um LLM novo, ele consegue decidir SOZINHO quando ativar?*

### 3. Conflicts
> Conflita com regras/skills existentes?

Procurar:
- Triggers overlap (2 skills competindo pelo mesmo prompt)
- Rules com globs que se sobrepõem
- Agents com personas duplicadas
- Hooks que bloqueiam comando que outro hook permite
- CLAUDE.md sections override que invalidam rules `alwaysApply`

**Cross-reference contra os 122 skills existentes:**
```bash
# Grep triggers similares
grep -r "your-new-trigger" skills/*/SKILL.md
```

### 4. Actionability
> Específico o suficiente pra agir?

Procurar:
- Rules sem instruções concretas ("seja cuidadoso com X")
- Skills sem outputs claros (não diz o que entregar)
- Agents sem critérios de "done"
- Triggers sem decisão tree ("se A, então B; se C, então D")
- Pseudo-code sem real code

**Bom:**
```yaml
description: >
  ACIONE em: TypeScript strict violations. AÇÃO: rodar `tsc --noEmit`,
  parsear output, listar erros priorizados por severidade, propor fix
  cada um.
```

**Ruim:**
```yaml
description: Cuida da qualidade do TypeScript no projeto
```

## Protocolo de critique

### Passo 1: Identificar o tipo de config

```python
config_type = detect_config_type(file_path)
# possíveis: skill, rule, hook, agent, claude_md_override
```

### Passo 2: Carregar baseline para comparação

```python
baseline = {
    "skill": load_all_skills_index("claude-code/SKILLS.md"),
    "rule": load_all_rules("rules/*.mdc"),
    "hook": load_hooks_json("hooks/hooks-claude-code.json"),
    "agent": load_all_agents("agents/*.md"),
}[config_type]
```

### Passo 3: Aplicar 4 eixos com structured output

```yaml
critique:
  file: skills/my-new-skill/SKILL.md
  overall_grade: B+   # A / B+ / B / C+ / C / D / F
  axes:
    clarity:
      score: 7/10
      issues:
        - line: 4
          severity: high
          message: "Description 'útil para tarefas' é vago. Substituir por triggers específicos."
          suggestion: "ACIONE quando: '...', '...', '...'"
    completeness:
      score: 8/10
      issues:
        - severity: medium
          message: "Falta seção 'Quando NÃO usar'"
          suggestion: "Adicionar seção entre 'Quando usar' e 'Protocolo'"
    conflicts:
      score: 6/10
      issues:
        - severity: high
          message: "Trigger 'design premium' conflita com skill `taste-design-dials` (linha 3)"
          suggestion: "Diferenciar: este skill é pra X, taste-design-dials é pra Y. Ajustar descriptions de ambos."
    actionability:
      score: 9/10
      issues: []
  recommendation: "Iterar Clarity + Conflicts antes de mergear. Completeness é nice-to-have."
```

### Passo 4: Recomendação final

| Grade | Ação |
|---|---|
| **A / A-** | Aprovar |
| **B+ / B** | Aprovar com sugestões opcionais |
| **B- / C+** | Requer iteração — listar fixes obrigatórios |
| **C / C-** | Requer rewrite — issues estruturais |
| **D / F** | Bloquear — conflitos sérios ou config quebrada |

## Regra de ouro

> Comente APENAS regras que podem ser melhoradas. Se está tudo bom, diga "tudo good"
> sucinto. Não sermãoneie. Não invente issues pra mostrar trabalho.

Se de 4 eixos, 3 passaram e 1 tem 1 issue: aponte o issue específico, elogie os outros 3, e termine. Não escreva 500 linhas pra justificar 1 fix de 1 linha.

## Anti-patterns

- ❌ Critique genérico ("poderia ser mais claro") — sem location nem fix
- ❌ Critique abrangente quando só 1 issue existe — sermão
- ❌ Aceitar config quebrada porque "está perto" — gate é gate
- ❌ Verificar só sintaxe — semântica > sintaxe
- ❌ Ignorar conflitos com configs existentes (esse é o eixo mais importante)

## Verificação meta (critique do próprio critique)

Antes de entregar:
- [ ] Cada issue tem location (line, file, section)
- [ ] Cada issue tem severity (low/medium/high/critical)
- [ ] Cada issue tem suggestion concreta
- [ ] Cross-reference com baseline foi feita
- [ ] Output é YAML/markdown parseável, não prose solto

## Integração com workflow

### Modo manual (interativo)
```
Usuário: "revisa essa skill que escrevi: skills/my-thing/SKILL.md"
Claude: [carrega config-critique skill] [aplica 4 eixos] [retorna structured]
```

### Modo automático (pre-commit hook)
Adicionar ao `.husky/pre-commit` ou ao hook do OSForge:
```bash
# Se arquivos em skills/, rules/, agents/ foram modificados:
modified=$(git diff --cached --name-only | grep -E '^(skills|rules|agents)/')
for file in $modified; do
  osforge-db critique "$file" || exit 1
done
```

### Modo PR (CI gate)
GitHub Action que roda config-critique em PRs que tocam skills/rules/agents.

---

## Related Skills

- `skill-creator` — cria skills; config-critique valida o resultado
- `autorefine-skill` — itera skills baseado em uso; complementa critique
- `adversarial-review` — review de código; config-critique é review de configuração
- `differential-review` — diff-focused review (PRs)
