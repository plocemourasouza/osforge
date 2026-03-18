# Plan Template: QUICK

## Plano: {título}
**Complexidade:** QUICK
**Fases:** 3

### Fase 1: Especificação
- **Objetivo:** Definir exatamente o que fazer com acceptance criteria
- **Skill:** `skills/planning/spec-builder`
- **Artefato:** `{output_dir}/tech-spec-{slug}.md`
- **Tamanho:** Pequeno

### Fase 2: Implementação
- **Objetivo:** Executar as tasks da spec
- **Skill:** Skills de execução relevantes (identificar pelo tipo de mudança)
- **Artefato:** Código + testes
- **Tamanho:** {estimar baseado na spec}

### Fase 3: Review
- **Objetivo:** Validar implementação
- **Skill:** `skills/quality/code-review`
- **Artefato:** Review report (aprovado ou changes requested)
- **Tamanho:** Pequeno

### Checkpoints
- Após Fase 1: aprovar spec antes de implementar
- Após Fase 3: verificar se tudo está coberto

### Notas
- Se durante implementação surgirem complicações, reclassificar para STANDARD
- Spec deve ter no máximo ~1600 tokens (escopo contido)
