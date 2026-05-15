# Future Work & Deferred Items

Open items surfaced during reviews and audits but consciously deferred to keep individual commits scoped. Tracked here so they survive after the repo goes public and don't get buried in commit-message archaeology.

**Convention:** each item has a `Source`, `Scope`, `Action`, and `Status` line. `Source` cites the file:line or commit where the issue was found. Mark items `DONE` rather than deleting them — the audit trail is the point.

**Cross-references:** items with private context (data exploration notes, expert panel deliberations) link to `paper/PAPER-NOTES.md`, which is gitignored. Public-safe summaries live here.

---

## Code Standards Refactor

Project standard template is `code/python/analysis/scoring_framework_vif.py` (refactored 2026-04-10). Audited scripts that pre-date this template need the same treatment: `from __future__ import annotations`, `_SCRIPT_DIR = Path(__file__).resolve().parent` pattern (no `os.path.dirname` chains), `pathlib.Path` throughout, function-level type hints, module-level constants for thresholds/columns/paths, `Author: Wolfgang Sanyer` tag, and Google-style docstrings.

### Data-acquisition scripts (7 of 8 non-compliant)

- **Source:** Folder audit commit `4ec7622` (2026-05-14)
- **Scope:** `code/python/data-acquisition/` — every script except `census_tract_boundaries.py` (the only template-compliant one).
  - `afdc_api_download.py`
  - `census_county_boundaries.py`
  - `census_zcta_boundaries.py`
  - `census_zip_population.py`
  - `cejst_justice40_download.py`
  - `lehd_lodes_download.py`
  - `ncdot_ev_pipeline.py` (partial — uses `pathlib.Path` and partial type hints, but missing `_SCRIPT_DIR` pattern, `from __future__`, and author tag)
- **Action:** Refactor each to match the template. Highest-value shared change: replace the 4-nested `os.path.dirname(...)` REPO_ROOT block (duplicated in 6 of 7 files) with the 2-line `_SCRIPT_DIR / PROJECT_ROOT` pattern.
- **Status:** OPEN

### Analysis + blog scripts (28 non-compliant)

- **Source:** `paper/PAPER-NOTES.md` ~line 733 (TODO opened 2026-04-10 after VIF refactor); analysis folder audit 2026-05-14 confirmed scope and updated count; blog folder audit 2026-05-14 extended scope to include `blog_graphics.py`
- **Scope:** 27 of 28 scripts in `code/python/analysis/` + `code/python/blog/blog_graphics.py` not yet matching the template. Only `phase5_climate_sensitivity.py` uses the `_SCRIPT_DIR` pattern, and even it pre-dates the full template. All affected scripts already have the corrected `Author: Wolfgang Sanyer` + `License:` lines as of commit `75acdf6` — that part is no longer pending.
- **Action:** Bring each script up to the `scoring_framework_vif.py` template: `from __future__ import annotations`, `_SCRIPT_DIR` path pattern, full function-signature type hints, modern union syntax (`X | Y` over `Union[X, Y]` for py3.14), module-level constants for thresholds/columns/paths, Google-style docstrings.
- **Status:** OPEN
- **Private notes:** see PAPER-NOTES.md "TODO: Full Code Standards Review — 23 Analysis Scripts" (the count there is pre-audit; the real count is 28 once `phase5_climate_sensitivity.py` is excluded and `blog_graphics.py` is added)

### Figure-script naming inconsistency (post-public-release polish)

- **Source:** `code/python/analysis/` folder audit, 2026-05-14
- **Scope:** 5 figure-batch scripts use abstract range-based names (`phase3_fig26_to_fig29.py`, `phase3_fig30_to_fig32.py`, `phase3_fig33_fig34.py`, `phase4_fig35_to_fig38.py`, `phase5_fig39_to_fig42.py`) while 1 uses content-descriptive naming (`phase3_fig25_underserved_choropleth.py`). Range-based names require opening the file to know what it does, which is reviewer-unfriendly for a portfolio/academic repo.
- **Action:** Rename each range-based script to a content-descriptive form (e.g., `phase3_fig26_to_fig29.py` → `phase3_equity_inequality_figures.py`). Update references in `code/README.md`, root `README.md`, and `paper/PAPER-NOTES.md`.
- **Status:** OPEN
- **Priority:** Low — polish item, not correctness. Defer to post-public-release.

---

## Documentation Drift

### STYLE-GUIDE.md authentication claim is stale

- **Source:** `STYLE-GUIDE.md:209-211` — flagged in commit `4ec7622` (2026-05-14)
- **Scope:** The section "No API Keys Required" states current data sources require no authentication and that AFDC is "pre-downloaded CSV data in Git LFS." Both are wrong as of Phase 2+:
  - `NREL_API_KEY` is required by `afdc_api_download.py`
  - `CENSUS_API_KEY` is required by `census_zip_population.py`
  - AFDC data is now pulled live via the API, not from a static LFS file
- **Action:** Rewrite the section to (a) list the two required env keys with their `.env` setup, (b) point to `code/README.md` for the canonical "two require credentials" reference, (c) update or remove the "When external API keys are ever needed (currently not applicable)" line in the Configuration Strategy section above it.
- **Status:** OPEN
- **Priority:** Medium — affects new-contributor onboarding accuracy

### STYLE-GUIDE.md type-hints example reference

- **Source:** `STYLE-GUIDE.md:58` — flagged 2026-05-14 during data-acquisition audit
- **Scope:** Says "Type hints at public function signatures (see `ncdot_ev_pipeline.py`)" — but `ncdot_ev_pipeline.py` has only *partial* type hints, not full coverage. Better exemplar would be `census_tract_boundaries.py` or `scoring_framework_vif.py`, both fully annotated.
- **Action:** Update the cross-reference to point at one of the fully-annotated scripts.
- **Status:** OPEN
- **Priority:** Low

### `.gitignore` inconsistency for `data/processed/`

- **Source:** `data/` folder audit, 2026-05-14
- **Scope:** `.gitignore:73-74` ignores `data/processed/*.csv` and `*.parquet` only. Project memory states intent is "all of `data/processed/` gitignored as regenerable from scripts" — but `*.xlsx` and `*.qa.txt` slip through. Three files are currently tracked that arguably shouldn't be: `nc-ev-registrations-2025.xlsx`, `nc-ev-registrations-2025.qa.txt`, `scoring-vif-check.csv` (the CSV was added before the ignore rule was tightened).
- **Action:** Decide whether to (a) widen the ignore to include `*.xlsx` and `*.qa.txt` in `data/processed/` and `git rm --cached` the existing tracked files; or (b) keep these tracked because they encode paper-citable results (e.g., `scoring-vif-check.csv` contains the VIF=1.41 number referenced in PAPER-NOTES). Recommendation leans (b): tracked-but-regenerable is fine for paper-claim verification.
- **Status:** OPEN
- **Priority:** Low — no correctness impact, just a stated-intent vs. actual-state gap

### AI / LLM workflow documentation (consolidation)

- **Source:** Data audit conversation, 2026-05-14 — user noted they want to formally document their AI/LLM stack and how it integrates into their research/analytics workflows, frameworks, and pipelines
- **Scope:** Documentation of the user's AI-assisted methodology (Claude Code, possibly other tools), where it sits in their pipeline (drafting, code review, doc generation, blog creation, etc.), and how it is/isn't credited in outputs. **A version of this may already exist in another repo** (user wasn't certain). The current `docs/internal/BLOG-CREATION-PROTOCOL.md` describes the blog-specific workflow but doesn't generalize.
- **Action:**
  1. Cross-check existing repos (course repos, personal/portfolio repos) for any prior AI-stack documentation. If it exists, link from this repo rather than duplicate.
  2. If no canonical doc exists, write one — `docs/internal/AI-WORKFLOW.md` is the obvious home in this repo. Should cover: tools used, prompting patterns, when AI is/isn't applied, attribution policy (matching global CLAUDE.md: tools may be mentioned in workflow docs but never as co-author attribution in deliverables).
  3. Update `BLOG-CREATION-PROTOCOL.md` to reference the AI-workflow doc rather than re-explaining the tool stack inline.
- **Status:** OPEN
- **Priority:** Medium — useful for transparency about methodology; not blocking public release

---

## Pending Folder Audits

Per-folder walkthrough for data duplication, restructuring needs, naming consistency, and README accuracy. Started during the public-prep sprint on 2026-05-14.

| Folder | Status | Outcome |
|---|---|---|
| `code/python/data-acquisition/` | DONE 2026-05-14 | Commit `4ec7622` — 2 bug fixes, 1 rename, README patches |
| `code/python/data-cleaning/` | DONE 2026-05-14 | Folder removed — both scripts were orphaned legacy (Option A: archive and accept) |
| `code/python/analysis/` | DONE 2026-05-14 | Audit complete — only blocker was `publication_style.py:3` BIDA 670 title (fixed inline). Standards-template refactor (27 scripts) and figure-script naming polish moved to dedicated entries above. |
| `code/python/blog/` | DONE 2026-05-14 | Audit complete — anticipatory infra for the 4 planned blog posts, well-structured. Removed misleading import-time Pillow warning (fallback works fine). Standards-template gaps folded into the analysis+blog refactor item above. |
| `data/` | DONE 2026-05-14 | Removed orphaned `generated/` folder + `afdc-charging-units.xlsx` legacy file; fixed stale README diagram and ACS provenance attribution; removed last BIDA 670 reference (`AFDC-DATA-COMPARISON.md`) and the only AI co-attribution in the repo. Gitignore-consistency and AI-workflow-docs items moved to dedicated entries above. |
| `docs/` | OPEN | research, internal, eda-reports subdirs |
| `paper/` | OPEN | manuscript-in-prep area |
| `frameworks/` | OPEN | methodology docs |
| `output/` | OPEN | figures + tables (mostly gitignored) |

---

## Public Release Preparation ("Part D")

- **Source:** Public-prep sprint plan, 2026-05-14
- **Scope:** Final step in the GitHub Portal Link submission flow. PRs #2 (`bac7cd9`) and #3 (`db2a725`) covered the portfolio cleanup (Phase A) and portfolio polish (Phase C). The remaining work is the folder-by-folder audit (in progress, this document) and then the actual visibility flip.
- **Action:** Once all folder audits land:
  1. Final README link-check
  2. Verify `CITATION.cff` parses (GitHub "Cite this repository" button)
  3. Confirm `LICENSE` is present and current
  4. Confirm no secrets or `.env` files are tracked
  5. `gh repo edit --visibility public`
  6. Sanity-check `paper/PAPER-NOTES.md` is gitignored before the flip (it contains private peer-review and consultation notes)
- **Status:** BLOCKED on folder-audit completion
- **Priority:** High — this is the goal of the current sprint
