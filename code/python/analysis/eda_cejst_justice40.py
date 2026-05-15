#!/usr/bin/env python3
"""
Phase 5 EDA: CEJST Justice40 Disadvantaged-Tract Data

Console-output-only sanity checks for the CEJST Justice40 tract-level
data used in the equity-overlay analysis.  No figures produced.

Files checked:
    1. cejst-justice40-tracts-nc.csv         (NC tracts, 2,195 rows)
    2. cejst-justice40-tracts-nc-border.csv   (NC + border tracts, 8,671 rows)
    3. lehd-nc-xwalk.csv.gz                  (LEHD crosswalk for tract matching)

Author: Wolfgang Sanyer
License: Polyform Noncommercial 1.0.0 (see LICENSE)
Date: 2026
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

# ---------------------------------------------------------------------------
# Project paths
# ---------------------------------------------------------------------------
_SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = _SCRIPT_DIR.parent.parent.parent
RAW = PROJECT_ROOT / "data" / "raw"

NC_PATH = RAW / "cejst-justice40-tracts-nc.csv"
BORDER_PATH = RAW / "cejst-justice40-tracts-nc-border.csv"
XW_PATH = RAW / "lehd-nc-xwalk.csv.gz"

# 10 study counties used throughout the project
STUDY_COUNTIES = [
    "Wake County",
    "Mecklenburg County",
    "Guilford County",
    "Durham County",
    "Forsyth County",
    "Buncombe County",
    "Cumberland County",
    "New Hanover County",
    "Cabarrus County",
    "Union County",
]

# ---------------------------------------------------------------------------
# Tracking helpers
# ---------------------------------------------------------------------------
_results: dict[str, list[tuple[str, str]]] = {}


def _record(section: str, tag: str, msg: str) -> None:
    """Print and record a check result."""
    _results.setdefault(section, [])
    _results[section].append((tag, msg))
    print(f"  [{tag}] {msg}")


def PASS(section: str, msg: str) -> None:
    _record(section, "PASS", msg)


def FAIL(section: str, msg: str) -> None:
    _record(section, "FAIL", msg)


def WARN(section: str, msg: str) -> None:
    _record(section, "WARN", msg)


# ===================================================================
# SECTION 1: Volume & Shape
# ===================================================================
def check_volume_shape(nc: pd.DataFrame, border: pd.DataFrame) -> None:
    SEC = "Volume & Shape"
    print(f"\n{'='*60}\n  {SEC}\n{'='*60}")

    # 1 NC row count
    n_nc = len(nc)
    (PASS if n_nc == 2195 else FAIL)(
        SEC, f"NC row count: {n_nc:,} (expect 2,195)"
    )

    # 2 Border row count
    n_border = len(border)
    (PASS if n_border == 8671 else FAIL)(
        SEC, f"Border row count: {n_border:,} (expect 8,671)"
    )

    # 3 Column count
    n_cols = len(nc.columns)
    (PASS if n_cols == 6 else FAIL)(
        SEC, f"Column count: {n_cols} (expect 6)"
    )
    print(f"    Columns: {list(nc.columns)}")

    # 4 Dtypes
    fips_dtype = nc["tract_fips"].dtype
    fips_ok = fips_dtype in (object, "object", "str", "string")
    disadv_ok = nc["disadvantaged"].dtype in ("int64", "float64")
    pop_ok = nc["population"].dtype == "float64"
    all_dtypes = fips_ok and disadv_ok and pop_ok
    (PASS if all_dtypes else FAIL)(
        SEC,
        f"Dtypes: tract_fips={fips_dtype} "
        f"(expect string/object), disadvantaged={nc['disadvantaged'].dtype} "
        f"(expect int/float), population={nc['population'].dtype} "
        f"(expect float)",
    )


# ===================================================================
# SECTION 2: Completeness & Quality
# ===================================================================
def check_completeness(nc: pd.DataFrame) -> None:
    SEC = "Completeness & Quality"
    print(f"\n{'='*60}\n  {SEC}\n{'='*60}")

    # 1 Nulls per column
    nulls = nc.isnull().sum()
    total_null = nulls.sum()
    (PASS if total_null == 0 else FAIL)(
        SEC, f"Total nulls: {total_null}"
    )
    if total_null > 0:
        for col, cnt in nulls.items():
            if cnt > 0:
                print(f"    {col}: {cnt}")

    # 2 tract_fips uniqueness
    n_unique = nc["tract_fips"].nunique()
    n_total = len(nc)
    (PASS if n_unique == n_total else FAIL)(
        SEC, f"tract_fips unique: {n_unique:,} vs rows: {n_total:,}"
    )

    # 3 FIPS format validation
    len_ok = (nc["tract_fips"].str.len() == 11).all()
    starts_37 = nc["tract_fips"].str[:2].eq("37").all()
    (PASS if len_ok and starts_37 else FAIL)(
        SEC,
        f"FIPS format: 11-digit={len_ok}, starts with '37'={starts_37}",
    )

    # 4 disadvantaged binary check
    vals = set(nc["disadvantaged"].unique())
    binary_ok = vals.issubset({0, 1, 0.0, 1.0})
    (PASS if binary_ok else FAIL)(
        SEC,
        f"disadvantaged values: {sorted(vals)} (expect only 0 and 1)",
    )


# ===================================================================
# SECTION 3: Distributions
# ===================================================================
def check_distributions(nc: pd.DataFrame) -> None:
    SEC = "Distributions"
    print(f"\n{'='*60}\n  {SEC}\n{'='*60}")

    # Evaluable tracts (population > 0)
    evaluable = nc[nc["population"] > 0].copy()
    n_eval = len(evaluable)
    n_excluded = len(nc) - n_eval
    print(f"    Evaluable tracts: {n_eval:,} (excluded {n_excluded} "
          f"with population=0)")

    # 1 Disadvantaged flag split on evaluable tracts
    n_disadv = int(evaluable["disadvantaged"].sum())
    pct_disadv = n_disadv / n_eval * 100
    pct_ok = 40.0 <= pct_disadv <= 46.0
    (PASS if pct_ok else WARN)(
        SEC,
        f"Disadvantaged split (evaluable): {n_disadv}/{n_eval} = "
        f"{pct_disadv:.1f}% (expect ~43.0%)",
    )

    # 2 threshold_count distribution
    tc = nc["threshold_count"]
    tc_stats = (
        f"min={tc.min()}, max={tc.max()}, "
        f"median={tc.median():.0f}, mean={tc.mean():.1f}"
    )
    PASS(SEC, f"threshold_count stats: {tc_stats}")
    bins = [0, 1, 2, 3, 4, 5, tc.max() + 1]
    labels = ["0", "1", "2", "3", "4", f"5-{int(tc.max())}"]
    tc_binned = pd.cut(tc, bins=bins, labels=labels, right=False)
    print("    threshold_count distribution:")
    for label, count in tc_binned.value_counts().sort_index().items():
        print(f"      {label}: {count:,}")

    # 3 Population summary stats
    pop = nc["population"]
    n_zeros = int((pop == 0).sum())
    pop_stats = (
        f"min={pop.min():.0f}, max={pop.max():.0f}, "
        f"median={pop.median():.0f}, sum={pop.sum():,.0f}, "
        f"zeros={n_zeros}"
    )
    zeros_ok = n_zeros == 25
    (PASS if zeros_ok else WARN)(
        SEC, f"Population stats: {pop_stats} (expect 25 zeros)"
    )

    # 4 Population vs disadvantaged cross-tab
    mean_disadv = evaluable.loc[
        evaluable["disadvantaged"] == 1, "population"
    ].mean()
    mean_non = evaluable.loc[
        evaluable["disadvantaged"] == 0, "population"
    ].mean()
    PASS(
        SEC,
        f"Mean pop: disadvantaged={mean_disadv:,.0f}, "
        f"non-disadvantaged={mean_non:,.0f}",
    )


# ===================================================================
# SECTION 4: County-Level Aggregation
# ===================================================================
def check_county_aggregation(nc: pd.DataFrame) -> None:
    SEC = "County Aggregation"
    print(f"\n{'='*60}\n  {SEC}\n{'='*60}")

    # Evaluable tracts only
    evaluable = nc[nc["population"] > 0].copy()

    # 1 Disadvantaged tract count & pct per county (evaluable only)
    county_stats = (
        evaluable.groupby("county_name")
        .agg(
            total_tracts=("tract_fips", "count"),
            disadv_tracts=("disadvantaged", "sum"),
            total_pop=("population", "sum"),
            disadv_pop=("population", lambda x: x[
                evaluable.loc[x.index, "disadvantaged"] == 1
            ].sum()),
        )
        .reset_index()
    )
    county_stats["disadv_tracts"] = county_stats["disadv_tracts"].astype(int)
    county_stats["pct_disadv_tracts"] = (
        county_stats["disadv_tracts"] / county_stats["total_tracts"] * 100
    )

    n_counties = len(county_stats)
    (PASS if n_counties == 100 else FAIL)(
        SEC, f"Counties with evaluable tracts: {n_counties} (expect 100)"
    )

    # 2 Highlight 10 study counties
    study = county_stats[
        county_stats["county_name"].isin(STUDY_COUNTIES)
    ].sort_values("pct_disadv_tracts", ascending=False)

    n_study = len(study)
    (PASS if n_study == 10 else FAIL)(
        SEC, f"Study counties found: {n_study}/10"
    )

    print("    Study county disadvantaged rates (evaluable tracts):")
    print(f"    {'County':<25} {'Tracts':>7} {'Disadv':>7} {'Pct':>7}")
    print(f"    {'-'*46}")
    for _, row in study.iterrows():
        print(
            f"    {row['county_name']:<25} "
            f"{row['total_tracts']:>7} "
            f"{row['disadv_tracts']:>7} "
            f"{row['pct_disadv_tracts']:>6.1f}%"
        )

    # 3 Population-weighted % vs simple tract-count %
    print("\n    Population-weighted vs tract-count % for study counties:")
    print(
        f"    {'County':<25} {'Tract%':>8} {'PopWt%':>8} {'Diff':>7}"
    )
    print(f"    {'-'*48}")
    for _, row in study.iterrows():
        cty = row["county_name"]
        cty_eval = evaluable[evaluable["county_name"] == cty]
        disadv_mask = cty_eval["disadvantaged"] == 1
        pop_wt_pct = (
            cty_eval.loc[disadv_mask, "population"].sum()
            / cty_eval["population"].sum()
            * 100
        )
        tract_pct = row["pct_disadv_tracts"]
        diff = pop_wt_pct - tract_pct
        print(
            f"    {cty:<25} {tract_pct:>7.1f}% "
            f"{pop_wt_pct:>7.1f}% {diff:>+6.1f}%"
        )

    PASS(SEC, "County-level aggregation complete")


# ===================================================================
# SECTION 5: Cross-File Validation (LEHD Crosswalk)
# ===================================================================
def check_crosswalk_match(nc: pd.DataFrame) -> None:
    SEC = "Crosswalk Match"
    print(f"\n{'='*60}\n  {SEC}\n{'='*60}")

    # 1 Extract unique NC tract FIPS from LEHD crosswalk
    xw = pd.read_csv(XW_PATH, dtype={"trct": str}, usecols=["trct"])
    xw_nc = xw[xw["trct"].str[:2] == "37"]
    xw_tracts = set(xw_nc["trct"].unique())
    n_xw = len(xw_tracts)
    PASS(SEC, f"Unique NC tracts in crosswalk: {n_xw:,}")

    # 2 Match CEJST tract FIPS against crosswalk
    cejst_tracts = set(nc["tract_fips"].unique())
    overlap = cejst_tracts & xw_tracts
    n_overlap = len(overlap)
    PASS(SEC, f"Overlapping tracts: {n_overlap:,}")

    # 3 Count mismatches
    cejst_only = sorted(cejst_tracts - xw_tracts)
    xw_only = sorted(xw_tracts - cejst_tracts)

    n_cejst_only = len(cejst_only)
    n_xw_only = len(xw_only)

    tag = "PASS" if n_cejst_only == 0 else "WARN"
    _record(
        SEC, tag,
        f"Tracts in CEJST but not crosswalk: {n_cejst_only}",
    )
    if n_cejst_only > 0 and n_cejst_only <= 20:
        for t in cejst_only:
            print(f"      {t}")
    elif n_cejst_only > 20:
        for t in cejst_only[:10]:
            print(f"      {t}")
        print(f"      ... and {n_cejst_only - 10} more")

    tag = "PASS" if n_xw_only == 0 else "WARN"
    _record(
        SEC, tag,
        f"Tracts in crosswalk but not CEJST: {n_xw_only}",
    )
    if n_xw_only > 0 and n_xw_only <= 20:
        for t in xw_only:
            print(f"      {t}")
    elif n_xw_only > 20:
        for t in xw_only[:10]:
            print(f"      {t}")
        print(f"      ... and {n_xw_only - 10} more")

    # 4 Document implications
    if n_cejst_only > 0 or n_xw_only > 0:
        print(
            "\n    NOTE: Mismatches are expected due to Census tract "
            "vintage differences\n"
            "    (CEJST uses 2010 tracts; LEHD crosswalk may use "
            "2010/2020 hybrid).\n"
            "    These will be handled via tract-level joins with "
            "appropriate fallbacks."
        )
        PASS(SEC, "Vintage mismatch documented")
    else:
        PASS(SEC, "Perfect tract match -- no vintage mismatch")


# ===================================================================
# SECTION 6: Border File Consistency
# ===================================================================
def check_border_consistency(
    nc: pd.DataFrame, border: pd.DataFrame
) -> None:
    SEC = "Border Consistency"
    print(f"\n{'='*60}\n  {SEC}\n{'='*60}")

    # 1 Verify border file contains all NC tracts
    nc_tracts = set(nc["tract_fips"])
    border_nc = border[border["state_name"] == "North Carolina"]
    border_nc_tracts = set(border_nc["tract_fips"])

    all_present = nc_tracts.issubset(border_nc_tracts)
    missing = nc_tracts - border_nc_tracts
    (PASS if all_present else FAIL)(
        SEC,
        f"All NC tracts in border file: {all_present} "
        f"(missing: {len(missing)})",
    )

    # 2 State distribution of border-only (non-NC) tracts
    non_nc = border[border["state_name"] != "North Carolina"]
    state_dist = non_nc["state_name"].value_counts()
    PASS(SEC, f"Non-NC states in border file: {len(state_dist)}")
    print("    State distribution of border tracts:")
    for state, count in state_dist.items():
        print(f"      {state}: {count:,}")


# ===================================================================
# SPECIAL CHECK: Dr. Whitfield Flag (Cumberland County)
# ===================================================================
def check_cumberland(nc: pd.DataFrame) -> None:
    SEC = "Cumberland (Whitfield)"
    print(f"\n{'='*60}\n  {SEC}\n{'='*60}")

    cumb_all = nc[nc["county_name"] == "Cumberland County"]
    cumb_eval = cumb_all[cumb_all["population"] > 0]
    cumb_excluded = cumb_all[cumb_all["population"] == 0]

    n_all = len(cumb_all)
    n_eval = len(cumb_eval)
    n_excl = len(cumb_excluded)
    print(
        f"    Cumberland County: {n_all} total tracts, "
        f"{n_eval} evaluable, {n_excl} excluded (pop=0)"
    )

    if n_excl > 0:
        print("    Excluded tracts:")
        for _, row in cumb_excluded.iterrows():
            print(
                f"      {row['tract_fips']}  "
                f"disadvantaged={int(row['disadvantaged'])}  "
                f"threshold_count={int(row['threshold_count'])}  "
                f"pop={row['population']}"
            )

    # With exclusion (evaluable only)
    disadv_eval = int(cumb_eval["disadvantaged"].sum())
    pct_eval = disadv_eval / n_eval * 100 if n_eval > 0 else 0

    # Without exclusion (all tracts)
    disadv_all = int(cumb_all["disadvantaged"].sum())
    pct_all = disadv_all / n_all * 100 if n_all > 0 else 0

    diff = abs(pct_eval - pct_all)
    negligible = diff < 2.0

    (PASS if negligible else WARN)(
        SEC,
        f"Disadvantaged %: with exclusion={pct_eval:.1f}% "
        f"({disadv_eval}/{n_eval}), "
        f"without exclusion={pct_all:.1f}% ({disadv_all}/{n_all}), "
        f"diff={diff:.1f}pp (negligible={negligible})",
    )


# ===================================================================
# SUMMARY TABLE
# ===================================================================
def print_summary() -> None:
    sections = [
        "Volume & Shape",
        "Completeness & Quality",
        "Distributions",
        "County Aggregation",
        "Crosswalk Match",
        "Border Consistency",
        "Cumberland (Whitfield)",
    ]

    print(f"\n{'='*60}")
    print("  PHASE 5 CEJST JUSTICE40 EDA SUMMARY")
    print(f"{'='*60}")
    header = (
        f"{'Section':<26} {'Checks':>7} {'Passed':>7} "
        f"{'Failed':>7} {'Warnings':>9}"
    )
    print(header)
    print("-" * len(header))

    grand = {"checks": 0, "passed": 0, "failed": 0, "warnings": 0}
    for section in sections:
        items = _results.get(section, [])
        checks = len(items)
        passed = sum(1 for t, _ in items if t == "PASS")
        failed = sum(1 for t, _ in items if t == "FAIL")
        warnings = sum(1 for t, _ in items if t == "WARN")
        grand["checks"] += checks
        grand["passed"] += passed
        grand["failed"] += failed
        grand["warnings"] += warnings
        print(
            f"{section:<26} {checks:>7} {passed:>7} "
            f"{failed:>7} {warnings:>9}"
        )

    print("-" * len(header))
    print(
        f"{'TOTAL':<26} {grand['checks']:>7} {grand['passed']:>7} "
        f"{grand['failed']:>7} {grand['warnings']:>9}"
    )

    if grand["failed"] == 0 and grand["warnings"] == 0:
        print(
            "\n  ALL GREEN -- safe to proceed to equity overlay analysis"
        )
    elif grand["failed"] == 0:
        print(
            f"\n  {grand['warnings']} WARNING(s) -- review above, "
            "likely safe to proceed"
        )
    else:
        print(
            f"\n  {grand['failed']} FAILURE(s) -- "
            "investigate before proceeding"
        )


# ===================================================================
# MAIN
# ===================================================================
def main() -> None:
    print("=" * 60)
    print("  Phase 5 EDA: CEJST Justice40 Disadvantaged-Tract Data")
    print("=" * 60)

    # Load data -- tract_fips always as string
    nc = pd.read_csv(NC_PATH, dtype={"tract_fips": str})
    border = pd.read_csv(BORDER_PATH, dtype={"tract_fips": str})

    check_volume_shape(nc, border)
    check_completeness(nc)
    check_distributions(nc)
    check_county_aggregation(nc)
    check_crosswalk_match(nc)
    check_border_consistency(nc, border)
    check_cumberland(nc)
    print_summary()


if __name__ == "__main__":
    main()
