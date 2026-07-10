# Shared trust/verification language across BOTH LP engines (premium.py + generate.py).
# Single source of truth for Cam's Notion feedback (2026-07-08): name the lab, Elite Level 3,
# 10x testing list, standardized refund window, "raw data" framing. Section HTML stays per-engine
# (different CSS), but the WORDS live here so the two engines never drift.
LAB = "Vanguard Labs"
LAB_LONG = "Vanguard Labs, an independent ISO-certified US testing facility"
ELITE = "Elite Level 3 Verified by Vanguard"
REFUND_DAYS = 30  # standardized window (Notion had 14 on Reta / 30 on Metabolic → one number)

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
