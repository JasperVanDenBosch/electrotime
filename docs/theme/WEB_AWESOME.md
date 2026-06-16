# Web Awesome in this theme

How the ElectroTime site uses [Web Awesome](https://webawesome.com) (`webawesome@3.5.0`,
loaded from CDN in `master.jinja2`; the `<html>` element carries `wa-theme-awesome`),
and the gotchas we've hit. Component reference: https://webawesome.com/docs ·
llms.txt: https://webawesome.com/llms.txt

## What we actually use

**Only `<wa-page>`** — the full-page scaffold, for its `header` and `footer` slots.
Nothing else. The old `<wa-card>` sections, `<wa-format-date>`, and the
`wa-split`/`wa-cluster`/`wa-stack` utility classes were all replaced by custom CSS.

## Design approach — keep WA, but don't lean on its visual components

The hero, header/nav, sections, and footer are all plain HTML/CSS. To keep a
distinctive, non-templated look without locking into WA:

- Use `<wa-page>` for its `header`/`footer` slot scaffold — convenient and frictionless.
- **Avoid WA's visual components** (e.g. `<wa-card appearance="outlined">`) where they
  impose a generic boxy look; prefer plain semantic markup styled directly.
- **Define our own design tokens** as regular CSS variables in
  `theme/assets/css/index.css` (`--ink`, `--brand`, `--signal`, `--font-display`, …),
  *not* `--wa-*`, so the identity is ours and portable. Fonts are Space Grotesk
  (display) / IBM Plex Sans (body) / IBM Plex Mono (labels & data), from Google Fonts.
- The visual identity now lives **entirely** in `index.css` — there is **no Web Awesome
  styling fallback**. If a page renders bare, suspect the `index.css` request
  (404 / stale `dist/` / browser cache), not individual rules. Always preview via the
  built `dist/` (`syrinx serve`, or a static server rooted at `dist/`) — never from the
  project root or `file://`, since `/assets/css/index.css` only exists after a build.
- Drop WA entirely only if the sticky header/footer slot or shadow-DOM theming starts
  dictating layout in ways that compromise the design. Replacement is straightforward:
  plain `<body>` + `position: sticky` header, and direct `@font-face`/Google Fonts links.

## Gotchas

- **WA's base stylesheet pads the semantic landmarks.** `<main>` gets ~48px top/bottom
  padding and `<header>`/`<footer>` get padding too (this is what made the header render
  ~97px tall and put a large gap between the header and the hero). Our layout is
  full-bleed with its own inner spacing, so we reset them in `index.css`:
  `main { padding: 0 } .site-header { padding: 0 } .site-footer { padding: 0 }`. The
  header height is then driven by `.site-header-inner { min-height: var(--header-h) }`
  (64px) and the logo size by `.site-logo { height: 38px }`.
- **`wa-page` scrolls the window normally** — it does *not* use an internal scroll
  container. The sticky header is a plain `position: sticky; top: 0` rule on
  `.site-header` (verified pinned on scroll), not a WA feature.
- **Icons** require a Font Awesome kit code — currently a scaffold placeholder
  (`[[ scaffold.fa_kit_code ]]`) in the loader script `src`.
