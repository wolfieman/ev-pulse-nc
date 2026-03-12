#!/usr/bin/env python3
"""
Phase 3: Distribution Analysis and Supply-Demand Comparison Figures.

Generates three publication-ready figures for the EV Pulse NC capstone:

    fig-30  Port Density Distribution (Histogram + KDE)
    fig-31  BEV Registrations vs Charging Port Supply by County
    fig-32  Charging Port Composition by County — Level 2 vs DC Fast

Output figures (600 DPI, PDF + PNG) are saved to output/figures/.

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

PROJECT_ROOT = _SCRIPT_DIR.parent.parent.parent

# Input paths
DENSITY_CSV = PROJECT_ROOT / "data" / "processed" / "phase3-zip-density.csv"
SUMMARY_CSV = PROJECT_ROOT / "data" / "processed" / "phase3-zip-density-summary.csv"
TOP10_CSV = PROJECT_ROOT / "data" / "processed" / "phase3-top10-counties.csv"

# Output
OUTPUT_DIR = PROJECT_ROOT / "output" / "figures"

# Export formats
EXPORT_FORMATS = ["png", "pdf"]


# =============================================================================
# FIG-30: Port Density Distribution (Histogram + KDE)
# =============================================================================


def generate_fig30() -> None:
    """Generate histogram + KDE of charging port density across ZIP codes."""
    print("[INFO] Generating fig-30: Port Density Distribution ...")

    df = pd.read_csv(DENSITY_CSV)

    # Filter to rankable ZIPs: non-zero, non-NaN ports_per_10k
    density = df["ports_per_10k"].dropna()
    density = density[density > 0]

    # Compute statistics
    mean_val = density.mean()
    median_val = density.median()
    skewness = float(density.skew())  # pandas Fisher skewness
    min_val = density.min()
    max_val = density.max()
    ratio = max_val / min_val

    # Log-transformed data for binning
    log_density = np.log10(density.values)

    fig, ax = plt.subplots(figsize=(7.0, 4.5))

    # Histogram on log scale — use log-spaced bins
    bins = np.linspace(log_density.min(), log_density.max(), 25)
    counts, _, patches = ax.hist(
        log_density,
        bins=bins,
        color=COLORS["neutral"],
        alpha=0.65,
        edgecolor="white",
        label="Distribution",
        zorder=2,
    )

    # KDE overlay using Gaussian kernel (pure numpy implementation)
    kde_x = np.linspace(log_density.min() - 0.3, log_density.max() + 0.3, 300)
    bw = 1.06 * np.std(log_density) * len(log_density) ** (-1 / 5)  # Silverman
    kde_y = np.zeros_like(kde_x)
    for xi in log_density:
        kde_y += np.exp(-0.5 * ((kde_x - xi) / bw) ** 2)
    kde_y /= len(log_density) * bw * np.sqrt(2 * np.pi)
    # Scale KDE to match histogram height
    bin_width = bins[1] - bins[0]
    kde_y_scaled = kde_y * len(log_density) * bin_width
    ax.plot(
        kde_x,
        kde_y_scaled,
        color=COLORS["highlight"],
        linewidth=2,
        label="KDE",
        zorder=3,
    )

    # Vertical lines for mean and median
    ax.axvline(
        np.log10(mean_val),
        color=COLORS["negative"],
        linestyle="--",
        linewidth=1.5,
        label=f"Mean ({mean_val:.2f})",
        zorder=4,
    )
    ax.axvline(
        np.log10(median_val),
        color=COLORS["positive"],
        linestyle="--",
        linewidth=1.5,
        label=f"Median ({median_val:.2f})",
        zorder=4,
    )

    # Custom x-axis: show actual density values, not log10 values
    tick_values = [0.2, 0.5, 1, 2, 5, 10, 20, 50, 80]
    ax.set_xticks([np.log10(v) for v in tick_values])
    ax.set_xticklabels([str(v) for v in tick_values])

    # Annotations
    ax.annotate(
        f"{ratio:.0f}\u00d7 gap between\nbest and worst ZIP",
        xy=(0.97, 0.95),
        xycoords="axes fraction",
        fontsize=FONT_SIZES["annotation"],
        ha="right",
        va="top",
        bbox=dict(
            boxstyle="round,pad=0.4",
            facecolor="#FFFDE7",
            edgecolor=COLORS["gray_light"],
            alpha=0.9,
        ),
    )
    ax.annotate(
        f"Skewness: {skewness:.2f} (right-skewed)",
        xy=(0.97, 0.78),
        xycoords="axes fraction",
        fontsize=FONT_SIZES["annotation"],
        ha="right",
        va="top",
        bbox=dict(
            boxstyle="round,pad=0.4",
            facecolor="#FFFDE7",
            edgecolor=COLORS["gray_light"],
            alpha=0.9,
        ),
    )

    ax.set_title(
        "Distribution of Charging Port Density Across ZIP Codes",
        fontsize=FONT_SIZES["title"],
        fontweight="bold",
    )
    ax.set_xlabel(
        "Ports per 10,000 Population",
        fontsize=FONT_SIZES["axis_label"],
    )
    ax.set_ylabel("Frequency", fontsize=FONT_SIZES["axis_label"])
    ax.legend(fontsize=FONT_SIZES["legend"], loc="upper left")

    paths = save_figure(
        fig, "fig-30-density-distribution", OUTPUT_DIR, formats=EXPORT_FORMATS
    )
    plt.close(fig)

    for p in paths:
        print(f"[SUCCESS] Saved {p}")


# =============================================================================
# FIG-31: BEV Registrations vs Port Supply by County
# =============================================================================


def generate_fig31() -> None:
    """Generate scatter of BEV registrations vs charging port supply."""
    print("[INFO] Generating fig-31: BEV vs Port Supply ...")

    top10 = pd.read_csv(TOP10_CSV)
    summary = pd.read_csv(SUMMARY_CSV)

    # Merge on county name (top10 uses 'County', summary uses 'county_name')
    merged = top10.merge(
        summary[["county_name", "total_ports"]],
        left_on="County",
        right_on="county_name",
        how="inner",
    )

    bev = merged["BEV"].values
    ports = merged["total_ports"].values
    counties = merged["County"].values

    # Compute average BEV-to-port ratio across all counties
    avg_ratio = bev.sum() / ports.sum()  # BEVs per port

    fig, ax = plt.subplots(figsize=(7.0, 5.5))

    # Reference line: ports = bev / avg_ratio
    x_ref = np.array([0, bev.max() * 1.15])
    y_ref = x_ref / avg_ratio
    ax.plot(
        x_ref,
        y_ref,
        color=COLORS["gray_medium"],
        linestyle="--",
        linewidth=1.2,
        label=f"Average ratio (1 port : {avg_ratio:.0f} BEVs)",
        zorder=1,
    )

    # Classify above/below reference line
    expected_ports = bev / avg_ratio
    oversupplied = ports >= expected_ports
    undersupplied = ~oversupplied

    ax.scatter(
        bev[oversupplied],
        ports[oversupplied],
        color=COLORS["positive"],
        s=90,
        zorder=3,
        edgecolors="white",
        linewidths=0.8,
        label="Above average supply",
    )
    ax.scatter(
        bev[undersupplied],
        ports[undersupplied],
        color=COLORS["negative"],
        s=90,
        zorder=3,
        edgecolors="white",
        linewidths=0.8,
        label="Below average supply",
    )

    # Label each county
    for i, county in enumerate(counties):
        offset_x = 5
        offset_y = 5
        ha = "left"
        # Adjust labels to avoid overlap for dense clusters
        if county == "Mecklenburg":
            offset_y = -12
        elif county == "Durham":
            offset_x = -5
            ha = "right"
        elif county == "Orange":
            offset_y = -12
        ax.annotate(
            county,
            (bev[i], ports[i]),
            textcoords="offset points",
            xytext=(offset_x, offset_y),
            fontsize=FONT_SIZES["annotation"],
            ha=ha,
            va="bottom",
        )

    ax.set_title(
        "EV Registrations vs. Charging Port Supply by County",
        fontsize=FONT_SIZES["title"],
        fontweight="bold",
    )
    ax.set_xlabel(
        "BEV Registrations",
        fontsize=FONT_SIZES["axis_label"],
    )
    ax.set_ylabel(
        "Total Charging Ports",
        fontsize=FONT_SIZES["axis_label"],
    )
    ax.legend(fontsize=FONT_SIZES["legend"], loc="upper left")

    # Start axes at 0
    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)

    paths = save_figure(fig, "fig-31-bev-vs-ports", OUTPUT_DIR, formats=EXPORT_FORMATS)
    plt.close(fig)

    for p in paths:
        print(f"[SUCCESS] Saved {p}")


# =============================================================================
# FIG-32: DC Fast Charger Gap by County
# =============================================================================


def generate_fig32() -> None:
    """Generate grouped horizontal bar chart of L2 vs DC fast ports."""
    print("[INFO] Generating fig-32: DC Fast Charger Gap ...")

    summary = pd.read_csv(SUMMARY_CSV)

    # Sort by total ports descending
    summary = summary.sort_values("total_ports", ascending=True)

    counties = summary["county_name"].values
    l2 = summary["l2_ports"].values
    dc_fast = summary["dc_fast_ports"].values
    y_pos = np.arange(len(counties))
    bar_height = 0.35

    fig, ax = plt.subplots(figsize=(7.0, 5.0))

    ax.barh(
        y_pos + bar_height / 2,
        l2,
        height=bar_height,
        color=COLORS["neutral"],
        edgecolor="white",
        label="Level 2 Ports",
        zorder=2,
    )
    ax.barh(
        y_pos - bar_height / 2,
        dc_fast,
        height=bar_height,
        color=COLORS["highlight"],
        edgecolor="white",
        label="DC Fast Ports",
        zorder=2,
    )

    ax.set_yticks(y_pos)
    ax.set_yticklabels(counties, fontsize=FONT_SIZES["tick_label"])

    ax.set_title(
        "Charging Port Composition by County \u2014 Level 2 vs. DC Fast",
        fontsize=FONT_SIZES["title"],
        fontweight="bold",
    )
    ax.set_xlabel(
        "Number of Ports",
        fontsize=FONT_SIZES["axis_label"],
    )
    ax.legend(fontsize=FONT_SIZES["legend"], loc="lower right")

    # Annotation about underserved ZIPs
    ax.annotate(
        "15 of 20 underserved ZIPs\nhave zero DC fast chargers",
        xy=(0.97, 0.22),
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

    paths = save_figure(fig, "fig-32-dcfast-gap", OUTPUT_DIR, formats=EXPORT_FORMATS)
    plt.close(fig)

    for p in paths:
        print(f"[SUCCESS] Saved {p}")


# =============================================================================
# MAIN
# =============================================================================


def main() -> None:
    """Generate all Phase 3 distribution and supply-demand figures."""
    setup_publication_style()

    generate_fig30()
    generate_fig31()
    generate_fig32()

    print("[INFO] All figures complete.")


if __name__ == "__main__":
    main()
