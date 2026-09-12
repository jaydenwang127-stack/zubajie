# Steps 2 and 2b: role-model and design reference passes (2026-09-11)

## Taipei competitors
公館森林 mansionforest.com, 戶外家 Outdoorgear.taipei (PIXNET blog), 逐露天下 rentals.campworld.tw (only one with real e-commerce, multi-branch). All publish prices as images. None has English.

## Best-in-class
やまどうぐレンタル屋 yamarent.com: language switcher, sets before items, policy as a trust banner, trust numbers up front, nav literally has "How to Rent".
LowerGear (Tempe AZ): headline "Nationwide Gear Rentals", destination packages, dedicated policies page.
Kit Lender: daily rate on every card with minimum period inline.
Kanwa Kimono / Yumeyakata / Rikawafuku (Kyoto): language via /en/ path or subdomains, "no hidden costs" FAQ, hours and last-entry time in the top fold, pinned reservation button on mobile.

## Decisions carried into the build
1. Real HTML price tables (text, not images). Category win in Taipei; makes the site findable for "北投 露營 出租".
2. English is an empty field among competitors.
3. Phase 1 static is correct; booking is out of scope.
4. Policy page is the highest-value new content. Content pending owner.
5. Keep the old site's five rate tiers: 售價 / 兩天一夜 / 每加一日 / 五至十天 / 月租.
6. Language switch: /en/ path prefix, mirrored page set, switcher in header and footer labelled 中文 / EN as text. The switch lands on the same page's translation, never the homepage.
7. Opening hours in the top fold: closed Wed and Sun, Saturday closes 15:00.
8. Mobile: pinned tap-to-call 02-2823-0080.
9. Not copying: struck-through "original" prices, multi-currency, hero video.
10. Sets (露營組 etc.) were in early directions; dropped from the prototype until the owner confirms contents.
