import json, pathlib
S = pathlib.Path(__file__).parent
items = json.load(open(S.parent/'data'/'items.json'))
pmap = json.load(open(S.parent/'data'/'photomap.json'))  # paths below assume this script lives in prototype/ next to data/ one level up
def clean(s): return s.replace('\\*','*').replace('\\_','_').replace('\\<','<').replace('\\>','>').replace('\\~','~')
for it in items:
    it['page'] = clean(it['page'])
    it['zh'] = clean(it['zh']); it['spec'] = clean(it['spec']); it['specen'] = clean(it['specen'])
    first = it['img'].split(';')[0].strip().replace('\\','')
    it['photo'] = pmap.get(first, '')
    for k in ('sale','d2','add','d5','mo'):
        it[k] = int(str(it[k]).replace(',','')) if str(it[k]).strip() else 0
    it.pop('img'); it.pop('note',None); it.pop('chk',None)
data = json.dumps(items, ensure_ascii=False)

def bi(zh, en): return f'<span class="zh">{zh}</span><span class="en">{en}</span>'

HTML = r'''<title>租八借</title>
<meta name="description" content="租八借 website rebuild prototype: home, rental catalog by category, policy and contact, in Chinese and English.">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+TC:wght@600;700&family=Noto+Sans+TC:wght@400;500;700&display=swap">
<style>
:root{--bg:#F1F2EA;--paper:#FFFFFF;--ink:#1B241E;--mute:#5C6B60;--green:#1E3A2B;--green-ink:#EEF0E6;--blue:#2F6F8F;--rule:#D6DACB;--soft:#E4E7DA;--warn:#8A4B12;--maxw:1080px}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-family:"Noto Sans TC",system-ui,sans-serif;line-height:1.6;-webkit-font-smoothing:antialiased}
body.en .zh{display:none} body:not(.en) .en{display:none} .zh,.en{display:inline}
h1,h2,h3{font-family:"Noto Serif TC",Georgia,serif;margin:0;text-wrap:balance;font-weight:700}
a{color:inherit}
:focus-visible{outline:3px solid var(--blue);outline-offset:2px}
button{font:inherit;cursor:pointer}
.wrap{max-width:var(--maxw);margin:0 auto;padding-inline:20px}
@media (min-width:720px){.wrap{padding-inline:32px}}
.ribbon{background:#111;color:#fff;font-size:.72rem;text-align:center;padding:.3rem;letter-spacing:.08em}

/* header */
header{background:var(--green);color:var(--green-ink);position:sticky;top:0;z-index:20}
header .wrap{display:flex;align-items:center;gap:1.5rem;min-height:64px}
.brand{font-family:"Noto Serif TC",serif;font-weight:700;font-size:1.45rem;letter-spacing:.08em;text-decoration:none;line-height:1.1}
.brand small{display:block;font-family:"Noto Sans TC";font-weight:400;font-size:.62rem;letter-spacing:.16em;opacity:.75;margin-top:.15rem}
nav.main{display:none;margin-left:auto;align-items:center;gap:.25rem}
nav.main a,nav.main button{color:inherit;text-decoration:none;background:none;border:0;padding:.55rem .8rem;border-radius:3px;font-size:.95rem}
nav.main a:hover,nav.main button:hover,nav.main a[aria-current=page]{background:rgba(255,255,255,.12)}
.dd{position:relative}
.dd button::after{content:"";display:inline-block;width:.4em;height:.4em;border:solid currentColor;border-width:0 1.5px 1.5px 0;transform:rotate(45deg);margin-left:.45em;position:relative;top:-.15em}
.dd-menu{position:absolute;top:100%;left:0;background:var(--paper);color:var(--ink);min-width:200px;border-radius:4px;box-shadow:0 10px 30px rgba(27,36,30,.18);padding:.4rem;display:none;flex-direction:column;margin-top:.3rem}
.dd.open .dd-menu,.dd:hover .dd-menu,.dd:focus-within .dd-menu{display:flex}
.dd-menu a{padding:.55rem .8rem;border-radius:3px;text-decoration:none;display:flex;justify-content:space-between;gap:1rem}
.dd-menu a:hover{background:var(--soft)}
.dd-menu a small{color:var(--mute);font-size:.8rem}
.lang{display:flex;border:1px solid rgba(255,255,255,.45);border-radius:3px;overflow:hidden;margin-left:auto}
.lang button{background:none;border:0;color:inherit;padding:.35rem .7rem;font-size:.85rem;white-space:nowrap}
@media (max-width:480px){.brand small{display:none}.brand{font-size:1.3rem}}
.lang button[aria-pressed=true]{background:var(--green-ink);color:var(--green)}
.callhead{display:none;text-decoration:none;font-weight:700;border:1px solid rgba(255,255,255,.45);border-radius:3px;padding:.35rem .8rem;font-size:.9rem}
.burger{background:none;border:0;color:inherit;padding:.4rem;display:grid;gap:5px;margin-left:.25rem}
.burger span{display:block;width:22px;height:2px;background:currentColor}
@media (min-width:860px){nav.main{display:flex}.lang{margin-left:0}.callhead{display:inline-block}.burger{display:none}}
.drawer{display:none;background:var(--green);color:var(--green-ink);border-top:1px solid rgba(255,255,255,.15)}
.drawer.open{display:block}
.drawer a{display:block;padding:.8rem 20px;text-decoration:none;border-bottom:1px solid rgba(255,255,255,.1)}
.drawer .sub a{padding-left:2.4rem;font-size:.95rem;opacity:.9}
.drawer .grp{padding:.8rem 20px .3rem;font-size:.72rem;letter-spacing:.14em;opacity:.7}

/* pages */
main{min-height:60vh}
.page{display:none}.page.active{display:block}
section{padding-block:3rem}
@media (min-width:720px){section{padding-block:4rem}}
.eyebrow{font-size:.75rem;letter-spacing:.16em;text-transform:uppercase;color:var(--blue);font-weight:500;margin-bottom:.6rem}
h2{font-size:1.65rem;margin-bottom:1.2rem}
.lead{max-width:44ch;color:var(--mute);margin:0}

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
.band .eyebrow{color:#9CC3D5}
.band h2{color:#fff}
.band .step p{color:rgba(238,240,230,.8)}
.info{display:grid;gap:2rem}
@media (min-width:720px){.info{grid-template-columns:1fr 1fr;gap:3rem}}
.hours{margin:0;display:grid;gap:.3rem;max-width:380px}
.hours div{display:flex;justify-content:space-between;padding:.45rem 0;border-bottom:1px solid rgba(255,255,255,.18)}
.hours dt{font-weight:500}.hours dd{margin:0;font-variant-numeric:tabular-nums}
.page-contact .hours div,#page-home .info .hours div{border-bottom-color:var(--rule)}
.band a{color:#fff}
.addr p{margin:.2rem 0}

/* catalog */
.cat-head{padding-block:2.5rem 1.5rem}
.cat-head h1{font-size:2rem}
.cat-head p{color:var(--mute);margin:.5rem 0 0;max-width:48ch}
.subnav{display:flex;gap:.4rem;flex-wrap:wrap;margin-top:1.4rem}
.subnav a{text-decoration:none;font-size:.9rem;padding:.4rem .85rem;border:1px solid var(--rule);border-radius:999px;background:var(--paper)}
.subnav a[aria-current=page]{background:var(--green);color:var(--green-ink);border-color:var(--green)}
.grid{display:grid;gap:1.25rem;grid-template-columns:1fr 1fr;padding-bottom:3rem}
@media (min-width:720px){.grid{grid-template-columns:repeat(3,1fr);gap:1.5rem}}
@media (min-width:1000px){.grid{grid-template-columns:repeat(4,1fr);gap:1.75rem}}
.card{background:var(--paper);border:1px solid var(--rule);border-radius:4px;text-decoration:none;display:flex;flex-direction:column;overflow:hidden}
.card:hover{border-color:var(--blue)}
.card .im{aspect-ratio:1;background:#fff;display:grid;place-items:center;padding:8%;border-bottom:1px solid var(--rule)}
.card img{max-width:100%;max-height:100%;object-fit:contain;display:block}
.card .ph{color:var(--mute);font-size:.75rem;text-align:center}
.card .t{padding:.9rem .9rem 1rem;display:grid;gap:.25rem}
.card h3{font-size:1rem;font-family:"Noto Sans TC";font-weight:700;line-height:1.35}
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
.prod .im img{max-width:100%;max-height:100%;object-fit:contain}
.prod h1{font-size:1.8rem;line-height:1.25}
.prod .spec{color:var(--mute);margin:.6rem 0 0;font-size:1rem}
.prod .cat-tag{display:inline-block;font-size:.75rem;letter-spacing:.12em;color:var(--blue);margin-bottom:.6rem}
.rates{margin-top:1.8rem;border-top:2px solid var(--green)}
.rates div{display:flex;justify-content:space-between;align-items:baseline;padding:.7rem 0;border-bottom:1px solid var(--rule)}
.rates dt{font-weight:500}.rates dd{margin:0;font-variant-numeric:tabular-nums;font-size:1.1rem}
.rates dt small{display:block;font-weight:400;color:var(--mute);font-size:.78rem}
.rates .buy dd{color:var(--mute);font-size:1rem}
.flag{margin-top:1rem;font-size:.85rem;color:var(--warn);background:#F6EBDD;padding:.6rem .8rem;border-radius:3px}
.prod .btn{margin-top:1.6rem}
.also{padding-top:.5rem}

/* policy */
.policy-list{display:grid;gap:1rem;max-width:720px}
@media (min-width:720px){.policy-list{grid-template-columns:1fr 1fr;gap:1.25rem}}
.policy-list div{background:var(--paper);border:1px solid var(--rule);border-radius:4px;padding:1.1rem 1.2rem}
.policy-list h3{font-size:1.05rem;margin-bottom:.3rem}
.policy-list p{margin:0;color:var(--mute);font-size:.9rem}

footer{background:var(--green);color:var(--green-ink);padding-block:2.5rem;font-size:.9rem}
footer .wrap{display:grid;gap:1.5rem}
@media (min-width:720px){footer .wrap{grid-template-columns:1fr 1fr 1fr}}
footer p{margin:.2rem 0}footer a{color:#fff}
footer .fh{font-family:"Noto Serif TC",serif;font-size:1.05rem;margin-bottom:.4rem}
footer .note{opacity:.6;font-size:.75rem;grid-column:1/-1;margin-top:.5rem}
.callbar{position:sticky;bottom:0;background:var(--green);padding:.6rem 20px;border-top:1px solid rgba(255,255,255,.2);z-index:15}
.callbar .call{display:block;text-align:center;background:var(--green-ink);color:var(--green);text-decoration:none;font-weight:700;padding:.75rem;border-radius:3px}
@media (min-width:860px){.callbar{display:none}}
@media (prefers-reduced-motion:reduce){*{transition:none!important}}
</style>

<div class="ribbon">網站重建示意 · 方向 A ｜ Rebuild prototype · Direction A</div>
<header>
  <div class="wrap">
    <a class="brand" href="#/">租八借<small>{BR_SUB}</small></a>
    <nav class="main" aria-label="Main">
      <a href="#/" data-nav="home">{NAV_HOME}</a>
      <div class="dd" id="dd">
        <button type="button" id="dd-btn" aria-haspopup="true" aria-expanded="false">{NAV_RENT}</button>
        <div class="dd-menu" id="dd-menu">{DD_LINKS}</div>
      </div>
      <a href="#/policy" data-nav="policy">{NAV_POLICY}</a>
      <a href="#/contact" data-nav="contact">{NAV_CONTACT}</a>
    </nav>
    <div class="lang" role="group" aria-label="Language 語言"><button type="button" id="lang-zh" data-lang="zh" aria-pressed="true">中文</button><button type="button" id="lang-en" data-lang="en" aria-pressed="false">EN</button></div>
    <a class="callhead" href="tel:+886228230080">02-2823-0080</a>
    <button type="button" class="burger" id="burger" aria-label="Menu" aria-expanded="false"><span></span><span></span><span></span></button>
  </div>
  <div class="drawer" id="drawer">
    <a href="#/">{NAV_HOME}</a>
    <div class="grp">{NAV_RENT}</div>
    <div class="sub">{DRAWER_LINKS}</div>
    <a href="#/policy">{NAV_POLICY}</a>
    <a href="#/contact">{NAV_CONTACT}</a>
  </div>
</header>

<main>
<!-- HOME -->
<div class="page" id="page-home">
  <div class="hero"><div class="wrap">
    <div>
      <h1>{HERO_H1}</h1>
      <p>{HERO_P}</p>
      <div class="hero-cta"><a class="btn" href="#/rent/camping">{CTA_BROWSE}</a><a class="btn ghost" href="tel:+886228230080">{CTA_CALL}</a></div>
      <div class="hours-note">{HOURS_NOTE}</div>
    </div>
    <div class="mosaic">
      <img class="m1" src="photos/big74.jpg" alt="">
      <img src="photos/big17.jpg" alt="">
      <img src="photos/big16.jpg" alt="">
    </div>
  </div></div>
  <section><div class="wrap">
        <h2>{H_CATS}</h2>
    <div class="cats">{CAT_CARDS}</div>
  </div></section>
  <section class="band"><div class="wrap">
        <h2>{H_HOW}</h2>
    <div class="steps">{STEPS}</div>
  </div></section>
  <section><div class="wrap info">
    <div>
            <h2>{H_HOURS}</h2>
      <dl class="hours">{HOURS_ROWS}</dl>
    </div>
    <div class="addr">
            <h2>{H_FIND}</h2>
      <p>{ADDR}</p>
      <p>{MRT}</p>
      <p style="margin-top:1rem"><a class="btn ghost" href="#/contact">{CTA_CONTACT}</a></p>
    </div>
  </div></section>
</div>

<!-- CATALOG -->
<div class="page" id="page-cat">
  <div class="wrap">
    <div class="cat-head">
            <h1 id="cat-title"></h1>
      <p id="cat-desc"></p>
      <div class="subnav" id="subnav"></div>
    </div>
    <div class="grid" id="grid"></div>
  </div>
</div>

<!-- PRODUCT -->
<div class="page" id="page-prod">
  <div class="wrap">
    <div class="crumbs" id="crumbs"></div>
    <div class="prod" id="prod"></div>
  </div>
</div>

<!-- POLICY -->
<div class="page" id="page-policy">
  <section><div class="wrap">
        <h2>{H_POLICY}</h2>
    <p class="lead" style="margin-bottom:2rem">{POLICY_LEAD}</p>
    <div class="policy-list">{POLICY_ITEMS}</div>
  </div></section>
</div>

<!-- CONTACT -->
<div class="page page-contact" id="page-contact">
  <section><div class="wrap info">
    <div>
            <h2>{H_CONTACT}</h2>
      <div class="addr">
        <p><strong>租八借</strong></p>
        <p>{ADDR}</p>
        <p>{MRT}</p>
        <p style="margin-top:1rem">{TEL} <a href="tel:+886228230080">02-2823-0080</a></p>
        <p>{FAX} 02-2821-0278</p>
        <p>Email <a href="mailto:suntreeyang@gmail.com">suntreeyang@gmail.com</a></p>
      </div>
    </div>
    <div>
            <h2>{H_HOURS}</h2>
      <dl class="hours">{HOURS_ROWS}</dl>
    </div>
  </div></section>
</div>
</main>

<footer><div class="wrap">
  <div><div class="fh">租八借</div><p>{ADDR}</p><p>{MRT}</p></div>
  <div><div class="fh">{NAV_CONTACT}</div><p><a href="tel:+886228230080">02-2823-0080</a></p><p><a href="mailto:suntreeyang@gmail.com">suntreeyang@gmail.com</a></p></div>
  <div><div class="fh">{H_HOURS}</div><p>{HOURS_SHORT1}</p><p>{HOURS_SHORT2}</p></div>
  <p class="note">{FOOT_NOTE}</p>
</div></footer>
<div class="callbar"><a class="call" href="tel:+886228230080">{CTA_CALL}</a></div>

<script>
const ITEMS = {DATA};
const CATS = [
  {slug:'camping', page:'camping.htm', zh:'露營裝備', en:'Camping', dzh:'帳篷、睡袋、睡墊、桌椅、爐具、燈具，兩天一夜起租。', den:'Tents, sleeping bags, pads, tables and chairs, stoves and lighting. Rent from 2 days / 1 night.', photo:'p74'},
  {slug:'mountain', page:'mount_2.htm', zh:'登山裝備', en:'Mountain', dzh:'登山帳、大背包、羽絨睡袋、雨衣、冰爪、爐頭。', den:'Backpacking tents, packs, down bags, rain shells, crampons, stoves.', photo:'p83'},
  {slug:'river', page:'river.htm', zh:'溯溪裝備', en:'River tracing', dzh:'溯溪鞋、防寒衣、救生衣、頭盔、吊帶與繩索。', den:'River shoes, wetsuits, PFDs, helmets, harnesses and rope.', photo:'p17'},
  {slug:'water', page:'water.htm', zh:'水上裝備', en:'Water', dzh:'獨木舟、救生衣、救生圈、防寒衣。獨木舟須自取。', den:'Kayaks, PFDs, life rings, wetsuits. Kayaks are collect-in-person only.', photo:'p16'},
  {slug:'other', page:'another.htm', zh:'其他裝備', en:'Other', dzh:'冰桶、手推車、園藝工具、大聲公、旅行箱。', den:'Coolers, carts, garden tools, megaphone, suitcases.', photo:'p56'}
];
const TIERS=[{k:'d2',zh:'兩天一夜',en:'2 days / 1 night',szh:'基本租金',sen:'base rate'},{k:'add',zh:'每加一日',en:'Each extra day',szh:'超過兩天一夜後',sen:'beyond 2D1N'},{k:'d5',zh:'五至十天',en:'5–10 days',szh:'包價',sen:'flat rate'},{k:'mo',zh:'月租',en:'Monthly',szh:'30 天包價',sen:'30-day flat rate'},{k:'sale',zh:'售價',en:'Buy',szh:'購買（非租金）',sen:'purchase, not rent',cls:'buy'}];
const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const bi=(zh,en)=>`<span class="zh">${esc(zh)}</span><span class="en">${esc(en)}</span>`;
const fmt=n=>n?'NT$'+n.toLocaleString('en-US'):'—';
const catBy=s=>CATS.find(c=>c.slug===s);
const img=(it,cls)=>it.photo?`<img src="photos/${it.photo}.jpg" alt="" loading="lazy">`:`<div class="ph">${bi('尚無照片','No photo yet')}</div>`;

function show(id){document.querySelectorAll('.page').forEach(p=>p.classList.toggle('active',p.id===id));window.scrollTo(0,0);}
function setNav(key){document.querySelectorAll('[data-nav]').forEach(a=>{if(a.dataset.nav===key)a.setAttribute('aria-current','page');else a.removeAttribute('aria-current');});document.getElementById('dd-btn').style.background=key==='rent'?'rgba(255,255,255,.12)':'';}
function renderCat(slug){
  const c=catBy(slug); if(!c) return route('/');
  document.getElementById('cat-title').innerHTML=bi(c.zh,c.en);
  document.getElementById('cat-desc').innerHTML=bi(c.dzh,c.den);
  document.getElementById('subnav').innerHTML=CATS.map(x=>`<a href="#/rent/${x.slug}"${x.slug===slug?' aria-current="page"':''}>${bi(x.zh,x.en)}</a>`).join('');
  const rows=ITEMS.filter(i=>i.page===c.page);
  document.getElementById('grid').innerHTML=rows.map(it=>`<a class="card" href="#/rent/${slug}/${it.id}">
    <div class="im">${img(it)}</div>
    <div class="t"><h3>${bi(it.zh,it.en)}</h3><div class="spec">${bi(it.spec,it.specen)}</div>
    <div class="price">${bi('兩天一夜','2 days / 1 night')} <b>${fmt(it.d2)}</b></div></div></a>`).join('');
  show('page-cat'); setNav('rent');
}
function renderProd(slug,id){
  const c=catBy(slug), it=ITEMS.find(i=>i.id===id); if(!c||!it) return route('/');
  document.getElementById('crumbs').innerHTML=`<a href="#/">${bi('首頁','Home')}</a> › <a href="#/rent/${slug}">${bi(c.zh,c.en)}</a> › ${bi(it.zh,it.en)}`;
  document.getElementById('prod').innerHTML=`<div class="im">${img(it)}</div>
   <div>
    <span class="cat-tag">${bi(c.zh,c.en)}</span>
    <h1>${bi(it.zh,it.en)}</h1>
    ${it.spec?`<p class="spec">${bi(it.spec,it.specen)}</p>`:''}
    <dl class="rates">${TIERS.map(t=>`<div class="${t.cls||''}"><dt>${bi(t.zh,t.en)}<small>${bi(t.szh,t.sen)}</small></dt><dd>${fmt(it[t.k])}</dd></div>`).join('')}</dl>
    ${it.conf?`<div class="flag">${bi('舊網站兩頁的價格不同，以上為本頁數字，待老闆確認。','The old site lists two different prices for this item. Figures above are from this page, pending confirmation.')}</div>`:''}
    <a class="btn" href="tel:+886228230080">${bi('電話預約 02-2823-0080','Call to reserve 02-2823-0080')}</a>
   </div>`;
  show('page-prod'); setNav('rent');
}
function route(){
  const h=location.hash.replace(/^#/,'')||'/'; const p=h.split('/').filter(Boolean);
  closeMenus();
  if(p.length===0){show('page-home');setNav('home');}
  else if(p[0]==='rent'&&p.length===2) renderCat(p[1]);
  else if(p[0]==='rent'&&p.length===3) renderProd(p[1],p[2]);
  else if(p[0]==='policy'){show('page-policy');setNav('policy');}
  else if(p[0]==='contact'){show('page-contact');setNav('contact');}
  else {location.hash='#/';}
}
function closeMenus(){document.getElementById('drawer').classList.remove('open');document.getElementById('burger').setAttribute('aria-expanded','false');document.getElementById('dd').classList.remove('open');document.getElementById('dd-btn').setAttribute('aria-expanded','false');}
function setLang(l){document.documentElement.lang=l==='en'?'en':'zh-Hant-TW';document.body.classList.toggle('en',l==='en');document.querySelectorAll('.lang button').forEach(b=>b.setAttribute('aria-pressed',b.dataset.lang===l));try{localStorage.setItem('zbj-lang',l)}catch(e){}}
document.addEventListener('DOMContentLoaded',()=>{
  document.querySelectorAll('.lang button').forEach(b=>b.addEventListener('click',()=>setLang(b.dataset.lang)));
  let l='zh';try{l=localStorage.getItem('zbj-lang')||'zh'}catch(e){} setLang(l);
  document.getElementById('burger').addEventListener('click',e=>{const d=document.getElementById('drawer');const o=!d.classList.contains('open');d.classList.toggle('open',o);e.currentTarget.setAttribute('aria-expanded',o);});
  document.getElementById('dd-btn').addEventListener('click',e=>{const d=document.getElementById('dd');const o=!d.classList.contains('open');d.classList.toggle('open',o);e.currentTarget.setAttribute('aria-expanded',o);});
  document.addEventListener('click',e=>{if(!e.target.closest('#dd'))document.getElementById('dd').classList.remove('open');});
  window.addEventListener('hashchange',route); route();
});
</script>'''

HOURS_ROWS = [('週一、二、四、五','Mon, Tue, Thu, Fri','10:00–20:00'),('週六','Saturday','10:00–15:00'),('國定假日','Public holidays','10:00–19:00'),('週三、週日','Wednesday & Sunday',bi('公休','Closed'))]
POLICY = [('押金','Deposit'),('證件','ID'),('歸還時間','Return time'),('損壞與遺失','Damage and loss'),('清潔','Cleaning'),('逾期','Late return')]
cat_defs = [('camping','露營裝備','Camping','big74'),('mountain','登山裝備','Mountain','big83'),('river','溯溪裝備','River tracing','big17'),('water','水上裝備','Water','big16'),('other','其他裝備','Other','p56')]
counts = {'camping':49,'mountain':44,'river':16,'water':9,'other':13}

rep = {
 'BR_SUB': bi('北投 · 戶外裝備出租','BEITOU · OUTDOOR GEAR RENTAL'),
 'NAV_HOME': bi('首頁','Home'), 'NAV_RENT': bi('租借裝備','Rent gear'), 'NAV_POLICY': bi('租借規則','Rental policy'), 'NAV_CONTACT': bi('聯絡我們','Contact'),
 'DD_LINKS': ''.join(f'<a href="#/rent/{s}">{bi(z,e)}<small>{counts[s]}</small></a>' for s,z,e,_ in cat_defs),
 'DRAWER_LINKS': ''.join(f'<a href="#/rent/{s}">{bi(z,e)}</a>' for s,z,e,_ in cat_defs),
 'HERO_H1': bi('北投戶外裝備出租','Outdoor gear rental in Beitou'),
 'HERO_P': bi('露營、登山、溯溪、水上裝備。電話預約，到店取還。','Camping, hiking, river-tracing and water gear. Book by phone, pick up in store.'),
 'CTA_BROWSE': bi('裝備與價格','Gear and prices'), 'CTA_CALL': bi('撥打 02-2823-0080','Call 02-2823-0080'), 'CTA_CONTACT': bi('聯絡與交通','Contact and directions'),
 'HOURS_NOTE': bi('週三、週日公休 · 週六 15:00 打烊','Closed Wed & Sun · Saturday closes 15:00'),
 'EB_RENT': bi('租借裝備','Rent gear'), 'H_CATS': bi('租借裝備','Rent gear'),
 'CAT_CARDS': ''.join(f'<a class="cat" href="#/rent/{s}"><div class="im"><img src="photos/{ph}.jpg" alt=""></div><div class="t"><h3>{bi(z,e)}</h3><small>{bi(str(counts[s])+" 項","%d items"%counts[s])}</small></div></a>' for s,z,e,ph in cat_defs),
 'EB_HOW': '', 'H_HOW': bi('如何租借','How to rent'),
 'STEPS': ''.join(f'<div class="step"><div class="n">{n}</div><h3>{bi(z,e)}</h3><p>{bi(dz,de)}</p></div>' for n,z,e,dz,de in [
   ('一','打電話預約','Call to reserve','告訴我們日期和需要的裝備，我們幫你留。','Tell us the dates and what you need; we hold it for you.'),
   ('二','到店取件','Pick up in store','捷運唭哩岸站步行 4 分鐘。鞋子、防寒衣可現場試穿。','4 minutes on foot from MRT Qilian. Try on shoes and wetsuits in the shop.'),
   ('三','歸還','Return','營業時間內送回店裡。','Return to the shop during opening hours.')]),
 'EB_HOURS': bi('營業時間','Opening hours'), 'H_HOURS': bi('營業時間','Opening hours'),
 'HOURS_ROWS': ''.join(f'<div><dt>{bi(z,e)}</dt><dd>{t}</dd></div>' for z,e,t in HOURS_ROWS),
 'EB_FIND': bi('店面位置','Where we are'), 'H_FIND': bi('店面位置','Location'),
 'ADDR': bi('台北市北投區東華街二段210號','No. 210, Sec. 2, Donghua St, Beitou District, Taipei'),
 'MRT': bi('捷運淡水信義線 唭哩岸站，步行約 4 分鐘','MRT Red Line, Qilian station, about 4 minutes on foot'),
 'EB_POLICY': bi('租借規則','Rental policy'), 'H_POLICY': bi('租借規則','Rental policy'),
 'POLICY_LEAD': bi('租借前先知道的事。每一項的內容都要和老闆確認後才會放上來。','What to know before you rent. Each item below is written once confirmed with the owner.'),
 'POLICY_ITEMS': ''.join(f'<div><h3>{bi(z,e)}</h3><p>{bi("內容待與老闆確認。","To be confirmed with the owner.")}</p></div>' for z,e in POLICY),
 'EB_CONTACT': bi('聯絡我們','Contact'), 'H_CONTACT': bi('聯絡我們','Contact'),
 'TEL': bi('電話','Tel'), 'FAX': bi('傳真','Fax'),
 'HOURS_SHORT1': bi('週一、二、四、五 10:00–20:00 · 週六 10:00–15:00','Mon Tue Thu Fri 10:00–20:00 · Sat 10:00–15:00'),
 'HOURS_SHORT2': bi('國定假日 10:00–19:00 · 週三、週日公休','Holidays 10:00–19:00 · Closed Wed & Sun'),
 'FOOT_NOTE': bi('網站重建示意頁，非正式網站。價格逐字取自舊站 dbk.url.tw，尚未經老闆確認。','Rebuild prototype, not the live site. Prices copied verbatim from the old site dbk.url.tw and not yet confirmed by the owner.'),
 'DATA': data,
}
out = HTML
for k,v in rep.items(): out = out.replace('{'+k+'}', v)
(S/'zubajie-site.html').write_text(out)
print('ok', len(out))
