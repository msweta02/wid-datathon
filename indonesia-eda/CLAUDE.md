# Indonesia Deep-Dive — GROW Track

## Project goal
Sibling to `grow-eda`, scoped to one country. The single-country scan has already
served its purpose: **Indonesia is locked as the focus**, and the project now has a
thesis — *Indonesia is the world's #1 wheat importer and grows zero wheat; the
domestic lever against that import vulnerability is cassava → MOCAF (fermented
cassava flour).* The GROW track's job is to make the production data (QCL/QI/QV)
**support and bound that thesis**: establish the structural wheat-zero, size the
cassava base, and quantify how much wheat cassava could realistically offset.

Sister tracks (EAT / TRADE / SUSTAIN) carry the demand, trade-flow, and
sustainability sides; this repo is the production-side lens, built to sit against
a TRADE import view.

## Data source — reused, not re-downloaded
This track has no bulk downloads of its own. `src/load.py` reads directly from:
- `../grow-eda/data/raw/Production_Crops_Livestock_E_All_Data.csv` (QCL)
- `../grow-eda/data/raw/Production_Indices_E_All_Data.csv` (QI)
- `../grow-eda/data/raw/Value_of_Production_E_All_Data.csv` (QV)
- `../sustain-eda/data/raw/Inputs_LandUse_E_All_Data.csv` (RL — Land Use)

melts wide→long, filters to `Area == "Indonesia"` and year in `[YEAR_MIN,
YEAR_MAX]` (default **2010-2024** — see `src/load.py`), and caches the small
result to `data/processed/*.parquet` in **this** track. If any of those sibling
CSVs are missing, `load_indonesia`/`load_landuse_indonesia` raise/print a clear
message pointing at where to get them — don't silently fall back to fabricated
data.

`load_indonesia` prefers grow-eda's own `data/processed/{code}_2010_2024.parquet`
(from grow-eda's `load_dataset_range`, additive — doesn't touch grow-eda's
full-history cache or its 01-08 notebooks) when present, and falls back to
reading+melting the raw CSV directly otherwise, so this track still works
standalone.

## Loader — quick reference
```python
from src.load import load_indonesia, load_landuse_indonesia, load_qcl_world
qcl = load_indonesia("QCL")   # Area, Item, Element, Unit, year, value, flag — 2010-2024 by default
qi  = load_indonesia("QI")
qv  = load_indonesia("QV")
land = load_landuse_indonesia()   # None if sustain-eda's RL CSV isn't present; full history
# override the window: load_indonesia("QCL", year_min=2000, year_max=2024)

# Cross-country slice — for benchmarking Indonesia against other producers (nb 05 §5).
cas   = load_qcl_world("Cassava, fresh", ["Yield", "Production", "Area harvested"])  # nb 05 §5
wheat = load_qcl_world("Wheat", ["Yield", "Production", "Area harvested"])           # nb 06
```
`load_qcl_world` reads grow-eda's already-melted global QCL cache
(`QCL_{ymin}_{ymax}.parquet`, else `QCL_long.parquet`, else melts the raw CSV), drops
**region aggregates** (`Area Code >= 5000`) and **FAOSTAT's China composite** (code 351,
which double-counts `China, mainland`), and caches the per-item slice locally. Everything
else in `src/load.py` is Indonesia-only.

**Peer-scale filter — required, not optional.** Any cross-country yield "frontier" must be
restricted to producers at a comparable scale (nb 05 uses `>= 50_000 ha` harvested). The
unfiltered global cassava-yield leader is Guyana on **2,399 ha** — a garden plot, not an
agronomic target, and using it inflates Indonesia's apparent gap from 20.6% to 32%.

Column names match grow-eda's raw convention (`Area`, `Item`, `Element`, lowercase
`year`/`value`/`flag`) — copy-paste between the two tracks works without renames.

## Conventions
Same as `grow-eda`: reusable code in `src/`, notebooks stay thin, figures →
`outputs/figures/`, cached frames → `data/processed/*.parquet` (never re-melt
the full global CSV if the country-filtered cache already exists).

## Known gap — "when it grows"
FAOSTAT (QCL/QI/QV/RL) is **annual only** — there is no planting/harvest month
data in anything downloaded so far. `03_when_it_grows` is honest about this:
it uses **cropping intensity** (area harvested ÷ arable land, from RL) as a
real proxy for multi-season cultivation — a ratio well above 100% is consistent
with Indonesia's documented 2–3 rice seasons/year in parts of Java — but it is
a proxy, not an actual calendar.

If the "when" angle becomes the project focus, the real fix is downloading
FAO's **Crop Calendar** tool data (https://www.fao.org/agriculture/seed/cropcalendar/),
which gives planting/harvest month ranges per crop per country. Add a loader
for it in `src/load.py` (follow the `try_read`-with-graceful-fallback pattern
used in `sustain-eda/src/load.py` for optional datasets) and extend
`03_when_it_grows` — don't invent monthly figures from the annual data.

## Indonesia-specific gotchas
- **Island-level variation**: FAOSTAT is national-only. Indonesia's agriculture
  differs hugely by island (Java = rice-dominant, multi-season; Sumatra/Kalimantan
  = oil palm plantations, different cycle entirely). A national aggregate can mask
  this — call it out rather than treat Indonesia as agriculturally uniform.
- **Oil palm dominates by tonnage** (fresh fruit bunches are heavy) — don't let
  raw production-tonnage rankings overstate its economic/caloric importance
  relative to rice; cross-check against QV (value) and calorie-relevant volume.
  But **do** use its *area* series: oil palm went 5.78M → 14.32M ha (2010→2024) and that
  reallocation is the mechanism behind the staple-area decline (nb 07 §2).
- **Area coincidence ≠ land conversion.** QCL can show total area grew while staples shrank;
  it cannot show a given cassava field became oil palm. State the former, don't claim the latter —
  parcel-level proof needs land-cover data (SUSTAIN).
- Same **flag** and **item-aggregate** (`"Cereals, primary"`, `"Fruit Primary"`, etc.)
  gotchas as grow-eda apply here — `src/clean.py` carries over the relevant helpers.
- **No trade data in this repo.** QCL/QI/QV/RL are production-side only; FAOSTAT's trade
  domain (TM / detailed trade matrix) is not downloaded. So import volumes and supplier
  shares are **carried in as sourced constants** (deck slides 3–4, USDA GAIN) — see nb 06 §1.
  Never present a supplier share as if this repo derived it. Adding a TM loader is the single
  highest-value data addition left for this track.

## Workflow
`notebooks/` run in order 01→07:
- 01 load + inventory
- 02 what it grows (crop mix; rice area-vs-yield: prod −10.4% on −14.8% area, +5.3% yield)
- 03 when it grows (cropping-intensity proxy 114% in 2015 → 96% in 2024; 2015→2024 area decomposition —
  rice, maize, soy, cassava all lost area; + the month-data gap note below)
- 04 synthesis (**written**, not placeholder): 01–03 + 05 into one findings page, ending in a
  scoped go-with-narrowed-scope recommendation. Recomputes its headline numbers in-notebook
  rather than restating them in prose.
- 05 cassava substitution (the thesis bridge): structural wheat-zero vs domestic
  staples; cassava production/area/yield trajectory; area-vs-yield decomposition;
  cassava yield gap vs the **peer-scale** frontier; MOCAF flour-equivalent vs wheat demand;
  the blend × conversion-yield decision matrix for slide 8. §7 feeds 04 and the deck.

- 06 supplier side (the *other* half of the deck's argument): who actually grows Indonesia's
  wheat and how reliably. Supplier production levels/volatility, Australia's yield-vs-area
  swing, the shock-correlation test → quantified diversification benefit, and the
  tradeable-pool framing. Feeds deck slides 3–5.

- 07 land + alternatives (closes the two biggest analytical gaps): **where the staple land went**
  (total cropped area *grew* 3.75M ha while 6 staples lost 5.04M ha and oil palm gained 8.54M ha —
  so it's reallocation, not shortage); **is cassava the right lever** (tested against sweet potato,
  potato, maize, rice — cassava wins by elimination; sago is absent from FAOSTAT); and the
  **maize→feed-wheat channel** (a second, independent route into wheat imports that MOCAF cannot
  touch). Ends in the ranked, sized action set for GROW rubric point 3.

Outputs beyond figures: `outputs/tables/slide8_mocaf_blend_matrix.csv` (blend rate ×
MOCAF conversion → fresh cassava needed, % of current crop, wheat avoided, $ saved,
% fundable by closing the yield gap) and
`outputs/tables/supplier_diversification_scenarios.csv` (sourcing mix → supply-pool
volatility and worst single year), and `outputs/tables/grow_action_levers.csv`
(lever → actor → sized effect).

Note: cassava **area is declining** (−53.2% since 2010) — the proposed solution's own raw
material is under pressure, and the area already lost is a **4.4× larger lever than the
entire remaining yield gap**. Keep that tension visible; it points policy at land retention
and processing yield rather than "just grow more" or "farm better." See CONTEXT.md for the
filled numbers.
