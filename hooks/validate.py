#!/usr/bin/env python3
"""
OSForge Project Validation Script
Template — copie para .scripts/validate.py no seu projeto e customize.

Uso:
  python3 validate.py --quick     # tipos + lint
  python3 validate.py --full      # todos os checks
  python3 validate.py --domain types
  python3 validate.py --pre-deploy
"""

import subprocess
import sys
import json
import time
from pathlib import Path

# ─── Configuração padrão ────────────────────────────────────────────────────

DEFAULT_CONFIG = {
    "commands": {
        "types":    "bun tsc --noEmit",
        "lint":     "bun run lint",
        "tests":    "bun run test",
        "build":    "bun run build",
        "prisma":   "bun prisma validate",
        "security": "bun run lint --rule no-eval,no-implied-eval",
    },
    "quick":      ["types", "lint"],
    "full":       ["types", "lint", "tests", "build"],
    "pre_deploy": ["types", "lint", "tests", "build", "prisma"],
}


# ─── Cores ANSI ─────────────────────────────────────────────────────────────

GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
BLUE   = "\033[94m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

def ok(msg):    print(f"  {GREEN}✅ {msg}{RESET}")
def fail(msg):  print(f"  {RED}❌ {msg}{RESET}")
def info(msg):  print(f"  {BLUE}→  {msg}{RESET}")
def warn(msg):  print(f"  {YELLOW}⚠️  {msg}{RESET}")
def header(msg): print(f"\n{BOLD}{msg}{RESET}")

# ─── Carregar config do projeto ──────────────────────────────────────────────

def load_config():
    config_path = Path(".scripts/validate.config.json")
    if config_path.exists():
        with open(config_path) as f:
            user_config = json.load(f)
        config = DEFAULT_CONFIG.copy()
        config["commands"].update(user_config.get("commands", {}))
        for key in ["quick", "full", "pre_deploy"]:
            if key in user_config:
                config[key] = user_config[key]
        return config
    return DEFAULT_CONFIG

# ─── Executar um check ──────────────────────────────────────────────────────

def run_check(name, command, config):
    if name not in config["commands"]:
        warn(f"Comando '{name}' não encontrado na config — pulando")
        return True

    cmd = config["commands"][name]
    info(f"Executando: {cmd}")
    start = time.time()

    result = subprocess.run(
        cmd, shell=True, capture_output=True, text=True
    )
    elapsed = time.time() - start

    if result.returncode == 0:
        ok(f"{name} passou ({elapsed:.1f}s)")
        return True
    else:
        fail(f"{name} falhou ({elapsed:.1f}s)")
        if result.stdout.strip():
            print(f"\n{result.stdout.strip()[:800]}\n")
        if result.stderr.strip():
            print(f"\n{result.stderr.strip()[:800]}\n")
        return False


# ─── Runner principal ────────────────────────────────────────────────────────

def run_suite(suite_name, checks, config):
    header(f"OSForge Validation — {suite_name.upper()}")
    results = {}
    for check in checks:
        results[check] = run_check(check, config["commands"].get(check, ""), config)

    passed = sum(1 for v in results.values() if v)
    total  = len(results)

    print(f"\n{'─' * 40}")
    if passed == total:
        print(f"{GREEN}{BOLD}✅ {passed}/{total} checks passaram{RESET}")
    else:
        failed = [k for k, v in results.items() if not v]
        print(f"{RED}{BOLD}❌ {passed}/{total} passaram — falharam: {', '.join(failed)}{RESET}")

    return passed == total

# ─── CLI ────────────────────────────────────────────────────────────────────

def main():
    args = sys.argv[1:]
    config = load_config()

    if not args or "--help" in args:
        print(__doc__)
        print("\nDomínios disponíveis:", ", ".join(config["commands"].keys()))
        return

    if "--quick" in args:
        success = run_suite("Quick", config["quick"], config)
    elif "--full" in args:
        success = run_suite("Full", config["full"], config)
    elif "--pre-deploy" in args:
        success = run_suite("Pre-Deploy", config["pre_deploy"], config)
    elif "--domain" in args:
        idx = args.index("--domain")
        if idx + 1 >= len(args):
            print("Erro: --domain requer um nome de domínio")
            sys.exit(1)
        domain = args[idx + 1]
        success = run_suite(f"Domain: {domain}", [domain], config)
    else:
        print(f"Argumento desconhecido: {args}")
        print("Use --help para ver as opções")
        sys.exit(1)

    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
