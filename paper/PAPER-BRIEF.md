# Paper Brief — EV Pulse NC

*Manuscript in preparation. This brief summarizes the question, headline findings, methods, and policy implications. The full working draft is maintained privately as `paper/PAPER-NOTES.md` (gitignored) until publication.*

**Working title:** EV Pulse NC — Quantifying and Closing the EV Infrastructure Gap in North Carolina
**Author:** Wolfgang Sanyer (sole author)
**Affiliation:** Fayetteville State University, Broadwell College of Business and Economics
**Course context:** BIDA 670 Advanced Analytics Capstone, Spring 2026

---

## Question

North Carolina's battery-electric vehicle (BEV) fleet grew 1,727% over seven years. Public charging infrastructure has not kept pace. **Where, specifically, is the gap, and how should the state's $109M federal NEVI Formula Program funding be allocated to close it equitably?**

---

## Headline Findings

1. **Demand-side concentration is severe.** Statewide BEV Gini coefficient = 0.805. Top 10 counties hold 72% of registrations; the Research Triangle (Wake + Durham + Orange) alone accounts for 35.2%.
2. **Supply is more dispersed than demand.** AFDC Feb 2026 baseline: 1,985 stations / 6,145 connectors across 267 cities and 358 ZIP codes. Weighted statewide Gini of charging-port density = 0.566 (less concentrated than BEV demand).
3. **Inequality lives within counties.** Theil-T decomposition: **84.5% of ZIP-level infrastructure inequality is within-county; only 15.5% between-county.** This is the paper's central methodological contribution.
4. **Justice40 alignment is roughly proportional.** 43.0% of NC's evaluable census tracts (934/2,170) are CEJST-disadvantaged; 24.5% of charging stations sit in those tracts. Climate-sensitivity check: removing the Climate Change burden category drops disadvantaged-tract share to 37.3%; the headline finding holds for 7 of 10 study counties.
5. **NEVI priority ranking is stable.** Top 3 counties (Union 0.561, Mecklenburg 0.548, Guilford 0.465) hold across equity-weight sensitivity sweep (0.30–0.50).
6. **Forecasting validation passes.** Python ARIMA replication of SAS Model Studio forecasts achieves MAPE = 4.36% on 4-month holdouts. Independent confirmation of the demand-forecasting baseline.

---

## Methods at a Glance

- **Data:** NCDOT vehicle registrations (Sept 2018 – June 2025, 8,200 obs); AFDC charging-station API (Feb 2026, 1,985 stations); ACS 2018–2022 (income, tenure); LEHD LODES 2021 (commuting flows); CEJST v2.0 (Justice40 designation); SAS Model Studio reference forecasts (auto-selected ESM × 82, ARIMA × 13, UCM × 5).
- **Pipeline:** 5 sequential analytical phases, each producing publication-quality figures (42 total, 600 DPI PDF + PNG).
- **Validation:** Independent Python ARIMA replication of SAS demand forecasts (MAPE 4.36%).
- **Inequality metrics:** Lorenz/Gini, Theil-T (GE(1)) for decomposition, Theil-L (GE(0)) for robustness. Population-weighted and unweighted variants both reported.
- **Composite score:** `NEVI Priority Score = 0.40·Equity + 0.35·Utilization + 0.25·Cost-Effectiveness`. VIF check confirms scoring pillars are sufficiently independent (no multicollinearity).
- **Sensitivity testing:** Equity-weight sweep (0.30–0.50); CEJST climate-category drop-test; weight-sensitivity grid. Top-3 ranking stable across all sweeps.

Full methodology spec: [`../frameworks/analytical-pipeline.md`](../frameworks/analytical-pipeline.md). Per-dataset schema: [`../data/DATA-DICTIONARY.md`](../data/DATA-DICTIONARY.md).

---

## Policy Implications

1. **County-level fund allocation is necessary but not sufficient.** With 84.5% of inequality within counties, county-only formulas miss the gap. NEVI deployment should pair county-level priority ranking with ZIP-level targeting within each priority county.
2. **Two-tier framework recommended.** This work proposes (a) a county-level NEVI Priority Score for policymakers and (b) a ZIP-level "top-20 underserved" list within each priority county for local planners.
3. **Justice40 alignment is acceptable as a baseline but not aspirational.** 24.5% of stations sitting in disadvantaged tracts is roughly proportional to disadvantaged-tract share (43.0%), but a Justice40-aligned framework would target oversampling — not parity.
4. **Forecasting-based capacity planning needs a buffer.** Phase 1 validation shows SAS auto-selected ESM models systematically under-predict BEV growth over 4-month holdouts. Demand-based capacity planning should include an upward adjustment (current framework uses 4.5%).

---

## Status

Manuscript in active preparation as of May 2026. Target venues under consideration: *Transportation Research Record*, *Energy Policy*, *Sustainable Cities and Society*. Working notes maintained at `paper/PAPER-NOTES.md` (private, gitignored).

---

## How to cite this work

See [`../CITATION.cff`](../CITATION.cff) at the repo root, or click **"Cite this repository"** on the GitHub page.
