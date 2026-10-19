## Task-specific criteria (task: fleet-tracking dashboard empty state)

- `markup_valid` (critical): one complete HTML document in a single ```html block, includes the
  Tailwind CDN script, no truncation, no obviously broken structure.
- `shell`: sidebar with the five items (Dashboard, Veículos, Motoristas, Relatórios, Configurações)
  and top bar with "Transportes Andrade" and an "MA" avatar.
- `actions`: primary "Conectar primeiro veículo", secondary "Importar planilha de frota", and the
  link "Ver como funciona (2 min)", with a clear visual hierarchy (one primary).
- `explains_value`: one or two lines explaining what appears once a vehicle is connected (live map,
  trip history, fuel alerts).
- `is_empty`: the main area is a genuine empty state (no fake vehicle data, fake charts or metrics
  presented as real).
- `brand`: primary #1D4ED8 and neutral grays; Inter loaded/applied.
- `responsive`: the sidebar collapses (hidden/drawer/toggle) on mobile.
- `accessible`: semantic nav/main, current page indicated (aria-current or equivalent), visible
  focus styles, lang="pt-BR", contrast plausibly AA.
