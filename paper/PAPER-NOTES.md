# Paper Notes — Items to Include

Findings and documentation requirements identified during Phase 3 EDA analysis.
These must be incorporated into the final paper at the appropriate sections.

---

## Data Section (Section 3)

### AFDC Infrastructure Data Description
- 1,985 stations, 6,145 connectors, all status E (available)
- 76 columns; 28 non-EV fuel columns are 100% null (dropped)
- Charging level distribution: L2-only 82.4% (1,636), DCFC-only 311, Mixed 29, L1-only 9
- Top network: ChargePoint 51.8% (1,028 stations)
- Access: 1,876 public, 109 private
- Connectors: J1772 (1,586), J1772COMBO (243), Tesla (234), CHAdeMO (143)
- Power range: 2-400 kW (extracted for 1,611 stations)
- Geographic coverage: 358 ZIP codes, 267 cities

### Census ZCTA Data Description
- 853 NC ZCTAs from ACS 2022 5-Year estimates
- Total population: 10,470,214 (98.8% of NC's ~10.6M)
- Right-skewed distribution: mean 12,275 vs median 5,380 (skewness 1.70)
- 19 uninhabited ZCTAs (pop=0), excluded from per-capita calculations

### County Boundaries
- 100 NC counties from Census TIGER/GENZ 2020 (500k resolution)
- All geometries valid, CRS EPSG:4269

---

## Data Cleaning & Validation Section (Section 4)

### AFDC Cleaning Steps
- 2 non-NC stations removed (ZIPs 20020 and 39817) — reduces to 1,983 NC stations
- The out-of-bounds coordinate (lat 38.87) is the same station as ZIP 20020 — resolved by ZIP filter
- 56 co-located stations (shared coordinates) confirmed as legitimate separate equipment — retained
- High missingness fields (ev_pricing 86%, facility_type 71.5%, owner_type_code 70%) documented and excluded from density analysis — core location/port fields nearly complete

### Join-Key Validation
- 354 of 358 AFDC ZIPs match Census ZCTAs (98.9% match rate)
- 4 unmatched AFDC ZIPs:
  - 28608 (Boone) — PO Box ZCTA, no Census population record
  - 27706 (Durham) — university PO Box ZCTA
  - 20020 — non-NC (DC area), removed in cleaning
  - 39817 — non-NC (Georgia), removed in cleaning
- 3 stations in PO Box ZIPs (28608, 27706) excluded from population-based density calculations
- 354 matched ZIPs cover 99.8% of station inventory

### Census Data Quality
- Zero missing values, no duplicates
- All ZCTAs match "ZCTA5 XXXXX" naming pattern
- Population stored as string in raw CSV — cast to int during processing

---

## Analysis Section (Section 5)

### Coverage Gap Finding
- 499 of 853 Census ZCTAs (58.5%) have zero charging stations
- These ZCTAs represent 2,208,854 people (21.1% of NC population)
- Key equity finding for NEVI funding recommendations

### Step 3 Findings: Station-to-County Mapping
- 1,983 NC stations (after removing 2 non-NC); 1,981 successfully mapped to counties via spatial join (2 fell outside polygons — coastal edge cases)
- Top 10 counties by BEV count: Wake (28,098), Mecklenburg (18,040), Durham (5,556), Guilford (4,610), Union (4,160), Buncombe (3,595), Cabarrus (3,524), Orange (3,494), Forsyth (2,747), New Hanover (2,023)
- 134 unique ZIPs in top 10 counties (slightly above the ~120 estimate)
- 1,210 stations with 3,736 total ports in the analysis scope

### Step 4 Findings: Infrastructure Density
- Overall density: mean 11.18 ports/10k, median 5.51 ports/10k
- Extreme intra-county variation: Mecklenburg ranges from 0.31 to 78.64 ports/10k (250x gap)
- Best-served ZIP: 28202 (Charlotte Uptown) at 78.64/10k
- Worst-served ZIP: 27215 (Burlington) at 0.22/10k — a 357x gap between best and worst
- 1,153 public stations (of 1,210 total), 3,493 public ports (of 3,736 total)
- 746 DC fast ports across the top 10 counties

### Step 5 Findings: Top 20 Underserved ZIPs
- **732,892 people** in the top 20 underserved ZIPs — served by only 58 ports (0.79/10k aggregate)
- **15 of 20** underserved ZIPs have **zero DC fast chargers**
- Most underserved: Burlington 27215 — 1 port for 45,982 people (0.22/10k, ~50x below median)
- Mecklenburg and Guilford dominate with 5 ZIPs each in the top 20
- 9 of 10 top counties have at least one ZIP in the top 20 — underservice is widespread, not concentrated
- Key example: Charlotte 28215 has 64,713 people but only 2 ports (0.31/10k)
- Some underserved ZIPs have only private chargers (e.g., Winston-Salem 27105) — effectively zero public access

### Step 6 Findings: Intra-County Inequality (Gini)
- Statewide population-weighted Gini: **0.566** (very high inequality)
- Most unequal: Mecklenburg (0.623), Guilford (0.571) — both "very high"
- Wake (0.496), Buncombe (0.485), New Hanover (0.477), Durham (0.408) — all "high"
- Union is uniformly underserved (low IQR 0.92) — every ZIP is bad, not just some
- Weighted vs unweighted Gini diverge meaningfully: Durham's weighted (0.41) < unweighted (0.51) — well-served ZIPs are the populated ones
- Compare with BEV ownership Gini of 0.805 from baseline — infrastructure inequality (0.566) is severe but lower than vehicle ownership concentration

#### Interpreting the Gini Coefficient (for paper narrative)
The Gini coefficient ranges from 0 to 1. In our context (ports per 10,000 population across ZCTAs within a county):

- **Gini = 0** would mean every ZCTA in the county has exactly the same charging density — perfectly equal distribution. Every resident has the same per-capita access regardless of which ZIP they live in.
- **Gini = 1** would mean all ports are concentrated in a single ZCTA and every other ZCTA has zero — perfect inequality.

What our values mean in practice:
- **Mecklenburg (0.623)**: Very high inequality. Charlotte Uptown (28202) has 78.64 ports/10k while Charlotte East (28215) has 0.31 ports/10k — a 250x gap within the same county. A resident's access to charging depends heavily on which ZIP they live in.
- **Guilford (0.571)**: Very high inequality. Infrastructure is clustered in downtown Greensboro ZIPs while suburban/peripheral ZIPs are severely underserved.
- **Wake (0.496)**: High inequality, but notably lower than Mecklenburg/Guilford. Charging infrastructure is more evenly spread across Raleigh-area ZIPs, though significant gaps remain.
- **Durham (0.408)**: The "best" of the top counties, but still high. The weighted Gini (0.41) being lower than unweighted (0.51) tells an important story — the well-served ZIPs happen to be the highly populated ones, so the average resident has better access than the average ZIP would suggest.
- **Union (Gini low, but uniformly bad)**: A low Gini does NOT mean good service — Union's low inequality reflects the fact that every ZIP is equally underserved (low IQR of 0.92). Equality at a low level is not the goal.

Key paper framing:
- The Gini captures *distribution* inequality, not *adequacy*. A county can have low Gini but still be underserved everywhere (Union). Policy must consider both.
- The statewide weighted Gini (0.566) vs BEV ownership Gini (0.805) comparison is important: infrastructure inequality is severe, but vehicle ownership is even more concentrated. This suggests infrastructure is partially following demand — but not equitably.
- The weighted vs unweighted distinction matters for policy: weighted Gini accounts for how many people are affected. Durham's divergence (0.41 weighted vs 0.51 unweighted) means small-population ZIPs are underserved but most residents live in well-served areas. Mecklenburg's convergence means large-population ZIPs are underserved too — a worse equity outcome.

### Step 7 Findings: County Heat Maps (Choropleths)
- Three counties selected for spatial visualization: Wake, Guilford, Mecklenburg (ordered by ascending Gini)
- ZCTA boundary geometries from Census TIGER/GENZ 2020 (500k resolution, same vintage as county boundaries)
- 1,485 ZCTAs downloaded (national file, spatially filtered to NC bounding box); 853 NC-prefix ZCTAs confirmed
- Shared LogNorm color scale (vmin=0.1, vmax=79.0) across all three maps enables direct cross-county comparison
- Zero-station ZCTAs rendered with distinct hatching pattern — categorically different from "low density"
- DC fast charger locations overlaid as point markers from station-level lat/lon data
- Per-county scaled supplementary maps also produced for within-county spatial pattern analysis
- Projection: NC State Plane (EPSG:32119) for accurate area representation
- Figures: fig-22 (Wake), fig-23 (Guilford), fig-24 (Mecklenburg); supplementary fig-22s, 23s, 24s

#### Spatial Observations from Heat Maps
- **Wake (fig-22)**: Most evenly distributed; dark blue clusters around downtown Raleigh spread into surrounding ZCTAs; 10 of 41 ZCTAs have no stations (24%), mostly rural edges; DC fast chargers well dispersed across the county
- **Guilford (fig-23)**: Stark inequality visible; 17 of 35 ZCTAs have no stations (49%); infrastructure concentrated in a downtown Greensboro corridor with secondary High Point cluster; large peripheral population areas completely unserved
- **Mecklenburg (fig-24)**: Extreme concentration; Charlotte Uptown (78.64/10k) is a tiny dark cluster surrounded by pale green/yellow; 7 of 37 ZCTAs have no stations (19%); hatched areas in the south include 28215 (64,713 people, 2 ports) — this is what Gini 0.623 looks like spatially
- Cross-county comparison confirms shared scale works: Mecklenburg's dark cluster is visibly more intense and more isolated than Wake's broader distribution
- Guilford's zero-station proportion (49%) is the highest — visually dominates the map with hatching, strongest case for NEVI gap-filling

### Step 8 Findings: Publication Figures (fig-25 to fig-32)

#### fig-25: Statewide Underserved Choropleth
- 199 ZCTAs plotted across 10 counties; 129 with stations, 70 without
- All 20 underserved ZIPs highlighted with red outlines — geographic spread of the problem is immediately visible
- Underserved ZIPs are not concentrated in one area; they span Mecklenburg, Guilford, Wake, Forsyth, Union, and others

#### fig-26: Population vs Port Density Scatter
- High-density ZIPs tend to be low-population (downtown commercial areas)
- Large-population ZIPs cluster near or below the statewide median (5.51) — more people live in underserved areas
- Supports the equity argument: infrastructure favors small commercial ZIPs over large residential ones

#### fig-27: Lorenz Curve
- Visual proof of inequality: substantial gap between equality line and all curves
- Mecklenburg's curve bows the most (Gini 0.623), Wake the least (0.496) — matches computed values
- Shaded area between equality line and statewide curve represents the Gini coefficient visually
- Essential figure for peer review — any inequality paper must include this

#### fig-28: Gini Comparison (Lollipop Chart)
- Mecklenburg and Guilford clearly above statewide line (0.566)
- Durham divergence highlighted: weighted (0.41) vs unweighted (0.51) — well-served ZIPs are the populated ones
- Cabarrus and Orange have lowest Gini but small-n caveat (4 and 5 ZIPs respectively)

#### fig-29: Top 20 Underserved Dot Plot
- Overwhelming majority of dots are red (no DC fast) — 15 of 20
- Burlington (27215) at the bottom: worst density, smallest dot relative to population
- Charlotte 28215 has the largest blue dot (64,713 people) — only 2 ports but at least has DC fast
- The 732,892 people / 58 ports statistic is annotated — powerful for policy audiences

#### fig-30: Density Distribution (Histogram + KDE)
- Right-skewed distribution (skewness 2.46) with mean (11.18) pulled well above median (5.51)
- Log-scale x-axis handles the 357x range cleanly
- Justifies use of Gini coefficient and median over mean for central tendency

#### fig-31: BEV Registrations vs Port Supply
- Average ratio: ~1 port per 20 BEVs across the 10 counties
- Wake and Guilford fall below the reference line (undersupplied relative to BEV demand)
- Union is the worst: 4,160 BEVs but only ~41 ports — furthest below the reference line
- Durham and Buncombe above the line (oversupplied relative to demand)

#### fig-32: DC Fast Gap by County
- Wake and Mecklenburg dominate total port counts but have proportionally more DC fast
- Orange County: almost entirely L2, negligible DC fast — a gap for corridor travel
- Union: starved on both L2 and DC fast
- Annotation reinforces: 15 of 20 underserved ZIPs have zero DC fast

### Step 9 Findings: Theil Decomposition & Scoring Framework

#### Theil-T Decomposition (GE(1)) — The Key Finding
- **Total Theil-T: 0.5791**
- **Between-county: 0.0900 (15.5%)**
- **Within-county: 0.4892 (84.5%)**
- Robustness check (Theil-L / GE(0)): 82.5% within, 17.5% between — consistent
- Exact decomposition verified to machine precision (diff = 2.22e-16)

#### Policy Interpretation
- **84.5% of EV charging infrastructure inequality occurs WITHIN counties, not between them**
- County-level scoring alone would miss 85% of the inequality problem
- This is the statistical justification for the two-tier scoring approach:
  - Tier 1 (county-level): identifies which counties deserve NEVI attention
  - Tier 2 (ZIP-level): identifies where within those counties to deploy
- Paper framing: "County-level analysis, the standard unit in state EV planning, misses the majority of infrastructure inequality"

#### Per-County Contributions to Within-County Inequality
- Mecklenburg contributes 41.5% of within-county inequality (largest by far — Gini 0.623, pop 1.09M)
- Wake contributes 28.1% (second — Gini 0.496, pop 1.11M)
- Together Mecklenburg + Wake = ~70% of within-county inequality
- Guilford ranks 4th in contribution (7.7%) despite 2nd-highest Gini — lower population reduces absolute contribution
- Union contributes only 0.6% — uniform underservice produces low inequality but high need

#### Scoring Framework Skeleton
- 10 counties × 20 columns; 9 of 17 data columns populated from Phase 3
- BEV-per-port ratio highlights: Union at 101:1 (worst), Buncombe at 11:1 (best)
- 8 columns await Phase 4 (CTPP cost-effectiveness) and Phase 5 (Justice40 equity)
- Composite NEVI Priority Score cannot be computed until all three components available
- Note: equity_zero_station_pct is 0.0 for all counties because density CSV only includes ZIPs with stations; needs full-county ZIP coverage for signal

#### Figures
- fig-33: Theil decomposition stacked bar (84.5% within / 15.5% between)
- fig-34: County contributions to within-county inequality (Mecklenburg dominates)

### Methodology Notes
- Top 10 counties selected by BEV registration count (demand-side ranking)
- Gini coefficient computed on ports per 10,000 population across populated ZCTAs within each county
- ZCTA-to-county assignment via spatial join (point-in-polygon using AFDC lat/lon + county boundary polygons)
- 19 uninhabited ZCTAs excluded from per-capita metrics (division-by-zero guard)
- "Underserved" defined as lowest ports_per_10k; tie-broken by population descending
- 4 special ZIPs excluded from ranking (3 uninhabited, 1 PO Box) — 130 ZIPs rankable
- Step 6 uses Gini + CV for intra-county inequality (Results section)
- Step 9 must include Theil decomposition (between-county vs within-county) — maps directly to NEVI allocation policy: spread dollars across more counties or concentrate within high-need ZIPs? (Discussion section)

---

## Discussion Section

### Infrastructure Deployment Context
Include a single sentence noting that the infrastructure captured in the snapshot was deployed over a roughly 16-year window (2010–2026), giving the reader context about how mature (or immature) the network is. (Per Dr. Whitfield — narrative detail, not analytical.)

---

## Methodology Section — Phase 1 EDA Note

Per expert panel recommendation: include a brief paragraph explaining why separate EDA was not required for the Phase 1 validation data — same data structure as baseline (profiled last semester), QA checks confirmed completeness, NCDOT methodology change documented via Methodology_PostMay2025 flag.

---

*Last updated: March 12, 2026*
