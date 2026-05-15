#!/usr/bin/env python3
"""
Census ZIP Code Population Download - EV Pulse NC
==================================================
Downloads ZIP code (ZCTA) population estimates from the
Census Bureau American Community Survey (ACS) 5-year API.

Usage:
    py code/python/data-acquisition/census_zip_population.py

Requires:
    - Census API key in .env file (CENSUS_API_KEY=your_key)
    - requests library (pip install requests)
    - python-dotenv library (pip install python-dotenv)

Output:
    data/raw/nc-zip-population-acs2022.csv
"""

import csv
import os
import sys
from datetime import datetime

import requests
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
API_KEY = os.getenv("CENSUS_API_KEY")

if not API_KEY:
    print("[ERROR] CENSUS_API_KEY not found in .env file")
    sys.exit(1)

# Census ACS 5-Year API (2022 vintage)
API_URL = "https://api.census.gov/data/2022/acs/acs5"

# Query: total population (B01003_001E) for all ZCTAs in NC (state FIPS 37)
# NC ZIP code prefixes (27xxx and 28xxx)
NC_ZIP_PREFIXES = ("27", "28")

PARAMS = {
    "get": "NAME,B01003_001E",
    "for": "zip code tabulation area:*",
    "key": API_KEY,
}

# Output path
REPO_ROOT = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
OUTPUT_FILE = os.path.join(REPO_ROOT, "data", "raw", "nc-zip-population-acs2022.csv")


def download_population():
    """Download NC ZCTA population from Census ACS API."""
    print("[INFO] Querying Census ACS 5-Year API for NC ZIP populations...")
    print(f"[INFO] Endpoint: {API_URL}")
    print("[INFO] Variables: B01003_001E (total population)")
    print("[INFO] Geography: All US ZCTAs, filtered to NC (27xxx, 28xxx)")

    response = requests.get(API_URL, params=PARAMS, timeout=60)
    response.raise_for_status()

    data = response.json()

    # First row is headers, rest is data
    headers = data[0]
    all_rows = data[1:]

    print(f"[INFO] API returned {len(all_rows)} US ZCTAs")

    # Filter to NC ZCTAs (ZIP prefixes 27xxx, 28xxx)
    zcta_idx = headers.index("zip code tabulation area")
    rows = [r for r in all_rows if r[zcta_idx].startswith(NC_ZIP_PREFIXES)]

    print(f"[INFO] Filtered to {len(rows)} NC ZCTAs (prefixes 27xxx, 28xxx)")

    if not rows:
        print("[ERROR] No NC ZCTAs found. Check filter logic.")
        sys.exit(1)

    return headers, rows


def save_csv(headers, rows, output_path):
    """Write population data to CSV with clean column names."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Map API field names to readable names
    column_map = {
        "NAME": "name",
        "B01003_001E": "population",
        "state": "state_fips",
        "zip code tabulation area": "zcta",
    }

    clean_headers = [column_map.get(h, h) for h in headers]

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(clean_headers)
        writer.writerows(rows)

    print(f"[SUCCESS] Saved {len(rows)} ZCTAs to {output_path}")


def sanity_check(headers, rows):
    """Print summary statistics for verification."""
    print("\n--- Sanity Check ---")
    print(f"Total ZCTAs: {len(rows)}")
    print(f"Columns: {headers}")

    # Find population column index
    pop_idx = headers.index("B01003_001E")
    zcta_idx = headers.index("zip code tabulation area")
    name_idx = headers.index("NAME")

    # Parse populations
    populations = []
    for row in rows:
        try:
            pop = int(row[pop_idx])
            populations.append((row[zcta_idx], row[name_idx], pop))
        except (ValueError, TypeError):
            pass

    total_pop = sum(p[2] for p in populations)
    print(f"Total population across all ZCTAs: {total_pop:,}")

    # Top 10 by population
    top_10 = sorted(populations, key=lambda x: x[2], reverse=True)[:10]
    print("\nTop 10 ZCTAs by population:")
    for zcta, name, pop in top_10:
        print(f"  {zcta} ({name}): {pop:,}")

    # Bottom 5
    bottom_5 = sorted(populations, key=lambda x: x[2])[:5]
    print("\nBottom 5 ZCTAs by population:")
    for zcta, name, pop in bottom_5:
        print(f"  {zcta} ({name}): {pop:,}")


def main():
    print("=" * 60)
    print("Census ZIP Population Download - EV Pulse NC")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)

    headers, rows = download_population()
    save_csv(headers, rows, OUTPUT_FILE)
    sanity_check(headers, rows)

    print(f"\n[DONE] Output: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
