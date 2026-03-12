#!/usr/bin/env python3
"""
Phase 3 Step 6: Gini Coefficient & Inequality Analysis.

Loads the ZIP-level density CSV from Step 4, excludes 4 special ZIPs
(uninhabited or population-missing), and computes per-county inequality
metrics for EV charging port distribution:

- Gini coefficient (population-weighted and unweighted)
- Coefficient of variation (CV)
- Max/min ratio
- Interquartile range (IQR)
- Descriptive statistics (mean, median, min, max ports_per_10k)

Also computes a statewide population-weighted Gini across all 130
rankable ZIPs.

Outputs:
- phase3-county-gini.csv  (10 rows, one per county)
- phase3-statewide-gini.csv  (1 row)

Author: BIDA 670 EV-Pulse-NC Project
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

INPUT_CSV = PROJECT_ROOT / "data" / "processed" / "phase3-zip-density.csv"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

# Population scaling factor for per-capita metrics
PER_CAPITA_SCALE = 10_000

# Counties with fewer than this many ZIPs get a small-n warning
SMALL_N_THRESHOLD = 6


# =============================================================================
# DATA LOADING
# =============================================================================


def load_density(path: Path) -> pd.DataFrame:
    """Load the ZIP-level density CSV from Step 4.

    Args:
        path: Path to phase3-zip-density.csv.

    Returns:
        DataFrame with correct dtypes applied.
    """
    df = pd.read_csv(
        path,
        dtype={"zip": str, "county_fips": str},
    )
    df["zip"] = df["zip"].str.zfill(5)
    df["county_fips"] = df["county_fips"].str.zfill(5)
    return df


# =============================================================================
# FILTERING
# =============================================================================


def exclude_special_zips(df: pd.DataFrame) -> pd.DataFrame:
    """Remove uninhabited and population-missing ZIPs.

    Args:
        df: Full ZIP-level density DataFrame (134 rows).

    Returns:
        Filtered DataFrame with only rankable ZIPs (~130 rows).
    """
    mask = (df["uninhabited"] == True) | (df["pop_missing"] == True)  # noqa: E712
    excluded = df[mask]
    if len(excluded) > 0:
        print(f"  Excluding {len(excluded)} special ZIPs:")
        for _, row in excluded.iterrows():
            reason = []
            if row["uninhabited"]:
                reason.append("uninhabited")
            if row["pop_missing"]:
                reason.append("pop_missing")
            print(f"    ZIP {row['zip']} ({row['city']}) -- {', '.join(reason)}")
    return df[~mask].copy()


# =============================================================================
# GINI COMPUTATION
# =============================================================================


def gini_unweighted(values: np.ndarray) -> float:
    """Compute the unweighted Gini coefficient for an array of values.

    Uses the mean-absolute-difference formula:
        G = sum_i sum_j |x_i - x_j| / (2 * n^2 * mean)

    Args:
        values: 1-D array of non-negative values.

    Returns:
        Gini coefficient in [0, 1].  Returns NaN if fewer than 2 values
        or if all values are zero.
    """
    v = np.asarray(values, dtype=float)
    v = v[~np.isnan(v)]
    n = len(v)
    if n < 2:
        return np.nan
    mean_val = v.mean()
    if mean_val == 0:
        return np.nan
    abs_diff_sum = np.sum(np.abs(v[:, None] - v[None, :]))
    return float(abs_diff_sum / (2 * n * n * mean_val))


def gini_weighted(values: np.ndarray, weights: np.ndarray) -> float:
    """Compute a population-weighted Gini coefficient.

    Uses the weighted mean-absolute-difference formula:
        G = sum_i sum_j w_i * w_j * |x_i - x_j| / (2 * W^2 * weighted_mean)

    where W = sum(weights).

    Args:
        values: 1-D array of non-negative values (ports_per_10k).
        weights: 1-D array of positive weights (population).

    Returns:
        Weighted Gini coefficient in [0, 1].  Returns NaN if fewer than
        2 observations or if all values are zero.
    """
    v = np.asarray(values, dtype=float)
    w = np.asarray(weights, dtype=float)
    # Drop entries where either is NaN
    valid = ~(np.isnan(v) | np.isnan(w))
    v, w = v[valid], w[valid]
    n = len(v)
    if n < 2:
        return np.nan
    total_w = w.sum()
    if total_w == 0:
        return np.nan
    weighted_mean = np.sum(v * w) / total_w
    if weighted_mean == 0:
        return np.nan
    # Weighted absolute differences
    abs_diff = np.abs(v[:, None] - v[None, :])
    weight_product = w[:, None] * w[None, :]
    numerator = np.sum(abs_diff * weight_product)
    return float(numerator / (2 * total_w * total_w * weighted_mean))


# =============================================================================
# COMPLEMENTARY METRICS
# =============================================================================


def coefficient_of_variation(values: np.ndarray) -> float:
    """Compute the coefficient of variation (std / mean).

    Args:
        values: 1-D array of values.

    Returns:
        CV as a float.  Returns NaN if mean is zero or fewer than 2 values.
    """
    v = np.asarray(values, dtype=float)
    v = v[~np.isnan(v)]
    if len(v) < 2 or v.mean() == 0:
        return np.nan
    return float(v.std(ddof=1) / v.mean())


def ratio_max_min(values: np.ndarray) -> float:
    """Compute the max/min ratio.

    Args:
        values: 1-D array of positive values.

    Returns:
        Max/min ratio.  Returns inf if min is zero, NaN if empty.
    """
    v = np.asarray(values, dtype=float)
    v = v[~np.isnan(v)]
    if len(v) == 0:
        return np.nan
    min_val = v.min()
    if min_val == 0:
        return float("inf")
    return float(v.max() / min_val)


def iqr(values: np.ndarray) -> float:
    """Compute the interquartile range (Q3 - Q1).

    Args:
        values: 1-D array of values.

    Returns:
        IQR as a float.  Returns NaN if fewer than 4 values.
    """
    v = np.asarray(values, dtype=float)
    v = v[~np.isnan(v)]
    if len(v) < 4:
        return np.nan
    q1, q3 = np.percentile(v, [25, 75])
    return float(q3 - q1)


# =============================================================================
# COUNTY-LEVEL COMPUTATION
# =============================================================================


def compute_county_gini(df: pd.DataFrame) -> pd.DataFrame:
    """Compute inequality metrics for each county.

    Args:
        df: Filtered ZIP-level DataFrame (rankable ZIPs only).

    Returns:
        DataFrame with one row per county and all inequality metrics.
    """
    rows = []
    for county_name, group in df.groupby("county_name"):
        vals = group["ports_per_10k"].values
        pops = group["population"].values
        row = {
            "county_name": county_name,
            "county_fips": group["county_fips"].iloc[0],
            "zip_count": len(group),
            "gini_weighted": round(gini_weighted(vals, pops), 4),
            "gini_unweighted": round(gini_unweighted(vals), 4),
            "cv": round(coefficient_of_variation(vals), 4),
            "ratio_max_min": round(ratio_max_min(vals), 2),
            "iqr": round(iqr(vals), 2),
            "mean_ports_per_10k": round(float(np.nanmean(vals)), 2),
            "median_ports_per_10k": round(float(np.nanmedian(vals)), 2),
            "min_ports_per_10k": round(float(np.nanmin(vals)), 2),
            "max_ports_per_10k": round(float(np.nanmax(vals)), 2),
            "total_population": int(group["population"].sum()),
            "total_ports": int(group["total_ports"].sum()),
        }
        rows.append(row)

    result = pd.DataFrame(rows)
    result = result.sort_values("gini_weighted", ascending=False).reset_index(drop=True)
    return result


# =============================================================================
# STATEWIDE COMPUTATION
# =============================================================================


def compute_statewide_gini(df: pd.DataFrame) -> pd.DataFrame:
    """Compute statewide population-weighted Gini across all rankable ZIPs.

    Args:
        df: Filtered ZIP-level DataFrame (130 rankable ZIPs).

    Returns:
        Single-row DataFrame with statewide inequality metrics.
    """
    vals = df["ports_per_10k"].values
    pops = df["population"].values

    row = {
        "scope": "statewide_10_counties",
        "zip_count": len(df),
        "gini_weighted": round(gini_weighted(vals, pops), 4),
        "gini_unweighted": round(gini_unweighted(vals), 4),
        "cv": round(coefficient_of_variation(vals), 4),
        "ratio_max_min": round(ratio_max_min(vals), 2),
        "iqr": round(iqr(vals), 2),
        "mean_ports_per_10k": round(float(np.nanmean(vals)), 2),
        "median_ports_per_10k": round(float(np.nanmedian(vals)), 2),
        "min_ports_per_10k": round(float(np.nanmin(vals)), 2),
        "max_ports_per_10k": round(float(np.nanmax(vals)), 2),
        "total_population": int(df["population"].sum()),
        "total_ports": int(df["total_ports"].sum()),
    }
    return pd.DataFrame([row])


# =============================================================================
# CSV OUTPUT
# =============================================================================


def write_csv(df: pd.DataFrame, path: Path) -> Path:
    """Write a DataFrame to CSV.

    Args:
        df: DataFrame to write.
        path: Output path.

    Returns:
        The path written to.
    """
    df.to_csv(path, index=False)
    return path


# =============================================================================
# CONSOLE REPORTING
# =============================================================================


def _gini_interpretation(g: float) -> str:
    """Return a qualitative label for a Gini coefficient.

    Args:
        g: Gini coefficient value.

    Returns:
        Human-readable interpretation string.
    """
    if np.isnan(g):
        return "N/A"
    if g < 0.20:
        return "low inequality"
    if g < 0.35:
        return "moderate inequality"
    if g < 0.50:
        return "high inequality"
    return "very high inequality"


def print_report(
    county_df: pd.DataFrame,
    statewide_df: pd.DataFrame,
    n_total: int,
    n_rankable: int,
) -> None:
    """Print a formatted console report of inequality metrics.

    Args:
        county_df: County-level Gini DataFrame (10 rows).
        statewide_df: Statewide Gini DataFrame (1 row).
        n_total: Total ZIPs before filtering.
        n_rankable: Rankable ZIPs after filtering.
    """
    sep = "=" * 78
    print(f"\n{sep}")
    print("PHASE 3 STEP 6: GINI COEFFICIENT & INEQUALITY ANALYSIS")
    print(sep)

    # --- interpretation guide ---
    print("\n  INTERPRETATION GUIDE")
    print("  " + "-" * 40)
    print("  Gini = 0.00 : perfect equality (all ZIPs identical)")
    print("  Gini < 0.20 : low inequality")
    print("  Gini 0.20-0.35 : moderate inequality")
    print("  Gini 0.35-0.50 : high inequality")
    print("  Gini > 0.50 : very high inequality")
    print("  Gini = 1.00 : maximum concentration (one ZIP has all ports)")
    print()
    print("  CV (coefficient of variation) = std / mean; higher = more spread")
    print("  Max/min ratio: how many times the best-served ZIP exceeds the worst")
    print("  IQR: spread of the middle 50% of ZIPs")

    # --- input overview ---
    print(
        f"\n  INPUT: {n_total} total ZIPs, {n_rankable} rankable "
        f"({n_total - n_rankable} special excluded)"
    )

    # --- per-county table ---
    print(f"\n{'-' * 78}")
    print("  COUNTY INEQUALITY METRICS (ranked by weighted Gini, descending)")
    print(f"{'-' * 78}")
    header = (
        f"  {'County':<15s} {'ZIPs':>4s} {'Gini_w':>7s} {'Gini_u':>7s} "
        f"{'CV':>6s} {'Max/Min':>8s} {'IQR':>7s} "
        f"{'Mean':>6s} {'Med':>6s} {'Min':>6s} {'Max':>6s}"
    )
    print(header)
    print(
        f"  {'-' * 15} {'-' * 4} {'-' * 7} {'-' * 7} "
        f"{'-' * 6} {'-' * 8} {'-' * 7} "
        f"{'-' * 6} {'-' * 6} {'-' * 6} {'-' * 6}"
    )
    for _, row in county_df.iterrows():
        ratio_str = (
            f"{row['ratio_max_min']:8.1f}"
            if np.isfinite(row["ratio_max_min"])
            else "     inf"
        )
        iqr_str = f"{row['iqr']:7.2f}" if not np.isnan(row["iqr"]) else "    N/A"
        gw_str = (
            f"{row['gini_weighted']:7.4f}"
            if not np.isnan(row["gini_weighted"])
            else "    N/A"
        )
        gu_str = (
            f"{row['gini_unweighted']:7.4f}"
            if not np.isnan(row["gini_unweighted"])
            else "    N/A"
        )
        cv_str = f"{row['cv']:6.4f}" if not np.isnan(row["cv"]) else "   N/A"
        print(
            f"  {row['county_name']:<15s} {row['zip_count']:4d} "
            f"{gw_str} {gu_str} "
            f"{cv_str} {ratio_str} {iqr_str} "
            f"{row['mean_ports_per_10k']:6.2f} "
            f"{row['median_ports_per_10k']:6.2f} "
            f"{row['min_ports_per_10k']:6.2f} "
            f"{row['max_ports_per_10k']:6.2f}"
        )

    # --- interpretation per county ---
    print(f"\n{'-' * 78}")
    print("  INTERPRETATION BY COUNTY")
    print(f"{'-' * 78}")
    for _, row in county_df.iterrows():
        label = _gini_interpretation(row["gini_weighted"])
        print(
            f"  {row['county_name']:<15s}  Gini_w={row['gini_weighted']:.4f}  "
            f"-> {label}"
        )

    # --- small-n warnings ---
    small_n = county_df[county_df["zip_count"] < SMALL_N_THRESHOLD]
    if len(small_n) > 0:
        print(f"\n{'-' * 78}")
        print("  SMALL-N WARNINGS (fewer than 6 ZIPs)")
        print(f"{'-' * 78}")
        for _, row in small_n.iterrows():
            print(
                f"  WARNING: {row['county_name']} has only {row['zip_count']} "
                f"ZIPs -- Gini estimate may be unreliable"
            )

    # --- statewide ---
    sw = statewide_df.iloc[0]
    print(f"\n{'-' * 78}")
    print("  STATEWIDE INEQUALITY (all 130 rankable ZIPs)")
    print(f"{'-' * 78}")
    label = _gini_interpretation(sw["gini_weighted"])
    print(f"  Population-weighted Gini:  {sw['gini_weighted']:.4f}  -> {label}")
    print(f"  Unweighted Gini:           {sw['gini_unweighted']:.4f}")
    print(f"  CV:                        {sw['cv']:.4f}")
    sw_ratio = sw["ratio_max_min"]
    ratio_str = f"{sw_ratio:.1f}" if np.isfinite(sw_ratio) else "inf"
    print(f"  Max/min ratio:             {ratio_str}")
    print(f"  IQR:                       {sw['iqr']:.2f}")
    print(f"  Mean ports/10k:            {sw['mean_ports_per_10k']:.2f}")
    print(f"  Median ports/10k:          {sw['median_ports_per_10k']:.2f}")
    print(
        f"  Range:                     {sw['min_ports_per_10k']:.2f} - "
        f"{sw['max_ports_per_10k']:.2f}"
    )
    print(f"  ZIPs:                      {sw['zip_count']}")
    print(f"  Total population:          {sw['total_population']:,}")
    print(f"  Total ports:               {sw['total_ports']:,}")

    print(f"\n{sep}")
    print("STEP 6 COMPLETE.")
    print(sep)


# =============================================================================
# CLI & MAIN
# =============================================================================


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments.

    Returns:
        Parsed arguments namespace.
    """
    parser = argparse.ArgumentParser(
        description="Phase 3 Step 6: Gini coefficient & inequality analysis"
    )
    parser.add_argument(
        "--input-csv",
        type=Path,
        default=INPUT_CSV,
        help="Path to phase3-zip-density.csv (default: auto-detect)",
    )
    parser.add_argument(
        "--processed-dir",
        type=Path,
        default=PROCESSED_DIR,
        help="Output directory for processed CSVs",
    )
    return parser.parse_args()


def main() -> None:
    """Entry point: load, filter, compute Gini metrics, write CSVs."""
    args = parse_args()
    args.processed_dir.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------
    # 1. Load data
    # ------------------------------------------------------------------
    print("Loading ZIP density data ...")
    df = load_density(args.input_csv)
    n_total = len(df)
    print(f"  Loaded {n_total} ZIPs from {args.input_csv.name}")

    # ------------------------------------------------------------------
    # 2. Exclude special ZIPs
    # ------------------------------------------------------------------
    print("\nFiltering special ZIPs ...")
    df_rank = exclude_special_zips(df)
    n_rankable = len(df_rank)
    print(f"  {n_rankable} rankable ZIPs remain")

    # ------------------------------------------------------------------
    # 3. County-level Gini & inequality metrics
    # ------------------------------------------------------------------
    print("\nComputing county-level inequality metrics ...")
    county_df = compute_county_gini(df_rank)
    print(f"  {len(county_df)} counties processed")

    # ------------------------------------------------------------------
    # 4. Statewide Gini
    # ------------------------------------------------------------------
    print("\nComputing statewide inequality metrics ...")
    statewide_df = compute_statewide_gini(df_rank)
    print(f"  Statewide weighted Gini = {statewide_df.iloc[0]['gini_weighted']:.4f}")

    # ------------------------------------------------------------------
    # 5. Write outputs
    # ------------------------------------------------------------------
    print("\nWriting output CSVs ...")
    p1 = write_csv(county_df, args.processed_dir / "phase3-county-gini.csv")
    print(f"  {p1.name}  ({len(county_df)} rows)")

    p2 = write_csv(statewide_df, args.processed_dir / "phase3-statewide-gini.csv")
    print(f"  {p2.name}  ({len(statewide_df)} rows)")

    # ------------------------------------------------------------------
    # 6. Console report
    # ------------------------------------------------------------------
    print_report(county_df, statewide_df, n_total, n_rankable)


if __name__ == "__main__":
    main()
