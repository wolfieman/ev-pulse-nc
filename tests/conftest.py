"""Pytest configuration: headless plotting and import-path bootstrap.

Makes the standalone analysis and data-acquisition scripts importable by
module name (they live in run-directly script directories, not an installed
package) and forces a non-interactive matplotlib backend so figure code can
run headless under pytest and CI.

Copyright © 2026 Wolfgang Sanyer
Licensed under the Polyform Noncommercial License 1.0.0 (see LICENSE).
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

_ROOT = Path(__file__).resolve().parent.parent
for _area in ("analysis", "data-acquisition"):
    sys.path.insert(0, str(_ROOT / "code" / "python" / _area))
