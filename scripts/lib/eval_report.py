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

# Ordem "mais difícil primeiro" (N-01/B-025): um vizinho errado é o caso onde a
# skill confundiu domínios vizinhos; um irrelevante errado é o caso fácil.
CATEGORY_ORDER = ["vizinho", "negacao", "irrelevante", "positivo"]


def fmt_int(n):
    return f"{int(n):,}".replace(",", " ")


def fmt_quota(q):
    """quota_at_start/quota_at_end (B-026, B3): read_state()'s dict, or None/"null"."""
    if not isinstance(q, dict):
        return "sem dados"
    parts = []
    five = q.get("five_hour")
    if isinstance(five, dict) and isinstance(five.get("pct"), (int, float)):
        parts.append(f"5h {five['pct']:.0f}%")
    if isinstance(q.get("rejected"), dict):
        parts.append("rejected")
    return " · ".join(parts) if parts else "sem dados"


def category_summary(cases):
    """Uma linha por categoria: quantos casos daquela categoria são PASS.
    Só aparece quando algum caso traz 'category' — nem toda suíte tem (routing
    não categoriza, trigger sim)."""
    by_cat = {}
    for c in cases:
        cat = c.get("category")
        if cat is None:
            continue
        passed, total = by_cat.get(cat, (0, 0))
        by_cat[cat] = (passed + (1 if c["verdict"] == "PASS" else 0), total + 1)
    if not by_cat:
        return None
    ordered = [c for c in CATEGORY_ORDER if c in by_cat]
    ordered += sorted(c for c in by_cat if c not in CATEGORY_ORDER)
    return " · ".join(f"`{cat}` {by_cat[cat][0]}/{by_cat[cat][1]} PASS" for cat in ordered)


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
    has_category = any(c.get("category") is not None for c in cases)

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
    quota_start, quota_end = data.get("quota_at_start"), data.get("quota_at_end")
    if quota_start is not None or quota_end is not None:
        L.append(f"- **Cota (B-026/B3):** início {fmt_quota(quota_start)} · fim {fmt_quota(quota_end)}")
    L.append("")

    # Críticos reprovados vão ANTES de tudo (EV-O-N05): um caso crítico (negação,
    # ou despacho obrigatório) que falhou é a primeira coisa que quem lê precisa
    # saber — reprova a suíte mesmo quando o placar geral parece bom.
    critical_failed = [c for c in cases if c.get("critical") and c["verdict"] != "PASS"]
    if critical_failed:
        L.append("## Críticos reprovados")
        L.append("")
        for c in sorted(critical_failed, key=lambda c: c["id"]):
            detail = str(c.get("detail", "")).replace("|", "\\|")
            L.append(f"- `{c['id']}` — {c['verdict']} ({c.get('k', '?')}/{c.get('n', runs)}){': ' + detail if detail else ''}")
        L.append("")

    L.append(f"**Resultado:** {passed}/{len(cases)} PASS ({100.0 * passed / total:.0f} %)"
             + "".join(f" · {k} {v}" for k, v in sorted(tally.items()) if k != "PASS"))
    L.append("")
    if has_category:
        summary = category_summary(cases)
        if summary:
            L.append(f"**Por categoria:** {summary}")
            L.append("")
    L.append("Um caso só é PASS quando acerta nas N execuções. `0 < k < N` é **FLAKY**: instável,")
    L.append("não aprovado — é esta lista que o experimento E1 consome.")
    L.append("")
    header = "| Caso | k de N | Veredito | Detalhe |" if not has_category else "| Caso | Categoria | k de N | Veredito | Detalhe |"
    sep = "|---|---|---|---|" if not has_category else "|---|---|---|---|---|"
    L.append(header)
    L.append(sep)
    order = {"FAIL": 0, "ERROR": 1, "TIMEOUT": 1, "FLAKY": 2, "NOT RUN": 2, "PASS": 3}
    for c in sorted(cases, key=lambda c: (order.get(c["verdict"], 9), c["id"])):
        detail = str(c.get("detail", "")).replace("|", "\\|")
        if has_category:
            cat = c.get("category", "")
            L.append(f"| `{c['id']}` | {cat} | {c.get('k', '?')}/{c.get('n', runs)} | {c['verdict']} | {detail} |")
        else:
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
