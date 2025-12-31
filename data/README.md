# Data Directory

## Raw Data (`raw/`)

### NC_EV_PHEV_TS.csv (520 MB)
- **Source:** North Carolina Department of Transportation (NCDOT)
- **Description:** Monthly electric vehicle (BEV) and plug-in hybrid (PHEV) registrations
- **Structure:** 8,200 observations (100 counties × 82 months)
- **Period:** September 2018 - June 2025
- **Variables:**
  - `Month`: YYYY-MM format
  - `County`: NC county name
  - `Electric`: Battery electric vehicle count (BEV) - **PRIMARY FOCUS**
  - `PlugInHybrid`: Plug-in hybrid count (PHEV) - excluded from analysis
  - `MonthDate`: Numeric month (YYYYMM)

### alt_fuel_stations_ev_charging_units.csv (695 MB)
- **Source:** U.S. Department of Energy, Alternative Fuels Data Center (AFDC)
- **Description:** Connector-level EV charging infrastructure data
- **Structure:** 1,725 charging unit records from 355 unique stations
- **Coverage:** 135 cities across North Carolina, deployed 2011-2025
- **Key Variables:**
  - Station identification, network provider, location (lat/long)
  - Connector types: NACS (J3400), CCS (J1772COMBO), CHAdeMO, J1772
  - Power output (kW) per connector
  - Facility type, access type, operational status

### ncdot-monthly/ (downloaded via Python script)
- **Source:** NCDOT Climate Change Documents
- **Description:** Monthly ZEV registration Excel files
- **Files:** `{year}-{month}-registration-data.xlsx`
- **Download:** Use `code/python/data-acquisition/ncdot_zev_downloader.py`

## Processed Data (`processed/`)

Cleaned and transformed datasets generated from SAS processing scripts.

**Note:** Use Git LFS for all CSV files >100MB
