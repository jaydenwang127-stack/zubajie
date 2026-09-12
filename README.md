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
Live at https://jaydenwang127-stack.github.io/zubajie/ (GitHub Pages, repo `jaydenwang127-stack/zubajie`). `main` holds the source; the `gh-pages` branch holds the contents of `site/` and is what Pages serves.

After any change:
```
./deploy.sh
```
That rebuilds, commits, pushes `main`, and force-pushes `site/` to `gh-pages`. Pages updates in about a minute.

If the site moves to its own domain, change `BASE_URL` at the top of `build_site.py` and run `./deploy.sh` again so the `hreflang` tags and `sitemap.xml` follow.

## Pending owner input (site shows placeholders until then)
- **The shop moved.** Address, hours and the 如何前往 route come from the Google listing and a customer review (`docs/05-google-listing.md`), not from the owner yet.
- Entrance photo: save one as `prototype/photos/entrance.jpg` and rebuild; the Find-us page picks it up.
- Policy page: six headings, each "待與老闆確認 / to be confirmed with the owner".
- 29 items carry a visible price-conflict note (`conf` in items.json).
- Footer note says prices are carried over from the old site pending confirmation. Remove `foot_note` from `T` in `build_site.py` once confirmed.
- 21 EN gear terms still flagged CHECK in the inventory sheet (marked with an HTML comment on those product pages).
