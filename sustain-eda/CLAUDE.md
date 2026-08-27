# CLAUDE.md — project notes for AI-assisted work

Context for anyone (or any AI assistant) picking up this repo.

## What this is

Datathon 2026 **Sustain track** EDA. Question: *what is the environmental footprint of how we
feed ourselves?* Deliverables: find the high-impact footprint, quantify it and locate levers,
set up a mitigation strategy that doesn't cut output.

## Conventions

- Analysis logic goes in `src/` (importable, testable); notebooks only orchestrate and narrate.
- Modules: `load` (I/O) → `clean` (filter/select) → `footprint` (analysis) → `viz` (plots).
- Data in `data/raw/` is never edited in place; derived tables go to `data/processed/`.
- Large CSVs are git-ignored — teammates download from FAOSTAT, they are not committed.

## Data gotchas (read before touching the data)

- **M49 aggregates**: `Area` mixes real countries with World/regions/income-groups. Always run
  `clean.split_countries_aggregates` and use the countries frame for rankings.
- **Two item-coding systems**: Emissions totals use `Item Code`; Emissions intensities use
  `Item Code (CPC)`. Never join on item code — align on `Area` + `Year`, match by name.
- **CO2eq comparability**: totals include multiple gases; use a CO2eq element
  (`clean.pick_co2eq_element`) before summing across sources.
- **Coverage**: recent years are partial; `clean.pick_analysis_year` picks the latest year at
  >=90% of peak country coverage.
- **Flags**: `Flag Description` marks estimated vs official values — worth reporting.

## Open items

- Confirm the auto-selected CO2eq element name against FAOSTAT docs.
- Consider per-capita / per-GDP normalization as an alternative lens.
- For the chosen lever commodity, size best-in-class vs worst-in-class intensity to quantify the
  achievable reduction.
