# SEINFORMS 2026 — Presentation Plan

**Talk:** in person, SEINFORMS 2026, Myrtle Beach, SC (Oct 15–16, 2026).
**Target:** ~15 minutes of talk plus Q&A (14 core slides, 4 backup slides).
**Deadline:** deck and rehearsal complete by Thu Oct 8, Fri Oct 9 at the latest.
**Working rule:** steps run in order, as fast as they go, not tied to calendar days.

Locked slide-by-slide content lives in [`deck-outline.md`](deck-outline.md).

---

## Sources

| Source | Role |
|---|---|
| SEINFORMS paper (`../output/ev-pulse-nc-seinforms-2026.pdf`, 31 pp; source `../seinforms_manuscript.md`) | Source of truth for every number, claim, and figure |
| MBA Showcase deck (`../../../competitions/mba-showcase-2026/`, 14 slides, 2nd place) | Storyline: tight and audience-friendly |
| Capstone defense deck (`../../../paper/ev-pulse-nc-sanyer-presentation.pdf`, 25 slides, presented Spring 2026) | Methods depth: Chow break, Theil deep dive, scoring formula, sensitivity, archetypes with the empty quadrant, Justice40 framing, direction-of-bias limitations |

Approach: keep the showcase storyline, take the methods slides from the capstone
deck, and check every number against the SEINFORMS paper.

## Decisions (locked)

**a. Deck-vs-paper differences.** All three sources come from the same capstone
manuscript; the differences are slips in the showcase slides, fixed in the new
deck. A few small slips inside the SEINFORMS manuscript are fixed at step 9.
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
| Quick setup | 2, 3, 4 | ~50 s | ~2.5 min |
| Figure slides | 5, 6, 7, 8, 9, 11, 12 | ~70–80 s | ~8.5 min |
| Framework, contributions/limitations | 10, 13 | ~70 s | ~2.5 min |
| **Total** | | | **~14.5 min** |

Slot adjustments:

- **20-minute slot (most likely):** 14 slides (~15 min) plus ~5 min Q&A.
- **15-minute slot:** move slides 4 and 8 to backup; 12 slides at ~12 min.
- **25+ minutes:** bring backup B1 (Theil math) into the main deck.

In the first timed run, any slide over 90 seconds gets trimmed in the outline.

## Steps

| # | Step | Owner | Status |
|---|---|---|---|
| 1 | Lock decisions (sources, a/b/c, ~15-min target) | Owner | ✅ done |
| 2 | Locked outline: per-slide text, numbers tied to paper sections, figure, source slide, draft speaker notes | Claude | ✅ drafted — [`deck-outline.md`](deck-outline.md) |
| 3 | Figure check at projector scale; re-render any that fail from the repo's figure scripts (same data and palette) | Claude | ⬜ |
| 4 | NEVI current-status check (~15 min), written up as a Q&A note | Claude | ⬜ |
| 5 | Gamma: generate from the outline with the 7 paper PNGs; no generated charts, no rewritten numbers; export `.pptx` to Drive | Owner | ⬜ |
| 6 | Polish in PowerPoint (Win 11 / Microsoft 365); finalize speaker notes per the humanization protocol | Owner + Claude | ⬜ |
| 7 | Verification: a fresh agent compares the exported PDF against the paper, number by number | Claude | ⬜ |
| 8 | Rehearsal: timed run-throughs; Q&A bank (~15 questions); mock Q&A with a skeptical-reviewer persona | Owner + Claude | ⬜ |
| 9 | Freeze: PDF committed here, `.pptx` in Drive, backups (USB + PDF); manuscript fixes from the corrections log; stale status notes in the repo | Owner + Claude | ⬜ |

Q&A bank topics (step 8): Chow break and underprediction, the "first" claim, why
these weights, why min-max normalization, the Justice40 rescission, the CEJST
archive, the LODES 2021 vintage, why the top 10 counties and not all 100.

## File policy

- The editable `.pptx` lives in Google Drive (also the Linux ↔ Windows handoff)
  and is never committed.
- The PDF export is the tracked artifact, committed in this folder at step 9.
