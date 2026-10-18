## Task-specific criteria (task: dental clinic app pricing section)

Ground truth for annual billing ("2 months free"): annual = 10 x monthly -> Consultório R$ 1.490/ano
(≈ R$ 124,17/mês), Clínica R$ 2.990/ano (≈ R$ 249,17/mês); Rede stays "Sob consulta". Rounded
displays like "R$ 124/mês" are acceptable.

- `markup_valid` (critical): one complete HTML document in a single ```html block, includes the
  Tailwind CDN script, no truncation, no obviously broken structure.
- `plans_exact`: the three plans with exact names, prices and listed features; nothing invented
  that contradicts the brief.
- `recommended`: "Clínica" is visually marked as the recommended plan.
- `toggle_works`: a monthly/annual toggle exists, its script plausibly works, and the annual prices
  are arithmetically consistent with "2 months free" (see ground truth). Wrong math fails.
- `brand`: teal #0E7490 primary, coral #F97362 used sparingly as accent; Nunito Sans loaded and applied.
- `faq`: an FAQ with 3 questions below the plans, in pt-BR.
- `tone_fit`: friendly, calm, non-technical copy suitable for dentists.
- `accessible`: toggle is keyboard-operable and labelled (button/aria-pressed/role=switch or
  radio group), visible focus styles, lang="pt-BR", contrast plausibly AA.
- `responsive`: plans stack on mobile.
