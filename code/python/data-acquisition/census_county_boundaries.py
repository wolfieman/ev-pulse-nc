#!/usr/bin/env python3
"""
Census County Boundaries Download - EV Pulse NC
================================================
Downloads NC county boundary geometries from the US Census Bureau
cartographic boundary files for spatial joins.

Usage:
    py code/python/data-acquisition/census_county_boundaries.py

Requires:
    - geopandas library (pip install geopandas)

Output:
    data/raw/nc-county-boundaries.geojson
"""

import os
import sys
from datetime import datetime

import geopandas as gpd

# Census Bureau cartographic boundary file (500k resolution, 2020 vintage)
BOUNDARY_URL = (
    "https://www2.census.gov/geo/tiger/GENZ2020/shp/cb_2020_us_county_500k.zip"
)

# NC state FIPS code
NC_FIPS = "37"

# Output path
REPO_ROOT = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
OUTPUT_FILE = os.path.join(REPO_ROOT, "data", "raw", "nc-county-boundaries.geojson")


def download_boundaries():
    """Download US county boundaries and filter to North Carolina."""
    print("[INFO] Downloading US county boundaries from Census Bureau...")
    print(f"[INFO] URL: {BOUNDARY_URL}")
    print("[INFO] This may take a moment (downloading ~30 MB shapefile)...")

    try:
        gdf = gpd.read_file(BOUNDARY_URL)
    except Exception as e:
        print(f"[ERROR] Failed to download boundaries: {e}")
        sys.exit(1)

    print(f"[INFO] Downloaded {len(gdf)} US counties")

    # Filter to NC
    nc_counties = gdf[gdf["STATEFP"] == NC_FIPS].copy()
    print(f"[INFO] Filtered to {len(nc_counties)} NC counties")

    if len(nc_counties) == 0:
        print("[ERROR] No NC counties found. Check FIPS filter.")
        sys.exit(1)

    return nc_counties


def save_geojson(gdf, output_path):
    """Save GeoDataFrame as GeoJSON."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    gdf.to_file(output_path, driver="GeoJSON")
    print(f"[SUCCESS] Saved {len(gdf)} counties to {output_path}")


def sanity_check(gdf):
    """Print summary statistics for verification."""
    print("\n--- Sanity Check ---")
    print(f"Total counties: {len(gdf)}")
    print(f"Geometry type: {gdf.geometry.geom_type.unique().tolist()}")
    print(f"CRS: {gdf.crs}")
    print(f"\nColumns: {list(gdf.columns)}")

    if "NAME" in gdf.columns:
        names = sorted(gdf["NAME"].tolist())
        print(f"\nFirst 10 counties: {names[:10]}")
        print(f"Last 10 counties: {names[-10:]}")

    if "COUNTYFP" in gdf.columns:
        print(f"FIPS codes range: {gdf['COUNTYFP'].min()} - {gdf['COUNTYFP'].max()}")

    if len(gdf) == 100:
        print("\n[OK] County count matches expected 100 NC counties")
    else:
        print(f"\n[WARNING] Expected 100 counties, got {len(gdf)}")


def main():
    print("=" * 60)
    print("Census County Boundaries Download - EV Pulse NC")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)

    nc_counties = download_boundaries()
    save_geojson(nc_counties, OUTPUT_FILE)
    sanity_check(nc_counties)

    print(f"\n[DONE] Output: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
