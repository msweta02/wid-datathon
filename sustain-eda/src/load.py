"""Loading FAOSTAT bulk CSVs.

FAOSTAT bulk downloads ("All Data", no account needed) come in WIDE format —
one column per year (Y1961, Y1961F, Y1962, Y1962F, ...) with single-letter flag
codes. clean.py/footprint.py expect the LONG format (one row per
Area/Item/Element/Year with Value + Flag Description), so this module melts on
read. Same shape of fix as grow-eda/src/load.py._melt_wide_to_long.
"""

import re
from pathlib import Path

import pandas as pd

# Default locations; override by passing explicit paths.
DATA_RAW = Path(__file__).resolve().parents[1] / "data" / "raw"

FILES = {
    "emissions": "Emissions_Totals_E_All_Data.csv",
    "intensities": "Environment_Emissions_intensities_E_All_Data.csv",
    "landuse": "Inputs_LandUse_E_All_Data.csv",
}

# Optional datasets. Download from FAOSTAT (bulk "All Data"):
#   Population.csv     <- Population domain > Annual population (Total, both sexes)
#   Food_Balances.csv  <- Food Balances > Food Balances (2010-), kcal/capita/day
#   nutrient_balance   <- Land, Inputs & Sustainability > Cropland Nutrient Balance
#                         (on disk: Environment_Cropland_nutrient_budget_E_All_Data.csv)
#   land_cover         <- Land, Inputs & Sustainability > Land Cover
#                         (on disk: Environment_LandCover_E_All_Data.csv)
OPTIONAL_FILES = {
    "population": "Population.csv",
    "food_balances": "Food_Balances.csv",
    "nutrient_balance": "Environment_Cropland_nutrient_budget_E_All_Data.csv",
    "land_cover": "Environment_LandCover_E_All_Data.csv",
}

# Standard FAOSTAT flag legend (code -> description), for the "Flag Description"
# column the Normalized export would otherwise have supplied.
FLAG_DESCRIPTIONS = {
    "": "Official figure",
    "A": "Official figure",
    "E": "Estimated value",
    "F": "FAO estimate",
    "Fc": "Calculated data",
    "I": "Imputed value",
    "M": "Data not available",
    "N": "Not officially reported",
    "P": "Provisional value",
    "R": "Estimated using trading partners database",
    "S": "Standardized data",
    "T": "Unofficial figure",
    "X": "Figure from international organization",
    "Z": "Not available",
}


def _read_csv(path: Path) -> pd.DataFrame:
    """Read one FAOSTAT bulk CSV, trying common encodings."""
    if not path.exists():
        raise FileNotFoundError(f"{path} not found. Put the CSV in data/raw/.")
    for enc in ("utf-8-sig", "latin-1"):
        try:
            return pd.read_csv(path, encoding=enc, low_memory=False)
        except UnicodeDecodeError:
            continue
    raise ValueError(f"Could not decode {path} with utf-8-sig or latin-1.")


def _melt_wide_to_long(wide: pd.DataFrame) -> pd.DataFrame:
    """Convert FAOSTAT wide bulk format to long: one row per id-cols x Year.

    If the frame is already long (no Y#### columns — e.g. a Normalized
    export), it's returned unchanged.
    """
    val_cols = [c for c in wide.columns if re.match(r"^Y\d{4}$", c)]
    if not val_cols:
        return wide

    id_cols = [c for c in wide.columns if not re.match(r"^Y\d{4}", c)]
    flag_cols = [c for c in wide.columns if re.match(r"^Y\d{4}F$", c)]

    long = wide.melt(id_vars=id_cols, value_vars=val_cols, var_name="Year", value_name="Value")
    long["Year"] = long["Year"].str.extract(r"(\d{4})").astype(int)

    if flag_cols:
        flags = wide.melt(id_vars=id_cols, value_vars=flag_cols, var_name="Year", value_name="Flag")
        flags["Year"] = flags["Year"].str.extract(r"(\d{4})").astype(int)
        long = long.merge(flags, on=id_cols + ["Year"], how="left")
        long["Flag"] = long["Flag"].fillna("")
        long["Flag Description"] = long["Flag"].map(FLAG_DESCRIPTIONS).fillna(long["Flag"])

    # wide format is sparse (many years unreported per row) -> drop no-observation rows
    return long.dropna(subset=["Value"]).reset_index(drop=True)


def read_faostat(path) -> pd.DataFrame:
    """Read one FAOSTAT bulk CSV and melt it to the long format the rest of src/ expects."""
    wide = _read_csv(Path(path))
    return _melt_wide_to_long(wide)


def try_read(key, data_dir=DATA_RAW):
    """Read an optional dataset by key; return None (with a hint) if absent.

    Tries the exact filename first, then a loose glob on distinctive tokens so
    a slightly different FAOSTAT bulk name still loads. Lets notebooks degrade
    gracefully when a dataset isn't downloaded yet, instead of raising.
    """
    data_dir = Path(data_dir)
    fname = OPTIONAL_FILES.get(key, FILES.get(key))
    path = data_dir / fname
    if path.exists():
        return read_faostat(path)

    # Loose fallback: match on distinctive tokens from the key.
    tokens = {
        "nutrient_balance": ["cropland", "nutrient"],
        "land_cover": ["landcover"],
        "population": ["population"],
        "food_balances": ["food", "balance"],
    }.get(key, [key])
    for cand in data_dir.glob("*.csv"):
        low = cand.name.lower().replace("_", "").replace(" ", "")
        if all(t.replace("_", "") in low for t in tokens):
            return read_faostat(cand)

    print(f"[optional] {fname} not found in data/raw/ — "
          f"download it to enable this analysis. Skipping.")
    return None


def load_all(data_dir=DATA_RAW) -> dict:
    """Load the three core Sustain datasets into a dict of DataFrames."""
    data_dir = Path(data_dir)
    return {key: read_faostat(data_dir / fname) for key, fname in FILES.items()}
