#!/usr/bin/env python3
"""
CEJST Justice40 Data Download - EV Pulse NC
============================================
Downloads the Climate & Economic Justice Screening Tool (CEJST) v2.0
tract-level data and filters to North Carolina and border states.

The original government site (screeningtool.geoplatform.gov) was taken
offline January 2025.  This script uses the community archive mirror
hosted via the PEDP (Public Environmental Data Partners) CloudFront CDN.

Usage:
    uv run code/python/data-acquisition/cejst_justice40_download.py

Requires:
    - requests library

Output:
    data/raw/cejst-justice40-tracts-nc.csv
    data/raw/cejst-justice40-tracts-nc-border.csv
"""

import csv
import io
import os
import sys
from datetime import datetime

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
NC_OUTPUT = os.path.join(RAW_DIR, "cejst-justice40-tracts-nc.csv")
BORDER_OUTPUT = os.path.join(
    RAW_DIR, "cejst-justice40-tracts-nc-border.csv"
)

# ---------------------------------------------------------------------------
# Data source URLs (try in order)
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

# ---------------------------------------------------------------------------
# FIPS codes
# ---------------------------------------------------------------------------
NC_FIPS = "37"
BORDER_FIPS = ["37", "51", "47", "13", "45"]  # NC, VA, TN, GA, SC

# ---------------------------------------------------------------------------
# Column mapping  (original CEJST name -> output name)
# ---------------------------------------------------------------------------
COLUMN_MAP = {
    "Census tract 2010 ID": "tract_fips",
    "State/Territory": "state_name",
    "County Name": "county_name",
    "Identified as disadvantaged": "disadvantaged",
    "Total threshold criteria exceeded": "threshold_count",
    "Total population": "population",
}

# ---------------------------------------------------------------------------
# Expected count ranges
# ---------------------------------------------------------------------------
US_ROWS_MIN, US_ROWS_MAX = 73_000, 75_000
NC_ROWS_MIN, NC_ROWS_MAX = 2_100, 2_300
BORDER_ROWS_MIN, BORDER_ROWS_MAX = 10_000, 15_000
NC_DISADV_PCT_MIN, NC_DISADV_PCT_MAX = 20.0, 50.0
NC_COUNTY_COUNT = 100


# ---------------------------------------------------------------------------
# Download
# ---------------------------------------------------------------------------
def download_cejst_csv():
    """Download the national CEJST CSV, trying multiple URLs.

    Returns the decoded text content on success, or calls sys.exit(1).
    """
    for url in CEJST_URLS:
        print(f"\n[INFO] Trying URL: {url}")
        try:
            resp = requests.get(url, stream=True, timeout=300)
            print(f"[INFO] HTTP status: {resp.status_code}")
            if resp.status_code != 200:
                print("[WARNING] Non-200 status, trying next URL...")
                resp.close()
                continue

            # Stream download with progress
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
                        f"\r[INFO]   {mb:.1f} MB downloaded",
                        end="",
                        flush=True,
                    )

            print()
            raw = b"".join(chunks)
            size_mb = len(raw) / (1024 * 1024)
            print(f"[SUCCESS] Downloaded {size_mb:.1f} MB from {url}")
            return raw.decode("utf-8", errors="replace"), url

        except requests.RequestException as exc:
            print(f"[WARNING] Request failed: {exc}")
            continue

    print("[ERROR] All download URLs failed.")
    sys.exit(1)


# ---------------------------------------------------------------------------
# Parse national CSV, select & rename columns
# ---------------------------------------------------------------------------
def parse_national_csv(text):
    """Parse the full CSV text and return (header, rows) with only the
    columns we need, renamed according to COLUMN_MAP.

    The disadvantaged column is converted from True/False to 1/0.
    Returns (output_header, list_of_dicts, total_us_rows).
    """
    reader = csv.DictReader(io.StringIO(text))
    original_columns = reader.fieldnames or []

    # Debug: print original column names that match our targets
    print("\n[INFO] Matching columns in source CSV:")
    col_index = {}
    for orig, out in COLUMN_MAP.items():
        if orig in original_columns:
            print(f"  '{orig}' -> '{out}'")
            col_index[orig] = out
        else:
            print(f"  [WARNING] Column '{orig}' NOT FOUND in CSV")

    missing = set(COLUMN_MAP.keys()) - set(col_index.keys())
    if missing:
        print(f"[ERROR] Missing required columns: {missing}")
        print(f"[INFO] Available columns ({len(original_columns)}):")
        for c in original_columns[:30]:
            print(f"    {c}")
        sys.exit(1)

    output_header = list(COLUMN_MAP.values())
    rows = []
    for row in reader:
        out = {}
        for orig, out_name in COLUMN_MAP.items():
            val = row.get(orig, "")
            if out_name == "disadvantaged":
                val = "1" if val == "True" else "0"
            if out_name == "tract_fips":
                # Ensure string, strip any .0 from float-like IDs
                val = str(val).split(".")[0]
            out[out_name] = val
        rows.append(out)

    total = len(rows)
    print(f"\n[INFO] Total US rows parsed: {total:,}")

    if not (US_ROWS_MIN <= total <= US_ROWS_MAX):
        print(
            f"[WARNING] Expected {US_ROWS_MIN:,}-{US_ROWS_MAX:,} "
            f"US rows, got {total:,}"
        )

    return output_header, rows, total


# ---------------------------------------------------------------------------
# Filter and save
# ---------------------------------------------------------------------------
def filter_and_save(header, rows, fips_prefixes, output_path, label):
    """Filter rows whose tract_fips starts with any of the given FIPS
    prefixes, then write to CSV. Returns the filtered row count.
    """
    prefixes = tuple(fips_prefixes)
    filtered = [r for r in rows if r["tract_fips"].startswith(prefixes)]
    count = len(filtered)
    print(f"\n[INFO] {label}: {count:,} rows")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=header)
        writer.writeheader()
        writer.writerows(filtered)

    size_kb = os.path.getsize(output_path) / 1024
    print(f"[SUCCESS] Saved {output_path} ({size_kb:.0f} KB)")

    # Verify non-empty
    if os.path.getsize(output_path) == 0:
        print(f"[ERROR] Output file is empty: {output_path}")
        sys.exit(1)

    return count


# ---------------------------------------------------------------------------
# Sanity checks
# ---------------------------------------------------------------------------
def sanity_check_nc(nc_path, nc_count):
    """Run all sanity checks on the NC output file. Returns True if all
    critical checks pass.
    """
    print("\n" + "=" * 60)
    print("Sanity Checks - NC CEJST Data")
    print("=" * 60)

    ok = True

    # --- NC row count ---
    if NC_ROWS_MIN <= nc_count <= NC_ROWS_MAX:
        print(
            f"[OK]      NC tract count: {nc_count:,} "
            f"(expected {NC_ROWS_MIN:,}-{NC_ROWS_MAX:,})"
        )
    else:
        print(
            f"[WARNING] NC tract count: {nc_count:,} "
            f"(expected {NC_ROWS_MIN:,}-{NC_ROWS_MAX:,})"
        )

    # Read back the file for detailed checks
    with open(nc_path, "r", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)

    # --- Tract FIPS length ---
    bad_fips = [r["tract_fips"] for r in rows if len(r["tract_fips"]) != 11]
    if bad_fips:
        print(
            f"[ERROR]   {len(bad_fips)} tracts with non-11-digit FIPS: "
            f"{bad_fips[:5]}"
        )
        ok = False
    else:
        print("[OK]      All tract FIPS are 11 characters")

    # --- State validation ---
    states = set(r["state_name"] for r in rows)
    if states == {"North Carolina"}:
        print("[OK]      All rows have State/Territory = North Carolina")
    else:
        print(f"[WARNING] Unexpected state values: {states}")

    # --- Null disadvantaged ---
    null_disadv = sum(
        1 for r in rows if r["disadvantaged"] not in ("0", "1")
    )
    if null_disadv == 0:
        print("[OK]      No null 'disadvantaged' values")
    elif null_disadv <= 5:
        print(
            f"[WARNING] {null_disadv} null 'disadvantaged' values "
            "(likely water-only tracts)"
        )
    else:
        print(f"[WARNING] {null_disadv} null 'disadvantaged' values")

    # --- Disadvantaged percentage ---
    total = len(rows)
    disadv_count = sum(1 for r in rows if r["disadvantaged"] == "1")
    if total > 0:
        disadv_pct = disadv_count * 100 / total
        if NC_DISADV_PCT_MIN <= disadv_pct <= NC_DISADV_PCT_MAX:
            print(
                f"[OK]      NC disadvantaged: {disadv_count:,} / "
                f"{total:,} ({disadv_pct:.1f}%)"
            )
        else:
            print(
                f"[WARNING] NC disadvantaged: {disadv_count:,} / "
                f"{total:,} ({disadv_pct:.1f}%) "
                f"(expected {NC_DISADV_PCT_MIN}-{NC_DISADV_PCT_MAX}%)"
            )

    # --- 100 NC counties ---
    county_fips_set = set(r["tract_fips"][2:5] for r in rows)
    n_counties = len(county_fips_set)
    if n_counties == NC_COUNTY_COUNT:
        print(f"[OK]      {n_counties} unique NC county FIPS codes")
    else:
        print(
            f"[WARNING] {n_counties} unique NC county FIPS codes "
            f"(expected {NC_COUNTY_COUNT})"
        )

    return ok


def sanity_check_border(border_path, border_count):
    """Lighter sanity checks on the border-states file."""
    print("\n" + "=" * 60)
    print("Sanity Checks - Border States CEJST Data")
    print("=" * 60)

    if BORDER_ROWS_MIN <= border_count <= BORDER_ROWS_MAX:
        print(
            f"[OK]      Border-states tract count: {border_count:,} "
            f"(expected {BORDER_ROWS_MIN:,}-{BORDER_ROWS_MAX:,})"
        )
    else:
        print(
            f"[WARNING] Border-states tract count: {border_count:,} "
            f"(expected {BORDER_ROWS_MIN:,}-{BORDER_ROWS_MAX:,})"
        )

    with open(border_path, "r", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)

    states = set(r["state_name"] for r in rows)
    print(f"[INFO]    States present: {sorted(states)}")

    bad_fips = [r["tract_fips"] for r in rows if len(r["tract_fips"]) != 11]
    if bad_fips:
        print(
            f"[ERROR]   {len(bad_fips)} tracts with non-11-digit FIPS"
        )
    else:
        print("[OK]      All tract FIPS are 11 characters")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print("=" * 60)
    print("CEJST Justice40 Download - EV Pulse NC (Phase 5)")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)

    # 1. Download national CSV
    text, used_url = download_cejst_csv()
    print(f"[INFO] Data retrieved from: {used_url}")

    # 2. Parse and select columns
    header, rows, us_total = parse_national_csv(text)

    # 3. Filter NC -> save
    nc_count = filter_and_save(
        header, rows, [NC_FIPS], NC_OUTPUT, "NC tracts"
    )

    # 4. Filter NC + border states -> save
    border_count = filter_and_save(
        header, rows, BORDER_FIPS, BORDER_OUTPUT, "Border-states tracts"
    )

    # 5. Sanity checks
    sanity_check_nc(NC_OUTPUT, nc_count)
    sanity_check_border(BORDER_OUTPUT, border_count)

    # 6. Summary
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"  National rows:        {us_total:,}")
    print(f"  NC tracts:            {nc_count:,}")
    print(f"  Border-states tracts: {border_count:,}")
    for path in (NC_OUTPUT, BORDER_OUTPUT):
        size_kb = os.path.getsize(path) / 1024
        print(f"  {os.path.basename(path)}: {size_kb:.0f} KB")

    print("\n[DONE] CEJST Justice40 data acquisition complete.")


if __name__ == "__main__":
    main()
