#!/usr/bin/env python3
"""Verify regenerated pipeline outputs against a pre-refactor golden baseline.

This is the reproducibility guardrail for the refactor: after a code change,
regenerate the pipeline and run this to prove the results did not move.

Comparison rules (see the data-quality / reproducibility review):
    CSVs    compared by VALUE, not bytes -- exact for integer and string
            columns (FIPS codes, ranks, names), rtol=1e-9 for floats,
            row-order-insensitive. Float formatting in to_csv may change
            without the numbers changing, so a byte hash would false-alarm.
    Figures compared by PNG pixel RMS with a small tolerance. PDFs are
            skipped: matplotlib stamps a non-deterministic CreationDate, so
            PDF bytes never match across runs.
    Canary  the Top-3 NEVI counties (Union, Mecklenburg, Guilford) -- the
            cheapest end-to-end check that the headline result is intact.

The baseline directory is machine-local; pass it with --baseline. RUN_ORDER
documents the canonical topological order in which the pipeline regenerates.

Usage:
    uv run tests/verify_against_baseline.py --baseline /path/to/baseline
    uv run tests/verify_against_baseline.py --list-order

Copyright © 2026 Wolfgang Sanyer
Licensed under the Polyform Noncommercial License 1.0.0 (see LICENSE).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = REPO_ROOT / "data" / "processed"
VALIDATION_DIR = REPO_ROOT / "output" / "validation"
FIGURES_DIR = REPO_ROOT / "output" / "figures"

FLOAT_RTOL = 1e-9
PNG_RMS_TOL = 2.0
CANARY_TOP3 = ["Union", "Mecklenburg", "Guilford"]

# Canonical topological run order (acquisition -> phase 3 -> phase 4 ->
# phase 5 -> scoring -> figures). Regeneration is run manually; this list is
# the single source of truth for ordering during a full rebuild.
RUN_ORDER = [
    "data-acquisition/ncdot_ev_pipeline.py",
    "analysis/phase3_zip_mapping.py",
    "analysis/phase3_zip_density.py",
    "analysis/phase3_gini_inequality.py",
    "analysis/phase3_theil_decomposition.py",
    "analysis/phase3_top20_underserved.py",
    "analysis/phase4_workplace_charging.py",
    "analysis/phase5_tract_zcta_crosswalk.py",
    "analysis/scoring_framework_skeleton.py",
    "analysis/scoring_framework_final.py",
    "analysis/scoring_framework_vif.py",
    "analysis/phase5_weight_sensitivity.py",
]


# =============================================================================
# CSV VALUE COMPARISON
# =============================================================================
def compare_csv(baseline: Path, current: Path) -> tuple[bool, str]:
    """Compare two CSVs by value. Returns (matches, detail)."""
    if not current.exists():
        return False, "missing in current outputs"
    a = pd.read_csv(baseline)
    b = pd.read_csv(current)
    if list(a.columns) != list(b.columns):
        return False, "column set differs"
    if a.shape != b.shape:
        return False, f"shape {a.shape} vs {b.shape}"
    sort_cols = list(a.columns)
    a = a.sort_values(sort_cols).reset_index(drop=True)
    b = b.sort_values(sort_cols).reset_index(drop=True)
    numeric = a.select_dtypes("number").columns
    for col in a.columns:
        if col in numeric:
            if not np.allclose(a[col], b[col], rtol=FLOAT_RTOL, equal_nan=True):
                worst = float((a[col] - b[col]).abs().max())
                return False, f"numeric drift in '{col}' (max abs {worst:.3e})"
        else:
            # Fill NA with a sentinel first: under the pandas string dtype,
            # NA != NA is NA (not False), which would false-flag missing values.
            sa = a[col].fillna("\x00NA").astype(str).to_numpy()
            sb = b[col].fillna("\x00NA").astype(str).to_numpy()
            if not (sa == sb).all():
                return False, f"string drift in '{col}'"
    return True, "ok"


def compare_csv_dirs(base_root: Path) -> list[tuple[str, bool, str]]:
    """Compare every baseline CSV against its current counterpart."""
    pairs = [
        (base_root / "processed", PROCESSED_DIR),
        (base_root / "validation", VALIDATION_DIR),
    ]
    results = []
    for base_dir, cur_dir in pairs:
        if not base_dir.is_dir():
            continue
        for csv in sorted(base_dir.glob("*.csv")):
            ok, detail = compare_csv(csv, cur_dir / csv.name)
            results.append((csv.name, ok, detail))
    return results


# =============================================================================
# FIGURE COMPARISON (PNG pixel RMS; PDFs skipped)
# =============================================================================
def png_rms(baseline: Path, current: Path) -> float:
    """Root-mean-square pixel difference; inf if missing or sized differently."""
    from PIL import Image

    if not current.exists():
        return float("inf")
    a = np.asarray(Image.open(baseline).convert("RGBA"), dtype=float)
    b = np.asarray(Image.open(current).convert("RGBA"), dtype=float)
    if a.shape != b.shape:
        return float("inf")
    return float(np.sqrt(np.mean((a - b) ** 2)))


def compare_figures(base_root: Path) -> list[tuple[str, bool, str]]:
    """Compare every baseline PNG against its current counterpart."""
    base_dir = base_root / "figures"
    if not base_dir.is_dir():
        return []
    results = []
    for png in sorted(base_dir.glob("*.png")):
        rms = png_rms(png, FIGURES_DIR / png.name)
        results.append((png.name, rms <= PNG_RMS_TOL, f"rms={rms:.3f}"))
    return results


# =============================================================================
# TOP-3 NEVI CANARY
# =============================================================================
def check_canary() -> tuple[bool, list[str]]:
    """Confirm the published Top-3 NEVI counties are intact."""
    path = PROCESSED_DIR / "scoring-framework-final.csv"
    if not path.exists():
        return False, []
    df = pd.read_csv(path).sort_values("nevi_priority_score", ascending=False)
    top3 = df["county_name"].head(3).tolist()
    return top3 == CANARY_TOP3, top3


# =============================================================================
# CLI & MAIN
# =============================================================================
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--baseline", type=Path, help="Path to the golden-baseline directory"
    )
    parser.add_argument(
        "--skip-figures", action="store_true", help="Skip PNG figure comparison"
    )
    parser.add_argument(
        "--list-order", action="store_true", help="Print the run order and exit"
    )
    return parser.parse_args()


def _report(title: str, rows: list[tuple[str, bool, str]]) -> bool:
    print(f"\n{title} ({sum(ok for _, ok, _ in rows)}/{len(rows)} match)")
    all_ok = True
    for name, ok, detail in rows:
        if not ok:
            all_ok = False
            print(f"  [FAIL] {name}: {detail}")
    return all_ok


def main() -> None:
    args = parse_args()

    if args.list_order:
        print("Canonical pipeline run order:")
        for i, script in enumerate(RUN_ORDER, 1):
            print(f"  {i:2d}. uv run src/{script}")
        return

    if not args.baseline or not args.baseline.is_dir():
        sys.exit("error: --baseline must point to an existing baseline directory")

    print(f"Verifying current outputs against baseline: {args.baseline}")
    passed = True

    passed &= _report("CSV value comparison", compare_csv_dirs(args.baseline))
    if not args.skip_figures:
        passed &= _report("Figure PNG comparison", compare_figures(args.baseline))

    canary_ok, top3 = check_canary()
    print(f"\nTop-3 NEVI canary: {top3} -> {'PASS' if canary_ok else 'FAIL'}")
    passed &= canary_ok

    print(
        "\n"
        + (
            "RESULT: PASS -- outputs match baseline"
            if passed
            else "RESULT: FAIL -- outputs diverged from baseline"
        )
    )
    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
