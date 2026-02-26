# Data Sources & References

> **See also:** [data/README.md](../data/README.md) for data directory overview | [data/processed/DATA-DICTIONARY.md](../data/processed/DATA-DICTIONARY.md) for detailed field definitions

## Primary Data Sources

### 1. North Carolina Electric Vehicle Registrations
- **Source:** North Carolina Department of Transportation (NCDOT)
- **Dataset:** ncdot-ev-phev-registrations-county-201809-202506.csv
- **Monthly Files URL:** https://www.ncdot.gov/initiatives-policies/environmental/climate-change/Documents/{year}-{month}-registration-data.xlsx
- **Coverage:** September 2018 - June 2025 (82 months)
- **Granularity:** County-month panel data (100 counties × 82 months = 8,200 observations)
- **Download Script:** `code/python/data-acquisition/ncdot_ev_pipeline.py`

### 2. Alternative Fuel Stations - Electric Vehicle Charging
- **Source:** U.S. Department of Energy, Alternative Fuels Data Center (AFDC)
- **API:** NREL Alternative Fuel Station Locator (`https://developer.nrel.gov/api/alt-fuel-stations/v1.json`)
- **Snapshots:**
  - `afdc-charging-stations-connector-2024-07.csv` — July 2024 (1,725 stations, 74 fields)
  - `afdc-charging-stations-connector-2026-02.csv` — Feb 2026 (1,985 stations, 74 fields)
- **Download Script:** `code/python/data-acquisition/afdc_api_download.py`
- **Coverage:** NC operational electric stations (Level 1, Level 2, DCFC)
- **Feb 2026 Stats:** 4,363 L2 EVSE + 1,747 DCFC + 35 L1 = 6,145 total connectors across 267 cities

## Supporting Research

- Anyer et al. - EV adoption modeling methodologies
- McKinsey & Company - Public EV charging station profitability analysis
- NREL - 2030 National Charging Network projections
- NEVI Formula Program guidelines - Federal infrastructure funding

## Reference Materials

- Reference analytics papers and case studies
- Industry research and best practices
