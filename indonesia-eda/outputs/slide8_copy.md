# Slide 8 — ready-to-paste copy

Asset: `outputs/figures/idn_slide8_blend_and_savings.png` (200 dpi)
Data:  `outputs/tables/slide8_mocaf_blend_matrix.csv`
Built by: `notebooks/05_cassava_substitution.ipynb` §6 ("SLIDE 8 ASSET" cell)

Every number below is reproduced by that notebook. Nothing here is an unsourced estimate except
the items explicitly labelled **assumption**.

---

## Title
> **The MOCAF Opportunity — Sized**

*(replaces the draft's "MOCAG Blending Matrix – DRAFT" — note the draft misspells MOCAF as "MOCAG",
and its subtitle has a stray leading "A")*

## Subtitle / kicker
> A 10% wheat-flour blend is reachable on cassava's yield gap alone. 20% is not.

---

## Body — three beats

**1. What a blend costs in cassava**
- A **10% blend** needs **2.8–4.9 Mt** of fresh cassava (**18–31%** of today's crop).
- A **20% blend** needs **5.7–9.8 Mt** — **36–63% of the entire national crop**.
- The spread inside each blend rate is **processing yield**: 34.6% lab tape-yeast vs 20% community
  sun-dried. Better processing nearly **halves** the cassava needed per tonne of wheat displaced.

**2. What is actually reachable**
- Closing cassava's yield gap to India adds **+4.06 Mt with no new land** (nb 05 §5).
- That alone covers **143%** of a 10% blend at lab-grade conversion — reachable **without new land
  and without diverting one tonne of today's crop**.
- It covers only **41–72%** of a 20% blend. 20% is not reachable on the yield gap.

**3. What it saves**
- A 10% blend avoids **0.98 Mt** of wheat imports a year: **~USD 0.26bn** at the 2010–2026 average
  wheat price, **0.18bn** in a soft market, **0.35bn** in a tight one.
- A 20% blend avoids 1.96 Mt: **~USD 0.52bn** (range 0.35–0.70bn).

**Credibility line (use early, it pre-empts the obvious challenge)**
> Indonesia is the world's **#6 cassava producer by volume** — and **#2 by yield among the 40 countries
> that grow it at scale**.

This concedes up front that the yield lever is nearly exhausted, which is what makes land retention and
processing yield the credible asks instead of "grow cassava better". Say *"40 countries that grow it at
scale"*, not *"peers"*: the ≥50,000 ha filter is load-bearing — unfiltered, the global yield leader is
Guyana on 2,399 ha, which would inflate Indonesia's apparent gap from 20.6% to 32%.

## The line to land
> Indonesia does not need more cassava land to start. It needs **better processing** — and it needs to
> **stop losing the cassava land it already has**.

---

## Footnotes (must travel with the numbers)

1. **Baseline: food-wheat demand 9.8 MMT** (USDA GAIN ID2026-0010). *Not* total wheat imports —
   MOCAF does not address the ~2.1 MMT **feed**-wheat stream, so a total-imports baseline would
   overstate the offset.
2. **Price basis: World Bank Pink Sheet, US HRW, 2010–2026** — mean 265 USD/t, observed range
   180–359 USD/t (p10–p90), full range 142–522 USD/t. **FOB US Gulf: a global benchmark, NOT
   Indonesia's CIF landed cost**, and not Indonesia's actual suppliers (the Pink Sheet carries no
   Australian, Ukrainian or Canadian series). Cassava volumes are price-independent.
3. **Flour-equivalent figures are ceilings, not forecasts** — cassava already serves food, feed and
   starch demand, so a blend competes with existing uses.
4. Yield-gap headroom is measured against a **peer-scale frontier** (India, 35,574 kg/ha, among
   producers ≥50,000 ha). Indonesia is already the **#2 cassava yielder of 40 such producers** — this
   is not a "farm better" story.

---

## Speaker notes

- Lead with the **verdict**, not the matrix: 10% yes, 20% no. The chart is evidence for that sentence.
- If asked *"why not just grow more cassava?"* — cassava **area fell 53%** since 2010 (nb 05 §3). The
  crop is shrinking; the yield gap is the only land-neutral headroom, and it is finite at +4.06 Mt.
- If asked *"why is Indonesia's yield gap small?"* — because it has already intensified: yield **+39.6%**
  since 2010, now #2 by yield of the 40 countries that grow cassava at scale (>=50,000 ha).
  Credit, not criticism.
- If asked *"is this the whole import bill?"* — no, and say so plainly. This addresses the **food**
  stream only. The feed stream (~2.1 MMT, growing because domestic maize area fell 38%) needs a
  separate lever: maize land retention (nb 07 §4).
- If challenged on the dollar figures — they are on an **FOB benchmark**, deliberately labelled. A true
  CIF Indonesia number needs observed import unit values from the TRADE track. Adding assumed freight
  of +25–55 USD/t would put it at ~290–320 USD/t (**assumption, not sourced**).
- **Do not say** "official sources confirm paddy area is falling." GAIN forecasts a decline; FAO GIEWS
  reports 2025 paddy area planted *above* the five-year average. The near-term direction is contested
  (nb 07 §2).

---

## Retired numbers — do not reintroduce

| Retired | Use instead |
|---|---|
| $300/t "CIF assumption" | 265 USD/t, Pink Sheet US HRW FOB mean |
| ~$0.29bn/yr at 10% blend | ~USD 0.26bn/yr |
| $0.25–0.34bn ($250–350/t) band | 0.18–0.35bn (observed p10–p90) |
| 8.25M t no-action baseline | 9.8 MMT food-wheat (GAIN) |
| Substitution axis to 30% | Cap at 20% — beyond that exceeds a third of the crop |
| 40,000 kg/ha yield frontier | 35,574 kg/ha (India, peer-scale) |

`python tools/check_stale_numbers.py` enforces the first five in the notebooks.
