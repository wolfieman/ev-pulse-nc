#!/usr/bin/env python3
"""
Phase 3: County-Level Choropleth Heat Maps of EV Charging Port Density.

Generates publication-ready choropleth maps for three NC counties (Wake,
Guilford, Mecklenburg) showing ZIP-level EV charging port density
(ports per 10,000 population) with DC fast station overlays.

Produces two variants per county:
- Primary figures (shared color scale across all three counties)
- Supplementary figures (per-county local color scale)

Output figures (600 DPI, PDF + PNG):
    fig-22-heatmap-wake          / fig-22s-heatmap-wake-local
    fig-23-heatmap-guilford      / fig-23s-heatmap-guilford-local
    fig-24-heatmap-mecklenburg   / fig-24s-heatmap-mecklenburg-local

Author: BIDA 670 EV-Pulse-NC Project
Date: 2026
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import geopandas as gpd
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.lines import Line2D
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
STATIONS_CSV = PROJECT_ROOT / "data" / "processed" / "phase3-urban-zip-stations.csv"
GINI_CSV = PROJECT_ROOT / "data" / "processed" / "phase3-county-gini.csv"

# Output
OUTPUT_DIR = PROJECT_ROOT / "output" / "figures"

# Export formats
EXPORT_FORMATS = ["png", "pdf"]

# Target CRS: NC State Plane (meters)
TARGET_CRS = "EPSG:32119"

# Figure dimensions
FIGURE_SIZE = (7.0, 6.0)

# Colormap
COLORMAP = "YlGnBu"

# LogNorm lower bound
LOGNORM_VMIN = 0.1

# Zero-station ZCTA styling
ZERO_FILL_COLOR = "#E0E0E0"
ZERO_HATCH_COLOR = "#9E9E9E"
ZERO_HATCH_PATTERN = "///"

# DC fast marker styling
DC_FAST_COLOR = "red"
DC_FAST_MARKER = "^"
DC_FAST_SIZE = 30
DC_FAST_EDGE_COLOR = "black"

# County boundary styling
COUNTY_EDGE_COLOR = "black"
COUNTY_LINEWIDTH = 1.5

# Sliver threshold (square meters)
SLIVER_THRESHOLD = 1000

# Counties of interest (ascending Gini order)
COUNTIES = [
    {
        "name": "Wake",
        "fips": "37183",
        "gini": 0.496,
        "fig_num": 22,
    },
    {
        "name": "Guilford",
        "fips": "37081",
        "gini": 0.571,
        "fig_num": 23,
    },
    {
        "name": "Mecklenburg",
        "fips": "37119",
        "gini": 0.623,
        "fig_num": 24,
    },
]


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


def load_stations(path: Path) -> pd.DataFrame:
    """Load station-level data for DC fast overlay.

    Args:
        path: Path to phase3-urban-zip-stations.csv.

    Returns:
        DataFrame with station locations.
    """
    df = pd.read_csv(path, dtype={"zip": str, "county_fips": str})
    df["zip"] = df["zip"].str.zfill(5)
    df["county_fips"] = df["county_fips"].str.zfill(5)
    df["ev_dc_fast_num"] = (
        pd.to_numeric(df["ev_dc_fast_num"], errors="coerce").fillna(0).astype(int)
    )
    return df


def load_gini_data(path: Path) -> pd.DataFrame:
    """Load county Gini coefficients.

    Args:
        path: Path to phase3-county-gini.csv.

    Returns:
        DataFrame with county-level Gini values.
    """
    df = pd.read_csv(path, dtype={"county_fips": str})
    df["county_fips"] = df["county_fips"].str.zfill(5)
    return df


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


def clip_and_clean(
    zcta_gdf: gpd.GeoDataFrame,
    county_boundary: gpd.GeoDataFrame,
) -> gpd.GeoDataFrame:
    """Clip ZCTAs to county boundary and remove empty/sliver geometries.

    Args:
        zcta_gdf: ZCTA GeoDataFrame in projected CRS.
        county_boundary: Single-county GeoDataFrame in projected CRS.

    Returns:
        Clipped and cleaned GeoDataFrame.
    """
    clipped = gpd.clip(zcta_gdf, county_boundary)

    # Remove empty geometries
    clipped = clipped[~clipped.geometry.is_empty].copy()
    clipped = clipped[clipped.geometry.notna()].copy()

    # Remove slivers
    clipped = clipped[clipped.geometry.area >= SLIVER_THRESHOLD].copy()

    return clipped


# =============================================================================
# SHARED VMAX COMPUTATION
# =============================================================================


def compute_shared_vmax(
    density_df: pd.DataFrame,
    county_fips_list: list[str],
) -> float:
    """Compute the shared vmax across all target counties, rounded up.

    Args:
        density_df: ZIP-level density DataFrame.
        county_fips_list: List of county FIPS codes.

    Returns:
        Rounded-up max ports_per_10k value.
    """
    subset = density_df[density_df["county_fips"].isin(county_fips_list)]
    max_val = subset["ports_per_10k"].max()
    if pd.isna(max_val) or max_val <= 0:
        return 100.0
    return float(math.ceil(max_val))


# =============================================================================
# PLOTTING
# =============================================================================


def create_heatmap(
    clipped_zcta: gpd.GeoDataFrame,
    county_boundary: gpd.GeoDataFrame,
    dc_fast_gdf: gpd.GeoDataFrame,
    county_info: dict,
    gini_row: pd.Series,
    vmin: float,
    vmax: float,
    is_local_scale: bool = False,
) -> plt.Figure:
    """Create a single county choropleth heat map.

    Args:
        clipped_zcta: Clipped ZCTA GeoDataFrame with density data joined.
        county_boundary: County boundary GeoDataFrame.
        dc_fast_gdf: DC fast station points GeoDataFrame.
        county_info: Dict with county name, fips, gini, fig_num.
        gini_row: Gini data row for this county.
        vmin: LogNorm lower bound.
        vmax: LogNorm upper bound.
        is_local_scale: Whether this is a local-scale supplementary figure.

    Returns:
        Matplotlib Figure object.
    """
    fig, ax = plt.subplots(figsize=FIGURE_SIZE)

    # Turn off grid for map
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
    norm = mcolors.LogNorm(vmin=vmin, vmax=vmax)
    if len(nonzero_zcta) > 0:
        nonzero_zcta.plot(
            ax=ax,
            column="ports_per_10k",
            cmap=COLORMAP,
            norm=norm,
            edgecolor="white",
            linewidth=0.5,
            legend=False,
            zorder=2,
        )

    # Layer 3: County boundary outline
    county_boundary.boundary.plot(
        ax=ax,
        color=COUNTY_EDGE_COLOR,
        linewidth=COUNTY_LINEWIDTH,
        zorder=3,
    )

    # Layer 4: DC fast station markers
    if len(dc_fast_gdf) > 0:
        dc_fast_gdf.plot(
            ax=ax,
            marker=DC_FAST_MARKER,
            color=DC_FAST_COLOR,
            markersize=DC_FAST_SIZE,
            edgecolor=DC_FAST_EDGE_COLOR,
            linewidth=0.5,
            zorder=4,
        )

    # Layer 5: Colorbar
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
    tick_values = [0.1, 0.5, 1, 2, 5, 10, 20, 50, 100]
    tick_values = [t for t in tick_values if vmin <= t <= vmax]
    if not tick_values:
        tick_values = [vmin, vmax]
    cbar.set_ticks(tick_values)
    cbar.set_ticklabels([str(t) for t in tick_values])
    cbar.ax.tick_params(labelsize=FONT_SIZES["tick_label"])

    # Layer 6: Stats annotation box
    county_name = county_info["name"]
    total_pop = int(gini_row["total_population"])
    total_ports = int(gini_row["total_ports"])
    gini_val = gini_row["gini_weighted"]
    stats_text = (
        f"{county_name} County\n"
        f"Pop: {total_pop:,}\n"
        f"Ports: {total_ports:,}\n"
        f"Gini: {gini_val:.3f}"
    )
    ax.annotate(
        stats_text,
        xy=(0.02, 0.02),
        xycoords="axes fraction",
        fontsize=FONT_SIZES["annotation"],
        ha="left",
        va="bottom",
        bbox=dict(
            boxstyle="round,pad=0.4",
            facecolor="#FFFDE7",
            edgecolor="#C6C6C6",
            alpha=0.9,
        ),
        zorder=10,
    )

    # Layer 7: Title
    scale_label = " (Local Scale)" if is_local_scale else ""
    title = f"EV Charging Port Density \u2014 {county_name} County{scale_label}"
    ax.set_title(
        title,
        fontsize=FONT_SIZES["title"],
        fontweight="bold",
        pad=12,
    )

    # Legend for special elements
    legend_elements = [
        Patch(
            facecolor=ZERO_FILL_COLOR,
            edgecolor=ZERO_HATCH_COLOR,
            hatch=ZERO_HATCH_PATTERN,
            label="No Charging Stations",
        ),
        Line2D(
            [0],
            [0],
            marker=DC_FAST_MARKER,
            color="none",
            markerfacecolor=DC_FAST_COLOR,
            markeredgecolor=DC_FAST_EDGE_COLOR,
            markersize=8,
            label="DC Fast Station",
        ),
    ]
    ax.legend(
        handles=legend_elements,
        loc="upper right",
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
    """Generate county-level choropleth heat maps for three NC counties."""
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

    print(f"  Loading station data: {STATIONS_CSV.name}")
    stations_df = load_stations(STATIONS_CSV)
    print(f"    {len(stations_df)} stations loaded")

    print(f"  Loading Gini data: {GINI_CSV.name}")
    gini_df = load_gini_data(GINI_CSV)
    print(f"    {len(gini_df)} county Gini rows loaded")

    # ------------------------------------------------------------------
    # 2. Reproject to NC State Plane
    # ------------------------------------------------------------------
    print(f"\n[INFO] Reprojecting to {TARGET_CRS}...")
    zcta_gdf = reproject_gdf(zcta_gdf, TARGET_CRS)
    county_gdf = reproject_gdf(county_gdf, TARGET_CRS)
    print("  Reprojection complete.")

    # ------------------------------------------------------------------
    # 3. Compute shared vmax
    # ------------------------------------------------------------------
    county_fips_list = [c["fips"] for c in COUNTIES]
    shared_vmax = compute_shared_vmax(density_df, county_fips_list)
    print(f"\n[INFO] Shared vmax = {shared_vmax} (ports_per_10k)")

    # ------------------------------------------------------------------
    # 4. Generate maps for each county
    # ------------------------------------------------------------------
    for county_info in COUNTIES:
        county_name = county_info["name"]
        county_fips = county_info["fips"]
        fig_num = county_info["fig_num"]

        print(f"\n{'=' * 60}")
        print(f"[INFO] Processing {county_name} County (FIPS {county_fips})")
        print(f"{'=' * 60}")

        # 4a. Extract county boundary
        county_boundary = county_gdf[county_gdf["GEOID"] == county_fips].copy()
        if len(county_boundary) == 0:
            print(f"  [WARN] No boundary found for FIPS {county_fips}, skipping.")
            continue
        print(f"  County boundary extracted ({len(county_boundary)} polygon(s))")

        # 4b. Clip ZCTAs to county boundary
        clipped = clip_and_clean(zcta_gdf, county_boundary)
        print(f"  Clipped ZCTAs: {len(clipped)}")

        if len(clipped) == 0:
            print(f"  [WARN] No ZCTAs after clipping for {county_name}, skipping.")
            continue

        # 4c. Left-join density data
        clipped = clipped.merge(
            density_df[["zip", "ports_per_10k", "total_ports", "dc_fast_ports"]],
            left_on="ZCTA5CE20",
            right_on="zip",
            how="left",
        )

        # 4d. Fill unmatched with 0
        clipped["ports_per_10k"] = clipped["ports_per_10k"].fillna(0)
        clipped["total_ports"] = clipped["total_ports"].fillna(0)
        clipped["dc_fast_ports"] = clipped["dc_fast_ports"].fillna(0)

        n_zero = (clipped["ports_per_10k"] == 0).sum()
        n_nonzero = (clipped["ports_per_10k"] > 0).sum()
        print(f"  ZCTAs with stations: {n_nonzero}, without: {n_zero}")

        # 4e. Filter DC fast stations for this county
        dc_fast = stations_df[
            (stations_df["county_fips"] == county_fips)
            & (stations_df["ev_dc_fast_num"] > 0)
        ].copy()
        print(f"  DC fast stations: {len(dc_fast)}")

        # Convert DC fast to GeoDataFrame in projected CRS
        if len(dc_fast) > 0:
            dc_fast_gdf = gpd.GeoDataFrame(
                dc_fast,
                geometry=gpd.points_from_xy(dc_fast["longitude"], dc_fast["latitude"]),
                crs="EPSG:4326",
            ).to_crs(TARGET_CRS)
        else:
            dc_fast_gdf = gpd.GeoDataFrame(geometry=[], crs=TARGET_CRS)

        # 4f. Get Gini value
        gini_match = gini_df[gini_df["county_fips"] == county_fips]
        if len(gini_match) == 0:
            print(f"  [WARN] No Gini data for {county_name}, using defaults.")
            gini_row = pd.Series(
                {
                    "total_population": 0,
                    "total_ports": 0,
                    "gini_weighted": county_info["gini"],
                }
            )
        else:
            gini_row = gini_match.iloc[0]

        # 4g-h. Primary figure (shared scale)
        print(f"  Generating shared-scale figure (fig-{fig_num})...")
        fig_shared = create_heatmap(
            clipped_zcta=clipped,
            county_boundary=county_boundary,
            dc_fast_gdf=dc_fast_gdf,
            county_info=county_info,
            gini_row=gini_row,
            vmin=LOGNORM_VMIN,
            vmax=shared_vmax,
            is_local_scale=False,
        )
        filename_shared = f"fig-{fig_num}-heatmap-{county_name.lower()}"
        saved = save_figure(fig_shared, filename_shared, OUTPUT_DIR, EXPORT_FORMATS)
        plt.close(fig_shared)
        for p in saved:
            print(f"    Saved: {p.name}")

        # 4i-j. Supplementary figure (local scale)
        local_max = clipped.loc[clipped["ports_per_10k"] > 0, "ports_per_10k"].max()
        if pd.isna(local_max) or local_max <= 0:
            local_vmax = shared_vmax
        else:
            local_vmax = float(math.ceil(local_max))

        print(f"  Generating local-scale figure (fig-{fig_num}s, vmax={local_vmax})...")
        fig_local = create_heatmap(
            clipped_zcta=clipped,
            county_boundary=county_boundary,
            dc_fast_gdf=dc_fast_gdf,
            county_info=county_info,
            gini_row=gini_row,
            vmin=LOGNORM_VMIN,
            vmax=local_vmax,
            is_local_scale=True,
        )
        filename_local = f"fig-{fig_num}s-heatmap-{county_name.lower()}-local"
        saved_local = save_figure(fig_local, filename_local, OUTPUT_DIR, EXPORT_FORMATS)
        plt.close(fig_local)
        for p in saved_local:
            print(f"    Saved: {p.name}")

        # 5. Console summary
        print(f"\n  [SUCCESS] {county_name} County summary:")
        print(f"    Population:     {int(gini_row['total_population']):,}")
        print(f"    Total ports:    {int(gini_row['total_ports']):,}")
        print(f"    Gini (weighted): {gini_row['gini_weighted']:.4f}")
        print(f"    ZCTAs clipped:  {len(clipped)}")
        print(f"    DC fast sites:  {len(dc_fast)}")
        print(f"    Shared vmax:    {shared_vmax}")
        print(f"    Local vmax:     {local_vmax}")

    # ------------------------------------------------------------------
    # Final summary
    # ------------------------------------------------------------------
    print(f"\n{'=' * 60}")
    print("[SUCCESS] All county heat maps generated.")
    print(f"  Output directory: {OUTPUT_DIR.resolve()}")
    print(f"  Shared color scale: LogNorm({LOGNORM_VMIN}, {shared_vmax})")
    print(f"  Projection: {TARGET_CRS}")
    print(f"  Formats: {EXPORT_FORMATS}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
