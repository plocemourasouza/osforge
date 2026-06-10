# Plan Template: STANDARD

## Plano: {título}
**Complexidade:** STANDARD
**Fases:** 4-6 (adaptar conforme necessidade)

### Fase 1: Especificação Técnica
- **Objetivo:** Definir requisitos, escopo e acceptance criteria
- **Skill:** `skills/planning/spec-builder`
- **Artefato:** `{output_dir}/tech-spec-{slug}.md`
- **Tamanho:** Pequeno a Médio

### Fase 2: Verificação de Arquitetura (se schema/API changes)
- **Objetivo:** Validar decisões técnicas contra o stack do projeto
- **Skill:** `skills/planning/arch-builder`
- **Artefato:** Seção de ADRs na spec ou `{output_dir}/arch-decisions-{slug}.md`
- **Tamanho:** Pequeno
- **Condição:** Pular se a mudança não afeta schema, API ou patterns existentes

### Fase 3: Decomposição em Stories
- **Objetivo:** Quebrar spec em stories implementáveis e ordenadas
- **Skill:** `skills/planning/epic-decomposer`
- **Artefato:** `{output_dir}/stories/{slug}/` (1 arquivo por story)
- **Tamanho:** Pequeno a Médio

### Fase 4-N: Implementação (loop por story)
- **Objetivo:** Implementar cada story em sequência de dependência
- **Skill:** `skills/planning/story-executor` → skills de execução
- **Artefato:** Código + testes por story
- **Tamanho:** Varia por story (S/M/L)

Para cada story:
1. Implementar tasks da story
2. Code review (`skills/quality/code-review`)
3. Se aprovado → próxima story
4. Se changes requested → corrigir e re-review

#### Metadados de paralelismo por task

Cada task gerada para este plano DEVE incluir o bloco YAML abaixo logo após o cabeçalho `### TN:`:

```yaml
id: T<N>
depends_on: []      # ids de tasks pré-requisito (ex: [T1, T2])
wave: 1             # onda de execução derivada de depends_on
parallel_ok: true   # false se toca arquivo compartilhado com outra task da mesma wave
```

Regras de derivação:
- Tasks sem predecessoras → `wave: 1`.
- Tasks cujo predecessor mais tardio está na wave N → `wave: N+1`.
- Tasks na mesma wave com `parallel_ok: true` são despachadas em paralelo pelo orchestrator.
- Duas tasks que editam o mesmo arquivo → `parallel_ok: false` ou waves diferentes.

### Fase Final: Review de Qualidade
- **Objetivo:** Validação adversarial do conjunto completo
- **Skill:** `skills/quality/adversarial-review` + `skills/quality/edge-case-hunter`
- **Artefato:** Review report consolidado
- **Tamanho:** Médio

### Checkpoints
- Após Fase 1: aprovar spec
- Após Fase 2: aprovar decisões de arquitetura (se aplicável)
- Após Fase 3: aprovar decomposição em stories antes de implementar
- Após cada story: code review
- Após Fase Final: aprovar para merge/deploy

### Notas
- Se spec exceder ~1600 tokens, considerar split ou reclassificar para COMPLEX
- Stories devem ser independentes o suficiente para review isolado
- Se surgir ambiguidade nos requisitos durante implementação → course correction
