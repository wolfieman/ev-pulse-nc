# EV Pulse NC - Analytical Frameworks Directory

**Purpose:** This directory contains conceptual frameworks and decision analyses for the EV Pulse NC BIDA 670 capstone project. These documents define WHAT to analyze and WHY, not HOW to implement.

**Status:** Active development (Jan 2026)
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

EV Pulse NC research priorities (post-SAS Cup redefinition):

| # | Priority | Framework Status | Key Decision |
|---|----------|------------------|--------------|
| **1** | Predictive Analysis Validation | ✅ Complete ([validation-analysis.md](./validation-analysis.md)) | Validate ARIMA with July-Oct 2025 data |
| **2** | ZIP Code Analysis | ✅ Complete ([zip-code-analysis.md](./zip-code-analysis.md)) | Infrastructure-only (adoption data unavailable at ZIP level) |
| **3** | CTPP Commuting Data | ✅ Complete ([ctpp-analysis.md](./ctpp-analysis.md)) | Top 15 employment centers, 30% workplace charging assumption |
| **4** | HEPGIS Equity Analysis | ⏳ Pending | Justice40 integration (not yet started) |
| **5** | AFDC API Update | ✅ Complete (3 frameworks) | **Dual-snapshot approach** (July 2024 + Jan 2026 growth analysis) |
| **6** | Buffer Analysis | ⏳ Pending | Coverage zones (not yet started) |

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

### Priority #1: Validation
- **Core Question:** Is our ARIMA model accurate for July-Oct 2025?
- **Key Insight:** Validation is independent of infrastructure update—proceed with July 2024 baseline
- **Validation Spectrum:** Not pass/fail, but interpretation of accuracy (MAPE <5% = strong, 5-10% = moderate, >10% = weak)

### Priority #2: ZIP Code Analysis
- **Core Question:** Can we analyze sub-county infrastructure gaps?
- **Key Constraint:** NCDOT doesn't publish ZIP-level BEV data (only county-level)
- **Key Insight:** Infrastructure-only ZIP analysis possible (AFDC has ZIP codes), adoption requires allocation heuristics
- **Expected Finding:** 400-500 ZIPs with <10 BEVs (50-60% of 800 ZIPs)—severe sparsity

### Priority #3: CTPP Workplace Charging
- **Core Question:** Does workplace demand differ from residential patterns?
- **Key Constraint:** CTPP data is 8-10 years old (2012-2016 ACS), requires remote work adjustments
- **Key Insight:** Workplace infrastructure 3× more efficient (15 EVs/port) than residential (7.5 EVs/port) but smaller absolute gap
- **Recommendation:** Focus on top 15 employment centers, not all 100 counties

### Priority #5: AFDC API Update
- **Core Question:** Should we update July 2024 infrastructure to Jan 2026?
- **Critical Finding:** 6-month staleness creates 15-22% gap overstatement (numerator current, denominator stale)
- **Key Insight:** **Dual-snapshot approach** transforms weakness into strength—infrastructure growth rate analysis
- **Stakeholder Value:** Private sector (9/10), County planners (8/10), NEVI admins (7/10)
- **Integration:** Enhances Priority #2 (spatial distribution), validates Priority #3 (station types), blocks Priority #6 (coverage zones)

---

## Cross-Priority Integration

### How Priorities Connect

```
Priority #1 (Validation)
    ↓ validates BEV forecasts
    ↓
Priority #5 (AFDC Update) ← uses validated forecasts
    ↓ provides infrastructure baseline
    ↓
Priority #2 (ZIP) + Priority #3 (CTPP) ← use Jan 2026 spatial data
    ↓ identify gaps
    ↓
Priority #6 (Buffer) ← requires Jan 2026 station locations
```

### Synergy Analysis

**Scenario 1:** Update AFDC (#5) but NOT ZIP (#2) or CTPP (#3)
- Value: 40% of potential impact (improved gaps, but county-level only)

**Scenario 2:** Pursue ZIP (#2) + CTPP (#3) but NOT AFDC (#5)
- Value: 60% of potential impact (sub-county insights, but stale data)

**Scenario 3:** Update AFDC (#5) AND pursue ZIP (#2) + CTPP (#3)
- Value: **100% of potential impact** (current baseline + spatial granularity)

---

## Recommended Decision Path (Priority #5)

Based on 3-agent analysis across decision framework, stakeholder value, and data structure research:

### Final Recommendation: Dual-Snapshot Approach (Option C)

**What:**
- Retain July 2024 as baseline (355 stations, 1,725 ports)
- Add Jan 2026 as current state (~400-450 stations)
- Calculate infrastructure growth rate (July → Jan)

**Why:**
- Transforms "data staleness" liability into "growth analysis" asset
- Enables unique research questions (which counties saw fastest deployment?)
- No rework of existing analysis (July 2024 remains valid)
- Addresses stakeholders: County planners (spatial distribution), Private sector (market intelligence), NEVI admins (deployment pace)

**Effort:** 3 hours (2 hrs API query + 1 hr growth analysis)

**Deliverables:**
1. Table: "NC EV Charging Infrastructure - Dual Baseline Comparison"
2. Metric: "Infrastructure deployment rate: +7.5 stations/month"
3. Map: "New Station Locations (July 2024-Jan 2026)"
4. Analysis: "Did growth occur in gap counties or already-served areas?"

**Integration:**
- Priority #1 (Validation): Independent—proceed with July 2024
- Priority #2 (ZIP): Enhanced by Jan 2026 spatial distribution
- Priority #3 (CTPP): Validates market response to workplace demand
- Priority #6 (Buffer): Requires Jan 2026 for coverage zones

---

## Risk Assessment Summary

### Risks of Updating Infrastructure Data

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Spatial join errors | Medium | High | Re-validate using data-validation-quality-checklist.md |
| API key approval delay | Low | Medium | Apply immediately (instant approval typical) |
| Station count unexpected | Low | Low | Document federal funding surge |
| Time overrun (>2 hrs) | Medium | Medium | Budget 3-4 hours buffer |

### Risks of NOT Updating

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Judges question data currency | High | High | Explicitly justify in methods section |
| Gap analysis overstates need | High | High | Add sensitivity analysis ("if infrastructure grew 20%...") |
| Policy recommendations misallocate | Medium | Very High | Caveat with "pending current infrastructure validation" |
| Competitors use current data | Medium | High | Accept competitive disadvantage |

**Conclusion:** Risks of NOT updating outweigh risks of updating (2-3 hour effort, foundational impact on all downstream priorities).

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
| **Supply (Infrastructure)** | 3 months | ❌ 6 months (July 2024) | **Update required** |
| **Demographics** | 5 years | ✅ 4-6 years (2020 Census + ACS) | None |
| **Traffic Volumes** | 3 years | ✅ 3 years (2023 HPMS) | None |
| **Commuting Patterns** | 10 years | ✅ 6-10 years (CTPP 2016-2020) | None |

**Rationale:** Infrastructure is MOST DYNAMIC dataset (47.6% deployed in 2024-2025) but currently STALEST. Policy recommendations require current baseline to avoid resource misallocation.

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
- **Last Updated:** January 30, 2026
- **Status:** Active (Priority #5 complete, Priority #4 and #6 pending)

### Related Documentation

**Research Files:**
- `/research/ev-pulse-nc/ev-pulse-nc-current-state-analysis.md` - Baseline analysis (82 months BEV data, 355 stations)
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
- Project partner: Braeden (data collection, GIS analysis)

**Note:** These frameworks are living documents. As priorities evolve or new constraints emerge, update frameworks accordingly.
