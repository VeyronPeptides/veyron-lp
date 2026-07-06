#!/usr/bin/env python3
"""
Veyron landing-page engine — generates many LPs from content data + swappable templates.
Each page is its own file (→ its own subdomain later). Multiple TEMPLATES = different feels for A/B.
Add a page: append to PAGES. Add a look: add a template function. Run: python3 generate.py
"""
SITE = "https://veyronbiologics.com"
GOLD = "#b8912f"

# ── CONTENT ─────────────────────────────────────────────────────────────────────
# Each page: file, template, tr (attribution key), product slug (for image + link) or None (niche),
# and the copy blocks. Stats are framed as research context, never claims for the vial.
PAGES = [
    # ---- PRODUCT-SPECIFIC (single-focus) ----
    dict(file="reta-bold", tpl="bold", tr="reta-bold", slug="retatrutide", img="reta",
         klass='"GLP-3" · triple-agonist', name="Retatrutide",
         hook="The triple-agonist that reset the ceiling.",
         sub="GLP-1 + GIP + glucagon. In published research it moved the metabolic numbers into a tier of their own.",
         stat="~24%", statlabel="mean reduction reported in 48-week research"),
    dict(file="tirz-clinical", tpl="clinical", tr="tirz-clinical", slug="tirzepatide", img="tirz",
         klass="dual-agonist · GLP-1 + GIP", name="Tirzepatide",
         hook="The dual-agonist workhorse — proven, dependable, decisive.",
         sub="The GLP-1 + GIP combination that became the research standard before the triple-agonist arrived.",
         stat="~21%", statlabel="mean reduction reported in trials"),
    dict(file="sema-minimal", tpl="minimal", tr="sema-minimal", slug="semaglutide", img="semaglutide",
         klass="GLP-1 · the baseline", name="Semaglutide",
         hook="Where the whole category started.",
         sub="The single-agonist that launched the incretin era. Well-studied, dependable, the entry point.",
         stat="~15%", statlabel="mean reduction reported in trials"),
    dict(file="cagri-bold", tpl="bold", tr="cagri-bold", slug="cagrilintide", img="cagrilintide",
         klass="amylin analog · stack partner", name="Cagrilintide",
         hook="The amylin analog the newest research is built around.",
         sub="The compound researchers pair with the incretins — the combination driving the latest metabolic studies.",
         stat="Stack", statlabel="the research favorite"),
    dict(file="nad-clinical", tpl="clinical", tr="nad-clinical", slug="nad", img="nad",
         klass="cellular · longevity research", name="NAD+",
         hook="The molecule at the center of the longevity conversation.",
         sub="Central to cellular energy and sirtuin research — the compound the aging field keeps coming back to.",
         stat="4,000+", statlabel="genes studied in NAD-linked pathways"),
    dict(file="ghk-minimal", tpl="minimal", tr="ghk-minimal", slug="ghk-cu", img="ghk-cu",
         klass="copper peptide · repair research", name="GHK-Cu",
         hook="The copper peptide the repair literature won't stop citing.",
         sub="Studied for its role in tissue-repair and regenerative signaling pathways.",
         stat="~33%", statlabel="faster repair reported in models"),
    dict(file="klow-bold", tpl="bold", tr="klow-bold", slug="klow", img="klow",
         klass="research blend · GHK/KPV/BPC/TB", name="KLOW",
         hook="Four research peptides. One vial.",
         sub="A blend built from the repair-and-recovery compounds the research community stacks by hand.",
         stat="4-in-1", statlabel="the convenience of a pre-built blend"),
    # ---- NICHE / THEME (catalog-forward) ----
    dict(file="longevity", tpl="offer", tr="longevity-lp", slug=None, img="nad",
         klass="the longevity research line", name="Longevity",
         hook="The compounds the longevity field can't stop studying.",
         sub="NAD+, GHK-Cu, Epithalon — the cellular-aging research everyone's chasing, tested to the decimal.",
         stat="", statlabel="", products=["nad","ghk-cu","epithalon"]),
    dict(file="recovery", tpl="offer", tr="recovery-lp", slug=None, img="klow",
         klass="the recovery research line", name="Recovery",
         hook="The repair-and-recovery research stack.",
         sub="BPC-157, TB-500, KLOW — the tissue-repair compounds the research community relies on.",
         stat="", statlabel="", products=["wolverine","klow","ghk-cu"]),
    # ---- GENERIC LANDING ----
    dict(file="buy", tpl="minimal", tr="buy-lp", slug=None, img="reta",
         klass="research-grade · verifiable", name="Veyron Biologics",
         hook="The research peptides you can actually verify.",
         sub="99%+ HPLC purity. QR-verified COA on every vial. A lab we name. This is the reference-grade version.",
         stat="99%+", statlabel="HPLC-verified purity"),
]

RUOBAR = 'FOR LABORATORY &amp; RESEARCH USE ONLY · NOT FOR HUMAN OR ANIMAL CONSUMPTION · 21+ QUALIFIED RESEARCHERS'
DISC = ('<strong>Research Use Only.</strong> All products sold by Veyron Biologics are for laboratory and research use only — '
        'not drugs, foods, or supplements, and <strong>not for human or animal consumption</strong>. Nothing here is medical '
        'advice, a therapeutic claim, or dosing guidance. Figures describe outcomes reported in published third-party research, '
        'given solely as scientific context — not claims about any product sold here. By purchasing you affirm you are 21+ and a '
        'qualified researcher acquiring materials for legitimate in-vitro research.')

def img_tag(img, cls=""):
    return f'<img class="{cls}" src="{SITE}/products/{img}.webp" alt="research vial" onerror="this.onerror=null;this.src=\'{SITE}/products/{img}.png\'">'

def cart(tr, label="Shop the catalog →"):
    return f'<a class="btn" href="{SITE}/catalog?tr={tr}">{label}</a>'

# ── TEMPLATES (each a distinct FEEL) ─────────────────────────────────────────────
def tpl_bold(p):  # feel: black, huge type, single product, high drama
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{p['name']} (RUO) | Veyron Biologics</title><style>
*{{margin:0;padding:0;box-sizing:border-box}}body{{font:16px/1.6 -apple-system,Segoe UI,Roboto,Arial,sans-serif;background:#0a0908;color:#f5f1e6}}
.wrap{{max-width:1000px;margin:0 auto;padding:0 22px}}.ruo{{background:#000;color:#7d7768;font-size:11.5px;text-align:center;padding:8px;letter-spacing:.4px}}
.btn{{display:inline-block;background:{GOLD};color:#0a0908;font-weight:800;text-transform:uppercase;letter-spacing:.5px;text-decoration:none;padding:17px 40px;border-radius:6px;font-size:15px;box-shadow:0 10px 30px rgba(184,145,47,.4)}}
nav{{padding:18px 0;border-bottom:1px solid #221e15}}nav .wrap{{display:flex;justify-content:space-between;align-items:center}}.logo{{font-family:Georgia,serif;font-size:19px;letter-spacing:2px}}.logo b{{color:{GOLD}}}
.hero{{padding:70px 0;display:grid;grid-template-columns:1fr 1fr;gap:40px;align-items:center}}
.tag{{color:{GOLD};font-family:monospace;font-size:12px;letter-spacing:2px;text-transform:uppercase;margin-bottom:16px}}
h1{{font-family:Georgia,serif;font-weight:400;font-size:clamp(38px,6.5vw,64px);line-height:1.03;margin-bottom:18px}}
.sub{{font-size:19px;color:#a79f8d;margin-bottom:30px}}.himg{{text-align:center}}.himg img{{max-width:80%}}
.stat{{border-top:1px solid #221e15;border-bottom:1px solid #221e15;padding:34px 0;text-align:center;margin:0 0 10px}}
.stat .n{{font-family:Georgia,serif;font-size:64px;color:{GOLD};font-weight:700}}.stat p{{color:#a79f8d;text-transform:uppercase;letter-spacing:1px;font-size:13px}}
.tr{{display:flex;justify-content:center;gap:30px;flex-wrap:wrap;padding:40px 0;color:#a79f8d;font-size:14px}}.tr b{{color:{GOLD}}}
.cta{{text-align:center;padding:50px 0}}footer{{border-top:1px solid #221e15;color:#6b6555;font-size:12.5px;padding:30px 0;line-height:1.7}}footer a{{color:{GOLD};text-decoration:none}}
@media(max-width:800px){{.hero{{grid-template-columns:1fr}}.himg{{order:-1}}}}</style></head><body>
<div class="ruo">{RUOBAR}</div>
<nav><div class="wrap"><div class="logo">VEYRON <b>BIOLOGICS</b></div>{cart(p['tr'],"Shop")}</div></nav>
<header class="hero"><div class="wrap" style="display:contents"><div><div class="tag">{p['klass']}</div><h1>{p['hook']}</h1><p class="sub">{p['sub']}</p>{cart(p['tr'], f"Shop {p['name']} →")}</div><div class="himg">{img_tag(p['img'])}</div></div></header>
<div class="stat"><div class="wrap"><div class="n">{p['stat']}</div><p>{p['statlabel']}</p></div></div>
<div class="tr"><span><b>99%+</b> HPLC purity</span><span><b>QR-verified COA</b> per vial</span><span><b>Lab named</b> · verify it yourself</span><span><b>USA</b> made &amp; shipped</span></div>
<div class="cta"><div class="wrap"><h1 style="font-size:34px;margin-bottom:8px">25% off your first order</h1><p class="sub">Code <b style="color:{GOLD};font-family:monospace">FIRST25</b> — applied automatically. Free shipping over $200.</p>{cart(p['tr'])}</div></div>
<footer><div class="wrap"><p style="border:1px solid #221e15;border-radius:8px;padding:16px;margin-bottom:14px;color:#8f8877">{DISC}</p><a href="{SITE}">© Veyron Biologics · veyronbiologics.com</a></div></footer>
</body></html>"""

def tpl_clinical(p):  # feel: clean white, data-forward, trust-heavy
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{p['name']} (RUO) | Veyron Biologics</title><style>
*{{margin:0;padding:0;box-sizing:border-box}}body{{font:16px/1.65 -apple-system,Segoe UI,Roboto,Arial,sans-serif;background:#fbfaf7;color:#161310}}
.wrap{{max-width:960px;margin:0 auto;padding:0 22px}}.ruo{{background:#161310;color:#c9c2b2;font-size:11.5px;text-align:center;padding:8px;letter-spacing:.4px}}
.btn{{display:inline-block;background:{GOLD};color:#fff;font-weight:700;text-transform:uppercase;letter-spacing:.5px;text-decoration:none;padding:15px 34px;border-radius:6px;font-size:14px}}
nav{{padding:15px 0;border-bottom:1px solid #eae4d6;background:#fff}}nav .wrap{{display:flex;justify-content:space-between;align-items:center}}.logo{{font-family:Georgia,serif;font-size:18px;letter-spacing:2px}}.logo b{{color:{GOLD}}}
.hero{{padding:52px 0;text-align:center}}.tag{{color:{GOLD};font-family:monospace;font-size:12px;letter-spacing:2px;text-transform:uppercase;margin-bottom:12px}}
h1{{font-family:Georgia,serif;font-weight:400;font-size:clamp(30px,4.6vw,44px);line-height:1.12;max-width:760px;margin:0 auto 14px}}
.sub{{font-size:18px;color:#6b6455;max-width:600px;margin:0 auto 24px}}.himg img{{max-width:150px;margin:18px auto 0;display:block}}
.grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:10px 0 40px}}
.c{{background:#fff;border:1px solid #eae4d6;border-radius:12px;padding:24px;text-align:center}}.c .n{{font-size:32px;font-weight:800;color:{GOLD};font-family:Georgia,serif}}.c p{{font-size:13.5px;color:#6b6455;margin-top:4px}}
.spec{{background:#fff;border:1px solid #eae4d6;border-radius:12px;padding:26px;margin-bottom:40px}}.spec h3{{font-family:Georgia,serif;font-weight:400;margin-bottom:14px;font-size:22px}}
.row{{display:flex;justify-content:space-between;padding:10px 0;border-bottom:1px solid #f1ece0;font-size:14.5px}}.row:last-child{{border:0}}.row b{{color:{GOLD}}}
.cta{{text-align:center;padding:46px 0;background:#fff;border-top:1px solid #eae4d6}}
footer{{color:#8f8877;font-size:12.5px;padding:28px 0;line-height:1.7}}footer a{{color:{GOLD};text-decoration:none}}
@media(max-width:760px){{.grid{{grid-template-columns:1fr}}}}</style></head><body>
<div class="ruo">{RUOBAR}</div>
<nav><div class="wrap"><div class="logo">VEYRON <b>BIOLOGICS</b></div>{cart(p['tr'],"Shop")}</div></nav>
<header class="hero"><div class="wrap"><div class="tag">{p['klass']}</div><h1>{p['hook']}</h1><p class="sub">{p['sub']}</p>{cart(p['tr'], f"View {p['name']} →")}<div class="himg">{img_tag(p['img'])}</div></div></header>
<div class="wrap"><div class="grid">
<div class="c"><div class="n">{p['stat']}</div><p>{p['statlabel']}</p></div>
<div class="c"><div class="n">99%+</div><p>HPLC-verified purity, reported to the decimal</p></div>
<div class="c"><div class="n">100%</div><p>Batches third-party COA-tested</p></div></div>
<div class="spec"><h3>Why the COA matters</h3>
<div class="row"><span>Purity assay</span><b>HPLC + mass-spec</b></div>
<div class="row"><span>Certificate of Analysis</span><b>QR-verified, per lot</b></div>
<div class="row"><span>Testing lab</span><b>Named &amp; verifiable</b></div>
<div class="row"><span>Synthesis &amp; shipping</span><b>USA</b></div></div></div>
<div class="cta"><div class="wrap"><h1 style="font-size:30px">25% off your first order</h1><p class="sub">Code <b style="color:{GOLD};font-family:monospace">FIRST25</b> — automatic. Free shipping over $200.</p>{cart(p['tr'])}</div></div>
<footer><div class="wrap"><p style="border:1px solid #eae4d6;border-radius:8px;padding:16px;margin-bottom:12px;background:#fff">{DISC}</p><a href="{SITE}">© Veyron Biologics · veyronbiologics.com</a></div></footer>
</body></html>"""

def tpl_minimal(p):  # feel: ultra-minimal, one message, one CTA
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{p['name']} (RUO) | Veyron Biologics</title><style>
*{{margin:0;padding:0;box-sizing:border-box}}body{{font:17px/1.7 -apple-system,Segoe UI,Roboto,Arial,sans-serif;background:#f3efe6;color:#161310;display:flex;flex-direction:column;min-height:100vh}}
.ruo{{background:#161310;color:#b8b09e;font-size:11px;text-align:center;padding:7px;letter-spacing:.4px}}
.btn{{display:inline-block;background:{GOLD};color:#fff;font-weight:800;text-transform:uppercase;letter-spacing:.6px;text-decoration:none;padding:18px 46px;border-radius:8px;font-size:16px;box-shadow:0 8px 24px rgba(184,145,47,.28)}}
main{{flex:1;display:flex;align-items:center;justify-content:center;text-align:center;padding:40px 22px}}.box{{max-width:620px}}
.tag{{color:{GOLD};font-family:monospace;font-size:12px;letter-spacing:2px;text-transform:uppercase;margin-bottom:20px}}
.box img{{max-width:150px;margin:0 auto 26px;display:block}}
h1{{font-family:Georgia,serif;font-weight:400;font-size:clamp(32px,5.4vw,50px);line-height:1.08;margin-bottom:16px}}
.sub{{font-size:19px;color:#6b6455;margin-bottom:14px}}.off{{font-size:15px;color:#161310;margin-bottom:28px}}.off b{{color:{GOLD};font-family:monospace}}
.foot{{text-align:center;font-size:11.5px;color:#8f8877;padding:20px;line-height:1.6}}.foot a{{color:{GOLD};text-decoration:none}}</style></head><body>
<div class="ruo">{RUOBAR}</div>
<main><div class="box"><div class="tag">{p['klass']}</div>{img_tag(p['img'])}<h1>{p['hook']}</h1><p class="sub">{p['sub']}</p><p class="off">25% off your first order — code <b>FIRST25</b>, automatic · free shipping over $200</p>{cart(p['tr'], f"Shop {p['name']} →")}</div></main>
<div class="foot">{DISC} · <a href="{SITE}">veyronbiologics.com</a></div>
</body></html>"""

def tpl_offer(p):  # feel: dark offer/niche page with a 3-product grid
    prods = p.get("products", [])
    cards = ""
    for s in prods:
        cards += f'<a class="pc" href="{SITE}/product/{s}?tr={p["tr"]}">{img_tag(s)}<span>{s.replace("-"," ").title()}</span><em>View →</em></a>'
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{p['name']} Research Line (RUO) | Veyron Biologics</title><style>
*{{margin:0;padding:0;box-sizing:border-box}}body{{font:16px/1.6 -apple-system,Segoe UI,Roboto,Arial,sans-serif;background:#0f0d09;color:#f3efe4}}
.wrap{{max-width:1000px;margin:0 auto;padding:0 22px}}.ruo{{background:#000;color:#8f8877;font-size:11.5px;text-align:center;padding:8px}}
.ann{{background:{GOLD};color:#12100c;text-align:center;font-weight:700;font-size:13px;padding:9px;text-transform:uppercase;letter-spacing:.5px}}
.btn{{display:inline-block;background:{GOLD};color:#12100c;font-weight:800;text-transform:uppercase;letter-spacing:.5px;text-decoration:none;padding:16px 38px;border-radius:6px;font-size:15px;box-shadow:0 8px 24px rgba(184,145,47,.35)}}
nav{{padding:16px 0;border-bottom:1px solid #2c271c}}nav .wrap{{display:flex;justify-content:space-between;align-items:center}}.logo{{font-family:Georgia,serif;font-size:19px;letter-spacing:2px}}.logo b{{color:{GOLD}}}
.hero{{text-align:center;padding:56px 0}}.tag{{color:{GOLD};font-family:monospace;font-size:12px;letter-spacing:2px;text-transform:uppercase;margin-bottom:14px}}
h1{{font-family:Georgia,serif;font-weight:400;font-size:clamp(32px,5.6vw,52px);line-height:1.08;max-width:820px;margin:0 auto 16px}}
.sub{{font-size:18px;color:#a79f8d;max-width:600px;margin:0 auto 28px}}
.grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;padding:20px 0 50px}}
.pc{{background:#1a1710;border:1px solid #2c271c;border-radius:14px;padding:22px;text-align:center;text-decoration:none;color:#f3efe4;transition:border-color .15s}}.pc:hover{{border-color:{GOLD}}}
.pc img{{height:120px;margin-bottom:8px}}.pc span{{display:block;font-family:Georgia,serif;font-size:19px;margin-bottom:6px}}.pc em{{color:{GOLD};font-size:12px;font-style:normal;text-transform:uppercase;letter-spacing:.5px}}
.cta{{text-align:center;padding:46px 0;border-top:1px solid #2c271c}}footer{{border-top:1px solid #2c271c;color:#7d7768;font-size:12.5px;padding:28px 0;line-height:1.7}}footer a{{color:{GOLD};text-decoration:none}}
@media(max-width:760px){{.grid{{grid-template-columns:1fr}}}}</style></head><body>
<div class="ruo">{RUOBAR}</div><div class="ann">First order → 25% off with FIRST25 · Free shipping over $200</div>
<nav><div class="wrap"><div class="logo">VEYRON <b>BIOLOGICS</b></div>{cart(p['tr'],"Shop")}</div></nav>
<header class="hero"><div class="wrap"><div class="tag">{p['klass']}</div><h1>{p['hook']}</h1><p class="sub">{p['sub']}</p>{cart(p['tr'],"Shop the line →")}</div></header>
<div class="wrap"><div class="grid">{cards}</div></div>
<div class="cta"><div class="wrap"><h1 style="font-size:30px">25% off your first order</h1><p class="sub">Code <b style="color:{GOLD};font-family:monospace">FIRST25</b>, automatic. Free shipping over $200.</p>{cart(p['tr'])}</div></div>
<footer><div class="wrap"><p style="border:1px solid #2c271c;border-radius:8px;padding:16px;margin-bottom:12px;color:#9a9384">{DISC}</p><a href="{SITE}">© Veyron Biologics · veyronbiologics.com</a></div></footer>
</body></html>"""

TEMPLATES = {"bold": tpl_bold, "clinical": tpl_clinical, "minimal": tpl_minimal, "offer": tpl_offer}

# ── BUILD ────────────────────────────────────────────────────────────────────────
import os
built = []
for p in PAGES:
    html = TEMPLATES[p["tpl"]](p)
    fn = p["file"] + ".html"
    open(fn, "w").write(html)
    built.append((fn, p["tpl"], p["name"]))

# index that lists every page grouped by feel
rows = "".join(f'<a class="card" href="{fn}"><b>{fn.replace(".html","")}.veyronbiologics.com</b><span>{name} · <em>{tpl}</em> feel</span></a>' for fn, tpl, name in built)
# keep the two hand-built originals in the index too
extra = ('<a class="card" href="reta.html"><b>reta.veyronbiologics.com</b><span>Retatrutide · <em>editorial</em> feel</span></a>'
         '<a class="card" href="weightloss.html"><b>weightloss.veyronbiologics.com</b><span>Metabolic stack · <em>offer</em> feel</span></a>')
index = f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Veyron LP Previews</title>
<style>body{{font:16px/1.6 -apple-system,Segoe UI,Roboto,Arial,sans-serif;background:#0f0d09;color:#f3efe4;margin:0;padding:50px 22px}}
.wrap{{max-width:720px;margin:0 auto}}h1{{font-family:Georgia,serif;font-weight:400;text-align:center}}p.s{{text-align:center;color:#a79f8d;margin-bottom:30px}}
a.card{{display:flex;justify-content:space-between;align-items:center;gap:14px;padding:18px 20px;margin:10px 0;border:1px solid #2c271c;border-radius:12px;background:#1a1710;color:#f3efe4;text-decoration:none}}
a.card:hover{{border-color:#b8912f}}a.card b{{color:#b8912f;font-family:monospace;font-size:14px}}a.card span{{color:#a79f8d;font-size:14px}}a.card em{{color:#f3efe4;font-style:normal}}</style></head>
<body><div class="wrap"><h1>Veyron Landing Pages</h1><p class="s">Every page = its own subdomain + a different feel. Pick winners, kill losers.</p>{extra}{rows}</div></body></html>"""
open("index.html", "w").write(index)
print(f"generated {len(built)} pages + index:")
for fn, tpl, name in built: print(f"  {fn:22} [{tpl}] {name}")
