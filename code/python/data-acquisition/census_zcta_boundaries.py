#!/usr/bin/env python3
"""
Census ZCTA Boundaries Download - EV Pulse NC
==============================================
Downloads ZCTA (ZIP Code Tabulation Area) boundary geometries from the
US Census Bureau cartographic boundary files, filtered to the North
Carolina region using a spatial bounding-box approach.

Usage:
    py code/python/data-acquisition/census_zcta_boundaries.py

Requires:
    - geopandas library (pip install geopandas)

Output:
    data/raw/nc-zcta-boundaries.geojson

Author: Wolfgang Sanyer
License: Polyform Noncommercial 1.0.0 (see LICENSE)
"""

import os
import sys
from datetime import datetime

import geopandas as gpd

# Census Bureau ZCTA cartographic boundary file (500k resolution, 2020)
ZCTA_URL = (
    "https://www2.census.gov/geo/tiger/GENZ2020/shp/"
    "cb_2020_us_zcta520_500k.zip"
)

# Bounding-box buffer in degrees (~0.1 deg ~ 11 km)
BBOX_BUFFER_DEG = 0.1

# Expected ZCTA count range for NC region
EXPECTED_MIN = 700
EXPECTED_MAX = 900

# Paths
REPO_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )
    )
)
NC_COUNTY_FILE = os.path.join(
    REPO_ROOT, "data", "raw", "nc-county-boundaries.geojson"
)
OUTPUT_FILE = os.path.join(
    REPO_ROOT, "data", "raw", "nc-zcta-boundaries.geojson"
)


def load_nc_bbox():
    """Load NC county boundaries and return a buffered bounding box."""
    print(f"[INFO] Loading NC county boundaries from {NC_COUNTY_FILE}")

    if not os.path.exists(NC_COUNTY_FILE):
        print(
            "[ERROR] NC county boundaries not found. "
            "Run census_county_boundaries.py first."
        )
        sys.exit(1)

    nc_counties = gpd.read_file(NC_COUNTY_FILE)
    print(f"[INFO] Loaded {len(nc_counties)} NC counties")

    minx, miny, maxx, maxy = nc_counties.total_bounds
    minx -= BBOX_BUFFER_DEG
    miny -= BBOX_BUFFER_DEG
    maxx += BBOX_BUFFER_DEG
    maxy += BBOX_BUFFER_DEG

    print(
        f"[INFO] NC bounding box (buffered {BBOX_BUFFER_DEG} deg): "
        f"({minx:.2f}, {miny:.2f}, {maxx:.2f}, {maxy:.2f})"
    )

    return minx, miny, maxx, maxy


def download_zcta_boundaries(bbox):
    """Download national ZCTA boundaries and filter to NC region."""
    minx, miny, maxx, maxy = bbox

    print("[INFO] Downloading US ZCTA boundaries from Census Bureau...")
    print(f"[INFO] URL: {ZCTA_URL}")
    print(
        "[INFO] This may take a moment (downloading ~80 MB shapefile)..."
    )

    try:
        gdf = gpd.read_file(ZCTA_URL)
    except Exception as e:
        print(f"[ERROR] Failed to download ZCTA boundaries: {e}")
        sys.exit(1)

    print(f"[INFO] Downloaded {len(gdf)} US ZCTAs")

    # Filter ZCTAs whose centroid falls within the NC bounding box
    centroids = gdf.geometry.centroid
    mask = (
        (centroids.x >= minx)
        & (centroids.x <= maxx)
        & (centroids.y >= miny)
        & (centroids.y <= maxy)
    )
    nc_zctas = gdf[mask].copy()
    print(f"[INFO] Filtered to {len(nc_zctas)} NC-area ZCTAs")

    if len(nc_zctas) == 0:
        print("[ERROR] No ZCTAs found in NC region. Check bounding box.")
        sys.exit(1)

    # Keep only ZCTA code and geometry
    nc_zctas = nc_zctas[["ZCTA5CE20", "geometry"]].copy()

    return nc_zctas


def save_geojson(gdf, output_path):
    """Save GeoDataFrame as GeoJSON."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    gdf.to_file(output_path, driver="GeoJSON")
    print(f"[SUCCESS] Saved {len(gdf)} ZCTAs to {output_path}")


def sanity_check(gdf):
    """Print summary statistics for verification."""
    print("\n--- Sanity Check ---")
    print(f"Total ZCTAs: {len(gdf)}")
    print(
        f"Geometry type: {gdf.geometry.geom_type.unique().tolist()}"
    )
    print(f"CRS: {gdf.crs}")
    print(f"\nColumns: {list(gdf.columns)}")

    if "ZCTA5CE20" in gdf.columns:
        codes = sorted(gdf["ZCTA5CE20"].tolist())
        print(f"\nFirst 10 ZCTAs: {codes[:10]}")
        print(f"Last 10 ZCTAs: {codes[-10:]}")

    if EXPECTED_MIN <= len(gdf) <= EXPECTED_MAX:
        print(
            f"\n[OK] ZCTA count ({len(gdf)}) is within expected "
            f"range ({EXPECTED_MIN}-{EXPECTED_MAX})"
        )
    else:
        print(
            f"\n[WARNING] Expected {EXPECTED_MIN}-{EXPECTED_MAX} "
            f"ZCTAs, got {len(gdf)}"
        )


def main():
    print("=" * 60)
    print("Census ZCTA Boundaries Download - EV Pulse NC")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)

    bbox = load_nc_bbox()
    nc_zctas = download_zcta_boundaries(bbox)
    save_geojson(nc_zctas, OUTPUT_FILE)
    sanity_check(nc_zctas)

    print(f"\n[DONE] Output: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
