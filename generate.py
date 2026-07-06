#!/usr/bin/env python3
"""
Veyron landing-page engine v2.
Matches the real brand: /veyron-logo.png (+ white), Cormorant Garamond (serif) + Inter (body),
real product photos by slug. Clean subdomain names (no dashes). Product pages link straight to the
product (add-to-cart on the real site), niche pages to the catalog. Distinct FEELS for A/B.
Run: python3 generate.py
"""
SITE = "https://veyronbiologics.com"
GOLD = "#b8912f"
FONTS = ("<link rel=preconnect href=https://fonts.googleapis.com>"
         "<link href='https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap' rel=stylesheet>")
SERIF = "'Cormorant Garamond',Georgia,serif"
SANS = "'Inter',system-ui,sans-serif"
MONO = "'JetBrains Mono',monospace"

RUOBAR = 'FOR LABORATORY &amp; RESEARCH USE ONLY · NOT FOR HUMAN OR ANIMAL CONSUMPTION · 21+ QUALIFIED RESEARCHERS'
DISC = ('<strong>Research Use Only.</strong> All products sold by Veyron Biologics are for laboratory and research use only — '
        'not drugs, foods, or supplements, and <strong>not for human or animal consumption</strong>. Nothing here is medical '
        'advice, a therapeutic claim, or dosing guidance. Figures describe outcomes reported in published third-party research, '
        'given solely as scientific context. By purchasing you affirm you are 21+ and a qualified researcher.')

def logo(dark=False):
    f = "veyron-logo-white.png" if dark else "veyron-logo.png"
    return f'<a href="{SITE}"><img src="{SITE}/{f}" alt="Veyron Biologics" style="height:34px;width:auto;display:block"></a>'

def img_tag(slug, cls=""):
    return f'<img class="{cls}" src="{SITE}/products/{slug}.webp" alt="{slug} research vial" loading="lazy" onerror="this.onerror=null;this.src=\'{SITE}/products/{slug}.png\'">'

def dest(p):  # product pages → straight to the product; niches → catalog
    return f'{SITE}/product/{p["slug"]}?tr={p["tr"]}' if p.get("slug") else f'{SITE}/catalog?tr={p["tr"]}'

def cta(p, label=None):
    lbl = label or (f'Add {p["name"]} to cart →' if p.get("slug") else "Shop the catalog →")
    return f'<a class="btn" href="{dest(p)}">{lbl}</a>'

# ── CONTENT ─────────────────────────────────────────────────────────────────────
# img = image file (by product slug); slug = product page slug (None = niche → catalog).
# what/why = education blocks (Cam wants real info). stat = headline number.
PAGES = [
 dict(file="reta", tpl="editorial", tr="reta", slug="retatrutide", img="retatrutide", name="Retatrutide",
   klass='"GLP-3" · triple-agonist', hook="The research compound that made <em>GLP-1 look like a warm-up.</em>",
   sub="Retatrutide is the triple-hormone agonist the field is calling \"GLP-3\" — and in published research it left the previous generation behind.",
   stat="~24%", statlabel="mean body-weight reduction reported in 48-week research",
   what="Retatrutide is a single molecule that acts on three receptors at once — GLP-1, GIP, and glucagon. Where semaglutide (GLP-1) hits one target and tirzepatide (GLP-2 class) hits two, the triple-agonist engages all three pathways implicated in metabolic research.",
   why="In the published literature, the triple-agonist didn't just improve on its predecessors — it reset the ceiling. Research on obese study subjects reported roughly 24% mean body-weight reduction over 48 weeks, with figures some researchers compared to bariatric outcomes."),
 dict(file="tirz", tpl="bold", tr="tirz", slug="tirzepatide", img="tirzepatide", name="Tirzepatide",
   klass="dual-agonist · GLP-1 + GIP", hook="The dual-agonist workhorse.",
   sub="The GLP-1 + GIP combination that became the research standard before the triple-agonist arrived — proven, dependable, decisive.",
   stat="~21%", statlabel="mean reduction reported in trials",
   what="Tirzepatide activates two incretin receptors — GLP-1 and GIP. The dual mechanism made it a clear step up over single-agonist research, and it remains the reference point the newer compounds are measured against.",
   why="The most-studied dual-agonist in the space, with the deepest body of research data behind it. When a study needs a proven benchmark, this is it."),
 dict(file="sema", tpl="clinical", tr="sema", slug="semaglutide", img="semaglutide", name="Semaglutide",
   klass="GLP-1 · the baseline", hook="Where the whole category started.",
   sub="The single-agonist that launched the incretin era. Well-studied, dependable — the entry point to the metabolic research line.",
   stat="~15%", statlabel="mean reduction reported in trials",
   what="Semaglutide is a GLP-1 receptor agonist — the first-generation incretin the entire modern category was built on. The single-agonist baseline every later compound is compared against.",
   why="The most extensively researched compound in the class, with years of published data. The dependable starting point for incretin research."),
 dict(file="cagri", tpl="bold", tr="cagri", slug="cagrilintide", img="cagrilintide", name="Cagrilintide",
   klass="amylin analog · stack partner", hook="The amylin analog the newest research is built around.",
   sub="The compound researchers pair with the incretins — the combination driving the latest metabolic studies.",
   stat="Stack", statlabel="the research favorite for combination work",
   what="Cagrilintide is a long-acting amylin analog — a different mechanism from the incretins. That's exactly why it's the pairing partner: researchers stack it with GLP-1/GIP compounds to study combined pathways.",
   why="The newest wave of metabolic research is built on combinations, and cagrilintide is the amylin half of the most-studied pairings."),
 dict(file="nad", tpl="clinical", tr="nad", slug="nad", img="nad-plus", name="NAD+",
   klass="cellular · longevity research", hook="The molecule at the center of the longevity conversation.",
   sub="Central to cellular energy and sirtuin research — the compound the aging field keeps coming back to.",
   stat="Sirtuins", statlabel="the pathway NAD+ research centers on",
   what="NAD+ (nicotinamide adenine dinucleotide) is a coenzyme found in every living cell, central to energy metabolism and the activity of sirtuins — the proteins at the heart of cellular-aging research.",
   why="NAD+ levels are a recurring variable in longevity studies. It's one of the most-cited molecules in the cellular-aging literature, which is why it anchors the research."),
 dict(file="ghk", tpl="minimal", tr="ghk", slug="ghk-cu", img="ghk-cu", name="GHK-Cu",
   klass="copper peptide · repair research", hook="The copper peptide the repair literature won't stop citing.",
   sub="Studied for its role in tissue-repair and regenerative signaling — one of the most-referenced peptides in the field.",
   stat="~33%", statlabel="faster repair reported in research models",
   what="GHK-Cu is a copper-binding tripeptide naturally present in human plasma. Research associates it with tissue-repair signaling and gene-expression pathways tied to regeneration.",
   why="Few peptides have GHK-Cu's depth of repair-and-regeneration research behind them — including studies reporting influence over thousands of genes tied to tissue repair."),
 dict(file="klow", tpl="bold", tr="klow", slug="klow", img="klow", name="KLOW",
   klass="research blend · GHK / KPV / BPC / TB-500", hook="Four research peptides. One vial.",
   sub="A blend built from the repair-and-recovery compounds the research community stacks by hand — pre-combined and COA-verified.",
   stat="4-in-1", statlabel="the convenience of a pre-built research blend",
   what="KLOW combines four of the most-studied repair-and-recovery research peptides — GHK-Cu, KPV, BPC-157, and TB-500 — in a single lyophilized vial.",
   why="Researchers who'd otherwise reconstitute four separate compounds get one COA-verified blend. Convenience without giving up the transparency."),
 # ---- NICHE (catalog) ----
 dict(file="weightloss", tpl="offer", tr="weightloss", slug=None, img="retatrutide", name="Metabolic Stack",
   klass="the metabolic research line", hook="The compounds the entire metabolic field <em>can't stop talking about.</em>",
   sub="Retatrutide. Tirzepatide. Cagrilintide. The incretin research everyone's chasing — sourced right, tested to the decimal.",
   stat="", statlabel="", products=[("retatrutide","Retatrutide"),("tirzepatide","Tirzepatide"),("cagrilintide","Cagrilintide")]),
 dict(file="longevity", tpl="offer", tr="longevity", slug=None, img="nad-plus", name="Longevity Line",
   klass="the longevity research line", hook="The compounds the longevity field <em>can't stop studying.</em>",
   sub="NAD+, GHK-Cu, Epithalon — the cellular-aging research everyone's chasing, tested to the decimal.",
   stat="", statlabel="", products=[("nad","NAD+"),("ghk-cu","GHK-Cu"),("epithalon","Epithalon")]),
 dict(file="recovery", tpl="offer", tr="recovery", slug=None, img="klow", name="Recovery Line",
   klass="the recovery research line", hook="The repair-and-recovery research stack.",
   sub="BPC-157, TB-500, KLOW — the tissue-repair compounds the research community relies on.",
   stat="", statlabel="", products=[("wolverine","BPC-157 / TB-500"),("klow","KLOW"),("ghk-cu","GHK-Cu")]),
 dict(file="buy", tpl="minimal", tr="buy", slug=None, img="retatrutide", name="Veyron Biologics",
   klass="research-grade · verifiable", hook="The research peptides you can <em>actually verify.</em>",
   sub="99%+ HPLC purity. QR-verified COA on every vial. A lab we name. The reference-grade version.",
   stat="99%+", statlabel="HPLC-verified purity"),
]

TRUST = ("<span><b>99%+</b> HPLC purity</span><span><b>QR-verified COA</b> per vial</span>"
         "<span><b>Lab named</b> · verify it yourself</span><span><b>USA</b> made &amp; shipped</span>")

def head(title, dark=False):
    bg = "#0f0d09" if dark else "#faf8f2"; ink = "#f3efe4" if dark else "#161310"
    return f"""<!DOCTYPE html><html lang=en><head><meta charset=UTF-8><meta name=viewport content="width=device-width,initial-scale=1">
<title>{title} | Veyron Biologics</title>{FONTS}<style>
*{{margin:0;padding:0;box-sizing:border-box}}body{{font:16px/1.65 {SANS};background:{bg};color:{ink}}}
.wrap{{max-width:1040px;margin:0 auto;padding:0 22px}}a{{color:inherit}}h1,h2,h3,.serif{{font-family:{SERIF};font-weight:500}}
.btn{{display:inline-block;background:{GOLD};color:#12100c;font-weight:700;font-family:{SANS};letter-spacing:.4px;text-transform:uppercase;text-decoration:none;padding:15px 34px;border-radius:6px;font-size:14px;box-shadow:0 8px 22px rgba(184,145,47,.3)}}
.ruo{{background:#12100c;color:#8f8877;font-size:11.5px;text-align:center;padding:8px;letter-spacing:.4px}}
nav{{padding:14px 0;border-bottom:1px solid {'#221e15' if dark else '#e7e1d3'}}}nav .wrap{{display:flex;justify-content:space-between;align-items:center}}
.kick{{color:{GOLD};font-family:{MONO};font-size:12px;letter-spacing:2px;text-transform:uppercase}}
</style></head><body><div class=ruo>{RUOBAR}</div>"""

FOOT = lambda dark: f'<footer style="border-top:1px solid {"#221e15" if dark else "#e7e1d3"};color:{"#7d7768" if dark else "#8f8877"};font-size:12.5px;padding:30px 0;line-height:1.7"><div class=wrap><p style="border:1px solid {"#221e15" if dark else "#e7e1d3"};border-radius:8px;padding:16px;margin-bottom:12px">{DISC}</p><a href="{SITE}" style="color:{GOLD};text-decoration:none">© Veyron Biologics · veyronbiologics.com</a></div></footer></body></html>'

# ── TEMPLATES (distinct feels, shared brand) ─────────────────────────────────────
def content_block(p, dark=False):
    line = "#221e15" if dark else "#e7e1d3"; mut = "#a79f8d" if dark else "#6b6455"
    return f"""<section style="padding:20px 0 50px"><div class=wrap style="max-width:760px">
    <div style="border-top:1px solid {line};padding-top:30px"><p class=kick>What it is</p><h2 style="font-size:28px;margin:6px 0 10px">{p['name']}</h2><p style="color:{mut};font-size:17px">{p['what']}</p></div>
    <div style="border-top:1px solid {line};padding-top:26px;margin-top:30px"><p class=kick>Why researchers use it</p><p style="color:{mut};font-size:17px;margin-top:8px">{p['why']}</p></div>
    </div></section>"""

def tpl_editorial(p):
    return head(p['name'],False)+f"""<nav><div class=wrap>{logo()}{cta(p,'Shop')}</div></nav>
<header style="padding:56px 0 40px"><div class=wrap style="display:grid;grid-template-columns:1.1fr .9fr;gap:40px;align-items:center">
<div><p class=kick>{p['klass']}</p><h1 style="font-size:clamp(32px,5vw,50px);line-height:1.08;margin:12px 0 16px">{p['hook']}</h1><p style="font-size:18px;color:#6b6455;margin-bottom:26px">{p['sub']}</p>{cta(p)}
<div style="display:flex;gap:18px;flex-wrap:wrap;margin-top:22px;font-size:13px;color:#6b6455">{TRUST}</div></div>
<div style="text-align:center;background:radial-gradient(circle at 50% 40%,#fff,#efe9db);border:1px solid #e7e1d3;border-radius:16px;padding:22px">{img_tag(p['img'],'')}<style>header img{{max-width:70%}}</style></div>
</div></header>{content_block(p,False)}
<section style="padding:44px 0;background:#fff;border-top:1px solid #e7e1d3;text-align:center"><div class=wrap><h2 style="font-size:30px">25% off your first order</h2><p style="color:#6b6455;margin:6px 0 22px">Code <b style="color:{GOLD};font-family:{MONO}">FIRST25</b> — automatic. Free shipping over $200.</p>{cta(p)}</div></section>{FOOT(False)}"""

def tpl_bold(p):
    return head(p['name'],True)+f"""<nav><div class=wrap>{logo(True)}{cta(p,'Shop')}</div></nav>
<header style="padding:64px 0"><div class=wrap style="display:grid;grid-template-columns:1fr 1fr;gap:40px;align-items:center">
<div><p class=kick>{p['klass']}</p><h1 style="font-size:clamp(40px,6.5vw,66px);line-height:1.02;margin:14px 0 16px">{p['hook']}</h1><p style="font-size:19px;color:#a79f8d;margin-bottom:28px">{p['sub']}</p>{cta(p)}</div>
<div style="text-align:center">{img_tag(p['img'])}<style>header img{{max-width:76%}}</style></div></div></header>
<div style="border-top:1px solid #221e15;border-bottom:1px solid #221e15;text-align:center;padding:36px 0"><div class=wrap><div style="font-family:{SERIF};font-size:60px;color:{GOLD}">{p['stat']}</div><p style="color:#a79f8d;text-transform:uppercase;letter-spacing:1px;font-size:12px">{p['statlabel']}</p></div></div>
{content_block(p,True)}
<div style="display:flex;justify-content:center;gap:28px;flex-wrap:wrap;padding:34px 0;color:#a79f8d;font-size:14px"><div class=wrap style="display:flex;justify-content:center;gap:28px;flex-wrap:wrap">{TRUST}</div></div>
<section style="text-align:center;padding:48px 0;border-top:1px solid #221e15"><div class=wrap><h2 style="font-size:32px">25% off your first order</h2><p style="color:#a79f8d;margin:6px 0 22px">Code <b style="color:{GOLD};font-family:{MONO}">FIRST25</b> — automatic. Free shipping over $200.</p>{cta(p)}</div></section>{FOOT(True)}"""

def tpl_clinical(p):
    return head(p['name'],False)+f"""<nav style="background:#fff"><div class=wrap>{logo()}{cta(p,'Shop')}</div></nav>
<header style="padding:52px 0;text-align:center"><div class=wrap><p class=kick>{p['klass']}</p><h1 style="font-size:clamp(30px,4.6vw,44px);line-height:1.1;max-width:760px;margin:12px auto 14px">{p['hook']}</h1><p style="font-size:18px;color:#6b6455;max-width:600px;margin:0 auto 22px">{p['sub']}</p>{cta(p)}<div style="margin-top:22px">{img_tag(p['img'])}<style>header img{{max-width:150px}}</style></div></div></header>
<div class=wrap><div style="display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-bottom:10px">
<div style="background:#fff;border:1px solid #e7e1d3;border-radius:12px;padding:24px;text-align:center"><div style="font-family:{SERIF};font-size:34px;color:{GOLD}">{p['stat']}</div><p style="font-size:13.5px;color:#6b6455;margin-top:4px">{p['statlabel']}</p></div>
<div style="background:#fff;border:1px solid #e7e1d3;border-radius:12px;padding:24px;text-align:center"><div style="font-family:{SERIF};font-size:34px;color:{GOLD}">99%+</div><p style="font-size:13.5px;color:#6b6455;margin-top:4px">HPLC-verified purity, to the decimal</p></div>
<div style="background:#fff;border:1px solid #e7e1d3;border-radius:12px;padding:24px;text-align:center"><div style="font-family:{SERIF};font-size:34px;color:{GOLD}">COA</div><p style="font-size:13.5px;color:#6b6455;margin-top:4px">QR-verified, per lot, lab named</p></div>
</div></div>{content_block(p,False)}
<section style="text-align:center;padding:44px 0;background:#fff;border-top:1px solid #e7e1d3"><div class=wrap><h2 style="font-size:30px">25% off your first order</h2><p style="color:#6b6455;margin:6px 0 22px">Code <b style="color:{GOLD};font-family:{MONO}">FIRST25</b> — automatic. Free shipping over $200.</p>{cta(p)}</div></section>{FOOT(False)}"""

def tpl_minimal(p):
    return head(p['name'],False)+f"""<main style="min-height:72vh;display:flex;align-items:center;justify-content:center;text-align:center;padding:40px 22px">
<div style="max-width:620px"><div style="margin-bottom:24px">{logo()}</div><p class=kick>{p['klass']}</p><div style="margin:14px 0 6px">{img_tag(p['img'])}<style>main img{{max-width:150px;margin:0 auto}}</style></div>
<h1 style="font-size:clamp(32px,5.4vw,50px);line-height:1.08;margin-bottom:14px">{p['hook']}</h1><p style="font-size:19px;color:#6b6455;margin-bottom:12px">{p['sub']}</p>
<p style="font-size:15px;margin-bottom:26px">25% off your first order — code <b style="color:{GOLD};font-family:{MONO}">FIRST25</b>, automatic · free shipping over $200</p>{cta(p)}</div></main>{FOOT(False)}"""

def tpl_offer(p):
    cards = ""
    for slug,label in p.get("products",[]):
        cards += f'<a href="{SITE}/product/{slug}?tr={p["tr"]}" style="background:#1a1710;border:1px solid #2c271c;border-radius:14px;padding:22px;text-align:center;text-decoration:none;color:#f3efe4;display:block">{img_tag(slug)}<style>.grid img{{height:120px}}</style><span style="display:block;font-family:{SERIF};font-size:20px;margin:8px 0 4px">{label}</span><em style="color:{GOLD};font-style:normal;font-size:12px;text-transform:uppercase;letter-spacing:.5px">Add to cart →</em></a>'
    return head(p['name'],True)+f"""<div style="background:{GOLD};color:#12100c;text-align:center;font-weight:700;font-size:13px;padding:9px;text-transform:uppercase;letter-spacing:.5px">First order → 25% off with FIRST25 · Free shipping over $200</div>
<nav><div class=wrap>{logo(True)}{cta(p,'Shop')}</div></nav>
<header style="text-align:center;padding:54px 0"><div class=wrap><p class=kick>{p['klass']}</p><h1 style="font-size:clamp(32px,5.6vw,52px);line-height:1.08;max-width:820px;margin:14px auto 16px">{p['hook']}</h1><p style="font-size:18px;color:#a79f8d;max-width:600px;margin:0 auto 28px">{p['sub']}</p>{cta(p,'Shop the line →')}</div></header>
<div class=wrap><div class=grid style="display:grid;grid-template-columns:repeat(3,1fr);gap:16px;padding-bottom:50px">{cards}</div></div>
<section style="text-align:center;padding:44px 0;border-top:1px solid #221e15"><div class=wrap><h2 style="font-size:30px">25% off your first order</h2><p style="color:#a79f8d;margin:6px 0 22px">Code <b style="color:{GOLD};font-family:{MONO}">FIRST25</b>, automatic. Free shipping over $200.</p>{cta(p)}</div></section>
<style>@media(max-width:760px){{.grid{{grid-template-columns:1fr!important}}header div[style*=grid]{{grid-template-columns:1fr!important}}}}</style>{FOOT(True)}"""

TEMPLATES = {"editorial":tpl_editorial,"bold":tpl_bold,"clinical":tpl_clinical,"minimal":tpl_minimal,"offer":tpl_offer}

built=[]
for p in PAGES:
    open(p["file"]+".html","w").write(TEMPLATES[p["tpl"]](p))
    built.append((p["file"],p["tpl"],p["name"]))
rows="".join(f'<a class=card href="{f}.html"><b>{f}.veyronbiologics.com</b><span>{n} · <em>{t}</em></span></a>' for f,t,n in built)
open("index.html","w").write(f"""<!DOCTYPE html><html><head><meta charset=UTF-8><meta name=viewport content="width=device-width,initial-scale=1"><title>Veyron LP Previews</title>{FONTS}
<style>body{{font:16px/1.6 {SANS};background:#0f0d09;color:#f3efe4;margin:0;padding:50px 22px}}.wrap{{max-width:720px;margin:0 auto}}h1{{font-family:{SERIF};font-weight:500;text-align:center}}
a.card{{display:flex;justify-content:space-between;align-items:center;padding:18px 20px;margin:10px 0;border:1px solid #2c271c;border-radius:12px;background:#1a1710;color:#f3efe4;text-decoration:none}}a.card:hover{{border-color:{GOLD}}}a.card b{{color:{GOLD};font-family:{MONO};font-size:14px}}a.card span{{color:#a79f8d;font-size:14px}}a.card em{{color:#f3efe4;font-style:normal}}</style></head>
<body><div class=wrap><h1>Veyron Landing Pages</h1><p style="text-align:center;color:#a79f8d;margin-bottom:26px">Clean names · real brand · distinct feels</p>{rows}</div></body></html>""")
print(f"generated {len(built)} pages:")
for f,t,n in built: print(f"  {f}.veyronbiologics.com  [{t}]  {n}")
