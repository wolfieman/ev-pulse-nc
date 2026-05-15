#!/usr/bin/env python3
"""
Phase 3 Step 3: Map AFDC Stations to Urban ZIPs in Top 10 NC Counties.

Assigns each AFDC charging station to a county via spatial join (point-in-
polygon), selects the top 10 counties by BEV registration count, filters
to ZIPs within those counties, and joins Census ZCTA population data.
Produces three analysis-ready CSVs for downstream Steps 4-9.

Author: Wolfgang Sanyer
License: Polyform Noncommercial 1.0.0 (see LICENSE)
Date: 2026
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

# ---------------------------------------------------------------------------
# Resolve project paths so the sibling module import works
# ---------------------------------------------------------------------------
_SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPT_DIR))

# =============================================================================
# MODULE-LEVEL CONSTANTS
# =============================================================================

PROJECT_ROOT = _SCRIPT_DIR.parent.parent.parent

AFDC_CSV = (
    PROJECT_ROOT / "data" / "raw" / "afdc-charging-stations-connector-2026-02.csv"
)
CENSUS_ZIP_CSV = PROJECT_ROOT / "data" / "raw" / "nc-zip-population-acs2022.csv"
NC_BOUNDARIES = PROJECT_ROOT / "data" / "raw" / "nc-county-boundaries.geojson"
BEV_REG_CSV = PROJECT_ROOT / "data" / "processed" / "nc-ev-registrations-2025.csv"

PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

# ZIPs to exclude (non-NC stations present in the NC AFDC extract)
NON_NC_ZIPS = {"20020", "39817"}

# Number of top counties to select (demand-side ranking)
TOP_N_COUNTIES = 10


# =============================================================================
# DATA LOADING
# =============================================================================


def load_afdc(path: Path) -> pd.DataFrame:
    """Load the AFDC charging station CSV.

    Args:
        path: Path to the AFDC CSV file.

    Returns:
        DataFrame with basic type casts applied.
    """
    df = pd.read_csv(path, dtype={"zip": str})
    df["zip"] = df["zip"].astype(str).str.zfill(5)
    for col in ("ev_level1_evse_num", "ev_level2_evse_num", "ev_dc_fast_num"):
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)
    df["total_ports"] = (
        df["ev_level1_evse_num"] + df["ev_level2_evse_num"] + df["ev_dc_fast_num"]
    )
    return df


def load_census(path: Path) -> pd.DataFrame:
    """Load the Census ZCTA population CSV.

    Args:
        path: Path to the Census CSV file.

    Returns:
        DataFrame with columns [name, population, zcta].
    """
    df = pd.read_csv(path, dtype={"zcta": str})
    df["zcta"] = df["zcta"].astype(str).str.zfill(5)
    df["population"] = df["population"].astype(int)
    return df


def load_county_boundaries(path: Path) -> gpd.GeoDataFrame:
    """Load NC county boundary polygons.

    Args:
        path: Path to the GeoJSON file.

    Returns:
        GeoDataFrame of county boundaries.
    """
    return gpd.read_file(path)


def load_bev_registrations(path: Path) -> pd.DataFrame:
    """Load BEV registration data and return latest-month county totals.

    Args:
        path: Path to the registration CSV.

    Returns:
        DataFrame with columns [County, BEV] for the most recent month.
    """
    df = pd.read_csv(path)
    latest_date = df["Date"].max()
    latest = df[df["Date"] == latest_date][["County", "BEV"]].copy()
    latest = latest.sort_values("BEV", ascending=False).reset_index(drop=True)
    return latest


# =============================================================================
# PROCESSING
# =============================================================================


def filter_nc_stations(df: pd.DataFrame) -> pd.DataFrame:
    """Remove non-NC stations identified by ZIP code.

    Args:
        df: Full AFDC DataFrame.

    Returns:
        Filtered DataFrame with only NC stations.
    """
    mask = ~df["zip"].isin(NON_NC_ZIPS)
    excluded = df[~mask]
    if len(excluded) > 0:
        print(f"  Excluding {len(excluded)} non-NC stations (ZIPs: {NON_NC_ZIPS})")
        for _, row in excluded.iterrows():
            print(
                f"    ID {row['id']}: ZIP {row['zip']}, "
                f"lat={row['latitude']:.4f}, lon={row['longitude']:.4f}"
            )
    return df[mask].copy()


def spatial_join_county(
    stations: pd.DataFrame, counties: gpd.GeoDataFrame
) -> pd.DataFrame:
    """Assign each station to a county via point-in-polygon spatial join.

    Args:
        stations: DataFrame with latitude and longitude columns.
        counties: GeoDataFrame of county boundary polygons.

    Returns:
        Stations DataFrame with county_name and county_fips columns added.
    """
    # Create GeoDataFrame from station coordinates
    gdf_stations = gpd.GeoDataFrame(
        stations,
        geometry=gpd.points_from_xy(stations["longitude"], stations["latitude"]),
        crs="EPSG:4326",
    )

    # Ensure counties have a compatible CRS (GeoJSON is EPSG:4269, but
    # the difference from EPSG:4326 is sub-meter at NC latitude — negligible)
    if counties.crs and counties.crs.to_epsg() != 4326:
        counties = counties.to_crs("EPSG:4326")

    # Spatial join: assign each point to the polygon it falls within
    joined = gpd.sjoin(
        gdf_stations,
        counties[["NAME", "GEOID", "geometry"]],
        how="left",
        predicate="within",
    )

    # Rename and clean up
    joined = joined.rename(columns={"NAME": "county_name", "GEOID": "county_fips"})
    joined = joined.drop(columns=["geometry", "index_right"], errors="ignore")

    # Convert back to plain DataFrame
    result = pd.DataFrame(joined)

    return result


def select_top_counties(bev_df: pd.DataFrame, n: int = TOP_N_COUNTIES) -> pd.DataFrame:
    """Select top N counties by BEV registration count.

    Args:
        bev_df: DataFrame with County and BEV columns.
        n: Number of top counties to select.

    Returns:
        DataFrame of top N counties with BEV counts.
    """
    return bev_df.head(n).copy()


def filter_urban_zips(
    stations: pd.DataFrame, top_counties: pd.DataFrame
) -> pd.DataFrame:
    """Filter stations to those in ZIPs within top N counties.

    Args:
        stations: Station DataFrame with county_name column.
        top_counties: Top counties DataFrame with County column.

    Returns:
        Filtered stations DataFrame.
    """
    top_names = set(top_counties["County"].str.strip())
    mask = stations["county_name"].str.strip().isin(top_names)
    return stations[mask].copy()


def join_census_population(
    stations: pd.DataFrame, census: pd.DataFrame
) -> pd.DataFrame:
    """Join Census ZCTA population onto station data.

    Args:
        stations: Station DataFrame with zip column.
        census: Census DataFrame with zcta and population columns.

    Returns:
        Stations DataFrame with population column added.
    """
    merged = stations.merge(
        census[["zcta", "population"]],
        left_on="zip",
        right_on="zcta",
        how="left",
    )
    merged = merged.drop(columns=["zcta"], errors="ignore")
    return merged


# =============================================================================
# OUTPUT
# =============================================================================


def write_station_county_mapping(df: pd.DataFrame, out_dir: Path) -> Path:
    """Write all NC stations with county assignments.

    Args:
        df: Station DataFrame with county columns.
        out_dir: Output directory.

    Returns:
        Path to the written CSV.
    """
    cols = [
        "id",
        "station_name",
        "city",
        "zip",
        "latitude",
        "longitude",
        "county_name",
        "county_fips",
        "ev_level1_evse_num",
        "ev_level2_evse_num",
        "ev_dc_fast_num",
        "total_ports",
        "ev_network",
        "access_code",
    ]
    out_cols = [c for c in cols if c in df.columns]
    path = out_dir / "phase3-station-county-mapping.csv"
    df[out_cols].to_csv(path, index=False)
    return path


def write_top10_counties(df: pd.DataFrame, out_dir: Path) -> Path:
    """Write top 10 counties CSV.

    Args:
        df: Top counties DataFrame.
        out_dir: Output directory.

    Returns:
        Path to the written CSV.
    """
    path = out_dir / "phase3-top10-counties.csv"
    df.to_csv(path, index=False)
    return path


def write_urban_zip_stations(df: pd.DataFrame, out_dir: Path) -> Path:
    """Write the analysis-ready urban ZIP stations dataset.

    Args:
        df: Filtered and joined station DataFrame.
        out_dir: Output directory.

    Returns:
        Path to the written CSV.
    """
    cols = [
        "id",
        "station_name",
        "city",
        "zip",
        "latitude",
        "longitude",
        "county_name",
        "county_fips",
        "ev_level1_evse_num",
        "ev_level2_evse_num",
        "ev_dc_fast_num",
        "total_ports",
        "ev_network",
        "access_code",
        "population",
    ]
    out_cols = [c for c in cols if c in df.columns]
    path = out_dir / "phase3-urban-zip-stations.csv"
    df[out_cols].to_csv(path, index=False)
    return path


# =============================================================================
# SUMMARY
# =============================================================================


def print_summary(
    raw_count: int,
    nc_stations: pd.DataFrame,
    top_counties: pd.DataFrame,
    urban_stations: pd.DataFrame,
    census: pd.DataFrame,
) -> None:
    """Print a clear summary of the mapping pipeline results.

    Args:
        raw_count: Original number of rows in AFDC file.
        nc_stations: NC-only stations with county assignments.
        top_counties: Top 10 counties DataFrame.
        urban_stations: Filtered urban ZIP stations with population.
        census: Census ZCTA DataFrame.
    """
    sep = "=" * 70
    print(f"\n{sep}")
    print("PHASE 3 STEP 3: ZIP MAPPING SUMMARY")
    print(sep)

    # Station counts
    print("\n1. STATION FILTERING")
    print(f"   Raw AFDC rows:       {raw_count:,}")
    print(f"   After NC filter:     {len(nc_stations):,}")

    # County assignment
    mapped = nc_stations["county_name"].notna().sum()
    unmapped = nc_stations["county_name"].isna().sum()
    n_counties = nc_stations["county_name"].dropna().nunique()
    print("\n2. COUNTY SPATIAL JOIN")
    print(f"   Mapped to a county:  {mapped:,}")
    print(f"   Unmapped (no match): {unmapped:,}")
    print(f"   Unique counties:     {n_counties}")

    # Top 10
    print(f"\n3. TOP {TOP_N_COUNTIES} COUNTIES BY BEV REGISTRATION")
    for _, row in top_counties.iterrows():
        print(f"   {row['County']:20s} {row['BEV']:,} BEVs")

    # Urban ZIPs
    n_zips = urban_stations["zip"].nunique()
    n_stations = len(urban_stations)
    total_ports = urban_stations["total_ports"].sum()
    print("\n4. URBAN ZIP FILTER (Top 10 counties)")
    print(f"   Unique ZIPs:         {n_zips}")
    print(f"   Stations:            {n_stations:,}")
    print(f"   Total ports:         {total_ports:,}")

    # Census join
    pop_matched = urban_stations["population"].notna().sum()
    pop_unmatched = urban_stations["population"].isna().sum()
    unmatched_zips = urban_stations.loc[
        urban_stations["population"].isna(), "zip"
    ].unique()
    print("\n5. CENSUS POPULATION JOIN")
    print(f"   Stations with pop:   {pop_matched:,}")
    print(f"   Stations w/o pop:    {pop_unmatched:,}")
    if len(unmatched_zips) > 0:
        print(f"   Unmatched ZIPs (PO Box / non-ZCTA): {list(unmatched_zips)}")

    # Uninhabited ZCTAs
    urban_zips = set(urban_stations["zip"].unique())
    census_in_scope = census[census["zcta"].isin(urban_zips)]
    uninhabited = census_in_scope[census_in_scope["population"] == 0]
    if len(uninhabited) > 0:
        print(
            f"   Uninhabited ZCTAs (pop=0) in scope: {len(uninhabited)}"
            f" -- retained but flagged for per-capita exclusion"
        )
        for _, row in uninhabited.iterrows():
            print(f"     ZCTA {row['zcta']}: {row['name']}")

    print(f"\n{sep}")
    print("PIPELINE COMPLETE.")
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
        description=(
            "Phase 3 Step 3: Map AFDC stations to urban ZIPs in top 10 NC counties"
        )
    )
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
        "--bev-csv",
        type=Path,
        default=BEV_REG_CSV,
        help="Path to BEV registration CSV",
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
        default=TOP_N_COUNTIES,
        help="Number of top counties to select",
    )
    return parser.parse_args()


def main() -> None:
    """Entry point: load data, map stations, produce outputs."""
    args = parse_args()
    args.processed_dir.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------
    # 1. Load data
    # ------------------------------------------------------------------
    print("Loading AFDC data ...")
    afdc = load_afdc(args.afdc_csv)
    raw_count = len(afdc)
    print(f"  Loaded {raw_count:,} rows.")

    print("\nLoading Census ZCTA population ...")
    census = load_census(args.census_csv)
    print(f"  Loaded {len(census):,} ZCTAs.")

    print("\nLoading county boundaries ...")
    counties = load_county_boundaries(args.nc_geo)
    print(f"  Loaded {len(counties)} county polygons (CRS: {counties.crs}).")

    print("\nLoading BEV registrations ...")
    bev_latest = load_bev_registrations(args.bev_csv)
    print(f"  Loaded {len(bev_latest):,} counties.")

    # ------------------------------------------------------------------
    # 2. Filter non-NC stations
    # ------------------------------------------------------------------
    print("\nFiltering non-NC stations ...")
    nc_stations = filter_nc_stations(afdc)
    print(f"  NC stations: {len(nc_stations):,}")

    # ------------------------------------------------------------------
    # 3. Spatial join: station → county
    # ------------------------------------------------------------------
    print("\nPerforming spatial join (station -> county) ...")
    nc_stations = spatial_join_county(nc_stations, counties)
    mapped = nc_stations["county_name"].notna().sum()
    print(f"  Mapped {mapped:,} of {len(nc_stations):,} stations to counties.")

    # ------------------------------------------------------------------
    # 4. Select top 10 counties by BEV count
    # ------------------------------------------------------------------
    print(f"\nSelecting top {args.top_n} counties by BEV registration ...")
    top_counties = select_top_counties(bev_latest, n=args.top_n)
    for _, row in top_counties.iterrows():
        print(f"  {row['County']:20s} {row['BEV']:>6,} BEVs")

    # ------------------------------------------------------------------
    # 5. Filter to urban ZIPs within top 10 counties
    # ------------------------------------------------------------------
    print("\nFiltering to urban ZIPs within top counties ...")
    urban_stations = filter_urban_zips(nc_stations, top_counties)
    n_zips = urban_stations["zip"].nunique()
    print(f"  {len(urban_stations):,} stations in {n_zips} ZIPs.")

    # ------------------------------------------------------------------
    # 6. Join Census population
    # ------------------------------------------------------------------
    print("\nJoining Census ZCTA population ...")
    urban_stations = join_census_population(urban_stations, census)
    pop_matched = urban_stations["population"].notna().sum()
    pop_unmatched = urban_stations["population"].isna().sum()
    print(f"  Population matched: {pop_matched:,}")
    print(f"  Population unmatched: {pop_unmatched:,}")

    # ------------------------------------------------------------------
    # 7. Write outputs
    # ------------------------------------------------------------------
    print("\nWriting output CSVs ...")

    p = write_station_county_mapping(nc_stations, args.processed_dir)
    print(f"  {p.name}")

    p = write_top10_counties(top_counties, args.processed_dir)
    print(f"  {p.name}")

    p = write_urban_zip_stations(urban_stations, args.processed_dir)
    print(f"  {p.name}")

    # ------------------------------------------------------------------
    # 8. Summary
    # ------------------------------------------------------------------
    print_summary(raw_count, nc_stations, top_counties, urban_stations, census)


if __name__ == "__main__":
    main()
