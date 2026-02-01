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

## Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Directories | kebab-case | `data-acquisition/` |
| Python files | snake_case | `ncdot_zev_downloader.py` |
| Data files | kebab-case with pattern | `ncdot-ev-registrations-county-202506.csv` |
| Functions/variables | snake_case | `download_month()`, `month_label` |
| Classes | PascalCase | `DownloadResult` |
| Constants | UPPER_SNAKE_CASE | `BASE_URL`, `USER_AGENT` |

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

### Directory Structure Note

The `code/python/` subdirectories use kebab-case because they contain standalone scripts run directly, not importable modules. If importable packages are needed later, they must use snake_case per Python requirements.

---

## Language Features Policy

### Encouraged

- **Type hints** at public function signatures (see `ncdot_zev_downloader.py`)
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
- Stabilized logic must be promoted to Python modules in `code/python/`
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
- Use `.env` files only if external API keys are ever needed (currently not applicable)

### No API Keys Required

Current data sources (NCDOT and AFDC) require no authentication:
- NCDOT: Public website downloads
- AFDC: Pre-downloaded CSV data in Git LFS

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

Run the linter before committing:

```bash
ruff check code/python/
ruff format code/python/
```

---

## Code Organization

### Module Structure

```python
#!/usr/bin/env python3
"""
Module docstring explaining purpose and usage.

Usage:
    python script.py --arg value
"""

# Standard library imports
import argparse
from pathlib import Path

# Third-party imports
import requests

# Local imports (if any)

# Constants
BASE_URL = "https://example.com"

# Type definitions (NamedTuple, dataclass)
class Result(NamedTuple):
    success: bool
    message: str

# Functions (ordered by call hierarchy or logical grouping)
def main():
    ...

if __name__ == "__main__":
    main()
```

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

*Last updated: February 2026*
