# sustain-eda

**Datathon 2026 · Sustain track — Emissions, land use & planet health**

> *What is the environmental footprint of how we feed ourselves?*

EDA of FAOSTAT emissions and land-use data to (1) pinpoint the high-impact footprint of food
production, (2) quantify its cost and locate the biggest levers, and (3) set up a strategy
that lowers impact without harming output.

## Structure

```
sustain-eda/
├── data/
│   ├── raw/            # FAOSTAT CSVs as downloaded (git-ignored)
│   └── processed/      # cleaned/derived tables
├── notebooks/
│   ├── 01_sources_and_countries.ipynb  # scoping: footprint, rankings, levers
│   ├── 02_gases.ipynb                  # CH4 vs N2O vs CO2 — which gas drives it
│   ├── 03_normalization.ipynb          # per-capita & per-calorie (needs extra data)
│   ├── 04_lever_gap.ipynb              # best- vs worst-in-class intensity (signature metric)
│   └── 05_candidate_comparison.ipynb   # compare angles, pick the project focus
├── src/
│   ├── load.py         # read FAOSTAT normalized CSVs (encoding-robust)
│   ├── clean.py        # M49 aggregate filtering, year & element selection
│   ├── footprint.py    # rankings, intensity, lever quadrant, per-hectare, routing
│   └── viz.py          # reusable plots
├── outputs/            # exported charts/tables
├── OtherDetails/       # track brief, notes, references
├── requirements.txt
├── .gitignore
├── CLAUDE.md           # working notes / conventions for AI-assisted dev
└── README.md
```

## Data

Place the full FAOSTAT normalized CSVs in `data/raw/`:

| File | Domain | Grain | Unit |
|---|---|---|---|
| `Emissions_totals.csv` | Emissions totals (GT) | Area × Element × Item × Source × Year | kt |
| `Emissions_intensities.csv` | Emissions intensities (EI) | Area × Element × Item (CPC) × Year | kg CO2eq/kg |
| `Land_Use.csv` | Land Use (RL) | Area × Element × Item × Year | 1000 ha |

**Optional** (for `03_normalization.ipynb` — notebooks degrade gracefully if absent):

| File | Domain | Element to use |
|---|---|---|
| `Population.csv` | Population → Annual population | Total Population - Both sexes |
| `Food_Balances.csv` | Food Balances (2010–) | Food supply (kcal/capita/day) |

Source: https://www.fao.org/faostat/en/#data — each domain's *Bulk Downloads → All Data
Normalized*; use `..._E_All_Data_(Normalized).csv` (all areas). Files are large (~20MB+) and
are git-ignored.

## Run

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
jupyter notebook notebooks/Sustain_EDA.ipynb
```

Run top to bottom. The notebook adds `..` to the path so `from src import ...` works.

## What it produces

- **Explore:** M49-filtered rankings of emission sources and countries → the high-impact footprint.
- **Quantify:** source trends, emissions intensity by commodity, a volume-vs-intensity lever
  quadrant, and emissions per hectare.
- **Strategize (setup):** headline "what's causing more issue" (by volume and by intensity) and
  the next FAOSTAT dataset to pull to prove the mechanism.

## Key findings

_Fill in after running:_

- Largest source by volume: …
- Most emissions-intensive food per kg: …
- Biggest lever (high volume + high intensity): …
- Analysis year: …

## Caveats

- **M49 aggregates** are filtered before any ranking (`clean.split_countries_aggregates`).
- **Do not merge totals with intensities on item code** — different coding systems
  (`Item Code` vs `Item Code (CPC)`); align on Area + Year.
- Confirm the auto-selected CO2eq element and agricultural-land item (both print when run).
