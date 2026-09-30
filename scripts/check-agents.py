#!/usr/bin/env python3
"""
check-agents.py — validates agents/*.md frontmatter (B-009, ADR-015).

Why: 18 of 27 agents declared no `tools` (the planner "does NOT write code" but
inherited Write), `validator` used a schema Claude Code does not read, and the
tier policy in claude-code/CLAUDE.md lived in no frontmatter (audit E-A41).
Runs in the deploy preflight and in CI. Exit 1 on any error; warnings never fail.

Rules
  E1  frontmatter present; `name` and `description` present
  E2  `name` equals the file stem (agents/orchestrator/AGENT.md → orchestrator)
  E3  `tools`, when present, is a comma-separated scalar of known Claude Code tool
      names — never a YAML list or a nested allowed/denied block
  E4  `model`, when present, is one of: sonnet | opus | haiku | inherit
  E5  READ_ONLY roles declare `tools` and none of Write/Edit/MultiEdit/NotebookEdit
  W1  unknown frontmatter keys (warning only)
Usage: python3 scripts/check-agents.py [--quiet]
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KNOWN_TOOLS = {"Read", "Write", "Edit", "MultiEdit", "NotebookEdit", "Bash", "Grep", "Glob", "LS",
               "WebFetch", "WebSearch", "Task", "Agent", "Skill", "TodoWrite", "TodoRead"}
WRITE_TOOLS = {"Write", "Edit", "MultiEdit", "NotebookEdit"}
MODELS = {"sonnet", "opus", "haiku", "inherit"}
KNOWN_KEYS = {"name", "description", "tools", "model", "skills", "color", "role", "version",
              "always-active", "model-tier"}
# Roles whose body says they do not change code. Keep in sync with claude-code/CLAUDE.md §2.
READ_ONLY = {"planner", "code-reviewer", "security-auditor", "validator", "explorer-agent",
             "system-architect", "product-manager", "product-owner"}


def frontmatter(text):
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end < 0:
        return None
    fm, keys = {}, []
    for line in text[4:end].splitlines():
        m = re.match(r"^([A-Za-z_-]+):\s*(.*)$", line)
        if m:
            fm[m.group(1)] = m.group(2).strip()
            keys.append(m.group(1))
        elif line.startswith((" ", "\t", "-")) and keys:
            fm[keys[-1]] += "\n" + line   # continuation (block scalar or YAML list)
    return fm


def check(path):
    errors, warnings = [], []
    stem = "orchestrator" if path.endswith("orchestrator/AGENT.md") else os.path.splitext(os.path.basename(path))[0]
    fm = frontmatter(open(path, encoding="utf-8").read())
    if fm is None:
        return [f"E1 no frontmatter"], warnings
    for k in ("name", "description"):
        if not fm.get(k):
            errors.append(f"E1 missing `{k}`")
    if fm.get("name") and fm["name"] != stem:
        errors.append(f"E2 name `{fm['name']}` != file stem `{stem}`")
    tools = fm.get("tools")
    tool_set = set()
    if tools is not None:
        if "\n" in tools or tools == "":
            errors.append("E3 `tools` must be a comma-separated scalar (got a YAML block)")
        else:
            tool_set = {t.strip() for t in tools.split(",") if t.strip()}
            unknown = tool_set - KNOWN_TOOLS
            if unknown:
                errors.append(f"E3 unknown tool names: {sorted(unknown)}")
    model = fm.get("model")
    if model is not None and model not in MODELS:
        errors.append(f"E4 model `{model}` not in {sorted(MODELS)}")
    if stem in READ_ONLY:
        if tools is None:
            errors.append("E5 read-only role must declare `tools` (otherwise it inherits Write/Edit)")
        elif tool_set & WRITE_TOOLS:
            errors.append(f"E5 read-only role declares write tools: {sorted(tool_set & WRITE_TOOLS)}")
    for k in fm:
        if k not in KNOWN_KEYS:
            warnings.append(f"W1 unknown key `{k}`")
    return errors, warnings


def main():
    quiet = "--quiet" in sys.argv
    files = sorted(
        [os.path.join(ROOT, "agents", f) for f in os.listdir(os.path.join(ROOT, "agents")) if f.endswith(".md")]
        + [os.path.join(ROOT, "agents", "orchestrator", "AGENT.md")]
    )
    total_err = 0
    for f in files:
        errors, warnings = check(f)
        rel = os.path.relpath(f, ROOT)
        for e in errors:
            print(f"  ❌ {rel}: {e}")
        for w in warnings:
            if not quiet:
                print(f"  ⚠️  {rel}: {w}")
        total_err += len(errors)
    print(f"check-agents: {len(files)} agents, {total_err} error(s)")
    sys.exit(1 if total_err else 0)


if __name__ == "__main__":
    main()
