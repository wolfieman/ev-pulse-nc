#!/usr/bin/env python3
"""
Phase 3 Step 5: Top-20 Underserved ZIPs Analysis.

Loads the ZIP-level density CSV from Step 4, excludes special ZIPs
(uninhabited or population-missing), computes additional metrics
(public_ports_per_10k, pct_below_median, density_percentile, dc_fast_zero),
ranks all 130 eligible ZIPs by ascending ports_per_10k (tie-break by
population descending), and outputs the top-20 underserved list, a
county-level breakdown, and a full ranked list for downstream use.

Author: BIDA 670 EV-Pulse-NC Project
Date: 2026
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

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

# Number of ZIPs for the "top underserved" cut
TOP_N = 20


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
# FILTERING & ENRICHMENT
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


def enrich_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """Add derived columns needed for ranking and output.

    Computes:
        - public_ports_per_10k
        - pct_below_median (True if ports_per_10k < median)
        - density_percentile (percentile rank of ports_per_10k, 0–100)
        - dc_fast_zero (True if dc_fast_ports == 0)

    Args:
        df: Filtered ZIP-level DataFrame (rankable ZIPs only).

    Returns:
        DataFrame with new columns added.
    """
    valid_pop = df["population"].where(df["population"] > 0)

    # Public ports per 10k population
    df["public_ports_per_10k"] = (
        df["public_ports"] / valid_pop * PER_CAPITA_SCALE
    ).round(2)

    # Median threshold
    median_val = df["ports_per_10k"].median()
    df["pct_below_median"] = df["ports_per_10k"] < median_val

    # Density percentile (lower percentile = more underserved)
    df["density_percentile"] = df["ports_per_10k"].rank(pct=True).mul(100).round(2)

    # DC-fast zero flag
    df["dc_fast_zero"] = df["dc_fast_ports"] == 0

    return df


# =============================================================================
# RANKING
# =============================================================================


def rank_zips(df: pd.DataFrame) -> pd.DataFrame:
    """Rank ZIPs by ascending ports_per_10k, tie-break by population descending.

    Args:
        df: Enriched ZIP-level DataFrame.

    Returns:
        Sorted DataFrame with a 1-based rank column.
    """
    df = df.sort_values(
        by=["ports_per_10k", "population"],
        ascending=[True, False],
    ).reset_index(drop=True)
    df.insert(0, "rank", range(1, len(df) + 1))
    return df


# =============================================================================
# OUTPUT COLUMNS
# =============================================================================

TOP20_COLUMNS = [
    "rank",
    "zip",
    "city",
    "county_name",
    "population",
    "station_count",
    "total_ports",
    "dc_fast_ports",
    "public_ports",
    "ports_per_10k",
    "dc_fast_per_10k",
    "public_ports_per_10k",
    "pct_below_median",
    "density_percentile",
    "dc_fast_zero",
]

ALL_RANKED_COLUMNS = TOP20_COLUMNS.copy()


# =============================================================================
# COUNTY BREAKDOWN
# =============================================================================


def county_breakdown(top20: pd.DataFrame) -> pd.DataFrame:
    """Summarise the top-20 underserved ZIPs by county.

    Args:
        top20: Top-20 DataFrame.

    Returns:
        County-level summary DataFrame.
    """
    county = top20.groupby("county_name", as_index=False).agg(
        zip_count=("zip", "count"),
        total_population=("population", "sum"),
        total_ports=("total_ports", "sum"),
        dc_fast_ports=("dc_fast_ports", "sum"),
        public_ports=("public_ports", "sum"),
        avg_ports_per_10k=("ports_per_10k", "mean"),
        min_ports_per_10k=("ports_per_10k", "min"),
        max_ports_per_10k=("ports_per_10k", "max"),
    )
    county["avg_ports_per_10k"] = county["avg_ports_per_10k"].round(2)
    county = county.sort_values("zip_count", ascending=False).reset_index(drop=True)
    return county


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


def print_report(
    top20: pd.DataFrame,
    county_df: pd.DataFrame,
    all_ranked: pd.DataFrame,
    median_val: float,
) -> None:
    """Print a formatted console report of the underserved analysis.

    Args:
        top20: Top-20 underserved ZIPs DataFrame.
        county_df: County-level breakdown DataFrame.
        all_ranked: Full ranked list (130 ZIPs).
        median_val: Median ports_per_10k across all rankable ZIPs.
    """
    sep = "=" * 78
    print(f"\n{sep}")
    print("PHASE 3 STEP 5: TOP-20 UNDERSERVED ZIPs")
    print(sep)

    # --- median reference ---
    print(f"\n  Median ports_per_10k (all 130 ZIPs): {median_val:.2f}")
    below_median_count = (all_ranked["pct_below_median"]).sum()
    print(f"  ZIPs below median:                   {below_median_count}")

    # --- top 20 table ---
    print(f"\n{'-' * 78}")
    print("  TOP 20 UNDERSERVED ZIPs (lowest ports_per_10k)")
    print(f"{'-' * 78}")
    header = (
        f"  {'Rk':>3s}  {'ZIP':<6s} {'City':<20s} {'County':<15s} "
        f"{'Pop':>8s} {'Ports':>5s} {'DC':>3s} {'Pub':>4s} "
        f"{'Per10k':>7s} {'PubP10k':>7s} {'DC=0':>4s}"
    )
    print(header)
    print(
        f"  {'-' * 3}  {'-' * 6} {'-' * 20} {'-' * 15} "
        f"{'-' * 8} {'-' * 5} {'-' * 3} {'-' * 4} "
        f"{'-' * 7} {'-' * 7} {'-' * 4}"
    )
    for _, row in top20.iterrows():
        dc_flag = "YES" if row["dc_fast_zero"] else ""
        print(
            f"  {row['rank']:3d}  {row['zip']:<6s} {row['city']:<20s} "
            f"{row['county_name']:<15s} "
            f"{row['population']:>8,.0f} {row['total_ports']:5d} "
            f"{row['dc_fast_ports']:3d} {row['public_ports']:4d} "
            f"{row['ports_per_10k']:7.2f} {row['public_ports_per_10k']:7.2f} "
            f"{dc_flag:>4s}"
        )

    # --- county breakdown ---
    print(f"\n{'-' * 78}")
    print("  COUNTY BREAKDOWN OF TOP 20")
    print(f"{'-' * 78}")
    print(
        f"  {'County':<20s} {'ZIPs':>5s} {'Pop':>10s} {'Ports':>6s} "
        f"{'DC':>4s} {'Pub':>5s} {'Avg P/10k':>9s} {'Min':>7s} {'Max':>7s}"
    )
    print(
        f"  {'-' * 20} {'-' * 5} {'-' * 10} {'-' * 6} "
        f"{'-' * 4} {'-' * 5} {'-' * 9} {'-' * 7} {'-' * 7}"
    )
    for _, row in county_df.iterrows():
        print(
            f"  {row['county_name']:<20s} {row['zip_count']:5d} "
            f"{row['total_population']:>10,.0f} {row['total_ports']:6d} "
            f"{row['dc_fast_ports']:4d} {row['public_ports']:5d} "
            f"{row['avg_ports_per_10k']:9.2f} "
            f"{row['min_ports_per_10k']:7.2f} {row['max_ports_per_10k']:7.2f}"
        )

    # --- aggregate stats ---
    print(f"\n{'-' * 78}")
    print("  AGGREGATE STATISTICS (TOP 20)")
    print(f"{'-' * 78}")
    total_pop = top20["population"].sum()
    total_ports = top20["total_ports"].sum()
    total_dc = top20["dc_fast_ports"].sum()
    total_pub = top20["public_ports"].sum()
    dc_zero_count = top20["dc_fast_zero"].sum()
    print(f"  Total underserved population:  {total_pop:>10,.0f}")
    print(f"  Total ports in top 20:         {total_ports:>10,}")
    print(f"  Total DC fast ports:           {total_dc:>10,}")
    print(f"  Total public ports:            {total_pub:>10,}")
    if total_pop > 0:
        agg_per10k = total_ports / total_pop * PER_CAPITA_SCALE
        print(f"  Aggregate ports/10k:           {agg_per10k:>10.2f}")
    print(f"  ZIPs with zero DC fast:        {dc_zero_count:>10}")
    print(f"  Counties represented:          {county_df.shape[0]:>10}")

    print(f"\n{sep}")
    print("STEP 5 COMPLETE.")
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
        description="Phase 3 Step 5: Top-20 underserved ZIPs analysis"
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
    parser.add_argument(
        "--top-n",
        type=int,
        default=TOP_N,
        help="Number of top underserved ZIPs (default: 20)",
    )
    return parser.parse_args()


def main() -> None:
    """Entry point: load, filter, enrich, rank, output."""
    args = parse_args()
    args.processed_dir.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------
    # 1. Load data
    # ------------------------------------------------------------------
    print("Loading ZIP density data ...")
    df = load_density(args.input_csv)
    print(f"  Loaded {len(df)} ZIPs from {args.input_csv.name}")

    # ------------------------------------------------------------------
    # 2. Exclude special ZIPs
    # ------------------------------------------------------------------
    print("\nFiltering special ZIPs ...")
    df_rank = exclude_special_zips(df)
    print(f"  {len(df_rank)} rankable ZIPs remain")

    # ------------------------------------------------------------------
    # 3. Enrich with derived metrics
    # ------------------------------------------------------------------
    print("\nComputing derived metrics ...")
    df_rank = enrich_metrics(df_rank)
    median_val = df_rank["ports_per_10k"].median()
    print(f"  Median ports_per_10k = {median_val:.2f}")

    # ------------------------------------------------------------------
    # 4. Rank all ZIPs
    # ------------------------------------------------------------------
    print("\nRanking ZIPs by ports_per_10k (ascending) ...")
    all_ranked = rank_zips(df_rank)

    # ------------------------------------------------------------------
    # 5. Top N
    # ------------------------------------------------------------------
    top20 = all_ranked.head(args.top_n).copy()
    print(f"  Top {args.top_n} underserved ZIPs selected")

    # ------------------------------------------------------------------
    # 6. County breakdown of top 20
    # ------------------------------------------------------------------
    county_df = county_breakdown(top20)

    # ------------------------------------------------------------------
    # 7. Write outputs
    # ------------------------------------------------------------------
    print("\nWriting output CSVs ...")
    p1 = write_csv(
        top20[TOP20_COLUMNS],
        args.processed_dir / "phase3-top20-underserved.csv",
    )
    print(f"  {p1.name}  ({len(top20)} rows)")

    p2 = write_csv(
        county_df,
        args.processed_dir / "phase3-underserved-summary.csv",
    )
    print(f"  {p2.name}  ({len(county_df)} rows)")

    p3 = write_csv(
        all_ranked[ALL_RANKED_COLUMNS],
        args.processed_dir / "phase3-all-zips-ranked.csv",
    )
    print(f"  {p3.name}  ({len(all_ranked)} rows)")

    # ------------------------------------------------------------------
    # 8. Console report
    # ------------------------------------------------------------------
    print_report(top20, county_df, all_ranked, median_val)


if __name__ == "__main__":
    main()
