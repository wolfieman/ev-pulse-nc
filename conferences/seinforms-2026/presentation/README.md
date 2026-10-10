# SEINFORMS 2026 — Presentation Plan

**Talk:** in person, SEINFORMS 2026, Myrtle Beach, SC. **Thursday Oct 15, 9:55–10:17am (22-min slot), Arcadian 1-2**, 2nd of 3 in "AI, BA, Statistics, & Tech Mgmt - Session 2" (chair: Prof. Jae-Dong Hong).
**Target:** under 15 minutes of talk plus Q&A (15 talk slides, 9 backup slides). Deck v6 notes: 12:52 at 150 wpm, about 14:10–14:50 live.
**Deadline:** deck and rehearsal complete by Thu Oct 8, Fri Oct 9 at the latest.
**Working rule:** steps run in order, as fast as they go, not tied to calendar days.

Locked slide-by-slide content lives in [`deck-outline.md`](deck-outline.md).

---

## Sources

The deck is built from three bases: the shortened SEINFORMS manuscript, the
MBA Showcase competition deck, and the BIDA-670 capstone deck. The full
100+ page capstone paper (`../../../paper/manuscript.md`; PDF
`../../../paper/ev-pulse-nc-sanyer-paper.pdf`) is the parent of all three and
settles any disagreement between them.

| Source | Role |
|---|---|
| SEINFORMS paper (`../output/ev-pulse-nc-seinforms-2026.pdf`, 31 pp; source `../seinforms_manuscript.md`) | Source of truth for every number, claim, and figure |
| MBA Showcase deck (`../../../competitions/mba-showcase-2026/`, 14 slides, 2nd place) | Storyline: tight and audience-friendly |
| BIDA-670 capstone deck (`../../../paper/ev-pulse-nc-sanyer-presentation.pdf`, 25 slides, presented Spring 2026) | Methods depth: Chow break, Theil deep dive, scoring formula, sensitivity, archetypes with the empty quadrant, Justice40 framing, direction-of-bias limitations |

Approach: keep the showcase storyline, take the methods slides from the capstone
deck, and check every number against the SEINFORMS paper.

## Decisions (locked)

**Numbers rule (owner, 2026-10-06).** Every number on a slide is quoted from
the SEINFORMS manuscript as written. Nothing is recalculated, and nothing is
invented. Where the paper states a figure two ways, the deck uses the abstract's
version (e.g., 73% of BEVs in the top 10 counties) and sticks to it.

**a. Deck-vs-paper differences.** All three sources come from the same capstone
manuscript; the differences are slips in the showcase slides, fixed in the new
deck. Slips inside the SEINFORMS manuscript are reported to the owner in step 3
and changed only with the owner's approval.
Full list: the corrections log at the top of [`deck-outline.md`](deck-outline.md).

- Gini: 0.805 is county-level BEV *ownership* concentration; 0.566 is ZIP-level
  *charging* inequality. The deck uses each for what it measures.
- Stations in Justice40 tracts: **24.5%** (296 of 1,210), not 24.9%.
- "47.6% of infrastructure added in 2024–25": not in the paper; dropped.

**b. Score-construction slide.** No new slide. The scoring slide combines the
capstone formula slide (weights, rationale, VIF 1.41) with one added line on
min-max normalization; the rankings slide carries the three sensitivity tests.

**c. Justice40 / NEVI.** Use the paper's framing: the 0.40 equity weight is an
analytical anchor reflecting the Justice40 target under EO 14008, rescinded
January 2025. The showcase line "Federal law requires 40%" is dropped. A short
check of NEVI's current status feeds the Q&A bank. The "first additive Theil-T
decomposition" claim gets a prepared answer (prior work, e.g. Choi, Xu & Jiao
2025, uses Theil as a scalar; this study uses the between/within split as a
design input).

## Deck structure

Current deck: v6 (2026-10-10). Slide-by-slide text and notes are in
[`deck-outline.md`](deck-outline.md) ("Current deck (v6)").

| # | Slide | Visual |
|---|---|---|
| 1 | Title | photo |
| 2 | $109 Million. 100 Counties. No Data-Driven County Ranking. | stat cards |
| 3 | Five Questions Drive the Work | question list |
| 4 | The BEV Fleet Grew 1,727% Since 2018. Ports Have Not Kept Pace. | stat cards |
| 5 | Five Analytical Phases, One Scoring Framework (PHASE n · Qn) | phase cards |
| 6 | Forecasts Hold Out of Sample, and Adoption Accelerated After 2022 | Fig 44 (talk version) |
| 7 | A 250-Fold Charging Gap Inside One County | Fig 24 + callouts |
| 8 | 84.5% of Charging Inequality Is Within Counties | native Theil bar |
| 9 | Commuters Shift Demand Toward Employment Centers | native commuter bar |
| 10 | Roughly Proportional Overall, with Strong County-by-County Variation | native tiles + dot plot |
| 11 | Three Pillars, One Score | formula + pillar cards |
| 12 | Top 3: Union, Mecklenburg, Guilford | native Table 2 bar |
| 13 | Three County Archetypes | native equity × utilization chart |
| 14 | Contributions and Limitations | two cards |
| 15 | A Ranking to Inform NCDOT's Decisions, and What Comes Next | takeaways ①–③ + contacts + QR |
| B1–B9 | Theil detail · crosswalk validation · Table 2 · data sources · Fig 36 · Fig 42 · Fig 43 · Tier 2 ZIP targeting · glossary | |

## Timing

Speaker notes total 1,938 words: 12:52 at 150 wpm, about 14:10–14:50 at live
pace (10–15% slower). No slides cut (owner, 2026-10-10); slides 5, 9 and 10
carry a "(Cut candidate…)" note if a timed rehearsal runs long. Longest notes:
slide 6 (210 words), slide 10 (~200).

## Steps

Corrections come first: the bases are cleaned before the deck is built on them.

| # | Step | Owner | Status |
|---|---|---|---|
| 1 | Lock decisions (sources, a/b/c, ~15-min target) | Owner | ✅ done |
| 2 | Draft outline: per-slide text, numbers tied to paper sections, figure, source slide, draft speaker notes | Claude | ✅ done — [`deck-outline.md`](deck-outline.md) |
| 3 | **Corrections pass** | | |
| 3b | Independent read-only audit (fresh agent): manuscript internal consistency; outline, showcase deck, and BIDA-670 deck checked number by number against the manuscript; condensation drift and tiebreaks against the full paper | Claude | ✅ done |
| 3c | Report findings to the owner; **no change to the manuscript, decks, or outline without owner approval** | Claude → Owner | ✅ done — owner ruling: inconsistencies are minor; the deck uses the SEINFORMS manuscript as written, no recalculation, spring-26 materials unchanged |
| 3d | Apply only the approved fixes | Claude | ✅ done — three outline slips fixed (slide 12 headline and source, slide 8 notes, slide 11 source note); manuscript untouched |
| 4 | *(moved to step 9b: the current-status check now runs on the whole final deck)* | | — |
| 5 | Build the `.pptx` from the corrected outline (pptxgenjs, `src/paper/seinforms_deck/`; showcase / BIDA-670 look, light, paper figures as-is, speaker notes); save to Drive | Claude | ✅ v4 in Drive: `01 Projects/seinforms-2026/ev-pulse-nc-seinforms-2026-deck-v4.pptx` (+ preview PDF); v2 added the research-questions slide, v3 the faculty-advisor line, v4 the closing-slide contacts and repo QR code |
| 6 | Review in PowerPoint (Win 11 / Microsoft 365) | Owner | ✅ owner is happy with the deck as is |
| 7 | Import into Gamma, compare with the built deck, choose per slide | Owner + Claude | — skipped (owner is happy with the deck as is) |
| 8 | Retouch the chosen version in PowerPoint | Owner | — skipped (no Gamma version) |
| 9 | Final number check: a fresh agent compares the exported PDF against the paper | Claude | ⬜ |
| 9b | Current-status check on the whole final deck | Claude → Owner | — not needed (owner ruling: only if an agent changes slide content) |
| 10 | Rehearsal: timed run-throughs; Q&A bank (~15 questions); mock Q&A with a skeptical-reviewer persona | Owner + Claude | ⬜ |
| 11 | Figure re-render | Claude | — not needed (owner: the figures look great) |
| 12 | Freeze: PDF committed here, `.pptx` in Drive, backups (USB + PDF) | Owner + Claude | 🟡 PDF committed ([`ev-pulse-nc-seinforms-2026-sanyer-plus-backup-slides.pdf`](ev-pulse-nc-seinforms-2026-sanyer-plus-backup-slides.pdf), 24 slides, v6); PPTX + PDF in Drive; USB copy pending |
| 13 | **Speaker notes pass** (delivery-ready, per the owner's humanization protocol) and add Dr. Burcu Adivar as Faculty Adviser on the title slide (v5) | Owner + Claude | ✅ done — v5 slide-by-slide review (all 15 slides), Dr. Adivar added |
| 13b | Independent whole-deck review (numbers, flow, Tufte/Knaflic, tell-them) and owner-approved fixes in six groups | Claude → Owner | ✅ done — v6 delivered: Drive root holds `…-sanyer-upload.pptx` (15 slides, sent 2026-10-10) and `…-sanyer-plus-backup-slides.pptx` (24 slides); v6 presenter set in `presentation/legacy/`; report in Drive `notes/review-whole-deck-2026-10-10.md` |
| 13c | Lock slide 15 | Owner | ✅ done — locked as in v6 (takeaways ①–③) |
| 14 | Send the final PPTX to Dr. Al-Ghandour, who uploads it to Ex Ordo (accepts ppt/pptx/key only) | Owner | ⬜ Fri/Sat Oct 9–10 |

Q&A bank topics (step 10): Chow break and underprediction, the "first" claim, why
these weights, why min-max normalization, the Justice40 rescission, the CEJST
archive, the LODES 2021 vintage, why the top 10 counties and not all 100.

## File policy

- The editable `.pptx` lives in Google Drive (also the Linux ↔ Windows handoff)
  and is never committed.
- The PDF export is the tracked artifact, committed in this folder at step 9.

## Coordination with Dr. Al-Ghandour (as of 2026-10-08)

His requests, and their status:

| Request | Status |
|---|---|
| Presentation as PPTX (Ex Ordo accepts ppt/pptx/key only; upload extended to Fri/Sat) | ⬜ owner sends the final PPTX Fri/Sat; he uploads |
| Shorten the owner's part so he can present a portion | ⬜ owner prefers not to cut unless necessary; to settle at the meeting |
| Presenter bio | ✅ approved text in [`presenter-bio.md`](presenter-bio.md), sent to him; he enters it in Ex Ordo (the owner's account cannot) |
| Add Dr. Burcu Adivar as Faculty Adviser | ⬜ owner agreed; added during the speaker-notes pass (v5) |
| Register as a student | ⬜ owner registers Fri/Sat ($145) |
| Travel pre-approval | ✅ under FSU Policy 707 he files it; the owner sent him the full packet (Travel Plan, Forms A–B pre-filled, Form C signed) on 2026-10-08 |
| Meeting | ⬜ Teams invite for Thu Oct 8 after 9:15 PM (awaiting his reply) |

Travel documents and reservations are kept in Google Drive
(`01 Projects/seinforms-2026/travel/`), not in git.

## Post-conference fixes (logged, not done before the talk)

Owner ruling: spring-26 materials stay unchanged until after the conference.

| # | Item | Where | Fix |
|---|---|---|---|
| 1 | LODES vintage described as "LODES8, 2021 (most recent public release)", but Census had posted NC 2022 (Oct 3, 2024) and 2023 (Dec 3, 2025) before the Feb 2026 pull | `data/README.md`, `data/DATA-DICTIONARY.md`, `frameworks/README.md` | Reword to "LODES8, 2021 vintage; 2022 and 2023 releases available" (results unaffected: rankings are invariant to the remote-work multiplier, paper §9.2) |
| 2 | Paper Fig 45 (archetype scatter): county labels are offset from their bubbles: "Mecklenburg" sits on New Hanover (0.607, 0.071), "New Hanover" on Durham, "Durham" on Buncombe; Mecklenburg's bubble is unlabeled, Guilford's is hidden behind the size legend, and the equity-driven quadrant label is missing | `output/figures/fig-45-equity-utilization-archetypes.png` (`src/analysis/phase5_fig45_archetype_scatter.py`); paper §7.3 | Fix the label placement and legend position, re-render, rebuild the paper PDF. The talk uses a native redraw from Table 2 (slide 13) |

