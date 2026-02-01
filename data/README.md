# Data Directory

**Last Updated:** 2026-02-01
**Project:** EV Pulse NC - North Carolina Electric Vehicle Analytics

---

## Directory Structure

```
data/
├── raw/                    # Immutable source downloads (NEVER edit)
│   └── ncdot-monthly/      # Monthly NCDOT Excel files
├── processed/              # Analysis-ready datasets
├── reference-forecasts/    # SAS Model Studio exports
├── generated/              # Legacy/intermediate files
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
- **Current Files:** January - October 2025 (10 files)

**Important:** Raw files should NEVER be modified. All transformations happen via processing scripts.

---

## Processed Data (`processed/`)

### nc-ev-registrations-2025.csv
- **Description:** Consolidated monthly EV registration counts by NC county for 2025
- **Created By:** `code/python/data-acquisition/ncdot_ev_pipeline.py`
- **Created:** 2026-02-01
- **Rows:** 1,000 (100 counties × 10 months)
- **Period:** January - October 2025
- **Data Dictionary:** See `processed/DATA-DICTIONARY.md`

### nc-ev-registrations-2025.xlsx
- **Description:** Excel version of the above for convenience
- **Same structure as CSV**

### nc-ev-registrations-2025.qa.txt
- **Description:** Quality assurance summary report
- **Contents:** County coverage, missing value rates, statewide totals

---

## Reference Forecasts (`reference-forecasts/`)

SAS Model Studio exports from the original forecasting study.

### sas-forecasts.csv
- **Description:** Monthly predictions with confidence intervals
- **Rows:** 9,400 (100 counties × 94 months)
- **Period:** September 2018 - June 2026 (82 months training + 12 months forecast)
- **Key Columns:**
  - `County`: NC county name
  - `MonthDate`: Month in "Mon YYYY" format
  - `ACTUAL`: Historical actual values (NaN for forecast period)
  - `PREDICT`: Model prediction
  - `LOWER`, `UPPER`: 95% confidence interval bounds
  - `_NAME_`: Variable name ("Electric" = BEV)

### sas-model-info.csv
- **Description:** Model type selected by SAS Model Studio per county
- **Rows:** 100 (one per county)
- **Key Columns:**
  - `County`: NC county name
  - `_MODELTYPE_`: Model type (ESM, ARIMA, or UCM)
  - `_MODEL_`: Specific model variant

### sas-fit-statistics.csv
- **Description:** In-sample fit statistics per county
- **Key Columns:** County, MAPE, RMSE, AIC, etc.

---

## Generated Data (`generated/`)

Legacy folder containing intermediate files from earlier processing stages.
May be deprecated in future cleanup.

---

## Data Provenance

| Dataset | Source | Script | Last Updated |
|---------|--------|--------|--------------|
| ncdot-monthly/*.xlsx | NCDOT website | ncdot_ev_pipeline.py | 2026-02-01 |
| nc-ev-registrations-2025.csv | ncdot-monthly/ | ncdot_ev_pipeline.py | 2026-02-01 |
| sas-forecasts.csv | SAS Model Studio | Manual export | 2025-06-XX |
| sas-model-info.csv | SAS Model Studio | Manual export | 2025-06-XX |

---

## Git LFS

Large files (>100KB CSV/XLSX) are tracked via Git LFS. See `.gitattributes` for patterns.

---

## Reproducibility

To regenerate processed data from raw sources:

```bash
# Download latest NCDOT data
uv run python code/python/data-acquisition/ncdot_ev_pipeline.py --years 2025

# Run validation
uv run python code/python/analysis/validate_sas_forecasts.py
```
