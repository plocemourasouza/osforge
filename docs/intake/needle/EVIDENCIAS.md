# Needle — evidências

**FATO** = lido no código ou medido · **INF** = inferência, dita como tal.

- Needle: `cactus-compute/needle` @ `42bf1f2d0a7784b0d4d1ec94bb5ade425cf9a67c`; os links abaixo usam
  `https://github.com/cactus-compute/needle/blob/42bf1f2d0a7784b0d4d1ec94bb5ade425cf9a67c/…`
- OSForge: `v5.1.0` @ `3f0446cafe57158ad7b9823c565ae4f973bdf014` (caminho:linha)
- Os prefixos levam a letra da fonte (`N`) para não colidir com os do Laya.

## Needle (EV-N)

| ID | Onde | Fato | Tipo |
|---|---|---|---|
| EV-N01 | [`needle/environments/_harness.py#L31-L60`](https://github.com/cactus-compute/needle/blob/42bf1f2d0a7784b0d4d1ec94bb5ade425cf9a67c/needle/environments/_harness.py#L31-L60) | Suíte passa com `round(0,9 × N)` acertos **e** nenhum caso `critical` reprovado; `min_confidence` trata chamada abaixo do limiar como recusa | FATO |
| EV-N02 | [`tests/test_environments.py#L11`](https://github.com/cactus-compute/needle/blob/42bf1f2d0a7784b0d4d1ec94bb5ade425cf9a67c/tests/test_environments.py#L11) · [`#L38`](https://github.com/cactus-compute/needle/blob/42bf1f2d0a7784b0d4d1ec94bb5ade425cf9a67c/tests/test_environments.py#L38) | Seis categorias obrigatórias (`positive`, `missing`, `irrelevant`, `negation`, `invalid`, `parallel`); um teste sem modelo reprova a suíte que não cobrir todas | FATO |
| EV-N03 | [`tests/test_environments.py#L42`](https://github.com/cactus-compute/needle/blob/42bf1f2d0a7784b0d4d1ec94bb5ade425cf9a67c/tests/test_environments.py#L42) | Cada chamada esperada de cada caso é validada contra o schema da ferramenta declarada (nome, obrigatórios, enum, limites, padrão) | FATO |
| EV-N04 | [`tests/test_environments.py#L29-L31`](https://github.com/cactus-compute/needle/blob/42bf1f2d0a7784b0d4d1ec94bb5ade425cf9a67c/tests/test_environments.py#L29-L31) | Cada ambiente tem **no máximo 5** ferramentas, por teste | FATO |
| EV-N05 | [`tests/test_environments.py#L95`](https://github.com/cactus-compute/needle/blob/42bf1f2d0a7784b0d4d1ec94bb5ade425cf9a67c/tests/test_environments.py#L95) | Motor falso escolhe a resposta pela consulta: a regra de placar é testada sem modelo | FATO |
| EV-N06 | [`needle/environments/smart_home.py#L111-L113`](https://github.com/cactus-compute/needle/blob/42bf1f2d0a7784b0d4d1ec94bb5ade425cf9a67c/needle/environments/smart_home.py#L111-L113) | Os casos críticos são os de informação faltando: agir ali significaria inventar um valor | FATO |
| EV-N07 | [`needle/agent/fetch.py#L11-L13`](https://github.com/cactus-compute/needle/blob/42bf1f2d0a7784b0d4d1ec94bb5ade425cf9a67c/needle/agent/fetch.py#L11-L13) · [`#L215`](https://github.com/cactus-compute/needle/blob/42bf1f2d0a7784b0d4d1ec94bb5ade425cf9a67c/needle/agent/fetch.py#L215) | O pacote pede o motor 3.0.2 e baixa a *wheel* do motor da `main` do repositório de pesos, sem `revision` e sem hash | FATO |
| EV-N08 | [`needle/__init__.py#L80`](https://github.com/cactus-compute/needle/blob/42bf1f2d0a7784b0d4d1ec94bb5ade425cf9a67c/needle/__init__.py#L80) · [`#L109`](https://github.com/cactus-compute/needle/blob/42bf1f2d0a7784b0d4d1ec94bb5ade425cf9a67c/needle/__init__.py#L109) | Sem biblioteca local, o motor é buscado na primeira execução e carregado via `ctypes` | FATO |
| EV-N09 | [`needle/__init__.py#L239`](https://github.com/cactus-compute/needle/blob/42bf1f2d0a7784b0d4d1ec94bb5ade425cf9a67c/needle/__init__.py#L239) · [`llms.txt#L22`](https://github.com/cactus-compute/needle/blob/42bf1f2d0a7784b0d4d1ec94bb5ade425cf9a67c/llms.txt#L22) | `tool_index_path` é passado ao motor; a documentação promete persistir os embeddings das ferramentas | FATO |
| EV-N10 | [`llms.txt#L159`](https://github.com/cactus-compute/needle/blob/42bf1f2d0a7784b0d4d1ec94bb5ade425cf9a67c/llms.txt#L159) | Com mais de 5 ferramentas, uma cabeça de recuperação escolhe as 5 que entram em cada turno | FATO |
| EV-N11 | [`llms.txt#L228`](https://github.com/cactus-compute/needle/blob/42bf1f2d0a7784b0d4d1ec94bb5ade425cf9a67c/llms.txt#L228) | O modelo base não passa em cinco das seis suítes de aceite no limiar padrão | FATO |
| EV-N12 | [`needle/_telemetry.py#L30-L31`](https://github.com/cactus-compute/needle/blob/42bf1f2d0a7784b0d4d1ec94bb5ade425cf9a67c/needle/_telemetry.py#L30-L31) · [`#L67`](https://github.com/cactus-compute/needle/blob/42bf1f2d0a7784b0d4d1ec94bb5ade425cf9a67c/needle/_telemetry.py#L67) | Telemetria ligada salvo `NEEDLE_TELEMETRY=0`, `DO_NOT_TRACK` ou `CI`; envia evento, versões, SO, arquitetura e um id aleatório persistido | FATO |
| EV-N13 | [`README.md#L118`](https://github.com/cactus-compute/needle/blob/42bf1f2d0a7784b0d4d1ec94bb5ade425cf9a67c/README.md#L118) | "By default, telemetry is turned on in the binary" — a parte nativa não é auditável pelo código | FATO |
| EV-N14 | [`pyproject.toml#L3`](https://github.com/cactus-compute/needle/blob/42bf1f2d0a7784b0d4d1ec94bb5ade425cf9a67c/pyproject.toml#L3) | O código no GitHub declara 3.0.1; o PyPI publica 3.0.5 (medido em 2026-09-24) | FATO |
| EV-N15 | [`llms.txt#L131`](https://github.com/cactus-compute/needle/blob/42bf1f2d0a7784b0d4d1ec94bb5ade425cf9a67c/llms.txt#L131) | Guia de confiança: agir acima de um limiar (o exemplo usa 0,7), confirmar abaixo, recusar sem chamada | FATO |
| EV-N16 | [`README.md#L5`](https://github.com/cactus-compute/needle/blob/42bf1f2d0a7784b0d4d1ec94bb5ade425cf9a67c/README.md#L5) | Promessa: pedido que nenhuma ferramenta cobre devolve lista vazia, não um palpite | FATO |

## Medição (EV-N-M) — 2026-09-24, Mac arm64, isolado

Ambiente: Python 3.14.5; `cactus-needle` 3.0.5 do PyPI; motor 3.0.1 (último publicado — o
pedido, 3.0.2, não existe) via `NEEDLE3_LIB_PATH`, `libneedle.dylib` de 821.696 bytes,
sha256 `fd87fba146edec4baeff16c42abd76ba46b02d99465eab7b30492ab9fe5fdd9c`; pesos
`needle3.cact` de 35.335.380 bytes (repositório de pesos em `b274efc`, 2026-09-19). Venv e
`HOME` em `/tmp`, `NEEDLE_TELEMETRY=0 DO_NOT_TRACK=1 CI=1`, `HF_HUB_OFFLINE=1` depois do
download; tudo removido ao final. Script e números em [`medicao/`](medicao/README.md).

| ID | Fato |
|---|---|
| EV-N-M01 | Acerto nos 75 positivos: 47 core PT **0**; 47 core com 1ª frase PT 4; 15 avaliadas PT 10; 47 core EN 3; 15 avaliadas EN 13. Linha de base léxica: PT 7 top-1 / 8 top-5; EN 16 / 33 |
| EV-N-M02 | Em nenhum cenário um negativo recebeu lista vazia (0 de 75, três cenários). No cenário 47 core PT, `receiving-code-review` foi escolhida em 93 de 150 consultas. Contraria EV-N16 no nosso domínio |
| EV-N-M03 | Confiança como separador de acerto e erro (AUC): PT 0,468 e 0,406; EN 0,639 e 0,571. Decisões PT com confiança ≥ 0,7 (EV-N15): 111, das quais 60 corretas |
| EV-N-M04 | Embeddings do Needle (3072 dimensões, ~80 ms por texto) como roteador por vizinho mais próximo: PT 4 top-1 / 12 top-5; EN 4 / 18 — abaixo da linha de base léxica em inglês |
| EV-N-M05 | Partida a frio num processo novo, pesos em cache, 47 ferramentas: 8,7 s · 10,5 s · 8,8 s; RAM de pico ~203 MB. `tool_index_path` informado nas três execuções e **nenhum arquivo** criado (EV-N09) |
| EV-N-M06 | Com o PyPI 3.0.5, o exemplo do README falha: 404 em `python/cactus_needle-3.0.2-py3-none-macosx_11_0_arm64.whl`. O repositório de pesos só tem *wheels* 3.0.0 e 3.0.1 |
| EV-N-M07 | 1 de 150 chamadas (47 core PT) falhou com `'utf-8' codec can't decode byte 0xc3` — envelope do motor truncado num caractere acentuado |
| EV-N-M08 | Só com uma ferramenta de clima: "what's the capital of France?" → lista vazia; "qual a capital da França?" → `get_weather(city="França")`, confiança 1,0 |
| EV-N-M09 | `huggingface.co` bloqueado (403 no proxy) no container da nuvem e na VM do Cowork |

## OSForge (EV-O-N) — `v5.1.0`

| ID | Onde | Fato | Tipo |
|---|---|---|---|
| EV-O-N01 | `scripts/evals/trigger/*.json`; validação em `scripts/run-trigger-eval.sh:61-110` | Caso = `{id, should_trigger, query}`. A validação confere `rel`, ids, mínimo 5+5, split e consulta repetida; não existe categoria nem caso crítico | FATO |
| EV-O-N02 | `scripts/test-skill-triggering.sh:478-497`, `:255` | O `--dry` imprime "ÓRFÃO" e sai com 0; na execução paga é só um aviso. Reproduzido: caso com skill inexistente → `--dry` exit 0 | FATO |
| EV-O-N03 | `scripts/test-orchestrator-routing.sh:112-138` | O `--dry` de roteamento lista os casos sem conferir se agente, skill ou tier esperados existem | FATO |
| EV-O-N04 | `scripts/test-skill-triggering.sh:551`, `scripts/test-orchestrator-routing.sh:243` | Com `--allow-flaky`, um FLAKY não reprova a suíte — sem exceção para caso nenhum | FATO |
| EV-O-N05 | `scripts/lib/eval_report.py:53` | Tabela do relatório: Caso · k de N · Veredito · Detalhe; sem categoria | FATO |
| EV-O-N06 | `.github/workflows/ci.yml:67-69` | O CI roda o `--dry` das três suítes: validação posta no `--dry` vira gate de CI sem mudar o workflow | FATO |
| EV-O-N07 | `docs/BACKLOG-EVOLUCAO.md:23-24` | E1 = 6 (piloto) + 48 (roteamento) + 180 (trigger `eval`) chamadas | FATO |
