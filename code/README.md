# Code Directory

## Directory Structure

```
code/
└── python/
    ├── data-acquisition/       # Data download scripts
    ├── data-cleaning/          # Data consolidation and transformation
    ├── analysis/               # Time series modeling and validation
    └── blog/                   # Blog graphics package
```

## Python Scripts (`python/`)

All analysis code is written in Python.

### data-acquisition/

Scripts for downloading and fetching data from sources.

**ncdot_ev_pipeline.py** - Downloads and consolidates county-level EV registration data from NCDOT

```bash
# Download all available data for 2025
python ncdot_ev_pipeline.py --years 2025

# Download a specific month range
python ncdot_ev_pipeline.py --start-month 2025-07 --end-month 2025-10 --outdir ../../../data/raw/ncdot-monthly

# Consolidation only (skip download, use existing files)
python ncdot_ev_pipeline.py --skip-download --out ../../../data/processed/master
```

**Dependencies:** `requests`, `openpyxl`

### data-cleaning/

Data cleaning, validation, and transformation scripts.

**consolidate_zev_monthly.py** - Consolidates monthly Excel files into a single dataset

```bash
# Consolidate all files in a directory
python consolidate_zev_monthly.py --indir ../../../data/raw/ncdot-monthly --out ../../../data/processed/nc_zev_consolidated.xlsx
```

**add_monthdate.py** - Adds `MonthDate` column (YYYYMM format) derived from `Month` column. Overwrites input file in place.

```bash
python add_monthdate.py
python add_monthdate.py --file ../../../data/generated/ncdot-ev-phev-latest.xlsx
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
- Outputs saved to `output/validation/`

**generate_phase1_figures.py** - Creates publication-quality visualizations from validation results

```bash
# Generate required figures (scatter, histogram, model comparison, CI coverage)
uv run python code/python/analysis/generate_phase1_figures.py

# Also generate nice-to-have figures (time series examples, boxplot, lollipop chart)
uv run python code/python/analysis/generate_phase1_figures.py --nice-to-have
```

Requires `validate_sas_forecasts.py` to be run first. Outputs saved to `output/figures/` in PNG and PDF formats.

**publication_style.py** - Shared matplotlib styling module for publication-quality figures (600 DPI, colorblind-friendly palette, IEEE-compatible dimensions). Imported by `generate_phase1_figures.py`.

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

### blog/

Importable Python package for generating blog graphics (LinkedIn, Substack).

**`__init__.py`** - Package initialization; re-exports `blog_graphics` module.

**blog_graphics.py** - Stat cards, multi-panel infographics, social media preview images, and comparison charts for blog content.

```python
from blog.blog_graphics import create_stat_card, create_social_preview
```

**Dependencies:** `matplotlib`, `Pillow`

---

## Running the Analysis

```bash
# Set up virtual environment
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install dependencies
pip install -e .

# Run scripts
python code/python/data-cleaning/consolidate_zev_monthly.py
```
