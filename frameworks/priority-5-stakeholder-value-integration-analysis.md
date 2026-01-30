# Priority #5: AFDC API Update - Stakeholder Value & Integration Analysis

## Executive Summary

This document analyzes WHO benefits from updating the AFDC infrastructure data from July 2024 to January 2026, and HOW this update integrates with EV Pulse NC's other analytical priorities. This is a conceptual analysis to inform decision-making—no implementation is performed.

---

## 1. Stakeholder Differential Value Matrix

### 1.1 NEVI Formula Program Administrators

**Current Need (July 2024 data):**
- **Low urgency** - NEVI funding operates on 5-year planning cycles (2022-2027)
- July 2024 baseline captures 355 stations, establishing infrastructure "starting point" for $109M allocation
- Policy decisions made in 2025-2026 already incorporate lag time expectations

**Jan 2026 Update Value:**
- **Moderate value** - Removes 6-month staleness critique in competition paper
- **Marginal benefit**: Likely adds 45-95 stations (13-27% increase) based on "47.6% recent deployment" finding
- **Risk**: Over-emphasizes short-term deployment surge vs. structural gaps

**Verdict**: State administrators operate on annual/multi-year cycles. Six-month staleness is acceptable for strategic planning. **Priority: Medium (7/10)**

---

### 1.2 County/Regional Planners

**Current Need (July 2024 data):**
- **Moderate urgency** - Local site selection requires current data
- County-level gaps already identified with July baseline (e.g., "Wake County: 266 BEVs/port")
- Regional planners work on 18-24 month implementation timelines

**Jan 2026 Update Value:**
- **High value** - Identifies *where* recent deployment occurred (urban concentration vs. rural expansion)
- **Critical insight**: If July-Jan growth concentrated in already-served areas, gap severity worsens
- **Actionable**: New stations in July-Jan period inform siting strategies ("avoid clustering near recent deployments")

**Scenario Analysis:**
- **If Jan 2026 shows 400 stations** (+45, +13%): Validates steady deployment, modest gap closure
- **If Jan 2026 shows 450 stations** (+95, +27%): Indicates deployment acceleration, revise projections upward

**Verdict**: Regional planners benefit from knowing *spatial distribution* of recent growth, not just count. **Priority: High (8/10)**

---

### 1.3 Private Sector (ChargePoint, EVgo, Tesla)

**Current Need (July 2024 data):**
- **High urgency** - Competitive intelligence drives site selection
- Private networks need to identify unserved markets before competitors

**Jan 2026 Update Value:**
- **Very high value** - Six months = significant competitive window
- **Market intelligence**: Which networks expanded where? (Tesla vs. third-party growth rates)
- **Gap identification**: Rural corridors remain unserved → opportunity zones
- **Pricing dynamics**: New entrants affect local pricing ($0.53/kWh Wake County benchmark)

**Key Question**: Did Tesla Supercharger expansion continue dominance (60.5% market share in July 2024)?

**Verdict**: Private sector operates on quarterly cycles. Six-month lag creates strategic blind spots. **Priority: Very High (9/10)**

---

### 1.4 Academic/Research

**Current Need (July 2024 data):**
- **Low urgency** - Research publications accept data vintage up to 12-18 months
- July 2024 baseline sufficient for peer review (competition deadline Feb 2026 = 7-month lag)

**Jan 2026 Update Value:**
- **Moderate value** - Eliminates "data currency" critique from reviewers
- **Methodological strength**: Demonstrates ability to integrate real-time API vs. static datasets
- **Replicability**: API-based approach allows future researchers to refresh analysis

**Trade-off**: Time spent updating (2 hours) vs. validating methodology (Priority #1: 4-6 hours)

**Verdict**: Competition judges may note data freshness, but won't penalize 6-month lag if methodology is sound. **Priority: Medium (6/10)**

---

### 1.5 EV Drivers/Public

**Current Need (July 2024 data):**
- **Low urgency** - Consumers use real-time apps (PlugShare, ChargePoint, Tesla) for trip planning
- Public analysis provides *long-term confidence* in infrastructure availability, not day-to-day routing

**Jan 2026 Update Value:**
- **Low value** - Six-month staleness irrelevant for "is NC infrastructure improving?" question
- **Perception impact**: "Analysis uses current data" signals credibility, even if substantive findings unchanged

**Verdict**: Public-facing analysis prioritizes trends over point-in-time accuracy. **Priority: Low (4/10)**

---

### Stakeholder Value Summary Table

| Stakeholder | July 2024 Adequate? | Jan 2026 Marginal Value | Priority Score | Key Concern |
|-------------|---------------------|-------------------------|----------------|-------------|
| **NEVI Administrators** | Yes (strategic cycles) | Removes staleness critique | 7/10 | Baseline credibility |
| **County Planners** | Moderate (need spatial detail) | Identifies *where* growth occurred | 8/10 | Spatial distribution |
| **Private Sector** | No (competitive intelligence) | 6-month competitive window | 9/10 | Market gaps |
| **Academic/Research** | Yes (peer review standard) | Methodological demonstration | 6/10 | Replicability |
| **EV Drivers/Public** | Yes (long-term trends) | Perception of currency | 4/10 | Trend confidence |

---

## 2. Analytical Question Mapping

### 2.1 Questions REQUIRING Current (Jan 2026) Data

**Q1: "Is NC infrastructure deployment accelerating or slowing?" (CRITICAL)**
- **Why Jan 2026 matters**: July 2024 shows "47.6% deployed in 2024-2025" → need Jan 2026 to validate if pace continued
- **Impact**: Informs whether county forecasts should adjust growth assumptions
- **Integration**: Priority #1 (Validation) - If deployment slowed, forecasted gaps worsen

**Q2: "Which networks are expanding fastest?" (HIGH)**
- **Why Jan 2026 matters**: Tesla dominance (60.5% in July) may shift if ChargePoint/Electrify America accelerate
- **Impact**: Informs NEVI "network diversity" requirement (avoid single-vendor lock-in)
- **Integration**: Priority #3 (CTPP) - Workplace charging typically ChargePoint, not Tesla

**Q3: "Are rural corridors being served?" (MEDIUM)**
- **Why Jan 2026 matters**: NEVI prioritizes 50-mile corridor coverage → need to track rural deployment
- **Impact**: Identifies if private sector is self-correcting gaps or if public funding still needed
- **Integration**: Priority #6 (Buffer Analysis) - Coverage % will change if rural stations added

---

### 2.2 Questions UNAFFECTED by 6-Month Staleness

**Q4: "Which counties have the highest infrastructure gaps?" (UNAFFECTED)**
- **Why July 2024 sufficient**: County *rankings* unlikely to change (Wake, Mecklenburg still top gaps)
- **Caveat**: Absolute gap values change, but ordinal rankings stable
- **Evidence**: Top 10 BEV counties account for 72% of vehicles → structural, not temporal

**Q5: "What is the infrastructure concentration (Gini coefficient)?" (UNAFFECTED)**
- **Why July 2024 sufficient**: Spatial inequality metric robust to 10-15% station additions
- **Current Gini**: 0.805 (extreme concentration)
- **Projected**: Jan 2026 likely 0.78-0.82 (marginal change)

**Q6: "What is the urban-rural disparity?" (UNAFFECTED)**
- **Why July 2024 sufficient**: 11 urban counties (11%) account for 70% of BEVs → structural pattern
- **Evidence**: Rural counties with 0 infrastructure won't suddenly gain 50 stations in 6 months

---

### 2.3 Hybrid Questions (Staleness Matters Conditionally)

**Q7: "What is the BEVs-per-charging-port ratio?" (CONDITIONAL)**
- **Current metric (July 2024)**: ~16.9 BEVs/port
- **Jan 2026 impact**: Numerator (BEVs) updated to Oct 2025 (current), denominator (stations) 6 months stale
- **Analysis**:
  - Oct 2025 BEVs: ~95,000 (NCDOT current data)
  - July 2024 ports: 1,725
  - **Current calculation**: 95,000 / 1,725 = 55 BEVs/port (OVERSTATES gap)
  - Jan 2026 ports: ~2,000 (estimated +15% growth)
  - **Updated calculation**: 95,000 / 2,000 = 47.5 BEVs/port (more accurate)

**Verdict**: **YES, staleness matters** - Mismatch creates 15% overestimation of gap severity

---

## 3. Integration with Completed Priorities

### 3.1 Priority #1: ARIMA Validation (July-Oct 2025)

**Question**: Does validation require concurrent infrastructure data?

**Answer**: **NO, infrastructure update not required for validation**

**Rationale**:
- Validation tests forecasting accuracy (predicted vs. actual BEV counts)
- Infrastructure data is *output metric* (gaps), not *validation input*
- Validation timeframe: July-Oct 2025 (4 months)
- Infrastructure change in 4 months: Minimal (~10-20 stations, <5% of total)

**Dependency Chain**:
```
Priority #1 (Validation) → Validates county BEV forecasts → Independent of infrastructure
Priority #5 (AFDC Update) → Updates infrastructure baseline → Uses validated forecasts to calculate gaps
```

**Conclusion**: Validation (Priority #1) can proceed with July 2024 infrastructure. Update to Jan 2026 is enhancement, not prerequisite.

---

### 3.2 Priority #2: ZIP Code Analysis

**Question**: Does ZIP-level infrastructure mapping require Jan 2026 data?

**Answer**: **MODERATE - Jan 2026 improves spatial analysis quality**

**Rationale**:
- ZIP analysis focuses on *intra-county heterogeneity* (e.g., Wake County's 28 ZIP codes)
- If July-Jan 2024-2026 stations clustered in already-served ZIPs → gap worsens in underserved ZIPs
- Example scenario:
  - **July 2024**: Wake ZIP 27603 (downtown Raleigh) has 30 stations
  - **Jan 2026**: +5 stations added, all in ZIP 27603 (not suburban ZIPs)
  - **Impact**: Intra-county inequality *increases* despite county total rising

**Spatial Distribution Matters**:
- If new stations are **evenly distributed**: Gap closure uniform
- If new stations are **clustered**: Gap severity bifurcates (urban improvement, suburban/rural worsening)

**Dependency Chain**:
```
Priority #2 (ZIP Analysis) → Identifies intra-county gaps → ENHANCED by Jan 2026 spatial detail
Priority #5 (AFDC Update) → Reveals WHERE recent growth occurred → Informs ZIP-level targeting
```

**Conclusion**: ZIP analysis can proceed with July 2024, but Jan 2026 adds critical *spatial distribution* insight. **Moderate dependency**.

---

### 3.3 Priority #3: CTPP Workplace Charging

**Question**: Does workplace station classification require most current data?

**Answer**: **NO - Methodology development uses July 2024, validation needs Jan 2026**

**Rationale**:
- CTPP analysis identifies *employment centers* (net inbound commuters) → independent of station count
- Workplace charging methodology requires *station classification* (M-F 8am-6pm vs. 24/7)
- Classification logic applies equally to 355 stations (July) or 400 stations (Jan)

**Station Classification Challenge**:
- Current problem: AFDC doesn't tag "workplace" vs. "residential"
- Workaround: Operating hours heuristic (Priority #3 framework, lines 253-258)
- **July 2024 sufficient** for proof-of-concept (develop classification logic on 355 stations)

**Validation Scenario**:
- If Jan 2026 adds 45 stations, WHAT TYPE?
  - If 90% are workplace (office parks, hospitals) → strengthens Priority #3 findings
  - If 90% are residential (apartments, retail) → weakens workplace investment case

**Dependency Chain**:
```
Priority #3 (CTPP) → Methodology: July 2024 sufficient → Validation: Jan 2026 tests if deployment matches need
Priority #5 (AFDC Update) → Station types reveal if market is self-correcting workplace gap
```

**Conclusion**: Methodology development independent of Jan 2026. Update validates whether *market is responding* to workplace demand signals. **Low dependency for methodology, HIGH for validation**.

---

## 4. Timing & Sequencing Considerations (Conceptual)

### 4.1 Critical Path Analysis

**Scenario A: Update Immediately (Week 1)**
```
Week 1: AFDC Update (2 hrs) → Baseline established
Week 1: Priority #1 Validation (4 hrs) → Uses new baseline
Week 2: Priority #2 ZIP Analysis (4 hrs) → Spatial distribution from Jan 2026
Week 2: Priority #3 CTPP (3 hrs) → Classification logic on 400 stations
```

**Pros**:
- Single source of truth throughout analysis
- Spatial distribution insights inform ZIP/CTPP priorities
- Competition paper says "Jan 2026 data" (freshness signal)

**Cons**:
- If API issues arise (2-hour estimate becomes 4 hours), delays cascade
- Baseline change may require recalculating county-level metrics (gap ratios, Gini coefficient)

---

**Scenario B: Parallel Track (Weeks 1-2)**
```
Week 1: Priority #1 Validation (July 2024 baseline) → Proceed independently
Week 1: Priority #2 ZIP Analysis (July 2024) → Spatial patterns established
Week 2: AFDC Update (2 hrs) → New baseline acquired
Week 2: Sensitivity Analysis (1 hr) → "How do findings change with Jan 2026 data?"
Week 3: Integration (2 hrs) → Update key tables/figures only
```

**Pros**:
- Parallel workstreams (no blocking dependencies)
- If API fails, analysis proceeds with July 2024
- Sensitivity analysis demonstrates methodological robustness

**Cons**:
- Risk of rework if Jan 2026 reveals unexpected patterns
- Two versions of truth (July vs. Jan) during analysis

---

**Scenario C: Update Post-Analysis (Week 4)**
```
Week 1-3: Complete Priorities #1-3 with July 2024 baseline
Week 4: AFDC Update (2 hrs) → Validate findings
Week 4: Spot-Check (1 hr) → Verify county rankings unchanged
Week 4: Update Paper (1 hr) → Refresh key statistics
```

**Pros**:
- No risk of delays to core analysis
- Jan 2026 serves as *validation* of July 2024 findings (methodological strength)
- Minimal rework if patterns stable

**Cons**:
- If Jan 2026 reveals major shifts (e.g., rural deployment surge), requires analysis redesign
- Tight timeline (Week 4 = competition prep week)

---

### 4.2 Dependency Matrix

| Priority | Requires Jan 2026? | Blocking Dependency? | Value-Add if Updated |
|----------|-------------------|----------------------|---------------------|
| **#1: Validation** | No | No | Low (validates BEV forecasts, not infrastructure) |
| **#2: ZIP Analysis** | Moderate | No | **High** (spatial distribution critical) |
| **#3: CTPP Workplace** | Methodology: No, Validation: Yes | No | Medium (tests market response) |
| **#6: Buffer Coverage** | Yes | **YES** | **Very High** (coverage % recalculates) |

**Critical Finding**: Only Priority #6 (Buffer Analysis) has **blocking dependency** on Jan 2026 data (coverage zones recalculate with new station locations).

---

## 5. Alternative Approaches - Trade-Off Analysis

### Option A: Update Now (Jan 2026) - Full Replacement

**Implementation**:
- Apply for NREL API key immediately (Week 1, Day 1)
- Replace July 2024 baseline entirely
- Recalculate all county-level metrics (gap ratios, Gini, rankings)

**Pros**:
- ✅ Maximum data currency (eliminates staleness critique)
- ✅ Single source of truth (no version confusion)
- ✅ Spatial distribution insights inform Priorities #2-3
- ✅ Enables Priority #6 (Buffer Analysis) with current coverage

**Cons**:
- ❌ Risk: API key approval delay (estimated instant, but unverified)
- ❌ Rework: County metrics recalculate (estimated +1 hour for Gini, rankings)
- ❌ Blocking: If API fails, analysis stalls

**Effort**: 2 hours (API) + 1 hour (recalculations) = **3 hours total**

**Recommended If**: API key confirmed by Week 1, Day 2 (Monday morning)

---

### Option B: Wait Until Pre-Final Analysis (April 2026)

**Implementation**:
- Complete competition analysis with July 2024 baseline
- After Feb 22 submission, update to April 2026 data (9-month gap)
- Publish updated analysis as research extension

**Pros**:
- ✅ Zero competition risk (no delays)
- ✅ Freshest possible data for publication (April 2026 = 10-month newer than July 2024)
- ✅ Enables temporal comparison (July 2024 → Jan 2026 → April 2026 = 9-month growth rate)

**Cons**:
- ❌ Competition paper uses stale data (judges may note)
- ❌ Misses spatial distribution insights for Priorities #2-3
- ❌ Priority #6 (Buffer Analysis) uses outdated coverage zones

**Effort**: 0 hours (Week 1-4), then 2 hours (post-competition)

**Recommended If**: Competition timeline at risk, need to eliminate all non-critical tasks

---

### Option C: Dual-Snapshot Approach (July 2024 + Jan 2026)

**Implementation**:
- Retain July 2024 as baseline ("starting point")
- Add Jan 2026 as "current state"
- Calculate 6-month growth metrics: station additions, network expansion, spatial patterns

**Pros**:
- ✅ **Transforms weakness into strength** - "Infrastructure growth rate analysis"
- ✅ Enables unique research questions:
  - "Which counties saw fastest infrastructure growth?" (Jan - July ratio)
  - "Is private sector self-correcting gaps?" (rural deployment rate)
  - "Network competition dynamics" (Tesla vs. ChargePoint market share change)
- ✅ Methodological sophistication (temporal analysis)
- ✅ No rework of July 2024 baseline (both coexist)

**Cons**:
- ❌ Increased complexity (two datasets to manage)
- ❌ Requires deciding which baseline for specific analyses (e.g., buffer zones use Jan, Gini uses both)
- ❌ +1 hour for growth rate calculations

**Effort**: 2 hours (API) + 1 hour (growth analysis) = **3 hours total**

**Deliverables**:
- Table: "NC Charging Infrastructure Growth (July 2024 - Jan 2026)"
- Metric: "Station deployment rate: +7.5 stations/month (45 added in 6 months)"
- Map: "New Stations by County (July-Jan 2026 additions highlighted)"

**Recommended If**: Time permits, want to maximize competitive differentiation

---

### Option D: Validation-Only (Spot-Check Specific Counties)

**Implementation**:
- Keep July 2024 as primary baseline (355 stations)
- Query Jan 2026 API for Top 10 BEV counties only (not statewide)
- Spot-check if county rankings/gaps changed materially

**Pros**:
- ✅ Minimal effort (30-minute API query, 30-minute validation = **1 hour total**)
- ✅ Eliminates uncertainty about whether update changes findings
- ✅ If stable, proceed with July 2024 confidently; if changed, trigger full update

**Cons**:
- ❌ Incomplete spatial picture (no rural/mid-tier county data)
- ❌ Can't support dual-snapshot analysis (Option C)
- ❌ If spot-check reveals major changes, requires full update anyway (wasted effort)

**Effort**: 1 hour (partial update) OR 3 hours (if triggers full update)

**Recommended If**: Ultra-conservative risk mitigation, testing waters before committing

---

## 6. Trade-Off Summary & Recommendations

### 6.1 Quantitative Comparison

| Option | Effort (Hours) | Competition Value | Research Value | Risk Level | Recommended? |
|--------|----------------|------------------|----------------|------------|--------------|
| **A: Update Now** | 3 | High (freshness) | Medium | Medium (API dependency) | ✅ **YES** (if API confirmed) |
| **B: Wait (April)** | 0 → 2 | Low (staleness) | High (publication) | Low | ⚠️ Only if timeline critical |
| **C: Dual-Snapshot** | 3 | **Very High** (growth analysis) | **Very High** | Medium | ✅ **YES** (best ROI) |
| **D: Validation-Only** | 1 → 3 | Medium | Low | Medium (rework risk) | ❌ No (indecisive) |

---

### 6.2 Final Recommendation: Option C (Dual-Snapshot)

**Rationale**:
1. **Transforms liability into asset**: Instead of "our data is 6 months stale" → "we analyzed infrastructure growth rate"
2. **Enables unique research questions**: Growth metrics differentiate from competitors
3. **No rework**: July 2024 baseline remains valid, Jan 2026 adds incremental insights
4. **Timing flexibility**: Can execute in Week 1 (parallel to Validation) or Week 2 (after Validation complete)
5. **Stakeholder value**: Addresses all high-priority stakeholders:
   - County planners: Spatial distribution of growth
   - Private sector: Network expansion dynamics
   - NEVI administrators: Deployment pace validation

**Implementation Timeline (Option C)**:
```
Week 1, Day 1: Apply for NREL API key (5 minutes)
Week 1, Day 2-3: Confirm API key received, test query (30 minutes)
Week 2, Day 1: Execute Jan 2026 query (1 hour)
Week 2, Day 2: Calculate growth metrics (July → Jan) (1 hour)
Week 2, Day 3: Generate growth analysis deliverables (1 hour)
Total: 3 hours over 2 weeks (non-blocking)
```

**Deliverables (Option C)**:
1. **Table**: "NC EV Charging Infrastructure - Dual Baseline Comparison"
   - July 2024: 355 stations, 1,725 ports
   - Jan 2026: ~400 stations, ~2,000 ports (+13% growth in 6 months)
2. **Metric**: "Infrastructure deployment rate: 7.5 stations/month (validates 47.6% recent deployment finding)"
3. **Map**: "New Station Locations (July 2024-Jan 2026)" - highlights spatial distribution of growth
4. **Analysis**: "Did growth occur in gap counties or already-served areas?"

---

### 6.3 Contingency Plan (If Option C Fails)

**If API key not received by Week 1, Day 3**:
- **Fallback**: Option B (Wait Until April) - proceed with July 2024 baseline
- **Paper language**: "Data current through July 2024; NREL API integration demonstrates replicable methodology for future updates"
- **Honest framing**: Methodology validation > data currency (judges will accept if acknowledged)

**If Jan 2026 query reveals major changes** (e.g., 500 stations, +40%):
- **Pivot**: Full replacement (Option A) - recalculate county metrics
- **Effort**: +1 hour for Gini/rankings recalculation
- **Benefit**: "Infrastructure surge validates accelerated deployment finding"

---

## 7. Critical Success Factors

**✅ DO THIS**:
- Apply for NREL API key **immediately** (Day 1, Week 1) - approval typically instant but unverified
- Frame dual-snapshot as **growth analysis**, not data update (strategic positioning)
- Report both baselines in paper ("July 2024 baseline, validated with Jan 2026 snapshot")
- Integrate growth findings with Priority #1 (Validation) - "Infrastructure deployment pace aligns with BEV forecast growth"

**❌ DON'T DO THIS**:
- Block Priorities #1-3 waiting for Jan 2026 data (unnecessary dependency)
- Discard July 2024 baseline (loses temporal comparison value)
- Claim false precision ("exactly 400 stations") - API data has 1-2 week lag, stations in "planned" status
- Skip NREL API key application (2-hour task becomes 0-hour if approved early)

---

## 8. Integration Summary

**How Jan 2026 Update Interacts with Other Priorities**:

| Priority | Dependency Type | Integration Method | Timing |
|----------|----------------|-------------------|--------|
| **#1: Validation** | Independent | Uses validated BEV forecasts to calculate gaps with Jan 2026 infrastructure | Week 2-3 |
| **#2: ZIP Code** | **Enhanced** | Spatial distribution of July-Jan growth reveals clustering patterns | Week 2 |
| **#3: CTPP** | Validation-level | Station types (workplace vs. residential) test market response | Week 2-3 |
| **#6: Buffer** | **Blocking** | Coverage zones recalculate with Jan 2026 station locations | Week 3 |

**Optimal Sequencing** (assuming Option C):
1. **Week 1**: Priority #1 (Validation) with July 2024 baseline → establishes forecast credibility
2. **Week 2**: AFDC Update (Jan 2026) → dual-snapshot acquired
3. **Week 2**: Priority #2 (ZIP Analysis) → uses spatial distribution from growth analysis
4. **Week 3**: Priority #3 (CTPP) → validates workplace charging deployment with Jan 2026 station types
5. **Week 3**: Priority #6 (Buffer Coverage) → executes with Jan 2026 coverage zones

---

## Conclusion

**Jan 2026 AFDC update delivers highest value when framed as growth analysis (Option C: Dual-Snapshot)**, not data replacement. This approach:
- **Maximizes stakeholder value**: County planners (8/10), Private sector (9/10)
- **Enables unique research**: Infrastructure growth rate differentiates from competitors
- **Minimizes risk**: Retains July 2024 baseline, adds incremental insights
- **Integrates strategically**: Enhances Priorities #2 (ZIP) and #6 (Buffer), validates Priority #3 (CTPP)

**Timing**: Execute in Week 2 (after Validation establishes credibility), parallel to ZIP/CTPP analysis.

**Effort**: 3 hours (2 API query, 1 growth analysis) - fits within 18-hour competition budget.

**Critical Action**: Apply for NREL API key immediately (Week 1, Day 1) to eliminate approval uncertainty.
