#!/usr/bin/env python3
"""
Phase 5: Publication Figures for Justice40 Equity Analysis (Figures 39-42).

Generates four publication-ready figures for the EV Pulse NC capstone:

    fig-39  CEJST Disadvantaged Tracts — 10-County Study Area
    fig-40  ZCTA-Level Justice40 Burden (134 Study ZIPs)
    fig-41  County-Level Justice40 Comparison Bar Chart
    fig-42  Charging Stations on Justice40 Tracts ("Money Shot")

Input data produced by Phase 5 CEJST/Justice40 pipeline.
Output: 600 DPI, PDF + PNG dual export via save_figure().

Author: BIDA 670 EV-Pulse-NC Project
Date: 2026
"""

from __future__ import annotations

import sys
from pathlib import Path

import geopandas as gpd
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from shapely.geometry import Point

# ---------------------------------------------------------------------------
# Resolve project paths and import publication style
# ---------------------------------------------------------------------------
_SCRIPT_DIR = Path(__file__).resolve().parent
_PROJECT_ROOT = _SCRIPT_DIR.parent.parent.parent
_DATA_DIR = _PROJECT_ROOT / "data" / "processed"
_RAW_DIR = _PROJECT_ROOT / "data" / "raw"
_OUTPUT_DIR = _PROJECT_ROOT / "output" / "figures"

sys.path.insert(0, str(_SCRIPT_DIR))

from publication_style import (  # noqa: E402
    COLORS,
    FONT_SIZES,
    save_figure,
    setup_publication_style,
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
EXPORT_FORMATS = ["png", "pdf"]
TARGET_CRS = "EPSG:32119"

# 10 study counties by FIPS
STUDY_COUNTY_FIPS = [
    "37183",  # Wake
    "37119",  # Mecklenburg
    "37063",  # Durham
    "37081",  # Guilford
    "37179",  # Union
    "37021",  # Buncombe
    "37025",  # Cabarrus
    "37135",  # Orange
    "37067",  # Forsyth
    "37129",  # New Hanover
]

# Colors for disadvantaged/non-disadvantaged tracts
CLR_DISADV = "#E74C3C"
CLR_NOT_DISADV = "#E0F3F8"

# Sliver threshold (square meters) for ZCTA clipping
SLIVER_THRESHOLD = 1000

# Input paths
_TRACT_GEOJSON = _RAW_DIR / "census-tracts-2010-study-area.geojson"
_CEJST_CSV = _RAW_DIR / "cejst-justice40-tracts-nc.csv"
_COUNTY_GEOJSON = _RAW_DIR / "nc-county-boundaries.geojson"
_ZCTA_GEOJSON = _RAW_DIR / "nc-zcta-boundaries.geojson"
_ZCTA_J40_CSV = _DATA_DIR / "phase5-zcta-justice40.csv"
_COUNTY_J40_CSV = _DATA_DIR / "phase5-county-justice40.csv"
_AFDC_CSV = _RAW_DIR / "afdc-charging-stations-connector-2026-02.csv"


# ===================================================================
# DATA LOADERS
# ===================================================================


def _load_tracts() -> gpd.GeoDataFrame:
    """Load census tract polygons."""
    gdf = gpd.read_file(_TRACT_GEOJSON)
    gdf["tract_fips"] = gdf["tract_fips"].astype(str).str.zfill(11)
    return gdf


def _load_cejst() -> pd.DataFrame:
    """Load CEJST disadvantaged flag data."""
    df = pd.read_csv(
        _CEJST_CSV,
        dtype={"tract_fips": str},
    )
    df["tract_fips"] = df["tract_fips"].str.zfill(11)
    return df


def _load_counties() -> gpd.GeoDataFrame:
    """Load county boundary polygons."""
    gdf = gpd.read_file(_COUNTY_GEOJSON)
    gdf["GEOID"] = gdf["GEOID"].astype(str).str.zfill(5)
    return gdf


def _load_zcta_boundaries() -> gpd.GeoDataFrame:
    """Load ZCTA boundary polygons."""
    gdf = gpd.read_file(_ZCTA_GEOJSON)
    gdf["ZCTA5CE20"] = gdf["ZCTA5CE20"].astype(str).str.zfill(5)
    return gdf


def _load_zcta_justice40() -> pd.DataFrame:
    """Load ZCTA-level Justice40 data."""
    df = pd.read_csv(
        _ZCTA_J40_CSV,
        dtype={"zip": str, "county_fips": str},
    )
    df["zip"] = df["zip"].str.zfill(5)
    df["county_fips"] = df["county_fips"].str.zfill(5)
    return df


def _load_county_justice40() -> pd.DataFrame:
    """Load county-level Justice40 data."""
    return pd.read_csv(
        _COUNTY_J40_CSV,
        dtype={"county_fips": str},
    )


def _load_afdc_stations() -> gpd.GeoDataFrame:
    """Load AFDC station data and convert to GeoDataFrame."""
    df = pd.read_csv(
        _AFDC_CSV,
        dtype={"fuel_type_code": str, "status_code": str},
        usecols=[
            "fuel_type_code",
            "status_code",
            "latitude",
            "longitude",
            "ev_dc_fast_num",
            "ev_level2_evse_num",
            "station_name",
        ],
    )
    # Filter to electric, open stations
    df = df[
        (df["fuel_type_code"] == "ELEC") & (df["status_code"] == "E")
    ].copy()
    df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
    df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")
    df = df.dropna(subset=["latitude", "longitude"])
    df["ev_dc_fast_num"] = pd.to_numeric(
        df["ev_dc_fast_num"], errors="coerce"
    ).fillna(0)
    geometry = [
        Point(lon, lat)
        for lon, lat in zip(df["longitude"], df["latitude"])
    ]
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")
    return gdf


# ===================================================================
# SHARED HELPERS
# ===================================================================


def _get_study_counties(
    county_gdf: gpd.GeoDataFrame,
) -> gpd.GeoDataFrame:
    """Filter county GeoDataFrame to 10 study counties."""
    return county_gdf[
        county_gdf["GEOID"].isin(STUDY_COUNTY_FIPS)
    ].copy()


def _prepare_tract_basemap(
    tract_gdf: gpd.GeoDataFrame,
    cejst_df: pd.DataFrame,
) -> gpd.GeoDataFrame:
    """Join tracts with CEJST data, filter to study area, reproject.

    Returns a GeoDataFrame with 'disadvantaged' column and EPSG:32119.
    """
    # Extract county FIPS (first 5 chars of tract_fips)
    tract_gdf = tract_gdf.copy()
    tract_gdf["county_fips"] = tract_gdf["tract_fips"].str[:5]

    # Filter to study counties
    tract_gdf = tract_gdf[
        tract_gdf["county_fips"].isin(STUDY_COUNTY_FIPS)
    ].copy()

    # Join CEJST data
    cejst_slim = cejst_df[["tract_fips", "disadvantaged"]].copy()
    tract_gdf = tract_gdf.merge(
        cejst_slim, on="tract_fips", how="left"
    )
    tract_gdf["disadvantaged"] = tract_gdf["disadvantaged"].fillna(0)

    # Reproject
    if tract_gdf.crs is None:
        tract_gdf = tract_gdf.set_crs("EPSG:4326")
    tract_gdf = tract_gdf.to_crs(TARGET_CRS)

    return tract_gdf


def _add_county_labels(
    ax: plt.Axes,
    county_gdf: gpd.GeoDataFrame,
) -> None:
    """Add bold county name labels at centroids."""
    for _, row in county_gdf.iterrows():
        centroid = row.geometry.centroid
        ax.annotate(
            row["NAME"],
            xy=(centroid.x, centroid.y),
            ha="center",
            va="center",
            fontsize=FONT_SIZES["annotation"],
            fontweight="bold",
            color="#2c3e50",
            bbox=dict(
                boxstyle="round,pad=0.15",
                facecolor="white",
                edgecolor="none",
                alpha=0.7,
            ),
            zorder=10,
        )


def _add_county_boundaries(
    ax: plt.Axes,
    county_gdf: gpd.GeoDataFrame,
) -> None:
    """Plot county boundary outlines in black."""
    county_gdf.boundary.plot(
        ax=ax, color="black", linewidth=1.0, zorder=5
    )


# ===================================================================
# FIG-39: CEJST Disadvantaged Tracts — 10-County Study Area
# ===================================================================


def generate_fig39(
    tract_gdf: gpd.GeoDataFrame,
    cejst_df: pd.DataFrame,
    county_gdf: gpd.GeoDataFrame,
) -> None:
    """CEJST disadvantaged tracts map for 10-county study area."""
    print("[INFO] Generating fig-39: CEJST Disadvantaged Tracts ...")

    tracts = _prepare_tract_basemap(tract_gdf, cejst_df)
    study_counties = _get_study_counties(county_gdf)
    study_counties = study_counties.to_crs(TARGET_CRS)

    # Compute study-area stats
    n_study = len(tracts)
    n_disadv = int(tracts["disadvantaged"].sum())
    pct_disadv = n_disadv / n_study * 100 if n_study > 0 else 0.0

    # Assign colors
    tracts["plot_color"] = tracts["disadvantaged"].apply(
        lambda x: CLR_DISADV if x == 1 else CLR_NOT_DISADV
    )

    fig, ax = plt.subplots(figsize=(10.0, 8.0))
    ax.set_axis_off()

    # Plot tracts
    tracts.plot(
        ax=ax,
        color=tracts["plot_color"],
        edgecolor="white",
        linewidth=0.2,
        alpha=0.7,
        zorder=1,
    )

    # County boundaries and labels
    _add_county_boundaries(ax, study_counties)
    _add_county_labels(ax, study_counties)

    # Stats annotation
    stats_text = (
        "934 / 2,170 evaluable tracts = 43.0% disadvantaged"
        " (statewide)\n"
        f"Study area: {n_disadv:,} / {n_study:,} tracts ="
        f" {pct_disadv:.1f}% disadvantaged"
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
            edgecolor=COLORS["gray_light"],
            alpha=0.9,
        ),
        zorder=15,
    )

    # Legend
    legend_handles = [
        Patch(
            facecolor=CLR_DISADV,
            alpha=0.7,
            edgecolor="white",
            label="Disadvantaged",
        ),
        Patch(
            facecolor=CLR_NOT_DISADV,
            alpha=0.7,
            edgecolor="white",
            label="Not Disadvantaged",
        ),
    ]
    ax.legend(
        handles=legend_handles,
        loc="lower right",
        fontsize=FONT_SIZES["legend"],
        framealpha=0.95,
    )

    ax.set_title(
        "CEJST Disadvantaged Tracts \u2014 10-County Study Area",
        fontsize=FONT_SIZES["title"],
        fontweight="bold",
        pad=12,
    )

    paths = save_figure(
        fig,
        "fig-39-cejst-disadvantaged-tracts",
        _OUTPUT_DIR,
        formats=EXPORT_FORMATS,
    )
    plt.close(fig)
    for p in paths:
        print(f"[SUCCESS] Saved {p}")


# ===================================================================
# FIG-40: ZCTA-Level Justice40 Burden Choropleth
# ===================================================================


def generate_fig40(
    zcta_gdf: gpd.GeoDataFrame,
    zcta_j40_df: pd.DataFrame,
    county_gdf: gpd.GeoDataFrame,
) -> None:
    """ZCTA-level Justice40 disadvantaged area choropleth."""
    print(
        "[INFO] Generating fig-40: "
        "ZCTA-Level Justice40 Choropleth ..."
    )

    study_counties = _get_study_counties(county_gdf)
    study_counties = study_counties.to_crs(TARGET_CRS)

    # Reproject ZCTAs
    zcta_proj = zcta_gdf.copy()
    if zcta_proj.crs is None:
        zcta_proj = zcta_proj.set_crs("EPSG:4326")
    zcta_proj = zcta_proj.to_crs(TARGET_CRS)

    # Clip ZCTAs to study area
    clipped = gpd.clip(zcta_proj, study_counties)
    clipped = clipped[~clipped.geometry.is_empty].copy()
    clipped = clipped[clipped.geometry.notna()].copy()
    clipped = clipped[
        clipped.geometry.area >= SLIVER_THRESHOLD
    ].copy()

    # Join justice40 data
    clipped = clipped.merge(
        zcta_j40_df[["zip", "justice40_pct"]],
        left_on="ZCTA5CE20",
        right_on="zip",
        how="left",
    )
    clipped["justice40_pct"] = clipped["justice40_pct"].fillna(0)

    # Compute stats
    matched = clipped[clipped["zip"].notna()]
    median_pct = matched["justice40_pct"].median()
    min_pct = matched["justice40_pct"].min()
    max_pct = matched["justice40_pct"].max()

    fig, ax = plt.subplots(figsize=(10.0, 8.0))
    ax.set_axis_off()

    # Separate zero and non-zero
    zero_mask = clipped["justice40_pct"] == 0
    zero_zcta = clipped[zero_mask]
    nonzero_zcta = clipped[~zero_mask]

    # Layer 1: Zero justice40 ZCTAs — solid light gray
    if len(zero_zcta) > 0:
        zero_zcta.plot(
            ax=ax,
            color="#F0F0F0",
            edgecolor="white",
            linewidth=0.3,
            zorder=1,
        )

    # Layer 2: Non-zero ZCTAs — YlOrRd choropleth
    norm = mcolors.Normalize(vmin=0, vmax=100)
    cmap = "YlOrRd"
    if len(nonzero_zcta) > 0:
        nonzero_zcta.plot(
            ax=ax,
            column="justice40_pct",
            cmap=cmap,
            norm=norm,
            edgecolor="white",
            linewidth=0.3,
            legend=False,
            zorder=2,
        )

    # County boundaries and labels
    _add_county_boundaries(ax, study_counties)
    _add_county_labels(ax, study_counties)

    # Colorbar
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
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
        "Justice40 Disadvantaged Area (%)",
        fontsize=FONT_SIZES["axis_label"],
    )
    cbar.set_ticks([0, 25, 50, 75, 100])
    cbar.ax.tick_params(labelsize=FONT_SIZES["tick_label"])

    # Stats annotation
    stats_text = (
        f"134 study ZCTAs | Median: {median_pct:.1f}%"
        f" | Range: {min_pct:.1f}%\u2013{max_pct:.1f}%"
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
            edgecolor=COLORS["gray_light"],
            alpha=0.9,
        ),
        zorder=15,
    )

    ax.set_title(
        "ZCTA-Level Justice40 Burden \u2014 134 Study ZIPs",
        fontsize=FONT_SIZES["title"],
        fontweight="bold",
        pad=12,
    )

    paths = save_figure(
        fig,
        "fig-40-zcta-justice40-choropleth",
        _OUTPUT_DIR,
        formats=EXPORT_FORMATS,
    )
    plt.close(fig)
    for p in paths:
        print(f"[SUCCESS] Saved {p}")


# ===================================================================
# FIG-41: County-Level Justice40 Comparison Bar Chart
# ===================================================================


def generate_fig41(county_j40_df: pd.DataFrame) -> None:
    """Horizontal bar chart comparing county Justice40 burden."""
    print(
        "[INFO] Generating fig-41: "
        "County-Level Justice40 Comparison ..."
    )

    df = county_j40_df.sort_values(
        "justice40_pct_popweighted", ascending=True
    ).copy()

    counties = df["county_name"].values
    pct_vals = df["justice40_pct_popweighted"].values

    fig, ax = plt.subplots(figsize=(7.0, 5.0))

    y_pos = np.arange(len(counties))

    # Bar color gradient using YlOrRd
    cmap = plt.cm.YlOrRd
    norm = mcolors.Normalize(vmin=0, vmax=100)
    bar_colors = [cmap(norm(v)) for v in pct_vals]

    ax.barh(
        y_pos,
        pct_vals,
        color=bar_colors,
        edgecolor="white",
        linewidth=0.5,
        zorder=2,
    )

    # Value labels
    for i, val in enumerate(pct_vals):
        ax.text(
            val + 0.5,
            y_pos[i],
            f"{val:.1f}%",
            ha="left",
            va="center",
            fontsize=FONT_SIZES["annotation"],
            color=COLORS["gray_dark"],
        )

    # Statewide reference line at 43.0%
    ax.axvline(
        43.0,
        color=COLORS["reference"],
        linestyle="--",
        linewidth=1.5,
        zorder=1,
        label="Statewide 43.0%",
    )
    ax.text(
        43.0 + 0.3,
        len(counties) - 0.5,
        "Statewide\n43.0%",
        fontsize=FONT_SIZES["annotation"],
        color=COLORS["reference"],
        ha="left",
        va="top",
        fontweight="bold",
    )

    ax.set_yticks(y_pos)
    ax.set_yticklabels(counties, fontsize=FONT_SIZES["tick_label"])
    ax.set_xlim(0, 50)
    ax.set_xlabel(
        "Population-Weighted Justice40 Disadvantaged (%)",
        fontsize=FONT_SIZES["axis_label"],
    )

    # Annotation
    ax.annotate(
        "All 10 study counties below statewide average (43.0%)",
        xy=(0.98, 0.05),
        xycoords="axes fraction",
        fontsize=FONT_SIZES["annotation"],
        ha="right",
        va="bottom",
        bbox=dict(
            boxstyle="round,pad=0.4",
            facecolor="#FFFDE7",
            edgecolor=COLORS["gray_light"],
            alpha=0.9,
        ),
    )

    ax.set_title(
        "County-Level Justice40 Comparison"
        " \u2014 10 Study Counties",
        fontsize=FONT_SIZES["title"],
        fontweight="bold",
    )

    paths = save_figure(
        fig,
        "fig-41-county-justice40-comparison",
        _OUTPUT_DIR,
        formats=EXPORT_FORMATS,
    )
    plt.close(fig)
    for p in paths:
        print(f"[SUCCESS] Saved {p}")


# ===================================================================
# FIG-42: Charging Stations on Justice40 Tracts ("Money Shot")
# ===================================================================


def generate_fig42(
    tract_gdf: gpd.GeoDataFrame,
    cejst_df: pd.DataFrame,
    county_gdf: gpd.GeoDataFrame,
    stations_gdf: gpd.GeoDataFrame,
) -> dict:
    """Overlay charging stations on disadvantaged tract map.

    Returns a dict with key statistics for reporting.
    """
    print(
        "[INFO] Generating fig-42: "
        "Stations on Justice40 Tracts ..."
    )

    tracts = _prepare_tract_basemap(tract_gdf, cejst_df)
    study_counties = _get_study_counties(county_gdf)
    study_counties = study_counties.to_crs(TARGET_CRS)

    # Assign colors
    tracts["plot_color"] = tracts["disadvantaged"].apply(
        lambda x: CLR_DISADV if x == 1 else CLR_NOT_DISADV
    )

    # Reproject stations to match
    stations_proj = stations_gdf.to_crs(TARGET_CRS)

    # Spatial join: filter stations to study area
    study_union = study_counties.union_all()
    stations_in_area = stations_proj[
        stations_proj.geometry.within(study_union)
    ].copy()

    n_stations = len(stations_in_area)
    print(f"  {n_stations} stations in study area")

    # Classify L2 vs DCFC
    stations_in_area["is_dcfc"] = stations_in_area["ev_dc_fast_num"] > 0
    l2_stations = stations_in_area[~stations_in_area["is_dcfc"]]
    dcfc_stations = stations_in_area[stations_in_area["is_dcfc"]]

    # Spatial join stations to tracts for disadvantaged stats
    stations_with_tract = gpd.sjoin(
        stations_in_area,
        tracts[["geometry", "disadvantaged"]],
        how="left",
        predicate="within",
    )
    n_in_disadv = int(
        stations_with_tract["disadvantaged"].sum()
    )
    n_in_non = n_stations - n_in_disadv
    pct_in_disadv = (
        n_in_disadv / n_stations * 100 if n_stations > 0 else 0.0
    )
    pct_in_non = (
        n_in_non / n_stations * 100 if n_stations > 0 else 0.0
    )

    fig, ax = plt.subplots(figsize=(10.0, 8.0))
    ax.set_axis_off()

    # Layer 1: Tract basemap (alpha 0.5 for visibility)
    tracts.plot(
        ax=ax,
        color=tracts["plot_color"],
        edgecolor="white",
        linewidth=0.2,
        alpha=0.5,
        zorder=1,
    )

    # Layer 2: County boundaries
    _add_county_boundaries(ax, study_counties)
    _add_county_labels(ax, study_counties)

    # Layer 3: L2 stations (small blue circles)
    if len(l2_stations) > 0:
        ax.scatter(
            l2_stations.geometry.x,
            l2_stations.geometry.y,
            s=15,
            c="#3498db",
            alpha=0.8,
            edgecolors="white",
            linewidths=0.3,
            zorder=6,
            label="L2 Station",
        )

    # Layer 4: DCFC stations (larger orange triangles)
    if len(dcfc_stations) > 0:
        ax.scatter(
            dcfc_stations.geometry.x,
            dcfc_stations.geometry.y,
            s=40,
            c="#f39c12",
            marker="^",
            alpha=0.9,
            edgecolors="white",
            linewidths=0.5,
            zorder=7,
            label="DCFC Station",
        )

    # Legend
    legend_handles = [
        Patch(
            facecolor=CLR_DISADV,
            alpha=0.5,
            edgecolor="white",
            label="Disadvantaged Tract",
        ),
        Patch(
            facecolor=CLR_NOT_DISADV,
            alpha=0.5,
            edgecolor="white",
            label="Not Disadvantaged",
        ),
        Line2D(
            [0],
            [0],
            marker="o",
            color="w",
            markerfacecolor="#3498db",
            markersize=6,
            label="L2 Station",
        ),
        Line2D(
            [0],
            [0],
            marker="^",
            color="w",
            markerfacecolor="#f39c12",
            markersize=8,
            label="DCFC Station",
        ),
    ]
    ax.legend(
        handles=legend_handles,
        loc="lower right",
        fontsize=FONT_SIZES["legend"],
        framealpha=0.95,
    )

    # Stats annotation
    stats_text = (
        f"{n_stations} stations in study area"
        f" | {pct_in_disadv:.1f}% in disadvantaged tracts"
        f" | {pct_in_non:.1f}% in non-disadvantaged"
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
            edgecolor=COLORS["gray_light"],
            alpha=0.9,
        ),
        zorder=15,
    )

    ax.set_title(
        "EV Charging Stations on Justice40 Tracts"
        " \u2014 10-County Study Area",
        fontsize=FONT_SIZES["title"],
        fontweight="bold",
        pad=12,
    )

    paths = save_figure(
        fig,
        "fig-42-stations-justice40-overlay",
        _OUTPUT_DIR,
        formats=EXPORT_FORMATS,
    )
    plt.close(fig)
    for p in paths:
        print(f"[SUCCESS] Saved {p}")

    return {
        "n_stations": n_stations,
        "n_in_disadv": n_in_disadv,
        "pct_in_disadv": pct_in_disadv,
        "n_in_non": n_in_non,
        "pct_in_non": pct_in_non,
    }


# ===================================================================
# MAIN
# ===================================================================


def main() -> None:
    """Generate all Phase 5 publication figures."""
    setup_publication_style()
    _OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Load shared data
    print("[INFO] Loading data ...")
    tract_gdf = _load_tracts()
    cejst_df = _load_cejst()
    county_gdf = _load_counties()
    zcta_gdf = _load_zcta_boundaries()
    zcta_j40_df = _load_zcta_justice40()
    county_j40_df = _load_county_justice40()
    stations_gdf = _load_afdc_stations()
    print("[INFO] Data loaded.\n")

    generate_fig39(tract_gdf, cejst_df, county_gdf)
    generate_fig40(zcta_gdf, zcta_j40_df, county_gdf)
    generate_fig41(county_j40_df)
    stats = generate_fig42(
        tract_gdf, cejst_df, county_gdf, stations_gdf
    )

    print(f"\n{'=' * 60}")
    print("[INFO] All Phase 5 figures complete.")
    print(
        f"  fig-42 key stat: {stats['pct_in_disadv']:.1f}%"
        " of stations in disadvantaged tracts"
    )
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
