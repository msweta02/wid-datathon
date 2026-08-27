# GROW Track — FAOSTAT EDA

Exploratory data analysis for the "Farm to Fork" datathon, **GROW track**
(crop & livestock production trends). Two goals: decide whether GROW is worth
committing to, and surface a sharp hypothesis to build the project on.

## Data
FAOSTAT (UN FAO) **bulk downloads** — no account or API key needed:
- **QCL** — Crops and livestock products (production, yield, area harvested)
- **QI** — Production Indices (trends normalized to 2014–16 = 100, incl. per-capita)
- **QV** — Value of Agricultural Production (economic value)

Download the three "All Data (Normalized)" bulk zips from the FAOSTAT site, and
**extract each so the `_All_Data.csv` lands in `data/raw/`** (the loader also checks
`~/Downloads/<name>_All_Data/` if you'd rather not move them). Use the flagged
version, not `_NOFLAG` — the flags feed the data-quality analysis.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m ipykernel install --user --name grow-eda
```

The loader reads the wide bulk CSVs, melts them to long format, and caches to
parquet in `data/processed/` — so the first run is a few seconds and the rest are instant.

## Notebooks
Files in `notebooks/` are stored as jupytext "percent" scripts (`# %%` cells) so
they diff cleanly in git and work with Claude Code. Open them directly in VS Code
(the Jupyter extension renders `# %%` cells as a notebook), or convert:

```bash
pip install jupytext
jupytext --to notebook notebooks/*.py     # makes .ipynb alongside
```

Run in order:
1. `01_data_loading` — load bulk CSVs, melt to long, inventory items/elements/areas.
2. `02_top_producers` — top-10 foods & countries, who leads each food, concentration.
3. `03_qcl_production` — production / yield / area, decline detection, yield gap, regional shift.
4. `04_qi_indices` — normalized & per-capita trends.
5. `05_qv_value` — economic value, value/volume decoupling.
6. `06_synthesis` — go/no-go verdict + ranked hypotheses.
7. `07_trade_adjacent` — production concentration, supply-shock & self-sufficiency (trade-flavored, GROW-only).

Both `.py` (jupytext percent source) and matching `.ipynb` files are included — open
either. The `.ipynb` are un-run; execute them to regenerate outputs and figures.

## Layout
```
src/       load.py (pull+cache)  clean.py (fix FAOSTAT quirks)  viz.py (plots)
data/raw   parquet cache of API pulls (gitignored)
data/processed  cleaned frames
outputs/figures  saved charts
CLAUDE.md  context for Claude Code — read this first
```

## Notes
See `CLAUDE.md` for FAOSTAT gotchas (flags, China entities, yield units, aggregates).
Element/item codes in the notebooks are the common ones but **verify against the
param tables in notebook 01** — FAOSTAT has shifted some element codes between releases.
