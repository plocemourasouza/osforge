#!/usr/bin/env python3
"""
archify-presentation.py — derive a PRESENTATION variant from a delivered Archify artifact.

Why this exists
---------------
The delivered HTML is the receipt copy: `deliver` hashed it, and the Archify
contract says never edit it afterwards. But a review deck or a README wants a
softer look than the engine's mono-forward instrument style: a friendlier
sans-serif, rounder corners, translucent cards. This script writes a SEPARATE
file (`<name>.presentation.html`) with a CSS override injected, and stamps it
with the sha256 of the artifact it derives from, so nobody mistakes it for
the receipt copy. The JSON source and the delivered HTML stay untouched.

Glow, transparency and motion do not need this script: they are the engine's
own `meta.visual_preset: "signal-flow"` + `meta.animation: "trace"`, and the
viewer's Flow/Blueprint/Editorial switch works at runtime on every artifact.

Usage
-----
    python3 scripts/archify-presentation.py <delivered.html> [--font "Inter, system-ui, sans-serif"] [--out <path>]

Exit 1 if the input does not look like an Archify artifact (no </head>).
"""
import argparse
import hashlib
import sys
from pathlib import Path

DEFAULT_FONT = "'Inter', 'SF Pro Text', system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', sans-serif"

TEMPLATE = """
<!-- OSForge presentation variant. Derived from a delivered Archify artifact
     (sha256 {sha}). This file is NOT the receipt copy: the verified artifact
     is the sibling without the .presentation suffix. -->
<style id="osforge-presentation-theme">
  :root {{ --osf-font: {font}; }}
  body, svg, .card, .header, button, input {{ font-family: var(--osf-font) !important; letter-spacing: 0 !important; }}
  svg text {{ font-weight: 500; }}
  .card {{ border-radius: 16px; backdrop-filter: blur(10px); }}
  svg rect {{ rx: 14px; ry: 14px; }}
</style>
"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("html", type=Path)
    ap.add_argument("--font", default=DEFAULT_FONT)
    ap.add_argument("--out", type=Path)
    a = ap.parse_args()

    raw = a.html.read_bytes()
    text = raw.decode("utf-8")
    if "</head>" not in text:
        print("error: no </head> — not an Archify artifact?", file=sys.stderr)
        return 1
    sha = hashlib.sha256(raw).hexdigest()
    out = a.out or a.html.with_name(a.html.stem + ".presentation.html")
    block = TEMPLATE.format(sha=sha, font=a.font)
    out.write_text(text.replace("</head>", block + "</head>", 1), encoding="utf-8")
    print(f"{out}  (derived from sha256 {sha[:12]}…; not a receipt)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
