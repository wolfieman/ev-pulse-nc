# Prior Work — Theil Index in EV Charging Infrastructure Literature

**Created:** 2026-05-12
**Context:** Pre-submission literature check on the novelty claim that the EV Pulse NC project's Theil-T decomposition is the first applied to EV charging infrastructure. Findings drive the lit review and contribution framing in the final BIDA 670 paper and the SEINFORMS 2026 conference submission.

---

## TL;DR — Verdict

The **bare claim** "first application of the Theil index to EV charging infrastructure" is **false**. Choi, Xu & Jiao (2025) already applied the Theil index to EV charger accessibility in Austin, TX.

The **narrower claim** — "first Theil-T (GE(1)) **between-county / within-county decomposition** applied to EV charging infrastructure inequality" — remains defensible. Choi et al. used the Theil index as a **scalar** inequality measure alongside Lorenz, Gini, Palma, etc., not as a decomposition.

**Locked framing (use this in the paper, email, and any future submissions):**

> "While prior EV charging equity studies have used the Theil index as a scalar inequality measure (Choi et al. 2025), this study is, to the authors' knowledge, the first to exploit the decomposability of Theil's T to separate within-county and between-county components of EV charging infrastructure inequality, using those components to motivate a two-tier prioritization framework."

---

## The Disqualifier — Choi et al. (2025)

**Full citation:**
Choi, S. J., Xu, Y., & Jiao, J. (2025). "Utility or equity? Analyzing public electric vehicle charger allocations in Austin, Texas." *Transportation Research Part D*, Elsevier.

- **Published:** September/November 2025
- **SSRN preprint:** abstract_id=4992707 (posted 2024)
- **DOI/URL:** https://www.sciencedirect.com/science/article/abs/pii/S1361920925004043
- **SSRN URL:** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4992707

**What they do:**
- Apply an inequality "toolkit" to EV charger accessibility in Austin, TX
- Tools used: **Lorenz Curve, Gini Coefficient, Theil Index, Segplot, Palma Ratio, concentration curve**
- The Theil index is used as a **scalar metric** alongside the others — not decomposed
- Comparison framing: accessibility inequality vs. accessibility poverty methods

**Crucially, what they do NOT do:**
- No between-group / within-group Theil decomposition
- No statements of the form "X% of inequality is within [geography] and Y% is between"
- No integration of Theil decomposition into an allocation framework

---

## How EV Pulse NC's Approach Differs

| Dimension | Choi, Xu & Jiao (2025) | EV Pulse NC (this study) |
|-----------|------------------------|---------------------------|
| **Geography** | Austin, TX (single city) | North Carolina (10-county cohort, 130 ZIPs) |
| **Theil usage** | Scalar inequality metric | **Exact additive decomposition** into between- and within-county components |
| **Decomposition result** | Not computed | 84.5% within-county, 15.5% between-county |
| **Methodological role** | One of several toolkit metrics | Structural diagnosis driving framework architecture |
| **Framework integration** | Comparison of inequality theories | Motivates the two-tier NEVI Priority Score + ZIP-level equity targeting |
| **Policy hook** | Equity vs. utility tradeoff in allocations | NEVI Formula Program county prioritization |

---

## What the Two-Tier Architecture Actually Is

Important nuance to keep clear in the paper: **the Theil decomposition does not drive the two-tier mechanism — it justifies it.**

- **Gini** → magnitude diagnostic. "How bad is statewide inequality?" (0.805 — extreme)
- **Theil-T decomposition** → structural diagnostic. "Where is the inequality concentrated?" (84.5% within counties)
- **NEVI Priority Score** → Tier 1 selection mechanism. County ranking using utilization + equity + cost-effectiveness pillars.
- **ZIP-level equity score** → Tier 2 targeting mechanism. Uses population, DAC status, and station density (NOT Theil) to identify underserved ZCTAs within priority counties.

The Theil decomposition's role is to **prove that Tier 2 is necessary**. Without the 84.5% within-county finding, a county-only allocation would appear sufficient.

---

## Other Inequality Measures in EV Charging Literature (for Lit Review)

Representative prior work for context:

1. **Gini coefficient (most common)** — Hong Kong (Gini 0.751 overall, 0.791-0.893 disadvantaged subgroups); California DC fast charging; Shanghai; Abu Dhabi
2. **Lorenz curves** — California, multiple US studies
3. **Theil index (scalar)** — Choi, Xu & Jiao (2025), Austin TX (the disqualifier)
4. **Custom metrics: PCS-LIN, Racial Gap Index** — Roy & Law (*Nature Communications* 2024), designed for race-aware accessibility. URL: https://www.nature.com/articles/s41467-024-49481-w
5. **Palma ratio, concentration curves, FGT poverty score** — used in Choi et al. (2025) and adjacent transit equity work

**Systematic review:** Equity Considerations in Public EV Charging (*MDPI* 2025): https://www.mdpi.com/2032-6653/16/10/553

---

## Adjacent Theil Applications (Transportation Infrastructure)

Closest prior applications of Theil to **non-EV** transportation infrastructure:

- **Public transit equity (Brazil)** — Theil alongside Gini/Palma for service distribution. *npj Sustainable Mobility and Transport* 2025: https://www.nature.com/articles/s44333-025-00039-3
- **Highway-railway accessibility (Shandong, China)** — Gini + Theil for regional network equity. *Sage* 2024: https://journals.sagepub.com/doi/abs/10.1177/03611981241239963
- **Bicycle accessibility** — Theil with composite accessibility indicator, decomposed by citizenship status
- **Cordon pricing accessibility** — Multimodal Theil index in transport equity reviews
- **Energy/emissions inequality (Kaya-Theil)** — Standard for CO2 per-capita decomposition (urban/rural China)

These applications establish that Theil decomposition is methodologically accepted in transportation equity research — just not yet applied to EV charging infrastructure specifically.

---

## Caveats and Open Risks

1. **Chinese-language literature (CNKI) not searched.** China is the most active region for EV charging spatial analytics. Before publishing the narrowed novelty claim, an advisor or research librarian should spot-check CNKI for prior Theil decomposition work on EV charging in Chinese journals.
2. **The "to our knowledge" hedge is non-optional.** Any "first" claim must be hedged. A future reviewer with a different search strategy could surface prior work.
3. **Methodology section must explicitly cite Choi et al.** as the comparable prior work using Theil-as-scalar. Failing to cite a paper that came up in 30 seconds of Google Scholar will damage the submission's credibility.

---

## Suggested Paper Language (for Discussion / Methods sections)

**For lit review:**
> "Building on Choi et al. (2025), who incorporate the Theil index as one of several inequality metrics in an EV charger accessibility toolkit for Austin, this study extends the use of entropy-based measures by applying a full Theil-T decomposition to identify the relative contributions of within- and between-county inequality in North Carolina's public EV charging infrastructure."

**For contribution claim:**
> "To the authors' knowledge, this is the first application of a full Theil-T (entropy) decomposition to quantify within- and between-county inequality in public EV charging infrastructure."

**For longer methodological positioning:**
> "While prior EV charging equity studies have used the Theil index as a scalar inequality measure, this study is, to the authors' knowledge, the first to exploit the decomposability of Theil's T to separate within-county and between-county components of EV charging infrastructure inequality and to use those components as design inputs to a prioritization framework."

---

## Source — Research Provenance

This file consolidates findings from a 2026-05-12 literature check triggered by Dr. Al-Ghandour's offer to support a conference submission. Search strategy:
- Google Scholar queries on "Theil" + "EV charging" / "electric vehicle charging" / "charging infrastructure"
- SSRN, ResearchGate, arXiv preprint searches
- Past 5 years emphasized
- Closest adjacent transportation Theil work also surfaced for context

Search did **not** include Chinese-language databases (CNKI) — flagged as an open risk above.
