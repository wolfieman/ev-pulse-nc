#!/usr/bin/env python3
"""
Phase 3 Step 4: ZIP-Level Charging Density Analysis.

Aggregates station-level data to one row per ZIP code, computing port
counts, per-capita density metrics, DC-fast share, network diversity,
and public-access subtotals. Produces a ZIP-level density CSV and a
county-level summary CSV for downstream modelling and visualisation.

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

INPUT_CSV = PROJECT_ROOT / "data" / "processed" / "phase3-urban-zip-stations.csv"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

# Population scaling factor for per-capita metrics
PER_CAPITA_SCALE = 10_000


# =============================================================================
# DATA LOADING
# =============================================================================


def load_stations(path: Path) -> pd.DataFrame:
    """Load the urban ZIP stations CSV from Step 3.

    Args:
        path: Path to phase3-urban-zip-stations.csv.

    Returns:
        DataFrame with correct dtypes applied.
    """
    df = pd.read_csv(path, dtype={"zip": str, "county_fips": str})
    df["zip"] = df["zip"].str.zfill(5)
    df["county_fips"] = df["county_fips"].str.zfill(5)
    for col in ("ev_level1_evse_num", "ev_level2_evse_num", "ev_dc_fast_num"):
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)
    df["total_ports"] = (
        df["ev_level1_evse_num"] + df["ev_level2_evse_num"] + df["ev_dc_fast_num"]
    )
    return df


# =============================================================================
# AGGREGATION
# =============================================================================


def _mode(series: pd.Series) -> str | float:
    """Return the most frequent value (mode) of a Series.

    Args:
        series: Input Series.

    Returns:
        The mode value, or NaN if the Series is empty.
    """
    m = series.mode()
    return m.iloc[0] if len(m) > 0 else np.nan


def aggregate_zip_density(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate station-level data to one row per ZIP.

    Args:
        df: Station-level DataFrame.

    Returns:
        ZIP-level DataFrame with density metrics.
    """
    # --- core aggregation ---
    agg = df.groupby("zip", as_index=False).agg(
        station_count=("id", "count"),
        total_ports=("total_ports", "sum"),
        l1_ports=("ev_level1_evse_num", "sum"),
        l2_ports=("ev_level2_evse_num", "sum"),
        dc_fast_ports=("ev_dc_fast_num", "sum"),
        network_count=("ev_network", "nunique"),
        population=("population", "first"),
        county_name=("county_name", _mode),
        county_fips=("county_fips", _mode),
        city=("city", _mode),
    )

    # --- public-only subtotals ---
    pub = df[df["access_code"] == "public"]
    pub_agg = pub.groupby("zip", as_index=False).agg(
        public_station_count=("id", "count"),
        public_ports=("total_ports", "sum"),
    )
    agg = agg.merge(pub_agg, on="zip", how="left")
    agg["public_station_count"] = agg["public_station_count"].fillna(0).astype(int)
    agg["public_ports"] = agg["public_ports"].fillna(0).astype(int)

    # --- flags ---
    agg["uninhabited"] = agg["population"] == 0
    agg["pop_missing"] = agg["population"].isna()

    # --- per-capita metrics (NaN where population is 0 or missing) ---
    valid_pop = agg["population"].where(agg["population"] > 0)
    agg["ports_per_10k"] = (agg["total_ports"] / valid_pop * PER_CAPITA_SCALE).round(2)
    agg["dc_fast_per_10k"] = (
        agg["dc_fast_ports"] / valid_pop * PER_CAPITA_SCALE
    ).round(2)

    # --- pct_dc_fast ---
    agg["pct_dc_fast"] = np.where(
        agg["total_ports"] > 0,
        (agg["dc_fast_ports"] / agg["total_ports"] * 100).round(2),
        0.0,
    )

    # --- column ordering ---
    col_order = [
        "zip",
        "city",
        "county_name",
        "county_fips",
        "population",
        "uninhabited",
        "pop_missing",
        "station_count",
        "total_ports",
        "l1_ports",
        "l2_ports",
        "dc_fast_ports",
        "public_station_count",
        "public_ports",
        "network_count",
        "ports_per_10k",
        "dc_fast_per_10k",
        "pct_dc_fast",
    ]
    agg = (
        agg[col_order]
        .sort_values("total_ports", ascending=False)
        .reset_index(drop=True)
    )
    return agg


def aggregate_county_summary(zip_df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate ZIP-level data to county-level summary.

    Args:
        zip_df: ZIP-level density DataFrame.

    Returns:
        County-level summary DataFrame (one row per county).
    """
    county = zip_df.groupby("county_name", as_index=False).agg(
        county_fips=("county_fips", "first"),
        zip_count=("zip", "count"),
        station_count=("station_count", "sum"),
        total_ports=("total_ports", "sum"),
        l2_ports=("l2_ports", "sum"),
        dc_fast_ports=("dc_fast_ports", "sum"),
        public_station_count=("public_station_count", "sum"),
        public_ports=("public_ports", "sum"),
        population=("population", "sum"),
        network_count=("network_count", "max"),
    )

    # County-level per-capita (exclude uninhabited/missing from sum already
    # handled because pop=0 or NaN contributes 0 or NaN to the sum)
    valid_pop = county["population"].where(county["population"] > 0)
    county["ports_per_10k"] = (
        county["total_ports"] / valid_pop * PER_CAPITA_SCALE
    ).round(2)
    county["dc_fast_per_10k"] = (
        county["dc_fast_ports"] / valid_pop * PER_CAPITA_SCALE
    ).round(2)

    county = county.sort_values("total_ports", ascending=False).reset_index(drop=True)
    return county


# =============================================================================
# OUTPUT
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
    stations: pd.DataFrame,
    zip_df: pd.DataFrame,
    county_df: pd.DataFrame,
) -> None:
    """Print a detailed console report of the density analysis.

    Args:
        stations: Original station-level DataFrame.
        zip_df: ZIP-level density DataFrame.
        county_df: County-level summary DataFrame.
    """
    sep = "=" * 70
    print(f"\n{sep}")
    print("PHASE 3 STEP 4: ZIP-LEVEL CHARGING DENSITY ANALYSIS")
    print(sep)

    # --- overview ---
    print("\n1. INPUT OVERVIEW")
    print(f"   Stations loaded:     {len(stations):,}")
    print(f"   Unique ZIPs:         {zip_df.shape[0]}")
    n_counties = zip_df["county_name"].nunique()
    print(f"   Unique counties:     {n_counties}")

    # --- special ZIPs ---
    uninhabited = zip_df[zip_df["uninhabited"]]
    pop_missing = zip_df[zip_df["pop_missing"]]
    print("\n2. SPECIAL ZIPs")
    if len(uninhabited) > 0:
        print(f"   Uninhabited (pop=0): {len(uninhabited)}")
        for _, row in uninhabited.iterrows():
            print(
                f"     ZIP {row['zip']} ({row['city']}): "
                f"{row['station_count']} stations, {row['total_ports']} ports"
            )
    else:
        print("   Uninhabited (pop=0): none")
    if len(pop_missing) > 0:
        print(f"   Pop missing (NaN):   {len(pop_missing)}")
        for _, row in pop_missing.iterrows():
            print(
                f"     ZIP {row['zip']} ({row['city']}): "
                f"{row['station_count']} stations, {row['total_ports']} ports"
            )
    else:
        print("   Pop missing (NaN):   none")

    # --- top 5 / bottom 5 by ports_per_10k ---
    ranked = zip_df.dropna(subset=["ports_per_10k"]).sort_values(
        "ports_per_10k", ascending=False
    )
    print("\n3. TOP 5 ZIPs BY PORTS PER 10K POPULATION")
    for _, row in ranked.head(5).iterrows():
        print(
            f"   ZIP {row['zip']:5s}  {row['city']:20s}  "
            f"{row['county_name']:15s}  "
            f"ports={row['total_ports']:4d}  pop={row['population']:,.0f}  "
            f"per_10k={row['ports_per_10k']:.2f}"
        )
    print("\n4. BOTTOM 5 ZIPs BY PORTS PER 10K POPULATION")
    for _, row in ranked.tail(5).iterrows():
        print(
            f"   ZIP {row['zip']:5s}  {row['city']:20s}  "
            f"{row['county_name']:15s}  "
            f"ports={row['total_ports']:4d}  pop={row['population']:,.0f}  "
            f"per_10k={row['ports_per_10k']:.2f}"
        )

    # --- county summary ---
    print("\n5. COUNTY SUMMARY")
    print(
        f"   {'County':<20s} {'ZIPs':>5s} {'Stations':>9s} "
        f"{'Ports':>6s} {'DC Fast':>8s} {'Pop':>10s} {'Per 10k':>8s}"
    )
    print(f"   {'-' * 20} {'-' * 5} {'-' * 9} {'-' * 6} {'-' * 8} {'-' * 10} {'-' * 8}")
    for _, row in county_df.iterrows():
        pop_str = f"{row['population']:,.0f}" if pd.notna(row["population"]) else "N/A"
        per10k_str = (
            f"{row['ports_per_10k']:.2f}" if pd.notna(row["ports_per_10k"]) else "N/A"
        )
        print(
            f"   {row['county_name']:<20s} {row['zip_count']:5d} "
            f"{row['station_count']:9d} {row['total_ports']:6d} "
            f"{row['dc_fast_ports']:8d} {pop_str:>10s} {per10k_str:>8s}"
        )

    # --- aggregate stats ---
    print("\n6. AGGREGATE STATISTICS")
    total_stations = zip_df["station_count"].sum()
    total_ports = zip_df["total_ports"].sum()
    total_dc = zip_df["dc_fast_ports"].sum()
    total_pop = zip_df["population"].sum()
    total_public_stations = zip_df["public_station_count"].sum()
    total_public_ports = zip_df["public_ports"].sum()
    print(f"   Total stations:        {total_stations:,}")
    print(f"   Total ports:           {total_ports:,}")
    print(f"   Total DC fast ports:   {total_dc:,}")
    print(f"   Public stations:       {total_public_stations:,}")
    print(f"   Public ports:          {total_public_ports:,}")
    if total_pop > 0:
        overall_per10k = total_ports / total_pop * PER_CAPITA_SCALE
        print(f"   Total population:      {total_pop:,.0f}")
        print(f"   Overall ports/10k:     {overall_per10k:.2f}")
    median_per10k = ranked["ports_per_10k"].median()
    mean_per10k = ranked["ports_per_10k"].mean()
    print(f"   Median ports/10k (ZIP): {median_per10k:.2f}")
    print(f"   Mean ports/10k (ZIP):   {mean_per10k:.2f}")

    print(f"\n{sep}")
    print("STEP 4 COMPLETE.")
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
        description="Phase 3 Step 4: ZIP-level charging density analysis"
    )
    parser.add_argument(
        "--input-csv",
        type=Path,
        default=INPUT_CSV,
        help="Path to phase3-urban-zip-stations.csv (default: auto-detect)",
    )
    parser.add_argument(
        "--processed-dir",
        type=Path,
        default=PROCESSED_DIR,
        help="Output directory for processed CSVs",
    )
    return parser.parse_args()


def main() -> None:
    """Entry point: load stations, aggregate to ZIP and county, write CSVs."""
    args = parse_args()
    args.processed_dir.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------
    # 1. Load data
    # ------------------------------------------------------------------
    print("Loading station data ...")
    stations = load_stations(args.input_csv)
    print(f"  Loaded {len(stations):,} stations from {args.input_csv.name}")

    # ------------------------------------------------------------------
    # 2. ZIP-level aggregation
    # ------------------------------------------------------------------
    print("\nAggregating to ZIP level ...")
    zip_df = aggregate_zip_density(stations)
    print(f"  {len(zip_df)} ZIPs produced.")

    # ------------------------------------------------------------------
    # 3. County-level summary
    # ------------------------------------------------------------------
    print("\nAggregating to county level ...")
    county_df = aggregate_county_summary(zip_df)
    print(f"  {len(county_df)} counties produced.")

    # ------------------------------------------------------------------
    # 4. Write outputs
    # ------------------------------------------------------------------
    print("\nWriting output CSVs ...")
    p1 = write_csv(zip_df, args.processed_dir / "phase3-zip-density.csv")
    print(f"  {p1.name}  ({len(zip_df)} rows)")

    p2 = write_csv(county_df, args.processed_dir / "phase3-zip-density-summary.csv")
    print(f"  {p2.name}  ({len(county_df)} rows)")

    # ------------------------------------------------------------------
    # 5. Console report
    # ------------------------------------------------------------------
    print_report(stations, zip_df, county_df)


if __name__ == "__main__":
    main()
