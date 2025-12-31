# Data Sources & References

## Primary Data Sources

### 1. North Carolina Electric Vehicle Registrations
- **Source:** North Carolina Department of Transportation (NCDOT)
- **Dataset:** NC_EV_PHEV_TS.csv
- **Monthly Files URL:** https://www.ncdot.gov/initiatives-policies/environmental/climate-change/Documents/{year}-{month}-registration-data.xlsx
- **Coverage:** September 2018 - June 2025 (82 months)
- **Granularity:** County-month panel data (100 counties × 82 months = 8,200 observations)
- **Download Script:** `code/python/data-acquisition/ncdot_zev_downloader.py`

### 2. Alternative Fuel Stations - Electric Vehicle Charging
- **Source:** U.S. Department of Energy, Alternative Fuels Data Center (AFDC)
- **Dataset:** alt_fuel_stations_ev_charging_units.csv
- **URL:** https://afdc.energy.gov/stations
- **Coverage:** 355 stations, 1,725 connector records
- **Updated:** 2025

## Supporting Research

- Anyer et al. - EV adoption modeling methodologies
- McKinsey & Company - Public EV charging station profitability analysis
- NREL - 2030 National Charging Network projections
- NEVI Formula Program guidelines - Federal infrastructure funding

## Competition Materials

- SAS Curiosity Cup 2026 Final Competition Guidelines
- Reference papers from 2025 winning teams:
  - Team DataMind (social media analysis)
  - Machine Learning Dynamite (breast cancer detection)
  - Team Data ACES (Alzheimer's prediction)
