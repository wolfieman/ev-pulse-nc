# Models — Index

This project's "models" live in several places. There are no pickled artifacts (`*.pkl`, `*.joblib`) committed to the repo — ARIMA fits run at-runtime, the SAS models live inside SAS Model Studio, and the NEVI scoring framework is a methodology composite rather than a trained ML object. This file documents where each model lives and what it produces.

## 1. SAS Model Studio Forecasts (Phase 1)

- **Output location:** `data/reference-forecasts/`
- **Coverage:** 100 NC counties, monthly forecasts Sept 2018 – June 2026 (82 months training + 12 months forecast)
- **Auto-selected model families:** ESM × 82 counties, ARIMA × 13, UCM × 5
- **Files:**
  - `sas-forecasts.csv` — per-county, per-month predicted means with 95% CIs
  - `sas-model-info.csv` — selected model family per county
  - `sas-fit-statistics.csv` — fit metrics (MAPE, RMSE, AIC, etc.)
- **Persistence:** Forecast outputs only; the SAS model objects themselves remain inside SAS.

## 2. Python ARIMA Replication (Phase 1)

- **Script:** `code/python/analysis/arima_bev_forecast.py` (full implementation)
- **Quick-reference scaffold:** `code/python/analysis/arima_template.py` (SAS → Python translation guide)
- **Purpose:** Cross-platform validation of the SAS forecasts; sanity-check of model selection and fit
- **Persistence:** None — fits at runtime. ARIMA on 82 monthly observations refits in under a second per county, so on-disk persistence is unnecessary.

## 3. NEVI Priority Score (Phase 5)

- **Build pipeline:**
  1. `code/python/analysis/scoring_framework_skeleton.py` → `data/processed/scoring-framework-skeleton.csv` (Phase 3/4 inputs assembled, Phase 5 slots left NaN)
  2. `code/python/analysis/scoring_framework_final.py` → `data/processed/scoring-framework-final.csv` (Justice40 merged in, all 17 columns populated)
  3. `code/python/analysis/scoring_framework_vif.py` → `data/processed/scoring-vif-check.csv` (variance-inflation multicollinearity check on the three pillars)
- **Composite formula:** `NEVI Priority Score = 0.40 × Equity + 0.35 × Utilization + 0.25 × Cost-Effectiveness`
- **Methodology reference:** `frameworks/analytical-pipeline.md`
- **Robustness:** weight sensitivity grids in `code/python/analysis/phase5_weight_sensitivity.py` and `data/processed/scoring-weight-sensitivity.csv`

## 4. Why no `.pkl` files are persisted

- ARIMA refits per county in under a second; saving and re-loading pickled fits would add complexity without speeding anything up.
- `.gitignore` excludes `*.pkl`, `*.pickle`, `*.joblib`, `*.h5`, `*.hdf5` — even if pickled models were generated locally, they would not be tracked.
- The "models" in this project are methodology (the scoring composite and its sub-weights) and forecast outputs, not trained ML weights.

If you later add a workflow that benefits from persistence (e.g., a large ensemble or a slow-to-fit Bayesian model), this folder is the intended home for the resulting `.pkl` files; remove the relevant entries from `.gitignore` at that point.
