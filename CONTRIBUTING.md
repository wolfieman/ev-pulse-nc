# Contributing to EV Pulse NC

Guidelines for contributing to the North Carolina Electric Vehicle Analytics project.

## General Principles

- **Keep the project reproducible at all times.** All analysis outputs must be regeneratable from raw data.
- **Prefer small, focused changes.** One logical change per commit or PR.
- **Ensure analytical assumptions remain explicit in code.** Document thresholds, ratios, and methodological choices inline.

## Style Compliance

All contributions must follow [STYLE-GUIDE.md](STYLE-GUIDE.md).

**Linting:** Run `ruff check` and `ruff format` before committing.

```bash
ruff check code/python/
ruff format code/python/
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
[EV-PULSE-NC] Brief description of change
```

**Guidelines:**
- Write clear, descriptive commit messages
- Each commit should represent one logical change
- Use present tense ("Add forecast model" not "Added forecast model")

**AI-assisted commits:** Include the co-author line:
```
Co-Authored-By: Claude <noreply@anthropic.com>
```

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
- `data/README.md` - Data dictionary and sources
- `code/README.md` - Code execution guide
- `README.md` - Project overview (major changes only)

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

3. **Create virtual environment**
   ```bash
   python -m venv .venv
   ```

4. **Activate environment**
   - Windows: `.venv\Scripts\activate`
   - Unix/macOS: `source .venv/bin/activate`

5. **Install project and dependencies**
   ```bash
   pip install -e .
   ```

6. **Install dev dependencies**
   ```bash
   pip install ruff pytest
   ```

7. **Verify setup**
   ```bash
   ruff check code/python/
   pytest
   ```

## Questions?

Open an issue on GitHub for questions about contributing.
