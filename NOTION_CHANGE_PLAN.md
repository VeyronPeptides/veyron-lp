# LP copy update from Cam's Notion feedback (2026-07-08)
Source: berry-fish-cc0.notion.site/Veyron-397ce5bd… — Cam's feedback on the 9 live LP subdomains.
Full copy: NOTION_FEEDBACK_2026-07-08.txt

## Targets (9 LP subdomains)
- reta.veyronbiologics.com (retatrutide) · klow · nad.→nad-plus · wolverine · ghk.→ghk-cu · bpc
- metabolic (Metabolic Research Line) · cellular (Cellular Research Line) · repair (Tissue Research Line)

## The consistent uplift (apply to ALL 9 — best as a SHARED template section in generate.py)
1. Name the lab: "Vanguard Labs" (independent, ISO-certified, US). Replaces generic "named third-party lab".
2. "Elite Level 3 Verified by Vanguard" — real-time COA verification, can't be faked/replicated/duplicated.
3. "10x testing" + list: HPLC chromatogram, spec-analysis/identity (spectrum), endotoxin, heavy metals,
   solubility/containment, FDA USP 71 sterility, vial integrity/conformity, exact batch number (+purity, +lot release).
4. Refund guarantee: if COA purity doesn't match, full refund/replacement. (STANDARDIZE the window — Notion has
   14 days on Reta, 30 on Metabolic → pick ONE, e.g. 30 days.)
5. "No anonymous reviews. Just the raw data." section — QR → raw batch report, harder to fake than a testimonial.

## Per-page fixes
- NAD: replace "[QUANTITY: State Vial Size/Mass Here]" placeholder with the real vial size.
- Typos to fix: "assayed by a Vanguard Labs" (drop 'a'), "under goes"→"undergoes", "t 99%+"→"to 99%+".
- bpc + metabolic/cellular/repair are defined minimally in generate.py (sub= only) — need full RICH entries
  or the shared section carries them.

## COMPLIANCE FLAG (raised to Cam 2026-07-08)
- Metabolic Research Line bundles Retatrutide + Tirzepatide + Cagrilintide. CLAUDE.md: don't bundle GLP-1s
  (reta/cagri) into weight-loss stacks. Notion copy is RUO "research line" framed (not weight-loss) → likely OK
  as a catalog/collection page, but it's the page a processor/FDA looks at twice. Cam aware.

## Deploy: veyron-lp = git push (GitHub Pages via Cloudflare Worker). Static — no Render restart, so the
## batch-deploy rule (Render 2-instance) doesn't apply here, but still do it as one clean push.
