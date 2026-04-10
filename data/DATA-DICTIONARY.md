# Data Dictionary — EV Pulse NC

**Project:** EV Pulse NC — EV Infrastructure Gap Analysis for North Carolina
**Last Updated:** 2026-04-10
**Scope:** All datasets actively used in the analytical pipeline (Phases 1-5)

This document defines the project-used columns for each dataset. For full API schemas (e.g., the complete 76-column AFDC structure), see `frameworks/afdc-data-structure.md`. For file locations and provenance, see `data/README.md` and `references/data-sources.md`.

---

## 1. NCDOT EV Registrations

**File:** `data/raw/ncdot-ev-phev-registrations-county-201809-202506.csv`
**Source:** North Carolina Department of Transportation (NCDOT)
**Granularity:** One row per county per month
**Rows:** 8,200 (100 counties x 82 months)
**Period:** September 2018 - June 2025
**Pipeline:** `code/python/data-acquisition/ncdot_ev_pipeline.py`

| Variable | Type | Description | Valid Values / Range |
|----------|------|-------------|---------------------|
| `County` | string | NC county name (title-cased) | 100 NC counties, e.g., "Wake", "McDowell" |
| `BEV` | integer | Cumulative battery-electric vehicle registrations | >= 0 (range: 0 - 28,098) |
| `PHEV` | integer | Cumulative plug-in hybrid registrations | >= 0 |
| `Hybrid` | integer | Traditional hybrid registrations | >= 0 |
| `AllHybrids` | integer | PHEV + Hybrid combined | >= 0 |
| `Gas` | integer | Gasoline vehicle registrations | >= 0 |
| `Diesel` | integer | Diesel vehicle registrations | >= 0 |
| `Date` | date | First day of month (YYYY-MM-DD) | 2018-09-01 to 2025-06-01 |
| `TotalEV` | integer | BEV + PHEV | Derived |
| `EV_Share` | float | TotalEV / (TotalEV + Gas + Diesel) | 0.0 - 1.0 (typically 0.01 - 0.05) |
| `Methodology_PostMay2025` | boolean | NCDOT methodology change flag: post-May 2025, NCDOT eliminated duplicate records and excluded vehicles with plates removed from circulation | True if Date >= 2025-05-01 |

**Missing values:** 0.0% across all variables. 162 legitimate zeros (early-period rural counties with no BEV registrations).

**QA artifact:** `data/processed/nc-ev-registrations-2025.qa.txt`

### 2025 Processed Slice

**File:** `data/processed/nc-ev-registrations-2025.csv`
**Rows:** 1,000 (100 counties x 10 months, Jan-Oct 2025)
**Purpose:** Holdout validation period. Same schema as above, restricted to 2025.

---

## 2. NREL AFDC Charging Infrastructure

**File:** `data/raw/afdc-charging-stations-connector-2026-02.csv`
**Source:** U.S. Department of Energy / NREL Alternative Fuels Data Center API
**Granularity:** One row per station
**Rows:** 1,985 stations (6,145 total connectors)
**Pull Date:** February 2026
**Full schema:** `frameworks/afdc-data-structure.md` (76 columns)

**Project-used columns:**

| Variable | Type | Description | Valid Values / Range |
|----------|------|-------------|---------------------|
| `id` | integer | AFDC station unique identifier | Positive integer |
| `station_name` | string | Station name | Free text |
| `city` | string | City name | NC cities |
| `state` | string | State abbreviation | "NC" after filtering |
| `zip` | string | 5-digit ZIP code (zero-padded) | "00000" - "99999" |
| `street_address` | string | Street address | Free text |
| `latitude` | float | Station latitude | 33.8 - 36.6 (NC bounds) |
| `longitude` | float | Station longitude | -84.3 - -75.5 (NC bounds) |
| `access_code` | string | Public or private access | "public", "private" |
| `facility_type` | string | Facility type | Various |
| `ev_network` | string | Charging network operator | "Tesla", "ChargePoint", etc. |
| `ev_level1_evse_num` | integer | Level 1 EVSE port count | >= 0 (NaN filled with 0) |
| `ev_level2_evse_num` | integer | Level 2 EVSE port count | >= 0 (NaN filled with 0) |
| `ev_dc_fast_num` | integer | DC Fast Charging port count | >= 0 (NaN filled with 0) |
| `status_code` | string | Station operational status | "E" (open), "P" (planned), "T" (temp closed) |
| `open_date` | date | Date station opened | Partial coverage (~40%+) |
| `date_last_confirmed` | date | Last confirmation date | Date |

**Missing values:** Port count columns have NaN filled with 0 at load time. `open_date` has significant missing values (threshold checked in EDA). ZIP codes zero-padded from raw.

**Filtering:** 2 non-NC stations removed by ZIP filter (ZIPs "20020", "39817") in `phase3_zip_mapping.py`. Post-filter: 1,983 NC stations.

**QA artifacts:** `data/processed/afdc-eda-quality-flags.csv` (682 flagged stations), `afdc-eda-column-profile.csv`, `afdc-unmatched-zips.csv`

### Historical Snapshot (Reference Only)

**File:** `data/raw/afdc-charging-stations-connector-2024-07.csv`
**Rows:** 1,725 (DCFC-only, public-only connector-level extract)
**Purpose:** Retained for dual-snapshot comparison only. Not used in scoring.

---

## 3. SAS Model Studio Forecasts

**Directory:** `data/reference-forecasts/`
**Source:** SAS Model Studio (auto-selected per county from ESM, ARIMA, UCM)
**Purpose:** County-level BEV forecasts used in Phase 1 validation and Phase 5 utilization scoring

### sas-forecasts.csv

**Rows:** 9,400 (100 counties x 94 months)
**Period:** September 2018 - June 2026 (82 months training + 12 months forecast)

| Variable | Type | Description | Valid Values / Range |
|----------|------|-------------|---------------------|
| `County` | string | NC county name | 100 NC counties |
| `MonthDate` | string | Month in "Mon YYYY" format | "Sep 2018" - "Jun 2026" |
| `ACTUAL` | float | Historical actual BEV count | >= 0 (NaN for forecast period) |
| `PREDICT` | float | Model prediction | >= 0 |
| `LOWER` | float | 95% confidence interval lower bound | >= 0 |
| `UPPER` | float | 95% confidence interval upper bound | >= PREDICT |
| `_NAME_` | string | Variable name | "Electric" (= BEV) |

### sas-model-info.csv

**Rows:** 100 (one per county)

| Variable | Type | Description | Valid Values |
|----------|------|-------------|-------------|
| `County` | string | NC county name | 100 NC counties |
| `_MODELTYPE_` | string | Model family | "ESM" (82), "ARIMA" (13), "UCM" (5) |
| `_MODEL_` | string | Specific model variant | Model-specific |

### sas-fit-statistics.csv

**Rows:** 100 (one per county)
**Key columns:** County, MAPE, RMSE, AIC, and other fit metrics.

---

## 4. LEHD LODES (Workplace Commuting)

**Source:** U.S. Census Bureau / Center for Economic Studies
**Vintage:** LODES8, 2021 (most recent public release)
**Purpose:** Workplace charging demand estimation (Phase 4)
**Caveat:** LODES data is noise-infused to protect confidentiality. Treated as published; no re-identification attempted.

### lehd-nc-od-main-2021.csv.gz (Origin-Destination)

**File:** `data/raw/lehd-nc-od-main-2021.csv.gz`
**Granularity:** One row per home-block to work-block commuter flow
**Rows:** 3,768,428 intra-NC flow records

| Variable | Type | Description | Valid Values |
|----------|------|-------------|-------------|
| `w_geocode` | string (15-digit) | Workplace Census block FIPS | NC block codes |
| `h_geocode` | string (15-digit) | Home Census block FIPS | NC block codes |
| `S000` | integer | Total primary jobs | >= 0 |
| `SE01` | integer | Jobs paying $1,250/month or less | >= 0 |
| `SE02` | integer | Jobs paying $1,251-$3,333/month | >= 0 |
| `SE03` | integer | Jobs paying > $3,333/month (> $40k/yr) | >= 0 |

**Validation:** Zero nulls, zero duplicate block pairs. Additive decomposition verified: SE01 + SE02 + SE03 = S000.

### lehd-nc-wac-2021.csv.gz (Workplace Area Characteristics)

**File:** `data/raw/lehd-nc-wac-2021.csv.gz`
**Granularity:** One row per workplace Census block
**Rows:** 71,921 workplace blocks

| Variable | Type | Description | Valid Values |
|----------|------|-------------|-------------|
| `w_geocode` | string (15-digit) | Workplace Census block FIPS | NC block codes |
| `C000` | integer | Total jobs at workplace | >= 0 |
| `CE01` | integer | Jobs paying $1,250/month or less | >= 0 |
| `CE02` | integer | Jobs paying $1,251-$3,333/month | >= 0 |
| `CE03` | integer | Jobs paying > $3,333/month | >= 0 |

**Validation:** Additive decomposition verified: CE01 + CE02 + CE03 = C000.

### lehd-nc-xwalk.csv.gz (Geography Crosswalk)

**File:** `data/raw/lehd-nc-xwalk.csv.gz`
**Granularity:** One row per Census block
**Purpose:** Maps blocks to counties and tracts

| Variable | Type | Description | Valid Values |
|----------|------|-------------|-------------|
| `tabblk2020` | string (15-digit) | 2020 Census block FIPS | NC block codes |
| `st` | string (2-digit) | State FIPS | "37" (NC) |
| `cty` | string (5-digit) | County FIPS | NC county codes |
| `ctyname` | string | County name | NC county names |
| `trct` | string (11-digit) | Census tract FIPS | NC tract codes |

**Validation:** 100% coverage — every OD and WAC block maps to a county. All 100 NC counties present.

---

## 5. CEJST v2.0 Justice40

**Source:** Climate and Economic Justice Screening Tool v2.0 (December 2024 federal release)
**Archive:** EDGI / Public Environmental Data Partners (`screening-tools.com`; `github.com/Public-Environmental-Data-Partners/cejst-2`). Original federal source (`screeningtool.geoplatform.gov`) offline since January 2025.
**Purpose:** Equity overlay (Phase 5) — identifies disadvantaged communities for Justice40 compliance
**Tract vintage:** 2010 Census tracts

### cejst-justice40-tracts-nc.csv (NC Only)

**File:** `data/raw/cejst-justice40-tracts-nc.csv`
**Granularity:** One row per Census tract
**Rows:** 2,195 NC tracts

| Variable | Type | Description | Valid Values |
|----------|------|-------------|-------------|
| `tract_fips` | string (11-digit) | Census tract FIPS (2010 vintage) | Starts with "37", length 11 |
| `state_name` | string | State name | "North Carolina" |
| `county_name` | string | County name | NC counties |
| `disadvantaged` | integer | Justice40 disadvantaged designation | 0 (not disadvantaged), 1 (disadvantaged) |
| `threshold_count` | integer | Number of burden thresholds exceeded | >= 0 |
| `population` | float | Tract population | >= 0.0 (25 tracts have population = 0) |

**Key stats:** 934 of 2,170 evaluable tracts (43.0%) designated disadvantaged.

**Validation:** tract_fips is unique. All values are 11-digit strings starting with "37". `disadvantaged` contains only 0 and 1.

### cejst-justice40-tracts-nc-categories.csv (Category Indicators)

**File:** `data/raw/cejst-justice40-tracts-nc-categories.csv`
**Rows:** 2,195 NC tracts
**Purpose:** Per-category burden flags for climate sensitivity analysis (Phase 5)

| Variable | Type | Description | Valid Values |
|----------|------|-------------|-------------|
| `tract_fips` | string | Census tract FIPS | Same as above |
| `state_name` | string | State name | "North Carolina" |
| `county_name` | string | County name | NC counties |
| `disadvantaged` | integer | Overall disadvantaged flag | 0 or 1 |
| `threshold_count` | integer | Burden threshold count | >= 0 |
| `population` | float | Tract population | >= 0.0 |
| `climate_change` | integer | Climate change burden flag | 0 or 1 |
| `energy` | integer | Energy burden flag | 0 or 1 |
| `transportation` | integer | Transportation burden flag | 0 or 1 |
| `housing` | integer | Housing burden flag | 0 or 1 |
| `legacy_pollution` | integer | Legacy pollution burden flag | 0 or 1 |
| `water_wastewater` | integer | Water/wastewater burden flag | 0 or 1 |
| `health` | integer | Health burden flag | 0 or 1 |
| `workforce_development` | integer | Workforce development burden flag | 0 or 1 |

### cejst-justice40-tracts-nc-border.csv (NC + Border States)

**File:** `data/raw/cejst-justice40-tracts-nc-border.csv`
**Rows:** 8,671 (NC + adjacent states)
**Purpose:** Buffer zone for spatial joins near state borders. Same schema as NC-only file.

---

## 6. Census ACS (Income, Tenure, Population)

**Source:** U.S. Census Bureau, American Community Survey 5-year estimates
**Vintage:** ACS 2018-2022 (latest available)
**Purpose:** Income thresholds for workplace EV affordability (Phase 4), population denominators (Phase 3)

### acs-nc-income-tenure-tracts.csv

**File:** `data/raw/acs-nc-income-tenure-tracts.csv`
**Granularity:** One row per Census tract
**Rows:** 2,672 NC tracts (after filtering state = "37")

| Variable | Type | Description | Valid Values |
|----------|------|-------------|-------------|
| `state` | string (2-digit) | State FIPS | "37" (NC) |
| `county` | string (3-digit) | County FIPS portion | NC counties |
| `tract` | string (6-digit) | Tract FIPS portion | NC tracts |
| `NAME` | string | Tract description | Free text |
| `B19001_001E` | integer | Total households (income universe) | >= 0 |
| `B19001_013E` | integer | Households earning $100,000-$124,999 | >= 0 |
| `B19001_014E` | integer | Households earning $125,000-$149,999 | >= 0 |
| `B19001_015E` | integer | Households earning $150,000-$199,999 | >= 0 |
| `B19001_016E` | integer | Households earning $200,000+ | >= 0 |
| `B19001_017E` | integer | (Additional income bracket) | >= 0 |

**Derived columns (computed in `phase4_workplace_charging.py`):**
- `high_income_share_75k` — Share of households earning >= $75k (sum of B19001_013E through B19001_017E / B19001_001E)
- `high_income_share_100k` — Share earning >= $100k
- `renter_share` — Renter-occupied share of housing units

**Missing value handling:** Tracts with missing income shares are filled with statewide median (line 354-367 of `phase4_workplace_charging.py`).

### nc-zip-population-acs2022.csv

**File:** `data/raw/nc-zip-population-acs2022.csv`
**Granularity:** One row per ZCTA (ZIP Code Tabulation Area)
**Rows:** 853 ZCTAs

| Variable | Type | Description | Valid Values |
|----------|------|-------------|-------------|
| `zcta` | string (5-digit) | ZIP Code Tabulation Area | Zero-padded |
| `population` | integer | Total population | >= 0 |

**Note:** ZCTAs are Census-defined geographic areas that approximate ZIP code delivery areas. They are not identical to USPS ZIP codes. 4 AFDC station ZIPs do not match any Census ZCTA (documented in `data/processed/afdc-unmatched-zips.csv`).

---

## Spatial Boundary Files

Not datasets per se, but used in spatial joins across multiple phases.

| File | Source | Vintage | Geometry | CRS |
|------|--------|---------|----------|-----|
| `nc-county-boundaries.geojson` | Census TIGER | 2020 | MultiPolygon (100 counties) | EPSG:4269 → reprojected to 32119 |
| `nc-zcta-boundaries.geojson` | Census TIGER | 2020 | MultiPolygon (ZCTAs) | EPSG:4269 → reprojected to 32119 |
| `census-tracts-2010-study-area.geojson` | Census TIGER | 2010 | MultiPolygon (tracts) | Reprojected to EPSG:32119 |

**Target CRS:** EPSG:32119 (NC State Plane, meters) used across all spatial operations.
