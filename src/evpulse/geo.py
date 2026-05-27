"""Geospatial helpers shared across the mapping scripts.

Reprojection and boundary-loading were copied verbatim into every figure
script that draws a map; the copies are collapsed here so the projection and
the FIPS-padding rule live in one place.

Copyright © 2026 Wolfgang Sanyer
Licensed under the Polyform Noncommercial License 1.0.0 (see LICENSE).
"""

from __future__ import annotations

from pathlib import Path

import geopandas as gpd


def reproject_gdf(gdf: gpd.GeoDataFrame, crs: str) -> gpd.GeoDataFrame:
    """Reproject a GeoDataFrame to the target CRS.

    Census GeoJSON arrives in EPSG:4326; some files omit the CRS tag entirely,
    so an untagged frame is assumed to be 4326 before reprojecting.

    Args:
        gdf: Input GeoDataFrame.
        crs: Target CRS string.

    Returns:
        Reprojected GeoDataFrame.
    """
    if gdf.crs is None:
        gdf = gdf.set_crs("EPSG:4326")
    return gdf.to_crs(crs)


def load_boundaries(path: Path, fips_col: str, width: int = 5) -> gpd.GeoDataFrame:
    """Load a boundary GeoJSON, zero-padding its identifier column to a string.

    Census shapefiles store GEOID/ZCTA/tract codes as integers, dropping the
    leading zeros that the joins downstream depend on. Re-padding to a fixed
    width restores them.

    Args:
        path: Path to the boundary GeoJSON.
        fips_col: Identifier column to normalise (e.g. "GEOID", "tract_fips").
        width: Zero-pad width (5 for county/ZCTA codes, 11 for tracts).

    Returns:
        GeoDataFrame with the identifier column as a zero-padded string.
    """
    gdf = gpd.read_file(path)
    gdf[fips_col] = gdf[fips_col].astype(str).str.zfill(width)
    return gdf
