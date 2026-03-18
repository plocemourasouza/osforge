---
name: artifact-chain
description: >
  Rule always-on que garante rastreabilidade entre artefatos de planning
  e respeito ao project-context.md como constituição do projeto.
type: always-on
version: 1.0.0
---

# Rule: Artifact Chain

## Rastreabilidade

- Toda spec deve referenciar project-context.md (se existir).
- Todo story deve referenciar a spec ou épico que o originou.
- Todo code review deve referenciar a story sendo revisada.
- Toda decisão de arquitetura deve ser documentada como ADR.
- Frontmatter com `depends_on: []` em artefatos que dependem de outros.

## Project Context como Constituição

- Se `project-context.md` existe no projeto, ele é a fonte de verdade para:
  - Stack e versões
  - Naming conventions
  - Patterns de código
  - Regras de segurança
  - Anti-patterns proibidos
- Qualquer skill ou agent DEVE carregar project-context.md antes de gerar
  código ou tomar decisões técnicas.
- Se uma decisão conflitar com project-context.md, HALT e perguntar ao
  usuário qual prevalece.
- Se project-context.md não existir em projeto existente: sugerir geração
  via `skills/context/project-context-generator` antes de trabalho significativo.

## Linguagem

- Comunicação com o dev: Português Brasileiro (default)
- Output de documentos técnicos: Inglês (default, override com instrução explícita)
- Código: sempre em inglês (variáveis, funções, comments, commits)
- Conventional Commits em inglês: `feat:`, `fix:`, `refactor:`, etc.
