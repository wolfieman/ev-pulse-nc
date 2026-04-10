# Data Directory

**Last Updated:** 2026-02-21
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
- **Data Dictionary:** See `DATA-DICTIONARY.md`

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

To regenerate processed data from raw sources:

```bash
# Download latest NCDOT data
uv run python code/python/data-acquisition/ncdot_ev_pipeline.py --years 2025

# Run validation
uv run python code/python/analysis/validate_sas_forecasts.py
```
