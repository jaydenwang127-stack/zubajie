# 租八借 website rebuild

Goodwill rebuild of dbk.url.tw, a one-man outdoor gear rental shop in Beitou, Taipei (owner 楊世銘, 02-2823-0080, 東華街二段210號, 4 min from MRT 唭哩岸). Bilingual ZH/EN. Elaine does not read Chinese: every ZH string must have its EN twin beside it in code and in any summary you give her.

## Scope (gated, do not creep)
Phase 1 only: static bilingual site on free hosting (his account, Elaine as collaborator). No forms, no booking, no CMS. Phase 2 and 3 exist only if the owner asks.

## Source of truth
- `data/items.json`: 131 items scraped verbatim from the old site (5 price tiers: sale, d2 = 兩天一夜, add = 每加一日, d5 = 五至十天, mo = 月租). `conf` non-empty means the old site listed two different prices; keep the flag visible on the product page until the owner confirms.
- `data/photomap.json`: old-site image filename → `photos/pNN.jpg`.
- `prototype/`: the approved single-file prototype (hash router) and its Python generator. Copy is the look and structure to reproduce as real pages. `photos/` are the owner's images pulled from his site, 240px thumbs plus 8 larger ones (`bigNN.jpg`).
- `docs/`: research notes 01–04 from the Cowork sessions.

## Build target
Plain static HTML/CSS, no framework, no build step the owner could break. Structure:
```
index.html            en/index.html
rent/camping.html     en/rent/camping.html   (mountain, river, water, other)
rent/item/CA-012.html en/rent/item/CA-012.html   (one per item, generated)
policy.html           en/policy.html
contact.html          en/contact.html
photos/               shared
```
Language switch links to the same page's translation, never the homepage. Generate the item pages with a small Python script from `data/items.json`; commit the output so hosting is just files.

## Design (Direction A, chosen)
Colours: bg #F1F2EA, green #1E3A2B, ink #1B241E, blue #2F6F8F, rule #D6DACB. Noto Serif TC for headings, Noto Sans TC body. Plain headings, no slogans, no eyebrow labels. Product card = photo, name, spec on its own line underneath, then the 2D1N price.

## Rules
- Never invent prices, policy text, or facts about the shop. Policy content is "待與老闆確認 / to be confirmed with the owner" until he supplies it.
- Do not publish the owner's postal bank account number anywhere.
- Keep the mobile call bar and the hours in the top fold.
- Elaine reviews on her phone first. Deploy previews must work at 390px.

## Build (added 2026-09-12)
`python3 build_site.py` regenerates `site/` (the hostable output) from `data/`. No JS on the site: mobile menu is a `<details>`, desktop dropdown is CSS hover, language switch is a plain link to the twin page. Keep all UI copy in the `T` dict as `(zh, en)` pairs.
