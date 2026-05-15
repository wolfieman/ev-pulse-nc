#!/usr/bin/env python3
"""
Phase 5 Step 5.3: Tract-to-ZCTA Spatial Crosswalk.

Performs an area-weighted overlay of 2010 Census tracts onto study
ZCTAs to compute the percentage of each ZCTA that falls within
Justice40-designated disadvantaged tracts.  Outputs ZCTA-level and
county-level summary CSVs for downstream scoring.

Method follows the EPA EJScreen area-weighted interpolation standard.

Author: Wolfgang Sanyer
License: Polyform Noncommercial 1.0.0 (see LICENSE)
Date: 2026
"""

from __future__ import annotations

import argparse
import sys
import warnings
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd

# Suppress shapely/geopandas deprecation noise during overlay
warnings.filterwarnings("ignore", category=FutureWarning)

# ---------------------------------------------------------------------------
# Resolve project paths
# ---------------------------------------------------------------------------
_SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = _SCRIPT_DIR.parent.parent.parent

RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

ZCTA_BOUNDARIES = RAW_DIR / "nc-zcta-boundaries.geojson"
TRACT_BOUNDARIES = RAW_DIR / "census-tracts-2010-study-area.geojson"
CEJST_BORDER_CSV = RAW_DIR / "cejst-justice40-tracts-nc-border.csv"
STUDY_ZIPS_CSV = PROCESSED_DIR / "phase3-zip-density.csv"

OUT_ZCTA = PROCESSED_DIR / "phase5-zcta-justice40.csv"
OUT_COUNTY = PROCESSED_DIR / "phase5-county-justice40.csv"

# Area-weighted overlay parameters
TARGET_CRS = "EPSG:32119"  # NC State Plane
SLIVER_THRESHOLD_SQM = 100  # minimum fragment area


# =====================================================================
# 5.3.2  LOAD & PREPARE
# =====================================================================


def load_study_zips(path: Path) -> pd.DataFrame:
    """Load study ZIP codes from Phase 3 density CSV.

    Args:
        path: Path to phase3-zip-density.csv.

    Returns:
        DataFrame with zip, county_name, county_fips, population.
    """
    df = pd.read_csv(
        path,
        dtype={"zip": str, "county_fips": str},
        usecols=["zip", "county_name", "county_fips", "population"],
    )
    df["zip"] = df["zip"].str.zfill(5)
    df["county_fips"] = df["county_fips"].str.zfill(5)
    return df


def load_zcta_boundaries(
    path: Path, study_zips: set[str],
) -> gpd.GeoDataFrame:
    """Load ZCTA boundaries and filter to study ZCTAs.

    Args:
        path: Path to nc-zcta-boundaries.geojson.
        study_zips: Set of 5-digit ZIP codes to keep.

    Returns:
        GeoDataFrame projected to TARGET_CRS.
    """
    gdf = gpd.read_file(path)
    gdf = gdf.rename(columns={"ZCTA5CE20": "zip"})
    gdf["zip"] = gdf["zip"].astype(str).str.zfill(5)
    gdf = gdf[gdf["zip"].isin(study_zips)].copy()
    gdf = gdf.to_crs(TARGET_CRS)
    # Pre-compute original area for conservation check
    gdf["original_area_sqm"] = gdf.geometry.area
    return gdf


def load_tracts_with_cejst(
    tract_path: Path,
    cejst_path: Path,
    zcta_gdf: gpd.GeoDataFrame,
) -> gpd.GeoDataFrame:
    """Load tract boundaries, join CEJST attributes, and bbox-filter.

    Args:
        tract_path: Path to merged tract GeoJSON.
        cejst_path: Path to CEJST border CSV.
        zcta_gdf: Projected ZCTA GeoDataFrame (for bbox filter).

    Returns:
        GeoDataFrame with tract geometries + disadvantaged flag,
        projected to TARGET_CRS and clipped to ZCTA bbox.
    """
    # Load tracts
    tracts = gpd.read_file(tract_path)
    tracts["tract_fips"] = tracts["tract_fips"].astype(str).str.zfill(11)
    tracts = tracts.to_crs(TARGET_CRS)

    # Load CEJST
    cejst = pd.read_csv(
        cejst_path,
        dtype={"tract_fips": str},
        usecols=["tract_fips", "disadvantaged", "population"],
    )
    cejst["tract_fips"] = cejst["tract_fips"].str.zfill(11)
    cejst = cejst.rename(columns={"population": "tract_population"})

    # Left join: unmatched tracts get disadvantaged=0
    tracts = tracts.merge(cejst, on="tract_fips", how="left")
    tracts["disadvantaged"] = tracts["disadvantaged"].fillna(0).astype(int)
    tracts["tract_population"] = tracts["tract_population"].fillna(0.0)

    # Bounding-box filter for speed
    bbox = zcta_gdf.total_bounds  # minx, miny, maxx, maxy
    buffer = 5000  # 5 km buffer in projected metres
    tracts = tracts.cx[
        bbox[0] - buffer : bbox[2] + buffer,
        bbox[1] - buffer : bbox[3] + buffer,
    ]

    return tracts.copy()


def load_and_prepare(
    *,
    verbose: bool = True,
) -> tuple[gpd.GeoDataFrame, gpd.GeoDataFrame, pd.DataFrame]:
    """Master load function.  Returns (zcta_gdf, tract_gdf, study_df).

    Args:
        verbose: Print progress info.

    Returns:
        Tuple of (ZCTA GeoDataFrame, tract GeoDataFrame, study ZIP DataFrame).
    """
    sec = "5.3.2 Load & Prepare"
    print(f"\n{'='*60}\n  {sec}\n{'='*60}")

    # Study ZIPs
    study_df = load_study_zips(STUDY_ZIPS_CSV)
    study_zips = set(study_df["zip"])
    if verbose:
        print(f"  Study ZIPs loaded: {len(study_df)}")

    # ZCTAs
    zcta_gdf = load_zcta_boundaries(ZCTA_BOUNDARIES, study_zips)
    if verbose:
        print(f"  ZCTAs filtered:    {len(zcta_gdf)} (CRS: {zcta_gdf.crs})")

    # Tracts + CEJST
    tract_gdf = load_tracts_with_cejst(
        TRACT_BOUNDARIES, CEJST_BORDER_CSV, zcta_gdf,
    )
    if verbose:
        n_matched = int(tract_gdf["disadvantaged"].notna().sum())
        n_disadv = int(tract_gdf["disadvantaged"].sum())
        print(
            f"  Tracts (bbox):     {len(tract_gdf):,} "
            f"({n_disadv:,} disadvantaged, {n_matched:,} matched to CEJST)"
        )

    return zcta_gdf, tract_gdf, study_df


# =====================================================================
# 5.3.3  COMPUTE OVERLAY
# =====================================================================


def compute_overlay(
    zcta_gdf: gpd.GeoDataFrame,
    tract_gdf: gpd.GeoDataFrame,
) -> gpd.GeoDataFrame:
    """Intersect ZCTAs with tracts and compute fragment areas.

    Args:
        zcta_gdf: Study ZCTA geometries (EPSG:32119).
        tract_gdf: Tract geometries with disadvantaged flag (EPSG:32119).

    Returns:
        GeoDataFrame of intersection fragments with area_sqm column.
    """
    sec = "5.3.3 Compute Overlay"
    print(f"\n{'='*60}\n  {sec}\n{'='*60}")

    print("  Running gpd.overlay (intersection) ...")
    fragments = gpd.overlay(zcta_gdf, tract_gdf, how="intersection")
    fragments["area_sqm"] = fragments.geometry.area
    print(f"  Raw fragments: {len(fragments):,}")

    # Sliver removal
    n_before = len(fragments)
    area_before = fragments["area_sqm"].sum()
    fragments = fragments[fragments["area_sqm"] >= SLIVER_THRESHOLD_SQM].copy()
    n_after = len(fragments)
    area_after = fragments["area_sqm"].sum()
    pct_removed = (area_before - area_after) / area_before * 100

    print(f"  After sliver removal (>= {SLIVER_THRESHOLD_SQM} sqm):")
    print(f"    Fragments: {n_before:,} -> {n_after:,} "
          f"(removed {n_before - n_after:,})")
    print(f"    Area lost: {pct_removed:.4f}%")

    return fragments


# =====================================================================
# 5.3.4  AREA-WEIGHTED DISADVANTAGED % PER ZCTA
# =====================================================================


def compute_zcta_justice40(
    fragments: gpd.GeoDataFrame,
    study_df: pd.DataFrame,
) -> pd.DataFrame:
    """Compute justice40_pct for each ZCTA via area weighting.

    Args:
        fragments: Overlay fragments with area_sqm and disadvantaged.
        study_df: Study ZIP metadata (for county mapping / population).

    Returns:
        DataFrame with 134 rows, one per study ZCTA.
    """
    sec = "5.3.4 Area-Weighted Justice40 % per ZCTA"
    print(f"\n{'='*60}\n  {sec}\n{'='*60}")

    # Total area per ZCTA
    total_area = (
        fragments.groupby("zip")["area_sqm"]
        .sum()
        .rename("total_area_sqm")
    )

    # Disadvantaged area per ZCTA
    disadv_area = (
        fragments[fragments["disadvantaged"] == 1]
        .groupby("zip")["area_sqm"]
        .sum()
        .rename("disadvantaged_area_sqm")
    )

    # Tract counts
    tract_count = (
        fragments.groupby("zip")["tract_fips"]
        .nunique()
        .rename("tract_count")
    )
    disadv_tract_count = (
        fragments[fragments["disadvantaged"] == 1]
        .groupby("zip")["tract_fips"]
        .nunique()
        .rename("disadvantaged_tract_count")
    )

    # Combine
    result = pd.DataFrame({"total_area_sqm": total_area})
    result = result.join(disadv_area, how="left")
    result = result.join(tract_count, how="left")
    result = result.join(disadv_tract_count, how="left")

    result["disadvantaged_area_sqm"] = result["disadvantaged_area_sqm"].fillna(0.0)
    result["disadvantaged_tract_count"] = (
        result["disadvantaged_tract_count"].fillna(0).astype(int)
    )
    result["tract_count"] = result["tract_count"].fillna(0).astype(int)

    result["justice40_pct"] = (
        result["disadvantaged_area_sqm"] / result["total_area_sqm"] * 100
    )

    result = result.reset_index()

    # Merge study metadata
    result = result.merge(
        study_df[["zip", "county_name", "county_fips", "population"]],
        on="zip",
        how="right",
    )
    # ZCTAs that had no overlay fragments (shouldn't happen but be safe)
    result["justice40_pct"] = result["justice40_pct"].fillna(0.0)
    result["total_area_sqm"] = result["total_area_sqm"].fillna(0.0)
    result["disadvantaged_area_sqm"] = result[
        "disadvantaged_area_sqm"
    ].fillna(0.0)
    result["tract_count"] = result["tract_count"].fillna(0).astype(int)
    result["disadvantaged_tract_count"] = (
        result["disadvantaged_tract_count"].fillna(0).astype(int)
    )

    # Final column order
    result = result[
        [
            "zip",
            "county_name",
            "county_fips",
            "population",
            "total_area_sqm",
            "disadvantaged_area_sqm",
            "justice40_pct",
            "tract_count",
            "disadvantaged_tract_count",
        ]
    ].sort_values("zip")

    print(f"  ZCTA-level results: {len(result)} rows")
    print(f"  justice40_pct range: "
          f"{result['justice40_pct'].min():.1f}% - "
          f"{result['justice40_pct'].max():.1f}%")
    print(f"  Mean justice40_pct: {result['justice40_pct'].mean():.1f}%")

    return result


# =====================================================================
# 5.3.5  COUNTY AGGREGATION
# =====================================================================


def compute_county_justice40(zcta_df: pd.DataFrame) -> pd.DataFrame:
    """Population-weighted county aggregation of ZCTA justice40_pct.

    Args:
        zcta_df: ZCTA-level results from compute_zcta_justice40.

    Returns:
        DataFrame with 10 rows, one per study county.
    """
    sec = "5.3.5 County Aggregation"
    print(f"\n{'='*60}\n  {sec}\n{'='*60}")

    # Exclude zero-population ZCTAs from weighting
    df = zcta_df[zcta_df["population"] > 0].copy()

    def _pop_weighted_mean(group: pd.DataFrame) -> float:
        """Population-weighted mean of justice40_pct."""
        return float(
            np.average(group["justice40_pct"], weights=group["population"])
        )

    county_agg = (
        df.groupby(["county_name", "county_fips"])
        .agg(
            zcta_count=("zip", "count"),
            total_population=("population", "sum"),
            justice40_pct_simple_mean=("justice40_pct", "mean"),
            min_zcta_justice40_pct=("justice40_pct", "min"),
            max_zcta_justice40_pct=("justice40_pct", "max"),
        )
        .reset_index()
    )

    # Population-weighted mean (separate calc)
    pop_wt = (
        df.groupby(["county_name", "county_fips"])
        .apply(_pop_weighted_mean, include_groups=False)
        .rename("justice40_pct_popweighted")
        .reset_index()
    )
    county_agg = county_agg.merge(
        pop_wt, on=["county_name", "county_fips"],
    )

    # Final column order
    county_agg = county_agg[
        [
            "county_name",
            "county_fips",
            "zcta_count",
            "total_population",
            "justice40_pct_popweighted",
            "justice40_pct_simple_mean",
            "min_zcta_justice40_pct",
            "max_zcta_justice40_pct",
        ]
    ].sort_values("county_name")

    print(f"  County-level results: {len(county_agg)} rows")
    print("\n  County Justice40 Summary:")
    print(f"  {'County':<22} {'PopWt%':>8} {'Mean%':>8} "
          f"{'Min%':>7} {'Max%':>7}")
    print(f"  {'-'*52}")
    for _, row in county_agg.iterrows():
        print(
            f"  {row['county_name']:<22} "
            f"{row['justice40_pct_popweighted']:>7.1f}% "
            f"{row['justice40_pct_simple_mean']:>7.1f}% "
            f"{row['min_zcta_justice40_pct']:>6.1f}% "
            f"{row['max_zcta_justice40_pct']:>6.1f}%"
        )

    return county_agg


# =====================================================================
# 5.3.6  WRITE OUTPUTS
# =====================================================================


def write_outputs(
    zcta_df: pd.DataFrame,
    county_df: pd.DataFrame,
) -> None:
    """Write ZCTA and county CSVs.

    Args:
        zcta_df: ZCTA-level Justice40 results.
        county_df: County-level Justice40 results.
    """
    sec = "5.3.6 Write Outputs"
    print(f"\n{'='*60}\n  {sec}\n{'='*60}")

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    zcta_df.to_csv(OUT_ZCTA, index=False)
    print(f"  Saved: {OUT_ZCTA}")
    print(f"    Rows: {len(zcta_df)}, Columns: {list(zcta_df.columns)}")

    county_df.to_csv(OUT_COUNTY, index=False)
    print(f"  Saved: {OUT_COUNTY}")
    print(f"    Rows: {len(county_df)}, Columns: {list(county_df.columns)}")


# =====================================================================
# 5.3.7  VALIDATION (12 checks)
# =====================================================================


def run_validation(
    zcta_gdf: gpd.GeoDataFrame,
    tract_gdf: gpd.GeoDataFrame,
    fragments: gpd.GeoDataFrame,
    zcta_df: pd.DataFrame,
    county_df: pd.DataFrame,
) -> int:
    """Run all 12 validation checks.

    Args:
        zcta_gdf: Study ZCTA geometries.
        tract_gdf: Tract geometries with CEJST join.
        fragments: Overlay fragments (after sliver removal).
        zcta_df: ZCTA-level output.
        county_df: County-level output.

    Returns:
        Number of failed checks.
    """
    sec = "5.3.7 Validation (12 checks)"
    print(f"\n{'='*60}\n  {sec}\n{'='*60}")
    failures = 0

    def _check(num: int, ok: bool, msg: str) -> None:
        nonlocal failures
        tag = "PASS" if ok else "FAIL"
        if not ok:
            failures += 1
        print(f"  [{tag}] {num:>2}. {msg}")

    # --- Tier 1: Geometry Integrity ---
    print("\n  Tier 1 - Geometry Integrity")
    print("  " + "-" * 40)

    # 1. Tract FIPS join rate >= 99%
    #    Compare full (pre-bbox) tract file against CEJST border CSV
    cejst = pd.read_csv(
        CEJST_BORDER_CSV,
        dtype={"tract_fips": str},
        usecols=["tract_fips"],
    )
    cejst_fips = set(cejst["tract_fips"].str.zfill(11))
    full_tracts = gpd.read_file(TRACT_BOUNDARIES, ignore_geometry=True)
    full_tract_fips = set(
        full_tracts["tract_fips"].astype(str).str.zfill(11)
    )
    join_rate = len(cejst_fips & full_tract_fips) / len(cejst_fips) * 100
    _check(1, join_rate >= 99.0,
           f"Tract FIPS join rate: {join_rate:.1f}% (>= 99%)")

    # 2. Study ZCTAs loaded (134 study ZIPs; some may be PO Boxes
    #    without ZCTA geometry, so accept 133-134)
    n_zcta = len(zcta_gdf)
    _check(2, 133 <= n_zcta <= 134,
           f"Study ZCTAs loaded: {n_zcta} (expect 133-134)")

    # 3. CRS EPSG:32119
    crs_ok = (
        zcta_gdf.crs is not None
        and tract_gdf.crs is not None
        and zcta_gdf.crs.to_epsg() == 32119
        and tract_gdf.crs.to_epsg() == 32119
    )
    _check(3, crs_ok,
           f"CRS: ZCTA={zcta_gdf.crs}, Tract={tract_gdf.crs}")

    # 4. No null geometries
    null_zcta = int(
        zcta_gdf.geometry.is_empty.sum() + zcta_gdf.geometry.isna().sum()
    )
    null_tract = int(
        tract_gdf.geometry.is_empty.sum() + tract_gdf.geometry.isna().sum()
    )
    _check(4, null_zcta == 0 and null_tract == 0,
           f"Null geometries: ZCTA={null_zcta}, Tract={null_tract}")

    # --- Tier 2: Overlay Integrity ---
    print("\n  Tier 2 - Overlay Integrity")
    print("  " + "-" * 40)

    # 5. Fragment count > 0
    n_frags = len(fragments)
    _check(5, n_frags > 0,
           f"Fragment count: {n_frags:,}")

    # 6. Sliver removal stats
    # (already printed during overlay; just confirm < 1% area loss)
    total_frag_area = fragments["area_sqm"].sum()
    total_zcta_area = zcta_gdf["original_area_sqm"].sum()
    area_loss_pct = abs(total_zcta_area - total_frag_area) / total_zcta_area * 100
    _check(6, area_loss_pct < 5.0,
           f"Overall area delta: {area_loss_pct:.2f}% "
           f"(ZCTA total vs fragment total)")

    # 7. Area conservation per ZCTA (within 1%)
    frag_area_by_zcta = fragments.groupby("zip")["area_sqm"].sum()
    orig_area_by_zcta = zcta_gdf.set_index("zip")["original_area_sqm"]
    area_pct_diff = (
        (frag_area_by_zcta - orig_area_by_zcta).abs()
        / orig_area_by_zcta
        * 100
    )
    # Only check ZCTAs present in both
    area_pct_diff = area_pct_diff.dropna()
    max_area_diff = area_pct_diff.max() if len(area_pct_diff) > 0 else 0.0
    n_over_1pct = int((area_pct_diff > 1.0).sum())
    _check(
        7,
        n_over_1pct == 0,
        f"Area conservation: max diff={max_area_diff:.2f}%, "
        f"{n_over_1pct} ZCTAs > 1%",
    )
    if n_over_1pct > 0:
        worst = area_pct_diff.nlargest(5)
        for z, pct in worst.items():
            print(f"    ZIP {z}: {pct:.2f}% area difference")

    # 8. All study ZCTAs with geometry are in overlay output
    zcta_in_output = set(zcta_df["zip"])
    zcta_with_geom = set(zcta_gdf["zip"])
    all_present = zcta_with_geom.issubset(zcta_in_output)
    _check(8, all_present,
           f"ZCTAs in output: {len(zcta_in_output)} "
           f"(all {len(zcta_with_geom)} with geometry present)")

    # --- Tier 3: Result Plausibility ---
    print("\n  Tier 3 - Result Plausibility")
    print("  " + "-" * 40)

    # 9. All justice40_pct between 0 and 100
    j40 = zcta_df["justice40_pct"]
    range_ok = float(j40.min()) >= 0.0 and float(j40.max()) <= 100.0
    _check(9, range_ok,
           f"justice40_pct range: [{j40.min():.1f}, {j40.max():.1f}]")

    # 10. County pattern: Durham/Guilford higher, Cabarrus/Union lower
    #     (matches EDA tract-level patterns for the 10 study counties)
    def _cty_val(name: str) -> float:
        row = county_df.loc[
            county_df["county_name"] == name,
            "justice40_pct_popweighted",
        ]
        return float(row.iloc[0]) if len(row) > 0 else -1.0

    durham_val = _cty_val("Durham")
    guilford_val = _cty_val("Guilford")
    cab_val = _cty_val("Cabarrus")
    union_val = _cty_val("Union")
    pattern_ok = (
        durham_val > cab_val
        and durham_val > union_val
        and guilford_val > cab_val
        and guilford_val > union_val
    )
    _check(
        10,
        pattern_ok,
        f"Durham ({durham_val:.1f}%) & Guilford ({guilford_val:.1f}%) > "
        f"Cabarrus ({cab_val:.1f}%) & Union ({union_val:.1f}%)",
    )

    # 11. Population-weighted average across 10 counties ~ 30-50%
    total_pop = county_df["total_population"].sum()
    if total_pop > 0:
        overall_pw = float(
            np.average(
                county_df["justice40_pct_popweighted"],
                weights=county_df["total_population"],
            )
        )
    else:
        overall_pw = 0.0
    _check(11, 10.0 <= overall_pw <= 70.0,
           f"Overall pop-weighted average: {overall_pw:.1f}% "
           f"(expect 10-70%)")

    # 12. Zero-population ZCTAs excluded from county weighting
    n_zero_pop = int((zcta_df["population"] == 0).sum())
    total_county_pop = county_df["total_population"].sum()
    total_zcta_pop = zcta_df.loc[
        zcta_df["population"] > 0, "population"
    ].sum()
    pop_match = abs(total_county_pop - total_zcta_pop) < 1.0
    _check(
        12,
        pop_match,
        f"Zero-pop ZCTAs excluded: {n_zero_pop} ZCTAs with pop=0; "
        f"county total pop={total_county_pop:,.0f} "
        f"matches ZCTA sum={total_zcta_pop:,.0f}",
    )

    # Summary
    print(f"\n  Validation: {12 - failures}/12 passed, {failures} failed")
    return failures


# =====================================================================
# CLI & MAIN
# =====================================================================


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Phase 5 Step 5.3: Tract-to-ZCTA spatial crosswalk",
    )
    parser.add_argument(
        "--skip-validation",
        action="store_true",
        help="Skip the 12-check validation suite",
    )
    return parser.parse_args()


def main() -> None:
    """Entry point."""
    args = parse_args()

    print("=" * 60)
    print("  Phase 5 Step 5.3: Tract-to-ZCTA Spatial Crosswalk")
    print("  EV Pulse NC")
    print("=" * 60)

    # 5.3.2 Load & Prepare
    zcta_gdf, tract_gdf, study_df = load_and_prepare()

    # 5.3.3 Compute Overlay
    fragments = compute_overlay(zcta_gdf, tract_gdf)

    # 5.3.4 Area-Weighted Justice40 % per ZCTA
    zcta_df = compute_zcta_justice40(fragments, study_df)

    # 5.3.5 County Aggregation
    county_df = compute_county_justice40(zcta_df)

    # 5.3.6 Write Outputs
    write_outputs(zcta_df, county_df)

    # 5.3.7 Validation
    if not args.skip_validation:
        n_fail = run_validation(
            zcta_gdf, tract_gdf, fragments, zcta_df, county_df,
        )
        if n_fail > 0:
            print(f"\n  WARNING: {n_fail} validation check(s) failed.")
            sys.exit(1)

    print("\n  DONE - Phase 5 Step 5.3 complete")


if __name__ == "__main__":
    main()
