# GROW Track — FAOSTAT EDA

## Project goal
Datathon "Farm to Fork" project, **GROW track**: crop & livestock production trends.
This repo is the **exploratory phase**. Two concrete objectives:
1. **Feasibility** — decide whether GROW is a good track to commit to (data quality,
   coverage, gaps, how hard it is to work with).
2. **Hypothesis** — surface 1–3 specific, well-defined questions worth building a
   project around (e.g. a crop/region/shift worth forecasting or flagging).

Guiding question from the brief: *"How is food production shifting across regions and over time?"*

## Data source
All data comes from **FAOSTAT** (UN FAO) **bulk downloads** (no account/API needed).
Extract each bulk zip so the `_All_Data.csv` sits in `data/raw/` (loader also checks
`~/Downloads/<name>_All_Data/`). Bulk files are WIDE (Y1961, Y1961F, ...) and latin-1
encoded; `src/load.py` melts them to LONG and caches to parquet.

Bulk file basenames: QCL=`Production_Crops_Livestock_E`, QI=`Production_Indices_E`,
QV=`Value_of_Production_E`. Use the flagged `_All_Data` (not `_NOFLAG`) so the
data-quality analysis has flags.

Three core datasets for GROW:

| Code | Name | What it holds | Key elements |
|------|------|---------------|--------------|
| **QCL** | Crops and livestock products | Physical production | Area harvested (ha), Yield (kg/ha or hg/ha), Production (tonnes), stocks/heads for livestock |
| **QI**  | Production Indices | Normalized production trends vs base period (2014–2016 = 100) | Gross/Net PIN, per-capita indices |
| **QV**  | Value of Agricultural Production | Economic value | Gross Production Value (current & constant USD, SLC, international $) |

Coverage: ~245 countries/territories + regional/income aggregates, **1961 → latest**.

### Metadata references
- QCL: https://www.fao.org/faostat/en/#data/QCL/metadata
- QI:  https://www.fao.org/faostat/en/#data/QI/metadata
- QV:  https://www.fao.org/faostat/en/#data/QV/metadata

## Loader (bulk CSV) — quick reference
```python
from src.load import load_dataset, load_codes
qcl = load_dataset("QCL")            # reads bulk CSV, melts to long, caches parquet
qi  = load_dataset("QI")
qv  = load_dataset("QV")
items = load_codes("QCL", "ItemCodes")   # optional lookup tables
```
- First call melts (slow, ~seconds); subsequent calls hit the parquet cache.
- Whole dataset loads at once — **filter with pandas** (`df[df.item.isin(...)]`),
  not with API params.
- `refresh=True` forces a re-melt from CSV. `search_dirs=[...]` points elsewhere.

## Conventions
- Raw pulls cached to `data/raw/*.parquet` (never re-hit API unnecessarily).
- Cleaned data → `data/processed/`.
- Reusable code in `src/` (`load.py`, `clean.py`, `viz.py`); notebooks stay thin.
- Figures → `outputs/figures/`.
- Use parquet, not CSV, for cached frames (dtypes + speed).

## FAOSTAT gotchas (important)
- **Flags**: every value has a flag (E=estimated, I=imputed, A=official, M=missing, etc.).
  Don't treat imputed/estimated as ground truth without noting it.
- **China**: appears as multiple entities — China mainland (41), Taiwan (214),
  China+Taiwan (357), China+HK+Macao+Taiwan. **Don't double-count.** Pick one convention.
- **Aggregates vs countries**: area codes >5000 are regional/income aggregates
  ("World", "Africa", "Least Developed Countries"). Separate them from country-level analysis.
- **Yield units**: FAOSTAT often reports yield in **hg/ha** (hectograms/ha). Divide by
  10000 for tonnes/ha, or /10 for kg/ha. Always check the unit column.
- **Item vs Item aggregates**: "Cereals, Total" is an aggregate of individual cereal items.
- **Missing years**: coverage is uneven pre-1990 for many developing countries.

## Workflow / phases
See `notebooks/` — run in order 01→07:
- 01 load + inventory, 02 top producers (what/where overview),
  03 QCL deep-dive (production/yield/area/decline/yield-gap/regional-shift),
  04 QI indices, 05 QV value, 06 synthesis (go/no-go + hypotheses),
  07 trade-adjacent (production concentration, supply-shock sim, self-sufficiency —
  trade-flavored questions answered with GROW data only; no trade flows loaded).
`06_synthesis` produces the go/no-go call and seven ranked candidate hypotheses.

`src/concentration.py` holds the trade-adjacent metrics: `production_shares`, `hhi`,
`top_n_share`, `concentration_table`, `supply_shock`, `per_capita_trend`,
`self_sufficiency_change`, `combined_risk_table`.

## Findings so far (from executed run)
- Coverage 1961–2024, 244 areas (34 aggregates), QCL ~4.1M long rows.
- Staples flags: ~81% official (A), 13% estimated (E), ~3% imputed/external — clean.
- Yield unit in this release is **kg/ha** (not hg/ha as older docs say) — verify per element.
- QV constant-int'l-$ element code = 152; QI gross PIN = 432, per-capita PIN = 434.
- Wheat decline signals: Serbia and Montenegro, Kuwait, Colombia, Madagascar (neg. 20y CAGR).
