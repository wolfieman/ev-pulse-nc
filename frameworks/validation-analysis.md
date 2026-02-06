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

## Original Framework (Pre-Execution)

The original decision framework defined 5 critical decision nodes:

1. **Validation Scope:** Out-of-sample accuracy (selected)
2. **Segmentation Strategy:** Stratified by model type (selected)
3. **Accuracy Thresholds:** MAPE < 5% = strong (achieved: 4.36%)
4. **Assumption Testing:** Addressed via bias analysis
5. **Interpretation Pathways:** Pathway A selected based on results

---

## Next Steps (Phase 2)

Based on validation findings, Phase 2 should prioritize:

1. **Diagnostic Analysis:** Root cause analysis of underprediction (IRA effects, Tesla pricing, infrastructure expansion)
2. **Prescriptive Recommendations:** Policy recommendations with bias-corrected forecasts
3. **Remaining Priorities:** ZIP code analysis (#2), CTPP workplace charging (#3), AFDC update (#5)
