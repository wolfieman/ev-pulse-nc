# EV Pulse NC - Analytical Pipeline Architecture

**Project:** EV Pulse NC — BIDA 670 Advanced Analytics Capstone
**Author:** Wolfgang Sanyer, Fayetteville State University
**Advisor:** Dr. Majed Al-Ghandour
**Date:** April 2026 (last updated)

---

## Purpose

This document maps the complete analytical pipeline for the EV Pulse NC capstone project as a network flow. It shows how raw data transforms into defensible NEVI funding recommendations through seven phases, three analytical lenses, and a prescriptive scoring framework.

The pipeline answers one question: **Where should North Carolina invest its federal NEVI dollars to maximize equity, utilization, and cost-effectiveness?**

---

## Pipeline Network Flow

```
 =============================================================================
 ||                    EV PULSE NC - ANALYTICAL PIPELINE                     ||
 =============================================================================

 FOUNDATION LAYER (Complete)
 ===========================

  +----------------------------------+    +----------------------------------+
  |  PHASE 1: DEMAND SIDE            |    |  PHASE 2: SUPPLY SIDE            |
  |  Predictive Validation           |    |  AFDC Infrastructure Data        |
  |  [COMPLETE]                      |    |  [COMPLETE]                      |
  |                                  |    |                                  |
  |  SAS Model Studio BEV forecasts  |    |  NREL API: 1,985 NC stations     |
  |  MAPE: 4.34%                     |    |  6,145 connectors                |
  |  Bias: 69.00% underprediction    |    |  All levels: L1, L2, DCFC        |
  |  8 publication figures           |    |  267 cities / 358 ZIP codes      |
  |                                  |    |                                  |
  |  Answers: "How many EVs will     |    |  Answers: "How many chargers     |
  |   NC have?"                      |    |   does NC have?"                 |
  +----------------+-----------------+    +----------------+-----------------+
                   |                                      |
                   |   Validated BEV         Complete      |
                   |   forecasts by          infrastructure |
                   |   county                baseline      |
                   |                                      |
                   v                                      v
          +-------+--------------------------------------+--------+
          |                                                       |
          |                  GAP ANALYSIS                         |
          |              (Convergence Point)                      |
          |                                                       |
          |  Demand (validated BEV forecasts) vs.                 |
          |  Supply (complete infrastructure baseline)            |
          |                                                       |
          |  Core question: "Where does supply fall               |
          |   short of demand?"                                   |
          |                                                       |
          +------+-------------------+-------------------+--------+
                 |                   |                   |
                 |                   |                   |
   WHERE?        |       WHO/WHEN?   |       EQUITY?     |
                 v                   v                   v
 +--------------+--+  +-------------+---+  +------------+-----+
 | PHASE 3         |  | PHASE 4         |  | PHASE 5          |
 | ZIP Code        |  | CTPP Workplace  |  | CEJST Equity     |
 | Analysis        |  | Charging        |  | Analysis         |
 | [COMPLETE]      |  | [COMPLETE]      |  | [COMPLETE]       |
 |                 |  |                 |  |                  |
 | Sub-county      |  | Census commute  |  | Justice40        |
 | infrastructure  |  | data sizes      |  | disadvantaged    |
 | mapping using   |  | workplace       |  | community        |
 | AFDC ZIP codes  |  | charging demand |  | overlay          |
 |                 |  |                 |  |                  |
 | ~120 urban ZIPs |  | Top 15 employ-  |  | NEVI: 40% of     |
 | in top 10       |  | ment centers,   |  | benefits to      |
 | counties        |  | bidirectional   |  | disadvantaged    |
 |                 |  | flow analysis   |  | communities      |
 |                 |  |                 |  |                  |
 | Complete        |  | Complete        |  | Complete         |
 +--------+--------+  +--------+--------+  +--------+---------+
          |                     |                     |
          | Utilization         | Cost-Effectiveness  | Equity
          | Score               | Score               | Score
          | + Equity Score      |                     |
          |                     |                     |
          v                     v                     v
 +--------+---------------------+---------------------+---------+
 |                                                              |
 |                  SCORING FRAMEWORK                           |
 |                 (Integration Layer)                           |
 |                                                              |
 |  NEVI Priority Score(county) =                               |
 |      0.40 x Equity_Score                                     |
 |    + 0.35 x Utilization_Score                                |
 |    + 0.25 x Cost_Effectiveness_Score                         |
 |                                                              |
 +------------------------------+-------------------------------+
                                |
                                | Ranked list of
                                | 100 NC counties
                                v
                 +--------------+--------------+
                 |                             |
                 |   NEVI COUNTY RANKINGS      |
                 |   Defensible dollar         |
                 |   allocations               |
                 |                             |
                 +-----+--------------+--------+
                       |              |
          OPTIONAL     |              |     OPTIONAL
                       v              v
         +-------------+--+  +--------+----------+
         | PHASE 6        |  | PHASE 7            |
         | Buffer         |  | NCDOT NEVI         |
         | Analysis       |  | Corridor           |
         | [OPTIONAL]     |  | Validation         |
         |                |  | [OPTIONAL]         |
         | GIS coverage   |  |                    |
         | zones around   |  | Compare scoring    |
         | stations —     |  | output vs. NCDOT   |
         | identifies     |  | planned deploy-    |
         | "charging      |  | ments              |
         | deserts"       |  |                    |
         +----------------+  +--------------------+
```

---

## Phase Summary

| Phase | Priority | Topic | Status | Time Est. | Key Deliverable | Scoring Component |
|:-----:|:--------:|-------|--------|-----------|-----------------|-------------------|
| **1** | 1 | Predictive Validation | **COMPLETE** | -- | 8 publication figures, MAPE 4.34%, bias analysis | Utilization Score (validated BEV forecasts) |
| **2** | 2 | AFDC Infrastructure Data | **COMPLETE** | -- | 1,985 stations, 6,145 connectors, all levels/access types | Utilization Score (BEVs-per-port ratios) |
| **3** | 3 | ZIP Code Analysis (WHERE) | **COMPLETE** | Mar 2026 | Top 20 underserved ZIPs, Wake County heat map, Gini coefficient | Utilization Score + Equity Score |
| **4** | 4 | CTPP Workplace Charging (WHO/WHEN) | **COMPLETE** | Mar 2026 | Top 10 employment centers, commuter flow map | Cost-Effectiveness Score |
| **5** | 5 | CEJST Equity Analysis (EQUITY) | **COMPLETE** | Apr 2026 | CEJST tract-level Justice40 overlay, county + ZCTA disadvantaged community shares, climate sensitivity, weight sensitivity, figures 39–42 | Equity Score (weight: 0.40) |
| **6** | 6 | Buffer Analysis | Future Direction | — | Coverage zone maps, "charging desert" identification | Post-capstone roadmap |
| **7** | 7 | NCDOT NEVI Corridor Validation | Future Direction | — | Comparison of scores vs. NCDOT planned deployments | Post-capstone roadmap |

---

## Data Flow Matrix

This table shows what each phase produces and what downstream phases consume.

| Source Phase | Data Produced | Consumed By | Purpose |
|:------------:|---------------|-------------|---------|
| **Phase 1** | Validated BEV forecasts by county (Jul-Oct 2025 holdout) | Gap Analysis, Phase 3, Scoring Framework | Demand-side numerator for BEVs-per-port ratios |
| **Phase 1** | Underprediction bias estimate (69.00%, +18.22 vehicles) | Scoring Framework | 4-5% upward adjustment buffer in utilization scores |
| **Phase 2** | 1,985 station records with ZIP, lat/lon, facility type | Gap Analysis, Phase 3, Phase 4, Phase 6, Scoring Framework | Supply-side denominator; spatial distribution baseline |
| **Phase 2** | Connector counts by level (L1, L2, DCFC) per station | Gap Analysis, Scoring Framework | Port-level utilization ratios by charging level |
| **Phase 2** | Facility-type classification (workplace, retail, parking) | Phase 4 | Identifies existing workplace vs. residential infrastructure |
| **Gap Analysis** | County-level demand-supply gap (BEVs minus ports) | Phase 3, Phase 4, Phase 5, Scoring Framework | Baseline gap that lenses decompose and refine |
| **Phase 3** | ZIP-level infrastructure density within top 10 counties | Scoring Framework | Utilization Score (sub-county granularity) |
| **Phase 3** | Gini coefficient of intra-county infrastructure inequality | Scoring Framework | Equity Score (identifies within-county disparities) |
| **Phase 3** | Top 20 underserved ZIPs | Scoring Framework | Priority targets for NEVI deployment |
| **Phase 4** | Workplace charging demand by employment center | Scoring Framework | Cost-Effectiveness Score (15 EVs/port efficiency) |
| **Phase 4** | Bidirectional commuter flows for top 15 counties | Scoring Framework | Adjusts county-level demand to include non-residents |
| **Phase 5** | Justice40 disadvantaged community overlay | Scoring Framework | Equity Score (heaviest weight: 0.40) |
| **Phase 5** | Community-level equity flags | Scoring Framework | NEVI compliance (40% of benefits to disadvantaged communities) |
| **Scoring** | Ranked list of 100 NC counties with NEVI scores | Phase 7 (optional) | Validation against NCDOT planned deployments |
| **Phase 6** | Coverage zone maps (optional) | Final paper | Visual enhancement for "charging deserts" |
| **Phase 7** | Score-vs-deployment comparison (optional) | Final paper | Methodology validation |

---

## Scoring Framework Detail

### The Equation

```
NEVI Priority Score(county) = 0.40 x Equity_Score
                            + 0.35 x Utilization_Score
                            + 0.25 x Cost_Effectiveness_Score
```

**Source:** Dr. Al-Ghandour's proposal feedback -- "clearly defining prioritization criteria (equity, utilization, cost-effectiveness) within a scoring framework to translate findings into defensible NEVI allocation decisions."

### Component Definitions

| Component | Weight | Source Phases | Key Metrics |
|-----------|:------:|:------------:|-------------|
| **Equity Score** | 0.40 | Phase 5 + Phase 3 | Justice40 disadvantaged community %, Gini coefficient, rural access gap, zero-infrastructure flag |
| **Utilization Score** | 0.35 | Phase 1 + Phase 2 + Phase 3 | BEVs-per-port ratio across all charging levels (L1, L2, DCFC), forecast growth rate, 4-5% underprediction buffer |
| **Cost-Effectiveness Score** | 0.25 | Phase 4 | Workplace commuter demand, workplace efficiency, population density |

### Weights Rationale

- **Equity-heavy (0.40):** Aligned with federal Justice40 mandate requiring 40% of benefits to disadvantaged communities
- **Utilization (0.35):** Largest data-driven component; validated BEV forecasts provide highest analytical confidence
- **Cost-effectiveness (0.25):** Workplace commuter demand and infrastructure efficiency; NC statewide 15.4 BEVs/port exceeds IEA global benchmark of ~10
- **Sensitivity analysis:** Top-ranked counties should remain robust across +/-10% weight variations

### Output

Ranked list of top 10 North Carolina counties (by BEV registration count, capturing 73% of statewide BEV fleet) with:
- Individual component scores (Equity, Utilization, Cost-Effectiveness)
- Composite NEVI Priority Score
- Weight sensitivity analysis across ±10pp equity variation

**Future work:** Extend to all 100 counties; add dollar allocation proportional to score; add confidence intervals on composite scores.

---

## Current Status

### Completed

| Phase | Completion Date | Key Results |
|-------|----------------|-------------|
| **Phase 1: Predictive Validation** | Feb 2026 | MAPE 4.34%, 69.00% underprediction bias, 8 publication figures (600 DPI, PDF) |
| **Phase 2: AFDC Infrastructure Data** | Feb 2026 | Complete API download: 1,985 stations, 6,145 connectors, L1/L2/DCFC, all access types, 267 cities, 358 ZIPs |
| **Phase 3: ZIP Code Analysis** | Mar 2026 | 134 ZIPs in 10 counties analyzed; Gini 0.566 statewide; Theil decomposition: 84.5% within-county inequality; 34 publication figures (fig-08 to fig-34); scoring framework skeleton (9/17 columns populated) |
| **Phase 4: CTPP Workplace Charging** | Mar 2026 | LEHD/LODES employment centers, commuter flow analysis, workplace-vs-residential efficiency comparison, figures fig-35 to fig-38 |
| **Phase 5: CEJST Equity Analysis** | Apr 2026 | CEJST tract-level Justice40 overlay, county + ZCTA Justice40 shares, climate-subset sensitivity, weight sensitivity, figures fig-39 to fig-42 |

### Future Directions

| Phase | Value |
|-------|-------|
| **Phase 6: Buffer Analysis** | Visual identification of "charging deserts" by distance — preserved for post-capstone roadmap |
| **Phase 7: NCDOT Validation** | Validates methodology against NCDOT's planned NEVI deployments — preserved for post-capstone roadmap |

### Critical Path

The minimum viable analysis requires Phases 1-5 plus the Scoring Framework:

```
Phase 1 (done) + Phase 2 (done) --> Gap Analysis --> Phases 3, 4, 5 --> Scoring --> Rankings
```

All core phases complete.

---

## Paper Alignment

This table maps each pipeline phase to the corresponding section of the BIDA 670 research paper.

| Pipeline Phase | Paper Section | Content Contribution |
|----------------|---------------|---------------------|
| **Phase 1: Predictive Validation** | Methods + Results | Methods: model selection (ESM/ARIMA/UCM), holdout design, accuracy metrics. Results: MAPE 4.34%, bias analysis, confidence interval coverage, 8 publication figures |
| **Phase 2: AFDC Infrastructure** | Data Description | Infrastructure landscape: 1,985 stations across L1/L2/DCFC, access type distribution, geographic coverage (267 cities, 358 ZIPs), comparison vs. prior DCFC-only extract |
| **Gap Analysis** | Results | County-level demand-supply comparison, identification of highest-gap counties, BEVs-per-port ratios |
| **Phase 3: ZIP Code Analysis** | Results | Sub-county gap analysis: top 20 underserved ZIPs, Wake County heat map, Gini coefficient for intra-county inequality |
| **Phase 4: CTPP Workplace** | Results | Workplace charging demand: top 10 employment centers, commuter flow analysis, NC statewide 15.4 BEVs/port vs IEA ~10 benchmark |
| **Phase 5: CEJST Equity** | Results + Discussion | Results: CEJST tract-level Justice40 overlay, county + ZCTA disadvantaged community shares, climate-subset sensitivity, weight sensitivity. Discussion: policy implications for equitable NEVI deployment |
| **Scoring Framework** | Discussion | NEVI recommendations: weighted scoring equation, ranked county list (top 10), weight sensitivity analysis |
| **Phase 7: NCDOT Validation** | Discussion | Methodology validation: do our equity-weighted scores independently recommend the same locations NCDOT chose in their Feb 18, 2026 rural deployment shift? |

---

## Related Framework Documents

| Document | Phase | Description |
|----------|:-----:|-------------|
| [validation-analysis.md](./validation-analysis.md) | 1 | ARIMA/ESM/UCM validation framework, out-of-sample accuracy metrics |
| [zip-code-analysis.md](./zip-code-analysis.md) | 3 | Sub-county spatial analysis framework, data availability constraints |
| [ctpp-analysis.md](./ctpp-analysis.md) | 4 | Workplace charging demand framework, CTPP data structure, remote work adjustments |
| [afdc-api-analysis.md](./afdc-api-analysis.md) | 2 | NREL API technical specifications, query parameters |
| [afdc-dataset-reference.md](./afdc-dataset-reference.md) | 2 | AFDC dataset source, vintage, current counts |
| [afdc-data-structure.md](./afdc-data-structure.md) | 2 | AFDC schema reference (76 fields), infrastructure classification |
| [stakeholder-value-analysis.md](./stakeholder-value-analysis.md) | All | Stakeholder value of the delivered scoring framework |

---

## Document Metadata

- **Created:** February 26, 2026
- **Last Updated:** April 2026
- **Version:** 1.1
- **Repository:** `C:\projects\ev-pulse-nc`
- **Purpose:** Standalone reference for BIDA 670 capstone paper and advisor review
