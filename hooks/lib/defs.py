#!/usr/bin/env python3
"""
hooks/lib/defs.py — top-level definitions and callers, per language (B-035, SPEC-P04).

Used by hooks/quality-guard.py. Regex-based on purpose: a parser per language would be
slower than the 150 ms budget allows and would add dependencies. The cost is precision, and
that is what the shadow mode measures before anything reaches the model (ADR-019).

Scope (D-G1): TypeScript/JavaScript and Python only.
Python 3.8+ stdlib only. Every function is pure: no git, no filesystem.
"""
import re

CODE_EXT = (".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".py")

# Paths never treated as project code (vendored, generated, build output).
_SKIP_DIR = re.compile(
    r"(^|/)(node_modules|\.git|\.next|dist|build|out|coverage|vendor|venv|\.venv|"
    r"__pycache__|migrations|generated|__generated__)(/|$)")
_TEST_PATH = re.compile(
    r"(^|/)(__tests__|tests?|spec|e2e|fixtures)(/|$)|\.(test|spec)\.[cm]?[jt]sx?$|"
    r"(^|/)test_[^/]*\.py$|_test\.py$")

# Names that are conventions, not reusable helpers: never a "duplicate".
GENERIC = frozenset("""
get set post put patch delete head options handle handler handlers render run main init setup
default index app page layout loading error template config metadata viewport revalidate
dynamic runtime middleware generatemetadata generatestaticparams generateviewport
route routes props state store schema types type utils helpers constants client server
create update remove list find fetch load save parse format validate component provider
""".split())

# Next.js file conventions: their exports repeat across routes by design.
NEXT_FILES = frozenset(("page", "layout", "route", "loading", "error", "not-found",
                        "template", "default", "middleware", "global-error", "opengraph-image",
                        "twitter-image", "icon", "apple-icon", "sitemap", "robots", "manifest"))

_TS_DECL = re.compile(
    r"^[ \t]*export[ \t]+(?:default[ \t]+)?(?:declare[ \t]+)?(?:async[ \t]+)?"
    r"(?:function\*?|const|let|var|class|abstract[ \t]+class|interface|type|enum)[ \t]+"
    r"([A-Za-z_$][\w$]*)", re.M)
_TS_LIST = re.compile(r"^[ \t]*export[ \t]*(?:type[ \t]+)?\{([^}]*)\}", re.M)
_PY_DECL = re.compile(r"^(?:async[ \t]+)?(?:def|class)[ \t]+([A-Za-z]\w*)|^([A-Za-z]\w*)[ \t]*(?::[^=\n]+)?=(?!=)", re.M)


def is_code(path):
    p = (path or "").replace("\\", "/")
    return p.endswith(CODE_EXT) and not _SKIP_DIR.search(p)


def is_test(path):
    return bool(_TEST_PATH.search((path or "").replace("\\", "/")))


def lang(path):
    return "py" if (path or "").endswith(".py") else "ts"


def exported(text, language):
    """Exported top-level names in a file or fragment. Python: public top-level def/class/
    assignment (no leading underscore). TS/JS: `export` declarations and `export { a, b as c }`."""
    names = set()
    text = text or ""
    if language == "py":
        for m in _PY_DECL.finditer(text):
            n = m.group(1) or m.group(2)
            if n and not n.startswith("_") and n not in ("if", "else", "try", "with", "for", "while"):
                names.add(n)
        return names
    for m in _TS_DECL.finditer(text):
        names.add(m.group(1))
    for m in _TS_LIST.finditer(text):
        for part in m.group(1).split(","):
            part = part.strip()
            if not part:
                continue
            alias = re.split(r"\s+as\s+", part)
            n = alias[-1].strip()
            if re.match(r"^[A-Za-z_$][\w$]*$", n) and n != "default":
                names.add(n)
    return names


def normalize(name):
    return re.sub(r"[_\-]", "", (name or "").lower())


def is_generic(name):
    n = normalize(name)
    return len(n) < 4 or n in GENERIC


def is_next_convention(path):
    base = (path or "").replace("\\", "/").rsplit("/", 1)[-1]
    stem = base.split(".", 1)[0]
    return stem in NEXT_FILES


def call_regex(name):
    """A line that USES `name` as code: a call, a JSX element, or an import of it.
    `obj.name(` (a property) and the bare word inside a string or comment do not count."""
    n = re.escape(name)
    return re.compile(
        r"(?<![\w$.])" + n + r"\s*(?:<[^()]*>)?\s*\("      # name( or name<T>(
        r"|<" + n + r"[\s/>]"                               # <Name ...> JSX
        r"|^\s*import\b[^;]*\b" + n + r"\b"                 # import { name } / import name
        r"|^\s*from\s+\S+\s+import\b.*\b" + n + r"\b"       # python: from x import name
        r"|^\s*export\s*\{[^}]*\b" + n + r"\b[^}]*\}\s*from"  # re-export
    )


_COMMENT = re.compile(r"^\s*(//|#|\*|/\*)")
_IMPORT_LINE = re.compile(r"^\s*(import\b|from\s+\S+\s+import\b|export\s*(type\s*)?\{[^}]*\}\s*from\b)")


def caller_lines(name, grep_lines, own_path):
    """Filter `git grep -n` output (path:line:text) down to lines that call `name`, outside
    `own_path`. Returns [(path, line_no)]."""
    rx = call_regex(name)
    out = []
    for raw in grep_lines:
        parts = raw.split(":", 2)
        if len(parts) < 3:
            continue
        path, ln, text = parts
        if path == own_path or not is_code(path):
            continue
        if _COMMENT.match(text):
            continue
        if _defines(name, text):        # `function name(` / `def name(` is a definition, not a call
            continue
        # Strip string literals so `"formatPrice("` in a message does not count.
        stripped = re.sub(r"(['\"`])(?:\\.|(?!\1).)*\1", "''", text)
        if rx.search(stripped):
            try:
                is_import = bool(_IMPORT_LINE.match(stripped))
                out.append((path, int(ln), is_import))
            except ValueError:
                pass
    # One place per file: the first real call, else the import (an import alone still breaks).
    best = {}
    for path, ln, is_import in out:
        cur = best.get(path)
        if cur is None or (cur[1] and not is_import):
            best[path] = (ln, is_import)
    return sorted((p, v[0]) for p, v in best.items())


_DEF_KW = r"(?:export\s+(?:default\s+)?)?(?:declare\s+)?(?:async\s+)?(?:function\*?|const|let|var|class|abstract\s+class|interface|type|enum|def)\s+"


def _defines(name, text):
    return bool(re.search(r"(?:^|[\s;{(])" + _DEF_KW + re.escape(name) + r"(?![\w$])", text))


def def_pattern(name):
    """ERE for `git grep -iE`: a definition of `name` or its snake/camel spelling."""
    n = normalize(name)
    letters = "_?".join(re.escape(c) for c in n)
    return (r"(function\*?|const|let|var|class|interface|type|enum|def)[[:space:]]+"
            + letters + r"([^A-Za-z0-9_$]|$)")


def def_lines(name, grep_lines, own_path):
    """Definitions of `name` (normalised) in other code files: [(path, line_no, found_name)]."""
    want = normalize(name)
    # Top level only (column 0): a method or a local variable is not a reusable helper.
    rx = re.compile(r"^" + _DEF_KW + r"([A-Za-z_$][\w$]*)")
    out = []
    for raw in grep_lines:
        parts = raw.split(":", 2)
        if len(parts) < 3:
            continue
        path, ln, text = parts
        if path == own_path or not is_code(path) or is_test(path) or path.endswith(".d.ts"):
            continue
        if _COMMENT.match(text):
            continue
        m = rx.match(text)
        if m and normalize(m.group(1)) == want:
            try:
                out.append((path, int(ln), m.group(1)))
            except ValueError:
                pass
    return out
