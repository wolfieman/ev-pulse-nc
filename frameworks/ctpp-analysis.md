# Priority #3: CTPP Commuting Data - Complete Conceptual Framework

> **Status update (Apr 2026):** The core analysis described below is complete and merged (Phase 4 CTPP/LEHD). See `frameworks/analytical-pipeline.md` and `data/processed/phase4-*.csv`. The "Phase 3B" sub-section below describes potential future extensions and remains aspirational.

## Executive Summary

CTPP integration transforms EV infrastructure analysis from a single-dimension residential model to a dual-dimension residential + workplace model. The current analysis misses a critical component: workplace charging demand driven by inter-county commuting patterns.

**Critical Finding**: Employment centers like Wake County need 2-3× more infrastructure than residential analysis suggests. Without CTPP data, systematic underinvestment in workplace charging is inevitable.

---

## Core Value Proposition

### What CTPP Adds:
- Quantifies workplace demand: Currently invisible in residential BEV counts
- Identifies employment centers: Net inbound commuters reveal workplace infrastructure priorities
- Enables equity targeting: Workplace charging serves renters who cannot install home chargers
- Informs NEVI allocation: $7M (30% of NC community charging funds) justified by commuting data

### Transformational Insight:
- **Current**: Wake County has 25,000 resident BEVs → "High priority"
- **Enhanced**: Wake County has 25,000 residents + 8,400 EV commuters → "VERY high priority + workplace focus"

---

## Five Critical Decision Nodes

### Decision Node 1: Geographic Scope

**Option A: All 100 counties (10,000 county pairs)**
- Comprehensive but overwhelming
- 8-10 hours analysis time

**Option B: Top 15-20 employment centers** ⭐ **RECOMMENDED**
- 80% of workplace demand in 20% of counties
- 3 hours analysis time (matches allocated budget)
- Employment centers: Wake, Mecklenburg, Durham, Guilford, Orange, Forsyth

**Option C: Top 10 BEV counties only**
- Too narrow, misses non-resident commuter demand

---

### Decision Node 2: Flow Direction

**Option A: Inbound only (where people work)**
- Sizes workplace infrastructure needs

**Option B: Outbound only (where people live but don't work)**
- Identifies bedroom communities

**Option C: Bidirectional with net calculation** ⭐ **RECOMMENDED**
- Enables county typology:
  - Employment centers (net +10,000): Heavy workplace investment
  - Balanced (net ±5,000): Mixed strategy
  - Bedroom communities (net -10,000): Residential focus only

---

### Decision Node 3: EV Adoption Rate Method

**Three competing approaches:**

**Origin County Rate (where commuters live):**
- Most defensible - home location determines charging access
- Accounts for geographic wealth variation (Wake 2.5% vs. rural 0.3%)

**Destination County Rate (where they work):**
- Assumes workplace income drives adoption

**State Average (1.5%):**
- Simplest but loses important variation

**RECOMMENDED: Origin × 1.25 (commuter income premium)**
- Recognizes that commuters earn 25% more than average residents
- Balances home infrastructure access with income effects

---

### Decision Node 4: Workplace Charging Rate Assumption

**Critical question**: What % of EV commuters charge at work?

**Research findings:**
- Current: 10% of EV charging at workplace (2025)
- Projected: 17% by 2030
- ChargePoint data: 30% of EV commuters use workplace charging regularly

**Segmentation:**

| Commuter Type | % of EV Commuters | Workplace Charging Rate |
|---------------|-------------------|-------------------------|
| Daily chargers (long commute, no home charging) | 12% | 100% |
| Frequent chargers (moderate commute, limited home) | 18% | 50% |
| Occasional chargers (short commute, home Level 2) | 23% | 30% |
| Non-chargers (home charging sufficient) | 47% | 0% |

**Weighted average: 30%** ⭐ **RECOMMENDED BASELINE**

---

### Decision Node 5: Charger Type Mix

**Level 2 (80%)** ⭐ **PRIMARY WORKPLACE TYPE**
- 8-hour parking ideal for offices, universities, hospitals
- Cost: $3,000-$7,000 per port
- Grid-friendly: Spreads load over work hours

**DCFC (20%) - Secondary**
- High-turnover sites: retail, transit hubs, hospitals (visitors)
- Cost: $50,000-$150,000 per station

**Key finding**: Most workplace sites need Level 2, NOT DCFC

---

## Major Findings from Three Expert Perspectives

### 1. Strategic Value (Policy Framework)

**What policy questions CTPP enables:**
- "Which counties are net employment centers?" → Prioritizes workplace infrastructure
- "Should Durham fund chargers for Wake commuters?" → Regional coordination
- "How do we serve renters without home charging?" → Workplace = equity solution
- "Where will daytime grid load strain occur?" → Peak load management

**NEVI funding context:**
- 80% corridor DCFC (mandatory)
- 20% community charging (discretionary):
  - Multi-family: 40% ($9M)
  - Workplace: 30% ($7M) ← CTPP justifies this allocation
  - Rural/destination: 30% ($6M)

### 2. Best Practices (Literature Review)

**Workplace charging role:**
- 80% home charging, 10% workplace, 10% public (current split)
- 73% of commuters have multi-hour parking at work
- Workplace charging demand growing 2× faster than supply (2023-2024)
- 30-40% of companies prioritize offices with EV chargers (talent retention)

**Remote work impact:**
- Office attendance remains below pre-COVID
- BUT workplace chargers are being used more intensively (users went up 57%, sessions up 64%)
- Peak charging shifted to Tuesday-Thursday (Friday declined significantly)
- Implication: 25-30% reduction in commute volumes, but higher per-capita charging

**NREL/DOT guidance:**
- Trip lengths determine infrastructure needs (30-mile commute = home OK, 80-mile = workplace critical)
- EVI-X modeling suite uses origin-destination data for regional forecasting
- Academic precedent: Peer-reviewed research uses O-D flows for EV load prediction at census block level

### 3. Technical Reality (Data Challenges)

**Data structure:**
- 100 counties × 100 counties = 10,000 possible pairs
- Estimated meaningful flows: 1,500-2,500 (only 15-25% of pairs have >100 workers)
- Threshold for viability: 500+ workers per corridor (yields 10+ EV commuters at 2% adoption)

**Data vintage problem:**
- CTPP: 2012-2016 (8-10 years old)
- Post-COVID reality: 30% remote work adjustment needed
- Solution: Apply 0.70-0.85 multiplier (sector-specific)

**Uncertainty cascade:**
- Remote work: ±25%
- EV adoption rate: ±25%
- Workplace charging rate: ±33%
- Combined uncertainty: ±60-80%
- Implication: Report ranges, not point estimates

---

## Key Trade-Offs

### 1. Data Staleness vs. Unique Value

CTPP is 8-10 years old, BUT:
- Only comprehensive county-to-county flow source
- No affordable alternative ($0 vs. $10,000-$50,000 for real-time mobility data)
- Commute patterns (structure) more stable than volumes
- With adjustments, provides order-of-magnitude estimates sufficient for strategic planning

### 2. Workplace vs. Residential Priority

**Comparison:**

| Infrastructure Type | Need (EVs) | Ports Needed | Current | Gap | ROI (EVs/port) |
|---------------------|------------|--------------|---------|-----|----------------|
| Residential Public  | 6,250      | 833          | 180     | 653 | 7.5            |
| Workplace           | 2,520      | 168          | 60      | 108 | 15             |

**Key finding**: Workplace gap is smaller (108 vs. 653 ports) but 3× more efficient (15 EVs/port vs. 7.5)

**RECOMMENDED STRATEGY: Workplace-first for employment centers**
- Phase 1 (2026-2027): 60% workplace, 40% residential
- Phase 2 (2028-2030): 40% workplace, 60% residential
- Rationale: Faster deployment, higher ROI, leverages employer co-funding

### 3. Complexity vs. Interpretability

- Full complexity: 10,000 county pairs overwhelming
- Simplified: Top 10 employment centers clear and actionable

**RECOMMENDED: Tiered communication**
- Executive summary: Top 10 employment centers ranked by gap
- Main paper: Network map + top 20 flows
- Appendix: Complete 100×100 matrix (for replication)

---

## Integration with Other Priorities

### Priority #1 (Validation):

- Validate county forecasts FIRST
- Use validated totals as constraints: "Wake forecast: 28,000 residents + 8,400 commuters = 36,400 total EV infrastructure demand"

### Priority #2 (ZIP Code Analysis):

**Triple-layer model:**
a. County: Where people live (BEV registrations)
b. ZIP: Within-county targeting (urban vs. suburban)
c. CTPP: Cross-county workplace demand

Example: Cary analysis enhanced by commute-in from Johnston/Chatham → +60 workplace ports

### Priority #4 (Equity):

- Critical dependency: Equity analysis REQUIRES workplace charging dimension
- Low-income workers in apartments CANNOT charge at home
- Equity metric: % low-income workers with workplace charging access
- Finding: Likely <50% (low-income half as likely to have workplace access vs. high-income)

---

## Methodological Challenges

### Challenge 1: Temporal Mismatch (2016 data vs. 2025 reality)

**Solution: Apply sector-specific remote work adjustment**
- Tech hubs (Wake, Mecklenburg): 0.75× multiplier (25% reduction)
- Traditional (Guilford, Forsyth): 0.85× multiplier (15% reduction)
- Rural: 0.90× multiplier (10% reduction)

### Challenge 2: Multi-Step Inference Chain

```
Workers (observed)
→ Adjust for remote work (±25% error)
→ Apply EV adoption rate (±25% error)
→ Apply charging propensity (±33% error)
→ Compare to workplace stations (±50% error - classification ambiguous)
= Combined ±60-80% uncertainty
```

**Solution: Transparent sensitivity analysis**
- Report: "Wake needs 90-239 workplace ports depending on assumptions"
- Baseline: 158 ports (moderate scenario)

### Challenge 3: Station Classification

**Current problem**: AFDC doesn't tag stations as "residential" vs. "workplace"

**Workaround: Operating hours heuristic**
- M-F 8am-6pm peak = Workplace
- 24/7 or evening peak = Residential/public
- Mixed-use = 50% allocation

---

## Recommended Approach for BIDA 670

### Phase 3A: CTPP Employment Center Analysis (3 hours)

**What to do:**
1. Query CTPP for top 15 employment counties (inbound + outbound flows)
2. Calculate net employment center effect (inbound - outbound)
3. Apply remote work adjustment (0.75-0.85 multiplier)
4. Estimate EV commuters (origin county rate × 1.25)
5. Calculate workplace ports needed (30% charging rate, 15 EVs/port ratio)

**Deliverables:**
- Table: "Top 10 Employment Centers Ranked by Workplace Infrastructure Gap"
- Map: "NC EV Commute Flows - Arrow thickness = EV commuter volume"
- Metric: "Employment centers need 2-3× more infrastructure than residential analysis suggests"

**Value**: High policy relevance, justifies NEVI workplace funding, addresses equity

### Phase 3B: Full Integration (Future - pending better data)

**Prerequisites:**
- Obtain 2017-2021 CTPP (expected 2026, includes early pandemic)
- Employer surveys to calibrate workplace charging propensity
- Validate with 2024-2025 traffic counts

**Timeline**: 2026-2027 (outside capstone scope)

---

## Critical Success Factors

### ✅ DO THIS:
- Focus on top 15 employment centers (sufficient for policy)
- Apply transparent adjustments (remote work, EV rates)
- Report sensitivity ranges (90-239 ports, not 158)
- Frame as proof-of-concept methodology

### ❌ DON'T DO THIS:
- Analyze all 10,000 county pairs (diminishing returns)
- Claim false precision ("exactly 158 ports needed")
- Present workplace as replacing residential (they're complementary)
- Ignore data vintage caveat
