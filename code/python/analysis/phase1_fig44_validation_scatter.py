#!/usr/bin/env python3
"""
fig-44: Forecast Validation Actual-vs-Predicted Scatter.

Scatter plot of actual versus predicted BEV registration counts across the
400-observation out-of-sample holdout (100 NC counties x 4 months,
July through October 2025). Each point is colored by the SAS Model Studio
auto-selected model family (ESM / ARIMA / UCM). The 45-degree identity line
(perfect prediction) anchors the visual; points above the line indicate
underprediction (the model's forecast was lower than the actual).

Design rationale (per Pereira panel recommendation):
    §6.1 reports MAPE 4.34%, underprediction 69.00%, mean bias +18.22,
    CI coverage 75.50% raw / 93.75% bias-corrected, and Chow F = 1,268.35
    -- a wall of numbers. This figure makes the systematic underprediction
    pattern visible in one glance. The 69% underprediction shows as points
    clustered above the identity line.

Design specifications:
    - Log-log scale (BEV counts span orders of magnitude: ~4 in Hyde,
      ~28,000 in Wake)
    - Points colored by model type (publication_style ESM/ARIMA/UCM palette)
    - 45-degree identity line as reference
    - Mecklenburg October 2025 highlighted (largest outlier: actual exceeded
      forecast by 975 vehicles in a single month)
    - Headline metrics annotated in an inset text block
    - 600 DPI, PDF + PNG dual export

Input:  output/validation/sas-validation-comparison.csv
Output: output/figures/fig-44-validation-scatter.{png,pdf}

Usage:
    uv run code/python/analysis/phase1_fig44_validation_scatter.py

Author: Wolfgang Sanyer
License: Polyform Noncommercial 1.0.0 (see LICENSE)
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
_PROJECT_ROOT = _SCRIPT_DIR.parent.parent.parent
_VALIDATION_DIR = _PROJECT_ROOT / "output" / "validation"
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
VALIDATION_CSV = _VALIDATION_DIR / "sas-validation-comparison.csv"

# Output
FIG_NAME = "fig-44-validation-scatter"

# Headline metrics (from validation; embedded for the inset annotation)
MAPE_PCT = 4.34
UNDERPREDICTION_PCT = 69.00
MEAN_BIAS = 18.22
CI_COVERAGE_RAW_PCT = 75.50
CI_COVERAGE_CORRECTED_PCT = 93.75
CHOW_F = 1268.35

# Highlighted observation
HIGHLIGHT_COUNTY = "Mecklenburg"
HIGHLIGHT_MONTH = "Oct 2025"

# Figure dimensions (inches)
FIG_WIDTH = 7.5
FIG_HEIGHT = 6.0

# Model color mapping (uses publication_style palette)
MODEL_COLORS = {
    "ESM": COLORS["ESM"],
    "ARIMA": COLORS["ARIMA"],
    "UCM": COLORS["UCM"],
}


# =============================================================================
# DATA LOADING
# =============================================================================


def load_validation_data() -> pd.DataFrame:
    """Load the 400-observation validation comparison CSV.

    Returns:
        DataFrame with columns Predicted, Actual, ModelType, County,
        MonthDate, etc. (validation file schema).

    Raises:
        FileNotFoundError: If the validation CSV is missing.
    """
    if not VALIDATION_CSV.exists():
        raise FileNotFoundError(f"Validation CSV not found: {VALIDATION_CSV}")
    df = pd.read_csv(VALIDATION_CSV)
    # Filter to rows with positive Predicted and Actual (log scale requirement)
    df = df[(df["Predicted"] > 0) & (df["Actual"] > 0)].copy()
    return df


def find_highlight_point(df: pd.DataFrame) -> tuple[float, float, float]:
    """Locate the Mecklenburg October 2025 point and return (predicted,
    actual, error)."""
    mask = (df["County"] == HIGHLIGHT_COUNTY) & (df["MonthDate"] == HIGHLIGHT_MONTH)
    rows = df[mask]
    if rows.empty:
        raise ValueError(
            f"Could not find {HIGHLIGHT_COUNTY} {HIGHLIGHT_MONTH} in validation data"
        )
    row = rows.iloc[0]
    return float(row["Predicted"]), float(row["Actual"]), float(row["Error"])


# =============================================================================
# FIGURE GENERATION
# =============================================================================


def create_fig44(df: pd.DataFrame) -> plt.Figure:
    """Generate the actual-vs-predicted scatter with identity line + annotations."""

    fig, ax = plt.subplots(figsize=(FIG_WIDTH, FIG_HEIGHT))

    # Scatter by model type (so each appears in legend independently)
    for model in ("ESM", "ARIMA", "UCM"):
        sub = df[df["ModelType"] == model]
        ax.scatter(
            sub["Predicted"],
            sub["Actual"],
            s=18,
            c=MODEL_COLORS[model],
            label=f"{model} (n={len(sub)})",
            alpha=0.65,
            edgecolors="white",
            linewidths=0.4,
        )

    # 45-degree identity line (perfect prediction). Compute extent from data.
    lo = float(np.min([df["Predicted"].min(), df["Actual"].min()])) * 0.8
    hi = float(np.max([df["Predicted"].max(), df["Actual"].max()])) * 1.2
    identity_xs = np.array([lo, hi])
    ax.plot(
        identity_xs,
        identity_xs,
        color=COLORS["reference"],
        linestyle="--",
        linewidth=1.2,
        label="Identity (Actual = Predicted)",
        zorder=2,
    )

    # Highlight Mecklenburg Oct 2025 outlier
    h_pred, h_actual, h_error = find_highlight_point(df)
    ax.scatter(
        h_pred,
        h_actual,
        s=120,
        facecolor="none",
        edgecolor=COLORS["negative"],
        linewidth=2.0,
        zorder=4,
    )
    ax.annotate(
        f"{HIGHLIGHT_COUNTY} {HIGHLIGHT_MONTH}\n+{int(round(h_error))} vehicles",
        xy=(h_pred, h_actual),
        xytext=(h_pred * 0.35, h_actual * 1.6),
        fontsize=FONT_SIZES["annotation"],
        color=COLORS["negative"],
        arrowprops=dict(
            arrowstyle="->",
            color=COLORS["negative"],
            lw=0.8,
        ),
        ha="center",
    )

    # Log-log scale (counts span ~4 to ~28,000)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(lo, hi)
    ax.set_ylim(lo, hi)

    # Axes
    ax.set_xlabel("Predicted BEV count (log scale)")
    ax.set_ylabel("Actual BEV count (log scale)")
    ax.set_title(
        "Forecast Validation: Actual vs Predicted BEV Counts\n"
        "n = 400 county-month observations, four-month out-of-sample holdout (Jul-Oct 2025)",
        loc="left",
    )

    # Headline metrics inset (lower-right corner of plot area)
    metrics_text = (
        f"MAPE: {MAPE_PCT:.2f}%\n"
        f"Underprediction rate: {UNDERPREDICTION_PCT:.2f}%\n"
        f"Mean bias: +{MEAN_BIAS:.2f} vehicles\n"
        f"CI coverage (raw / bias-corrected): {CI_COVERAGE_RAW_PCT:.2f}% / {CI_COVERAGE_CORRECTED_PCT:.2f}%\n"
        f"Chow F (IRA Aug 2022 break): {CHOW_F:,.2f} (p < 1e-6)"
    )
    ax.text(
        0.97,
        0.03,
        metrics_text,
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        fontsize=FONT_SIZES["annotation"],
        color=COLORS["gray_dark"],
        bbox=dict(
            boxstyle="round,pad=0.4",
            facecolor="white",
            edgecolor=COLORS["gray_light"],
            linewidth=0.6,
            alpha=0.95,
        ),
    )

    # Legend (upper-left)
    ax.legend(loc="upper left", frameon=True, fontsize=FONT_SIZES["legend"])

    # Grid: subtle log grid on both axes
    ax.grid(visible=True, which="major", alpha=0.4)
    ax.grid(visible=True, which="minor", alpha=0.15)

    # Note: constrained_layout is set in publication_style rcparams;
    # do not call tight_layout() — it conflicts with constrained_layout.
    return fig


# =============================================================================
# MAIN
# =============================================================================


def main() -> None:
    """Generate fig-44 and write PNG + PDF to output/figures/."""
    setup_publication_style()

    df = load_validation_data()
    print(f"Loaded {len(df)} validation observations from {VALIDATION_CSV.name}")
    n_underpred = int((df["Actual"] > df["Predicted"]).sum())
    print(
        f"Underprediction rate (recomputed): {n_underpred / len(df) * 100:.2f}% "
        f"({n_underpred} / {len(df)})"
    )
    h_pred, h_actual, h_error = find_highlight_point(df)
    print(
        f"Highlight point: {HIGHLIGHT_COUNTY} {HIGHLIGHT_MONTH}: "
        f"Predicted={h_pred:.1f}, Actual={h_actual:.0f}, Error=+{h_error:.0f}"
    )

    fig = create_fig44(df)
    saved = save_figure(fig, FIG_NAME, _OUTPUT_DIR)
    print(f"Saved figure to {len(saved)} file(s):")
    for path in saved:
        print(f"  {path}")
    plt.close(fig)


if __name__ == "__main__":
    main()
