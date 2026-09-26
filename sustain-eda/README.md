# SUSTAIN Track — Emissions, Land Use & Planet Health

Exploratory analysis for the WiD 2026 "Farm to Fork" datathon, **SUSTAIN track**.

> *What is the environmental footprint of how we feed ourselves?*

Three deliverables, in order: **(1) Explore** — locate the high-impact footprint. **(2) Quantify** —
size its cost and find the biggest levers. **(3) Strategize** — set up a mitigation angle that
lowers impact without cutting output.

---

## Key findings

From the executed run — **analysis year 2023**, element **`Emissions (CO2eq) (AR5)`** (both
auto-selected and printed by the notebook, so they're verifiable rather than assumed):

| | |
|---|---|
| **Largest agrifood source by volume** | **Pre- and post-production** — 16.7% of the ranked agrifood total. Food processing, transport, retail and waste, *not* the farm itself |
| **Most emissions-intensive food per kg** | **Meat of cattle with the bone, fresh or chilled** |
| **Biggest lever** (high volume × high intensity) | Cattle meat — where intensity and volume coincide |
| **Next dataset to pull** | Emissions from pre- and post-agricultural production (Agrifood systems) — to prove the supply-chain mechanism |

**The finding worth arguing about:** the single largest agrifood emissions bucket sits *outside the
farm gate*. That points a mitigation strategy at processing, transport, retail and waste rather
than at production practice — which is also the part of the system a production-side dataset can't
fully see. Hence the "next dataset" call.

> **Read the source rankings as a landscape, not a partition.** FAOSTAT mixes hierarchy levels in
> `Item` — *Emissions from livestock* partly contains *Enteric Fermentation*; *Land-use change*
> overlaps *Net Forest conversion*. Don't sum overlapping items as though they were mutually
> exclusive. Rankings here are also scoped to **agrifood** sources: economy-wide Energy, IPPU
> (industry) and Waste are excluded, since the track asks about the *food* footprint.

---

## Data

Download each domain's *Bulk Downloads → All Data (Normalized)* from
<https://www.fao.org/faostat/en/#data> and place the CSV in `data/raw/`. Files are large (~20 MB+
each) and git-ignored.

| File | Domain | Used for |
|---|---|---|
| `Emissions_Totals_E_All_Data.csv` | GT — Emissions totals | Source and country rankings; gas breakdown |
| `Environment_Emissions_intensities_E_All_Data.csv` | EI — Emissions intensities | kg CO2eq per kg of commodity; the efficiency lever |
| `Inputs_LandUse_E_All_Data.csv` | RL — Land use | Emissions per hectare; agricultural land base |
| `Environment_LandCover_E_All_Data.csv` | LC — Land cover | Forest trend and change by country (nb 06) |
| `Environment_Cropland_nutrient_budget_E_All_Data.csv` | ES — Cropland nutrient budget | Nutrient surplus (nb 06) |

**Optional** — `03_normalization` degrades gracefully if these are absent:

| File | Element to use |
|---|---|
| Population | `Total Population - Both sexes` |
| Food Balances (2010–) | `Food supply (kcal/capita/day)` |

`src/load.try_read` returns `None` with a clear message for anything missing, so a partial download
still runs.

> `Inputs_LandUse_E_All_Data.csv` is also read by **[`../indonesia-eda/`](../indonesia-eda/)** for
> its cropping-intensity proxy — the one place the two tracks share data. Don't move or rename it
> without checking there.

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

Committed **with outputs** — readable without running. `00` is the full narrative; `01`–`06` are
the focused chapters.

| # | Notebook | What it does |
|---|---|---|
| 00 | `00_Sustain_EDA` | **The whole story end to end** — explore → quantify → strategize. Start here |
| 01 | `01_sources_and_countries` | Scoping: footprint, source and country rankings, levers |
| 02 | `02_gases` | CH4 vs N2O vs CO2 — which gas actually drives the total |
| 03 | `03_normalization` | Per-capita and per-calorie lenses *(needs the optional datasets)* |
| 04 | `04_lever_gap` | Best- vs worst-in-class intensity — the signature metric |
| 05 | `05_candidate_comparison` | Compare candidate angles, pick the project focus |
| 06 | `06_land_and_planet` | Land composition, forest trend and change, nutrient surplus |

Each notebook adds `..` to `sys.path`, so `from src import ...` works when run from `notebooks/`.

> Charts render **inline in the notebooks**; `outputs/` is currently empty. Call `viz.save(fig,
> name)` if you need a chart as a file for a deck.

---

## Code

```
src/
├── load.py        read_faostat · try_read · load_all        (encoding-robust FAOSTAT readers)
├── clean.py       split_countries_aggregates · pick_analysis_year · pick_co2eq_element
│                  scope_agrifood · drop_aggregate_items · basic_report
├── footprint.py   rank_sources · rank_countries · source_trends · commodity_intensity
│                  lever_table · pick_lever_commodity · emissions_per_land · next_dataset
│                  gas_breakdown · per_capita · intensity_gap · land_composition
│                  forest_trend · forest_change_by_country · nutrient_surplus
└── viz.py         barh_ranking · line_trends · lever_quadrant
```

The pipeline runs in one direction: **`load` → `clean` → `footprint` → `viz`.** Analysis logic
lives in `src/` where it's importable and testable; notebooks orchestrate and narrate.

---

## Layout

```
notebooks/        00–06, committed with outputs
src/              load → clean → footprint → viz
data/raw/         FAOSTAT bulk CSVs (git-ignored, you download these)
data/processed/   derived tables
outputs/          exported charts and tables (currently empty — figures render inline)
CLAUDE.md         conventions and gotchas — read before touching the data
```

---

## Open items

- Confirm the auto-selected CO2eq element name against FAOSTAT documentation.
- Per-capita and per-GDP normalisation as an alternative lens (started in `03`, needs the optional
  Population and Food Balances downloads).
- For the chosen lever commodity, size best-in-class against worst-in-class intensity to quantify
  the achievable reduction — that's the number a strategy recommendation would rest on.
