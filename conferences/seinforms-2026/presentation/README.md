# SEINFORMS 2026 — Presentation Plan

**Talk:** in person, SEINFORMS 2026, Myrtle Beach, SC (Oct 15–16, 2026).
**Target:** ~15.5 minutes of talk plus Q&A (15 core slides, 4 backup slides).
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

| # | Slide | Main source | Paper figure |
|---|---|---|---|
| 1 | Title | — | |
| 2 | $109M, 100 counties, no framework | Showcase | |
| 2a | Research questions (deck slide 3; added at owner request) | Capstone s5 + §1.3 | |
| 3 | Demand signal | Showcase / Capstone | |
| 4 | Five-phase pipeline + public data | Capstone | |
| 5 | Forecast validation: MAPE, underprediction, Chow break | Capstone | Fig 44 |
| 6 | Infrastructure gap: zero-station ZIPs, 250× within Mecklenburg | Showcase | Fig 24 |
| 7 | 84.5% of inequality is within counties (Theil) | Capstone | Fig 33 |
| 8 | Workplace demand | New | Fig 36 |
| 9 | Justice40 overlay (paper framing) | Capstone | Fig 42 |
| 10 | Scoring framework + normalization + VIF | Capstone + Showcase | |
| 11 | Rankings + three sensitivity tests | Showcase / Capstone | Fig 43 |
| 12 | Archetypes + empty quadrant | Capstone | Fig 45 |
| 13 | Contributions + limitations (direction of bias) | Capstone | |
| 14 | Implications, future work, thank you | Showcase | |
| B1–B4 | Backup: Theil math, 23/23 crosswalk validation, sensitivity table, data sources | Capstone | |

## Timing

Pace from earlier talks: capstone defense 25 slides in 23.2 min (~56 s/slide);
showcase 14 slides in ~15 min (~64 s/slide).

| Slide type | Slides | Time each | Subtotal |
|---|---|---|---|
| Title, closing | 1, 14 | ~30 s | ~1 min |
| Quick setup | 2, 2a, 3, 4 | ~50 s | ~3.3 min |
| Figure slides | 5, 6, 7, 8, 9, 11, 12 | ~70–80 s | ~8.5 min |
| Framework, contributions/limitations | 10, 13 | ~70 s | ~2.5 min |
| **Total** | | | **~15.3 min** |

Slot adjustments:

- **20-minute slot (most likely):** 14 slides (~15 min) plus ~5 min Q&A.
- **15-minute slot:** move slides 4 and 8 to backup; 12 slides at ~12 min.
- **25+ minutes:** bring backup B1 (Theil math) into the main deck.

In the first timed run, any slide over 90 seconds gets trimmed in the outline.

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
| 5 | Build the `.pptx` from the corrected outline (pptxgenjs, `src/paper/seinforms_deck/`; showcase / BIDA-670 look, light, paper figures as-is, speaker notes); save to Drive | Claude | ✅ v3 in Drive: `01 Projects/seinforms-2026/ev-pulse-nc-seinforms-2026-deck-v3.pptx` (+ preview PDF); v2 added the research-questions slide, v3 the faculty-advisor line |
| 6 | Review in PowerPoint (Win 11 / Microsoft 365) | Owner | ⬜ |
| 7 | Import into Gamma, compare with the built deck, choose per slide | Owner + Claude | ⬜ |
| 8 | Retouch the chosen version in PowerPoint | Owner | ⬜ |
| 9 | Final number check: a fresh agent compares the exported PDF against the paper | Claude | ⬜ |
| 9b | **Current-status check on the whole final deck:** flag any slide claim that may be out of date as of the talk (e.g., NEVI program status and rules, Justice40/CEJST successor, NCDOT deployment plans). Findings go to the owner as Q&A notes or proposed wording; no slide changes without owner approval | Claude → Owner | ⬜ |
| 10 | Rehearsal: timed run-throughs; Q&A bank (~15 questions); mock Q&A with a skeptical-reviewer persona | Owner + Claude | ⬜ |
| 11 | Figure re-render, only if steps 6–10 show it is needed (styling only: fonts, sizes, titles; same data and design) | Claude | ⬜ |
| 12 | Freeze: PDF committed here, `.pptx` in Drive, backups (USB + PDF) | Owner + Claude | ⬜ |

Q&A bank topics (step 8): Chow break and underprediction, the "first" claim, why
these weights, why min-max normalization, the Justice40 rescission, the CEJST
archive, the LODES 2021 vintage, why the top 10 counties and not all 100.

## File policy

- The editable `.pptx` lives in Google Drive (also the Linux ↔ Windows handoff)
  and is never committed.
- The PDF export is the tracked artifact, committed in this folder at step 9.
