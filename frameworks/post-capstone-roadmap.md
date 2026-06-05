# EV Pulse NC — Post-Capstone Roadmap & Expert-Review Brief

**Project:** EV Pulse NC — North Carolina Electric Vehicle Analytics
**Owner:** Wolfgang Sanyer — personal portfolio project (no institutional affiliation)
**Created:** June 4, 2026
**Status:** Roadmap / not started — slated to be picked up the second week of July 2026 (target ~Mon July 13). **Exception: Direction 6 (Fayetteville/Cumberland stakeholder brief, added 2026-06-04) is near-term** — picked up after the owner's exam / next week, ahead of the July grid work.
**Purpose:** A self-contained brief that an expert panel (run in plan mode) can read cold and turn into a prioritized, sequenced implementation plan.

---

## How to use this document

This is a **future-direction roadmap**, not an implementation guide. It exists so that, when work resumes (~July 2026), we can hand a panel of expert agents a single artifact and ask them to review, challenge, and sequence it — without first re-reading the whole repository.

The document has four parts:

| Part | What it is | Audience |
|------|-----------|----------|
| **A. Context snapshot** | What EV Pulse NC is today + the gap that motivates this roadmap | Anyone picking this up cold |
| **B. Candidate directions** | Six candidate additions, each with rationale, data, integration, effort, risk, acceptance criteria, and open questions | The expert panel |
| **C. Open questions & decision points** | The cross-cutting decisions the panel must resolve before sequencing | The expert panel |
| **D. Expert-panel handoff brief** | A ready-to-paste prompt for running the review in plan mode | Whoever kicks off the review |

> **Convention reminder:** these are conceptual roadmaps only (per [`frameworks/README.md`](./README.md)) — no code, no fixed timeline, no final decisions. Effort estimates are rough sizing, not commitments.

---

## Part A — Context snapshot

### What EV Pulse NC is today

A complete, award-winning (MBA Showcase 2026, 2nd place) 5-phase analytics pipeline that answers: *Where should North Carolina invest its $109M federal NEVI dollars?* It does so by converging a **demand** estimate and a **supply** estimate into a **gap**, then refining the gap through three lenses into a weighted **NEVI Priority Score** per county.

```
Phase 1 Demand (validated BEV forecasts, MAPE 4.34%)  ─┐
Phase 2 Supply (1,985 AFDC stations, 6,145 connectors) ─┴─> Gap Analysis
                                                              │
   Phase 3 ZIP (where)  ·  Phase 4 Workplace (who/when)  ·  Phase 5 Equity (CEJST/Justice40)
                                                              │
                              NEVI Score = 0.40·Equity + 0.35·Utilization + 0.25·Cost-Effectiveness
                                                              │
                                          Ranked top-10 NC counties (73% of BEV fleet)
```

Full detail: [`frameworks/analytical-pipeline.md`](./analytical-pipeline.md). Phases 6 (buffer/charging-desert) and 7 (NCDOT corridor validation) are already documented there as **Future Directions** and are folded into this roadmap (Direction 3 below) rather than restated.

### The motivating gap

**The entire project is about EV-charging infrastructure, yet it contains no electrical-grid dimension.** The scoring weighs demand, ports, and equity, but never asks whether a recommended site can actually be *energized* — i.e., whether there is grid capacity nearby. For DC fast charging (150–350 kW), proximity to grid capacity is a first-order driver of cost and build time. This gap is the origin of this roadmap (it surfaced from a review of grid-mapping tools — inframap.org / openinframap.org — in June 2026).

### North Carolina grid context (important for any grid-related work)

This context determines which grid data is even *available* for NC, and it is a common source of wrong assumptions:

- **NC is not in an ISO/RTO.** Most of the eastern U.S. grid is run by market operators (PJM, MISO, etc.) that publish rich, near-real-time public data: nodal prices, minute-level load, generation mix, interconnection queues. **NC has none of this.**
- **NC is a regulated, vertically-integrated market** served almost entirely by **Duke Energy** (Duke Energy Carolinas + Duke Energy Progress), plus Dominion in the far northeast and various co-ops/munis. Duke owns generation + transmission + distribution and is its own balancing authority.
- **SERC** sits "over" NC, but only as a NERC *reliability* region (standards enforcement) — it is **not** a market operator and publishes no market data.
- **Consequence:** ISO/RTO-centric tools (e.g., inframap.org) show NC poorly or not at all — there are no nodal prices and no public minute-level market load to display.
- **What *is* available for NC:**
  - **Physical grid geometry** (substations, transmission lines) from **OpenStreetMap** via the openinframap / Overpass API — covers NC like everywhere else, regardless of market structure. This is the usable backbone for a grid-readiness layer.
  - **Coarser load data** from **EIA's Hourly Electric Grid Monitor** — hourly demand at the *balancing-authority* level (Duke Carolinas / Duke Progress). Real and free, just not nodal.
  - **Planning data** from Duke's **Integrated Resource Plans (IRPs)** and FERC/EIA filings.

> **Bottom line for the panel:** physical grid geometry → OSM/openinframap (works in NC); load context → EIA balancing-authority feeds (NC-appropriate, hourly not nodal); RTO market-price data → does not exist for NC, do not design around it.

---

## Part B — Candidate directions

Six candidate additions, grouped. Direction 1 (grid-readiness) and Direction 2 (dashboard) are the headline additions; Direction 3 collects already-roadmapped items; Directions 4–5 are methodological polish; Direction 6 (added 2026-06-04) is a near-term, stakeholder-facing deliverable that leapfrogs the others in urgency. The panel should treat ordering here as *proposed*, not fixed.

---

### Direction 1 — Grid-readiness layer ⭐ (flagship; new analytical dimension)

**What.** Add a fourth analytical lens: for each underserved county / ZIP, estimate how *feasible* it is to actually build charging there given the grid. A v1 proxy is **distance to the nearest substation and to the nearest transmission line**, producing a per-location "grid-readiness" score.

**Why it's useful.** The current model finds where demand outstrips ports. But a charging desert adjacent to spare substation capacity is cheap and fast to energize; one far from any grid asset implies a costly, slow interconnection — especially for DCFC. NEVI administrators weigh this heavily, and the pipeline currently ignores it entirely. It also differentiates the project from typical "demand vs. supply" EV studies.

**Integration into the existing pipeline.** Two options for the panel to weigh:
- **(a) As a new sub-factor of the Cost-Effectiveness Score** (currently 0.25, Phase 4 only) — re-balance that component to include grid proximity.
- **(b) As a feasibility filter / tie-breaker** applied *after* scoring — does not disturb the validated weights, flags "high-need but hard-to-build" vs. "high-need and shovel-ready."

**Data & sources.**
- `power=substation`, `power=line`, `power=tower` from **OpenStreetMap** via the **Overpass API** or **openinframap** tiles/data. Free, NC-covered, vector geometry.
- Spatial-join to existing station / ZIP / county layers using **GeoPandas** (already a project dependency).
- Optional enrichment: **EIA Hourly Electric Grid Monitor** for Duke BA load context.

**Effort (rough).** Moderate — one new acquisition script (`src/data-acquisition/osm_grid_download.py`), one analysis module, 2–3 figures, plus DATA-DICTIONARY and data-sources updates.

**Risks & honest caveats.**
- **OSM capacity attributes are patchy in NC.** Voltage/MVA tags are incompletely mapped. Proximity is a defensible v1 *feasibility proxy*; do **not** present it as a capacity/load-flow model.
- **OSM completeness** for transmission vs. distribution differs — transmission lines are well-mapped; sub-transmission/distribution substations less so.
- **Spatial-join correctness** (CRS, projection for distance in meters) must be validated against a handful of known sites.

**Acceptance criteria.**
- A reproducible script pulls NC grid geometry from a documented, free source.
- Each of the existing top-20 underserved ZIPs has a computed distance-to-substation and distance-to-transmission.
- A figure overlays grid assets on the underserved choropleth.
- A short written validation: spot-check 5–10 locations against a public map; state OSM coverage limitations explicitly.

**Open questions for the panel.** See Part C, Q1–Q3.

---

### Direction 2 — Interactive dashboard ⭐ (largest portfolio lever)

**What.** A lightweight, interactive web map/dashboard of the NEVI results: county + ZIP choropleths with toggleable layers (demand, supply gap, equity, and — if Direction 1 ships — grid), plus the top-20 underserved list and component-score breakdowns.

**Why it's useful.** The project currently lives in a 109-page PDF and 45 static figures. An interactive artifact a reviewer can click through is far more memorable for a portfolio and far more useful to a stakeholder (county planner, NEVI admin). The "grid-intelligence dashboard" UX pattern — a headline metric, regional breakdown cards, a layer-toggle map explorer, an alerts/priority strip — is well established (inframap.org is a strong *design* reference; borrow the layout, feed it our data).

**Integration.** Read-only consumer of existing processed outputs (`data/processed/*.csv`, scoring outputs). No change to the analytical pipeline.

**Data & sources.** All from existing project outputs. No new external data required.

**Effort (rough).** Moderate — depends heavily on stack choice (see Q4).

**Risks & caveats.**
- **Hosting / reproducibility:** a server-based app (Streamlit) needs hosting; a static client-side map (Leaflet/Observable) hosts free on GitHub Pages but is less dynamic. Decide before building (Q4).
- **License:** the repo is Polyform Noncommercial — any hosted demo must respect that.
- **Scope creep:** easy to over-build. Define an MVP (one map, the layer toggles, the top-20 list) and stop.

**Acceptance criteria.**
- An MVP renders the NEVI choropleth with at least demand / gap / equity layer toggles.
- The top-20 underserved list is visible and tied to the map.
- A documented run/deploy path (`how to launch locally`, and hosting target if any).

**Open questions for the panel.** See Part C, Q4.

---

### Direction 3 — Already-roadmapped items (lowest risk; pre-scoped)

These are documented in [`analytical-pipeline.md`](./analytical-pipeline.md) as Future Directions; collected here so the panel can sequence them alongside the new work.

**3a — Phase 6: Buffer / charging-desert analysis.**
- *What:* coverage zones around stations to visually define "charging deserts." Simple version: fixed-radius buffers; better: road-network drive-time isochrones (e.g., OSRM/Valhalla on OSM road data).
- *Why:* a compelling visual that pairs naturally with Direction 1 (grid-readiness) — "underserved AND hard to energize" is the strongest NEVI-targeting signal.
- *Effort:* Low–moderate (buffers low; isochrones moderate). *Acceptance:* desert map + count of population in deserts.

**3b — Phase 7: NCDOT corridor validation.**
- *What:* compare the project's equity-weighted top counties against NCDOT's actual Feb-2026 rural-deployment pivot (50 corridor stations → 16 rural locations; second-wave RFP opened late March 2026). NCDOT NEVI Mapping Tool: https://experience.arcgis.com/experience/a1e1459fffee4ccbafaf888f838dcac6/page/NCDOT-NEVI-Mapping-Tool
- *Why:* an external benchmark. If our scores independently recommend rural sites, it validates *both* the methodology and NCDOT's policy shift.
- *Effort:* 3–5 hrs (per existing estimate). *Acceptance:* a score-vs-deployment comparison table + agreement metric. *Note:* advisor (former DOT/CDOT) suggested NCDOT planning data may be obtainable directly.

**3c — Statewide extension + dollar allocation + confidence intervals.**
- *What:* extend scoring from top-10 to all 100 counties; add a NEVI dollar allocation proportional to score; add confidence intervals on composite scores.
- *Why:* turns "top-10 ranking" into a complete, fundable allocation table — directly more useful to an administrator and a stronger headline result.
- *Effort:* Moderate. *Acceptance:* all-100 ranked table with $ allocation summing to the $109M envelope and CI bands.

---

### Direction 4 — Forecast bias correction (methodological polish)

**What.** Phase 1 found a **systematic 69.00% underprediction bias** (+18.22 vehicles mean). Add a bias-corrected forecast variant (or a model/specification that addresses the systematic under-shoot) and re-run the utilization-score sensitivity.

**Why useful.** Utilization is 35% of the score and rests on these forecasts; the underprediction is the pipeline's most-acknowledged weak point. A documented correction tightens the project's central analytical claim.

**Effort.** Low–moderate (re-uses existing SAS/Python forecast tooling). **Acceptance:** corrected-vs-raw comparison + impact on the top-10 ranking (does the order change?).

---

### Direction 5 — Living-data refresh (portfolio durability)

**What.** Both primary feeds update monthly (NCDOT registrations; AFDC/NREL API). Add a scheduled/automatable refresh so the analysis stays current rather than frozen at the capstone snapshot.

**Why useful.** A repo that visibly stays current is a strong portfolio signal and makes the dashboard (Direction 2) genuinely live. Could be driven by the orchestrator's scheduling.

**Effort.** Low for the data pull (scripts exist); moderate if it must re-render figures/scoring end-to-end. **Risks:** the NCDOT May-2025 methodology break shows schemas can shift — a refresh needs validation/guardrails, not blind overwrite. **Acceptance:** a documented one-command refresh + a freshness indicator; guardrail that flags schema/row-count anomalies before overwriting.

---

### Direction 6 — Fayetteville / Cumberland stakeholder brief ⭐ (near-term; stakeholder-facing, no new analytical dimension)

**Status & priority.** Added 2026-06-04. Unlike Directions 1–5 (parked for ~July), this is the **most immediate** extension — picked up after the owner's exam / next week. Motivated by a concrete opportunity: a prospective meeting with the **Fayetteville mayor's office** about collaborating on EV-charging deployment. Near-term sequencing: (1) paper publishing / SEINFORMS, (2) **this brief**, (3) grid extension (Direction 1).

**What.** A self-contained, stakeholder-facing analytical brief applying the existing EV Pulse methodology to **Cumberland County and Fayetteville specifically** — a place the statewide study covered in its base layers but never *scored* (Cumberland is #11 by BEV count, just outside the scored top-10). Two-tier, matching the project's core method:
- **Tier 1 — county score (context):** compute Cumberland's NEVI Priority Score (util / cost / equity) on the same framework as the top-10, on a comparable scale. Computed **standalone** — does **not** edit the locked 10-county manuscript table.
- **Tier 2 — Fayetteville ZIP/tract targeting (the deployment ask):** Phase-3 underserved-ZIP ranking + Phase-5 Justice40 overlay, filtered to Fayetteville's ZIPs, producing specific "deploy here" targets. Full Cumberland County framing kept available for parallel **county-level** engagement (a combined city + county effort).

**Why it's useful.** The data tells a compelling stakeholder story: Cumberland is a **high-equity-need county the demand-ranking skipped** — exactly the population NEVI's equity provisions exist to catch. Headline signals (from repo data, June 2026):
- BEV registrations **1,584** (Oct 2025), **#11 statewide** — just outside the scored top-10.
- EV share of fleet **0.96%** vs Wake 4.0% / Mecklenburg 3.0% — low adoption; a charging chicken-and-egg gap.
- **34/68 tracts (50%) Justice40-disadvantaged** vs 43% statewide — among the most disadvantaged study areas.
- **Fort Bragg** proximity (note: the base was redesignated from "Fort Liberty" **back to Fort Bragg in Feb 2025** — use *Fort Bragg*) — a distinct military/veteran demand pool and a federal-alignment angle.
- **I-95 corridor** — economic-development / through-traffic charging case.

**Four framing angles** (all four in scope): Equity / Justice40 · Economic development (I-95) · Military / Fort Bragg · NEVI funding readiness.

**Integration.** Read-only consumer of existing processed outputs plus the existing scoring / Phase-3 / Phase-5 methods. Does **not** disturb the validated weights or the locked 10-county manuscript table. New artifacts only: a standalone Cumberland score table, Fayetteville ZIP targets, ~3 figures, and a brief doc (markdown → PDF).

**Data & sources.**
- *Existing (sufficient for 3 of 4 angles):* NCDOT registrations, AFDC stations, CEJST/Justice40 tracts, ACS income/tenure, the scoring-framework method.
- *New / optional — military quantification (Fort Bragg):* combination approach — **(a)** qualitative proximity framing (always), plus **(b)** a Census/DoD source to quantify *if clean data is obtainable* (e.g., ACS military-employment / veteran-population tables for Cumberland; DoD installation personnel). Fall back to qualitative-only if no defensible source exists. This is the only angle requiring data outside the repo.

**Effort (rough).** Low–moderate — reuses existing methods; new work is filtering to one county / ZIP set, a standalone score, ~3 figures, the brief doc, and the optional military data pull.

**Panel.** Reviewed by the **standard advisory panel (Reyes / Okonkwo / Whitfield)** — *not* the grid-specific Part-D panel — expandable if a gap surfaces. Per workflow, the plan goes to the panel for approval before execution.

**Acceptance criteria.**
- A standalone Cumberland NEVI score on the same scale as the top-10, with components shown.
- A ranked list of underserved Fayetteville ZIPs with Justice40 overlay.
- ≥3 figures (Cumberland-in-context score; Fayetteville underserved map; equity overlay with existing stations).
- A stakeholder brief (PDF) organized around the four angles, readable by a non-technical mayor's office.
- Military angle either quantified from a cited source or explicitly framed qualitatively — no hand-waving.

**Open questions for the panel.**
- **Fayetteville boundary:** which ZCTAs define "Fayetteville" (e.g., 28301 / 28303 / 28304 / 28305 / 28311 / 28312 / 28314 …) vs whole-county.
- **Score placement:** standalone Cumberland table (recommended) vs an 11-county re-run — confirm the manuscript table stays untouched.
- **Military quantification:** is a defensible free Census/DoD figure obtainable, or is qualitative-only the honest call?
- **City vs county emphasis:** lead with the city (mayor's audience) while keeping county framing for parallel county engagement?

---

## Part C — Open questions & decision points (for the panel)

The cross-cutting decisions the panel should resolve and feed into sequencing:

| # | Question | Why it matters |
|---|----------|----------------|
| **Q1** | Should grid-readiness enter the **score** (re-weight Cost-Effectiveness) or sit as a **post-hoc feasibility filter**? | Re-weighting touches the validated 0.40/0.35/0.25 framework and its sensitivity analysis; a filter preserves it. Trade-off: integration vs. defensibility. |
| **Q2** | Is **OSM proximity** a defensible grid-readiness proxy for an academic/portfolio claim, or does it need EIA/Duke capacity enrichment to be credible? | Determines whether Direction 1 is a weekend spike or a larger data effort. |
| **Q3** | What **granularity** for the grid layer — county, ZIP/ZCTA, or station-point? | Must align with the layer it feeds; finer = more OSM-completeness risk. |
| **Q4** | Dashboard stack: **Streamlit (server, dynamic, needs hosting)** vs. **Leaflet/Observable (static, free GH Pages, less dynamic)** vs. **other**? | Drives effort, hosting cost, and how "live" Direction 5 can make it. Respect Polyform Noncommercial. |
| **Q5** | **Sequencing & dependencies:** Direction 1 and 3a (buffers) are synergistic; 2 benefits from 1; 5 benefits from 2. What is the optimal order given ~a few weekends of effort? | This is the panel's core deliverable. |
| **Q6** | **Scope ceiling:** which subset is the right "v1" to actually ship in the next work block, vs. parked? | Prevents over-building; the project is already complete and award-winning — additions must clear a value bar. |
| **Q7** | Any **data-availability blockers** to verify *before* committing (OSM NC substation completeness, EIA BA coverage for Duke, obtainability of NCDOT planning data)? | De-risks the plan; cheap to check first. |

---

## Part D — Expert-panel handoff brief (plan mode)

> **How to run this:** open a session in the `ev-pulse-nc` repo, enter **plan mode**, and paste the brief below. Run it as a panel (multiple expert perspectives — e.g., an energy/grid analyst, a geospatial/data-engineering reviewer, and a policy/NEVI reviewer) and ask for a synthesized, sequenced plan. Pair this brief with the two anchor docs it references.
>
> **Note (2026-06-04):** this handoff covers Directions 1–5 (the grid-centric directions) and references "the five candidate directions" deliberately. **Direction 6 (Fayetteville/Cumberland stakeholder brief) is out of scope for this prompt** — it is reviewed separately by the standard advisory panel (Reyes / Okonkwo / Whitfield), not this grid-focused panel.

```
ROLE
You are a panel of three reviewers evaluating a post-capstone roadmap for EV Pulse NC,
an award-winning North Carolina EV-charging NEVI-allocation analytics project:
  1. An energy/electrical-grid analyst (US grid markets, interconnection, NC/Duke specifics)
  2. A geospatial + data-engineering reviewer (GeoPandas, OSM/Overpass, reproducible pipelines)
  3. A transportation-policy / NEVI-program reviewer (federal NEVI, Justice40, NCDOT)

CONTEXT TO READ FIRST (in this repo)
  - frameworks/post-capstone-roadmap.md   (this roadmap — Parts A–C)
  - frameworks/analytical-pipeline.md      (the completed 5-phase pipeline + scoring)
  - references/data-sources.md             (existing data sources)
Treat Part A's "North Carolina grid context" as binding: NC is non-RTO (Duke / SERC),
so RTO-style nodal/real-time market data does not exist for NC. Do not design around it.

YOUR TASK
Review the five candidate directions and the open questions (Part C), then produce a
single SEQUENCED IMPLEMENTATION PLAN. For each direction you recommend:
  - A crisp problem statement and the decision you make on its open questions
  - Concrete data sources + endpoints, and a pre-flight data-availability check to run first
  - How it integrates with the existing pipeline WITHOUT breaking the validated scoring weights
  - Effort sizing, key risks, and explicit acceptance criteria
  - Dependencies on other directions (what must precede it)

CONSTRAINTS
  - These are additions to a COMPLETE, award-winning project. Every addition must clear a
    value bar; recommend parking anything that doesn't. Propose a defensible "v1" scope.
  - Free / public data only. Stack already includes Python, pandas, GeoPandas, SAS.
  - Repo license is Polyform Noncommercial — any hosted demo must comply.
  - Be honest about OSM data-completeness limits in NC; flag where a proxy is being sold
    as more than a proxy.

DELIVERABLE
  1. A recommended scope (which directions are in v1, which are parked, and why).
  2. A dependency-ordered sequence with rough effort per step.
  3. Resolved answers to open questions Q1–Q7, with reasoning.
  4. A pre-flight checklist of data-availability checks to run before committing.
  5. The top 3 risks to the plan and how to de-risk each.
```

---

## Reference — websites, data sources & endpoints

Complete link inventory so the panel (and future-us) never has to reconstruct a URL. Grouped by purpose.

### Grid data & tools (new — Directions 1, 2)

| Resource | URL | What it is / why here |
|----------|-----|-----------------------|
| **openinframap** (web map) | https://openinframap.org/ | Open, OSM-backed map of world power/telecom/oil/gas/water infrastructure. The **usable** sibling for NC grid geometry. |
| openinframap — about | https://openinframap.org/about | Data provenance + project description (data sourced from OpenStreetMap). |
| openinframap — source code | https://github.com/openinframap/openinframap | Open-source; reference for tiling/rendering a grid layer. |
| Open Infrastructure Map — OSM wiki | https://wiki.openstreetmap.org/wiki/Open_Infrastructure_Map | Background + tagging conventions for `power=*`. |
| **Overpass API** (OSM query) | https://overpass-api.de/api/interpreter | Pull `power=substation` / `power=line` / `power=tower` for NC. Free; capacity tags patchy. |
| Overpass Turbo (interactive) | https://overpass-turbo.eu/ | Prototype/visualize Overpass queries before scripting. |
| **inframap.org** (design reference only) | https://www.inframap.org/ | Commercial US "grid-intelligence" dashboard (ISO/RTO-centric → **weak NC coverage**). Borrow the **UX/layout** for Direction 2; **not** a data source for NC. |
| **EIA Hourly Electric Grid Monitor** | https://www.eia.gov/electricity/gridmonitor/ | Hourly demand at balancing-authority level (Duke Carolinas / Duke Progress) — NC-appropriate load context. |
| EIA Open Data (API) | https://www.eia.gov/opendata/ | Programmatic access to the above. |
| Duke Energy IRPs / FERC filings | public filings (Duke / FERC eLibrary) | Coarse, planning-horizon capacity context. |

### NEVI / policy & validation (Direction 3b)

| Resource | URL | Why here |
|----------|-----|----------|
| NCDOT NEVI Mapping Tool | https://experience.arcgis.com/experience/a1e1459fffee4ccbafaf888f838dcac6/page/NCDOT-NEVI-Mapping-Tool | NCDOT planned deployments — validation benchmark. |
| NCDOT ZEV registration data | https://www.ncdot.gov/initiatives-policies/environmental/climate-change/Pages/zev-registration-data.aspx | Source of the BEV registration panel (existing). |
| NCDOT 2nd-wave NEVI press release | https://www.ncdot.gov/news/press-releases/Pages/2026/2026-03-27-applications-open-second-wave-ev-charging-stations.aspx | $109M allocation + Feb-2026 rural pivot context. |
| FHWA NEVI Formula Program | https://www.fhwa.dot.gov/environment/nevi/ | Federal program authority + Justice40 mandate. |

### Existing pipeline data (already integrated)

| Resource | URL | Notes |
|----------|-----|-------|
| NREL AFDC API (charging stations) | https://developer.nrel.gov/api/alt-fuel-stations/v1.json | Supply-side baseline (Phase 2). |
| NREL API key signup | https://developer.nrel.gov/signup/ | Free, instant. |
| IEA Global EV Outlook (benchmark) | https://www.iea.org/reports/global-ev-outlook-2024/trends-in-electric-vehicle-charging | EVs-per-charger benchmarks (global ~10). |
| Full existing source list | see [`../references/data-sources.md`](../references/data-sources.md) | NCDOT, AFDC, CEJST, LEHD/LODES, etc. |

---

## Document metadata

- **Created:** June 4, 2026
- **Status:** Roadmap — not started; scheduled to revisit the second week of July 2026 (target ~Mon July 13). Direction 6 (added 2026-06-04) is near-term, ahead of the July work.
- **Version:** 1.1 (2026-06-04 — added Direction 6, Fayetteville/Cumberland stakeholder brief; no prior content removed)
- **Related:** [`analytical-pipeline.md`](./analytical-pipeline.md) (Phases 6/7 Future Directions), [`README.md`](./README.md), [`../references/data-sources.md`](../references/data-sources.md)
- **Origin:** Grew out of a June 2026 review of grid-mapping tools (inframap.org / openinframap.org) that surfaced the project's missing electrical-grid dimension.
