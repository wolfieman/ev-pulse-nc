# Output Directory

## Figures (`figures/`)

42 publication-quality figures spanning all 5 analytical phases. Dual export: PNG (web/preview) + PDF (publication, 600 DPI).

| Phase | Range | Topic |
|---|---|---|
| **Phase 1 — Validation** | `fig-01` – `fig-07` (plus `fig-07-county-performance-5x5` variant) | SAS forecast accuracy, error distribution, model-type comparison (ESM / ARIMA / UCM), 95% CI coverage, county-level performance grids |
| **Phase 2 / 3 — AFDC + ZIP equity** | `fig-08` – `fig-34` (plus `fig-22s` / `fig-23s` / `fig-24s` supplementary heatmaps) | AFDC EDA (missing values, levels, networks, geographic coverage), Lorenz / Gini / Theil inequality, county heatmaps (Wake / Guilford / Mecklenburg), underserved-ZIP choropleth |
| **Phase 4 — Workplace charging** | `fig-35` – `fig-38` | Net commuter flow, residential vs. residential+workplace demand, county commuter-typology choropleth, port scenario range |
| **Phase 5 — Justice40 equity** | `fig-39` – `fig-42` | CEJST disadvantaged tracts, ZCTA / county Justice40 overlays, stations-on-Justice40 overlay |

Methodology and which script produces which figure: [`../frameworks/analytical-pipeline.md`](../frameworks/analytical-pipeline.md) and [`../code/README.md`](../code/README.md).

## Validation (`validation/`)

Output from `validate_sas_forecasts.py` — SAS Model Studio forecast accuracy assessment.

| File | Description |
|------|-------------|
| `sas-validation-comparison.csv` | Per-county, per-month predicted vs actual with error metrics |
| `sas-validation-by-county.csv` | Aggregate accuracy metrics by county and model type |
| `sas-validation-by-model.csv` | Aggregate accuracy metrics by model type (ESM, ARIMA, UCM) |
| `sas-validation-report.txt` | Human-readable validation report with executive summary |

## Models (`models/`)

Index doc only — see [`models/README.md`](models/README.md). The project's models live elsewhere: SAS reference forecasts in `data/reference-forecasts/`, Python ARIMA replication in `code/python/analysis/arima_bev_forecast.py`, NEVI scoring composite in `scoring_framework_final.py`. No `.pkl` artifacts are persisted — fits run at-runtime.
