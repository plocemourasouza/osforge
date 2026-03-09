#!/usr/bin/env python3
"""
🔍 Busca de Agent Skills no repositório local consolidado.

Uso:
    python3 buscar-skill.py <termo>           # Busca por nome/descrição
    python3 buscar-skill.py --cat security     # Filtra por categoria
    python3 buscar-skill.py --src vercel       # Filtra por origem
    python3 buscar-skill.py --install react    # Mostra comando de instalação
    python3 buscar-skill.py --list-cats        # Lista categorias
    python3 buscar-skill.py --list-sources     # Lista origens
    python3 buscar-skill.py --stats            # Estatísticas gerais

Exemplos:
    python3 buscar-skill.py typescript
    python3 buscar-skill.py "react best"
    python3 buscar-skill.py --cat security audit
    python3 buscar-skill.py --install supabase
"""
import json
import sys
import os
from pathlib import Path

BASE = Path(__file__).parent
INDEX = BASE / "INDICE-SKILLS.json"

# Colors
class C:
    BOLD = '\033[1m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    DIM = '\033[2m'
    RESET = '\033[0m'

def load_index():
    with open(INDEX, 'r', encoding='utf-8') as f:
        return json.load(f)

def search(skills, term, cat_filter=None, src_filter=None):
    term_lower = term.lower() if term else ""
    results = []
    for s in skills:
        if cat_filter and cat_filter.lower() not in s['category'].lower():
            continue
        if src_filter and src_filter.lower() not in s['source'].lower():
            continue
        if term_lower:
            text = f"{s['name']} {s['description']} {s['local_path']}".lower()
            if term_lower not in text:
                continue
        results.append(s)
    return results

def print_result(s, show_install=False):
    print(f"  {C.BOLD}{C.CYAN}{s['name']}{C.RESET}")
    print(f"    {C.DIM}Origem:{C.RESET} {s['source_emoji']} {s['source']}")
    print(f"    {C.DIM}Categoria:{C.RESET} {s['category']}")
    desc = s['description'][:200]
    if len(s['description']) > 200:
        desc += "…"
    print(f"    {C.DIM}Descrição:{C.RESET} {desc}")
    print(f"    {C.DIM}Path:{C.RESET} {C.GREEN}{s['local_path']}/{C.RESET}")
    if show_install:
        full_path = BASE / s['local_path']
        print(f"    {C.YELLOW}Instalar:{C.RESET} cp -R \"{full_path}\" .claude/skills/")
    print()

def list_categories(skills):
    cats = {}
    for s in skills:
        c = s['category']
        cats[c] = cats.get(c, 0) + 1
    print(f"\n{C.BOLD}📂 Categorias disponíveis:{C.RESET}\n")
    for c, n in sorted(cats.items(), key=lambda x: -x[1]):
        print(f"  {c}  ({n} skills)")
    print()

def list_sources(skills):
    srcs = {}
    for s in skills:
        k = f"{s['source_emoji']} {s['source']}"
        srcs[k] = srcs.get(k, 0) + 1
    print(f"\n{C.BOLD}📦 Origens disponíveis:{C.RESET}\n")
    for src, n in sorted(srcs.items(), key=lambda x: -x[1]):
        print(f"  {src}  ({n} skills)")
    print()

def show_stats(skills):
    cats = {}
    srcs = {}
    for s in skills:
        cats[s['category']] = cats.get(s['category'], 0) + 1
        srcs[s['source']] = srcs.get(s['source'], 0) + 1
    
    print(f"\n{C.BOLD}📊 Estatísticas do Índice{C.RESET}\n")
    print(f"  Total de skills: {C.BOLD}{len(skills)}{C.RESET}")
    print(f"  Repositórios: {len(srcs)}")
    print(f"  Categorias: {len(cats)}")
    print(f"\n  {C.BOLD}Top 5 Categorias:{C.RESET}")
    for c, n in sorted(cats.items(), key=lambda x: -x[1])[:5]:
        bar = "█" * (n // 5)
        print(f"    {c}: {n} {C.DIM}{bar}{C.RESET}")
    print(f"\n  {C.BOLD}Por Origem:{C.RESET}")
    for src, n in sorted(srcs.items(), key=lambda x: -x[1]):
        print(f"    {src}: {n}")
    print()

def main():
    if not INDEX.exists():
        print(f"{C.RED}❌ Índice não encontrado em {INDEX}{C.RESET}")
        print("   Execute: python3 _extract_index.py")
        sys.exit(1)
    
    skills = load_index()
    args = sys.argv[1:]
    
    if not args:
        print(__doc__)
        show_stats(skills)
        sys.exit(0)
    
    if "--list-cats" in args:
        list_categories(skills)
        sys.exit(0)
    
    if "--list-sources" in args:
        list_sources(skills)
        sys.exit(0)
    
    if "--stats" in args:
        show_stats(skills)
        sys.exit(0)
    
    cat_filter = None
    src_filter = None
    show_install = False
    terms = []
    
    i = 0
    while i < len(args):
        if args[i] == "--cat" and i + 1 < len(args):
            cat_filter = args[i + 1]
            i += 2
        elif args[i] == "--src" and i + 1 < len(args):
            src_filter = args[i + 1]
            i += 2
        elif args[i] == "--install":
            show_install = True
            i += 1
        else:
            terms.append(args[i])
            i += 1
    
    term = " ".join(terms)
    results = search(skills, term, cat_filter, src_filter)
    
    if not results:
        print(f"\n{C.RED}❌ Nenhuma skill encontrada para: '{term}'{C.RESET}")
        if cat_filter:
            print(f"   Categoria: {cat_filter}")
        if src_filter:
            print(f"   Origem: {src_filter}")
        print(f"\n   Dica: tente termos mais genéricos ou use --list-cats / --list-sources\n")
        sys.exit(1)
    
    # Limit display
    max_show = 30
    showing = min(len(results), max_show)
    
    print(f"\n{C.BOLD}🔍 {len(results)} resultado(s) para '{term or '(todos)'}'{C.RESET}")
    if cat_filter:
        print(f"   Categoria: {cat_filter}")
    if src_filter:
        print(f"   Origem: {src_filter}")
    if len(results) > max_show:
        print(f"   {C.DIM}Mostrando {max_show} de {len(results)}. Refine sua busca.{C.RESET}")
    print()
    
    for s in results[:max_show]:
        print_result(s, show_install)

if __name__ == "__main__":
    main()
