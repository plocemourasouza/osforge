#!/usr/bin/env python3
"""Generate searchable markdown index from INDICE-SKILLS.json"""
import json
from collections import defaultdict
from pathlib import Path

BASE = Path(__file__).parent.parent  # raiz do repo (extract grava o JSON lá)
with open(BASE / "INDICE-SKILLS.json", 'r', encoding='utf-8') as f:
    skills = json.load(f)

by_cat = defaultdict(list)
for s in skills:
    by_cat[s['category']].append(s)

cat_order = sorted(by_cat.keys(), key=lambda c: -len(by_cat[c]))

by_source = defaultdict(int)
for s in skills:
    by_source[s['source']] += 1

source_priority = {
    "Anthropic (Oficial)": 0, "Superpowers (obra)": 1, "Vercel Labs": 2,
    "Trail of Bits": 3, "Supabase": 4, "Cloudflare": 5, "Sentry": 6,
    "Expo": 7, "Context Engineering": 8, "Antigravity (634+)": 9,
}

L = []
L.append("# 📚 Índice Completo de Agent Skills\n")
L.append(f"> **Total:** {len(skills)} skills indexadas de {len(by_source)} repositórios")
L.append("> **Pasta local:** `~/Development/osforge/sources/` (fontes) e `~/Development/osforge/skills/` (curadas)")
L.append(">")
L.append("> 💡 **Dica de busca:** Use `Ctrl+F` / `Cmd+F` para pesquisar por palavra-chave.")
L.append("> Para instalar uma skill: `cp -R ~/Development/osforge/<path_local> .claude/skills/`\n")
L.append("---\n")

# Stats
L.append("## 📊 Estatísticas\n")
L.append("### Por Categoria\n")
L.append("| Categoria | Qtd | % |")
L.append("|-----------|-----|---|")
total = len(skills)
for cat in cat_order:
    n = len(by_cat[cat])
    L.append(f"| {cat} | {n} | {round(n/total*100,1)}% |")
L.append(f"| **TOTAL** | **{total}** | **100%** |\n")

L.append("### Por Origem\n")
L.append("| Origem | Repo | Qtd |")
L.append("|--------|------|-----|")
for src, n in sorted(by_source.items(), key=lambda x: -x[1]):
    url = next((s['source_url'] for s in skills if s['source'] == src and s['source_url']), "")
    link = f"[Link]({url})" if url else "—"
    L.append(f"| {src} | {link} | {n} |")
L.append("\n---\n")

# TOC
L.append("## 🗂️ Sumário por Categoria\n")
for cat in cat_order:
    L.append(f"- [{cat} ({len(by_cat[cat])})](#)")
L.append("\n---\n")

# Details per category
for cat in cat_order:
    cat_skills = by_cat[cat]
    L.append(f"## {cat}\n")
    L.append(f"**{len(cat_skills)} skills**\n")
    L.append("| Skill | Origem | Descrição | Path Local |")
    L.append("|-------|--------|-----------|-----------|")
    
    cat_skills.sort(key=lambda s: (source_priority.get(s['source'], 99), s['name'].lower()))
    
    for s in cat_skills:
        name = s['name'].replace('|', '\\|')
        desc = s['description'][:150].replace('|', '\\|').replace('\n', ' ')
        if len(s['description']) > 150:
            desc += "…"
        src = f"{s['source_emoji']} {s['source']}"
        path = f"`{s['local_path']}/`"
        L.append(f"| **{name}** | {src} | {desc} | {path} |")
    L.append("")

# Alphabetical index
L.append("---\n")
L.append("## 🔤 Índice Alfabético Rápido\n")
L.append("Lista compacta para busca rápida com `Ctrl+F`:\n")

all_sorted = sorted(skills, key=lambda s: s['name'].lower())
current_letter = ""
for s in all_sorted:
    first = s['name'][0].upper() if s['name'][0].isalpha() else "#"
    if first != current_letter:
        current_letter = first
        L.append(f"\n**{current_letter}**")
    short_src = s['source'].split('(')[0].strip()[:15]
    L.append(f"- `{s['name']}` — {short_src} — `{s['local_path']}/`")

L.append("\n---\n")
L.append("*Índice gerado automaticamente por Claude Opus 4.6 a partir de 770 SKILL.md files.*")

content = '\n'.join(L)
out = BASE / "docs" / "INDICE-SKILLS.md"
with open(out, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"✅ {out}")
print(f"   {len(skills)} skills | {len(L)} linhas | {len(content):,} chars")
