#!/usr/bin/env python3
"""
Phase 4, Step 2: Workplace Charging Demand Analysis.

Three-layer adjustment pipeline:
    Raw LODES commuter count (SE03: workers earning >$40K)
    -> ACS income correction (estimate >$75K household share)
    -> Remote work reduction (0.85 multiplier)
    = Adjusted workplace charging demand

Outputs:
    data/processed/phase4-employment-centers.csv
    data/processed/phase4-cost-effectiveness.csv

Usage:
    uv run code/python/analysis/phase4_workplace_charging.py

Author: BIDA 670 EV-Pulse-NC Project
Date: 2026
"""

from __future__ import annotations

from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd

# -------------------------------------------------------------------
# Project paths
# -------------------------------------------------------------------
_SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = _SCRIPT_DIR.parent.parent.parent
RAW = PROJECT_ROOT / "data" / "raw"
PROCESSED = PROJECT_ROOT / "data" / "processed"

OD_PATH = RAW / "lehd-nc-od-main-2021.csv.gz"
WAC_PATH = RAW / "lehd-nc-wac-2021.csv.gz"
XW_PATH = RAW / "lehd-nc-xwalk.csv.gz"
ACS_PATH = RAW / "acs-nc-income-tenure-tracts.csv"
COUNTY_GEO_PATH = RAW / "nc-county-boundaries.geojson"
SKELETON_CSV = PROCESSED / "scoring-framework-skeleton.csv"

# Remote work multiplier (15% reduction)
REMOTE_WORK_FACTOR = 0.85

# Workplace port estimation parameters
CHARGING_RATE_SCENARIOS = {
    "low": {"charging_rate": 0.20, "evs_per_port": 20},
    "baseline": {"charging_rate": 0.30, "evs_per_port": 15},
    "high": {"charging_rate": 0.40, "evs_per_port": 10},
}
L2_PORT_SHARE = 0.80
DCFC_PORT_SHARE = 0.20

# Top-10 BEV counties for scoring output
SCORING_COUNTIES = [
    "Wake",
    "Mecklenburg",
    "Durham",
    "Guilford",
    "Union",
    "Buncombe",
    "Cabarrus",
    "Orange",
    "Forsyth",
    "New Hanover",
]

# County typology thresholds
EMPLOYMENT_CENTER_THRESHOLD = 10_000
BEDROOM_COMMUNITY_THRESHOLD = -10_000

# Square meters to square miles conversion
SQ_METERS_TO_SQ_MILES = 1 / 2_589_988.11


# ===================================================================
# SUB-STEP 1: Load All Data
# ===================================================================
def load_data() -> (
    tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, gpd.GeoDataFrame]
):
    """Load all input datasets with string dtypes for FIPS codes."""
    print("=" * 70)
    print("  SUB-STEP 1: Load All Data")
    print("=" * 70)

    od = pd.read_csv(
        OD_PATH,
        dtype={"w_geocode": str, "h_geocode": str},
        usecols=["w_geocode", "h_geocode", "S000", "SE01", "SE02", "SE03"],
    )
    print(f"  OD loaded: {len(od):,} rows")

    wac = pd.read_csv(
        WAC_PATH,
        dtype={"w_geocode": str},
        usecols=["w_geocode", "C000", "CE01", "CE02", "CE03"],
    )
    print(f"  WAC loaded: {len(wac):,} rows")

    xw = pd.read_csv(
        XW_PATH,
        dtype={"tabblk2020": str, "st": str, "cty": str, "trct": str},
        usecols=["tabblk2020", "st", "cty", "ctyname", "trct"],
    )
    print(f"  Crosswalk loaded: {len(xw):,} rows")

    acs = pd.read_csv(
        ACS_PATH,
        dtype={"state": str, "county": str, "tract": str},
    )
    # Drop Census API header row if present
    first_val = acs["B19001_001E"].iloc[0]
    try:
        float(first_val)
    except (ValueError, TypeError):
        acs = acs.iloc[1:].reset_index(drop=True)
        print("  ACS: dropped Census API header row")
    # Cast numeric columns
    for c in acs.columns:
        if c not in ("NAME", "state", "county", "tract"):
            acs[c] = pd.to_numeric(acs[c], errors="coerce")
    acs = acs[acs["state"] == "37"].copy().reset_index(drop=True)
    print(f"  ACS loaded: {len(acs):,} NC tracts")

    county_geo = gpd.read_file(COUNTY_GEO_PATH)
    print(f"  County boundaries loaded: {len(county_geo):,} polygons")

    return od, wac, xw, acs, county_geo


# ===================================================================
# SUB-STEP 2: Build Crosswalk Lookups
# ===================================================================
def build_crosswalk(xw: pd.DataFrame) -> pd.DataFrame:
    """Build block-to-county and block-to-tract lookups."""
    print("\n" + "=" * 70)
    print("  SUB-STEP 2: Build Crosswalk Lookups")
    print("=" * 70)

    n_blocks = xw["tabblk2020"].nunique()
    n_counties = xw["cty"].nunique()
    n_tracts = xw["trct"].nunique()
    print(f"  Blocks: {n_blocks:,}  Counties: {n_counties}  Tracts: {n_tracts:,}")

    assert n_counties == 100, f"Expected 100 counties, got {n_counties}"
    return xw


# ===================================================================
# SUB-STEP 3: Harmonize ACS Tract FIPS
# ===================================================================
def harmonize_acs_tracts(
    acs: pd.DataFrame, xw: pd.DataFrame
) -> pd.DataFrame:
    """Construct 11-digit FIPS and verify alignment with crosswalk."""
    print("\n" + "=" * 70)
    print("  SUB-STEP 3: Harmonize ACS Tract FIPS")
    print("=" * 70)

    acs["tract_fips"] = acs["state"] + acs["county"] + acs["tract"]
    n_acs = acs["tract_fips"].nunique()

    xw_tracts = set(xw["trct"].unique())
    acs_tracts = set(acs["tract_fips"].unique())
    overlap = xw_tracts & acs_tracts
    xw_only = xw_tracts - acs_tracts
    acs_only = acs_tracts - xw_tracts

    print(f"  ACS tracts: {n_acs:,}")
    print(f"  Crosswalk tracts: {len(xw_tracts):,}")
    print(f"  Overlap: {len(overlap):,}")
    print(f"  XW-only: {len(xw_only):,}  ACS-only: {len(acs_only):,}")

    overlap_pct = len(overlap) / max(len(xw_tracts), len(acs_tracts)) * 100
    print(f"  Overlap rate: {overlap_pct:.1f}%")

    return acs


# ===================================================================
# SUB-STEP 4: Compute ACS Tract-Level Indicators
# ===================================================================
def compute_acs_indicators(acs: pd.DataFrame) -> pd.DataFrame:
    """Compute high-income shares and renter share per tract."""
    print("\n" + "=" * 70)
    print("  SUB-STEP 4: Compute ACS Tract-Level Indicators")
    print("=" * 70)

    # $75K+ baseline: bins 013-017
    high_inc_75k = (
        acs["B19001_013E"]
        + acs["B19001_014E"]
        + acs["B19001_015E"]
        + acs["B19001_016E"]
        + acs["B19001_017E"]
    )
    acs["high_income_share_75k"] = np.where(
        acs["B19001_001E"] > 0,
        high_inc_75k / acs["B19001_001E"],
        0.0,
    )

    # $100K+ sensitivity: bins 014-017
    high_inc_100k = (
        acs["B19001_014E"]
        + acs["B19001_015E"]
        + acs["B19001_016E"]
        + acs["B19001_017E"]
    )
    acs["high_income_share_100k"] = np.where(
        acs["B19001_001E"] > 0,
        high_inc_100k / acs["B19001_001E"],
        0.0,
    )

    # Renter share (descriptive only)
    acs["renter_share"] = np.where(
        acs["B25003_001E"] > 0,
        acs["B25003_003E"] / acs["B25003_001E"],
        0.0,
    )

    # Note about $60K threshold
    print("  NOTE: B19001_012E not available; $60K threshold skipped.")
    print(
        f"  $75K+ share: mean={acs['high_income_share_75k'].mean():.3f}, "
        f"median={acs['high_income_share_75k'].median():.3f}"
    )
    print(
        f"  $100K+ share: mean={acs['high_income_share_100k'].mean():.3f}, "
        f"median={acs['high_income_share_100k'].median():.3f}"
    )
    print(
        f"  Renter share: mean={acs['renter_share'].mean():.3f}, "
        f"median={acs['renter_share'].median():.3f}"
    )

    return acs


# ===================================================================
# SUB-STEP 5: Map OD Flows to Counties and Origin Tracts
# ===================================================================
def map_od_flows(
    od: pd.DataFrame, xw: pd.DataFrame
) -> pd.DataFrame:
    """Join OD flows to destination county and origin tract."""
    print("\n" + "=" * 70)
    print("  SUB-STEP 5: Map OD Flows to Counties and Origin Tracts")
    print("=" * 70)

    n_before = len(od)

    # Destination: w_geocode -> county
    dest_lookup = xw[["tabblk2020", "cty", "ctyname"]].rename(
        columns={
            "tabblk2020": "w_geocode",
            "cty": "dest_county_fips",
            "ctyname": "dest_county_name",
        }
    )
    od = od.merge(dest_lookup, on="w_geocode", how="left")

    # Origin: h_geocode -> county + tract
    orig_lookup = xw[["tabblk2020", "cty", "ctyname", "trct"]].rename(
        columns={
            "tabblk2020": "h_geocode",
            "cty": "orig_county_fips",
            "ctyname": "orig_county_name",
            "trct": "orig_tract",
        }
    )
    od = od.merge(orig_lookup, on="h_geocode", how="left")

    n_after = len(od)
    n_dest_null = od["dest_county_fips"].isna().sum()
    n_orig_null = od["orig_county_fips"].isna().sum()

    print(f"  Rows before join: {n_before:,}")
    print(f"  Rows after join:  {n_after:,}")
    print(f"  Dest county null: {n_dest_null:,}")
    print(f"  Orig county null: {n_orig_null:,}")

    # Drop rows where crosswalk lookup failed (should be very few)
    if n_dest_null > 0 or n_orig_null > 0:
        s000_lost = od[
            od["dest_county_fips"].isna() | od["orig_county_fips"].isna()
        ]["S000"].sum()
        s000_total = od["S000"].sum()
        pct_lost = s000_lost / s000_total * 100
        print(
            f"  WARNING: dropping {n_dest_null + n_orig_null:,} "
            f"unmatched rows ({pct_lost:.2f}% of S000)"
        )
        od = od.dropna(
            subset=["dest_county_fips", "orig_county_fips"]
        ).copy()

    # Verify Main type (all h_geocode start with 37)
    all_nc = od["h_geocode"].str[:2].eq("37").all()
    print(f"  All h_geocode NC (Main type): {all_nc}")

    return od


# ===================================================================
# SUB-STEP 6: Layer 1 — SE03 Filter
# ===================================================================
def layer1_se03_filter(od: pd.DataFrame) -> pd.DataFrame:
    """Use SE03 as base commuter count (workers earning >$40K)."""
    print("\n" + "=" * 70)
    print("  SUB-STEP 6: Layer 1 -- SE03 Filter")
    print("=" * 70)

    total_s000 = od["S000"].sum()
    total_se03 = od["SE03"].sum()
    ratio = total_se03 / total_s000

    print(f"  Total S000: {total_s000:,}")
    print(f"  Total SE03: {total_se03:,}")
    print(f"  SE03/S000 ratio: {ratio:.4f} ({ratio * 100:.1f}%)")

    od["flow_se03"] = od["SE03"].astype(float)
    return od


# ===================================================================
# SUB-STEP 7: Layer 2 — ACS Income Correction
# ===================================================================
def layer2_income_correction(
    od: pd.DataFrame, acs: pd.DataFrame
) -> pd.DataFrame:
    """Apply ACS high-income share to SE03 flows."""
    print("\n" + "=" * 70)
    print("  SUB-STEP 7: Layer 2 -- ACS Income Correction")
    print("=" * 70)

    acs_lookup = acs[
        ["tract_fips", "high_income_share_75k", "high_income_share_100k"]
    ].copy()
    acs_lookup = acs_lookup.rename(
        columns={"tract_fips": "orig_tract"}
    )

    n_before = len(od)
    od = od.merge(acs_lookup, on="orig_tract", how="left")
    assert len(od) == n_before, "Merge changed row count"

    # Fill missing income shares with statewide median
    median_75k = acs["high_income_share_75k"].median()
    median_100k = acs["high_income_share_100k"].median()
    n_missing = od["high_income_share_75k"].isna().sum()
    if n_missing > 0:
        print(
            f"  Filling {n_missing:,} missing income shares "
            f"with median ({median_75k:.3f})"
        )
    od["high_income_share_75k"] = od["high_income_share_75k"].fillna(
        median_75k
    )
    od["high_income_share_100k"] = od["high_income_share_100k"].fillna(
        median_100k
    )

    od["flow_income_adj_75k"] = od["flow_se03"] * od["high_income_share_75k"]
    od["flow_income_adj_100k"] = (
        od["flow_se03"] * od["high_income_share_100k"]
    )

    total_se03 = od["flow_se03"].sum()
    total_adj_75k = od["flow_income_adj_75k"].sum()
    total_adj_100k = od["flow_income_adj_100k"].sum()

    print(f"  Total SE03:          {total_se03:,.0f}")
    print(f"  Total income-adj 75k: {total_adj_75k:,.0f}")
    print(f"  Total income-adj 100k:{total_adj_100k:,.0f}")
    print(f"  75k/SE03 ratio:      {total_adj_75k / total_se03:.4f}")
    print(f"  100k/SE03 ratio:     {total_adj_100k / total_se03:.4f}")

    return od


# ===================================================================
# SUB-STEP 8: Layer 3 — Remote Work Reduction
# ===================================================================
def layer3_remote_work(od: pd.DataFrame) -> pd.DataFrame:
    """Apply 0.85 remote work multiplier."""
    print("\n" + "=" * 70)
    print("  SUB-STEP 8: Layer 3 -- Remote Work Reduction")
    print("=" * 70)

    od["flow_final_75k"] = od["flow_income_adj_75k"] * REMOTE_WORK_FACTOR
    od["flow_final_100k"] = od["flow_income_adj_100k"] * REMOTE_WORK_FACTOR

    total_adj = od["flow_income_adj_75k"].sum()
    total_final = od["flow_final_75k"].sum()

    print(f"  Remote work factor: {REMOTE_WORK_FACTOR}")
    print(f"  Before: {total_adj:,.0f}")
    print(f"  After:  {total_final:,.0f}")
    print(f"  Check:  {total_adj * REMOTE_WORK_FACTOR:,.0f} (should match)")

    return od


# ===================================================================
# SUB-STEP 9: Aggregate to County Level
# ===================================================================
def aggregate_counties(
    od: pd.DataFrame, acs: pd.DataFrame
) -> pd.DataFrame:
    """Aggregate flows to destination county level."""
    print("\n" + "=" * 70)
    print("  SUB-STEP 9: Aggregate to County Level")
    print("=" * 70)

    # Inbound aggregation (by destination county)
    inbound = (
        od.groupby(["dest_county_fips", "dest_county_name"])
        .agg(
            gross_inbound_s000=("S000", "sum"),
            inbound_se03=("flow_se03", "sum"),
            adjusted_demand_75k=("flow_final_75k", "sum"),
            adjusted_demand_100k=("flow_final_100k", "sum"),
        )
        .reset_index()
        .rename(
            columns={
                "dest_county_fips": "county_fips",
                "dest_county_name": "county_name",
            }
        )
    )

    # Outbound aggregation (by origin county)
    outbound = (
        od.groupby("orig_county_fips")["S000"]
        .sum()
        .reset_index()
        .rename(
            columns={
                "orig_county_fips": "county_fips",
                "S000": "gross_outbound_s000",
            }
        )
    )

    # Merge inbound + outbound
    county = inbound.merge(outbound, on="county_fips", how="left")
    county["gross_outbound_s000"] = county["gross_outbound_s000"].fillna(0)
    county["net_commuting"] = (
        county["gross_inbound_s000"] - county["gross_outbound_s000"]
    )

    # Normalize county names: "Wake County, NC" -> "Wake"
    county["county_name_full"] = county["county_name"]
    county["county_name"] = (
        county["county_name"]
        .str.replace(r"\s+County,\s*NC$", "", regex=True)
    )

    # Renter-origin descriptive stats for top-15
    # For each dest county, find what % of commuter origins come from
    # renter-heavy tracts (renter_share > 0.50)
    acs_renter = acs[["tract_fips", "renter_share"]].rename(
        columns={"tract_fips": "orig_tract"}
    )
    od_with_renter = od.merge(acs_renter, on="orig_tract", how="left")
    od_with_renter["renter_share_y"] = od_with_renter[
        "renter_share"
    ].fillna(0)
    od_with_renter["from_renter_heavy"] = (
        od_with_renter["renter_share_y"] > 0.50
    )
    od_with_renter["s000_renter_heavy"] = (
        od_with_renter["S000"] * od_with_renter["from_renter_heavy"]
    )

    renter_agg = (
        od_with_renter.groupby("dest_county_fips")
        .agg(
            total_s000_for_renter=("S000", "sum"),
            s000_from_renter_heavy=("s000_renter_heavy", "sum"),
        )
        .reset_index()
        .rename(columns={"dest_county_fips": "county_fips"})
    )
    renter_agg["pct_from_renter_heavy_tracts"] = (
        renter_agg["s000_from_renter_heavy"]
        / renter_agg["total_s000_for_renter"]
        * 100
    )

    county = county.merge(
        renter_agg[["county_fips", "pct_from_renter_heavy_tracts"]],
        on="county_fips",
        how="left",
    )

    # Sort and identify top 15
    county = county.sort_values(
        "adjusted_demand_75k", ascending=False
    ).reset_index(drop=True)

    top15 = county.head(15).copy()

    print(f"  Total counties: {len(county):,}")
    print("\n  Top 15 Employment Centers by Adjusted Demand (75k):")
    print(f"  {'County':<22} {'Inbound':>10} {'Outbound':>10} "
          f"{'Net':>10} {'Adj Demand':>12}")
    print("  " + "-" * 66)
    for _, row in top15.iterrows():
        print(
            f"  {row['county_name']:<22} "
            f"{row['gross_inbound_s000']:>10,.0f} "
            f"{row['gross_outbound_s000']:>10,.0f} "
            f"{row['net_commuting']:>10,.0f} "
            f"{row['adjusted_demand_75k']:>12,.0f}"
        )

    return county


# ===================================================================
# SUB-STEP 10: County Typology
# ===================================================================
def assign_typology(county: pd.DataFrame) -> pd.DataFrame:
    """Classify counties by net commuting pattern."""
    print("\n" + "=" * 70)
    print("  SUB-STEP 10: County Typology")
    print("=" * 70)

    conditions = [
        county["net_commuting"] > EMPLOYMENT_CENTER_THRESHOLD,
        county["net_commuting"] < BEDROOM_COMMUNITY_THRESHOLD,
    ]
    choices = ["Employment Center", "Bedroom Community"]
    county["typology"] = np.select(conditions, choices, default="Balanced")

    typology_counts = county["typology"].value_counts()
    for typ, cnt in typology_counts.items():
        print(f"  {typ}: {cnt}")

    return county


# ===================================================================
# SUB-STEP 11: Workplace Port Estimates
# ===================================================================
def estimate_ports(county: pd.DataFrame) -> pd.DataFrame:
    """Compute workplace charging port estimates for three scenarios."""
    print("\n" + "=" * 70)
    print("  SUB-STEP 11: Workplace Port Estimates")
    print("=" * 70)

    for scenario, params in CHARGING_RATE_SCENARIOS.items():
        cr = params["charging_rate"]
        epp = params["evs_per_port"]
        col_total = f"ports_total_{scenario}"
        col_l2 = f"ports_l2_{scenario}"
        col_dcfc = f"ports_dcfc_{scenario}"

        county[col_total] = (
            county["adjusted_demand_75k"] * cr / epp
        )
        county[col_l2] = county[col_total] * L2_PORT_SHARE
        county[col_dcfc] = county[col_total] * DCFC_PORT_SHARE

    # Print baseline for top 15
    top15 = county.head(15)
    print("\n  Baseline Port Estimates (top 15):")
    print(
        f"  {'County':<22} {'Total':>8} {'L2':>8} {'DCFC':>8}"
    )
    print("  " + "-" * 48)
    for _, row in top15.iterrows():
        print(
            f"  {row['county_name']:<22} "
            f"{row['ports_total_baseline']:>8,.0f} "
            f"{row['ports_l2_baseline']:>8,.0f} "
            f"{row['ports_dcfc_baseline']:>8,.0f}"
        )

    return county


# ===================================================================
# SUB-STEP 12: Scoring Columns
# ===================================================================
def compute_scoring_columns(
    county: pd.DataFrame,
    county_geo: gpd.GeoDataFrame,
    wac: pd.DataFrame,
    xw: pd.DataFrame,
) -> pd.DataFrame:
    """Compute cost-effectiveness sub-metrics for scoring counties."""
    print("\n" + "=" * 70)
    print("  SUB-STEP 12: Scoring Columns")
    print("=" * 70)

    # cost_commuter_demand: adjusted_demand_75k (raw, unnormalized)
    county["cost_commuter_demand"] = county["adjusted_demand_75k"]

    # cost_workplace_efficiency: adjusted_demand_75k / existing ports
    # Load skeleton for util_total_ports
    skeleton = pd.read_csv(SKELETON_CSV)
    port_map = dict(
        zip(skeleton["county_name"], skeleton["util_total_ports"], strict=False)
    )
    county["existing_ports"] = county["county_name"].map(port_map)
    county["cost_workplace_efficiency"] = np.where(
        county["existing_ports"].notna() & (county["existing_ports"] > 0),
        county["cost_commuter_demand"] / county["existing_ports"],
        np.nan,
    )

    # cost_pop_density: population / land area (sq miles)
    # Use WAC C000 as population proxy (total employment at workplace)
    # But we need residential population -- use county land area from
    # GeoJSON ALAND field and WAC total workers as a proxy
    wac_with_county = wac.merge(
        xw[["tabblk2020", "cty", "ctyname"]].rename(
            columns={"tabblk2020": "w_geocode"}
        ),
        on="w_geocode",
        how="left",
    )
    county_pop_proxy = (
        wac_with_county.groupby("cty")["C000"]
        .sum()
        .reset_index()
        .rename(columns={"cty": "county_fips", "C000": "worker_population"})
    )

    # County land area from GeoJSON (ALAND in sq meters)
    geo_area = county_geo[["GEOID", "NAME", "ALAND"]].copy()
    geo_area = geo_area.rename(
        columns={"GEOID": "county_fips", "ALAND": "land_area_sqm"}
    )
    geo_area["land_area_sqmi"] = (
        geo_area["land_area_sqm"] * SQ_METERS_TO_SQ_MILES
    )

    county = county.merge(
        county_pop_proxy, on="county_fips", how="left"
    )
    county = county.merge(
        geo_area[["county_fips", "land_area_sqmi"]],
        on="county_fips",
        how="left",
    )
    county["cost_pop_density"] = np.where(
        county["land_area_sqmi"].notna() & (county["land_area_sqmi"] > 0),
        county["worker_population"] / county["land_area_sqmi"],
        np.nan,
    )

    # Print scoring columns for the 10 target counties
    scoring = county[county["county_name"].isin(SCORING_COUNTIES)].copy()
    scoring = scoring.sort_values(
        "cost_commuter_demand", ascending=False
    )

    print("\n  Scoring Columns for Top-10 BEV Counties:")
    print(
        f"  {'County':<16} {'Commuter Demand':>16} "
        f"{'Workplace Eff':>14} {'Pop Density':>12}"
    )
    print("  " + "-" * 60)
    for _, row in scoring.iterrows():
        eff = (
            f"{row['cost_workplace_efficiency']:.2f}"
            if pd.notna(row["cost_workplace_efficiency"])
            else "N/A"
        )
        den = (
            f"{row['cost_pop_density']:.1f}"
            if pd.notna(row["cost_pop_density"])
            else "N/A"
        )
        print(
            f"  {row['county_name']:<16} "
            f"{row['cost_commuter_demand']:>16,.0f} "
            f"{eff:>14} "
            f"{den:>12}"
        )

    return county


# ===================================================================
# SUB-STEP 13: Export CSVs
# ===================================================================
def export_results(county: pd.DataFrame) -> None:
    """Save output CSVs to data/processed/."""
    print("\n" + "=" * 70)
    print("  SUB-STEP 13: Export CSVs")
    print("=" * 70)

    PROCESSED.mkdir(parents=True, exist_ok=True)

    # --- phase4-employment-centers.csv (Top 15) ---
    top15 = county.head(15).copy()
    emp_cols = [
        "county_fips",
        "county_name",
        "gross_inbound_s000",
        "gross_outbound_s000",
        "net_commuting",
        "inbound_se03",
        "adjusted_demand_75k",
        "adjusted_demand_100k",
        "typology",
        "ports_total_baseline",
        "ports_l2_baseline",
        "ports_dcfc_baseline",
        "ports_total_low",
        "ports_l2_low",
        "ports_dcfc_low",
        "ports_total_high",
        "ports_l2_high",
        "ports_dcfc_high",
        "pct_from_renter_heavy_tracts",
    ]
    emp_out = top15[emp_cols]
    emp_path = PROCESSED / "phase4-employment-centers.csv"
    emp_out.to_csv(emp_path, index=False)
    print(f"  Saved: {emp_path}")
    print(f"  Shape: {emp_out.shape}")

    # --- phase4-cost-effectiveness.csv (10 scoring counties) ---
    scoring = county[county["county_name"].isin(SCORING_COUNTIES)].copy()
    scoring = scoring.sort_values(
        "cost_commuter_demand", ascending=False
    )
    cost_cols = [
        "county_fips",
        "county_name",
        "cost_commuter_demand",
        "cost_workplace_efficiency",
        "cost_pop_density",
    ]
    cost_out = scoring[cost_cols]
    cost_path = PROCESSED / "phase4-cost-effectiveness.csv"
    cost_out.to_csv(cost_path, index=False)
    print(f"  Saved: {cost_path}")
    print(f"  Shape: {cost_out.shape}")


# ===================================================================
# DIAGNOSTIC SUMMARY
# ===================================================================
def print_diagnostic_summary(od: pd.DataFrame, county: pd.DataFrame) -> None:
    """Print pipeline flow diagnostics."""
    print("\n" + "=" * 70)
    print("  DIAGNOSTIC CHECKPOINT SUMMARY")
    print("=" * 70)

    total_s000 = od["S000"].sum()
    total_se03 = od["flow_se03"].sum()
    total_inc_75k = od["flow_income_adj_75k"].sum()
    total_final_75k = od["flow_final_75k"].sum()

    print(f"  Stage 0 (Raw S000):       {total_s000:>14,.0f}")
    print(f"  Stage 1 (SE03 filter):    {total_se03:>14,.0f}  "
          f"({total_se03 / total_s000 * 100:.1f}% of S000)")
    print(f"  Stage 2 (Income adj 75k): {total_inc_75k:>14,.0f}  "
          f"({total_inc_75k / total_se03 * 100:.1f}% of SE03)")
    print(f"  Stage 3 (Remote work):    {total_final_75k:>14,.0f}  "
          f"({total_final_75k / total_inc_75k * 100:.1f}% of Stage 2)")

    print(f"\n  Statewide adjusted demand (75k): {total_final_75k:,.0f}")

    # Total baseline ports statewide
    total_ports = county["ports_total_baseline"].sum()
    total_l2 = county["ports_l2_baseline"].sum()
    total_dcfc = county["ports_dcfc_baseline"].sum()
    print("\n  Statewide baseline port estimates:")
    print(f"    Total ports: {total_ports:,.0f}")
    print(f"    L2 ports:    {total_l2:,.0f}")
    print(f"    DCFC ports:  {total_dcfc:,.0f}")


# ===================================================================
# MAIN
# ===================================================================
def main() -> None:
    """Execute the full Phase 4 workplace charging analysis."""
    print("=" * 70)
    print("  PHASE 4 STEP 2: Workplace Charging Demand Analysis")
    print("=" * 70)
    print("  Pipeline: SE03 -> ACS Income Correction -> Remote Work")
    print()

    # Sub-step 1: Load
    od, wac, xw, acs, county_geo = load_data()

    # Sub-step 2: Crosswalk
    xw = build_crosswalk(xw)

    # Sub-step 3: Harmonize ACS
    acs = harmonize_acs_tracts(acs, xw)

    # Sub-step 4: ACS indicators
    acs = compute_acs_indicators(acs)

    # Sub-step 5: Map OD flows
    od = map_od_flows(od, xw)

    # Sub-step 6: Layer 1
    od = layer1_se03_filter(od)

    # Sub-step 7: Layer 2
    od = layer2_income_correction(od, acs)

    # Sub-step 8: Layer 3
    od = layer3_remote_work(od)

    # Sub-step 9: Aggregate
    county = aggregate_counties(od, acs)

    # Sub-step 10: Typology
    county = assign_typology(county)

    # Sub-step 11: Port estimates
    county = estimate_ports(county)

    # Sub-step 12: Scoring columns
    county = compute_scoring_columns(county, county_geo, wac, xw)

    # Sub-step 13: Export
    export_results(county)

    # Diagnostic summary
    print_diagnostic_summary(od, county)

    print("\n" + "=" * 70)
    print("  PHASE 4 STEP 2 COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
