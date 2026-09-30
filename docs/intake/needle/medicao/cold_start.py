#!/usr/bin/env python3
"""Partida a frio: o que um hook pagaria por prompt (processo novo, 47 ferramentas, pesos em cache).

Uso: cold_start.py <repo_osforge>   (rodar 3 vezes, cada uma num processo novo)
"""
import json, os, sys, time

t0 = time.perf_counter()
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
sys.argv = ["needle_eval.py", sys.argv[1], os.devnull]
import needle_eval as ne  # noqa: E402

t1 = time.perf_counter()
agent = ne.needle.Needle(tools=ne.tools_for(sorted(ne.skills), "full"), stateless=True,
                         tool_index_path=os.path.join(os.environ.get("TMPDIR", "/tmp"), "needle-cold.idx"))
t2 = time.perf_counter()
r = agent.complete("Revisa esse diff com olhar crítico.")
t3 = time.perf_counter()
print(json.dumps({"import_ms": round((t1 - t0) * 1000), "init_ms": round((t2 - t1) * 1000),
                  "first_call_ms": round((t3 - t2) * 1000), "total_ms": round((t3 - t0) * 1000),
                  "peak_ram_mb": r.get("peak_ram_mb")}))
