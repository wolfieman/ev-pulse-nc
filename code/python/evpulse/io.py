"""Tabular I/O helpers shared across the analysis scripts.

The pipeline keys everything on FIPS-style codes (ZIP, county, tract), which
pandas will silently read as integers and strip of leading zeros -- a classic
join-breaking bug. ``load_fips_csv`` is the single reader that keeps those
columns as zero-padded strings so the convention can't drift per script.

Copyright © 2026 Wolfgang Sanyer
Licensed under the Polyform Noncommercial License 1.0.0 (see LICENSE).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd


def load_fips_csv(
    path: Path,
    fips_widths: dict[str, int],
    **read_kwargs: Any,
) -> pd.DataFrame:
    """Read a CSV, keeping FIPS-style code columns as zero-padded strings.

    Args:
        path: Path to the CSV.
        fips_widths: Maps a code column to its zero-pad width, e.g.
            ``{"zip": 5, "county_fips": 5}`` or ``{"tract_fips": 11}``. Each
            listed column is read as a string and left-padded to ``width`` so
            leading zeros survive.
        **read_kwargs: Forwarded to :func:`pandas.read_csv` (``usecols`` etc.).
            A caller-supplied ``dtype`` is merged with -- and overridden by --
            the string dtypes implied by ``fips_widths``.

    Returns:
        DataFrame with the listed columns as zero-padded strings.
    """
    dtype = {**read_kwargs.pop("dtype", {}), **{col: str for col in fips_widths}}
    df = pd.read_csv(path, dtype=dtype, **read_kwargs)
    for col, width in fips_widths.items():
        df[col] = df[col].str.zfill(width)
    return df
