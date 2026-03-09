---
description: Cria ou atualiza a constituição do projeto — princípios, convenções e governança que guiam todas as decisões técnicas. Use ao iniciar um projeto novo ou quando precisar formalizar regras do time. Gatilhos: "constituição do projeto", "criar constitution", "definir princípios", "governance".
---

## Contexto necessário
Leia antes de executar:
- `README.md` (se existir) — visão geral do projeto
- `.specs/memory/constitution.md` (se existir) — versão anterior a atualizar
- `package.json` — stack atual

## Fase: Pré-projeto — Constituição

## Saída esperada
`.specs/memory/constitution.md`

## Processo

1. **Verificar existência**: Se `.specs/memory/constitution.md` existe, carregue-o e identifique a versão atual.

2. **Coletar valores** para os seguintes elementos:
   - Nome do projeto e propósito central
   - Princípios de desenvolvimento (máximo 7, mínimo 3)
   - Stack técnica obrigatória
   - Padrões de qualidade (testes, code review, deploy)
   - Convenções de nomenclatura e estrutura
   - Critérios para aceitar ou rejeitar mudanças arquiteturais

3. **Versionar**: Se é nova constituição → v1.0.0. Se é atualização:
   - Mudança de princípio → MAJOR (v2.0.0)
   - Novo princípio adicionado → MINOR (v1.1.0)
   - Clarificação ou correção → PATCH (v1.0.1)

4. **Criar** `.specs/memory/` (se não existir) e salvar o arquivo:

```markdown
# Constituição do Projeto: [NOME]
**Versão:** [x.y.z] | **Ratificado:** [YYYY-MM-DD] | **Última alteração:** [YYYY-MM-DD]

## Propósito
[Uma frase que define o que este projeto faz e para quem]

## Princípios
1. **[Nome]**: [Descrição — como aplicar, o que implica]
2. **[Nome]**: [Descrição]
...

## Stack Obrigatória
[Lista com versões fixas]

## Padrões de Qualidade
- Cobertura mínima de testes: [%]
- Code review: [quem revisa, critérios]
- Deploy: [processo, branches]

## Convenções
[Nomenclatura, estrutura de pastas, padrões de commits]

## Critérios para Mudanças Arquiteturais
[O que justifica mudar a arquitetura vs. adaptar dentro dela]
```

5. **Confirmar** ao usuário: versão criada/atualizada, path do arquivo, próximos passos.

## Notas
- Não pergunte por cada campo individualmente — use o contexto existente e inferência do README/package.json
- Se o usuário forneceu input, use-o diretamente sem reconfirmar cada item
- A constituição é referenciada pelos commands `/spec:specify` e `/spec:design`
