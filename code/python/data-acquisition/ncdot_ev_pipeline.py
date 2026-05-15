#!/usr/bin/env python3
"""
NCDOT Electric Vehicle Registration Data Pipeline

Scrapes and consolidates county-level EV registration data from NCDOT.
Discovers all monthly Excel files, downloads them, standardizes schemas
across different time periods, and produces a consolidated master dataset.

Originally developed for nc-ev-atlas project.

Usage:
    python ncdot_ev_pipeline.py --years 2025
    python ncdot_ev_pipeline.py --start-month 2025-07 --end-month 2025-10
    python ncdot_ev_pipeline.py --outdir ../../../data/raw/ncdot-monthly
    python ncdot_ev_pipeline.py --skip-download --out ../../../data/processed/master

Author: Wolfgang Sanyer
License: Polyform Noncommercial 1.0.0 (see LICENSE)
"""

import argparse
import calendar
import re
import sys
from pathlib import Path
from urllib.parse import urljoin

import pandas as pd
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.ncdot.gov/initiatives-policies/environmental/climate-change/Pages/zev-registration-data.aspx"
YEAR_URL_TEMPLATE = "https://www.ncdot.gov/initiatives-policies/environmental/climate-change/Pages/{year}-zev-registration-data.aspx"
YEAR_URL_OVERRIDES = {
    2020: "https://www.ncdot.gov/initiatives-policies/environmental/climate-change/Pages/2020-zev-data.aspx"
}
USER_AGENT = {"User-Agent": "EV-Pulse-NC/1.0"}

FULL_MONTHS = {m.lower(): i for i, m in enumerate(calendar.month_name) if m}
ABBR_MONTHS = {m.lower(): i for i, m in enumerate(calendar.month_abbr) if m}
FULL_MONTHS["sept"] = 9
ABBR_MONTHS["sept"] = 9


def parse_month_string(month_str: str) -> tuple[int, int]:
    """Parse a YYYY-MM month string into (year, month) tuple.

    Args:
        month_str: Month in YYYY-MM format (e.g., '2025-07')

    Returns:
        Tuple of (year, month) as integers

    Raises:
        ValueError: If format is invalid or month is out of range
    """
    match = re.match(r"^(\d{4})-(\d{2})$", month_str)
    if not match:
        raise ValueError(
            f"Invalid month format '{month_str}'. Expected YYYY-MM (e.g., 2025-07)"
        )
    year, month = int(match.group(1)), int(match.group(2))
    if not 1 <= month <= 12:
        raise ValueError(f"Month must be 1-12, got {month}")
    return year, month


def is_in_month_range(
    year: int | None,
    month: int | None,
    start: tuple[int, int] | None,
    end: tuple[int, int] | None,
) -> bool:
    """Check if a (year, month) falls within the specified range.

    Args:
        year: Year to check (or None if unknown)
        month: Month to check (or None if unknown)
        start: Start of range as (year, month) tuple, or None for no lower bound
        end: End of range as (year, month) tuple, or None for no upper bound

    Returns:
        True if within range or if year/month is None (include unknown dates).
        False if outside the specified range.
    """
    if year is None or month is None:
        return True  # Include files with unknown dates
    if start and (year, month) < start:
        return False
    if end and (year, month) > end:
        return False
    return True


def parse_year_month_from_filename(name: str) -> tuple[int | None, int | None]:
    """Extract year and month from NCDOT filename patterns.

    Handles patterns like '2025-june-registration-data.xlsx' or 'june-2025-data.xlsx'.
    Supports both full month names and three-letter abbreviations.

    Args:
        name: Filename string to parse (e.g., '2025-june-registration-data.xlsx')

    Returns:
        Tuple of (year, month) as integers, or (None, None) if pattern not matched.
        Month is 1-indexed (January = 1).
    """
    s = name.lower()
    m1 = re.search(
        r"(\d{4})[-_](jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec|january|february|march|april|may|june|july|august|september|october|november|december)",
        s,
    )
    if m1:
        year = int(m1.group(1))
        mon_txt = m1.group(2)
        mon = ABBR_MONTHS.get(mon_txt, FULL_MONTHS.get(mon_txt))
        return (year, mon)
    m2 = re.search(
        r"(jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec|january|february|march|april|may|june|july|august|september|october|november|december)[-_](\d{4})",
        s,
    )
    if m2:
        mon_txt = m2.group(1)
        year = int(m2.group(2))
        mon = ABBR_MONTHS.get(mon_txt, FULL_MONTHS.get(mon_txt))
        return (year, mon)
    return (None, None)


def get_soup(url: str) -> BeautifulSoup:
    """Fetch URL and return parsed BeautifulSoup object.

    Args:
        url: The URL to fetch

    Returns:
        BeautifulSoup object parsed from the HTML content

    Raises:
        requests.RequestException: If the HTTP request fails
        requests.HTTPError: If the response status code indicates an error
    """
    r = requests.get(url, headers=USER_AGENT, timeout=30)
    r.raise_for_status()
    return BeautifulSoup(r.text, "html.parser")


def discover_year_pages(years: list[int]) -> list[str]:
    """Build list of NCDOT year pages to scrape for xlsx links.

    Constructs URLs for each year's registration data page. Uses override URLs
    for years with non-standard URL patterns (e.g., 2020).

    Args:
        years: List of years to build page URLs for (e.g., [2023, 2024, 2025])

    Returns:
        List of URLs starting with the main hub page, followed by year-specific pages
    """
    urls = [BASE_URL]
    for y in years:
        urls.append(YEAR_URL_OVERRIDES.get(y, YEAR_URL_TEMPLATE.format(year=y)))
    return urls


def discover_xlsx_links(pages: list[str]) -> list[str]:
    """Scrape pages to find all registration-data xlsx download links.

    Parses each page's HTML to extract links to Excel files containing
    registration data. Deduplicates results based on URL path (ignoring query params).

    Args:
        pages: List of NCDOT page URLs to scrape for xlsx links

    Returns:
        Sorted list of unique xlsx download URLs found across all pages
    """
    links = []
    for page in pages:
        try:
            soup = get_soup(page)
            for a in soup.select("a[href]"):
                href = a["href"]
                if (
                    href.lower().endswith(".xlsx")
                    and "registration-data" in href.lower()
                ):
                    links.append(urljoin(page, href))
        except (requests.RequestException, requests.HTTPError) as e:
            print(f"[warn] Failed to parse {page}: {e}", file=sys.stderr)
    seen, unique = set(), []
    for u in links:
        key = u.split("?")[0]
        if key not in seen:
            seen.add(key)
            unique.append(u)
    return sorted(unique)


def download_with_checks(url: str, dest: Path, retries: int = 2) -> bool:
    """Download file with retry logic, skipping if already exists and non-zero.

    Implements idempotent download behavior: existing files with non-zero size
    are skipped. Zero-byte files are re-downloaded. Failed downloads are retried
    up to the specified number of times.

    Args:
        url: URL of the file to download
        dest: Destination Path where the file should be saved
        retries: Maximum number of retry attempts after initial failure (default: 2)

    Returns:
        True if file exists or was downloaded successfully, False on failure
    """
    if dest.exists():
        try:
            if dest.stat().st_size > 0:
                print(f"[skip] {dest.name} (exists, {dest.stat().st_size} bytes)")
                return True
            else:
                print(f"[redo] {dest.name} exists but is 0 bytes; re-downloading...")
        except FileNotFoundError:
            pass

    last_err = None
    with requests.Session() as s:
        s.headers.update(USER_AGENT)
        for attempt in range(1, retries + 2):
            try:
                resp = s.get(url, timeout=60)
                resp.raise_for_status()
                data = resp.content
                if not data:
                    raise RuntimeError("downloaded 0 bytes")
                dest.write_bytes(data)
                print(f"[ok] {dest.name} ({len(data)} bytes)")
                return True
            except Exception as e:
                last_err = e
                print(
                    f"[warn] Attempt {attempt} failed for {dest.name}: {e}",
                    file=sys.stderr,
                )
    print(f"[fail] {dest.name}: {last_err}", file=sys.stderr)
    return False


def filter_links_by_month_range(
    links: list[str],
    start: tuple[int, int] | None,
    end: tuple[int, int] | None,
) -> list[str]:
    """Filter download links to only include those within the month range.

    Args:
        links: List of xlsx file URLs
        start: Start of range as (year, month) tuple, or None for no lower bound
        end: End of range as (year, month) tuple, or None for no upper bound

    Returns:
        Filtered list of URLs whose filenames fall within the month range
    """
    if start is None and end is None:
        return links
    filtered = []
    for url in links:
        fname = Path(url.split("?")[0]).name
        year, month = parse_year_month_from_filename(fname)
        if is_in_month_range(year, month, start, end):
            filtered.append(url)
    return filtered


def download_all(links: list[str], outdir: Path) -> list[Path]:
    """Download all xlsx files to output directory.

    Creates the output directory if it does not exist. Extracts filenames
    from URLs, stripping query parameters.

    Args:
        links: List of xlsx file URLs to download
        outdir: Directory Path where files should be saved

    Returns:
        List of Path objects for successfully downloaded files
    """
    outdir.mkdir(parents=True, exist_ok=True)
    files = []
    for url in links:
        fname = Path(url.split("?")[0]).name
        dest = outdir / fname
        ok = download_with_checks(url, dest)
        if ok:
            files.append(dest)
    return files


def filter_files_by_month_range(
    files: list[Path],
    start: tuple[int, int] | None,
    end: tuple[int, int] | None,
) -> list[Path]:
    """Filter local files to only include those within the month range.

    Args:
        files: List of Path objects pointing to xlsx files
        start: Start of range as (year, month) tuple, or None for no lower bound
        end: End of range as (year, month) tuple, or None for no upper bound

    Returns:
        Filtered list of Path objects whose filenames fall within the month range
    """
    if start is None and end is None:
        return files
    filtered = []
    for path in files:
        year, month = parse_year_month_from_filename(path.name)
        if is_in_month_range(year, month, start, end):
            filtered.append(path)
    return filtered


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Map varying NCDOT column names to standard schema.

    Handles three schema variations:
    - 2018-2019: COUNTY, Fuel.Type.Primary.Description, Total.Vehicles
    - 2020-2021: County, Fuel Type - Primary, Total Vehicles
    - 2022-2025: County, Fuel Type, Count

    Args:
        df: Raw DataFrame from an NCDOT Excel file

    Returns:
        DataFrame with standardized column names (County, BEV, PHEV, etc.)

    Raises:
        ValueError: If County column is not found in the input data
    """
    mapping = {
        "county": "County",
        "electric": "BEV",
        "plug-in hybrid": "PHEV",
        "hybrid": "Hybrid",
        "all hybrids": "AllHybrids",
        "gas": "Gas",
        "diesel": "Diesel",
    }
    cols = {}
    lower_map = {c.lower(): c for c in df.columns}
    for k, tgt in mapping.items():
        cand = None
        for lc, orig in lower_map.items():
            if lc.startswith(k) and "difference" not in lc:
                cand = orig
                break
        cols[tgt] = df[cand] if (cand and cand in df.columns) else pd.NA
    if "County" not in cols or (
        isinstance(cols["County"], pd.Series) and cols["County"].isna().all()
    ):
        county_col = [c for c in df.columns if c.lower() == "county"]
        if not county_col:
            raise ValueError("County column not found.")
        cols["County"] = df[county_col[0]]
    return pd.DataFrame(cols)


def build_master(xlsx_files: list[Path]) -> pd.DataFrame:
    """Consolidate all xlsx files into a single master DataFrame.

    Reads each Excel file, standardizes column names across schema variations,
    extracts date from filename, and combines into a master dataset. Adds
    computed columns for total EV count and EV share.

    Args:
        xlsx_files: List of Path objects pointing to xlsx files to consolidate

    Returns:
        DataFrame with standardized columns (County, BEV, PHEV, Hybrid, etc.),
        sorted by County and Date

    Raises:
        RuntimeError: If no files could be processed successfully
    """
    frames = []
    for p in xlsx_files:
        try:
            try:
                raw = pd.read_excel(p, sheet_name="Results", engine="openpyxl")
            except Exception:
                raw = pd.read_excel(p, engine="openpyxl")
            tidy = standardize_columns(raw)
            tidy = tidy[tidy["County"].astype(str).str.lower() != "total"].copy()
            y, m = parse_year_month_from_filename(p.name)
            dt = pd.NaT if not (y and m) else pd.Timestamp(y, m, 1)
            tidy["Date"] = dt
            frames.append(tidy)
        except Exception as e:
            print(f"[warn] Failed to process {p.name}: {e}", file=sys.stderr)
    if not frames:
        raise RuntimeError("No files processed.")
    master = pd.concat(frames, ignore_index=True)
    for c in ["BEV", "PHEV", "Hybrid", "AllHybrids", "Gas", "Diesel"]:
        master[c] = pd.to_numeric(master[c], errors="coerce")
    master["TotalEV"] = master[["BEV", "PHEV"]].fillna(0).sum(axis=1)
    denom = master[["Gas", "Diesel"]].fillna(0).sum(axis=1) + master["TotalEV"].fillna(
        0
    )
    master["EV_Share"] = (master["TotalEV"] / denom).where(denom > 0)
    master["Methodology_PostMay2025"] = master["Date"] >= pd.Timestamp(2025, 5, 1)
    master = master.sort_values(["County", "Date"]).reset_index(drop=True)
    return master


def qa_report(master: pd.DataFrame) -> str:
    """Generate QA summary report for the master dataset.

    Produces a text report summarizing data coverage, including date range,
    county counts per month, statewide EV totals, and missing value rates.

    Args:
        master: The consolidated master DataFrame to analyze

    Returns:
        Multi-line string containing the QA report summary
    """
    lines = []
    lines.append("=== NCDOT EV Registrations: QA Summary ===")
    months = master["Date"].dropna().dt.to_period("M").unique()
    months = sorted(months)
    if months:
        lines.append(f"Months covered: {months[0]} → {months[-1]}  (n={len(months)})")
    g = master.groupby(master["Date"].dt.to_period("M"))["County"].nunique()
    if not g.empty:
        lines.append(f"Median counties per month: {int(g.median())}")
        lines.append("Last 6 months – counties present:")
        for per, n in g.tail(6).items():
            lines.append(f"  {per}: {n}")
    sw = (
        master.groupby(master["Date"].dt.to_period("M"))[["BEV", "PHEV", "TotalEV"]]
        .sum()
        .tail(6)
    )
    if not sw.empty:
        lines.append("\nStatewide EV totals (last 6 months):")
        lines.append(sw.to_string())
    miss = master.isna().mean().sort_values(ascending=False).head(10)
    lines.append("\nTop missing-value rates:")
    lines.append(miss.to_string())
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="NCDOT EV Registration Data Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --years 2025
  %(prog)s --start-month 2025-07 --end-month 2025-10
  %(prog)s --years 2024 2025 --start-month 2024-06
  %(prog)s --outdir ../../../data/raw/ncdot-monthly
  %(prog)s --skip-download --out ../../../data/processed/master
        """,
    )
    parser.add_argument(
        "--outdir",
        default="../../../data/raw/ncdot-monthly",
        help="Directory for raw xlsx downloads",
    )
    parser.add_argument(
        "--out",
        default="../../../data/processed/nc-ev-registrations-master",
        help="Output path for master dataset (without extension)",
    )
    parser.add_argument(
        "--years",
        nargs="*",
        type=int,
        default=[2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025],
        help="Years to scrape (used to determine which year pages to check)",
    )
    parser.add_argument(
        "--start-month",
        type=str,
        default=None,
        help="Start month in YYYY-MM format (e.g., 2025-07). "
        "Filters to this month and later.",
    )
    parser.add_argument(
        "--end-month",
        type=str,
        default=None,
        help="End month in YYYY-MM format (e.g., 2025-10). "
        "Filters to this month and earlier.",
    )
    parser.add_argument(
        "--skip-download",
        action="store_true",
        help="Skip download, use existing files in outdir",
    )
    args = parser.parse_args()

    # Parse month range arguments
    start_month = None
    end_month = None
    if args.start_month:
        try:
            start_month = parse_month_string(args.start_month)
        except ValueError as e:
            print(f"[error] {e}", file=sys.stderr)
            sys.exit(1)
    if args.end_month:
        try:
            end_month = parse_month_string(args.end_month)
        except ValueError as e:
            print(f"[error] {e}", file=sys.stderr)
            sys.exit(1)

    # Validate that start <= end if both specified
    if start_month and end_month and start_month > end_month:
        print(
            f"[error] --start-month ({args.start_month}) must be before or equal to "
            f"--end-month ({args.end_month})",
            file=sys.stderr,
        )
        sys.exit(1)

    # Log month range if specified
    if start_month or end_month:
        start_str = args.start_month or "beginning"
        end_str = args.end_month or "latest"
        print(f"[i] Filtering to month range: {start_str} to {end_str}")

    outdir = Path(args.outdir)
    if args.skip_download:
        print("[i] Skipping download; using existing files.")
        files = sorted(outdir.glob("*.xlsx"))
        files = filter_files_by_month_range(files, start_month, end_month)
    else:
        pages = discover_year_pages(args.years)
        print(f"[i] Scanning {len(pages)} pages...")
        links = discover_xlsx_links(pages)
        print(f"[i] Found {len(links)} .xlsx links")
        links = filter_links_by_month_range(links, start_month, end_month)
        if start_month or end_month:
            print(f"[i] After month filtering: {len(links)} links")
        files = download_all(links, outdir)

    print(f"[i] Merging {len(files)} files...")
    master = build_master(files)

    out_base = Path(args.out)
    out_base.parent.mkdir(parents=True, exist_ok=True)
    master.to_csv(out_base.with_suffix(".csv"), index=False)
    with pd.ExcelWriter(out_base.with_suffix(".xlsx"), engine="openpyxl") as w:
        master.to_excel(w, index=False, sheet_name="NC_EV_Registrations_Master")

    qa = qa_report(master)
    (out_base.with_suffix(".qa.txt")).write_text(qa, encoding="utf-8")

    print("[done] Wrote:")
    print(" ", out_base.with_suffix(".csv").resolve())
    print(" ", out_base.with_suffix(".xlsx").resolve())
    print(" ", out_base.with_suffix(".qa.txt").resolve())


if __name__ == "__main__":
    main()
