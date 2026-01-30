# Priority #1: Validation Decision Framework

## Executive Summary

The validation roadmap defines 5 critical decision nodes with clear analytical pathways:

## Decision Node 1: Validation Scope

- Out-of-sample accuracy only? (July-Oct 2025 actuals vs. predictions)
- Methodological soundness? (ARIMA assumptions tested)
- Both? (comprehensive but time-intensive)

## Decision Node 2: Segmentation Strategy

- Aggregate (single MAPE across all counties)
- Stratified (urban/suburban/rural performance)
- Temporal (month-by-month drift analysis)
- Combined

## Decision Node 3: Accuracy Thresholds

- MAPE < 5%: Strong validation → proceed with confidence
- MAPE 5-10%: Moderate validation → proceed with caution (wider intervals)
- MAPE > 10%: Weak validation → remediate before policy use

## Decision Node 4: Assumption Testing

- Stationarity (Dickey-Fuller test)
- Autocorrelation (Ljung-Box test)
- Structural breaks (Chow test at IRA passage date)
- Heteroscedasticity (Breusch-Pagan test)

## Decision Node 5: Interpretation Pathways

- Pathway A (Strong): Extend forecast with published confidence intervals
- Pathway B (Weak): Diagnose failure mode → bias correction, hybrid approach, or methodology switch
- Pathway C (Ambiguous): Scenario bracketing, tiered thresholds, transparent limitations

---

## Key Trade-Offs Identified

1. **Accuracy vs. Interpretability**: ARIMA is transparent but may underperform complex models
2. **County-level vs. State-level**: Aggregate validation is robust but hides local failures
3. **Point Estimates vs. Intervals**: Actionable but overconfident vs. honest but imprecise
4. **4-Month Period**: Sufficient for aggregate validation, inadequate for individual rural counties

---

## Critical Insight

Validation is not pass/fail - it's a spectrum requiring interpretation based on:
- Error magnitude and distribution
- Policy tolerance for uncertainty
- Methodological soundness
- Stakeholder expectations

The framework maps how different validation outcomes lead to different analytical pathways for the remaining priorities.
