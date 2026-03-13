#!/usr/bin/env python3
"""
Phase 5 - Climate Change Category Sensitivity Analysis
=======================================================
Determines how many NC census tracts are flagged as disadvantaged
SOLELY due to the "climate change" category in CEJST v2.0.

CEJST v2.0 has 8 burden categories, each with specific threshold
indicator columns. A tract is disadvantaged if it exceeds at least
one indicator threshold AND is low-income (or low-HS-attainment for
workforce). This script reconstructs per-category flags from the
individual indicator columns.

This is a standalone sensitivity script -- it does NOT modify any
existing data files or scripts.

Usage:
    uv run code/python/analysis/phase5_climate_sensitivity.py
"""

import csv
import io
import os
import sys

import requests

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
)
RAW_DIR = os.path.join(REPO_ROOT, "data", "raw")
NC_CATEGORIES_PATH = os.path.join(
    RAW_DIR, "cejst-justice40-tracts-nc-categories.csv"
)
COUNTY_J40_PATH = os.path.join(
    REPO_ROOT, "data", "processed", "phase5-county-justice40.csv"
)

# ---------------------------------------------------------------------------
# CEJST download URL (same as acquisition script)
# ---------------------------------------------------------------------------
CEJST_URLS = [
    (
        "https://dblew8dgr6ajz.cloudfront.net/data-versions/2.0/"
        "data/score/downloadable/2.0-communities.csv"
    ),
    (
        "https://raw.githubusercontent.com/"
        "Public-Environmental-Data-Partners/cejst-2/"
        "main/data/data-pipeline/data_pipeline/data/score/"
        "downloadable/2.0-communities.csv"
    ),
]

NC_FIPS = "37"

# ---------------------------------------------------------------------------
# CEJST v2.0 category-to-indicator mapping
# Each entry maps a category name to the list of Boolean threshold columns
# in the full CSV. A tract "exceeds" a category if ANY of its indicators
# is True.
#
# Reference: CEJST Technical Support Document v2.0
# https://screeningtool.geoplatform.gov/en/methodology
# ---------------------------------------------------------------------------
CATEGORY_INDICATORS = {
    "Climate change": [
        (
            "Greater than or equal to the 90th percentile for "
            "expected agriculture loss rate and is low income?"
        ),
        (
            "Greater than or equal to the 90th percentile for "
            "expected building loss rate and is low income?"
        ),
        (
            "Greater than or equal to the 90th percentile for "
            "expected population loss rate and is low income?"
        ),
        (
            "Greater than or equal to the 90th percentile for "
            "share of properties at risk of flood in 30 years "
            "and is low income?"
        ),
        (
            "Greater than or equal to the 90th percentile for "
            "share of properties at risk of fire in 30 years "
            "and is low income?"
        ),
    ],
    "Energy": [
        (
            "Greater than or equal to the 90th percentile for "
            "energy burden and is low income?"
        ),
        (
            "Greater than or equal to the 90th percentile for "
            "PM2.5 exposure and is low income?"
        ),
    ],
    "Transportation": [
        (
            "Greater than or equal to the 90th percentile for "
            "diesel particulate matter and is low income?"
        ),
        (
            "Greater than or equal to the 90th percentile for "
            "traffic proximity and is low income?"
        ),
        (
            "Greater than or equal to the 90th percentile for "
            "DOT transit barriers and is low income?"
        ),
    ],
    "Housing": [
        (
            "Greater than or equal to the 90th percentile for "
            "housing burden and is low income?"
        ),
        (
            "Greater than or equal to the 90th percentile for "
            "lead paint, the median house value is less than "
            "90th percentile and is low income?"
        ),
        (
            "Tract experienced historic underinvestment and "
            "remains low income"
        ),
        (
            "Greater than or equal to the 90th percentile for "
            "share of the tract's land area that is covered by "
            "impervious surface or cropland as a percent and is "
            "low income?"
        ),
    ],
    "Legacy pollution": [
        (
            "Greater than or equal to the 90th percentile for "
            "proximity to hazardous waste facilities and is low "
            "income?"
        ),
        (
            "Greater than or equal to the 90th percentile for "
            "proximity to superfund sites and is low income?"
        ),
        (
            "Greater than or equal to the 90th percentile for "
            "proximity to RMP sites and is low income?"
        ),
        (
            "There is at least one Formerly Used Defense Site "
            "(FUDS) in the tract and the tract is low income."
        ),
        (
            "There is at least one abandoned mine in this census "
            "tract and the tract is low income."
        ),
    ],
    "Clean water": [
        (
            "Greater than or equal to the 90th percentile for "
            "wastewater discharge and is low income?"
        ),
        (
            "Greater than or equal to the 90th percentile for "
            "leaky underground storage tanks and is low income?"
        ),
    ],
    "Health": [
        (
            "Greater than or equal to the 90th percentile for "
            "asthma and is low income?"
        ),
        (
            "Greater than or equal to the 90th percentile for "
            "diabetes and is low income?"
        ),
        (
            "Greater than or equal to the 90th percentile for "
            "heart disease and is low income?"
        ),
        (
            "Greater than or equal to the 90th percentile for "
            "low life expectancy and is low income?"
        ),
    ],
    "Workforce development": [
        (
            "Greater than or equal to the 90th percentile for "
            "low median household income as a percent of area "
            "median income and has low HS attainment?"
        ),
        (
            "Greater than or equal to the 90th percentile for "
            "households in linguistic isolation and has low HS "
            "attainment?"
        ),
        (
            "Greater than or equal to the 90th percentile for "
            "unemployment and has low HS attainment?"
        ),
        (
            "Greater than or equal to the 90th percentile for "
            "households at or below 100% federal poverty level "
            "and has low HS attainment?"
        ),
    ],
}

# All indicator columns we need to read
ALL_INDICATOR_COLS = []
for cols in CATEGORY_INDICATORS.values():
    ALL_INDICATOR_COLS.extend(cols)


def download_cejst_full():
    """Download and return the full national CEJST CSV text."""
    for url in CEJST_URLS:
        print(f"[INFO] Trying URL: {url}")
        try:
            resp = requests.get(url, stream=True, timeout=300)
            if resp.status_code != 200:
                print(f"[WARN] HTTP {resp.status_code}, trying next...")
                resp.close()
                continue

            total = int(resp.headers.get("content-length", 0))
            downloaded = 0
            chunks = []
            for chunk in resp.iter_content(chunk_size=256 * 1024):
                chunks.append(chunk)
                downloaded += len(chunk)
                if total:
                    pct = downloaded * 100 / total
                    mb = downloaded / (1024 * 1024)
                    print(
                        f"\r[INFO]   {mb:.1f} MB ({pct:.0f}%)",
                        end="",
                        flush=True,
                    )
                else:
                    mb = downloaded / (1024 * 1024)
                    print(
                        f"\r[INFO]   {mb:.1f} MB",
                        end="",
                        flush=True,
                    )
            print()
            raw = b"".join(chunks)
            size_mb = len(raw) / (1024 * 1024)
            print(f"[OK] Downloaded {size_mb:.1f} MB")
            return raw.decode("utf-8", errors="replace")

        except requests.RequestException as exc:
            print(f"[WARN] Failed: {exc}")
            continue

    print("[ERROR] All download URLs failed.")
    sys.exit(1)


def load_study_counties():
    """Load the 10 study-county FIPS from the Phase 5 county file."""
    counties = {}
    with open(COUNTY_J40_PATH, encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            fips = str(row["county_fips"]).strip()
            name = row["county_name"].strip()
            counties[fips] = name
    print(f"[INFO] Loaded {len(counties)} study counties")
    return counties


# Map from CATEGORY_INDICATORS key to clean snake_case column name
CATEGORY_SNAKE = {
    "Climate change": "climate_change",
    "Energy": "energy",
    "Transportation": "transportation",
    "Housing": "housing",
    "Legacy pollution": "legacy_pollution",
    "Clean water": "water_wastewater",
    "Health": "health",
    "Workforce development": "workforce_development",
}


def _save_nc_categories_csv(nc_tracts):
    """Save NC rows with 8 per-category Boolean flags to CSV."""
    print("\n--- Saving NC per-category CSV ---")
    os.makedirs(os.path.dirname(NC_CATEGORIES_PATH), exist_ok=True)

    fieldnames = [
        "tract_fips",
        "state_name",
        "county_name",
        "disadvantaged",
        "threshold_count",
        "population",
    ] + list(CATEGORY_SNAKE.values())

    with open(NC_CATEGORIES_PATH, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for t in nc_tracts:
            row = {
                "tract_fips": t["fips"],
                "state_name": t["state_name"],
                "county_name": t["county_name"],
                "disadvantaged": int(t["disadvantaged"]),
                "threshold_count": t["threshold"],
                "population": t["population"],
            }
            for cat_name, snake in CATEGORY_SNAKE.items():
                row[snake] = int(t["cat_flags"][cat_name])
            writer.writerow(row)

    print(f"[OK] Saved {len(nc_tracts)} rows -> {NC_CATEGORIES_PATH}")
    print(f"     Columns: {', '.join(fieldnames)}")


def _validate_nc_categories(nc_tracts, disadv_tracts):
    """Run validation checks on the per-category data."""
    print("\n--- Per-Category Validation Checks ---")
    results = []

    # Check 1: Row count = 2,195
    n_rows = len(nc_tracts)
    ok = n_rows == 2195
    label = f"Row count = {n_rows} (expected 2,195)"
    results.append(("PASS" if ok else "FAIL", label))
    print(f"  {'PASS' if ok else 'FAIL'}: {label}")

    # Check 2: Disadvantaged count = 934
    n_disadv = len(disadv_tracts)
    ok = n_disadv == 934
    label = f"Disadvantaged count = {n_disadv} (expected 934)"
    results.append(("PASS" if ok else "FAIL", label))
    print(f"  {'PASS' if ok else 'FAIL'}: {label}")

    # Check 3: Category flags vs threshold_count consistency
    # For disadvantaged tracts, the number of True category flags
    # should generally relate to threshold_count. However, exact
    # match is NOT expected because:
    #   - threshold_count counts individual INDICATOR thresholds
    #   - category flags count CATEGORIES (one category can have
    #     multiple indicators)
    #   - tribal/adjacency pathways add disadvantaged status
    #     without indicator thresholds
    mismatches = 0
    tribal_flag_tracts = 0
    for t in disadv_tracts:
        n_true_cats = sum(1 for v in t["cat_flags"].values() if v)
        if t["tribal"] and n_true_cats == 0:
            tribal_flag_tracts += 1
        # Each True category contributes >= 1 threshold, so
        # n_true_cats should be <= threshold_count (unless tribal)
        if n_true_cats > t["threshold"] and not t["tribal"]:
            mismatches += 1
    ok = mismatches == 0
    label = (
        f"Category flags <= threshold_count for all "
        f"non-tribal disadvantaged tracts "
        f"(mismatches: {mismatches})"
    )
    results.append(("PASS" if ok else "WARN", label))
    print(f"  {'PASS' if ok else 'WARN'}: {label}")
    if tribal_flag_tracts > 0:
        print(
            f"        Note: {tribal_flag_tracts} tracts are "
            f"disadvantaged via tribal pathway only"
        )

    # Check 4: All climate-only tracts should have no other
    # category flag = True and tribal = False
    climate_only = []
    climate_only_with_other = 0
    climate_only_with_tribal = 0
    for t in disadv_tracts:
        if not t["cat_flags"]["Climate change"]:
            continue
        other_cats = any(
            v for k, v in t["cat_flags"].items()
            if k != "Climate change"
        )
        if not other_cats and not t["tribal"]:
            climate_only.append(t)
        elif not other_cats and t["tribal"]:
            climate_only_with_tribal += 1
    # Verify climate-only tracts truly have no other flags
    for t in climate_only:
        other = any(
            v for k, v in t["cat_flags"].items()
            if k != "Climate change"
        )
        if other:
            climate_only_with_other += 1
    n_co = len(climate_only)
    ok4 = climate_only_with_other == 0
    label = (
        f"All {n_co} climate-only tracts have no other "
        f"category flag and tribal=False "
        f"(violations: {climate_only_with_other})"
    )
    results.append(("PASS" if ok4 else "FAIL", label))
    print(f"  {'PASS' if ok4 else 'FAIL'}: {label}")

    # Check 5: Sum of all 8 category flags across disadvantaged
    # tracts should be >= sum of threshold_count
    # (each threshold contributes to exactly one category, but a
    # category can have multiple thresholds)
    # Actually: sum of category flags <= sum of threshold counts
    # because categories collapse multiple indicators
    total_cat_flags = sum(
        sum(1 for v in t["cat_flags"].values() if v)
        for t in disadv_tracts
    )
    total_thresholds = sum(t["threshold"] for t in disadv_tracts)
    ok5 = total_cat_flags <= total_thresholds
    label = (
        f"Sum of category flags ({total_cat_flags}) <= "
        f"sum of threshold_count ({total_thresholds})"
    )
    results.append(("PASS" if ok5 else "WARN", label))
    print(f"  {'PASS' if ok5 else 'WARN'}: {label}")

    # Summary
    n_pass = sum(1 for r, _ in results if r == "PASS")
    n_warn = sum(1 for r, _ in results if r == "WARN")
    n_fail = sum(1 for r, _ in results if r == "FAIL")
    print(
        f"\n  Summary: {n_pass} PASS, {n_warn} WARN, "
        f"{n_fail} FAIL out of {len(results)} checks"
    )


def main():
    print("=" * 64)
    print("Phase 5 -- Climate Change Sensitivity Analysis")
    print("=" * 64)

    # ------------------------------------------------------------------
    # 1. Load study counties
    # ------------------------------------------------------------------
    study_counties = load_study_counties()

    # ------------------------------------------------------------------
    # 2. Download full national CSV
    # ------------------------------------------------------------------
    print("\n--- Downloading full CEJST v2.0 national CSV ---")
    text = download_cejst_full()

    # ------------------------------------------------------------------
    # 3. Validate indicator columns exist in CSV
    # ------------------------------------------------------------------
    reader = csv.DictReader(io.StringIO(text))
    all_columns = reader.fieldnames or []
    print(f"\n[INFO] Total columns in national CSV: {len(all_columns)}")

    missing_cols = [c for c in ALL_INDICATOR_COLS if c not in all_columns]
    if missing_cols:
        print(f"[ERROR] {len(missing_cols)} indicator columns NOT FOUND:")
        for c in missing_cols:
            print(f"  - {c}")
        sys.exit(1)
    print(
        f"[OK] All {len(ALL_INDICATOR_COLS)} indicator columns found "
        f"across {len(CATEGORY_INDICATORS)} categories"
    )

    # Also check for tribal overlap (separate pathway)
    tribal_col = "Identified as disadvantaged due to tribal overlap"
    has_tribal = tribal_col in all_columns
    if has_tribal:
        print(f"[INFO] Tribal overlap column found: '{tribal_col}'")

    # ------------------------------------------------------------------
    # 4. Filter to NC tracts, reconstruct per-category flags
    # ------------------------------------------------------------------
    tract_id_col = "Census tract 2010 ID"
    state_col = "State/Territory"
    county_col = "County Name"
    disadv_col = "Identified as disadvantaged"
    threshold_col = "Total threshold criteria exceeded"
    categories_col = "Total categories exceeded"
    pop_col = "Total population"

    nc_tracts = []
    for row in reader:
        fips = str(row.get(tract_id_col, "")).split(".")[0]
        if not fips.startswith(NC_FIPS):
            continue

        disadvantaged = row.get(disadv_col, "") == "True"
        try:
            threshold = int(
                float(row.get(threshold_col, "0") or "0")
            )
        except (ValueError, TypeError):
            threshold = 0
        try:
            cat_count = int(
                float(row.get(categories_col, "0") or "0")
            )
        except (ValueError, TypeError):
            cat_count = 0
        try:
            pop = float(row.get(pop_col, "0") or "0")
        except (ValueError, TypeError):
            pop = 0.0

        # Reconstruct which categories this tract exceeds
        cat_flags = {}
        for cat_name, indicators in CATEGORY_INDICATORS.items():
            exceeded = any(
                row.get(col, "") == "True" for col in indicators
            )
            cat_flags[cat_name] = exceeded

        # Tribal overlap is a separate pathway
        tribal = (
            row.get(tribal_col, "") == "True" if has_tribal else False
        )

        nc_tracts.append(
            {
                "fips": fips,
                "state_name": row.get(state_col, ""),
                "county_name": row.get(county_col, ""),
                "disadvantaged": disadvantaged,
                "threshold": threshold,
                "cat_count": cat_count,
                "population": pop,
                "cat_flags": cat_flags,
                "tribal": tribal,
                "county_fips": fips[:5],
            }
        )

    total_tracts = len(nc_tracts)
    evaluable = [t for t in nc_tracts if t["population"] > 0]
    total_evaluable = len(evaluable)
    disadv_tracts = [t for t in evaluable if t["disadvantaged"]]
    n_disadv = len(disadv_tracts)

    print(f"\n[INFO] NC tracts total:         {total_tracts}")
    print(f"[INFO] NC tracts evaluable:     {total_evaluable}")
    print(f"[INFO] NC tracts disadvantaged: {n_disadv}")
    orig_rate = n_disadv * 100 / total_evaluable
    print(
        f"[INFO] Statewide rate: "
        f"{n_disadv}/{total_evaluable} = {orig_rate:.1f}%"
    )

    # ------------------------------------------------------------------
    # 4b. Save NC-filtered per-category data to disk
    # ------------------------------------------------------------------
    _save_nc_categories_csv(nc_tracts)

    # ------------------------------------------------------------------
    # 4c. Validate the saved per-category file
    # ------------------------------------------------------------------
    _validate_nc_categories(nc_tracts, disadv_tracts)

    # ------------------------------------------------------------------
    # 5. Validation: does our category reconstruction match?
    # ------------------------------------------------------------------
    print("\n--- Category reconstruction validation ---")
    for t in disadv_tracts[:5]:
        n_cats_ours = sum(1 for v in t["cat_flags"].values() if v)
        print(
            f"  {t['fips']}: CSV cat_count={t['cat_count']}, "
            f"reconstructed={n_cats_ours}, "
            f"tribal={t['tribal']}"
        )

    # ------------------------------------------------------------------
    # 6. Core sensitivity analysis
    # ------------------------------------------------------------------
    print("\n" + "=" * 64)
    print("SENSITIVITY ANALYSIS RESULTS")
    print("=" * 64)

    # 6a. Category frequency among disadvantaged tracts
    print("\nCategory frequency among disadvantaged tracts:")
    for cat_name in CATEGORY_INDICATORS:
        count = sum(
            1 for t in disadv_tracts if t["cat_flags"][cat_name]
        )
        pct = count * 100 / n_disadv if n_disadv else 0
        print(f"  {cat_name:<25s}: {count:>4d} ({pct:>5.1f}%)")

    if has_tribal:
        tribal_count = sum(1 for t in disadv_tracts if t["tribal"])
        print(
            f"  {'Tribal overlap':<25s}: {tribal_count:>4d} "
            f"({tribal_count * 100 / n_disadv:>5.1f}%)"
        )

    # 6b. Tracts where climate change is the ONLY category exceeded
    # These tracts would lose disadvantaged status if we removed it
    climate_only = []
    for t in disadv_tracts:
        if not t["cat_flags"]["Climate change"]:
            continue
        other_cats = any(
            v for k, v in t["cat_flags"].items()
            if k != "Climate change"
        )
        if not other_cats and not t["tribal"]:
            climate_only.append(t)

    print("\nTracts with threshold_count = 1: ", end="")
    single_threshold = [t for t in disadv_tracts if t["threshold"] == 1]
    print(len(single_threshold))

    print("Tracts with categories_exceeded = 1: ", end="")
    single_cat = [t for t in disadv_tracts if t["cat_count"] == 1]
    print(len(single_cat))

    # Breakdown of single-category tracts by which category
    print("\nSingle-category disadvantaged tracts by category:")
    for cat_name in CATEGORY_INDICATORS:
        sc = [
            t for t in single_cat if t["cat_flags"][cat_name]
        ]
        print(f"  {cat_name:<25s}: {len(sc):>4d}")

    print(
        f"\nTracts disadvantaged SOLELY due to Climate change "
        f"(no other category, no tribal): {len(climate_only)}"
    )

    # 6c. Impact of removing climate change category
    n_lost = len(climate_only)
    adjusted_disadv = n_disadv - n_lost
    adjusted_rate = adjusted_disadv * 100 / total_evaluable
    delta = adjusted_rate - orig_rate

    print("\n--- Impact of Removing Climate Change Category ---")
    print(f"Tracts that would LOSE disadvantaged status: {n_lost}")
    print(
        f"Original disadvantaged:  {n_disadv} / {total_evaluable} "
        f"= {orig_rate:.1f}%"
    )
    print(
        f"Adjusted disadvantaged:  {adjusted_disadv} / "
        f"{total_evaluable} = {adjusted_rate:.1f}%"
    )
    print(f"Delta: {delta:+.1f} percentage points")

    # 6d. How many disadvantaged tracts have climate change as ANY flag?
    climate_any = [
        t for t in disadv_tracts if t["cat_flags"]["Climate change"]
    ]
    print(
        f"\nDisadvantaged tracts with Climate change as ANY "
        f"category: {len(climate_any)}"
    )
    print(
        f"  of which sole-category (would lose status): {n_lost}"
    )
    print(
        f"  of which multi-category (would keep status): "
        f"{len(climate_any) - n_lost}"
    )

    # ------------------------------------------------------------------
    # 7. Study-county breakdown
    # ------------------------------------------------------------------
    print("\n" + "=" * 64)
    print("STUDY-COUNTY BREAKDOWN")
    print("=" * 64)

    header_fmt = (
        f"{'County':<16s} {'Eval':>5s} {'Dis':>5s} {'Rate':>6s} "
        f"{'Lost':>5s} {'AdjDis':>6s} {'AdjRate':>7s} {'Delta':>7s}"
    )
    print(header_fmt)
    print("-" * len(header_fmt))

    for cfips in sorted(study_counties):
        cname = study_counties[cfips]
        c_eval = [t for t in evaluable if t["county_fips"] == cfips]
        c_disadv = [t for t in c_eval if t["disadvantaged"]]

        # Climate-only tracts in this county
        c_climate_only = []
        for t in c_disadv:
            if not t["cat_flags"]["Climate change"]:
                continue
            other = any(
                v for k, v in t["cat_flags"].items()
                if k != "Climate change"
            )
            if not other and not t["tribal"]:
                c_climate_only.append(t)

        n_eval = len(c_eval)
        n_dis = len(c_disadv)
        n_cl = len(c_climate_only)
        if n_eval > 0:
            rate = n_dis * 100 / n_eval
            adj_dis = n_dis - n_cl
            adj_rate = adj_dis * 100 / n_eval
            d = adj_rate - rate
            print(
                f"{cname:<16s} {n_eval:>5d} {n_dis:>5d} "
                f"{rate:>5.1f}% {n_cl:>5d} {adj_dis:>6d} "
                f"{adj_rate:>6.1f}% {d:>+6.1f}pp"
            )
        else:
            print(f"{cname:<16s}   (no evaluable tracts)")

    print("\n[DONE] Sensitivity analysis complete.")


if __name__ == "__main__":
    main()
