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

### ncdot-monthly/
- **Source:** NCDOT Climate Change Documents
- **URL:** https://www.ncdot.gov/initiatives-policies/environmental/climate-change/Pages/zev-registration-data.aspx
- **Description:** Monthly ZEV registration Excel files by county
- **Files:** `{year}-{month}-registration-data.xlsx`
- **Download Script:** `code/python/data-acquisition/ncdot_ev_pipeline.py`
- **Current Files:** July - October 2025 (4 validation-period files)

**Important:** Raw files should NEVER be modified. All transformations happen via processing scripts.

---

## Processed Data (`processed/`)

### nc-ev-registrations-2025.csv
- **Description:** Consolidated monthly EV registration counts by NC county for 2025
- **Created By:** `code/python/data-acquisition/ncdot_ev_pipeline.py`
- **Created:** 2026-02-01
- **Rows:** 1,000 (100 counties × 10 months)
- **Period:** January - October 2025

### nc-ev-registrations-2025.xlsx
- **Description:** Excel version of the above for convenience
- **Same structure as CSV**

### nc-ev-registrations-2025.qa.txt
- **Description:** Quality assurance summary report
- **Contents:** County coverage, missing value rates, statewide totals

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

| Dataset | Source | Script | Last Updated |
|---------|--------|--------|--------------|
| ncdot-monthly/*.xlsx (Jul-Oct) | NCDOT website | ncdot_ev_pipeline.py | 2026-02-01 |
| nc-ev-registrations-2025.csv | ncdot-monthly/ | ncdot_ev_pipeline.py | 2026-02-01 |
| sas-forecasts.csv | SAS Model Studio | Manual export | 2025-06 |
| sas-model-info.csv | SAS Model Studio | Manual export | 2025-06 |

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
