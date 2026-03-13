#!/usr/bin/env python3
"""
NEVI Scoring Framework — Weight Sensitivity Analysis.

Tests equity weight at 0.30, 0.35, 0.40, 0.45, 0.50 while holding the
utilization-to-cost-effectiveness ratio constant at 7:5.  Reports whether
the top-3 county rankings are stable across weight choices.

Output:
    data/processed/scoring-weight-sensitivity.csv
    Console summary table

Usage:
    uv run code/python/analysis/phase5_weight_sensitivity.py

Author: BIDA 670 EV-Pulse-NC Project
Date: 2026
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

# ---------------------------------------------------------------------------
# Resolve project paths
# ---------------------------------------------------------------------------
_SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPT_DIR))

PROJECT_ROOT = _SCRIPT_DIR.parent.parent.parent

FINAL_CSV = PROJECT_ROOT / "data" / "processed" / "scoring-framework-final.csv"
OUTPUT_CSV = PROJECT_ROOT / "data" / "processed" / "scoring-weight-sensitivity.csv"

# Weight scenarios: equity weight varies; remaining weight split 7:5 util:cost
EQUITY_WEIGHTS = [0.30, 0.35, 0.40, 0.45, 0.50]


def compute_scenario(
    df: pd.DataFrame, w_equity: float
) -> pd.DataFrame:
    """Recompute NEVI scores under a given equity weight.

    Args:
        df: Final scoring framework with equity_score, util_score, cost_score.
        w_equity: Equity pillar weight (0-1).

    Returns:
        DataFrame with county_name, rank, and score for this scenario.
    """
    remaining = 1.0 - w_equity
    # Split remaining weight 7:5 between utilization and cost-effectiveness
    w_util = remaining * (7 / 12)
    w_cost = remaining * (5 / 12)

    scores = (
        w_equity * df["equity_score"]
        + w_util * df["util_score"]
        + w_cost * df["cost_score"]
    )

    result = df[["county_name"]].copy()
    result["nevi_score"] = scores
    result = result.sort_values("nevi_score", ascending=False).reset_index(drop=True)
    result["rank"] = result.index + 1
    return result


def main() -> None:
    """Run weight sensitivity analysis across 5 equity weight scenarios."""
    print("[INFO] Weight Sensitivity Analysis")
    print(f"[INFO] Equity weights tested: {EQUITY_WEIGHTS}")
    print()

    df = pd.read_csv(FINAL_CSV, dtype={"county_fips": str})
    print(f"[INFO] Loaded final framework: {len(df)} counties\n")

    # Build wide table: county × scenario ranks
    rank_table = df[["county_name"]].copy()
    score_table = df[["county_name"]].copy()

    for w_eq in EQUITY_WEIGHTS:
        scenario = compute_scenario(df, w_eq)
        label = f"eq_{int(w_eq * 100)}"

        # Map rank and score back by county name
        rank_map = scenario.set_index("county_name")["rank"]
        score_map = scenario.set_index("county_name")["nevi_score"]

        rank_table[f"rank_{label}"] = rank_table["county_name"].map(rank_map)
        score_table[f"score_{label}"] = score_table["county_name"].map(score_map)

    # Sort by the baseline (eq_40) rank
    rank_table = rank_table.sort_values("rank_eq_40").reset_index(drop=True)
    score_table = score_table.sort_values(
        score_table.columns[3], ascending=False
    ).reset_index(drop=True)

    # Print rank table
    print("=" * 80)
    print("RANK STABILITY ACROSS EQUITY WEIGHT SCENARIOS")
    print("=" * 80)
    print(f"\n  Util:Cost ratio held constant at 7:5")
    print(f"  Baseline equity weight = 0.40 (column rank_eq_40)\n")
    print(rank_table.to_string(index=False))

    # Print score table
    print("\n\n" + "=" * 80)
    print("NEVI SCORES ACROSS EQUITY WEIGHT SCENARIOS")
    print("=" * 80)
    with pd.option_context("display.float_format", "{:.4f}".format):
        print(score_table.to_string(index=False))

    # Stability analysis
    print("\n\n" + "=" * 80)
    print("STABILITY ANALYSIS")
    print("=" * 80)

    rank_cols = [c for c in rank_table.columns if c.startswith("rank_")]
    baseline_top3 = set(
        rank_table.nsmallest(3, "rank_eq_40")["county_name"].tolist()
    )

    all_stable = True
    for col in rank_cols:
        scenario_top3 = set(
            rank_table.nsmallest(3, col)["county_name"].tolist()
        )
        match = scenario_top3 == baseline_top3
        status = "STABLE" if match else "CHANGED"
        if not match:
            all_stable = False
        print(f"  {col}: top-3 = {sorted(scenario_top3)} — {status}")

    print()
    if all_stable:
        print(
            "  RESULT: Top-3 rankings are STABLE across all equity weight "
            "scenarios (0.30-0.50)."
        )
        print(
            "  Paper defense: 'Rankings are robust to ±10 percentage-point "
            "variation in equity weight.'"
        )
    else:
        print(
            "  RESULT: Top-3 rankings CHANGE under some weight scenarios."
        )
        print("  Document which scenarios cause rank changes.")

    # Per-county rank range
    print("\n  Per-county rank range:")
    for _, row in rank_table.iterrows():
        ranks = [int(row[c]) for c in rank_cols]
        lo, hi = min(ranks), max(ranks)
        stability = "fixed" if lo == hi else f"varies {lo}-{hi}"
        print(f"    {row['county_name']:15s}: {stability}")

    # Save combined output
    merged = rank_table.merge(score_table, on="county_name")
    merged.to_csv(OUTPUT_CSV, index=False)
    print(f"\n[SUCCESS] Sensitivity results saved to {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
