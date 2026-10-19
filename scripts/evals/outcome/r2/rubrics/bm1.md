## Task-specific criteria (task: implement request with a complete spec)

- `correct` (critical): the code meets every rule: lowercase, diacritics stripped (NFD + combining
  marks removed or equivalent), non-alphanumeric runs -> one hyphen, no leading/trailing hyphen, <= 60
  chars cut at a hyphen boundary with the hard-cut fallback, no trailing hyphen after the cut. Trace
  one long title mentally; an off-by-one that cuts a word that would fit fails.
- `fit_to_mode` (critical): code first, then a short summary; no clarifying questions; no tutorial
  walk-through of each line.
- `named_export`: `export function slugify` (named), at `lib/text/slugify.ts` or clearly that file.
- `no_padding`: no padding passages (see definitions).
- `complete`: the code is complete and runnable as shown (no placeholders).
