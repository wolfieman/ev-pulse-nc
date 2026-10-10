# SEINFORMS 2026: Q&A Bank

Answers rest on the SEINFORMS paper (section numbers below). Items marked
*briefing* come from the current-status briefing in Drive
(`01 Projects/seinforms-2026/qa-briefing-current-status-2026-10-09.md`) and are
context, not results of the study. Deck slide numbers count the title slide
as 1.

---

## Slide 6: forecast validation (cheat sheet)

**Reading the chart**

- **Log-log scale.** Both axes are logarithmic: each gridline is ×10 (10, 100,
  1,000, 10,000). Counties range from about 4 BEVs (Hyde) to about 28,000
  (Wake); on a normal scale most counties would be squashed into a corner. On a
  log scale, equal distances mean equal percentages.
- **Each dot** is one county in one month (100 counties × 4 holdout months =
  400 dots).
- **Dashed diagonal** = actual equals forecast (perfect prediction). It sits at
  45° only because both axes use the same scale; it is a reference, not a
  result.
- **Vertical distance from the line** = percentage error. Above the line:
  actual higher than forecast (under-forecast). Below: lower.
- **Position along the diagonal** = county size: small rural counties lower
  left, large counties upper right.
- **Colors** = the model type SAS chose for that county.
- **Circled point** = Mecklenburg, October 2025: the largest single miss, 975
  vehicles above forecast (§4.2, §6.1). It looks small because, on a log
  scale, 975 is a small percentage of Mecklenburg's count; it is above the
  line too.

**The four numbers**

| Number | Meaning | Why it matters |
|---|---|---|
| MAPE 4.34% (true holdout, n = 400, Jul–Oct 2025) | Average absolute percentage miss; the four months were not used to build the models | Under the 5% usability bar (§4.2, §6.1) |
| 69.00% of actuals exceeded forecast; mean bias +18.22 | Actual was higher than forecast in 69% of cases; on average 18.22 vehicles per county-month above | Random errors would split about 50/50; this is systematic underprediction |
| Chow test F = 1,268.35, p < 1 × 10⁻⁶ at Aug 2022 (IRA) | Tests whether the trend changed at that date: one trend line vs. separate lines before and after | Adoption clearly accelerated after the IRA; models trained on the slower pattern run low (§4.9) |
| 95% interval coverage 75.50% → 93.75% | Only 75.50% of actuals fell inside the 95% ranges; misses were 18.0% above vs. 6.5% below (about 3:1); after shifting each county's forecast by its own bias, coverage is 93.75% | The ranges had the right width but sat too low: re-center, don't widen. Hence the 4–5% planning buffer (§4.9) |

**Why three model types (ESM, ARIMA, UCM)? Which one was chosen?**

> "There's no single winner. SAS Model Studio picked the best model per county
> (exponential smoothing for 82 counties, ARIMA for 13, unobserved components
> for 5), and all three types show the same small, consistent
> underprediction, so the conclusion doesn't depend on the model choice."

- n in the legend = county-months: 328 = 82 × 4, 52 = 13 × 4, 20 = 5 × 4.
- In-sample fit of the selected models: weighted MAPE 2.73% (§4.2).
- ARIMA estimator choice (SAS CSS vs. Python MLE) changes forecasts by less
  than 0.1% (§4.9).
- The paper does not state SAS's selection criterion: say "SAS Model Studio's
  automatic selection"; do not name a criterion.

**Is adoption still accelerating?** (*briefing*)

> "Through our data window, yes: the Chow test shows the post-2022 break.
> Federal purchase credits ended in September 2025, effectively a second policy
> break; registrations paused for a few months and have since resumed growing.
> That's why the paper recommends an upward planning buffer and re-running the
> forecasts."

---

## Slide 8: Theil decomposition (cheat sheet)

- **What Theil measures:** how unevenly charging ports are spread relative to
  where people live. 0 = every ZIP code has the same access per person; higher
  = more uneven.
- **It does not run from 0 to 1.** Unlike the Gini (capped at 1), the Theil
  index has no fixed upper limit: its maximum depends on how many units are
  compared (it is logarithmic). So 0.5791 is not a percentage or a score "out
  of 1"; the meaningful result is the split.
- **How 0.0900 becomes 15.5%:** each part divided by the total (§6.3):
  0.0900 ÷ 0.5791 = 15.5% between; 0.4892 ÷ 0.5791 = 84.5% within. The parts
  sum to the whole (additive decomposition, no residual).
- **"0.0900 + 0.4892 = 0.5792, not 0.5791":** rounding; each part is shown to
  four decimals. The paper verifies the exact sum to machine precision
  (2.22 × 10⁻¹⁶).
- **Robustness:** Theil-L (GE(0)) gives 82.5% within; the pattern does not
  depend on the index (§6.3).
- **Theil is a design input, not a score input:** the 84.5% finding justifies
  the ZIP-level tier; it does not enter either tier's score (§4.4).
- **Who drives it:** Mecklenburg 41.5% and Wake 28.1% of within-county
  inequality, together about 70% (§6.3).

- **Gini vs. Theil (one-liner):** "The Gini tells us how uneven charging
  access is; the Theil decomposition tells us where that unevenness sits, and
  84.5% of it is inside counties."

| | Gini | Theil |
|---|---|---|
| Measures | how much inequality, for one chosen set of units | how much, and where it sits |
| Scale | 0 to 1 | 0 upward, no fixed maximum (logarithmic) |
| Splits into between and within? | no | yes, exactly |
| Inside a ZIP? | no (ZIP is the smallest unit) | no |
| In the deck | 0.805 EVs across counties (slide 4); 0.566 ports across ZIPs statewide (slide 8); 0.623 Mecklenburg's ZIPs (equity pillar) | 0.5791 total across the top 10 counties' ZIPs; 84.5% within (slide 8) |

- **Scope:** the Theil decomposition covers the top 10 counties' ZIPs (134
  urban ZIPs); the 0.566 Gini is statewide. Within-county contributions:
  Mecklenburg 41.5%, Wake 28.1%, Guilford 7.7% (smaller county), Union 0.6%
  (evenly under-served) (§6.3).

---

## Slide 10: equity (cheat sheet)

- **Left numbers:** 18.5% of residents in the 10 counties live in disadvantaged
  tracts; 24.5% of the 1,210 stations sit in those tracts. Proportional siting
  would put about 18.5% there, so in total disadvantaged areas are not short of
  stations (station counts, not ports or speed) (§6.5).
- **Right chart:** each dot is a county's share of residents in disadvantaged
  tracts (population-weighted, §6.5; Orange §6.6). This is the equity pillar's
  largest input (§4.7). Wake is low (8.1%) because CEJST requires low-income
  tracts and Wake's are relatively high-income (context, not a paper finding);
  that is why Wake ranks 5th despite the most EVs (§6.6).
- **"Is Guilford the most disadvantaged county?"**

  > "Guilford has the highest share, 29.2%, and the highest equity score in the
  > cohort (0.855). Mecklenburg has more people in disadvantaged tracts in
  > absolute terms because it's much larger."

  Avoid "most disadvantaged": CEJST flags tracts, not counties or people.
- **Mecklenburg has lots of chargers, so why 23.7%?** Supply (chargers in the
  county) and need (residents in disadvantaged tracts) are different measures.
  Its chargers concentrate in Uptown (slide 7), so it needs better-targeted
  stations (§7.3), not just more.
- **Link to Theil:** slide 8 (84.5% within counties) justifies Tier 2 ZIP
  targeting; slide 10 (need varies between counties) feeds Tier 1's equity
  pillar.

---

## Slide 11: the score (cheat sheet)

- **Min-max normalization:** each measure rescaled so the lowest county is 0
  and the highest is 1, so measures in different units can be added (§4.7).
  - **Weakness (expect from the chair):** sensitive to extremes. Union's 101.5
    BEVs per port (over three times the next county) becomes 1.0 and
    compresses the other nine (§4.7). Bounds come from the sample, so adding a
    county rescales every score.
  - **Answer:** "The paper discloses that compression; the top three hold
    across the equity-weight sweep and the remote-work multiplier (§4.7.1). A rank-stability check under z-score or
    rank normalization is the natural next test."
- **VIF (variance inflation factor):** predict each pillar from the other two;
  VIF = 1 / (1 − R²). 1 = no overlap; under 5 = fine. Ours: Equity 1.41,
  Cost-Effectiveness 1.32, Utilization 1.08 (§4.9). It guards against double
  counting, so the stated weights are the real emphasis.
  - **Pushback 1:** only 10 counties, so it's a rough check, not proof.
  - **Pushback 2:** Equity and Cost-Effectiveness correlate +0.48 (§4.9);
    hence "measure different things", not "independent". The paper's reason:
    disadvantaged counties also tend to have workforce demand.
  - **Pushback 3:** stated vs. effective weights (Becker et al. 2017,
    *briefing*). Answer: rankings are stable when the weights move (next
    slide).
- **"Why 0.40 for equity?"**

  > "The weights follow data confidence and the Justice40 40% target as an
  > analytical anchor. And the top three hold for equity weights anywhere from
  > 0.30 to 0.50 (§4.7.1), so the result doesn't depend on that exact
  > choice."

---

## Slide 12: rankings (cheat sheet)

- **Reading the chart:** each bar is a county's total score; segments are
  pillar contributions (equity blue, utilization orange, cost-effectiveness
  green), Table 2 / Fig 43.
- **Robustness shown on the slide:** the equity-weight sweep 0.30–0.50 (five
  scenarios) and the remote-work multiplier (0.75 / 0.85 / 0.95, which cancels
  in min-max normalization) (§4.7.1, §6.6, §9.2). One-factor-at-a-time, not a
  full design over the weight simplex (§4.7.1, future work §11.3).
- **"The paper says triply robust; what's the third test?"** The paper cites
  cost-effectiveness sub-weight extremes (§4.7.1), but the detail isn't shown
  in §4.7, so the talk presents the two documented tests. If asked: "The paper
  also reports a cost-effectiveness sub-weight check; the two I show are the
  ones with full results in the paper."
- **"Has anyone built a county-level weighted NEVI index like this?"**
  (*briefing*): "Not that we found: published NEVI work is mostly qualitative
  state-plan comparisons, tract- or city-level equity metrics, or optimization
  models."

---

## Slide 13: archetypes (cheat sheet)

- **"Why is Mecklenburg above New Hanover and Durham on equity, when fewer of
  its residents live in disadvantaged tracts?"** The equity pillar has four
  inputs, each min-max scaled (§4.7): share of residents in disadvantaged
  tracts (0.40 of the pillar), within-county charging Gini (0.30), number of
  underserved ZIPs (0.20), share of zero-station ZIPs (0.10; the same for all
  10 counties). Mecklenburg has the cohort's highest within-county Gini (0.623)
  and 5 of the top-20 underserved ZIPs (§6.2–6.3); Durham has the lowest Gini
  (0.408).

  > "Equity combines how many residents live in disadvantaged tracts with how
  > unevenly chargers are spread inside the county. Mecklenburg's chargers are
  > concentrated in Uptown, so it scores high even though its disadvantaged
  > share is lower."

- **Chart:** native redraw of Fig 45 from Table 2 (equity, utilization);
  quadrants split at 0.5. The paper's own Fig 45 mislabels three counties
  (post-conference fix #2): use the slide, not the paper figure, if asked.

---

## Slide 15: closing (cheat sheet)

- **"Decision support, not decision-making"** (paper §10.4): the ranking informs
  NCDOT's allocation; it doesn't make it. The model leaves out right-of-way,
  utility coordination, supply-chain timing and politics (§9.10, §10.4).
- **Right-of-way:** the legal right to use a piece of land (the strip along a
  road, or a property) to build there. A site can look ideal in the data but
  be unbuildable without permission. **Utilities** = the power hookup: whether
  the local grid can supply a fast charger at that spot.
- **"Community phase"** (*briefing*): NCDOT builds highway-corridor fast
  charging first (Phase 1, Rounds 1 and 2; Round 2 awarded Sept 2026, 14
  sites). On Jan 27, 2026 it cut the corridor buildout from 41 to 16 locations
  to free money for local and rural (community) charging later; that phase
  has not been solicited yet. That later phase is where a county ranking helps
  most. "Community phase" is shorthand; the paper itself predates these facts.

---

## Settled answers from the slide review

**"Top 10 counties hold 73%": I get 72%.**

> "73% is the scoring cohort's share as reported throughout the paper; the
> concentration analysis in the Gini section cites 72%. Either way, about
> three-quarters of the state's EVs are in those ten counties."

Do not defend it as "rounding up".

**Why LODES 2021 when newer releases exist?**

> "We used the 2021 vintage; newer releases exist. The vintage changes absolute
> demand, but not the rankings: the remote-work adjustment cancels out in the
> normalization, and the rankings are identical across 0.75, 0.85 and 0.95
> (§9.2)."

Do not say "the most recent release".

**Is this the first Theil decomposition of EV charging?** (*briefing*)

> "To my knowledge, the first application of the between/within Theil-T
> decomposition to a state-level EV-charging allocation problem, where the
> decomposition sets the design of a two-tier framework. A city-level
> descriptive precedent exists: Guo et al. (2025), Guangzhou, also
> within-dominant."

**Didn't NCDOT already move to Phase 2?** (*briefing*)

> "The September 2026 awards were Round 2 of Phase 1, highway corridors. The
> community and rural phase hasn't been solicited yet, and that's where a
> county ranking matters most."

**Isn't "16.9 BEVs per public port" counting private ports too?** (*briefing*)

> "The 6,145-port count from the February 2026 inventory covers all access
> types; public-only ports are fewer. The ratio is a demand-pressure proxy
> either way (§9.6)."

**The IEA benchmark is now about 11, and the US is about 33.** (*briefing*)

> "We used the benchmark as published at the time. The point stands: North
> Carolina is above the global benchmark."
