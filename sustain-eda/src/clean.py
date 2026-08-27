"""Cleaning helpers for FAOSTAT data.

The single most important step is dropping M49 *aggregates* (World, regions,
income groups) before any ranking, or they dominate every chart.
"""

import pandas as pd

# Named aggregates to catch defensively alongside the numeric M49 rule.
AGG_NAME_PAT = (
    r"World|Africa|Americas|America|Asia|Europe|Oceania|European Union|"
    r"Annex|Non-Annex|income|OECD|least developed|landlocked|small island|"
    r"developed|developing|Net Food|Low Income|Central|Eastern|Western|"
    r"Northern|Southern|Caribbean|Melanesia|Micronesia|Polynesia|"
    r"Australia and New Zealand|European|Union|USSR|Yugoslav|"
    r"Belgium-Luxembourg|Czechoslovakia|Serbia and Montenegro"
)

# FAOSTAT lists "China" (a roll-up of mainland + HK + Macao + Taiwan) alongside
# those parts. Keeping both double-counts. We drop the "China" aggregate and keep
# "China, mainland" as the country. Handled as an exact-name rule below.
CHINA_ROLLUP = "China"


def split_countries_aggregates(df: pd.DataFrame):
    """Split a FAOSTAT frame into (countries, aggregates).

    Real countries have M49 code < 500; aggregates use >= 500 plus a few
    named exceptions caught by AGG_NAME_PAT.
    """
    # Find the M49 code column (name varies slightly across exports).
    code_col = next(
        (c for c in df.columns if "M49" in c or c == "Area Code"), None
    )
    if code_col is not None:
        codes = pd.to_numeric(
            df[code_col].astype(str).str.replace("'", "", regex=False),
            errors="coerce",
        )
        is_agg_code = codes >= 500
    else:
        is_agg_code = pd.Series(False, index=df.index)

    is_agg = is_agg_code | df["Area"].str.contains(
        AGG_NAME_PAT, case=False, na=False, regex=True
    )
    # Drop the exact "China" roll-up (keep "China, mainland"); avoids double count.
    is_agg = is_agg | (df["Area"] == CHINA_ROLLUP)
    return df[~is_agg].copy(), df[is_agg].copy()


def pick_analysis_year(df_countries: pd.DataFrame, coverage=0.9) -> int:
    """Most recent year whose country coverage is >= `coverage` of the peak."""
    cov = df_countries.groupby("Year")["Area"].nunique()
    good = cov[cov >= coverage * cov.max()]
    return int(good.index.max())


def pick_co2eq_element(df_countries: pd.DataFrame):
    """Pick a CO2eq 'total' element so gases are comparable, else the first CO2eq one."""
    co2eq = [e for e in df_countries["Element"].unique() if "CO2eq" in str(e)]
    if not co2eq:
        return None

    # We want the ALL-GAS total, not a single-gas CO2eq (e.g. "...from N2O").
    # Single-gas elements name the gas; exclude them, then prefer a "total".
    single_gas = ("n2o", "ch4", "co2", "f-gas", "fgas")
    all_gas = [e for e in co2eq if not any(g in e.lower() for g in single_gas)]
    pool = all_gas or co2eq  # fall back to any CO2eq if all name a gas

    # Prefer an explicit total/net; else the shortest name (usually the plain total).
    for kw in ("total", "net", "all ghg", "ghg"):
        hit = next((e for e in pool if kw in e.lower()), None)
        if hit:
            return hit
    return min(pool, key=len)


def basic_report(df: pd.DataFrame, name: str) -> None:
    """Print a quick shape/coverage/flag summary."""
    print(f"=== {name} ===")
    print("shape:", df.shape)
    print("years:", df["Year"].min(), "->", df["Year"].max())
    print("missing Value:", df["Value"].isna().sum())
    if "Flag Description" in df.columns:
        print("flags:\n", df["Flag Description"].value_counts(dropna=False).head())
    print()
