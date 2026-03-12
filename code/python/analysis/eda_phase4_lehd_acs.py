#!/usr/bin/env python3
"""
Phase 4 EDA Sanity Checks: LEHD LODES + ACS Income/Tenure Data

Console-output-only sanity checks for four data files used in the
commuter-flow / socioeconomic analysis pipeline.  No figures produced.

Files checked:
    1. lehd-nc-od-main-2021.csv.gz  (OD commuter flows)
    2. lehd-nc-wac-2021.csv.gz      (workplace area characteristics)
    3. lehd-nc-xwalk.csv.gz         (geographic crosswalk)
    4. acs-nc-income-tenure-tracts.csv (ACS tract-level income + tenure)

Author: BIDA 670 EV-Pulse-NC Project
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

OD_PATH = RAW / "lehd-nc-od-main-2021.csv.gz"
WAC_PATH = RAW / "lehd-nc-wac-2021.csv.gz"
XW_PATH = RAW / "lehd-nc-xwalk.csv.gz"
ACS_PATH = RAW / "acs-nc-income-tenure-tracts.csv"

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
# CHECK 1: LODES OD
# ===================================================================
def check_od() -> pd.DataFrame:
    SEC = "LODES OD"
    print(f"\n{'='*60}\n  {SEC}\n{'='*60}")

    od_cols_needed = [
        "w_geocode", "h_geocode",
        "S000", "SA01", "SA02", "SA03",
        "SE01", "SE02", "SE03",
        "SI01", "SI02", "SI03",
        "createdate",
    ]
    df = pd.read_csv(
        OD_PATH,
        dtype={"w_geocode": str, "h_geocode": str},
        usecols=od_cols_needed,
    )

    # 1 row count
    n = len(df)
    tag = "PASS" if 3_500_000 <= n <= 4_000_000 else "WARN"
    _record(SEC, tag, f"Row count: {n:,} (expect ~3,768,428)")

    # 2 columns
    expected = {"w_geocode", "h_geocode", "S000", "SA01", "SA02", "SA03",
                "SE01", "SE02", "SE03", "SI01", "SI02", "SI03"}
    present = expected.issubset(set(df.columns))
    (PASS if present else FAIL)(SEC, f"Expected columns present: {present}")

    # 3 nulls
    nc = df.isnull().sum()
    total_null = nc.sum()
    (PASS if total_null == 0 else FAIL)(SEC, f"Total nulls: {total_null}")

    # 4 duplicates
    dup = df.duplicated(subset=["w_geocode", "h_geocode"]).sum()
    (PASS if dup == 0 else FAIL)(SEC, f"Duplicate (w,h) pairs: {dup:,}")

    # 5 NC FIPS w_geocode
    w_nc = df["w_geocode"].str[:2].eq("37").all()
    (PASS if w_nc else FAIL)(SEC, f"All w_geocode start with '37': {w_nc}")

    # 6 h_geocode state distribution
    # NOTE: "Main" type = both workplace AND residence in-state, so
    # all h_geocode starting with "37" is *expected* for NC Main file.
    # "Aux" type would show cross-state flows.
    h_states = df["h_geocode"].str[:2].value_counts().head(5)
    all_37 = (h_states.index == "37").all()
    if all_37:
        PASS(SEC, "h_geocode ALL '37' -- correct for Main OD type")
    else:
        WARN(SEC, "h_geocode has non-37 prefixes -- unexpected for Main type")
    for st, cnt in h_states.items():
        print(f"        {st}: {cnt:,}")

    # 7 S000 range
    s_min, s_max = df["S000"].min(), df["S000"].max()
    (PASS if s_min >= 1 else FAIL)(
        SEC, f"S000 range: min={s_min}, max={s_max:,}"
    )

    # 8 additive checks
    sa_ok = (df["SA01"] + df["SA02"] + df["SA03"] == df["S000"]).all()
    se_ok = (df["SE01"] + df["SE02"] + df["SE03"] == df["S000"]).all()
    si_ok = (df["SI01"] + df["SI02"] + df["SI03"] == df["S000"]).all()
    all_add = sa_ok and se_ok and si_ok
    (PASS if all_add else FAIL)(
        SEC,
        f"Additive: SA={sa_ok}, SE={se_ok}, SI={si_ok}",
    )

    # 9 SE03 share
    se3_share = df["SE03"].sum() / df["S000"].sum() * 100
    tag = "PASS" if 45 <= se3_share <= 65 else "WARN"
    _record(SEC, tag, f"SE03 share of S000: {se3_share:.1f}% (expect ~50-60%)")

    # 10 total S000
    total_s = df["S000"].sum()
    tag = "PASS" if 3_500_000 <= total_s <= 6_000_000 else "WARN"
    _record(SEC, tag, f"Total S000: {total_s:,} (expect ~4-5M)")

    # 11 geocode length
    w_len = (df["w_geocode"].str.len() == 15).all()
    h_len = (df["h_geocode"].str.len() == 15).all()
    (PASS if w_len and h_len else FAIL)(
        SEC, f"Geocode length 15: w={w_len}, h={h_len}"
    )

    # 12 createdate
    cd = df["createdate"].unique()
    PASS(SEC, f"createdate unique values: {cd.tolist()}")

    return df


# ===================================================================
# CHECK 2: LODES WAC
# ===================================================================
def check_wac() -> pd.DataFrame:
    SEC = "LODES WAC"
    print(f"\n{'='*60}\n  {SEC}\n{'='*60}")

    df = pd.read_csv(WAC_PATH, dtype={"w_geocode": str})

    # 1 row count
    n = len(df)
    tag = "PASS" if 65_000 <= n <= 80_000 else "WARN"
    _record(SEC, tag, f"Row count: {n:,} (expect ~71,921)")

    # 2 columns
    for c in ["C000", "CE01", "CE02", "CE03"]:
        (PASS if c in df.columns else FAIL)(SEC, f"Column {c} present")

    # 3 CE additive
    ce_ok = (df["CE01"] + df["CE02"] + df["CE03"] == df["C000"]).all()
    (PASS if ce_ok else FAIL)(SEC, f"CE01+CE02+CE03 == C000: {ce_ok}")

    # 4 CA additive
    if {"CA01", "CA02", "CA03"}.issubset(df.columns):
        ca_ok = (df["CA01"] + df["CA02"] + df["CA03"] == df["C000"]).all()
        (PASS if ca_ok else FAIL)(SEC, f"CA01+CA02+CA03 == C000: {ca_ok}")
    else:
        WARN(SEC, "CA01/CA02/CA03 columns not found, skip additive check")

    # 5 zero-worker blocks
    zero_w = (df["C000"] == 0).sum()
    (PASS if zero_w == 0 else WARN)(SEC, f"Blocks with C000=0: {zero_w}")

    # 6 NC FIPS
    all_nc = df["w_geocode"].str[:2].eq("37").all()
    (PASS if all_nc else FAIL)(SEC, f"All w_geocode start with '37': {all_nc}")

    # 7 length
    len_ok = (df["w_geocode"].str.len() == 15).all()
    (PASS if len_ok else FAIL)(SEC, f"w_geocode length 15: {len_ok}")

    # 8 nulls
    total_null = df.isnull().sum().sum()
    (PASS if total_null == 0 else FAIL)(SEC, f"Total nulls: {total_null}")

    # 9 C000 range
    c_min, c_max = df["C000"].min(), df["C000"].max()
    PASS(SEC, f"C000 range: min={c_min}, max={c_max:,}")

    # 10 CE03 share
    ce3_share = df["CE03"].sum() / df["C000"].sum() * 100
    tag = "PASS" if 45 <= ce3_share <= 65 else "WARN"
    _record(SEC, tag, f"CE03 share of C000: {ce3_share:.1f}% (expect ~50-60%)")

    # 11 unique w_geocode
    n_unique = df["w_geocode"].nunique()
    (PASS if n_unique == n else FAIL)(
        SEC, f"Unique w_geocode: {n_unique:,} vs rows: {n:,}"
    )

    # 12 total C000
    total_c = df["C000"].sum()
    tag = "PASS" if 4_000_000 <= total_c <= 5_500_000 else "WARN"
    _record(SEC, tag, f"Total C000: {total_c:,} (expect ~4.5-5M)")

    return df


# ===================================================================
# CHECK 3: Crosswalk
# ===================================================================
def check_xwalk(od_df: pd.DataFrame, wac_df: pd.DataFrame) -> pd.DataFrame:
    SEC = "Crosswalk"
    print(f"\n{'='*60}\n  {SEC}\n{'='*60}")

    xw = pd.read_csv(
        XW_PATH,
        dtype={"tabblk2020": str, "st": str, "cty": str, "trct": str},
        usecols=["tabblk2020", "st", "cty", "ctyname", "trct"],
    )

    # 1 row count
    n = len(xw)
    tag = "PASS" if 230_000 <= n <= 245_000 else "WARN"
    _record(SEC, tag, f"Row count: {n:,} (expect ~236,638)")

    # 2 key columns
    for c in ["tabblk2020", "st", "cty", "trct", "ctyname"]:
        (PASS if c in xw.columns else FAIL)(SEC, f"Column '{c}' present")

    # 3 st == 37
    st_ok = (xw["st"] == "37").all()
    (PASS if st_ok else FAIL)(SEC, f"All st == '37': {st_ok}")

    # 4 unique counties
    n_cty = xw["cty"].nunique()
    (PASS if n_cty == 100 else FAIL)(SEC, f"Unique cty values: {n_cty} (expect 100)")

    # 5 county names
    counties = sorted(xw["ctyname"].dropna().unique())
    PASS(SEC, f"County names ({len(counties)} unique):")
    for i in range(0, len(counties), 5):
        chunk = counties[i : i + 5]
        print(f"        {', '.join(chunk)}")

    # 6 unique tracts
    n_trct = xw["trct"].nunique()
    tag = "PASS" if 2_100 <= n_trct <= 2_800 else "WARN"
    _record(SEC, tag, f"Unique trct count: {n_trct:,} (expect ~2,195-2,672)")

    # 7 tabblk2020 length
    len_ok = (xw["tabblk2020"].str.len() == 15).all()
    (PASS if len_ok else FAIL)(SEC, f"tabblk2020 length 15: {len_ok}")

    # 8 nulls
    null_counts = xw[["tabblk2020", "st", "cty", "trct", "ctyname"]].isnull().sum()
    total_null = null_counts.sum()
    (PASS if total_null == 0 else FAIL)(SEC, f"Nulls in key cols: {total_null}")

    # 9 coverage: OD w_geocode in crosswalk
    xw_blocks = set(xw["tabblk2020"])
    od_w = set(od_df["w_geocode"].unique())
    orphan_od = od_w - xw_blocks
    n_orph = len(orphan_od)
    if n_orph == 0:
        PASS(SEC, "OD w_geocode coverage: all found in crosswalk")
    else:
        orphan_s000 = od_df[od_df["w_geocode"].isin(orphan_od)]["S000"].sum()
        total_s000 = od_df["S000"].sum()
        pct = orphan_s000 / total_s000 * 100
        tag = "WARN" if pct < 1 else "FAIL"
        _record(
            SEC,
            tag,
            f"OD w_geocode orphans: {n_orph:,} blocks, "
            f"S000={orphan_s000:,} ({pct:.2f}% of total)",
        )

    # 10 coverage: WAC w_geocode in crosswalk
    wac_w = set(wac_df["w_geocode"].unique())
    orphan_wac = wac_w - xw_blocks
    n_orph_w = len(orphan_wac)
    (PASS if n_orph_w == 0 else WARN)(
        SEC, f"WAC w_geocode orphans: {n_orph_w:,}"
    )

    # 11 duplicate tabblk2020
    dup = xw["tabblk2020"].duplicated().sum()
    (PASS if dup == 0 else FAIL)(SEC, f"Duplicate tabblk2020: {dup:,}")

    # 12 cty format
    sample_cty = xw["cty"].iloc[0]
    cty_len = len(sample_cty)
    PASS(SEC, f"cty column format: {cty_len}-digit (sample: '{sample_cty}')")

    return xw


# ===================================================================
# CHECK 4: ACS Income/Tenure
# ===================================================================
def check_acs() -> pd.DataFrame:
    SEC = "ACS Income/Tenure"
    print(f"\n{'='*60}\n  {SEC}\n{'='*60}")

    df = pd.read_csv(
        ACS_PATH,
        dtype={"state": str, "county": str, "tract": str},
    )

    # 1 row count and header check
    n_raw = len(df)
    PASS(SEC, f"Raw row count: {n_raw:,}")

    # Check for Census API header row (strings in numeric columns)
    first = df.iloc[0]
    numeric_cols = [
        "B19001_001E", "B25003_001E", "B25003_002E", "B25003_003E",
    ]
    header_row = False
    for c in numeric_cols:
        if c in df.columns:
            try:
                float(first[c])
            except (ValueError, TypeError):
                header_row = True
                break
    if header_row:
        WARN(SEC, "First row looks like Census API header -- dropping it")
        df = df.iloc[1:].reset_index(drop=True)

    # Cast numeric columns
    for c in df.columns:
        if c not in ("NAME", "state", "county", "tract"):
            df[c] = pd.to_numeric(df[c], errors="coerce")

    # 2 filter state == 37
    df37 = df[df["state"] == "37"].copy()
    n37 = len(df37)
    tag = "PASS" if 2_100 <= n37 <= 2_800 else "WARN"
    _record(SEC, tag, f"Rows with state='37': {n37:,} (expect ~2,195-2,672)")

    # 3 unique counties
    n_cty = df37["county"].nunique()
    (PASS if n_cty == 100 else FAIL)(
        SEC, f"Unique counties: {n_cty} (expect 100)"
    )

    # 4 unique tracts
    n_trct = df37["tract"].nunique()
    PASS(SEC, f"Unique tracts: {n_trct:,}")

    # 5 sentinel -666666666
    sentinel_count = (df37[numeric_cols] == -666666666).sum().sum()
    (PASS if sentinel_count == 0 else WARN)(
        SEC, f"Sentinel -666666666 values: {sentinel_count}"
    )

    # 6 nulls
    total_null = df37.isnull().sum().sum()
    (PASS if total_null == 0 else WARN)(SEC, f"Total nulls: {total_null}")

    # 7 tenure additive
    tenure_ok = (
        df37["B25003_002E"] + df37["B25003_003E"] == df37["B25003_001E"]
    ).all()
    (PASS if tenure_ok else FAIL)(
        SEC, f"B25003_002E + 003E == 001E (owner+renter=total): {tenure_ok}"
    )

    # 8 income bins sum <= total
    inc_cols = [
        "B19001_013E", "B19001_014E", "B19001_015E",
        "B19001_016E", "B19001_017E",
    ]
    bin_sum = df37[inc_cols].sum(axis=1)
    inc_ok = (bin_sum <= df37["B19001_001E"]).all()
    (PASS if inc_ok else FAIL)(
        SEC, f"Income bins 013-017 sum <= B19001_001E: {inc_ok}"
    )

    # 9 >$75K share
    high_inc = df37[inc_cols].sum().sum()
    total_hh = df37["B19001_001E"].sum()
    high_share = high_inc / total_hh * 100
    tag = "PASS" if 30 <= high_share <= 50 else "WARN"
    _record(
        SEC, tag,
        f"Statewide >$75K share: {high_share:.1f}% (expect ~35-45%)",
    )

    # 10 renter share
    renter = df37["B25003_003E"].sum()
    tenure_total = df37["B25003_001E"].sum()
    renter_share = renter / tenure_total * 100
    tag = "PASS" if 28 <= renter_share <= 42 else "WARN"
    _record(
        SEC, tag,
        f"Statewide renter share: {renter_share:.1f}% (expect ~33-37%)",
    )

    # 11 B25003_001E vs B19001_001E comparison
    ratio = tenure_total / total_hh
    tag = "PASS" if 0.90 <= ratio <= 1.10 else "WARN"
    _record(
        SEC, tag,
        f"B25003_001E / B19001_001E ratio: {ratio:.4f} "
        f"(tenure total {tenure_total:,} vs income total {total_hh:,})",
    )

    # 12 tract FIPS format
    tract_lens = df37["tract"].str.len().unique()
    PASS(SEC, f"Tract FIPS lengths: {sorted(tract_lens.tolist())}")

    return df37


# ===================================================================
# CROSS-FILE CHECKS
# ===================================================================
def check_cross(
    od: pd.DataFrame,
    wac: pd.DataFrame,
    xw: pd.DataFrame,
    acs: pd.DataFrame,
) -> None:
    SEC = "Cross-File"
    print(f"\n{'='*60}\n  {SEC} Consistency\n{'='*60}")

    # 1 OD total S000 ≈ WAC total C000
    od_s000 = od["S000"].sum()
    wac_c000 = wac["C000"].sum()
    pct_diff = abs(od_s000 - wac_c000) / wac_c000 * 100
    tag = "PASS" if pct_diff < 5 else "WARN"
    _record(
        SEC, tag,
        f"OD S000={od_s000:,} vs WAC C000={wac_c000:,} "
        f"(diff {pct_diff:.2f}%)",
    )

    # 2 OD SE03 ≈ WAC CE03
    od_se3 = od["SE03"].sum()
    wac_ce3 = wac["CE03"].sum()
    pct_diff2 = abs(od_se3 - wac_ce3) / wac_ce3 * 100
    tag = "PASS" if pct_diff2 < 5 else "WARN"
    _record(
        SEC, tag,
        f"OD SE03={od_se3:,} vs WAC CE03={wac_ce3:,} "
        f"(diff {pct_diff2:.2f}%)",
    )

    # 3 crosswalk tracts vs ACS tracts
    # Crosswalk trct is 11-digit (state+county+tract), ACS has separate
    # state/county/tract columns. Build full FIPS from ACS for comparison.
    xw_trcts = set(xw["trct"].unique())
    acs_trcts = set(
        (acs["state"] + acs["county"] + acs["tract"]).unique()
    )
    print(f"    (xw trct sample: {next(iter(xw_trcts))}, "
          f"ACS built sample: {next(iter(acs_trcts))})")
    overlap = xw_trcts & acs_trcts
    xw_only = xw_trcts - acs_trcts
    acs_only = acs_trcts - xw_trcts
    overlap_pct = len(overlap) / max(len(xw_trcts), len(acs_trcts)) * 100
    tag = "PASS" if overlap_pct >= 95 else "WARN"
    _record(
        SEC, tag,
        f"Tract overlap: {len(overlap):,} shared, "
        f"{len(xw_only):,} xwalk-only, {len(acs_only):,} ACS-only "
        f"({overlap_pct:.1f}%)",
    )

    # 4 county counts
    xw_cty = xw["cty"].nunique()
    acs_cty = acs["county"].nunique()
    all_100 = xw_cty == 100 and acs_cty == 100
    (PASS if all_100 else WARN)(
        SEC,
        f"County counts: crosswalk={xw_cty}, ACS={acs_cty} (expect 100)",
    )


# ===================================================================
# SUMMARY TABLE
# ===================================================================
def print_summary() -> None:
    print(f"\n{'='*60}")
    print("  PHASE 4 EDA SUMMARY")
    print(f"{'='*60}")
    header = f"{'File':<22} {'Checks':>7} {'Passed':>7} {'Failed':>7} {'Warnings':>9}"
    print(header)
    print("-" * len(header))

    grand = {"checks": 0, "passed": 0, "failed": 0, "warnings": 0}
    for section in [
        "LODES OD", "LODES WAC", "Crosswalk",
        "ACS Income/Tenure", "Cross-File",
    ]:
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
            f"{section:<22} {checks:>7} {passed:>7} {failed:>7} {warnings:>9}"
        )

    print("-" * len(header))
    print(
        f"{'TOTAL':<22} {grand['checks']:>7} {grand['passed']:>7} "
        f"{grand['failed']:>7} {grand['warnings']:>9}"
    )

    if grand["failed"] == 0 and grand["warnings"] == 0:
        print("\n  ALL GREEN -- safe to proceed to Step 2 (analysis pipeline)")
    elif grand["failed"] == 0:
        print(
            f"\n  {grand['warnings']} WARNING(s) -- review above, "
            "likely safe to proceed"
        )
    else:
        print(
            f"\n  {grand['failed']} FAILURE(s) -- investigate before proceeding"
        )


# ===================================================================
# MAIN
# ===================================================================
def main() -> None:
    print("=" * 60)
    print("  Phase 4 EDA: LEHD LODES + ACS Income/Tenure")
    print("=" * 60)

    od_df = check_od()
    wac_df = check_wac()
    xw_df = check_xwalk(od_df, wac_df)
    acs_df = check_acs()
    check_cross(od_df, wac_df, xw_df, acs_df)
    print_summary()


if __name__ == "__main__":
    main()
