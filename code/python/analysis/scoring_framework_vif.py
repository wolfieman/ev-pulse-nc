#!/usr/bin/env python3
"""
NEVI Scoring Framework — VIF / Multicollinearity Check.

Computes Variance Inflation Factors for the three scoring pillars
(equity, utilization, cost-effectiveness) to verify they are
sufficiently independent to justify the weighted composite.

VIF interpretation (DAMA-DMBOK / standard econometric thresholds):
    VIF = 1.0    Perfectly orthogonal (ideal)
    VIF < 5.0    Acceptable — pillars are independent
    VIF 5-10     Concerning — investigate overlap
    VIF > 10     Problematic — pillars are redundant

Output:
    data/processed/scoring-vif-check.csv

Usage:
    uv run code/python/analysis/scoring_framework_vif.py

Author: Wolfgang Sanyer
License: Polyform Noncommercial 1.0.0 (see LICENSE)
Date: 2026
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.tools import add_constant

# ---------------------------------------------------------------------------
# Resolve project paths
# ---------------------------------------------------------------------------
_SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPT_DIR))

# =============================================================================
# MODULE-LEVEL CONSTANTS
# =============================================================================

PROJECT_ROOT = _SCRIPT_DIR.parent.parent.parent

# Input
FINAL_CSV = PROJECT_ROOT / "data" / "processed" / "scoring-framework-final.csv"

# Output
OUTPUT_CSV = PROJECT_ROOT / "data" / "processed" / "scoring-vif-check.csv"

# Scoring pillar columns (must match scoring_framework_final.py output)
PILLAR_COLUMNS = ["equity_score", "util_score", "cost_score"]

# VIF interpretation thresholds
VIF_ACCEPTABLE = 5.0
VIF_CONCERNING = 10.0

# Display
_SEP_WIDTH = 60


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================


def _print_header(title: str) -> None:
    """Print a section header with separator lines."""
    print("=" * _SEP_WIDTH)
    print(title)
    print("=" * _SEP_WIDTH)


def compute_correlations(scores: pd.DataFrame) -> pd.DataFrame:
    """Compute and display pairwise Pearson correlations."""
    _print_header("PAIRWISE CORRELATIONS (Pearson)")
    corr = scores.corr()
    print(corr.round(4))
    return corr


def compute_vif(scores: pd.DataFrame) -> pd.DataFrame:
    """Compute Variance Inflation Factors for each scoring pillar.

    Adds a constant column, then computes VIF for each original
    variable against the others.

    Returns:
        DataFrame with Variable and VIF columns.
    """
    _print_header("VARIANCE INFLATION FACTORS")
    design = add_constant(scores)
    vif_data = pd.DataFrame({
        "Variable": scores.columns,
        "VIF": [
            variance_inflation_factor(design.values, i + 1)
            for i in range(len(scores.columns))
        ],
    })
    print(vif_data.to_string(index=False))
    return vif_data


def interpret_vif(vif_data: pd.DataFrame) -> None:
    """Print human-readable interpretation of VIF results."""
    max_vif = vif_data["VIF"].max()
    print(f"\nMax VIF: {max_vif:.2f}")

    if max_vif < VIF_ACCEPTABLE:
        print("RESULT: No multicollinearity concern (all VIF < 5).")
        print("The three scoring pillars are sufficiently independent.")
        print("The 0.40/0.35/0.25 weights are defensible.")
    elif max_vif < VIF_CONCERNING:
        print("WARNING: Moderate multicollinearity detected (VIF 5-10).")
        print("Investigate which pillars overlap. Consider combining or PCA.")
    else:
        print("PROBLEM: High multicollinearity (VIF > 10).")
        print("Scoring pillars are redundant. Weights are unstable.")


# =============================================================================
# MAIN
# =============================================================================


def main() -> None:
    """Run VIF multicollinearity check on NEVI scoring pillars."""
    df = pd.read_csv(FINAL_CSV)
    scores = df[PILLAR_COLUMNS].copy()

    print(f"Loaded {len(df)} counties from {FINAL_CSV.name}\n")

    compute_correlations(scores)
    print()
    vif_data = compute_vif(scores)
    interpret_vif(vif_data)

    vif_data.to_csv(OUTPUT_CSV, index=False)
    print(f"\nSaved: {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
