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
from src.load import load_indonesia, load_landuse_indonesia
qcl = load_indonesia("QCL")   # Area, Item, Element, Unit, year, value, flag — 2010-2024 by default
qi  = load_indonesia("QI")
qv  = load_indonesia("QV")
land = load_landuse_indonesia()   # None if sustain-eda's RL CSV isn't present; full history
# override the window: load_indonesia("QCL", year_min=2000, year_max=2024)
```
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
- Same **flag** and **item-aggregate** (`"Cereals, primary"`, `"Fruit Primary"`, etc.)
  gotchas as grow-eda apply here — `src/clean.py` carries over the relevant helpers.

## Workflow
`notebooks/` run in order 01→05:
- 01 load + inventory
- 02 what it grows (crop mix; rice area-vs-yield: prod −10.4% on −14.8% area, +5.3% yield)
- 03 when it grows (cropping-intensity proxy 114%→99%; 2015→2024 area decomposition —
  rice, maize, soy, cassava all lost area; + the month-data gap note below)
- 04 synthesis (findings; being rewritten from a generic go/no-go into the scoped
  cassava recommendation fed by 05)
- 05 cassava substitution (the thesis bridge): structural wheat-zero vs domestic
  staples; cassava production/area/yield trajectory; area-vs-yield decomposition;
  cassava yield gap vs global frontier; MOCAF flour-equivalent vs wheat demand;
  realistic 10–20% blend requirement. §7 feeds 04 and deck slide 8.

Note: cassava **area is declining** — the proposed solution's own raw material is
under pressure. Keep that tension visible; it's what points policy at yield +
land-retention rather than "just grow more."
