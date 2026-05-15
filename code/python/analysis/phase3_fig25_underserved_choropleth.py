#!/usr/bin/env python3
"""
Phase 3, Figure 25: Statewide Underserved ZIP Choropleth Map.

Generates a publication-ready choropleth map of all 10 study-area counties
showing ZIP-level EV charging port density (ports per 10,000 population),
with the top-20 underserved ZIPs highlighted using bold red outlines.

This is the "money figure" — one map showing the full study area with
equity gaps visible at a glance.

Output figures (600 DPI, PDF + PNG):
    fig-25-underserved-choropleth.png
    fig-25-underserved-choropleth.pdf

Author: Wolfgang Sanyer
License: Polyform Noncommercial 1.0.0 (see LICENSE)
Date: 2026
"""

from __future__ import annotations

import sys
from pathlib import Path

import geopandas as gpd
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import Patch

# ---------------------------------------------------------------------------
# Resolve project paths and import publication style
# ---------------------------------------------------------------------------
_SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPT_DIR))

from publication_style import (  # noqa: E402
    FONT_SIZES,
    save_figure,
    setup_publication_style,
)

# =============================================================================
# MODULE-LEVEL CONSTANTS
# =============================================================================

PROJECT_ROOT = _SCRIPT_DIR.parent.parent.parent

# Input paths
ZCTA_GEOJSON = PROJECT_ROOT / "data" / "raw" / "nc-zcta-boundaries.geojson"
COUNTY_GEOJSON = PROJECT_ROOT / "data" / "raw" / "nc-county-boundaries.geojson"
DENSITY_CSV = PROJECT_ROOT / "data" / "processed" / "phase3-zip-density.csv"
TOP20_CSV = PROJECT_ROOT / "data" / "processed" / "phase3-top20-underserved.csv"
TOP10_COUNTIES_CSV = PROJECT_ROOT / "data" / "processed" / "phase3-top10-counties.csv"

# Output
OUTPUT_DIR = PROJECT_ROOT / "output" / "figures"

# Export formats
EXPORT_FORMATS = ["png", "pdf"]

# Target CRS: NC State Plane (meters)
TARGET_CRS = "EPSG:32119"

# Figure dimensions (larger than county maps — shows 10 counties)
FIGURE_SIZE = (10.0, 8.0)

# Colormap (same as county heat maps for consistency)
COLORMAP = "YlGnBu"

# LogNorm bounds
LOGNORM_VMIN = 0.1
LOGNORM_VMAX = 79.0

# Zero-station ZCTA styling
ZERO_FILL_COLOR = "#E0E0E0"
ZERO_HATCH_COLOR = "#9E9E9E"
ZERO_HATCH_PATTERN = "///"

# Top-20 underserved ZIP styling
UNDERSERVED_EDGE_COLOR = "red"
UNDERSERVED_LINEWIDTH = 2.0

# County boundary styling
COUNTY_EDGE_COLOR = "black"
COUNTY_LINEWIDTH = 1.0

# Sliver threshold (square meters)
SLIVER_THRESHOLD = 1000

# Output filename
OUTPUT_FILENAME = "fig-25-underserved-choropleth"


# =============================================================================
# DATA LOADING
# =============================================================================


def load_zcta_boundaries(path: Path) -> gpd.GeoDataFrame:
    """Load ZCTA boundary polygons from GeoJSON.

    Args:
        path: Path to nc-zcta-boundaries.geojson.

    Returns:
        GeoDataFrame with ZCTA geometries.
    """
    gdf = gpd.read_file(path)
    gdf["ZCTA5CE20"] = gdf["ZCTA5CE20"].astype(str).str.zfill(5)
    return gdf


def load_county_boundaries(path: Path) -> gpd.GeoDataFrame:
    """Load county boundary polygons from GeoJSON.

    Args:
        path: Path to nc-county-boundaries.geojson.

    Returns:
        GeoDataFrame with county geometries.
    """
    gdf = gpd.read_file(path)
    gdf["GEOID"] = gdf["GEOID"].astype(str).str.zfill(5)
    return gdf


def load_density_data(path: Path) -> pd.DataFrame:
    """Load ZIP-level density CSV.

    Args:
        path: Path to phase3-zip-density.csv.

    Returns:
        DataFrame with zip as zero-padded string.
    """
    df = pd.read_csv(path, dtype={"zip": str, "county_fips": str})
    df["zip"] = df["zip"].str.zfill(5)
    df["county_fips"] = df["county_fips"].str.zfill(5)
    return df


def load_top20_underserved(path: Path) -> set[str]:
    """Load top-20 underserved ZIP codes.

    Args:
        path: Path to phase3-top20-underserved.csv.

    Returns:
        Set of zero-padded ZIP code strings.
    """
    df = pd.read_csv(path, dtype={"zip": str})
    df["zip"] = df["zip"].str.zfill(5)
    return set(df["zip"].tolist())


def load_top10_counties(path: Path) -> list[str]:
    """Load top-10 county names from CSV.

    Args:
        path: Path to phase3-top10-counties.csv.

    Returns:
        List of county name strings.
    """
    df = pd.read_csv(path)
    return df["County"].tolist()


# =============================================================================
# GEOMETRY HELPERS
# =============================================================================


def reproject_gdf(gdf: gpd.GeoDataFrame, crs: str) -> gpd.GeoDataFrame:
    """Reproject a GeoDataFrame to the target CRS.

    Args:
        gdf: Input GeoDataFrame.
        crs: Target CRS string.

    Returns:
        Reprojected GeoDataFrame.
    """
    if gdf.crs is None:
        gdf = gdf.set_crs("EPSG:4326")
    return gdf.to_crs(crs)


def resolve_county_fips(
    county_names: list[str],
    density_df: pd.DataFrame,
) -> list[str]:
    """Map county names to FIPS codes using the density data.

    Args:
        county_names: List of county names from top-10 CSV.
        density_df: Density DataFrame with county_name and county_fips.

    Returns:
        List of unique 5-digit FIPS codes.
    """
    name_to_fips = (
        density_df[["county_name", "county_fips"]]
        .drop_duplicates()
        .set_index("county_name")["county_fips"]
        .to_dict()
    )
    fips_list = []
    for name in county_names:
        fips = name_to_fips.get(name)
        if fips is not None:
            fips_list.append(fips)
        else:
            print(f"  [WARN] No FIPS mapping for county: {name}")
    return fips_list


def clip_and_clean(
    zcta_gdf: gpd.GeoDataFrame,
    clip_boundary: gpd.GeoDataFrame,
) -> gpd.GeoDataFrame:
    """Clip ZCTAs to boundary and remove empty/sliver geometries.

    Args:
        zcta_gdf: ZCTA GeoDataFrame in projected CRS.
        clip_boundary: Boundary GeoDataFrame in projected CRS.

    Returns:
        Clipped and cleaned GeoDataFrame.
    """
    clipped = gpd.clip(zcta_gdf, clip_boundary)

    # Remove empty geometries
    clipped = clipped[~clipped.geometry.is_empty].copy()
    clipped = clipped[clipped.geometry.notna()].copy()

    # Remove slivers
    clipped = clipped[clipped.geometry.area >= SLIVER_THRESHOLD].copy()

    return clipped


# =============================================================================
# PLOTTING
# =============================================================================


def create_underserved_choropleth(
    clipped_zcta: gpd.GeoDataFrame,
    county_boundaries: gpd.GeoDataFrame,
    underserved_zips: set[str],
) -> plt.Figure:
    """Create the statewide underserved ZIP choropleth map.

    Args:
        clipped_zcta: Clipped ZCTA GeoDataFrame with density data joined.
        county_boundaries: County boundary GeoDataFrame for the 10 counties.
        underserved_zips: Set of top-20 underserved ZIP codes.

    Returns:
        Matplotlib Figure object.
    """
    fig, ax = plt.subplots(figsize=FIGURE_SIZE)

    # Turn off grid and axes for map
    ax.set_axis_off()

    # Separate zero-station and non-zero ZCTAs
    zero_mask = clipped_zcta["ports_per_10k"].isna() | (
        clipped_zcta["ports_per_10k"] == 0
    )
    zero_zcta = clipped_zcta[zero_mask]
    nonzero_zcta = clipped_zcta[~zero_mask]

    # Layer 1: Zero-station ZCTAs (gray + hatching)
    if len(zero_zcta) > 0:
        zero_zcta.plot(
            ax=ax,
            color=ZERO_FILL_COLOR,
            edgecolor=ZERO_HATCH_COLOR,
            linewidth=0.5,
            hatch=ZERO_HATCH_PATTERN,
            zorder=1,
        )

    # Layer 2: Non-zero ZCTAs (choropleth)
    norm = mcolors.LogNorm(vmin=LOGNORM_VMIN, vmax=LOGNORM_VMAX)
    if len(nonzero_zcta) > 0:
        nonzero_zcta.plot(
            ax=ax,
            column="ports_per_10k",
            cmap=COLORMAP,
            norm=norm,
            edgecolor="white",
            linewidth=0.3,
            legend=False,
            zorder=2,
        )

    # Layer 3: County boundary outlines for context
    county_boundaries.boundary.plot(
        ax=ax,
        color=COUNTY_EDGE_COLOR,
        linewidth=COUNTY_LINEWIDTH,
        zorder=3,
    )

    # Layer 4: Top-20 underserved ZIPs — bold RED outlines
    underserved_mask = clipped_zcta["ZCTA5CE20"].isin(underserved_zips)
    underserved_zcta = clipped_zcta[underserved_mask]
    if len(underserved_zcta) > 0:
        underserved_zcta.boundary.plot(
            ax=ax,
            color=UNDERSERVED_EDGE_COLOR,
            linewidth=UNDERSERVED_LINEWIDTH,
            zorder=4,
        )

    # Layer 5: County name labels at centroids
    for _, row in county_boundaries.iterrows():
        centroid = row.geometry.centroid
        ax.annotate(
            row["NAME"],
            xy=(centroid.x, centroid.y),
            ha="center",
            va="center",
            fontsize=FONT_SIZES["annotation"],
            fontweight="bold",
            color="#2c3e50",
            zorder=5,
        )

    # Colorbar
    sm = plt.cm.ScalarMappable(cmap=COLORMAP, norm=norm)
    sm.set_array([])
    cbar = fig.colorbar(
        sm,
        ax=ax,
        orientation="vertical",
        fraction=0.03,
        pad=0.02,
        shrink=0.8,
    )
    cbar.set_label(
        "Ports per 10,000 Population",
        fontsize=FONT_SIZES["axis_label"],
    )

    # Log-scale ticks for colorbar
    tick_values = [0.1, 0.5, 1, 2, 5, 10, 20, 50]
    tick_values = [t for t in tick_values if LOGNORM_VMIN <= t <= LOGNORM_VMAX]
    if not tick_values:
        tick_values = [LOGNORM_VMIN, LOGNORM_VMAX]
    cbar.set_ticks(tick_values)
    cbar.set_ticklabels([str(t) for t in tick_values])
    cbar.ax.tick_params(labelsize=FONT_SIZES["tick_label"])

    # Title
    ax.set_title(
        "EV Charging Port Density \u2014 Top 10 NC Counties by BEV Registration",
        fontsize=FONT_SIZES["title"],
        fontweight="bold",
        pad=12,
    )

    # Legend
    legend_elements = [
        Patch(
            facecolor=ZERO_FILL_COLOR,
            edgecolor=ZERO_HATCH_COLOR,
            hatch=ZERO_HATCH_PATTERN,
            label="No Charging Stations",
        ),
        Patch(
            facecolor="none",
            edgecolor=UNDERSERVED_EDGE_COLOR,
            linewidth=UNDERSERVED_LINEWIDTH,
            label="Top 20 Underserved",
        ),
    ]
    ax.legend(
        handles=legend_elements,
        loc="lower left",
        fontsize=FONT_SIZES["legend"],
        framealpha=0.95,
        facecolor="white",
        edgecolor="#C6C6C6",
    )

    return fig


# =============================================================================
# MAIN PIPELINE
# =============================================================================


def main() -> None:
    """Generate the statewide underserved ZIP choropleth map."""
    print("[INFO] Setting up publication style...")
    setup_publication_style(use_serif=True, context="paper")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------
    # 1. Load all input data
    # ------------------------------------------------------------------
    print("[INFO] Loading input data...")

    print(f"  Loading ZCTA boundaries: {ZCTA_GEOJSON.name}")
    zcta_gdf = load_zcta_boundaries(ZCTA_GEOJSON)
    print(f"    {len(zcta_gdf)} ZCTA polygons loaded")

    print(f"  Loading county boundaries: {COUNTY_GEOJSON.name}")
    county_gdf = load_county_boundaries(COUNTY_GEOJSON)
    print(f"    {len(county_gdf)} county polygons loaded")

    print(f"  Loading density data: {DENSITY_CSV.name}")
    density_df = load_density_data(DENSITY_CSV)
    print(f"    {len(density_df)} ZIP rows loaded")

    print(f"  Loading top-20 underserved: {TOP20_CSV.name}")
    underserved_zips = load_top20_underserved(TOP20_CSV)
    print(f"    {len(underserved_zips)} underserved ZIPs loaded")

    print(f"  Loading top-10 counties: {TOP10_COUNTIES_CSV.name}")
    county_names = load_top10_counties(TOP10_COUNTIES_CSV)
    print(f"    {len(county_names)} counties: {', '.join(county_names)}")

    # ------------------------------------------------------------------
    # 2. Resolve county names to FIPS codes
    # ------------------------------------------------------------------
    print("\n[INFO] Resolving county FIPS codes...")
    county_fips_list = resolve_county_fips(county_names, density_df)
    print(f"  Resolved {len(county_fips_list)} FIPS codes: {county_fips_list}")

    # ------------------------------------------------------------------
    # 3. Reproject to NC State Plane
    # ------------------------------------------------------------------
    print(f"\n[INFO] Reprojecting to {TARGET_CRS}...")
    zcta_gdf = reproject_gdf(zcta_gdf, TARGET_CRS)
    county_gdf = reproject_gdf(county_gdf, TARGET_CRS)
    print("  Reprojection complete.")

    # ------------------------------------------------------------------
    # 4. Filter to 10 target counties and compute union boundary
    # ------------------------------------------------------------------
    print("\n[INFO] Filtering to target counties...")
    target_counties = county_gdf[county_gdf["GEOID"].isin(county_fips_list)].copy()
    print(f"  {len(target_counties)} county boundaries selected")

    if len(target_counties) == 0:
        print("[ERROR] No matching county boundaries found. Exiting.")
        return

    # ------------------------------------------------------------------
    # 5. Clip ZCTAs to the union of all 10 county boundaries
    # ------------------------------------------------------------------
    print("[INFO] Clipping ZCTAs to study area...")
    clipped = clip_and_clean(zcta_gdf, target_counties)
    print(f"  {len(clipped)} ZCTAs after clipping and cleaning")

    if len(clipped) == 0:
        print("[ERROR] No ZCTAs after clipping. Exiting.")
        return

    # ------------------------------------------------------------------
    # 6. Left-join density data; unmatched ZCTAs get ports_per_10k = 0
    # ------------------------------------------------------------------
    print("[INFO] Joining density data...")
    clipped = clipped.merge(
        density_df[["zip", "ports_per_10k"]],
        left_on="ZCTA5CE20",
        right_on="zip",
        how="left",
    )
    clipped["ports_per_10k"] = clipped["ports_per_10k"].fillna(0)

    n_zero = (clipped["ports_per_10k"] == 0).sum()
    n_nonzero = (clipped["ports_per_10k"] > 0).sum()
    print(f"  ZCTAs with stations: {n_nonzero}, without: {n_zero}")

    # Count how many top-20 underserved ZIPs are in the clipped area
    matched_underserved = underserved_zips & set(clipped["ZCTA5CE20"].tolist())
    print(f"  Top-20 underserved ZIPs in study area: {len(matched_underserved)}")

    # ------------------------------------------------------------------
    # 7. Generate the choropleth
    # ------------------------------------------------------------------
    print("\n[INFO] Generating choropleth map...")
    fig = create_underserved_choropleth(
        clipped_zcta=clipped,
        county_boundaries=target_counties,
        underserved_zips=underserved_zips,
    )

    # ------------------------------------------------------------------
    # 8. Save figure
    # ------------------------------------------------------------------
    print("[INFO] Saving figure...")
    saved = save_figure(fig, OUTPUT_FILENAME, OUTPUT_DIR, EXPORT_FORMATS)
    plt.close(fig)
    for p in saved:
        print(f"  Saved: {p.name}")

    # ------------------------------------------------------------------
    # Final summary
    # ------------------------------------------------------------------
    print(f"\n{'=' * 60}")
    print("[SUCCESS] Figure 25 generated.")
    print(f"  Output directory: {OUTPUT_DIR.resolve()}")
    print(f"  Counties: {len(county_fips_list)}")
    print(f"  ZCTAs plotted: {len(clipped)}")
    print(f"  Color scale: LogNorm({LOGNORM_VMIN}, {LOGNORM_VMAX})")
    print(f"  Projection: {TARGET_CRS}")
    print(f"  Formats: {EXPORT_FORMATS}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
