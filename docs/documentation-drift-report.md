---
title: "EV Pulse NC — Documentation Drift Audit"
auditor: "Documentation Drift Auditor (sub-agent)"
audit_date: 2026-04-09
ground_truth_basis: "git log --all --merges + file inventory of data/, code/, output/"
scope: "All .md / .txt docs across the repo (plus in-scope code string labels for HEPGIS)"
output_pass: "A — read-only audit"
---

# Executive Summary

- **Phases verified merged into `main`:** Phase 1 (validation), Phase 2 (AFDC update), Phase 3 (ZIP analysis), Phase 4 (workplace charging / LEHD), Phase 5 (CEJST equity). All 5 phases complete.
- **Total drift items found:** 27 (Critical: 9, Moderate: 13, Minor: 5)
- **Total inconsistency items found:** 7
- **Files audited:** 30 markdown/text docs + 2 code files (HEPGIS string hits)
- **Files with at least one issue:** 14

**Most important finding:** The two top-of-repo "face of the project" docs — `README.md` and `PROJECT-BRIEF.md` / `PROJECT-EXPLANATION.md` — still describe EV Pulse NC as "Phase 1 Complete" with 355 stations / 1,725 connectors as the active infrastructure baseline, three pending extensions, and no mention of Phases 3, 4, or 5. Any advisor (Dr. Al-Ghandour), reviewer, or peer opening the repo will see a February 2026 snapshot that undersells five merged phases of work. This is the single most load-bearing correction for Pass B.

# Ground Truth Verified

## Merge commits on `main` (git log --all --merges)

```
d9685fd Merge feat/phase5-equity-analysis into main (Phase 5 complete)
93b617c Merge feat/phase4-workplace-charging into main (Phase 4 complete)
0c67187 Merge feat/phase3-zip-analysis into main (Phase 3 complete)
a431dc2 Merge feat/phase2-afdc-update into main (Phase 2 complete)
362758c Merge pull request #1 from wolfieman/feat/phase1-validation
```

## Phase 5 implemented with CEJST (NOT HEPGIS)

Verified by data files and code:
- `data/raw/cejst-justice40-tracts-nc.csv`
- `data/raw/cejst-justice40-tracts-nc-border.csv`
- `data/raw/cejst-justice40-tracts-nc-categories.csv`
- `code/python/analysis/eda_cejst_justice40.py`
- `code/python/analysis/phase5_climate_sensitivity.py`
- `code/python/analysis/phase5_tract_zcta_crosswalk.py`
- `code/python/analysis/phase5_fig39_to_fig42.py`
- `code/python/analysis/phase5_weight_sensitivity.py`
- `data/processed/phase5-county-justice40.csv`, `phase5-zcta-justice40.csv`
- Publication figures fig-39 through fig-42 (CEJST disadvantaged tracts, ZCTA Justice40 choropleth, county comparison, stations Justice40 overlay) present in `output/figures/`.
- Commit `1546560` explicitly fixes "CEJST denominator (43.0% not 42.6%)" — Phase 5 analytic results are post-review stage.

There is **zero** evidence in `data/raw/` or `code/` of an HEPGIS dataset ever being acquired or used.

## Phase 4 implemented with LEHD/LODES + ACS (workplace charging)

- `data/raw/lehd-nc-od-main-2021.csv.gz`, `lehd-nc-wac-2021.csv.gz`, `lehd-nc-xwalk.csv.gz`
- `code/python/analysis/eda_phase4_lehd_acs.py`
- `code/python/analysis/phase4_workplace_charging.py`
- `code/python/analysis/phase4_fig35_to_fig38.py`
- `data/processed/phase4-cost-effectiveness.csv`, `phase4-employment-centers.csv`
- Figures fig-35 to fig-38 present.

## Phase 3 implemented

- 18 `phase3_*.py` scripts in `code/python/analysis/`
- `data/processed/phase3-*` CSVs (Gini, Theil, ZIP density, top 20 underserved, county mapping, etc.)
- Figures fig-25 to fig-34 present.
- Scoring framework: `scoring_framework_final.py`, `scoring_framework_skeleton.py`, `data/processed/scoring-framework-final.csv`, `scoring-weight-sensitivity.csv`.

## Phase 2 implemented

- `data/raw/afdc-charging-stations-connector-2026-02.csv` (current baseline)
- Per `AFDC-DATA-COMPARISON.md`: 1,985 stations, 6,145 connectors

## Canonical infrastructure baseline

**Current (post-Phase 2):** 1,985 stations, 6,145 connectors, 267 cities, 358 ZIPs (all levels L1/L2/DCFC).
**Stale (pre-Phase 2):** 355 stations, 1,725 connectors (DCFC-only extract, retained for reference only per `AFDC-DATA-COMPARISON.md` and `frameworks/README.md` §"Actual Outcome").

## Commit-prefix convention

Of the last 50 commits on `main`:
- `[EVPULSE]` — dominant on all Phase 3, 4, 5 work (recent)
- `[EVPULS]` — used during Phase 2 transition and earlier
- `[EV-PULSE]` — 2 commits (Apr 8–9 docs/fix)
- `[EVPULS]` (typo-shortened) — legacy

**Recommended canonical form for docs: `[EVPULSE]`.**

---

# Drift Items (Pass B will fix)

## D1 — `README.md` top-level project status frozen at "Phase 1 Complete"
- **File:** `README.md`
- **Line(s):** 320–321
- **Stale claim (verbatim):** `**Status:** Phase 1 Complete (Forecast Validation)` / `**Last Updated:** February 2026`
- **Reality:** All 5 phases merged. Phase 5 analysis post-review as of April 2026.
- **Recommended fix:** `**Status:** All 5 phases complete (Phase 1 Validation, Phase 2 AFDC Update, Phase 3 ZIP Analysis, Phase 4 Workplace Charging, Phase 5 CEJST Equity)` / `**Last Updated:** April 2026`
- **Severity:** Critical

## D2 — `README.md` Infrastructure Snapshot uses stale 355/1,725
- **File:** `README.md`
- **Line(s):** 32, 67, 249
- **Stale claim:** "355 charging stations, 1,725 individual charging units" (line 32); "1,725 charging connector records across 355 stations" (line 67); "1,725 individual charging units analyzed (4.85x more granular than station-level)" (line 249)
- **Reality:** Phase 2 replaced this with 1,985 stations / 6,145 connectors (all levels). Old extract retained for reference only.
- **Recommended fix:** Replace with "1,985 charging stations, 6,145 charging connectors (all levels L1/L2/DCFC, 267 cities, 358 ZIPs)". Update the "Key Differentiator #3" text to reflect connector count 6,145.
- **Severity:** Critical

## D3 — `README.md` "Analytical Workflow" section uses the old 5-phase descriptive-analytics taxonomy, not the 5 merged project phases
- **File:** `README.md`
- **Line(s):** 169–223
- **Stale claim:** Sections "Phase 1: Exploratory Analysis" … "Phase 5: Prescriptive Analysis" correspond to a generic 5-phase analytics framework (exploratory/descriptive/diagnostic/predictive/prescriptive), not the project's actual Phase 1–5 (Validation / AFDC / ZIP / Workplace / Equity) that are documented in `frameworks/analytical-pipeline.md` and `frameworks/README.md`.
- **Reality:** The project now uses "Phase N" to mean the merged work branches. Having two incompatible "Phase" definitions in one repo is actively confusing.
- **Recommended fix:** Replace this section with a table referencing the five merged phases and pointing to `frameworks/analytical-pipeline.md` as the canonical pipeline doc. Key Findings counts (Gini 0.805, 72% top-10, 16.9 BEV/port) are baseline-semester numbers and can stay but should be labeled "Baseline (Fall 2025)".
- **Severity:** Moderate

## D4 — `PROJECT-BRIEF.md` describes three extensions as pending
- **File:** `PROJECT-BRIEF.md`
- **Line(s):** entire document, esp. 14, 20–34 (only Priority #1 marked COMPLETE), 38–46 (ZIP "extension will geocode…"), 50–58 (workplace "extension adds…"), 62–66 ("Integration Logic"), 86–90 ("Conclusion")
- **Stale claim:** Document is dated February 1, 2026 and frames Priorities #2, #3, #5 as future work. Also uses 1,725 connectors / 355 stations throughout (lines 12, 16, 42, 76).
- **Reality:** Priorities 2–5 and the scoring framework are merged. AFDC baseline is 1,985 / 6,145.
- **Recommended fix:** Either (a) rewrite as a post-hoc project brief reflecting what was delivered (5 phases, CEJST equity, NEVI scoring framework), or (b) mark the file "Historical — Feb 1 2026 proposal" at the top and add a pointer to `frameworks/analytical-pipeline.md` + `paper/PAPER-NOTES.md` for current status. Replace all `1,725` / `355` counts with `6,145` / `1,985`.
- **Severity:** Critical

## D5 — `PROJECT-EXPLANATION.md` is a Feb 1, 2026 snapshot frozen mid-Phase 1
- **File:** `PROJECT-EXPLANATION.md`
- **Line(s):** 5 (Date), 13, 15 (1,725/355), 27, 147 (1,725/355), 43 (Priority #5 as next), 89–104 (ZIP code extension described as future, "The baseline analysis used AFDC's July 2024 infrastructure snapshot, which is now six months stale"), 107–123 (workplace extension as future), 131 ("Without updated infrastructure data, extensions would compound the 6-month staleness problem"), 159 ("Remaining extensions include …")
- **Stale claim:** Entire document treats Phases 2–5 as future work and uses stale infrastructure counts.
- **Reality:** All extensions delivered; infrastructure has been updated; CEJST equity layer (not HEPGIS) implemented.
- **Recommended fix:** Same as D4 — either rewrite reflecting completion or mark as "Historical proposal (Feb 1 2026)" with a forward link to current docs. Replace all `1,725` / `355` references. The "dual-snapshot" framing (lines 97–101, 149) is particularly out of date: per `frameworks/README.md` §"Actual Outcome", the dual-snapshot idea was abandoned once the July 2024 file was found to be a DCFC-only extract with data through Dec 2025. Remove the dual-snapshot narrative or caveat it.
- **Severity:** Critical

## D6 — `frameworks/README.md` marks Phase 5 as "⏳ Pending" and names it "HEPGIS Equity Analysis"
- **File:** `frameworks/README.md`
- **Line(s):** 50, 128–131
- **Stale claim (line 50):** `| **5** | **5** (was #4) | HEPGIS Equity Analysis | ⏳ Pending | Justice40 integration (not yet started) |`
- **Stale claim (lines 128–131):** `### Priority #5 / Phase 5: HEPGIS Equity Analysis` … `**Status:** Not yet started`
- **Reality:** Phase 5 merged (commit `d9685fd`); implemented with CEJST tract-level Justice40, not HEPGIS.
- **Recommended fix:** Change row to `| **5** | **5** | CEJST Equity Analysis (Phase 5) | ✅ Complete | CEJST Justice40 tract overlay; county + ZCTA Justice40 shares; climate sensitivity; weight sensitivity; figures 39–42 |`. Rewrite §"Priority #5 / Phase 5" heading to "CEJST Equity Analysis" and change Status to "Complete (Mar–Apr 2026)" with a 1–2 line summary of what was delivered.
- **Severity:** Critical

## D7 — `frameworks/README.md` Equity_Score cites "HEPGIS + ZIP"
- **File:** `frameworks/README.md`
- **Line:** 65
- **Stale claim:** `| **Equity_Score** | HEPGIS + ZIP code analysis (#3/#5) | Justice40 disadvantaged community %, Gini coefficient, rural access gap, zero-infrastructure flag |`
- **Reality:** Equity score is computed from CEJST Justice40 (Phase 5) + Phase 3 Gini/Theil.
- **Recommended fix:** `| **Equity_Score** | CEJST Justice40 equity (Phase 5) + Phase 3 ZIP analysis | Justice40 disadvantaged community %, Gini coefficient, rural access gap, zero-infrastructure flag |`
- **Severity:** Moderate

## D8 — `frameworks/README.md` marks Phase 6 (Buffer) as Pending
- **File:** `frameworks/README.md`
- **Line:** 51
- **Stale claim:** `| **6** | **6** | Buffer Analysis | ⏳ Pending | Coverage zones (not yet started) |`
- **Reality:** Phase 6 was always marked optional/enhancement. No buffer analysis is merged (consistent with the "all 5 core phases" framing). This is **partially stale**: "Pending" is technically true (not done) but in the context of a project that is research-complete, the correct label is "Deferred / Out of scope" or "Optional — not pursued", not an unresolved TODO.
- **Recommended fix:** `| **6** | **6** | Buffer Analysis | Deferred (optional enhancement, out of scope for paper) | — |`
- **Severity:** Minor

## D9 — `frameworks/README.md` Phase 7 NCDOT corridor row frames it as "Optional, pending"
- **File:** `frameworks/README.md`
- **Line:** 52, 133–141
- **Stale claim:** Frames as active optional work.
- **Reality:** No evidence of NCDOT corridor validation output in `data/processed/` or `output/`. This appears to be legitimately not done. Same ask as D8: relabel "Deferred / not pursued" if that is the case, or leave as-is if still active.
- **Recommended fix:** Clarify status — either mark "Deferred" with a 1-line note, or confirm it remains an open option and leave. Report-only; Pass C should confirm with user.
- **Severity:** Minor

## D10 — `frameworks/README.md` top-level "Status: Phase 1 Complete (Feb 2026)"
- **File:** `frameworks/README.md`
- **Line(s):** 5, 292–293
- **Stale claim:** `**Status:** Phase 1 Complete (Feb 2026)` (line 5) / `**Last Updated:** February 26, 2026` / `**Status:** Phases 1-2 Complete; …` (line 293)
- **Reality:** All 5 phases merged.
- **Recommended fix:** Update both to "All 5 phases complete (Apr 2026)" and "Last Updated: April 2026".
- **Severity:** Critical

## D11 — `frameworks/analytical-pipeline.md` ASCII diagram shows Phases 3/4/5 as [PENDING]
- **File:** `frameworks/analytical-pipeline.md`
- **Line(s):** 63–80
- **Stale claim:** Diagram boxes labeled `PHASE 3 ZIP Code Analysis [PENDING]`, `PHASE 4 CTPP Workplace Charging [PENDING]`, `PHASE 5 HEPGIS Equity Analysis [PENDING]`. Phase 5 labeled "HEPGIS Equity / Analysis".
- **Reality:** All complete; Phase 5 is CEJST.
- **Recommended fix:** Change all three `[PENDING]` labels to `[COMPLETE]`. Rename the Phase 5 box from "HEPGIS Equity / Analysis" to "CEJST Equity / Analysis". Update the inline descriptors (line 69 "Justice40 / disadvantaged / community / overlay" is fine as-is since that's what CEJST provides). Line 79 "Est: TBD" for Phase 5 → "Complete".
- **Severity:** Critical

## D12 — `frameworks/analytical-pipeline.md` Phase Summary table marks Phases 3/4/5 PENDING
- **File:** `frameworks/analytical-pipeline.md`
- **Line(s):** 135–137
- **Stale claim:** `| **3** | 3 | ZIP Code Analysis (WHERE) | **PENDING** | 4-6 hrs | … |` / `| **4** | 4 | CTPP Workplace Charging (WHO/WHEN) | **PENDING** | 3 hrs | … |` / `| **5** | 5 | HEPGIS Equity Analysis (EQUITY) | **PENDING** | TBD | Justice40 overlay, disadvantaged community mapping | Equity Score (weight: 0.40) |`
- **Reality:** All three merged. Phase 5 is CEJST.
- **Recommended fix:** Mark all three **COMPLETE**, replace time estimates with completion dates (Mar 2026 for Phase 3/4, Apr 2026 for Phase 5). Rename Phase 5 row to "CEJST Equity Analysis (EQUITY)".
- **Severity:** Critical

## D13 — `frameworks/analytical-pipeline.md` Paper Alignment table uses "HEPGIS Equity"
- **File:** `frameworks/analytical-pipeline.md`
- **Line:** 252
- **Stale claim:** `| **Phase 5: HEPGIS Equity** | Results + Discussion | Results: Justice40 overlay, disadvantaged community mapping. Discussion: policy implications for equitable NEVI deployment |`
- **Recommended fix:** `| **Phase 5: CEJST Equity** | Results + Discussion | Results: CEJST tract-level Justice40 overlay, county + ZCTA disadvantaged community shares, climate-subset sensitivity, weight sensitivity. Discussion: policy implications for equitable NEVI deployment |`
- **Severity:** Moderate

## D14 — `frameworks/analytical-pipeline.md` "Pending (Core)" section lists Phase 4 and Phase 5
- **File:** `frameworks/analytical-pipeline.md`
- **Line(s):** 215–221
- **Stale claim:** Header "### Pending (Core)" with rows for Phase 4 (CTPP) and Phase 5 (HEPGIS Equity).
- **Reality:** Both merged. The existing "### Completed" section (lines 207–214) lists Phases 1–3 only and needs to be extended.
- **Recommended fix:** Move Phase 4 and Phase 5 into the "Completed" table with completion dates and key results. Delete the "Pending (Core)" section (or leave as an empty header with "None — all core phases complete"). Update line 237 "Total remaining core effort: approximately 7-9 hours plus Phase 5 (TBD)" → "All core phases complete."
- **Severity:** Critical

## D15 — `frameworks/analytical-pipeline.md` Data Flow Matrix Phase 5 row says "Justice40 disadvantaged community overlay" but references HEPGIS in context
- **File:** `frameworks/analytical-pipeline.md`
- **Line(s):** 160–161
- **Stale claim (inline context):** Paired with the HEPGIS labeling elsewhere in the file. The matrix text itself is defensible (it says "Justice40"), but for consistency the upstream phase label should say "Phase 5: CEJST".
- **Recommended fix:** Once D11–D14 are applied, no change needed here. Pass B should verify nothing in lines 160–161 says "HEPGIS".
- **Severity:** Minor (verification only)

## D16 — `frameworks/analytical-pipeline.md` header date
- **File:** `frameworks/analytical-pipeline.md`
- **Line:** 6
- **Stale claim:** `**Date:** February 26, 2026`
- **Recommended fix:** `**Date:** April 2026 (last updated)`. Also line 272 "Created: February 26, 2026" can stay; add a "Last Updated" row.
- **Severity:** Minor

## D17 — `code/python/analysis/scoring_framework_skeleton.py` string labels say "Phase 5 (HEPGIS)" and "BLOCKED"
- **File:** `code/python/analysis/scoring_framework_skeleton.py`
- **Line(s):** 110, 114, 346, 498
- **Stale claims:**
  - L110: `"Phase 5 (HEPGIS)",`
  - L114: `"Phase 3 + Phase 5 (HEPGIS)",`
  - L346: `skeleton["equity_source"] = "Phase 3 + Phase 5 (HEPGIS)"`
  - L498: `"\n  Status: BLOCKED -- awaiting Phase 5 (HEPGIS) data\n"`
- **Reality:** Phase 5 complete using CEJST. The authoritative scoring implementation is `scoring_framework_final.py` (not skeleton). The skeleton is apparently retained for traceability.
- **Recommended fix (per user Option B):** Replace all four HEPGIS strings with CEJST equivalents:
  - `"Phase 5 (CEJST)"`
  - `"Phase 3 + Phase 5 (CEJST)"`
  - `skeleton["equity_source"] = "Phase 3 + Phase 5 (CEJST)"`
  - Replace the BLOCKED status string with `"\n  Status: Superseded by scoring_framework_final.py (Phase 5 CEJST implementation)\n"` or simply remove the BLOCKED line.
- **Severity:** Moderate (inside code but user-visible via script output)

## D18 — `scripts/generate_pipeline_diagram.py` draws Phase 5 as "HEPGIS Equity" and "PENDING"
- **File:** `scripts/generate_pipeline_diagram.py`
- **Line(s):** 259, 264
- **Stale claims:**
  - L259 (comment): `# Phase 5 — HEPGIS Equity (EQUITY) — PENDING`
  - L264 (rendered label): `draw_text(ax, x_lens[2], y_lenses + 0.15, "HEPGIS Equity", fontsize=10.5, …)`
- **Reality:** Phase 5 complete with CEJST. The rendered PNG is checked in at `docs/figures/analytical-pipeline.png`, so the pipeline diagram image itself is also drifted — see D27 below.
- **Recommended fix:** Change comment to `# Phase 5 — CEJST Equity (EQUITY) — COMPLETE` and label string to `"CEJST Equity"`. Also audit the same file for `[PENDING]` status coloring on Phases 3/4/5 and flip to complete coloring. Regenerate the PNG after edits.
- **Severity:** Critical

## D19 — `frameworks/priority-5-afdc-update-decision-framework.md` refers to HEPGIS equity as upcoming work
- **File:** `frameworks/priority-5-afdc-update-decision-framework.md`
- **Line(s):** 568, 595, 603
- **Stale claims:**
  - L568: `**Priority Ranking:** #4 in your Top 5 Quick Wins (after ZIP analysis, CTPP, HEPGIS equity, before buffer analysis)`
  - L595: `3. HEPGIS Equity Analysis (3 hrs, Score: 45)`
  - L603: `4. **Week 2, Day 1-2:** HEPGIS Equity Analysis (3 hrs) - equity layer over Jan 2026 infrastructure`
- **Reality:** This document is a pre-Phase-2 decision framework. Phase 5 was delivered with CEJST, not HEPGIS.
- **Recommended fix:** This is a historical decision framework. Two options: (a) replace "HEPGIS equity"/"HEPGIS Equity Analysis" with "CEJST equity analysis" inline per Option B, or (b) add a banner at the top of the file stating "Historical — see frameworks/analytical-pipeline.md for current status; Phase 5 delivered with CEJST, not HEPGIS" and leave HEPGIS mentions intact as historical record. **Per user's Option B instruction, default to (a): inline replacement.**
- **Severity:** Moderate

## D20 — `frameworks/afdc-data-structure-snapshot-comparison-framework.md` baseline uses 355/1,725
- **File:** `frameworks/afdc-data-structure-snapshot-comparison-framework.md`
- **Line(s):** 6, 88, 183–184, 194–195, 352–354, 376, 378, 854–860, 898
- **Stale claim:** Document frames "Current Baseline: July 2024 snapshot (355 stations, 1,725 connectors)" and repeatedly uses those counts in worked examples.
- **Reality:** Per `frameworks/README.md` §"Actual Outcome" and `AFDC-DATA-COMPARISON.md`, the "July 2024 file" was a mislabeled DCFC-only extract. The authoritative baseline is the Feb 2026 API download (1,985 stations, 6,145 connectors).
- **Recommended fix:** This is a deep methodological framework document that predates the Phase 2 finding. Recommend adding a banner at the top: `> **Historical note (Apr 2026):** This framework was written before the Phase 2 AFDC data investigation. The "July 2024 snapshot" it references was subsequently identified as a DCFC-only, public-only extract (not a full snapshot). The authoritative infrastructure baseline is now the Feb 2026 API download: 1,985 stations, 6,145 connectors. See frameworks/README.md §"Actual Outcome (Priority #5)" and data/raw/AFDC-DATA-COMPARISON.md. The methodology in this document — data structure, snapshot comparison approach, field-level classification — remains valid, but the specific counts are stale.` Do **not** rewrite the worked examples — the banner is sufficient.
- **Severity:** Moderate

## D21 — `frameworks/priority-5-stakeholder-value-integration-analysis.md` uses stale 355/1,725 and dual-snapshot framing
- **File:** `frameworks/priority-5-stakeholder-value-integration-analysis.md`
- **Line(s):** 17, 71, 156–157, 281, 338
- **Stale claim:** Treats 355 stations / 1,725 ports as the live baseline and frames "July 2024 as primary baseline" as a live recommendation.
- **Recommended fix:** Add the same historical banner as D20. Do not rewrite the document body.
- **Severity:** Moderate

## D22 — `docs/research-notes.md` pinned at Phase 1
- **File:** `docs/research-notes.md`
- **Line(s):** 5–6, 160–177, 203
- **Stale claim:** `**Last Updated:** 2026-02-21` / `**Phase:** 1 - Forecast Validation (Complete)`; "## Next Steps (Phase 2)" section lists Priority 1/2/3 tasks that were either done differently or superseded; Revision History stops at Feb 1.
- **Reality:** Phases 2–5 merged and `paper/PAPER-NOTES.md` is now the active research-notes home.
- **Recommended fix:** Either (a) update `Last Updated`, mark "Phase 1 notes (historical)", and add a pointer to `paper/PAPER-NOTES.md` as the live narrative location; or (b) delete "Next Steps (Phase 2)" section since those priorities were reframed after Feb 20. Option (a) is safer for a read-and-report pass.
- **Severity:** Moderate

## D23 — `docs/blog/BLOG-CREATION-PROTOCOL.md` stat table uses 355 stations / 1,725 connectors
- **File:** `docs/blog/BLOG-CREATION-PROTOCOL.md`
- **Line(s):** 8, 900–901, 937
- **Stale claim:** `Created: February 2026`; stat table shows `| Charging Connectors | 1,725 | Individual units |` and `| Charging Stations | 355 | Physical locations |`; `*Last updated: February 2026*`
- **Reality:** 1,985 stations / 6,145 connectors; protocol is still active per commit `bd53fd2` (Apr 2026 blog work).
- **Recommended fix:** Update the stat table to `1,985 / 6,145`. Update "Last updated" to April 2026.
- **Severity:** Moderate

## D24 — `INSTALLATION.md` and `STYLE-GUIDE.md` "Last Updated: February 2026"
- **Files:** `INSTALLATION.md` (line 151), `STYLE-GUIDE.md` (line 332)
- **Stale claim:** Both footer-stamped Feb 2026.
- **Reality:** Content of both files is stable and still accurate. Only the date is drifted.
- **Recommended fix:** Update both dates to April 2026. No other edits needed.
- **Severity:** Minor

## D25 — `frameworks/zip-code-analysis.md` and `frameworks/ctpp-analysis.md` labeled as "framework / pending data acquisition"
- **Files:** `frameworks/zip-code-analysis.md` (line 226 "Phase 2B: Full ZIP Adoption (Future - pending data acquisition)"), `frameworks/ctpp-analysis.md` (line 289 "Phase 3B: Full Integration (Future - pending better data)")
- **Stale claim:** Both treat the core Phase 3/4 work as future.
- **Reality:** Phase 3 and Phase 4 merged. The "Phase 2B/3B" sub-phases these docs refer to may genuinely be future enhancements, but the enclosing narrative treats the main work as TBD.
- **Recommended fix:** Add a banner at the top of each: `> **Status update (Apr 2026):** The core analysis described below is complete and merged (Phase 3 for ZIP / Phase 4 for CTPP). See frameworks/analytical-pipeline.md and data/processed/phase3-*.csv / phase4-*.csv. The "Phase 2B/3B" sub-sections below describe potential future extensions and remain aspirational.` Do not rewrite body.
- **Severity:** Moderate

## D26 — `frameworks/validation-analysis.md` Status line uses stale framing
- **File:** `frameworks/validation-analysis.md`
- **Line:** 3
- **Stale claim:** `**Status:** COMPLETE (February 2026)`
- **Reality:** This one is actually accurate — Phase 1 validation was complete in Feb 2026. No fix needed. Listed here only to confirm it was audited.
- **Severity:** N/A (clean)

## D27 — `docs/figures/analytical-pipeline.png` is a rendered artifact of the drifted diagram script
- **File:** `docs/figures/analytical-pipeline.png` (+ `analytical-pipeline-thumb.png`)
- **Stale claim:** The committed PNG was rendered from `scripts/generate_pipeline_diagram.py` at a point when Phases 3/4/5 were [PENDING] and Phase 5 was labeled "HEPGIS Equity".
- **Recommended fix:** After D18 is fixed, regenerate the PNG (and thumb) and commit the new artifact.
- **Severity:** Critical (visible in any rendering of `frameworks/analytical-pipeline.md` or anywhere else the diagram is embedded)

---

# Inconsistency Items (Pass C will decide)

## I1 — Two incompatible "Phase" taxonomies in the repo
- **Files:** `README.md` (lines 169–223, generic 5-phase analytics framework: exploratory/descriptive/diagnostic/predictive/prescriptive) vs. `frameworks/analytical-pipeline.md` / `frameworks/README.md` (project-specific Phase 1 Validation / Phase 2 AFDC / Phase 3 ZIP / Phase 4 CTPP / Phase 5 CEJST Equity).
- **Evidence:** `README.md` §"Phase 4: Predictive Analysis (COMPLETE)" uses "Phase 4" to mean SAS forecasting, but elsewhere in the repo "Phase 4" means workplace charging / LEHD. This will confuse any new reader.
- **Recommended action:** Pass C decides whether to (a) remove the generic taxonomy from README entirely and refer to the project-phase taxonomy, or (b) rename the generic sections to "Analytical Approach" without using the word "Phase". Report only.

## I2 — Commit prefix convention drift: `[EVPULS]` / `[EVPULSE]` / `[EV-PULSE]`
- **Files:** `CONTRIBUTING.md` line 37 documents `[EVPULS]` (the legacy typo-shortened form); recent commits use `[EVPULSE]` dominantly, with `[EV-PULSE]` appearing in 2 recent commits.
- **Evidence:** `git log --oneline -50` shows all Phase 3, 4, 5 work as `[EVPULSE]`; only 2 commits use `[EV-PULSE]`.
- **Recommended action:** Pass C decides canonical form. Recommendation: update `CONTRIBUTING.md` to `[EVPULSE]` and stop using `[EV-PULSE]` and the legacy `[EVPULS]`.

## I3 — "5 phases" overloaded
- **Files:** `README.md` line 12 ("5-phase analytics framework—exploratory, descriptive, diagnostic, predictive, and prescriptive"); `frameworks/README.md` ("5 phases" meaning Validation/AFDC/ZIP/CTPP/Equity).
- **Evidence:** Same word, two meanings. Related to I1.
- **Recommended action:** Resolve via I1.

## I4 — `references/data-sources.md` still lists the old 355/1,725 extract as live reference
- **File:** `references/data-sources.md` line 19
- **Evidence:** Describes old file as "Retained for reference only" — this is actually accurate. Included here because Pass B should double-check that the rest of `references/data-sources.md` includes the new AFDC, CEJST, LEHD, and ACS datasets that were added in Phases 2–5. I did not do a full field-level audit of that file.
- **Recommended action:** Pass B (or Pass C) verify `references/data-sources.md` has entries for CEJST Justice40, LEHD/LODES, ACS income/tenure, Census tracts 2010, ZCTA boundaries, and county boundaries. If any are missing, that's a documentation-completeness gap (not drift).

## I5 — `PAPER-NOTES.md` TODO markers for fig-43 and VIF check
- **File:** `paper/PAPER-NOTES.md` lines 547, 555
- **Evidence:** Explicit `TODO:` markers. Recent commit `0f8324b` added the VIF action plan; commit `1546560` mentions "add scoring figure TODO". These are live TODOs, not stale ones.
- **Recommended action:** Leave alone. Report only.

## I6 — `docs/blog/consultation.md` "Status: Awaiting panel responses"
- **File:** `docs/blog/consultation.md` line 4
- **Evidence:** This file may or may not be live. Commit `2e9b3cb` moved SEINFORMS consultation to the BIDA 670 repo; this consultation.md may be an orphan.
- **Recommended action:** Pass C verify whether this blog consultation is still active or should be marked archived.

## I7 — Missing documentation for the NEVI scoring framework delivery
- **Files:** The scoring framework is delivered (commits `b96a186`, `1ff3f59`, `6a45635`) and is the capstone deliverable per Dr. Al-Ghandour's feedback, but there is no dedicated doc describing the final equation, weights used, sensitivity results, and ranked-county output. `frameworks/README.md` §"Phase 5: Prescriptive Scoring Framework" describes the *plan*. `paper/PAPER-NOTES.md` has inline notes. There is no single "here is what we delivered" scoring doc.
- **Recommended action:** Pass C decides whether a standalone `frameworks/nevi-scoring-framework.md` or `paper/scoring-framework-results.md` doc is warranted. Completeness, not drift.

---

# Files Audited (Full List)

| File | Status |
|---|---|
| `README.md` | has-drift (Critical) |
| `PROJECT-BRIEF.md` | has-drift (Critical) |
| `PROJECT-EXPLANATION.md` | has-drift (Critical) |
| `QUICK-REFERENCE.md` | clean (not read in depth — small file, no obvious drift indicators in grep) |
| `INSTALLATION.md` | has-drift (Minor, date only) |
| `CONTRIBUTING.md` | has-inconsistency (I2) |
| `STYLE-GUIDE.md` | has-drift (Minor, date only) |
| `NOTICE.md` | clean (license notice, no drift surface) |
| `frameworks/README.md` | has-drift (Critical) |
| `frameworks/analytical-pipeline.md` | has-drift (Critical) |
| `frameworks/afdc-api-analysis.md` | clean (small file, no status drift) |
| `frameworks/afdc-data-structure-snapshot-comparison-framework.md` | has-drift (Moderate — historical doc, banner recommended) |
| `frameworks/ctpp-analysis.md` | has-drift (Moderate — banner recommended) |
| `frameworks/priority-5-afdc-update-decision-framework.md` | has-drift (Moderate, HEPGIS mentions) |
| `frameworks/priority-5-stakeholder-value-integration-analysis.md` | has-drift (Moderate — banner recommended) |
| `frameworks/proposed-project-titles.md` | clean (not audited in depth) |
| `frameworks/validation-analysis.md` | clean (D26 — already accurate) |
| `frameworks/zip-code-analysis.md` | has-drift (Moderate — banner recommended) |
| `paper/README.md` | clean |
| `paper/PAPER-NOTES.md` | has-inconsistency (I5 — live TODOs, not stale) |
| `paper/vif-scoring-framework-action-plan.md` | clean (added Apr 9 2026) |
| `docs/research-notes.md` | has-drift (Moderate) |
| `docs/blog/BLOG-CREATION-PROTOCOL.md` | has-drift (Moderate) |
| `docs/blog/consultation.md` | has-inconsistency (I6) |
| `data/README.md` | clean (not audited in depth; Feb 21 stamp is near-current) |
| `data/processed/DATA-DICTIONARY.md` | not audited (Pass B should spot-check for stale column sets from pre-Phase-5) |
| `data/raw/AFDC-DATA-COMPARISON.md` | clean — this is the canonical "here's what the old file really was" doc |
| `references/data-sources.md` | has-inconsistency (I4 — verify completeness) |
| `code/README.md` | clean (covers data-acquisition / data-cleaning / analysis / blog; does not enumerate Phase 3–5 analysis scripts but this is acceptable as an overview) |
| `output/README.md` | not audited in depth |
| `code/python/analysis/scoring_framework_skeleton.py` | has-drift (D17) |
| `scripts/generate_pipeline_diagram.py` | has-drift (D18) |
| `docs/figures/analytical-pipeline.png` | has-drift (D27 — rendered artifact) |

---

# Notes for Pass B

## Canonical strings to use

- **Commit prefix:** `[EVPULSE]` (see I2). Most-used on last 50 commits.
- **Infrastructure baseline:** `1,985 stations, 6,145 connectors (L1/L2/DCFC, all access types, 267 cities, 358 ZIPs, Feb 2026 API download)`. Old `355 / 1,725` numbers should only appear inside historical banners or the AFDC-DATA-COMPARISON.md doc.
- **Phase 5 name:** "Phase 5 — CEJST Equity Analysis" (NOT "HEPGIS Equity Analysis"). Data source citation: "CEJST tract-level Justice40 designations".
- **Phase count / status:** "All 5 core phases complete (Phase 1 Validation, Phase 2 AFDC Update, Phase 3 ZIP Analysis, Phase 4 Workplace Charging / LEHD, Phase 5 CEJST Equity)"

## HEPGIS replacement summary (Option B)

HEPGIS appears in **5 files** across **16 inline references**:

1. `frameworks/README.md` — 3 references (lines 50, 65, 128–131 block, 136 block body)
2. `frameworks/analytical-pipeline.md` — 4 references (lines 65, 137, 220, 252)
3. `frameworks/priority-5-afdc-update-decision-framework.md` — 3 references (lines 568, 595, 603)
4. `code/python/analysis/scoring_framework_skeleton.py` — 4 references (lines 110, 114, 346, 498)
5. `scripts/generate_pipeline_diagram.py` — 2 references (lines 259, 264) + rendered PNG at `docs/figures/analytical-pipeline.png`

Per user's Option B: replace each inline mention with the CEJST equivalent. Do **not** preserve as historical note. The one exception is `frameworks/priority-5-afdc-update-decision-framework.md`, which is itself a historical decision framework — Pass B should still do inline replacement there per instruction, but this is the closest case to a "maybe preserve" call.

Line 136 of `frameworks/README.md` says "What it is: ArcGIS map of NCDOT's planned NEVI station deployments along Alternative Fuel Corridors (AFCs)". This describes the **NCDOT NEVI Mapping Tool** (Phase 7, optional), which genuinely does use Alternative Fuel Corridors — this is **not** the HEPGIS drift, this is about NCDOT's own AFC-aligned tool. Pass B should **leave this alone**.

## Pass B sizing estimate

- **Files needing edits (documentation):** 13 markdown files
  - 5 Critical: `README.md`, `PROJECT-BRIEF.md`, `PROJECT-EXPLANATION.md`, `frameworks/README.md`, `frameworks/analytical-pipeline.md`
  - 6 Moderate: 4 frameworks docs (banners), `docs/research-notes.md`, `docs/blog/BLOG-CREATION-PROTOCOL.md`
  - 2 Minor: `INSTALLATION.md`, `STYLE-GUIDE.md` (date stamps only)
- **Files needing edits (code):** 2 Python files + regeneration of 1 PNG
  - `code/python/analysis/scoring_framework_skeleton.py` (4 string replacements)
  - `scripts/generate_pipeline_diagram.py` (1 comment + 1 label + status coloring for Phases 3/4/5) → regenerate `docs/figures/analytical-pipeline.png` + thumb
- **Approximate edit volume:**
  - README.md: ~20–40 lines touched (status block, infra counts, optionally Phase taxonomy rewrite)
  - PROJECT-BRIEF.md: either full rewrite (~100 lines) or historical banner (~5 lines) + inline count replacements (~6 lines)
  - PROJECT-EXPLANATION.md: either full rewrite (~200 lines) or banner (~5 lines) + inline count replacements (~10 lines)
  - frameworks/README.md: ~15 lines touched (Phase 5 row, Equity_Score row, Priority #5 section, Status lines)
  - frameworks/analytical-pipeline.md: ~25 lines touched (diagram labels, Phase Summary table, Pending → Complete section, Paper Alignment table, date)
  - 4 framework banners: ~5 lines each = ~20 lines
  - scoring_framework_skeleton.py: 4 string replacements
  - generate_pipeline_diagram.py: 2 string edits + Pass B judgment on phase-status coloring
  - **Total estimated edit volume:** 150–300 lines across 13 docs + 2 code files, plus 1 PNG regeneration.
- **Estimated Pass B effort:** 60–90 minutes of focused editing if Pass B takes the banner approach for PROJECT-BRIEF and PROJECT-EXPLANATION, or 2–3 hours if Pass B rewrites those two docs in full.

## Watch-outs for Pass B

1. **Don't conflate the two "Phase" taxonomies.** README's Phase 4 = SAS Predictive; frameworks' Phase 4 = CTPP Workplace. Pass B must either pick one or be explicit about which is being used in each context.
2. **Don't delete historical AFDC data comparison content.** The 355/1,725 numbers are legitimately part of the Phase 2 narrative (the "we discovered the old file was a DCFC-only extract" finding). They should live in `AFDC-DATA-COMPARISON.md` and be referenced from banners in the affected framework docs.
3. **Regenerate the pipeline diagram PNG** after editing `generate_pipeline_diagram.py`. If Pass B edits the Python but skips the regen, the drift persists.
4. **`frameworks/README.md` line 136 mentions "Alternative Fuel Corridors (AFCs)"** in the context of the NCDOT NEVI Mapping Tool (Phase 7). This is NOT HEPGIS drift — leave it alone.
5. **The dual-snapshot narrative** (in PROJECT-EXPLANATION.md lines 97–101, 149; PROJECT-BRIEF.md lines 14, 44, 78) is a defunct analytical framing that was abandoned when the July 2024 file was found to be a DCFC-only extract. Pass B should either remove these passages or caveat them — don't leave readers thinking a dual-snapshot growth analysis is in the paper.
