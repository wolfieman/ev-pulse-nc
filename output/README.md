# Output Directory

## Figures (`figures/`)

Publication-quality visualizations for the research paper (600 DPI, PDF exports).

### Phase 1 Validation Figures (Complete)

| Figure | Description |
|--------|-------------|
| fig-01-predicted-vs-actual-scatter | Scatter plot comparing SAS predictions to actual values |
| fig-02-error-distribution-histogram | Distribution of forecast errors across all observations |
| fig-03-metrics-by-model-type | MAPE/MAE/RMSE comparison by model type (ESM, ARIMA, UCM) |
| fig-04-confidence-interval-coverage | 95% CI coverage rates by model type |
| fig-05-time-series-examples | Sample county time series with forecasts and actuals |
| fig-06-mape-boxplot-by-model | MAPE distribution boxplot by model type |
| fig-07-county-performance-5x5 | County-level performance grid (5x5 subset) |
| fig-07-county-performance-10x10 | County-level performance grid (10x10 full view) |

All figures available in both PNG and PDF formats.

## Validation (`validation/`)

Output from `validate_sas_forecasts.py` — SAS Model Studio forecast accuracy assessment.

| File | Description |
|------|-------------|
| sas-validation-comparison.csv | Per-county, per-month predicted vs actual with error metrics |
| sas-validation-by-county.csv | Aggregate accuracy metrics by county and model type |
| sas-validation-by-model.csv | Aggregate accuracy metrics by model type (ESM, ARIMA, UCM) |
| sas-validation-report.txt | Human-readable validation report with executive summary |

## Tables (`tables/`)

Summary statistics and results tables.

## Models (`models/`)

Model index — see [`models/README.md`](models/README.md) for a one-stop guide to where every model in the project lives (SAS reference forecasts in `data/reference-forecasts/`, Python ARIMA replication in `code/python/analysis/arima_bev_forecast.py`, NEVI scoring composite in `scoring_framework_final.py`). No `.pkl` artifacts are persisted — fits run at-runtime.
