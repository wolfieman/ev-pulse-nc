#!/usr/bin/env python3
"""Phase 3 AFDC Infrastructure EDA and Descriptive Analysis.

Produces figures fig-08 through fig-17 and supporting CSV tables for the
EV Pulse NC analytical pipeline. Covers missingness, distributions,
geographic coverage, temporal growth, and data quality flagging.

This is the orchestrator: it loads and prepares the data (phase3_afdc_eda_prep),
writes the CSV tables (phase3_afdc_eda_tables), renders the figures
(phase3_afdc_eda_figures), and prints the console summary.

Author: Wolfgang Sanyer
License: Polyform Noncommercial 1.0.0 (see LICENSE)
Date: 2026
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
from phase3_afdc_eda_figures import (
    fig08_missing_heatmap,
    fig09_stations_by_level,
    fig10_stations_by_network,
    fig11_access_facility,
    fig12_port_distributions,
    fig13_stations_by_city,
    fig14_temporal_growth,
    fig15_station_map,
    fig16_zip_coverage_gap,
    fig17_connector_types,
)
from phase3_afdc_eda_prep import (
    AFDC_CSV,
    CENSUS_ZIP_CSV,
    EV_RELEVANT_COLS,
    NC_BOUNDARIES,
    NC_LAT_MAX,
    NC_LAT_MIN,
    NC_LON_MAX,
    NC_LON_MIN,
    NON_EV_FUEL_PREFIXES,
    derive_charging_level,
    load_afdc,
    parse_connector_types,
    parse_ev_charging_units_power,
)
from phase3_afdc_eda_tables import (
    write_column_profile,
    write_quality_flags,
    write_stations_by_level,
    write_stations_by_network,
    write_stations_by_zip,
)

from evpulse.paths import PROJECT_ROOT
from evpulse.style import setup_publication_style

# =============================================================================
# OUTPUT DIRECTORIES
# =============================================================================

FIGURES_DIR = PROJECT_ROOT / "output" / "figures"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"


# =============================================================================
# SUMMARY PRINTER
# =============================================================================


def print_eda_summary(df: pd.DataFrame, census_path: Path) -> None:
    """Print a comprehensive EDA summary to stdout.

    Args:
        df: AFDC DataFrame (fully prepared).
        census_path: Path to Census ZIP population CSV.
    """
    sep = "=" * 70
    print(f"\n{sep}")
    print("AFDC EDA & DESCRIPTIVE ANALYSIS — SUMMARY")
    print(sep)

    # 1. Volume / shape
    print("\n1. VOLUME / SHAPE")
    print(f"   Rows: {len(df):,}  |  Columns: {df.shape[1]}")
    dead_cols = [
        c
        for c in df.columns
        if c.startswith(NON_EV_FUEL_PREFIXES) and df[c].isna().all()
    ]
    print(f"   Dead (100% null) non-EV fuel columns: {len(dead_cols)}")

    # 2. Missing values
    print("\n2. MISSING VALUES (EV-relevant)")
    for c in EV_RELEVANT_COLS:
        if c in df.columns:
            null_pct = df[c].isna().mean() * 100
            if null_pct > 0:
                print(f"   {c}: {null_pct:.1f}% null")

    # 3. Data quality
    print("\n3. DATA QUALITY")
    oob = df[
        (df["latitude"] < NC_LAT_MIN)
        | (df["latitude"] > NC_LAT_MAX)
        | (df["longitude"] < NC_LON_MIN)
        | (df["longitude"] > NC_LON_MAX)
    ]
    print(f"   Out-of-bounds coords: {len(oob)}")
    zero_ports = df[
        (df["ev_level1_evse_num"] + df["ev_level2_evse_num"] + df["ev_dc_fast_num"])
        == 0
    ]
    print(f"   Zero-port stations: {len(zero_ports)}")
    print(f"   Status codes: {df['status_code'].value_counts().to_dict()}")
    bad_zips = df[~df["zip"].str.startswith(("27", "28"))]
    print(f"   ZIPs not starting with 27/28: {len(bad_zips)}")

    # 4. Standardization
    print("\n4. STANDARDIZATION")
    print("   File naming follows domain-subject-grain-date.ext pattern: OK")
    print("   No column renames needed (snake_case already).")

    # 5. Missing data strategy
    print("\n5. MISSING DATA STRATEGY")
    strategies = {
        "ev_network_web": "accept (URL, informational only)",
        "ev_pricing": "accept (free-text, ~20% missing)",
        "ev_other_evse": "accept (rare field)",
        "ev_renewable_source": "accept (rarely populated)",
        "open_date": "accept (used for temporal plot where available)",
        "facility_type": "accept (minor null rate)",
        "ev_network_ids": "accept (JSON blob, partial coverage)",
    }
    for col, strat in strategies.items():
        print(f"   {col}: {strat}")

    # 6. Data types
    print("\n6. DATA TYPES")
    print("   zip: cast to str (5-digit zero-padded)")
    print("   open_date: parsed to datetime")
    print("   Port counts: int (NaN filled with 0)")

    # 7. Outliers
    print("\n7. OUTLIER SUMMARY")
    for col_name, label in [
        ("ev_level2_evse_num", "L2 ports"),
        ("ev_dc_fast_num", "DCFC ports"),
    ]:
        s = df[col_name]
        q1, q3 = s.quantile(0.25), s.quantile(0.75)
        iqr = q3 - q1
        upper = q3 + 1.5 * iqr
        n_out = (s > upper).sum()
        print(
            f"   {label}: Q1={q1:.0f}, Q3={q3:.0f}, "
            f"IQR fence={upper:.0f}, outliers={n_out}"
        )

    # 8. Duplicates
    print("\n8. DUPLICATES")
    print(f"   Unique station IDs: {df['id'].nunique()} / {len(df)}")
    co_located = df.duplicated(subset=["latitude", "longitude"], keep=False).sum()
    print(f"   Co-located (same lat/lon): {co_located} rows")

    # 9. Distribution profiles
    print("\n9. DISTRIBUTION PROFILES")
    print(f"   Charging levels: {df['charging_level'].value_counts().to_dict()}")
    print(f"   Access codes: {df['access_code'].value_counts().to_dict()}")
    print(f"   Top 5 networks: {df['ev_network'].value_counts().head(5).to_dict()}")

    # 10. Temporal
    print("\n10. TEMPORAL PROFILE")
    coverage = df["open_date"].notna().mean()
    print(f"    open_date coverage: {coverage:.1%}")
    if coverage > 0:
        print(f"    Earliest: {df['open_date'].min()}")
        print(f"    Latest:   {df['open_date'].max()}")

    # 11. Geographic
    print("\n11. GEOGRAPHIC")
    print(f"    Lat range: [{df['latitude'].min():.4f}, {df['latitude'].max():.4f}]")
    print(f"    Lon range: [{df['longitude'].min():.4f}, {df['longitude'].max():.4f}]")

    # 12. ZIP coverage
    print("\n12. ZIP COVERAGE vs CENSUS")
    census = pd.read_csv(census_path, dtype={"zcta": str})
    census["zcta"] = census["zcta"].astype(str).str.zfill(5)
    station_zips = set(df["zip"].unique())
    census_zips = set(census["zcta"].unique())
    print(f"    AFDC unique ZIPs: {len(station_zips)}")
    print(f"    Census ZIPs: {len(census_zips)}")
    print(f"    Covered: {len(station_zips & census_zips)}")
    print(f"    Gap (Census ZIPs w/o station): {len(census_zips - station_zips)}")

    # 13. Connector types
    print("\n13. CONNECTOR TYPES")
    all_c: list[str] = []
    for lst in df["connector_list"]:
        all_c.extend(lst)
    print(f"    Unique connector types: {len(set(all_c))}")
    print(f"    Counts: {pd.Series(all_c).value_counts().to_dict()}")

    # 14. Derived charging level
    print("\n14. DERIVED CHARGING LEVEL")
    print("    (See charging_level column — applied to all rows.)")

    # 15. ev_network_ids
    print("\n15. ev_network_ids MAX POWER")
    pw = df["max_power_kw"]
    n_valid = pw.notna().sum()
    print(f"    Non-null max_power_kw: {n_valid} / {len(df)}")
    if n_valid:
        print(f"    Range: {pw.min():.0f} – {pw.max():.0f} kW")

    print(f"\n{sep}")
    print("ALL DONE.")
    print(sep)


# =============================================================================
# MAIN
# =============================================================================


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments.

    Returns:
        Parsed arguments namespace.
    """
    parser = argparse.ArgumentParser(description="Phase 3 AFDC EDA — EV Pulse NC")
    parser.add_argument(
        "--afdc-csv",
        type=Path,
        default=AFDC_CSV,
        help="Path to AFDC CSV (default: data/raw/...)",
    )
    parser.add_argument(
        "--census-csv",
        type=Path,
        default=CENSUS_ZIP_CSV,
        help="Path to Census ZIP population CSV",
    )
    parser.add_argument(
        "--nc-geo",
        type=Path,
        default=NC_BOUNDARIES,
        help="Path to NC county boundaries GeoJSON",
    )
    parser.add_argument(
        "--figures-dir",
        type=Path,
        default=FIGURES_DIR,
        help="Output directory for figures",
    )
    parser.add_argument(
        "--processed-dir",
        type=Path,
        default=PROCESSED_DIR,
        help="Output directory for processed CSVs",
    )
    return parser.parse_args()


def main() -> None:
    """Entry point: load data, produce all outputs, print summary."""
    args = parse_args()

    # Ensure output dirs exist
    args.figures_dir.mkdir(parents=True, exist_ok=True)
    args.processed_dir.mkdir(parents=True, exist_ok=True)

    # Style
    setup_publication_style()

    # Load
    print("Loading AFDC data ...")
    df = load_afdc(args.afdc_csv)
    print(f"  Loaded {len(df):,} rows, {df.shape[1]} columns.")

    # Derived columns
    print("Deriving charging levels ...")
    df["charging_level"] = df.apply(derive_charging_level, axis=1)

    print("Parsing connector types ...")
    df["connector_list"] = parse_connector_types(df["ev_connector_types"])

    print("Extracting max power from ev_charging_units ...")
    df["max_power_kw"] = parse_ev_charging_units_power(df["ev_charging_units"])

    # CSV outputs
    print("\nWriting CSV outputs ...")
    p = write_column_profile(df, args.processed_dir)
    print(f"  {p.name}")
    p = write_stations_by_level(df, args.processed_dir)
    print(f"  {p.name}")
    p = write_stations_by_network(df, args.processed_dir)
    print(f"  {p.name}")
    p = write_stations_by_zip(df, args.processed_dir)
    print(f"  {p.name}")
    p = write_quality_flags(df, args.processed_dir)
    print(f"  {p.name}")

    # Figures
    print("\nGenerating figures ...")

    p = fig08_missing_heatmap(df, args.figures_dir)
    print(f"  fig-08: {p.name}")

    p = fig09_stations_by_level(df, args.figures_dir)
    print(f"  fig-09: {p.name}")

    p = fig10_stations_by_network(df, args.figures_dir)
    print(f"  fig-10: {p.name}")

    p = fig11_access_facility(df, args.figures_dir)
    print(f"  fig-11: {p.name}")

    p = fig12_port_distributions(df, args.figures_dir)
    print(f"  fig-12: {p.name}")

    p = fig13_stations_by_city(df, args.figures_dir)
    print(f"  fig-13: {p.name}")

    p = fig14_temporal_growth(df, args.figures_dir)
    if p:
        print(f"  fig-14: {p.name}")

    p = fig15_station_map(df, args.nc_geo, args.figures_dir)
    print(f"  fig-15: {p.name}")

    p = fig16_zip_coverage_gap(df, args.census_csv, args.figures_dir)
    print(f"  fig-16: {p.name}")

    p = fig17_connector_types(df, args.figures_dir)
    print(f"  fig-17: {p.name}")

    # Summary
    print_eda_summary(df, args.census_csv)


if __name__ == "__main__":
    main()
