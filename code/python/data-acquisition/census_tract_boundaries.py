#!/usr/bin/env python3
"""
Census 2010 Tract Boundaries Download - EV Pulse NC
====================================================
Downloads 2010 TIGER/Line tract shapefiles for NC and four border
states (GA, SC, TN, VA), merges into a single GeoJSON for the
tract-to-ZCTA spatial crosswalk in Phase 5.

Source: Census TIGER FTP
    https://www2.census.gov/geo/tiger/TIGER2010/TRACT/2010/

Usage:
    uv run code/python/data-acquisition/census_tract_boundaries.py

Output:
    data/raw/census-tracts-2010-study-area.geojson

Author: Wolfgang Sanyer
License: Polyform Noncommercial 1.0.0 (see LICENSE)
"""

from __future__ import annotations

import argparse
import sys
import tempfile
import zipfile
from io import BytesIO
from pathlib import Path

import geopandas as gpd
import pandas as pd
import requests

# ---------------------------------------------------------------------------
# Resolve project paths
# ---------------------------------------------------------------------------
_SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = _SCRIPT_DIR.parent.parent.parent

RAW_DIR = PROJECT_ROOT / "data" / "raw"
OUTPUT_PATH = RAW_DIR / "census-tracts-2010-study-area.geojson"

# ---------------------------------------------------------------------------
# State FIPS codes for the study area
# ---------------------------------------------------------------------------
STUDY_STATES: dict[str, str] = {
    "37": "North Carolina",
    "13": "Georgia",
    "45": "South Carolina",
    "47": "Tennessee",
    "51": "Virginia",
}

TIGER_BASE_URL = (
    "https://www2.census.gov/geo/tiger/TIGER2010/TRACT/2010"
)

# Expected NC tract count (from CEJST)
EXPECTED_NC_TRACTS = 2195


# ---------------------------------------------------------------------------
# Download helpers
# ---------------------------------------------------------------------------


def _download_state_tracts(fips: str, state_name: str) -> gpd.GeoDataFrame:
    """Download and extract 2010 TIGER/Line tracts for one state.

    Args:
        fips: Two-digit state FIPS code.
        state_name: State name for logging.

    Returns:
        GeoDataFrame with tract geometries.
    """
    filename = f"tl_2010_{fips}_tract10.zip"
    url = f"{TIGER_BASE_URL}/{filename}"
    print(f"  Downloading {state_name} ({fips}): {url}")

    resp = requests.get(url, timeout=120)
    resp.raise_for_status()

    # Extract shapefile from ZIP into a temp directory
    with tempfile.TemporaryDirectory() as tmpdir:
        zf = zipfile.ZipFile(BytesIO(resp.content))
        zf.extractall(tmpdir)
        # Find the .shp file
        shp_files = list(Path(tmpdir).glob("*.shp"))
        if not shp_files:
            msg = f"No .shp file found in {filename}"
            raise FileNotFoundError(msg)
        gdf = gpd.read_file(shp_files[0])

    print(f"    -> {len(gdf):,} tracts loaded (CRS: {gdf.crs})")
    return gdf


def download_all_states() -> gpd.GeoDataFrame:
    """Download tract boundaries for all study states and merge.

    Returns:
        Single GeoDataFrame with all tracts, standardised columns.
    """
    print("\n" + "=" * 60)
    print("  Downloading 2010 TIGER/Line Tract Boundaries")
    print("=" * 60)

    frames: list[gpd.GeoDataFrame] = []
    for fips, name in STUDY_STATES.items():
        gdf = _download_state_tracts(fips, name)
        # Standardise to a minimal schema
        gdf = gdf.rename(columns={"GEOID10": "tract_fips"})[
            ["tract_fips", "geometry"]
        ]
        gdf["state_fips"] = fips
        frames.append(gdf)

    merged = gpd.GeoDataFrame(
        pd.concat(frames, ignore_index=True),
        crs=frames[0].crs,
    )
    print(f"\n  Merged: {len(merged):,} tracts across "
          f"{len(STUDY_STATES)} states")
    return merged


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------


def validate(
    gdf: gpd.GeoDataFrame,
    cejst_path: Path | None = None,
) -> bool:
    """Run sanity checks on the merged tract boundaries.

    Args:
        gdf: Merged tract GeoDataFrame.
        cejst_path: Optional path to CEJST NC CSV for FIPS matching.

    Returns:
        True if all critical checks pass.
    """
    print("\n" + "=" * 60)
    print("  Validation")
    print("=" * 60)
    ok = True

    # 1. CRS
    crs_ok = gdf.crs is not None and gdf.crs.to_epsg() == 4269
    tag = "PASS" if crs_ok else "FAIL"
    print(f"  [{tag}] CRS: {gdf.crs} (expect EPSG:4269)")
    if not crs_ok:
        ok = False

    # 2. State counts
    state_counts = gdf["state_fips"].value_counts().sort_index()
    for fips, name in STUDY_STATES.items():
        n = state_counts.get(fips, 0)
        print(f"  [INFO] {name} ({fips}): {n:,} tracts")

    # 3. NC tract count
    nc_count = int(state_counts.get("37", 0))
    nc_ok = nc_count >= EXPECTED_NC_TRACTS
    tag = "PASS" if nc_ok else "FAIL"
    print(f"  [{tag}] NC tracts: {nc_count:,} (expect >= {EXPECTED_NC_TRACTS})")
    if not nc_ok:
        ok = False

    # 4. No null geometries
    null_geom = int(gdf.geometry.is_empty.sum() + gdf.geometry.isna().sum())
    tag = "PASS" if null_geom == 0 else "FAIL"
    print(f"  [{tag}] Null/empty geometries: {null_geom}")
    if null_geom > 0:
        ok = False

    # 5. CEJST FIPS match (if file available)
    cejst_nc_path = cejst_path or (
        PROJECT_ROOT / "data" / "raw" / "cejst-justice40-tracts-nc.csv"
    )
    if cejst_nc_path.exists():
        cejst = pd.read_csv(cejst_nc_path, dtype={"tract_fips": str})
        cejst_fips = set(cejst["tract_fips"])
        gdf_nc_fips = set(gdf.loc[gdf["state_fips"] == "37", "tract_fips"])
        matched = cejst_fips & gdf_nc_fips
        pct = len(matched) / len(cejst_fips) * 100
        match_ok = pct >= 99.0
        tag = "PASS" if match_ok else "FAIL"
        print(
            f"  [{tag}] CEJST FIPS match: {len(matched):,}/{len(cejst_fips):,} "
            f"= {pct:.1f}%"
        )
        if not match_ok:
            ok = False
        # Show missing if any
        missing = sorted(cejst_fips - gdf_nc_fips)
        if missing:
            print(f"    Missing tracts ({len(missing)}):")
            for t in missing[:10]:
                print(f"      {t}")
            if len(missing) > 10:
                print(f"      ... and {len(missing) - 10} more")
    else:
        print("  [SKIP] CEJST NC CSV not found; skipping FIPS match check")

    return ok


# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------


def save_geojson(gdf: gpd.GeoDataFrame, path: Path) -> None:
    """Write the merged GeoDataFrame to GeoJSON.

    Args:
        gdf: Merged tract boundaries.
        path: Output file path.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    gdf.to_file(path, driver="GeoJSON")
    size_mb = path.stat().st_size / (1024 * 1024)
    print(f"\n  Saved: {path}")
    print(f"  Size:  {size_mb:.1f} MB")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Download 2010 TIGER/Line tract boundaries for NC + border states",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=OUTPUT_PATH,
        help="Output GeoJSON path (default: %(default)s)",
    )
    return parser.parse_args()


def main() -> None:
    """Entry point."""
    args = parse_args()

    print("=" * 60)
    print("  Census 2010 Tract Boundaries Download")
    print("  EV Pulse NC - Phase 5")
    print("=" * 60)

    gdf = download_all_states()
    all_ok = validate(gdf)
    save_geojson(gdf, args.output)

    if not all_ok:
        print("\n  WARNING: Some validation checks failed.")
        sys.exit(1)

    print("\n  DONE - tract boundaries ready for crosswalk")


if __name__ == "__main__":
    main()
