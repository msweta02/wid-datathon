"""Reusable plotting helpers, trimmed from grow-eda/src/viz.py. Keep notebooks thin."""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
FIGDIR = ROOT / "outputs" / "figures"
FIGDIR.mkdir(parents=True, exist_ok=True)

sns.set_theme(style="whitegrid", context="notebook")

# Fixed categorical order — assign in this order, never cycle/reshuffle per chart.
CATEGORICAL_COLORS = [
    "#2a78d6", "#eb6834", "#1baf7a", "#eda100",
    "#e87ba4", "#008300", "#4a3aa7", "#e34948",
]


def save(fig, name: str, dpi: int = 150) -> Path:
    path = FIGDIR / f"{name}.png"
    fig.savefig(path, dpi=dpi, bbox_inches="tight")
    print(f"figure -> {path}")
    return path


def barh_ranking(series: pd.Series, title: str, xlabel: str, n: int = 12,
                 color: str = "#2a78d6", ax=None):
    """Horizontal bar chart of the top-n of a ranked Series."""
    if ax is None:
        fig, ax = plt.subplots(figsize=(9, 5))
    else:
        fig = ax.figure
    series.head(n)[::-1].plot.barh(color=color, ax=ax)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    fig.tight_layout()
    return fig, ax


def trend_over_time(df: pd.DataFrame, year_col: str, value_col: str,
                    group_col: str | None = None, title: str = "",
                    ylabel: str = "", top_n: int | None = None, ax=None):
    """Line plot of a value over years, optionally split by group (e.g. crop)."""
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
        for color, (key, sub) in zip(CATEGORICAL_COLORS, d.groupby(group_col)):
            agg = sub.groupby(year_col)[value_col].sum()
            ax.plot(agg.index, agg.values, label=str(key), linewidth=1.8, color=color)
        ax.legend(bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=8)
    else:
        agg = d.groupby(year_col)[value_col].sum()
        ax.plot(agg.index, agg.values, linewidth=2)

    ax.set_title(title or f"{value_col} over time")
    ax.set_xlabel("Year")
    ax.set_ylabel(ylabel or value_col)
    fig.tight_layout()
    return fig, ax
