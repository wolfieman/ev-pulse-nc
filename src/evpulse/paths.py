"""Canonical filesystem paths for the project.

A single, location-independent source of truth for the repository root. Scripts
previously each hardcoded their own depth below the root via chained `.parent`
calls (e.g. ``Path(__file__).resolve().parent.parent.parent``), which silently
breaks the moment a file is moved to a different depth. Here the root is found
by walking upward until the directory holding ``pyproject.toml`` (or ``.git``)
is reached, so it survives any directory restructuring.

Copyright © 2026 Wolfgang Sanyer
Licensed under the Polyform Noncommercial License 1.0.0 (see LICENSE).
"""

from __future__ import annotations

from pathlib import Path


def _find_project_root() -> Path:
    """Walk up from this file to the directory containing the repo markers."""
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists() or (parent / ".git").exists():
            return parent
    raise RuntimeError(
        "Could not locate the project root: no pyproject.toml or .git found "
        "in any parent of evpulse/paths.py."
    )


PROJECT_ROOT = _find_project_root()
