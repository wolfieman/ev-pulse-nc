#!/usr/bin/env python3
"""Phase 3 AFDC EDA: CSV table outputs.

Aggregation tables derived from the prepared AFDC DataFrame: per-column
profile, station/port counts by charging level, network, and ZIP, plus a
data-quality flag list. Run via generate_phase3_afdc_eda.py.

Author: Wolfgang Sanyer
License: Polyform Noncommercial 1.0.0 (see LICENSE)
Date: 2026
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from phase3_afdc_eda_prep import (
    NC_LAT_MAX,
    NC_LAT_MIN,
    NC_LON_MAX,
    NC_LON_MIN,
)


def write_column_profile(df: pd.DataFrame, out_dir: Path) -> Path:
    """Write per-column profile CSV.

    Args:
        df: AFDC DataFrame.
        out_dir: Output directory.

    Returns:
        Path to the written CSV.
    """
    # Exclude derived list/object columns that break nunique
    exclude = {"connector_list", "max_power_kw"}
    cols = [c for c in df.columns if c not in exclude]
    sub = df[cols]
    profile = pd.DataFrame(
        {
            "column": sub.columns,
            "dtype": sub.dtypes.astype(str).values,
            "non_null_count": sub.notna().sum().values,
            "null_count": sub.isna().sum().values,
            "null_pct": (sub.isna().sum() / len(sub) * 100).round(2).values,
            "unique_count": sub.nunique().values,
        }
    )
    path = out_dir / "afdc-eda-column-profile.csv"
    profile.to_csv(path, index=False)
    return path


def write_stations_by_level(df: pd.DataFrame, out_dir: Path) -> Path:
    """Write station and port counts by charging level.

    Args:
        df: AFDC DataFrame with charging_level column.
        out_dir: Output directory.

    Returns:
        Path to the written CSV.
    """
    agg = (
        df.groupby("charging_level")
        .agg(
            station_count=("id", "count"),
            l1_ports=("ev_level1_evse_num", "sum"),
            l2_ports=("ev_level2_evse_num", "sum"),
            dcfc_ports=("ev_dc_fast_num", "sum"),
        )
        .reset_index()
    )
    agg["total_ports"] = agg["l1_ports"] + agg["l2_ports"] + agg["dcfc_ports"]
    path = out_dir / "afdc-eda-stations-by-level.csv"
    agg.to_csv(path, index=False)
    return path


def write_stations_by_network(df: pd.DataFrame, out_dir: Path) -> Path:
    """Write station and port counts by ev_network.

    Args:
        df: AFDC DataFrame.
        out_dir: Output directory.

    Returns:
        Path to the written CSV.
    """
    agg = (
        df.groupby("ev_network")
        .agg(
            station_count=("id", "count"),
            l2_ports=("ev_level2_evse_num", "sum"),
            dcfc_ports=("ev_dc_fast_num", "sum"),
        )
        .reset_index()
    )
    agg["total_ports"] = agg["l2_ports"] + agg["dcfc_ports"]
    agg = agg.sort_values("station_count", ascending=False).reset_index(drop=True)
    path = out_dir / "afdc-eda-stations-by-network.csv"
    agg.to_csv(path, index=False)
    return path


def write_stations_by_zip(df: pd.DataFrame, out_dir: Path) -> Path:
    """Write per-ZIP station and port counts.

    Args:
        df: AFDC DataFrame.
        out_dir: Output directory.

    Returns:
        Path to the written CSV.
    """
    agg = (
        df.groupby("zip")
        .agg(
            station_count=("id", "count"),
            l2_ports=("ev_level2_evse_num", "sum"),
            dcfc_ports=("ev_dc_fast_num", "sum"),
        )
        .reset_index()
    )
    agg["total_ports"] = agg["l2_ports"] + agg["dcfc_ports"]
    agg = agg.sort_values("station_count", ascending=False).reset_index(drop=True)
    path = out_dir / "afdc-eda-stations-by-zip.csv"
    agg.to_csv(path, index=False)
    return path


def write_quality_flags(df: pd.DataFrame, out_dir: Path) -> Path:
    """Flag rows with quality issues and write CSV.

    Flags:
        - out-of-bounds lat/lon (outside NC bounding box)
        - zero total ports
        - near-duplicate street addresses (case-insensitive)

    Args:
        df: AFDC DataFrame.
        out_dir: Output directory.

    Returns:
        Path to the written CSV.
    """
    flags: list[pd.DataFrame] = []

    # Out-of-bounds coords
    oob = df[
        (df["latitude"] < NC_LAT_MIN)
        | (df["latitude"] > NC_LAT_MAX)
        | (df["longitude"] < NC_LON_MIN)
        | (df["longitude"] > NC_LON_MAX)
    ].copy()
    if len(oob):
        oob["flag"] = "out_of_bounds_coords"
        flags.append(oob[["id", "station_name", "latitude", "longitude", "flag"]])

    # Zero total ports
    df["_total_ports"] = (
        df["ev_level1_evse_num"] + df["ev_level2_evse_num"] + df["ev_dc_fast_num"]
    )
    zero = df[df["_total_ports"] == 0].copy()
    if len(zero):
        zero["flag"] = "zero_ports"
        flags.append(zero[["id", "station_name", "latitude", "longitude", "flag"]])
    df.drop(columns="_total_ports", inplace=True)

    # Near-duplicate addresses (same normalised address + city)
    addr_norm = (
        df["street_address"].str.lower().str.strip()
        + "|"
        + df["city"].str.lower().str.strip()
    )
    dup_mask = addr_norm.duplicated(keep=False)
    dups = df[dup_mask].copy()
    if len(dups):
        dups["flag"] = "near_duplicate_address"
        flags.append(dups[["id", "station_name", "latitude", "longitude", "flag"]])

    if flags:
        result = pd.concat(flags, ignore_index=True)
    else:
        result = pd.DataFrame(
            columns=["id", "station_name", "latitude", "longitude", "flag"]
        )
    path = out_dir / "afdc-eda-quality-flags.csv"
    result.to_csv(path, index=False)
    return path
