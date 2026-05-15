# SAS Model Studio Screenshots — Methodology Provenance

Working screenshots captured during the project's initial SAS Model Studio exploration (Feb 1, 2026). Documents the SAS environment used to produce the reference forecasts in [`data/reference-forecasts/`](../../../data/reference-forecasts/) — the basis for Phase 1 validation.

These are not part of the reader-facing documentation, but are kept in-repo as methodology provenance: a reviewer or future-you can confirm what the SAS environment looked like when the model selection (ESM × 82, ARIMA × 13, UCM × 5) was performed.

## Contents

| File | Shows |
|------|-------|
| `sas-data-view.png` | Raw NCDOT registration data loaded into SAS Model Studio |
| `sas-pipelines.png` | Pipeline configuration in SAS Model Studio |
| `sas-models-comparison.png` | Auto-model-selection comparison (ESM / ARIMA / UCM) |
| `sas-forecast-output.png` | Forecast output for a representative county |
| `sas-tables-view.png` | Tabular result view |
| `sas-export-options.png` | Export menu showing which results were downloadable for the Python validation pipeline |

## Why these matter

The forecasts these screenshots document are checked into `data/reference-forecasts/` as CSVs (`sas-forecasts.csv`, `sas-model-info.csv`, `sas-fit-statistics.csv`) and re-validated by Python in [`code/python/analysis/validate_sas_forecasts.py`](../../../code/python/analysis/validate_sas_forecasts.py) with MAPE = 4.36%. The screenshots provide the human-readable record of how those CSVs were generated.
