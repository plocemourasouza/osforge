#!/usr/bin/env python3
"""
Medir o custo REAL de contexto a partir dos logs do harness.

Por que existe
--------------
Todo número de contexto que usamos até aqui foi estimativa por soma de arquivos
(`len(texto)//4`), que ignora prompt de sistema, definição de ferramentas e —
sobretudo — os schemas dos MCP servers, que costumam ser o maior item isolado.

Os logs que o harness já gravou contêm a resposta certa: o evento de init lista
as ferramentas e os MCP servers realmente carregados, e o primeiro `usage` diz
quantos tokens de entrada a sessão consumiu antes de qualquer trabalho útil.
Custo zero de API — é só ler o que está em /tmp.

Uso
---
    python3 scripts/measure-context.py                       # última rodada
    python3 scripts/measure-context.py /tmp/osforge-skill-tests/20260730_232332
    python3 scripts/measure-context.py --raw                 # despeja o evento de init

Se o formato do stream mudar, `--raw` mostra o evento cru para ajustar o parser
em vez de o script mentir em silêncio.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

LOGS_ROOT = Path("/tmp/osforge-skill-tests")


def latest_run() -> Path | None:
    if not LOGS_ROOT.is_dir():
        return None
    runs = sorted((p for p in LOGS_ROOT.iterdir() if p.is_dir()), key=lambda p: p.name)
    return runs[-1] if runs else None


def load_events(stream: Path) -> list[dict]:
    out = []
    for line in stream.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out


def find_init(events: list[dict]) -> dict | None:
    for e in events:
        if e.get("type") == "system" and e.get("subtype") == "init":
            return e
    # fallback: qualquer evento que pareça um init
    for e in events:
        if "tools" in e or "mcp_servers" in e:
            return e
    return None


def first_usage(events: list[dict]) -> dict | None:
    for e in events:
        u = (e.get("message") or {}).get("usage") if isinstance(e.get("message"), dict) else None
        if u:
            return u
        if isinstance(e.get("usage"), dict):
            return e["usage"]
    return None


def report_case(stream: Path, raw: bool) -> dict | None:
    events = load_events(stream)
    if not events:
        return None

    init = find_init(events)
    usage = first_usage(events)

    if raw and init is not None:
        print(json.dumps(init, indent=2, ensure_ascii=False)[:4000])
        print("...")

    tools = init.get("tools") if init else None
    mcps = init.get("mcp_servers") if init else None

    def names(v):
        if isinstance(v, list):
            return [x if isinstance(x, str) else (x.get("name") or str(x)) for x in v]
        return []

    res = {
        "case": stream.parent.name,
        "tools": names(tools),
        "mcps": names(mcps),
        "usage": usage or {},
    }
    return res


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("run_dir", nargs="?", help="diretório da rodada (padrão: a mais recente)")
    ap.add_argument("--raw", action="store_true", help="despeja o evento de init de um caso")
    args = ap.parse_args()

    run = Path(args.run_dir) if args.run_dir else latest_run()
    if not run or not run.is_dir():
        print(f"nenhuma rodada encontrada em {LOGS_ROOT} — rode o harness primeiro.", file=sys.stderr)
        return 1

    streams = sorted(run.rglob("stream.json"))
    if not streams:
        print(f"nenhum stream.json em {run}", file=sys.stderr)
        return 1

    print(f"Rodada: {run}")
    print(f"Casos:  {len(streams)}\n")

    results = []
    for i, s in enumerate(streams):
        r = report_case(s, raw=args.raw and i == 0)
        if r:
            results.append(r)

    if not results:
        print("nenhum evento parseável nos logs.", file=sys.stderr)
        return 1

    ref = results[0]

    print("── Ferramentas e MCPs carregados na sessão ──────────────────────────")
    if ref["mcps"]:
        print(f"MCP servers ({len(ref['mcps'])}): {', '.join(sorted(ref['mcps']))}")
    else:
        print("MCP servers: nenhum reportado no init")
    if ref["tools"]:
        mcp_tools = [t for t in ref["tools"] if t.startswith("mcp__")]
        print(f"Ferramentas ({len(ref['tools'])}) — sendo {len(mcp_tools)} de MCP")
        if mcp_tools:
            print("  ferramentas MCP carregadas de imediato (não diferidas):")
            for t in sorted(mcp_tools)[:20]:
                print(f"    {t}")
            if len(mcp_tools) > 20:
                print(f"    … +{len(mcp_tools) - 20}")
        else:
            print("  nenhuma ferramenta MCP no init → tool search está DIFERINDO os schemas")
    else:
        print("Ferramentas: não reportadas no init (use --raw para inspecionar)")

    print("\n── Tokens de entrada por caso (antes de qualquer trabalho) ──────────")
    print(f"{'caso':<34} {'input':>8} {'cache_read':>11} {'cache_new':>10}")
    tot = []
    for r in results:
        u = r["usage"]
        inp = u.get("input_tokens", 0)
        cr = u.get("cache_read_input_tokens", 0)
        cc = u.get("cache_creation_input_tokens", 0)
        baseline = inp + cr + cc
        tot.append(baseline)
        print(f"{r['case']:<34} {inp:>8} {cr:>11} {cc:>10}")

    if tot:
        print(f"\nBaseline real (input+cache) — mediana: {sorted(tot)[len(tot)//2]:,} tokens")
        print(f"                              mínimo:  {min(tot):,}   máximo: {max(tot):,}")
        print("\nEsse número inclui prompt de sistema, CLAUDE.md, SKILLS.md, descriptions")
        print("das skills nativas, definição de ferramentas e schemas de MCP não diferidos.")
        print("É o custo fixo de abrir uma sessão — compare com a estimativa por arquivos.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
