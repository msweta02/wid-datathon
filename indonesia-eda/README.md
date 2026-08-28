# Indonesia Deep-Dive — GROW Track

Country-level follow-up to `grow-eda`: what does Indonesia grow, and when/how
intensively — building toward a sharper, single-country hypothesis instead of
the global GROW overview.

## Data
No new downloads needed — reuses the FAOSTAT bulk CSVs already pulled for the
other tracks, filtered down to Indonesia:
- **QCL / QI / QV** (production, indices, value) ← `../grow-eda/data/raw/`
- **RL** (Land Use — arable land, for the cropping-intensity proxy) ← `../sustain-eda/data/raw/`

Run `grow-eda`'s own `01_data_loading` first (or otherwise make sure
`grow-eda/data/raw/*_All_Data.csv` exist) — `src/load.py` here reads straight
from those files and caches a small Indonesia-only parquet slice in this
track's own `data/processed/`, so it never re-melts the full ~4M-row global
CSV on repeat runs.

## Setup
Shares the repo-root `.venv` and `requirements.txt` (see `../requirements.txt`) —
no separate environment needed. Register a kernel if you haven't:
```bash
cd ..
python -m ipykernel install --user --name indonesia-eda --python /path/to/.venv/bin/python
```

## Notebooks
Run in order:
1. `01_data_loading` — load QCL/QI/QV filtered to Indonesia, inventory elements/items/years, flag quality.
2. `02_what_it_grows` — top crops by production/area harvested/value, crop-mix trend, rice area-vs-yield.
3. `03_when_it_grows` — **data gap stated up front**: FAOSTAT is annual, no planting/harvest months.
   Uses cropping intensity (area harvested ÷ arable land) as a real proxy for multi-season
   cultivation, and points at FAO's Crop Calendar tool as what a true "when" answer would need.
4. `04_synthesis` — pulls 01–03 into a findings summary + go/no-go recommendation.

## Layout
```
src/       load.py (reuse grow-eda/sustain-eda's bulk CSVs, filter to Indonesia)
           clean.py (flags, unit normalization, item-aggregate filtering)
           viz.py (plots)
data/raw/       only if you want a local CSV copy (gitignored either way)
data/processed/ cached Indonesia-only parquet slices (gitignored)
outputs/figures/ saved charts (gitignored)
CLAUDE.md  context for Claude Code — read this first
```

## Known gap
There is no month-level crop-calendar data in this repo. If the "when" angle
becomes the project focus, download FAO's Crop Calendar
(https://www.fao.org/agriculture/seed/cropcalendar/) and add a loader for it —
`03_when_it_grows` is the notebook to extend.
