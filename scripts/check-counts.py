#!/usr/bin/env python3
"""
check-counts.py — numbers quoted in always-loaded and user-facing docs must match the tree
(B-008, ADR-015 §4). The audit found "~64 core" vs 47, "auto" vs "true", "8 hooks" vs 9,
"770+ skills", "8 MCP servers" vs 1 (E-A35–E-A37, §4.4). Exit 1 on any mismatch.

Each rule: (file, regex with one capture group, expected value, label). A rule whose regex
is not found at all also fails — the sentence is part of the contract, so drift by deletion
is caught too. Usage: python3 scripts/check-counts.py
"""
import glob, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

skills = len([p for p in glob.glob("skills/**/SKILL.md", recursive=True) if "/_" not in p])
core = len([l for l in open("claude-code/skills-core.txt", encoding="utf-8") if l.strip() and not l.startswith("#")])
agents = len(glob.glob("agents/*.md")) + (1 if os.path.exists("agents/orchestrator/AGENT.md") else 0)
rules = len([f for f in os.listdir("rules") if f.endswith((".md", ".mdc"))])
rules_mdc = len([f for f in os.listdir("rules") if f.endswith(".mdc")])
rules_always = rules - sum(1 for f in os.listdir("rules") if f.endswith(".mdc")
                           and "alwaysApply: false" in open(os.path.join("rules", f), encoding="utf-8").read())
spec_cmds = len(glob.glob("commands/spec-*.md"))
hooks_json = json.load(open("hooks/hooks-claude-code.json", encoding="utf-8"))["hooks"]
hook_scripts = {os.path.basename(h["command"].split()[-1]) for arr in hooks_json.values() for e in arr for h in e["hooks"]}
hooks = len(hook_scripts)
mcps = len(json.load(open("mcp/claude-code.json", encoding="utf-8")).get("mcpServers", {}))
tool_search = json.load(open("claude-code/settings-base.json", encoding="utf-8")).get("env", {}).get("ENABLE_TOOL_SEARCH", "")

RULES = [
    ("README.md", r"(\d+) specialized agents", agents, "agents"),
    ("README.md", r"(\d+) on-demand skills", skills, "skills"),
    ("README.md", r"(\d+) rules \(Cursor: \d+ always-on", rules, "rules"),
    ("README.md", r"\d+ rules \(Cursor: (\d+) always-on", rules_always, "always-on rules"),
    ("README.md", r"(\d+) spec commands", spec_cmds, "spec commands"),
    ("README.md", r"\*\*MCP servers\*\* — (\d+) global", mcps, "global MCPs"),
    ("CLAUDE.md", r"\*\*(\d+) skills, \d+ agents\*\*", skills, "skills"),
    ("CLAUDE.md", r"\*\*\d+ skills, (\d+) agents\*\*", agents, "agents"),
    ("CLAUDE.md", r"\*\*(\d+) rules \(deployed to Cursor\)", rules, "rules"),
    ("CLAUDE.md", r"(\d+) global MCP server", mcps, "global MCPs"),
    ("CLAUDE.md", r"\*\*, (\d+) hooks,", hooks, "hooks"),
    ("claude-code/CLAUDE.md", r"OSForge ships \*\*(\d+) skills\*\*", skills, "skills"),
    ("claude-code/CLAUDE.md", r"\*\*(\d+) agents\*\* \(orchestrator", agents, "agents"),
    ("claude-code/CLAUDE.md", r"\*\*(\d+)\*\* \*\*rules\*\* \(Cursor only; \d+ always-on", rules, "rules"),
    ("claude-code/CLAUDE.md", r"\*\*\d+\*\* \*\*rules\*\* \(Cursor only; (\d+) always-on", rules_always, "always-on rules"),
    ("claude-code/CLAUDE.md", r"the (\d+) core skills in `~/\.claude/skills/`", core, "core skills"),
    ("claude-code/CLAUDE.md", r"`env\.ENABLE_TOOL_SEARCH=(\w+)`", tool_search, "ENABLE_TOOL_SEARCH"),
    ("claude-code/CLAUDE.md", r"`@SKILLS\.md`, (\d+) skills\)", skills, "skills"),
    ("USAGE.md", r"índice de triggers das (\d+) skills", skills, "skills"),
    ("USAGE.md", r"Syncs (\d+) agents \(orchestrator", agents, "agents"),
    ("USAGE.md", r"Installs (\d+) hooks to", hooks, "hooks"),
    ("USAGE.md", r"Copies (\d+) `spec-\*` commands", spec_cmds, "spec commands"),
    ("USAGE.md", r"Copies (\d+) rules \(\d+ `\.mdc`", rules, "rules"),
    ("USAGE.md", r"Copies \d+ rules \((\d+) `\.mdc`", rules_mdc, "mdc rules"),
    ("USAGE.md", r"What each hook does \((\d+) hooks\)", hooks, "hooks"),
]

fails = 0
for path, rx, expected, label in RULES:
    text = open(path, encoding="utf-8").read()
    m = re.search(rx, text)
    if not m:
        print(f"  ❌ {path}: sentence for {label} not found (regex {rx!r})"); fails += 1; continue
    got = m.group(1)
    if str(got) != str(expected):
        print(f"  ❌ {path}: {label} says {got}, tree has {expected}"); fails += 1
banned = [("rules/agent-skills-reference.mdc", r"770"), ("scripts/_generate_index_md.py", r"\b770\b"),
          ("claude-code/CLAUDE.md", r"~64 core"), ("CLAUDE.md", r"no build, lint, or test suite")]
for path, rx in banned:
    if re.search(rx, open(path, encoding="utf-8").read()):
        print(f"  ❌ {path}: stale text matches {rx!r}"); fails += 1
print(f"check-counts: skills={skills} core={core} agents={agents} rules={rules} spec={spec_cmds} hooks={hooks} mcps={mcps} tool_search={tool_search} → {fails} mismatch(es)")
sys.exit(1 if fails else 0)
