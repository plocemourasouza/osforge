# P-04 · Guardas durante a edição (chamadores abertos, duplicata, estado dos testes)

**Origem:** a faixa do Ponytail (EV-P31, EV-P32, EV-P15, EV-P16), que mostra esses sinais só ao
humano (EV-P33). Aqui eles viram hooks clássicos e chegam ao **modelo**, no ato.
**Evidência local:** EV-O-P13, EV-O-P17, EV-C-P06.
**Esforço:** M. **Chamadas pagas:** 0. **Adoção:** modo sombra → injeção.

## Problema

Os dois erros que mais escapam numa mudança são quebrar quem chama o que mudou e reescrever
o que já existe noutro arquivo. O OSForge tenta evitar os dois só com texto
(`coding-guidelines`), e esse texto inteiro carregou em 10 de 277 subagentes que codaram
(EV-M-P01). Nenhum hook olha para isso: os `PostToolUse` atuais protegem testes e registram
observações (EV-O-P13). E o "pronto" da lei de verificação não tem nenhum dado sobre quando os
testes rodaram por último.

## Desenho

**Hook:** `hooks/quality-guard.py` (NOVO), com duas entradas em `PostToolUse` no
`hooks/hooks-claude-code.json`:

- `Edit|Write|MultiEdit` → G-1 e G-2;
- `Bash` → G-3.

O payload do Edit já é contrato testado no OSForge: `tool_input.file_path`, `old_string`,
`new_string` (EV-O-P17).

**G-1 chamadores abertos**

1. Só para arquivos de código do projeto (`.ts`, `.tsx`, `.js`, `.jsx`, `.mjs`, `.py`), fora de
   `node_modules`, `.next`, `dist`, testes e gerados.
2. Definições de topo exportadas antes e depois. No Edit, de `old_string` e `new_string`.
   No Write, do `git show HEAD:<arquivo>` contra o conteúdo novo; se o arquivo é novo, nada a
   remover.
3. Para cada nome que sumiu e não reapareceu: `git grep -nw -- <nome>` no repositório, com
   timeout de 1 s. Ficam só as linhas que **chamam** (`nome(`, `<Nome`, `import { nome`), fora
   do próprio arquivo.
4. Se sobrou alguma:

   > `[OSForge quality-guard] Você removeu ou renomeou \`formatPrice\`; ainda é usado em
   > src/app/cart/page.tsx:41, src/lib/invoice.ts:12. Atualize esses chamadores ou mantenha o
   > nome.`

   Até 5 locais, mais um "+N".

**G-2 duplicata provável**

1. Definições exportadas **novas** no arquivo editado.
2. Nome normalizado (minúsculas, sem `_` e `-`) igual a uma definição existente em **outro**
   arquivo, achada por `git grep -nE` do padrão de definição.
3. Ignora nomes genéricos (`get`, `handle`, `render`, `default`, `Page`, `Layout`…) e as
   convenções do Next.js (`page.tsx`, `layout.tsx`, `route.ts`, `generateMetadata`).
4. Se achar:

   > `[OSForge quality-guard] Já existe \`formatCurrency\` em src/lib/format.ts:8. Reutilize
   > (escada, degrau 2) ou diga por que precisa de outro.`

**G-3 estado dos testes**

1. Detecta o comando de teste pelo `package.json` do projeto (`test`, `test:*`) e pelos
   executores comuns (`vitest`, `jest`, `playwright test`). O comando precisa ser **executado**,
   não apenas mencionado: o `echo pytest` que engana a faixa do Ponytail não conta.
2. Grava `passou` ou `falhou` (código de saída), com contagens quando o executor as imprime
   (stdout e stderr). Contagem com falhas vence o código de saída. Se o teste não é o último
   comando da linha ou há `|`, `||` ou `;` (o código de saída deixa de ser o do executor) e
   não há resumo legível, grava `incerto` (`unknown`). Achado da revisão: `npx vitest run | tail`
   gravava `passou` com testes falhando.
3. Qualquer Edit ou Write num arquivo de código do projeto, depois disso, marca `desatualizado`.
4. Nesta fase vai só para o monitor; não injeta nada. Ligar ao `Stop`, para lembrar o modelo
   antes de um "pronto" sem teste fresco, é uma decisão posterior (D-G2).

**Sinais:** tabela `signals` em `osforge-db.py` (migração idempotente):
`id`, `ts`, `project_id`, `session_id`, `kind` (`callers_open` | `duplicate` | `tests`),
`subject`, `detail` (JSON, só caminhos e nomes), `resolved_at`.

- Um G-1 se resolve sozinho quando um Edit posterior faz o `grep` voltar vazio.
- Comandos: `osforge-db add-signal`, `osforge-db signals <slug> [--open]`.
- Retenção: 90 dias, como `calls`.

**Modo sombra:** `OSFORGE_QUALITY_GUARD=shadow` (padrão na primeira versão) grava os sinais e
não injeta. Depois de duas semanas, `osforge-db signals --report` mostra quantos houve e quantos
se resolveram sozinhos, e uma amostra de 20 é conferida à mão. Liga (`=on`) se:

- o alarme falso de G-1 for ≤ 10%;
- o alarme falso de G-2 for ≤ 25%.

`=off` desliga tudo.

## Arquivos

`hooks/quality-guard.py` **(NOVO)** · `hooks/lib/defs.py` **(NOVO**, definições por linguagem) ·
`hooks/hooks-claude-code.json` · `scripts/osforge-db.py` (`signals`, `add-signal`, relatório) ·
`tests/test-quality-guard.sh` **(NOVO)** · `tests/hooks/` (casos de contrato) · README e
`check-counts` (11 → 12 hooks) · `docs/HOOKS.md`.

## Testes (offline, repositório git temporário)

1. Renomear `formatPrice` usado em dois arquivos → G-1 lista os dois; corrigir os chamadores e
   editar de novo → sinal resolvido, nenhuma injeção.
2. Renomear uma função que **ninguém** chama → silêncio.
3. Mesmo nome em outro módulo, mas só como texto ou propriedade (`obj.formatPrice`) → silêncio.
4. Write de arquivo novo com `formatCurrency` já existente em `lib/format.ts` → G-2; com `get` → silêncio.
5. `page.tsx` novo com `export default function Page` → silêncio.
6. Bash `npm test` saindo 0 → `tests=passou`; Edit em `.ts` depois → `desatualizado`;
   `echo npm test` → nada muda.
7. Modo sombra → sinais gravados e stdout vazio; `=off` → nada gravado.
8. Repositório sem git, arquivo fora do projeto, payload inválido → exit 0 em silêncio.
9. Orçamento: repositório sintético com 5 mil arquivos → p95 < 150 ms no Edit comum.

## Aceite

Os nove casos verdes; as suítes atuais verdes; contrato de hooks atualizado; duas semanas de
sombra com o relatório versionado em `docs/evals/` antes de ligar a injeção.

## Decisões

- **D-G1** — linguagens além de TS/JS/Python. Recomendação: não agora.
- **D-G2** — G-3 lembrar o modelo no `Stop`. Recomendação: depois da sombra, e só se o alarme
  falso for baixo.
