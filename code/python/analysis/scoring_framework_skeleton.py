#!/usr/bin/env python3
"""
NEVI Scoring Framework Skeleton Table.

Builds the integration table that maps Phase 3 and Phase 4 outputs to
the NEVI scoring framework.  Populates utilization sub-metrics from
Phases 1-3, cost-effectiveness sub-metrics from Phase 4, and partial
equity sub-metrics from Phase 3.  Leaves NaN placeholders for Phase 5
columns, and documents the source phase for each column.

Scoring equation (from analytical-pipeline.md):

    NEVI Priority Score(county) = 0.40 * Equity_Score
                                + 0.35 * Utilization_Score
                                + 0.25 * Cost_Effectiveness_Score

Output:
    data/processed/scoring-framework-skeleton.csv

Usage:
    uv run code/python/analysis/scoring_framework_skeleton.py

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

# Input files (Phase 3 processed outputs)
TOP10_COUNTIES_CSV = PROJECT_ROOT / "data" / "processed" / "phase3-top10-counties.csv"
COUNTY_GINI_CSV = PROJECT_ROOT / "data" / "processed" / "phase3-county-gini.csv"
ZIP_DENSITY_CSV = PROJECT_ROOT / "data" / "processed" / "phase3-zip-density.csv"
ZIP_DENSITY_SUMMARY_CSV = (
    PROJECT_ROOT / "data" / "processed" / "phase3-zip-density-summary.csv"
)
TOP20_UNDERSERVED_CSV = (
    PROJECT_ROOT / "data" / "processed" / "phase3-top20-underserved.csv"
)
PHASE4_COST_CSV = (
    PROJECT_ROOT / "data" / "processed" / "phase4-cost-effectiveness.csv"
)

# Output
OUTPUT_CSV = PROJECT_ROOT / "data" / "processed" / "scoring-framework-skeleton.csv"

# Phase 1 underprediction bias constant (4.5% upward adjustment)
FORECAST_BUFFER = 0.045

# NEVI scoring weights (for documentation; not used in computation yet)
WEIGHT_EQUITY = 0.40
WEIGHT_UTILIZATION = 0.35
WEIGHT_COST_EFFECTIVENESS = 0.25

# Column ordering for the final output
OUTPUT_COLUMNS = [
    # Identifiers
    "county_name",
    "county_fips",
    # Utilization sub-metrics (weight: 0.35)
    "util_bev_count",
    "util_total_ports",
    "util_bev_per_port",
    "util_forecast_buffer",
    "util_score",
    "util_source",
    # Cost-effectiveness sub-metrics (weight: 0.25)
    "cost_workplace_efficiency",
    "cost_commuter_demand",
    "cost_pop_density",
    "cost_score",
    "cost_source",
    # Equity sub-metrics (weight: 0.40)
    "equity_gini_weighted",
    "equity_zero_station_pct",
    "equity_underserved_zips",
    "equity_justice40_pct",
    "equity_score",
    "equity_source",
    # Composite
    "nevi_priority_score",
]

# Documentation for NaN columns: column -> (phase needed, description)
NAN_COLUMN_DOCS: dict[str, tuple[str, str]] = {
    "util_score": (
        "Phase 1 + 2 + 3 (all 100 counties)",
        "Cannot normalize without all 100 NC counties; "
        "requires min-max scaling across full state",
    ),
    "equity_justice40_pct": (
        "Phase 5 (CEJST)",
        "Percentage of census tracts designated as Justice40 disadvantaged communities",
    ),
    "equity_score": (
        "Phase 3 + Phase 5 (CEJST)",
        "Cannot compute without Justice40 data; "
        "Gini and zero-station metrics alone are insufficient",
    ),
    "nevi_priority_score": (
        "Phase 5",
        "Composite score = 0.40*Equity + 0.35*Utilization + "
        "0.25*Cost_Effectiveness; blocked until equity_score exists",
    ),
}


# =============================================================================
# DATA LOADING
# =============================================================================


def load_top10_counties(path: Path) -> pd.DataFrame:
    """Load Phase 3 top-10 counties with BEV registration counts.

    Args:
        path: Path to phase3-top10-counties.csv.

    Returns:
        DataFrame with County and BEV columns.
    """
    df = pd.read_csv(path)
    print(f"[INFO] Loaded {len(df)} counties from {path.name}")
    return df


def load_county_gini(path: Path) -> pd.DataFrame:
    """Load Phase 3 county-level Gini coefficients.

    Args:
        path: Path to phase3-county-gini.csv.

    Returns:
        DataFrame with county_name, county_fips, gini_weighted, total_ports.
    """
    df = pd.read_csv(path)
    print(f"[INFO] Loaded {len(df)} counties from {path.name}")
    return df


def load_zip_density(path: Path) -> pd.DataFrame:
    """Load Phase 3 ZIP-level charging density data.

    Args:
        path: Path to phase3-zip-density.csv.

    Returns:
        DataFrame with per-ZIP station/port counts and county mapping.
    """
    df = pd.read_csv(path)
    print(f"[INFO] Loaded {len(df)} ZIPs from {path.name}")
    return df


def load_top20_underserved(path: Path) -> pd.DataFrame:
    """Load Phase 3 top-20 underserved ZIPs.

    Args:
        path: Path to phase3-top20-underserved.csv.

    Returns:
        DataFrame with underserved ZIP details.
    """
    df = pd.read_csv(path)
    print(f"[INFO] Loaded {len(df)} underserved ZIPs from {path.name}")
    return df


def load_phase4_cost(path: Path) -> pd.DataFrame:
    """Load Phase 4 cost-effectiveness data (LEHD + ACS).

    Args:
        path: Path to phase4-cost-effectiveness.csv.

    Returns:
        DataFrame with cost sub-metric columns per county.
    """
    df = pd.read_csv(path)
    if "county_fips" in df.columns:
        df = df.drop(columns=["county_fips"])
    print(f"[INFO] Loaded {len(df)} counties from {path.name}")
    return df


# =============================================================================
# COMPUTATION
# =============================================================================


def compute_zero_station_pct(zip_density: pd.DataFrame) -> pd.DataFrame:
    """Compute percentage of ZIPs with zero stations per county.

    Args:
        zip_density: ZIP-level density DataFrame.

    Returns:
        DataFrame with county_name and zero_station_pct columns.
    """
    # Exclude uninhabited and pop-missing ZIPs for consistency
    eligible = zip_density[
        (~zip_density["uninhabited"]) & (~zip_density["pop_missing"])
    ].copy()

    county_groups = eligible.groupby("county_name")
    total_zips = county_groups.size().rename("total_zips")
    zero_zips = (
        county_groups["station_count"]
        .apply(lambda s: (s == 0).sum())
        .rename("zero_zips")
    )

    result = pd.DataFrame({"total_zips": total_zips, "zero_zips": zero_zips})
    result["zero_station_pct"] = result["zero_zips"] / result["total_zips"]

    return result[["zero_station_pct"]].reset_index()


def count_underserved_per_county(underserved: pd.DataFrame) -> pd.DataFrame:
    """Count top-20 underserved ZIPs per county.

    Args:
        underserved: Top-20 underserved ZIPs DataFrame.

    Returns:
        DataFrame with county_name and underserved_zips count.
    """
    counts = (
        underserved.groupby("county_name")
        .size()
        .rename("underserved_zips")
        .reset_index()
    )
    return counts


def build_skeleton(
    top10: pd.DataFrame,
    gini: pd.DataFrame,
    zip_density: pd.DataFrame,
    underserved: pd.DataFrame,
    phase4_cost: pd.DataFrame,
) -> pd.DataFrame:
    """Assemble the NEVI scoring framework skeleton table.

    Populates columns computable from Phase 3 and Phase 4 data, sets
    NaN for columns awaiting Phase 5.

    Args:
        top10: Top-10 counties with BEV counts.
        gini: County Gini coefficients.
        zip_density: ZIP-level density data.
        underserved: Top-20 underserved ZIPs.
        phase4_cost: Phase 4 cost-effectiveness sub-metrics.

    Returns:
        DataFrame with one row per county and all scoring columns.
    """
    # --- Identifiers + BEV counts from top-10 ---
    skeleton = top10.rename(columns={"County": "county_name", "BEV": "util_bev_count"})

    # --- Merge county_fips and total_ports from Gini table ---
    gini_cols = gini[["county_name", "county_fips", "total_ports", "gini_weighted"]]
    skeleton = skeleton.merge(gini_cols, on="county_name", how="left")

    # --- Utilization sub-metrics ---
    skeleton = skeleton.rename(columns={"total_ports": "util_total_ports"})
    skeleton["util_bev_per_port"] = (
        skeleton["util_bev_count"] / skeleton["util_total_ports"]
    )
    skeleton["util_forecast_buffer"] = FORECAST_BUFFER
    skeleton["util_score"] = np.nan
    skeleton["util_source"] = "Phase 1 + Phase 2 + Phase 3"

    # --- Cost-effectiveness sub-metrics (Phase 4) ---
    skeleton = skeleton.merge(phase4_cost, on="county_name", how="left")

    cost_cols = [
        "cost_commuter_demand",
        "cost_workplace_efficiency",
        "cost_pop_density",
    ]
    assert (
        skeleton[cost_cols].notna().all().all()
    ), "Phase 4 merge left NaN in cost columns"

    # Min-max normalize each sub-metric
    for col in cost_cols:
        col_min = skeleton[col].min()
        col_max = skeleton[col].max()
        if col_max != col_min:
            skeleton[f"{col}_norm"] = (
                (skeleton[col] - col_min) / (col_max - col_min)
            )
        else:
            skeleton[f"{col}_norm"] = 0.0

    # Equal-weight composite
    skeleton["cost_score"] = (
        skeleton["cost_commuter_demand_norm"]
        + skeleton["cost_workplace_efficiency_norm"]
        + skeleton["cost_pop_density_norm"]
    ) / 3.0

    # Drop temporary norm columns
    skeleton = skeleton.drop(
        columns=[c for c in skeleton.columns if c.endswith("_norm")]
    )

    skeleton["cost_source"] = "Phase 4 (LEHD + ACS)"

    # --- Equity sub-metrics ---
    # gini_weighted already merged above
    skeleton = skeleton.rename(columns={"gini_weighted": "equity_gini_weighted"})

    # Zero-station percentage
    zero_pct = compute_zero_station_pct(zip_density)
    skeleton = skeleton.merge(zero_pct, on="county_name", how="left")
    skeleton = skeleton.rename(columns={"zero_station_pct": "equity_zero_station_pct"})

    # Underserved ZIP counts
    underserved_counts = count_underserved_per_county(underserved)
    skeleton = skeleton.merge(underserved_counts, on="county_name", how="left")
    skeleton["underserved_zips"] = skeleton["underserved_zips"].fillna(0).astype(int)
    skeleton = skeleton.rename(columns={"underserved_zips": "equity_underserved_zips"})

    skeleton["equity_justice40_pct"] = np.nan
    skeleton["equity_score"] = np.nan
    skeleton["equity_source"] = "Phase 3 + Phase 5 (CEJST)"

    # --- Composite ---
    skeleton["nevi_priority_score"] = np.nan

    # Enforce column order
    skeleton = skeleton[OUTPUT_COLUMNS]

    return skeleton


# =============================================================================
# CONSOLE REPORTING
# =============================================================================


def print_skeleton_table(skeleton: pd.DataFrame) -> None:
    """Print the full skeleton table to console.

    Args:
        skeleton: The assembled scoring framework DataFrame.
    """
    print("\n" + "=" * 80)
    print("NEVI SCORING FRAMEWORK SKELETON TABLE")
    print("=" * 80)

    # Use pandas display options for readable output
    with pd.option_context(
        "display.max_columns",
        None,
        "display.width",
        120,
        "display.float_format",
        "{:.4f}".format,
        "display.max_colwidth",
        30,
    ):
        print(skeleton.to_string(index=False))


def print_column_status(skeleton: pd.DataFrame) -> None:
    """Print which columns are populated vs NaN.

    Args:
        skeleton: The assembled scoring framework DataFrame.
    """
    print("\n" + "-" * 80)
    print("COLUMN STATUS")
    print("-" * 80)

    populated = []
    nan_cols = []
    constant_cols = []

    # String/source columns are always populated
    source_cols = {"util_source", "cost_source", "equity_source"}

    for col in OUTPUT_COLUMNS:
        if col in source_cols:
            constant_cols.append(col)
        elif skeleton[col].dtype == object:
            populated.append(col)
        elif skeleton[col].isna().all():
            nan_cols.append(col)
        elif skeleton[col].notna().all():
            populated.append(col)
        else:
            populated.append(col)  # Partially populated counts as populated

    print(f"\n  POPULATED ({len(populated)} columns):")
    for col in populated:
        print(f"    - {col}")

    print(f"\n  SOURCE LABELS ({len(constant_cols)} columns):")
    for col in constant_cols:
        val = skeleton[col].iloc[0]
        print(f'    - {col} = "{val}"')

    print(f"\n  NaN / AWAITING DATA ({len(nan_cols)} columns):")
    for col in nan_cols:
        if col in NAN_COLUMN_DOCS:
            phase, desc = NAN_COLUMN_DOCS[col]
            print(f"    - {col}")
            print(f"      Needs: {phase}")
            print(f"      Why:   {desc}")
        else:
            print(f"    - {col}")

    total_data_cols = len(populated) + len(nan_cols)
    print(
        f"\n  SUMMARY: {len(populated)} of {total_data_cols} data columns "
        f"populated from Phase 3 + Phase 4 data"
    )


# =============================================================================
# MAIN
# =============================================================================


def main() -> None:
    """Build and export the NEVI scoring framework skeleton."""
    parser = argparse.ArgumentParser(
        description="Generate the NEVI scoring framework skeleton table."
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=OUTPUT_CSV,
        help=f"Output CSV path (default: {OUTPUT_CSV.relative_to(PROJECT_ROOT)})",
    )
    args = parser.parse_args()

    print("[INFO] Building NEVI scoring framework skeleton table")
    print(f"[INFO] Project root: {PROJECT_ROOT}")

    # --- Load source data ---
    print()
    top10 = load_top10_counties(TOP10_COUNTIES_CSV)
    gini = load_county_gini(COUNTY_GINI_CSV)
    zip_density = load_zip_density(ZIP_DENSITY_CSV)
    underserved = load_top20_underserved(TOP20_UNDERSERVED_CSV)
    phase4_cost = load_phase4_cost(PHASE4_COST_CSV)

    # --- Build skeleton ---
    skeleton = build_skeleton(
        top10, gini, zip_density, underserved, phase4_cost
    )

    # --- Save ---
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    skeleton.to_csv(output_path, index=False)
    print(f"\n[SUCCESS] Skeleton table saved to {output_path}")
    print(f"[INFO] Shape: {skeleton.shape[0]} counties x {skeleton.shape[1]} columns")

    # --- Console reporting ---
    print_skeleton_table(skeleton)
    print_column_status(skeleton)

    print("\n" + "=" * 80)
    print("SCORING EQUATION (for reference)")
    print("=" * 80)
    print(f"\n  NEVI Priority Score(county) = {WEIGHT_EQUITY:.2f} x Equity_Score")
    print(
        f"                               + {WEIGHT_UTILIZATION:.2f} x Utilization_Score"
    )
    print(
        f"                               + "
        f"{WEIGHT_COST_EFFECTIVENESS:.2f} x Cost_Effectiveness_Score"
    )
    print(
        "\n  Status: Superseded by scoring_framework_final.py (Phase 5 CEJST implementation)\n"
    )


if __name__ == "__main__":
    main()
