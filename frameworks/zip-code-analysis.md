# Phase 3: ZIP Code Analysis — Delivered Framework

## Executive Summary

Phase 3 delivered sub-county infrastructure magnification in North Carolina's urban counties, where county-level aggregation obscures critical spatial patterns. The analysis geocoded all 6,145 AFDC connectors to ZIP codes and calculated density, inequality, and underservice metrics across 134 ZIPs in the top 10 urban counties (roughly 80% of statewide BEV population).

**Critical finding:** A Theil decomposition attributes **84.5% of statewide spatial inequality to within-county variation** — meaning the bulk of the equity problem is hidden below the county level. Within Charlotte alone, the port density gap between ZIP 28202 and ZIP 28215 is roughly 250-fold. This is exactly the signal county-only analysis cannot see.

Phase 3 outputs feed both the Utilization Score and the Equity Score of the NEVI scoring framework.

## Results

| Output | File | Description |
|--------|------|-------------|
| County Gini | `data/processed/phase3-county-gini.csv` | Within-county infrastructure Gini coefficients |
| Statewide Gini | `data/processed/phase3-statewide-gini.csv` | Statewide connector Gini (0.805) |
| Theil decomposition | `data/processed/phase3-theil-decomposition.csv` | Within vs. between county inequality (84.5% within) |
| ZIP density | `data/processed/phase3-zip-density.csv` | Ports per sq mi, per capita, per BEV by ZIP |
| Top-20 underserved | `data/processed/phase3-top20-underserved.csv` | Site-selection priority ZIPs |
| Top 10 counties | `data/processed/phase3-top10-counties.csv` | Urban counties analyzed in Phase 3 |
| Station-county mapping | `data/processed/phase3-station-county-mapping.csv` | Geocoded station-to-county join |

Phase 3 produced 34 publication figures (fig-08 through fig-34) and populated the first 9 of 17 columns of the scoring framework skeleton. See `frameworks/analytical-pipeline.md` for how Phase 3 feeds the scoring framework.

---

---

## Framing and Decision Context (Retained from Planning)

The sections below document the decision framework used to scope Phase 3. They are preserved as methodological rationale for the delivered analysis.

## Core Findings from Three Expert Perspectives

### 1. Strategic Value (Decision Framework)

**What ZIP-level enables that county-level cannot:**
- Site selection precision: "Deploy 50 stations in ZIP 27603" vs. "Deploy in Wake County"
- Equity targeting: Low-income ZIP codes within wealthy counties
- Hotspot identification: Early adopter neighborhoods signal diffusion patterns
- Intra-county inequality: Wake County masks 3:1 disparity between richest/poorest ZIPs

**Marginal value calculation:**
- Urban ZIPs: 90% of analytical value in 10% of geographic units
- Rural ZIPs: Data sparsity overwhelms benefits

### 2. Best Practices (Literature Review)

**Standard spatial units in EV planning:**
- ZIP code level: Widely used for adoption tracking (CA, CO, NY, WA precedents)
- Census tract level: Preferred for demographic stability (avg 4,000 population)
- TAZ (Traffic Analysis Zones): Transportation modeling standard (500-5,000 zones per region)

**Policy context:**
- NEVI funding: Operates at state level, no formal ZIP-based allocation
- Municipal planning: Requires micro-level detail for site selection
- Electric utilities: Need feeder-level granularity for grid planning

**Data availability:**
- Nearly all US states publish ZIP-level EV registration data
- Exception: North Carolina - NCDOT publishes county-level only
- Infrastructure data: Already contains ZIP codes (ready for analysis)

### 3. Technical Reality (Spatial Analysis)

**Data availability in THIS project:**
- ❌ ZIP-level BEV registration data: NOT available from NCDOT
- ✅ ZIP-level charging infrastructure: Available (addresses with ZIP codes)
- Current status: County-level BEV data (100 units × 82 months)

**Boundary stability challenge:**
- Counties: Extremely stable over decades
- ZIP codes: "Frequently change, making time series analysis difficult to impossible"
- ZCTAs: Fixed for 10-year census cycles (2010, 2020)
- Your timeframe (Sep 2018-Jun 2025) spans two ZCTA definitions

**Projected sparsity:**
- 400-500 ZIPs with <10 BEVs (50-60% of 800 ZIPs)
- 200-300 ZIPs with <5 BEVs (25-35%)
- 100-150 ZIPs with 0 BEVs (12-18%)

---

## Five Critical Decision Nodes

### Decision Node 1: Scope Selection

**Option A: Universal (all ~800 NC ZIPs)**
- ❌ 60% of ZIPs have <5 BEVs (statistical noise)
- ❌ Visualization overload (800 units illegible)
- Use case: Research publication demonstrating comprehensive methodology

**Option B: Selective (urban ZIPs only)** ⭐ **RECOMMENDED**
- ✅ Focus on 80% of BEVs in 15% of ZIPs (~120 urban ZIPs)
- ✅ Manageable visualization
- ✅ Statistical reliability (n≥50 per ZIP)
- Criteria: Population density >1,000/sq mi, BEVs >50, within top 10 counties

**Option C: Hybrid (case study ZIPs)**
- Wake County's 28 ZIPs as proof-of-concept
- Extrapolate to similar urban counties
- Use case: Time-constrained projects

---

### Decision Node 2: Analytical Depth

**Option A: Descriptive Only** ⭐ **RECOMMENDED FOR THIS PROJECT**
- Current state snapshot (June 2025)
- BEVs per ZIP, infrastructure gap metrics
- Effort: 2-4 hours
- Value: High for site selection

**Option B: Predictive Modeling**
- ARIMA for each ZIP (800 separate models)
- Effort: 20-30 hours
- Challenge: Data sparsity makes forecasting unreliable
- Recommendation: SKIP - use county forecasts + ZIP proportions instead

---

### Decision Node 3: Integration Strategy

**Option A: Replace counties** (❌ Not recommended)
- Throws away 82 months of validated county work
- Introduces sparsity issues

**Option B: Validation layer** ⭐ **RECOMMENDED**
- County-level remains primary (100 × 82 months validated)
- ZIP-level provides sub-county detail for top 5-10 counties
- Workflow:
  a. Validate county forecasts (Priority #1)
  b. Use ZIP snapshot to decompose top counties
  c. Show intra-county heterogeneity
- Effort: 4-6 hours

**Option C: Equity deep-dive (integrates with Priority #4)**
- ZIP codes ONLY for equity analysis
- Overlay demographics with infrastructure
- Focus: Charging deserts in disadvantaged communities
- Effort: 6-8 hours

---

### Decision Node 4: Data Acquisition Reality

**What you have:**
- ✅ County-level BEV data (82 months, complete)
- ✅ Infrastructure with ZIP codes (stations, addresses)

**What you don't have:**
- ❌ ZIP-level BEV registration data (NCDOT doesn't publish)

**Options:**
1. **Phase 2A: Infrastructure ZIP analysis (immediate)**
   - Charging station density by ZIP
   - Overlay with county-level adoption
   - Deliverable: "Coverage analysis"
   - Effort: 4-6 hours

2. **Phase 2B: Full ZIP adoption analysis (Future Direction)**
   - Prerequisite: Acquire ZIP-level BEV registration data
   - FOI request to NCDOT (may be denied)
   - Commercial vendors (IHS Markit, requires license)
   - Post-capstone roadmap

---

### Decision Node 5: Hierarchical Approach

**Tier 1: Urban counties (ZIP-level)**
- Mecklenburg, Wake, Durham, Guilford, Forsyth
- ~200-250 ZIPs total
- Deliverable: ZIP-level heat maps

**Tier 2: Suburban counties (county-level)**
- Ranks 6-30 by BEV count
- Deliverable: County summaries

**Tier 3: Rural counties (regional aggregation)**
- Remaining 70 counties
- Deliverable: Regional clusters ("Western Mountains", "Coastal Plain")

---

## Key Trade-Offs

### 1. Precision vs. Reliability

- Finer resolution = More insights but lower statistical confidence
- Sweet spot: Urban ZIPs (granular enough to show inequality, aggregated enough for reliability)

### 2. Complexity vs. Interpretability

- 800 ZIPs overwhelming for policy audiences
- Solution: Tiered reporting (state summary → county detail → ZIP appendix)

### 3. Effort vs. Value

| Analysis | Hours | Policy Value | Recommended? |
|----------|-------|--------------|--------------|
| ZIP descriptive (top 10 counties) | 4-6 | High | ✅ YES |
| ZIP descriptive (all ZIPs) | 10-12 | Medium | Only if publication |
| ZIP forecasting | 20-30 | Medium | ❌ SKIP |

---

## Integration with Other Priorities

**Priority #1 (Validation):**
- Validate county forecasts FIRST → establishes credibility
- Use validated county totals as constraints for ZIP allocation

**Priority #3 (CTPP Commuting):**
- CTPP: County-to-county flows
- ZIP: Intra-county workplace detail
- Synergy: Identify employment center ZIPs needing workplace charging

**Priority #4 (Equity):**
- CRITICAL DEPENDENCY: Equity analysis REQUIRES sub-county resolution
- ZIP codes are operational units for targeting (not census tracts)
- NEVI requires 40% benefits to disadvantaged communities

**Priority #6 (Buffer Coverage):**
- Coverage shows WHERE gaps exist
- ZIP analysis shows WHO is affected
- Prioritize gaps by BEV density (not just land area)

---

## Recommended Approach for BIDA 670

### Phase 2A: Infrastructure ZIP Analysis (Immediate - 4-6 hours)

**What to do:**
1. Spatial join charging stations to ZIPs (data already has ZIP field)
2. Calculate infrastructure density by ZIP
3. Identify top 20 underserved ZIPs (high BEV counties, low infrastructure)
4. Overlay with county-level adoption trends

**Deliverables:**
- Table: "Top 20 NC ZIP Codes by Infrastructure Need"
- Map: "Wake County Infrastructure Gap by ZIP"
- Metric: "X% of Wake County BEVs in Y ZIPs (Gini coefficient)"

**Value**: High policy relevance, supports equity targeting, demonstrates analytical depth

### Phase 2B: Full ZIP Adoption — Future Direction

**Prerequisites:**
- Obtain ZIP-level BEV registration data from NCDOT or vendor
- Validate data quality and boundary stability

Preserved as a post-capstone roadmap item. Unlikely within the BIDA 670 capstone timeframe given NCDOT's current publication policy, but a reasonable extension if data access changes.

---

## Critical Success Factors

### ✅ DO THIS:
- Focus on 100-120 urban ZIPs (sufficient density)
- Descriptive analysis only (no forecasting)
- Integration with county validation (Priority #1)
- Link to equity analysis (Priority #4)

### ❌ DON'T DO THIS:
- Analyze all 800 ZIPs (sparse data overwhelms)
- Build 800 ARIMA models (diminishing returns)
- Present ZIP detail to state policymakers (they think in counties)
- Fight boundary crosswalk issues (accept imperfection)
