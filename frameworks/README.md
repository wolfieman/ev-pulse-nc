# EV Pulse NC - Analytical Frameworks Directory

**Purpose:** This directory contains conceptual frameworks and decision analyses for the EV Pulse NC BIDA 670 capstone project. These documents define WHAT to analyze and WHY, not HOW to implement.

**Status:** Phase 1 Complete (Feb 2026)
**Scope:** Research priorities, decision trees, integration strategies
**Implementation:** None—these are conceptual roadmaps only

---

## Directory Organization

### Full Frameworks (Markdown)

Comprehensive decision frameworks with trade-off analyses, stakeholder assessments, and integration strategies.

| Framework | Priority | Size | Status | Description |
|-----------|----------|------|--------|-------------|
| **[priority-5-afdc-update-decision-framework.md](./priority-5-afdc-update-decision-framework.md)** | #5 | 31K | ✅ Complete | 5-node decision tree for AFDC infrastructure data update (Value Proposition → Update Scope → Temporal Strategy → Integration → Data Currency) |
| **[priority-5-stakeholder-value-integration-analysis.md](./priority-5-stakeholder-value-integration-analysis.md)** | #5 | 24K | ✅ Complete | Stakeholder differential value matrix (NEVI admins, county planners, private sector, academic, public) + integration with Priorities #1-3 |
| **[afdc-data-structure-snapshot-comparison-framework.md](./afdc-data-structure-snapshot-comparison-framework.md)** | #5 | 53K | ✅ Complete | AFDC API capabilities, data structure (50+ fields), snapshot comparison methodology, infrastructure classification for ZIP/CTPP integration |
| **[analytical-pipeline.md](./analytical-pipeline.md)** | All | — | ✅ Complete | Project analytical pipeline architecture: foundation (demand + supply) → gap analysis → three lenses (ZIP, CTPP, equity) → scoring framework → NEVI rankings |

### Analysis Notes (Text)

Shorter conceptual analyses and decision summaries from expert agent research.

| Analysis | Priority | Size | Status | Description |
|----------|----------|------|--------|-------------|
| **[validation-analysis.md](./validation-analysis.md)** | #1 | 3.5K | ✅ Complete | ARIMA validation framework (July-Oct 2025 BEV data), out-of-sample accuracy testing |
| **[zip-code-analysis.md](./zip-code-analysis.md)** | #2 | 11K | ✅ Complete | Sub-county spatial analysis framework, data availability constraints (NCDOT county-only), sparsity challenges |
| **[ctpp-analysis.md](./ctpp-analysis.md)** | #3 | 15K | ✅ Complete | Workplace charging demand framework using Census Transportation Planning Products (2016-2020 ACS), remote work adjustments |
| **[afdc-api-analysis.md](./afdc-api-analysis.md)** | #5 | 1.9K | ✅ Complete | NREL API technical specifications, rate limits, query parameters |
| **[proposed-project-titles.md](./proposed-project-titles.md)** | — | — | ✅ Complete | Candidate project titles for paper and presentations |

---

## Priority Map

EV Pulse NC research priorities and phases (aligned Feb 26, 2026):

> **Note:** Priority numbers were realigned to match phase numbers on Feb 26, 2026. Old Priority #5 (AFDC) moved to #2; old Priorities #2-4 shifted to #3-5. Framework filenames retain original numbering for traceability.

| Phase | Priority | Topic | Status | Key Decision |
|:-----:|:--------:|-------|--------|--------------|
| **1** | **1** | Predictive Analysis Validation | **Phase 1 Complete** | MAPE 4.36%, 68.9% underprediction, 8 publication figures |
| **2** | **2** (was #5) | AFDC Infrastructure Data | **Phase 2 Complete** | Complete API dataset replaces DCFC-only extract (1,985 stations, all levels) |
| **3** | **3** (was #2) | ZIP Code Analysis | ✅ Framework Complete ([zip-code-analysis.md](./zip-code-analysis.md)) | Infrastructure-only (adoption data unavailable at ZIP level) |
| **4** | **4** (was #3) | CTPP Commuting Data | ✅ Framework Complete ([ctpp-analysis.md](./ctpp-analysis.md)) | Top 15 employment centers, 30% workplace charging assumption |
| **5** | **5** (was #4) | HEPGIS Equity Analysis | ⏳ Pending | Justice40 integration (not yet started) |
| **6** | **6** | Buffer Analysis | ⏳ Pending | Coverage zones (not yet started) |
| **7** | **7** | NCDOT NEVI Corridor Validation | ⏳ Optional | Compare scoring framework output vs. NCDOT planned deployments |

### Phase 5: Prescriptive Scoring Framework (Integration Layer)

**Source:** Dr. Al-Ghandour's proposal feedback — "clearly defining prioritization criteria (equity, utilization, cost-effectiveness) within a scoring framework to translate findings into defensible NEVI allocation decisions."

**Formula:**
```
NEVI Priority Score(county) = w1 × Equity_Score + w2 × Utilization_Score + w3 × Cost_Effectiveness_Score
```

| Component | Source Extension | Metrics |
|-----------|----------------|---------|
| **Equity_Score** | HEPGIS + ZIP code analysis (#3/#5) | Justice40 disadvantaged community %, Gini coefficient, rural access gap, zero-infrastructure flag |
| **Utilization_Score** | Validation (#1) + AFDC complete baseline (#2) | BEVs/port ratio across all charging levels (L1, L2, DCFC), 4-5% underprediction buffer |
| **Cost_Effectiveness_Score** | CTPP workplace charging (#4) | Workplace efficiency (15 vs 7.5 BEVs/port), commuter demand sizing, population density |

**Weights:** Literature-driven from DOE/FHWA NEVI guidance (equity-heavy per Justice40: ~0.40/0.35/0.25) + sensitivity analysis showing top counties robust across weight variations.

**Output:** Ranked list of 100 NC counties with defensible NEVI dollar allocations.

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
- **Result:** MAPE 4.36% (strong validation), but systematic underprediction detected
- **Key Finding:** 68.9% of forecasts fell below actual values (Bias: +18.36 vehicles)
- **Model Distribution:** ESM (82 counties), ARIMA (13 counties), UCM (5 counties)
- **95% CI Coverage:** 75.3% (below nominal 95% due to bias)
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

### Priority #5 / Phase 5: HEPGIS Equity Analysis
- **Core Question:** Which communities face inequitable access to EV charging?
- **Key Framework:** Justice40 integration — 40% of benefits to disadvantaged communities
- **Status:** Not yet started

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

**Endpoint:** `https://developer.nrel.gov/api/alt-fuel-stations/v1.json`

**NC Query Parameters:**
- `state=NC`
- `fuel_type=ELEC`
- `status=E` (operational stations)
- `limit=all`

**Rate Limits:** 1,000 requests/hour (rolling 60-min window)
**EV Pulse NC Need:** 1 request per snapshot (well within limits)
**API Key:** Free, instant approval at https://developer.nrel.gov/signup/

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
| **Demand (BEV registrations)** | 6 months | ✅ 3 months (Oct 2025) | None |
| **Supply (Infrastructure)** | 3 months | ✅ Current (Feb 2026 API) | Complete dataset acquired (1,985 stations, all levels) |
| **Demographics** | 5 years | ✅ 4-6 years (2020 Census + ACS) | None |
| **Traffic Volumes** | 3 years | ✅ 3 years (2023 HPMS) | None |
| **Commuting Patterns** | 10 years | ✅ 6-10 years (CTPP 2016-2020) | None |

**Rationale:** Infrastructure data is now current and complete. The Feb 2026 API download provides full coverage of 1,985 NC stations across all charging levels and access types, replacing the previous DCFC-only extract that covered only 355 stations. All data types now meet or exceed their staleness thresholds.

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
- **Last Updated:** February 26, 2026
- **Status:** Phases 1-2 Complete; Priority numbers realigned to match phase numbers (old #5 → #2, old #2-4 → #3-5); Scoring framework defined; NCDOT corridor validation added as optional Priority #7

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
