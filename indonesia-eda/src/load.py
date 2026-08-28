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

Import from notebooks:  from src.load import load_indonesia, load_landuse_indonesia
"""
from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"
RAW.mkdir(parents=True, exist_ok=True)
PROCESSED.mkdir(parents=True, exist_ok=True)

# Sibling tracks' data/raw — reuse their already-downloaded bulk CSVs.
GROW_RAW = ROOT.parent / "grow-eda" / "data" / "raw"
SUSTAIN_RAW = ROOT.parent / "sustain-eda" / "data" / "raw"

COUNTRY = "Indonesia"

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


def load_indonesia(code: str, country: str = COUNTRY, refresh: bool = False) -> pd.DataFrame:
    """
    Load one GROW dataset (QCL/QI/QV), filtered to `country`, cached to parquet.

    Reads the wide bulk CSV from grow-eda/data/raw/ (falls back to this track's
    own data/raw/ if you'd rather keep a local copy), melts to long, filters to
    the country, and caches the small result — so repeat runs are instant without
    re-melting the full ~4M-row global file.
    """
    cache = PROCESSED / f"{code}_{country.lower()}.parquet"
    if cache.exists() and not refresh:
        print(f"[cache] {cache.name}")
        return pd.read_parquet(cache)

    basename = BULK_BASENAMES[code]
    path = _find_bulk_csv(basename, [RAW, GROW_RAW])
    print(f"[bulk] reading {code} from {path} ...")
    wide = pd.read_csv(path, encoding=BULK_ENCODING, low_memory=False)
    long = _melt_wide_to_long(wide)
    sub = long[long["Area"] == country].copy()
    sub.to_parquet(cache, index=False)
    print(f"[bulk] {country} {code}: {len(sub):,} rows -> {cache.name}")
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
