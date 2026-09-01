# Build direction — Indonesia wheat-vulnerability / cassava-substitution

Companion to `CLAUDE.md`. That file owns the **infrastructure** (loaders, data
provenance, conventions, FAOSTAT gotchas) — don't duplicate it here. This file owns
the **thesis, deliverable state, and build queue**. The findings section below is filled from
an actual notebook-05 run — if you re-run with a newer FAOSTAT release, re-fill it rather than
leaving stale numbers in the deck.

## Thesis
Indonesia is the world's #1 wheat importer and grows **zero** wheat (tropical climate).
Demand is inelastic and rising. The domestic lever is **cassava -> MOCAF** (fermented
cassava flour), constrained on the production and processing sides. The deck argues:
**Problem (import vulnerability) -> Mechanism (why substitution fails today) -> Solution
(data-driven recommendation).**

## Reference numbers (from USDA GAIN ID2026-0010 — use these, don't re-derive from FAOSTAT)
- Indonesia grows no wheat — fully import-dependent.
- Wheat imports: 10.45 MMT (2024/25) -> 12.3 MMT forecast (2025/26).
- Wheat food consumption ~9.8 MMT; total ~11.6 MMT (2025/26).
- Feed wheat ~doubled (~1.1 -> 2.1 MMT) as millers substitute wheat for costly corn.
- Team's FAOSTAT import trend: ~+0.48 Mt/yr, R^2~=0.82 (2010–2024).
- Supplier fragility: Ukraine share ~26.8% -> 1.8% in one year (2021->2022 war);
  Australia (top-3 supplier) drought/El-Nino exposed.
- MOCAF conversion yields: ~20% community sun-dried, ~34.6% lab tape-yeast.
- Live 2026 angle: BMKG 50–60% moderate El Nino mid-2026; Citi raising wheat targets.

## Filled findings from notebook 05 (RUN 2026-09-01, FAOSTAT 2010-2024 — no brackets left)
- **Cassava base is shrinking.** Production **-34.7%** (23.9 -> 15.6 Mt), driven by **area -53.2%**
  (1.18M -> 0.55M ha) against **yield +39.6%**; corr(area, production) = +0.97.
- **Yield gap is real but small.** Indonesia is the **#2 cassava yielder of 40 peer producers**
  (>=50k ha harvested): 28.2 t/ha vs the frontier **India 35.6 t/ha** = a **20.6% gap**, and
  *at parity with the peer top-5 mean (28.1 t/ha)*. Closing it on today's area adds
  **+4.06 Mt, no new land**.
- **Area is the 4.4x bigger lever.** The 630k ha lost since 2010, at today's yield, is **+17.8 Mt** —
  more than the entire current crop. Yield alone cannot carry the substitution story.
- **Offset ceiling.** All 15.6 Mt -> MOCAF = 3.12-5.41 Mt flour = **32-55% of food-wheat demand**
  (9.8 MMT). Ceiling, not forecast.
- **Achievable band.** **10% blend**: 2.83-4.90 Mt fresh cassava (**18-31%** of crop), 0.98 Mt wheat
  avoided, **~$0.25-0.34bn/yr** ($250-350/t). **20% blend**: 5.66-9.80 Mt (**36-63%** of crop) —
  out of reach without new land or large diversion.
- **The land-neutral headline (best deck line).** Closing the yield gap alone funds an
  **8.3-14.3% blend from new cassava only** — no new land, no diversion. Processing yield
  (20% sun-dried vs 34.6% lab tape-yeast) decides which end of the range.

Correction worth knowing: the pre-run draft used a **40,000 kg/ha placeholder frontier** (=> a 29% gap).
The real peer frontier is 35,574 kg/ha and the raw global ranking is topped by micro-producers
(Guyana, 2,399 ha). Notebook 05 now filters to producers >=50k ha so the frontier is one Indonesia
could copy. Net effect: the yield story got *smaller*, and the land-retention story got bigger.

## Deliverable state (`Indonesia.pptx`, 11 slides — spine locked)
Open items, ranked:
1. **Slide 8 (MOCAF blending/savings matrix)** — numbers now exist. Build the slide from
   `outputs/tables/slide8_mocaf_blend_matrix.csv` + `outputs/figures/idn_mocaf_blend_requirement.png`
   (blend x conversion yield -> fresh cassava, % of crop, wheat avoided, $ saved, % fundable by the
   yield gap). **Still a slide-build task, no longer a data task.**
2. **El Nino angle underused** — live 2026 event, makes vulnerability timely not historical.
3. **Supplier % reconciliation** — OEC $-share vs GAIN volume-share (Australia 37.8% /
   Ukraine 18.3% / Canada 16.1%, Jul'25-Jan'26) differ. Pick one basis, footnote it.
4. **Forecast caveat** — linear-only is fine for 15 points; keep the overfitting note visible.
5. **New: reframe the "grow more cassava" ask.** The data does not support a pure yield pitch —
   Indonesia is already #2 of 40 peers. Slide language should be land retention + processing yield.

## Build queue (for Claude Code)
Done (2026-09-01):
- ~~Notebook 05 frontier cell~~ — `src/load.py` now has **`load_qcl_world(item, elements)`**, reading
  grow-eda's `QCL_2010_2024.parquet` / `QCL_long.parquet`, dropping region aggregates (Area Code
  >= 5000) and FAOSTAT's China composite (code 351, was double-counting `China, mainland`).
  Real frontier wired in; peer-scale filter `PEER_MIN_AREA_HA = 50_000`.
- ~~Populate `04_synthesis`~~ — rewritten around the cassava recommendation, with a code cell that
  recomputes the headline numbers rather than restating them in prose.
- ~~Slide-8 savings model~~ — nb 05 §6: full matrix + $ saved + price sensitivity ($250/300/350/t),
  exported to `outputs/tables/slide8_mocaf_blend_matrix.csv`, plus the blend-requirement figure.
- Also fixed: two `''`-in-f-string bugs in nb 05 that were printing literal `{cur_area:,.0f}`.

Still open:
1. **Replace the $300/t CIF wheat-price assumption** with observed import unit values from the TRADE
   track. It is the softest number in the slide-8 matrix (the volume columns don't depend on it).
2. **Why did cassava area fall 53%?** Not answerable in QCL — needs SUSTAIN's land-cover data
   (oil palm? urbanisation?). This is *the* determinant of whether MOCAF can scale, and currently
   the deck's biggest unbacked link.
3. **Optional GROW extensions** — cassava production concentration (supply security of the substitute
   itself); QV value angle (cassava worth more as flour than tapioca? QV has cassava at $4.76bn);
   tie land-conversion (SUSTAIN) to the cassava area decline in nb 03/05.

## Intellectual-honesty guardrails (keep in the story, don't smooth over)
- Cassava **area is declining** — the solution's raw material is itself under pressure.
  Name it; it's what points policy at yield + land-retention.
- MOCAF flour-equivalent numbers are **ceilings** (cassava already has food/feed/starch
  uses) — present as a bounded band, never a point forecast.
- FAOSTAT is national-only — island/province claims come from external sources, not this data.
- **Don't pitch cassava yield as the fix.** Indonesia is already #2 of 40 peer producers and at the
  peer top-5 mean. The honest version is "the remaining gap is worth +4.06 Mt and funds an 8-14%
  blend on no new land" — real, bounded, and 4.4x smaller than the area already lost.
- Any yield "frontier" must be **peer-scale filtered**. The unfiltered global leader is Guyana on
  2,399 ha; using it inflates the gap and the whole opportunity.
