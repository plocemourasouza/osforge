---
name: editorial-review
description: >
  Revisão editorial de documentos técnicos em 2 modos: prose (copy-editing
  clínico) e structure (reorganização e simplificação).
  Use com "editorial review", "review prose", "review structure", "revisar redação".
trigger: editorial|review prose|review structure|revisar redação
model-tier: sonnet
---

# Editorial Review

## Modos de Operação

Detectar modo pelo trigger ou perguntar se ambíguo.

### Modo Prose (default)
Copy-editor clínico. Revisar texto para problemas de comunicação.

**Checklist:**
- **Clareza:** Frases ambíguas, modificadores pendentes, referências vagas
- **Concisão:** Palavras desnecessárias, redundâncias, circunlóquios
- **Consistência:** Terminologia variando, formatos inconsistentes, tom mudando
- **Precisão:** Afirmações vagas que deveriam ser específicas, números sem fonte
- **Tom:** Shifts de registro, voz passiva excessiva, jargão desnecessário
- **Gramática:** Erros técnicos de linguagem, concordância, regência

**Output:**
```markdown
## Editorial Review — Prose

### Issues Encontrados: {N}

1. **[Linha ~{N}]** {tipo}: "{trecho problemático}"
   → Sugestão: "{correção proposta}"

2. **[Seção {nome}]** {tipo}: {descrição}
   → Sugestão: {correção}
...
```

### Modo Structure
Editor estrutural. Propor reorganização sem reescrever.

**Análise:**
- **Cortes:** Seções que podem ser removidas sem perda de compreensão
- **Reorganização:** Seções fora de ordem lógica (dependência de leitura)
- **Merge:** Seções que cobrem o mesmo tema e devem ser combinadas
- **Split:** Seções que tentam cobrir assuntos demais
- **Simplificação:** Hierarquias de heading desnecessariamente profundas
- **Gaps:** Informação esperada mas ausente dado o tipo de documento

**Output:**
```markdown
## Editorial Review — Structure

### Plano de Reestruturação

1. **CORTAR** seção "{nome}" — Razão: {justificativa}
2. **MOVER** seção "{nome}" para depois de "{outra}" — Razão: {justificativa}
3. **MERGE** seções "{A}" e "{B}" — Razão: {justificativa}
4. **SPLIT** seção "{nome}" em "{sub-A}" e "{sub-B}" — Razão: {justificativa}
5. **GAP** falta seção sobre "{tópico}" — Razão: {justificativa}

### Estrutura Proposta
{outline da nova estrutura com headings}
```

## Regra Fundamental
NÃO reescrever o documento — apenas listar findings e sugestões.
O usuário decide o que aplicar.
