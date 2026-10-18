## AI-default tells (count; lower is better)

Also return `tells_present`: the list of ids below that are clearly present in the delivered page
(empty list if none, or if no page was delivered). Count a tell only when it is actually in the
markup/classes/copy, not when it is merely mentioned in prose.

- `T1_cream_bg`: the page or main section background is cream / beige / warm off-white (e.g.
  stone-50, amber-50, #FAF7F2, #F5F1EA) where the brief did not ask for it.
- `T2_italic_accent`: one word or phrase of the headline is set apart in italic and/or a different
  (usually serif) font or color as a decorative accent.
- `T3_numbered_labels`: decorative numbered section/step labels like "01", "02", "03" (or "01 /").
- `T4_mono_eyebrow`: small uppercase monospace (or tracking-widest) eyebrow/kicker labels above headings.
- `T5_pill_everywhere`: every button/CTA (and typically badges) is fully rounded (`rounded-full`).
- `T6_purple_or_neon`: purple/violet palette or dark background with neon glow, not from the brief.
- `T7_gradient_blobs`: mesh/aurora gradient blobs, blurred colored orbs, or glow effects as decoration.
- `T8_glass`: glassmorphism (translucent backdrop-blur cards/panels) as a main visual device.
- `T9_bento`: bento-grid card mosaic used for content that does not need a grid.
- `T10_ai_copy`: generic AI marketing copy written by the assistant (e.g. "empower", "seamless",
  "unlock", "supercharge", "revolutionize", "orchestrate", "elevate") in text the brief did not supply.
