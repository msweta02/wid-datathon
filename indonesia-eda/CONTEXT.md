# Build direction — Indonesia wheat-vulnerability / cassava-substitution

Companion to `CLAUDE.md`. That file owns the **infrastructure** (loaders, data
provenance, conventions, FAOSTAT gotchas) — don't duplicate it here. This file owns
the **thesis, deliverable state, and build queue**. Numbers in `[brackets]` get filled
from notebook 05's outputs after a run.

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

## Filled findings from notebook 05 (update after running — replace brackets)
- Cassava base: production changed **[+/- X%]** 2010->latest, driven by **[area/yield]**
  -> MOCAF raw-material base is **[shrinking/holding/growing]**.
- Yield gap: Indonesia **[X%]** below cassava frontier (**[country]**); closing on today's
  area adds **[X Mt]**, no new land.
- Offset ceiling: cassava->MOCAF could cover **[X–Y%]** of food-wheat demand; a 10–20% blend
  needs **[X Mt]** fresh cassava (**[X%]** of current crop).

## Deliverable state (`Indonesia.pptx`, 11 slides — strong, spine locked)
Open items, ranked:
1. **Slide 8 (MOCAF blending/savings matrix) is a DRAFT** — the payoff. Notebook 05 section 6
   produces the numbers. **Main open item.**
2. **El Nino angle underused** — live 2026 event, makes vulnerability timely not historical.
3. **Supplier % reconciliation** — OEC $-share vs GAIN volume-share (Australia 37.8% /
   Ukraine 18.3% / Canada 16.1%, Jul'25–Jan'26) differ. Pick one basis, footnote it.
4. **Forecast caveat** — linear-only is fine for 15 points; keep the overfitting note visible.

## Build queue (for Claude Code)
1. **Finish notebook 05's frontier cell (section 5)** — it auto-probes for a full multi-country
   QCL loader and falls back to a manual value. Wire it to grow-eda's `QCL_long.parquet` cache so
   the yield gap is real. (See CLAUDE.md for loader details.)
2. **Populate `04_synthesis`** from 05's outputs — replace the "..." placeholders and the generic
   go/no-go with the scoped cassava recommendation (05 section 7).
3. **Build the slide-8 savings model** — from 05 section 6's blend -> fresh-cassava requirement, add
   wheat-tonnes-avoided and $-saved at import prices; output a matrix
   (blend rate x MOCAF yield -> wheat offset, cassava needed, % of current crop).
4. **Optional GROW extensions** — cassava production concentration (supply security of the
   substitute itself); QV value angle (cassava worth more as flour than tapioca?); tie
   land-conversion (SUSTAIN) to the cassava area decline in nb 03/05.

## Intellectual-honesty guardrails (keep in the story, don't smooth over)
- Cassava **area is declining** — the solution's raw material is itself under pressure.
  Name it; it's what points policy at yield + land-retention.
- MOCAF flour-equivalent numbers are **ceilings** (cassava already has food/feed/starch
  uses) — present as a bounded band, never a point forecast.
- FAOSTAT is national-only — island/province claims come from external sources, not this data.
