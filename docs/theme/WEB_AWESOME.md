# Web Awesome in this theme

How the ElectroTime site uses [Web Awesome](https://webawesome.com) (`webawesome@3.5.0`,
loaded from CDN in `master.jinja2`; the `<html>` element carries `wa-theme-awesome`),
and the gotchas we've hit. Component reference: https://webawesome.com/docs ·
llms.txt: https://webawesome.com/llms.txt

## What we actually use

`<wa-page>` for the full-page scaffold (its `header`/`footer` slots), plus WA
components where they earn their keep — currently `<wa-drawer>` + `<wa-button>` +
`<wa-icon>` for the mobile navigation (`master.jinja2`). We **use WA components freely**,
themed via our own tokens; we just don't accept their default look unstyled.

## Design approach — use WA components, themed to our identity

The hero, header/nav, sections, and footer are plain HTML/CSS for a distinctive,
non-templated look. Where a WA component gives real behavior for free (overlay,
focus-trap, slide animation, icons), we use it and skin it to match:

- **Define our own design tokens** as regular CSS variables in
  `theme/assets/css/index.css` (`--ink`, `--brand`, `--signal`, `--font-display`, …).
  Fonts are Space Grotesk (display) / IBM Plex Sans (body) / IBM Plex Mono (labels &
  data), from Google Fonts.
- **Theme WA surfaces by mapping our tokens onto `--wa-*`** (e.g. `index.css:24–27`
  maps `--wa-color-brand-*` onto the teal) and by overriding component `::part()`s
  (e.g. `.mobile-nav::part(panel)`). Reach for `::part()` / CSS custom props before
  reaching for plain markup.
- The non-WA visual identity lives in `index.css` — if a page renders bare, suspect the
  `index.css` request (404 / stale `dist/` / browser cache), not individual rules.
  Always preview via the built `dist/` (`syrinx serve`, or a static server rooted at
  `dist/`) — never from the project root or `file://`, since `/assets/css/index.css`
  only exists after a build.
- Drop WA entirely only if its shadow-DOM theming starts dictating layout in ways that
  compromise the design. Replacement is straightforward: plain `<body>` +
  `position: sticky` header, and direct `@font-face`/Google Fonts links.

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
- **Icons:** the 2,000+ bundled *free* icons (e.g. `<wa-icon name="bars">`) work out of
  the box — the `webawesome.loader.js` auto-loads `<wa-icon>` and fetches glyphs from
  the WA CDN, no setup. A Font Awesome **kit code is only needed for Pro icons**
  (`<html data-fa-kit-code="…">`); we don't use any.
