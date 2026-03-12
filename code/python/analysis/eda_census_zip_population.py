#!/usr/bin/env python3
"""
EDA and Descriptive Analysis: Census ZCTA Population Data (ACS 2022)

Performs exploratory data analysis on NC Census ZCTA population data,
validates join keys against AFDC charging station ZIP codes, and
produces publication-quality figures and summary CSVs.

Figures produced:
    fig-18: ZCTA population distribution histogram (log-scale x-axis)
    fig-19: ZCTA population box plot with top-5 outlier labels
    fig-20: AFDC ZIP match summary (matched / AFDC-only / Census-only)
    fig-21: ZCTA population bands with station count overlay

Author: BIDA 670 EV-Pulse-NC Project
Date: 2026
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Resolve project paths so imports work regardless of cwd
# ---------------------------------------------------------------------------
_SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPT_DIR))

from publication_style import (  # noqa: E402
    COLORS,
    FIGURE_SIZES,
    FONT_SIZES,
    add_stats_annotation,
    save_figure,
    setup_publication_style,
)

# =============================================================================
# CONSTANTS
# =============================================================================

PROJECT_ROOT = _SCRIPT_DIR.parent.parent.parent

DEFAULT_CENSUS_CSV = PROJECT_ROOT / "data" / "raw" / "nc-zip-population-acs2022.csv"
DEFAULT_AFDC_CSV = (
    PROJECT_ROOT / "data" / "raw" / "afdc-charging-stations-connector-2026-02.csv"
)
DEFAULT_GEOJSON = PROJECT_ROOT / "data" / "raw" / "nc-county-boundaries.geojson"
DEFAULT_FIG_DIR = PROJECT_ROOT / "output" / "figures"
DEFAULT_CSV_DIR = PROJECT_ROOT / "data" / "processed"

NC_ZCTA_PREFIXES = ("27", "28")
NC_APPROX_POPULATION = 10_600_000  # ~10.6M (2022 ACS estimate)
NC_COUNTY_COUNT = 100
NC_STATEFP = "37"

POPULATION_BANDS: list[tuple[str, int, int]] = [
    ("0 - 1 k", 0, 1_000),
    ("1 k - 5 k", 1_000, 5_000),
    ("5 k - 10 k", 5_000, 10_000),
    ("10 k - 25 k", 10_000, 25_000),
    ("25 k - 50 k", 25_000, 50_000),
    ("50 k+", 50_000, 10_000_000),
]


# =============================================================================
# DATA LOADING & VALIDATION
# =============================================================================


def load_census_data(path: Path) -> pd.DataFrame:
    """Load and validate NC Census ZCTA population CSV.

    Args:
        path: Path to the Census CSV file.

    Returns:
        Validated DataFrame with columns [name, population, zcta].
    """
    df = pd.read_csv(path, dtype={"zcta": str})
    df["population"] = df["population"].astype(int)
    df["zcta"] = df["zcta"].astype(str).str.zfill(5)
    return df


def load_afdc_data(path: Path) -> pd.DataFrame:
    """Load AFDC charging station CSV, keeping only needed columns.

    Args:
        path: Path to the AFDC CSV file.

    Returns:
        DataFrame with at least the 'zip' column (plus city, id for diagnostics).
    """
    cols = ["id", "zip", "city", "state"]
    df = pd.read_csv(path, usecols=cols, dtype={"zip": str})
    df["zip"] = df["zip"].astype(str).str.zfill(5)
    return df


def load_geojson(path: Path) -> gpd.GeoDataFrame:
    """Load NC county boundaries GeoJSON.

    Args:
        path: Path to the GeoJSON file.

    Returns:
        GeoDataFrame of county boundaries.
    """
    return gpd.read_file(path)


# =============================================================================
# EDA FUNCTIONS
# =============================================================================


def eda_volume_shape(df: pd.DataFrame, label: str) -> None:
    """Print volume and shape summary for a DataFrame.

    Args:
        df: Input DataFrame.
        label: Descriptive label for the dataset.
    """
    mem_mb = df.memory_usage(deep=True).sum() / 1_048_576
    print(f"\n{'=' * 60}")
    print(f"  {label}")
    print(f"{'=' * 60}")
    print(f"  Rows:    {len(df):,}")
    print(f"  Columns: {len(df.columns)}")
    print(f"  Memory:  {mem_mb:.2f} MB")
    print(f"  Dtypes:\n{df.dtypes.to_string()}")


def eda_missing_values(df: pd.DataFrame, label: str) -> None:
    """Report missing values.

    Args:
        df: Input DataFrame.
        label: Descriptive label for the dataset.
    """
    missing = df.isnull().sum()
    total_missing = missing.sum()
    print(f"\n--- Missing Values: {label} ---")
    if total_missing == 0:
        print("  No missing values found.")
    else:
        for col, cnt in missing[missing > 0].items():
            print(f"  {col}: {cnt} missing ({cnt / len(df) * 100:.1f}%)")


def eda_census_quality(df: pd.DataFrame) -> list[str]:
    """Validate Census data quality rules.

    Args:
        df: Census DataFrame.

    Returns:
        List of quality issue descriptions (empty if clean).
    """
    issues: list[str] = []

    # ZCTA format: 5-digit starting with 27 or 28
    bad_prefix = df[~df["zcta"].str[:2].isin(NC_ZCTA_PREFIXES)]
    if len(bad_prefix) > 0:
        issues.append(
            f"  {len(bad_prefix)} ZCTAs do not start with 27/28: "
            f"{bad_prefix['zcta'].tolist()[:10]}"
        )

    bad_len = df[df["zcta"].str.len() != 5]
    if len(bad_len) > 0:
        issues.append(f"  {len(bad_len)} ZCTAs are not 5-digit")

    # Population non-negative
    neg_pop = df[df["population"] < 0]
    if len(neg_pop) > 0:
        issues.append(f"  {len(neg_pop)} ZCTAs have negative population")

    # Name pattern
    bad_name = df[~df["name"].str.match(r"^ZCTA5 \d{5}$")]
    if len(bad_name) > 0:
        issues.append(
            f"  {len(bad_name)} names do not match 'ZCTA5 XXXXX' pattern: "
            f"{bad_name['name'].tolist()[:5]}"
        )

    # Name-ZCTA consistency
    df_check = df.copy()
    df_check["expected_name"] = "ZCTA5 " + df_check["zcta"]
    mismatch = df_check[df_check["name"] != df_check["expected_name"]]
    if len(mismatch) > 0:
        issues.append(f"  {len(mismatch)} name/zcta mismatches")

    # Duplicates
    dups = df[df["zcta"].duplicated(keep=False)]
    if len(dups) > 0:
        issues.append(f"  {len(dups)} duplicate ZCTA rows")

    # Zero population
    zero_pop = df[df["population"] == 0]
    if len(zero_pop) > 0:
        issues.append(
            f"  {len(zero_pop)} ZCTAs with population = 0 (uninhabited, valid)"
        )

    # Very low population
    low_pop = df[(df["population"] > 0) & (df["population"] < 50)]
    if len(low_pop) > 0:
        issues.append(f"  {len(low_pop)} ZCTAs with population 1-49 (very low)")

    print("\n--- Data Quality: Census ---")
    if not issues:
        print("  All quality checks passed.")
    else:
        for issue in issues:
            print(issue)

    return issues


def eda_geojson_validation(gdf: gpd.GeoDataFrame) -> None:
    """Validate county boundary GeoJSON.

    Args:
        gdf: GeoDataFrame of county boundaries.
    """
    print("\n--- GeoJSON Validation: County Boundaries ---")
    print(f"  Feature count: {len(gdf)} (expected {NC_COUNTY_COUNT})")

    # STATEFP check
    if "STATEFP" in gdf.columns:
        unique_states = gdf["STATEFP"].unique()
        all_nc = all(s == NC_STATEFP for s in unique_states)
        print(f"  All STATEFP == '37': {all_nc} (unique: {unique_states})")
    else:
        print("  WARNING: STATEFP column not found")

    # Missing NAME / COUNTYFP
    for col in ["NAME", "COUNTYFP"]:
        if col in gdf.columns:
            n_missing = gdf[col].isnull().sum()
            print(f"  Missing {col}: {n_missing}")
        else:
            print(f"  WARNING: {col} column not found")

    # Geometry validity
    invalid_geom = gdf[~gdf.geometry.is_valid]
    print(f"  Invalid geometries: {len(invalid_geom)}")

    # CRS
    print(f"  CRS: {gdf.crs}")


def eda_population_stats(df: pd.DataFrame) -> dict:
    """Compute population distribution summary statistics.

    Args:
        df: Census DataFrame.

    Returns:
        Dictionary of summary statistics.
    """
    pop = df["population"]
    summary = {
        "count": len(pop),
        "mean": pop.mean(),
        "median": pop.median(),
        "std": pop.std(),
        "min": pop.min(),
        "max": pop.max(),
        "q25": pop.quantile(0.25),
        "q75": pop.quantile(0.75),
        "skewness": float(pop.skew()),
        "kurtosis": float(pop.kurtosis()),
        "total": pop.sum(),
        "pct_of_nc": pop.sum() / NC_APPROX_POPULATION * 100,
    }

    print("\n--- Population Distribution ---")
    for k, v in summary.items():
        if isinstance(v, float):
            print(f"  {k}: {v:,.2f}")
        else:
            print(f"  {k}: {v:,}")

    print(f"\n  Total ZCTA population: {summary['total']:,}")
    print(f"  NC approximate pop (~10.6M): coverage = {summary['pct_of_nc']:.1f}%")
    print(
        "  NOTE: ZCTAs != USPS ZIP codes. ZCTAs are Census-defined geographic"
        " areas that approximate ZIP code service areas. Some USPS ZIP codes"
        " (PO Boxes, unique delivery) have no corresponding ZCTA."
    )
    return summary


def assign_population_band(population: int) -> str:
    """Assign a population band label.

    Args:
        population: Population count.

    Returns:
        Band label string.
    """
    for label, lo, hi in POPULATION_BANDS:
        if lo <= population < hi:
            return label
    return POPULATION_BANDS[-1][0]


# =============================================================================
# JOIN-KEY VALIDATION
# =============================================================================


def join_key_analysis(
    census_df: pd.DataFrame, afdc_df: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Perform join-key validation between Census ZCTAs and AFDC ZIPs.

    Args:
        census_df: Census DataFrame with 'zcta' column.
        afdc_df: AFDC DataFrame with 'zip' column.

    Returns:
        Tuple of (eda_summary_df, match_report_df, unmatched_df).
    """
    census_zctas = set(census_df["zcta"].unique())

    # Station counts by ZIP
    station_counts = (
        afdc_df.groupby("zip")
        .agg(
            station_count=("id", "nunique"),
            cities=("city", lambda x: ", ".join(sorted(x.dropna().unique()))),
        )
        .reset_index()
    )
    station_counts.rename(columns={"zip": "afdc_zip"}, inplace=True)

    afdc_zips = set(station_counts["afdc_zip"].unique())

    matched = census_zctas & afdc_zips
    afdc_only = afdc_zips - census_zctas
    census_only = census_zctas - afdc_zips

    print("\n--- Join-Key Validation: Census ZCTA vs AFDC ZIP ---")
    print(f"  Unique Census ZCTAs:  {len(census_zctas):,}")
    print(f"  Unique AFDC ZIPs:     {len(afdc_zips):,}")
    print(f"  Matched:              {len(matched):,}")
    print(f"  AFDC-only (no ZCTA):  {len(afdc_only):,}")
    print(f"  Census-only (no stn): {len(census_only):,}")
    print(f"  Match rate (AFDC):    {len(matched) / len(afdc_zips) * 100:.1f}%")
    print(f"  Match rate (Census):  {len(matched) / len(census_zctas) * 100:.1f}%")

    # Census-only: total population with no stations
    census_only_pop = census_df[census_df["zcta"].isin(census_only)]["population"].sum()
    print(
        f"  Census-only total pop: {census_only_pop:,}"
        f" ({census_only_pop / census_df['population'].sum() * 100:.1f}%"
        " of Census total)"
    )

    # Investigate AFDC-only ZIPs
    if afdc_only:
        print(f"\n  AFDC-only ZIPs (no Census ZCTA match) — {len(afdc_only)} total:")
        afdc_only_df = station_counts[
            station_counts["afdc_zip"].isin(afdc_only)
        ].sort_values("station_count", ascending=False)
        for _, row in afdc_only_df.head(15).iterrows():
            prefix_note = ""
            if not row["afdc_zip"].startswith(("27", "28")):
                prefix_note = " [non-NC prefix]"
            print(
                f"    ZIP {row['afdc_zip']}: {row['station_count']} station(s)"
                f" — {row['cities']}{prefix_note}"
            )
        print(
            "  Likely causes: PO Box ZIPs, unique delivery ZIPs,"
            " cross-state ZIPs, or data entry errors."
        )

    # --- Build output DataFrames ---

    # 1. EDA Summary: one row per ZCTA
    eda_summary = census_df[["zcta", "population"]].copy()
    eda_summary["has_afdc_station"] = eda_summary["zcta"].isin(matched)

    # Merge station counts
    sc_map = station_counts.set_index("afdc_zip")["station_count"]
    eda_summary["station_count"] = eda_summary["zcta"].map(sc_map).fillna(0).astype(int)
    eda_summary["population_band"] = eda_summary["population"].apply(
        assign_population_band
    )

    # 2. Match report: every unique ZIP/ZCTA with status
    rows = []
    for z in sorted(matched):
        pop = census_df.loc[census_df["zcta"] == z, "population"].iloc[0]
        sc = int(sc_map.get(z, 0))
        rows.append(
            {
                "zip_zcta": z,
                "match_status": "matched",
                "station_count": sc,
                "population": pop,
            }
        )
    for z in sorted(afdc_only):
        sc = int(sc_map.get(z, 0))
        rows.append(
            {
                "zip_zcta": z,
                "match_status": "afdc_only",
                "station_count": sc,
                "population": None,
            }
        )
    for z in sorted(census_only):
        pop = census_df.loc[census_df["zcta"] == z, "population"].iloc[0]
        rows.append(
            {
                "zip_zcta": z,
                "match_status": "census_only",
                "station_count": 0,
                "population": pop,
            }
        )
    match_report = pd.DataFrame(rows)

    # 3. Unmatched AFDC ZIPs
    unmatched = station_counts[station_counts["afdc_zip"].isin(afdc_only)].copy()
    unmatched.rename(columns={"afdc_zip": "zip", "cities": "city_names"}, inplace=True)
    unmatched = unmatched.sort_values("station_count", ascending=False).reset_index(
        drop=True
    )

    return eda_summary, match_report, unmatched


# =============================================================================
# FIGURE GENERATION
# =============================================================================


def fig18_population_histogram(
    df: pd.DataFrame,
    pop_stats: dict,
    output_dir: Path,
) -> None:
    """Create fig-18: ZCTA population distribution histogram (log x-axis).

    Args:
        df: Census DataFrame.
        pop_stats: Population summary statistics dict.
        output_dir: Figure output directory.
    """
    pop = df["population"]
    pop_pos = pop[pop > 0]

    fig, ax = plt.subplots(figsize=FIGURE_SIZES["wide"])

    # Log-spaced bins
    bins = np.logspace(np.log10(pop_pos.min()), np.log10(pop_pos.max()), 40)
    ax.hist(
        bins[:-1],
        bins=bins,
        weights=np.histogram(pop_pos, bins=bins)[0],
        color=COLORS["neutral"],
        edgecolor="white",
        alpha=0.85,
    )

    ax.set_xscale("log")
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))

    # Median and mean lines
    ax.axvline(
        pop_stats["median"],
        color=COLORS["negative"],
        linestyle="--",
        linewidth=1.5,
        label=f"Median: {pop_stats['median']:,.0f}",
    )
    ax.axvline(
        pop_stats["mean"],
        color=COLORS["highlight"],
        linestyle="-.",
        linewidth=1.5,
        label=f"Mean: {pop_stats['mean']:,.0f}",
    )

    ax.set_xlabel("Population (log scale)")
    ax.set_ylabel("Number of ZCTAs")
    ax.set_title("Fig 18: NC ZCTA Population Distribution (ACS 2022)")
    ax.legend(fontsize=FONT_SIZES["legend"])

    stats_text = (
        f"n = {pop_stats['count']}\n"
        f"Skew = {pop_stats['skewness']:.2f}\n"
        f"Min = {pop_stats['min']:,}\n"
        f"Max = {pop_stats['max']:,}"
    )
    add_stats_annotation(ax, stats_text, loc="upper right")

    paths = save_figure(fig, "fig-18-zcta-population-distribution", output_dir)
    plt.close(fig)
    print(f"  Saved: {[str(p) for p in paths]}")


def fig19_population_boxplot(
    df: pd.DataFrame,
    output_dir: Path,
) -> None:
    """Create fig-19: ZCTA population box plot with top-5 outlier labels.

    Args:
        df: Census DataFrame.
        output_dir: Figure output directory.
    """
    fig, ax = plt.subplots(figsize=(7.0, 5.0))

    ax.boxplot(
        df["population"],
        vert=True,
        patch_artist=True,
        widths=0.5,
        boxprops=dict(facecolor=COLORS["neutral"], alpha=0.7),
        medianprops=dict(color=COLORS["negative"], linewidth=2),
        flierprops=dict(
            marker="o",
            markersize=4,
            markerfacecolor=COLORS["gray_medium"],
            markeredgecolor="white",
        ),
    )

    # Top 5 outliers
    top5 = df.nlargest(5, "population")
    for _, row in top5.iterrows():
        ax.annotate(
            f"{row['name'].replace('ZCTA5 ', '')}\n({row['population']:,})",
            xy=(1, row["population"]),
            xytext=(1.15, row["population"]),
            fontsize=FONT_SIZES["annotation"],
            arrowprops=dict(arrowstyle="-", color=COLORS["gray_medium"], lw=0.8),
            va="center",
        )

    ax.set_ylabel("Population")
    ax.set_title("Fig 19: NC ZCTA Population Box Plot (ACS 2022)")
    ax.set_xticks([])
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))

    paths = save_figure(fig, "fig-19-zcta-population-boxplot", output_dir)
    plt.close(fig)
    print(f"  Saved: {[str(p) for p in paths]}")


def fig20_afdc_match_summary(
    match_report: pd.DataFrame,
    output_dir: Path,
) -> None:
    """Create fig-20: Horizontal stacked bar showing join-key match rates.

    Args:
        match_report: Match report DataFrame.
        output_dir: Figure output directory.
    """
    counts = match_report["match_status"].value_counts()
    matched = counts.get("matched", 0)
    afdc_only = counts.get("afdc_only", 0)
    census_only = counts.get("census_only", 0)
    total = matched + afdc_only + census_only

    fig, ax = plt.subplots(figsize=FIGURE_SIZES["wide"])

    categories = ["All ZIP/ZCTAs"]
    bar_data = [
        ("Matched", matched, COLORS["positive"]),
        ("AFDC-only\n(no Census ZCTA)", afdc_only, COLORS["highlight"]),
        ("Census-only\n(no stations)", census_only, COLORS["neutral"]),
    ]

    left = 0
    for label, count, color in bar_data:
        ax.barh(
            categories,
            count,
            left=left,
            color=color,
            label=label,
            edgecolor="white",
            height=0.5,
        )
        # Label inside bar if wide enough
        if count / total > 0.05:
            ax.text(
                left + count / 2,
                0,
                f"{count}\n({count / total * 100:.1f}%)",
                ha="center",
                va="center",
                fontsize=FONT_SIZES["annotation"],
                fontweight="bold",
                color="white" if color != COLORS["highlight"] else COLORS["gray_dark"],
            )
        left += count

    ax.set_xlabel("Number of Unique ZIP / ZCTA Codes")
    ax.set_title("Fig 20: AFDC ZIP vs Census ZCTA Join-Key Match Summary")
    ax.legend(loc="upper right", fontsize=FONT_SIZES["legend"])
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))

    paths = save_figure(fig, "fig-20-afdc-zip-match-summary", output_dir)
    plt.close(fig)
    print(f"  Saved: {[str(p) for p in paths]}")


def fig21_population_bands(
    eda_summary: pd.DataFrame,
    output_dir: Path,
) -> None:
    """Create fig-21: ZCTAs binned by population band with station overlay.

    Args:
        eda_summary: EDA summary DataFrame with population_band and station_count.
        output_dir: Figure output directory.
    """
    band_order = [b[0] for b in POPULATION_BANDS]
    band_stats = (
        eda_summary.groupby("population_band")
        .agg(
            zcta_count=("zcta", "count"),
            total_stations=("station_count", "sum"),
        )
        .reindex(band_order)
        .fillna(0)
        .astype(int)
    )

    fig, ax1 = plt.subplots(figsize=FIGURE_SIZES["wide"])

    x = np.arange(len(band_stats))
    width = 0.45

    bars1 = ax1.bar(
        x - width / 2,
        band_stats["zcta_count"],
        width,
        color=COLORS["neutral"],
        edgecolor="white",
        label="ZCTA count",
    )
    ax1.set_ylabel("Number of ZCTAs", color=COLORS["neutral"])
    ax1.set_xlabel("Population Band")
    ax1.set_xticks(x)
    ax1.set_xticklabels(band_stats.index, rotation=15, ha="right")

    # Value labels on ZCTA bars
    for bar in bars1:
        height = bar.get_height()
        if height > 0:
            ax1.text(
                bar.get_x() + bar.get_width() / 2,
                height + 2,
                f"{int(height)}",
                ha="center",
                va="bottom",
                fontsize=FONT_SIZES["annotation"],
            )

    # Station count overlay on secondary axis
    ax2 = ax1.twinx()
    bars2 = ax2.bar(
        x + width / 2,
        band_stats["total_stations"],
        width,
        color=COLORS["highlight"],
        edgecolor="white",
        alpha=0.85,
        label="Station count",
    )
    ax2.set_ylabel("Number of Stations", color=COLORS["highlight"])

    for bar in bars2:
        height = bar.get_height()
        if height > 0:
            ax2.text(
                bar.get_x() + bar.get_width() / 2,
                height + 2,
                f"{int(height)}",
                ha="center",
                va="bottom",
                fontsize=FONT_SIZES["annotation"],
                color=COLORS["highlight"],
            )

    ax1.set_title("Fig 21: ZCTA Population Bands with Station Count Overlay")

    # Combined legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(
        lines1 + lines2,
        labels1 + labels2,
        loc="upper right",
        fontsize=FONT_SIZES["legend"],
    )

    paths = save_figure(fig, "fig-21-zcta-population-bands", output_dir)
    plt.close(fig)
    print(f"  Saved: {[str(p) for p in paths]}")


# =============================================================================
# MAIN
# =============================================================================


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments.

    Returns:
        Parsed argument namespace.
    """
    parser = argparse.ArgumentParser(
        description="EDA & Descriptive Analysis: NC Census ZCTA Population"
    )
    parser.add_argument(
        "--census-csv",
        type=Path,
        default=DEFAULT_CENSUS_CSV,
        help="Path to Census ZCTA population CSV",
    )
    parser.add_argument(
        "--afdc-csv",
        type=Path,
        default=DEFAULT_AFDC_CSV,
        help="Path to AFDC charging stations CSV",
    )
    parser.add_argument(
        "--geojson",
        type=Path,
        default=DEFAULT_GEOJSON,
        help="Path to NC county boundaries GeoJSON",
    )
    parser.add_argument(
        "--fig-dir",
        type=Path,
        default=DEFAULT_FIG_DIR,
        help="Output directory for figures",
    )
    parser.add_argument(
        "--csv-dir",
        type=Path,
        default=DEFAULT_CSV_DIR,
        help="Output directory for processed CSVs",
    )
    return parser.parse_args()


def main() -> None:
    """Run the full EDA pipeline."""
    args = parse_args()

    # Apply publication style
    setup_publication_style()

    print("=" * 60)
    print("  EDA: Census ZCTA Population (ACS 2022)")
    print("=" * 60)

    # ------------------------------------------------------------------
    # 1. Load data
    # ------------------------------------------------------------------
    print("\n[1/7] Loading data...")
    census_df = load_census_data(args.census_csv)
    afdc_df = load_afdc_data(args.afdc_csv)
    try:
        county_gdf = load_geojson(args.geojson)
    except Exception as e:
        print(f"  WARNING: Could not load GeoJSON: {e}")
        county_gdf = None

    # ------------------------------------------------------------------
    # 2. Volume / shape
    # ------------------------------------------------------------------
    print("\n[2/7] Volume and shape...")
    eda_volume_shape(census_df, "Census ZCTA Population")
    eda_volume_shape(afdc_df, "AFDC Charging Stations (subset)")

    # ------------------------------------------------------------------
    # 3. Missing values
    # ------------------------------------------------------------------
    print("\n[3/7] Missing values...")
    eda_missing_values(census_df, "Census")
    eda_missing_values(afdc_df, "AFDC")

    # ------------------------------------------------------------------
    # 4. Data quality & standardization
    # ------------------------------------------------------------------
    print("\n[4/7] Data quality & standardization...")
    eda_census_quality(census_df)

    # Confirm column names are snake_case
    print("\n--- Column Name Check ---")
    for col in census_df.columns:
        is_snake = col == col.lower() and " " not in col
        print(f"  {col}: {'OK' if is_snake else 'NOT snake_case'}")

    # Confirm zcta is string
    print(f"\n  zcta dtype: {census_df['zcta'].dtype} (should be object/string)")

    # ------------------------------------------------------------------
    # 5. GeoJSON validation
    # ------------------------------------------------------------------
    if county_gdf is not None:
        eda_geojson_validation(county_gdf)

    # ------------------------------------------------------------------
    # 6. Population distribution & outliers
    # ------------------------------------------------------------------
    print("\n[5/7] Population distribution...")
    pop_stats = eda_population_stats(census_df)

    # Outlier flags
    print("\n--- Outlier Summary ---")
    zero_pop = census_df[census_df["population"] == 0]
    very_low = census_df[(census_df["population"] > 0) & (census_df["population"] < 50)]
    q75 = pop_stats["q75"]
    iqr = q75 - pop_stats["q25"]
    upper_fence = q75 + 1.5 * iqr
    very_high = census_df[census_df["population"] > upper_fence]
    print(f"  Population = 0:         {len(zero_pop)}")
    print(f"  Population 1-49:        {len(very_low)}")
    print(f"  Upper fence ({upper_fence:,.0f}): {len(very_high)} ZCTAs above")
    if len(very_high) > 0:
        top10 = very_high.nlargest(10, "population")
        for _, row in top10.iterrows():
            print(f"    {row['zcta']} ({row['name']}): {row['population']:,}")

    # ------------------------------------------------------------------
    # 7. Join-key validation
    # ------------------------------------------------------------------
    print("\n[6/7] Join-key validation...")
    eda_summary, match_report, unmatched = join_key_analysis(census_df, afdc_df)

    # ------------------------------------------------------------------
    # 8. Figures
    # ------------------------------------------------------------------
    print("\n[7/7] Generating figures...")
    args.fig_dir.mkdir(parents=True, exist_ok=True)
    args.csv_dir.mkdir(parents=True, exist_ok=True)

    try:
        fig18_population_histogram(census_df, pop_stats, args.fig_dir)
    except Exception as e:
        print(f"  SKIP fig-18: {e}")

    try:
        fig19_population_boxplot(census_df, args.fig_dir)
    except Exception as e:
        print(f"  SKIP fig-19: {e}")

    try:
        fig20_afdc_match_summary(match_report, args.fig_dir)
    except Exception as e:
        print(f"  SKIP fig-20: {e}")

    try:
        fig21_population_bands(eda_summary, args.fig_dir)
    except Exception as e:
        print(f"  SKIP fig-21: {e}")

    # ------------------------------------------------------------------
    # 9. CSV outputs
    # ------------------------------------------------------------------
    print("\n--- Saving CSV outputs ---")

    eda_summary.to_csv(args.csv_dir / "census-zcta-eda-summary.csv", index=False)
    print(f"  Saved: {args.csv_dir / 'census-zcta-eda-summary.csv'}")

    match_report.to_csv(args.csv_dir / "afdc-zip-match-report.csv", index=False)
    print(f"  Saved: {args.csv_dir / 'afdc-zip-match-report.csv'}")

    unmatched.to_csv(args.csv_dir / "afdc-unmatched-zips.csv", index=False)
    print(f"  Saved: {args.csv_dir / 'afdc-unmatched-zips.csv'}")

    # ------------------------------------------------------------------
    # Final summary
    # ------------------------------------------------------------------
    print("\n" + "=" * 60)
    print("  EDA COMPLETE")
    print("=" * 60)
    print(f"  Census ZCTAs:     {len(census_df):,}")
    print(f"  AFDC stations:    {len(afdc_df):,} rows")
    print(f"  Matched ZIPs:     {(match_report['match_status'] == 'matched').sum():,}")
    print(
        f"  AFDC-only ZIPs:   {(match_report['match_status'] == 'afdc_only').sum():,}"
    )
    print(
        f"  Census-only ZCTAs:"
        f" {(match_report['match_status'] == 'census_only').sum():,}"
    )
    print(f"  Figures saved to: {args.fig_dir}")
    print(f"  CSVs saved to:    {args.csv_dir}")


if __name__ == "__main__":
    main()
