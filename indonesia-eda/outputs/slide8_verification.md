# Slide 8 — pre-build verification record

**Date:** 2026-09-01 · **Verdict: all three checks PASS.**
Sign-off on the slide-8 inputs before the slide was built. Kept because these are the exact
questions a judge would ask about the numbers on the slide.

Inputs verified:
- `outputs/tables/slide8_mocaf_blend_matrix.csv`
- `outputs/figures/idn_slide8_blend_and_savings.png` (two-panel deck asset)
- `outputs/figures/idn_mocaf_blend_requirement.png` (single-panel analytical version)

Reproduce with: `notebooks/05_cassava_substitution.ipynb` §6 · `python tools/check_stale_numbers.py`

---

## Check 1 — the matrix is final, and every dollar figure is on the labelled FOB basis ✅

Final values (rounded for reading; CSV carries full precision):

| blend | MOCAF conversion | flour Mt | fresh cassava Mt | % of crop | wheat avoided Mt | saved USDbn (FOB) | % fundable by yield gap |
|---|---|---|---|---|---|---|---|
| 5%  | community sun-dried (~20%) | 0.49 | 2.45 | 15.7 | 0.49 | 0.13 | 165.9 |
| 5%  | lab tape-yeast (~34.6%)    | 0.49 | 1.42 |  9.1 | 0.49 | 0.13 | 287.0 |
| 10% | community sun-dried (~20%) | 0.98 | 4.90 | 31.4 | 0.98 | 0.26 |  82.9 |
| 10% | lab tape-yeast (~34.6%)    | 0.98 | 2.83 | 18.1 | 0.98 | 0.26 | 143.5 |
| 15% | community sun-dried (~20%) | 1.47 | 7.35 | 47.0 | 1.47 | 0.39 |  55.3 |
| 15% | lab tape-yeast (~34.6%)    | 1.47 | 4.25 | 27.2 | 1.47 | 0.39 |  95.7 |
| 20% | community sun-dried (~20%) | 1.96 | 9.80 | 62.7 | 1.96 | 0.52 |  41.5 |
| 20% | lab tape-yeast (~34.6%)    | 1.96 | 5.66 | 36.3 | 1.96 | 0.52 |  71.7 |

**Basis audit:**
- **Exactly one monetary column**, `saved_USDbn_FOB_mean` — the basis is *in the column name*, so it
  cannot be quoted without it.
- **Implied price is $265.335/t on all eight rows** (`saved × 1000 ÷ wheat_avoided`), matching the
  loader exactly: `load_wheat_prices()` → HRW mean **$265.3352/t**, 199 months 2010M01–2026M07,
  vintage *"Updated on August 04, 2026"*, basis *"FOB export price, US Gulf — NOT CIF Indonesia"*.
- **No standalone `300` token** in the file (regex-verified). A naive substring grep *does* hit — it is
  float noise inside `0.13001423618090452`, **not** a price. Recorded so nobody re-raises it.
- **No CIF column**, and **no monetary column lacking a basis tag.**

**Open nit (not fixed — analysis is frozen):** the CSV carries raw float noise
(`0.13001423618090452` rather than `0.13`). Numerically correct, but someone may paste it verbatim.
Use the rounded table above for the slide. Rounding the export would mean editing nb 05 and re-running.

---

## Check 2 — the "8.3–14.3% blend, no new land" headline traces cleanly ✅

**Important caveat: this is not a column in the matrix.** It is recoverable from it in two steps, and
reconciles exactly — but reproduction needs two inputs the CSV does not carry.

**Step 1 — recover the yield-gap headroom from CSV columns alone:**
```
fresh_cassava_Mt × %_fundable_by_yield_gap ÷ 100
    = 2.832370 × 1.434991
    = 4.064426 Mt
```
Recovered identically from **all 8 rows** (min = max = 4.064426) — the matrix is internally consistent.

**Step 2 — express that new cassava as a share of food-wheat demand:**
```
community sun-dried : 4.0644 Mt × 0.20  ÷ 9.8 MMT = 8.295%  ->  8.3%
lab tape-yeast      : 4.0644 Mt × 0.346 ÷ 9.8 MMT = 14.350% -> 14.3%
```

**Two inputs live outside the CSV** — flag if anyone tries to reproduce from the CSV in isolation:
1. **Food-wheat demand 9.8 MMT** — USDA GAIN ID2026-0010, not derived here.
2. **The conversion rates** (0.20 / 0.346) — present only inside the `mocaf_conversion` label text.

---

## Check 3 — both cassava ranks are correct, and they are not in conflict ✅

Recomputed from `load_qcl_world('Cassava, fresh')`, 2024, region aggregates and FAOSTAT's China
composite dropped.

**By production volume — #6 of 97 countries:**

| # | Country | Mt |
|---|---|---|
| 1 | Nigeria | 62.62 |
| 2 | DR Congo | 46.56 |
| 3 | Thailand | 28.62 |
| 4 | Ghana | 27.92 |
| 5 | Brazil | 19.07 |
| **6** | **Indonesia** | **15.62** |

**By yield among peer-scale producers (≥50,000 ha) — #2 of 40:**

| # | Country | t/ha |
|---|---|---|
| 1 | India | 35.6 |
| **2** | **Indonesia** | **28.2** |
| 3 | Ghana | 25.9 |
| 4 | Malawi | 25.5 |
| 5 | Laos | 25.1 |

**No conflict — different metrics.** Indonesia is a mid-sized grower that farms unusually well:
**4.6% of world cassava output** (342 Mt global, 2024) on near-frontier yields.

### Agreed slide phrasing

> **Indonesia is the world's #6 cassava producer by volume — and #2 by yield among the 40 countries
> that grow it at scale.**

Two precisions against the shorter "#6 by volume, #2 by yield among peers":
- **"among the 40 countries that grow it at scale"**, not "among peers" — "peers" is undefined to an
  audience, and the **≥50,000 ha filter is load-bearing**: unfiltered, the global yield leader is
  **Guyana on 2,399 ha**, which inflates Indonesia's apparent gap from **20.6% to 32%**.
- **"by volume"** stated explicitly on the #6, since a bare "#6 producer" reads as capability
  rather than scale.

**Why it earns slide space:** it pre-empts the obvious challenge. It concedes the yield lever is
nearly exhausted *before* anyone asks — Indonesia is already second-best in the world — which is what
makes land retention and processing yield the credible asks instead of "grow cassava better".
