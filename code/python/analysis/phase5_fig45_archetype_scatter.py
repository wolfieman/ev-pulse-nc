#!/usr/bin/env python3
"""
fig-45: Equity-Utilization Archetype Scatter for the Top 10 NEVI Counties.

Two-dimensional bubble scatter visualizing each county's position in the
(Equity x Utilization) pillar space, with bubble size proportional to the
composite NEVI Priority Score. Four quadrants visually identify the three
named archetypes that organize the Discussion section:

    Top-left  (low equity, high utilization)  Utilization-driven   - Union
    Bottom-right (high equity, low utilization) Equity-driven      - Mecklenburg, Guilford
    Bottom-left (low equity, low utilization) Low across pillars   - Orange
    Top-right (high equity, high utilization) Dual-driver          - (empty in this cohort)

Design rationale (per Pereira panel recommendation):
    The three-archetype framing in PAPER-NOTES L542-550 organizes the entire
    Discussion section. fig-43 (bar chart) shows the *ranking*; fig-45 (this
    scatter) shows the *typology*. A reader who sees only fig-45 should be
    able to reconstruct the policy implication: different counties need
    investment for different reasons.

Design specifications:
    - X-axis: Equity pillar score (0 to 1, min-max normalized)
    - Y-axis: Utilization pillar score (0 to 1, min-max normalized)
    - Bubble size: NEVI Priority Score (composite)
    - 4 quadrant background shadings with archetype labels at corners
    - Union, Mecklenburg, Orange highlighted with thicker borders in Okabe-Ito
      colors matching fig-43 (orange = utilization, blue = equity, gray = low)
    - All 10 counties labeled with name next to bubble
    - Quadrant dividing lines at Equity = 0.5 and Utilization = 0.5
    - 600 DPI, PDF + PNG dual export

Input:  data/processed/scoring-framework-final.csv
Output: output/figures/fig-45-equity-utilization-archetypes.{png,pdf}

Usage:
    uv run code/python/analysis/phase5_fig45_archetype_scatter.py

Author: Wolfgang Sanyer
License: Polyform Noncommercial 1.0.0 (see LICENSE)
Date: 2026
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.patches as mpatches
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
FIG_NAME = "fig-45-equity-utilization-archetypes"

# Quadrant dividers (clean 0.5 midpoints on the normalized scale)
EQUITY_DIVIDER = 0.5
UTIL_DIVIDER = 0.5

# Archetype colors (Okabe-Ito, matching fig-43)
ARCHETYPE_COLORS = {
    "utilization": "#E69F00",         # Orange (Union)
    "equity": "#0072B2",              # Blue (Mecklenburg, Guilford)
    "low": COLORS["gray_medium"],     # Gray (Orange, low across pillars)
    "default": "#56B4E9",             # Light blue for other counties
}

# Highlighted counties (matching fig-43)
HIGHLIGHTS = {
    "Union": "utilization",
    "Mecklenburg": "equity",
    "Orange": "low",
}

# Quadrant label text and position (in axes coordinates)
QUADRANT_LABELS = {
    "top_left": {
        "text": "Utilization-driven",
        "pos": (0.05, 0.95),
        "color": ARCHETYPE_COLORS["utilization"],
    },
    "top_right": {
        "text": "Dual-driver\n(none in cohort)",
        "pos": (0.95, 0.95),
        "color": COLORS["gray_medium"],
    },
    "bottom_right": {
        "text": "Equity-driven",
        "pos": (0.95, 0.05),
        "color": ARCHETYPE_COLORS["equity"],
    },
    "bottom_left": {
        "text": "Low across pillars",
        "pos": (0.05, 0.05),
        "color": ARCHETYPE_COLORS["low"],
    },
}

# Quadrant background tints (very subtle)
QUADRANT_TINTS = {
    "top_left": "#FFF4E0",        # Faint orange
    "top_right": "#F4F4F4",       # Faint gray
    "bottom_right": "#E6F0F8",    # Faint blue
    "bottom_left": "#F4F4F4",     # Faint gray
}

# Bubble size scaling (matplotlib scatter `s` is in points^2)
BUBBLE_SIZE_MIN = 80
BUBBLE_SIZE_MAX = 1200

# Figure dimensions (inches)
FIG_WIDTH = 8.0
FIG_HEIGHT = 7.0


# =============================================================================
# DATA LOADING
# =============================================================================


def load_scoring_data() -> pd.DataFrame:
    """Load the scoring framework CSV.

    Returns:
        DataFrame with at minimum the columns county_name, equity_score,
        util_score, and nevi_priority_score.

    Raises:
        FileNotFoundError: If the scoring CSV is missing.
    """
    if not FINAL_CSV.exists():
        raise FileNotFoundError(f"Scoring CSV not found: {FINAL_CSV}")
    df = pd.read_csv(FINAL_CSV)
    return df


def scale_bubble_sizes(nevi_scores: pd.Series) -> pd.Series:
    """Linearly scale NEVI scores to bubble sizes (points^2)."""
    lo, hi = nevi_scores.min(), nevi_scores.max()
    return BUBBLE_SIZE_MIN + (nevi_scores - lo) / (hi - lo) * (
        BUBBLE_SIZE_MAX - BUBBLE_SIZE_MIN
    )


# =============================================================================
# FIGURE GENERATION
# =============================================================================


def create_fig45(df: pd.DataFrame) -> plt.Figure:
    """Build the equity-utilization archetype scatter."""

    fig, ax = plt.subplots(figsize=(FIG_WIDTH, FIG_HEIGHT))

    # Axis limits — fixed to the [0, 1] normalized score range with margin
    ax.set_xlim(-0.04, 1.02)
    ax.set_ylim(-0.04, 1.05)

    # Quadrant background shading
    ax.axvspan(-0.04, EQUITY_DIVIDER, ymin=0, ymax=UTIL_DIVIDER / 1.09,
               facecolor=QUADRANT_TINTS["bottom_left"], zorder=0)
    ax.axvspan(EQUITY_DIVIDER, 1.02, ymin=0, ymax=UTIL_DIVIDER / 1.09,
               facecolor=QUADRANT_TINTS["bottom_right"], zorder=0)
    ax.axvspan(-0.04, EQUITY_DIVIDER, ymin=UTIL_DIVIDER / 1.09, ymax=1,
               facecolor=QUADRANT_TINTS["top_left"], zorder=0)
    ax.axvspan(EQUITY_DIVIDER, 1.02, ymin=UTIL_DIVIDER / 1.09, ymax=1,
               facecolor=QUADRANT_TINTS["top_right"], zorder=0)

    # Quadrant dividing lines (subtle gray)
    ax.axvline(EQUITY_DIVIDER, color=COLORS["gray_medium"], linestyle=":",
               linewidth=0.8, alpha=0.6, zorder=1)
    ax.axhline(UTIL_DIVIDER, color=COLORS["gray_medium"], linestyle=":",
               linewidth=0.8, alpha=0.6, zorder=1)

    # Bubble sizes from NEVI score
    df = df.copy()
    df["bubble_size"] = scale_bubble_sizes(df["nevi_priority_score"])

    # Plot bubbles — highlighted counties first (so labels overlay cleanly)
    for _, row in df.iterrows():
        county = row["county_name"]
        is_highlight = county in HIGHLIGHTS
        if is_highlight:
            face = ARCHETYPE_COLORS[HIGHLIGHTS[county]]
            edge = ARCHETYPE_COLORS[HIGHLIGHTS[county]]
            linewidth = 2.0
            alpha = 0.75
        else:
            face = ARCHETYPE_COLORS["default"]
            edge = COLORS["gray_dark"]
            linewidth = 0.8
            alpha = 0.55

        ax.scatter(
            row["equity_score"],
            row["util_score"],
            s=row["bubble_size"],
            facecolor=face,
            edgecolor=edge,
            linewidth=linewidth,
            alpha=alpha,
            zorder=3,
        )

    # County name labels positioned to avoid bubble overlap and inter-label
    # collision. Mecklenburg and Guilford bubbles overlap in the
    # bottom-right; place Mecklenburg's label well to the left and
    # Guilford's well above to separate them.
    label_offsets = {
        # county_name: (dx, dy) in data coords, ha, va
        "Union": (0.00, -0.07, "center", "top"),
        "Mecklenburg": (-0.09, 0.00, "right", "center"),
        "Guilford": (0.00, 0.10, "center", "bottom"),
        "New Hanover": (-0.09, 0.00, "right", "center"),
        "Wake": (0.04, 0.00, "left", "center"),
        "Durham": (0.04, -0.02, "left", "top"),
        "Forsyth": (0.04, 0.00, "left", "center"),
        "Cabarrus": (0.04, 0.00, "left", "center"),
        "Buncombe": (0.04, -0.02, "left", "top"),
        "Orange": (0.03, 0.02, "left", "bottom"),
    }
    for _, row in df.iterrows():
        county = row["county_name"]
        offset = label_offsets.get(county, (0.02, 0.02, "left", "bottom"))
        dx, dy, ha, va = offset
        ax.text(
            row["equity_score"] + dx,
            row["util_score"] + dy,
            county,
            fontsize=FONT_SIZES["annotation"],
            color=COLORS["gray_dark"],
            ha=ha,
            va=va,
            zorder=4,
        )

    # Quadrant labels at corners
    for q in QUADRANT_LABELS.values():
        ax.text(
            q["pos"][0],
            q["pos"][1],
            q["text"],
            transform=ax.transAxes,
            fontsize=FONT_SIZES["annotation"],
            fontweight="bold",
            color=q["color"],
            alpha=0.75,
            ha="left" if q["pos"][0] < 0.5 else "right",
            va="top" if q["pos"][1] > 0.5 else "bottom",
            zorder=2,
        )

    # Axes labels and title
    ax.set_xlabel("Equity pillar score (min-max normalized)")
    ax.set_ylabel("Utilization pillar score (min-max normalized)")
    ax.set_title(
        "County Archetypes in the Equity-Utilization Pillar Space\n"
        "Bubble size proportional to composite NEVI Priority Score",
        loc="left",
    )

    # Bubble-size legend (3 reference sizes)
    legend_sizes = [0.10, 0.30, 0.56]  # NEVI scores spanning observed range
    legend_handles = []
    for nevi in legend_sizes:
        # Scale using the same formula as the actual bubbles
        lo, hi = df["nevi_priority_score"].min(), df["nevi_priority_score"].max()
        s = BUBBLE_SIZE_MIN + (nevi - lo) / (hi - lo) * (
            BUBBLE_SIZE_MAX - BUBBLE_SIZE_MIN
        )
        # Clamp to non-negative
        s = max(s, BUBBLE_SIZE_MIN)
        legend_handles.append(
            plt.scatter(
                [], [],
                s=s,
                facecolor=ARCHETYPE_COLORS["default"],
                edgecolor=COLORS["gray_dark"],
                linewidth=0.8,
                alpha=0.55,
                label=f"NEVI = {nevi:.2f}",
            )
        )
    ax.legend(
        handles=legend_handles,
        loc="lower right",
        title="Composite NEVI Score",
        title_fontsize=FONT_SIZES["legend"],
        fontsize=FONT_SIZES["annotation"],
        labelspacing=1.2,
        borderpad=0.8,
        frameon=True,
        framealpha=0.95,
    )

    # Grid (subtle, axes only)
    ax.grid(visible=True, alpha=0.3, zorder=0)

    # Note: constrained_layout is set in publication_style rcparams;
    # do NOT call tight_layout() — it conflicts and emits a UserWarning.
    return fig


# =============================================================================
# MAIN
# =============================================================================


def main() -> None:
    """Generate fig-45 and write PNG + PDF to output/figures/."""
    setup_publication_style()

    df = load_scoring_data()
    print(f"Loaded {len(df)} counties from {FINAL_CSV.name}")
    print(
        "NEVI score range: "
        f"{df['nevi_priority_score'].min():.3f} to "
        f"{df['nevi_priority_score'].max():.3f}"
    )
    # Quadrant breakdown
    for _, row in df.iterrows():
        equity_side = "high" if row["equity_score"] >= EQUITY_DIVIDER else "low"
        util_side = "high" if row["util_score"] >= UTIL_DIVIDER else "low"
        print(
            f"  {row['county_name']:<14} "
            f"equity={row['equity_score']:.3f} ({equity_side}) | "
            f"util={row['util_score']:.3f} ({util_side}) | "
            f"NEVI={row['nevi_priority_score']:.3f}"
        )

    fig = create_fig45(df)
    saved = save_figure(fig, FIG_NAME, _OUTPUT_DIR)
    print(f"Saved figure to {len(saved)} file(s):")
    for path in saved:
        print(f"  {path}")
    plt.close(fig)


if __name__ == "__main__":
    main()
