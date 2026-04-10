# Data Directory

**Last Updated:** 2026-04-10
**Project:** EV Pulse NC - North Carolina Electric Vehicle Analytics

**Data Dictionary:** See [`DATA-DICTIONARY.md`](DATA-DICTIONARY.md) for column definitions, types, valid ranges, and missing value policies for all 6 datasets.

---

## Directory Structure

```
data/
├── raw/                    # Immutable source downloads (NEVER edit)
│   └── ncdot-monthly/      # Monthly NCDOT Excel files
├── processed/              # Analysis-ready datasets
├── reference-forecasts/    # SAS Model Studio exports
├── generated/              # Legacy/intermediate files
├── DATA-DICTIONARY.md      # Column definitions for all datasets
└── README.md               # This file
```

---

## Raw Data (`raw/`)

**Important:** Raw files should NEVER be modified. All transformations happen via processing scripts.

### NCDOT EV Registrations

| File | Description |
|------|-------------|
| `ncdot-ev-phev-registrations-county-201809-202506.csv` | Full county-month panel (8,200 rows, Sep 2018 - Jun 2025) |
| `ncdot-monthly/*.xlsx` (4 files) | Individual monthly workbooks (Jul - Oct 2025, validation period) |

- **Source:** [NCDOT Climate Change Documents](https://www.ncdot.gov/initiatives-policies/environmental/climate-change/Pages/zev-registration-data.aspx)
- **Script:** `ncdot_ev_pipeline.py`

### NREL AFDC Charging Stations

| File | Description |
|------|-------------|
| `afdc-charging-stations-connector-2026-02.csv` | Complete station-level API download (1,985 stations, 76 columns) — **primary** |
| `afdc-charging-stations-connector-2024-07.csv` | DCFC-only, public-only extract (1,725 rows) — retained for comparison only |
| `AFDC-DATA-COMPARISON.md` | Documents differences between old and new AFDC files |

- **Source:** [NREL AFDC API](https://developer.nrel.gov/api/alt-fuel-stations/v1.json)
- **Script:** `afdc_api_download.py`

### LEHD LODES (Workplace Commuting)

| File | Description |
|------|-------------|
| `lehd-nc-od-main-2021.csv.gz` | Origin-destination commuter flows (3.77M records) |
| `lehd-nc-wac-2021.csv.gz` | Workplace area characteristics (71,921 blocks) |
| `lehd-nc-xwalk.csv.gz` | Geography crosswalk (block to county/tract) |

- **Source:** [Census LEHD](https://lehd.ces.census.gov/data/lodes/LODES8/nc/)
- **Script:** `lehd_lodes_download.py`
- **Vintage:** LODES8, 2021 (most recent public release)

### CEJST Justice40

| File | Description |
|------|-------------|
| `cejst-justice40-tracts-nc.csv` | NC tracts only (2,195 rows) |
| `cejst-justice40-tracts-nc-border.csv` | NC + border-state tracts (8,671 rows) |
| `cejst-justice40-tracts-nc-categories.csv` | Per-category burden flags (2,195 rows, 8 categories) |

- **Source:** [EDGI/PEDP community archive](https://screening-tools.com) (original federal source offline since Jan 2025)
- **Script:** `cejst_justice40_download.py`
- **Vintage:** CEJST v2.0 (December 2024 federal release)

### Census ACS

| File | Description |
|------|-------------|
| `acs-nc-income-tenure-tracts.csv` | Tract-level income and tenure (2,672 NC tracts) |
| `nc-zip-population-acs2022.csv` | ZCTA population (853 ZCTAs) |

- **Source:** [Census ACS API](https://api.census.gov) (5-year estimates, 2018-2022)
- **Script:** `census_zip_population.py`

### Spatial Boundary Files

| File | Description |
|------|-------------|
| `nc-county-boundaries.geojson` | County polygons (100 counties, 2020 TIGER) |
| `nc-zcta-boundaries.geojson` | ZCTA polygons (2020 TIGER) |
| `census-tracts-2010-study-area.geojson` | Tract polygons (2010 vintage, for CEJST alignment) |

- **Source:** Census TIGER/Line
- **Scripts:** `census_county_boundaries.py`, `census_zcta_boundaries.py`, `census_tract_boundaries_download.py`

---

## Processed Data (`processed/`)

### Phase 1 — NCDOT Registrations & Validation

| File | Description | Rows |
|------|-------------|------|
| `nc-ev-registrations-2025.csv` | Consolidated 2025 registrations (100 counties x 10 months) | 1,000 |
| `nc-ev-registrations-2025.xlsx` | Excel version of the above | 1,000 |
| `nc-ev-registrations-2025.qa.txt` | QA report: coverage, missing values, statewide totals | — |

**Created by:** `ncdot_ev_pipeline.py` (2026-02-01)

### Phase 3 — AFDC Infrastructure & ZIP Equity

| File | Description | Rows |
|------|-------------|------|
| `afdc-eda-quality-flags.csv` | Station-level quality flags from EDA | 682 |
| `afdc-eda-column-profile.csv` | Column-level profiling (dtype, missing rates) | 76 |
| `afdc-eda-stations-by-level.csv` | Station count by charging level | 3 |
| `afdc-eda-stations-by-network.csv` | Station count by network operator | ~20 |
| `afdc-eda-stations-by-zip.csv` | Station count by ZIP code | ~500 |
| `afdc-unmatched-zips.csv` | AFDC ZIPs not matching Census ZCTAs | 4 |
| `afdc-zip-match-report.csv` | Full ZIP match report (AFDC vs Census) | ~500 |
| `phase3-station-county-mapping.csv` | Station-to-county spatial join results | 1,983 |
| `phase3-urban-zip-stations.csv` | Stations in urban ZIPs (top 10 counties) | ~1,200 |
| `phase3-top10-counties.csv` | Top 10 counties by BEV count | 10 |
| `phase3-all-zips-ranked.csv` | All ZIPs ranked by port density | ~500 |
| `phase3-top20-underserved.csv` | Top 20 underserved ZIPs | 20 |
| `phase3-underserved-summary.csv` | Underserved analysis summary | — |
| `phase3-zip-density.csv` | ZIP-level charging density metrics | ~500 |
| `phase3-zip-density-summary.csv` | County-level density summary | 10 |
| `phase3-county-gini.csv` | Gini coefficients per county | 10 |
| `phase3-statewide-gini.csv` | Statewide Gini coefficient | 1 |
| `phase3-theil-decomposition.csv` | Theil index: total, between, within | 1 |
| `phase3-theil-county-contributions.csv` | Per-county Theil contributions | 10 |

**Created by:** `generate_phase3_afdc_eda.py`, `phase3_zip_mapping.py`, `phase3_zip_density.py`

### Phase 4 — Workplace Charging Demand

| File | Description | Rows |
|------|-------------|------|
| `phase4-employment-centers.csv` | Employment center analysis (all counties) | 100 |
| `phase4-cost-effectiveness.csv` | Cost-effectiveness sub-metrics (top 10) | 10 |

**Created by:** `phase4_workplace_charging.py`

### Phase 5 — CEJST Justice40 Equity Overlay

| File | Description | Rows |
|------|-------------|------|
| `phase5-zcta-justice40.csv` | ZCTA-level Justice40 percentages | ~500 |
| `phase5-county-justice40.csv` | County-level Justice40 percentages | 10 |
| `census-zcta-eda-summary.csv` | Census ZCTA EDA summary statistics | ~850 |

**Created by:** `phase5_tract_zcta_crosswalk.py`, `eda_cejst_justice40.py`, `eda_census_zip_population.py`

### Scoring Framework

| File | Description | Rows |
|------|-------------|------|
| `scoring-framework-skeleton.csv` | Scoring framework with Phase 5 placeholders | 10 |
| `scoring-framework-final.csv` | Fully populated scoring framework (top 10) | 10 |
| `scoring-weight-sensitivity.csv` | Weight sensitivity analysis results | 50 |

**Created by:** `scoring_framework_skeleton.py`, `scoring_framework_final.py`, `phase5_weight_sensitivity.py`

---

## Reference Forecasts (`reference-forecasts/`)

SAS Model Studio exports from the original forecasting study.

- `sas-forecasts.csv` — Monthly predictions with confidence intervals (9,400 rows)
- `sas-model-info.csv` — Model type per county (100 rows)
- `sas-fit-statistics.csv` — In-sample fit statistics per county

**Column definitions:** See `DATA-DICTIONARY.md` § 3.

---

## Generated Data (`generated/`)

Legacy folder containing intermediate files from earlier processing stages.
May be deprecated in future cleanup.

---

## Data Provenance

| Dataset | Source | Script | Pull Date |
|---------|--------|--------|-----------|
| ncdot-monthly/*.xlsx (Jul-Oct) | NCDOT website | ncdot_ev_pipeline.py | 2026-02-01 |
| ncdot-ev-phev-registrations-county-201809-202506.csv | NCDOT website | ncdot_ev_pipeline.py | 2026-02-01 |
| nc-ev-registrations-2025.csv | Derived from above | ncdot_ev_pipeline.py | 2026-02-01 |
| afdc-charging-stations-connector-2026-02.csv | NREL AFDC API | afdc_api_download.py | 2026-02 |
| afdc-charging-stations-connector-2024-07.csv | NREL AFDC website | Manual download | ~2025-12 |
| lehd-nc-od-main-2021.csv.gz | Census LEHD | lehd_lodes_download.py | 2026-02 |
| lehd-nc-wac-2021.csv.gz | Census LEHD | lehd_lodes_download.py | 2026-02 |
| lehd-nc-xwalk.csv.gz | Census LEHD | lehd_lodes_download.py | 2026-02 |
| cejst-justice40-tracts-nc.csv | EDGI/PEDP archive | cejst_justice40_download.py | 2026-02 |
| cejst-justice40-tracts-nc-border.csv | EDGI/PEDP archive | cejst_justice40_download.py | 2026-02 |
| cejst-justice40-tracts-nc-categories.csv | EDGI/PEDP archive | cejst_justice40_download.py | 2026-02 |
| acs-nc-income-tenure-tracts.csv | Census ACS API | Manual / census_zip_population.py | 2026-02 |
| nc-zip-population-acs2022.csv | Census ACS API | census_zip_population.py | 2026-02 |
| nc-county-boundaries.geojson | Census TIGER | census_county_boundaries.py | 2026-02 |
| nc-zcta-boundaries.geojson | Census TIGER | census_zcta_boundaries.py | 2026-02 |
| census-tracts-2010-study-area.geojson | Census TIGER | census_tract_boundaries_download.py | 2026-02 |
| sas-forecasts.csv | SAS Model Studio | Manual export | 2025-06 |
| sas-model-info.csv | SAS Model Studio | Manual export | 2025-06 |
| sas-fit-statistics.csv | SAS Model Studio | Manual export | 2025-06 |

---

## Git LFS

Large files (>100KB CSV/XLSX) are tracked via Git LFS. See `.gitattributes` for patterns.

---

## Reproducibility

Every raw dataset has a dedicated download script in `code/python/data-acquisition/`. To regenerate from source:

```bash
# 1. NCDOT EV registrations (monthly county-level)
uv run python code/python/data-acquisition/ncdot_ev_pipeline.py --years 2025

# 2. AFDC charging stations (requires NREL API key in environment)
uv run python code/python/data-acquisition/afdc_api_download.py

# 3. LEHD LODES (OD, WAC, crosswalk — NC, 2021 vintage)
uv run python code/python/data-acquisition/lehd_lodes_download.py

# 4. CEJST Justice40 tracts (from EDGI/PEDP community archive)
uv run python code/python/data-acquisition/cejst_justice40_download.py

# 5. Census ACS ZIP population
uv run python code/python/data-acquisition/census_zip_population.py

# 6. Spatial boundary files
uv run python code/python/data-acquisition/census_county_boundaries.py
uv run python code/python/data-acquisition/census_zcta_boundaries.py
uv run python code/python/data-acquisition/census_tract_boundaries_download.py

# 7. Validate SAS forecasts against actuals
uv run python code/python/analysis/validate_sas_forecasts.py
```

**Note:** SAS forecast files (`data/reference-forecasts/`) were manually exported from SAS Model Studio and are not re-downloadable via script. The raw exports are committed to the repo.
