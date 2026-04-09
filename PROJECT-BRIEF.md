# EV Pulse NC: Project Brief

**Audience:** Dr. Majed Al-Ghandour, BIDA 670 Instructor
**Date:** February 1, 2026 (original); current-state banner added April 2026

---

## Current State (Apr 2026)

All five project extensions are merged into `main`: Phase 1 (Validation), Phase 2 (AFDC Update), Phase 3 (ZIP Analysis), Phase 4 (Workplace Charging / LEHD), Phase 5 (CEJST Equity). The Phase 5 equity layer was implemented using CEJST tract-level Justice40 designations (not HEPGIS corridors as originally contemplated). The current AFDC infrastructure baseline is 1,985 stations and 6,145 connectors (all levels L1/L2/DCFC, Feb 2026 API download) — the earlier 355/1,725 numbers used in the original proposal below were later identified as a DCFC-only public extract. The dual-snapshot growth framing described below was abandoned once that was discovered. For the current analytical pipeline and results narrative, see `frameworks/analytical-pipeline.md` and `paper/PAPER-NOTES.md`.

---

## Historical Proposal (Feb 1, 2026)

The sections below are preserved as the original proposal-stage brief.

## Project Overview

North Carolina faces a critical infrastructure challenge: EV adoption is outpacing charging deployment, with 53.8% CAGR in BEV registrations but infrastructure lagging 13-40% by county (see [README.md — Key Findings](README.md#-key-findings) for detailed statistics).

This project analyzes alignment between EV adoption and infrastructure across all 100 North Carolina counties using 8,200 county-month observations (82 months) and 1,725 individual charging connectors. Core question: where should North Carolina's $109 million in NEVI funding go?

**Baseline analysis last semester** produced county-level ARIMA forecasts (weighted MAPE 2.73%), identified the infrastructure gap, and revealed extreme geographic inequality (Gini 0.805). This semester adds three extensions to enhance spatial precision, temporal currency, and demand dimensionality.

What makes this distinctive: county-level granularity over 82 months with connector-level detail (1,725 units vs. 355 stations)—4.85 times more precision than typical state-level snapshot studies.

---

## Extension Slice #1: Validation (Priority #1) - COMPLETE

The validation extension tested SAS Model Studio forecast accuracy using true out-of-sample data (Jul-Oct 2025).

**Results:**
- **MAPE:** 4.36% (strong validation, below 5% threshold)
- **MAE:** 27.10 vehicles, **RMSE:** 114.11 vehicles
- **Systematic Bias:** +18.36 vehicles (underprediction)
- **Underprediction Rate:** 68.9% of forecasts fell below actuals
- **95% CI Coverage:** 75.3% (below nominal 95% due to bias)
- **Model Distribution:** ESM (82 counties), ARIMA (13 counties), UCM (5 counties)

**Key Finding:** EV adoption in North Carolina is accelerating faster than historical patterns predicted. The models systematically underestimated growth, particularly in high-growth urban counties (Mecklenburg, Wake). This suggests that forecast-based infrastructure planning should add a 4-5% buffer to account for faster-than-predicted adoption.

**Deliverables:** 8 publication-quality figures (600 DPI, PDF exports) documenting validation analysis.

---

## Extension Slice #2: ZIP Code Analysis + Infrastructure Update (Priority #2 + #5)

County-level aggregation obscures intra-county variation. Wake County spans 857 square miles with 28 ZIP codes having dramatically different BEV densities.

While NCDOT does not publish ZIP-level BEV data, charging stations have ZIP codes. The extension geocodes all 1,725 connectors, calculating infrastructure density metrics: ports per square mile, ports per capita, and spatial clustering.

This integrates with Priority #5 (infrastructure update). The dual-snapshot approach (July 2024 + January 2026) calculates growth rates: which counties saw fastest deployment, what charger types were added, and whether new infrastructure targeted gap counties or amplified disparities.

Value proposition: "deploy in ZIP codes 27603, 27607, 27615" provides actionable site selection. Analysis focuses on 100-120 ZIP codes within top 10 urban counties (80% of state BEVs).

---

## Extension Slice #3: Workplace Charging (Priority #3)

The baseline treated BEV demand as residential (80% of charging at home). This is accurate but incomplete—EVs also require workplace charging.

The workplace extension adds a second dimension using Census Transportation Planning Products (CTPP) data—county-to-county commuting flow matrices.

The methodology identifies employment centers by calculating net commuting effects: inbound workers minus outbound residents. Wake County has 450,000 workers but only 350,000 residents employed within the county—100,000 daily inbound commuters representing workplace demand that residential analysis misses.

Employment centers need 2-3 times more infrastructure than residential analysis suggests. Wake County's residential demand requires 1,700-2,500 ports. Adding workplace demand (8,400 net EV commuters) increases needs to 2,200-3,100 ports.

---

## Integration Logic

The extensions connect through a dependency chain. Validation (Priority #1) established confidence in SAS Model Studio forecasting with MAPE 4.36% (below 5% threshold). The systematic underprediction finding (68.9% of forecasts below actuals) informs how forecasts should be applied: with a 4-5% upward buffer to account for accelerating adoption. The AFDC infrastructure update (Priority #5) provides the current baseline that subsequent extensions require.

ZIP code analysis (Priority #2) and CTPP workplace charging (Priority #3) complement each other, creating a triple-layer model: county-level totals (baseline), sub-county spatial patterns (ZIP codes), and cross-county commuting flows (CTPP).

---

## Methodological Innovation Summary

Five innovations distinguish this from typical EV infrastructure studies (see [PROJECT-EXPLANATION.md — Methodological Innovation Summary](PROJECT-EXPLANATION.md#methodological-innovation-summary) for expanded discussion):

1. **County-level granularity over 82 months:** Examines all 100 counties across seven years of monthly observations, enabling time series forecasting that captures heterogeneous adoption trajectories.

2. **Connector-level infrastructure detail:** Analyzes 1,725 individual connectors rather than 355 stations—4.85 times more granular, enabling capacity-weighted analysis.

3. **Dual-snapshot infrastructure growth:** Dual-snapshot approach (July 2024 + January 2026) treats temporal evolution as a research question, revealing whether market forces close gaps or amplify disparities.

4. **Dual-dimension demand model:** Combines residential registrations with workplace commuting flows for complete demand picture.

5. **Validation-first approach:** Tests forecast accuracy with out-of-sample data before policy recommendations.

---

## Conclusion

EV Pulse NC addresses how North Carolina should allocate $109 million in NEVI funding to maximize efficiency and equity. The baseline analysis last semester established comprehensive county-level understanding. This semester's three extensions enhance that foundation by validating forecast accuracy, updating infrastructure data with dual-snapshot growth analysis, adding sub-county spatial precision, and incorporating workplace charging demand.

The project provides stakeholders with actionable insights at multiple scales: statewide trends for policy, county-level forecasts for regional planning, ZIP code detail for site selection, and workplace demand sizing for employment centers.

---

**Project Team:**
Wolfgang Sanyer<BR>
MBA Candidate, Business & Data Analytics Concentration<BR>
Fayetteville State University

**Faculty Advisor:** Dr. Majed Al-Ghandour<BR>
**Course:** BIDA 670 - Advanced Analytics Capstone<BR>
**Semester:** Spring 2026
