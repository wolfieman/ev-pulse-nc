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
| CFP full-paper requirements captured | ✅ done, committed | Codex → `cfp-requirements.md` (commit `93471c2`) |
| Conference README links the spec | ✅ done, committed | Codex |
| Cross-repo handoff scratch kept out of repo | ✅ done | `CLAUDE_HANDOFF.md` gitignored |
| SEINFORMS working manuscript imported | ✅ done (this checkout) | Claude → `seinforms_manuscript.md` (gitignored, raw PDF extraction) |
| Portal abstract (250–400w) drafted | ✅ done | `abstract.md` — 297w, ready to paste |
| In-paper abstract trimmed to ≤200w | ✅ done | applied to `abstract.md` (159 words; §5 draft) |
| Content condensation (→ ~15 single-sp pp) | ⬜ todo | needs the working manuscript (now present) |
| Double-blind scrub | ⬜ todo | §4 checklist |
| `build_seinforms_docx.py` compiler | ⬜ todo | §6 spec; adapt `src/paper/build_docx.py` |
| Compile → PDF → Exordo upload | ⬜ todo | §7 checklist |

---

## 2. Source → target gap

| Category | Capstone (source) | SEINFORMS 2026 (target) |
|---|---|---|
| Length | 109 pp (double-spaced) | ~15 single-spaced pp internal target; **no hard cap** (chair-confirmed); ≥ 2,000 words |
| Review | Authored (APA 7) | **Double-blind** — no author/affiliation/advisor/institution/repo info |
| Font / margins | 12 pt TNR, 1″ | **11 pt** TNR (or similar), 1″ all sides |
| Spacing | Double-spaced, indented paragraphs | **Single-spaced, justified**, flush-left, no indent, blank line between paragraphs |
| Headings | APA 7 | Title + L1 **ALL-CAPS bold centered**; L2 bold flush-left mixed case |
| Citations | APA author-year | **Bracketed numeric** `[1]`, `[2, p. 18]`; alphabetical numbered `REFERENCES` |
| In-paper abstract | 207 words | **100–200 words**, begins with `ABSTRACT` |

> On length: the portal's "20 single-spaced pages" is a **readability/preparation
> target, not a hard cap** — confirmed with the chair (no page/word maximum;
> 2,000-word minimum). Internal aim ~15 pp keeps it tight.

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

---

## 4. Double-blind scrub checklist

Remove from the review PDF **and** the file name:

- [ ] Author name → `[Author Name]` or remove.
- [ ] Faculty advisor name.
- [ ] Institution / college name.
- [ ] Acknowledgements section.
- [ ] Appendix B (AI Methodology Disclosure) — identifying context; drop for the blind paper.
- [ ] Any links/paths to the author's other (private) repositories.
- [ ] PDF document metadata (author/title fields) — clear before upload.
- [ ] File name carries no author name → use `ev-pulse-nc-seinforms-2026.pdf`.

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

Adapt the existing `src/paper/build_docx.py` (present, 26 KB). Changes:

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

1. Export `seinforms_manuscript.docx` → PDF; confirm blind + clean metadata; rename `ev-pulse-nc-seinforms-2026.pdf`.
2. Step 1 — Track: `ARTIFICIAL INTELLIGENCE, BUSINESS ANALYTICS, STATISTICS, & TECHNOLOGY MANAGEMENT`.
3. Step 2 — Format: **Student** or **Oral** *(owner decision — see §8)*.
4. Step 3 — Title + paste the **297-word portal abstract** from `abstract.md` (≤450-word field limit; no citations/figures).
5. Step 4 — Author/presenter metadata (kept separate from the blind PDF). Student-submission flag *(owner decision — see §8)*.
6. Step 5 — Topic: `Analytics` (ANALYTICS group).
7. Step 6 — Upload the blind PDF.

No slides/supplemental files are requested at submission. Only other portal date: hotel-discount deadline 2026-09-12.

---

## 8. Open decisions for the owner

- **Presentation format (Step 2): Student or Oral?** Student enters student-track competition.
- **Student-submission flag (Step 4): Yes/No?** (MBA in progress through Dec 2026 → likely Yes.)
- **Internal length target:** ~15 single-spaced pp acceptable, or aim closer to the 20-page guidance?
- **Title:** keep the capstone title or adjust for the conference?

---

## 9. Environment constraint (Claude Code checkout)

This checkout has the **built PDF** and `src/paper/build_docx.py` and
`output/figures/`, but **not** the original markdown `paper/manuscript.md`
(gitignored, regenerable, absent here). The working manuscript
(`seinforms_manuscript.md`) was therefore seeded by `pdftotext -layout`
extraction of the capstone PDF — usable for condensation but carrying extraction
artifacts (page numbers, running headers, broken tables, mangled equations). If
the true `manuscript.md` source is available elsewhere, dropping it in (same
gitignored path) gives higher-fidelity input than the PDF extraction.
