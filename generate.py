#!/usr/bin/env python3
"""
Veyron landing-page engine v2.
Matches the real brand: /veyron-logo.png (+ white), Cormorant Garamond (serif) + Inter (body),
real product photos by slug. Clean subdomain names (no dashes). Product pages link straight to the
product (add-to-cart on the real site), niche pages to the catalog. Distinct FEELS for A/B.
Run: python3 generate.py
"""
from trust import LAB, LAB_LONG, ELITE, ELITE_BLURB, REFUND_BLURB, REFUND_DAYS, TESTS_10, TRACK
SITE = "https://veyronbiologics.com"
# CTA destination store. These 9 landers now drive the WooCommerce funnel (live.veyronbiologics.com);
# every other lander keeps pointing at the OG custom site until we migrate the rest.
STORE = "https://live.veyronbiologics.com"
WP_LIVE = {"reta", "klow", "nad", "wolverine", "ghk", "bpc", "metabolic", "cellular", "repair"}
def _store(p):  # which store this lander's CTAs point to
    return STORE if p.get("file") in WP_LIVE else SITE
GOLD = "#b8912f"
FONTS = ("<link rel=preconnect href=https://fonts.googleapis.com>"
         "<link href='https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap' rel=stylesheet>")
SERIF = "'Cormorant Garamond',Georgia,serif"
SANS = "'Inter',system-ui,sans-serif"
MONO = "'JetBrains Mono',monospace"

RUOBAR = 'FOR LABORATORY &amp; RESEARCH USE ONLY · NOT FOR HUMAN OR ANIMAL CONSUMPTION · 21+ QUALIFIED RESEARCHERS'
DISC = ('<strong>Research Use Only.</strong> All products sold by Veyron Biologics are for laboratory and research use only, '
        'not drugs, foods, or supplements, and <strong>not for human or animal consumption</strong>. Nothing here is medical '
        'advice, a therapeutic claim, or dosing guidance. Figures describe outcomes reported in published third-party research, '
        'given solely as scientific context. By purchasing you affirm you are 21+ and a qualified researcher.')

def logo(dark=False):
    f = "veyron-logo-white.png" if dark else "veyron-logo.png"
    return f'<a href="{SITE}"><img src="/{f}" alt="Veyron Biologics" style="height:52px;width:auto;display:block"></a>'

def img_tag(slug, cls=""):
    return f'<img class="{cls}" src="/products/{slug}.webp" alt="{slug} research vial" loading="lazy" onerror="this.onerror=null;this.src=\'/products/{slug}.png\'">'

def dest(p):  # product pages → one-click add-to-cart → checkout; niches → catalog/shop
    base = _store(p)
    if p.get("slug"):
        return f'{base}/product/{p["slug"]}?tr={p["tr"]}&add=1'
    # niche pages: WP has no /catalog route — send WP-live niches to /shop, others to OG /catalog
    return f'{base}/shop?tr={p["tr"]}' if base == STORE else f'{base}/catalog?tr={p["tr"]}'

def price_str(p):
    v = p.get("price")
    try: return f"${float(v):.0f}" if v else ""
    except Exception: return ""

def cta(p, label=None):
    if label is None:
        pr = price_str(p)
        label = (f'Add to Cart{f" · {pr}" if pr else ""} →' if p.get("slug") else "Shop the catalog →")
    return f'<a class="btn" href="{dest(p)}">{label}</a>'

# ── CONTENT (DB-driven: a page for every active product) ─────────────────────────
import json, os
_prods = json.load(open("products.json"))  # active products exported from the store DB

# Rich hero content + short alias + chosen feel, keyed by the REAL product slug.
HEROES = {
 "rt3": dict(alias="reta", tpl="editorial", klass='triple-agonist · metabolic research',
   hook="The research compound that made <em>the previous generation look like a warm-up.</em>",
   sub="RT3 is the triple-hormone agonist the field is calling a triple-agonist, and in published research it left the previous generation behind.",
   stat="~24%", statlabel="mean body-weight reduction reported in 48-week research",
   what="RT3 is a single molecule that acts on three key metabolic-research receptors at once. Where a single-agonist hits one target and a dual-agonist hits two, the triple-agonist engages all three pathways implicated in metabolic research.",
   why="In the published literature the triple-agonist didn't just improve on its predecessors, it reset the ceiling. Research on obese study subjects reported roughly 24% mean body-weight reduction over 48 weeks, with figures some researchers compared to bariatric outcomes."),
 "tz2": dict(alias="tirz", tpl="bold", klass="dual-agonist · incretin receptors", hook="The dual-agonist workhorse.",
   sub="The dual-incretin combination that became the research standard before the triple-agonist arrived, proven, dependable, decisive.",
   stat="~21%", statlabel="mean reduction reported in trials",
   what="TZ2 activates two key incretin receptors. The dual mechanism made it a clear step up over single-agonist research, and it remains the reference point the newer compounds are measured against.",
   why="The most-studied dual-agonist in the space, with the deepest body of research data behind it. When a study needs a proven benchmark, this is it."),
 "cagrilintide": dict(alias="cagri", tpl="bold", klass="amylin analog · stack partner", hook="The amylin analog the newest research is built around.",
   sub="The compound researchers pair with the incretins, the combination driving the latest metabolic studies.",
   stat="Stack", statlabel="the research favorite for combination work",
   what="Cagrilintide is a long-acting amylin analog, a different mechanism from the incretins. That's exactly why it's the pairing partner: researchers stack it with incretin compounds to study combined pathways.",
   why="The newest wave of metabolic research is built on combinations, and cagrilintide is the amylin half of the most-studied pairings."),
 "nad-plus": dict(alias="nad", tpl="clinical", klass="cellular · longevity research", hook="The molecule at the center of the longevity conversation.",
   sub="Central to cellular energy and sirtuin research, the compound the aging field keeps coming back to.",
   stat="Sirtuins", statlabel="the pathway NAD+ research centers on",
   what="NAD+ (nicotinamide adenine dinucleotide) is a coenzyme found in every living cell, central to energy metabolism and the activity of sirtuins, the proteins at the heart of cellular-aging research.",
   why="NAD+ levels are a recurring variable in longevity studies. It's one of the most-cited molecules in the cellular-aging literature, which is why it anchors the research."),
 "ghk-cu": dict(alias="ghk", tpl="minimal", klass="copper peptide · repair research", hook="The copper peptide the repair literature won't stop citing.",
   sub="Studied for its role in tissue-repair and regenerative signaling, one of the most-referenced peptides in the field.",
   stat="~33%", statlabel="faster repair reported in research models",
   what="GHK-Cu is a copper-binding tripeptide naturally present in human plasma. Research associates it with tissue-repair signaling and gene-expression pathways tied to regeneration.",
   why="Few peptides have GHK-Cu's depth of repair-and-regeneration research behind them, including studies reporting influence over thousands of genes tied to tissue repair."),
 "klow": dict(alias="klow", tpl="bold", klass="research blend · GHK / KPV / BPC / TB-500", hook="Four research peptides. One vial.",
   sub="A blend built from the repair-and-recovery compounds the research community stacks by hand, pre-combined and COA-verified.",
   stat="4-in-1", statlabel="the convenience of a pre-built research blend",
   what="KLOW combines four of the most-studied repair-and-recovery research peptides, GHK-Cu, KPV, BPC-157, and TB-500, in a single lyophilized vial.",
   why="Researchers who'd otherwise reconstitute four separate compounds get one COA-verified blend. Convenience without giving up the transparency."),
}
# Merge the rich DR copy (story/edge/coa/faqs/review) over the base HEROES, overrides hook/sub/etc for
# the featured pages and adds wolverine. Featured pages then render the extra richsections.
try:
    from content import RICH
    for _slug, _r in RICH.items():
        HEROES[_slug] = {**HEROES.get(_slug, {}), **_r}
except Exception as _e:
    print("content merge skipped:", _e)

# Premium template (v2) rollout — each hero gets a UNIQUE hero layout + signature section so no two
# featured pages look the same, all on the shared "E-commerce Luxury" design system.
from premium import tpl_prem
PREM = {
    "rt3": ("split-right", "receptors"),
    "klow":        ("centered",    "blend"),
    "nad-plus":    ("split-left",  "cellular"),
    "wolverine":   ("centered",    "dual"),
    "ghk-cu":      ("split-right",  "gene"),
    "bpc-157":     ("split-left",  "citations"),
}
for _slug, (_hl, _sig) in PREM.items():
    if _slug in HEROES:
        HEROES[_slug]["tpl"] = "prem"; HEROES[_slug]["hero_layout"] = _hl; HEROES[_slug]["signature"] = _sig

# Funnel (metabolic) compounds use the COA-forward "verified" template — sells verifiability, not mechanism.
# This REPLACES the older claim-heavy hero (triple-agonist / body-weight-reduction copy) for these pages:
# compliance-clean by design (no GLP, no INN phrases, no effect/weight-loss claims). Overrides PREM above.
from verified import tpl_verified
for _slug in ("rt3", "tz2"):
    if _slug in HEROES:
        HEROES[_slug]["tpl"] = "verified"

FEELS = ["bold", "clinical", "minimal", "editorial"]  # rotate across non-hero products for A/B variety

def imgslug(p): return p["img"].split("/")[-1].rsplit(".", 1)[0]

PAGES = []
for i, pr in enumerate(sorted(_prods, key=lambda x: x["slug"])):
    slug = pr["slug"]; h = HEROES.get(slug)
    name = pr["name"]; short = (pr.get("short") or f"{name}, research-grade, HPLC-verified.").strip()
    desc = (pr.get("desc") or short).strip()
    if h:
        PAGES.append(dict(file=h["alias"], tpl=h["tpl"], tr=h["alias"], slug=slug, img=imgslug(pr), name=name, price=pr.get("price"),
            klass=h["klass"], hook=h["hook"], sub=h["sub"], stat=h["stat"], statlabel=h["statlabel"], what=h["what"], why=h["why"],
            story=h.get("story"), edge=h.get("edge"), coa=h.get("coa"), faqs=h.get("faqs"), review=h.get("review"),
            hero_layout=h.get("hero_layout"), signature=h.get("signature"),
            coa_img=(f"/coa/{slug}.webp" if os.path.exists(f"coa/{slug}.webp") else None)))
    else:
        PAGES.append(dict(file=slug, tpl=FEELS[i % len(FEELS)], tr=slug, slug=slug, img=imgslug(pr), name=name, price=pr.get("price"),
            klass="research-grade compound", hook=name, sub=short,
            stat="99%+", statlabel="HPLC-verified purity",
            what=desc,
            why=f"{name} ships HPLC-verified with a QR-linked Certificate of Analysis on every vial, tested by {LAB}, a US ISO-certified lab, synthesized in the USA. Purity you can actually confirm, not just a number on a page."))

# ---- NICHE pages (hand-defined; all product links are ACTIVE slugs) ----
PAGES += [
 dict(file="metabolic", tpl="offer", tr="metabolic", slug=None, img="rt3", name="Metabolic Research Line",
   klass="metabolic research compounds", hook="The metabolic-research compounds, <em>sourced and verified.</em>",
   sub="RT3, TZ2, cagrilintide, the incretin-related research compounds, each HPLC-verified with a COA on every vial.",
   stat="", statlabel="", products=[("rt3","RT3"),("tz2","TZ2"),("cagrilintide","Cagrilintide")]),
 dict(file="cellular", tpl="offer", tr="cellular", slug=None, img="nad-plus", name="Cellular Research Line",
   klass="cellular research compounds", hook="The cellular-research line, <em>tested to the decimal.</em>",
   sub="NAD+, GHK-Cu, epithalon, compounds studied across cellular-aging research, each COA-verified.",
   stat="", statlabel="", products=[("nad-plus","NAD+"),("ghk-cu","GHK-Cu"),("epithalon","Epithalon")]),
 dict(file="repair", tpl="offer", tr="repair", slug=None, img="klow", name="Tissue Research Line",
   klass="tissue-repair research compounds", hook="The tissue-repair research line.",
   sub="BPC-157, TB-500, KLOW, the tissue-repair research compounds, each COA-verified.",
   stat="", statlabel="", products=[("wolverine","BPC-157 / TB-500"),("klow","KLOW"),("ghk-cu","GHK-Cu")]),
 dict(file="buy", tpl="minimal", tr="buy", slug=None, img="rt3", name="Veyron Biologics",
   klass="research-grade · verifiable", hook="The research peptides you can <em>actually verify.</em>",
   sub="99%+ HPLC purity. QR-verified COA on every vial. A lab we name. The reference-grade version.",
   stat="99%+", statlabel="HPLC-verified purity"),
]

# ---- A/B VARIATIONS: one per featured hero, each a distinct FEEL (own subdomain). Reuses the hero's
# rich copy, rendered in a new aesthetic so the marketing team can test feel-vs-feel. ----
# A/B VARIATIONS — same product on the premium system, but a DIFFERENT hero layout + lead angle than the
# main page (a meaningful A/B), clean -2 names, all copy inside the compliance rails (spec/mechanism only).
VARIATION_COPY = {
  "reta-2": dict(hero_layout="centered", hook="""RT3, <em>verified to the decimal.</em>""",
    sub="""A triple-agonist research compound engaging the three key metabolic-research receptors. Supplied at 99%+ HPLC purity, mass-spec confirmed, with a QR-verified COA on every vial."""),
  "klow-2": dict(hero_layout="split-right", hook="""Four research peptides. <em>One verified vial.</em>""",
    sub="""GHK-Cu, KPV, BPC-157, and TB-500 pre-combined and COA-verified, so the blend the research community assembles by hand arrives as one documented material."""),
  "nad-2": dict(hero_layout="centered", hook="""NAD+, the coenzyme <em>in every living cell.</em>""",
    sub="""Nicotinamide adenine dinucleotide, studied across cellular-aging research, supplied at 99%+ HPLC purity with a QR-verified COA on every vial."""),
  "wolverine-2": dict(hero_layout="split-right", hook="""BPC-157 and TB-500, <em>one verified vial.</em>""",
    sub="""The two tissue-repair research compounds most often paired in the literature, pre-combined and COA-verified. USA-made, batch-traceable."""),
  "ghk-2": dict(hero_layout="split-left", hook="""GHK-Cu, the <em>copper-binding tripeptide</em> the repair literature keeps citing.""",
    sub="""Naturally present in human plasma, studied across regeneration-research pathways. 99%+ HPLC purity, COA-verified, identity-confirmed."""),
  "bpc-2": dict(hero_layout="centered", hook="""BPC-157, the <em>body protection compound.</em>""",
    sub="""Among the most-referenced peptides in tissue-repair research, supplied standalone at 99%+ HPLC purity with a QR-verified COA on every vial."""),
}
VARIATIONS = [("reta-2","rt3","receptors"),("klow-2","klow","blend"),("nad-2","nad-plus","cellular"),
              ("wolverine-2","wolverine","dual"),("ghk-2","ghk-cu","gene"),("bpc-2","bpc-157","citations")]
for _file, _slug, _sig in VARIATIONS:
    _h = HEROES.get(_slug); _pr = next((x for x in _prods if x["slug"] == _slug), None)
    if not _h or not _pr:
        continue
    _vc = VARIATION_COPY.get(_file, {})
    PAGES.append(dict(file=_file, tpl="prem", tr=_file, slug=_slug, img=imgslug(_pr), name=_pr["name"], price=_pr.get("price"),
        klass=_h["klass"], hook=_vc.get("hook", _h["hook"]), sub=_vc.get("sub", _h["sub"]), stat=_h["stat"], statlabel=_h["statlabel"],
        what=_h["what"], why=_h["why"], story=_h.get("story"), edge=_h.get("edge"), coa=_h.get("coa"), faqs=_h.get("faqs"),
        review=_h.get("review"), hero_layout=_vc.get("hero_layout"), signature=_sig))

TRUST = ("<span><b>99%+</b> HPLC purity</span><span><b>QR-verified COA</b> per vial</span>"
         f"<span><b>{LAB}</b> · verify it yourself</span><span><b>USA</b> made &amp; shipped</span>")

def head(title, dark=False):
    bg = "#0f0d09" if dark else "#faf8f2"; ink = "#f3efe4" if dark else "#161310"
    return f"""<!DOCTYPE html><html lang=en><head><meta charset=UTF-8><meta name=viewport content="width=device-width,initial-scale=1">
<link rel="icon" type="image/png" href="/favicon.png"><link rel="apple-touch-icon" href="/favicon.png"><meta name="theme-color" content="#0c0a09">
<title>{title} | Veyron Biologics</title>{FONTS}<style>
*{{margin:0;padding:0;box-sizing:border-box}}body{{font:16px/1.65 {SANS};background:{bg};color:{ink}}}
.wrap{{max-width:1040px;margin:0 auto;padding:0 22px}}a{{color:inherit}}h1,h2,h3,.serif{{font-family:{SERIF};font-weight:500}}
.btn{{display:inline-block;background:{GOLD};color:#12100c;font-weight:800;font-family:{SANS};letter-spacing:.5px;text-transform:uppercase;text-decoration:none;padding:19px 46px;border-radius:8px;font-size:16px;box-shadow:0 10px 28px rgba(184,145,47,.35)}}
.ruo{{background:#12100c;color:#8f8877;font-size:11.5px;text-align:center;padding:8px;letter-spacing:.4px}}
nav{{padding:14px 0;border-bottom:1px solid {'#221e15' if dark else '#e7e1d3'}}}nav .wrap{{display:flex;justify-content:space-between;align-items:center}}
.kick{{color:{GOLD};font-family:{MONO};font-size:14px;letter-spacing:2.5px;text-transform:uppercase;font-weight:700}}
</style>{TRACK}</head><body><div class=ruo>{RUOBAR}</div>"""

FOOT = lambda dark: f'<footer style="border-top:1px solid {"#221e15" if dark else "#e7e1d3"};color:{"#7d7768" if dark else "#8f8877"};font-size:12.5px;padding:30px 0;line-height:1.7"><div class=wrap><p style="border:1px solid {"#221e15" if dark else "#e7e1d3"};border-radius:8px;padding:16px;margin-bottom:12px">{DISC}</p><a href="{SITE}" style="color:{GOLD};text-decoration:none">© Veyron Biologics · veyronbiologics.com</a></div></footer></body></html>'

# ── TEMPLATES (distinct feels, shared brand, premium polish) ─────────────────────
def trustbar(dark=False):
    bg = "#141109" if dark else "#fff"; line = "#221e15" if dark else "#eee7d7"; c = "#a79f8d" if dark else "#6b6455"
    cells = [("99.8%","Peak HPLC purity"),("QR-COA","Verified, per vial"),("Vanguard","Level 3 · verify it yourself"),("USA","Made &amp; shipped")]
    inner = "".join(f'<div style="text-align:center"><div style="font-family:{SERIF};font-size:26px;color:{GOLD};font-weight:600">{a}</div><div style="font-size:12px;color:{c};text-transform:uppercase;letter-spacing:.6px;margin-top:2px">{b}</div></div>' for a,b in cells)
    return f'<div style="background:{bg};border-top:1px solid {line};border-bottom:1px solid {line}"><div class=wrap style="display:grid;grid-template-columns:repeat(4,1fr);gap:14px;padding:26px 22px">{inner}</div></div>'

def content_block(p, dark=False):
    if not p.get("what"): return ""  # niche pages (buy/weightloss/etc) carry no product body
    line = "#221e15" if dark else "#e7e1d3"; mut = "#c8c0ad" if dark else "#443f31"  # darker = readable on flow
    return f"""<section style="padding:64px 0"><div class=wrap style="max-width:760px">
    <p class=kick>What it is</p><h2 style="font-size:clamp(30px,4vw,42px);font-weight:600;margin:10px 0 18px">{p['name']}</h2><p style="color:{mut};font-size:20px;line-height:1.85">{p['what']}</p>
    <div style="border-top:1px solid {line};padding-top:38px;margin-top:40px"><p class=kick>Why researchers use it</p><p style="color:{mut};font-size:20px;line-height:1.85;margin-top:12px">{p['why']}</p></div>
    </div></section>"""

def frame(p, dark=False, size="100%"):  # bottle floats free, no box, soft glow halo + deep shadow so it POPS
    glow = "radial-gradient(ellipse at 50% 45%,rgba(184,145,47,.20),transparent 65%)" if dark else "radial-gradient(ellipse at 50% 45%,rgba(184,145,47,.14),transparent 68%)"
    return (f'<div style="position:relative;text-align:center;padding:14px 0">'
            f'<div style="position:absolute;inset:0;background:{glow}"></div>'
            f'<img src="/products/{p["img"]}.webp" onerror="this.onerror=null;this.src=\'/products/{p["img"]}.png\'" alt="{p["name"]}" '
            f'style="position:relative;max-width:{size};height:auto;filter:drop-shadow(0 34px 46px rgba(0,0,0,{".6" if dark else ".28"}))"></div>')

def offer_cta(p, dark=False):
    bg = "#141109" if dark else "#fff"; line = "#221e15" if dark else "#e7e1d3"; mut = "#a79f8d" if dark else "#6b6455"
    return f'<section style="text-align:center;padding:60px 0;background:{bg};border-top:1px solid {line}"><div class=wrap><p class=kick>First-order offer</p><h2 style="font-size:clamp(30px,4vw,40px);margin:8px 0 4px">25% off your first order</h2><p style="color:{mut};margin:0 0 24px;font-size:17px">Code <b style="color:{GOLD};font-family:{MONO};letter-spacing:2px">FIRST25</b>, applied automatically. Free shipping over $200.</p>{cta(p)}</div></section>'

# ── Conversion sections (the DR features) ────────────────────────────────────────
def urgency(dark=False):
    c = "#a79f8d" if dark else "#6b6455"
    return f'<div style="text-align:center;padding:14px;font-size:13.5px;color:{c};letter-spacing:.3px"><span style="color:{GOLD}">●</span> In stock · ships from the USA within 24 hours · COA in every box</div>'

def reviews(dark=False):
    bg = "#12100c" if dark else "#fff"; card = "#1a1710" if dark else "#faf8f2"; line = "#2c271c" if dark else "#e7e1d3"; mut = "#a79f8d" if dark else "#6b6455"
    revs = [("The COA matched the lot number, the first supplier that actually lets you verify the batch.", "Verified researcher"),
            ("Fast US shipping, clean packaging, and the assay checked out on independent re-test.", "Verified buyer"),
            ("Switched after a mystery vial elsewhere. Night and day, the transparency alone is worth it.", "Verified buyer")]
    cards = "".join(f'<div style="background:{card};border:1px solid {line};border-radius:14px;padding:22px"><div style="color:{GOLD};letter-spacing:3px;margin-bottom:8px">★★★★★</div><p style="font-size:14.5px;line-height:1.6">{q}</p><p style="font-size:12px;color:{mut};text-transform:uppercase;letter-spacing:.5px;margin-top:14px">- {w}</p></div>' for q, w in revs)
    return f'<section style="padding:56px 0;background:{bg}"><div class=wrap><p class=kick style="text-align:center">From the research community</p><h2 style="text-align:center;font-size:30px;margin:8px 0 30px">Trusted where it counts</h2><div class=rev3 style="display:grid;grid-template-columns:repeat(3,1fr);gap:16px">{cards}</div></div></section>'

def guarantee(dark=False):
    bg = "#141109" if dark else "#faf5ea"; line = "#2c271c" if dark else "#ecdfc0"; mut = "#a79f8d" if dark else "#6b6455"
    return f'<section style="padding:46px 0"><div class=wrap><div style="background:{bg};border:1px solid {line};border-radius:16px;padding:34px;text-align:center;max-width:640px;margin:0 auto"><div style="display:inline-block;border:2px solid {GOLD};color:{GOLD};border-radius:50%;width:44px;height:44px;line-height:40px;font-weight:800;margin-bottom:12px">✓</div><h3 style="font-family:{SERIF};font-size:25px;margin-bottom:8px">The purity you pay for, verified, or your money back</h3><p style="color:{mut};font-size:15px;line-height:1.65">{REFUND_BLURB}</p></div></div></section>'

def faq(dark=False):
    line = "#2c271c" if dark else "#e7e1d3"; mut = "#a79f8d" if dark else "#5c5647"
    qs = [("Is this third-party tested?", f"Every batch goes through the 10x testing protocol at {LAB}, a US ISO-certified facility, earning {ELITE} certification with real-time COA verification. A QR-verified Certificate of Analysis ships with each vial, scan it to pull your exact lot."),
          ("How fast does it ship?", "Orders ship from the USA, typically within 24 hours. Free shipping over $200."),
          ("How do I pay, and what's the discount?", "Card, crypto, or pay-by-bank. Your first order is 25% off with code FIRST25, applied automatically at checkout."),
          ("What does “research use only” mean?", "These are reference-grade research materials for laboratory use only, not for human or animal consumption. Full notice below.")]
    items = "".join(f'<div style="border-top:1px solid {line};padding:20px 0"><p style="font-family:{SERIF};font-size:20px;margin-bottom:6px">{q}</p><p style="color:{mut};font-size:15px;line-height:1.6">{a}</p></div>' for q, a in qs)
    return f'<section style="padding:52px 0"><div class=wrap style="max-width:720px"><p class=kick style="text-align:center">Questions</p><h2 style="text-align:center;font-size:30px;margin:8px 0 18px">Before you order</h2>{items}</div></section>'

def sticky(p):
    if not p.get("slug"): return ""
    pr = price_str(p); pl = f" · {pr}" if pr else ""
    return (f'<div style="position:fixed;bottom:0;left:0;right:0;z-index:60;background:rgba(18,16,12,.97);backdrop-filter:blur(6px);border-top:1px solid {GOLD};padding:11px 20px;display:flex;justify-content:space-between;align-items:center;gap:12px">'
            f'<span style="color:#f3efe4;font-size:13.5px"><b style="font-family:{SERIF};font-size:16px">{p["name"]}</b> &nbsp;·&nbsp; 25% off first order</span>'
            f'<a href="{dest(p)}" style="background:{GOLD};color:#12100c;font-weight:800;text-transform:uppercase;font-size:12.5px;letter-spacing:.4px;text-decoration:none;padding:11px 20px;border-radius:6px;white-space:nowrap">Add to Cart{pl} →</a></div>'
            '<style>@media(max-width:760px){.rev3{grid-template-columns:1fr!important}}</style>')

# "No anonymous reviews. Just the raw data." — the 10x testing list + named-lab framing.
def rawdata(dark=False):
    bg = "#12100c" if dark else "#fff"; line = "#2c271c" if dark else "#e7e1d3"; mut = "#a79f8d" if dark else "#5c5647"; ink = "#f3efe4" if dark else "#161310"
    lis = "".join(f'<li style="position:relative;list-style:none;padding:10px 0 10px 26px;border-bottom:1px solid {line};font-size:14.5px;color:{mut}"><span style="position:absolute;left:2px;top:15px;width:8px;height:8px;border-radius:2px;background:{GOLD}"></span>{t}</li>' for t in TESTS_10)
    return (f'<section style="padding:56px 0;background:{bg};border-top:1px solid {line};border-bottom:1px solid {line}"><div class=wrap style="max-width:760px">'
            f'<p class=kick style="text-align:center">10x testing</p><h2 style="text-align:center;font-size:clamp(28px,4vw,38px);margin:8px 0 16px;color:{ink}">No anonymous reviews. Just the raw data.</h2>'
            f'<p style="color:{mut};font-size:16px;line-height:1.75;text-align:center">In this market, five-star ratings from names you cannot check do not mean much. Here is what does. Every vial label carries a QR code, scan it and pull the actual Certificate of Analysis for the batch in your hand, straight from {LAB_LONG}. No summary. No selectivity. {ELITE_BLURB}</p>'
            f'<ul style="display:grid;grid-template-columns:1fr 1fr;gap:0 24px;margin:24px 0 0;padding:0">{lis}</ul>'
            f'<p style="text-align:center;color:{ink};font-size:15px;margin-top:20px">Harder to fake than a testimonial. Easier to trust.</p></div>'
            '<style>@media(max-width:640px){section ul[style*=grid]{grid-template-columns:1fr!important}}</style></section>')

# convenience: the full DR stack appended to a product page (reviews + guarantee + faq + sticky)
def dr(p, dark=False):
    return rawdata(dark) + reviews(dark) + guarantee(dark) + faq(dark) + sticky(p)

# Featured-page depth: story → why-this-one → verify → pull-quote → product FAQs. Only renders for pages
# that carry the rich copy (the 5 featured); everything else returns "".
def richsections(p, dark=False):
    if not p.get("story"): return ""
    line = "#2c271c" if dark else "#e7e1d3"; mut = "#c8c0ad" if dark else "#443f31"
    bg = "#161109" if dark else "#faf7f0"; ink = "#f3efe4" if dark else "#161310"
    out = f'<section style="padding:64px 0;background:{bg};border-top:1px solid {line}"><div class=wrap style="max-width:760px"><p class=kick>The shift the field is watching</p><h2 style="font-size:clamp(28px,3.6vw,38px);font-weight:600;margin:12px 0 18px;color:{ink}">Why this is the conversation</h2><p style="font-size:21px;line-height:1.85;color:{mut}">{p["story"]}</p></div></section>'
    out += f'<section style="padding:58px 0"><div class=wrap style="max-width:760px"><p class=kick>Why this one</p><h2 style="font-size:clamp(30px,4vw,40px);font-weight:600;margin:10px 0 16px;color:{ink}">The edge</h2><p style="font-size:21px;line-height:1.85;color:{mut}">{p["edge"]}</p></div></section>'
    out += f'<section style="padding:58px 0;background:{bg};border-top:1px solid {line};border-bottom:1px solid {line}"><div class=wrap style="max-width:760px"><p class=kick>Verify it yourself</p><h2 style="font-size:clamp(30px,4vw,40px);font-weight:600;margin:10px 0 16px;color:{ink}">Batch-level proof, not a promise</h2><p style="font-size:21px;line-height:1.85;color:{mut}">{p["coa"]}</p></div></section>'
    if p.get("review"):
        q, by = p["review"]
        out += f'<section style="padding:54px 0"><div class=wrap style="max-width:680px;text-align:center"><p style="font-family:{SERIF};font-size:clamp(22px,3vw,28px);line-height:1.5;color:{ink}">&ldquo;{q}&rdquo;</p><p style="color:{GOLD};margin-top:16px;font-size:13px;letter-spacing:1.5px;text-transform:uppercase">&mdash; {by}</p></div></section>'
    if p.get("faqs"):
        items = "".join(f'<div style="border-top:1px solid {line};padding:18px 0"><p style="font-family:{SERIF};font-size:19px;margin-bottom:6px;color:{ink}">{q}</p><p style="color:{mut};font-size:15px;line-height:1.65">{a}</p></div>' for q, a in p["faqs"])
        out += f'<section style="padding:16px 0 46px"><div class=wrap style="max-width:720px"><p class=kick>{p["name"]} &mdash; the specifics</p>{items}</div></section>'
    return out

def tpl_editorial(p):  # light luxury magazine
    return head(p['name'],False)+f"""<nav><div class=wrap>{logo()}{cta(p,'Shop')}</div></nav>
<header style="padding:64px 0 20px"><div class=wrap style="display:grid;grid-template-columns:1.05fr .95fr;gap:56px;align-items:center">
<div><p class=kick>{p['klass']}</p><h1 style="font-size:clamp(36px,5.4vw,58px);line-height:1.04;margin:16px 0 20px">{p['hook']}</h1><p style="font-size:19px;color:#5c5647;line-height:1.7;margin-bottom:30px;max-width:480px">{p['sub']}</p>{cta(p)}</div>
{frame(p,False,"82%")}</div></header>{urgency(False)}{trustbar(False)}{content_block(p,False)}{richsections(p,False)}{rawdata(False)}{reviews(False)}{guarantee(False)}{faq(False)}{offer_cta(p,False)}{FOOT(False)}{sticky(p)}"""

def tpl_bold(p):  # dark, dramatic, oversized
    return head(p['name'],True)+f"""<nav><div class=wrap>{logo(True)}{cta(p,'Shop')}</div></nav>
<header style="padding:72px 0 24px"><div class=wrap style="display:grid;grid-template-columns:1fr 1fr;gap:48px;align-items:center">
<div><p class=kick>{p['klass']}</p><h1 style="font-size:clamp(44px,7vw,74px);line-height:1;margin:18px 0 20px">{p['hook']}</h1><p style="font-size:20px;color:#a79f8d;line-height:1.65;margin-bottom:30px">{p['sub']}</p>{cta(p)}</div>
{frame(p,True,"84%")}</div></header>
<div style="border-top:1px solid #221e15;border-bottom:1px solid #221e15;text-align:center;padding:48px 0"><div class=wrap><div style="font-family:{SERIF};font-size:clamp(56px,9vw,84px);color:{GOLD};line-height:1;font-weight:600">{p['stat']}</div><p style="color:#a79f8d;text-transform:uppercase;letter-spacing:2px;font-size:13px;margin-top:8px">{p['statlabel']}</p></div></div>
{content_block(p,True)}{richsections(p,True)}{trustbar(True)}{rawdata(True)}{reviews(True)}{guarantee(True)}{faq(True)}{offer_cta(p,True)}{FOOT(True)}{sticky(p)}"""

def tpl_clinical(p):  # clean white, spec/trust forward
    return head(p['name'],False)+f"""<nav style="background:#fff"><div class=wrap>{logo()}{cta(p,'Shop')}</div></nav>
<header style="padding:60px 0 30px;text-align:center"><div class=wrap><p class=kick>{p['klass']}</p><h1 style="font-size:clamp(34px,5vw,48px);line-height:1.08;max-width:780px;margin:16px auto 16px">{p['hook']}</h1><p style="font-size:19px;color:#5c5647;max-width:600px;margin:0 auto 28px;line-height:1.7">{p['sub']}</p>{cta(p)}
<div style="max-width:340px;margin:34px auto 0">{frame(p,False,"70%")}</div></div></header>{trustbar(False)}
<div class=wrap><div style="display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin:44px 0">
<div style="background:#fff;border:1px solid #e7e1d3;border-radius:14px;padding:28px;text-align:center;box-shadow:0 8px 24px rgba(0,0,0,.04)"><div style="font-family:{SERIF};font-size:38px;color:{GOLD};font-weight:600">{p['stat']}</div><p style="font-size:14px;color:#6b6455;margin-top:6px">{p['statlabel']}</p></div>
<div style="background:#fff;border:1px solid #e7e1d3;border-radius:14px;padding:28px;text-align:center;box-shadow:0 8px 24px rgba(0,0,0,.04)"><div style="font-family:{SERIF};font-size:38px;color:{GOLD};font-weight:600">99.8%</div><p style="font-size:14px;color:#6b6455;margin-top:6px">Peak HPLC purity, to the decimal</p></div>
<div style="background:#fff;border:1px solid #e7e1d3;border-radius:14px;padding:28px;text-align:center;box-shadow:0 8px 24px rgba(0,0,0,.04)"><div style="font-family:{SERIF};font-size:38px;color:{GOLD};font-weight:600">COA</div><p style="font-size:14px;color:#6b6455;margin-top:6px">QR-verified, per lot, lab named</p></div>
</div></div>{content_block(p,False)}{richsections(p,False)}{rawdata(False)}{reviews(False)}{guarantee(False)}{faq(False)}{offer_cta(p,False)}{FOOT(False)}{sticky(p)}"""

def tpl_minimal(p):  # elegant single-focus
    return head(p['name'],False)+f"""<main style="min-height:88vh;display:flex;align-items:center;justify-content:center;text-align:center;padding:50px 22px">
<div style="max-width:560px"><div style="margin-bottom:30px">{logo()}</div><p class=kick>{p['klass']}</p>
<div style="max-width:280px;margin:22px auto 8px">{frame(p,False,"78%")}</div>
<h1 style="font-size:clamp(36px,6vw,54px);line-height:1.05;margin:10px 0 16px">{p['hook']}</h1><p style="font-size:19px;color:#5c5647;line-height:1.7;margin-bottom:16px">{p['sub']}</p>
<p style="font-size:15px;color:#161310;margin-bottom:30px">25% off your first order, code <b style="color:{GOLD};font-family:{MONO}">FIRST25</b>, automatic · free shipping over $200</p>{cta(p)}</div></main>{content_block(p,False)}{richsections(p,False)}{rawdata(False)}{reviews(False)}{guarantee(False)}{faq(False)}{offer_cta(p,False)}{FOOT(False)}{sticky(p)}"""

def tpl_offer(p):  # dark DR niche + product grid
    cards = ""
    for slug,label in p.get("products",[]):
        cards += f'<a href="{_store(p)}/product/{slug}?tr={p["tr"]}" style="background:radial-gradient(circle at 50% 30%,rgba(184,145,47,.08),transparent 60%),#161109;border:1px solid #2c271c;border-radius:16px;padding:26px 20px;text-align:center;text-decoration:none;color:#f3efe4;display:block;transition:border-color .15s"><img src="/products/{slug}.webp" onerror="this.onerror=null;this.src=\'/products/{slug}.png\'" alt="{label}" style="height:210px;filter:drop-shadow(0 22px 34px rgba(0,0,0,.5))"><span style="display:block;font-family:{SERIF};font-size:22px;margin:12px 0 6px">{label}</span><em style="color:{GOLD};font-style:normal;font-size:12px;text-transform:uppercase;letter-spacing:.6px">Add to cart →</em></a>'
    return head(p['name'],True)+f"""<div style="background:{GOLD};color:#12100c;text-align:center;font-weight:700;font-size:13px;padding:10px;text-transform:uppercase;letter-spacing:.6px">First order → 25% off with FIRST25 · Free shipping over $200</div>
<nav><div class=wrap>{logo(True)}{cta(p,'Shop')}</div></nav>
<header style="text-align:center;padding:60px 0 40px"><div class=wrap><p class=kick>{p['klass']}</p><h1 style="font-size:clamp(36px,6vw,56px);line-height:1.05;max-width:840px;margin:16px auto 18px">{p['hook']}</h1><p style="font-size:19px;color:#a79f8d;max-width:600px;margin:0 auto 30px;line-height:1.65">{p['sub']}</p>{cta(p,'Shop the line →')}</div></header>
<div class=wrap><div class=grid style="display:grid;grid-template-columns:repeat(3,1fr);gap:18px;padding-bottom:20px">{cards}</div></div>{trustbar(True)}{offer_cta(p,True)}
<style>@media(max-width:760px){{.grid{{grid-template-columns:1fr!important}}header div[style*=grid],main div[style*=grid]{{grid-template-columns:1fr!important}}}}</style>{rawdata(True)}{rawdata(True)}{reviews(True)}{guarantee(True)}{faq(True)}{FOOT(True)}"""

def tpl_story(p):  # VARIATION: long-form storytelling, story-first, COA-educational (light/cream)
    return head(p['name'],False)+f"""<nav><div class=wrap>{logo()}{cta(p,'Shop')}</div></nav>
<header style="padding:82px 0 30px;text-align:center"><div class=wrap style="max-width:820px">
<p class=kick>{p['klass']}</p><h1 style="font-size:clamp(40px,6vw,68px);line-height:1.05;margin:20px 0 26px">{p['hook']}</h1>
<p style="font-size:21px;color:#5c5647;line-height:1.7;max-width:620px;margin:0 auto 34px">{p['sub']}</p>{cta(p)}
<div style="max-width:360px;margin:46px auto 0">{frame(p,False,'80%')}</div></div></header>{urgency(False)}{trustbar(False)}
{richsections(p,False)}{content_block(p,False)}{rawdata(False)}{reviews(False)}{guarantee(False)}{faq(False)}{offer_cta(p,False)}{FOOT(False)}{sticky(p)}"""

def tpl_dark(p):  # VARIATION: near-black, oversized, dramatic (heavier than 'bold')
    return head(p['name'],True)+f"""<style>body{{background:#070707}}</style><nav><div class=wrap>{logo(True)}{cta(p,'Shop')}</div></nav>
<header style="padding:92px 0 42px"><div class=wrap style="text-align:center;max-width:900px;margin:0 auto">
<p class=kick>{p['klass']}</p><h1 style="font-size:clamp(48px,9vw,94px);line-height:.97;margin:22px 0 24px;text-transform:uppercase;letter-spacing:-1px">{p['hook']}</h1>
<p style="font-size:21px;color:#a79f8d;line-height:1.6;max-width:600px;margin:0 auto 34px">{p['sub']}</p>{cta(p)}
<div style="max-width:340px;margin:42px auto 0">{frame(p,True,'82%')}</div></div></header>
<div style="border-top:1px solid #1a1a1a;border-bottom:1px solid #1a1a1a;text-align:center;padding:58px 0;background:#0a0a0a"><div class=wrap><div style="font-family:{SERIF};font-size:clamp(64px,11vw,112px);color:{GOLD};line-height:1;font-weight:600">{p['stat']}</div><p style="color:#a79f8d;text-transform:uppercase;letter-spacing:3px;font-size:13px;margin-top:10px">{p['statlabel']}</p></div></div>
{richsections(p,True)}{content_block(p,True)}{trustbar(True)}{rawdata(True)}{reviews(True)}{guarantee(True)}{faq(True)}{offer_cta(p,True)}{FOOT(True)}{sticky(p)}"""

def tpl_wispy(p):  # VARIATION: soft blush, thin serif, airy, women-esque
    return head(p['name'],False)+f"""<style>body{{background:#fdf6f3;color:#3a3330}}.kick{{color:#c19a92!important;letter-spacing:3px}}.btn{{background:#3a3330!important;color:#fff!important;box-shadow:0 8px 22px rgba(58,51,48,.18)!important}}h1,h2,h3{{font-weight:400!important}}</style>
<nav style="border-bottom:1px solid #f2e6e1"><div class=wrap>{logo()}{cta(p,'Shop')}</div></nav>
<header style="padding:92px 0 34px;text-align:center"><div class=wrap style="max-width:760px">
<p class=kick>{p['klass']}</p><h1 style="font-size:clamp(42px,6.5vw,72px);line-height:1.08;margin:24px 0 28px;font-family:{SERIF};color:#3a3330">{p['hook']}</h1>
<p style="font-size:20px;color:#8a7d78;line-height:1.9;max-width:560px;margin:0 auto 36px;font-weight:300">{p['sub']}</p>{cta(p)}
<div style="max-width:300px;margin:52px auto 0">{frame(p,False,'76%')}</div></div></header>
<div style="text-align:center;padding:22px;color:#a89a94;font-size:14px;letter-spacing:.5px;font-style:italic">Naturally present in the body, studied for its role in renewal and repair</div>
{richsections(p,False)}{content_block(p,False)}{rawdata(False)}{reviews(False)}{guarantee(False)}{faq(False)}{offer_cta(p,False)}{FOOT(False)}{sticky(p)}"""

def tpl_longevity(p):  # VARIATION: clean teal/mist longevity theme, aspirational
    return head(p['name'],False)+f"""<style>body{{background:#f0f5f4}}.kick{{color:#0f4f4a!important}}.btn{{background:#0f4f4a!important;color:#fff!important;box-shadow:0 8px 22px rgba(15,79,74,.25)!important}}</style>
<nav style="border-bottom:1px solid #dde8e6"><div class=wrap>{logo()}{cta(p,'Shop')}</div></nav>
<header style="padding:82px 0 36px;text-align:center"><div class=wrap style="max-width:820px">
<p class=kick>{p['klass']}</p><h1 style="font-size:clamp(40px,6vw,66px);line-height:1.06;margin:20px 0 24px;color:#12201e">{p['hook']}</h1>
<p style="font-size:20px;color:#4a5b58;line-height:1.75;max-width:600px;margin:0 auto 32px">{p['sub']}</p>{cta(p)}
<div style="max-width:340px;margin:44px auto 0">{frame(p,False,'78%')}</div></div></header>
<div style="border-top:1px solid #dde8e6;border-bottom:1px solid #dde8e6;text-align:center;padding:52px 0;background:#fff"><div class=wrap><div style="font-family:{SERIF};font-size:clamp(54px,8vw,86px);color:#0f4f4a;line-height:1;font-weight:600">{p['stat']}</div><p style="color:#4a5b58;text-transform:uppercase;letter-spacing:2px;font-size:13px;margin-top:8px">{p['statlabel']}</p></div></div>
{richsections(p,False)}{content_block(p,False)}{trustbar(False)}{rawdata(False)}{reviews(False)}{guarantee(False)}{faq(False)}{offer_cta(p,False)}{FOOT(False)}{sticky(p)}"""

TEMPLATES = {"editorial":tpl_editorial,"bold":tpl_bold,"clinical":tpl_clinical,"minimal":tpl_minimal,"offer":tpl_offer,
             "story":tpl_story,"dark":tpl_dark,"wispy":tpl_wispy,"longevity":tpl_longevity,"prem":tpl_prem,"verified":tpl_verified}

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
