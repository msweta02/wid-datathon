"""
Trade-adjacent production metrics — computed from PRODUCTION data alone (QCL/QI),
no trade flows required.

The idea: production data already encodes supply-chain risk.
- If world output of a crop sits in a few countries, global supply is fragile
  (the production-side analogue of "supplier concentration").
- If a region's per-capita production falls, it must increasingly rely on imports
  (a self-sufficiency proxy, without needing trade data).
- Removing the top producer of a concentrated crop simulates a supply shock.

All functions take LONG frames after src.clean.standardize_columns
(columns: area, area_code, item, element, year, value, ...).
"""
from __future__ import annotations

import numpy as np
import pandas as pd


# ------------------------------------------------------------ concentration (HHI etc.)
def production_shares(countries: pd.DataFrame, item: str, year: int,
                      element: str = "Production") -> pd.Series:
    """Each country's share (fraction) of world production of `item` in `year`."""
    sub = countries[(countries["item"] == item)
                    & (countries["element"].str.contains(element, na=False))
                    & (countries["year"] == year)]
    by_country = sub.groupby("area")["value"].sum()
    total = by_country.sum()
    if total <= 0:
        return pd.Series(dtype=float)
    return (by_country / total).sort_values(ascending=False)


def top_n_share(countries: pd.DataFrame, item: str, year: int, n: int = 3,
                element: str = "Production") -> float:
    """Combined share of the top-n producing countries (fraction in [0,1])."""
    shares = production_shares(countries, item, year, element)
    return float(shares.head(n).sum()) if len(shares) else np.nan


def hhi(countries: pd.DataFrame, item: str, year: int,
        element: str = "Production") -> float:
    """
    Herfindahl-Hirschman Index of production concentration (0–10000 scale).
    Sum of squared percentage shares. >2500 is 'highly concentrated' (antitrust rule
    of thumb) — here a proxy for global supply fragility.
    """
    shares = production_shares(countries, item, year, element)
    if not len(shares):
        return np.nan
    return float(((shares * 100) ** 2).sum())


def concentration_table(countries: pd.DataFrame, items: list[str], year: int,
                        n: int = 3) -> pd.DataFrame:
    """Concentration summary for several crops: top-n share, HHI, #1 country."""
    rows = []
    for it in items:
        shares = production_shares(countries, it, year)
        if not len(shares):
            continue
        rows.append({
            "item": it,
            "top1_country": shares.index[0],
            "top1_share": round(float(shares.iloc[0]), 3),
            f"top{n}_share": round(float(shares.head(n).sum()), 3),
            "hhi": round(hhi(countries, it, year), 0),
            "n_producers": int((shares > 0).sum()),
        })
    return pd.DataFrame(rows).sort_values("hhi", ascending=False)


# ------------------------------------------------------------ supply-shock simulation
def supply_shock(countries: pd.DataFrame, item: str, year: int, drop_top: int = 1,
                 element: str = "Production") -> dict:
    """
    Simulate losing the top `drop_top` producer(s): how much of world supply vanishes?
    Pure production-side analogue of a trade supply shock.
    """
    shares = production_shares(countries, item, year, element)
    if not len(shares):
        return {}
    lost = float(shares.head(drop_top).sum())
    return {
        "item": item,
        "year": year,
        "dropped": list(shares.head(drop_top).index),
        "world_supply_lost_pct": round(lost * 100, 1),
        "remaining_top_producer": shares.index[drop_top] if len(shares) > drop_top else None,
    }


# ------------------------------------------------------------ self-sufficiency proxy
def per_capita_trend(qi_aggregates: pd.DataFrame, region: str,
                     element_kw: str = "capita") -> pd.Series:
    """
    Per-capita production index trajectory for a region (from QI aggregates).
    Falling = the region increasingly cannot feed itself from its own output →
    rising structural import need. A self-sufficiency proxy without trade data.
    """
    sub = qi_aggregates[(qi_aggregates["area"] == region)
                        & (qi_aggregates["element"].str.contains(element_kw,
                                                                 case=False, na=False))]
    return sub.groupby("year")["value"].mean().sort_index()


def self_sufficiency_change(qi_aggregates: pd.DataFrame, regions: list[str],
                            span: int = 10, element_kw: str = "capita") -> pd.DataFrame:
    """
    Change in per-capita production index over the last `span` years, per region.
    Negative = losing self-sufficiency (import need rising).
    """
    rows = []
    for r in regions:
        s = per_capita_trend(qi_aggregates, r, element_kw)
        if len(s) < 2:
            continue
        latest = int(s.index.max())
        if (latest - span) in s.index:
            change = s.loc[latest] - s.loc[latest - span]
        else:
            change = s.iloc[-1] - s.iloc[0]
        rows.append({"region": r, "latest_index": round(float(s.loc[latest]), 1),
                     f"change_{span}y": round(float(change), 1)})
    return pd.DataFrame(rows).sort_values(f"change_{span}y")


# ------------------------------------------------------------ combined risk view
def combined_risk_table(countries: pd.DataFrame, items: list[str], year: int,
                        n: int = 3) -> pd.DataFrame:
    """
    Per-crop trade-adjacent risk: concentration (supply fragility) plus the size of
    the shock if the #1 producer is lost. One row per crop, ready to rank.
    """
    conc = concentration_table(countries, items, year, n=n)
    shocks = [supply_shock(countries, it, year, drop_top=1) for it in conc["item"]]
    shock_pct = {s["item"]: s["world_supply_lost_pct"] for s in shocks if s}
    conc["shock_if_top1_lost_pct"] = conc["item"].map(shock_pct)
    return conc
