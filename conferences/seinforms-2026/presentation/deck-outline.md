# SEINFORMS 2026 — Locked Deck Outline

Status: **deck v6 (2026-10-10), after the whole-deck review**; all 15 talk
slides locked (slide 15 locked 2026-10-10 with its v6 takeaways).
Every number below comes from the SEINFORMS paper. Citations use the paper's
section, table, and figure numbers (`§6.2`, `Table 1 #10`, `Fig 43`), so they
also work against the submitted PDF. Manuscript line numbers (`L291`) refer to
`../seinforms_manuscript.md` and are secondary; they shift after manuscript fixes.

The deck is built by `src/paper/seinforms_deck/build.js`. The per-slide section
at the end ("Current deck (v6)") is generated from the built presenter edition,
so it matches the deck exactly: on-slide text, native chart titles, and speaker
notes with word counts. The earlier hand-written v1–v4 per-slide sections (with
manuscript line references per slide) are in git history.

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

## Deck v5 decisions (owner, 2026-10-09)

**Slide review status (deck numbering, title = slide 1):** 🔒 1 Title · 🔒 2 The
Problem · 🔒 3 Research Questions · 🔒 4 Demand Signal · 🔒 5 Pipeline · 🔒 6 Forecast Validation · 🔒 7 Infrastructure Gap · 🔒 8 Theil · 🔒 9 Workplace Demand · 🔒 10 Justice40 (cut candidate) · 🔒 11 Framework · 🔒 12 Rankings · 🔒 13 Archetypes · 🔒 14 Contributions · ⬜ 15 (slide 4 notes reopened for the Gini definition on 2026-10-10, then re-locked). The v6 section below supersedes this list where they differ.

- **Slide 1 locked:** "Faculty Advisors: Dr. Majed Al-Ghandour, Dr. Burcu
  Adivar"; program stays "MBA, Business Analytics"; speaker notes end with the
  spring-2026 sentence above.
- **Abbreviations:** spelled out in place at first use and said aloud: NEVI,
  NCDOT (slide 2); BEV (research questions); IEA (demand signal); MAPE
  (forecast); GE(1) (Theil); ACS (workplace); EO, EDGI, PEDP (Justice40 note);
  VIF (framework); FHWA (closing). The pipeline slide carries one small line
  spelling out NREL, AFDC, API, LEHD LODES, CEJST, ZCTA. EV, SAS, NC and ZIP stay
  as is.
- **Data as of:** first data slide (demand signal) carries "Data as of Feb 2026:
  NCDOT registrations through Oct 2025; Alternative Fuels Data Center (AFDC)
  stations as of Feb 2026".
- **Backup slides:** B5 glossary added. The builder writes three files: upload
  (15 talk slides, sent for the Ex Ordo upload), presenter (talk + B1–B5, USB),
  and backup (B1–B5 only, USB).
- Gamma step skipped; the deck is built and kept in PowerPoint.
- **Slide 2 (option B, owner):** card 3 reads "The NC Department of Transportation
  (NCDOT) revises its NEVI plan, narrowing the corridor buildout and shifting
  funds toward rural and community charging". The paper's "16 rural and community
  locations" wording is dropped: NCDOT's Jan 27, 2026 release cut the corridor
  buildout from 41 to 16 corridor sites to free funds for a later community phase
  (see the Q&A briefing). Speaker notes say NEVI and NCDOT in full and match the card.
- **Slide 2 claim narrowed (owner, after advisor feedback):** title "$109
  Million. 100 Counties. No Data-Driven County Ranking."; card 2 "No county
  ranking: NCDOT has a federally approved NEVI plan, but no publicly available,
  data-driven method for ranking counties" (paper §2.1, §2.3). Notes add that
  NCDOT is building corridors in rounds and the community phase is still ahead
  (the Sept 2026 awards were Round 2 of Phase 1).
- **Slide 5:** footer reads "SAS Model Studio forecasts (fall 2025), validated in
  Python (spring 2026)"; notes say AFDC, LODES and CEJST in full.
- **Slide 6:** title "Forecasts Hold Out of Sample, and Adoption Accelerated
  After 2022" (past tense: federal EV purchase credits ended Sept 30, 2025);
  notes say MAPE in full and end on the planning buffer (paper §4.9) instead of
  "which the score carries" (the buffer is uniform across the cohort, §4.7).
- **Slide 6 figure:** talk version of Fig 44 (`src/paper/seinforms_deck/fig44_talk.py`,
  output `assets/fig-44-validation-scatter-talk.png`): same 400 points (verified
  identical), spelled-out legend with county-month counts, larger text and
  Mecklenburg callout, statistics inset and figure title removed. Notes walk
  through the chart, spell out ARIMA, explain the Chow test and the interval
  coverage. Cheat sheet in `qa-bank.md`.
- **Slide 7:** bullet "499 of 853 ZIP areas have zero stations" (ZCTA stays on
  slide 5 and in the glossary). The paper's map image is unchanged; the slide
  overlays labels "28202 Uptown: 78.64" and "28215: 0.31" (positions from
  `fig24_labels.py`, raw ZCTA boundaries, map projection), a projector-size
  legend ("Triangles: DC fast-charging stations · Colors: all charging ports ·
  No charging stations"), and a white patch over the corner box (its population
  and port counts are not in the paper text). Notes explain the map.
- **Slide 8:** the Fig 33 image (its title and subtitle overlap) is replaced by a
  native PowerPoint stacked bar of the paper's values (§6.3: between 0.0900,
  within 0.4892, total 0.5791). The first bullet (same numbers) is dropped. Notes
  add a plain-language explanation of within vs. between.
- **Slide 9 (advisor feedback; Tufte/Knaflic):** Fig 36 replaced by a native
  diverging bar of net daily commuters for the four counties the paper reports
  (§6.4: Mecklenburg +194,361, Wake +126,517, Durham +89,450, Union −36,113).
  LEHD LODES spelled out on the slide; "859,260 adjusted commuters" (paper
  wording); cost-effectiveness link (Mecklenburg 0.801). Fig 36 moved to backup
  B5 with a blue/orange explanation; glossary is now B6.
- **Slide 10 (Tufte/Knaflic):** Fig 42 replaced by a native bar of residents in
  disadvantaged tracts for the counties the paper reports (§6.5: Guilford 29.2%,
  New Hanover 28.8%, Durham 26.6%, Mecklenburg 23.7%, Wake 8.1%) with the
  top-10 average 18.5% as a grey bar. Notes define "disadvantaged" (CEJST, §3.4).
  Fig 42 moved to backup B6 with L2 and DCFC spelled out (its marker colours
  differ from slide 7); glossary is now B7 and adds DCFC and L2.
- **Slide 10 redesign (owner):** title "Roughly Proportional Overall; Equity Gaps
  Are County by County". Left: stat tiles 24.5% of stations / 18.5% of residents
  (stations and communities together, as the message needs). Right: a dot plot
  of residents in disadvantaged tracts by county (same §6.5 values) with a
  dashed 18.5% average line, so it no longer repeats slide 9's bar layout. Orange (4.9%, §6.6) added as a sixth dot; notes link back to slides 7–8
  (proportional in total, not well served inside each county).
- **Slide 11:** utilization card reads "BEVs per port; demand data validated out
  of sample (strongest data)" (the pillar is registrations ÷ ports, §4.7); green
  bar reads "Pillars measure different things" (VIF 1.41; Equity–CE r = +0.48,
  §4.9). Notes explain min-max and the VIF in plain words.
- **Slide 12:** Wake box reads "8.1% of residents in disadvantaged tracts"
  (matches slide 10, §6.5); robustness shows the two tests with full results
  in the paper (equity-weight sweep, remote-work multiplier; the
  cost-effectiveness sub-weight test is cited in §4.7.1 but not shown in §4.7);
  notes explain how to read the bars. Fig 43 kept.
- **Slide 13:** the paper's Fig 45 image is replaced by a native chart drawn
  from Table 2 (equity, utilization), because the image mislabels three counties
  and hides Guilford (logged as post-conference fix #2). Quadrants split at 0.5
  and all four are named; the top three are in colour; no size encoding (totals
  are on slide 12). Notes say how to read the axes.
- **Slides 10 and 13 aligned (equity pillar):** slide 10 calls the county spread
  "the largest input to the equity pillar" (notes; slide 10 reopened,
  then re-locked); slide 13 notes explain that Mecklenburg's equity score also
  reflects its uneven within-county charging (§4.7 equity sub-metrics: J40 share
  0.40, population-weighted Gini 0.30, underserved ZIPs 0.20, zero-station share
  0.10).
- **Slide 14:** contribution 3 reads "non-redundant pillars (VIF 1.41)" (matches
  slide 11); notes say "To my knowledge, it's the first state-level application,
  and the first to use the split to design the allocation itself" (no Choi et al.
  contrast; the Guo et al. 2025 Guangzhou precedent is in the Q&A bank).
  The policy limitation reads "direction unknown (policy risk)" (§9.8–9.9);
  notes explain what a direction of bias is.
- **Slide 15 (advisor feedback on the title):** title "A Ranking to Inform
  NCDOT's Decisions, and What Comes Next" (paper §10.4: decision-support, not
  decision-making); planners line reads "for siting priorities" (site selection
  is out of scope, §2.5). Notes open with "inform, not replace", tie back to the
  community phase (slide 2), restate the big idea (county first, then
  neighborhood), and thank both faculty advisors.

---

## Deck v6 changes (whole-deck review, owner-approved 2026-10-10)

An independent whole-deck review (Drive: `01 Projects/seinforms-2026/notes/review-whole-deck-2026-10-10.md`)
checked numbers, flow, Tufte/Knaflic design, and "tell them what you told them".
The owner approved its fixes in six groups. No slides were cut; time was
recovered by trimming the notes.

1. **Tell them:** slide 3 notes end with a one-sentence preview of the answer
   (within-county inequality → two tiers; top three). Slide 15 replaces the
   NCDOT/FHWA and planner lines with three takeaways (①–③: 84.5% within →
   "county rankings for where to invest, ZIP-level targeting for whom" (§3.3);
   top 3 with scores; MAPE 4.34% with a 4 to 5% upward buffer) plus "Next".
2. **Methods wording:** slide 11 equity card names its inputs; notes define
   Justice40 (§3.4) and say the VIF means modest overlap, not none (r = +0.48).
   Slide 12: "Top-3 set held; order shifts" (§6.6); the remote-work multiplier
   is an invariance (cancels by construction), not a test. Slide 13 notes
   disclose min-max compression (§4.7; others ≤ 0.229). Slide 14 notes use
   §9.11's "No limitation… directly undermines the headline rankings."
3. **Polish:** "more than 3×" (slide 13); "12 checks, 23 of 23 sub-checks"
   (slide 14); "largest single miss" dropped (slide 6 notes, not in paper);
   Fig 44 talk legend shows 82 / 13 / 5 counties (§4.2) instead of derived
   county-months; slide 8 chart scoped to the top 10 counties, within = blue,
   between = grey; slide 10 tile scoped; EVs → BEVs where the figure is BEVs;
   IEA named aloud; "pillars that measure different things" (slide 14);
   "NEVI Priority Score" on slide 11; Orange card labelled; slide 9 no longer
   uses the ranking before it is shown.
4. **Bridges and trim:** bridge lines 3→4, 8→9, 10→11, 13→14; notes trimmed from
   2,109 to 1,938 words with every context-bearing cut restored (12:52 at
   150 wpm, about 14:10–14:50 live).
5. **Owner decisions:** slide 12 is a native bar of the Table 2 composite scores
   (top 3 blue); Fig 43 moved to backup B7. Slide 7 title "A 250-Fold Charging
   Gap Inside One County" (§6.2), 58.5% moved into the first bullet, card "The
   gap is not rural alone" (§6.2). Slide 10 title "Roughly Proportional
   Overall, with Strong County-by-County Variation" (§6.5). Phase kickers kept;
   slide 5 cards tagged "PHASE n · Qn" and the score box "→ Q5".
6. **Backups (B1–B9):** B1 native chart of within-county shares (§6.3:
   Mecklenburg 41.5%, Wake 28.1%, Guilford 7.7%, Union 0.6%) replaces the Fig 33
   image; B7 Fig 43; new B8 "Tier 2: ZIP-Level Targeting" (§4.4, §6.2); B9
   glossary in two columns at 12 pt with ARIMA, ESM, UCM, CSS/MLE, E/U/CE, EPA
   EJScreen, EPSG, HUD USPS, TIGER, GE(0) and Justice40 added. `qa-bank.md`
   updated to match.

---

## Key terms and numbers register (consistency check)

One standard phrasing per concept, where it is first explained (deck slide
numbers), and the paper source. Every slide and its notes are checked against
this as they are reviewed; a fresh-agent pass reads the whole deck against it
before the freeze.

| Concept | Standard phrasing | First explained | Also used | Paper |
|---|---|---|---|---|
| Gini coefficient | "on a scale where 0 is perfectly even and 1 is everything in one place" | slide 4 notes | slide 8 | §3.3 |
| Gini 0.805 | EV (BEV) **ownership** across counties | slide 4 | — | §1.2, Table 1 #6 |
| Gini 0.566 | "a second Gini": charging **ports** across ZIP codes (statewide, population-weighted) | slide 8 | — | §6.3, Table 1 #7 |
| Theil index | "measures how unevenly charging ports are spread relative to where people live; zero would mean every ZIP code has the same access per person"; not on a 0–1 scale; the split matters, not the size | slide 8 notes | slide 14 | §3.3, §6.3 |
| 84.5% / 15.5% | share of Theil-T inequality within / between counties, top 10 counties (0.4892 / 0.0900 of 0.5791) | slide 8 | slides 14–15 | §6.3 |
| 73% | top 10 counties' share of the statewide BEV fleet (scope) | slide 4 | slide 14 | Abstract, §2.2 |
| 16.9 | BEVs per public port (Feb 2026) vs. IEA global benchmark ≈10 | slide 4 | — | §1.2, Table 1 #5 |
| 250-fold | port-density gap, ZIP 28202 (78.64) vs. 28215 (0.31) per 10,000 residents | slide 7 (title) | slide 13 | §6.2 |
| Justice40 | "a 2021 federal goal that 40% of certain federal benefits, NEVI included, flow to disadvantaged communities"; an analytical anchor, EO 14008 rescinded Jan 2025 | slide 11 notes | slide 10, B9 | §3.4 |
| Pillar overlap | "pillars measure different things" (max VIF 1.41; modest overlap, E–CE r = +0.48), not "independent" or "non-redundant" | slide 11 | slide 14 | §4.9 |
| Robustness | "top-3 set held; order shifts" (equity weight 0.30–0.50); remote-work multiplier = invariance, not a test | slide 12 | slide 14 | §4.7.1, §6.6, §9.2 |
| NEVI Priority Score | full name on slides 5 and 11 | slide 5 | slide 11 | §4.7 |
| MAPE 4.34% | mean absolute percentage error, true four-month holdout, 400 county-months | slide 6 | slide 15 | §6.1 |
| Disadvantaged (tract) | "CEJST flags a census tract as disadvantaged when it's low-income and also burdened on at least one of eight environmental, health, or infrastructure measures" | slide 10 notes | — | §3.4 |
| Fast-charger marker | red triangle = DC fast-charging station (slide 7); Fig 42 (backup B6) uses orange triangles, noted on that slide | slide 7 | backup B6 | — |
| NEVI / NCDOT / BEV | spelled out at first use (slides 2, 2, 3) and said aloud | slides 2–3 | throughout | — |

---

## Current deck (v6): slide text and speaker notes

Generated from the v6 presenter edition (15 talk slides + backups B1–B9).
Word counts exclude the "(Cut candidate…)" stage directions; times assume
150 words per minute.

### Slide 1 — EV Pulse NC: A Data-Driven Framework for Equitable and Demand-Driven EV Charging Infrastructure Investment Prioritization in North Carolina

*Kicker:* SEINFORMS 2026 · MYRTLE BEACH, SC · OCTOBER 2026

**On-slide text**

- Wolfgang Sanyer
- MBA, Business Analytics · Fayetteville State University
- Faculty Advisors: Dr. Majed Al-Ghandour, Dr. Burcu Adivar

**Speaker notes** (56 words, ~22 s)

Good morning. I'm Wolfgang Sanyer, an MBA student in business analytics at Fayetteville State. This talk is about how North Carolina could decide where $109 million in federal EV charging money should go, and what the data says about where the real gaps are. The analysis was completed in spring 2026, using data through February 2026.

---

### Slide 2 — $109 Million. 100 Counties. No Data-Driven County Ranking.

*Kicker:* THE PROBLEM

**On-slide text**

- $109M
- NC's federal National Electric Vehicle Infrastructure (NEVI) Formula Program funding
- No county ranking
- The NC Department of Transportation (NCDOT) has a federally approved NEVI plan, but no publicly available, data-driven method for ranking counties
- Feb 2026
- NCDOT revises its NEVI plan, narrowing the corridor buildout and shifting funds toward rural and community charging
- Efficiency vs. equity
- Demand-driven allocation reinforces existing concentration; equity-driven allocation can place stations where use is too low to sustain them.

**Speaker notes** (124 words, ~50 s)

North Carolina has $109 million in National Electric Vehicle Infrastructure, or NEVI, formula funding for public charging. The two obvious approaches pull against each other. Follow demand, and you put chargers where they already are. Follow equity alone, and you can build stations nobody uses. The North Carolina Department of Transportation, NCDOT, has a federally approved NEVI plan and is building out highway corridors in rounds. In February 2026 it revised that plan, narrowing the corridor buildout and shifting funds toward rural and community charging. What it hasn't published is a data-driven way to rank counties, and that matters most for the community phase still ahead. So this is a live decision, and the question is whether there's a defensible way to make it.

---

### Slide 3 — Five Questions Drive the Work

*Kicker:* RESEARCH QUESTIONS

**On-slide text**

- Forecast Accuracy
- How accurate are SAS Model Studio's county-level battery electric vehicle (BEV) forecasts against unseen data?
- Demand-Supply Gaps
- Where are the largest demand-supply gaps?
- Sub-County Inequality
- How do ZIP-level density patterns reveal priorities county aggregation obscures?
- Commuter Flows
- How do commuting flows reshape demand once workplace needs are layered onto residential data?
- Defensible Rankings
- Can a weighted scoring equation translate these layers into defensible recommendations?

**Speaker notes** (102 words, ~41 s)

Five questions drive the work. Can the county forecasts of battery electric vehicles, or BEVs, be trusted on data they haven't seen? Where are the biggest gaps between demand and supply? What do ZIP codes show that county averages hide? How does commuting change where charging is needed? And can one weighted score turn all of that into a ranking you can defend? The rest of the talk follows these questions. The short answer: most of the charging inequality is inside counties, not between them, so the framework works in two tiers, and the top three counties are Union, Mecklenburg, and Guilford.

---

### Slide 4 — The BEV Fleet Grew 1,727% Since 2018. Ports Have Not Kept Pace.

*Kicker:* DEMAND SIGNAL

**On-slide text**

- 5,165 → 94,371
- BEVs, Sep 2018 → Jun 2025
- 53.8%
- Compound annual growth
- Gini 0.805
- County-level BEV ownership is highly concentrated; Wake alone holds more BEVs than the bottom 60 counties combined
- 16.9
- BEVs per public port (Feb 2026) vs. International Energy Agency (IEA) global benchmark ≈10
- Top 10 counties hold 73% of the statewide BEV fleet
- Data as of Feb 2026: NCDOT registrations through Oct 2025; Alternative Fuels Data Center (AFDC) stations as of Feb 2026

**Speaker notes** (104 words, ~42 s)

Start with the backdrop: demand isn't in doubt. The fleet went from 5,165 battery-electric vehicles in 2018 to 94,371 by mid-2025, a 53.8% annual growth rate. It's also very concentrated: a Gini coefficient of 0.805 across counties, on a scale where 0 is perfectly even and 1 is everything in one place. Wake County alone has more BEVs than the bottom 60 counties put together. Supply hasn't kept up. North Carolina has 16.9 BEVs per public port, against the International Energy Agency's global benchmark of about 10. The top 10 counties hold 73% of the fleet, which is why the scoring focuses on them.

---

### Slide 5 — Five Analytical Phases, One Scoring Framework

*Kicker:* METHOD

**On-slide text**

- PHASE 1 · Q1
- Forecast validation
- NCDOT registrations, Sep 2018–Oct 2025
- PHASE 2 · Q2
- Infrastructure baseline
- NREL AFDC API, Feb 2026: 1,985 stations, 6,145 connectors
- PHASE 3 · Q3
- ZIP-level inequality
- Gini + additive Theil-T decomposition
- PHASE 4 · Q4
- Workplace charging demand
- LEHD LODES 2021
- PHASE 5
- Justice40 equity overlay
- CEJST v2.0, area-weighted tract-to-ZCTA crosswalk
- NEVI Priority Score  →  Q5
- All public data · 8,600 county-month observations · SAS Model Studio forecasts (fall 2025), validated in Python (spring 2026)
- NREL: National Renewable Energy Laboratory · AFDC: Alternative Fuels Data Center · API: application programming interface · LEHD LODES: Longitudinal Employer-Household Dynamics Origin-Destination Employment Statistics · CEJST: Climate and Economic Justice Screening Tool · ZCTA: ZIP Code Tabulation Area

**Speaker notes** (79 words, ~32 s)

The work runs in five phases. Phase 1 tests the demand forecasts on data they never saw. Phase 2 rebuilds the supply side from the Department of Energy's Alternative Fuels Data Center, all charger levels, not just fast chargers. Phase 3 measures inequality at the ZIP level. Phase 4 adds workplace demand from Census commuting data. Phase 5 overlays the federal disadvantaged-community designations. Everything feeds one score, every input is public, and the whole pipeline reruns from the repository.

(Cut candidate for a 15-minute slot: move to backup.)

---

### Slide 6 — Forecasts Hold Out of Sample, and Adoption Accelerated After 2022

*Kicker:* PHASE 1 · FORECAST VALIDATION

**On-slide text**

- Mean absolute percentage error (MAPE) 4.34% on a true holdout (n = 400 county-months, Jul–Oct 2025, all 100 counties)
- 69.00% of actuals exceeded forecast (mean bias +18.22 vehicles per county-month)
- Chow test: F = 1,268.35, p < 1 × 10⁻⁶ at the Aug 2022 Inflation Reduction Act passage
- 95% interval coverage 75.50% raw → 93.75% after county bias correction: a centering problem, not a width problem

**Speaker notes** (210 words, ~84 s)

First question: can we trust the demand forecasts? The SAS models were tested on four months they never saw: all 100 counties, 400 observations. Each dot is one county in one month, forecast across, actual up, on a log scale because counties range from a handful of BEVs to tens of thousands. The colors are the model type SAS picked for each county. Dots on the dashed line are perfect forecasts. The mean absolute percentage error, or MAPE, was 4.34%, under the 5% usability bar. On this log scale the misses are hard to see, but 69% of them go the same way: actual registrations beat the forecast. The circled point is Mecklenburg in October 2025: its actual exceeded the forecast by 975 vehicles in a single month. That isn't a broken model. A Chow test, which checks whether a trend changed at a specific date, finds a strong break at the Inflation Reduction Act in August 2022. The models learned a slower world. Their 95% ranges caught only 75.5% of the actual counts, but after shifting each county's forecast up by its own average miss, 93.75%. So the ranges were the right width, just centered too low, and planners should add an upward buffer of 4 to 5 percent.

---

### Slide 7 — A 250-Fold Charging Gap Inside One County

*Kicker:* PHASE 2 · INFRASTRUCTURE GAP

**On-slide text**

- 58.5% of NC ZIP areas (499 of 853) have zero stations: 2.2 million people (21.1% of the state)
- Charlotte 28202: 78.64 ports per 10,000 residents
- Charlotte 28215, 14 miles east: 0.31 (64,713 residents, 2 ports)
- The gap is not rural alone
- ▲ DC fast-charging stations
- ■ Color: all charging ports
- ▨ No charging stations
- 28202 Uptown: 78.64
- 28215: 0.31

**Speaker notes** (101 words, ~40 s)

On the supply side, more than half of North Carolina's ZIP areas have no charger at all, covering 2.2 million people. That's not only a rural story. This map zooms into one county, Mecklenburg. The color is all charging ports per 10,000 residents, darker means more; gray hatching means no stations at all; the red triangles mark fast-charging stations. Uptown Charlotte, ZIP 28202, has 78.64 ports per 10,000 residents. Fourteen miles east, ZIP 28215 has 64,713 people and two ports. That's a 250-fold difference inside one county. Hold on to this picture, because the next slide shows it isn't an outlier.

---

### Slide 8 — 84.5% of Charging Inequality Is Within Counties

*Kicker:* PHASE 3 · THE HEADLINE FINDING

**On-slide text**

- 84.5%
- within
- 15.5%
- between
- Exact additive decomposition (generalized entropy index GE(1)); verified to 2.22 × 10⁻¹⁶; Theil-L check: 82.5% within
- ZIP-level charging Gini (statewide, population-weighted): 0.566
- County-only formulas miss most of the problem → two-tier design: county ranking + ZIP-level targeting

**Native chart:** Theil-T inequality index, top 10 counties (total = 0.5791)

**Speaker notes** (161 words, ~64 s)

This is the central result. A second Gini, this time for charging ports across ZIP codes, is 0.566: inequality is high, but that doesn't tell you where it lives. The Theil index measures how unevenly ports are spread relative to where people live; zero would mean every ZIP code has the same access per person. The Theil-T version splits exactly into a between-county part and a within-county part, with no residual. If every county had the same average access but big differences between its own ZIP codes, all the inequality would be within counties. That's essentially what we see: for the top 10 counties, 84.5% of the inequality is within counties. The Theil-L version gives 82.5%, so it isn't an artifact of the index. Mecklenburg alone contributes 41.5% of it. Most state NEVI formulas allocate by county, so they miss most of the problem. That is why the framework has two tiers: rank the counties, then target ZIP codes inside them.

---

### Slide 9 — Commuters Shift Demand Toward Employment Centers

*Kicker:* PHASE 4 · WORKPLACE DEMAND

**On-slide text**

- U.S. Census commuting data (Longitudinal Employer-Household Dynamics Origin-Destination Employment Statistics, LEHD LODES, 2021): 4,198,163 workers → 859,260 adjusted commuters after income and remote-work filters
- Union sends more commuters out than it takes in: a bedroom community of Charlotte
- Feeds the cost-effectiveness pillar: Mecklenburg scores highest (0.801)

**Native chart:** Net daily commuters, selected counties (in minus out)

**Speaker notes** (122 words, ~49 s)

That's where the inequality is. Next, where the demand is during the day. Registration data tells you where EVs sleep, not where they sit during the workday. For the workday I used Census commuting data, LODES, for 2021: 4,198,163 workers, filtered to EV-affordable incomes and adjusted for remote work, leaving 859,260 commuters. The chart shows net daily commuters. Mecklenburg takes in 194,361 more workers a day than it sends out, and Wake and Durham are job centers too. Union is the opposite: 36,113 more people leave each day than arrive. It's a bedroom community: people live there and drive to Charlotte for work. That daytime demand feeds the cost-effectiveness part of the score I'll show in a moment, where Mecklenburg scores highest.

(Cut candidate for a 15-minute slot: move to backup.)

---

### Slide 10 — Roughly Proportional Overall, with Strong County-by-County Variation

*Kicker:* PHASE 5 · JUSTICE40 OVERLAY

**On-slide text**

- 24.5%
- of stations in the top 10 counties sit in disadvantaged tracts (296 of 1,210)
- 18.5%
- of residents in the top 10 counties live in those tracts
- Roughly proportional overall
- Statewide: 43.0% of NC census tracts designated disadvantaged (934 of 2,170; CEJST v2.0)
- Removing CEJST's climate category: 7 of 10 study counties unchanged
- Residents in disadvantaged tracts, by county
- Top-10 average 18.5%
- Guilford
- 29.2%
- New Hanover
- 28.8%
- Durham
- 26.6%
- Mecklenburg
- 23.7%
- Wake
- 8.1%
- Orange
- 4.9%
- 0%
- 10%
- 20%
- 30%
- CEJST v2.0 as of Jan 21, 2025; tool removed Jan 22, 2025 after Executive Order (EO) 14008 was rescinded; data from the Environmental Data & Governance Initiative (EDGI) / Public Environmental Data Partners (PEDP) archive

**Speaker notes** (197 words, ~79 s)

Phase 5 brings in equity. The federal Climate and Economic Justice Screening Tool, CEJST, flags a census tract as disadvantaged when it's low-income and also burdened on at least one of eight environmental, health, or infrastructure measures. In the top 10 counties, 18.5% of residents live in those tracts, and 24.5% of stations sit in them. Those are the two numbers on the left: in aggregate the siting is roughly proportional. The story is in the variation, on the right. Each dot is a county's share of residents in disadvantaged tracts; the dashed line is the 18.5% average. Guilford is at 29.2%; Wake is at only 8.1%, and Orange at 4.9%. That share is the largest input to the equity pillar; the others are how unevenly chargers are spread inside each county and how many ZIP codes are underserved. And as the Theil result showed, proportional in total doesn't mean well served inside each county: Mecklenburg has plenty of chargers, but they're concentrated in Uptown. One caveat: the federal screening tool was taken down in January 2025. I use the archived version 2.0 data, and removing its most contested category, climate, leaves 7 of 10 counties unchanged.

(Cut candidate: trim first at rehearsal if the talk runs long.)

---

### Slide 11 — Three Pillars, One Score

*Kicker:* THE FRAMEWORK

**On-slide text**

- NEVI Priority Score = 0.40 × Equity + 0.35 × Utilization + 0.25 × Cost-Effectiveness
- 0.40
- Equity
- Disadvantaged residents, within-county charging Gini, underserved ZIPs; anchored on the Justice40 40% target (EO 14008, rescinded Jan 2025)
- 0.35
- Utilization
- BEVs per port; demand data validated out of sample (strongest data)
- 0.25
- Cost-Effectiveness
- Workplace demand (most uncertain input)
- Weights follow data confidence. Each pillar is a weighted composite of sub-metrics, min-max normalized to 0–1.
- Pillars measure different things: max variance inflation factor (VIF) 1.41 (concern threshold 5.0)

**Speaker notes** (152 words, ~61 s)

Those three layers, demand, workplace, and equity, now go into one score with three pillars. Each pillar is built from several measures, and every measure is min-max normalized: rescaled so the lowest county gets 0 and the highest gets 1, so measures in different units can be added together. The weights follow data confidence. Equity gets 0.40. It's anchored on Justice40, a 2021 federal goal that 40% of certain federal benefits, NEVI included, flow to disadvantaged communities. I treat that as an analytical anchor, not a legal requirement, since the executive order was rescinded in January 2025. Utilization, which is BEVs per charging port, gets 0.35 because its demand data passed the out-of-sample test. Cost-effectiveness gets 0.25 because workplace demand is the least certain input. The highest variance inflation factor is 1.41, well under the usual concern threshold of 5, so the pillars overlap only modestly and each adds its own information.

---

### Slide 12 — Top 3: Union, Mecklenburg, Guilford

*Kicker:* THE RANKINGS

**On-slide text**

- 0.561
- #1 Union
- 0.548
- #2 Mecklenburg
- 0.465
- #3 Guilford
- Top-3 set held; order shifts:
- Equity weight 0.30–0.50 (five scenarios): Mecklenburg gains and Union falls as the equity weight rises
- Remote-work multiplier 0.75 / 0.85 / 0.95: cancels in min-max normalization, so the rankings are identical by construction
- Wake ranks 5th despite the most BEVs (equity 0.322; 8.1% of residents in disadvantaged tracts)

**Native chart:** NEVI Priority Score, top 10 counties (Table 2)

**Speaker notes** (109 words, ~44 s)

Here's the result. Union, Mecklenburg, and Guilford come out on top. Each bar is a county's total score, and the top three are in blue. The same three stay on top as the equity weight moves from 0.30 to 0.50, though the order shifts: Mecklenburg gains as equity counts more. The remote-work assumption can't change the ranking at all, because a uniform multiplier cancels in the normalization, so I treat it as an invariance, not a test. And this is one factor at a time, not a full search of all weight combinations. Notice Wake: the most BEVs in the state, but fifth, because its equity burden is low.

---

### Slide 13 — Three County Archetypes

*Kicker:* WHAT THE RANKING MEANS

**On-slide text**

- Union: utilization-driven
- 101.5 BEVs per port, more than 3× the next county → more stations
- Mecklenburg & Guilford: equity-driven
- Equity 0.810 and 0.855 → better-targeted stations in underserved ZIPs
- Orange: low across all pillars
- Lowest overall score (0.077) → no priority deployment now
- Empty quadrant: no county is high on both equity and utilization
- Utilization-driven
- High on both: none
- Low across pillars
- Equity-driven
- 0.0
- 0.0
- 0.5
- 0.5
- 1.0
- 1.0
- Equity pillar score (0–1) →
- Utilization pillar score (0–1) →
- Union
- Mecklenburg
- Guilford
- New Hanover
- Wake
- Durham
- Forsyth
- Cabarrus
- Buncombe
- Orange

**Speaker notes** (166 words, ~66 s)

The ranking says where, but not why. Plotting equity against utilization gives three archetypes. Equity runs left to right, utilization bottom to top, and the top three counties are in color. Union is utilization-driven: 101.5 BEVs per port, more than three times the next county. It needs more stations. One caveat: Union is so far ahead that min-max scaling puts it at 1.0 and squeezes the other nine counties to 0.229 or below on utilization. The gap is real, not a data artifact, but the scoring is sensitive to an extreme value like this. Mecklenburg and Guilford are equity-driven. Mecklenburg's equity score is high not only because of its disadvantaged residents, but because its chargers are so unevenly spread across its ZIP codes, the Uptown gap. They need better-targeted stations. Orange is low on everything and isn't a priority now. And the top-right corner is empty: no county is high on both equity and utilization, so every county is a trade-off, which the framework makes visible.

---

### Slide 14 — Contributions and Limitations

*Kicker:* WHAT IT ADDS

**On-slide text**

- Contributions
- Additive Theil-T decomposition of EV charging inequality, used as a design input to allocation
- Area-weighted CEJST–AFDC crosswalk at ZIP resolution (12 checks, 23 of 23 sub-checks passed)
- Three-pillar NEVI score with pillars that measure different things (VIF 1.41) and a robust top 3
- Limitations, each with a direction of bias
- Top-10 scope (73% of fleet): bounded
- LODES 2021 vintage: cancels in normalization
- Static BEV counts: understates growth (conservative)
- CEJST v2.0 lock, NEVI rule changes: direction unknown (policy risk)

**Speaker notes** (130 words, ~52 s)

So what does this add, and where is it weak? Three contributions. First, using the Theil decomposition as a design input, not just a summary number. To my knowledge, it's the first state-level application, and the first to use the split to design the allocation itself. Second, a validated crosswalk that brings the federal equity designations down to ZIP level. Third, a score whose pillars measure different things and whose top three holds across the equity-weight sweep. Each limitation comes with its direction of bias. The scope covers 73% of the fleet. The 2021 commuting data cancels out in normalization. Static counts understate growth, which makes the scores conservative. And federal policy changes are a risk whose direction we can't know yet. None of them directly undermines the headline rankings.

---

### Slide 15 — A Ranking to Inform NCDOT's Decisions, and What Comes Next

*Kicker:* IMPLICATIONS AND NEXT STEPS

**On-slide text**

- ①  84.5% of charging inequality is within counties: county rankings for where to invest, ZIP-level targeting for whom
- ②  Top 3: Union 0.561 · Mecklenburg 0.548 · Guilford 0.465
- ③  Forecasts hold out of sample (MAPE 4.34%) but run low: plan an upward buffer of 4 to 5%
- Next: all 100 counties · validate against NCDOT's actual NEVI deployments · confidence intervals on composite scores
- Thank you
- wolfgang.sanyer@gmail.com
- linkedin.com/in/wolfgangsanyer
- github.com/wolfieman/ev-pulse-nc
- sanyer.org/research-lab

**Speaker notes** (115 words, ~46 s)

This ranking is meant to inform NCDOT's decisions, not replace them. Right-of-way, utilities, and politics all matter and aren't in the model. What it gives is an analytical floor: a ranking an auditor can trace, and ZIP-level targets a planner can use. And NCDOT's community phase, which is still ahead, is exactly where a county ranking can help. Next: all 100 counties, a check against NCDOT's actual deployments, and confidence intervals on the scores. If you remember one thing: most of the charging gap is inside counties, so allocation has to work county first, then neighborhood. I'd like to thank my faculty advisors, Dr. Al-Ghandour and Dr. Adivar. Thank you, I'm happy to take questions.

---

### B1 — Theil-T Decomposition

**On-slide text**

- GE(1) / Theil-T is additively decomposable: T = T_between + T_within, with no residual (Bourguignon 1979; Shorrocks 1980)
- Top 10 counties: 0.5791 = 0.0900 (15.5%) + 0.4892 (84.5%)
- Theil-L (GE(0)) robustness: 82.5% within
- Within-county contribution: Mecklenburg 41.5%, Wake 28.1%, Guilford 7.7%, Union 0.6%
- Theil is a diagnostic for the architecture (why Tier 2 exists), not an input to either tier's score

**Native chart:** Share of within-county inequality (the four counties reported in §6.3)

---

### B2 — Crosswalk Validation

**On-slide text**

- CEJST v2.0 (2010 tracts) → 2020 ZCTAs, area-weighted in NC State Plane (EPSG:32119), the EPA EJScreen / HUD USPS approach
- 12 checks in 3 tiers, 23 of 23 sub-checks passed; per-ZCTA area conservation within 1%
- Slivers < 100 m² dropped; border-state tracts (VA, SC, TN, GA) included; 25 zero-population tracts excluded
- Known limit: uniform within-tract population (weaker in large rural tracts)

---

### B3 — Full NEVI Scores (Table 2)

**On-slide text**

- Rank | County | NEVI | Equity | Utilization | Cost-Eff.
- 1 | Union | 0.561 | 0.319 | 1.000 | 0.333
- 2 | Mecklenburg | 0.548 | 0.810 | 0.067 | 0.801
- 3 | Guilford | 0.465 | 0.855 | 0.103 | 0.347
- 4 | New Hanover | 0.341 | 0.607 | 0.071 | 0.293
- 5 | Wake | 0.316 | 0.322 | 0.130 | 0.568
- 6 | Durham | 0.313 | 0.469 | 0.033 | 0.454
- 7 | Forsyth | 0.285 | 0.283 | 0.156 | 0.467
- 8 | Cabarrus | 0.199 | 0.228 | 0.229 | 0.111
- 9 | Buncombe | 0.197 | 0.470 | 0.000 | 0.034
- 10 | Orange | 0.077 | 0.059 | 0.101 | 0.071
- Equity weight 0.30–0.50 sweep: top 3 unchanged; Mecklenburg gains and Union falls as the equity weight rises; Orange stays 10th.

---

### B4 — Data Sources and Diagnostics

**On-slide text**

- Source | Content | Window
- NCDOT | Monthly county BEV registrations | Sep 2018 – Oct 2025
- NREL AFDC API | Station inventory, all levels | Feb 2026 pull
- U.S. Census ACS + TIGER | Income, tenure, population; boundaries | ACS 2022 five-year; TIGER 2020
- LEHD LODES | Block-level commuter flows | 2021
- CEJST v2.0 | Disadvantaged tract designations | Dec 2024 release (EDGI / PEDP archive)
- CSS vs. MLE estimator: forecast difference < 0.1%
- NCDOT counting change (May 2025): ~0.4% of totals, works against the underprediction
- Pillar correlations: E–U −0.26 · E–CE +0.48 · U–CE −0.03

---

### B5 — Workplace Demand by County (Paper Fig 36)

**On-slide text**

- Blue: registered BEVs in the county (residential demand)
- Orange: residential BEVs plus adjusted commuters who work in the county
- The orange bar adds commuters to EVs: it shows where daytime demand concentrates, not an EV count. Port need uses a 30% charging adoption rate and a 15:1 port ratio (§6.4).

---

### B6 — Stations on Justice40 Tracts (Paper Fig 42)

**On-slide text**

- Pink: disadvantaged census tracts (CEJST v2.0)
- Blue dots: Level 2 (L2) charging stations
- Orange triangles: DC fast-charging (DCFC) stations
- 1,210 stations in the 10 study counties; 24.5% in disadvantaged tracts (§6.5)

---

### B7 — Pillar Contributions to the NEVI Score (Paper Fig 43)

**On-slide text**

- Blue: equity (weight 0.40)
- Orange: utilization (weight 0.35)
- Green: cost-effectiveness (weight 0.25)
- Union's bar is dominated by utilization; Mecklenburg's and Guilford's by equity (§6.7)

---

### B8 — Tier 2: ZIP-Level Targeting

**On-slide text**

- What Tier 2 uses: population, disadvantaged-community status, and station density, ranking ZIPs within each county (§4.4)
- Its output: the top 20 underserved ZIPs hold 732,892 residents served by 58 ports; 15 have zero DC fast chargers (§6.2)
- Mecklenburg and Guilford each contribute 5 ZIPs to the top 20: the state's two most infrastructure-rich counties also hold some of its worst gaps (§6.2)
- Theil justifies Tier 2 but is not an input to either tier's score (§4.4)

---

### B9 — Glossary of Abbreviations

**On-slide text**

- Abbreviation | Meaning
- ACS | American Community Survey
- AFDC | Alternative Fuels Data Center
- API | Application programming interface
- ARIMA | Autoregressive integrated moving average
- BEV | Battery electric vehicle
- CEJST | Climate and Economic Justice Screening Tool
- CSS / MLE | Conditional sum of squares / maximum likelihood estimation
- DCFC | DC fast charging
- E / U / CE | Equity / Utilization / Cost-Effectiveness pillars
- EDGI | Environmental Data & Governance Initiative
- EO | Executive Order
- EPA EJScreen | U.S. Environmental Protection Agency environmental justice screening tool
- EPSG | Standard ID code for a map projection (here, NC State Plane)
- ESM | Exponential smoothing model
- FHWA | Federal Highway Administration
- GE(0) / GE(1) | Generalized entropy index, alpha = 0 (Theil-L) / alpha = 1 (Theil-T)
- Abbreviation | Meaning
- HUD USPS | Dept. of Housing and Urban Development / U.S. Postal Service ZIP crosswalk
- IEA | International Energy Agency
- IRA | Inflation Reduction Act
- Justice40 | Federal goal (EO 14008, 2021): 40% of certain federal benefits to disadvantaged communities; rescinded Jan 2025
- L2 | Level 2 charging
- LEHD LODES | Longitudinal Employer-Household Dynamics Origin-Destination Employment Statistics
- MAPE | Mean absolute percentage error
- NCDOT | North Carolina Department of Transportation
- NEVI | National Electric Vehicle Infrastructure (Formula Program)
- NREL | National Renewable Energy Laboratory
- PEDP | Public Environmental Data Partners
- TIGER | Census Topologically Integrated Geographic Encoding and Referencing (boundaries)
- UCM | Unobserved components model
- VIF | Variance inflation factor
- ZCTA | ZIP Code Tabulation Area

---

## Figure inventory

| Slide | Visual | Source |
|---|---|---|
| 6 | Talk version of Fig 44 (`assets/fig-44-validation-scatter-talk.png`, from `fig44_talk.py`) | §6.1 data, legend counts §4.2 |
| 7 | Fig 24 (`fig-24-heatmap-mecklenburg.png`) with ZIP callouts (`fig24_labels.py`) | §6.2 |
| 8 | Native stacked bar: Theil-T between / within, top 10 counties | §6.3 |
| 9 | Native diverging bar: net daily commuters, four counties | §6.4 |
| 10 | Native tiles and dot plot: residents in disadvantaged tracts | §6.5, §6.6 |
| 12 | Native bar: NEVI Priority Score, Table 2 | §6.6 |
| 13 | Native equity × utilization chart from Table 2 (replaces Fig 45) | §6.6, §7.3 |
| B1 | Native bar: share of within-county inequality, four counties | §6.3 |
| B5 / B6 / B7 | Paper Figs 36 / 42 / 43, as-is | §6.4 / §6.5 / §6.7 |
