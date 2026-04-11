# EV Pulse NC: Project Explanation for Dr. Al-Ghandour

**Audience:** Dr. Majed Al-Ghandour, BIDA 670 Instructor
**Purpose:** Explain project structure, baseline vs. extensions, and methodological innovation

---

## Project Overview

North Carolina faces a critical infrastructure challenge: electric vehicle (EV) adoption is outpacing the deployment of public charging infrastructure, creating geographic inequalities that threaten equitable access to electric mobility. Between September 2018 and June 2025, the state's battery electric vehicle (BEV) fleet expanded from 5,165 to 94,371 vehicles — a 1,727% increase at a 53.8% compound annual growth rate.

This project analyzes the alignment between EV adoption and infrastructure deployment across all 100 North Carolina counties over 82 months of time series data (September 2018 through June 2025). The demand side is an 8,200 county-month panel of NCDOT BEV registrations. The supply side is the full NREL AFDC infrastructure baseline: **1,985 stations and 6,145 connectors across all charging levels (L1, L2, DCFC) and all access types, covering 267 cities and 358 ZIPs (Feb 2026 API pull).** The core research question addresses resource allocation: where should North Carolina's $109 million in NEVI Formula Program funding be deployed to maximize infrastructure equity, utilization, and cost-effectiveness?

What makes this analysis distinctive is its granularity and temporal depth. Most EV infrastructure studies operate at the state or metropolitan level using snapshot data; this project examines county-level dynamics over nearly seven years, then decomposes the gap through sub-county, workplace, and equity lenses that feed a prescriptive NEVI scoring framework.

---

## Baseline Analysis — Completed Last Semester

The baseline analysis established the analytical foundation through a five-phase framework (exploratory, descriptive, diagnostic, predictive, prescriptive) completed during Fall 2025.

> **Key statistics:** See [README.md — Key Findings](README.md#-key-findings) for the canonical demand-side and supply-side metrics referenced throughout this section.

On the demand side, the analysis processed NCDOT's complete time series of BEV registrations: 8,200 observations spanning 100 counties across 82 months. The data reveals extreme geographic concentration (statewide connector Gini 0.805), creating a tension between efficiency (deploying infrastructure where demand already exists) and equity (ensuring rural and disadvantaged communities have access).

The predictive component employed county-level ARIMA forecasting to project BEV adoption through June 2028. Rather than a single statewide model, 100 separate county models capture heterogeneous adoption trajectories. The weighted in-sample MAPE across all counties was 2.73%, indicating strong historical fit. The gap analysis compared BEVs per county to charging ports per county using both simple ratios and capacity-weighted metrics, and classified counties into well-aligned, emerging-strain, and high-strain tiers. Roughly 47.6% of current infrastructure was added during 2024-2025, reflecting NEVI Formula Program dollars and Inflation Reduction Act tax credits.

This baseline established credibility through methodological rigor and comprehensive coverage. The extension work this semester adds strategic depth without replacing the baseline.

---

## The Extension Framework — This Semester

This semester's work builds on the baseline through five targeted extensions that enhance rather than replace the county-level temporal analysis. The extensions follow a clear dependency chain: validation first, then a current infrastructure baseline, then three lenses (spatial, workplace, equity) that decompose the county-level gap. All five extensions are complete and merged into `main`, and their outputs feed a prescriptive NEVI scoring framework that translates findings into defensible county-level funding allocations.

The extensions share a common analytical philosophy: acknowledge limitations transparently, report ranges rather than false precision, and frame findings as proof-of-concept methodologies that future work can refine.

---

## Extension Slice #1: Phase 1 — Predictive Validation

The validation extension addressed a fundamental question: how accurate are the SAS Model Studio forecasts used to project future infrastructure needs? The baseline reported strong historical fit (MAPE 2.73%), but that is in-sample performance. Out-of-sample validation tests whether models maintain accuracy on genuinely new data.

### Validation Results

The validation compared SAS Model Studio predictions against NCDOT actual data for July-October 2025 (4 months out-of-sample).

| Metric | Result | Interpretation |
|--------|--------|----------------|
| MAPE | 4.34% | Strong validation (below 5% threshold) |
| MAE | 26.88 vehicles | Average absolute error per county-month |
| RMSE | 113.54 vehicles | Root mean squared error |
| Bias | +18.22 vehicles | Systematic underprediction |
| Underprediction Rate | 69.00% | Majority of forecasts fell below actuals |
| 95% CI Coverage | 75.50% | Below nominal 95% due to bias |

SAS Model Studio auto-selected different model types per county: ESM (82 counties), ARIMA (13 counties), and UCM (5 counties). ESM models performed best overall (MAPE 4.16%); ARIMA models showed higher errors (MAPE 5.43%), reflecting their use in larger, more volatile urban counties.

### Key Finding: Systematic Underprediction

The most significant finding is systematic underprediction. Actual EV registrations exceeded forecasts in 69.00% of observations, with a mean bias of +18.22 vehicles per county-month. The 95% prediction interval coverage is only 75.50%. The pattern is most pronounced in high-growth urban counties — Mecklenburg County underpredicted by up to 975 vehicles in October 2025. EV adoption in North Carolina is accelerating faster than historical patterns predicted, likely driven by Inflation Reduction Act tax credits, Tesla price reductions, and expanding infrastructure. For policy planning, this finding justifies a **4-5% upward buffer on forecast-based infrastructure allocations**, which is applied in the Utilization Score of the NEVI scoring framework.

### Deliverables

Eight publication-quality figures (600 DPI, PDF): predicted-vs-actual scatter, error distribution histogram, metrics comparison by model type, CI coverage analysis, time series examples, MAPE boxplot by model type, and county-level performance grids (5x5 and 10x10).

---

## Extension Slice #2: Phase 2 — AFDC Infrastructure Baseline

Phase 2 replaced the prior DCFC-only public extract with a full NREL AFDC API pull covering all charging levels (L1, L2, DCFC) and all access types. The current baseline is **1,985 stations and 6,145 connectors across 267 cities and 358 ZIP codes (Feb 2026 pull)**. This supersedes earlier station and connector counts that were later identified as DCFC-only.

The full-coverage pull matters because roughly half of North Carolina's workplace and destination charging infrastructure is Level 2, and a DCFC-only extract systematically understates the supply side — particularly in employment centers where L2 dominates. Phase 2 provides the complete infrastructure baseline that Phases 3, 4, and 5 all depend on. See `frameworks/afdc-dataset-reference.md` and `frameworks/afdc-data-structure.md` for the dataset reference and schema.

---

## Extension Slice #3: Phase 3 — ZIP Code Analysis

County-level aggregation obscures critical intra-county variation, particularly in large urban counties. Wake County alone spans 857 square miles across roughly 28 ZIP codes with dramatically different BEV adoption densities. ZIP code analysis provides sub-county precision that enables targeted deployment strategies.

NCDOT does not publish ZIP-level BEV registration data, so Phase 3 focuses on the supply side: geocoding all 6,145 connectors to their ZIP codes and calculating infrastructure density metrics (ports per square mile, ports per capita, spatial clustering) across **134 ZIP codes in the top 10 urban counties**. These ZIPs capture roughly 80% of the state's BEV population. The analysis uses county-level BEV forecasts as constraints and examines within-county infrastructure distribution.

### Key Findings

- Statewide connector **Gini coefficient of 0.805** — comparable to highly unequal wealth distributions.
- A **Theil decomposition attributes 84.5% of spatial inequality to within-county variation**, meaning most of the spatial inequality in charging access is hidden below the county level — exactly the kind of gap county-only analysis cannot see.
- Within Charlotte alone, the port density gap between ZIP 28202 and ZIP 28215 is roughly **250-fold**.
- The top-20 underserved ZIPs are concentrated in high-BEV urban counties with poor sub-county distribution — the clearest site-selection targets from the project.

Outputs: `data/processed/phase3-county-gini.csv`, `phase3-theil-decomposition.csv`, `phase3-zip-density.csv`, `phase3-top20-underserved.csv`. These feed both the Utilization Score and the Equity Score of the NEVI scoring framework.

---

## Extension Slice #4: Phase 4 — Workplace Charging (LEHD/LODES)

The baseline analysis treats BEV demand as a residential phenomenon (vehicles registered to home addresses, ~80% of charging at home). This is accurate but incomplete: EVs also need workplace charging, particularly for commuters with long distances or multi-family residents without home access. Phase 4 adds a second analytical dimension by incorporating inter-county commuting patterns.

### Data and Method

Phase 4 uses LEHD LODES (not CTPP, which was the originally planned source) — specifically the Origin-Destination (OD) tables, Workplace Area Characteristics (WAC), and the LODES geography crosswalk, corrected with ACS income tabulations. LODES gives near-current (2021) county-to-county commuter flow data at higher geographic fidelity than CTPP. The workplace-eligible flow is filtered to **SE03 (earnings > $3,333/month)** as a proxy for workers with income profiles consistent with EV ownership, then adjusted with a **0.85 multiplier for post-COVID remote work** sourced from Barrero, Bloom, and Davis (2023, "The Evolution of Work from Home"). EV adoption rates are applied at origin county (where commuters live, which determines home charging access), with a 1.25 commuter-income premium to reflect the higher average earnings of commuters vs. residents.

### Key Findings

- **Statewide adjusted workplace demand: 859,260** commuter-based EV charging events (post-remote-work adjustment, after SE03 income filter).
- **Top net employment centers (net inbound commuters):** Mecklenburg +194,361, Wake +126,517, Durham +89,450. These are the counties where residential-only analysis systematically underfunds infrastructure.
- **NC infrastructure gap:** The statewide ratio of 15.4 BEVs per port exceeds the IEA global benchmark of ~10 EVs per public charger (IEA Global EV Outlook, 2023-2024), and the top-10 urban county median of 20.6 indicates acute infrastructure strain. Workplace chargers have consistent demand (same commuters Mon-Fri) and long dwell times (8-hour workdays) that maximize utilization compared to variable, transient public retail demand.

Phase 4 explicitly acknowledges uncertainty through sensitivity ranges rather than point estimates. Outputs: `data/processed/phase4-cost-effectiveness.csv`, `phase4-employment-centers.csv`. These feed the Cost-Effectiveness Score in the NEVI scoring framework.

---

## Extension Slice #5: Phase 5 — CEJST Equity Overlay

Phase 5 delivers the equity layer of the project. It uses the Council on Environmental Quality's **Climate and Economic Justice Screening Tool (CEJST) v2.0** to identify federally-designated Justice40 disadvantaged communities in North Carolina. CEJST provides the official tract-level Justice40 designations that the NEVI program's 40%-to-disadvantaged-communities mandate is enforced against.

### Data and Method

- **934 of 2,170 NC census tracts (43%)** are CEJST-designated disadvantaged.
- Tract-level flags are overlaid on counties and ZCTAs via **area-weighted interpolation** to produce a county-level and ZCTA-level disadvantaged community share.
- A **climate-only subset sensitivity** tests whether results hold if only the climate indicators are used rather than the full CEJST indicator set.
- A **weight sensitivity analysis** confirms that top-ranked counties in the NEVI scoring framework remain robust across +/-10% variations in the framework weights.
- Figures fig-39 through fig-42 document the equity layer.

Outputs: `data/processed/phase5-county-justice40.csv`, `phase5-zcta-justice40.csv`, `scoring-weight-sensitivity.csv`. Phase 5 produces the Equity Score, which carries the heaviest weight (0.40) in the NEVI scoring framework.

---

## Integration Logic — The NEVI Scoring Framework

The extensions connect through a logical dependency chain, and they converge on a single deliverable: the NEVI Priority Score, a weighted composite that translates analytical findings into a ranked list of all 100 NC counties with defensible dollar allocations.

```
NEVI Priority Score(county) = 0.40 x Equity_Score
                            + 0.35 x Utilization_Score
                            + 0.25 x Cost_Effectiveness_Score
```

- **Equity Score (0.40)** from Phase 5 (Justice40 share) + Phase 3 (intra-county Gini). The 0.40 weight is aligned with the federal Justice40 mandate.
- **Utilization Score (0.35)** from Phase 1 (validated BEV forecasts with the 4-5% underprediction buffer) + Phase 2 (BEVs-per-port across all charging levels) + Phase 3 (sub-county density).
- **Cost-Effectiveness Score (0.25)** from Phase 4 (workplace-vs-residential efficiency, net commuter demand sizing).

Phase 1 established confidence in the forecasting methodology. Phase 2 provided the complete infrastructure baseline that Phases 3, 4, and 5 all require. Phases 3, 4, and 5 operate at different analytical scales — sub-county spatial, cross-county workplace, tract-level equity — but complement each other to form a triple-layer analytical model on top of the baseline county-level gap analysis. See `frameworks/analytical-pipeline.md` for the full pipeline diagram and data flow matrix, and `data/processed/scoring-framework-final.csv` for the final ranked county output.

---

## Methodological Innovation Summary

> **Summary version:** See [PROJECT-BRIEF.md](PROJECT-BRIEF.md) for the condensed project brief. This section provides the expanded rationale for each innovation.

Several analytical innovations distinguish this project from typical EV infrastructure studies:

**County-level granularity over 82 months.** All 100 NC counties across nearly seven years of monthly observations, enabling time series forecasting that captures heterogeneous adoption trajectories rather than assuming uniform statewide trends.

**Connector-level infrastructure detail with full-coverage AFDC pull.** The supply-side analysis operates on 6,145 individual charging connectors across all levels and access types, rather than a DCFC-only extract. This enables capacity-weighted analysis accounting for charging power levels — a 250kW DCFC serves far more vehicles daily than a 7kW Level 2 charger — and ensures that employment centers dominated by L2 infrastructure are not systematically understated.

**Triple-lens decomposition of the county-level gap.** Phase 3 (sub-county ZIP-level spatial), Phase 4 (cross-county workplace demand via LEHD LODES), and Phase 5 (tract-level Justice40 equity) decompose the county-level gap along three independent dimensions, producing insights that county-only analyses cannot see (Theil 84.5% within-county, 859,260 workplace demand events, 43% of NC tracts Justice40-designated).

**Dual-dimension demand model.** Combining residential BEV registrations with workplace commuting flows creates a more complete demand picture. Employment centers serve both residents and net inbound commuters; bedroom communities primarily serve residents. This distinction drives infrastructure type allocation.

**Validation-first approach.** Explicit out-of-sample forecast validation (MAPE 4.34%, 69.00% underprediction) before any policy recommendation is made. Most applied infrastructure studies deploy forecasts without validation, assuming historical fit guarantees future accuracy. Here, the validation results directly inform how forecasts are applied — with a 4-5% upward buffer in the Utilization Score.

**Prescriptive scoring framework with sensitivity analysis.** The five phases converge on a weighted scoring equation whose component weights are defended by federal policy context (Justice40 = 0.40), data-driven confidence (validated forecasts = 0.35), and analytical support (workplace efficiency = 0.25), and whose top-ranked counties are shown to be robust across +/-10% weight variations.

---

## Conclusion

EV Pulse NC addresses how North Carolina should allocate $109 million in NEVI Formula Program funding to maximize equity, utilization, and cost-effectiveness. The baseline analysis established a comprehensive county-level understanding of the demand-supply gap. This semester's five extensions validated forecast accuracy (Phase 1), rebuilt the infrastructure baseline with full-coverage AFDC data (Phase 2), decomposed the gap through sub-county (Phase 3), workplace (Phase 4), and equity (Phase 5) lenses, and converged on a prescriptive NEVI scoring framework that produces a ranked list of all 100 NC counties with defensible dollar allocations.

The project's methodological innovations — temporal depth, connector-level granularity with full-coverage AFDC data, triple-lens decomposition, dual-dimension demand modeling, validation-first forecasting, and the prescriptive scoring framework — collectively provide stakeholders with actionable insights at multiple scales: statewide trends for policy, county-level forecasts for regional planning, ZIP code detail for site selection, workplace demand sizing for employment centers, and Justice40 equity overlays for federal compliance. Two extensions are preserved as post-capstone roadmap items: Phase 6 (Buffer Analysis) for visual "charging desert" identification and Phase 7 (NCDOT NEVI Corridor Validation) for methodology validation against NCDOT's planned deployments.

---

**Project Team:**
Wolfgang Sanyer<BR>
MBA Candidate, Business & Data Analytics Concentration<BR>
Fayetteville State University

**Faculty Advisor:** Dr. Majed Al-Ghandour<BR>
**Course:** BIDA 670 - Advanced Analytics Capstone<BR>
**Semester:** Spring 2026
