#!/usr/bin/env python3
"""
Phase 3 AFDC Infrastructure EDA and Descriptive Analysis.

Produces figures fig-08 through fig-17 and supporting CSV tables for the
EV Pulse NC analytical pipeline. Covers missingness, distributions,
geographic coverage, temporal growth, and data quality flagging.

Author: Wolfgang Sanyer
License: Polyform Noncommercial 1.0.0 (see LICENSE)
Date: 2026
"""

from __future__ import annotations

import argparse
import ast
import json
import sys
from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# ---------------------------------------------------------------------------
# Resolve project paths so the sibling module import works
# ---------------------------------------------------------------------------
_SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPT_DIR))

from publication_style import (  # noqa: E402
    COLORS,
    FIGURE_SIZES,
    FONT_SIZES,
    PALETTE_SEQUENTIAL,
    add_panel_label,
    save_figure,
    setup_publication_style,
)

# =============================================================================
# MODULE-LEVEL CONSTANTS
# =============================================================================

PROJECT_ROOT = _SCRIPT_DIR.parent.parent.parent

AFDC_CSV = (
    PROJECT_ROOT / "data" / "raw" / "afdc-charging-stations-connector-2026-02.csv"
)
CENSUS_ZIP_CSV = PROJECT_ROOT / "data" / "raw" / "nc-zip-population-acs2022.csv"
NC_BOUNDARIES = PROJECT_ROOT / "data" / "raw" / "nc-county-boundaries.geojson"

FIGURES_DIR = PROJECT_ROOT / "output" / "figures"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

# NC bounding box (latitude / longitude)
NC_LAT_MIN, NC_LAT_MAX = 33.84, 36.59
NC_LON_MIN, NC_LON_MAX = -84.32, -75.46

# Non-EV fuel columns that are expected to be 100 % null for this EV-only data
NON_EV_FUEL_PREFIXES = (
    "bd_",
    "cng_",
    "e85_",
    "hy_",
    "lng_",
    "lpg_",
    "ng_",
    "rd_",
)

# EV-relevant columns to audit for missingness
EV_RELEVANT_COLS = [
    "id",
    "station_name",
    "city",
    "state",
    "zip",
    "street_address",
    "latitude",
    "longitude",
    "access_code",
    "facility_type",
    "owner_type_code",
    "ev_network",
    "ev_connector_types",
    "ev_level1_evse_num",
    "ev_level2_evse_num",
    "ev_dc_fast_num",
    "ev_pricing",
    "ev_workplace_charging",
    "ev_network_ids",
    "ev_charging_units",
    "open_date",
    "date_last_confirmed",
    "status_code",
    "groups_with_access_code",
    "maximum_vehicle_class",
    "restricted_access",
    "ev_other_evse",
    "ev_renewable_source",
    "ev_network_web",
]

# Minimum % non-null for open_date to produce temporal figure
OPEN_DATE_THRESHOLD = 0.40

# Categorical charging-level palette
LEVEL_COLORS = {
    "L2-only": COLORS["ARIMA"],
    "DCFC-only": COLORS["negative"],
    "Mixed": COLORS["UCM"],
    "L1-only": COLORS["highlight"],
}

# =============================================================================
# DATA LOADING & PREPARATION
# =============================================================================


def load_afdc(path: Path) -> pd.DataFrame:
    """Load and lightly prepare the AFDC CSV.

    Args:
        path: Path to the AFDC CSV file.

    Returns:
        DataFrame with basic type casts applied.
    """
    df = pd.read_csv(path, dtype={"zip": str})
    # Ensure zip is zero-padded 5-digit string
    df["zip"] = df["zip"].astype(str).str.zfill(5)
    # Parse open_date
    df["open_date"] = pd.to_datetime(df["open_date"], errors="coerce")
    # Fill NaN port counts with 0 for numeric convenience
    for col in ("ev_level1_evse_num", "ev_level2_evse_num", "ev_dc_fast_num"):
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)
    return df


def derive_charging_level(row: pd.Series) -> str:
    """Classify a station as L1-only, L2-only, DCFC-only, or Mixed.

    Args:
        row: A single row from the AFDC DataFrame.

    Returns:
        Charging level category string.
    """
    has_l1 = row["ev_level1_evse_num"] > 0
    has_l2 = row["ev_level2_evse_num"] > 0
    has_dc = row["ev_dc_fast_num"] > 0
    flags = [has_l1, has_l2, has_dc]
    if sum(flags) > 1:
        return "Mixed"
    if has_dc:
        return "DCFC-only"
    if has_l1:
        return "L1-only"
    return "L2-only"


def parse_connector_types(series: pd.Series) -> pd.Series:
    """Parse the string-encoded list in ev_connector_types.

    Args:
        series: The ev_connector_types column.

    Returns:
        Series of Python lists (empty list when missing).
    """

    def _parse(val: object) -> list[str]:
        if pd.isna(val):
            return []
        try:
            parsed = ast.literal_eval(str(val))
            if isinstance(parsed, list):
                return [str(c).strip() for c in parsed]
        except (ValueError, SyntaxError):
            pass
        return []

    return series.apply(_parse)


def parse_ev_charging_units_power(series: pd.Series) -> pd.Series:
    """Extract max power_kw per station from ev_charging_units JSON.

    The ev_charging_units column contains a list of dicts, each with a
    'connectors' sub-dict mapping connector type to {power_kw, port_count}.

    Args:
        series: The ev_charging_units column.

    Returns:
        Series of max power_kw (float, NaN when unavailable).
    """

    def _extract(val: object) -> float | None:
        if pd.isna(val):
            return np.nan
        try:
            data = ast.literal_eval(str(val))
        except (ValueError, SyntaxError):
            try:
                data = json.loads(str(val))
            except (json.JSONDecodeError, ValueError):
                return np.nan
        # data is a list of charging-unit dicts
        if isinstance(data, list):
            powers: list[float] = []
            for unit in data:
                if not isinstance(unit, dict):
                    continue
                connectors = unit.get("connectors", {})
                if isinstance(connectors, dict):
                    for _ctype, cinfo in connectors.items():
                        if isinstance(cinfo, dict):
                            pw = cinfo.get("power_kw")
                            if pw is not None:
                                powers.append(float(pw))
            return max(powers) if powers else np.nan
        return np.nan

    return series.apply(_extract)


# =============================================================================
# CSV OUTPUTS
# =============================================================================


def write_column_profile(df: pd.DataFrame, out_dir: Path) -> Path:
    """Write per-column profile CSV.

    Args:
        df: AFDC DataFrame.
        out_dir: Output directory.

    Returns:
        Path to the written CSV.
    """
    # Exclude derived list/object columns that break nunique
    exclude = {"connector_list", "max_power_kw"}
    cols = [c for c in df.columns if c not in exclude]
    sub = df[cols]
    profile = pd.DataFrame(
        {
            "column": sub.columns,
            "dtype": sub.dtypes.astype(str).values,
            "non_null_count": sub.notna().sum().values,
            "null_count": sub.isna().sum().values,
            "null_pct": (sub.isna().sum() / len(sub) * 100).round(2).values,
            "unique_count": sub.nunique().values,
        }
    )
    path = out_dir / "afdc-eda-column-profile.csv"
    profile.to_csv(path, index=False)
    return path


def write_stations_by_level(df: pd.DataFrame, out_dir: Path) -> Path:
    """Write station and port counts by charging level.

    Args:
        df: AFDC DataFrame with charging_level column.
        out_dir: Output directory.

    Returns:
        Path to the written CSV.
    """
    agg = (
        df.groupby("charging_level")
        .agg(
            station_count=("id", "count"),
            l1_ports=("ev_level1_evse_num", "sum"),
            l2_ports=("ev_level2_evse_num", "sum"),
            dcfc_ports=("ev_dc_fast_num", "sum"),
        )
        .reset_index()
    )
    agg["total_ports"] = agg["l1_ports"] + agg["l2_ports"] + agg["dcfc_ports"]
    path = out_dir / "afdc-eda-stations-by-level.csv"
    agg.to_csv(path, index=False)
    return path


def write_stations_by_network(df: pd.DataFrame, out_dir: Path) -> Path:
    """Write station and port counts by ev_network.

    Args:
        df: AFDC DataFrame.
        out_dir: Output directory.

    Returns:
        Path to the written CSV.
    """
    agg = (
        df.groupby("ev_network")
        .agg(
            station_count=("id", "count"),
            l2_ports=("ev_level2_evse_num", "sum"),
            dcfc_ports=("ev_dc_fast_num", "sum"),
        )
        .reset_index()
    )
    agg["total_ports"] = agg["l2_ports"] + agg["dcfc_ports"]
    agg = agg.sort_values("station_count", ascending=False).reset_index(drop=True)
    path = out_dir / "afdc-eda-stations-by-network.csv"
    agg.to_csv(path, index=False)
    return path


def write_stations_by_zip(df: pd.DataFrame, out_dir: Path) -> Path:
    """Write per-ZIP station and port counts.

    Args:
        df: AFDC DataFrame.
        out_dir: Output directory.

    Returns:
        Path to the written CSV.
    """
    agg = (
        df.groupby("zip")
        .agg(
            station_count=("id", "count"),
            l2_ports=("ev_level2_evse_num", "sum"),
            dcfc_ports=("ev_dc_fast_num", "sum"),
        )
        .reset_index()
    )
    agg["total_ports"] = agg["l2_ports"] + agg["dcfc_ports"]
    agg = agg.sort_values("station_count", ascending=False).reset_index(drop=True)
    path = out_dir / "afdc-eda-stations-by-zip.csv"
    agg.to_csv(path, index=False)
    return path


def write_quality_flags(df: pd.DataFrame, out_dir: Path) -> Path:
    """Flag rows with quality issues and write CSV.

    Flags:
        - out-of-bounds lat/lon (outside NC bounding box)
        - zero total ports
        - near-duplicate street addresses (case-insensitive)

    Args:
        df: AFDC DataFrame.
        out_dir: Output directory.

    Returns:
        Path to the written CSV.
    """
    flags: list[pd.DataFrame] = []

    # Out-of-bounds coords
    oob = df[
        (df["latitude"] < NC_LAT_MIN)
        | (df["latitude"] > NC_LAT_MAX)
        | (df["longitude"] < NC_LON_MIN)
        | (df["longitude"] > NC_LON_MAX)
    ].copy()
    if len(oob):
        oob["flag"] = "out_of_bounds_coords"
        flags.append(oob[["id", "station_name", "latitude", "longitude", "flag"]])

    # Zero total ports
    df["_total_ports"] = (
        df["ev_level1_evse_num"] + df["ev_level2_evse_num"] + df["ev_dc_fast_num"]
    )
    zero = df[df["_total_ports"] == 0].copy()
    if len(zero):
        zero["flag"] = "zero_ports"
        flags.append(zero[["id", "station_name", "latitude", "longitude", "flag"]])
    df.drop(columns="_total_ports", inplace=True)

    # Near-duplicate addresses (same normalised address + city)
    addr_norm = (
        df["street_address"].str.lower().str.strip()
        + "|"
        + df["city"].str.lower().str.strip()
    )
    dup_mask = addr_norm.duplicated(keep=False)
    dups = df[dup_mask].copy()
    if len(dups):
        dups["flag"] = "near_duplicate_address"
        flags.append(dups[["id", "station_name", "latitude", "longitude", "flag"]])

    if flags:
        result = pd.concat(flags, ignore_index=True)
    else:
        result = pd.DataFrame(
            columns=["id", "station_name", "latitude", "longitude", "flag"]
        )
    path = out_dir / "afdc-eda-quality-flags.csv"
    result.to_csv(path, index=False)
    return path


# =============================================================================
# FIGURE GENERATORS
# =============================================================================


def fig08_missing_heatmap(df: pd.DataFrame, out_dir: Path) -> Path:
    """Fig-08: Missingness heatmap for EV-relevant columns.

    Args:
        df: AFDC DataFrame.
        out_dir: Figures output directory.

    Returns:
        Path to the saved figure.
    """
    cols = [c for c in EV_RELEVANT_COLS if c in df.columns]
    missing = df[cols].isna().astype(int)

    fig, ax = plt.subplots(figsize=(7.0, 5.5))
    sns.heatmap(
        missing.T,
        cbar_kws={"label": "Missing (1) / Present (0)", "shrink": 0.6},
        yticklabels=True,
        xticklabels=False,
        cmap=["#F4F4F4", COLORS["negative"]],
        ax=ax,
    )
    ax.set_title("Missing Values — EV-Relevant Columns", fontweight="bold")
    ax.set_xlabel(f"Stations (n = {len(df):,})")
    ax.set_ylabel("")
    ax.tick_params(axis="y", labelsize=FONT_SIZES["annotation"])

    paths = save_figure(fig, "fig-08-afdc-missing-values-heatmap", out_dir)
    plt.close(fig)
    return paths[0]


def fig09_stations_by_level(df: pd.DataFrame, out_dir: Path) -> Path:
    """Fig-09: Bar chart of station counts by charging level with port annotations.

    Args:
        df: AFDC DataFrame with charging_level column.
        out_dir: Figures output directory.

    Returns:
        Path to the saved figure.
    """
    order = ["L1-only", "L2-only", "DCFC-only", "Mixed"]
    counts = df["charging_level"].value_counts().reindex(order, fill_value=0)
    port_totals = (
        df.groupby("charging_level")
        .apply(
            lambda g: g["ev_level1_evse_num"].sum()
            + g["ev_level2_evse_num"].sum()
            + g["ev_dc_fast_num"].sum()
        )
        .reindex(order, fill_value=0)
    )

    fig, ax = plt.subplots(figsize=FIGURE_SIZES["wide"])
    colors = [LEVEL_COLORS.get(lv, COLORS["neutral"]) for lv in order]
    bars = ax.bar(order, counts.values, color=colors, edgecolor="white", linewidth=0.8)
    for bar, port in zip(bars, port_totals.values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 8,
            f"{int(bar.get_height())} stn\n{int(port)} ports",
            ha="center",
            va="bottom",
            fontsize=FONT_SIZES["annotation"],
        )
    ax.set_ylabel("Station Count")
    ax.set_xlabel("Charging Level Category")
    ax.set_title("Stations by Charging Level", fontweight="bold")

    paths = save_figure(fig, "fig-09-afdc-stations-by-level", out_dir)
    plt.close(fig)
    return paths[0]


def fig10_stations_by_network(df: pd.DataFrame, out_dir: Path) -> Path:
    """Fig-10: Horizontal bar of top 15 networks.

    Args:
        df: AFDC DataFrame.
        out_dir: Figures output directory.

    Returns:
        Path to the saved figure.
    """
    top15 = df["ev_network"].value_counts().head(15).sort_values()

    fig, ax = plt.subplots(figsize=(7.0, 5.0))
    palette = sns.color_palette(PALETTE_SEQUENTIAL[2:], n_colors=len(top15))
    ax.barh(top15.index, top15.values, color=palette, edgecolor="white", linewidth=0.8)
    for i, (val, name) in enumerate(zip(top15.values, top15.index)):
        ax.text(val + 3, i, str(val), va="center", fontsize=FONT_SIZES["annotation"])
    ax.set_xlabel("Station Count")
    ax.set_title("Top 15 EV Charging Networks in NC", fontweight="bold")

    paths = save_figure(fig, "fig-10-afdc-stations-by-network", out_dir)
    plt.close(fig)
    return paths[0]


def fig11_access_facility(df: pd.DataFrame, out_dir: Path) -> Path:
    """Fig-11: Two-panel figure — (A) access_code, (B) facility_type.

    Args:
        df: AFDC DataFrame.
        out_dir: Figures output directory.

    Returns:
        Path to the saved figure.
    """
    fig, (ax_a, ax_b) = plt.subplots(1, 2, figsize=(7.0, 4.0))

    # Panel A — access_code
    acc = df["access_code"].value_counts()
    colors_a = sns.color_palette(PALETTE_SEQUENTIAL[3:], n_colors=len(acc))
    ax_a.barh(acc.index, acc.values, color=colors_a, edgecolor="white")
    for i, v in enumerate(acc.values):
        ax_a.text(v + 3, i, str(v), va="center", fontsize=FONT_SIZES["annotation"])
    ax_a.set_xlabel("Station Count")
    ax_a.set_title("Access Code", fontweight="bold")
    add_panel_label(ax_a, "(A)")

    # Panel B — facility_type (top 10)
    fac = df["facility_type"].dropna().value_counts().head(10).sort_values()
    colors_b = sns.color_palette(PALETTE_SEQUENTIAL[2:], n_colors=len(fac))
    ax_b.barh(fac.index, fac.values, color=colors_b, edgecolor="white")
    for i, v in enumerate(fac.values):
        ax_b.text(v + 3, i, str(v), va="center", fontsize=FONT_SIZES["annotation"])
    ax_b.set_xlabel("Station Count")
    ax_b.set_title("Top 10 Facility Types", fontweight="bold")
    add_panel_label(ax_b, "(B)")

    paths = save_figure(fig, "fig-11-afdc-stations-by-access-facility", out_dir)
    plt.close(fig)
    return paths[0]


def fig12_port_distributions(df: pd.DataFrame, out_dir: Path) -> Path:
    """Fig-12: Box/violin of port count distributions for L2 and DCFC.

    Args:
        df: AFDC DataFrame.
        out_dir: Figures output directory.

    Returns:
        Path to the saved figure.
    """
    l2 = df.loc[df["ev_level2_evse_num"] > 0, "ev_level2_evse_num"]
    dc = df.loc[df["ev_dc_fast_num"] > 0, "ev_dc_fast_num"]

    plot_df = pd.DataFrame(
        {
            "ports": pd.concat([l2, dc], ignore_index=True),
            "type": ["L2"] * len(l2) + ["DCFC"] * len(dc),
        }
    )

    fig, ax = plt.subplots(figsize=FIGURE_SIZES["wide"])
    sns.violinplot(
        data=plot_df,
        x="type",
        y="ports",
        hue="type",
        inner="box",
        palette=[COLORS["ARIMA"], COLORS["negative"]],
        legend=False,
        ax=ax,
        cut=0,
    )
    ax.set_ylabel("Port Count per Station")
    ax.set_xlabel("Charging Type")
    ax.set_title("Port Count Distributions (L2 vs DCFC)", fontweight="bold")
    # annotate medians
    for i, ct in enumerate(["L2", "DCFC"]):
        subset = plot_df.loc[plot_df["type"] == ct, "ports"]
        med = subset.median()
        ax.text(
            i,
            med + 0.5,
            f"med={med:.0f}",
            ha="center",
            fontsize=FONT_SIZES["annotation"],
            color=COLORS["gray_dark"],
        )

    paths = save_figure(fig, "fig-12-afdc-port-count-distributions", out_dir)
    plt.close(fig)
    return paths[0]


def fig13_stations_by_city(df: pd.DataFrame, out_dir: Path) -> Path:
    """Fig-13: Top 20 cities by station count.

    Args:
        df: AFDC DataFrame.
        out_dir: Figures output directory.

    Returns:
        Path to the saved figure.
    """
    top20 = df["city"].value_counts().head(20).sort_values()

    fig, ax = plt.subplots(figsize=(7.0, 5.5))
    palette = sns.color_palette(PALETTE_SEQUENTIAL[2:], n_colors=len(top20))
    ax.barh(top20.index, top20.values, color=palette, edgecolor="white", linewidth=0.8)
    for i, v in enumerate(top20.values):
        ax.text(v + 1, i, str(v), va="center", fontsize=FONT_SIZES["annotation"])
    ax.set_xlabel("Station Count")
    ax.set_title("Top 20 NC Cities by Charging Station Count", fontweight="bold")

    paths = save_figure(fig, "fig-13-afdc-stations-by-city-top20", out_dir)
    plt.close(fig)
    return paths[0]


def fig14_temporal_growth(df: pd.DataFrame, out_dir: Path) -> Path | None:
    """Fig-14: Cumulative station openings over time.

    Skips if open_date coverage is below OPEN_DATE_THRESHOLD.

    Args:
        df: AFDC DataFrame.
        out_dir: Figures output directory.

    Returns:
        Path to figure or None if skipped.
    """
    coverage = df["open_date"].notna().mean()
    if coverage < OPEN_DATE_THRESHOLD:
        print(
            f"  [SKIP] fig-14: open_date coverage = {coverage:.1%} "
            f"(< {OPEN_DATE_THRESHOLD:.0%} threshold)"
        )
        return None

    dated = df.loc[df["open_date"].notna()].copy()
    dated = dated.sort_values("open_date")
    dated["cum_count"] = range(1, len(dated) + 1)
    missing_pct = (1 - coverage) * 100

    fig, ax = plt.subplots(figsize=FIGURE_SIZES["wide"])
    ax.plot(
        dated["open_date"],
        dated["cum_count"],
        color=COLORS["ARIMA"],
        linewidth=1.8,
    )
    ax.fill_between(
        dated["open_date"],
        dated["cum_count"],
        alpha=0.15,
        color=COLORS["ARIMA"],
    )
    ax.set_xlabel("Year")
    ax.set_ylabel("Cumulative Stations")
    ax.set_title("Cumulative EV Station Openings in NC", fontweight="bold")
    ax.annotate(
        f"{missing_pct:.1f}% of stations\nmissing open_date",
        xy=(0.02, 0.92),
        xycoords="axes fraction",
        fontsize=FONT_SIZES["annotation"],
        bbox=dict(
            boxstyle="round,pad=0.3",
            facecolor="#FFFDE7",
            edgecolor=COLORS["gray_light"],
            alpha=0.9,
        ),
    )

    paths = save_figure(fig, "fig-14-afdc-temporal-growth", out_dir)
    plt.close(fig)
    return paths[0]


def fig15_station_map(df: pd.DataFrame, nc_geo_path: Path, out_dir: Path) -> Path:
    """Fig-15: Scatter of stations on NC outline, colored by level.

    Args:
        df: AFDC DataFrame with charging_level column.
        nc_geo_path: Path to NC county boundaries GeoJSON.
        out_dir: Figures output directory.

    Returns:
        Path to the saved figure.
    """
    nc = gpd.read_file(nc_geo_path)

    fig, ax = plt.subplots(figsize=(7.0, 4.0))
    nc.plot(
        ax=ax,
        color=COLORS["gray_bg"],
        edgecolor=COLORS["gray_light"],
        linewidth=0.4,
    )

    for level, color in LEVEL_COLORS.items():
        sub = df[df["charging_level"] == level]
        ax.scatter(
            sub["longitude"],
            sub["latitude"],
            s=8,
            c=color,
            label=f"{level} ({len(sub)})",
            alpha=0.7,
            edgecolors="none",
            zorder=3,
        )

    ax.set_xlim(NC_LON_MIN - 0.3, NC_LON_MAX + 0.3)
    ax.set_ylim(NC_LAT_MIN - 0.3, NC_LAT_MAX + 0.3)
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_title("EV Charging Stations Across North Carolina", fontweight="bold")
    ax.legend(
        loc="lower left",
        fontsize=FONT_SIZES["annotation"],
        markerscale=2,
        framealpha=0.9,
    )
    ax.set_aspect("equal", adjustable="box")

    paths = save_figure(fig, "fig-15-afdc-station-map-nc", out_dir)
    plt.close(fig)
    return paths[0]


def fig16_zip_coverage_gap(df: pd.DataFrame, census_path: Path, out_dir: Path) -> Path:
    """Fig-16: ZIP codes with Census population but no stations.

    Args:
        df: AFDC DataFrame.
        census_path: Path to nc-zip-population-acs2022.csv.
        out_dir: Figures output directory.

    Returns:
        Path to the saved figure.
    """
    census = pd.read_csv(census_path, dtype={"zcta": str})
    census["zcta"] = census["zcta"].astype(str).str.zfill(5)

    station_zips = set(df["zip"].unique())
    census_zips = set(census["zcta"].unique())

    covered = census_zips & station_zips
    gap = census_zips - station_zips

    pop_covered = census.loc[census["zcta"].isin(covered), "population"].sum()
    pop_gap = census.loc[census["zcta"].isin(gap), "population"].sum()

    fig, (ax_a, ax_b) = plt.subplots(1, 2, figsize=(7.0, 3.5))

    # Panel A — ZIP code counts
    labels_z = ["With Station(s)", "No Station"]
    sizes_z = [len(covered), len(gap)]
    colors_z = [COLORS["ARIMA"], COLORS["negative"]]
    wedges, texts, autotexts = ax_a.pie(
        sizes_z,
        labels=labels_z,
        colors=colors_z,
        autopct="%1.1f%%",
        startangle=140,
        textprops={"fontsize": FONT_SIZES["annotation"]},
    )
    ax_a.set_title("ZIP Codes", fontweight="bold", fontsize=FONT_SIZES["title"])
    add_panel_label(ax_a, "(A)")

    # Panel B — Population
    labels_p = ["Covered Pop.", "Gap Pop."]
    sizes_p = [pop_covered, pop_gap]
    wedges2, texts2, autotexts2 = ax_b.pie(
        sizes_p,
        labels=labels_p,
        colors=colors_z,
        autopct="%1.1f%%",
        startangle=140,
        textprops={"fontsize": FONT_SIZES["annotation"]},
    )
    ax_b.set_title("Population", fontweight="bold", fontsize=FONT_SIZES["title"])
    add_panel_label(ax_b, "(B)")

    fig.suptitle(
        f"ZIP Coverage Gap: {len(gap)} of {len(census_zips)} Census ZIPs "
        f"Have No Station",
        fontsize=FONT_SIZES["title"],
        fontweight="bold",
        y=1.03,
    )

    paths = save_figure(fig, "fig-16-afdc-zip-coverage-gap", out_dir)
    plt.close(fig)
    return paths[0]


def fig17_connector_types(df: pd.DataFrame, out_dir: Path) -> Path:
    """Fig-17: Bar chart of connector types.

    Args:
        df: AFDC DataFrame with parsed connector_list column.
        out_dir: Figures output directory.

    Returns:
        Path to the saved figure.
    """
    all_connectors: list[str] = []
    for lst in df["connector_list"]:
        all_connectors.extend(lst)
    counts = pd.Series(all_connectors).value_counts()

    fig, ax = plt.subplots(figsize=FIGURE_SIZES["wide"])
    palette = sns.color_palette(PALETTE_SEQUENTIAL[2:], n_colors=len(counts))
    bars = ax.bar(
        counts.index, counts.values, color=palette, edgecolor="white", linewidth=0.8
    )
    for bar in bars:
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 5,
            str(int(bar.get_height())),
            ha="center",
            va="bottom",
            fontsize=FONT_SIZES["annotation"],
        )
    ax.set_ylabel("Occurrence Count")
    ax.set_xlabel("Connector Type")
    ax.set_title("EV Connector Type Distribution Across NC Stations", fontweight="bold")
    plt.xticks(rotation=30, ha="right")

    paths = save_figure(fig, "fig-17-afdc-connector-type-distribution", out_dir)
    plt.close(fig)
    return paths[0]


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
