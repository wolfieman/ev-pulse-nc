#!/usr/bin/env python3
"""Phase 3 AFDC EDA: data loading, parsing, and schema constants.

The foundational layer of the AFDC EDA pipeline: loading the raw CSV, deriving
the charging-level classification, and parsing the string-encoded connector
and charging-unit fields. The tables and figures modules build on the prepared
DataFrame produced here. Run via generate_phase3_afdc_eda.py.

Copyright © 2026 Wolfgang Sanyer
Licensed under the Polyform Noncommercial License 1.0.0 (see LICENSE).
"""

from __future__ import annotations

import ast
import json
from pathlib import Path

import numpy as np
import pandas as pd

from evpulse.paths import PROJECT_ROOT

# =============================================================================
# INPUT DATA PATHS
# =============================================================================

AFDC_CSV = (
    PROJECT_ROOT / "data" / "raw" / "afdc-charging-stations-connector-2026-02.csv"
)
CENSUS_ZIP_CSV = PROJECT_ROOT / "data" / "raw" / "nc-zip-population-acs2022.csv"
NC_BOUNDARIES = PROJECT_ROOT / "data" / "raw" / "nc-county-boundaries.geojson"

# =============================================================================
# SCHEMA CONSTANTS
# =============================================================================

# NC bounding box (latitude / longitude)
NC_LAT_MIN, NC_LAT_MAX = 33.84, 36.59
NC_LON_MIN, NC_LON_MAX = -84.32, -75.46

# Non-EV fuel columns that are expected to be 100 % null for this EV-only data
NON_EV_FUEL_PREFIXES = (
    "bd_",
    "cng_",
    "e85_",
    "hy_",
    "lng_",
    "lpg_",
    "ng_",
    "rd_",
)

# EV-relevant columns to audit for missingness
EV_RELEVANT_COLS = [
    "id",
    "station_name",
    "city",
    "state",
    "zip",
    "street_address",
    "latitude",
    "longitude",
    "access_code",
    "facility_type",
    "owner_type_code",
    "ev_network",
    "ev_connector_types",
    "ev_level1_evse_num",
    "ev_level2_evse_num",
    "ev_dc_fast_num",
    "ev_pricing",
    "ev_workplace_charging",
    "ev_network_ids",
    "ev_charging_units",
    "open_date",
    "date_last_confirmed",
    "status_code",
    "groups_with_access_code",
    "maximum_vehicle_class",
    "restricted_access",
    "ev_other_evse",
    "ev_renewable_source",
    "ev_network_web",
]

# =============================================================================
# DATA LOADING & PREPARATION
# =============================================================================


def load_afdc(path: Path) -> pd.DataFrame:
    """Load and lightly prepare the AFDC CSV.

    Args:
        path: Path to the AFDC CSV file.

    Returns:
        DataFrame with basic type casts applied.
    """
    df = pd.read_csv(path, dtype={"zip": str})
    # Ensure zip is zero-padded 5-digit string
    df["zip"] = df["zip"].astype(str).str.zfill(5)
    # Parse open_date
    df["open_date"] = pd.to_datetime(df["open_date"], errors="coerce")
    # Fill NaN port counts with 0 for numeric convenience
    for col in ("ev_level1_evse_num", "ev_level2_evse_num", "ev_dc_fast_num"):
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)
    return df


def derive_charging_level(row: pd.Series) -> str:
    """Classify a station as L1-only, L2-only, DCFC-only, or Mixed.

    Args:
        row: A single row from the AFDC DataFrame.

    Returns:
        Charging level category string.
    """
    has_l1 = row["ev_level1_evse_num"] > 0
    has_l2 = row["ev_level2_evse_num"] > 0
    has_dc = row["ev_dc_fast_num"] > 0
    flags = [has_l1, has_l2, has_dc]
    if sum(flags) > 1:
        return "Mixed"
    if has_dc:
        return "DCFC-only"
    if has_l1:
        return "L1-only"
    return "L2-only"


def parse_connector_types(series: pd.Series) -> pd.Series:
    """Parse the string-encoded list in ev_connector_types.

    Args:
        series: The ev_connector_types column.

    Returns:
        Series of Python lists (empty list when missing).
    """

    def _parse(val: object) -> list[str]:
        if pd.isna(val):
            return []
        try:
            parsed = ast.literal_eval(str(val))
            if isinstance(parsed, list):
                return [str(c).strip() for c in parsed]
        except (ValueError, SyntaxError):
            pass
        return []

    return series.apply(_parse)


def parse_ev_charging_units_power(series: pd.Series) -> pd.Series:
    """Extract max power_kw per station from ev_charging_units JSON.

    The ev_charging_units column contains a list of dicts, each with a
    'connectors' sub-dict mapping connector type to {power_kw, port_count}.

    Args:
        series: The ev_charging_units column.

    Returns:
        Series of max power_kw (float, NaN when unavailable).
    """

    def _extract(val: object) -> float | None:
        if pd.isna(val):
            return np.nan
        try:
            data = ast.literal_eval(str(val))
        except (ValueError, SyntaxError):
            try:
                data = json.loads(str(val))
            except (json.JSONDecodeError, ValueError):
                return np.nan
        # data is a list of charging-unit dicts
        if isinstance(data, list):
            powers: list[float] = []
            for unit in data:
                if not isinstance(unit, dict):
                    continue
                connectors = unit.get("connectors", {})
                if isinstance(connectors, dict):
                    for _ctype, cinfo in connectors.items():
                        if isinstance(cinfo, dict):
                            pw = cinfo.get("power_kw")
                            if pw is not None:
                                powers.append(float(pw))
            return max(powers) if powers else np.nan
        return np.nan

    return series.apply(_extract)
