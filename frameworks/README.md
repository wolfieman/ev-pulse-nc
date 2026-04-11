# EV Pulse NC - Analytical Frameworks Directory

**Purpose:** This directory contains conceptual frameworks and decision analyses for the EV Pulse NC BIDA 670 capstone project. These documents define WHAT to analyze and WHY, not HOW to implement.

**Status:** All 5 phases complete (Apr 2026)
**Scope:** Research priorities, decision trees, integration strategies
**Implementation:** None—these are conceptual roadmaps only

---

## Directory Organization

### Full Frameworks (Markdown)

Comprehensive decision frameworks with trade-off analyses, stakeholder assessments, and integration strategies.

| Framework | Priority | Size | Status | Description |
|-----------|----------|------|--------|-------------|
| **[afdc-dataset-reference.md](./afdc-dataset-reference.md)** | #2 | — | ✅ Current | AFDC dataset source, vintage, file paths, current counts (1,985 stations / 6,145 connectors / 267 cities / 358 ZIPs), refresh cadence, downstream usage |
| **[afdc-data-structure.md](./afdc-data-structure.md)** | #2 | — | ✅ Current | Field-level schema reference for the 76-column AFDC station-level CSV; identification, geography, charging, facility, temporal fields |
| **[stakeholder-value-analysis.md](./stakeholder-value-analysis.md)** | All | — | ✅ Current | Stakeholder value of the delivered NEVI scoring framework (NEVI admins, county planners, private operators, academic, public/Justice40 communities) |
| **[analytical-pipeline.md](./analytical-pipeline.md)** | All | — | ✅ Complete | Project analytical pipeline architecture: foundation (demand + supply) → gap analysis → three lenses (ZIP, CTPP, equity) → scoring framework → NEVI rankings |

### Analysis Notes (Text)

Shorter conceptual analyses and decision summaries from expert agent research.

| Analysis | Priority | Size | Status | Description |
|----------|----------|------|--------|-------------|
| **[validation-analysis.md](./validation-analysis.md)** | #1 | 3.5K | ✅ Complete | ARIMA validation framework (July-Oct 2025 BEV data), out-of-sample accuracy testing |
| **[zip-code-analysis.md](./zip-code-analysis.md)** | #2 | 11K | ✅ Complete | Sub-county spatial analysis framework, data availability constraints (NCDOT county-only), sparsity challenges |
| **[ctpp-analysis.md](./ctpp-analysis.md)** | #3 | 15K | ✅ Complete | Workplace charging demand framework using Census Transportation Planning Products (2016-2020 ACS), remote work adjustments |
| **[afdc-api-analysis.md](./afdc-api-analysis.md)** | #5 | 1.9K | ✅ Complete | NREL API technical specifications, rate limits, query parameters |

---

## Priority Map

EV Pulse NC research priorities and phases (aligned Feb 26, 2026):

> **Note:** Priority numbers were realigned to match phase numbers on Feb 26, 2026. Old Priority #5 (AFDC) moved to #2; old Priorities #2-4 shifted to #3-5. Framework filenames retain original numbering for traceability.

| Phase | Priority | Topic | Status | Key Decision |
|:-----:|:--------:|-------|--------|--------------|
| **1** | **1** | Predictive Analysis Validation | **Phase 1 Complete** | MAPE 4.34%, 69.00% underprediction, 8 publication figures |
| **2** | **2** (was #5) | AFDC Infrastructure Data | **Phase 2 Complete** | Complete API dataset replaces DCFC-only extract (1,985 stations, all levels) |
| **3** | **3** (was #2) | ZIP Code Analysis | ✅ Framework Complete ([zip-code-analysis.md](./zip-code-analysis.md)) | Infrastructure-only (adoption data unavailable at ZIP level) |
| **4** | **4** (was #3) | CTPP Commuting Data | ✅ Framework Complete ([ctpp-analysis.md](./ctpp-analysis.md)) | Top 15 employment centers, 30% workplace charging assumption |
| **5** | **5** (was #4) | CEJST Equity Analysis | **Phase 5 Complete** | CEJST Justice40 tract overlay; county + ZCTA Justice40 shares; climate sensitivity; weight sensitivity; figures 39–42 |
| **6** | **6** | Buffer Analysis | **Future Direction** | Coverage zones — preserved for post-capstone roadmap |
| **7** | **7** | NCDOT NEVI Corridor Validation | **Future Direction** | Compare scoring framework output vs. NCDOT planned deployments — post-capstone roadmap |

### Phase 5: Prescriptive Scoring Framework (Integration Layer)

**Source:** Dr. Al-Ghandour's proposal feedback — "clearly defining prioritization criteria (equity, utilization, cost-effectiveness) within a scoring framework to translate findings into defensible NEVI allocation decisions."

**Formula:**
```
NEVI Priority Score(county) = w1 × Equity_Score + w2 × Utilization_Score + w3 × Cost_Effectiveness_Score
```

| Component | Source Extension | Metrics |
|-----------|----------------|---------|
| **Equity_Score** | CEJST Justice40 equity (Phase 5) + Phase 3 ZIP analysis | Justice40 disadvantaged community %, Gini coefficient, rural access gap, zero-infrastructure flag |
| **Utilization_Score** | Validation (#1) + AFDC complete baseline (#2) | BEVs/port ratio across all charging levels (L1, L2, DCFC), 4-5% underprediction buffer |
| **Cost_Effectiveness_Score** | CTPP workplace charging (#4) | Workplace efficiency (15 vs 7.5 BEVs/port), commuter demand sizing, population density |

**Weights:** Literature-driven from DOE/FHWA NEVI guidance (equity-heavy per Justice40: ~0.40/0.35/0.25) + sensitivity analysis showing top counties robust across weight variations.

**Output:** Ranked list of top 10 NC counties (73% of statewide BEV fleet) with component scores and weight sensitivity analysis. Framework designed for statewide extension to all 100 counties.

---

## Framework Usage

### How to Use These Documents

1. **For Planning:** Read decision frameworks BEFORE starting implementation work
2. **For Integration:** Use integration analyses to understand how priorities connect
3. **For Stakeholders:** Reference stakeholder value matrices when writing papers/presentations
4. **For Methodology:** Cite conceptual frameworks in research methods sections

### What These Are NOT

- ❌ **NOT implementation guides** - No code, no step-by-step instructions
- ❌ **NOT scheduled timelines** - No execution dates or resource allocation
- ❌ **NOT final decisions** - These are decision SUPPORT tools, not mandates

### What These ARE

- ✅ **Decision architecture** - Options, trade-offs, recommendations
- ✅ **Analytical roadmaps** - What questions to ask, what data to consider
- ✅ **Integration strategies** - How priorities connect and enhance each other
- ✅ **Risk assessments** - What could go wrong, how to mitigate

---

## Key Insights by Priority

### Priority #1 / Phase 1: Validation (COMPLETE)
- **Core Question:** How accurate are SAS Model Studio forecasts for July-Oct 2025?
- **Result:** MAPE 4.34% (strong validation), but systematic underprediction detected
- **Key Finding:** 69.00% of forecasts fell below actual values (Bias: +18.22 vehicles)
- **Model Distribution:** ESM (82 counties), ARIMA (13 counties), UCM (5 counties)
- **95% CI Coverage:** 75.50% (below nominal 95% due to bias)
- **Deliverables:** 8 publication-quality figures (600 DPI, PDF exports)

### Priority #2 / Phase 2: AFDC Infrastructure Data (COMPLETE)
- **Core Question:** Do we have complete infrastructure coverage for gap analysis?
- **Critical Finding:** Old file was a DCFC-only, public-only, connector-level extract (355 stations); the Feb 2026 API download provides complete coverage (1,985 stations across L1, L2, DCFC, all access types)
- **Key Insight:** Complete dataset enables accurate BEVs-per-port ratios, ZIP-level infrastructure mapping, and facility-type classification for workplace charging analysis
- **Background:** The old file's "July 2024" filename was misleading — it contained data through Dec 2025, so no temporal comparison was possible. The real gap was completeness, not currency.
- **Integration:** Enhances Priority #3 (ZIP-level spatial distribution), validates Priority #4 (station types for workplace charging), enables Priority #6 (coverage zones require all station locations), feeds Scoring Framework (utilization scores across all charging levels)

### Priority #3 / Phase 3: ZIP Code Analysis
- **Core Question:** Can we analyze sub-county infrastructure gaps?
- **Key Constraint:** NCDOT doesn't publish ZIP-level BEV data (only county-level)
- **Key Insight:** Infrastructure-only ZIP analysis possible (AFDC has ZIP codes), adoption requires allocation heuristics
- **Expected Finding:** 400-500 ZIPs with <10 BEVs (50-60% of 800 ZIPs) — severe sparsity

### Priority #4 / Phase 4: CTPP Workplace Charging
- **Core Question:** Does workplace demand differ from residential patterns?
- **Key Constraint:** CTPP data is 8-10 years old (2012-2016 ACS), requires remote work adjustments
- **Key Insight:** Workplace infrastructure 3x more efficient (15 EVs/port) than residential (7.5 EVs/port) but smaller absolute gap
- **Recommendation:** Focus on top 15 employment centers, not all 100 counties

### Priority #5 / Phase 5: CEJST Equity Analysis
- **Core Question:** Which communities face inequitable access to EV charging?
- **Key Framework:** CEJST tract-level Justice40 designations — 40% of benefits to disadvantaged communities
- **Status:** Complete (Mar–Apr 2026). Delivered: county + ZCTA Justice40 shares, climate-subset sensitivity, weight sensitivity, publication figures 39–42

### Priority #7 / Phase 7: NCDOT NEVI Corridor Validation (OPTIONAL)
- **Source:** Dr. Al-Ghandour introduced the NCDOT NEVI Mapping Tool during Week 6 check-in (Feb 20, 2026)
- **Tool:** https://experience.arcgis.com/experience/a1e1459fffee4ccbafaf888f838dcac6/page/NCDOT-NEVI-Mapping-Tool
- **What it is:** ArcGIS map of NCDOT's planned NEVI station deployments along Alternative Fuel Corridors (AFCs)
- **Breaking development (Feb 18, 2026):** NCDOT announced shift from corridor-only to rural/community deployment — from 50 corridor stations to 16 rural locations. RFP coming late March 2026.
- **Alignment:** This is NOT part of the three proposed extensions. It's a **validation benchmark** — do our equity-weighted scores recommend the same locations NCDOT just chose?
- **Work estimate:** 3-5 hours if folded into scoring framework as validation layer
- **Professor offering:** Dr. Al-Ghandour (former DOT/CDOT) offered to help obtain NCDOT planning data directly
- **Strategic value:** If our scoring framework independently recommends rural deployment, it validates both our methodology AND NCDOT's Feb 18 policy shift

---

## Cross-Priority Integration

### How Priorities Connect

```
Phase 1: Priority #1 (Validation) ✅ COMPLETE
    ↓ validates BEV forecasts
    ↓
Phase 2: Priority #2 (AFDC Data) ✅ COMPLETE ← complete infrastructure baseline (1,985 stations, all levels)
    ↓ provides supply-side foundation
    ↓
Phase 3: Priority #3 (ZIP) + Phase 4: Priority #4 (CTPP) ← use Feb 2026 complete spatial data
    ↓ identify gaps → feed into
    ↓
Scoring Framework ← integrates equity + utilization + cost-effectiveness
    ↓ produces ranked county allocations
    ↓
Phase 7: Priority #7 (NCDOT Corridor Validation) ← OPTIONAL: compare scores vs. NCDOT planned sites
Phase 6: Priority #6 (Buffer) ← requires Feb 2026 complete station locations
```

### Synergy Analysis

**Scenario 1:** Use complete AFDC data (#2) but NOT ZIP (#3) or CTPP (#4)
- Value: 40% of potential impact (complete infrastructure baseline, but county-level only)

**Scenario 2:** Pursue ZIP (#3) + CTPP (#4) but with incomplete DCFC-only data
- Value: 60% of potential impact (sub-county insights, but missing L1/L2 stations and non-public access points)

**Scenario 3:** Use complete AFDC data (#2) AND pursue ZIP (#3) + CTPP (#4)
- Value: **100% of potential impact** (complete all-levels baseline + spatial granularity)

---

## Actual Outcome (Priority #5)

Based on data investigation (Feb 2026) — original 3-agent framework analysis has been superseded by findings:

### Result: Complete API Dataset Replaces Incomplete Extract

**What happened:**
- The old file (`afdc-charging-stations-connector-2024-07.csv`) was NOT a July 2024 full snapshot — it was a DCFC-only, public-only, connector-level extract with data through Dec 2025
- The Feb 2026 API download (`afdc-charging-stations-connector-2026-02.csv`) is a complete station-level dataset: 1,985 stations, all charging levels (L1, L2, DCFC), all access types
- Both files represent roughly the same point in time — the "6-month staleness gap" never existed

**Why this matters:**
- The old extract covered only 355 DCFC stations; the complete dataset covers 1,985 stations across all levels
- Full coverage enables accurate BEVs-per-port ratios that account for ALL charging infrastructure, not just fast chargers
- ZIP-level infrastructure mapping now includes L2 workplace/residential chargers (critical for Priority #3 workplace charging analysis)
- Facility-type classification (workplace, retail, parking, etc.) now available across all station types

**Effort:** 2 hours (API query + validation of completeness)

**Deliverables:**
1. Complete infrastructure baseline: 1,985 NC stations across L1, L2, and DCFC
2. All access types included (public, private, workplace, fleet)
3. Facility-type classification for workplace charging integration
4. ZIP-level station distribution for spatial analysis

**Integration:**
- Priority #1 (Validation): Independent — BEV forecast validation unaffected
- Priority #2 (ZIP): Enhanced by complete spatial distribution across all levels
- Priority #3 (CTPP): Facility-type data enables workplace vs. residential infrastructure classification
- Priority #6 (Buffer): Complete station locations enable accurate coverage zone analysis
- Scoring Framework: BEVs/port ratios now calculated against full infrastructure inventory

---

## Risk Assessment Summary

### Risks of Updating Infrastructure Data

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Spatial join errors | Medium | High | Re-validate spatial joins by spot-checking 10 stations against Google Maps and confirming county assignments match geocoded coordinates |
| API key approval delay | Low | Medium | Apply immediately (instant approval typical) |
| Station count unexpected | Low | Low | Document federal funding surge |
| Time overrun (>2 hrs) | Medium | Medium | Budget 3-4 hours buffer |

### Risks of Using Incomplete (DCFC-Only) Data

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| BEVs/port ratios exclude L1/L2 infrastructure | High | High | Use complete Feb 2026 API dataset (1,985 stations vs. 355 DCFC-only) |
| Workplace charging analysis misses L2 chargers | High | Very High | Complete dataset includes facility-type classification across all levels |
| ZIP-level gap analysis undercounts infrastructure | High | High | Complete dataset covers all access types and charging levels |
| Policy recommendations misallocate NEVI funds | Medium | Very High | Full infrastructure inventory prevents overstatement of gaps |

**Conclusion:** The incomplete DCFC-only extract (355 stations) is retained for reference but should NOT be used for analysis. The complete Feb 2026 API dataset (1,985 stations) is the authoritative infrastructure baseline for all downstream priorities.

---

## Technical Specifications

### AFDC API Details

**Endpoint:** `https://developer.nlr.gov/api/alt-fuel-stations/v1.json`

**NC Query Parameters:**
- `state=NC`
- `fuel_type=ELEC`
- `status=E` (operational stations)
- `limit=all`

**Rate Limits:** 1,000 requests/hour (rolling 60-min window)
**EV Pulse NC Need:** 1 request per snapshot (well within limits)
**API Key:** Free, instant approval at https://developer.nlr.gov/signup/

**Key Fields (50+ total):**
- `id`, `station_name`, `zip`, `latitude`, `longitude`
- `ev_level2_evse_num`, `ev_dc_fast_num`
- `facility_type` (for workplace classification)
- `ev_network` (Tesla, ChargePoint, Electrify America, etc.)
- `date_last_confirmed`, `open_date` (temporal tracking)

---

## Data Currency Standards

### Acceptable Staleness Thresholds (EV Pulse NC)

| Data Type | Max Staleness | Current Status | Action Required |
|-----------|---------------|----------------|-----------------|
| **Demand (BEV registrations)** | 6 months | ✅ 3 months (Oct 2025 actuals, as of Feb 2026) | None |
| **Supply (Infrastructure)** | 3 months | ✅ Current (Feb 2026 API, 1,985 stations, all levels) | None |
| **Demographics** | 5 years | ✅ 4 years (ACS 2018-2022 5-year estimates) | None |
| **Commuting Patterns** | 10 years | ✅ 5 years (LEHD LODES 2021, most recent public release) | None |
| **Equity Designations** | 5 years | ✅ Current (CEJST v2.0, December 2024 release) | None |

**Rationale:** All data types meet or exceed their staleness thresholds. Infrastructure data is current and complete (Feb 2026 full API download). LEHD LODES 2021 replaces the originally planned CTPP 2016-2020; a 0.85 remote-work multiplier (Barrero/Bloom/Davis 2023) adjusts for post-COVID commuting shifts. Traffic Volumes (HPMS) removed — not used by this project.

---

## Document Metadata

### Framework Authorship

All frameworks created by expert agent analysis (Jan 30, 2026) for EV Pulse NC BIDA 670 capstone project.

**Agent Contributors:**
- Decision Framework Agent (a18649a): 5-node decision tree analysis
- Data Structure Agent (ab08c82): AFDC API research, snapshot comparison methodology
- Stakeholder Value Agent (a6086db): Differential value matrix, integration analysis

### Version Control

- **Created:** January 30, 2026
- **Last Updated:** April 2026
- **Status:** All 5 core phases complete (Phase 1 Validation, Phase 2 AFDC Update, Phase 3 ZIP Analysis, Phase 4 Workplace Charging, Phase 5 CEJST Equity). Phases 6 (Buffer) and 7 (NCDOT Corridor Validation) preserved as Future Directions for the post-capstone roadmap.

### Related Documentation

**Research Files:**
- `/research/ev-pulse-nc/ev-pulse-nc-current-state-analysis.md` - Baseline analysis (82 months BEV data, 355 DCFC-only stations — superseded by Feb 2026 complete API dataset: 1,985 stations across all levels)
- `/research/ev-pulse-nc/ev-pulse-nc-recommendations-RANKED.md` - Original 25 recommendations (pre-SAS Cup removal)
- `/research/ev-pulse-nc/top-priorities.txt` - Post-redefinition top 6 priorities

**Project Repository:**
- `C:\projects\spring-26-bida670-advanced-analytics\` - Root directory
- `C:\projects\spring-26-mba-orchestrator\` - Cross-course hub (templates, prompts, resources)

---

## Questions or Clarifications?

For conceptual questions about these frameworks, refer to:
- Original agent analysis outputs (tool results from Jan 30, 2026 session)
- Project lead: Wolfgang Sanyer

**Note:** These frameworks are living documents. As priorities evolve or new constraints emerge, update frameworks accordingly.
