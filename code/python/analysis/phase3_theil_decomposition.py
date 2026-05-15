#!/usr/bin/env python3
"""
Phase 3: Theil Index Decomposition for EV Charging Port Density.

Computes the Theil-T index (GE(1)) for EV charging port density across
~130 rankable ZIPs in 10 counties, with exact additive decomposition
into between-county and within-county components. Also computes
Theil-L (GE(0)) as a robustness check.

Outputs:
- phase3-theil-decomposition.csv   (3 rows: total, between, within)
- phase3-theil-county-contributions.csv  (10 rows, one per county)

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

INPUT_CSV = PROJECT_ROOT / "data" / "processed" / "phase3-zip-density.csv"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

# Floating-point tolerance for decomposition verification
DECOMPOSITION_TOL = 1e-10


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
    mask = (df["uninhabited"] == True) | (  # noqa: E712
        df["pop_missing"] == True  # noqa: E712
    )
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


def exclude_zero_density(df: pd.DataFrame) -> pd.DataFrame:
    """Remove ZIPs with zero, NaN, or missing ports_per_10k.

    Theil index requires strictly positive values for all observations.

    Args:
        df: Filtered ZIP-level DataFrame.

    Returns:
        DataFrame with only positive-density ZIPs.
    """
    before = len(df)
    df_out = df.dropna(subset=["ports_per_10k"]).copy()
    df_out = df_out[df_out["ports_per_10k"] > 0].copy()
    after = len(df_out)
    if before != after:
        print(
            f"  Excluded {before - after} ZIPs with zero/missing "
            f"ports_per_10k (Theil requires positive values)"
        )
    return df_out


# =============================================================================
# THEIL-T (GE(1)) COMPUTATION
# =============================================================================


def theil_t(values: np.ndarray, weights: np.ndarray) -> float:
    """Compute the population-weighted Theil-T index (GE(1)).

    T = sum_i (w_i / W) * (x_i / x_bar) * ln(x_i / x_bar)

    Args:
        values: 1-D array of positive values (ports_per_10k).
        weights: 1-D array of positive weights (population).

    Returns:
        Theil-T index value. Returns NaN if fewer than 2 observations.
    """
    x = np.asarray(values, dtype=float)
    w = np.asarray(weights, dtype=float)
    n = len(x)
    if n < 2:
        return np.nan
    total_w = w.sum()
    x_bar = np.sum(x * w) / total_w
    if x_bar == 0:
        return np.nan
    share = w / total_w
    ratio = x / x_bar
    return float(np.sum(share * ratio * np.log(ratio)))


# =============================================================================
# THEIL-L (GE(0)) COMPUTATION
# =============================================================================


def theil_l(values: np.ndarray, weights: np.ndarray) -> float:
    """Compute the population-weighted Theil-L index (GE(0), mean log deviation).

    L = sum_i (w_i / W) * ln(x_bar / x_i)

    Args:
        values: 1-D array of positive values (ports_per_10k).
        weights: 1-D array of positive weights (population).

    Returns:
        Theil-L index value. Returns NaN if fewer than 2 observations.
    """
    x = np.asarray(values, dtype=float)
    w = np.asarray(weights, dtype=float)
    n = len(x)
    if n < 2:
        return np.nan
    total_w = w.sum()
    x_bar = np.sum(x * w) / total_w
    if x_bar == 0:
        return np.nan
    share = w / total_w
    return float(np.sum(share * np.log(x_bar / x)))


# =============================================================================
# THEIL-T DECOMPOSITION
# =============================================================================


def decompose_theil_t(
    df: pd.DataFrame,
) -> tuple[float, float, float, pd.DataFrame]:
    """Decompose Theil-T into between-county and within-county components.

    Args:
        df: Filtered DataFrame with columns ports_per_10k, population,
            county_fips, county_name.

    Returns:
        Tuple of (t_total, t_between, t_within, county_detail_df).
    """
    x = df["ports_per_10k"].values
    w = df["population"].values

    total_w = w.sum()
    x_bar = np.sum(x * w) / total_w

    # Total Theil-T
    t_total = theil_t(x, w)

    # Between-county component
    t_between = 0.0
    county_rows = []

    for (county_name, county_fips), grp in df.groupby(["county_name", "county_fips"]):
        x_g = grp["ports_per_10k"].values
        w_g = grp["population"].values
        w_g_total = w_g.sum()
        x_bar_g = np.sum(x_g * w_g) / w_g_total

        pop_share = w_g_total / total_w
        ratio_g = x_bar_g / x_bar

        # Between-county contribution for this county
        t_between += pop_share * ratio_g * np.log(ratio_g)

        # Within-county Theil-T for this county
        t_g = theil_t(x_g, w_g)

        contrib_raw = pop_share * ratio_g * t_g

        county_rows.append(
            {
                "county_name": county_name,
                "county_fips": county_fips,
                "population": int(w_g_total),
                "weighted_mean_ports_per_10k": round(x_bar_g, 4),
                "theil_t_within": round(t_g, 6),
                "contribution_to_total_within": round(contrib_raw, 6),
                "_contrib_raw": contrib_raw,
                "zip_count": len(grp),
            }
        )

    # Within-county component: sum from unrounded values for exact decomposition
    t_within = sum(r["_contrib_raw"] for r in county_rows)

    county_detail = pd.DataFrame(county_rows)
    county_detail = county_detail.drop(columns=["_contrib_raw"])
    county_detail = county_detail.sort_values(
        "contribution_to_total_within", ascending=False
    ).reset_index(drop=True)

    return t_total, t_between, t_within, county_detail


# =============================================================================
# THEIL-L DECOMPOSITION
# =============================================================================


def decompose_theil_l(
    df: pd.DataFrame,
) -> tuple[float, float, float]:
    """Decompose Theil-L into between-county and within-county components.

    Args:
        df: Filtered DataFrame with columns ports_per_10k, population,
            county_fips, county_name.

    Returns:
        Tuple of (l_total, l_between, l_within).
    """
    x = df["ports_per_10k"].values
    w = df["population"].values

    total_w = w.sum()
    x_bar = np.sum(x * w) / total_w

    # Total Theil-L
    l_total = theil_l(x, w)

    # Between-county component
    l_between = 0.0
    l_within = 0.0

    for _, grp in df.groupby("county_fips"):
        x_g = grp["ports_per_10k"].values
        w_g = grp["population"].values
        w_g_total = w_g.sum()
        x_bar_g = np.sum(x_g * w_g) / w_g_total

        pop_share = w_g_total / total_w

        # Between-county contribution
        l_between += pop_share * np.log(x_bar / x_bar_g)

        # Within-county Theil-L
        l_g = theil_l(x_g, w_g)
        l_within += pop_share * l_g

    return l_total, l_between, l_within


# =============================================================================
# OUTPUT GENERATION
# =============================================================================


def build_decomposition_csv(
    t_total: float,
    t_between: float,
    t_within: float,
    l_total: float,
    l_between: float,
    l_within: float,
) -> pd.DataFrame:
    """Build the decomposition summary DataFrame.

    Args:
        t_total: Total Theil-T.
        t_between: Between-county Theil-T component.
        t_within: Within-county Theil-T component.
        l_total: Total Theil-L.
        l_between: Between-county Theil-L component.
        l_within: Within-county Theil-L component.

    Returns:
        DataFrame with 3 rows (total, between, within).
    """
    rows = [
        {
            "component": "total",
            "theil_t": round(t_total, 6),
            "theil_l": round(l_total, 6),
            "pct_of_total_t": 100.0,
            "pct_of_total_l": 100.0,
        },
        {
            "component": "between",
            "theil_t": round(t_between, 6),
            "theil_l": round(l_between, 6),
            "pct_of_total_t": round(t_between / t_total * 100, 2),
            "pct_of_total_l": round(l_between / l_total * 100, 2),
        },
        {
            "component": "within",
            "theil_t": round(t_within, 6),
            "theil_l": round(l_within, 6),
            "pct_of_total_t": round(t_within / t_total * 100, 2),
            "pct_of_total_l": round(l_within / l_total * 100, 2),
        },
    ]
    return pd.DataFrame(rows)


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


def print_report(
    t_total: float,
    t_between: float,
    t_within: float,
    l_total: float,
    l_between: float,
    l_within: float,
    county_detail: pd.DataFrame,
    n_total: int,
    n_rankable: int,
    n_positive: int,
) -> None:
    """Print a formatted console report of the Theil decomposition.

    Args:
        t_total: Total Theil-T.
        t_between: Between-county Theil-T component.
        t_within: Within-county Theil-T component.
        l_total: Total Theil-L.
        l_between: Between-county Theil-L component.
        l_within: Within-county Theil-L component.
        county_detail: Per-county contribution DataFrame.
        n_total: Total ZIPs before filtering.
        n_rankable: Rankable ZIPs after excluding special ZIPs.
        n_positive: ZIPs with positive ports_per_10k.
    """
    sep = "=" * 78
    print(f"\n{sep}")
    print("PHASE 3: THEIL INDEX DECOMPOSITION")
    print(sep)

    # --- input overview ---
    print(
        f"\n[INFO] INPUT: {n_total} total ZIPs -> "
        f"{n_rankable} rankable -> "
        f"{n_positive} with positive density"
    )

    # --- Theil-T decomposition ---
    print(f"\n{'-' * 78}")
    print("  THEIL-T (GE(1)) DECOMPOSITION  [population-weighted]")
    print(f"{'-' * 78}")
    print(f"  Total Theil-T:           {t_total:.6f}")
    print(
        f"  Between-county:          {t_between:.6f}  "
        f"({t_between / t_total * 100:.1f}%)"
    )
    print(
        f"  Within-county:           {t_within:.6f}  ({t_within / t_total * 100:.1f}%)"
    )

    # --- Verification ---
    recon = t_between + t_within
    diff = abs(recon - t_total)
    print(f"\n  Verification: between + within = {recon:.6f}")
    if diff < DECOMPOSITION_TOL:
        print(f"  [SUCCESS] Exact decomposition verified (diff = {diff:.2e})")
    else:
        print(f"  [WARNING] Decomposition mismatch! diff = {diff:.2e}")

    # --- Theil-L robustness check ---
    print(f"\n{'-' * 78}")
    print("  THEIL-L (GE(0)) DECOMPOSITION  [robustness check]")
    print(f"{'-' * 78}")
    print(f"  Total Theil-L:           {l_total:.6f}")
    print(
        f"  Between-county:          {l_between:.6f}  "
        f"({l_between / l_total * 100:.1f}%)"
    )
    print(
        f"  Within-county:           {l_within:.6f}  ({l_within / l_total * 100:.1f}%)"
    )

    recon_l = l_between + l_within
    diff_l = abs(recon_l - l_total)
    print(f"\n  Verification: between + within = {recon_l:.6f}")
    if diff_l < DECOMPOSITION_TOL:
        print(f"  [SUCCESS] Exact decomposition verified (diff = {diff_l:.2e})")
    else:
        print(f"  [WARNING] Decomposition mismatch! diff = {diff_l:.2e}")

    # --- Key ratio ---
    within_pct = t_within / t_total * 100
    print(f"\n{'-' * 78}")
    print("  KEY RATIO")
    print(f"{'-' * 78}")
    print(f"  T_within / T_total = {within_pct:.1f}%")

    # --- Policy interpretation ---
    print(f"\n{'-' * 78}")
    print("  POLICY INTERPRETATION")
    print(f"{'-' * 78}")
    if within_pct > 50:
        print(
            "  Within-county inequality dominates -- sub-county targeting recommended"
        )
        print(
            f"  {within_pct:.1f}% of total inequality occurs WITHIN "
            f"counties, not between them."
        )
        print(
            "  Policy implication: county-level averages mask large "
            "ZIP-level disparities."
        )
    else:
        print(
            "  Between-county inequality dominates "
            "-- county-level targeting may be sufficient"
        )
        print(f"  {100 - within_pct:.1f}% of total inequality occurs BETWEEN counties.")

    # --- Per-county contributions ---
    print(f"\n{'-' * 78}")
    print("  PER-COUNTY CONTRIBUTIONS TO WITHIN-COUNTY INEQUALITY")
    print("  (sorted by contribution, descending)")
    print(f"{'-' * 78}")
    header = (
        f"  {'County':<15s} {'FIPS':>5s} {'Pop':>9s} "
        f"{'Mean p/10k':>10s} {'T_within':>10s} "
        f"{'Contrib':>10s} {'ZIPs':>5s}"
    )
    print(header)
    print(
        f"  {'-' * 15} {'-' * 5} {'-' * 9} {'-' * 10} {'-' * 10} {'-' * 10} {'-' * 5}"
    )
    for _, row in county_detail.iterrows():
        print(
            f"  {row['county_name']:<15s} {row['county_fips']:>5s} "
            f"{row['population']:>9,d} "
            f"{row['weighted_mean_ports_per_10k']:>10.4f} "
            f"{row['theil_t_within']:>10.6f} "
            f"{row['contribution_to_total_within']:>10.6f} "
            f"{row['zip_count']:>5d}"
        )

    print(f"\n{sep}")
    print("[SUCCESS] THEIL DECOMPOSITION COMPLETE.")
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
        description=("Phase 3: Theil index decomposition for EV charging port density")
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
    """Entry point: load, filter, decompose Theil, write CSVs."""
    args = parse_args()
    args.processed_dir.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------
    # 1. Load data
    # ------------------------------------------------------------------
    print("[INFO] Loading ZIP density data ...")
    df = load_density(args.input_csv)
    n_total = len(df)
    print(f"  Loaded {n_total} ZIPs from {args.input_csv.name}")

    # ------------------------------------------------------------------
    # 2. Exclude special ZIPs (uninhabited / pop_missing)
    # ------------------------------------------------------------------
    print("\n[INFO] Filtering special ZIPs ...")
    df_rank = exclude_special_zips(df)
    n_rankable = len(df_rank)
    print(f"  {n_rankable} rankable ZIPs remain")

    # ------------------------------------------------------------------
    # 3. Exclude zero/missing density (Theil requires positive values)
    # ------------------------------------------------------------------
    print("\n[INFO] Filtering zero/missing density ZIPs ...")
    df_pos = exclude_zero_density(df_rank)
    n_positive = len(df_pos)
    print(f"  {n_positive} ZIPs with positive ports_per_10k")

    # ------------------------------------------------------------------
    # 4. Theil-T decomposition
    # ------------------------------------------------------------------
    print("\n[INFO] Computing Theil-T decomposition ...")
    t_total, t_between, t_within, county_detail = decompose_theil_t(df_pos)
    print(f"  Theil-T total = {t_total:.6f}")

    # ------------------------------------------------------------------
    # 5. Theil-L decomposition (robustness check)
    # ------------------------------------------------------------------
    print("\n[INFO] Computing Theil-L decomposition ...")
    l_total, l_between, l_within = decompose_theil_l(df_pos)
    print(f"  Theil-L total = {l_total:.6f}")

    # ------------------------------------------------------------------
    # 6. Write outputs
    # ------------------------------------------------------------------
    print("\n[INFO] Writing output CSVs ...")

    decomp_df = build_decomposition_csv(
        t_total,
        t_between,
        t_within,
        l_total,
        l_between,
        l_within,
    )
    p1 = write_csv(
        decomp_df,
        args.processed_dir / "phase3-theil-decomposition.csv",
    )
    print(f"  [SUCCESS] {p1.name}  ({len(decomp_df)} rows)")

    p2 = write_csv(
        county_detail,
        args.processed_dir / "phase3-theil-county-contributions.csv",
    )
    print(f"  [SUCCESS] {p2.name}  ({len(county_detail)} rows)")

    # ------------------------------------------------------------------
    # 7. Console report
    # ------------------------------------------------------------------
    print_report(
        t_total,
        t_between,
        t_within,
        l_total,
        l_between,
        l_within,
        county_detail,
        n_total,
        n_rankable,
        n_positive,
    )


if __name__ == "__main__":
    main()
