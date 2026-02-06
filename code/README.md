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

### analysis/

Core analysis scripts for time series modeling and forecasting.

**validate_sas_forecasts.py** - Validates SAS Model Studio forecasts against actual NCDOT data

```bash
# Run validation analysis
uv run python code/python/analysis/validate_sas_forecasts.py
```

Features:
- Out-of-sample validation (Jul-Oct 2025 actuals vs. SAS predictions)
- Metrics: MAPE, MAE, RMSE, Bias, 95% CI Coverage
- Model-type stratification (ESM, ARIMA, UCM)
- Publication-quality figures (600 DPI, PDF exports)
- Outputs saved to `output/figures/`

**arima_bev_forecast.py** - Full ARIMA implementation for BEV registration forecasting

```bash
# Run with default ARIMA(1,1,1)
python arima_bev_forecast.py

# Specify custom order
python arima_bev_forecast.py --order 2 1 1

# Auto-select best order
python arima_bev_forecast.py --auto-select

# Compare with SAS AIC
python arima_bev_forecast.py --order 1 1 1 --sas-aic 1523.45
```

Features:
- Stationarity testing (ADF, KPSS)
- Model fitting with diagnostics
- Forecast generation with confidence intervals
- Holdout validation (MAPE, MAE, RMSE)
- Diagnostic plots saved to `output/arima/`

**arima_template.py** - Minimal template for SAS-to-Python ARIMA translation

Use this as a quick reference for replicating SAS PROC ARIMA in Python.

**Dependencies:** `pandas`, `numpy`, `statsmodels`, `matplotlib`, `scipy`

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
