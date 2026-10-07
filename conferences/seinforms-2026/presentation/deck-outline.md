# SEINFORMS 2026 — Locked Deck Outline

Status: **draft v1, locked for content** (step 2 of [`README.md`](README.md)).
Every number below comes from the SEINFORMS paper. Citations use the paper's
section, table, and figure numbers (`§6.2`, `Table 1 #10`, `Fig 43`), so they
also work against the submitted PDF. Manuscript line numbers (`L291`) refer to
`../seinforms_manuscript.md` and are secondary; they shift after manuscript fixes.

Structure per slide: **On-slide text** (what goes on the slide), **Figure**
(file + layout), **Sources** (paper refs, source-deck slide), **Speaker notes**
(what you say; not on the slide).

---

## Open decisions (owner)

| # | Decision | Default until decided |
|---|---|---|
| D1 | Final title | Exordo program title (below) |
| D2 | Title-slide author line | ✅ Decided: Wolfgang Sanyer, plus a smaller line "Faculty Advisor: Dr. Majed Al-Ghandour" (advisor, not co-author). Prof. Burcu Adivar (3rd author in the Exordo programme) is not on the slide, by owner decision |
| D3 | Repo link / QR code on the closing slide | ✅ Decided: `github.com/wolfieman/ev-pulse-nc` + QR code to it, and `sanyer.org/research-lab` |
| D4 | Contact line on the closing slide | ✅ Decided: `wolfgang.sanyer@gmail.com` and `linkedin.com/in/wolfgangsanyer` |

---

## Corrections log

### Deck-side (fixed in this outline)

| # | Item | Where it appears | Paper value | Fix |
|---|---|---|---|---|
| C1 | Gini 0.805 presented as charging inequality | Showcase s5; MBA README | 0.805 = county BEV *ownership* Gini; 0.566 = ZIP-level *charging* Gini (Table 1 #6, #7) | Each number used for what it measures (slides 3, 7) |
| C2 | 24.9% of stations in disadvantaged tracts | Showcase s7 | **24.5%** (296 of 1,210) (Table 1 #10) | Slide 9 |
| C3 | "Federal law requires 40%" / "Three federal mandates" | Showcase s7, s8 | Analytical anchor; EO 14008 rescinded Jan 2025 (§2.3, §3.4) | Slides 9, 10 |
| C4 | Justice40 headline "mandate 40%, reality 25%" | Showcase s7 | Against the comparable 18.5% study-county benchmark, the 24.5% station share is roughly proportional; the gap is county-by-county variation (§6.5) | Slide 9 reframed |
| C5 | "47.6% of infrastructure added in 2024–25" | Showcase s4 | Not in the paper | Dropped |
| C6 | Guilford "Balanced across all three pillars" | Showcase s9 | Equity-dominated; cohort-highest equity 0.855; same archetype as Mecklenburg (§6.7, §7.3) | Slide 12 |
| C7 | Archetype labels for ranks 4–10 (e.g., Buncombe "Rural") | Showcase s9 | Not in the paper | Replaced by Table 2 pillar scores (B3) |
| C8 | "Five stakeholder groups" | Showcase s12 | Six (§8.2) | Slide 14 |
| C9 | "47 publication-grade figures" | Capstone s21 | 42 (§8.1) | Not used on slides |
| C10 | ACS "2021 5-year" | Capstone s7 | ACS **2022** five-year (§5.3) | Slide 4, B4 |
| C11 | "First mentioned Theil-T decomposition" | Showcase s12 | Use §10.3 Contribution 1 wording | Slide 13 |
| C12 | "1,727% in seven years" | Showcase s3 | Sep 2018 → Jun 2025 (§1.2) | Slide 3 says "since 2018" |

### Manuscript-side (fix at step 9; only matters for any proceedings/camera-ready version)

| # | Location | Issue | Proposed fix |
|---|---|---|---|
| M1 | §1.2 (L25) | "As of January 2026, the state has 1,985 stations" vs February 2026 AFDC pull everywhere else | "As of February 2026" |
| M2 | §1.2 (L25) | "top 10 counties hold 72% of all BEVs" vs 73% everywhere else | Verify against repo data, then align |
| M3 | §2.3 (L49) | "satisfying the Justice40 mandate" contradicts "informed by, not mandated by" later in the paragraph | "aligned with the Justice40 target" |
| M4 | §2.4 (L53) | "federal equity mandates" | "federal equity designations" |
| M5 | §1.2, §2.1, §3.1 vs Table 1 #5, §6.4 | Two benchmarks: "recommended 10 to 15" (DOE) and IEA "≈10" | Optional harmonize; the deck uses IEA ≈10 (referenced) |

---

## Instructions for Gamma (paste first)

> Build a 16:9 conference presentation from the outline below, one card per
> slide, in order, 14 main slides then 4 backup slides.
> - Use the uploaded figure images exactly as provided. Do not crop, recolor,
>   redraw, or regenerate them, and do not generate any charts or graphs.
> - Keep every number, label, and county name exactly as written. Do not round,
>   paraphrase, or add statistics.
> - On-slide text only: use the "On-slide text" sections. Put the "Speaker
>   notes" sections in the slide notes, not on the slides.
> - Visual style: clean, academic, high contrast, readable from the back of a
>   room. Decorative elements are fine; they must not overlap figures or numbers.

---

## Slide 1 — Title

**On-slide text**

- Title (D1): *EV Pulse NC: A Data-Driven Framework for Equitable and
  Demand-Driven EV Charging Infrastructure Investment Prioritization in North
  Carolina*
- Wolfgang Sanyer · MBA, Business Analytics · Fayetteville State University
- Faculty Advisor: Dr. Majed Al-Ghandour (D2)
- SEINFORMS 2026 · Myrtle Beach, SC · October 2026

**Figure:** none.

**Sources:** Exordo listing; showcase s1.

**Speaker notes** (~30 s)

Good morning. I'm Wolfgang Sanyer, an MBA student in business analytics at
Fayetteville State. This talk is about how North Carolina could decide where
$109 million in federal EV charging money should go, and what the data says
about where the real gaps are.

---

## Slide 2 — The Problem

**On-slide text**

- Headline: **$109 Million. 100 Counties. No Allocation Framework.**
- NC's federal NEVI Formula Program funding: **$109M**
- No publicly available, data-driven method for allocating it across counties
- Efficiency vs. equity: demand-driven allocation reinforces existing
  concentration; equity-driven allocation can place stations where use is too
  low to sustain them
- Feb 2026: NCDOT shifts from 50 interstate-corridor stations toward **16 rural
  and community locations**

**Figure:** none (stat-card layout).

**Sources:** §1.2, §2.1 (L25, L41); showcase s2; capstone s3.

**Speaker notes** (~50 s)

North Carolina has $109 million in NEVI formula funding for public charging.
What it doesn't have is a published, data-driven way to decide which counties
get it. The two obvious approaches pull against each other. Follow demand, and
you put chargers where they already are. Follow equity alone, and you can build
stations nobody uses. NCDOT itself moved in February 2026, from a corridor-only
plan to 16 rural and community sites. So this is a live decision, and the
question is whether there's a defensible way to make it.

---

## Slide 2a — Research Questions

Added at owner request (option A). In the deck it is slide 3, and every later
slide shifts by one; outline slide numbers are kept as they were.

**On-slide text**

- Headline: **Five Questions Drive the Work**
- 1 · Forecast Accuracy: How accurate are SAS Model Studio's county-level BEV
  forecasts against unseen data?
- 2 · Demand-Supply Gaps: Where are the largest demand-supply gaps?
- 3 · Sub-County Inequality: How do ZIP-level density patterns reveal
  priorities county aggregation obscures?
- 4 · Commuter Flows: How do commuting flows reshape demand once workplace
  needs are layered onto residential data?
- 5 · Defensible Rankings: Can a weighted scoring equation translate these
  layers into defensible recommendations?

**Figure:** none (five numbered rows; deliberately not the card layout of slide 4).

**Sources:** §1.3 (L29) for the questions; capstone s5 for the labels. The
capstone subtitle "each maps directly to one of the five analytical phases" is
not used: question 5 is answered by the scoring framework, and Phase 5 has no
question of its own.

**Speaker notes** (~50 s)

Five questions drive the work. Can the county forecasts be trusted on data
they haven't seen? Where are the biggest gaps between demand and supply? What
do ZIP codes show that county averages hide? How does commuting change where
charging is needed? And can one weighted score turn all of that into a ranking
you can defend? The rest of the talk answers them in order.

---

## Slide 3 — Demand Signal

**On-slide text**

- Headline: **The BEV Fleet Grew 1,727% Since 2018. Ports Have Not Kept Pace.**
- **5,165 → 94,371** BEVs (Sep 2018 → Jun 2025) · **53.8%** compound annual growth
- **Gini 0.805**: county-level BEV ownership is highly concentrated; Wake alone
  holds more BEVs than the bottom 60 counties combined
- **16.9 BEVs per public port** (Feb 2026) vs. IEA global benchmark **≈10**
- Top 10 counties hold **73%** of the statewide BEV fleet

**Figure:** none (four stat cards).

**Sources:** §1.2 (L25), Table 1 #5, #6, Abstract, §2.2; showcase s3; capstone s4.

**Speaker notes** (~50 s)

Demand isn't the question. The fleet went from 5,165 battery-electric vehicles in 2018 to 94,371 by mid-2025, a 53.8% annual growth rate. It's
also very concentrated: a county-level Gini of 0.805, and Wake County alone has
more EVs than the bottom 60 counties put together. Supply hasn't kept up. North Carolina has 16.9 EVs per public port, against a global benchmark of about 10. The top 10 counties hold 73% of the fleet, which is why the scoring focuses
on them.

---

## Slide 4 — Five-Phase Pipeline

**On-slide text**

- Headline: **Five Analytical Phases, One Scoring Framework**
- Phase 1 · Forecast validation (NCDOT registrations, Sep 2018–Oct 2025)
- Phase 2 · Infrastructure baseline (NREL AFDC API, Feb 2026: 1,985 stations,
  6,145 connectors)
- Phase 3 · ZIP-level inequality (Gini + additive Theil-T decomposition)
- Phase 4 · Workplace charging demand (LEHD LODES 2021)
- Phase 5 · Justice40 equity overlay (CEJST v2.0, area-weighted tract-to-ZCTA
  crosswalk)
- Footer: All public data · 8,600 county-month observations · Python + SAS
  Model Studio

**Figure:** none (five-step flow diagram feeding a "NEVI Priority Score" box).

**Sources:** §4.1, §2.2, §4.8; capstone s6–s7. ACS is 2022 five-year (C10).

**Speaker notes** (~50 s)

The work runs in five phases. Phase 1 tests the demand forecasts on data they
never saw. Phase 2 rebuilds the supply side from a full AFDC pull, all charger
levels, not just fast chargers. Phase 3 measures inequality at the ZIP level.
Phase 4 adds workplace demand from Census commuter flows. Phase 5 overlays the
federal disadvantaged-community designations. Everything feeds one score.
Every input is public, and the whole pipeline reruns from the repository.

*(Cut candidate for a 15-minute slot: move to backup.)*

---

## Slide 5 — Forecast Validation

**On-slide text**

- Headline: **Forecasts Hold Out of Sample, and Adoption Is Accelerating**
- **MAPE 4.34%** on a true holdout (n = 400 county-months, Jul–Oct 2025, all
  100 counties)
- **69.00%** of actuals exceeded forecast (mean bias +18.22 vehicles per
  county-month)
- **Chow test: F = 1,268.35, p < 1 × 10⁻⁶** at the Aug 2022 Inflation
  Reduction Act passage
- 95% interval coverage **75.50% raw → 93.75%** after county bias correction:
  a centering problem, not a width problem

**Figure:** `fig-44-validation-scatter.png` (aspect 1.25). Figure left (~60% of
width), bullets right.

**Sources:** §6.1, §4.2, §4.9, Table 1 #1–#4 (L262–L266, L190, L194); capstone s11.

**Speaker notes** (~75 s)

First question: can we trust the demand forecasts? The SAS models were tested
on four months they never saw, all 100 counties, 400 observations. The error
was 4.34%, under the 5% usability bar. But look at the scatter: most points sit
above the line. In 69% of cases actual registrations beat the forecast. That
isn't a broken model. A Chow test puts a strong structural break at the Inflation Reduction Act in August 2022, F of 1,268.35. The models learned a
slower world. The intervals are the right width but centered too low, so the
fix is an upward buffer of 4 to 5% in planning, which the score carries.

---

## Slide 6 — Infrastructure Gap

**On-slide text**

- Headline: **58.5% of NC ZIP Areas Have No Charging Station**
- **499 of 853** ZCTAs have zero stations: **2.2 million people** (21.1% of the
  state)
- Charlotte 28202: **78.64** ports per 10,000 residents
- Charlotte 28215, 14 miles east: **0.31** (64,713 residents, 2 ports)
- **250-fold gap inside one county**

**Figure:** `fig-24-heatmap-mecklenburg.png` (portrait, aspect 0.92). Figure
right (~45% of width), bullets left.

**Sources:** §6.2, §6.3 (L291–L293, L307); showcase s4, s10; capstone s12.

**Speaker notes** (~75 s)

On the supply side, more than half of North Carolina's ZIP areas have no
charger at all, covering 2.2 million people. That's not only a rural story.
This map is Mecklenburg. Uptown Charlotte, the dark cluster, has 78.64 ports per 10,000 residents. Fourteen miles east, ZIP 28215 has 64,713 people and two ports. That's a 250-fold difference inside one county. Hold on to this
picture, because the next slide shows it isn't an outlier.

---

## Slide 7 — The Headline Finding (Theil)

**On-slide text**

- Headline: **84.5% of Charging Inequality Is Within Counties**
- Theil-T (top 10 counties) = **0.5791** = between **0.0900 (15.5%)** +
  within **0.4892 (84.5%)**
- Exact additive decomposition (GE(1)); verified to **2.22 × 10⁻¹⁶**; Theil-L
  check: **82.5%** within
- ZIP-level charging Gini (statewide, population-weighted): **0.566**
- County-only formulas miss most of the problem → **two-tier design**: county
  ranking + ZIP-level targeting

**Figure:** `fig-33-theil-decomposition.png` (aspect 1.73). Figure top, full
width; bullets below.

**Sources:** §6.3, §4.4, §3.3, Table 1 #7, #8 (L303–L305, L133–L139); capstone s9, s12; showcase s5. Fixes C1.

**Speaker notes** (~80 s)

This is the central result. The Gini tells you inequality is high, 0.566
across ZIP codes, but not where it lives. The Theil-T index splits exactly into
a between-county part and a within-county part, with no residual. For the top
10 counties, 84.5% of the inequality is within counties, not between them. The
Theil-L version gives 82.5%, so it isn't an artifact of the index. Mecklenburg
and Wake alone account for about 70% of it. The implication is structural: most
state NEVI formulas allocate by county, so they miss most of the problem. That
is why the framework has two tiers: rank the counties, then target ZIP codes
inside them.

---

## Slide 8 — Workplace Demand

**On-slide text**

- Headline: **Commuters Shift Demand Toward Employment Centers**
- LEHD LODES 2021: 4,198,163 workers → **859,260** EV-relevant commuters
  (income filter, ACS $75K household correction, 0.85 remote-work multiplier)
- Net daily inflow: Mecklenburg **+194,361** · Wake **+126,517** · Durham
  **+89,450**
- Union (ranked #1) is a bedroom community: **−36,113** net per day

**Figure:** `fig-36-demand-comparison.png` (aspect 1.39). Figure left (~60%),
bullets right.

**Sources:** §6.4, §4.6 (L311–L315); new slide (replaces showcase s6 chart,
which is not a paper figure).

**Speaker notes** (~70 s)

Registration data tells you where EVs sleep, not where they park during the
day. Census commuter flows fill that in. Starting from 4,198,163 workers, I
filtered by income, corrected to EV-affordable households, and applied a
remote-work adjustment, leaving 859,260 commuters. Mecklenburg takes in 194,361 more workers a day than it sends out. Union, which ends up ranked first,
is a bedroom community of Charlotte, with a net outflow of 36,113
commuters a day; its residents drive to Mecklenburg for work. This feeds the
cost-effectiveness pillar.

*(Cut candidate for a 15-minute slot: move to backup.)*

---

## Slide 9 — Justice40 Overlay

**On-slide text**

- Headline: **Where Stations Sit vs. Where Disadvantaged Communities Live**
- **43.0%** of NC census tracts designated disadvantaged (934 of 2,170; CEJST v2.0)
- Top 10 counties: **18.5%** population-weighted disadvantaged rate
- **24.5%** of stations (296 of 1,210) sit in disadvantaged tracts: roughly
  proportional overall, with **strong county-by-county variation**
- Removing CEJST's climate category: **7 of 10** study counties unchanged
- Footnote: CEJST v2.0 as of Jan 21, 2025; tool removed Jan 22, 2025 after
  EO 14008 was rescinded; data from the EDGI / PEDP archive

**Figure:** `fig-42-stations-justice40-overlay.png` (wide, aspect 1.63). Figure
full width; bullets as a compact strip below.

**Sources:** §6.5, §4.5, §5.5, Table 1 #9, #10 (L319–L325, L149, L240); capstone s15; showcase s7. Fixes C2–C4.

**Speaker notes** (~75 s)

Phase 5 overlays the federal disadvantaged-community map. Statewide, 43.0% of tracts are designated disadvantaged. In the top 10 EV counties it's 18.5% of
the population. About a quarter of stations, 24.5%, sit in those tracts. So in
aggregate the siting is roughly proportional. The story is in the variation:
some counties site stations in line with their disadvantaged population, others
fall well short, and that variation is what drives the equity pillar. One
caveat I want to be upfront about: the federal screening tool was taken down
in January 2025. I use the archived v2.0 data, and removing its most contested
category leaves 7 of 10 counties unchanged.

---

## Slide 10 — Scoring Framework

**On-slide text**

- Headline: **NEVI Score = 0.40 × Equity + 0.35 × Utilization + 0.25 × Cost-Effectiveness**
- Each pillar is a weighted composite of sub-metrics, **min-max normalized to 0–1**
- Weights follow data confidence:
  - Equity 0.40: analytical anchor on the Justice40 40% target (EO 14008,
    rescinded Jan 2025)
  - Utilization 0.35: BEVs per port, from validated forecasts (strongest data)
  - Cost-Effectiveness 0.25: workplace demand (most uncertain input)
- Pillars are independent: **max VIF 1.41** (concern threshold 5.0)

**Figure:** none (formula banner + three pillar cards).

**Sources:** §2.3, §4.7, §4.9, Table 1 #12 (L49, L165–L169, L188); capstone s10; showcase s8. Fixes C3.

**Speaker notes** (~70 s)

The score combines three pillars. Each one is built from sub-metrics, all
min-max normalized to a 0-to-1 scale. The weights follow data confidence.
Equity gets 0.40, anchored on the Justice40 40% target. I treat that as an
analytical anchor, not a legal requirement, since the executive order was
rescinded in January 2025. Utilization gets 0.35 because it rests on the
validated forecasts. Cost-effectiveness gets 0.25 because workplace demand is
the least certain input. And the pillars aren't three views of one thing: the
highest variance inflation factor is 1.41.

---

## Slide 11 — Rankings

**On-slide text**

- Headline: **Top 3: Union, Mecklenburg, Guilford**
- **Union 0.561 · Mecklenburg 0.548 · Guilford 0.465**
- Top 3 held across three perturbations:
  - equity weight 0.30–0.50 (five scenarios)
  - cost-effectiveness sub-weight extremes
  - remote-work multiplier 0.75 / 0.85 / 0.95 (cancels in normalization)
- Wake ranks 5th despite the most BEVs (equity 0.322; 8.1% of tracts
  disadvantaged)

**Figure:** `fig-43-nevi-priority-scores.png` (aspect 1.45). Figure left
(~60%), bullets right.

**Sources:** §6.6, §4.7.1, §9.2 (0.75 / 0.85 / 0.95, L428), Table 2, Table 1 #11 (L335–L354, L178); capstone s13; showcase s9. Fixes C7.

**Speaker notes** (~75 s)

Here's the result. Union, Mecklenburg, and Guilford come out on top, and each
bar shows how much of the score comes from each pillar. The top three held
under three separate tests: moving the equity weight from 0.30 to 0.50, the
extremes of the cost-effectiveness sub-weights, and the remote-work assumption,
which cancels out in the normalization. To be precise about what that means:
these are one-factor-at-a-time tests, not a full search over all weight
combinations. Notice Wake: the most EVs in the state, but fifth, because its
equity burden is low.

---

## Slide 12 — Three Archetypes

**On-slide text**

- Headline: **Three County Archetypes**
- **Union: utilization-driven.** 101.5 BEVs per port, 3× the next county →
  *more stations*
- **Mecklenburg & Guilford: equity-driven.** Equity 0.810 and 0.855 →
  *better-targeted stations* in underserved ZIPs
- **Orange: low across all pillars** (0.077) → no priority deployment now
- **Empty quadrant:** no county is high on both equity and utilization

**Figure:** `fig-45-equity-utilization-archetypes.png` (near-square, aspect
1.14). Figure right (~50%), bullets left.

**Sources:** §7.3, §6.6 (L386–L394, L348); capstone s14 (headline; Orange "no priority deployment" wording). Fixes C6.

**Speaker notes** (~75 s)

The ranking says where, but not why. Plotting equity against utilization gives
three archetypes. Union is utilization-driven: 101.5 EVs per port, more than three times the next county. It needs more stations. Mecklenburg and Guilford are
equity-driven. They don't just need more stations, they need them in the right
ZIP codes. Orange scores low on everything and doesn't need priority
deployment now. Then look at the top-right corner: it's empty. No county is
high on both equity and utilization, so every county is a trade-off, and the
framework makes that trade-off visible instead of hiding it.

---

## Slide 13 — Contributions and Limitations

**On-slide text**

- Headline: **Contributions and Limitations**
- Contributions:
  1. Additive Theil-T decomposition of EV charging inequality, used as a design
     input to allocation
  2. Area-weighted CEJST–AFDC crosswalk at ZIP resolution (23 of 23 validation
     checks)
  3. Three-pillar NEVI score with VIF-confirmed independence and a robust top 3
- Limitations, each with a direction of bias:
  - Top-10 scope (73% of fleet): bounded
  - LODES 2021 vintage: cancels in normalization
  - Static BEV counts: understates growth (conservative)
  - CEJST v2.0 lock, NEVI rule changes: policy risk

**Figure:** none (two-column layout).

**Sources:** §10.3, §9, §9.11, §7.1 (L478–L490, L420–L464); capstone s16–s17. Fixes C11.

**Speaker notes** (~70 s)

Three contributions. First, using the Theil decomposition as a design input,
not just a summary number; prior EV work, such as Choi, Xu and Jiao on Austin,
reports Theil as a single magnitude. Second, a validated crosswalk that brings
the federal equity designations down to ZIP level. Third, a score whose pillars
are independent and whose top three survives perturbation. On limitations, I
gave each one a direction. The scope covers 73% of the fleet. The 2021
commuting data cancels out in normalization. Static counts understate growth,
which makes the scores conservative. None of them overturns the top three.

---

## Slide 14 — Implications and Next Steps

**On-slide text**

- Headline: **Decision Support, Not Decision-Making**
- NCDOT / FHWA: an auditable county ranking (VIF 1.41, MAPE 4.34%, robust top 3)
- County planners: ZIP-level gap analysis for site selection
- Next: all 100 counties · validate against NCDOT's actual NEVI deployments ·
  confidence intervals on composite scores
- Thank you · wolfgang.sanyer@gmail.com · linkedin.com/in/wolfgangsanyer ·
  github.com/wolfieman/ev-pulse-nc (with QR code) · sanyer.org/research-lab

**Figure:** none.

**Sources:** §10.4, §7.2, §8.2, §11 (L494, L372–L382, L504–L512); showcase s12–s14; capstone s18–s19, s25. Fixes C8.

**Speaker notes** (~40 s)

This isn't meant to replace NCDOT's judgment. Right-of-way, utilities, and
politics all matter and aren't in the model. What it gives is an analytical
floor: a ranking an auditor can trace, and ZIP-level targets a planner can use.
Next steps are extending it to all 100 counties, checking it against NCDOT's
actual deployments, and putting confidence intervals on the scores. Thank you,
I'm happy to take questions.

---

## Backup slides (for Q&A; not presented)

### B1 — Theil-T Decomposition

**On-slide text**

- GE(1) / Theil-T is additively decomposable: **T = T_between + T_within**,
  with no residual (Bourguignon 1979; Shorrocks 1980)
- Top 10 counties: **0.5791 = 0.0900 (15.5%) + 0.4892 (84.5%)**
- Theil-L (GE(0)) robustness: **82.5%** within
- Within-county contribution: Mecklenburg **41.5%**, Wake **28.1%**, Guilford
  **7.7%**, Union **0.6%**
- Theil is a diagnostic for the architecture (why Tier 2 exists), not an input
  to either tier's score

**Figure:** `fig-33-theil-decomposition.png` (reuse) or none.

**Sources:** §6.3, §4.4, §3.3 (L303–L305, L139). Before adding the full formula,
take it from the repo's Theil script so the notation matches the code.

### B2 — Crosswalk Validation

**On-slide text**

- CEJST v2.0 (2010 tracts) → 2020 ZCTAs, area-weighted in NC State Plane
  (EPSG:32119), the EPA EJScreen / HUD USPS approach
- **12 checks in 3 tiers, 23 of 23 sub-checks passed**; per-ZCTA area
  conservation within 1%
- Slivers < 100 m² dropped; border-state tracts (VA, SC, TN, GA) included;
  25 zero-population tracts excluded
- Known limit: uniform within-tract population (weaker in large rural tracts)

**Sources:** §4.5, §7.1, §9.7 (L143–L147, L368, L448).

### B3 — Full NEVI Scores (Table 2)

**On-slide text:** Table 2, all 10 counties:

| Rank | County | NEVI | Equity | Utilization | Cost-Eff. |
|:--:|---|:--:|:--:|:--:|:--:|
| 1 | Union | 0.561 | 0.319 | 1.000 | 0.333 |
| 2 | Mecklenburg | 0.548 | 0.810 | 0.067 | 0.801 |
| 3 | Guilford | 0.465 | 0.855 | 0.103 | 0.347 |
| 4 | New Hanover | 0.341 | 0.607 | 0.071 | 0.293 |
| 5 | Wake | 0.316 | 0.322 | 0.130 | 0.568 |
| 6 | Durham | 0.313 | 0.469 | 0.033 | 0.454 |
| 7 | Forsyth | 0.285 | 0.283 | 0.156 | 0.467 |
| 8 | Cabarrus | 0.199 | 0.228 | 0.229 | 0.111 |
| 9 | Buncombe | 0.197 | 0.470 | 0.000 | 0.034 |
| 10 | Orange | 0.077 | 0.059 | 0.101 | 0.071 |

Footer: equity weight 0.30–0.50 sweep: top 3 unchanged; Mecklenburg gains and
Union falls as the equity weight rises; Orange stays 10th.

**Sources:** Table 2, §6.6 (L335–L354).

### B4 — Data Sources and Diagnostics

**On-slide text**

| Source | Content | Window |
|---|---|---|
| NCDOT | Monthly county BEV registrations | Sep 2018 – Oct 2025 |
| NREL AFDC API | Station inventory, all levels | Feb 2026 pull |
| U.S. Census ACS + TIGER | Income, tenure, population; boundaries | ACS 2022 five-year; TIGER 2020 |
| LEHD LODES | Block-level commuter flows | 2021 |
| CEJST v2.0 | Disadvantaged tract designations | Dec 2024 release (EDGI / PEDP archive) |

- CSS vs. MLE estimator: forecast difference **< 0.1%**
- NCDOT counting change (May 2025): ~**0.4%** of totals, works *against* the
  underprediction
- Pillar correlations: E–U −0.26 · E–CE +0.48 · U–CE −0.03

**Sources:** §5.1–§5.5, §4.9 (L188–L192, L206). Fixes C10.

---

## Figure inventory

| Slide | File (`output/figures/`) | Pixels | Aspect | Layout |
|---|---|---|---|---|
| 5 | `fig-44-validation-scatter.png` | 4569 × 3669 | 1.25 | Left 60% |
| 6 | `fig-24-heatmap-mecklenburg.png` | 3384 × 3669 | 0.92 (portrait) | Right 45% |
| 7, B1 | `fig-33-theil-decomposition.png` | 4269 × 2469 | 1.73 | Full width, top |
| 8 | `fig-36-demand-comparison.png` | 4269 × 3069 | 1.39 | Left 60% |
| 9 | `fig-42-stations-justice40-overlay.png` | 6069 × 3733 | 1.63 | Full width |
| 11 | `fig-43-nevi-priority-scores.png` | 4869 × 3369 | 1.45 | Left 60% |
| 12 | `fig-45-equity-utilization-archetypes.png` | 4869 × 4269 | 1.14 | Right 50% |

Projector legibility (label and tick size at slide scale) is checked at step 3.
