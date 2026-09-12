# 租八借 website rebuild — Phase 1

See CLAUDE.md for the brief and rules.

## What is where
- `site/` — the finished static site. **This folder is what gets hosted.** 280 pages: 131 items × 2 languages, plus home, 5 category pages, policy, contact and 404 in each language. One CSS file, no JavaScript.
- `build_site.py` — regenerates `site/` from `data/items.json` + `data/photomap.json`. Every UI string in it is a `(zh, en)` pair.
- `data/` — source of truth for items and photo mapping.
- `prototype/` — the approved single-file prototype the site reproduces.
- `docs/` — research notes 01–04.

## Rebuild after editing data or copy
```
python3 build_site.py
```
Python 3.9+, no dependencies. It wipes and rewrites `site/`.

## Preview locally
```
python3 -m http.server 8000 --directory site
```
Then open http://localhost:8000/ (Chinese) or http://localhost:8000/en/ (English).

## Deploy
Upload the contents of `site/` to any static host (GitHub Pages, Netlify, Cloudflare Pages). All links are relative, so it also works from a sub-path. Once the site has a domain, set `BASE_URL` at the top of `build_site.py` and rebuild: that adds `hreflang` alternates and `sitemap.xml`.

## Pending owner input (site shows placeholders until then)
- Policy page: six headings, each "待與老闆確認 / to be confirmed with the owner".
- 29 items carry a visible price-conflict note (`conf` in items.json).
- Footer note says prices are carried over from the old site pending confirmation. Remove `foot_note` from `T` in `build_site.py` once confirmed.
- 21 EN gear terms still flagged CHECK in the inventory sheet (marked with an HTML comment on those product pages).
