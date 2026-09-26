# GROW Track — FAOSTAT Global Scan

Exploratory analysis for the WiD 2026 "Farm to Fork" datathon, **GROW track** (crop and livestock
production). Guiding question from the brief: *how is food production shifting across regions and
over time?*

**This track is a scan, not a conclusion.** Its job was to sweep all of FAOSTAT's production data —
1961–2024, ~200 countries, ~4.1M rows — and answer two things:

1. **Feasibility** — is GROW data good enough to build a project on? *(Yes. The bottleneck is
   framing a sharp question, not wrangling the data.)*
2. **Hypothesis** — what specific shift is worth building around?

The answer to (2) became a separate track: **[`../indonesia-eda/`](../indonesia-eda/)**, the
country deep-dive that is the team's primary deliverable. Start here to see *how* the focus was
chosen; go there for the actual analysis.

---

## What the scan established

- **Coverage is strong.** 1961–2024, 244 areas (34 of them aggregates), QCL ~4.1M long rows.
- **The data is clean enough to trust.** Staple flags run ~81% official (A), 13% estimated (E),
  ~3% imputed or from international organisations.
- **Yield is in `kg/ha` in this release** — *not* `hg/ha` as older FAOSTAT documentation says.
  Verify per element rather than assuming; this is the single easiest way to be wrong by 10×.
- **Element codes have shifted between releases.** QV constant-international-$ = 152; QI gross
  PIN = 432, per-capita PIN = 434. Verify against notebook 01's parameter tables, not from memory.
- **Wheat decline signals** (negative 20-year CAGR): Serbia and Montenegro, Kuwait, Colombia,
  Madagascar.
- **Notebook 08** builds the production-side mirror of the TRADE track's import charts — same
  countries, production quantity vs production value instead of import quantity vs value.

> **Status note:** `06_synthesis` is still a **structured template** — the feasibility scorecard has
> `TODO` fields and the go/no-go verdict is unfilled. The hypotheses section is written out, and the
> decision it was meant to record was effectively made by starting `indonesia-eda`. Treat it as
> scaffolding rather than a finished chapter.

---

## Data

FAOSTAT **bulk downloads** — no account or API key needed. Three domains:

| Code | Domain | What it holds |
|---|---|---|
| **QCL** | Crops and livestock products | Production (t), yield (kg/ha), area harvested (ha) |
| **QI** | Production indices | Trends normalised to 2014–16 = 100, incl. per-capita |
| **QV** | Value of agricultural production | Economic value, current and constant |

Download each domain's *Bulk Downloads → All Data (Normalized)* from
<https://www.fao.org/faostat/en/#data> and extract so the `_All_Data.csv` lands in `data/raw/`
(the loader also checks `~/Downloads/<name>_All_Data/`).

**Use the flagged version, not `_NOFLAG`** — the flags feed the data-quality analysis.

Files are ~200 MB total and git-ignored. The loader melts the wide CSVs to long format once and
caches to parquet in `data/processed/`, so only the first run is slow.

---

## Setup

Uses the **shared root virtualenv** — there's no per-track requirements file.

```bash
cd ..
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m ipykernel install --user --name wid-datathon
```

---

## Notebooks

Committed **with outputs** — readable without running. Execute in order:

| # | Notebook | What it does |
|---|---|---|
| 01 | `01_data_loading` | Load bulk CSVs, melt to long, inventory items/elements/areas, quality report |
| 02 | `02_top_producers` | Top-10 foods and countries, who leads each food, concentration |
| 03 | `03_qcl_production` | Production / yield / area, decline detection, yield gap, regional shift |
| 04 | `04_qi_indices` | Normalised and per-capita trends |
| 05 | `05_qv_value` | Economic value; where value and volume decouple |
| 06 | `06_synthesis` | Go/no-go scorecard + ranked candidate hypotheses *(template, partly unfilled)* |
| 07 | `07_trade_adjacent` | Production concentration, supply-shock simulation, self-sufficiency — trade-flavoured questions answered with **GROW data only**, no trade flows loaded |
| 08 | `08_production_mirror` | Production-side mirror of the TRADE deck's import charts (top producers; quantity vs value panels) |

---

## Code

```
src/
├── load.py            load_dataset · load_dataset_range · load_codes · save/load_processed
├── clean.py           standardize_columns · split_aggregates · resolve_china · annotate_flags
│                      yield_to_tonnes_per_ha · flag_item_aggregates · data_quality_report
├── concentration.py   production_shares · hhi · top_n_share · concentration_table
│                      supply_shock · per_capita_trend · self_sufficiency_change · combined_risk_table
└── viz.py             save · trend_over_time · trend_top_bottom · missingness_heatmap · flag_composition
```

```python
from src.load import load_dataset, load_codes

qcl   = load_dataset("QCL")                 # melts + caches on first call, instant after
items = load_codes("QCL", "ItemCodes")      # optional lookup tables
```

The whole dataset loads at once — **filter with pandas**, not with API parameters. `refresh=True`
forces a re-melt; `search_dirs=[...]` points elsewhere.

`load_dataset_range(code, 2010, 2024)` writes a separate, additive year-sliced cache — that's what
`indonesia-eda` reads, and it doesn't disturb this track's full-history cache or notebooks.

---

## Layout

```
notebooks/        01–08, run in order, committed with outputs
src/              reusable logic — notebooks stay thin
data/raw/         FAOSTAT bulk CSVs (git-ignored, you download these)
data/processed/   parquet caches (git-ignored, generated)
outputs/figures/  24 saved charts
CLAUDE.md         conventions and gotchas — read before touching the data
```
