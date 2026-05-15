#!/usr/bin/env python3
"""
LEHD LODES & ACS Income/Tenure Download - EV Pulse NC
======================================================
Downloads LEHD LODES commuter-flow data and ACS income/tenure
estimates for Phase 4 workplace-charging demand analysis.

Data sources:
  1. LODES OD Main (origin-destination commuter flows)
  2. LODES WAC (workplace area characteristics)
  3. LODES Geographic Crosswalk (block-to-county mapping)
  4. ACS B19001 (income distribution) + B25003 (tenure) by tract

Usage:
    uv run code/python/data-acquisition/lehd_lodes_download.py

Requires:
    - requests library

Output:
    data/raw/lehd-nc-od-main-2021.csv.gz
    data/raw/lehd-nc-wac-2021.csv.gz
    data/raw/lehd-nc-xwalk.csv.gz
    data/raw/acs-nc-income-tenure-tracts.csv

Author: Wolfgang Sanyer
License: Polyform Noncommercial 1.0.0 (see LICENSE)
"""

import csv
import gzip
import io
import os
import sys
from datetime import datetime

import requests

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO_ROOT = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
RAW_DIR = os.path.join(REPO_ROOT, "data", "raw")

# ---------------------------------------------------------------------------
# LEHD LODES URLs  (LODES 8, NC, 2021, all job types)
# ---------------------------------------------------------------------------
LODES_FILES = {
    "od": {
        "url": "https://lehd.ces.census.gov/data/lodes/LODES8/nc/od/nc_od_main_JT00_2021.csv.gz",
        "dest": "lehd-nc-od-main-2021.csv.gz",
        "label": "LODES OD Main (origin-destination)",
    },
    "wac": {
        "url": "https://lehd.ces.census.gov/data/lodes/LODES8/nc/wac/nc_wac_S000_JT00_2021.csv.gz",
        "dest": "lehd-nc-wac-2021.csv.gz",
        "label": "LODES WAC (workplace area characteristics)",
    },
    "xwalk": {
        "url": "https://lehd.ces.census.gov/data/lodes/LODES8/nc/nc_xwalk.csv.gz",
        "dest": "lehd-nc-xwalk.csv.gz",
        "label": "LODES Geographic Crosswalk",
    },
}

# ---------------------------------------------------------------------------
# ACS API
# ---------------------------------------------------------------------------
ACS_API_URL = "https://api.census.gov/data/2022/acs/acs5"
ACS_OUTPUT = "acs-nc-income-tenure-tracts.csv"

# Income distribution variables (B19001)
INCOME_VARS = [
    "B19001_001E",  # Total households
    "B19001_013E",  # $75,000-$99,999
    "B19001_014E",  # $100,000-$124,999
    "B19001_015E",  # $125,000-$149,999
    "B19001_016E",  # $150,000-$199,999
    "B19001_017E",  # $200,000 or more
]

# Housing tenure variables (B25003)
TENURE_VARS = [
    "B25003_001E",  # Total occupied units
    "B25003_002E",  # Owner occupied
    "B25003_003E",  # Renter occupied
]


# ---------------------------------------------------------------------------
# Download helpers
# ---------------------------------------------------------------------------
def download_gz_file(url, dest_path, label):
    """Stream-download a gzipped file with progress reporting."""
    print(f"\n[INFO] Downloading {label}...")
    print(f"[INFO] URL: {url}")

    try:
        resp = requests.get(url, stream=True, timeout=300)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"[ERROR] Failed to download {label}: {e}")
        return False

    total = int(resp.headers.get("content-length", 0))
    downloaded = 0
    chunk_size = 1024 * 256  # 256 KB chunks

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "wb") as f:
        for chunk in resp.iter_content(chunk_size=chunk_size):
            f.write(chunk)
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

    size_mb = os.path.getsize(dest_path) / (1024 * 1024)
    print(f"\n[SUCCESS] Saved {dest_path} ({size_mb:.1f} MB)")
    return True


def peek_gz_csv(path, required_cols=None):
    """Read a gzipped CSV, verify columns, return row count."""
    with gzip.open(path, "rt", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        row_count = sum(1 for _ in reader)

    print(f"[INFO]   Columns ({len(header)}): {header[:10]}{'...' if len(header) > 10 else ''}")
    print(f"[INFO]   Row count: {row_count:,}")

    if required_cols:
        missing = [c for c in required_cols if c not in header]
        if missing:
            print(f"[WARNING] Missing expected columns: {missing}")
        else:
            print(
                f"[INFO]   Required columns verified: {required_cols}"
            )

    return header, row_count


# ---------------------------------------------------------------------------
# ACS download
# ---------------------------------------------------------------------------
def download_acs_tracts():
    """Download ACS income + tenure data for NC tracts."""
    print("\n[INFO] Downloading ACS income & tenure data for NC tracts...")
    print(f"[INFO] Endpoint: {ACS_API_URL}")

    all_vars = INCOME_VARS + TENURE_VARS
    var_string = ",".join(all_vars)

    params = {
        "get": f"NAME,{var_string}",
        "for": "tract:*",
        "in": "state:37",
    }

    print(f"[INFO] Variables: {var_string}")
    print("[INFO] Geography: tract:* in state:37 (NC)")

    try:
        resp = requests.get(ACS_API_URL, params=params, timeout=60)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"[ERROR] ACS API request failed: {e}")
        # Try again with an empty key parameter
        print("[INFO] Retrying with key parameter...")
        params["key"] = ""
        try:
            resp = requests.get(ACS_API_URL, params=params, timeout=60)
            resp.raise_for_status()
        except requests.RequestException as e2:
            print(f"[ERROR] ACS API retry also failed: {e2}")
            return None, None

    data = resp.json()
    headers = data[0]
    rows = data[1:]

    print(f"[INFO] API returned {len(rows)} tracts")

    if not rows:
        print("[ERROR] No tract data returned from ACS API.")
        return None, None

    return headers, rows


def save_acs_csv(headers, rows, output_path):
    """Write ACS data to CSV."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

    size_kb = os.path.getsize(output_path) / 1024
    print(f"[SUCCESS] Saved {len(rows)} tracts to {output_path} ({size_kb:.0f} KB)")


# ---------------------------------------------------------------------------
# Sanity checks
# ---------------------------------------------------------------------------
def sanity_check_lodes():
    """Verify LODES downloads."""
    print("\n" + "=" * 60)
    print("Sanity Checks - LODES Files")
    print("=" * 60)

    # OD Main
    od_path = os.path.join(RAW_DIR, LODES_FILES["od"]["dest"])
    if os.path.exists(od_path):
        print(f"\n--- {LODES_FILES['od']['label']} ---")
        peek_gz_csv(
            od_path,
            required_cols=[
                "w_geocode",
                "h_geocode",
                "S000",
                "SE01",
                "SE02",
                "SE03",
            ],
        )
    else:
        print(f"[WARNING] OD file not found: {od_path}")

    # WAC
    wac_path = os.path.join(RAW_DIR, LODES_FILES["wac"]["dest"])
    if os.path.exists(wac_path):
        print(f"\n--- {LODES_FILES['wac']['label']} ---")
        peek_gz_csv(
            wac_path,
            required_cols=["CE01", "CE02", "CE03"],
        )
    else:
        print(f"[WARNING] WAC file not found: {wac_path}")

    # Crosswalk
    xwalk_path = os.path.join(RAW_DIR, LODES_FILES["xwalk"]["dest"])
    if os.path.exists(xwalk_path):
        print(f"\n--- {LODES_FILES['xwalk']['label']} ---")
        peek_gz_csv(xwalk_path, required_cols=["cty"])
    else:
        print(f"[WARNING] Crosswalk file not found: {xwalk_path}")


def sanity_check_acs(headers, rows):
    """Verify ACS download."""
    print("\n" + "=" * 60)
    print("Sanity Checks - ACS Income & Tenure")
    print("=" * 60)

    if headers is None or rows is None:
        print("[WARNING] ACS data not available for sanity check.")
        return

    print(f"[INFO] Tract count: {len(rows)}")
    print(f"[INFO] Columns: {headers}")

    # Check income bins present
    for v in INCOME_VARS:
        if v in headers:
            print(f"[INFO]   {v} present")
        else:
            print(f"[WARNING] {v} missing from ACS data")

    # Check tenure vars present
    for v in TENURE_VARS:
        if v in headers:
            print(f"[INFO]   {v} present")
        else:
            print(f"[WARNING] {v} missing from ACS data")


def print_file_sizes():
    """Print file sizes for all downloads."""
    print("\n" + "=" * 60)
    print("File Sizes Summary")
    print("=" * 60)

    files = [
        LODES_FILES["od"]["dest"],
        LODES_FILES["wac"]["dest"],
        LODES_FILES["xwalk"]["dest"],
        ACS_OUTPUT,
    ]

    for fname in files:
        fpath = os.path.join(RAW_DIR, fname)
        if os.path.exists(fpath):
            size = os.path.getsize(fpath)
            if size > 1024 * 1024:
                print(f"  {fname}: {size / (1024 * 1024):.1f} MB")
            else:
                print(f"  {fname}: {size / 1024:.0f} KB")
        else:
            print(f"  {fname}: NOT FOUND")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print("=" * 60)
    print("LEHD LODES & ACS Download - EV Pulse NC (Phase 4)")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)

    # ------------------------------------------------------------------
    # 1-3. Download LODES files (gz)
    # ------------------------------------------------------------------
    for key in ("od", "wac", "xwalk"):
        info = LODES_FILES[key]
        dest = os.path.join(RAW_DIR, info["dest"])
        ok = download_gz_file(info["url"], dest, info["label"])
        if not ok:
            print(f"[ERROR] Could not download {info['label']}. Continuing...")

    # ------------------------------------------------------------------
    # 4. Download ACS income + tenure
    # ------------------------------------------------------------------
    acs_headers, acs_rows = download_acs_tracts()
    if acs_headers and acs_rows:
        acs_path = os.path.join(RAW_DIR, ACS_OUTPUT)
        save_acs_csv(acs_headers, acs_rows, acs_path)

    # ------------------------------------------------------------------
    # Sanity checks
    # ------------------------------------------------------------------
    sanity_check_lodes()
    sanity_check_acs(acs_headers, acs_rows)
    print_file_sizes()

    print("\n[DONE] All downloads complete.")


if __name__ == "__main__":
    main()
