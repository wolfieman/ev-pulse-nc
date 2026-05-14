---
title: "EV Pulse NC — Tonal Drift Audit (B3)"
auditor: "Tonal Drift Auditor"
audit_date: 2026-04-09
scope: "Re-audit of Pass A clean files + verification of Pass B/B-prime edited files for tonal drift"
output_pass: "B3 — read-only audit"
---

# Executive Summary

- Files scanned: 27 markdown files (all in-scope repo `.md` files outside `.venv/`, `build/`, and the Pass A drift report itself)
- Files with tonal drift: 3
- Total tonal drift items: 4
- Severity breakdown: 1 high, 1 medium, 2 low

The repo is overwhelmingly tonally clean after Pass B/B-prime. The surviving drift is concentrated in two legacy Phase-1-era framework docs (`frameworks/validation-analysis.md`, `frameworks/proposed-project-titles.md`) that still carry "Next Steps (Phase 2)" / "Next Steps" sections describing work that is now merged to `main`. The top-level `README.md` uses an infinitive goal list that reads slightly aspirational but is defensible as a project-scope description; flagged low.

Note: `docs/research-notes.md` also has a "Next Steps (Phase 2)" section, but the file's H1, preamble, and date line already mark it as "Historical — Phase 1" and explicitly point readers to `paper/PAPER-NOTES.md` as the live narrative. That framing neutralizes the tonal drift, so it is **not** flagged. It is called out in Notes below as a judgment call.

# Tonal Drift Items

## T1 — `frameworks/validation-analysis.md` "Next Steps (Phase 2)" section describes completed work as upcoming

- **File:** `frameworks/validation-analysis.md`
- **Line(s):** 108-114
- **Sentence (verbatim):**
  > "## Next Steps (Phase 2)
  >
  > Based on validation findings, Phase 2 should prioritize:
  >
  > 1. **Diagnostic Analysis:** Root cause analysis of underprediction (IRA effects, Tesla pricing, infrastructure expansion)
  > 2. **Prescriptive Recommendations:** Policy recommendations with bias-corrected forecasts
  > 3. **Remaining Priorities:** ZIP code analysis (#2), CTPP workplace charging (#3), AFDC update (#5)"
- **Why it's tonal drift:** The section describes Phases 2-5 as "should prioritize" / "remaining priorities." All five phases are merged. A current-state reader arriving at this doc is told Phase 3/4/5 are upcoming priorities. Unlike `docs/research-notes.md`, this file is NOT marked historical — its H1 is "Validation Analysis Framework" with no historical-only caveat, so it reads as live.
- **Recommended fix:** Replace the section with something like: "## Follow-On Phases (Delivered)" and a one-paragraph pointer: "Phase 2 (AFDC infrastructure update), Phase 3 (ZIP code analysis with Theil decomposition), Phase 4 (LEHD LODES workplace charging), and Phase 5 (CEJST equity) were delivered and merged. See `frameworks/analytical-pipeline.md` for the completed pipeline and `paper/PAPER-NOTES.md` for the live narrative." Alternatively, add a "Historical — Phase 1 framework" banner to the top of the file matching the `research-notes.md` treatment.
- **Severity:** high

## T2 — `frameworks/proposed-project-titles.md` "Next Steps" describes project as pre-kickoff

- **File:** `frameworks/proposed-project-titles.md`
- **Line(s):** 106-111
- **Sentence (verbatim):**
  > "## Next Steps
  >
  > 1. **Professor Feedback:** Submit titles for instructor input on scope/focus preferences
  > 2. **Abstract Development:** Draft 250-word abstract for selected title
  > 3. **Methodology Section:** Link title to analytical framework documentation
  > 4. **Deliverable Mapping:** Ensure project outputs align with title promises"
- **Why it's tonal drift:** This is a title-brainstorm artifact from before the project title was locked and before the paper narrative existed. All four "next steps" are completed: title is selected, abstract exists in `paper/PAPER-NOTES.md`, methodology is linked in every phase doc, and deliverables are mapped in `frameworks/analytical-pipeline.md`. A current reader is given pre-kickoff planning as if it's the active to-do list.
- **Recommended fix:** Either (a) add a "Historical — pre-kickoff title brainstorm" banner at the top of the file and leave the "Next Steps" section as-is (cheapest fix), or (b) delete the "Next Steps" section and replace with a "Selected Title" pointer to wherever the final paper title lives. Option (a) matches the `research-notes.md` treatment and is the lowest-risk read-and-report recommendation.
- **Severity:** medium

## T3 — `README.md` project objectives stated as infinitive goals rather than delivered results

- **File:** `README.md`
- **Line(s):** 12-18
- **Sentence (verbatim):**
  > "This project applies the standard 5-part analytics framework — exploratory, descriptive, diagnostic, predictive, and prescriptive — across the project's five merged extensions (see `frameworks/analytical-pipeline.md` for the extension-by-extension pipeline) to:
  >
  > 1. **Quantify infrastructure gaps** at the county level across North Carolina
  > 2. **Forecast future demand** using time series models
  > 3. **Identify high-priority deployment zones** through gap severity analysis
  > 4. **Optimize investment strategies** for the $109M NEVI Formula Program funding"
- **Why it's tonal drift:** The "to: Quantify.../Forecast.../Identify.../Optimize..." infinitive list frames these as project aims. The preamble does say "five merged extensions," which anchors the reader in completed state, so this is borderline — but a pure current-state rewrite would read "quantifies / forecasts / identifies / optimizes." Low severity because the surrounding Key Findings section (lines 21-45) immediately delivers the numerical results, so the infinitive list does not leave a reader confused about completion status.
- **Recommended fix:** Change the four bullets to finite-verb present tense: "**Quantifies** infrastructure gaps...", "**Forecasts** BEV demand...", "**Identifies** high-priority deployment zones...", "**Optimizes** investment strategies for the $109M NEVI funding." Or leave as-is — it's acceptable README idiom.
- **Severity:** low

## T4 — `README.md` line 199 "Forecast future BEV adoption" as Predictive Analysis objective

- **File:** `README.md`
- **Line(s):** 199
- **Sentence (verbatim):** "- **Objective:** Forecast future BEV adoption to anticipate infrastructure needs"
- **Why it's tonal drift:** Same pattern as T3 — infinitive "Forecast" inside an "Objective:" field. The surrounding lines 200-213 list validation results, MAPE, figures, so the reader knows the work is done. Low severity.
- **Recommended fix:** Either change "Objective" labels across the Phase 1-5 sections (lines 169-225) to past-tense "What it did" / "Results," or leave alone as a README idiom. No semantic confusion.
- **Severity:** low

# Files Scanned (Full List)

| File | Status | Notes |
|---|---|---|
| `README.md` | drift (T3, T4) | Low-severity infinitive/objective phrasing; Key Findings section anchors the reader in completion |
| `PROJECT-BRIEF.md` | clean | Single "will" on line 48 is inside Future Directions (Phase 7), legitimate |
| `PROJECT-EXPLANATION.md` | clean | Line 36 "future work can refine" refers to post-capstone roadmap; line 170 same. All Phase 1-5 prose is past/present tense |
| `QUICK-REFERENCE.md` | clean | No future-tense markers for completed phases |
| `CONTRIBUTING.md` | clean | No tonal drift |
| `NOTICE.md` | clean | License only |
| `INSTALLATION.md` | clean | Single "planning" hit is a `mkdir` path example |
| `STYLE-GUIDE.md` | clean | No drift |
| `paper/README.md` | clean | Only "Future Study" reference is a legitimate report section heading |
| `paper/PAPER-NOTES.md` | clean (within scope) | Live TODOs for fig-43 and VIF check (I5) are legitimate per Pass A carve-out; "future work" mentions on lines 460, 533, 536 all refer to post-capstone extensions in a limitations context, which is allowed |
| `paper/vif-scoring-framework-action-plan.md` | clean | Future-tense is appropriate — this is an action plan for unimplemented work |
| `frameworks/README.md` | clean | Phase 6/7 "Future Direction" rows are legitimate; "planned" hits refer to NCDOT's own planned deployments (Phase 7 context) |
| `frameworks/analytical-pipeline.md` | clean | Phase 5 labeled [COMPLETE]; "will" on line 38 is inside a rhetorical question the Phase 1 forecasting work already answered — borderline, but defensible |
| `frameworks/afdc-dataset-reference.md` | clean | Line 59 "No additional refreshes are planned" is a deliberate current-state statement |
| `frameworks/afdc-data-structure.md` | clean | "planned" hits refer to AFDC `status_code=P` field definition |
| `frameworks/afdc-api-analysis.md` | clean | "planners" refers to stakeholder group, not drift |
| `frameworks/stakeholder-value-analysis.md` | clean | "would relieve" on line 40 is a conditional in a limitations/opportunity context, allowed |
| `frameworks/validation-analysis.md` | **drift (T1, high)** | Phase-1-era "Next Steps (Phase 2)" section survives without historical banner |
| `frameworks/proposed-project-titles.md` | **drift (T2, medium)** | Pre-kickoff "Next Steps" brainstorm artifact survives without historical banner |
| `frameworks/zip-code-analysis.md` | clean | Rewritten to "delivered framework" tone |
| `frameworks/ctpp-analysis.md` | clean | Rewritten to "delivered framework" tone |
| `data/README.md` | clean | "May be deprecated in future cleanup" is a legitimate forward-looking note about a deprecated file |
| `data/processed/DATA-DICTIONARY.md` | clean | Data dictionary — field descriptions only |
| `data/raw/AFDC-DATA-COMPARISON.md` | clean | Canonical comparison doc |
| `code/README.md` | clean | Script usage docs |
| `output/README.md` | clean | Output directory index |
| `references/data-sources.md` | clean | Data source table |
| `docs/research-notes.md` | clean (judgment call) | "Next Steps (Phase 2)" section at line 160 is legitimate because the file H1, preamble, and date line all mark it as "Historical — Phase 1" and point readers to `paper/PAPER-NOTES.md`. See Notes below. |
| `docs/blog/consultation.md` | clean | Future-tense "will" on lines 142, 208 are inside example blog-post drafts and commentary about reader reactions, not project-status claims |
| `docs/blog/BLOG-CREATION-PROTOCOL.md` | clean | Protocol / how-to doc; "aim for <30% AI probability" is a GPTZero target, "pending" on line 536 is part of a sample-post bullet about NEVI funding context |
| `docs/documentation-drift-report.md` | excluded | Pass A report, out of scope |

# Notes

**Judgment call 1 — `docs/research-notes.md` "Next Steps (Phase 2)".** I did NOT flag this despite it matching every surface pattern for drift, because the file's own H1 is "Research Notes (Historical — Phase 1)" and its preamble + "Last Updated" line explicitly tell the reader: "This file is preserved as a historical record... The live research-notes location for the current paper narrative (Phases 2–5) is `paper/PAPER-NOTES.md`." That framing neutralizes the tonal drift: the "Next Steps" section is understood as "what Phase 1 thought Phase 2 should do, preserved for the record." By contrast, `frameworks/validation-analysis.md` has no such banner, which is why T1 is flagged at high severity and T2 (`proposed-project-titles.md`) at medium — the cheapest fix for both is to add the same historical-banner treatment.

**Judgment call 2 — `README.md` infinitive goal list (T3, T4).** I flagged these at low severity rather than waving them through because the auditor brief specifically names "to: Quantify.../Forecast.../Identify.../Optimize..." style as a potential signal. That said, this is standard README idiom and the immediately-following Key Findings section delivers concrete numbers, so there is zero risk of reader confusion. A cleanup pass can touch these or skip them without any cost to the repo's credibility.

**Judgment call 3 — `frameworks/analytical-pipeline.md` line 38 "How many EVs will NC have?".** This is a rhetorical question the Phase 1 forecasting work answered. The "will" is correct English inside a forecasting question ("how many X will there be?") and the box label immediately above says `[COMPLETE]`. Not flagged.

**Judgment call 4 — `PROJECT-BRIEF.md` and `PROJECT-EXPLANATION.md` "future work can refine" / "post-capstone roadmap" mentions.** These are inside explicit Future Directions / limitations framing and describe the Phase 6/7 deferred enhancements. Legitimate.

**Estimated follow-up cleanup effort:** **S (small)** — the fix for T1 and T2 is a single "Historical — Phase 1 framework" / "Historical — pre-kickoff brainstorm" banner at the top of each file (2 files, ~4 lines each). T3 and T4 are optional stylistic touch-ups on `README.md` (one paragraph and one line). Total edit surface: under 30 lines across 3 files, single commit.
