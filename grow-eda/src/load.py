"""
Data loading helpers for FAOSTAT GROW datasets (QCL, QI, QV).

Reads the FAOSTAT **bulk download** CSVs (no account/API needed). The bulk files
come in WIDE format (Y1961, Y1961F, Y1962, Y1962F, ...); this module melts them
to the LONG format (one row per area/item/element/year) that the notebooks expect,
and caches the result to parquet so the (slow) melt runs only once.

Import from notebooks:  from src.load import load_dataset, load_codes
"""
from __future__ import annotations

import re
import zipfile
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"
RAW.mkdir(parents=True, exist_ok=True)
PROCESSED.mkdir(parents=True, exist_ok=True)

GROW_DATASETS = {
    "QCL": "Crops and livestock products",
    "QI": "Production Indices",
    "QV": "Value of Agricultural Production",
}

# Map dataset code -> the bulk file's base name (the part before _E_All_Data).
# Point these at wherever you extracted the CSVs (default: data/raw/).
BULK_BASENAMES = {
    "QCL": "Production_Crops_Livestock_E",
    "QI": "Production_Indices_E",
    "QV": "Value_of_Production_E",
}

# FAOSTAT bulk CSVs are latin-1 / cp1252 encoded, not utf-8.
BULK_ENCODING = "latin-1"


def _find_bulk_file(code: str, suffix: str, search_dirs: list[Path]) -> Path | None:
    """Locate a bulk CSV (or its zip) by dataset code + suffix across search dirs."""
    base = BULK_BASENAMES[code]
    name = f"{base}_{suffix}.csv"
    for d in search_dirs:
        p = d / name
        if p.exists():
            return p
    # look inside a matching zip if the loose csv isn't found
    for d in search_dirs:
        for z in d.glob(f"{base}_All_Data*.zip"):
            with zipfile.ZipFile(z) as zf:
                if name in zf.namelist():
                    return z  # signal: caller reads from zip
    return None


def _read_bulk_csv(code: str, suffix: str, search_dirs: list[Path]) -> pd.DataFrame:
    base = BULK_BASENAMES[code]
    name = f"{base}_{suffix}.csv"
    for d in search_dirs:
        p = d / name
        if p.exists():
            return pd.read_csv(p, encoding=BULK_ENCODING, low_memory=False)
        for z in d.glob(f"{base}_All_Data*.zip"):
            with zipfile.ZipFile(z) as zf:
                if name in zf.namelist():
                    with zf.open(name) as fh:
                        return pd.read_csv(fh, encoding=BULK_ENCODING, low_memory=False)
    raise FileNotFoundError(
        f"Could not find {name} in {', '.join(str(d) for d in search_dirs)}. "
        f"Extract the bulk zip into data/raw/ or pass search_dirs=[...]."
    )


def _melt_wide_to_long(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert FAOSTAT wide bulk format to long.
    Year value columns look like 'Y2020'; matching flag columns like 'Y2020F'.
    """
    id_cols = [c for c in df.columns if not re.match(r"^Y\d{4}", c)]
    val_cols = [c for c in df.columns if re.match(r"^Y\d{4}$", c)]
    flag_cols = [c for c in df.columns if re.match(r"^Y\d{4}F$", c)]

    vals = df.melt(id_vars=id_cols, value_vars=val_cols,
                   var_name="year", value_name="value")
    vals["year"] = vals["year"].str.extract(r"Y(\d{4})").astype(int)

    if flag_cols:
        flags = df.melt(id_vars=id_cols, value_vars=flag_cols,
                        var_name="year", value_name="flag")
        flags["year"] = flags["year"].str.extract(r"Y(\d{4})F").astype(int)
        long = vals.merge(flags, on=id_cols + ["year"], how="left")
    else:
        long = vals
        long["flag"] = pd.NA

    # drop rows with no observation (wide format is sparse -> many NaN values)
    long = long.dropna(subset=["value"]).reset_index(drop=True)
    return long


def load_dataset(
    code: str,
    search_dirs: list[str | Path] | None = None,
    refresh: bool = False,
    tag: str = "long",
) -> pd.DataFrame:
    """
    Load a GROW dataset from bulk CSV, melted to long format, cached to parquet.

    Parameters
    ----------
    code : 'QCL' | 'QI' | 'QV'
    search_dirs : where to look for the extracted CSV / zip.
                  Defaults to [data/raw/, ~/Downloads/<basename>_All_Data/].
    refresh : re-melt from CSV even if a parquet cache exists.
    tag : cache label.
    """
    cache = PROCESSED / f"{code}_{tag}.parquet"
    if cache.exists() and not refresh:
        print(f"[cache] {cache.name}")
        return pd.read_parquet(cache)

    dirs = _default_search_dirs(code, search_dirs)
    print(f"[bulk] reading {code} from CSV ...")
    wide = _read_bulk_csv(code, "All_Data", dirs)
    print(f"[bulk] wide: {wide.shape[0]:,} rows x {wide.shape[1]} cols -> melting")
    long = _melt_wide_to_long(wide)
    long.to_parquet(cache, index=False)
    print(f"[bulk] long: {len(long):,} rows -> {cache.name}")
    return long


def load_dataset_range(
    code: str,
    start_year: int = 2010,
    end_year: int = 2024,
    search_dirs: list[str | Path] | None = None,
    refresh: bool = False,
) -> pd.DataFrame:
    """
    Load a GROW dataset restricted to [start_year, end_year], cached separately
    from the full-history cache (does not touch `{code}_long.parquet` or any
    notebook that calls `load_dataset` directly — purely additive).

    Use this for a "recent years only" analysis (e.g. the Indonesia deep-dive)
    without invalidating the full 1961-2024 cache the existing 01-08 notebooks
    already ran against.
    """
    cache = PROCESSED / f"{code}_{start_year}_{end_year}.parquet"
    if cache.exists() and not refresh:
        print(f"[cache] {cache.name}")
        return pd.read_parquet(cache)

    full = load_dataset(code, search_dirs=search_dirs, refresh=refresh)
    ranged = full[(full["year"] >= start_year) & (full["year"] <= end_year)].copy()
    ranged.to_parquet(cache, index=False)
    print(f"[range] {code} {start_year}-{end_year}: {len(ranged):,} rows -> {cache.name}")
    return ranged


def load_codes(code: str, kind: str,
               search_dirs: list[str | Path] | None = None) -> pd.DataFrame:
    """
    Load a lookup table that ships with the bulk download.
    kind in {'AreaCodes', 'ItemCodes', 'Elements', 'Flags'}.
    """
    dirs = _default_search_dirs(code, search_dirs)
    return _read_bulk_csv(code, kind, dirs)


def _default_search_dirs(code: str, search_dirs) -> list[Path]:
    if search_dirs:
        return [Path(d) for d in search_dirs]
    base = BULK_BASENAMES[code]
    return [
        RAW,
        Path.home() / "Downloads" / f"{base}_All_Data",
        Path.home() / "Downloads",
    ]


def load_processed(name: str) -> pd.DataFrame:
    return pd.read_parquet(PROCESSED / f"{name}.parquet")


def save_processed(df: pd.DataFrame, name: str) -> Path:
    path = PROCESSED / f"{name}.parquet"
    df.to_parquet(path, index=False)
    print(f"saved -> {path}")
    return path
