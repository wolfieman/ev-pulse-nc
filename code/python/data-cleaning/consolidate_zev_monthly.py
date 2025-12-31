#!/usr/bin/env python3
"""
Consolidate NCDOT ZEV monthly registration files into a single dataset.

Reads multiple monthly Excel files, extracts relevant columns (County, Electric,
Plug-In Hybrid), adds a Month column derived from filenames, and produces a
consolidated output matching the NC_EV_PHEV.xlsx format.

Usage:
    python consolidate_zev_monthly.py --indir ../../../data/raw/ncdot-monthly --out ../../../data/processed/nc_zev_consolidated.xlsx
    python consolidate_zev_monthly.py --files file1.xlsx file2.xlsx --out combined.xlsx
"""

import argparse
import re
import sys
from pathlib import Path

import pandas as pd

MONTH_PATTERN = re.compile(r"(\d{4})[-_]?(january|february|march|april|may|june|july|august|september|october|november|december)", re.IGNORECASE)

MONTH_MAP = {
    "january": "01", "february": "02", "march": "03", "april": "04",
    "may": "05", "june": "06", "july": "07", "august": "08",
    "september": "09", "october": "10", "november": "11", "december": "12"
}

COLUMN_MAP = {
    "county": "County",
    "electric": "Electric",
    "plug-in hybrid": "PlugInHybrid",
}


def extract_month_from_filename(filename: str) -> str | None:
    """Extract YYYY-MM from filename like '2025-july-registration-data.xlsx'."""
    match = MONTH_PATTERN.search(filename.lower())
    if match:
        year = match.group(1)
        month_name = match.group(2)
        month_num = MONTH_MAP.get(month_name)
        if month_num:
            return f"{year}-{month_num}"
    return None


REQUIRED_COLUMNS = {"County", "Electric", "PlugInHybrid"}


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Map source columns to target column names.

    Args:
        df: Input DataFrame with original column names

    Returns:
        DataFrame with standardized column names (County, Electric, PlugInHybrid)

    Note:
        Column matching is case-insensitive. Missing columns will result in
        an incomplete DataFrame that should be validated by the caller.
    """
    col_lower = {c.lower().strip(): c for c in df.columns}
    result = {}

    for src_key, target_name in COLUMN_MAP.items():
        original_col = col_lower.get(src_key)
        if original_col:
            result[target_name] = df[original_col]

    return pd.DataFrame(result)


def load_monthly_file(path: Path) -> tuple[pd.DataFrame, str | None]:
    """Load a single monthly file and extract its month.

    Args:
        path: Path to the Excel file

    Returns:
        Tuple of (DataFrame with normalized columns, month string or None)
        Returns empty DataFrame if file cannot be read or is missing required columns.
    """
    month = extract_month_from_filename(path.name)

    # Try reading from "Results" sheet first, fall back to default sheet
    try:
        df = pd.read_excel(path, sheet_name="Results", engine="openpyxl")
    except (KeyError, ValueError):
        # Sheet name not found, try default sheet
        df = pd.read_excel(path, engine="openpyxl")

    df = normalize_columns(df)

    # Validate required columns are present
    missing_cols = REQUIRED_COLUMNS - set(df.columns)
    if missing_cols:
        print(f"  [warn] {path.name}: missing columns {missing_cols}", file=sys.stderr)
        return pd.DataFrame(), month

    if df.empty:
        return pd.DataFrame(), month

    # Exclude Total row
    df = df[df["County"].astype(str).str.lower() != "total"]

    return df, month


def consolidate(files: list[Path]) -> pd.DataFrame:
    """Consolidate multiple monthly files into one DataFrame."""
    frames = []

    for path in files:
        df, month = load_monthly_file(path)

        if df.empty:
            print(f"  [skip] {path.name}: no valid data", file=sys.stderr)
            continue

        if not month:
            print(f"  [warn] {path.name}: could not parse month from filename", file=sys.stderr)
            continue

        df.insert(0, "Month", month)
        frames.append(df)
        print(f"  [ok] {path.name}: {len(df)} counties, month={month}")

    if not frames:
        return pd.DataFrame()

    combined = pd.concat(frames, ignore_index=True)

    # Sort: Month ascending, County ascending
    combined = combined.sort_values(["Month", "County"], ascending=[True, True])
    combined = combined.reset_index(drop=True)

    # Ensure column order
    return combined[["Month", "County", "Electric", "PlugInHybrid"]]


def main():
    parser = argparse.ArgumentParser(
        description="Consolidate NCDOT ZEV monthly files into a single dataset",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --indir ../../../data/raw/ncdot-monthly --out ../../../data/processed/nc_zev_consolidated.xlsx
  %(prog)s --files 2025-july*.xlsx 2025-august*.xlsx --out combined.csv
        """
    )

    parser.add_argument("--indir", help="Directory containing monthly Excel files")
    parser.add_argument("--files", nargs="+", help="Specific files to consolidate")
    parser.add_argument("--out", required=True, help="Output file path (.xlsx or .csv)")

    args = parser.parse_args()

    # Gather input files
    if args.files:
        files = [Path(f).resolve() for f in args.files]
    elif args.indir:
        indir = Path(args.indir).resolve()
        files = sorted(indir.glob("*.xlsx"))
    else:
        parser.error("Provide either --indir or --files")

    if not files:
        print("No input files found.", file=sys.stderr)
        sys.exit(1)

    print(f"Consolidating {len(files)} files...")

    combined = consolidate(files)

    if combined.empty:
        print("No data to write.", file=sys.stderr)
        sys.exit(1)

    # Write output
    out_path = Path(args.out).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    if out_path.suffix.lower() == ".csv":
        combined.to_csv(out_path, index=False)
    else:
        combined.to_excel(out_path, index=False, sheet_name="NC_EV_PHEV")

    # Summary
    print()
    print(f"Output: {out_path}")
    print(f"  Rows: {len(combined)}")
    print(f"  Months: {combined['Month'].nunique()} ({combined['Month'].min()} to {combined['Month'].max()})")
    print(f"  Counties: {combined['County'].nunique()}")


if __name__ == "__main__":
    main()
