"""
Cleaning / standardization helpers for FAOSTAT frames.

Handles the common FAOSTAT gotchas: flags, aggregate vs country separation,
the China multi-entity problem, and unit normalization.
"""
from __future__ import annotations

import pandas as pd

# FAOSTAT area codes >= this are regional / income / special aggregates, not countries.
AGGREGATE_AREA_THRESHOLD = 5000

# The China entity tangle. Keep ONE to avoid double counting.
CHINA_CODES = {
    41: "China, mainland",
    214: "China, Taiwan Province of",
    96: "China, Hong Kong SAR",
    128: "China, Macao SAR",
    351: "China",              # China + HK + Macao + Taiwan
    357: "China, mainland + Taiwan",
}
# Default: use mainland only for country-level comparisons.
CHINA_KEEP_DEFAULT = 41

# Common flag meanings (FAOSTAT 2023+ flag scheme; older data uses letters).
FLAG_MEANINGS = {
    "A": "Official figure",
    "E": "Estimated value",
    "I": "Imputed value",
    "M": "Missing (data cannot exist / not collected)",
    "X": "Figure from international organizations",
    "T": "Unofficial figure",
    "B": "Time series break",
    "": "Official / unspecified",
}


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Lowercase, snake_case column names for consistency across datasets."""
    df = df.copy()
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("__", "_")
    )
    return df


def split_aggregates(df: pd.DataFrame, area_code_col: str = "area_code") -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Split into (countries, aggregates) using the area-code threshold.
    Returns two frames so you never accidentally sum 'World' into a country total.
    """
    if area_code_col not in df.columns:
        raise KeyError(f"{area_code_col!r} not in columns: {list(df.columns)[:10]}...")
    codes = pd.to_numeric(df[area_code_col], errors="coerce")
    is_agg = codes >= AGGREGATE_AREA_THRESHOLD
    return df[~is_agg].copy(), df[is_agg].copy()


def resolve_china(df: pd.DataFrame, keep: int = CHINA_KEEP_DEFAULT,
                  area_code_col: str = "area_code") -> pd.DataFrame:
    """Drop all China entities except the one you choose to keep."""
    codes = pd.to_numeric(df[area_code_col], errors="coerce")
    drop = set(CHINA_CODES) - {keep}
    return df[~codes.isin(drop)].copy()


def annotate_flags(df: pd.DataFrame, flag_col: str = "flag") -> pd.DataFrame:
    """Add a human-readable flag_meaning column."""
    if flag_col not in df.columns:
        return df
    df = df.copy()
    df["flag_meaning"] = df[flag_col].fillna("").map(FLAG_MEANINGS).fillna("Other")
    return df


def yield_to_tonnes_per_ha(series: pd.Series, unit: str) -> pd.Series:
    """
    Normalize FAOSTAT yield to tonnes/ha.
    FAOSTAT commonly reports hg/ha (hectograms per hectare).
    """
    unit = (unit or "").lower()
    if "hg/ha" in unit or "hectogram" in unit:
        return series / 10000.0
    if "kg/ha" in unit:
        return series / 1000.0
    if "100 g/ha" in unit:
        return series / 10000.0
    return series  # assume already t/ha


# Item-aggregate detection.
# FAOSTAT mixes individual commodities (Wheat) with roll-up aggregates
# (e.g. "Cereals, Total", "Meat, Total", "... nes") in QCL. Ranking production
# without excluding these double-counts the underlying items.
ITEM_AGGREGATE_PATTERNS = (
    ", total", " total", "primary", " nes", "n.e.c", "roots and tubers, total",
    "citrus fruit, total", "oilcrops", "pulses, total", "cereals",
    "vegetables primary", "fruit primary", "coarse grain", "treenuts, total",
)


def flag_item_aggregates(df: pd.DataFrame, item_col: str = "item") -> pd.Series:
    """
    Boolean mask marking rows whose item is a FAOSTAT roll-up/aggregate rather than
    a single commodity. Heuristic (label-based); verify against ItemCodes if unsure.
    """
    low = df[item_col].astype(str).str.lower()
    mask = pd.Series(False, index=df.index)
    for pat in ITEM_AGGREGATE_PATTERNS:
        mask |= low.str.contains(pat, regex=False)
    return mask


def data_quality_report(df: pd.DataFrame, value_col: str = "value",
                        flag_col: str = "flag") -> dict:
    """Quick dictionary of quality stats for a frame — use in the feasibility notebook."""
    report = {
        "rows": len(df),
        "n_missing_value": int(df[value_col].isna().sum()) if value_col in df else None,
        "pct_missing_value": (
            round(100 * df[value_col].isna().mean(), 2) if value_col in df else None
        ),
    }
    if flag_col in df.columns:
        report["flag_distribution"] = (
            df[flag_col].fillna("").value_counts(normalize=True).round(3).to_dict()
        )
    for col in ("year",):
        if col in df.columns:
            yrs = pd.to_numeric(df[col], errors="coerce")
            report["year_min"] = int(yrs.min())
            report["year_max"] = int(yrs.max())
    return report
