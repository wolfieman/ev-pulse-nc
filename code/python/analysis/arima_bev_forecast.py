#!/usr/bin/env python3
"""
ARIMA Model for NC Statewide BEV Registration Forecasting

Re-implementation of SAS ARIMA model in Python using statsmodels.

Data:
    - Training: Monthly observations, Sept 2018 - June 2025 (82 data points)
    - Validation: July-Oct 2025 (4 months holdout)

Usage:
    python arima_bev_forecast.py
    python arima_bev_forecast.py --order 1 1 1
    python arima_bev_forecast.py --auto-select

Author: EV-Pulse-NC Project
"""

import argparse
import warnings
from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

# statsmodels imports
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.stattools import adfuller, kpss

warnings.filterwarnings("ignore")


# =============================================================================
# Configuration
# =============================================================================

# Project paths (relative to this script)
SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent.parent.parent
DATA_RAW = PROJECT_ROOT / "data" / "raw"
DATA_GENERATED = PROJECT_ROOT / "data" / "generated"
OUTPUT_DIR = PROJECT_ROOT / "output" / "arima"

# Data files
MAIN_DATA_FILE = DATA_RAW / "ncdot-ev-phev-registrations-county-201809-202506.csv"
HOLDOUT_DIR = DATA_RAW / "nc-regs-latest-data"

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
    df["Electric"] = pd.to_numeric(df["Electric"].astype(str).str.strip(), errors="coerce")
    df["PlugInHybrid"] = pd.to_numeric(df["PlugInHybrid"].astype(str).str.strip(), errors="coerce")

    # Aggregate to statewide level
    statewide = df.groupby("Month").agg({
        "Electric": "sum",
        "PlugInHybrid": "sum"
    }).reset_index()

    # Rename for clarity
    statewide = statewide.rename(columns={"Electric": "BEV", "PlugInHybrid": "PHEV"})

    # Create proper datetime index
    statewide["Month"] = pd.to_datetime(statewide["Month"] + "-01")
    statewide = statewide.sort_values("Month").reset_index(drop=True)
    statewide = statewide.set_index("Month")

    # Set frequency for time series
    statewide.index = pd.DatetimeIndex(statewide.index, freq="MS")  # Month Start

    print(f"  Loaded {len(statewide)} monthly observations")
    print(f"  Date range: {statewide.index.min().strftime('%Y-%m')} to {statewide.index.max().strftime('%Y-%m')}")
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
        "january": "01", "february": "02", "march": "03", "april": "04",
        "may": "05", "june": "06", "july": "07", "august": "08",
        "september": "09", "october": "10", "november": "11", "december": "12"
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
                        df = pd.read_excel(xlsx_file, sheet_name="Results", engine="openpyxl")
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
                        bev_total = pd.to_numeric(df[electric_col], errors="coerce").sum()

                        # Handle PHEV if present
                        phev_col = col_lower.get("plug-in hybrid") or col_lower.get("pluginhybrid")
                        phev_total = 0
                        if phev_col:
                            phev_total = pd.to_numeric(df[phev_col], errors="coerce").sum()

                        month_str = f"{year}-{month_num}"
                        frames.append({
                            "Month": pd.to_datetime(month_str + "-01"),
                            "BEV": int(bev_total),
                            "PHEV": int(phev_total)
                        })
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
    print(f"\n{'='*60}")
    print(f"STATIONARITY TESTS: {name}")
    print("="*60)

    results = {}

    # ADF Test (H0: unit root exists, series is non-stationary)
    adf_result = adfuller(series.dropna(), autolag="AIC")
    results["adf"] = {
        "statistic": adf_result[0],
        "pvalue": adf_result[1],
        "lags": adf_result[2],
        "nobs": adf_result[3],
        "critical_values": adf_result[4]
    }

    print(f"\nAugmented Dickey-Fuller Test:")
    print(f"  Test Statistic: {adf_result[0]:.4f}")
    print(f"  p-value: {adf_result[1]:.4f}")
    print(f"  Lags Used: {adf_result[2]}")
    print(f"  Critical Values:")
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
            "critical_values": kpss_result[3]
        }

        print(f"\nKPSS Test:")
        print(f"  Test Statistic: {kpss_result[0]:.4f}")
        print(f"  p-value: {kpss_result[1]:.4f}")
        print(f"  Critical Values:")
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
    seasonal_order: Optional[tuple] = None,
    trend: str = "n"
) -> ARIMA:
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
    print(f"\n{'='*60}")
    print(f"FITTING ARIMA{order} MODEL")
    if seasonal_order:
        print(f"Seasonal Order: {seasonal_order}")
    print(f"Trend: {trend}")
    print("="*60)

    if seasonal_order:
        # Use SARIMAX for seasonal models
        model = SARIMAX(
            series,
            order=order,
            seasonal_order=seasonal_order,
            trend=trend,
            enforce_stationarity=False,
            enforce_invertibility=False
        )
    else:
        # Use ARIMA for non-seasonal models
        model = ARIMA(
            series,
            order=order,
            trend=trend,
            enforce_stationarity=False,
            enforce_invertibility=False
        )

    # Fit the model
    # method options: "statespace" (default MLE), "innovations_mle", "hannan_rissanen"
    # For closer SAS match, you might try different methods
    fitted = model.fit(method_kwargs={"warn_convergence": False})

    return fitted


def print_model_summary(fitted_model, sas_comparison: Optional[dict] = None):
    """
    Print model summary with coefficient estimates and fit statistics.

    Args:
        fitted_model: Fitted ARIMA/SARIMAX results
        sas_comparison: Optional dict with SAS results for comparison
    """
    print("\n" + "="*60)
    print("MODEL SUMMARY")
    print("="*60)

    # Full statsmodels summary
    print(fitted_model.summary())

    # Extract key statistics
    print("\n" + "-"*40)
    print("KEY FIT STATISTICS")
    print("-"*40)
    print(f"  AIC:       {fitted_model.aic:.4f}")
    print(f"  BIC:       {fitted_model.bic:.4f}")
    print(f"  HQIC:      {fitted_model.hqic:.4f}")
    print(f"  Log-Lik:   {fitted_model.llf:.4f}")

    # Residual statistics
    resid = fitted_model.resid
    print(f"\n  Residual Std Dev:  {resid.std():.4f}")
    print(f"  Residual Mean:     {resid.mean():.4f}")

    # Coefficient table
    print("\n" + "-"*40)
    print("COEFFICIENT ESTIMATES")
    print("-"*40)
    print(f"{'Parameter':<15} {'Estimate':>12} {'Std Error':>12} {'z-stat':>10} {'p-value':>10}")
    print("-"*60)

    params = fitted_model.params
    stderr = fitted_model.bse
    zvalues = fitted_model.zvalues
    pvalues = fitted_model.pvalues

    for param_name in params.index:
        print(f"{param_name:<15} {params[param_name]:>12.4f} {stderr[param_name]:>12.4f} "
              f"{zvalues[param_name]:>10.4f} {pvalues[param_name]:>10.4f}")

    # SAS comparison if provided
    if sas_comparison:
        print("\n" + "-"*40)
        print("SAS vs PYTHON COMPARISON")
        print("-"*40)
        if "aic" in sas_comparison:
            diff = abs(fitted_model.aic - sas_comparison["aic"])
            print(f"  AIC - SAS: {sas_comparison['aic']:.4f}, Python: {fitted_model.aic:.4f}, Diff: {diff:.4f}")
        if "params" in sas_comparison:
            print("\n  Coefficient Differences:")
            for param, sas_val in sas_comparison["params"].items():
                if param in params.index:
                    py_val = params[param]
                    diff = abs(py_val - sas_val)
                    print(f"    {param}: SAS={sas_val:.4f}, Python={py_val:.4f}, Diff={diff:.4f}")


# =============================================================================
# Model Diagnostics
# =============================================================================

def run_diagnostics(fitted_model, output_dir: Optional[Path] = None):
    """
    Run and display model diagnostics.

    Args:
        fitted_model: Fitted ARIMA results
        output_dir: Optional path to save diagnostic plots
    """
    print("\n" + "="*60)
    print("MODEL DIAGNOSTICS")
    print("="*60)

    resid = fitted_model.resid.dropna()

    # Ljung-Box test for autocorrelation in residuals
    print("\nLjung-Box Test for Residual Autocorrelation:")
    lb_results = acorr_ljungbox(resid, lags=[10, 20], return_df=True)
    print(lb_results)

    # Jarque-Bera test for normality
    jb_stat, jb_pvalue, skew, kurtosis = stats.jarque_bera(resid)
    print(f"\nJarque-Bera Normality Test:")
    print(f"  Statistic: {jb_stat:.4f}")
    print(f"  p-value: {jb_pvalue:.4f}")
    print(f"  Skewness: {skew:.4f}")
    print(f"  Kurtosis: {kurtosis:.4f}")

    if jb_pvalue > 0.05:
        print("  --> Residuals appear normally distributed")
    else:
        print("  --> Residuals may not be normally distributed")

    # Create diagnostic plots
    if output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)

        # Statsmodels built-in diagnostic plot
        fig = fitted_model.plot_diagnostics(figsize=(12, 10))
        fig.suptitle("ARIMA Model Diagnostics", y=1.02)
        fig.tight_layout()
        fig.savefig(output_dir / "diagnostics_panel.png", dpi=150, bbox_inches="tight")
        print(f"\n  Saved: {output_dir / 'diagnostics_panel.png'}")
        plt.close(fig)

        # ACF/PACF of residuals
        fig, axes = plt.subplots(1, 2, figsize=(12, 4))
        plot_acf(resid, ax=axes[0], lags=24, title="Residual ACF")
        plot_pacf(resid, ax=axes[1], lags=24, title="Residual PACF")
        fig.tight_layout()
        fig.savefig(output_dir / "residual_acf_pacf.png", dpi=150)
        print(f"  Saved: {output_dir / 'residual_acf_pacf.png'}")
        plt.close(fig)


# =============================================================================
# Forecasting
# =============================================================================

def generate_forecast(
    fitted_model,
    steps: int = 12,
    alpha: float = 0.05
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
    print(f"\n{'='*60}")
    print(f"GENERATING {steps}-STEP FORECAST")
    print(f"Confidence Level: {(1-alpha)*100:.0f}%")
    print("="*60)

    # Get forecast
    forecast_result = fitted_model.get_forecast(steps=steps)

    # Extract point forecasts and confidence intervals
    forecast_mean = forecast_result.predicted_mean
    conf_int = forecast_result.conf_int(alpha=alpha)

    # Create output DataFrame
    forecast_df = pd.DataFrame({
        "Forecast": forecast_mean,
        "Lower_CI": conf_int.iloc[:, 0],
        "Upper_CI": conf_int.iloc[:, 1],
        "CI_Width": conf_int.iloc[:, 1] - conf_int.iloc[:, 0]
    })

    print("\nForecast Results:")
    print("-"*70)
    print(f"{'Month':<12} {'Forecast':>12} {'Lower CI':>12} {'Upper CI':>12} {'CI Width':>12}")
    print("-"*70)

    for idx in forecast_df.index:
        row = forecast_df.loc[idx]
        month_str = idx.strftime("%Y-%m") if hasattr(idx, "strftime") else str(idx)
        print(f"{month_str:<12} {row['Forecast']:>12,.0f} {row['Lower_CI']:>12,.0f} "
              f"{row['Upper_CI']:>12,.0f} {row['CI_Width']:>12,.0f}")

    return forecast_df


# =============================================================================
# Validation Against Holdout Data
# =============================================================================

def validate_forecast(
    forecast_df: pd.DataFrame,
    actual_df: pd.DataFrame,
    output_dir: Optional[Path] = None
) -> dict:
    """
    Validate forecasts against actual holdout data.

    Args:
        forecast_df: DataFrame with Forecast column
        actual_df: DataFrame with actual BEV values
        output_dir: Optional path to save validation plots

    Returns:
        Dictionary with validation metrics
    """
    print("\n" + "="*60)
    print("FORECAST VALIDATION (Holdout Period)")
    print("="*60)

    # Align forecast and actual data
    common_idx = forecast_df.index.intersection(actual_df.index)

    if len(common_idx) == 0:
        print("No overlapping dates between forecast and actual data")
        return {}

    forecast_values = forecast_df.loc[common_idx, "Forecast"]
    actual_values = actual_df.loc[common_idx, "BEV"]

    # Calculate metrics
    errors = actual_values - forecast_values
    abs_errors = np.abs(errors)
    pct_errors = abs_errors / actual_values * 100

    metrics = {
        "n_periods": len(common_idx),
        "MAE": abs_errors.mean(),
        "RMSE": np.sqrt((errors ** 2).mean()),
        "MAPE": pct_errors.mean(),
        "MedAPE": pct_errors.median(),
        "MPE": (errors / actual_values * 100).mean(),  # Mean Percentage Error (bias)
        "MaxAPE": pct_errors.max()
    }

    print(f"\nValidation Period: {common_idx.min().strftime('%Y-%m')} to {common_idx.max().strftime('%Y-%m')}")
    print(f"Number of Periods: {metrics['n_periods']}")

    print("\nAccuracy Metrics:")
    print(f"  MAE (Mean Absolute Error):       {metrics['MAE']:,.0f} registrations")
    print(f"  RMSE (Root Mean Squared Error):  {metrics['RMSE']:,.0f} registrations")
    print(f"  MAPE (Mean Abs % Error):         {metrics['MAPE']:.2f}%")
    print(f"  MedAPE (Median Abs % Error):     {metrics['MedAPE']:.2f}%")
    print(f"  MPE (Mean % Error - Bias):       {metrics['MPE']:.2f}%")
    print(f"  MaxAPE (Maximum Abs % Error):    {metrics['MaxAPE']:.2f}%")

    # Period-by-period comparison
    print("\nPeriod-by-Period Comparison:")
    print("-"*80)
    print(f"{'Month':<12} {'Actual':>12} {'Forecast':>12} {'Error':>12} {'APE %':>10} {'In CI?':>10}")
    print("-"*80)

    for idx in common_idx:
        actual = actual_values.loc[idx]
        forecast = forecast_values.loc[idx]
        error = actual - forecast
        ape = abs(error) / actual * 100

        # Check if actual is within confidence interval
        lower = forecast_df.loc[idx, "Lower_CI"]
        upper = forecast_df.loc[idx, "Upper_CI"]
        in_ci = "Yes" if lower <= actual <= upper else "No"

        month_str = idx.strftime("%Y-%m")
        print(f"{month_str:<12} {actual:>12,.0f} {forecast:>12,.0f} {error:>12,.0f} {ape:>10.2f} {in_ci:>10}")

    # CI coverage
    in_ci_count = sum(1 for idx in common_idx
                      if forecast_df.loc[idx, "Lower_CI"] <= actual_df.loc[idx, "BEV"] <= forecast_df.loc[idx, "Upper_CI"])
    metrics["CI_Coverage"] = in_ci_count / len(common_idx) * 100
    print(f"\nConfidence Interval Coverage: {metrics['CI_Coverage']:.1f}% ({in_ci_count}/{len(common_idx)} periods)")

    # Create validation plot
    if output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)

        fig, ax = plt.subplots(figsize=(10, 6))

        x = range(len(common_idx))
        ax.bar(x, actual_values.values, width=0.4, label="Actual", alpha=0.8, color="steelblue")
        ax.bar([i + 0.4 for i in x], forecast_values.values, width=0.4, label="Forecast", alpha=0.8, color="coral")

        # Add error bars for CI
        ci_errors = [
            [forecast_values.values - forecast_df.loc[common_idx, "Lower_CI"].values],
            [forecast_df.loc[common_idx, "Upper_CI"].values - forecast_values.values]
        ]
        ax.errorbar([i + 0.4 for i in x], forecast_values.values,
                    yerr=[forecast_df.loc[common_idx, "Lower_CI"].values - forecast_values.values + forecast_values.values - forecast_df.loc[common_idx, "Lower_CI"].values,
                          forecast_df.loc[common_idx, "Upper_CI"].values - forecast_values.values],
                    fmt="none", color="black", capsize=3)

        ax.set_xlabel("Month")
        ax.set_ylabel("BEV Registrations")
        ax.set_title(f"Forecast Validation: MAPE = {metrics['MAPE']:.2f}%")
        ax.set_xticks([i + 0.2 for i in x])
        ax.set_xticklabels([idx.strftime("%Y-%m") for idx in common_idx])
        ax.legend()
        ax.grid(axis="y", alpha=0.3)

        fig.tight_layout()
        fig.savefig(output_dir / "forecast_validation.png", dpi=150)
        print(f"\n  Saved: {output_dir / 'forecast_validation.png'}")
        plt.close(fig)

    return metrics


# =============================================================================
# Visualization
# =============================================================================

def plot_forecast(
    train_data: pd.DataFrame,
    forecast_df: pd.DataFrame,
    fitted_model,
    actual_holdout: Optional[pd.DataFrame] = None,
    output_dir: Optional[Path] = None
):
    """
    Create forecast visualization with historical data and predictions.
    """
    if output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(14, 7))

    # Historical data
    ax.plot(train_data.index, train_data["BEV"],
            label="Historical Data", color="steelblue", linewidth=1.5)

    # Fitted values (in-sample)
    fitted_values = fitted_model.fittedvalues
    ax.plot(fitted_values.index, fitted_values,
            label="Fitted Values", color="green", linewidth=1, alpha=0.7, linestyle="--")

    # Forecast
    ax.plot(forecast_df.index, forecast_df["Forecast"],
            label="Forecast", color="coral", linewidth=2, marker="o", markersize=4)

    # Confidence interval
    ax.fill_between(forecast_df.index,
                    forecast_df["Lower_CI"],
                    forecast_df["Upper_CI"],
                    color="coral", alpha=0.2, label="95% CI")

    # Actual holdout data if available
    if actual_holdout is not None and not actual_holdout.empty:
        ax.scatter(actual_holdout.index, actual_holdout["BEV"],
                   color="red", s=80, zorder=5, label="Actual (Holdout)", marker="D")

    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("BEV Registrations", fontsize=12)
    ax.set_title("NC Statewide BEV Registrations: ARIMA Forecast", fontsize=14)
    ax.legend(loc="upper left")
    ax.grid(alpha=0.3)

    # Format y-axis with thousands separator
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: format(int(x), ',')))

    fig.tight_layout()

    if output_dir:
        fig.savefig(output_dir / "forecast_plot.png", dpi=150, bbox_inches="tight")
        print(f"\n  Saved: {output_dir / 'forecast_plot.png'}")

    plt.close(fig)


# =============================================================================
# Auto Order Selection (optional)
# =============================================================================

def auto_select_order(
    series: pd.Series,
    max_p: int = 5,
    max_d: int = 2,
    max_q: int = 5,
    criterion: str = "aic"
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
    print(f"\n{'='*60}")
    print(f"AUTO-SELECTING ARIMA ORDER (criterion={criterion.upper()})")
    print("="*60)

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
                except:
                    continue

    # Show top 5 models
    results.sort(key=lambda x: x[3])
    print(f"\nTop 5 models by {criterion.upper()}:")
    print(f"{'Order':<15} {criterion.upper():>12}")
    print("-"*30)
    for p, d, q, score in results[:5]:
        marker = " <-- BEST" if (p, d, q) == best_order else ""
        print(f"({p}, {d}, {q}){'':<8} {score:>12.2f}{marker}")

    return best_order


# =============================================================================
# Main Execution
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="ARIMA Model for NC BEV Registration Forecasting",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "--order", "-o",
        nargs=3,
        type=int,
        default=list(DEFAULT_ORDER),
        metavar=("P", "D", "Q"),
        help=f"ARIMA order (p, d, q). Default: {DEFAULT_ORDER}"
    )

    parser.add_argument(
        "--auto-select",
        action="store_true",
        help="Automatically select best ARIMA order"
    )

    parser.add_argument(
        "--forecast-steps", "-f",
        type=int,
        default=12,
        help="Number of months to forecast (default: 12)"
    )

    parser.add_argument(
        "--no-plots",
        action="store_true",
        help="Skip generating plots"
    )

    parser.add_argument(
        "--sas-aic",
        type=float,
        help="SAS AIC value for comparison"
    )

    args = parser.parse_args()

    # Setup output directory
    output_dir = OUTPUT_DIR if not args.no_plots else None

    print("="*70)
    print("NC STATEWIDE BEV REGISTRATION ARIMA FORECASTING")
    print("="*70)

    # Load data
    train_data = load_training_data()
    holdout_data = load_holdout_data()

    # Extract BEV series for modeling
    bev_series = train_data["BEV"]

    # Stationarity tests
    test_stationarity(bev_series, "BEV (Original)")
    test_stationarity(bev_series.diff().dropna(), "BEV (First Difference)")

    # Determine ARIMA order
    if args.auto_select:
        order = auto_select_order(bev_series)
    else:
        order = tuple(args.order)

    # Fit model
    fitted_model = fit_arima_model(bev_series, order=order)

    # Model summary
    sas_comparison = None
    if args.sas_aic:
        sas_comparison = {"aic": args.sas_aic}
    print_model_summary(fitted_model, sas_comparison)

    # Diagnostics
    run_diagnostics(fitted_model, output_dir)

    # Generate forecast
    forecast_df = generate_forecast(fitted_model, steps=args.forecast_steps)

    # Validate against holdout if available
    if not holdout_data.empty:
        metrics = validate_forecast(forecast_df, holdout_data, output_dir)

    # Create forecast plot
    if output_dir:
        plot_forecast(train_data, forecast_df, fitted_model, holdout_data, output_dir)

    print("\n" + "="*70)
    print("ANALYSIS COMPLETE")
    print("="*70)

    if output_dir:
        print(f"\nOutput files saved to: {output_dir}")


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


if __name__ == "__main__":
    main()
