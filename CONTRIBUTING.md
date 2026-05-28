# Contributing to EV Pulse NC

Guidelines for contributing to the North Carolina Electric Vehicle Analytics project.

## General Principles

- **Keep the project reproducible at all times.** All analysis outputs must be regeneratable from raw data.
- **Prefer small, focused changes.** One logical change per commit or PR.
- **Ensure analytical assumptions remain explicit in code.** Document thresholds, ratios, and methodological choices inline.

## Style Compliance

All contributions must follow [STYLE-GUIDE.md](STYLE-GUIDE.md).

**Lint, format, and type-check** before committing:

```bash
uv run ruff check src/ tests/
uv run ruff format src/ tests/
uv run pyright
```

The VS Code ruff extension handles lint/format automatically on save. `pyright` runs in basic mode, scoped to the `evpulse/` package (see `pyproject.toml`).

## Branching Model

- **`main` must always be runnable.** Never push broken code to main.
- **Use short-lived feature branches.** Merge or close within days, not weeks.
- **Branch naming conventions:**
  - `feat-*` - New features or analysis capabilities
  - `fix-*` - Bug fixes or data corrections
  - `docs-*` - Documentation updates

## Commits

**Format:**
```
[EVPULSE][TYPE] Imperative subject, ≤72 characters
```

The project tag is always `[EVPULSE]` — never `[EVPULS]`, `[EV-PULSE]`, or any other variant. `TYPE` is one of:

| TYPE | Use for |
|------|---------|
| `FEAT` | New feature or analysis capability |
| `FIX` | Bug fix or data correction |
| `DOCS` | Documentation |
| `REFAC` | Refactor (no behaviour change) |
| `TEST` | Tests or test infrastructure |
| `CHORE` | Housekeeping (dependencies, gitignore, tooling) |
| `META` | Project / repo metadata |

**Guidelines:**
- Use the imperative mood ("Add forecast model", not "Added" or "Adds").
- Each commit should represent one logical change.
- An optional body explains *why*, not *what* — the diff already shows the what.

**Never include in a commit message:**
- AI or AI-tool attribution of any kind (no `Co-Authored-By`, no "Generated with …").
- Private references — internal repositories, course names, advisor or teammate names.
- Secrets, email addresses, or absolute filesystem paths (`C:\Users\…`).
- File-by-file dumps — summarize the change rather than listing every touched file.

**Enable the commit-message guard** (a dependency-free hook that enforces the format and blocks the items above). Copy it into your local hooks directory so it runs alongside the Git LFS hooks:

```bash
cp .githooks/commit-msg .git/hooks/commit-msg
chmod +x .git/hooks/commit-msg
```

> **Note:** Do *not* run `git config core.hooksPath .githooks`. Because this repository uses Git LFS, setting `core.hooksPath` replaces the default `.git/hooks/` directory wholesale and disables the LFS hooks (`post-checkout`, `post-merge`, `pre-push`), breaking large-file checkout. Copying the single hook into `.git/hooks/` lets it coexist with them.

## Testing Requirements

- **Add or update unit tests** when logic changes.
- **Ensure existing tests pass** before merging: `uv run pytest`.
- **Run the reproducibility guardrail** for any pipeline- or figure-affecting change: regenerate the affected outputs, then run the verifier below. It value-compares CSVs (exact for integer/string columns, `rtol=1e-9` for floats), pixel-compares figures, and checks the Top-3 NEVI canary against a golden baseline kept outside the repo.

```bash
uv run pytest
uv run tests/verify_against_baseline.py --baseline <path-to-baseline>
```

## Documentation Updates

Update documentation when changes:
- Affect outputs or data schemas
- Change assumptions or methodology
- Modify how the pipeline is run
- Add new data sources or dependencies

Key files to update:
- `data/README.md` - Data directory overview and sources
- `data/DATA-DICTIONARY.md` - Detailed data dictionary
- `src/README.md` - Code execution guide
- `README.md` - Project overview (major changes only)

## Extension Protocol

Adding a new analysis, phase, or feature follows the same right-sized loop the project was built and standardized with — scoped to the one change:

1. **Plan** — state the change and its expected effect on outputs (none, or a specific, justified change).
2. **Baseline** — if results could move, snapshot the current outputs (a golden baseline kept *outside* the repo) so "did it move?" is answerable.
3. **Tests** — add or update unit tests for any new closed-form logic *before* implementing.
4. **Implement** — small, focused `[EVPULSE][TYPE]` commits, one logical change each.
5. **Verify** — `uv run ruff check`, `uv run pyright`, `uv run pytest`; for pipeline- or figure-affecting changes, regenerate and run `verify_against_baseline.py` (CSV value-equality + figure pixels + Top-3 NEVI canary).
6. **Clean up** — the three phase-transition tasks below.
7. **Re-baseline** — when a change *intentionally* moves results (or the hardware/dependencies change), regenerate the golden baseline and reconcile it to the paper's published numbers, so it stays the source of truth.

### Phase-transition cleanup

At the end of each analytical phase (the clean-up sub-step above), run these three in order:

1. **Structure optimization & deduplication** — consolidate files added during the phase, remove duplicates, and ensure the directory layout matches `README.md`.
2. **Staleness audit** — verify all timestamps, dates, and status markers in documentation reflect the work just completed.
3. **Code & structure cleanup** — add missing boundary validations, complete docstrings for new scripts, and resolve any naming or style inconsistencies.

> **Timing:** Run at phase boundaries, not mid-phase. Each task builds on the previous one's output, so execute them sequentially.

## Definition of Done

A change is complete when:

- [ ] Code follows STYLE-GUIDE.md
- [ ] Tests pass (when applicable)
- [ ] Outputs remain reproducible
- [ ] Relevant documentation is updated
- [ ] Ruff reports no errors

## Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/wolfieman/ev-pulse-nc.git
   cd ev-pulse-nc
   ```

2. **Install Git LFS and pull data**
   ```bash
   git lfs install
   git lfs pull
   ```

3. **Install dependencies with uv**
   ```bash
   # Install uv if needed: https://docs.astral.sh/uv/
   uv sync                # runtime + dev deps (the dev group syncs by default)
   ```

4. **Verify setup**
   ```bash
   uv run ruff check src/ tests/
   uv run pyright
   uv run pytest
   ```

> **Run everything via `uv run`** — never invoke `.venv/Scripts/python.exe` or system `python` directly. See [`STYLE-GUIDE.md`](STYLE-GUIDE.md) for the full convention list.

## Questions?

Open an issue on GitHub for questions about contributing.
