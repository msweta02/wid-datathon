# WiD Datathon 2026 — "Farm to Fork"

FAOSTAT-based exploratory analysis for the Women in Data 2026 datathon, team **Data à la Carte**.

The brief spans four tracks — **GROW** (production), **TRADE** (flows), **EAT** (consumption) and
**SUSTAIN** (environmental footprint). This repository holds the two we built here:

| Track | Folder | Question | State |
|---|---|---|---|
| **GROW** — global scan | [`grow-eda/`](grow-eda/) | How is food production shifting across regions and over time? | Scan complete; used to pick a focus |
| **GROW** — country deep-dive | [`indonesia-eda/`](indonesia-eda/) | Indonesia imports more wheat than anyone and grows none. Can cassava close the gap? | **Primary deliverable** |
| **SUSTAIN** | [`sustain-eda/`](sustain-eda/) | What is the environmental footprint of how we feed ourselves? | Scoping EDA complete |

TRADE and EAT were built by other track members outside this repo.

---

## The thread through the repo

**`grow-eda` was a scan, not a conclusion.** It sweeps all of FAOSTAT's production data
(1961–2024, ~200 countries) to find something worth investigating, and ends with a ranked
shortlist of candidate hypotheses rather than an answer.

**`indonesia-eda` is what the scan pointed at, and where the real work is.** One country, one
question, seven notebooks:

> Indonesia is the world's largest wheat importer and produces **zero wheat** — not a small
> number, literally absent from FAOSTAT in every year 2010–2024. It is also the world's **#6
> cassava producer**, and it invented **MOCAF**, a fermented cassava flour that substitutes for
> wheat. So why hasn't substitution happened, and how far could it actually go?

The short answer the data supports: **a 10% wheat-flour blend is reachable without a hectare of
new land; 20% is not.** The binding constraints turn out to be *land retention* and *processing
yield* — not agronomy. Indonesia is already the **#2 cassava yielder among the 40 countries that
grow it at scale**, so "farm better" is not the ask.

**`sustain-eda` is a parallel track exploration**, sharing the same FAOSTAT plumbing and
conventions. Its land-use data (RL domain) is reused by `indonesia-eda` for the cropping-intensity
proxy — the one place the two tracks touch.

---

## Setup

One shared virtualenv at the repo root serves all three tracks. There are no per-track
requirements files.

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m ipykernel install --user --name wid-datathon
```

### Getting the data

**No data is committed** — the FAOSTAT bulk CSVs total ~300 MB and are git-ignored. Download them
from <https://www.fao.org/faostat/en/#data>, each domain's *Bulk Downloads → All Data (Normalized)*,
and extract so the `_All_Data.csv` lands in the right `data/raw/`:

| Domain | File | Goes in |
|---|---|---|
| QCL — Crops & livestock | `Production_Crops_Livestock_E_All_Data.csv` | `grow-eda/data/raw/` |
| QI — Production indices | `Production_Indices_E_All_Data.csv` | `grow-eda/data/raw/` |
| QV — Value of production | `Value_of_Production_E_All_Data.csv` | `grow-eda/data/raw/` |
| GT — Emissions totals | `Emissions_Totals_E_All_Data.csv` | `sustain-eda/data/raw/` |
| EI — Emissions intensities | `Environment_Emissions_intensities_E_All_Data.csv` | `sustain-eda/data/raw/` |
| RL — Land use | `Inputs_LandUse_E_All_Data.csv` | `sustain-eda/data/raw/` |
| LC — Land cover | `Environment_LandCover_E_All_Data.csv` | `sustain-eda/data/raw/` |
| ES — Cropland nutrient budget | `Environment_Cropland_nutrient_budget_E_All_Data.csv` | `sustain-eda/data/raw/` |

Use the **flagged** version, not `_NOFLAG` — the flags drive the data-quality checks.

`indonesia-eda` needs **no downloads of its own**: it reads the sibling tracks' CSVs and caches a
small Indonesia-only slice. The one exception is the World Bank Pink Sheet workbook for wheat
prices — see that track's README.

Each loader fails with a message telling you which file is missing and where to get it, rather
than silently substituting fabricated data.

---

## Running the notebooks

Every notebook is committed **with its outputs**, so you can read the whole analysis on GitHub
without running anything. To re-execute:

```bash
jupyter lab            # then run a track's notebooks in numeric order
```

> **Note:** the `jupyter nbconvert` CLI does not work in this environment. To run notebooks
> headlessly, drive `nbclient` from Python instead. Kernel startup is slow on a mounted drive, so
> expect a few minutes per notebook.

---

## Repo layout

```
grow-eda/         GROW global scan        — 8 notebooks, 24 figures
indonesia-eda/    GROW country deep-dive  — 7 notebooks, 24 figures, 3 tables, deck assets
sustain-eda/      SUSTAIN scoping EDA     — 7 notebooks
requirements.txt  shared dependencies
```

Each track follows the same shape, so moving between them is cheap:

```
<track>/
├── notebooks/        numbered, run in order, committed with outputs
├── src/              load.py · clean.py · viz.py  (+ track-specific analysis modules)
├── data/raw/         FAOSTAT bulk CSVs (git-ignored, you download these)
├── data/processed/   parquet caches (git-ignored, generated)
├── outputs/figures/  saved charts
├── CLAUDE.md         conventions, data gotchas, working notes
└── README.md         this orientation
```

**The convention everywhere:** reusable logic lives in `src/`; notebooks orchestrate and narrate
but stay thin. Wide FAOSTAT CSVs are melted to long format once and cached to parquet, so only the
first run is slow.

---

## Where to start reading

1. **[`indonesia-eda/FINDINGS.md`](indonesia-eda/FINDINGS.md)** — every finding, number, correction
   and known limit from the main analysis, in one place. If you read one file, read this.
2. **[`indonesia-eda/README.md`](indonesia-eda/README.md)** — how that track is built.
3. **[`grow-eda/README.md`](grow-eda/README.md)** — the scan that chose the focus.
4. **[`sustain-eda/README.md`](sustain-eda/README.md)** — the SUSTAIN track.

## Before quoting a number

Some figures were revised during the analysis, so **earlier deck drafts carry superseded values**.
`indonesia-eda/FINDINGS.md` §5 maps each old number to its replacement, and:

```bash
cd indonesia-eda && python tools/check_stale_numbers.py
```

fails if a retired number has survived anywhere in the notebooks.

Where the data cannot answer something, the notebooks say so rather than estimating — FAOSTAT is
national-only and annual, and this repo holds no trade-flow data. Limits are named in each track's
README and in `FINDINGS.md` §6.
