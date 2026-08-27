"""Plotting helpers. All functions take an optional ax and return it."""

import matplotlib.pyplot as plt


def _style():
    plt.rcParams["figure.figsize"] = (10, 5)
    plt.rcParams["axes.grid"] = True
    plt.rcParams["grid.alpha"] = 0.3
    plt.rcParams["axes.spines.top"] = False
    plt.rcParams["axes.spines.right"] = False


def barh_ranking(series, title, xlabel, n=12, color="seagreen", ax=None):
    """Horizontal bar chart of the top-n of a ranked Series."""
    _style()
    if ax is None:
        _, ax = plt.subplots()
    series.head(n)[::-1].plot.barh(color=color, ax=ax)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    plt.tight_layout()
    return ax


def line_trends(df_wide, title, ylabel, ax=None):
    """Line plot of a Year-indexed wide DataFrame (one line per column)."""
    _style()
    if ax is None:
        _, ax = plt.subplots()
    df_wide.plot(ax=ax)
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.legend(bbox_to_anchor=(1.02, 1), loc="upper left")
    plt.tight_layout()
    return ax


def lever_quadrant(q, commodity, ax=None):
    """Scatter of country volume (log) vs intensity, labelling the top-right."""
    _style()
    if ax is None:
        _, ax = plt.subplots()
    ax.scatter(q["volume"], q["intensity"], alpha=0.6)
    vmed, imed = q["volume"].median(), q["intensity"].median()
    ax.axhline(imed, ls="--", c="grey")
    ax.axvline(vmed, ls="--", c="grey")
    ax.set_xscale("log")
    ax.set_xlabel("Country emission volume (proxy, log)")
    ax.set_ylabel(f"Intensity: {commodity}")
    ax.set_title("Lever quadrant — high volume + high intensity (top-right)")
    for _, r in q.iterrows():
        if r["volume"] > vmed and r["intensity"] > imed:
            ax.annotate(r["Area"], (r["volume"], r["intensity"]), fontsize=8)
    plt.tight_layout()
    return ax
