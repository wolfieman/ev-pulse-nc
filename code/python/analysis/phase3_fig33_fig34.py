#!/usr/bin/env python3
"""
Phase 3: Theil Decomposition Visualizations (Figures 33-34).

Generates two publication-ready figures illustrating the Theil index
decomposition of EV charging infrastructure inequality:

    fig-33  Theil Decomposition — Between vs Within County
    fig-34  County Contributions to Within-County Inequality

Input CSVs are produced by phase3_theil_decomposition.py and must exist
before running this script.

Output: 600 DPI, PDF + PNG dual export via save_figure().

Author: BIDA 670 EV-Pulse-NC Project
Date: 2026
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
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

_THEIL_DECOMP_CSV = _DATA_DIR / "phase3-theil-decomposition.csv"
_THEIL_COUNTY_CSV = _DATA_DIR / "phase3-theil-county-contributions.csv"
_COUNTY_GINI_CSV = _DATA_DIR / "phase3-county-gini.csv"

# Colors for decomposition segments
COLOR_BETWEEN = COLORS["ARIMA"]  # blue
COLOR_WITHIN = COLORS["highlight"]  # orange


# =============================================================================
# DATA LOADING
# =============================================================================


def _load_theil_decomposition() -> pd.DataFrame | None:
    """Load the Theil decomposition summary CSV.

    Returns:
        DataFrame with columns: component, theil_t, theil_l,
        pct_of_total_t, pct_of_total_l.  Returns None if file missing.
    """
    if not _THEIL_DECOMP_CSV.exists():
        print(
            f"[ERROR] File not found: {_THEIL_DECOMP_CSV}\n"
            "        Run phase3_theil_decomposition.py first to generate "
            "the Theil decomposition results."
        )
        return None
    return pd.read_csv(_THEIL_DECOMP_CSV)


def _load_county_contributions() -> pd.DataFrame | None:
    """Load the per-county Theil within-county contributions CSV.

    Returns:
        DataFrame with columns: county_name, county_fips, population,
        weighted_mean_ports_per_10k, theil_t_within,
        contribution_to_total_within, zip_count.
        Returns None if file missing.
    """
    if not _THEIL_COUNTY_CSV.exists():
        print(
            f"[ERROR] File not found: {_THEIL_COUNTY_CSV}\n"
            "        Run phase3_theil_decomposition.py first to generate "
            "the county contribution results."
        )
        return None
    return pd.read_csv(_THEIL_COUNTY_CSV)


def _load_county_gini() -> pd.DataFrame | None:
    """Load the county Gini CSV for cross-referencing (optional).

    Returns:
        DataFrame or None if the file does not exist.
    """
    if not _COUNTY_GINI_CSV.exists():
        return None
    return pd.read_csv(_COUNTY_GINI_CSV)


# =============================================================================
# FIGURE 33: Theil Decomposition — Between vs Within County
# =============================================================================


def generate_fig33(decomp: pd.DataFrame) -> None:
    """Stacked horizontal bar showing between vs within Theil-T shares."""
    print("[INFO] Generating fig-33: Theil Decomposition — Between vs Within County")

    # Extract values
    total_row = decomp[decomp["component"] == "total"].iloc[0]
    between_row = decomp[decomp["component"] == "between"].iloc[0]
    within_row = decomp[decomp["component"] == "within"].iloc[0]

    t_total = total_row["theil_t"]
    t_between = between_row["theil_t"]
    t_within = within_row["theil_t"]
    pct_between = between_row["pct_of_total_t"]
    pct_within = within_row["pct_of_total_t"]

    fig, ax = plt.subplots(figsize=(7.0, 4.0))

    # Single stacked horizontal bar
    bar_height = 0.5
    y_pos = 0

    # Between segment (left)
    ax.barh(
        y_pos,
        t_between,
        height=bar_height,
        color=COLOR_BETWEEN,
        edgecolor="white",
        linewidth=1.0,
        label="Between Counties",
        zorder=3,
    )

    # Within segment (right, stacked)
    ax.barh(
        y_pos,
        t_within,
        left=t_between,
        height=bar_height,
        color=COLOR_WITHIN,
        edgecolor="white",
        linewidth=1.0,
        label="Within Counties",
        zorder=3,
    )

    # Label each segment with absolute value and percentage
    ax.text(
        t_between / 2,
        y_pos,
        f"{t_between:.4f}\n({pct_between:.1f}%)",
        ha="center",
        va="center",
        fontsize=FONT_SIZES["annotation"],
        fontweight="bold",
        color="white",
        zorder=4,
    )
    ax.text(
        t_between + t_within / 2,
        y_pos,
        f"{t_within:.4f}\n({pct_within:.1f}%)",
        ha="center",
        va="center",
        fontsize=FONT_SIZES["annotation"],
        fontweight="bold",
        color="white",
        zorder=4,
    )

    # Total annotation above the bar
    ax.text(
        t_total / 2,
        y_pos + bar_height / 2 + 0.08,
        f"Total Theil-T = {t_total:.4f}",
        ha="center",
        va="bottom",
        fontsize=FONT_SIZES["subtitle"],
        fontweight="bold",
        color=COLORS["gray_dark"],
    )

    # Key finding annotation
    dominant_component = "within" if pct_within > 50 else "between"
    dominant_pct = max(pct_within, pct_between)

    if dominant_component == "within":
        finding_text = f"{dominant_pct:.1f}% of inequality is within counties"
        policy_text = "Sub-county targeting recommended\nfor NEVI deployment"
    else:
        finding_text = f"{dominant_pct:.1f}% of inequality is between counties"
        policy_text = "County-level targeting recommended\nfor NEVI deployment"

    ax.annotate(
        finding_text,
        xy=(t_total * 0.5, y_pos - bar_height / 2 - 0.05),
        fontsize=FONT_SIZES["subtitle"],
        fontweight="bold",
        ha="center",
        va="top",
        color=COLORS["gray_dark"],
    )

    # Policy interpretation text box
    ax.annotate(
        policy_text,
        xy=(0.98, 0.05),
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

    # Subtitle for decomposition method
    ax.text(
        0.5,
        1.02,
        "Theil-T Index Decomposition (GE(1))",
        transform=ax.transAxes,
        fontsize=FONT_SIZES["annotation"],
        ha="center",
        va="bottom",
        color=COLORS["gray_medium"],
        style="italic",
    )

    # Axis formatting
    ax.set_xlim(0, t_total * 1.05)
    ax.set_ylim(-0.5, 0.6)
    ax.set_yticks([])
    ax.set_xlabel("Theil-T Index Value", fontsize=FONT_SIZES["axis_label"])
    ax.set_title(
        "Infrastructure Inequality Decomposition \u2014 Between vs. Within Counties",
        fontsize=FONT_SIZES["title"],
        fontweight="bold",
    )
    ax.legend(
        fontsize=FONT_SIZES["legend"],
        loc="upper right",
        framealpha=0.95,
    )

    save_figure(fig, "fig-33-theil-decomposition", _OUTPUT_DIR)
    plt.close(fig)
    print("[SUCCESS] fig-33-theil-decomposition saved")


# =============================================================================
# FIGURE 34: County Contributions to Within-County Inequality
# =============================================================================


def generate_fig34(
    contributions: pd.DataFrame,
    county_gini: pd.DataFrame | None,
) -> None:
    """Horizontal bar chart of county contributions to within-county Theil."""
    print("[INFO] Generating fig-34: County Contributions to Within-County Inequality")

    # Sort by contribution descending (largest first at top of chart)
    df = contributions.sort_values(
        "contribution_to_total_within", ascending=True
    ).copy()

    fig, ax = plt.subplots(figsize=(7.0, 5.0))

    y_pos = range(len(df))
    values = df["contribution_to_total_within"].values

    # Compute percentage of within-county total
    total_within = values.sum()
    pct_values = (values / total_within * 100) if total_within > 0 else values

    # Color gradient from sequential palette (darker = larger contribution)
    n_counties = len(df)
    cmap = plt.cm.get_cmap("YlOrRd", n_counties + 2)
    bar_colors = [cmap(i + 2) for i in range(n_counties)]

    bars = ax.barh(
        y_pos,
        values,
        color=bar_colors,
        edgecolor="white",
        linewidth=0.5,
        zorder=3,
    )

    # Add percentage labels on each bar
    for i, (bar, pct) in enumerate(zip(bars, pct_values)):
        width = bar.get_width()
        label_x = width + max(values) * 0.01
        ax.text(
            label_x,
            bar.get_y() + bar.get_height() / 2,
            f"{pct:.1f}%",
            ha="left",
            va="center",
            fontsize=FONT_SIZES["annotation"],
            color=COLORS["gray_dark"],
        )

    # Annotate top contributors with Gini values if available
    if county_gini is not None and "gini_weighted" in county_gini.columns:
        # Get the top 3 counties (last 3 in ascending-sorted df)
        top_counties = df.tail(3)
        for _, row in top_counties.iterrows():
            county_name = row["county_name"]
            gini_row = county_gini[county_gini["county_name"] == county_name]
            if gini_row.empty:
                continue
            gini_val = gini_row["gini_weighted"].iloc[0]
            idx = df.index.get_loc(row.name)
            bar_width = values[idx]
            ax.annotate(
                f"Gini = {gini_val:.3f}",
                xy=(bar_width, idx),
                xytext=(max(values) * 0.15, 0),
                textcoords="offset points",
                fontsize=FONT_SIZES["annotation"],
                color=COLORS["gray_dark"],
                va="center",
                ha="left",
                arrowprops=dict(
                    arrowstyle="-|>",
                    color=COLORS["gray_medium"],
                    lw=0.6,
                ),
                bbox=dict(
                    boxstyle="round,pad=0.2",
                    facecolor="#FFFDE7",
                    edgecolor=COLORS["gray_light"],
                    alpha=0.9,
                ),
            )

    ax.set_yticks(list(y_pos))
    ax.set_yticklabels(df["county_name"].values, fontsize=FONT_SIZES["tick_label"])
    ax.set_xlabel(
        "Contribution to Within-County Theil-T",
        fontsize=FONT_SIZES["axis_label"],
    )
    ax.set_title(
        "County Contributions to Within-County Infrastructure Inequality",
        fontsize=FONT_SIZES["title"],
        fontweight="bold",
    )

    # Provide right-side padding for percentage labels
    ax.set_xlim(0, max(values) * 1.20)

    save_figure(fig, "fig-34-theil-county-contributions", _OUTPUT_DIR)
    plt.close(fig)
    print("[SUCCESS] fig-34-theil-county-contributions saved")


# =============================================================================
# MAIN
# =============================================================================


def main() -> None:
    """Generate Theil decomposition figures (fig-33 and fig-34)."""
    setup_publication_style()

    # Load required data
    decomp = _load_theil_decomposition()
    contributions = _load_county_contributions()

    if decomp is None or contributions is None:
        print(
            "[ERROR] Cannot generate figures. Please run "
            "phase3_theil_decomposition.py first."
        )
        sys.exit(1)

    # Load optional Gini data for cross-referencing in fig-34
    county_gini = _load_county_gini()
    if county_gini is not None:
        print("[INFO] County Gini data loaded for cross-referencing")
    else:
        print("[INFO] County Gini data not found; skipping Gini annotations")

    generate_fig33(decomp)
    generate_fig34(contributions, county_gini)

    print("[SUCCESS] Both figures (fig-33 and fig-34) generated.")


if __name__ == "__main__":
    main()
