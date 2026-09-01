"""
Data loading helpers for Indonesia-focused GROW analysis.

Reuses the FAOSTAT bulk CSVs already downloaded for the other tracks instead of
re-downloading ~200MB of global data:
  - QCL / QI / QV  <- ../grow-eda/data/raw/   (production, indices, value)
  - RL (Land Use)  <- ../sustain-eda/data/raw/ (arable land, for the cropping-
                       intensity proxy used in notebook 03 "when it grows")

Bulk files are WIDE (Y1961, Y1961F, ...); this module melts them to LONG and
caches an Indonesia-only slice to parquet (small + fast — no need to cache the
full global melt here, grow-eda/sustain-eda already do that for their own use).

Default year range is 2010-2024 (recent years, max in the tables) — set by
YEAR_MIN/YEAR_MAX below. This reuses grow-eda's `load_dataset_range` (its own
separate 2010-2024 parquet cache; doesn't touch grow-eda's full-history cache
or its existing notebooks).

Import from notebooks:  from src.load import load_indonesia, load_landuse_indonesia
"""
from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

from .clean import drop_china_composite

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"
RAW.mkdir(parents=True, exist_ok=True)
PROCESSED.mkdir(parents=True, exist_ok=True)

# Sibling tracks' data/raw — reuse their already-downloaded bulk CSVs.
GROW_RAW = ROOT.parent / "grow-eda" / "data" / "raw"
GROW_PROCESSED = ROOT.parent / "grow-eda" / "data" / "processed"
SUSTAIN_RAW = ROOT.parent / "sustain-eda" / "data" / "raw"

COUNTRY = "Indonesia"

# Default year window — recent years only (2024 is the max in the tables).
YEAR_MIN = 2010
YEAR_MAX = 2024

GROW_DATASETS = {
    "QCL": "Crops and livestock products",
    "QI": "Production Indices",
    "QV": "Value of Agricultural Production",
}
BULK_BASENAMES = {
    "QCL": "Production_Crops_Livestock_E",
    "QI": "Production_Indices_E",
    "QV": "Value_of_Production_E",
}
BULK_ENCODING = "latin-1"


def _find_bulk_csv(basename: str, search_dirs: list[Path]) -> Path:
    for d in search_dirs:
        p = d / f"{basename}_All_Data.csv"
        if p.exists():
            return p
    raise FileNotFoundError(
        f"Could not find {basename}_All_Data.csv in "
        f"{', '.join(str(d) for d in search_dirs)}. "
        f"grow-eda's own loader extracts it into grow-eda/data/raw/ — run that "
        f"track's 01_data_loading first, or drop the CSV into indonesia-eda/data/raw/."
    )


def _melt_wide_to_long(df: pd.DataFrame) -> pd.DataFrame:
    """FAOSTAT wide (Y1961, Y1961F, ...) -> long (one row per id-cols x year)."""
    id_cols = [c for c in df.columns if not re.match(r"^Y\d{4}", c)]
    val_cols = [c for c in df.columns if re.match(r"^Y\d{4}$", c)]
    flag_cols = [c for c in df.columns if re.match(r"^Y\d{4}F$", c)]

    vals = df.melt(id_vars=id_cols, value_vars=val_cols, var_name="year", value_name="value")
    vals["year"] = vals["year"].str.extract(r"Y(\d{4})").astype(int)

    if flag_cols:
        flags = df.melt(id_vars=id_cols, value_vars=flag_cols, var_name="year", value_name="flag")
        flags["year"] = flags["year"].str.extract(r"Y(\d{4})F").astype(int)
        long = vals.merge(flags, on=id_cols + ["year"], how="left")
    else:
        long = vals
        long["flag"] = pd.NA

    return long.dropna(subset=["value"]).reset_index(drop=True)


def load_indonesia(code: str, country: str = COUNTRY, refresh: bool = False,
                   year_min: int = YEAR_MIN, year_max: int = YEAR_MAX) -> pd.DataFrame:
    """
    Load one GROW dataset (QCL/QI/QV), filtered to `country` and [year_min, year_max],
    cached to parquet.

    Prefers grow-eda's own `{code}_{year_min}_{year_max}.parquet` (its
    `load_dataset_range` cache — same underlying data, already year-filtered, no
    re-melt needed) when present; falls back to reading+melting the raw bulk CSV
    directly and filtering both country and year range itself otherwise, so this
    still works standalone if grow-eda hasn't generated that cache yet.
    """
    cache = PROCESSED / f"{code}_{country.lower()}_{year_min}_{year_max}.parquet"
    if cache.exists() and not refresh:
        print(f"[cache] {cache.name}")
        return pd.read_parquet(cache)

    grow_range_cache = GROW_PROCESSED / f"{code}_{year_min}_{year_max}.parquet"
    if grow_range_cache.exists() and not refresh:
        print(f"[grow-eda cache] {grow_range_cache.name}")
        long = pd.read_parquet(grow_range_cache)
    else:
        basename = BULK_BASENAMES[code]
        path = _find_bulk_csv(basename, [RAW, GROW_RAW])
        print(f"[bulk] reading {code} from {path} ...")
        wide = pd.read_csv(path, encoding=BULK_ENCODING, low_memory=False)
        long = _melt_wide_to_long(wide)
        long = long[(long["year"] >= year_min) & (long["year"] <= year_max)]

    sub = long[long["Area"] == country].copy()
    sub.to_parquet(cache, index=False)
    print(f"[bulk] {country} {code} {year_min}-{year_max}: {len(sub):,} rows -> {cache.name}")
    return sub


def load_landuse_indonesia(country: str = COUNTRY, refresh: bool = False) -> pd.DataFrame:
    """
    Load FAOSTAT Land Use (RL domain), filtered to `country`.

    Reused from sustain-eda/data/raw/ — same underlying FAOSTAT bulk file, no new
    download needed. Used in 03_when_it_grows for the cropping-intensity proxy
    (area harvested vs arable land -> multiple-cropping signal).
    """
    cache = PROCESSED / f"RL_{country.lower()}.parquet"
    if cache.exists() and not refresh:
        print(f"[cache] {cache.name}")
        return pd.read_parquet(cache)

    path = SUSTAIN_RAW / "Inputs_LandUse_E_All_Data.csv"
    if not path.exists():
        print(f"[optional] {path} not found — sustain-eda's Land Use CSV isn't "
              f"downloaded, so the cropping-intensity proxy will be skipped.")
        return None

    print(f"[bulk] reading Land Use from {path} ...")
    wide = pd.read_csv(path, encoding="utf-8-sig", low_memory=False)
    long = _melt_wide_to_long(wide)
    sub = long[long["Area"] == country].copy()
    sub.to_parquet(cache, index=False)
    print(f"[bulk] {country} Land Use: {len(sub):,} rows -> {cache.name}")
    return sub


def load_processed(name: str) -> pd.DataFrame:
    return pd.read_parquet(PROCESSED / f"{name}.parquet")


def save_processed(df: pd.DataFrame, name: str) -> Path:
    path = PROCESSED / f"{name}.parquet"
    df.to_parquet(path, index=False)
    print(f"saved -> {path}")
    return path


# --- Cross-country slices -------------------------------------------------
# Everything above is Indonesia-only. The cassava yield-gap analysis in
# notebook 05 needs a *multi-country* frontier, so this reads grow-eda's
# already-melted global QCL cache rather than re-melting the 92MB bulk CSV.

# FAOSTAT mixes real countries with regional/income roll-ups in the same Area
# column. Region aggregates all carry Area Code >= 5000 ("World" = 5000,
# continents 5100+, income groups 5800+) — the cheapest reliable filter.
AREA_CODE_AGGREGATE_MIN = 5000


def load_qcl_world(item: str | None = None, elements: list[str] | None = None,
                   year_min: int = YEAR_MIN, year_max: int = YEAR_MAX,
                   refresh: bool = False) -> pd.DataFrame:
    """
    Load QCL for **all countries** (region aggregates dropped), optionally
    narrowed to one `item` and a list of `elements`.

    Source preference, cheapest first:
      1. grow-eda/data/processed/QCL_{year_min}_{year_max}.parquet  (year-filtered)
      2. grow-eda/data/processed/QCL_long.parquet                   (full history)
      3. the raw bulk CSV, melted here (slow — last resort)

    When `item` is given, the narrowed slice is cached locally so repeat runs
    don't touch the multi-hundred-MB global frame at all.

    >>> cas = load_qcl_world('Cassava, fresh', ['Yield', 'Production', 'Area harvested'])
    """
    slug = None
    if item is not None:
        slug = re.sub(r"[^a-z0-9]+", "_", item.lower()).strip("_")
        cache = PROCESSED / f"QCL_world_{slug}_{year_min}_{year_max}.parquet"
        if cache.exists() and not refresh:
            print(f"[cache] {cache.name}")
            out = pd.read_parquet(cache)
            return out[out["Element"].isin(elements)].copy() if elements else out

    ranged = GROW_PROCESSED / f"QCL_{year_min}_{year_max}.parquet"
    full = GROW_PROCESSED / "QCL_long.parquet"
    if ranged.exists():
        print(f"[grow-eda cache] {ranged.name}")
        world = pd.read_parquet(ranged)
    elif full.exists():
        print(f"[grow-eda cache] {full.name} (full history — filtering to {year_min}-{year_max})")
        world = pd.read_parquet(full)
    else:
        path = _find_bulk_csv(BULK_BASENAMES["QCL"], [RAW, GROW_RAW])
        print(f"[bulk] no grow-eda QCL cache — melting {path} (slow) ...")
        world = _melt_wide_to_long(pd.read_csv(path, encoding=BULK_ENCODING, low_memory=False))

    world = world[(world["year"] >= year_min) & (world["year"] <= year_max)]
    if "Area Code" in world.columns:
        world = world[world["Area Code"] < AREA_CODE_AGGREGATE_MIN]
    world = drop_china_composite(world)   # 'China' composite double-counts 'China, mainland'

    if item is not None:
        world = world[world["Item"] == item].copy()
        if world.empty:
            raise ValueError(f"No QCL rows for Item={item!r} in {year_min}-{year_max}.")
        world.to_parquet(cache, index=False)
        print(f"[world] {item} {year_min}-{year_max}: {len(world):,} rows, "
              f"{world['Area'].nunique()} countries -> {cache.name}")

    return world[world["Element"].isin(elements)].copy() if elements else world
