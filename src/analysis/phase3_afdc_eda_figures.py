#!/usr/bin/env python3
"""Phase 3 AFDC EDA: figure generators.

Produces figures fig-08 through fig-17 from the prepared AFDC DataFrame:
missingness, charging-level and network distributions, geographic coverage,
temporal growth, and connector types. Run via generate_phase3_afdc_eda.py.

Copyright © 2026 Wolfgang Sanyer
Licensed under the Polyform Noncommercial License 1.0.0 (see LICENSE).
"""

from __future__ import annotations

from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from phase3_afdc_eda_prep import (
    EV_RELEVANT_COLS,
    NC_LAT_MAX,
    NC_LAT_MIN,
    NC_LON_MAX,
    NC_LON_MIN,
)

from evpulse.style import (
    COLORS,
    FIGURE_SIZES,
    FONT_SIZES,
    PALETTE_SEQUENTIAL,
    add_panel_label,
    save_figure,
)

# Minimum % non-null for open_date to produce temporal figure
OPEN_DATE_THRESHOLD = 0.40

# Categorical charging-level palette
LEVEL_COLORS = {
    "L2-only": COLORS["ARIMA"],
    "DCFC-only": COLORS["negative"],
    "Mixed": COLORS["UCM"],
    "L1-only": COLORS["highlight"],
}


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
