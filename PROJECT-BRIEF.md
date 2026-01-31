# EV Pulse NC: Project Brief

**Audience:** Dr. Majed Al-Ghandour, BIDA 670 Instructor
**Date:** January 30, 2026

---

## Project Overview

North Carolina faces a critical infrastructure challenge: electric vehicle adoption is outpacing charging infrastructure deployment. Between September 2018 and June 2025, the state's BEV fleet grew from 5,165 to 94,371 vehicles—a 1,727% increase (53.8% CAGR). Public charging infrastructure has struggled to keep pace, with 16.9 BEVs per port versus the 10-15 national benchmark.

This project analyzes alignment between EV adoption and infrastructure across all 100 North Carolina counties using 8,200 county-month observations (82 months) and 1,725 individual charging connectors. Core question: where should North Carolina's $109 million in NEVI funding go?

**Baseline analysis last semester** produced county-level ARIMA forecasts (weighted MAPE 2.73%), identified infrastructure gap of 16.9 BEVs per port, and revealed extreme geographic inequality (Gini 0.805—top 10 counties hold 72% of BEVs, bottom 50 hold 4.8%). This semester adds four extensions to enhance spatial precision, temporal currency, and demand dimensionality.

What makes this distinctive: county-level granularity over 82 months with connector-level detail (1,725 units vs. 355 stations)—4.85 times more precision than typical state-level snapshot studies.

---

## Extension Slice #1: Validation (Priority #1)

The validation extension tests forecast accuracy using out-of-sample data. The baseline reported strong historical fit (MAPE 2.73%), but this measures in-sample performance.

NCDOT has published July-October 2025 actual BEV counts. The validation process compares ARIMA predictions against actuals, calculating accuracy metrics (MAPE, MAE, RMSE). Most infrastructure planning studies deploy forecasts without validation. Strong performance (MAPE below 5%) enables confident policy recommendations through 2028.

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

The extensions connect through a dependency chain. Validation (Priority #1) establishes confidence in ARIMA forecasting. If validation is strong (MAPE below 5%), county-level forecasts can be used as constraints for ZIP code allocation and workplace demand calculations. The AFDC infrastructure update (Priority #5) provides the current baseline that subsequent extensions require.

ZIP code analysis (Priority #2) and CTPP workplace charging (Priority #3) complement each other, creating a triple-layer model: county-level totals (baseline), sub-county spatial patterns (ZIP codes), and cross-county commuting flows (CTPP).

---

## Methodological Innovation Summary

Five innovations distinguish this from typical EV infrastructure studies:

1. **County-level granularity over 82 months:** Examines all 100 counties across seven years of monthly observations, enabling time series forecasting that captures heterogeneous adoption trajectories.

2. **Connector-level infrastructure detail:** Analyzes 1,725 individual connectors rather than 355 stations—4.85 times more granular, enabling capacity-weighted analysis.

3. **Dual-snapshot infrastructure growth:** Dual-snapshot approach (July 2024 + January 2026) treats temporal evolution as a research question, revealing whether market forces close gaps or amplify disparities.

4. **Dual-dimension demand model:** Combines residential registrations with workplace commuting flows for complete demand picture.

5. **Validation-first approach:** Tests forecast accuracy with out-of-sample data before policy recommendations.

---

## Conclusion

EV Pulse NC addresses how North Carolina should allocate $109 million in NEVI funding to maximize efficiency and equity. The baseline analysis last semester established comprehensive county-level understanding. This semester's four extensions enhance that foundation by validating forecast accuracy, updating infrastructure data with dual-snapshot growth analysis, adding sub-county spatial precision, and incorporating workplace charging demand.

The project provides stakeholders with actionable insights at multiple scales: statewide trends for policy, county-level forecasts for regional planning, ZIP code detail for site selection, and workplace demand sizing for employment centers.

---

**Project Team:**
Wolfgang Sanyer & Braeden Baker
MBA Candidates, Business & Data Analytics Concentration
Fayetteville State University

**Faculty Advisor:** Dr. Majed Al-Ghandour
**Course:** BIDA 670 - Advanced Analytics Capstone
**Semester:** Spring 2026
