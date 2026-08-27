"""Footprint analysis: rank sources/countries, intensity, levers, per-hectare.

This is the Sustain-track analog of the grow track's concentration.py — it
quantifies the environmental cost of production and locates the biggest levers.
"""

import pandas as pd

# Roll-up / total Items in Emissions totals that DOUBLE-COUNT leaf sources.
# These must be excluded from source rankings, or the grand total wins trivially.
# (e.g. "All sectors with LULUCF" contains "Farm gate" contains "Emissions from
# livestock".) Matched case-insensitively as substrings.
AGGREGATE_ITEMS = (
    "all sectors", "agrifood systems", "afolu", "farm gate",
    "ipcc agriculture", "emissions on agricultural land",
    "land use, land-use change", "lulucf", "total",
)
# NOTE: mid-level items like "Emissions from livestock" / "Emissions from crops"
# are KEPT — they're a useful grouping level. If you drill to true leaves
# (Enteric Fermentation, Synthetic Fertilizers, Rice Cultivation, ...), add them
# here or filter to the specific items you want. Inspect with the discovery cell.

# Non-agrifood IPCC sectors present in Emissions totals. For the SUSTAIN track
# ("how we feed ourselves") these are OUT OF SCOPE — economy-wide energy,
# industry, and waste are not food-system sources and otherwise dominate.
NON_AGRIFOOD_ITEMS = (
    "energy",          # economy-wide fossil energy (NOT "on-farm energy use")
    "ippu",            # industrial processes & product use
    "waste",           # municipal/industrial waste
    "other",           # residual sectors
    "international bunkers",
)


def is_agrifood_source(item: str) -> bool:
    """True if the Item is a food-system source (excludes Energy/IPPU/Waste).

    Keeps 'On-farm energy use' while excluding economy-wide 'Energy'.
    """
    s = str(item).lower()
    if "on-farm energy" in s:      # explicitly an agrifood item
        return True
    return not any(a == s or s.startswith(a) for a in NON_AGRIFOOD_ITEMS)


def scope_agrifood(df):
    """Restrict to food-system items: leaf-level AND agrifood (no IPCC sectors)."""
    m = df["Item"].map(lambda x: is_leaf_source(x) and is_agrifood_source(x))
    return df[m].copy()


def is_leaf_source(item: str) -> bool:
    """True if the Item is a specific source, not a roll-up total."""
    s = str(item).lower()
    return not any(a in s for a in AGGREGATE_ITEMS)


def drop_aggregate_items(df):
    """Keep only leaf-level source Items (drop roll-up totals)."""
    return df[df["Item"].map(is_leaf_source)].copy()


def rank_sources(df_countries, year, element=None, leaf_only=True,
                 agrifood_only=True):
    """Total emissions by Item (activity) for one year, ranked descending.

    leaf_only drops roll-up totals; agrifood_only drops non-food IPCC sectors
    (Energy, IPPU, Waste) so the ranking reflects the FOOD-system footprint.
    """
    yr = df_countries[df_countries["Year"] == year]
    if element is not None:
        yr = yr[yr["Element"] == element]
    if agrifood_only:
        yr = scope_agrifood(yr)
    elif leaf_only:
        yr = drop_aggregate_items(yr)
    return yr.groupby("Item")["Value"].sum().sort_values(ascending=False)


def rank_countries(df_countries, year, element=None, leaf_only=True,
                   agrifood_only=True):
    """Total emissions by country for one year, ranked descending.

    Scopes to agrifood leaf sources to avoid double-counting and to keep the
    food-system framing consistent with rank_sources.
    """
    yr = df_countries[df_countries["Year"] == year]
    if element is not None:
        yr = yr[yr["Element"] == element]
    if agrifood_only:
        yr = scope_agrifood(yr)
    elif leaf_only:
        yr = drop_aggregate_items(yr)
    return yr.groupby("Area")["Value"].sum().sort_values(ascending=False)


def source_trends(df_countries, items, element=None):
    """Time series (Year x Item) of emissions for the given items."""
    sub = df_countries[df_countries["Item"].isin(items)]
    if element is not None:
        sub = sub[sub["Element"] == element]
    return sub.groupby(["Year", "Item"])["Value"].sum().unstack()


def _intensity_only(intensities, unit_contains="kg"):
    """Keep only rows that are per-kg emissions INTENSITY.

    The Emissions intensities file also carries production/emission amounts;
    filter to the intensity Element (unit like 'kg CO2eq/kg') so we never mix
    tiny per-kg ratios with huge absolute quantities.
    """
    df = intensities
    # Prefer an explicit intensity element; else fall back to unit match.
    if "Element" in df.columns:
        mask_e = df["Element"].str.contains("intensit", case=False, na=False)
        if mask_e.any():
            df = df[mask_e]
    if "Unit" in df.columns:
        mask_u = df["Unit"].str.contains(unit_contains, case=False, na=False)
        if mask_u.any():
            df = df[mask_u]
    return df


def commodity_intensity(intensities_countries, year):
    """Median emissions intensity (kg CO2eq/kg) by commodity for one year."""
    iy = _intensity_only(intensities_countries)
    iy = iy[iy["Year"] == year]
    return iy.groupby("Item")["Value"].median().sort_values(ascending=False)


def lever_table(emissions_countries, intensities_countries, year,
                commodity, min_countries=20):
    """Country volume vs intensity for a commodity -> the lever quadrant data.

    NOTE: emissions and intensities use different item-coding systems, so this
    joins on Area + Year only, never on item code.
    """
    iy = intensities_countries[
        (intensities_countries["Year"] == year)
        & (intensities_countries["Item"] == commodity)
    ][["Area", "Value"]].rename(columns={"Value": "intensity"})

    vol = (
        emissions_countries[emissions_countries["Year"] == year]
        .groupby("Area")["Value"].sum().rename("volume")
    )
    q = iy.merge(vol, on="Area", how="inner")
    return q


def pick_lever_commodity(intensity_series, intensities_countries, year,
                         min_countries=20):
    """Highest-intensity commodity that still has enough country coverage."""
    iy = intensities_countries[intensities_countries["Year"] == year]
    for c in intensity_series.index:
        if iy[iy["Item"] == c]["Area"].nunique() >= min_countries:
            return c
    return intensity_series.index[0]


def emissions_per_land(emissions_countries, landuse_countries, year,
                       land_item=None, element=None, agrifood_only=True):
    """Agrifood emissions per 1000 ha of agricultural land, ranked descending."""
    if land_item is None:
        land_item = next(
            (i for i in landuse_countries["Item"].unique()
             if "Agricultural" in str(i) or "Cropland" in str(i)),
            None,
        )
    if land_item is None:
        return None, None
    la = (
        landuse_countries[
            (landuse_countries["Item"] == land_item)
            & (landuse_countries["Year"] == year)
        ].groupby("Area")["Value"].sum().rename("land_1000ha")
    )
    em_df = emissions_countries[emissions_countries["Year"] == year]
    if element is not None:
        em_df = em_df[em_df["Element"] == element]
    if agrifood_only:
        em_df = scope_agrifood(em_df)
    em = em_df.groupby("Area")["Value"].sum().rename("emissions")
    per = pd.concat([em, la], axis=1).dropna()
    per = per[per["land_1000ha"] > 0]
    per["emis_per_1000ha"] = per["emissions"] / per["land_1000ha"]
    return per.sort_values("emis_per_1000ha", ascending=False), land_item


# Route the dominant source to the FAOSTAT dataset that explains its mechanism.
_ROUTES = [
    (("pre- and post", "pre and post", "household consumption", "retail",
      "processing", "packaging", "transport"),
     "Emissions from pre and post agricultural production (Agrifood systems)",
     "food processing, transport, retail, waste — supply-chain levers"),
    (("enteric", "livestock", "cattle", "manure", "animal"),
     "Emissions from Livestock (Farm gate)",
     "drill into methane by animal + manure management"),
    (("fertil", "soil", "n2o", "synthetic"),
     "Fertilizers by Nutrient (Land, Inputs & Sustainability)",
     "link N applied to N2O emissions -> a concrete lever"),
    (("rice", "paddy"),
     "Emissions from Crops (Farm gate) + Production/Crops",
     "methane per tonne of rice; water-management levers"),
    (("forest", "fire", "land", "drained", "organic soil", "conversion"),
     "Emissions from Forests / Fires / Drained organic soils",
     "separate land-conversion footprint from farm-gate"),
    (("energy", "fuel"),
     "Emissions from Energy use in agriculture (Farm gate)",
     "on-farm fuel/electricity decarbonization"),
]


def next_dataset(top_source_name):
    """Given the top source, suggest the next FAOSTAT dataset to pull."""
    s = str(top_source_name).lower()
    match = next((r for r in _ROUTES if any(k in s for k in r[0])), None)
    if match:
        return match[1], match[2]
    return None, "No preset match; inspect the top-10 sources and pick the Farm-gate / Land-use-change file naming that source."


# ---------------------------------------------------------------------------
# Analysis helpers for the extra EDA notebooks (gases, normalization, gap).
# ---------------------------------------------------------------------------

def gas_breakdown(df_countries, year, agrifood_only=True):
    """Emissions by gas (CH4 / N2O / CO2 / F-gases) for one year.

    Uses the per-gas CO2eq elements so gases are comparable on one scale.
    Returns a Series indexed by gas label.
    """
    gas_elems = {
        "CH4": "Emissions (CO2eq) from CH4 (AR5)",
        "N2O": "Emissions (CO2eq) from N2O (AR5)",
        "F-gases": "Emissions (CO2eq) from F-gases (AR5)",
    }
    yr = df_countries[df_countries["Year"] == year]
    if agrifood_only:
        yr = scope_agrifood(yr)
    out = {}
    for label, elem in gas_elems.items():
        out[label] = yr[yr["Element"] == elem]["Value"].sum()
    # CO2 = all-gas total minus the named gases (FAOSTAT has no direct CO2 CO2eq).
    total = yr[yr["Element"] == "Emissions (CO2eq) (AR5)"]["Value"].sum()
    out["CO2 (residual)"] = max(total - sum(out.values()), 0)
    import pandas as pd
    return pd.Series(out).sort_values(ascending=False)


def per_capita(value_by_area, population_by_area):
    """Divide an emissions Series by a population Series (aligned on Area)."""
    import pandas as pd
    df = pd.concat([value_by_area.rename("value"),
                    population_by_area.rename("pop")], axis=1).dropna()
    df = df[df["pop"] > 0]
    df["per_capita"] = df["value"] / df["pop"]
    return df.sort_values("per_capita", ascending=False)


def population_series(pop_df, year, element_contains="Total Population - Both"):
    """Extract a country->population Series from FAOSTAT Annual population."""
    p = pop_df[pop_df["Year"] == year]
    p = p[p["Element"].str.contains(element_contains, case=False, na=False)]
    # FAOSTAT population unit is often "1000 persons"; keep raw, note in notebook.
    return p.groupby("Area")["Value"].sum()


def intensity_gap(intensities_countries, commodity, year, min_countries=10,
                  trim=0.02):
    """Best-in-class vs worst-in-class intensity for a commodity.

    Filters to the per-kg intensity element and trims extreme outliers so the
    ratio reflects real best/worst producers, not data artifacts.
    """
    iy = _intensity_only(intensities_countries)
    iy = iy[(iy["Item"] == commodity) & (iy["Year"] == year)]
    s = iy.groupby("Area")["Value"].median()
    s = s[(s > 0) & s.notna()]
    if s.nunique() < min_countries:
        return None
    # Trim the extreme tails (default 2% each side) to drop artifacts.
    lo, hi = s.quantile(trim), s.quantile(1 - trim)
    s = s[(s >= lo) & (s <= hi)]
    if len(s) < min_countries:
        return None
    best_area, best_val = s.idxmin(), s.min()
    worst_area, worst_val = s.idxmax(), s.max()
    p10, p90 = s.quantile(0.10), s.quantile(0.90)
    return {
        "commodity": commodity,
        "year": year,
        "best_country": best_area, "best_intensity": round(best_val, 2),
        "worst_country": worst_area, "worst_intensity": round(worst_val, 2),
        "ratio": round(worst_val / best_val, 1),
        "p10": round(p10, 2), "p90": round(p90, 2),
        "robust_ratio": round(p90 / p10, 1) if p10 > 0 else None,
        "median": round(s.median(), 2),
        "n_countries": int(s.nunique()),
    }


# ---------------------------------------------------------------------------
# Non-overlapping candidate shares (fixes parent+child double-counting).
# ---------------------------------------------------------------------------

# Leaf-level items that sum WITHOUT overlap, grouped into candidate footprints.
# Using leaves avoids counting e.g. "Emissions from livestock" AND its child
# "Enteric Fermentation" twice.
CANDIDATE_LEAVES = {
    "Supply chain": [
        "Food Household Consumption", "Food Retail", "Food Processing",
        "Food Transport", "Food Packaging", "Fertilizers Manufacturing",
        "Waste disposal", "Food systems waste disposal",
    ],
    "Livestock": [
        "Enteric Fermentation", "Manure Management",
        "Manure left on Pasture", "Manure applied to Soils",
    ],
    "Rice": ["Rice Cultivation"],
    "Land-use change": [
        "Net Forest conversion", "Drained organic soils (CO2)",
        "Drained organic soils (N2O)", "Savanna fires", "Forest fires",
        "Fires in organic soils", "Fires in humid tropical forests",
    ],
    "Crops (other)": [
        "Synthetic Fertilizers", "Crop Residues",
        "Burning - Crop residues",
    ],
    "On-farm energy": ["On-farm energy use"],
}


def candidate_shares(df_countries, year, element, candidates=None):
    """Non-overlapping emissions share per candidate footprint (leaves only).

    Returns a DataFrame with absolute value, % of the summed leaves, and which
    leaf items were actually found. Each emission is counted once.
    """
    import pandas as pd
    candidates = candidates or CANDIDATE_LEAVES
    yr = df_countries[(df_countries["Year"] == year)
                      & (df_countries["Element"] == element)]
    present = set(yr["Item"].unique())
    rows = []
    for label, leaves in candidates.items():
        found = [i for i in leaves if i in present]
        val = yr[yr["Item"].isin(found)]["Value"].sum()
        rows.append({"candidate": label, "value": val,
                     "items_found": found})
    out = pd.DataFrame(rows)
    tot = out["value"].sum()
    out["pct_of_leaves"] = (100 * out["value"] / tot).round(1) if tot else 0
    return out.sort_values("value", ascending=False).reset_index(drop=True)


# ---------------------------------------------------------------------------
# Land use & planet-health helpers (notebook 06).
# ---------------------------------------------------------------------------

def land_area_by_item(landuse_countries, year, top=15):
    """Total land area by land-use Item for one year (1000 ha), ranked.

    Restricts to non-overlapping top-level categories so nested items (forest
    sub-types, organic/tillage splits) don't double-count against their parents.
    """
    yr = landuse_countries[landuse_countries["Year"] == year]
    return yr.groupby("Item")["Value"].sum().sort_values(ascending=False)


# Non-overlapping top-level land categories for an honest composition chart.
TOPLEVEL_LAND_ITEMS = [
    "Agricultural land", "Forest land", "Cropland", "Arable land",
    "Permanent meadows and pastures", "Land area", "Country area",
    "Inland waters",
]


def land_composition(landuse_countries, year, items=None):
    """Land area for a fixed set of non-overlapping categories (1000 ha)."""
    items = items or TOPLEVEL_LAND_ITEMS
    yr = landuse_countries[(landuse_countries["Year"] == year)
                           & (landuse_countries["Item"].isin(items))]
    return yr.groupby("Item")["Value"].sum().sort_values(ascending=False)


def nutrient_metric(nutrient_countries, year, element, item="Nutrient balance"):
    """Per-country cropland nutrient value for a given element + item.

    Planet-health uses: element='Cropland nitrogen', item='Nutrient balance'
    for surplus; element='Cropland nitrogen use efficiency' for efficiency.
    """
    df = nutrient_countries[(nutrient_countries["Year"] == year)
                            & (nutrient_countries["Element"] == element)
                            & (nutrient_countries["Item"] == item)]
    if df.empty:
        return None
    return df.groupby("Area")["Value"].sum().sort_values(ascending=False)


def forest_trend(landuse_countries, forest_item="Forest land", min_coverage=0.8):
    """Global forest-land area over time, restricted to well-covered years.

    Early FAOSTAT years are barely reported, so summing them understates the
    total and produces fake growth. We keep only years where country coverage
    is >= min_coverage of the peak, giving an honest trend.
    """
    sub = landuse_countries[landuse_countries["Item"] == forest_item]
    if sub.empty:
        return None, None
    cov = sub.groupby("Year")["Area"].nunique()
    good_years = cov[cov >= min_coverage * cov.max()].index
    sub = sub[sub["Year"].isin(good_years)]
    ft = sub.groupby("Year")["Value"].sum()
    return ft, forest_item


def forest_change_by_country(landuse_countries, year_from, year_to,
                             forest_item="Forest land"):
    """Change in forest land per country between two years (1000 ha).

    Negative = forest loss. Only countries reporting in BOTH years are compared.
    Pick year_from from the well-covered range (see forest_trend), not 1961.
    """
    sub = landuse_countries[landuse_countries["Item"] == forest_item]
    if sub.empty:
        return None, None
    a = sub[sub["Year"] == year_from].groupby("Area")["Value"].sum()
    b = sub[sub["Year"] == year_to].groupby("Area")["Value"].sum()
    change = (b - a).dropna().sort_values()
    return change, forest_item


def nutrient_surplus(nutrient_countries, year, element_contains="nitrogen",
                     surplus_item_contains="surplus"):
    """Cropland nutrient surplus per country (planet-health: over-fertilization).

    Falls back to listing available items/elements if the expected ones aren't
    found, so the notebook can guide refinement.
    """
    df = nutrient_countries[nutrient_countries["Year"] == year]
    if "Element" in df.columns:
        df = df[df["Element"].str.contains(element_contains, case=False, na=False)]
    sur = df[df["Item"].str.contains(surplus_item_contains, case=False, na=False)]
    if sur.empty:
        return None
    return sur.groupby("Area")["Value"].sum().sort_values(ascending=False)
