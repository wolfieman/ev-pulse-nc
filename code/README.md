# Code Directory

## Python Scripts (`python/`)

All analysis code is written in Python.

### data-acquisition/

Scripts for downloading and fetching data from sources.

**ncdot_zev_downloader.py** - Downloads monthly ZEV registration data from NCDOT

```bash
# Download a range of months
python ncdot_zev_downloader.py --start 2025-07 --end 2025-10 --outdir ../../../data/raw/ncdot-monthly

# Download specific months
python ncdot_zev_downloader.py --months 2025-07 2025-08 2025-09
```

**Dependencies:** `requests`, `openpyxl`

### data-cleaning/

Data cleaning, validation, and transformation scripts.

**consolidate_zev_monthly.py** - Consolidates monthly Excel files into a single dataset

```bash
# Consolidate all files in a directory
python consolidate_zev_monthly.py --indir ../../../data/raw/ncdot-monthly --out ../../../data/processed/nc_zev_consolidated.xlsx
```

**Dependencies:** `pandas`, `openpyxl`

### analysis/ (planned)

Core analysis scripts:
- Exploratory data analysis
- Descriptive statistics
- Diagnostic gap analysis
- Predictive modeling (ARIMA forecasting)
- Prescriptive recommendations

### visualization/ (planned)

Chart and map generation code.

---

## Running the Analysis

```bash
# Set up virtual environment
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install dependencies
pip install pandas statsmodels matplotlib seaborn geopandas requests openpyxl

# Run scripts
python code/python/data-cleaning/consolidate_zev_monthly.py
```
