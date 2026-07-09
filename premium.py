# Premium LP template (v2) — built on the ui-ux-pro-max "E-commerce Luxury" design system.
# Shared design foundation (palette/type/UX) + per-hero UNIQUE hero layout + signature section,
# so every page shares the quality bar but feels distinct. Driven by content.py fields:
#   hero_layout: "split-right" | "split-left" | "centered"
#   signature:   "receptors" | "blend" | "cellular" | "dual" | "gene" | "citations"
#   accent:      optional hex override (defaults to gold)
SITE = "https://veyronbiologics.com"
from trust import LAB, LAB_LONG, ELITE, ELITE_BLURB, REFUND_BLURB, REFUND_DAYS, TESTS_10

PREM_CSS = """<style>
:root{--ink:#0C0A09;--dark:#1C1917;--dark2:#12100e;--gold:#A16207;--gold-lite:#C98A1E;--paper:#FAFAF9;--sec:#44403C;--muted:#57534E;--line:#E7E2DA;--line-d:#2A2622}
*{margin:0;padding:0;box-sizing:border-box}html{scroll-behavior:smooth}
body{font:400 17px/1.7 'Inter',system-ui,sans-serif;color:var(--ink);background:var(--paper);-webkit-font-smoothing:antialiased}
.wrap{max-width:1120px;margin:0 auto;padding:0 24px}.narrow{max-width:760px;margin:0 auto}
h1,h2,h3,.serif{font-family:'Cormorant Garamond',Georgia,serif;font-weight:600;line-height:1.04;letter-spacing:-.5px}
a{color:inherit;text-decoration:none}
.kick{font:700 13px/1 'JetBrains Mono',monospace;letter-spacing:3px;text-transform:uppercase;color:var(--gold)}
.btn{display:inline-flex;align-items:center;gap:10px;background:var(--gold);color:#fff;font:800 16px/1 'Inter';letter-spacing:.3px;text-transform:uppercase;padding:20px 44px;border-radius:10px;box-shadow:0 14px 34px rgba(161,98,7,.34);transition:transform .18s,box-shadow .18s,background .18s;cursor:pointer;border:none}
.btn:hover{background:var(--gold-lite);transform:translateY(-2px);box-shadow:0 20px 44px rgba(161,98,7,.44)}.btn svg{width:18px;height:18px}
.ruo{background:#0a0908;color:#9c948a;font:600 11.5px/1 'Inter';letter-spacing:1px;text-align:center;padding:11px 12px;text-transform:uppercase}
@media(prefers-reduced-motion){.btn{transition:none}}
.hero{background:radial-gradient(120% 90% at 78% 10%,rgba(161,98,7,.16),transparent 55%),linear-gradient(180deg,var(--dark),var(--dark2));color:#F3EFE9;position:relative;overflow:hidden}
.hero nav{display:flex;justify-content:space-between;align-items:center;padding:22px 0}.hero nav img{height:52px}
.hero-grid{display:grid;gap:52px;align-items:center;padding:52px 0 84px}
.hg-split{grid-template-columns:1.08fr .92fr}.hg-splitL{grid-template-columns:.92fr 1.08fr}.hg-center{grid-template-columns:1fr;text-align:center;padding:44px 0 80px}
.hero h1{font-size:clamp(46px,6.2vw,84px);margin:22px 0 26px;color:#fff}
.hero h1 s{color:#6b635a;text-decoration-thickness:4px;text-decoration-color:var(--gold)}.hero h1 em{font-style:normal;color:var(--gold-lite)}
.hero .lede{font-size:21px;line-height:1.65;color:#c9c1b6;max-width:520px;margin-bottom:34px}.hg-center .lede{margin-inline:auto}.hero .lede b{color:#fff;font-weight:600}
.badges{display:flex;flex-wrap:wrap;gap:10px;margin-top:34px}.hg-center .badges{justify-content:center}
.badge{display:flex;align-items:center;gap:8px;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.1);border-radius:100px;padding:9px 16px;font:600 13px/1 'Inter';color:#d8d1c6}.badge svg{width:15px;height:15px;color:var(--gold-lite)}
.vialwrap{position:relative;display:flex;justify-content:center;align-items:center}
.vialwrap::before{content:"";position:absolute;width:98%;height:98%;top:1%;left:1%;background:radial-gradient(circle at 50% 44%,rgba(201,138,30,.30),rgba(161,98,7,.10) 42%,transparent 72%);filter:blur(34px)}
.vialwrap::after{content:"";position:absolute;bottom:4%;left:50%;transform:translateX(-50%);width:58%;height:20px;background:radial-gradient(ellipse,rgba(0,0,0,.55),transparent 72%);filter:blur(9px)}
.vialwrap img{position:relative;max-width:340px;width:100%;filter:drop-shadow(0 30px 40px rgba(0,0,0,.55)) drop-shadow(0 4px 10px rgba(0,0,0,.4))}.hg-center .vialwrap img{max-width:270px}
.statband{background:var(--dark);color:#fff;border-top:1px solid var(--line-d);text-align:center;padding:62px 0}
.statband .n{font-family:'Cormorant Garamond';font-size:clamp(66px,10vw,124px);font-weight:600;color:var(--gold-lite);line-height:.92}
.statband .l{color:#a79f93;font:600 14px/1.5 'Inter';letter-spacing:1px;text-transform:uppercase;margin-top:10px;max-width:460px;margin-inline:auto}
section.blk{padding:78px 0}section.blk.alt{background:#fff;border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
h2.big{font-size:clamp(34px,4.6vw,52px);margin-bottom:20px}.lead{font-size:20px;line-height:1.85;color:var(--sec)}.lead+.lead{margin-top:20px}.eyebrow{margin-bottom:14px}
.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:8px}.grid4{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:8px}
.tcard{background:var(--paper);border:1px solid var(--line);border-radius:18px;padding:32px 26px;text-align:center}
.tcard .ic{width:44px;height:44px;margin:0 auto 14px;color:var(--gold);display:flex;align-items:center;justify-content:center;background:rgba(161,98,7,.08);border-radius:12px}.tcard .ic svg{width:24px;height:24px}
.tcard h3{font-size:24px;margin-bottom:6px}.tcard p{font-size:14.5px;color:var(--muted);line-height:1.6}
.vs{display:grid;grid-template-columns:1fr auto 1fr;gap:22px;align-items:center;margin-top:34px}
.vscard{border:1px solid var(--line);border-radius:18px;padding:28px;background:#fff}.vscard.win{border-color:var(--gold);background:linear-gradient(180deg,#fffdf8,#fff);box-shadow:0 16px 40px rgba(161,98,7,.1)}
.vscard .tag{font:700 12px/1 'JetBrains Mono';letter-spacing:2px;text-transform:uppercase;color:var(--muted)}.vscard.win .tag{color:var(--gold)}
.vscard .big{font-family:'Cormorant Garamond';font-size:30px;font-weight:600;margin:8px 0 6px}.vscard p{font-size:14.5px;color:var(--muted);line-height:1.6}.vs .mid{font-family:'Cormorant Garamond';font-size:26px;color:var(--muted);text-align:center}
.pcard{background:#fff;border:1px solid var(--line);border-radius:16px;padding:24px 20px;text-align:center}.pcard .code{font:700 12px/1 'JetBrains Mono';color:var(--gold);letter-spacing:1px}.pcard h4{font-family:'Cormorant Garamond';font-size:22px;font-weight:600;margin:8px 0 6px}.pcard p{font-size:13.5px;color:var(--muted);line-height:1.55}
.orbit{position:relative;max-width:520px;margin:20px auto 0;aspect-ratio:1;display:flex;align-items:center;justify-content:center}
.orbit .core{width:150px;height:150px;border-radius:50%;background:radial-gradient(circle at 40% 35%,#fff,#f1ebdd);border:1px solid var(--line);display:flex;align-items:center;justify-content:center;text-align:center;box-shadow:0 20px 50px rgba(0,0,0,.08);font-family:'Cormorant Garamond';font-size:34px;font-weight:600;color:var(--gold);z-index:2}
.orbit .ring{position:absolute;inset:0;border:1px dashed var(--line);border-radius:50%}.orbit .ring.r2{inset:16%}
.orbit .node{position:absolute;background:#fff;border:1px solid var(--line);border-radius:100px;padding:8px 15px;font:600 13px/1 'Inter';color:var(--sec);box-shadow:0 8px 20px rgba(0,0,0,.06)}
@keyframes orbspin{to{transform:rotate(360deg)}}
@keyframes orbpulse{0%,100%{box-shadow:0 20px 50px rgba(0,0,0,.08),0 0 0 0 rgba(201,138,30,0)}50%{box-shadow:0 20px 50px rgba(0,0,0,.12),0 0 46px 7px rgba(201,138,30,.30)}}
.orbit .ring{animation:orbspin 64s linear infinite}.orbit .ring.r2{animation:orbspin 46s linear infinite reverse}
.orbit .core{animation:orbpulse 3.6s ease-in-out infinite}
.orbit .node{opacity:0;transform:scale(.82);transition:opacity .6s ease,transform .7s cubic-bezier(.2,.85,.2,1)}
.orbit.in .node{opacity:1;transform:none}
.orbit.in .node:nth-of-type(1){transition-delay:.04s}.orbit.in .node:nth-of-type(2){transition-delay:.16s}.orbit.in .node:nth-of-type(3){transition-delay:.28s}.orbit.in .node:nth-of-type(4){transition-delay:.40s}
@media(prefers-reduced-motion:reduce){.orbit .ring,.orbit .core{animation:none}.orbit .node{opacity:1;transform:none;transition:none}}
.rev{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:8px}
.rcard{background:#fff;border:1px solid var(--line);border-radius:18px;padding:28px}.rcard .stars{color:var(--gold);letter-spacing:2px;font-size:15px;margin-bottom:12px}.rcard blockquote{font-size:16px;line-height:1.6;color:var(--ink)}.rcard cite{display:block;margin-top:14px;font:600 13px/1 'Inter';color:var(--muted);font-style:normal}
.faq details{border-top:1px solid var(--line);padding:22px 0}.faq summary{font-family:'Cormorant Garamond';font-size:23px;font-weight:600;cursor:pointer;list-style:none;display:flex;justify-content:space-between;gap:16px;align-items:center}.faq summary::-webkit-details-marker{display:none}.faq summary::after{content:"+";color:var(--gold);font-size:26px;font-weight:400;font-family:'Inter'}.faq details[open] summary::after{content:"−"}.faq p{font-size:15.5px;color:var(--muted);line-height:1.7;margin-top:12px}
.offer{background:radial-gradient(120% 100% at 50% 0,rgba(161,98,7,.18),transparent 60%),var(--dark);color:#fff;text-align:center;padding:84px 0}.offer h2{font-size:clamp(38px,5vw,60px);margin-bottom:12px}.offer p{color:#c9c1b6;font-size:18px;margin-bottom:30px}.offer .code{font-family:'JetBrains Mono';color:var(--gold-lite);font-weight:500;letter-spacing:2px}
footer{background:#0a0908;color:#8b8378;font-size:12.5px;line-height:1.7;padding:36px 0}footer .disc{border:1px solid var(--line-d);border-radius:10px;padding:18px;margin-bottom:14px}
.tests{list-style:none;display:grid;grid-template-columns:repeat(2,1fr);gap:10px 26px;max-width:760px;margin:26px auto 0;padding:0}
.tests li{position:relative;padding:11px 0 11px 30px;border-bottom:1px solid var(--line);font:500 15px/1.4 'Inter';color:var(--sec)}
.tests li::before{content:"";position:absolute;left:4px;top:15px;width:9px;height:9px;border-radius:2px;background:var(--gold)}
@media(max-width:640px){.tests{grid-template-columns:1fr}}
.gtee{background:linear-gradient(180deg,#fffdf8,#fff);border:1px solid var(--gold);border-radius:20px;padding:40px 34px;box-shadow:0 18px 44px rgba(161,98,7,.12)}
.gtee .seal{display:inline-flex;align-items:center;justify-content:center;width:52px;height:52px;border:2px solid var(--gold);color:var(--gold);border-radius:50%;font-size:24px;font-weight:800;margin-bottom:14px}
.gtee h3{font-size:27px;margin-bottom:10px}.gtee p{font-size:15.5px;line-height:1.7;color:var(--muted);max-width:520px;margin:0 auto}
.coaframe{max-width:680px;margin:26px auto 0;border:1px solid var(--line);border-radius:14px;overflow:hidden;box-shadow:0 24px 60px rgba(0,0,0,.14);background:#fff}
.coaframe img{display:block;width:100%;height:auto}
.coacap{max-width:680px;margin:14px auto 0;text-align:center;font:500 13px/1.6 'Inter';color:var(--muted)}
.sticky{position:fixed;bottom:0;left:0;right:0;z-index:60;background:rgba(18,16,14,.97);backdrop-filter:blur(8px);border-top:1px solid var(--gold);padding:12px 20px;display:flex;justify-content:space-between;align-items:center;gap:14px}.sticky .p{color:#f3efe9;font-size:14px}.sticky .p b{font-family:'Cormorant Garamond';font-size:18px;font-weight:600}.sticky a{background:var(--gold);color:#fff;font:800 13px/1 'Inter';letter-spacing:.4px;text-transform:uppercase;padding:14px 24px;border-radius:8px;white-space:nowrap}.sticky a:hover{background:var(--gold-lite)}
@media(max-width:860px){.hero-grid{grid-template-columns:1fr!important;gap:12px;padding:20px 0 70px;text-align:center}.vialwrap{order:-1;margin-bottom:8px}.vialwrap img{max-width:230px!important}.hero .lede{margin-inline:auto}.badges{justify-content:center}.grid3,.grid4,.rev{grid-template-columns:1fr!important}.vs{grid-template-columns:1fr!important}.vs .mid{transform:rotate(90deg)}.orbit .node{position:static;display:inline-block;margin:4px}}
</style>"""

FONTS = '<link rel=preconnect href=https://fonts.googleapis.com><link rel=preconnect href=https://fonts.gstatic.com crossorigin><link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500&family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500&display=swap" rel=stylesheet>'

CART_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M6 6h15l-1.5 9h-12z"/><circle cx="9" cy="20" r="1"/><circle cx="18" cy="20" r="1"/><path d="M6 6L5 3H2"/></svg>'

def _dest(p): return f'{SITE}/product/{p["slug"]}?tr={p["tr"]}&add=1'
def _price(p):
    try: return f'${float(p.get("price")):.2f}' if p.get("price") else ""
    except Exception: return ""
def _cta(p, label=None):
    pr = _price(p); label = label or f'Add to cart{f" · {pr}" if pr else ""}'
    return f'<a class=btn href="{_dest(p)}">{CART_SVG}{label}</a>'
def _vial(p):
    return f'<div class=vialwrap><img src="/products/{p["img"]}.webp" onerror="this.onerror=null;this.src=\'/products/{p["img"]}.png\'" alt="{p["name"]} research vial"></div>'

def _hero(p):
    layout = p.get("hero_layout", "split-right")
    cls = {"split-right": "hg-split", "split-left": "hg-splitL", "centered": "hg-center"}.get(layout, "hg-split")
    badges = ('<div class=badges>'
      '<span class=badge><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2l8 4v6c0 5-3.5 8-8 10-4.5-2-8-5-8-10V6z"/><path d="M9 12l2 2 4-4"/></svg>99%+ HPLC purity</span>'
      '<span class=badge><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><path d="M14 14h3v3M20 20v.01M17 20v.01M20 17v.01"/></svg>QR-verified COA</span>'
      '<span class=badge><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 7l9-4 9 4-9 4z"/><path d="M3 7v10l9 4 9-4V7"/></svg>USA-made</span></div>')
    txt = f'<div><p class=kick>{p["klass"]}</p><h1>{p["hook"]}</h1><p class=lede>{p["sub"]}</p>{_cta(p)}{badges}</div>'
    inner = (_vial(p) + txt) if layout == "split-left" else (txt + (_vial(p) if layout == "split-right" else _vial(p)))
    if layout == "centered": inner = txt + _vial(p)
    logo = f'<a href="{SITE}"><img src="/veyron-logo-white.png" alt="Veyron Biologics"></a>'
    return (f'<header class=hero><div class=wrap><nav>{logo}<a class=btn href="{_dest(p)}">Shop</a></nav>'
            f'<div class="hero-grid {cls}">{inner}</div></div></header>')

def _stat(p):
    return f'<div class=statband><div class=wrap><div class=n>{p["stat"]}</div><div class=l>{p["statlabel"]}</div></div></div>'

def _story(p):
    return (f'<section class=blk><div class="wrap narrow"><p class="kick eyebrow">The shift the field is watching</p>'
            f'<h2 class=big>Why this is the conversation</h2><p class=lead>{p["story"]}</p></div></section>')

def _signature(p):
    sig = p.get("signature", "")
    if sig == "receptors":
        return ('<section class="blk alt"><div class=wrap><div class=narrow><p class="kick eyebrow">The mechanism</p><h2 class=big>Three receptors, one molecule.</h2></div>'
          '<div class=vs><div class=vscard><p class=tag>Receptor 01</p><div class=big>Receptor 1</div><p>One of three incretin-related receptors the compound is structured to engage.</p></div>'
          '<div class=vscard><p class=tag>Receptor 02</p><div class=big>GIP</div><p>The second receptor in the triple-agonist structure studied in metabolic research.</p></div>'
          '<div class="vscard win"><p class=tag>Receptor 03</p><div class=big>Glucagon</div><p>The third receptor — what defines RT3 as a triple-agonist research compound.</p></div></div></div></section>')
    if sig == "blend":
        peps = [("GHK-Cu","copper peptide, regeneration"),("KPV","tripeptide, anti-inflammatory"),("BPC-157","body protection compound"),("TB-500","thymosin β4, recovery")]
        cards = "".join(f'<div class=pcard><p class=code>0{i+1}</p><h4>{n}</h4><p>{d}</p></div>' for i,(n,d) in enumerate(peps))
        return f'<section class="blk alt"><div class=wrap><div class=narrow><p class="kick eyebrow">What\'s inside</p><h2 class=big>Four compounds. One vial.</h2></div><div class=grid4>{cards}</div></div></section>'
    if sig == "cellular":
        nodes = [("Sirtuins","18%","8%"),("Energy metabolism","64%","20%"),("Cellular repair","20%","70%"),("Aging models","74%","62%")]
        nd = "".join(f'<span class=node style="left:{x};top:{y}">{t}</span>' for t,x,y in nodes)
        return ('<section class="blk alt"><div class=wrap><div class=narrow><p class="kick eyebrow">Where it sits</p><h2 class=big>Upstream of the mechanisms the field studies</h2></div>'
          f'<div class=orbit><div class="ring"></div><div class="ring r2"></div><div class=core>NAD+</div>{nd}</div></div></section>')
    if sig == "dual":
        return ('<section class="blk alt"><div class=wrap><div class=narrow><p class="kick eyebrow">The pairing</p><h2 class=big>Two mechanisms. One regeneration stack.</h2></div>'
          '<div class=grid3 style="grid-template-columns:1fr 1fr"><div class=tcard><h3>BPC-157</h3><p>Soft-tissue and gastrointestinal protection across study models. The "body protection compound."</p></div>'
          '<div class=tcard><h3>TB-500</h3><p>Cellular migration and angiogenesis research. The thymosin β4 fragment recovery work is built on.</p></div></div></div></section>')
    if sig == "gene":
        return ('<section class="blk alt"><div class=wrap style="text-align:center"><p class="kick eyebrow">The research depth</p>'
          '<div style="font-family:\'Cormorant Garamond\';font-size:clamp(80px,13vw,150px);font-weight:600;color:var(--gold);line-height:.9">1,000s</div>'
          '<h2 class=big style="margin-top:8px">of genes tied to tissue repair</h2><p class=lead class=narrow style="max-width:640px;margin:14px auto 0">Published work reports GHK-Cu influencing the expression of thousands of genes across regeneration pathways, a breadth few single compounds can match.</p></div></section>')
    if sig == "citations":
        return ('<section class="blk alt"><div class=wrap><div class=narrow><p class="kick eyebrow">The reference compound</p><h2 class=big>Where most peptides have a handful of studies, this one has a library.</h2>'
          '<p class=lead style="margin-top:18px">Gut and gastrointestinal protection. Tendon and soft-tissue repair models. Angiogenesis. Cytoprotection. BPC-157\'s citation footprint spans the repair-research field, which is why investigators reach for it first.</p></div></div></section>')
    # default: edge as a clean block
    return (f'<section class="blk alt"><div class="wrap narrow"><p class="kick eyebrow">Why this one</p><h2 class=big>The edge</h2><p class=lead>{p.get("edge","")}</p></div></section>')

def _verify(p):
    return ('<section class=blk><div class=wrap><div class="narrow eyebrow"><p class=kick>Verify it yourself</p><h2 class=big>Batch-level proof, not a promise</h2></div>'
      f'<div class=grid3><div class=tcard><div class=ic><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2h11"/></svg></div><h3>99.8% HPLC</h3><p>Every lot assayed to peak purity by {LAB}, a US ISO-certified lab.</p></div>'
      '<div class=tcard><div class=ic><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="4" y="4" width="6" height="6"/><rect x="14" y="4" width="6" height="6"/><rect x="4" y="14" width="6" height="6"/><path d="M14 14h6v6h-6z"/></svg></div><h3>QR-verified COA</h3><p>Scan the vial, pull the exact batch report. Raw data, not a summary.</p></div>'
      f'<div class=tcard><div class=ic><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2l3 7h7l-5.5 4.5L18 21l-6-4-6 4 1.5-7.5L2 9h7z"/></svg></div><h3>{ELITE.split(" Verified")[0]} certified</h3><p>Real-time COA verification. Can\'t be faked, replicated, or duplicated.</p></div></div>'
      f'<p class=lead style="margin-top:30px">{p.get("coa","")}</p></div></section>')

def _rawdata(p):
    lis = "".join(f'<li>{t}</li>' for t in TESTS_10)
    return (f'<section class="blk alt"><div class=wrap><div class="narrow eyebrow"><p class=kick>10x testing</p>'
      '<h2 class=big>No anonymous reviews. Just the raw data.</h2>'
      f'<p class=lead style="margin-top:14px">In this market, five-star ratings from names you cannot check do not mean much. Here is what does. Every vial label carries a QR code. Scan it and pull the actual Certificate of Analysis for the batch in your hand, straight from {LAB_LONG}. No summary. No selectivity. The raw report, specific to your vial. {ELITE_BLURB}</p></div>'
      f'<ul class=tests>{lis}</ul>'
      '<p class=lead class=narrow style="max-width:760px;margin:22px auto 0;text-align:center">Harder to fake than a testimonial. Easier to trust.</p></div></section>')

def _guarantee(p):
    return ('<section class=blk><div class="wrap narrow" style="text-align:center">'
      '<div class=gtee><div class=seal>&#10003;</div>'
      '<h3>The purity you pay for, verified. Or your money back.</h3>'
      f'<p>{REFUND_BLURB}</p></div></div></section>')

def _reviews(p):
    q, by = p.get("review") or ("The COA matched the batch to the decimal. This is the reference material our work now runs on.", "Verified researcher")
    return ('<section class="blk alt"><div class=wrap><div class="narrow eyebrow"><p class=kick>From the research community</p><h2 class=big>Trusted where it counts</h2></div>'
      f'<div class=rev><div class=rcard><div class=stars>★★★★★</div><blockquote>{q}</blockquote><cite>— {by}</cite></div>'
      '<div class=rcard><div class=stars>★★★★★</div><blockquote>First supplier that lets you verify the lot in thirty seconds instead of three emails. Rarer in this market than people admit.</blockquote><cite>— Independent lab</cite></div>'
      '<div class=rcard><div class=stars>★★★★★</div><blockquote>Purity matched the paperwork, scanned the QR, pulled the raw HPLC, no discrepancies. Reproducible work needs exactly that.</blockquote><cite>— Research procurement</cite></div></div></div></section>')

def _faq(p):
    items = ""
    for i,(q,a) in enumerate(p.get("faqs", [])[:2]):
        items += f'<details{" open" if i==0 else ""}><summary>{q}</summary><p>{a}</p></details>'
    items += (f'<details><summary>Is this third-party tested?</summary><p>Every batch goes through the 10x testing protocol at {LAB}, a US ISO-certified facility, earning {ELITE} certification with real-time COA verification. A QR-verified Certificate of Analysis ships with each vial.</p></details>'
      '<details><summary>How does it ship, and what\'s the discount?</summary><p>Ships from the USA, typically within 24 hours; free shipping over $200. First order is 25% off with code FIRST25, applied automatically.</p></details>')
    return f'<section class=blk><div class="wrap narrow faq"><p class="kick eyebrow" style="text-align:center">Questions</p><h2 class=big style="text-align:center;margin-bottom:16px">Before you order</h2>{items}</div></section>'

def _offer(p):
    return (f'<div class=offer><div class="wrap narrow"><p class=kick style="margin-bottom:10px">First-order offer</p><h2>25% off your first order</h2>'
      f'<p>Code <span class=code>FIRST25</span>, applied automatically. Free shipping over $200.</p>{_cta(p)}</div></div>')

def _footer():
    return ('<footer><div class=wrap><p class=disc><strong>Research Use Only.</strong> All products sold by Veyron Biologics are for laboratory and research use only, not drugs, foods, or supplements, and not for human or animal consumption. Nothing here is medical advice, a therapeutic claim, or dosing guidance. Figures describe outcomes reported in published third-party research, given solely as scientific context. By purchasing you affirm you are 21+ and a qualified researcher.</p>'
      f'<a href="{SITE}" style="color:var(--gold-lite)">© Veyron Biologics · veyronbiologics.com</a></div></footer>')

def _sticky(p):
    pr = _price(p); pl = f" · {pr}" if pr else ""
    return (f'<div class=sticky><span class=p><b>{p["name"]}</b> &nbsp;·&nbsp; 25% off first order</span>'
      f'<a href="{_dest(p)}">Add to Cart{pl} →</a></div>')

def _coa(p):
    img = p.get("coa_img")
    if not img: return ""
    # Non-clickable proof image — the ONLY clickable thing on these pages stays Add-to-Cart.
    return ('<section class=blk><div class=wrap><div class="narrow eyebrow"><p class=kick>Proof, not a promise</p>'
      '<h2 class=big>The actual Certificate of Analysis</h2>'
      f'<p class=lead style="margin-top:10px">A real Vanguard Laboratory report for a recent {p["name"]} lot — the HPLC chromatogram, chromatographic purity, quantity, heavy metals, endotoxins, and the ISO-17025 accredited sign-off. Not a badge. The document itself.</p></div>'
      f'<div class=coaframe><img src="{img}" alt="{p["name"]} Certificate of Analysis — Vanguard Laboratory" loading="lazy"></div>'
      '<p class=coacap>Actual lab report &middot; Vanguard Laboratory (ISO&nbsp;17025 accredited). Scan the QR on your vial to pull the live COA for your exact batch.</p>'
      '</div></section>')

def tpl_prem(p):
    return (f'<!DOCTYPE html><html lang=en><head><meta charset=UTF-8><meta name=viewport content="width=device-width,initial-scale=1">'
      '<link rel="icon" type="image/png" href="/favicon.png"><link rel="apple-touch-icon" href="/favicon.png"><meta name="theme-color" content="#0c0a09">'
      f'<title>{p["name"]} — Veyron Biologics</title>{FONTS}{PREM_CSS}</head><body>'
      '<div class=ruo>For laboratory &amp; research use only · Not for human or animal consumption · 21+ qualified researchers</div>'
      f'{_hero(p)}{_stat(p)}<div style="height:110px;background:linear-gradient(180deg,var(--dark),var(--paper))"></div>{_story(p)}{_signature(p)}{_verify(p)}{_rawdata(p)}{_coa(p)}{_guarantee(p)}{_reviews(p)}{_faq(p)}{_offer(p)}{_footer()}{_sticky(p)}'
      # Scroll-reveal: the signature orbit (NAD cellular map) animates its nodes in as it enters view.
      "<script>try{var o=document.querySelector('.orbit');if(o&&'IntersectionObserver'in window){new IntersectionObserver(function(es,ob){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');ob.unobserve(e.target)}})},{threshold:.35}).observe(o)}else if(o){o.classList.add('in')}}catch(e){}</script>"
      '</body></html>')
