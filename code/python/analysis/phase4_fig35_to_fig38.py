#!/usr/bin/env python3
"""
Phase 4: Publication Figures for Commuter-Flow Analysis (Figures 35-38).

Generates four publication-ready figures for the EV Pulse NC capstone:

    fig-35  Net Commuter Flow (Diverging Horizontal Bar)
    fig-36  Residential vs Residential+Workplace Demand (Grouped Bar)
    fig-37  County Commuter Typology Choropleth (100 NC counties)
    fig-38  Workplace Port Scenario Range (Dot-and-Whisker)

Input data produced by Phase 4 LODES/CTPP pipeline.
Output: 600 DPI, PDF + PNG dual export via save_figure().

Author: BIDA 670 EV-Pulse-NC Project
Date: 2026
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd

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

# Input CSV paths
_EMPLOYMENT_CSV = _DATA_DIR / "phase4-employment-centers.csv"
_COST_CSV = _DATA_DIR / "phase4-cost-effectiveness.csv"
_TOP10_CSV = _DATA_DIR / "phase3-top10-counties.csv"
_GEOJSON = _RAW_DIR / "nc-county-boundaries.geojson"
_OD_CSV = _RAW_DIR / "lehd-nc-od-main-2021.csv.gz"
_XWALK_CSV = _RAW_DIR / "lehd-nc-xwalk.csv.gz"

EXPORT_FORMATS = ["png", "pdf"]

# Typology colors
_CLR_EMP = COLORS["positive"]  # green
_CLR_BAL = COLORS["gray_medium"]  # gray
_CLR_BED = COLORS["negative"]  # red


# ===================================================================
# DATA LOADERS
# ===================================================================


def _load_employment_centers() -> pd.DataFrame:
    """Load the 15-row employment-centers CSV."""
    df = pd.read_csv(
        _EMPLOYMENT_CSV, dtype={"county_fips": str}
    )
    return df


def _load_cost_effectiveness() -> pd.DataFrame:
    """Load the 10-row cost-effectiveness CSV."""
    df = pd.read_csv(
        _COST_CSV, dtype={"county_fips": str}
    )
    return df


def _load_bev_counts() -> pd.DataFrame:
    """Load Phase 3 top-10 county BEV registration counts."""
    df = pd.read_csv(_TOP10_CSV)
    return df


# ===================================================================
# FIG-35: Net Commuter Flow (Diverging Horizontal Bar)
# ===================================================================


def generate_fig35(df: pd.DataFrame) -> None:
    """Diverging horizontal bar chart of net commuter flow."""
    print("[INFO] Generating fig-35: Net Commuter Flow ...")

    df_sorted = df.sort_values("net_commuting", ascending=True).copy()

    counties = df_sorted["county_name"].values
    net = df_sorted["net_commuting"].values
    typologies = df_sorted["typology"].values

    fig, ax = plt.subplots(figsize=(7.0, 5.5))

    y_pos = np.arange(len(counties))
    bar_colors = [
        _CLR_EMP if v > 0 else _CLR_BED for v in net
    ]

    ax.barh(
        y_pos,
        net,
        color=bar_colors,
        edgecolor="white",
        linewidth=0.5,
        zorder=2,
    )

    # Vertical zero line
    ax.axvline(0, color=COLORS["gray_dark"], linewidth=0.8, zorder=1)

    # Bar value labels
    for i, val in enumerate(net):
        label = f"+{val:,.0f}" if val > 0 else f"{val:,.0f}"
        offset = 3000 if val > 0 else -3000
        ha = "left" if val > 0 else "right"
        ax.text(
            val + offset,
            i,
            label,
            ha=ha,
            va="center",
            fontsize=FONT_SIZES["annotation"],
            color=COLORS["gray_dark"],
        )

    # Color-coded y-axis labels by typology
    ax.set_yticks(y_pos)
    ax.set_yticklabels(counties, fontsize=FONT_SIZES["tick_label"])
    for i, (label, typ) in enumerate(
        zip(ax.get_yticklabels(), typologies)
    ):
        if typ == "Employment Center":
            label.set_color(_CLR_EMP)
        elif typ == "Bedroom Community":
            label.set_color(_CLR_BED)
        else:
            label.set_color(_CLR_BAL)

    # Stats annotation
    ax.annotate(
        "8 Employment Centers | 75 Balanced"
        " | 17 Bedroom Communities\n(statewide)",
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
    )

    ax.set_title(
        "Net Commuter Flow by County"
        " \u2014 Top 15 Employment Destinations",
        fontsize=FONT_SIZES["title"],
        fontweight="bold",
    )
    ax.set_xlabel(
        "Net Commuting (Inbound minus Outbound Workers)",
        fontsize=FONT_SIZES["axis_label"],
    )
    ax.xaxis.set_major_formatter(
        mticker.FuncFormatter(lambda x, _: f"{x:,.0f}")
    )

    paths = save_figure(
        fig,
        "fig-35-net-commuter-flow",
        _OUTPUT_DIR,
        formats=EXPORT_FORMATS,
    )
    plt.close(fig)
    for p in paths:
        print(f"[SUCCESS] Saved {p}")


# ===================================================================
# FIG-36: Residential vs Workplace Demand (Grouped Horizontal Bar)
# ===================================================================


def generate_fig36(
    df: pd.DataFrame,
    bev_df: pd.DataFrame,
    cost_df: pd.DataFrame,
) -> None:
    """Grouped horizontal bar: residential BEV vs workplace-adjusted."""
    print(
        "[INFO] Generating fig-36: "
        "Residential vs Workplace Demand ..."
    )

    # Merge BEV counts onto employment-centers for scoring counties
    scoring_counties = cost_df["county_name"].tolist()
    df_10 = df[df["county_name"].isin(scoring_counties)].copy()

    bev_merged = bev_df.rename(columns={"County": "county_name"})
    df_10 = df_10.merge(
        bev_merged[["county_name", "BEV"]],
        on="county_name",
        how="left",
    )

    df_10 = df_10.sort_values(
        "adjusted_demand_75k", ascending=True
    ).copy()

    counties = df_10["county_name"].values
    bev_vals = df_10["BEV"].values.astype(float)
    workplace_vals = df_10["adjusted_demand_75k"].values

    fig, ax = plt.subplots(figsize=(7.0, 5.0))

    y_pos = np.arange(len(counties))
    bar_height = 0.35

    ax.barh(
        y_pos + bar_height / 2,
        bev_vals,
        height=bar_height,
        color=COLORS["neutral"],
        edgecolor="white",
        label="Residential BEV Count",
        zorder=2,
    )
    ax.barh(
        y_pos - bar_height / 2,
        workplace_vals,
        height=bar_height,
        color=COLORS["highlight"],
        edgecolor="white",
        label="Residential + Workplace Demand",
        zorder=2,
    )

    # Delta annotation (percentage increase)
    deltas = []
    for i in range(len(counties)):
        if bev_vals[i] > 0:
            pct = (workplace_vals[i] - bev_vals[i]) / bev_vals[i] * 100
        else:
            pct = 0.0
        deltas.append(pct)
        ax.text(
            workplace_vals[i] + max(workplace_vals) * 0.01,
            y_pos[i] - bar_height / 2,
            f"+{pct:.0f}%",
            ha="left",
            va="center",
            fontsize=FONT_SIZES["annotation"],
            color=COLORS["gray_dark"],
            fontweight="bold",
        )

    avg_delta = np.mean(deltas)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(counties, fontsize=FONT_SIZES["tick_label"])

    ax.annotate(
        f"Average increase: +{avg_delta:.0f}%",
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
        "Residential-Only vs. Workplace-Adjusted"
        " Charging Demand",
        fontsize=FONT_SIZES["title"],
        fontweight="bold",
    )
    ax.set_xlabel(
        "Estimated Charging Demand (Vehicles)",
        fontsize=FONT_SIZES["axis_label"],
    )
    ax.xaxis.set_major_formatter(
        mticker.FuncFormatter(lambda x, _: f"{x:,.0f}")
    )
    ax.legend(
        fontsize=FONT_SIZES["legend"], loc="lower right"
    )

    paths = save_figure(
        fig,
        "fig-36-demand-comparison",
        _OUTPUT_DIR,
        formats=EXPORT_FORMATS,
    )
    plt.close(fig)
    for p in paths:
        print(f"[SUCCESS] Saved {p}")


# ===================================================================
# FIG-37: County Typology Choropleth (all 100 NC counties)
# ===================================================================


def generate_fig37(
    df_15: pd.DataFrame,
    xwalk_path: Path,
    od_path: Path,
    county_shp_path: Path,
) -> None:
    """Choropleth of all 100 NC counties by commuter typology."""
    print(
        "[INFO] Generating fig-37: "
        "County Commuter Typology Choropleth ..."
    )
    try:
        import geopandas as gpd
    except ImportError:
        print(
            "[WARN] geopandas not available; "
            "skipping fig-37 choropleth."
        )
        return

    try:
        # --- Load crosswalk: block -> county FIPS ----
        xwalk = pd.read_csv(
            xwalk_path,
            compression="gzip",
            dtype=str,
            usecols=["tabblk2020", "cty"],
        )
        xwalk = xwalk.rename(
            columns={"tabblk2020": "block", "cty": "county_fips"}
        )

        # --- Load OD flows (memory-efficient) ---
        od = pd.read_csv(
            od_path,
            compression="gzip",
            dtype={"w_geocode": str, "h_geocode": str},
            usecols=["w_geocode", "h_geocode", "S000"],
        )

        # Map blocks to counties
        od = od.merge(
            xwalk.rename(
                columns={
                    "block": "w_geocode",
                    "county_fips": "w_county",
                }
            ),
            on="w_geocode",
            how="left",
        )
        od = od.merge(
            xwalk.rename(
                columns={
                    "block": "h_geocode",
                    "county_fips": "h_county",
                }
            ),
            on="h_geocode",
            how="left",
        )

        # Compute inbound and outbound per county
        inbound = (
            od.groupby("w_county")["S000"]
            .sum()
            .reset_index()
            .rename(
                columns={
                    "w_county": "county_fips",
                    "S000": "inbound",
                }
            )
        )
        outbound = (
            od.groupby("h_county")["S000"]
            .sum()
            .reset_index()
            .rename(
                columns={
                    "h_county": "county_fips",
                    "S000": "outbound",
                }
            )
        )

        flows = inbound.merge(
            outbound, on="county_fips", how="outer"
        ).fillna(0)
        flows["net"] = flows["inbound"] - flows["outbound"]

        # Classify typology
        def _classify(net: float) -> str:
            if net > 10_000:
                return "Employment Center"
            elif net < -10_000:
                return "Bedroom Community"
            return "Balanced"

        flows["typology"] = flows["net"].apply(_classify)

        # Count typologies
        typ_counts = flows["typology"].value_counts()
        n_emp = typ_counts.get("Employment Center", 0)
        n_bed = typ_counts.get("Bedroom Community", 0)

        # --- Load county boundaries ---
        gdf = gpd.read_file(county_shp_path)

        # Identify FIPS column
        fips_col = None
        for col in gdf.columns:
            if "fips" in col.lower() or "geoid" in col.lower():
                fips_col = col
                break
        if fips_col is None:
            # Try common alternatives
            for col in ["FIPS", "GEOID", "COUNTYFP", "fips"]:
                if col in gdf.columns:
                    fips_col = col
                    break
        if fips_col is None:
            print(
                "[WARN] Cannot identify FIPS column in "
                "GeoJSON; skipping fig-37."
            )
            return

        gdf[fips_col] = gdf[fips_col].astype(str)
        flows["county_fips"] = flows["county_fips"].astype(str)

        # Merge flows into geodataframe
        gdf = gdf.merge(
            flows[["county_fips", "typology", "net"]],
            left_on=fips_col,
            right_on="county_fips",
            how="left",
        )
        gdf["typology"] = gdf["typology"].fillna("Balanced")

        # Project to NC State Plane
        gdf = gdf.to_crs(epsg=32119)

        # Color map
        color_map = {
            "Employment Center": _CLR_EMP,
            "Balanced": COLORS["gray_light"],
            "Bedroom Community": _CLR_BED,
        }
        gdf["plot_color"] = gdf["typology"].map(color_map)

        fig, ax = plt.subplots(figsize=(7.0, 5.0))

        gdf.plot(
            ax=ax,
            color=gdf["plot_color"],
            edgecolor="white",
            linewidth=0.3,
        )

        # Label top 5 employment centers
        top5_labels = [
            "Mecklenburg",
            "Wake",
            "Durham",
            "Guilford",
            "Forsyth",
        ]

        # Identify name column
        name_col = None
        for col in gdf.columns:
            if "name" in col.lower() and col != "county_name":
                name_col = col
                break
        if name_col is None:
            name_col = "county_name" if "county_name" in gdf.columns else None

        if name_col:
            for label in top5_labels:
                match = gdf[
                    gdf[name_col].str.contains(
                        label, case=False, na=False
                    )
                ]
                if not match.empty:
                    centroid = match.geometry.centroid.iloc[0]
                    ax.annotate(
                        label,
                        xy=(centroid.x, centroid.y),
                        fontsize=FONT_SIZES["annotation"],
                        ha="center",
                        va="center",
                        fontweight="bold",
                        color=COLORS["gray_dark"],
                        bbox=dict(
                            boxstyle="round,pad=0.15",
                            facecolor="white",
                            edgecolor="none",
                            alpha=0.7,
                        ),
                    )

        # Legend
        from matplotlib.patches import Patch

        legend_handles = [
            Patch(
                facecolor=_CLR_EMP,
                edgecolor="white",
                label="Employment Center",
            ),
            Patch(
                facecolor=COLORS["gray_light"],
                edgecolor="white",
                label="Balanced",
            ),
            Patch(
                facecolor=_CLR_BED,
                edgecolor="white",
                label="Bedroom Community",
            ),
        ]
        ax.legend(
            handles=legend_handles,
            loc="lower left",
            fontsize=FONT_SIZES["legend"],
            framealpha=0.95,
        )

        # Stats annotation
        ax.annotate(
            f"N = 100 counties | {n_emp} Employment Centers"
            f" | {n_bed} Bedroom Communities",
            xy=(0.98, 0.02),
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
            "County Commuter Typology \u2014 Employment Centers"
            " vs. Bedroom Communities",
            fontsize=FONT_SIZES["title"],
            fontweight="bold",
        )
        ax.set_axis_off()

        paths = save_figure(
            fig,
            "fig-37-commuter-typology-map",
            _OUTPUT_DIR,
            formats=EXPORT_FORMATS,
        )
        plt.close(fig)
        for p in paths:
            print(f"[SUCCESS] Saved {p}")

    except Exception as exc:
        print(
            f"[WARN] fig-37 generation failed: {exc}. Skipping."
        )


# ===================================================================
# FIG-38: Workplace Port Scenario Range (Dot-and-Whisker)
# ===================================================================


def generate_fig38(
    df: pd.DataFrame, cost_df: pd.DataFrame
) -> None:
    """Dot-and-whisker plot of port scenario ranges."""
    print(
        "[INFO] Generating fig-38: "
        "Workplace Port Scenario Range ..."
    )

    scoring_counties = cost_df["county_name"].tolist()
    df_10 = df[df["county_name"].isin(scoring_counties)].copy()
    df_10 = df_10.sort_values(
        "ports_total_baseline", ascending=True
    )

    counties = df_10["county_name"].values
    baseline = df_10["ports_total_baseline"].values
    low = df_10["ports_total_low"].values
    high = df_10["ports_total_high"].values

    fig, ax = plt.subplots(figsize=(7.0, 4.5))

    y_pos = np.arange(len(counties))

    # Whisker lines (low to high)
    for i in range(len(counties)):
        ax.plot(
            [low[i], high[i]],
            [y_pos[i], y_pos[i]],
            color=COLORS["gray_medium"],
            linewidth=2,
            zorder=2,
            solid_capstyle="round",
        )

    # Baseline dots
    ax.scatter(
        baseline,
        y_pos,
        color=COLORS["neutral"],
        s=70,
        zorder=3,
        edgecolors="white",
        linewidths=0.8,
    )

    # Baseline value labels
    for i, val in enumerate(baseline):
        ax.text(
            val + max(high) * 0.02,
            y_pos[i],
            f"{val:,.0f}",
            ha="left",
            va="center",
            fontsize=FONT_SIZES["annotation"],
            color=COLORS["gray_dark"],
        )

    # Compute statewide totals from the 15-row dataset
    sw_baseline = df["ports_total_baseline"].sum()
    sw_l2 = df["ports_l2_baseline"].sum()
    sw_dcfc = df["ports_dcfc_baseline"].sum()

    ax.annotate(
        f"Statewide baseline: {sw_baseline:,.0f} ports"
        f" ({sw_l2:,.0f} L2 / {sw_dcfc:,.0f} DCFC)",
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

    ax.set_yticks(y_pos)
    ax.set_yticklabels(
        counties, fontsize=FONT_SIZES["tick_label"]
    )
    ax.set_title(
        "Workplace Charging Port Estimates"
        " \u2014 Low, Baseline, and High Scenarios",
        fontsize=FONT_SIZES["title"],
        fontweight="bold",
    )
    ax.set_xlabel(
        "Estimated Workplace Ports Needed",
        fontsize=FONT_SIZES["axis_label"],
    )
    ax.xaxis.set_major_formatter(
        mticker.FuncFormatter(lambda x, _: f"{x:,.0f}")
    )

    paths = save_figure(
        fig,
        "fig-38-port-scenario-range",
        _OUTPUT_DIR,
        formats=EXPORT_FORMATS,
    )
    plt.close(fig)
    for p in paths:
        print(f"[SUCCESS] Saved {p}")


# ===================================================================
# MAIN
# ===================================================================


def main() -> None:
    """Generate all Phase 4 publication figures."""
    setup_publication_style()

    df = _load_employment_centers()
    cost_df = _load_cost_effectiveness()
    bev_df = _load_bev_counts()

    generate_fig35(df)
    generate_fig36(df, bev_df, cost_df)
    generate_fig37(df, _XWALK_CSV, _OD_CSV, _GEOJSON)
    generate_fig38(df, cost_df)

    print("[INFO] All Phase 4 figures complete.")


if __name__ == "__main__":
    main()
