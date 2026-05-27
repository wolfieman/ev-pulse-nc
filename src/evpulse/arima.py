"""ARIMA forecasting core for NC statewide BEV registrations.

The data loaders, stationarity tests, model fitting, forecasting, and order
selection behind the BEV registration forecast. Plotting, console reporting,
and the CLI live in the analysis script (arima_bev_forecast.py); this module
is the reusable, figure-free modelling core that re-implements the reference
SAS PROC ARIMA model in statsmodels.

Copyright © 2026 Wolfgang Sanyer
Licensed under the Polyform Noncommercial License 1.0.0 (see LICENSE).
"""

# statsmodels ships no type stubs and pandas-stubs types time-series reductions
# (.sum() on a possibly-scalar Series, int() of a reduction, dynamic-label
# df[col] access) as scalar|Series unions. Basic-mode pyright reports those as
# attribute/argument errors that are not real bugs; suppress just those two
# categories for this statistics-wrapper module. All other checks stay on.
# pyright: reportAttributeAccessIssue=false, reportArgumentType=false

from __future__ import annotations

import warnings
from pathlib import Path
from typing import cast

import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA, ARIMAResults
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.stattools import adfuller, kpss

from evpulse.paths import PROJECT_ROOT

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning, module="statsmodels")

# =============================================================================
# Configuration
# =============================================================================

DATA_RAW = PROJECT_ROOT / "data" / "raw"

# Data files
MAIN_DATA_FILE = DATA_RAW / "ncdot-ev-phev-registrations-county-201809-202506.csv"
HOLDOUT_DIR = DATA_RAW / "ncdot-monthly"

# Default ARIMA order - adjust based on your SAS model
DEFAULT_ORDER = (1, 1, 1)  # (p, d, q)


# =============================================================================
# Data Loading Functions
# =============================================================================


def load_training_data(filepath: Path = MAIN_DATA_FILE) -> pd.DataFrame:
    """
    Load and aggregate county-level data to statewide BEV totals.

    Args:
        filepath: Path to the CSV file with county-level registrations

    Returns:
        DataFrame with columns: Month (datetime index), BEV (statewide total)
    """
    print(f"Loading training data from: {filepath}")

    df = pd.read_csv(filepath)

    # Clean numeric columns (they have leading spaces)
    df["Electric"] = pd.to_numeric(
        df["Electric"].astype(str).str.strip(), errors="coerce"
    )
    df["PlugInHybrid"] = pd.to_numeric(
        df["PlugInHybrid"].astype(str).str.strip(), errors="coerce"
    )

    # Aggregate to statewide level
    statewide = (
        df.groupby("Month")
        .agg({"Electric": "sum", "PlugInHybrid": "sum"})
        .reset_index()
    )

    # Rename for clarity
    statewide = statewide.rename(columns={"Electric": "BEV", "PlugInHybrid": "PHEV"})

    # Create proper datetime index
    statewide["Month"] = pd.to_datetime(statewide["Month"] + "-01")
    statewide = statewide.sort_values("Month").reset_index(drop=True)
    statewide = statewide.set_index("Month")

    # Set frequency for time series
    statewide.index = pd.DatetimeIndex(statewide.index, freq="MS")  # Month Start

    print(f"  Loaded {len(statewide)} monthly observations")
    print(
        f"  Date range: {statewide.index.min().strftime('%Y-%m')} "
        f"to {statewide.index.max().strftime('%Y-%m')}"
    )
    print(f"  BEV range: {statewide['BEV'].min():,} to {statewide['BEV'].max():,}")

    return statewide


def load_holdout_data(holdout_dir: Path = HOLDOUT_DIR) -> pd.DataFrame:
    """
    Load holdout/validation data from monthly Excel files.

    Expected files: 2025-july-registration-data.xlsx, etc.

    Returns:
        DataFrame with same structure as training data
    """
    print(f"\nLoading holdout data from: {holdout_dir}")

    month_map = {
        "january": "01",
        "february": "02",
        "march": "03",
        "april": "04",
        "may": "05",
        "june": "06",
        "july": "07",
        "august": "08",
        "september": "09",
        "october": "10",
        "november": "11",
        "december": "12",
    }

    frames = []

    for xlsx_file in sorted(holdout_dir.glob("*.xlsx")):
        # Extract month from filename (e.g., "2025-july-registration-data.xlsx")
        parts = xlsx_file.stem.lower().split("-")
        if len(parts) >= 2:
            year = parts[0]
            month_name = parts[1]
            month_num = month_map.get(month_name)

            if month_num:
                try:
                    # Try "Results" sheet first, then default
                    try:
                        df = pd.read_excel(
                            xlsx_file, sheet_name="Results", engine="openpyxl"
                        )
                    except (KeyError, ValueError):
                        df = pd.read_excel(xlsx_file, engine="openpyxl")

                    # Normalize column names
                    col_lower = {c.lower().strip(): c for c in df.columns}

                    if "county" in col_lower and "electric" in col_lower:
                        county_col = col_lower["county"]
                        electric_col = col_lower["electric"]

                        # Exclude total row
                        df = df[df[county_col].astype(str).str.lower() != "total"]

                        # Sum statewide
                        bev_total = pd.to_numeric(
                            df[electric_col], errors="coerce"
                        ).sum()

                        # Handle PHEV if present
                        phev_col = col_lower.get("plug-in hybrid") or col_lower.get(
                            "pluginhybrid"
                        )
                        phev_total = 0
                        if phev_col:
                            phev_total = pd.to_numeric(
                                df[phev_col], errors="coerce"
                            ).sum()

                        month_str = f"{year}-{month_num}"
                        frames.append(
                            {
                                "Month": pd.to_datetime(month_str + "-01"),
                                "BEV": int(bev_total),
                                "PHEV": int(phev_total),
                            }
                        )
                        print(f"  Loaded {xlsx_file.name}: BEV={int(bev_total):,}")

                except Exception as e:
                    print(f"  [warn] Could not read {xlsx_file.name}: {e}")

    if not frames:
        print("  No holdout data found")
        return pd.DataFrame()

    holdout = pd.DataFrame(frames)
    holdout = holdout.sort_values("Month").reset_index(drop=True)
    holdout = holdout.set_index("Month")
    holdout.index = pd.DatetimeIndex(holdout.index, freq="MS")

    return holdout


# =============================================================================
# Stationarity Tests
# =============================================================================


def test_stationarity(series: pd.Series, name: str = "Series") -> dict:
    """
    Perform stationarity tests (ADF and KPSS).

    Args:
        series: Time series to test
        name: Name for display

    Returns:
        Dictionary with test results
    """
    print(f"\n{'=' * 60}")
    print(f"STATIONARITY TESTS: {name}")
    print("=" * 60)

    results = {}

    # ADF Test (H0: unit root exists, series is non-stationary)
    adf_result: tuple = adfuller(series.dropna(), autolag="AIC")
    results["adf"] = {
        "statistic": adf_result[0],
        "pvalue": adf_result[1],
        "lags": adf_result[2],
        "nobs": adf_result[3],
        "critical_values": adf_result[4],
    }

    print("\nAugmented Dickey-Fuller Test:")
    print(f"  Test Statistic: {adf_result[0]:.4f}")
    print(f"  p-value: {adf_result[1]:.4f}")
    print(f"  Lags Used: {adf_result[2]}")
    print("  Critical Values:")
    for key, value in adf_result[4].items():
        print(f"    {key}: {value:.4f}")

    if adf_result[1] < 0.05:
        print("  --> STATIONARY (reject H0: unit root)")
    else:
        print("  --> NON-STATIONARY (cannot reject H0: unit root)")

    # KPSS Test (H0: series is stationary)
    try:
        kpss_result = kpss(series.dropna(), regression="c", nlags="auto")
        results["kpss"] = {
            "statistic": kpss_result[0],
            "pvalue": kpss_result[1],
            "lags": kpss_result[2],
            "critical_values": kpss_result[3],
        }

        print("\nKPSS Test:")
        print(f"  Test Statistic: {kpss_result[0]:.4f}")
        print(f"  p-value: {kpss_result[1]:.4f}")
        print("  Critical Values:")
        for key, value in kpss_result[3].items():
            print(f"    {key}: {value:.4f}")

        if kpss_result[1] < 0.05:
            print("  --> NON-STATIONARY (reject H0: stationarity)")
        else:
            print("  --> STATIONARY (cannot reject H0: stationarity)")
    except Exception as e:
        print(f"\nKPSS Test: Could not compute ({e})")

    return results


# =============================================================================
# ARIMA Model Fitting
# =============================================================================


def fit_arima_model(
    series: pd.Series,
    order: tuple = DEFAULT_ORDER,
    seasonal_order: tuple | None = None,
    trend: str = "n",
) -> ARIMAResults:
    """
    Fit ARIMA or SARIMAX model to the time series.

    Args:
        series: Time series data (with datetime index)
        order: (p, d, q) order for ARIMA
        seasonal_order: (P, D, Q, s) for SARIMAX, None for non-seasonal
        trend: Trend component ("n", "c", "t", "ct")
               "n" = no trend
               "c" = constant only
               "t" = linear trend only
               "ct" = constant and linear trend

    Returns:
        Fitted model results

    Notes on SAS vs Python differences:
        - SAS PROC ARIMA uses conditional sum of squares (CSS) by default
        - Python statsmodels uses exact maximum likelihood (MLE) by default
        - To match SAS more closely, use method="css" or method="css-mle"
    """
    print(f"\n{'=' * 60}")
    print(f"FITTING ARIMA{order} MODEL")
    if seasonal_order:
        print(f"Seasonal Order: {seasonal_order}")
    print(f"Trend: {trend}")
    print("=" * 60)

    if seasonal_order:
        # Use SARIMAX for seasonal models
        model = SARIMAX(
            series,
            order=order,
            seasonal_order=seasonal_order,
            trend=trend,
            enforce_stationarity=False,
            enforce_invertibility=False,
        )
    else:
        # Use ARIMA for non-seasonal models
        model = ARIMA(
            series,
            order=order,
            trend=trend,
            enforce_stationarity=False,
            enforce_invertibility=False,
        )

    # Fit the model
    # method options: "statespace" (default MLE), "innovations_mle", "hannan_rissanen"
    # For closer SAS match, you might try different methods
    fitted = model.fit(method_kwargs={"warn_convergence": False})

    return cast(ARIMAResults, fitted)


# =============================================================================
# Forecasting
# =============================================================================


def generate_forecast(
    fitted_model, steps: int = 12, alpha: float = 0.05
) -> pd.DataFrame:
    """
    Generate forecasts with confidence intervals.

    Args:
        fitted_model: Fitted ARIMA model
        steps: Number of periods to forecast
        alpha: Significance level for confidence intervals (default 5% -> 95% CI)

    Returns:
        DataFrame with forecast, lower CI, upper CI
    """
    print(f"\n{'=' * 60}")
    print(f"GENERATING {steps}-STEP FORECAST")
    print(f"Confidence Level: {(1 - alpha) * 100:.0f}%")
    print("=" * 60)

    # Get forecast
    forecast_result = fitted_model.get_forecast(steps=steps)

    # Extract point forecasts and confidence intervals
    forecast_mean = forecast_result.predicted_mean
    conf_int = forecast_result.conf_int(alpha=alpha)

    # Create output DataFrame
    forecast_df = pd.DataFrame(
        {
            "Forecast": forecast_mean,
            "Lower_CI": conf_int.iloc[:, 0],
            "Upper_CI": conf_int.iloc[:, 1],
            "CI_Width": conf_int.iloc[:, 1] - conf_int.iloc[:, 0],
        }
    )

    print("\nForecast Results:")
    print("-" * 70)
    print(
        f"{'Month':<12} {'Forecast':>12} {'Lower CI':>12} "
        f"{'Upper CI':>12} {'CI Width':>12}"
    )
    print("-" * 70)

    for idx in forecast_df.index:
        row = forecast_df.loc[idx]
        month_str = idx.strftime("%Y-%m") if hasattr(idx, "strftime") else str(idx)
        print(
            f"{month_str:<12} {row['Forecast']:>12,.0f} {row['Lower_CI']:>12,.0f} "
            f"{row['Upper_CI']:>12,.0f} {row['CI_Width']:>12,.0f}"
        )

    return forecast_df


# =============================================================================
# Auto Order Selection (optional)
# =============================================================================


def auto_select_order(
    series: pd.Series,
    max_p: int = 5,
    max_d: int = 2,
    max_q: int = 5,
    criterion: str = "aic",
) -> tuple:
    """
    Automatically select ARIMA order using information criteria.

    Note: For more sophisticated selection, consider using pmdarima's auto_arima.

    Args:
        series: Time series data
        max_p, max_d, max_q: Maximum orders to consider
        criterion: "aic" or "bic"

    Returns:
        Best (p, d, q) order tuple
    """
    print(f"\n{'=' * 60}")
    print(f"AUTO-SELECTING ARIMA ORDER (criterion={criterion.upper()})")
    print("=" * 60)

    best_score = np.inf
    best_order = (0, 0, 0)
    results = []

    for d in range(max_d + 1):
        for p in range(max_p + 1):
            for q in range(max_q + 1):
                if p == 0 and q == 0:
                    continue
                try:
                    model = ARIMA(series, order=(p, d, q))
                    fitted = model.fit()
                    score = fitted.aic if criterion == "aic" else fitted.bic
                    results.append((p, d, q, score))

                    if score < best_score:
                        best_score = score
                        best_order = (p, d, q)
                except (ValueError, np.linalg.LinAlgError):
                    continue

    # Show top 5 models
    results.sort(key=lambda x: x[3])
    print(f"\nTop 5 models by {criterion.upper()}:")
    print(f"{'Order':<15} {criterion.upper():>12}")
    print("-" * 30)
    for p, d, q, score in results[:5]:
        marker = " <-- BEST" if (p, d, q) == best_order else ""
        print(f"({p}, {d}, {q}){'':<8} {score:>12.2f}{marker}")

    return best_order


# =============================================================================
# SAS vs Python Differences Reference
# =============================================================================
"""
KEY DIFFERENCES BETWEEN SAS PROC ARIMA AND PYTHON STATSMODELS:

1. ESTIMATION METHOD:
   - SAS: Uses Conditional Sum of Squares (CSS) by default, then switches to
          exact Maximum Likelihood (ML) for final estimates
   - Python: Uses exact MLE (state space) by default
   - Impact: Slight differences in parameter estimates, especially for small samples

2. STANDARD ERRORS:
   - SAS: Uses observed information matrix
   - Python: Uses expected information matrix by default
   - Impact: Standard errors may differ slightly

3. INFORMATION CRITERIA (AIC/BIC):
   - SAS: AIC = -2*logL + 2*k (may use different likelihood calculations)
   - Python: AIC = -2*logL + 2*k (uses exact likelihood)
   - Impact: AIC values will differ, but relative rankings usually match

4. CONFIDENCE INTERVALS:
   - SAS: Uses unconditional forecast variance
   - Python: Uses state space forecast variance
   - Impact: CI widths may differ, especially for longer horizons

5. DIFFERENCING:
   - Both handle d>0 similarly, but initial conditions may differ

6. TREND/MEAN SPECIFICATION:
   - SAS: Uses MU option for mean, NOINT to exclude constant
   - Python: Use trend="c" for constant, trend="n" for no constant

TIPS FOR MATCHING SAS RESULTS:
   - Compare coefficient signs and magnitudes (not exact values)
   - Compare AIC rankings rather than absolute values
   - Focus on forecast accuracy metrics (MAPE, MAE) for validation
   - If results differ significantly, check:
     * Are you using the same differencing (d)?
     * Is there a constant/mean term in both?
     * Check for any data preprocessing differences
"""
