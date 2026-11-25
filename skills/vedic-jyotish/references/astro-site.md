# Publishing readings as an Astro website (from the astro-framework skill)

Only use when the user wants a **website or web report** (not a PDF). Astro suits this: readings are mostly static content.

Recommended structure:
```
src/content.config.ts          # collection of readings (glob loader over data/readings/*.json)
data/readings/<slug>.json      # output of scripts/jyotish.py + numerology.py + your prose
src/pages/readings/[slug].astro
src/components/SouthIndianChart.astro   # static SVG, no JS
src/components/DashaTimeline.astro      # static; hydrate (client:visible) only if interactive
```
Rules:
- Output mode: `static` unless the site has live forms; if users enter birth data on the site, use `hybrid` with a server endpoint/action that calls the Python engine or the VedAstro API. Never compute ephemeris in the browser.
- Content Layer (Astro 5+): `defineCollection({ loader: glob({ pattern: '**/*.json', base: './data/readings' }), schema: z.object({...}) })` and validate fields (name, ascendant, planets, dasha, prose sections).
- Default to zero client JS. Use `client:visible` for charts that animate, `client:idle` for small widgets; never `client:load` for below-the-fold content.
- Personalised snippets on cached pages (e.g. "current dasha today") -> server island: `<Dasha server:defer />` with a fallback slot.
- i18n routing for Hindi/English readings (`i18n` config, `/hi/...`).
- Treat birth data as personal data: no analytics on reading pages, no sharing of URLs with names in them, `noindex` meta by default.
- Reuse the reading prose rules in SKILL.md (ethics, confidence flags, disclaimer) in every page template.
Not for: Next.js/Remix/SvelteKit-style full SPAs.
