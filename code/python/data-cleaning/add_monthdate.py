#!/usr/bin/env python3
"""
Add MonthDate column to EV/PHEV datasets for numeric month format.

Derives MonthDate (YYYYMM format) from the Month column (YYYY-MM format).
Overwrites the input file in place.

Usage:
    python add_monthdate.py
    python add_monthdate.py --file ../../../data/generated/ncdot-ev-phev-latest.xlsx

Author: Wolfgang Sanyer
License: Polyform Noncommercial 1.0.0 (see LICENSE)
"""

import argparse
import sys
from pathlib import Path

import pandas as pd

DEFAULT_FILE = Path(__file__).resolve().parent.parent.parent.parent / "data" / "generated" / "ncdot-ev-phev-latest.xlsx"


def add_monthdate(filepath: Path) -> None:
    """Add MonthDate column derived from Month column.

    Modifies the file in place, overwriting the original.

    Args:
        filepath: Path to Excel file to process

    Raises:
        ValueError: If Month column not found in file
        FileNotFoundError: If file doesn't exist
    """
    print(f"Reading: {filepath}")
    try:
        df = pd.read_excel(filepath)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {filepath}")
    except Exception as e:
        raise RuntimeError(f"Failed to read Excel file {filepath}: {e}") from e

    if "Month" not in df.columns:
        raise ValueError(f"Month column not found. Available columns: {df.columns.tolist()}")

    if "MonthDate" in df.columns:
        print("MonthDate column already exists, updating...")

    # Convert YYYY-MM to YYYYMM (numeric format for analysis)
    df["MonthDate"] = df["Month"].astype(str).str.replace("-", "", regex=False)

    # Reorder columns to place MonthDate after Month
    cols = df.columns.tolist()
    cols.remove("MonthDate")
    month_idx = cols.index("Month") + 1
    cols.insert(month_idx, "MonthDate")
    df = df[cols]

    print(f"Writing: {filepath}")
    try:
        df.to_excel(filepath, index=False)
    except PermissionError:
        raise PermissionError(f"Cannot write to file (may be open): {filepath}")
    except Exception as e:
        raise RuntimeError(f"Failed to write Excel file {filepath}: {e}") from e
    print(f"Done. Added MonthDate column ({len(df)} rows)")


def main():
    """Parse arguments and run the MonthDate column addition."""
    parser = argparse.ArgumentParser(description="Add MonthDate column to EV/PHEV Excel files")
    parser.add_argument("--file", type=Path, default=DEFAULT_FILE,
                        help=f"Excel file to process (default: {DEFAULT_FILE})")
    args = parser.parse_args()

    if not args.file.exists():
        print(f"Error: File not found: {args.file}")
        return 1

    add_monthdate(args.file)
    return 0


if __name__ == "__main__":
    sys.exit(main())
