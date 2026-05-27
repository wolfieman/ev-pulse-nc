# EV Pulse NC: Python Style Guide

This document defines the coding standards and design philosophy for the EV Pulse NC project.

---

## Design Philosophy

**Python-first, not Java-lite.**

- Prefer functions and modules over classes
- Use classes only at boundaries: API clients, storage backends, stateful resources
- No forced OOP, no design patterns for their own sake
- Explicit over clever
- Code should read like a book with narrative flow and well-named functions
- Strive for code that is elegant, idiomatic, effective, efficient, and optimal
- Measure before optimizing
- Defensive at boundaries, trusting internally

---

## Readability & Narrative Style

Code should read top-to-bottom like prose; a reader should rarely have to jump around to follow what a script does.

- **Narrative ordering.** `main()` reads like a table of contents. Order helper functions by the sequence in which they are first called, not alphabetically.
- **Naming is documentation.** A well-named function rarely needs a comment — prefer `load_training_data()` over `load()` plus a comment. If you reach for a comment to explain *what* a line does, rename instead.
- **Comments earn their place.** Comment the *why* — a non-obvious threshold, a data quirk, a SAS-vs-Python difference — never the *what*. Delete comments that merely restate the code.
- **Section banners** (`# === Section ===`) split a long script into chapters (data loading / computation / output). Banner the phases, not every function.
- **Function size.** When a function outgrows a screen or mixes computation with I/O and plotting, split it along those seams. The ARIMA and AFDC-EDA splits are the worked examples: a reusable compute core in `evpulse/`, plotting and CLI in the script.

> Read these first as exemplars: `phase3_zip_density.py` (clean compute), `scoring_framework_vif.py` (narrative `main()`), `census_tract_boundaries.py` (boundary I/O with validation).

---

## Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Directories | kebab-case | `data-acquisition/` |
| Python files | snake_case | `ncdot_ev_pipeline.py` |
| Data files | kebab-case with pattern | `ncdot-ev-registrations-county-202506.csv` |
| Functions/variables | snake_case | `download_month()`, `month_label` |
| Classes | PascalCase | `DownloadResult` |
| Constants | UPPER_SNAKE_CASE | `BASE_URL`, `USER_AGENT` |
| DataFrames | `df`, `gdf` (GeoDataFrame), `<grain>_df` | `county_df`, `zip_df`, `tract_gdf` |
| Figure functions | `figNN_<subject>` | `fig09_stations_by_level()` |
| Private helpers | leading underscore | `_parse()`, `_extract()` |

### Abbreviations

Use the established domain abbreviations consistently, and spell out anything not on this list — clarity beats brevity:

`df` (DataFrame), `gdf` (GeoDataFrame), `fips`, `zcta`, `bev` / `phev`, `l2` / `dcfc`, `ci` (confidence interval), `crs`.

When more than one DataFrame is in scope, suffix it with its grain (`county_df`, `zip_df`) rather than relying on a bare `df`.

### Data File Naming Pattern

Follow the `domain-subject-grain-date.ext` convention:

```
ncdot-ev-registrations-county-202506.csv
│     │              │      │
│     │              │      └── Date (YYYYMM or YYYY-MM-DD)
│     │              └── Grain (county, state, station)
│     └── Subject (ev-registrations, charging-stations)
└── Domain/Source (ncdot, afdc)
```

> **Raw file exemption:** Downloaded files in `data/raw/` retain their source naming (e.g., `2025-july-registration-data.xlsx`) and are exempt from the `domain-subject-grain-date.ext` convention. The naming standard applies to processed and generated files only.

### Directory Structure Note

Two strata live under `src/`:

- **`src/evpulse/`** — the importable shared package (snake_case, per Python's import rules): paths, constants, IO/geo loaders, plotting style, and the ARIMA model core. Imported as `from evpulse.x import ...`.
- **`src/<area>/`** (`analysis/`, `data-acquisition/`, …) — standalone scripts run directly via `uv run`. These directories use kebab-case because they hold scripts, not importable modules. Scripts import sibling scripts by bare module name, resolved by the script's own directory on `sys.path`; they import shared logic from `evpulse`.

The only deliberate `sys.path` manipulation is in `tests/conftest.py`, which adds the script directories so the test suite can import scripts by bare name.

---

## Language Features Policy

### Encouraged

- **Type hints** at public function signatures (see `scoring_framework_vif.py` or `census_tract_boundaries.py` for fully-annotated exemplars)
- **dataclasses** for structured data with behavior
- **NamedTuple** for simple immutable record types
- **Generators** for streaming and pagination
- **Context managers** (`with`) for resource safety
- **Comprehensions** when simple and readable
- **pathlib.Path** over string path manipulation

### Discouraged

- Deep inheritance hierarchies
- Premature abstractions
- Metaprogramming or clever tricks
- Global mutable state

### Example: Good Use of NamedTuple

```python
from typing import NamedTuple
from pathlib import Path

class DownloadResult(NamedTuple):
    month: str
    success: bool
    path: Path | None
    message: str
```

---

## Notebooks Policy

- Use VS Code notebooks (`.ipynb`) for exploratory data analysis only
- Notebooks are for discovery, not authoritative code
- Stabilized logic must be promoted to Python modules in `src/`
- Promote quickly; do not let notebooks become a shadow codebase

---

## Testing Scope

| Test Type | Purpose | When to Write |
|-----------|---------|---------------|
| Unit tests | Pure transformations and business logic | Test-first for critical logic |
| Contract tests | Verify external API assumptions (e.g., NCDOT file structure) | When integrating new data sources |
| Integration tests | End-to-end validation (1-2 tests) | For critical data pipelines |

### Guiding Principles

- Test-first at boundaries and critical logic
- Test-after for exploratory work
- Focus on behavior, not implementation details

---

## Error Handling

### At Boundaries (External APIs, File I/O)

- Use exceptions with specific exception types
- Implement retry patterns for network calls
- Validate inputs defensively

```python
def download_file(url: str, dest: Path, retries: int = 3, timeout: int = 60) -> tuple[bool, str]:
    """Download with retry logic. Returns (success, message)."""
    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            # ... handle response
        except requests.exceptions.HTTPError as e:
            if response.status_code == 404:
                return False, "File not found (404)"
            last_error = f"HTTP error: {e}"
        # ... other exception handlers
    return False, f"{last_error} (after {retries} attempts)"
```

### Internal Logic

- Prefer return values over exceptions
- Use `print()` for CLI script output (acceptable for research project)

---

## Data Validation

### Philosophy

Validate defensively **at boundaries** (file I/O, external APIs, user input), trust **internally** in pure transformations. This keeps code simple while catching real problems early.

### Validation Patterns

**At Boundaries (File I/O, APIs):**
- Check file existence and size
- Validate external data structure (columns, sheet names, formats)
- Provide specific, actionable error messages
- Return `(success: bool, message: str)` tuples
- Log warnings to stderr for skipped/malformed data

```python
def validate_excel(file_path: Path) -> tuple[bool, str]:
    """Validate file exists and meets minimum standards."""
    if not file_path.exists():
        return False, "File does not exist"
    if file_path.stat().st_size < 1000:
        return False, "File suspiciously small"
    return True, "Valid"
```

**In Data Processing:**
- Check required columns are present
- Log warnings for skipped rows/files, don't fail silently

```python
missing_cols = REQUIRED_COLUMNS - set(df.columns)
if missing_cols:
    print(f"[warn] Missing columns {missing_cols}", file=sys.stderr)
    return pd.DataFrame(), None
```

### Framework Decision

**Do not use pandera, pydantic, or great_expectations** for this project:
- Validation logic is simple enough to read and understand
- Data volumes are research scale, not production scale
- Adds complexity without solving current problems

**When to reconsider:** If adding 5+ data sources or moving to automated pipelines.

---

## Configuration Strategy

This project uses a simple, explicit configuration approach:

### Current Approach

1. **Command-line arguments** (preferred) - All scripts use `argparse` with sensible defaults
2. **Module-level constants** - For fixed values like URLs and column names
3. **Default paths** - Scripts infer reasonable directories when not specified

### Guidelines

- Use CLI arguments for parameters users might customize
- Use constants for fixed values (URLs, formats, thresholds)
- Use `.env` files for external API keys (see below)

### API Keys Required

Two data-acquisition scripts require API keys, loaded from a project-root `.env` file via `python-dotenv`:

| Key | Used by | Get one |
|---|---|---|
| `NREL_API_KEY` | `src/data-acquisition/afdc_api_download.py` (AFDC charging stations) | https://developer.nrel.gov/signup/ (free, instant) |
| `CENSUS_API_KEY` | `src/data-acquisition/census_zip_population.py` (ACS ZCTA populations) | https://api.census.gov/data/key_signup.html (free) |

`.env` is gitignored — never commit credentials. NCDOT data is fetched via public web scraping (no key needed); LEHD/CEJST/Census boundaries use no-auth public endpoints.

---

## Ruff Linter Configuration

The project uses ruff with these rules (configured in `pyproject.toml`):

```toml
[tool.ruff]
line-length = 88
target-version = "py314"

[tool.ruff.lint]
select = ["E", "F", "W", "I"]
```

| Rule | Description |
|------|-------------|
| E | pycodestyle errors |
| F | pyflakes (unused imports, undefined names) |
| W | pycodestyle warnings |
| I | isort (import ordering) |

Run the linter before committing (always via `uv run`, never a bare `ruff`):

```bash
uv run ruff check src/
uv run ruff format src/
```

---

## Console Output Conventions

Scripts print progress and results to stdout. Standardize the tag vocabulary so output is scannable and greppable:

| Tag | Meaning | Stream |
|-----|---------|--------|
| `[ok]` | A step succeeded | stdout |
| `[warn]` | Recoverable problem; processing continues (e.g. a skipped malformed row) | stderr |
| `[SKIP]` | A step was deliberately skipped (e.g. coverage below a threshold) | stdout |
| `[PASS]` / `[FAIL]` | A verification or test assertion result | stdout |

Reserve `[PASS]` / `[FAIL]` for pass/fail checks (e.g. the baseline verifier); use `[ok]` / `[warn]` / `[SKIP]` for ordinary progress. Send `[warn]` to stderr so warnings survive stdout redirection.

---

## Code Organization

### Module Structure

```python
#!/usr/bin/env python3
"""Module docstring explaining purpose and usage.

Usage:
    uv run src/<area>/script.py --arg value

Copyright © 2026 Wolfgang Sanyer
Licensed under the Polyform Noncommercial License 1.0.0 (see LICENSE).
"""

from __future__ import annotations

# Standard library imports
import argparse
from pathlib import Path

# Third-party imports
import requests

# First-party imports
from evpulse.paths import PROJECT_ROOT

# Constants
BASE_URL = "https://example.com"

# Type definitions (NamedTuple, dataclass)
class Result(NamedTuple):
    success: bool
    message: str

# Functions (ordered by call hierarchy or logical grouping)
def main() -> None:
    ...

if __name__ == "__main__":
    main()
```

Mandatory in every module:

- **`from __future__ import annotations`** as the first statement after the docstring (one blank line below it). This keeps annotations zero-cost and lets `X | None` / `list[str]` be used freely.
- **The 2-line `Copyright ©` banner** as the last lines of the module docstring (see below).
- **`pathlib.Path`**, never `os.path` string juggling. Derive the repo root from `evpulse.paths.PROJECT_ROOT`, never from `__file__` parent-walking.
- **Double quotes** for strings (ruff-formatted).
- **Type hints** on public function signatures; modern syntax (`X | None`, `list[str]`, `dict[str, int]`) over `typing.Optional` / `Union` / `Dict` / `List`.

### Authorship & License Banner (required)

Every module's docstring **must end** with the binding two-line notice:

```text
Copyright © 2026 Wolfgang Sanyer
Licensed under the Polyform Noncommercial License 1.0.0 (see LICENSE).
```

This is the required-notice line for the Polyform Noncommercial license; an `Author:` line is not a substitute. There is no SPDX identifier — Polyform Noncommercial has none registered, so the plain copyright banner is canonical.

### Function Docstrings

Use Google-style docstrings for public functions:

```python
def generate_month_range(start: str, end: str) -> list[tuple[int, int]]:
    """Generate list of (year, month) tuples from start to end inclusive.

    Args:
        start: Start month in YYYY-MM format
        end: End month in YYYY-MM format

    Returns:
        List of (year, month) tuples covering the range

    Raises:
        ValueError: If start month is after end month
    """
```

---

## Evolution Rules

1. **Measure before optimizing** - Profile first, optimize second
2. **Add orchestration only when needed** - Scheduling and backfills justify complexity
3. **Traceability** - Changes that affect results must be documented
4. **Rule of three** - Introduce abstractions only after patterns repeat three times

---

## Quick Reference

```
Do:
  - Write functions, not classes (unless at boundaries)
  - Use type hints on public APIs
  - Keep functions small and focused
  - Use descriptive names that read naturally
  - Validate at boundaries, trust internally

Don't:
  - Create abstract base classes "just in case"
  - Use inheritance when composition works
  - Add configuration for hypothetical future needs
  - Let notebooks accumulate production logic
```

---

*Last updated: May 2026*
