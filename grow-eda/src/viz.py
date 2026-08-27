"""
Reusable plotting helpers. Keep notebooks thin by calling these.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
FIGDIR = ROOT / "outputs" / "figures"
FIGDIR.mkdir(parents=True, exist_ok=True)

sns.set_theme(style="whitegrid", context="notebook")

# Fixed categorical order (colorblind-checked, adjacent-pair safe). Assign in this
# order, never cycle/reshuffle per chart, so a given slot always means the same rank.
CATEGORICAL_COLORS = [
    "#2a78d6",  # blue
    "#eb6834",  # orange
    "#1baf7a",  # aqua
    "#eda100",  # yellow
    "#e87ba4",  # magenta
    "#008300",  # green
    "#4a3aa7",  # violet
    "#e34948",  # red
]


def save(fig, name: str, dpi: int = 150) -> Path:
    path = FIGDIR / f"{name}.png"
    fig.savefig(path, dpi=dpi, bbox_inches="tight")
    print(f"figure -> {path}")
    return path


def trend_over_time(df: pd.DataFrame, year_col: str, value_col: str,
                    group_col: str | None = None, title: str = "",
                    ylabel: str = "", top_n: int | None = None, ax=None):
    """
    Line plot of a value over years, optionally split by group (e.g. region, crop).
    If top_n is set and group_col given, keep only the top_n groups by final-year value.
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 6))
    else:
        fig = ax.figure

    d = df.copy()
    if group_col and top_n:
        last_year = d[year_col].max()
        top = (
            d[d[year_col] == last_year]
            .groupby(group_col)[value_col].sum()
            .nlargest(top_n).index
        )
        d = d[d[group_col].isin(top)]

    if group_col:
        for key, sub in d.groupby(group_col):
            agg = sub.groupby(year_col)[value_col].sum()
            ax.plot(agg.index, agg.values, label=str(key), linewidth=1.8)
        ax.legend(bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=8)
    else:
        agg = d.groupby(year_col)[value_col].sum()
        ax.plot(agg.index, agg.values, linewidth=2)

    ax.set_title(title or f"{value_col} over time")
    ax.set_xlabel("Year")
    ax.set_ylabel(ylabel or value_col)
    return fig, ax


def trend_top_bottom(df: pd.DataFrame, year_col: str, value_col: str, group_col: str,
                     n: int = 5, title: str = "", ylabel: str = ""):
    """
    Small multiples for a group_col with too many members to put on one axes:
    top-n and bottom-n groups by final-year value, each in its own panel.
    Keeps a "which regions/countries lead vs lag" chart readable instead of a
    spaghetti plot of every group.
    """
    d = df.copy()
    last_year = d[year_col].max()
    last_vals = d[d[year_col] == last_year].groupby(group_col)[value_col].sum()
    top = last_vals.nlargest(n).index
    bottom = last_vals.nsmallest(n).index

    fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharey=True)
    for ax, keys, subtitle in zip(axes, [top, bottom], [f"Top {n}", f"Bottom {n}"]):
        sub = d[d[group_col].isin(keys)]
        for color, (key, grp) in zip(CATEGORICAL_COLORS, sub.groupby(group_col)):
            agg = grp.groupby(year_col)[value_col].sum()
            ax.plot(agg.index, agg.values, label=str(key), linewidth=2, color=color)
        ax.set_title(subtitle, fontsize=11)
        ax.set_xlabel("Year")
        ax.legend(fontsize=8, loc="best", frameon=False)

    axes[0].set_ylabel(ylabel or value_col)
    fig.suptitle(title or f"{value_col} by {group_col} — top {n} vs bottom {n}")
    fig.tight_layout()
    return fig, axes


def missingness_heatmap(df: pd.DataFrame, index_col: str, year_col: str,
                        value_col: str, title: str = "Data coverage", ax=None):
    """
    Heatmap of value presence (index x year). Great for the feasibility notebook —
    shows which countries/crops have sparse coverage.
    """
    pivot = df.pivot_table(index=index_col, columns=year_col,
                           values=value_col, aggfunc="size")
    presence = pivot.notna().astype(int)
    if ax is None:
        fig, ax = plt.subplots(figsize=(14, max(4, len(presence) * 0.25)))
    else:
        fig = ax.figure
    sns.heatmap(presence, cmap="Greens", cbar=False, ax=ax)
    ax.set_title(title)
    return fig, ax


def flag_composition(df: pd.DataFrame, flag_col: str = "flag",
                     year_col: str = "year", title: str = "Flag composition over time", ax=None):
    """Stacked area of flag share by year — shows how much data is estimated/imputed."""
    d = df.copy()
    d[flag_col] = d[flag_col].fillna("")
    share = (
        d.groupby([year_col, flag_col]).size()
        .groupby(level=0).apply(lambda s: s / s.sum())
        .unstack(fill_value=0)
    )
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 5))
    else:
        fig = ax.figure
    share.plot.area(ax=ax, linewidth=0)
    ax.set_title(title)
    ax.set_ylabel("share of records")
    ax.legend(bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=8)
    return fig, ax
