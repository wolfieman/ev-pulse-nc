# Code Directory

## SAS Scripts (`sas/`)

Execute in numerical order:

### 01-data-import/
Data import scripts (.ctl files) for loading datasets into SAS libraries

**TODO:** Export your SAS import scripts here
- `alt-fuel-stations-import.ctl`
- `ev_charging_units-import.ctl`
- `nc_ev_phev_ts-import.ctl`

### 02-data-prep/
Data cleaning, validation, and transformation

- `nc-regs/` - BEV registration data processing
- `supply/` - Charging infrastructure processing
- `shapefiles/` - Geographic data handling (if used)

**TODO:** Export your data prep .sas scripts here

### 03-eda/
Exploratory data analysis scripts

**TODO:** Export your EDA .sas scripts here

### 04-forecasting/
Time series forecasting models (ARIMA, Exponential Smoothing)

**TODO:** Export your forecasting .sas scripts here

### 05-gap-analysis/
Diagnostic gap metrics and county classification

**TODO:** Export your gap analysis .sas scripts here

### 06-visualization/
Chart and map generation code

**TODO:** Export your visualization .sas scripts here

## Python Scripts (`python/`)

Utility scripts for data acquisition and preprocessing.

### data-acquisition/

**ncdot_zev_downloader.py** - Downloads monthly ZEV registration data from NCDOT

```bash
# Download a range of months
python ncdot_zev_downloader.py --start 2025-07 --end 2025-10 --outdir ../../../data/raw/ncdot-monthly

# Download specific months
python ncdot_zev_downloader.py --months 2025-07 2025-08 2025-09
```

**Dependencies:** `requests`, `openpyxl` (optional, for Excel validation)

### data-cleaning/

**consolidate_zev_monthly.py** - Consolidates monthly Excel files into a single dataset

```bash
# Consolidate all files in a directory
python consolidate_zev_monthly.py --indir ../../../data/raw/ncdot-monthly --out ../../../data/processed/nc_zev_consolidated.xlsx
```

**Dependencies:** `pandas`, `openpyxl`
