# Step 3: design directions (2026-09-11), updated 2026-09-12 with copy pass

## Current: one site prototype (Direction A)
Elaine rejected three single-scroll pages as cluttered ("should flow like a normal website"). Rebuilt as a multi-page prototype in Direction A's palette (forest green, lichen, river blue, Noto Serif TC headings).

Prototype: https://claude.ai/code/artifact/feef0875-7a81-491d-952d-53c7bac7caea (same file as prototype/zubajie-site.html)

Structure: Home (hero with three of his photos, five category cards, 如何租借 three steps, hours, location) · 租借裝備 dropdown → five category pages (露營 49 / 登山 44 / 溯溪 16 / 水上 9 / 其他 13) · product page per item (photo, name, spec on its own line, five rate rows, call button; items with cross-page conflicts carry a note) · 租借規則 (six headings, content pending owner) · 聯絡我們. 中文/EN toggle on every page. Mobile: hamburger drawer plus sticky call bar. Desktop: dropdown nav plus phone number in header.

Copy rules Elaine set (2026-09-12): plain headings, no slogans. Hero is 北投戶外裝備出租 / Outdoor gear rental in Beitou. Section headings are 租借裝備 / 如何租借 / 營業時間 / 店面位置. No eyebrow labels. Reference: LowerGear's headline is "Nationwide Gear Rentals"; Yamarent's nav says "How to Rent".

Product cards: photo, name, spec underneath in muted small type, then the 2D1N price. Elaine's specific ask.

Photos: all 90 of the old site's product images pulled via Elaine's Chrome (site is http-only). Owner's existing images: shop-floor shots (2009-era) and supplier cut-outs. A photo pass at the shop is still the biggest quality upgrade available.

Navigation is a hash router inside one page for the prototype. The real build is separate pages with /en/ mirroring.

## Superseded: three single-page directions
A 山屋 (green/serif), B 價目板 (white/orange/mono), C 河谷 (navy/teal/rounded). Elaine chose A's colours and rejected the single-scroll format.

## Data provenance
Prices verbatim from the inventory Google Sheet (租八借_舊站盤點_inventory), 131 rows, five rate tiers as on the old site. "About 20 years" is from the role-model notes, not from the owner. Policy text does not exist yet. EN gear terms still carry 21 CHECK flags from the inventory sheet.

## Next
Build Phase 1 as real static pages in Claude Code, from this prototype. Then walk-in mockup, set the walk-in date.
