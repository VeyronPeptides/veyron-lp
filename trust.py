# Shared trust/verification language across BOTH LP engines (premium.py + generate.py).
# Single source of truth for Cam's Notion feedback (2026-07-08): name the lab, Elite Level 3,
# 10x testing list, standardized refund window, "raw data" framing. Section HTML stays per-engine
# (different CSS), but the WORDS live here so the two engines never drift.
LAB = "Vanguard Labs"
LAB_LONG = "Vanguard Labs, an independent ISO-certified US testing facility"
ELITE = "Elite Level 3 Verified by Vanguard"
REFUND_DAYS = 30  # standardized window (Notion had 14 on Reta / 30 on Metabolic → one number)

# ── Hyros universal tracking (Team 1 attribution, account 216899, added 2026-07-16) ──────────────
# Client-side click/lead/pageview tracker. MUST be on the landers too (that's where the ad click lands) —
# same full-funnel lesson as the Meta pixel. Loads as high in <head> as we inject. Sales/revenue come from
# the Hyros↔WooCommerce API integration on live.veyron, not this script.
HYROS = """<script>var head=document.head;var script=document.createElement('script');script.type='text/javascript';script.src="https://216899.t.hyros.com/v1/lst/universal-script?ph=af50f23a1eaa9188de2347020b6184aaa156b29db55a3354515c9ac3afe7689d&tag=!clicked&ref_url="+encodeURI(document.URL);head.appendChild(script);</script>"""

# ── Per-runner Meta pixel + attribution pass-through (added 2026-07-14) ───────────────────────────
# The ad tags the lander URL with ?tr=<runner> (odhfgwv=John / jkrehez=Caleb). This snippet, injected into
# every lander <head>, (1) fires THAT runner's pixel on the lander pageview via veyronbiologics.com/px.js,
# and (2) rewrites every live.veyron CTA to carry the same ?tr=<runner> so the runner's pixel fires on the
# store too and attribution survives the hand-off. Before this the landers had ZERO pixels and hard-coded
# product codes (reta/bpc/…) that resolved to house/no-pixel — the whole ad→lander→store funnel was dark,
# which is exactly why runners saw no events. px.js resolves the runner→pixel server-side (nothing baked in).
# HYROS is prepended so it loads first (Hyros wants to be as high in <head> as possible).
TRACK = HYROS + """<script>!function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');(function(){var tr=(new URLSearchParams(location.search).get('tr')||'').replace(/[^a-zA-Z0-9_-]/g,'').slice(0,48);var s=document.createElement('script');s.async=true;s.src='https://app.veyronbiologics.com/px.js'+(tr?'?tr='+encodeURIComponent(tr):'');document.head.appendChild(s);if(tr){var ap=function(){document.querySelectorAll('a[href*="veyronbiologics.com"]').forEach(function(n){try{var u=new URL(n.href);u.searchParams.set('tr',tr);n.href=u.toString();}catch(e){}});};if(document.readyState!='loading')ap();else document.addEventListener('DOMContentLoaded',ap);}})();</script>"""

# The 10x testing protocol — the exact ten checkpoints, in order, every batch passes before it ships.
TESTS_10 = [
    "HPLC chromatogram",
    "Spectrum analysis for identity confirmation",
    "Endotoxin screening",
    "Heavy metal testing",
    "Solubility and containment screening",
    "USP 61 bioburden screening",
    "Vial integrity and conformity",
    "Exact batch number",
    "Purity threshold confirmation",
    "Final lot release",
]

# One-liner describing the certification (reused in trust cards + FAQ answers).
ELITE_BLURB = (f"Every batch earns {ELITE} certification — real-time verification of every Certificate "
               "of Analysis, that cannot be faked, replicated, or duplicated.")
REFUND_BLURB = (f"Scan the QR on your vial and pull the batch report from {LAB}. If the HPLC purity "
                f"does not match what we state, contact us within {REFUND_DAYS} days of delivery for a "
                "full refund or replacement. The data is the arbiter.")
