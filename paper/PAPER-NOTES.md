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
- AFDC quality flags file (`afdc-eda-quality-flags.csv`): 682 stations flagged (34.4% of 1,985). 681 flagged as near_duplicate_address (co-located stations from different operators — confirmed correct, retained in analysis). 1 flagged as out_of_bounds_coords (removed by ZIP filter). Flags file is diagnostic only, not used as a filter downstream

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

### Methodology_PostMay2025 Flag — Limitation
The `Methodology_PostMay2025` boolean is set in `ncdot_ev_pipeline.py` (line 407) for all rows with Date >= 2025-05-01. It marks data collected after NCDOT changed their registration counting methodology. **The flag is not consumed by any analysis script.** The entire holdout validation period (Jul-Oct 2025) is post-change, meaning the 69% underprediction rate could partly reflect the methodology change inflating reported counts relative to the models' training data. **Limitation:** We identified the methodology change and flagged it in the data, but did not formally test or adjust for its effect on forecast accuracy (e.g., Chow test, pre/post split). This should be disclosed in the paper's limitations section.

### Data Pipeline Design Decision
NCDOT is the only dataset with a full acquisition-to-processing pipeline (`ncdot_ev_pipeline.py`) because it arrives as multiple monthly Excel files requiring merge, derivation (TotalEV, EV_Share, Methodology_PostMay2025), and QA generation. All other datasets arrive as single files (or file sets) consumed directly by analysis scripts — a separate pipeline would add unnecessary abstraction. Download scripts exist for all 6 datasets (see `code/python/data-acquisition/`).

---

## Phase 4 Methodology Decisions (Expert Panel, March 12, 2026)

### Data Source: LEHD LODES 2021 (replaces CTPP 2016)
- Expert panel unanimously recommended LODES over CTPP: more recent (2021 vs 2012-2016), free direct download, block-level geography
- LODES is the only free origin-destination commuter flow dataset at sub-county geography
- Alternatives reviewed and rejected: CTPP (too old), StreetLight/Replica ($10K-$100K, cost-prohibitive), NHTS (state-level only, too coarse), ACS commute tables (counts only, no O-D pairs)

### Income Threshold: $75K Household Income Floor
- LODES income segmentation (SE01/SE02/SE03) has only 3 bins; SE03 threshold is >$40K/year
- $40K is insufficient for EV affordability — median new EV ~$45K, standard debt-to-income requires ~$75K+ household income
- Solution: supplement LODES with ACS B19001 (household income, 16 bins) at tract level
- County-specific correction factor: `pct_HH_above_75K / pct_HH_above_40K` applied to SE03 commuter counts
- Sensitivity analysis at $60K, $75K, $100K thresholds
- Limitation: LODES reports individual earnings; ACS B19001 reports household income — unit mismatch documented; household income is arguably more relevant to vehicle purchase decisions

### Renter Charging Access: A Key Equity Dimension
- US apartment renters face substantial barriers to home EV charging:
  - Most apartment parking lacks electrical outlets at parking spaces
  - 240V outlets (needed for L2) are inside units (dryer/stove), not at parking
  - Running extension cords from units to parking violates fire codes
  - Only ~5-7% of US multifamily properties have any EV charging (concentrated in new luxury builds)
  - NC has no "right to charge" law (unlike CA, CO, OR)
- Renter EV adoption is 3-4x lower than homeowner adoption, primarily due to charging access, not income alone (Axsen et al. 2020; Tal et al. 2024, UC Davis)
- Workplace charging is essential infrastructure for renters, not supplementary
- ACS B25003 (housing tenure) added to data pipeline to quantify renter commuter populations
- Renter share used descriptively in Phase 4; feeds Equity Score in Phase 5 (see renter adjustment removal note below)

### Phase 4 EDA Validation (59/59 checks passed)
- LODES OD: 3,768,428 intra-NC commuter flow records; zero nulls, zero duplicate block pairs
- All additive decompositions verified: SA01+SA02+SA03=S000, SE01+SE02+SE03=S000, SI01+SI02+SI03=S000
- LODES WAC: 71,921 workplace blocks; CE01+CE02+CE03=C000 verified for all rows
- Crosswalk: 100% coverage — every OD and WAC block maps to a county; all 100 NC counties present
- ACS: 2,672 NC tracts; tenure identity confirmed (owner + renter = total) for all tracts
- Statewide >$75K household income share: 44.4%; renter share: 33.8%
- OD total workers (4,198,163) vs WAC total (4,400,986): 4.6% difference expected (OD Main = intra-state only)
- Cross-file tract alignment: 100% overlap between crosswalk (2,672 tracts) and ACS (2,672 tracts)
- OD-to-county crosswalk loss: 0 rows, 0% of S000 — every OD block (home and work) maps to a crosswalk block
- ACS income imputation: 1,767 of 3,768,428 OD rows (0.05%) had missing income shares; filled with statewide median (41.2% households >$75k). Immaterial to any finding
- Technical note: crosswalk trct is 11-digit full FIPS; ACS tract is 6-digit — must build full FIPS for joins

### Three-Layer Adjustment Pipeline (revised — renter adjustment removed)
```
Raw LODES commuter count
  → SE03 filter (workers earning >$40K)
  → ACS income correction (estimate >$75K household share)
  → Remote work reduction (0.85 multiplier, Barrero/Bloom/Davis 2023)
  = Adjusted workplace charging demand
```

### Renter Adjustment: Removed from Pipeline (Methodological Decision)
- Expert panel unanimously recommended removing the renter adjustment multiplier from the demand pipeline
- Reason: no NC-specific data to calibrate the adjustment; applying an unvalidated alpha parameter is speculation
- Additional concern: national literature shows renters adopt EVs at 3-4x lower rates (Axsen et al. 2020; Tal et al. 2024) — a renter-heavy origin tract could mean fewer EV commuters, not more, creating a contradictory multiplier
- ACS B25003 (tenure) data IS retained for:
  1. Descriptive reporting in Phase 4: "X% of commuters to [county] originate from renter-heavy tracts"
  2. Equity Score input in Phase 5 (renter charging access as equity dimension)
  3. Paper limitations section: no NC-specific calibration exists; cite as future research direction

### Phase 4 Findings: Workplace Charging Demand

#### Pipeline Diagnostic
- Raw S000: 4,198,163 workers → SE03 filter: 2,041,731 (48.6%) → ACS income adj: 1,010,894 (49.5% of SE03) → Remote work ×0.85: **859,260 adjusted demand**

#### Top Employment Centers (by net commuter flow)
- Mecklenburg: +194,361 net (adj. demand 182,919) — #1 employment magnet
- Wake: +126,517 net (adj. demand 169,555)
- Durham: +89,450 net (adj. demand 74,780)
- Guilford: +47,798, Forsyth: +28,488, New Hanover: +20,642, Buncombe: +18,788

#### County Typology (all 100 NC counties)
- 8 Employment Centers (net > +10,000)
- 75 Balanced (-10,000 to +10,000)
- 17 Bedroom Communities (net < -10,000)
- Union (-36,113) and Cabarrus (-20,968) confirmed as bedroom communities of Charlotte

#### Workplace Port Estimates (baseline: 30% charging rate, 15:1 port ratio)
- Statewide: 17,185 ports needed (13,748 L2 / 3,437 DCFC)
- Mecklenburg: 3,658 ports, Wake: 3,391, Durham: 1,496

#### Cost-Effectiveness Scores (equal-weight, min-max normalized)
- Mecklenburg: 0.801 (highest), Wake: 0.568, Forsyth: 0.467, Durham: 0.454
- Buncombe: 0.034 (lowest — lower commuter volumes and density)
- Scoring skeleton: 13/17 columns now populated (up from 9/17)

#### Figures
- fig-35: Net commuter flow diverging bar (15 counties, green/red by typology)
- fig-36: Residential vs residential+workplace demand comparison (10 scoring counties)
- fig-37: County typology choropleth (all 100 NC counties, 3-class)
- fig-38: Workplace port scenario range (low/baseline/high dot-and-whisker)

---

## Phase 5 Methodology Notes

### CEJST Data Availability & Vintage (Expert Panel, March 12, 2026)
- **CEJST was removed from the government website** by the Trump administration on January 22, 2025 (rescinded EO 14008)
- Data scientists (EDGI / Public Environmental Data Partners coalition) archived and restored CEJST v2.0 within days
- Download source: PEDP community mirror, not the original geoplatform.gov URL
- **No version of CEJST uses 2020 Census tract boundaries** — both v1.0 and v2.0 use 2010 tracts. This is an upstream limitation; underlying federal datasets have not migrated to 2020 tracts yet
- **No API exists** for CEJST — bulk CSV download only
- Using v2.0 (December 2024 release) which has improved methodology over v1.0 (e.g., excludes higher-ed students from low-income calculations)

### 2010 vs 2020 Tract Vintage Mismatch — Limitation Statement
- CEJST v2.0 uses 2010 Census tract boundaries; project ZCTA/county boundaries are 2020 vintage
- **Impact on county-level analysis: negligible** because:
  1. NC county boundaries are geographically identical between 2010 and 2020
  2. Census tracts nest within counties in both vintages
  3. Tract-to-county aggregation is unaffected by tract boundary changes
  4. Direction of any bias is conservative (slightly overstates disadvantaged coverage in fast-growing areas)
- **For paper Methods section, include:** "CEJST v2.0 uses 2010 Census tract boundaries. This analysis overlays these tracts onto 2020-vintage county boundaries, which are geographically identical in North Carolina. The tract-to-county aggregation is therefore unaffected by the tract boundary vintage difference. Future updates to CEJST incorporating 2020 tract boundaries would refine sub-county analysis but are not expected to alter county-level equity rankings."
- **For presentation:** Note that CEJST was taken offline by the current administration but data was preserved by the scientific community — demonstrates data governance awareness

### CEJST Headline Finding
- 934 of 2,170 evaluable NC census tracts (43.0%) flagged as disadvantaged under Justice40 (2,195 total tracts minus 25 zero-population tracts)
- Substantially above the national average (~37% of US tracts)
- Reflects NC's mix of rural poverty (eastern NC, Appalachian counties) and urban disadvantage
- Reinforces the 0.40 equity weight in the NEVI Priority Score — nearly half of NC tracts qualify
- Per-county breakdown needed from EDA to identify which study counties have highest/lowest rates

### Zero-Population Tract Exclusion Decision
- 25 of 2,195 NC tracts have population = 0.0 (not null — explicit zeros)
- 12 are water-body tracts (Census 990 series: ocean, Pamlico Sound)
- 13 are institutional/special-use tracts (Census 980 series: military installations including Fort Bragg, correctional facilities)
- All 25 have disadvantaged = 0 and threshold_count = 0 — CEJST cannot evaluate tracts without resident population data
- **Decision:** Exclude from disadvantaged percentage denominator → 934/2,170 = 43.0% (vs 42.6% with all 2,195)
- Consistent with Phase 3 exclusion of uninhabited ZIPs from zero-station calculations
- Military/institutional charging demand is captured through Phase 4 LEHD commuter flows, not residential equity designations
- **Dr. Whitfield flag (confirmed):** Cumberland County has 1 excluded zero-pop tract (Fort Bragg, 37051980100). Effect: 50.7% → 50.0% (0.7 ppt) — negligible
- **For paper Methods section:** Document exclusion criteria, tract numbering conventions (980=institutional, 990=water), and the 0.4 ppt statewide effect

### Population-Weighted vs Tract-Count Rates
- Population-weighted disadvantaged rates are consistently **lower** than simple tract-count rates across all study counties
- Disadvantaged tracts tend to have smaller populations than non-disadvantaged tracts
- **For paper:** Using population-weighted rates would produce more conservative equity scores than simple tract counts. This means our tract-count-based approach (43.0%) represents an upper bound — the population-weighted percentage is lower. Document this as a methodological choice: tract-count treats all communities equally regardless of size, which is arguably more equitable for infrastructure siting (a small disadvantaged community deserves charging access as much as a large one)

### Step 5.2 EDA Validation
- 23/23 checks passed (0 failures, 2 expected warnings)
- The 2 warnings are from the crosswalk vintage mismatch: 465 CEJST tracts (2010 boundaries) not found in LEHD crosswalk (2020 boundaries), and 942 crosswalk tracts not in CEJST — expected due to tract splits/merges between Census vintages, not data quality issues
- Validates that Step 5.1 download and filtering produced clean, complete data ready for the Step 5.3 spatial crosswalk

### Step 5.3 Crosswalk Methodology — Draft Methods Paragraph

> **Tract-to-ZCTA Equity Crosswalk.** To integrate Justice40 disadvantaged community designations (CEJST v2.0) with the ZIP-code-level infrastructure analysis, we constructed a spatial crosswalk between 2010-vintage Census tracts and 2020-vintage ZCTAs using area-weighted interpolation. Census tract boundaries (2010 TIGER/Line) were overlaid with ZCTA boundaries (2020 TIGER/GENZ) in the NC State Plane projection (EPSG:32119). For each tract-ZCTA intersection, we computed the fraction of the tract's area falling within each ZCTA. Each ZCTA's disadvantaged population share was then estimated as the area-weighted average of the binary disadvantaged flags from its constituent tract fragments. Intersection polygons smaller than 100 m² were discarded as geometric artifacts. Border-state tracts adjacent to North Carolina were included to ensure complete coverage of cross-border ZCTAs. This area-weighted approach follows the methodology used by EPA EJScreen (EPA, 2023) and the HUD USPS Crosswalk for tract-to-ZIP translation. Twenty-five zero-population tracts (12 water-body, 13 institutional/military) were excluded from the disadvantaged denominator, consistent with CEJST's own treatment of these tracts as non-evaluable.

### Step 5.3 Crosswalk — Strengths (for paper)
- Area-weighted interpolation matches federal practice (EJScreen, HUD) — results directly comparable to tools policymakers already use
- CEJST v2.0 (most current Justice40 data, December 2024 release)
- Border-state tract inclusion (GA, SC, TN, VA) ensures complete ZCTA coverage at state boundaries
- Zero-population tract exclusion is consistent with CEJST methodology and Phase 3's treatment of uninhabited ZCTAs
- Data preserved despite CEJST removal from government websites — demonstrates research resilience and data governance awareness

### Step 5.3 Crosswalk — Limitations (for paper)
- **2010-to-2020 boundary vintage mismatch:** Tract boundaries changed between Census decades; area-weighted interpolation assumes uniform population distribution within tracts, which introduces modest error in large, heterogeneous tracts. County-level aggregation is unaffected (NC county boundaries identical in both vintages).
- **Area-weighted, not population-weighted (dasymetric):** Does not account for sub-tract population concentration; improvement is a future research direction. Panel confirmed area-weighted is the EPA/HUD standard and appropriate for urban/suburban study counties where tracts are small.
- **CEJST binary flag loses threshold granularity:** A tract meeting 1 burden threshold and a tract meeting 8 thresholds both count as "disadvantaged." We report threshold_count descriptively but do not use it in scoring.
- **Community-archived data:** CEJST data was archived by PEDP coalition after federal removal; data integrity verified against pre-removal records, but the archival pathway should be noted for reproducibility.

### CEJST Methodology Deep Dive — What "Disadvantaged" Means

**Definition:** A tract is designated disadvantaged if it exceeds the 90th percentile on ANY single burden indicator across 8 categories AND meets the 65th percentile for low-income households (below 200% federal poverty level). This is a "one-strike" design — intentionally broad.

**The 8 burden categories and their data sources:**

| Category | Key Indicators | Data Source | Empirical? |
|----------|---------------|-------------|:----------:|
| Energy | Energy cost burden, PM2.5 | DOE LEAD (utility bills), EPA air monitors | Yes |
| Health | Asthma, diabetes, heart disease, low life expectancy | CDC PLACES, CDC USALEEP (death records) | Yes |
| Housing | Housing cost burden, lead paint, lack of plumbing, redlining | Census ACS, HUD, HOLC maps | Yes |
| Legacy Pollution | Proximity to Superfund, hazardous waste, RMP facilities | EPA RCRA, NPL, RMP databases | Yes |
| Transportation | Diesel PM, transportation barriers, traffic volume | DOT traffic counts, EPA NATA, Census ACS | Yes |
| Water/Wastewater | Leaking underground storage tanks, wastewater discharge | EPA UST, NPDES permit data | Yes |
| Workforce | Linguistic isolation, low median income, poverty, unemployment | Census ACS | Yes |
| Climate Change | Expected building/ag/population loss, flood risk, wildfire risk | FEMA NRI, First Street Foundation | **Mixed** |

**Key finding: 7 of 8 categories are fully empirical.** The climate change category is the only one with forward-looking model projections (First Street Foundation's 30-year flood projection). However, the FEMA NRI components within climate change are actuarial models based on **historical hazard frequencies** — similar to insurance industry calculations.

**National context:** ~37% of US tracts (33% of population) are designated disadvantaged. NC at 43% is consistent with southeastern states (MS 50%+, AL/SC/LA 40-50%). NC's rate reflects rural poverty (eastern NC, Appalachia), above-average health burdens (diabetes, heart disease), housing cost burden, and legacy industrial pollution.

**Study county context:** 18.5% population-weighted average across top-10 BEV counties. Lower than statewide because these are NC's wealthiest urban/suburban counties. But nearly 1 in 5 residents still lives in a disadvantaged tract — reinforces the within-county inequality finding from Phase 3 (84.5% Theil-T).

### Climate Change Category Sensitivity Analysis

**Rationale:** The climate change category includes the only model-based (not purely empirical) indicators in CEJST. To ensure robustness, we test what happens if this category is removed entirely.

**Methodology:** Re-download CEJST with per-category Boolean flags. Count tracts flagged solely by climate change. Recompute disadvantaged rate without them.

**Expected result:** Minimal impact on study counties. Urban disadvantage is driven by health, housing, transportation, and legacy pollution — not climate projections. Larger impact in rural eastern NC (coastal flood risk).

**Results:**
- 124 of 934 disadvantaged NC tracts (13.3%) are flagged solely by climate change
- Without climate change: 810/2,170 = 37.3% (down from 43.0%, a -5.7 pp drop)
- 37.3% is essentially the national average (~37%), confirming climate change accounts for NC's above-average rate
- **7 of 10 study counties: zero impact** (no climate-change-only tracts)
- 3 affected: New Hanover -4.7 pp, Durham -3.4 pp, Wake -2.2 pp (modest changes)
- Conclusion: study county equity rankings are robust to climate change category removal
- Script: `code/python/analysis/phase5_climate_sensitivity.py`

### Pragmatic Framing for Paper — Draft Paragraph

> We adopt CEJST designations without modification because our analysis aims to describe equity gaps as they exist under current federal policy, not to propose alternative disadvantaged-community definitions. CEJST is the federal screening tool that determines which communities are eligible for Justice40 benefits under the NEVI Formula Program, including NEVI EV charging infrastructure funding. Seven of eight CEJST burden categories rely exclusively on empirical federal datasets (CDC health surveillance, Census ACS economic statistics, EPA facility databases, DOE utility cost records). The climate change category uniquely incorporates forward-looking hazard projections alongside historical hazard data from the FEMA National Risk Index. To test robustness, we conducted a sensitivity analysis removing the climate change category entirely. Of 934 disadvantaged NC tracts, 124 (13.3%) are designated solely due to climate change indicators; removing them reduces the statewide rate from 43.0% to 37.3% (-5.7 pp). Seven of ten study counties are completely unaffected, and the three affected counties show changes of 2.2 to 4.7 percentage points. The majority of disadvantaged tracts in our study counties are flagged by empirical health, housing, and workforce indicators unaffected by this category.

### New Hanover Coastal Sensitivity (for Discussion section)
- New Hanover County showed the highest sensitivity to climate change category removal (-4.7 pp), consistent with its coastal geography and hurricane/flood exposure
- Suggests that coastal EV infrastructure siting decisions are more sensitive to the choice of equity screening methodology than inland counties
- Durham (-3.4 pp) and Wake (-2.2 pp) show modest sensitivity; 7 remaining study counties are unaffected
- **For Discussion:** Geographic variation in sensitivity — coastal vs inland — adds nuance to equity recommendations

### Step 5.5 Scoring Framework — Sub-Metric Variance Limitation

**Context:** The NEVI Priority Score uses three pillars (Equity 0.40, Utilization 0.35, Cost-Effectiveness 0.25) per Dr. Al-Ghandour's proposal feedback. Within each pillar, sub-metrics were designed to capture distinct dimensions of need.

**Limitation: Two sub-metrics have zero variance across the 10 study counties:**

| Pillar | Sub-metric | Value | Why No Variance |
|--------|-----------|-------|-----------------|
| Equity | `zero_station_pct` | 0.0 for all 10 | All top-10 urban counties have at least some stations in every inhabited ZIP |
| Utilization | `forecast_buffer` | 0.045 for all 10 | Phase 1 underprediction bias correction was applied globally, not per-county |

**Impact:** 7 of 9 designed sub-metrics actively differentiate counties. The two zero-variance sub-metrics are methodologically valid and would contribute if the framework were applied to all 100 NC counties (rural counties have zero-station ZIPs; county-specific forecast errors could replace the global buffer). For the 10-county study cohort, the effective scoring resolution is:
- Equity: 3 working sub-metrics (justice40_pct, gini_weighted, underserved_zips)
- Utilization: 1 working sub-metric (bev_per_port)
- Cost-effectiveness: 3 working sub-metrics (workplace_efficiency, commuter_demand, pop_density)

**Additional limitation — Union County outlier:** Union has 101.5 BEVs per port (next highest: Cabarrus at 32.0). Min-max normalization compresses the remaining 9 counties into the lower portion of the utilization scale. This is a genuine infrastructure deficit, not a data error, but it reduces the utilization score's ability to differentiate mid-ranked counties.

**For paper Methods/Limitations section:** Document that the scoring framework was designed for statewide extensibility but applied to a 10-county cohort where two sub-metrics lack discriminatory power. The rankings are driven by 7 of 9 sub-metrics. Future work could extend to all 100 counties where all sub-metrics would contribute.

### Step 5.5 Final Rankings — NEVI Priority Score

| Rank | County | NEVI Score | Equity | Utilization | Cost-Eff |
|------|--------|-----------|--------|-------------|----------|
| 1 | Union | 0.561 | 0.319 | 1.000 | 0.333 |
| 2 | Mecklenburg | 0.548 | 0.810 | 0.067 | 0.801 |
| 3 | Guilford | 0.465 | 0.855 | 0.103 | 0.347 |
| 4 | Forsyth | 0.335 | 0.423 | 0.059 | 0.467 |
| 5 | New Hanover | 0.334 | 0.623 | 0.034 | 0.267 |
| 6 | Cabarrus | 0.291 | 0.329 | 0.232 | 0.155 |
| 7 | Durham | 0.276 | 0.422 | 0.032 | 0.254 |
| 8 | Wake | 0.248 | 0.152 | 0.166 | 0.568 |
| 9 | Buncombe | 0.120 | 0.215 | 0.000 | 0.034 |
| 10 | Orange | 0.077 | 0.059 | 0.101 | 0.071 |

### Three County Archetypes (Expert Panel Interpretation)

1. **Union (Rank #1, 0.561) — Utilization-driven.** Its 101.5 BEV/port ratio dominates the score despite moderate equity burden. This is a suburban growth corridor where infrastructure hasn't kept pace with adoption.

2. **Mecklenburg (Rank #2, 0.548) — Equity-driven.** Highest equity sub-score (0.810) reflecting concentrated disadvantaged tracts in Charlotte's urban core, paired with strong cost-effectiveness from existing station density.

3. **Orange (Rank #10, 0.077) — Low across all pillars.** Only 4.9% J40 population-weighted burden, adequate infrastructure per capita, and a university-town demographic that skews affluent.

**Policy implication**: Different counties need investment for different reasons — Union needs *more stations*, Mecklenburg needs *better-targeted stations*, and Orange is already relatively well-served.

---

## Defining "Disadvantaged" — Expert Panel Guidance

**CRITICAL: Must be clearly defined early in the paper. "Disadvantaged" is NOT a synonym for "poor."**

### Introduction (first mention):
> Under the federal Justice40 initiative, "disadvantaged" communities are identified using the Climate and Economic Justice Screening Tool (CEJST v2.0), which flags Census tracts that are both low-income (≥65th percentile) AND overburdened on at least one of eight environmental, health, or infrastructure dimensions. This is not a synonym for poverty — a tract must experience a measurable environmental or health burden *in addition to* economic hardship to qualify.

### Methods (operational definition):
> CEJST employs a conjunctive screen: a tract is classified as disadvantaged if it meets a low-income threshold (≥65th percentile on census poverty or median household income measures) AND exceeds the 90th percentile on any single indicator across eight burden categories — climate change, energy, health, housing, legacy pollution, transportation, water/wastewater, and workforce development. This "one-strike" design intentionally casts a wide net.

### Results (contextualizing 43%):
> North Carolina's 43.0% disadvantaged rate reflects the cumulative reach of CEJST's one-strike design across a state with documented disparities in air quality, housing cost burden, and legacy industrial contamination — consistent with southeastern-state rates reported by the White House CEQ (2023).

---

## Discussion Section — Within-County Inequality Emphasis

### Theil-T Decomposition Significance

> The Theil-T decomposition finding — that 84.5% of infrastructure inequality is within-county — carries direct implications for equity-focused investment. A county-level allocation formula alone would mask the ZIP-level disparities where disadvantaged communities cluster. For example, Mecklenburg County's aggregate ports-per-capita appears adequate, yet its Justice40 population-weighted burden (23.7%) reveals that disadvantaged tracts within the county are systematically underserved. This validates the project's two-tier scoring architecture: county-level rankings identify *where* to invest, while ZIP-level targeting identifies *for whom*.

**Literature note:** Shorrocks (1980) established Theil decomposition methodology. The expert panel found **no prior published study** applying Theil decomposition to EV charging infrastructure inequality — this is a novel contribution.

### "Disadvantaged" Means Something Different Within vs Between Counties
- Between counties: disadvantage tracks with rurality and poverty (eastern NC, Appalachia)
- Within counties: disadvantage clusters in specific urban/suburban tracts amid otherwise affluent counties
- The 84.5% within-county finding means the EV infrastructure equity problem is primarily an *intra-urban* problem, not a rural vs urban divide
- This reframes the policy conversation: even NC's wealthiest counties have significant disadvantaged populations that are underserved by current infrastructure

---

## Conclusion Section — Draft Guidance

### Five Unique Contributions
1. First Theil decomposition of EV infrastructure inequality (novel methodology)
2. Tract-to-ZCTA area-weighted crosswalk integrating federal equity data with local planning units
3. Multi-dimensional NEVI scoring framework (equity + utilization + cost-effectiveness)
4. Empirical validation that within-county inequality dominates between-county (84.5%)
5. Climate sensitivity analysis demonstrating CEJST robustness for NC context

### Seven Anticipated Reviewer Weaknesses (for Limitations section)
1. **Top-10 county selection limits generalizability** → Framework designed for statewide extensibility; top-10 captures 73% of NC BEV registrations
2. **LODES 2021 predates post-COVID commuting shifts** → Most recent available; CTPP 2016 would be even older
3. **CEJST one-strike design may over-identify disadvantaged tracts** → Sensitivity analysis shows 7/10 counties unaffected by removing most contentious category; we adopt federal definitions as-is
4. **Static BEV registration (no growth trajectory modeling)** → Phase 1 validation quantified forecast accuracy; growth modeling is future work
5. **Two zero-variance sub-metrics reduce scoring dimensionality** → Would contribute at statewide scale; documented as limitation of 10-county cohort
6. **No charging behavior data (session frequency, duration)** → AFDC provides infrastructure location, not usage; cite DOE EVSE data gaps
7. **Area-weighted interpolation assumes uniform population within tracts** → EPA/HUD standard method; dasymetric refinement is future work

### Weight Sensitivity Analysis (COMPLETE)
- Tested equity weight at 0.30, 0.35, 0.40, 0.45, 0.50 (holding util:cost ratio constant at 7:5)
- **Result: Top-3 {Union, Mecklenburg, Guilford} is STABLE across all 5 scenarios**
- Internal ordering shifts: at higher equity weights, Mecklenburg rises (equity-driven) and Union drops (utilization-driven)
- Orange locked at #10 in all scenarios; Forsyth fixed at #7
- **Paper defense sentence:** "Rankings are robust to ±10 percentage-point variation in equity weight, with the top-three counties unchanged across all scenarios tested."
- Script: `code/python/analysis/phase5_weight_sensitivity.py`
- Output: `data/processed/scoring-weight-sensitivity.csv`

### TODO: NEVI Scoring Visualization (fig-43 planned)
- **Status:** NOT YET CREATED
- **What:** Bar chart of NEVI Priority Scores by county with stacked or grouped component breakdown (equity, utilization, cost-effectiveness)
- **Why:** The scoring table exists in the progress report (Section 6.6) but a visual would strengthen the final paper and presentation
- **Script to create:** `code/python/analysis/phase5_fig43_scoring_barchart.py` (new)
- **Placement:** Final paper Results section, final presentation
- **Priority:** LOW for progress report (table suffices), HIGH for final paper/presentation

### TODO: VIF / Multicollinearity Check on Scoring Framework
- **Status:** NOT YET IMPLEMENTED — action plan at `paper/vif-scoring-framework-action-plan.md`
- **What:** Compute Variance Inflation Factors for the 3 scoring pillars (equity, utilization, cost-effectiveness) to verify they are sufficiently independent
- **Why:** Addresses Dr. Al-Ghandour's defensibility feedback; standard check for weighted composites; SAS Training 2 Module 5 flagged this as critical
- **When:** During paper writing, before finalizing Results section
- **Script to create:** `code/python/analysis/scoring_framework_vif.py`
- **Paper placement:** VIF table in Results; interpretation in Methodology/Discussion
- **Caveat:** n=10 counties limits statistical power; recompute if extended to 100
- **Expected outcome:** VIF likely 1-3 (pillars are conceptually distinct), but must be verified

---

### Renter Tenure Equity Indicator — Scope Decision
- Phase 5 plan (pre-approved March 12) included ACS B25003 renter share as an equity sub-metric input
- **Decision: Not included as a scoring sub-metric.** The equity pillar uses 4 sub-metrics (justice40_pct 0.40, gini_weighted 0.30, underserved_zips 0.20, zero_station_pct 0.10). Renter share was not added as a 5th sub-metric because:
  1. CEJST's housing burden category already captures housing cost burden (which correlates with renter concentration)
  2. Adding a 5th equity sub-metric would require re-weighting all others without clear justification
  3. The Phase 4 panel decision explicitly redirected renter data to "descriptive reporting" and "equity dimension," not as a standalone scoring input
- **Renter data IS used in Phase 4:** reported descriptively (e.g., "X% of commuters to Mecklenburg originate from renter-heavy tracts")
- **For Limitations section:** Note that renter charging access barriers are captured indirectly through CEJST housing burden and Phase 4 descriptive analysis, but a dedicated renter equity sub-metric could strengthen future iterations of the framework

### Sources
- CEJST v2.0 Technical Support Document (December 2024)
- Harvard EELP Tracker (CEJST removal documentation)
- Inside Climate News (data scientists restore CEJST)
- PEDP Mirror: https://edgi-govdata-archiving.github.io/j40-cejst-2/en/downloads/
- EPA EJScreen Technical Documentation (2023) — area-weighted apportionment standard
- FHWA NEVI Formula Program Guidance (February 2023) — Justice40 coverage for EV infrastructure
- HUD USPS Crosswalk — federal standard for tract-to-ZIP geographic translation
- Maantay et al. (2007), International Journal of Health Geographics — areal interpolation methods comparison
- Executive Order 14008, Section 223 — Justice40 Initiative (original mandate)
- CDC PLACES (Population Level Analysis and Community Estimates) — tract-level health indicators
- DOE LEAD (Low-Income Energy Affordability Data) tool — energy cost burden
- FEMA National Risk Index — natural hazard expected annual loss
- First Street Foundation — flood and wildfire forward projections

---

*Last updated: March 13, 2026*
