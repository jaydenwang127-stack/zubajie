#!/usr/bin/env python3
"""Generate the static 租八借 site into site/ from data/items.json and data/photomap.json.

    python3 build_site.py

Output is plain HTML + one CSS file + photos. No JavaScript, no framework.
Every visible string below is written as a (zh, en) pair so the two language
trees stay in sync and the English twin is always beside the Chinese.
"""
import html
import json
import pathlib
import re
import shutil

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / 'site'
PHOTOS_SRC = ROOT / 'prototype' / 'photos'

# Set this once the site has a domain (no trailing slash). Enables absolute
# hreflang alternates and sitemap.xml. Leave empty until then.
BASE_URL = 'https://jaydenwang127-stack.github.io/zubajie'

TEL = '02-2823-0080'
TEL_HREF = 'tel:+886228230080'
FAX = '02-2821-0278'
EMAIL = 'suntreeyang@gmail.com'
ADDRESS = ('台北市北投區東華街二段210號', 'No. 210, Sec. 2, Donghua St, Beitou District, Taipei')
MAPS_URL = 'https://www.google.com/maps/search/?api=1&query=' + '%E5%8F%B0%E5%8C%97%E5%B8%82%E5%8C%97%E6%8A%95%E5%8D%80%E6%9D%B1%E8%8F%AF%E8%A1%97%E4%BA%8C%E6%AE%B5210%E8%99%9F'

# ---------------------------------------------------------------- copy (zh, en)
T = {
    'brand_sub':   ('北投 · 戶外裝備出租', 'BEITOU · OUTDOOR GEAR RENTAL'),
    'nav_home':    ('首頁', 'Home'),
    'nav_rent':    ('租借裝備', 'Rent gear'),
    'nav_policy':  ('租借規則', 'Rental policy'),
    'nav_contact': ('聯絡我們', 'Contact'),
    'menu':        ('選單', 'Menu'),
    'lang_label':  ('語言', 'Language'),

    'site_title':  ('租八借｜北投戶外裝備出租', '租八借 · Outdoor gear rental in Beitou'),
    'site_desc':   ('北投戶外裝備出租：露營、登山、溯溪、水上裝備。電話預約 02-2823-0080，捷運唭哩岸站步行約 4 分鐘。',
                    'Outdoor gear rental in Beitou, Taipei: camping, hiking, river-tracing and water gear. Call 02-2823-0080. About 4 minutes on foot from MRT Qilian.'),
    'hero_h1':     ('北投戶外裝備出租', 'Outdoor gear rental in Beitou'),
    'hero_p':      ('露營、登山、溯溪、水上裝備。電話預約，到店取還。',
                    'Camping, hiking, river-tracing and water gear. Book by phone, pick up in store.'),
    'cta_browse':  ('裝備與價格', 'Gear and prices'),
    'cta_call':    (f'撥打 {TEL}', f'Call {TEL}'),
    'cta_contact': ('聯絡與交通', 'Contact and directions'),
    'hours_note':  ('週三、週日公休 · 週六 15:00 打烊', 'Closed Wed & Sun · Saturday closes 15:00'),

    'h_cats':      ('租借裝備', 'Rent gear'),
    'h_how':       ('如何租借', 'How to rent'),
    'h_hours':     ('營業時間', 'Opening hours'),
    'h_find':      ('店面位置', 'Location'),
    'h_policy':    ('租借規則', 'Rental policy'),
    'h_contact':   ('聯絡我們', 'Contact'),
    'mrt':         ('捷運淡水信義線 唭哩岸站，步行約 4 分鐘', 'MRT Red Line, Qilian station, about 4 minutes on foot'),
    'maps':        ('在 Google 地圖開啟', 'Open in Google Maps'),
    'tel':         ('電話', 'Tel'),
    'fax':         ('傳真', 'Fax'),

    'policy_lead': ('租借前先知道的事。每一項的內容都要和老闆確認後才會放上來。',
                    'What to know before you rent. Each item below is written once confirmed with the owner.'),
    'policy_tbc':  ('內容待與老闆確認。', 'To be confirmed with the owner.'),

    'crumb_home':  ('首頁', 'Home'),
    'price_2d1n':  ('兩天一夜', '2 days / 1 night'),
    'no_photo':    ('尚無照片', 'No photo yet'),
    'call_reserve': (f'電話預約 {TEL}', f'Call to reserve {TEL}'),
    'conf_flag':   ('舊網站兩頁的價格不同，以上為本頁數字，待老闆確認。',
                    'The old site lists two different prices for this item. Figures above are from this page, pending confirmation.'),
    'items_n':     ('{n} 項', '{n} items'),

    'hours_short1': ('週一、二、四、五 10:00–20:00 · 週六 10:00–15:00', 'Mon Tue Thu Fri 10:00–20:00 · Sat 10:00–15:00'),
    'hours_short2': ('國定假日 10:00–19:00 · 週三、週日公休', 'Holidays 10:00–19:00 · Closed Wed & Sun'),
    'foot_note':   ('價格取自舊網站 dbk.url.tw，待老闆確認後正式生效。',
                    'Prices carried over from the old site dbk.url.tw, pending the owner\'s confirmation.'),

    'nf_h':        ('找不到這一頁', 'Page not found'),
    'nf_p':        ('這個網址不存在，或裝備已下架。', 'This address does not exist, or the item is no longer listed.'),
    'nf_cta':      ('回首頁', 'Back to home'),
}

HOURS = [
    (('週一、二、四、五', 'Mon, Tue, Thu, Fri'), ('10:00–20:00', '10:00–20:00')),
    (('週六', 'Saturday'), ('10:00–15:00', '10:00–15:00')),
    (('國定假日', 'Public holidays'), ('10:00–19:00', '10:00–19:00')),
    (('週三、週日', 'Wednesday & Sunday'), ('公休', 'Closed')),
]

STEPS = [
    ('一', ('打電話預約', 'Call to reserve'),
     ('告訴我們日期和需要的裝備，我們幫你留。', 'Tell us the dates and what you need; we hold it for you.')),
    ('二', ('到店取件', 'Pick up in store'),
     ('捷運唭哩岸站步行 4 分鐘。鞋子、防寒衣可現場試穿。', '4 minutes on foot from MRT Qilian. Try on shoes and wetsuits in the shop.')),
    ('三', ('歸還', 'Return'),
     ('營業時間內送回店裡。', 'Return to the shop during opening hours.')),
]

POLICY = [('押金', 'Deposit'), ('證件', 'ID'), ('歸還時間', 'Return time'),
          ('損壞與遺失', 'Damage and loss'), ('清潔', 'Cleaning'), ('逾期', 'Late return')]

CATS = [
    dict(slug='camping',  page='camping.htm', photo='big74', name=('露營裝備', 'Camping'),
         desc=('帳篷、睡袋、睡墊、桌椅、爐具、燈具，兩天一夜起租。',
               'Tents, sleeping bags, pads, tables and chairs, stoves and lighting. Rent from 2 days / 1 night.')),
    dict(slug='mountain', page='mount_2.htm', photo='big83', name=('登山裝備', 'Mountain'),
         desc=('登山帳、大背包、羽絨睡袋、雨衣、冰爪、爐頭。',
               'Backpacking tents, packs, down bags, rain shells, crampons, stoves.')),
    dict(slug='river',    page='river.htm',   photo='big17', name=('溯溪裝備', 'River tracing'),
         desc=('溯溪鞋、防寒衣、救生衣、頭盔、吊帶與繩索。',
               'River shoes, wetsuits, PFDs, helmets, harnesses and rope.')),
    dict(slug='water',    page='water.htm',   photo='big16', name=('水上裝備', 'Water'),
         desc=('獨木舟、救生衣、救生圈、防寒衣。獨木舟須自取。',
               'Kayaks, PFDs, life rings, wetsuits. Kayaks are collect-in-person only.')),
    dict(slug='other',    page='another.htm', photo='p56',   name=('其他裝備', 'Other'),
         desc=('冰桶、手推車、園藝工具、大聲公、旅行箱。',
               'Coolers, carts, garden tools, megaphone, suitcases.')),
]

# The five rate tiers exactly as on the old site. (key, label, sub-label, css class)
TIERS = [
    ('d2',   ('兩天一夜', '2 days / 1 night'), ('基本租金', 'base rate'), ''),
    ('add',  ('每加一日', 'Each extra day'),   ('超過兩天一夜後', 'beyond 2D1N'), ''),
    ('d5',   ('五至十天', '5–10 days'),        ('包價', 'flat rate'), ''),
    ('mo',   ('月租', 'Monthly'),              ('30 天包價', '30-day flat rate'), ''),
    ('sale', ('售價', 'Buy'),                  ('購買（非租金）', 'purchase, not rent'), 'buy'),
]

LANGS = {'zh': 'zh-Hant-TW', 'en': 'en'}

# ---------------------------------------------------------------- helpers
def esc(s):
    return html.escape(str(s), quote=True)

def t(key, lang, **kw):
    s = T[key][0 if lang == 'zh' else 1]
    return esc(s.format(**kw) if kw else s)

def pick(pair, lang):
    return esc(pair[0] if lang == 'zh' else pair[1])

def clean(s):
    # The sheet export markdown-escaped these characters.
    return re.sub(r'\\([*_<>~])', r'\1', s or '')

def price(n):
    return f'NT${n:,}' if n else '—'

def load_items():
    items = json.loads((ROOT / 'data' / 'items.json').read_text())
    pmap = json.loads((ROOT / 'data' / 'photomap.json').read_text())
    out = []
    for it in items:
        first = clean(it['img'].split(';')[0].strip())
        row = dict(
            id=it['id'], page=clean(it['page']),
            name=(clean(it['zh']), clean(it['en'])),
            spec=(clean(it['spec']), clean(it['specen'])),
            photo=pmap.get(first, ''),
            conf=bool(str(it.get('conf', '')).strip()),
            chk=bool(str(it.get('chk', '')).strip()),
        )
        for k in ('sale', 'd2', 'add', 'd5', 'mo'):
            v = str(it[k]).replace(',', '').strip()
            row[k] = int(v) if v else 0
        out.append(row)
    return out

ITEMS = load_items()
BY_PAGE = {c['slug']: [i for i in ITEMS if i['page'] == c['page']] for c in CATS}
assert sum(len(v) for v in BY_PAGE.values()) == len(ITEMS), 'every item must map to a category'

# ---------------------------------------------------------------- paths
def page_path(lang, path):
    """Path of a page inside site/. zh pages live at the root, en pages under en/."""
    return ('en/' + path) if lang == 'en' else path

def twin_path(lang, path):
    """Same page in the other language."""
    return path[3:] if lang == 'en' else 'en/' + path

class Ctx:
    """Link helpers for one page: everything is relative so the site works from any sub-path."""
    def __init__(self, lang, path):
        self.lang = lang
        self.path = page_path(lang, path)      # e.g. en/rent/camping.html
        self.rel = '../' * self.path.count('/')
        self.twin = self.rel + twin_path(lang, self.path)

    def link(self, path):              # page in the same language
        return self.rel + page_path(self.lang, path)

    def asset(self, path):             # shared css / photos
        return self.rel + path

    def photo(self, name):
        return self.asset(f'photos/{name}.jpg')

# ---------------------------------------------------------------- fragments
def img_or_placeholder(c, it, cls=''):
    if it['photo']:
        return f'<img src="{c.photo(it["photo"])}" alt="{pick(it["name"], c.lang)}" loading="lazy" width="240" height="240">'
    return f'<div class="ph">{t("no_photo", c.lang)}</div>'

def hours_rows(lang):
    return ''.join(f'<div><dt>{pick(d, lang)}</dt><dd>{pick(h, lang)}</dd></div>' for d, h in HOURS)

def cat_links(c, current=None, counts=True):
    out = []
    for cat in CATS:
        cur = ' aria-current="page"' if cat['slug'] == current else ''
        n = f'<small>{len(BY_PAGE[cat["slug"]])}</small>' if counts else ''
        href = c.link('rent/%s.html' % cat['slug'])
        out.append(f'<a href="{href}"{cur}>{pick(cat["name"], c.lang)}{n}</a>')
    return ''.join(out)

def header(c, nav):
    L = c.lang
    def cur(key):
        return ' aria-current="page"' if nav == key else ''
    zh_cur, en_cur = (' aria-current="true"', '') if L == 'zh' else ('', ' aria-current="true"')
    # language switch links point at the same page in the other language, never the homepage
    zh_href = c.twin if L == 'en' else '#'
    en_href = c.twin if L == 'zh' else '#'
    first_cat = c.link('rent/camping.html')
    return f'''<header>
  <div class="wrap">
    <a class="brand" href="{c.link('index.html')}">租八借<small>{t('brand_sub', L)}</small></a>
    <nav class="main" aria-label="{t('menu', L)}">
      <a href="{c.link('index.html')}"{cur('home')}>{t('nav_home', L)}</a>
      <div class="dd">
        <a href="{first_cat}"{cur('rent')}>{t('nav_rent', L)}</a>
        <div class="dd-menu">{cat_links(c)}</div>
      </div>
      <a href="{c.link('policy.html')}"{cur('policy')}>{t('nav_policy', L)}</a>
      <a href="{c.link('contact.html')}"{cur('contact')}>{t('nav_contact', L)}</a>
    </nav>
    <div class="lang" aria-label="{t('lang_label', L)}"><a href="{zh_href}" lang="zh-Hant-TW"{zh_cur}>中文</a><a href="{en_href}" lang="en"{en_cur}>EN</a></div>
    <a class="callhead" href="{TEL_HREF}">{TEL}</a>
    <details class="menu">
      <summary aria-label="{t('menu', L)}"><span></span><span></span><span></span></summary>
      <div class="drawer">
        <a href="{c.link('index.html')}">{t('nav_home', L)}</a>
        <div class="grp">{t('nav_rent', L)}</div>
        <div class="sub">{cat_links(c, counts=False)}</div>
        <a href="{c.link('policy.html')}">{t('nav_policy', L)}</a>
        <a href="{c.link('contact.html')}">{t('nav_contact', L)}</a>
      </div>
    </details>
  </div>
</header>'''

def footer(c):
    L = c.lang
    zh_href = c.twin if L == 'en' else '#'
    en_href = c.twin if L == 'zh' else '#'
    zh_cur, en_cur = (' aria-current="true"', '') if L == 'zh' else ('', ' aria-current="true"')
    return f'''<footer><div class="wrap">
  <div><div class="fh">租八借</div><p>{pick(ADDRESS, L)}</p><p>{t('mrt', L)}</p></div>
  <div><div class="fh">{t('nav_contact', L)}</div><p><a href="{TEL_HREF}">{TEL}</a></p><p><a href="mailto:{EMAIL}">{EMAIL}</a></p></div>
  <div><div class="fh">{t('h_hours', L)}</div><p>{t('hours_short1', L)}</p><p>{t('hours_short2', L)}</p></div>
  <p class="note">{t('foot_note', L)} · <a href="{zh_href}" lang="zh-Hant-TW"{zh_cur}>中文</a> / <a href="{en_href}" lang="en"{en_cur}>EN</a></p>
</div></footer>
<div class="callbar"><a class="call" href="{TEL_HREF}">{t('cta_call', L)}</a></div>'''

def layout(c, title, desc, body, nav=None):
    L = c.lang
    alt = ''
    if BASE_URL:
        zh_abs = f'{BASE_URL}/{twin_path("en", c.path) if L == "en" else c.path}'
        en_abs = f'{BASE_URL}/{c.path if L == "en" else twin_path("zh", c.path)}'
        alt = (f'\n<link rel="alternate" hreflang="zh-Hant" href="{zh_abs}">'
               f'\n<link rel="alternate" hreflang="en" href="{en_abs}">'
               f'\n<link rel="alternate" hreflang="x-default" href="{zh_abs}">')
    return f'''<!DOCTYPE html>
<html lang="{LANGS[L]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">{alt}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+TC:wght@600;700&family=Noto+Sans+TC:wght@400;500;700&display=swap">
<link rel="stylesheet" href="{c.asset('css/site.css')}">
</head>
<body>
{header(c, nav)}
<main>
{body}
</main>
{footer(c)}
</body>
</html>
'''

# ---------------------------------------------------------------- pages
def page_home(lang):
    c = Ctx(lang, 'index.html')
    cats = ''.join(
        f'<a class="cat" href="{c.link("rent/%s.html" % cat["slug"])}">'
        f'<div class="im"><img src="{c.photo(cat["photo"])}" alt="" width="240" height="180"></div>'
        f'<div class="t"><h3>{pick(cat["name"], lang)}</h3><small>{t("items_n", lang, n=len(BY_PAGE[cat["slug"]]))}</small></div></a>'
        for cat in CATS)
    steps = ''.join(
        f'<div class="step"><div class="n">{n}</div><h3>{pick(h, lang)}</h3><p>{pick(p, lang)}</p></div>'
        for n, h, p in STEPS)
    body = f'''<div class="hero"><div class="wrap">
  <div>
    <h1>{t('hero_h1', lang)}</h1>
    <p>{t('hero_p', lang)}</p>
    <div class="hero-cta"><a class="btn" href="{c.link('rent/camping.html')}">{t('cta_browse', lang)}</a><a class="btn ghost" href="{TEL_HREF}">{t('cta_call', lang)}</a></div>
    <div class="hours-note">{t('hours_note', lang)}</div>
  </div>
  <div class="mosaic">
    <img class="m1" src="{c.photo('big74')}" alt="">
    <img src="{c.photo('big17')}" alt="">
    <img src="{c.photo('big16')}" alt="">
  </div>
</div></div>
<section><div class="wrap">
  <h2>{t('h_cats', lang)}</h2>
  <div class="cats">{cats}</div>
</div></section>
<section class="band"><div class="wrap">
  <h2>{t('h_how', lang)}</h2>
  <div class="steps">{steps}</div>
</div></section>
<section><div class="wrap info">
  <div>
    <h2>{t('h_hours', lang)}</h2>
    <dl class="hours">{hours_rows(lang)}</dl>
  </div>
  <div class="addr">
    <h2>{t('h_find', lang)}</h2>
    <p>{pick(ADDRESS, lang)}</p>
    <p>{t('mrt', lang)}</p>
    <p class="mt"><a class="btn ghost" href="{c.link('contact.html')}">{t('cta_contact', lang)}</a></p>
  </div>
</div></section>'''
    return c, t('site_title', lang), t('site_desc', lang), body, 'home'

def page_cat(lang, cat):
    c = Ctx(lang, f'rent/{cat["slug"]}.html')
    cards = ''.join(
        f'<a class="card" href="{c.link("rent/item/%s.html" % it["id"])}">'
        f'<div class="im">{img_or_placeholder(c, it)}</div>'
        f'<div class="t"><h3>{pick(it["name"], lang)}</h3><div class="spec">{pick(it["spec"], lang)}</div>'
        f'<div class="price">{t("price_2d1n", lang)} <b>{price(it["d2"])}</b></div></div></a>'
        for it in BY_PAGE[cat['slug']])
    body = f'''<div class="wrap">
  <div class="cat-head">
    <h1>{pick(cat['name'], lang)}</h1>
    <p>{pick(cat['desc'], lang)}</p>
    <nav class="subnav" aria-label="{t('nav_rent', lang)}">{cat_links(c, current=cat['slug'], counts=False)}</nav>
  </div>
  <div class="grid">{cards}</div>
</div>'''
    sep = '｜' if lang == 'zh' else ' | '
    title = f'{pick(cat["name"], lang)}{sep}租八借'
    return c, title, pick(cat['desc'], lang), body, 'rent'

def page_item(lang, cat, it):
    c = Ctx(lang, f'rent/item/{it["id"]}.html')
    name, spec = pick(it['name'], lang), pick(it['spec'], lang)
    rates = ''.join(
        f'<div class="{cls}"><dt>{pick(lbl, lang)}<small>{pick(sub, lang)}</small></dt><dd>{price(it[k])}</dd></div>'
        for k, lbl, sub, cls in TIERS)
    flag = f'<div class="flag">{t("conf_flag", lang)}</div>' if it['conf'] else ''
    chk = '<!-- EN term flagged CHECK in the inventory sheet -->\n' if it['chk'] else ''
    body = f'''{chk}<div class="wrap">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="{c.link('index.html')}">{t('crumb_home', lang)}</a> › <a href="{c.link("rent/%s.html" % cat["slug"])}">{pick(cat['name'], lang)}</a> › {name}</nav>
  <div class="prod">
    <div class="im">{img_or_placeholder(c, it)}</div>
    <div>
      <span class="cat-tag">{pick(cat['name'], lang)}</span>
      <h1>{name}</h1>
      {f'<p class="spec">{spec}</p>' if spec else ''}
      <dl class="rates">{rates}</dl>
      {flag}
      <a class="btn" href="{TEL_HREF}">{t('call_reserve', lang)}</a>
    </div>
  </div>
</div>'''
    sep = '｜' if lang == 'zh' else ' | '
    title = f'{name}{sep}{pick(cat["name"], lang)}{sep}租八借'
    if lang == 'zh':
        desc = f'{name}{"，" + spec if spec else ""}。兩天一夜 {price(it["d2"])}。租八借，北投戶外裝備出租。'
    else:
        desc = f'{name}{", " + spec if spec else ""}. 2 days / 1 night {price(it["d2"])}. 租八借, outdoor gear rental in Beitou.'
    return c, title, desc, body, 'rent'

def page_policy(lang):
    c = Ctx(lang, 'policy.html')
    items = ''.join(f'<div><h3>{pick(p, lang)}</h3><p>{t("policy_tbc", lang)}</p></div>' for p in POLICY)
    body = f'''<section><div class="wrap">
  <h1>{t('h_policy', lang)}</h1>
  <p class="lead">{t('policy_lead', lang)}</p>
  <div class="policy-list">{items}</div>
</div></section>'''
    sep = '｜' if lang == 'zh' else ' | '
    return c, f'{t("h_policy", lang)}{sep}租八借', t('policy_lead', lang), body, 'policy'

def page_contact(lang):
    c = Ctx(lang, 'contact.html')
    body = f'''<section><div class="wrap info">
  <div>
    <h1>{t('h_contact', lang)}</h1>
    <div class="addr">
      <p><strong>租八借</strong></p>
      <p>{pick(ADDRESS, lang)}</p>
      <p>{t('mrt', lang)}</p>
      <p><a href="{MAPS_URL}" rel="noopener">{t('maps', lang)}</a></p>
      <p class="mt">{t('tel', lang)} <a href="{TEL_HREF}">{TEL}</a></p>
      <p>{t('fax', lang)} {FAX}</p>
      <p>Email <a href="mailto:{EMAIL}">{EMAIL}</a></p>
    </div>
  </div>
  <div>
    <h2>{t('h_hours', lang)}</h2>
    <dl class="hours">{hours_rows(lang)}</dl>
  </div>
</div></section>'''
    sep = '｜' if lang == 'zh' else ' | '
    desc = f'{pick(ADDRESS, lang)}. {t("tel", lang)} {TEL}. {t("hours_short1", lang)}. {t("hours_short2", lang)}'
    return c, f'{t("h_contact", lang)}{sep}租八借', desc, body, 'contact'

def page_404(lang):
    c = Ctx(lang, '404.html')
    body = f'''<section><div class="wrap">
  <h1>{t('nf_h', lang)}</h1>
  <p class="lead">{t('nf_p', lang)}</p>
  <p class="mt"><a class="btn" href="{c.link('index.html')}">{t('nf_cta', lang)}</a></p>
</div></section>'''
    return c, f'{t("nf_h", lang)} · 租八借', t('nf_p', lang), body, None

# ---------------------------------------------------------------- css
CSS = r'''
:root{--bg:#F1F2EA;--paper:#FFFFFF;--ink:#1B241E;--mute:#5C6B60;--green:#1E3A2B;--green-ink:#EEF0E6;--blue:#2F6F8F;--rule:#D6DACB;--soft:#E4E7DA;--warn:#8A4B12;--maxw:1080px}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--ink);font-family:"Noto Sans TC",system-ui,-apple-system,"PingFang TC","Microsoft JhengHei",sans-serif;line-height:1.6;-webkit-font-smoothing:antialiased}
h1,h2,h3{font-family:"Noto Serif TC",Georgia,"PingFang TC",serif;margin:0;text-wrap:balance;font-weight:700}
a{color:inherit}
:focus-visible{outline:3px solid var(--blue);outline-offset:2px}
img{max-width:100%}
.wrap{max-width:var(--maxw);margin:0 auto;padding-inline:20px}
@media (min-width:720px){.wrap{padding-inline:32px}}
.mt{margin-top:1rem!important}

/* header */
header{background:var(--green);color:var(--green-ink);position:sticky;top:0;z-index:20}
header .wrap{display:flex;align-items:center;gap:1.5rem;min-height:64px}
.brand{font-family:"Noto Serif TC",serif;font-weight:700;font-size:1.45rem;letter-spacing:.08em;text-decoration:none;line-height:1.1}
.brand small{display:block;font-family:"Noto Sans TC",sans-serif;font-weight:400;font-size:.62rem;letter-spacing:.16em;opacity:.75;margin-top:.15rem}
nav.main{display:none;margin-left:auto;align-items:center;gap:.25rem}
nav.main a{color:inherit;text-decoration:none;padding:.55rem .8rem;border-radius:3px;font-size:.95rem;display:inline-block}
nav.main a:hover,nav.main a[aria-current=page]{background:rgba(255,255,255,.12)}
.dd{position:relative}
.dd>a::after{content:"";display:inline-block;width:.4em;height:.4em;border:solid currentColor;border-width:0 1.5px 1.5px 0;transform:rotate(45deg);margin-left:.45em;position:relative;top:-.15em}
.dd-menu{position:absolute;top:100%;left:0;background:var(--paper);color:var(--ink);min-width:220px;border-radius:4px;box-shadow:0 10px 30px rgba(27,36,30,.18);padding:.4rem;display:none;flex-direction:column;margin-top:.3rem}
.dd:hover .dd-menu,.dd:focus-within .dd-menu{display:flex}
.dd-menu a{padding:.55rem .8rem;border-radius:3px;text-decoration:none;display:flex;justify-content:space-between;gap:1rem;font-size:.95rem}
.dd-menu a:hover,.dd-menu a[aria-current=page]{background:var(--soft)}
.dd-menu a small{color:var(--mute);font-size:.8rem}
.lang{display:flex;border:1px solid rgba(255,255,255,.45);border-radius:3px;overflow:hidden;margin-left:auto}
.lang a{color:inherit;text-decoration:none;padding:.35rem .7rem;font-size:.85rem;white-space:nowrap;line-height:1.4}
.lang a[aria-current=true]{background:var(--green-ink);color:var(--green)}
.callhead{display:none;text-decoration:none;font-weight:700;border:1px solid rgba(255,255,255,.45);border-radius:3px;padding:.35rem .8rem;font-size:.9rem}
@media (max-width:480px){.brand small{display:none}.brand{font-size:1.3rem}}
@media (min-width:860px){nav.main{display:flex}.lang{margin-left:0}.callhead{display:inline-block}.menu{display:none}}

/* mobile menu: <details>, no script needed */
.menu{margin-left:.25rem}
.menu summary{list-style:none;cursor:pointer;padding:.4rem;display:grid;gap:5px;border-radius:3px}
.menu summary::-webkit-details-marker{display:none}
.menu summary span{display:block;width:22px;height:2px;background:currentColor}
.menu[open] summary{background:rgba(255,255,255,.12)}
.drawer{position:absolute;left:0;right:0;top:100%;background:var(--green);color:var(--green-ink);border-top:1px solid rgba(255,255,255,.15);box-shadow:0 12px 24px rgba(27,36,30,.25)}
.drawer a{display:block;padding:.8rem 20px;text-decoration:none;border-bottom:1px solid rgba(255,255,255,.1)}
.drawer .sub a{padding-left:2.4rem;font-size:.95rem;opacity:.9}
.drawer .grp{padding:.8rem 20px .3rem;font-size:.72rem;letter-spacing:.14em;opacity:.7}

/* pages */
main{min-height:60vh}
section{padding-block:3rem}
@media (min-width:720px){section{padding-block:4rem}}
h2{font-size:1.65rem;margin-bottom:1.2rem}
section h1{font-size:2rem;margin-bottom:1.2rem}
.lead{max-width:44ch;color:var(--mute);margin:0 0 2rem}

/* home */
.hero{padding-block:2.5rem 3rem}
.hero .wrap{display:grid;gap:2rem}
@media (min-width:860px){.hero .wrap{grid-template-columns:1.05fr 1fr;align-items:center;gap:3.5rem}.hero{padding-block:4rem}}
.hero h1{font-size:2rem;line-height:1.25}
@media (min-width:720px){.hero h1{font-size:2.6rem}}
.hero p{max-width:40ch;margin:1rem 0 0;color:var(--mute);font-size:1.05rem}
.hero-cta{display:flex;gap:.75rem;flex-wrap:wrap;margin-top:1.6rem}
.btn{display:inline-block;text-decoration:none;padding:.8rem 1.3rem;border-radius:3px;font-weight:700;border:1px solid var(--green);background:var(--green);color:var(--green-ink)}
.btn.ghost{background:transparent;color:var(--green)}
.hours-note{margin-top:1.4rem;display:inline-flex;gap:.6rem;align-items:center;background:var(--soft);padding:.5rem .8rem;border-left:4px solid var(--blue);font-size:.92rem}
.mosaic{display:grid;grid-template-columns:1fr 1fr;grid-template-rows:180px 140px;gap:8px}
@media (min-width:720px){.mosaic{grid-template-rows:240px 190px}}
.mosaic img{width:100%;height:100%;object-fit:cover;display:block;border-radius:3px}
.mosaic .m1{grid-column:1/3}
.cats{display:grid;gap:1rem;grid-template-columns:1fr 1fr}
@media (min-width:720px){.cats{grid-template-columns:repeat(3,1fr);gap:1.25rem}}
@media (min-width:1000px){.cats{grid-template-columns:repeat(5,1fr)}}
.cat{background:var(--paper);border:1px solid var(--rule);border-radius:4px;overflow:hidden;text-decoration:none;display:block}
.cat:hover{border-color:var(--blue)}
.cat .im{aspect-ratio:4/3;background:#fff;display:grid;place-items:center;overflow:hidden}
.cat img{width:100%;height:100%;object-fit:cover;display:block}
.cat .t{padding:.8rem .9rem 1rem}
.cat h3{font-size:1.1rem}
.cat small{display:block;color:var(--mute);font-size:.8rem;margin-top:.15rem}
.steps{display:grid;gap:1.5rem}
@media (min-width:720px){.steps{grid-template-columns:repeat(3,1fr);gap:2rem}}
.step h3{font-size:1.1rem;margin-bottom:.35rem}
.step p{margin:0;color:var(--mute);font-size:.95rem}
.step .n{font-family:"Noto Serif TC",serif;color:var(--blue);font-size:1.6rem;line-height:1;margin-bottom:.6rem}
.band{background:var(--green);color:var(--green-ink)}
.band h2{color:#fff}
.band .step p{color:rgba(238,240,230,.8)}
.band .step .n{color:#9CC3D5}
.info{display:grid;gap:2rem}
@media (min-width:720px){.info{grid-template-columns:1fr 1fr;gap:3rem}}
.hours{margin:0;display:grid;gap:.3rem;max-width:380px}
.hours div{display:flex;justify-content:space-between;padding:.45rem 0;border-bottom:1px solid var(--rule)}
.hours dt{font-weight:500}.hours dd{margin:0;font-variant-numeric:tabular-nums}
.addr p{margin:.2rem 0}

/* catalog */
.cat-head{padding-block:2.5rem 1.5rem}
.cat-head h1{font-size:2rem}
.cat-head p{color:var(--mute);margin:.5rem 0 0;max-width:48ch}
.subnav{display:flex;gap:.4rem;flex-wrap:wrap;margin-top:1.4rem}
.subnav a{text-decoration:none;font-size:.9rem;padding:.4rem .85rem;border:1px solid var(--rule);border-radius:999px;background:var(--paper)}
.subnav a:hover{border-color:var(--blue)}
.subnav a[aria-current=page]{background:var(--green);color:var(--green-ink);border-color:var(--green)}
.grid{display:grid;gap:1.25rem;grid-template-columns:1fr 1fr;padding-bottom:3rem}
@media (min-width:720px){.grid{grid-template-columns:repeat(3,1fr);gap:1.5rem}}
@media (min-width:1000px){.grid{grid-template-columns:repeat(4,1fr);gap:1.75rem}}
.card{background:var(--paper);border:1px solid var(--rule);border-radius:4px;text-decoration:none;display:flex;flex-direction:column;overflow:hidden}
.card:hover{border-color:var(--blue)}
.card .im{aspect-ratio:1;background:#fff;display:grid;place-items:center;padding:8%;border-bottom:1px solid var(--rule)}
.card img{width:auto;height:auto;max-width:100%;max-height:100%;object-fit:contain;display:block}
.ph{color:var(--mute);font-size:.75rem;text-align:center}
.card .t{padding:.9rem .9rem 1rem;display:grid;gap:.25rem}
.card h3{font-size:1rem;font-family:"Noto Sans TC",sans-serif;font-weight:700;line-height:1.35}
.card .spec{color:var(--mute);font-size:.8rem;line-height:1.4;min-height:1.1em}
.card .price{margin-top:.5rem;font-size:.85rem;color:var(--mute)}
.card .price b{color:var(--ink);font-size:1.05rem;font-variant-numeric:tabular-nums}

/* product */
.prod{padding-block:2rem 4rem;display:grid;gap:2rem}
@media (min-width:860px){.prod{grid-template-columns:1fr 1fr;gap:3.5rem;align-items:start;padding-block:3rem 5rem}}
.crumbs{font-size:.85rem;color:var(--mute);padding-top:1.5rem}
.crumbs a{color:var(--mute);text-decoration:none}
.crumbs a:hover{text-decoration:underline}
.prod .im{background:var(--paper);border:1px solid var(--rule);border-radius:4px;aspect-ratio:1;display:grid;place-items:center;padding:8%}
.prod .im img{width:auto;height:auto;max-width:100%;max-height:100%;object-fit:contain}
.prod h1{font-size:1.8rem;line-height:1.25}
.prod .spec{color:var(--mute);margin:.6rem 0 0;font-size:1rem}
.prod .cat-tag{display:inline-block;font-size:.75rem;letter-spacing:.12em;color:var(--blue);margin-bottom:.6rem}
.rates{margin:1.8rem 0 0;border-top:2px solid var(--green)}
.rates div{display:flex;justify-content:space-between;align-items:baseline;padding:.7rem 0;border-bottom:1px solid var(--rule)}
.rates dt{font-weight:500}.rates dd{margin:0;font-variant-numeric:tabular-nums;font-size:1.1rem}
.rates dt small{display:block;font-weight:400;color:var(--mute);font-size:.78rem}
.rates .buy dd{color:var(--mute);font-size:1rem}
.flag{margin-top:1rem;font-size:.85rem;color:var(--warn);background:#F6EBDD;padding:.6rem .8rem;border-radius:3px}
.prod .btn{margin-top:1.6rem}

/* policy */
.policy-list{display:grid;gap:1rem;max-width:720px}
@media (min-width:720px){.policy-list{grid-template-columns:1fr 1fr;gap:1.25rem}}
.policy-list div{background:var(--paper);border:1px solid var(--rule);border-radius:4px;padding:1.1rem 1.2rem}
.policy-list h3{font-size:1.05rem;margin-bottom:.3rem}
.policy-list p{margin:0;color:var(--mute);font-size:.9rem}

/* footer + mobile call bar */
footer{background:var(--green);color:var(--green-ink);padding-block:2.5rem;font-size:.9rem}
footer .wrap{display:grid;gap:1.5rem}
@media (min-width:720px){footer .wrap{grid-template-columns:1fr 1fr 1fr}}
footer p{margin:.2rem 0}footer a{color:#fff}
footer .fh{font-family:"Noto Serif TC",serif;font-size:1.05rem;margin-bottom:.4rem}
footer .note{opacity:.7;font-size:.75rem;grid-column:1/-1;margin-top:.5rem}
footer .note a[aria-current=true]{font-weight:700;text-decoration:none}
.callbar{position:sticky;bottom:0;background:var(--green);padding:.6rem 20px;border-top:1px solid rgba(255,255,255,.2);z-index:15}
.callbar .call{display:block;text-align:center;background:var(--green-ink);color:var(--green);text-decoration:none;font-weight:700;padding:.75rem;border-radius:3px}
@media (min-width:860px){.callbar{display:none}}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
'''.lstrip()

# ---------------------------------------------------------------- build
def write(rel, text):
    p = OUT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding='utf-8')

def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    shutil.copytree(PHOTOS_SRC, OUT / 'photos')
    write('css/site.css', CSS)

    pages = []
    for lang in ('zh', 'en'):
        pages.append(page_home(lang))
        pages.append(page_policy(lang))
        pages.append(page_contact(lang))
        pages.append(page_404(lang))
        for cat in CATS:
            pages.append(page_cat(lang, cat))
            for it in BY_PAGE[cat['slug']]:
                pages.append(page_item(lang, cat, it))

    for c, title, desc, body, nav in pages:
        write(c.path, layout(c, title, desc, body, nav))

    # GitHub Pages serves /404.html for any missing path; the zh one is the default.
    write('robots.txt', 'User-agent: *\nAllow: /\n' + (f'Sitemap: {BASE_URL}/sitemap.xml\n' if BASE_URL else ''))
    if BASE_URL:
        urls = ''.join(f'  <url><loc>{BASE_URL}/{c.path}</loc></url>\n' for c, *_ in pages if not c.path.endswith('404.html'))
        write('sitemap.xml', f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')

    n_items = len(ITEMS)
    print(f'ok: {len(pages)} pages ({n_items} items x 2 languages + {len(pages) - 2 * n_items} others) -> {OUT.relative_to(ROOT)}/')
    print('   ', ', '.join(f'{c["slug"]} {len(BY_PAGE[c["slug"]])}' for c in CATS))
    print(f'    conf flags shown: {sum(1 for i in ITEMS if i["conf"])}, no photo: {sum(1 for i in ITEMS if not i["photo"])}')

if __name__ == '__main__':
    main()
