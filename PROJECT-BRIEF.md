# EV Pulse NC: Project Brief

**Audience:** Dr. Majed Al-Ghandour, BIDA 670 Instructor

---

## Project Overview

EV Pulse NC analyzes the alignment between electric vehicle adoption and public charging infrastructure across all 100 North Carolina counties, and translates the findings into a defensible allocation model for North Carolina's $109 million NEVI Formula Program. The core research question is where NEVI dollars should go to maximize equity, utilization, and cost-effectiveness. The project combines a county-month BEV registration panel (NCDOT, 82 months, 8,200 observations) with a complete AFDC infrastructure baseline, and decomposes both through sub-county, workplace, and equity lenses that feed a prescriptive scoring framework.

---

## Completed Extensions

Five extensions are merged into `main` and collectively form the analytical pipeline that feeds the NEVI scoring framework.

1. **Phase 1 — Predictive Validation.** Out-of-sample testing of SAS Model Studio BEV forecasts against Jul-Oct 2025 NCDOT actuals. Headline accuracy: **MAPE 4.36%**, with **69.0% underprediction** and a +18.36 vehicle mean bias indicating adoption is accelerating faster than historical patterns. Eight publication-quality figures (600 DPI, PDF).
2. **Phase 2 — AFDC Infrastructure Baseline.** Full NREL AFDC API pull replacing the prior DCFC-only public extract. Current baseline: **1,985 stations / 6,145 connectors** across all charging levels (L1, L2, DCFC) and all access types, covering **267 cities / 358 ZIPs** (Feb 2026 pull).
3. **Phase 3 — ZIP Code Analysis.** Sub-county infrastructure decomposition across 134 ZIPs in the top 10 urban counties. Statewide connector Gini **0.805**; a **Theil decomposition attributes 84.5% of spatial inequality to within-county variation**; the gap between Charlotte ZIPs 28202 and 28215 is roughly **250-fold in port density**. Outputs: `phase3-county-gini.csv`, `phase3-theil-decomposition.csv`, `phase3-zip-density.csv`, `phase3-top20-underserved.csv`.
4. **Phase 4 — Workplace Charging (LEHD/LODES).** County-to-county commuting flows built from LEHD LODES OD/WAC tables cross-walked via the LODES geography crosswalk, with ACS income corrections and a Barrero/Bloom/Davis (2023) 0.85 remote-work multiplier. Statewide adjusted workplace demand: **859,260 commuter-based EV charging events**. Mecklenburg (+194,361), Wake (+126,517), and Durham (+89,450) are the dominant net employment centers. Workplace infrastructure serves roughly **15 BEVs/port vs. 7.5 for residential public** — a 2x efficiency finding. Outputs: `phase4-cost-effectiveness.csv`, `phase4-employment-centers.csv`.
5. **Phase 5 — CEJST Equity Overlay.** CEJST v2.0 tract-level Justice40 designations (**934 of 2,170 NC tracts disadvantaged**), overlaid on counties and ZCTAs via area-weighted interpolation. Includes a climate-only subset sensitivity and a weight sensitivity test demonstrating that top-priority counties remain robust across +/-10% weight variations. Outputs: `phase5-county-justice40.csv`, `phase5-zcta-justice40.csv`, `scoring-weight-sensitivity.csv`.

---

## The NEVI Scoring Framework

The five phases converge on a prescriptive scoring framework that translates analytical findings into county-level NEVI allocation recommendations:

```
NEVI Priority Score(county) = 0.40 x Equity_Score
                            + 0.35 x Utilization_Score
                            + 0.25 x Cost_Effectiveness_Score
```

- **Equity Score (0.40)** draws from Phase 5 (Justice40 share) and Phase 3 (intra-county Gini). Weight aligned with the federal Justice40 mandate (40% of benefits to disadvantaged communities).
- **Utilization Score (0.35)** draws from Phase 1 (validated BEV forecasts with a 4-5% upward buffer for the systematic underprediction bias), Phase 2 (BEVs-per-port across all levels), and Phase 3 (sub-county density).
- **Cost-Effectiveness Score (0.25)** draws from Phase 4 (workplace-vs-residential efficiency, commuter demand sizing).

The output is a ranked list of all 100 NC counties with component scores, a composite NEVI Priority Score, and proportional NEVI dollar allocations. See `data/processed/scoring-framework-final.csv`.

---

## Future Directions

Two extensions are preserved as post-capstone roadmap items:

- **Phase 6 — Buffer Analysis.** GIS coverage zones around existing stations to visually identify "charging deserts" by drive-time distance.
- **Phase 7 — NCDOT NEVI Corridor Validation.** Compares the scoring framework's recommended county ranking against NCDOT's actual planned NEVI deployments as a methodology validation.

---

## Live References

For the detailed pipeline architecture and scoring framework, see `frameworks/analytical-pipeline.md`. For the live research narrative and paper-in-progress, see `paper/PAPER-NOTES.md`. For the current AFDC dataset reference, see `frameworks/afdc-dataset-reference.md` and `frameworks/afdc-data-structure.md`.

---

**Project Team:**
Wolfgang Sanyer<BR>
MBA Candidate, Business & Data Analytics Concentration<BR>
Fayetteville State University

**Faculty Advisor:** Dr. Majed Al-Ghandour<BR>
**Course:** BIDA 670 - Advanced Analytics Capstone<BR>
**Semester:** Spring 2026
