# Priority #1: Validation Analysis

**Status:** COMPLETE (February 2026)

## Executive Summary

Phase 1 validation tested SAS Model Studio forecasts against out-of-sample NCDOT data (Jul-Oct 2025). The analysis revealed strong point accuracy (MAPE 4.36%) but systematic underprediction, with 68.9% of forecasts falling below actual values.

---

## Validation Results

### Study Design

| Component | Specification |
|-----------|---------------|
| Training Period | September 2018 - June 2025 (82 months) |
| Validation Period | July - October 2025 (4 months) |
| Geographic Scope | 100 North Carolina counties (99 matched) |
| Target Variable | BEV (Battery Electric Vehicle) registrations |
| Validation Type | True out-of-sample holdout |

### Model Selection by SAS Model Studio

| Model Type | Counties | Description |
|------------|----------|-------------|
| ESM (Exponential Smoothing) | 82 | Weighted averages with decay |
| ARIMA | 13 | Autoregressive integrated moving average |
| UCM (Unobserved Components) | 5 (4 matched) | Structural time series |

### Accuracy Metrics

| Metric | Overall | ESM | ARIMA | UCM |
|--------|---------|-----|-------|-----|
| MAPE | 4.36% | 4.16% | 5.43% | 4.87% |
| MAE | 27.10 | 19.10 | 84.83 | 3.48 |
| RMSE | 114.11 | 74.67 | 252.94 | 6.53 |

### Bias Analysis

| Metric | Value | Interpretation |
|--------|-------|----------------|
| Mean Bias | +18.36 vehicles | Forecasts systematically too LOW |
| Underprediction Rate | 68.9% | Majority of forecasts exceeded by actuals |
| Direction | UNDERPREDICTION | EV adoption outpaced predictions |

### Confidence Interval Coverage

| Model | Observed Coverage | Expected | Gap |
|-------|-------------------|----------|-----|
| ARIMA | 67.3% | 95% | -27.7 pp |
| ESM | 75.3% | 95% | -19.7 pp |
| UCM | 100.0% | 95% | +5.0 pp |

---

## Interpretation

### Why Did Models Underpredict?

1. **Accelerating EV Adoption:** EV adoption appears to be in an acceleration phase, outpacing historical growth patterns. Potential drivers include IRA tax credits, increased model availability, Tesla price reductions, and expanding charging infrastructure.

2. **Structural Break Hypothesis:** A structural break may have occurred in EV market dynamics, making historical patterns less predictive of future behavior.

3. **Evidence Supporting These Hypotheses:**
   - Urban concentration of errors (Mecklenburg and Wake showed largest underpredictions)
   - Systematic direction (68.9% underprediction is not random)
   - CI failure pattern (actuals fall ABOVE upper bounds, not below)

### Pathway Determination

Based on MAPE 4.36% (below 5% threshold): **Pathway A (Strong Validation)**

Forecasts can be used for policy recommendations with the following caveats:
- Add 4-5% buffer to forecast-based allocations to account for faster-than-predicted adoption
- Report systematic underprediction bias in methodology sections
- Use confidence intervals with explicit acknowledgment of undercoverage

---

## Deliverables

### Publication-Quality Figures (8 total, 600 DPI, PDF exports)

1. fig-01-predicted-vs-actual-scatter.pdf
2. fig-02-error-distribution-histogram.pdf
3. fig-03-metrics-by-model-type.pdf
4. fig-04-confidence-interval-coverage.pdf
5. fig-05-time-series-examples.pdf
6. fig-06-mape-boxplot-by-model.pdf
7. fig-07-county-performance-5x5.pdf
8. fig-07-county-performance-10x10.pdf

---

## Follow-On Phases (Delivered)

Phase 1's findings flowed forward into the four subsequent extensions and the prescriptive layer:

- **Phase 2 — AFDC Infrastructure Update** (`frameworks/afdc-dataset-reference.md`):
  Replaced the prior DCFC-only extract with a full Feb 2026 NREL AFDC API pull —
  1,985 stations, 6,145 connectors covering all charging levels (L1/L2/DCFC) and
  access types (public/private). The dual-snapshot approach originally considered
  in Phase 1 was abandoned once the prior file was identified as a filtered extract.

- **Phase 3 — ZIP Code Analysis** (`frameworks/zip-code-analysis.md`):
  Decomposed infrastructure inequality at the sub-county level. Statewide Gini =
  0.805; Theil decomposition attributed 84.5% of inequality to within-county
  variation. Found a 250-fold port density gap between Charlotte ZIPs 28202 and
  28215. Produced figures fig-08 through fig-34.

- **Phase 4 — Workplace Charging (LEHD/LODES)** (`frameworks/ctpp-analysis.md`):
  Used LEHD LODES rather than the originally planned CTPP, with a Barrero/Bloom/
  Davis (2023) 0.85 remote-work multiplier and an SE03 income filter. Estimated
  859,260 statewide adjusted workplace charging events; identified Mecklenburg
  (+194,361 net commuter inflow), Wake (+126,517), and Durham (+89,450) as the
  dominant employment centers.

- **Phase 5 — CEJST Equity Analysis** (`frameworks/stakeholder-value-analysis.md`):
  Implemented Phase 5 equity using CEJST v2.0 tract-level Justice40 designations
  (934/2,170 NC tracts flagged disadvantaged). Tract-to-ZCTA area-weighted overlay
  in EPSG:32119 produced county and ZCTA-level Justice40 shares feeding the
  Equity_Score pillar. Climate sensitivity and weight sensitivity sub-analyses
  produced figures fig-39 through fig-42.

- **Prescriptive Layer — NEVI Scoring Framework**:
  All four extensions feed the composite formula
  `NEVI Score = 0.40 · Equity_Score + 0.35 · Utilization_Score + 0.25 · Cost_Effectiveness_Score`,
  with the Phase 1 underprediction-bias-derived ~4-5% buffer applied to the
  Utilization pillar. See `frameworks/analytical-pipeline.md` for the full pipeline
  integration and `frameworks/stakeholder-value-analysis.md` for delivered
  stakeholder value.
