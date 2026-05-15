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
- **Action:** Rewrote the "No API Keys Required" section to accurately list `NREL_API_KEY` and `CENSUS_API_KEY` requirements with their `.env` source links. Also updated the Configuration Strategy guideline above it from "currently not applicable" to "see below."
- **Status:** DONE 2026-05-14 (root audit)

### STYLE-GUIDE.md type-hints example reference

- **Source:** `STYLE-GUIDE.md:58` — flagged 2026-05-14 during data-acquisition audit
- **Action:** Updated the exemplar reference from `ncdot_ev_pipeline.py` (partial coverage) to `scoring_framework_vif.py` and `census_tract_boundaries.py` (both fully annotated).
- **Status:** DONE 2026-05-14 (root audit)

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
- **Preserved raw material for the eventual doc** (removed from `frameworks/README.md` during the frameworks/ folder audit, 2026-05-14):

  > All frameworks created by expert agent analysis (Jan 30, 2026) for the EV Pulse NC project.
  >
  > **Agent Contributors:**
  > - Decision Framework Agent (a18649a): 5-node decision tree analysis
  > - Data Structure Agent (ab08c82): AFDC API research, snapshot comparison methodology
  > - Stakeholder Value Agent (a6086db): Differential value matrix, integration analysis

  These are task-specific Claude Code subagent contributions from the Jan 30 framework-design session. Useful as concrete examples in the "specific contributions" section of the eventual AI-WORKFLOW.md — the agent IDs are session hashes that can be looked up in the user's Claude Code transcript archive if more context is needed.

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
| `docs/` | DONE 2026-05-14 | Comprehensive BIDA 670 + Dr. Al-Ghandour sweep across the public-facing repo (30 edits across 13 files); regenerated pipeline diagram PNG with clean institutional subtitle and generic framework caption; embedded the regenerated pipeline figure in root README and `paper/PAPER-BRIEF.md`; created `docs/figures/README.md` provenance doc; moved blog consultation from `docs/internal/` to new `docs/blog/`. Advisor name retained in academic-attribution contexts (root README:242 Acknowledgments, NOTICE.md:14). |
| `paper/` | DONE 2026-05-14 | Removed stale pre-implementation planning doc (`vif-scoring-framework-action-plan.md`) — work it described is complete (script + results + PAPER-NOTES writeup all live elsewhere). PAPER-BRIEF.md, README.md, and the gitignored PAPER-NOTES.md verified clean. |
| `frameworks/` | DONE 2026-05-14 | Removed references to nonexistent `afdc-api-analysis.md` (3 sites); renamed `ctpp-analysis.md` → `phase4-workplace-charging.md` to match its actual LEHD/LODES content (filename was legacy from the abandoned CTPP plan); stripped stale Size column values in the README table; removed AI agent-attribution section (preserved in the AI-workflow FUTURE-WORK entry above as raw material); removed local-filesystem-path sections that leaked the user's directory layout. |
| `output/` | DONE 2026-05-14 | Removed obsolete placeholders (`PLACEHOLDER-figures-here.txt` + the empty `output/tables/` subdir with its placeholder — all tabular outputs land in `data/processed/`). Rewrote `output/README.md` figures section to cover all 5 phases (it had only documented Phase 1, missing 35 figures). Validation outputs + models README verified clean. |
| **Root files** | DONE 2026-05-14 | Cross-folder audit of top-level files + subfolder READMEs. Fixed stale references in root README (`output/tables/` tree entry), `INSTALLATION.md` (pre-uv setup commands + stale mkdir paths for removed `data/generated/` and `output/tables/`), and `CONTRIBUTING.md` (wrong commit format `[EVPULS]` + pre-uv dev setup). Fixed STYLE-GUIDE drift (auth-claim + type-hints exemplar). Moved `PROJECT-BRIEF.md` and `PROJECT-EXPLANATION.md` from root to `paper/` to colocate project-narrative-tier docs; updated all internal cross-references and the root README documentation table. |

---

## Public Release Preparation ("Part D")

- **Source:** Public-prep sprint plan, 2026-05-14
- **Scope:** Final step in the GitHub Portal Link submission flow. PRs #2 (`bac7cd9`) and #3 (`db2a725`) covered the portfolio cleanup (Phase A) and portfolio polish (Phase C). PR #4 (`420b66c`) bundled the folder-by-folder audit + repo-wide attribution sweep + uv migration + root-file cleanup.
- **Result:**
  - PR #4 squash-merged 2026-05-15
  - Visibility flipped to public via `gh repo edit --visibility public` immediately after merge
  - `chore/tidy-walkthrough` branch deleted (local + remote) — audit trail lives in the squashed `420b66c` commit body
  - All pre-flip safety items verified: `paper/PAPER-NOTES.md` gitignored, no tracked `.env`, `CITATION.cff` valid, `LICENSE` current
- **Status:** DONE 2026-05-15

---

## Post-Launch: Convert highest-value FUTURE-WORK entries to GitHub Issues

- **Source:** Decision conversation, 2026-05-15 (post-launch reflection)
- **Scope:** Now that the repo is public, an empty Issues tab reads as "static / abandoned." A handful of well-scoped Issues signals active maintenance and gives each item its own discoverable URL for resume/portfolio linking.
- **Timing:** **Defer until after paper + presentation deadlines clear.** Paper has a fixed deadline; portfolio polish does not. Don't trade focus on the deliverable for Issues triage.
- **Hybrid approach** (do not replace this doc with Issues):
  - `FUTURE-WORK.md` remains the canonical master log — full `Source` / `Scope` / `Action` / `Status` context, links to source commits
  - GitHub Issues track only items being actively worked or that benefit from public visibility
  - Cross-link both ways: Issue body links back to its FUTURE-WORK section; the FUTURE-WORK Status field references the Issue number (e.g., "OPEN — see #5")
- **Recommended candidates for issue conversion** (priority order):
  1. **Standards-template refactor** (28 scripts in `code/python/analysis/` + `code/python/blog/blog_graphics.py`) — concrete scope, could be tagged `good first issue` for external contributors
  2. **AI / LLM workflow documentation consolidation** — useful for portfolio transparency; agent-attribution raw material is preserved in this doc
  3. **Figure-script naming polish** (5 range-based filenames → content-descriptive) — small, well-scoped, easy "completed" win
- **NOT recommended for issue conversion** (keep here only):
  - `.gitignore` consistency for `data/processed/*.xlsx` and `*.qa.txt` — low priority, stated-intent gap only
  - The per-folder audit table — historical record, not actionable work
- **Optional polish:** a simple GitHub Project (Kanban board) once 3-5 issues are open, for visual portfolio screenshots.
- **Status:** OPEN — deferred to post-paper-deadline
- **Priority:** Low — repo is shipped and healthy; this is portfolio polish, not blocking
