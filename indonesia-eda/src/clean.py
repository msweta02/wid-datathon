"""
Cleaning / standardization helpers, trimmed from grow-eda/src/clean.py.

No aggregate-splitting or China-entity handling here — data is already filtered
to a single country (Indonesia) by src/load.py. What's still needed: flags and
unit normalization.
"""
from __future__ import annotations

import pandas as pd

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

# FAOSTAT mixes individual commodities (Rice) with roll-up aggregates
# ("Cereals, primary", "Fruit Primary") in QCL. Ranking production without
# excluding these double-counts the underlying items.
ITEM_AGGREGATE_PATTERNS = (
    ", total", " total", "primary", " nes", "n.e.c", "roots and tubers, total",
    "citrus fruit, total", "oilcrops", "pulses, total", "cereals",
    "vegetables primary", "fruit primary", "coarse grain", "treenuts, total",
)


def annotate_flags(df: pd.DataFrame, flag_col: str = "flag") -> pd.DataFrame:
    """Add a human-readable flag_meaning column."""
    if flag_col not in df.columns:
        return df
    df = df.copy()
    df["flag_meaning"] = df[flag_col].fillna("").map(FLAG_MEANINGS).fillna("Other")
    return df


def yield_to_tonnes_per_ha(series: pd.Series, unit: str) -> pd.Series:
    """Normalize FAOSTAT yield to tonnes/ha (commonly reported as hg/ha)."""
    unit = (unit or "").lower()
    if "hg/ha" in unit or "hectogram" in unit:
        return series / 10000.0
    if "kg/ha" in unit:
        return series / 1000.0
    if "100 g/ha" in unit:
        return series / 10000.0
    return series  # assume already t/ha


def flag_item_aggregates(df: pd.DataFrame, item_col: str = "Item") -> pd.Series:
    """Boolean mask marking rows whose item is a FAOSTAT roll-up rather than a
    single commodity. Heuristic (label-based); verify against ItemCodes if unsure."""
    low = df[item_col].astype(str).str.lower()
    mask = pd.Series(False, index=df.index)
    for pat in ITEM_AGGREGATE_PATTERNS:
        mask |= low.str.contains(pat, regex=False)
    return mask


def drop_item_aggregates(df: pd.DataFrame, item_col: str = "Item") -> pd.DataFrame:
    """Keep only leaf-level items (drop roll-up totals)."""
    return df[~flag_item_aggregates(df, item_col)].copy()


# Indonesia's largest permanent (tree/shrub) crops by area — NOT part of FAO's
# "Arable land" by definition (that's temporary-crop land only; permanent crops
# sit on "Land under permanent crops" instead). Comparing all-crop area harvested
# against arable land alone overstates cropping intensity by exactly this much —
# oil palm alone is ~14M ha, more than the entire rice area. Heuristic list, not
# exhaustive; verify against FAOSTAT's Item Group classification if precision matters.
PERMANENT_CROP_ITEMS = (
    "oil palm fruit", "coconuts, in shell", "cocoa beans", "coffee, green",
    "cloves", "cashew nuts, in shell", "mangoes, guavas and mangosteens",
    "rubber, natural", "bananas", "oranges",
)


def drop_permanent_crops(df: pd.DataFrame, item_col: str = "Item") -> pd.DataFrame:
    """Drop permanent/perennial tree & shrub crops (see PERMANENT_CROP_ITEMS)."""
    low = df[item_col].astype(str).str.lower()
    mask = pd.Series(False, index=df.index)
    for pat in PERMANENT_CROP_ITEMS:
        mask |= low.str.contains(pat, regex=False)
    return df[~mask].copy()


# --- Cross-country hygiene ------------------------------------------------
# Only needed once a frame spans multiple countries (see load.load_qcl_world);
# the Indonesia-only frames above never hit this.

# FAOSTAT ships China three ways at once: 351 "China" (composite = mainland +
# Taiwan + HK + Macao), 41 "China, mainland", plus the SARs/Taiwan separately.
# Keeping 351 alongside its parts double-counts China in any ranking.
CHINA_COMPOSITE_AREA_CODE = 351


def drop_china_composite(df: pd.DataFrame) -> pd.DataFrame:
    """Drop FAOSTAT's 'China' composite, keeping 'China, mainland' + the SARs/Taiwan."""
    if "Area Code" in df.columns:
        return df[df["Area Code"] != CHINA_COMPOSITE_AREA_CODE].copy()
    return df[df["Area"] != "China"].copy()


# FAOSTAT reports QCL "Production" in more than one unit: crops in tonnes, but
# eggs (and some livestock items) in "1000 No". Grouping by Item alone therefore
# sums heads/numbers into tonnages — which ranked hen eggs as Indonesia's #2
# "crop" (146bn eggs + 6.6Mt read as 1.5e8 t). Always filter before ranking.
TONNE_UNITS = ("t", "tonnes")


def tonnes_only(df: pd.DataFrame, unit_col: str = "Unit") -> pd.DataFrame:
    """Keep only rows reported in tonnes, so a tonnage ranking stays comparable."""
    if unit_col not in df.columns:
        return df
    return df[df[unit_col].astype(str).str.strip().str.lower().isin(TONNE_UNITS)].copy()
