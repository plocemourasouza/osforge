Mode: IMPLEMENT. Expected shape: the code first, then a short summary; no clarifying questions (the
spec is complete), no tutorial.
Correct implementation (one possibility): `normalize("NFD")` + strip `\p{M}` / U+0300–U+036F,
lowercase, replace `/[^a-z0-9]+/g` with "-", trim hyphens; if length > 60, cut at the last hyphen at or
before index 60 (i.e. take `s.slice(0, 61)` and cut at its last "-", or equivalent), falling back to
a hard cut at 60 when there is no hyphen in the first 60 characters; ensure no trailing hyphen after
the cut. Off-by-one at the boundary: a slug whose 61st character is "-" can be cut exactly at 60.
Named export (no default export). Tests are welcome but not required.
