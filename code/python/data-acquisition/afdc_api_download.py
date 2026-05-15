#!/usr/bin/env python3
"""
AFDC API Download Script - EV Pulse NC
=======================================
Downloads current NC electric vehicle charging station data
from the NREL Alternative Fuels Station Locator API.

Usage:
    py code/python/data-acquisition/afdc_api_download.py

Requires:
    - NREL API key in .env file (NREL_API_KEY=your_key)
    - requests library (pip install requests)
    - python-dotenv library (pip install python-dotenv)

Output:
    data/raw/afdc-charging-stations-connector-YYYY-MM.csv

Author: Wolfgang Sanyer
License: Polyform Noncommercial 1.0.0 (see LICENSE)
"""

import csv
import os
import sys
from datetime import datetime

import requests
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
API_KEY = os.getenv("NREL_API_KEY")

if not API_KEY:
    print("[ERROR] NREL_API_KEY not found in .env file")
    sys.exit(1)

# AFDC API endpoint
API_URL = "https://developer.nrel.gov/api/alt-fuel-stations/v1.json"

# Query parameters: all operational electric stations in NC
PARAMS = {
    "api_key": API_KEY,
    "state": "NC",
    "fuel_type": "ELEC",
    "status": "E",
    "limit": "all",
}

# Output path
REPO_ROOT = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
DATE_STAMP = datetime.now().strftime("%Y-%m")
OUTPUT_FILE = os.path.join(
    REPO_ROOT, "data", "raw", f"afdc-charging-stations-connector-{DATE_STAMP}.csv"
)


def download_stations():
    """Download all NC electric charging stations from AFDC API."""
    print(f"[INFO] Querying AFDC API for NC electric stations...")
    print(f"[INFO] Endpoint: {API_URL}")
    print(f"[INFO] Parameters: state=NC, fuel_type=ELEC, status=E, limit=all")

    response = requests.get(API_URL, params=PARAMS, timeout=60)
    response.raise_for_status()

    data = response.json()
    stations = data.get("fuel_stations", [])
    total_results = data.get("total_results", 0)

    print(f"[INFO] API returned {total_results} stations")

    if not stations:
        print("[ERROR] No stations returned. Check API key and parameters.")
        sys.exit(1)

    return stations


def stations_to_csv(stations, output_path):
    """Write station data to CSV."""
    if not stations:
        return

    # Collect all unique keys across all stations (not all records have same fields)
    fieldnames = list(dict.fromkeys(k for s in stations for k in s.keys()))

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(stations)

    print(f"[SUCCESS] Saved {len(stations)} stations to {output_path}")


def sanity_check(stations):
    """Print summary statistics for verification."""
    print("\n--- Sanity Check ---")
    print(f"Total stations: {len(stations)}")
    print(f"Fields per station: {len(stations[0].keys()) if stations else 0}")

    # Count by level
    l2_total = sum(s.get("ev_level2_evse_num") or 0 for s in stations)
    dcfc_total = sum(s.get("ev_dc_fast_num") or 0 for s in stations)
    l1_total = sum(s.get("ev_level1_evse_num") or 0 for s in stations)
    print(f"Level 1 EVSE: {l1_total}")
    print(f"Level 2 EVSE: {l2_total}")
    print(f"DC Fast Chargers: {dcfc_total}")
    print(f"Total connectors: {l1_total + l2_total + dcfc_total}")

    # Count by network
    networks = {}
    for s in stations:
        net = s.get("ev_network") or "Unknown"
        networks[net] = networks.get(net, 0) + 1
    print("\nStations by network:")
    for net, count in sorted(networks.items(), key=lambda x: -x[1])[:10]:
        print(f"  {net}: {count}")

    # Count unique cities
    cities = set(s.get("city") for s in stations if s.get("city"))
    print(f"\nUnique cities: {len(cities)}")

    # Count unique ZIP codes
    zips = set(s.get("zip") for s in stations if s.get("zip"))
    print(f"Unique ZIP codes: {len(zips)}")


def main():
    print("=" * 60)
    print("AFDC API Download - EV Pulse NC")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)

    stations = download_stations()
    stations_to_csv(stations, OUTPUT_FILE)
    sanity_check(stations)

    print(f"\n[DONE] Output: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
