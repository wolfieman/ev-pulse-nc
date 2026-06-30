# SEINFORMS 2026 — Submission Plan (shared)

**Audience:** the three agents working this repo (Claude Code, agy/Antigravity,
Codex) plus the owner. This is the single shared plan; keep it in sync as steps
complete.
**Goal:** prepare and submit a condensed, double-blind SEINFORMS 2026 conference
paper derived from the EV Pulse NC capstone, by the **2026-07-31** deadline.
**Authoritative spec:** [`cfp-requirements.md`](cfp-requirements.md) — the
verified Exordo full-paper requirements. If anything here disagrees with that
file, that file wins.

Contributions merged into this plan: Codex (CFP requirements capture + README
link), agy (gap analysis, step plan, build-script mods, abstract trim, portal
checklist), Claude (manuscript import, corrections, environment constraints).

---

## 1. Status snapshot

| Item | State | Owner / notes |
|---|---|---|
| CFP full-paper requirements captured | ✅ done | Codex → `cfp-requirements.md` |
| Conference README links the spec | ✅ done | Codex |
| High-fidelity manuscript source imported | ✅ done | clean `manuscript.md` markdown copied to `seinforms_manuscript.md` (gitignored) |
| Portal abstract (250–400w) | ✅ done | `abstract.md` — 297w, ready to paste |
| In-paper abstract (100–200w) | ✅ done | `abstract.md` — 159w |
| Double-blind scrub (source text) | ✅ done | de-identified (Claude, `seinforms-002`) |
| `build_seinforms_docx.py` compiler | ✅ done | Claude (`seinforms-003`); committed `b429c80` |
| Numeric `[n]` citations + numbered `REFERENCES` | ✅ done | Codex (`seinforms-004`); processor runs in build |
| Content condensation | ✅ done | 23,618 → ~13,500 words (Claude, `seinforms-005`); renders ~31 pp |
| Bibliography cleanup (cited-only, 20 refs) | ✅ done | `Additional Sources Consulted` + uncited entries removed |
| Appendix-before-References reorder + CFP QA | ✅ done | Codex (`seinforms-008`) |
| Humanization (em-dash removal + sentence-split) | ✅ done | Claude (`seinforms-009`); docs-prose + mgmt-615 protocol |
| Final blind PDF (metadata-stripped, TNR) | ✅ done | Codex → `inter-agency/seinforms/output/ev-pulse-nc-seinforms-2026.pdf` (31 pp) |
| **Exordo portal upload** | ⬜ **todo — owner** | §7; manual submission by **2026-07-31** |

---

## 2. Source → target gap

| Category | Capstone (source) | SEINFORMS 2026 (target) |
|---|---|---|
| Length | 109 pp (double-spaced) | **Realized ~31 single-spaced pp** with all content/figures intact; no hard cap (chair-confirmed); ≥ 2,000 words ✓ |
| Review | Authored (APA 7) | **Double-blind** — no author/affiliation/advisor/institution/repo info |
| Font / margins | 12 pt TNR, 1″ | **11 pt** TNR (or similar), 1″ all sides |
| Spacing | Double-spaced, indented paragraphs | **Single-spaced, justified**, flush-left, no indent, blank line between paragraphs |
| Headings | APA 7 | Title + L1 **ALL-CAPS bold centered**; L2 bold flush-left mixed case |
| Citations | APA author-year | **Bracketed numeric** `[1]`, `[2, p. 18]`; alphabetical numbered `REFERENCES` |
| In-paper abstract | 207 words | **100–200 words**, begins with `ABSTRACT` |

> On length: the portal's "20 single-spaced pages" is a **readability/preparation
> target, not a hard cap** (chair-confirmed; no page/word maximum, 2,000-word
> minimum). The realized paper is **~31 pp**: the content is irreducibly
> data-dense, and the owner approved keeping all methodology, tables, figures,
> and quantitative results intact over hitting a lower page count.

---

## 3. Work sequence

1. **Condense** the working manuscript to the ~15-page target: shorten the
   literature review and background, keep the core method + results, retain only
   the high-impact figures (Theil decomposition, Gini/Lorenz, demand comparison,
   Justice40 overlay, NEVI priority scores, ARIMA validation, archetypes).
2. **Scrub** for double-blind (§4) — do this as part of, or immediately after,
   condensation so no identifying text survives.
3. **Trim** the in-paper abstract to the ≤200-word version (§5).
4. **Write** `build_seinforms_docx.py` (§6) and compile to DOCX.
5. **Export** DOCX → PDF (manual, per repo pipeline), verify blind, rename neutral.
6. **Submit** via Exordo (§7).

Steps 1–3 and 4 are independent and can run in parallel.

**Status (2026-06-30): steps 1–5 complete.** Only step 6 (Exordo submission)
remains, as the owner's manual portal upload.

---

## 4. Double-blind scrub checklist

Remove from the review PDF **and** the file name:

- [x] Author name → removed (title block now `*[Author name and affiliation removed…]*`).
- [x] Faculty advisor name → removed (title block, §1.4, §13).
- [x] Institution / college name → removed (title block, §1.4, §13).
- [x] Acknowledgements section → §13 retitled "Data Sources and Disclosures"; personal thanks removed, public-data credits + Funding/COI/AI disclosures kept (de-identified).
- [x] Appendix B (AI Methodology Disclosure) → dropped entirely.
- [x] Any links/paths to the author's other (private) repositories → all `github.com/wolfieman/*` URLs, the `orchestrator` repo reference, `docs/research/*` paths, the `nc-ev-atlas` name, and `Sanyer, W.` citation forms removed/neutralized.
- [ ] PDF document metadata (author/title fields) — clear before upload (export-time, `seinforms-005`).
- [ ] File name carries no author name → use `ev-pulse-nc-seinforms-2026.pdf` (export-time, `seinforms-005`).

Keep neutral, non-identifying phrasing for any unavoidable self-citations.
(Portal does not state a self-citation or funding policy.)

---

## 5. In-paper abstract — ≤200-word draft (apply to `abstract.md`)

**159 words** (160 counting the `ABSTRACT` lead; comfortably within the 100–200
limit). Corrects agy's draft by restoring "workplace-charging" (not "commuting")
to match the manuscript and the 297-word portal abstract.

> ABSTRACT: North Carolina holds $109 million in federal NEVI Formula Program
> funding for public EV charging infrastructure but lacks a data-driven method
> for prioritizing county-level allocation against utilization efficiency and
> Justice40 equity, amid BEV adoption growing at a 53.8% compound annual rate.
> This study integrates five analytical phases into a two-tier NEVI Priority
> Score combining a county-level ranking with ZIP-level targeting: out-of-sample
> forecast validation, an updated NREL AFDC infrastructure baseline, ZIP-level
> density analysis with an additive Theil-T decomposition, LEHD LODES
> workplace-charging demand modeling, and a CEJST v2.0 Justice40 overlay.
> Forecast validation yielded a mean absolute percentage error of 4.34%; the
> Theil-T decomposition found that 84.5% of charging-infrastructure inequality
> occurs within counties rather than between them, motivating the two-tier
> design. The three scoring pillars proved statistically independent (maximum
> VIF 1.41) with stable top-three rankings (Union, Mecklenburg, Guilford) under
> sensitivity perturbation. The framework informs state transportation-agency
> allocation decisions, captures 73% of the statewide BEV fleet, and is fully
> reproducible from public data.

---

## 6. Compiler script — `src/paper/build_seinforms_docx.py`

**Status: ✅ implemented** (committed `b429c80`; figure width later set to 5 in,
`9d99a82`). The citation processor (`tools/citation_processor.py`, Codex) runs
inside the build to convert APA → `[n]`. Original spec, adapted from
`src/paper/build_docx.py`:

- Font size → `Pt(11)`.
- Line spacing → `WD_LINE_SPACING.SINGLE`.
- Paragraph format → justified; `first_line_indent = Inches(0)`; `space_after = Pt(11)` (blank line between paragraphs).
- Title + L1 headings → centered, ALL CAPS, bold.
- L2 headings → flush left, mixed case, bold.
- Citations → emit bracketed numerics `[n]`; build an alphabetical, numbered `REFERENCES` list.
- Reads the gitignored `seinforms_manuscript.md`; embeds figures from `output/figures/`.
- Run via `uv run python src/paper/build_seinforms_docx.py` (repo rule: OS CPython only; never install an interpreter).

---

## 7. Exordo submission checklist

1. ✅ **Done** — blind, metadata-stripped `ev-pulse-nc-seinforms-2026.pdf` (31 pp, TNR embedded) is built at `inter-agency/seinforms/output/`. (Optional: a Word re-export for maximum font fidelity before upload.)
2. Step 1 — Track: `ARTIFICIAL INTELLIGENCE, BUSINESS ANALYTICS, STATISTICS, & TECHNOLOGY MANAGEMENT`.
3. Step 2 — Format: **Student** *(resolved, §8)*.
4. Step 3 — Title + paste the **297-word portal abstract** from `abstract.md` (≤450-word field limit; no citations/figures).
5. Step 4 — Author/presenter metadata (kept separate from the blind PDF). Student-submission flag: **Yes** (MBA in progress).
6. Step 5 — Topic: `Analytics` (ANALYTICS group).
7. Step 6 — Upload the blind PDF.

No slides/supplemental files are requested at submission. Only other portal date: hotel-discount deadline 2026-09-12.

---

## 8. Owner decisions (resolved)

- **Presentation format (Step 2): Student.**
- **Student-submission flag (Step 4): Yes** (MBA in progress through Dec 2026); confirm in the portal.
- **Length:** all content kept intact; **~31 single-spaced pp accepted** (CFP has no hard cap).
- **Title: keep the original capstone title** — a known, owner-approved double-blind exposure, since the project name is searchable.

---

## 9. Environment note (resolved)

The earlier constraint (only a `pdftotext`-extracted manuscript was available) is
**resolved**: the high-fidelity `manuscript.md` markdown source was located and
used as the condensation input, so the working `seinforms_manuscript.md` carries
no extraction artifacts. It stays gitignored as a pre-publication working draft;
the canonical tracked artifact is the exported PDF.
