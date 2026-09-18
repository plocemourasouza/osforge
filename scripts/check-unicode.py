#!/usr/bin/env python3
"""
check-unicode.py — invisible / bidi / tag code points in curated text (R-16, B-024).

OSForge vendors 13 upstream skill collections under sources/ and copies curated skills into
every session's context. A zero-width or Unicode-Tag character inside a SKILL.md is read by the
model and invisible to the reviewer — the canonical "ASCII smuggling" prompt-injection vector.
This script fails when any such code point appears in the files it is pointed at.

Ranges: the set ECC's scripts/ci/check-unicode-safety.js uses (MIT, © 2026 Affaan Mustafa; see
THIRD_PARTY_NOTICES) — zero-width space/joiners, word joiner, BOM (not at file start), bidi
embeddings/overrides/isolates, variation selectors, the Tag block U+E0000–E007F, Mongolian vowel
separator, Hangul fillers, invisible math operators.

Usage:  scripts/check-unicode.py [PATH ...]      (default: skills agents rules claude-code docs hooks scripts)
        scripts/check-unicode.py --sources        (also walk sources/, which is disk-only and large)
        scripts/check-unicode.py --fix FILE ...   (strip the code points in place; prints what changed)
Exit 0 when clean, 1 when any file has a hit. Text files only (by extension); binary skipped.
"""
import os
import sys

TEXT_EXT = {".md", ".mdc", ".txt", ".json", ".yaml", ".yml", ".toml", ".py", ".sh", ".ts", ".js",
            ".tsx", ".jsx", ".html", ".css", ".tsv", ".csv", ".prisma", ".sql", ".mjs", ".cjs", ""}
DEFAULT_ROOTS = ["skills", "agents", "rules", "claude-code", "docs", "hooks", "scripts", "commands", "mcp"]
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".osforge", "outputs", "_deprecated"}


def is_dangerous(cp: int) -> bool:
    return (
        0x200B <= cp <= 0x200D or cp == 0x2060 or cp == 0xFEFF
        or 0x202A <= cp <= 0x202E or 0x2066 <= cp <= 0x2069
        or 0xFE00 <= cp <= 0xFE0F or 0xE0100 <= cp <= 0xE01EF
        or 0xE0000 <= cp <= 0xE007F
        or cp == 0x180E or cp == 0x115F or cp == 0x1160
        or 0x2061 <= cp <= 0x2064 or cp == 0x3164
    )


def _tolerated(text: str, i: int, cp: int) -> bool:
    """Legitimate uses of otherwise-flagged code points: a BOM at offset 0, and the emoji
    presentation selectors U+FE0E/U+FE0F right after a pictograph (⚠️ is U+26A0 U+FE0F —
    181 of them live in this repo's docs). A selector after ASCII stays flagged."""
    if i == 0 and cp == 0xFEFF:
        return True
    if cp in (0xFE0E, 0xFE0F) and i > 0 and ord(text[i - 1]) >= 0x2000:
        return True
    if cp == 0xFE0F and i + 1 < len(text) and ord(text[i + 1]) == 0x20E3:   # keycap: 1️⃣ = "1" FE0F 20E3
        return True
    if cp == 0x200D and 0 < i < len(text) - 1 and ord(text[i - 1]) >= 0x2000 and ord(text[i + 1]) >= 0x2000:
        return True                                    # ZWJ sequence: 👨‍👩‍👧 (found in sources/ Swift grapheme example)
    return False


def scan_text(text: str):
    """Yield (line, col, codepoint) for every dangerous code point (see _tolerated)."""
    line, col = 1, 0
    for i, ch in enumerate(text):
        cp = ord(ch)
        if ch == "\n":
            line += 1; col = 0
            continue
        col += 1
        if is_dangerous(cp) and not _tolerated(text, i, cp):
            yield line, col, cp


def iter_files(roots):
    for root in roots:
        if os.path.isfile(root):
            yield root; continue
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            for f in filenames:
                if os.path.splitext(f)[1].lower() in TEXT_EXT:
                    yield os.path.join(dirpath, f)


def main(argv):
    fix = "--fix" in argv
    sources = "--sources" in argv
    roots = [a for a in argv if not a.startswith("--")]
    if not roots:
        roots = [r for r in DEFAULT_ROOTS if os.path.exists(r)] + (["sources"] if sources and os.path.isdir("sources") else [])
    hits = 0; files = 0
    for path in iter_files(roots):
        try:
            with open(path, encoding="utf-8", errors="strict") as fh:
                text = fh.read()
        except (OSError, UnicodeDecodeError):
            continue
        files += 1
        found = list(scan_text(text))
        if not found:
            continue
        hits += len(found)
        for line, col, cp in found[:5]:
            print(f"  ❌ {path}:{line}:{col} U+{cp:04X}")
        if len(found) > 5:
            print(f"     … +{len(found) - 5} em {path}")
        if fix:
            cleaned = "".join(ch for i, ch in enumerate(text) if not (is_dangerous(ord(ch)) and not _tolerated(text, i, ord(ch))))
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(cleaned)
            print(f"  🧹 {path}: {len(found)} code point(s) removido(s)")
    print(f"check-unicode: {files} arquivos, {hits} code point(s) invisível(is)" + (" (corrigidos)" if fix and hits else ""))
    return 1 if (hits and not fix) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
