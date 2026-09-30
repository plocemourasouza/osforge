# Medição do Needle 3 contra os casos de trigger do OSForge

Registro de 2026-09-24. Os números estão em [`../EVIDENCIAS.md`](../EVIDENCIAS.md)
(EV-N-M01 a EV-N-M09) e o veredito em [`../ANALISE.md`](../ANALISE.md). Estes scripts ficam
aqui para que a recusa possa ser refeita com uma versão nova do modelo, em vez de rediscutida.

**Não rodar no `HOME` real.** O Needle baixa e carrega uma biblioteca nativa sem conferência de
hash e tem telemetria ligada por padrão (EV-N07, EV-N12, EV-N13).

```sh
W=$(mktemp -d); python3 -m venv "$W/venv"
"$W/venv/bin/pip" install --no-cache-dir "cactus-needle==3.0.5"
export HOME="$W/home" HF_HOME="$W/hf" NEEDLE_TELEMETRY=0 DO_NOT_TRACK=1 CI=1
mkdir -p "$HOME"
# Em 2026-09-24 o motor pedido pelo pacote (3.0.2) não estava publicado (EV-N-M06);
# o último publicado era o 3.0.1, apontado pela variável documentada:
"$W/venv/bin/python" -c "import needle.agent.fetch as f; print(f.fetch_library(version='3.0.1', dest_dir='$W/lib', generation=3))"
export NEEDLE3_LIB_PATH="$W/lib/libneedle.dylib"     # .so no Linux

R=/caminho/do/osforge
"$W/venv/bin/python" needle_eval.py "$R" "$W/result.json" A B C   # PT: 3 cenários × 150 casos
"$W/venv/bin/python" en_eval.py     "$R" "$W/result_en.json"      # EN: 75 positivos traduzidos
for i in 1 2 3; do "$W/venv/bin/python" cold_start.py "$R"; done  # partida a frio
rm -rf "$W"
```

| Arquivo | O que faz |
|---|---|
| `needle_eval.py` | Skills core como ferramentas; cenários A (47, descrição inteira), B (47, 1ª frase), C (15 avaliadas); linhas de base léxica e por embeddings do próprio Needle |
| `en_eval.py` + `en_positives.tsv` | Controle de idioma: os 75 positivos traduzidos, cenários A e C |
| `cold_start.py` | Custo de um processo novo — o que um hook pagaria a cada prompt |

Nenhum script chama modelo pago. Tempo total: ~6 min num Mac M-series.
