#!/usr/bin/env python3
"""
NEVI Scoring Framework — Final Integration (Step 5.5).

Reads the Phase 3/4 skeleton table and Phase 5 Justice40 county data,
fills the four remaining NaN columns (equity_justice40_pct, equity_score,
util_score, nevi_priority_score), and exports the fully populated scoring
framework.

Scoring equation (from analytical-pipeline.md):

    NEVI Priority Score(county) = 0.40 * Equity_Score
                                + 0.35 * Utilization_Score
                                + 0.25 * Cost_Effectiveness_Score

Sub-score definitions:

    equity_score = 0.40 * minmax(equity_justice40_pct)
                 + 0.30 * minmax(equity_gini_weighted)
                 + 0.20 * minmax(equity_underserved_zips)
                 + 0.10 * minmax(equity_zero_station_pct)

    util_score   = minmax(util_bev_per_port)

    cost_score   = (inherited from skeleton, Phase 4)

Notes on zero-variance sub-metrics:
    - equity_zero_station_pct is 0.0 for all 10 counties.  After min-max
      normalization this collapses to 0.0 for every county, contributing
      nothing.  The weight (0.10) is retained for methodological
      completeness; if future counties with non-zero values are added,
      the metric will differentiate automatically.
    - util_forecast_buffer is 0.045 constant for all counties.  It cannot
      differentiate and is excluded from util_score normalization.

Output:
    data/processed/scoring-framework-final.csv

Usage:
    uv run code/python/analysis/scoring_framework_final.py

Author: Wolfgang Sanyer
License: Polyform Noncommercial 1.0.0 (see LICENSE)
Date: 2026
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Resolve project paths
# ---------------------------------------------------------------------------
_SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPT_DIR))

# =============================================================================
# MODULE-LEVEL CONSTANTS
# =============================================================================

PROJECT_ROOT = _SCRIPT_DIR.parent.parent.parent

# Input files
SKELETON_CSV = (
    PROJECT_ROOT / "data" / "processed" / "scoring-framework-skeleton.csv"
)
JUSTICE40_CSV = (
    PROJECT_ROOT / "data" / "processed" / "phase5-county-justice40.csv"
)

# Output
OUTPUT_CSV = (
    PROJECT_ROOT / "data" / "processed" / "scoring-framework-final.csv"
)

# NEVI scoring weights
WEIGHT_EQUITY = 0.40
WEIGHT_UTILIZATION = 0.35
WEIGHT_COST_EFFECTIVENESS = 0.25

# Equity sub-metric weights
EQUITY_W_J40 = 0.40
EQUITY_W_GINI = 0.30
EQUITY_W_UNDERSERVED = 0.20
EQUITY_W_ZERO_STATION = 0.10


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================


def minmax(series: pd.Series) -> pd.Series:
    """Min-max normalize a Series to [0, 1].

    If min == max (zero variance), returns 0.0 for all values.

    Args:
        series: Numeric pandas Series.

    Returns:
        Normalized Series with values in [0, 1].
    """
    s_min = series.min()
    s_max = series.max()
    if s_max == s_min:
        return pd.Series(0.0, index=series.index)
    return (series - s_min) / (s_max - s_min)


# =============================================================================
# DATA LOADING
# =============================================================================


def load_skeleton(path: Path) -> pd.DataFrame:
    """Load the Phase 3/4 scoring framework skeleton.

    Args:
        path: Path to scoring-framework-skeleton.csv.

    Returns:
        DataFrame with 10 rows, 20 columns (4 NaN columns).
    """
    df = pd.read_csv(path, dtype={"county_fips": str})
    print(f"[INFO] Loaded skeleton: {len(df)} counties, {len(df.columns)} cols")
    nan_cols = [c for c in df.columns if df[c].isna().all()]
    print(f"[INFO] NaN columns to fill: {nan_cols}")
    return df


def load_justice40(path: Path) -> pd.DataFrame:
    """Load Phase 5 county-level Justice40 percentages.

    Args:
        path: Path to phase5-county-justice40.csv.

    Returns:
        DataFrame with county_fips and justice40_pct_popweighted.
    """
    df = pd.read_csv(path, dtype={"county_fips": str})
    print(f"[INFO] Loaded Justice40 data: {len(df)} counties")
    return df[["county_fips", "justice40_pct_popweighted"]]


# =============================================================================
# COMPUTATION
# =============================================================================


def fill_scores(skeleton: pd.DataFrame, j40: pd.DataFrame) -> pd.DataFrame:
    """Fill the 4 NaN columns and compute the NEVI Priority Score.

    Args:
        skeleton: Scoring framework skeleton (13 populated, 4 NaN).
        j40: Justice40 data with county_fips and justice40_pct_popweighted.

    Returns:
        Fully populated DataFrame with all 17 data columns.
    """
    df = skeleton.copy()

    # ------------------------------------------------------------------
    # 1. Fill equity_justice40_pct from Phase 5
    # ------------------------------------------------------------------
    j40_map = j40.set_index("county_fips")["justice40_pct_popweighted"]
    df["equity_justice40_pct"] = df["county_fips"].map(j40_map)

    assert df["equity_justice40_pct"].notna().all(), (
        "Justice40 merge failed — NaN values remain"
    )

    # ------------------------------------------------------------------
    # 2. Compute equity_score
    # ------------------------------------------------------------------
    norm_j40 = minmax(df["equity_justice40_pct"])
    norm_gini = minmax(df["equity_gini_weighted"])
    norm_underserved = minmax(df["equity_underserved_zips"])
    norm_zero_station = minmax(df["equity_zero_station_pct"])

    df["equity_score"] = (
        EQUITY_W_J40 * norm_j40
        + EQUITY_W_GINI * norm_gini
        + EQUITY_W_UNDERSERVED * norm_underserved
        + EQUITY_W_ZERO_STATION * norm_zero_station
    )

    # Update equity_source to reflect Phase 5 integration
    df["equity_source"] = "Phase 3 + Phase 5 (Justice40 integrated)"

    # ------------------------------------------------------------------
    # 3. Compute util_score
    # ------------------------------------------------------------------
    # NOTE: forecast_buffer is 0.045 constant for all counties and cannot
    # differentiate. util_score is based solely on bev_per_port.
    df["util_score"] = minmax(df["util_bev_per_port"])

    # ------------------------------------------------------------------
    # 4. Compute nevi_priority_score
    # ------------------------------------------------------------------
    df["nevi_priority_score"] = (
        WEIGHT_EQUITY * df["equity_score"]
        + WEIGHT_UTILIZATION * df["util_score"]
        + WEIGHT_COST_EFFECTIVENESS * df["cost_score"]
    )

    return df


# =============================================================================
# VALIDATION
# =============================================================================


def validate(
    final: pd.DataFrame, skeleton: pd.DataFrame
) -> None:
    """Run all validation checks on the final scoring framework.

    Args:
        final: Fully populated scoring framework.
        skeleton: Original skeleton for comparison.

    Raises:
        AssertionError: If any validation check fails.
    """
    print("\n" + "-" * 80)
    print("VALIDATION CHECKS")
    print("-" * 80)

    # 1. No NaN remaining
    nan_count = final.isna().sum().sum()
    print(f"\n  [CHECK 1] NaN count: {nan_count}")
    assert nan_count == 0, f"Expected 0 NaN, got {nan_count}"
    print("    PASS — all columns populated")

    # 2. All scores in [0, 1]
    score_cols = [
        "equity_score",
        "util_score",
        "cost_score",
        "nevi_priority_score",
    ]
    for col in score_cols:
        lo, hi = final[col].min(), final[col].max()
        assert 0.0 <= lo and hi <= 1.0, (
            f"{col} out of range: [{lo}, {hi}]"
        )
        print(f"  [CHECK 2] {col}: [{lo:.4f}, {hi:.4f}] — PASS")

    # 3. Arithmetic verification: nevi = 0.40*equity + 0.35*util + 0.25*cost
    recomputed = (
        WEIGHT_EQUITY * final["equity_score"]
        + WEIGHT_UTILIZATION * final["util_score"]
        + WEIGHT_COST_EFFECTIVENESS * final["cost_score"]
    )
    diff = (final["nevi_priority_score"] - recomputed).abs().max()
    print(f"\n  [CHECK 3] NEVI recomputation max diff: {diff:.2e}")
    assert diff < 1e-12, f"Arithmetic mismatch: max diff = {diff}"
    print("    PASS — composite arithmetic verified")

    # 4. Previously populated columns are IDENTICAL to skeleton
    skeleton_orig = skeleton.copy()
    # Columns that existed in skeleton and were not NaN
    nan_or_changed = {
        "equity_justice40_pct",
        "equity_score",
        "util_score",
        "nevi_priority_score",
        "equity_source",
    }
    preserved_cols = [
        c
        for c in skeleton_orig.columns
        if c not in nan_or_changed
        and skeleton_orig[c].dtype in (np.float64, np.int64, float, int)
        and not skeleton_orig[c].isna().all()
    ]
    for col in preserved_cols:
        match = np.allclose(
            final[col].values.astype(float),
            skeleton_orig[col].values.astype(float),
            equal_nan=True,
        )
        assert match, f"Column {col} was modified!"
    # Check string columns too
    for col in ["county_name", "county_fips", "util_source", "cost_source"]:
        assert (final[col] == skeleton_orig[col]).all(), (
            f"String column {col} was modified!"
        )
    print("\n  [CHECK 4] 13 previously populated columns: IDENTICAL to skeleton")
    print("    PASS — no upstream data was altered")

    # 5. Intuition checks
    ranked = final.sort_values("nevi_priority_score", ascending=False)
    top3 = ranked["county_name"].head(3).tolist()
    bottom2 = ranked["county_name"].tail(2).tolist()

    print("\n  [CHECK 5] Intuition checks:")
    print(f"    Top 3: {top3}")
    print(f"    Bottom 2: {bottom2}")

    # Guilford or Mecklenburg should be in top 3
    assert "Guilford" in top3 or "Mecklenburg" in top3, (
        "Neither Guilford nor Mecklenburg in top 3 — unexpected"
    )
    print("    PASS — Guilford/Mecklenburg in top 3 as expected")

    # Orange should be in bottom half
    orange_rank = ranked["county_name"].tolist().index("Orange") + 1
    print(f"    Orange ranked #{orange_rank} of 10")
    assert orange_rank > 5, f"Orange ranked #{orange_rank}, expected bottom half"
    print("    PASS — Orange in bottom half (lowest J40, lowest Gini)")


# =============================================================================
# CONSOLE REPORTING
# =============================================================================


def print_final_table(df: pd.DataFrame) -> None:
    """Print the full final scoring framework table.

    Args:
        df: Fully populated scoring framework.
    """
    print("\n" + "=" * 80)
    print("NEVI SCORING FRAMEWORK — FINAL (ALL 17 DATA COLUMNS POPULATED)")
    print("=" * 80)

    with pd.option_context(
        "display.max_columns",
        None,
        "display.width",
        140,
        "display.float_format",
        "{:.4f}".format,
        "display.max_colwidth",
        35,
    ):
        print(df.to_string(index=False))


def print_ranked_list(df: pd.DataFrame) -> None:
    """Print counties ranked by NEVI Priority Score.

    Args:
        df: Fully populated scoring framework.
    """
    print("\n" + "=" * 80)
    print("NEVI PRIORITY RANKING (descending)")
    print("=" * 80)

    ranked = df.sort_values("nevi_priority_score", ascending=False).reset_index(
        drop=True
    )
    ranked.index = ranked.index + 1  # 1-based rank

    display_cols = [
        "county_name",
        "nevi_priority_score",
        "equity_score",
        "util_score",
        "cost_score",
    ]
    print()
    with pd.option_context(
        "display.float_format",
        "{:.4f}".format,
        "display.width",
        100,
    ):
        print(ranked[display_cols].to_string())


def print_score_decomposition(df: pd.DataFrame) -> None:
    """Print score decomposition for each county.

    Args:
        df: Fully populated scoring framework.
    """
    print("\n" + "=" * 80)
    print("SCORE DECOMPOSITION BY COUNTY")
    print("=" * 80)

    ranked = df.sort_values("nevi_priority_score", ascending=False)

    for _, row in ranked.iterrows():
        equity_contrib = WEIGHT_EQUITY * row["equity_score"]
        util_contrib = WEIGHT_UTILIZATION * row["util_score"]
        cost_contrib = WEIGHT_COST_EFFECTIVENESS * row["cost_score"]

        print(f"\n  {row['county_name']} (FIPS {row['county_fips']})")
        print(f"    NEVI Priority Score: {row['nevi_priority_score']:.4f}")
        print(
            f"    = {WEIGHT_EQUITY:.2f} x equity({row['equity_score']:.4f})"
            f" + {WEIGHT_UTILIZATION:.2f} x util({row['util_score']:.4f})"
            f" + {WEIGHT_COST_EFFECTIVENESS:.2f} x cost({row['cost_score']:.4f})"
        )
        print(
            f"    = {equity_contrib:.4f}"
            f" + {util_contrib:.4f}"
            f" + {cost_contrib:.4f}"
        )
        print(
            f"    Equity sub-metrics: J40={row['equity_justice40_pct']:.1f}%,"
            f" Gini={row['equity_gini_weighted']:.4f},"
            f" underserved_ZIPs={int(row['equity_underserved_zips'])},"
            f" zero_station={row['equity_zero_station_pct']:.1f}%"
        )


def print_top_county_analysis(df: pd.DataFrame) -> None:
    """Print analysis of the #1 ranked county.

    Args:
        df: Fully populated scoring framework.
    """
    print("\n" + "=" * 80)
    print("TOP COUNTY ANALYSIS")
    print("=" * 80)

    ranked = df.sort_values("nevi_priority_score", ascending=False)
    top = ranked.iloc[0]
    second = ranked.iloc[1]

    print(f"\n  #1 County: {top['county_name']} "
          f"(NEVI Score = {top['nevi_priority_score']:.4f})")
    print()
    print(f"  Why {top['county_name']} ranks first:")
    print(
        f"    - Equity Score:  {top['equity_score']:.4f}"
        f" (Justice40: {top['equity_justice40_pct']:.1f}%,"
        f" Gini: {top['equity_gini_weighted']:.4f},"
        f" underserved ZIPs: {int(top['equity_underserved_zips'])})"
    )
    print(
        f"    - Util Score:    {top['util_score']:.4f}"
        f" (BEV/port: {top['util_bev_per_port']:.1f})"
    )
    print(
        f"    - Cost Score:    {top['cost_score']:.4f}"
    )
    print(
        f"\n  Runner-up: {second['county_name']} "
        f"(NEVI Score = {second['nevi_priority_score']:.4f})"
    )
    gap = top["nevi_priority_score"] - second["nevi_priority_score"]
    print(f"  Gap: {gap:.4f}")


# =============================================================================
# MAIN
# =============================================================================


def main() -> None:
    """Build the final NEVI scoring framework with all columns populated."""
    parser = argparse.ArgumentParser(
        description=(
            "Fill remaining NaN columns and compute NEVI Priority Score."
        )
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=OUTPUT_CSV,
        help=(
            f"Output CSV path "
            f"(default: {OUTPUT_CSV.relative_to(PROJECT_ROOT)})"
        ),
    )
    args = parser.parse_args()

    print("[INFO] NEVI Scoring Framework — Final Integration (Step 5.5)")
    print(f"[INFO] Project root: {PROJECT_ROOT}")

    # --- Load source data ---
    print()
    skeleton = load_skeleton(SKELETON_CSV)
    j40 = load_justice40(JUSTICE40_CSV)

    # --- Fill scores ---
    final = fill_scores(skeleton, j40)

    # --- Validate ---
    validate(final, skeleton)

    # --- Save ---
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    final.to_csv(output_path, index=False)
    print(f"\n[SUCCESS] Final scoring framework saved to {output_path}")
    print(
        f"[INFO] Shape: {final.shape[0]} counties x {final.shape[1]} columns"
    )

    # --- Console reporting ---
    print_final_table(final)
    print_ranked_list(final)
    print_score_decomposition(final)
    print_top_county_analysis(final)

    print("\n" + "=" * 80)
    print("SCORING EQUATION")
    print("=" * 80)
    print(
        f"\n  NEVI Priority Score = "
        f"{WEIGHT_EQUITY:.2f} x Equity"
        f" + {WEIGHT_UTILIZATION:.2f} x Utilization"
        f" + {WEIGHT_COST_EFFECTIVENESS:.2f} x Cost_Effectiveness"
    )
    print(
        f"\n  Equity sub-weights: "
        f"J40={EQUITY_W_J40:.2f}, "
        f"Gini={EQUITY_W_GINI:.2f}, "
        f"Underserved={EQUITY_W_UNDERSERVED:.2f}, "
        f"ZeroStation={EQUITY_W_ZERO_STATION:.2f}"
    )
    print(
        "\n  Note: equity_zero_station_pct = 0.0 for all 10 counties"
        " (zero variance, contributes 0.0 after min-max)."
    )
    print(
        "  Note: util_forecast_buffer = 0.045 constant"
        " (cannot differentiate, excluded from util_score)."
    )
    print(
        f"\n  Status: COMPLETE — all {final.shape[1]} columns populated, "
        f"0 NaN remaining.\n"
    )


if __name__ == "__main__":
    main()
