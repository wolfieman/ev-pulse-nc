#!/usr/bin/env python3
"""
Phase 3: Equity and Inequality Visualizations (Figures 26-29).

Generates four publication-ready figures exploring EV charging
infrastructure equity across North Carolina's ten study counties:

    fig-26  Population vs Port Density Scatter
    fig-27  Lorenz Curve — Port Distribution Inequality
    fig-28  County Gini Coefficient Comparison (Lollipop)
    fig-29  Top-20 Underserved ZIPs Dot Plot

Output: 600 DPI, PDF + PNG dual export via save_figure().

Author: BIDA 670 EV-Pulse-NC Project
Date: 2026
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Resolve project paths and import publication style
# ---------------------------------------------------------------------------
_SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPT_DIR))

from publication_style import (  # noqa: E402
    COLORS,
    FONT_SIZES,
    save_figure,
    setup_publication_style,
)

# =============================================================================
# MODULE-LEVEL CONSTANTS
# =============================================================================

_PROJECT_ROOT = _SCRIPT_DIR.parent.parent.parent
_DATA_DIR = _PROJECT_ROOT / "data" / "processed"
_OUTPUT_DIR = _PROJECT_ROOT / "output" / "figures"

STATEWIDE_MEDIAN_PORTS_PER_10K = 5.51
STATEWIDE_GINI_WEIGHTED = 0.566

# Ten distinct colors for the ten study counties, sourced from
# publication_style COLORS plus colorblind-safe supplements.
COUNTY_COLORS = {
    "Buncombe": COLORS["ESM"],  # green
    "Cabarrus": COLORS["ARIMA"],  # blue
    "Durham": COLORS["UCM"],  # purple
    "Forsyth": COLORS["highlight"],  # orange
    "Guilford": COLORS["negative"],  # red
    "Mecklenburg": COLORS["reference"],  # dark slate
    "New Hanover": "#17becf",  # teal / cyan
    "Orange": "#bcbd22",  # olive / yellow-green
    "Union": "#e377c2",  # pink
    "Wake": "#8c564b",  # brown
}

# Lorenz curve counties and their Gini values
LORENZ_GINI = {
    "Statewide": 0.566,
    "Wake": 0.496,
    "Guilford": 0.571,
    "Mecklenburg": 0.623,
}


# =============================================================================
# HELPER: Lorenz curve computation
# =============================================================================


def _compute_lorenz(
    population: np.ndarray,
    ports: np.ndarray,
    density: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Return (cum_pop_share, cum_ports_share) sorted by density ascending.

    Args:
        population: Array of ZIP populations.
        ports: Array of total ports per ZIP.
        density: Array of ports_per_10k (used for sorting).

    Returns:
        Tuple of cumulative population share and cumulative ports share
        arrays, each starting from (0, 0).
    """
    order = np.argsort(density)
    sorted_pop = population[order]
    sorted_ports = ports[order]

    cum_pop = np.cumsum(sorted_pop) / sorted_pop.sum()
    cum_ports = np.cumsum(sorted_ports) / sorted_ports.sum()

    # Prepend origin
    cum_pop = np.insert(cum_pop, 0, 0.0)
    cum_ports = np.insert(cum_ports, 0, 0.0)
    return cum_pop, cum_ports


# =============================================================================
# FIGURE 26: Population vs Port Density Scatter
# =============================================================================


def generate_fig26(df: pd.DataFrame) -> None:
    """Scatter plot of ZIP population vs charging port density by county."""
    print("[INFO] Generating fig-26: Population vs Port Density Scatter")

    # Drop rows without valid density
    plot_df = df.dropna(subset=["ports_per_10k", "population"]).copy()
    plot_df = plot_df[plot_df["population"] > 0]

    fig, ax = plt.subplots(figsize=(7.0, 4.5))

    for county, color in COUNTY_COLORS.items():
        subset = plot_df[plot_df["county_name"] == county]
        if subset.empty:
            continue
        ax.scatter(
            subset["population"],
            subset["ports_per_10k"],
            c=color,
            label=county,
            alpha=0.75,
            s=50,
            edgecolors="white",
            linewidths=0.5,
            zorder=3,
        )

    # Reference line at statewide median
    ax.axhline(
        y=STATEWIDE_MEDIAN_PORTS_PER_10K,
        color=COLORS["gray_dark"],
        linestyle="--",
        linewidth=1.2,
        zorder=2,
    )
    ax.annotate(
        f"Statewide Median ({STATEWIDE_MEDIAN_PORTS_PER_10K})",
        xy=(ax.get_xlim()[1] * 0.98, STATEWIDE_MEDIAN_PORTS_PER_10K),
        xytext=(0, 6),
        textcoords="offset points",
        fontsize=FONT_SIZES["annotation"],
        color=COLORS["gray_dark"],
        ha="right",
        va="bottom",
    )

    ax.set_xlabel("ZIP Code Population", fontsize=FONT_SIZES["axis_label"])
    ax.set_ylabel("Ports per 10,000 Population", fontsize=FONT_SIZES["axis_label"])
    ax.set_title(
        "ZIP Population vs. Charging Port Density",
        fontsize=FONT_SIZES["title"],
        fontweight="bold",
    )
    ax.legend(
        fontsize=FONT_SIZES["legend"],
        loc="upper right",
        ncol=2,
        framealpha=0.95,
    )

    save_figure(fig, "fig-26-population-vs-density", _OUTPUT_DIR)
    plt.close(fig)
    print("[SUCCESS] fig-26-population-vs-density saved")


# =============================================================================
# FIGURE 27: Lorenz Curve — Port Distribution Inequality
# =============================================================================


def generate_fig27(df: pd.DataFrame) -> None:
    """Lorenz curve showing port distribution inequality."""
    print("[INFO] Generating fig-27: Lorenz Curve")

    # Filter to rankable ZIPs (population > 0, density not NaN)
    plot_df = df.dropna(subset=["ports_per_10k", "population"]).copy()
    plot_df = plot_df[plot_df["population"] > 0]

    fig, ax = plt.subplots(figsize=(7.0, 6.0))

    # Line of equality
    ax.plot(
        [0, 1],
        [0, 1],
        color=COLORS["gray_medium"],
        linestyle="--",
        linewidth=1.2,
        label="Line of Equality",
        zorder=2,
    )

    # Statewide Lorenz curve
    pop_all = plot_df["population"].values
    ports_all = plot_df["total_ports"].values
    density_all = plot_df["ports_per_10k"].values

    cum_pop_sw, cum_ports_sw = _compute_lorenz(pop_all, ports_all, density_all)
    ax.plot(
        cum_pop_sw,
        cum_ports_sw,
        color=COLORS["reference"],
        linewidth=2.0,
        label=f"Statewide (Gini={LORENZ_GINI['Statewide']:.3f})",
        zorder=4,
    )

    # Shading between equality line and statewide curve
    ax.fill_between(
        cum_pop_sw,
        cum_pop_sw,  # equality line y = x
        cum_ports_sw,
        color=COLORS["reference"],
        alpha=0.2,
        zorder=1,
    )

    # Overlay individual county curves
    county_styles = {
        "Wake": {
            "color": COUNTY_COLORS["Wake"],
            "gini": LORENZ_GINI["Wake"],
        },
        "Guilford": {
            "color": COUNTY_COLORS["Guilford"],
            "gini": LORENZ_GINI["Guilford"],
        },
        "Mecklenburg": {
            "color": COUNTY_COLORS["Mecklenburg"],
            "gini": LORENZ_GINI["Mecklenburg"],
        },
    }

    for county, style in county_styles.items():
        subset = plot_df[plot_df["county_name"] == county]
        if subset.empty:
            continue
        cpop, cports = _compute_lorenz(
            subset["population"].values,
            subset["total_ports"].values,
            subset["ports_per_10k"].values,
        )
        ax.plot(
            cpop,
            cports,
            color=style["color"],
            linewidth=1.5,
            linestyle="-",
            label=f"{county} ({style['gini']:.3f})",
            zorder=3,
        )

    ax.set_xlabel("Cumulative Share of Population", fontsize=FONT_SIZES["axis_label"])
    ax.set_ylabel("Cumulative Share of Ports", fontsize=FONT_SIZES["axis_label"])
    ax.set_title(
        "Lorenz Curve \u2014 EV Charging Port Distribution",
        fontsize=FONT_SIZES["title"],
        fontweight="bold",
    )
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal", adjustable="box")
    ax.legend(
        fontsize=FONT_SIZES["legend"],
        loc="upper left",
        framealpha=0.95,
    )

    save_figure(fig, "fig-27-lorenz-curve", _OUTPUT_DIR)
    plt.close(fig)
    print("[SUCCESS] fig-27-lorenz-curve saved")


# =============================================================================
# FIGURE 28: County Gini Coefficient Comparison (Lollipop)
# =============================================================================


def generate_fig28(
    county_gini: pd.DataFrame,
    statewide_gini: pd.DataFrame,
) -> None:
    """Horizontal lollipop chart of county Gini coefficients."""
    print("[INFO] Generating fig-28: County Gini Comparison")

    # Sort by weighted Gini descending
    cg = county_gini.sort_values("gini_weighted", ascending=True).copy()

    sw_gini = statewide_gini["gini_weighted"].iloc[0]

    fig, ax = plt.subplots(figsize=(7.0, 5.0))

    y_pos = np.arange(len(cg))

    # Stems from weighted to unweighted
    for i, (_, row) in enumerate(cg.iterrows()):
        ax.plot(
            [row["gini_weighted"], row["gini_unweighted"]],
            [y_pos[i], y_pos[i]],
            color=COLORS["gray_light"],
            linewidth=1.5,
            zorder=1,
        )

    # Weighted dots (filled)
    ax.scatter(
        cg["gini_weighted"],
        y_pos,
        color=COLORS["ARIMA"],
        s=80,
        zorder=3,
        label="Population-Weighted",
        edgecolors="white",
        linewidths=0.5,
    )

    # Unweighted dots (open)
    ax.scatter(
        cg["gini_unweighted"],
        y_pos,
        facecolors="none",
        edgecolors=COLORS["UCM"],
        s=80,
        linewidths=1.5,
        zorder=3,
        label="Unweighted",
    )

    # Statewide reference line
    ax.axvline(
        x=sw_gini,
        color=COLORS["negative"],
        linestyle="--",
        linewidth=1.2,
        label=f"Statewide Gini ({sw_gini:.3f})",
        zorder=2,
    )

    # Durham divergence annotation
    durham_row = cg[cg["county_name"] == "Durham"]
    if not durham_row.empty:
        dur_idx = cg.index.get_loc(durham_row.index[0])
        dur_w = durham_row["gini_weighted"].iloc[0]
        dur_u = durham_row["gini_unweighted"].iloc[0]
        ax.annotate(
            f"Durham divergence\nWeighted {dur_w:.2f} vs Unweighted {dur_u:.2f}",
            xy=((dur_w + dur_u) / 2, y_pos[dur_idx]),
            xytext=(0.62, y_pos[dur_idx] + 1.5),
            fontsize=FONT_SIZES["annotation"],
            color=COLORS["gray_dark"],
            ha="center",
            arrowprops=dict(
                arrowstyle="-|>",
                color=COLORS["gray_medium"],
                lw=0.8,
            ),
            bbox=dict(
                boxstyle="round,pad=0.3",
                facecolor="#FFFDE7",
                edgecolor=COLORS["gray_light"],
                alpha=0.9,
            ),
        )

    ax.set_yticks(y_pos)
    ax.set_yticklabels(cg["county_name"], fontsize=FONT_SIZES["tick_label"])
    ax.set_xlabel("Gini Coefficient", fontsize=FONT_SIZES["axis_label"])
    ax.set_title(
        "Infrastructure Inequality by County \u2014 Gini Coefficients",
        fontsize=FONT_SIZES["title"],
        fontweight="bold",
    )
    ax.legend(
        fontsize=FONT_SIZES["legend"],
        loc="lower right",
        framealpha=0.95,
    )

    save_figure(fig, "fig-28-gini-comparison", _OUTPUT_DIR)
    plt.close(fig)
    print("[SUCCESS] fig-28-gini-comparison saved")


# =============================================================================
# FIGURE 29: Top-20 Underserved ZIPs Dot Plot
# =============================================================================


def generate_fig29(top20: pd.DataFrame) -> None:
    """Horizontal dot plot of the 20 most underserved ZIP codes."""
    print("[INFO] Generating fig-29: Top 20 Underserved ZIPs")

    # Sort by ports_per_10k ascending (worst first = bottom of plot)
    t20 = top20.sort_values("ports_per_10k", ascending=True).copy()

    fig, ax = plt.subplots(figsize=(7.0, 7.0))

    y_pos = np.arange(len(t20))

    # Labels: "ZIP (City)"
    labels = [f"{int(row['zip'])} ({row['city']})" for _, row in t20.iterrows()]

    # Color: red if dc_fast == 0, blue otherwise
    dot_colors = [
        COLORS["negative"] if row["dc_fast_ports"] == 0 else COLORS["ARIMA"]
        for _, row in t20.iterrows()
    ]

    # Size proportional to population (scale for readability)
    pop_vals = t20["population"].values
    size_min, size_max = 40, 300
    pop_min, pop_max = pop_vals.min(), pop_vals.max()
    if pop_max > pop_min:
        sizes = size_min + (pop_vals - pop_min) / (pop_max - pop_min) * (
            size_max - size_min
        )
    else:
        sizes = np.full_like(pop_vals, (size_min + size_max) / 2)

    # Stems
    for i in range(len(t20)):
        ax.plot(
            [0, t20["ports_per_10k"].iloc[i]],
            [y_pos[i], y_pos[i]],
            color=COLORS["gray_light"],
            linewidth=1.2,
            zorder=1,
        )

    # Dots
    ax.scatter(
        t20["ports_per_10k"].values,
        y_pos,
        c=dot_colors,
        s=sizes,
        edgecolors="white",
        linewidths=0.5,
        zorder=3,
    )

    # Statewide median reference
    ax.axvline(
        x=STATEWIDE_MEDIAN_PORTS_PER_10K,
        color=COLORS["gray_dark"],
        linestyle="--",
        linewidth=1.2,
        zorder=2,
    )
    ax.annotate(
        f"Statewide Median ({STATEWIDE_MEDIAN_PORTS_PER_10K})",
        xy=(STATEWIDE_MEDIAN_PORTS_PER_10K, len(t20) - 0.5),
        xytext=(4, 0),
        textcoords="offset points",
        fontsize=FONT_SIZES["annotation"],
        color=COLORS["gray_dark"],
        ha="left",
        va="top",
    )

    # Summary annotations
    total_pop = int(t20["population"].sum())
    total_ports = int(t20["total_ports"].sum())
    dc_fast_zero_count = int((t20["dc_fast_ports"] == 0).sum())

    ax.annotate(
        f"{total_pop:,} people served by {total_ports} ports",
        xy=(0.97, 0.08),
        xycoords="axes fraction",
        fontsize=FONT_SIZES["annotation"],
        ha="right",
        va="bottom",
        bbox=dict(
            boxstyle="round,pad=0.4",
            facecolor="#FFFDE7",
            edgecolor=COLORS["gray_light"],
            alpha=0.9,
        ),
    )
    ax.annotate(
        f"{dc_fast_zero_count} of 20 have zero DC fast chargers",
        xy=(0.97, 0.03),
        xycoords="axes fraction",
        fontsize=FONT_SIZES["annotation"],
        ha="right",
        va="bottom",
        color=COLORS["negative"],
    )

    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, fontsize=FONT_SIZES["tick_label"])
    ax.set_xlabel("Ports per 10,000 Population", fontsize=FONT_SIZES["axis_label"])
    ax.set_title(
        "Top 20 Underserved ZIP Codes by Charging Port Density",
        fontsize=FONT_SIZES["title"],
        fontweight="bold",
    )

    # Legend for dot color meaning
    from matplotlib.lines import Line2D

    legend_elements = [
        Line2D(
            [0],
            [0],
            marker="o",
            color="w",
            markerfacecolor=COLORS["negative"],
            markersize=8,
            label="No DC fast chargers",
        ),
        Line2D(
            [0],
            [0],
            marker="o",
            color="w",
            markerfacecolor=COLORS["ARIMA"],
            markersize=8,
            label="Has DC fast chargers",
        ),
    ]
    ax.legend(
        handles=legend_elements,
        fontsize=FONT_SIZES["legend"],
        loc="lower right",
        framealpha=0.95,
    )

    save_figure(fig, "fig-29-top20-underserved", _OUTPUT_DIR)
    plt.close(fig)
    print("[SUCCESS] fig-29-top20-underserved saved")


# =============================================================================
# MAIN
# =============================================================================


def main() -> None:
    """Generate all four equity/inequality figures."""
    setup_publication_style()

    # Load data
    zip_density = pd.read_csv(_DATA_DIR / "phase3-zip-density.csv")
    county_gini = pd.read_csv(_DATA_DIR / "phase3-county-gini.csv")
    statewide_gini = pd.read_csv(_DATA_DIR / "phase3-statewide-gini.csv")
    top20 = pd.read_csv(_DATA_DIR / "phase3-top20-underserved.csv")

    generate_fig26(zip_density)
    generate_fig27(zip_density)
    generate_fig28(county_gini, statewide_gini)
    generate_fig29(top20)

    print("[SUCCESS] All four figures (fig-26 through fig-29) generated.")


if __name__ == "__main__":
    main()
