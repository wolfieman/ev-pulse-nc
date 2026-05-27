# Contributing to EV Pulse NC

Guidelines for contributing to the North Carolina Electric Vehicle Analytics project.

## General Principles

- **Keep the project reproducible at all times.** All analysis outputs must be regeneratable from raw data.
- **Prefer small, focused changes.** One logical change per commit or PR.
- **Ensure analytical assumptions remain explicit in code.** Document thresholds, ratios, and methodological choices inline.

## Style Compliance

All contributions must follow [STYLE-GUIDE.md](STYLE-GUIDE.md).

**Linting:** Run `uv run ruff check` and `uv run ruff format` before committing.

```bash
uv run ruff check src/
uv run ruff format src/
```

The VS Code ruff extension handles this automatically on save.

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

## Testing Requirements

- **Add or update unit tests** when logic changes
- **Ensure existing tests pass** before merging: `pytest`
- **Integration tests must pass** for pipeline-affecting changes

Run tests:
```bash
pytest tests/
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

## Phase Transition Protocol

At the end of each analytical phase (e.g., Phase 1 → Phase 2), run these three maintenance tasks in order before beginning the next phase:

1. **Structure Optimization & Deduplication** — Consolidate any files added during the phase, remove duplicates, and ensure the directory layout matches `README.md`.
2. **Staleness Audit** — Verify all timestamps, dates, and status markers in documentation reflect the work just completed.
3. **Code & Structure Cleanup** — Add missing boundary validations, complete documentation for new scripts, and resolve any naming or style inconsistencies.

> **Timing:** Run at phase boundaries only, not mid-phase. Each task builds on the previous one's output, so execute them sequentially.

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
   uv sync                # runtime dependencies
   uv sync --extra dev    # also includes ruff + pytest
   ```

4. **Verify setup**
   ```bash
   uv run ruff check src/
   uv run pytest
   ```

> **Run everything via `uv run`** — never invoke `.venv/Scripts/python.exe` or system `python` directly. See [`STYLE-GUIDE.md`](STYLE-GUIDE.md) for the full convention list.

## Questions?

Open an issue on GitHub for questions about contributing.
