#!/usr/bin/env python3
"""
fig-43: NEVI Priority Score Bar Chart with Pillar Contribution Decomposition.

Horizontal stacked bar chart visualizing the NEVI Priority Score rankings for
the top 10 NC counties. Each county's total score is decomposed into its three
weighted pillar contributions (0.40 x Equity, 0.35 x Utilization, 0.25 x
Cost-Effectiveness), making the three archetype patterns immediately legible:

    Union        - utilization-driven (dominant Utilization component)
    Mecklenburg  - equity-driven (balanced Equity + Cost-Effectiveness)
    Orange       - low across all pillars

Design specifications (per manuscript advisory panel, 2026-05-15):
    - Horizontal stacked bar (not vertical, not grouped)
    - Stack order: Equity (left), Utilization (middle), Cost-Effectiveness (right)
    - Sorted by total NEVI score descending
    - Okabe-Ito colorblind-safe palette (deuteranopia, protanopia, tritanopia)
    - Total NEVI score annotated at right end of each bar (3 decimal places)
    - Archetype callouts on Union, Mecklenburg, Orange (italic, gray)
    - 600 DPI, PDF + PNG dual export via save_figure()

Input:  data/processed/scoring-framework-final.csv
Output: output/figures/fig-43-nevi-priority-scores.{png,pdf}

Usage:
    uv run code/python/analysis/phase5_fig43_scoring_barchart.py

Author: Wolfgang Sanyer
License: Polyform Noncommercial 1.0.0 (see LICENSE)
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
_PROJECT_ROOT = _SCRIPT_DIR.parent.parent.parent
_DATA_DIR = _PROJECT_ROOT / "data" / "processed"
_OUTPUT_DIR = _PROJECT_ROOT / "output" / "figures"

sys.path.insert(0, str(_SCRIPT_DIR))

from publication_style import (  # noqa: E402
    COLORS,
    FONT_SIZES,
    save_figure,
    setup_publication_style,
)

# =============================================================================
# CONSTANTS
# =============================================================================

# Input
FINAL_CSV = _DATA_DIR / "scoring-framework-final.csv"

# Output
FIG_NAME = "fig-43-nevi-priority-scores"

# Pillar weights (per NEVI scoring framework, Section 2.3 of manuscript)
WEIGHT_EQUITY = 0.40
WEIGHT_UTILIZATION = 0.35
WEIGHT_COST_EFFECTIVENESS = 0.25

# Okabe-Ito colorblind-safe palette (per Pereira panel recommendation)
# Distinguishable for deuteranopia, protanopia, and tritanopia
# Survives grayscale print as three distinct lightness levels
OKABE_ITO = {
    "equity": "#0072B2",              # Blue
    "utilization": "#E69F00",         # Orange
    "cost_effectiveness": "#009E73",  # Green
}

# Archetype annotations (per panel + PAPER-NOTES three-archetypes framing)
ARCHETYPES = {
    "Union": "utilization-driven",
    "Mecklenburg": "equity-driven",
    "Orange": "low across pillars",
}

# Figure dimensions (inches)
FIG_WIDTH = 8.0
FIG_HEIGHT = 5.5


# =============================================================================
# DATA LOADING
# =============================================================================


def load_scoring_data() -> pd.DataFrame:
    """Load scoring framework CSV; compute weighted pillar contributions.

    Returns:
        DataFrame sorted by NEVI score descending, with weighted pillar
        contributions (equity_contribution, util_contribution,
        cost_contribution) that sum to nevi_priority_score.

    Raises:
        FileNotFoundError: If the scoring CSV is missing.
        ValueError: If weighted contributions do not match the stored
            NEVI scores within numerical tolerance (1e-9), indicating
            either a CSV corruption or a mismatch between this script's
            weights and the scoring framework's.
    """
    if not FINAL_CSV.exists():
        raise FileNotFoundError(f"Scoring CSV not found: {FINAL_CSV}")

    df = pd.read_csv(FINAL_CSV)

    # Compute weighted contributions (these sum to nevi_priority_score)
    df["equity_contribution"] = WEIGHT_EQUITY * df["equity_score"]
    df["util_contribution"] = WEIGHT_UTILIZATION * df["util_score"]
    df["cost_contribution"] = WEIGHT_COST_EFFECTIVENESS * df["cost_score"]

    # Verify decomposition matches stored NEVI score within tolerance
    df["recomputed_nevi"] = (
        df["equity_contribution"]
        + df["util_contribution"]
        + df["cost_contribution"]
    )
    max_diff = (df["recomputed_nevi"] - df["nevi_priority_score"]).abs().max()
    if max_diff > 1e-9:
        raise ValueError(
            f"Weighted contributions do not sum to NEVI score "
            f"(max diff = {max_diff:.2e}). Check scoring CSV or weights."
        )

    # Sort by total NEVI score descending
    df = df.sort_values("nevi_priority_score", ascending=False).reset_index(
        drop=True
    )
    return df


# =============================================================================
# FIGURE GENERATION
# =============================================================================


def create_fig43(df: pd.DataFrame) -> plt.Figure:
    """Create the horizontal stacked bar chart for NEVI Priority Scores."""

    fig, ax = plt.subplots(figsize=(FIG_WIDTH, FIG_HEIGHT))

    # Reverse for top-down display (highest score at top of plot)
    df_plot = df.iloc[::-1].reset_index(drop=True)
    counties = df_plot["county_name"].tolist()
    y_positions = list(range(len(counties)))

    # Stacked bars: Equity (left), Utilization (middle), Cost-Eff (right)
    ax.barh(
        y_positions,
        df_plot["equity_contribution"],
        color=OKABE_ITO["equity"],
        label=f"Equity (weight = {WEIGHT_EQUITY:.2f})",
        edgecolor="white",
        linewidth=0.5,
    )
    ax.barh(
        y_positions,
        df_plot["util_contribution"],
        left=df_plot["equity_contribution"],
        color=OKABE_ITO["utilization"],
        label=f"Utilization (weight = {WEIGHT_UTILIZATION:.2f})",
        edgecolor="white",
        linewidth=0.5,
    )
    ax.barh(
        y_positions,
        df_plot["cost_contribution"],
        left=df_plot["equity_contribution"] + df_plot["util_contribution"],
        color=OKABE_ITO["cost_effectiveness"],
        label=f"Cost-Effectiveness (weight = {WEIGHT_COST_EFFECTIVENESS:.2f})",
        edgecolor="white",
        linewidth=0.5,
    )

    # Annotate total NEVI score at right end of each bar
    for i in y_positions:
        total = df_plot.loc[i, "nevi_priority_score"]
        ax.text(
            total + 0.010,
            i,
            f"{total:.3f}",
            va="center",
            ha="left",
            fontsize=FONT_SIZES["annotation"],
            color=COLORS["gray_dark"],
            fontweight="bold",
        )

    # Archetype callouts (italic, gray, positioned right of the score)
    for county, label in ARCHETYPES.items():
        if county not in counties:
            continue
        idx = counties.index(county)
        total = df_plot.loc[idx, "nevi_priority_score"]
        ax.annotate(
            label,
            xy=(total + 0.075, idx),
            va="center",
            ha="left",
            fontsize=FONT_SIZES["annotation"],
            fontstyle="italic",
            color=COLORS["gray_medium"],
        )

    # Y-axis: county names with rank prefix
    rank_labels = [
        f"{len(counties) - i}. {county}" for i, county in enumerate(counties)
    ]
    ax.set_yticks(y_positions)
    ax.set_yticklabels(rank_labels)

    # X-axis: leave room for score annotation + archetype callout
    max_nevi = df["nevi_priority_score"].max()
    ax.set_xlabel("NEVI Priority Score (pillar contributions)")
    ax.set_xlim(0, max_nevi * 1.50)

    # Title (left-aligned)
    ax.set_title(
        "NEVI Priority Score by County:\nPillar Contribution Decomposition",
        loc="left",
    )

    # Legend below the plot
    ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, -0.10),
        ncol=3,
        frameon=False,
    )

    # Grid: x only (vertical reference lines), no y grid
    ax.grid(axis="y", visible=False)
    ax.grid(axis="x", visible=True)

    # Note: constrained_layout is set in publication_style rcparams; do not
    # call tight_layout() — it conflicts and emits a UserWarning.
    return fig


# =============================================================================
# MAIN
# =============================================================================


def main() -> None:
    """Generate fig-43 and write PNG + PDF to output/figures/."""
    setup_publication_style()

    df = load_scoring_data()
    print(f"Loaded {len(df)} counties from {FINAL_CSV.name}")
    print(
        "Top-3: "
        + ", ".join(
            f"{row['county_name']} ({row['nevi_priority_score']:.3f})"
            for _, row in df.head(3).iterrows()
        )
    )

    fig = create_fig43(df)
    saved = save_figure(fig, FIG_NAME, _OUTPUT_DIR)
    print(f"Saved figure to {len(saved)} file(s):")
    for path in saved:
        print(f"  {path}")
    plt.close(fig)


if __name__ == "__main__":
    main()
