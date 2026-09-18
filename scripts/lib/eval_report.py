#!/usr/bin/env python3
"""
eval_report.py — relatório versionável de uma rodada de eval (B-012).

Lê um JSON no stdin e escreve o markdown de `docs/evals/<data>-<modelo>-<suite>.md`.
O formato é o mínimo que torna um resultado comparável com outro: SHA do OSForge,
id do modelo, comando exato, k de N por caso, tokens e tempo. Números de eval soltos
em prosa (CLAUDE.md, route-guard.py) passam a citar um arquivo daqui em vez de
afirmarem "medido" sem dizer quando, com que modelo e a que custo.

Uso:  ... | scripts/lib/eval_report.py [ARQUIVO_SAIDA]   (sem argumento: stdout)
"""
import json
import os
import sys


def fmt_int(n):
    return f"{int(n):,}".replace(",", " ")


def main(argv):
    data = json.load(sys.stdin)
    cases = data.get("cases", [])
    runs = data.get("runs", 1)
    tok = data.get("tokens", {})
    tally = {}
    for c in cases:
        tally[c["verdict"]] = tally.get(c["verdict"], 0) + 1
    total = len(cases) or 1
    passed = tally.get("PASS", 0)

    L = []
    L.append(f"# Eval · {data.get('suite', '?')} · {data.get('model', '?')}")
    L.append("")
    L.append(f"- **Data (UTC):** {data.get('started', '?')} · duração {data.get('duration_s', '?')} s")
    L.append(f"- **Modelo:** `{data.get('model', '?')}`")
    L.append(f"- **OSForge:** v{data.get('repo_version', '?')} · `{data.get('repo_sha', '?')}`"
             + (" · **árvore suja**" if data.get("dirty") else ""))
    L.append(f"- **HOME usado:** `{data.get('home', '?')}`")
    L.append(f"- **Execuções por caso:** {runs}")
    L.append(f"- **Comando:** `{data.get('command', '?')}`")
    if tok:
        L.append(f"- **Tokens:** in {fmt_int(tok.get('input', 0))} · out {fmt_int(tok.get('output', 0))} · "
                 f"cache_read {fmt_int(tok.get('cache_read', 0))} · cache_create {fmt_int(tok.get('cache_create', 0))}")
    L.append("")
    L.append(f"**Resultado:** {passed}/{len(cases)} PASS ({100.0 * passed / total:.0f} %)"
             + "".join(f" · {k} {v}" for k, v in sorted(tally.items()) if k != "PASS"))
    L.append("")
    L.append("Um caso só é PASS quando acerta nas N execuções. `0 < k < N` é **FLAKY**: instável,")
    L.append("não aprovado — é esta lista que o experimento E1 consome.")
    L.append("")
    L.append("| Caso | k de N | Veredito | Detalhe |")
    L.append("|---|---|---|---|")
    order = {"FAIL": 0, "TIMEOUT": 1, "FLAKY": 2, "PASS": 3}
    for c in sorted(cases, key=lambda c: (order.get(c["verdict"], 9), c["id"])):
        detail = str(c.get("detail", "")).replace("|", "\\|")
        L.append(f"| `{c['id']}` | {c.get('k', '?')}/{c.get('n', runs)} | {c['verdict']} | {detail} |")
    L.append("")
    flaky = [c["id"] for c in cases if c["verdict"] == "FLAKY"]
    if flaky:
        L.append("## Casos instáveis (entrada do E1)")
        L.append("")
        L.append(", ".join(f"`{x}`" for x in flaky))
        L.append("")
    if data.get("notes"):
        L.append("## Notas")
        L.append("")
        L.append(str(data["notes"]))
        L.append("")
    out = "\n".join(L)

    if argv:
        path = argv[0]
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(out)
        print(path)
    else:
        sys.stdout.write(out)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
