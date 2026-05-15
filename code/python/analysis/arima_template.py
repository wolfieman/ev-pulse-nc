#!/usr/bin/env python3
"""
Minimal ARIMA Template for SAS Replication

This is a simplified template showing the essential steps to replicate
a SAS ARIMA model in Python. Use this as a quick reference.

For full implementation with diagnostics and validation, see:
    arima_bev_forecast.py

Author: Wolfgang Sanyer
License: Polyform Noncommercial 1.0.0 (see LICENSE)
"""

import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX

# =============================================================================
# 1. LOAD AND PREPARE DATA
# =============================================================================


def prepare_time_series(df: pd.DataFrame, date_col: str, value_col: str) -> pd.Series:
    """
    Prepare data for ARIMA modeling.

    Key requirements:
    - DatetimeIndex with proper frequency
    - No missing values in the series

    Args:
        df: DataFrame containing the time series data
        date_col: Name of the column containing date values
        value_col: Name of the column containing the values to forecast

    Returns:
        Series with DatetimeIndex set to month-start frequency
    """
    # Create datetime index
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])
    df = df.set_index(date_col)
    df = df.sort_index()

    # Extract series and set frequency
    series = df[value_col]

    # Set frequency - critical for forecasting
    # Common frequencies: "MS" (month start), "M" (month end), "D" (daily)
    series.index = pd.DatetimeIndex(series.index, freq="MS")

    return series


# =============================================================================
# 2. FIT ARIMA MODEL
# =============================================================================


def fit_arima(series: pd.Series, order: tuple, trend: str = "n"):
    """
    Fit ARIMA model.

    Args:
        series: Time series with DatetimeIndex
        order: (p, d, q) tuple
            p = AR order (autoregressive terms)
            d = differencing order
            q = MA order (moving average terms)
        trend: "n" (none), "c" (constant), "t" (linear), "ct" (both)

    Returns:
        Fitted model results
    """
    model = ARIMA(
        series,
        order=order,
        trend=trend,
        enforce_stationarity=False,  # Allow non-stationary parameters
        enforce_invertibility=False,  # Allow non-invertible parameters
    )

    # Fit using exact MLE (default)
    results = model.fit()

    return results


def fit_sarima(
    series: pd.Series, order: tuple, seasonal_order: tuple, trend: str = "n"
):
    """
    Fit Seasonal ARIMA (SARIMA) model.

    Args:
        series: Time series with DatetimeIndex
        order: (p, d, q) non-seasonal order
        seasonal_order: (P, D, Q, s) seasonal order
            P = seasonal AR order
            D = seasonal differencing
            Q = seasonal MA order
            s = seasonal period (12 for monthly data with yearly seasonality)
        trend: "n" (none), "c" (constant), "t" (linear), "ct" (both)

    Returns:
        Fitted SARIMAX model results object
    """
    model = SARIMAX(
        series,
        order=order,
        seasonal_order=seasonal_order,
        trend=trend,
        enforce_stationarity=False,
        enforce_invertibility=False,
    )

    results = model.fit(disp=False)

    return results


# =============================================================================
# 3. EXTRACT MODEL INFORMATION
# =============================================================================


def get_model_info(results) -> dict:
    """
    Extract key model information comparable to SAS output.

    Args:
        results: Fitted ARIMA/SARIMAX model results object

    Returns:
        Dictionary containing model information criteria, parameters,
        standard errors, p-values, and residual diagnostics
    """
    info = {
        # Information criteria
        "aic": results.aic,
        "bic": results.bic,
        "hqic": results.hqic,
        "log_likelihood": results.llf,
        # Parameters
        "params": results.params.to_dict(),
        "std_errors": results.bse.to_dict(),
        "pvalues": results.pvalues.to_dict(),
        # Residual diagnostics
        "residual_variance": results.resid.var(),
        "residual_std": results.resid.std(),
        # Number of observations
        "nobs": results.nobs,
    }

    return info


# =============================================================================
# 4. GENERATE FORECASTS
# =============================================================================


def forecast(results, steps: int, alpha: float = 0.05) -> pd.DataFrame:
    """
    Generate forecasts with confidence intervals.

    Args:
        results: Fitted model results
        steps: Number of periods ahead to forecast
        alpha: Significance level (0.05 = 95% CI)

    Returns:
        DataFrame with forecast, lower_ci, upper_ci
    """
    # Get forecast object
    forecast_obj = results.get_forecast(steps=steps)

    # Extract values
    forecast_mean = forecast_obj.predicted_mean
    conf_int = forecast_obj.conf_int(alpha=alpha)

    # Build output DataFrame
    output = pd.DataFrame(
        {
            "forecast": forecast_mean,
            "lower_ci": conf_int.iloc[:, 0],
            "upper_ci": conf_int.iloc[:, 1],
        }
    )

    return output


# =============================================================================
# 5. CALCULATE ACCURACY METRICS
# =============================================================================


def calculate_accuracy(actual: pd.Series, predicted: pd.Series) -> dict:
    """
    Calculate forecast accuracy metrics.

    Use these to compare Python results with SAS holdout validation.

    Args:
        actual: Series of actual observed values with DatetimeIndex
        predicted: Series of predicted/forecasted values with DatetimeIndex

    Returns:
        Dictionary containing MAE, RMSE, MAPE, MedAPE, MPE, and count (n)
    """
    # Align series
    common_idx = actual.index.intersection(predicted.index)
    actual = actual.loc[common_idx]
    predicted = predicted.loc[common_idx]

    errors = actual - predicted
    abs_errors = np.abs(errors)
    pct_errors = abs_errors / actual * 100

    metrics = {
        "MAE": abs_errors.mean(),
        "RMSE": np.sqrt((errors**2).mean()),
        "MAPE": pct_errors.mean(),
        "MedAPE": pct_errors.median(),
        "MPE": (errors / actual * 100).mean(),  # Bias indicator
        "n": len(common_idx),
    }

    return metrics


# =============================================================================
# EXAMPLE USAGE
# =============================================================================

if __name__ == "__main__":
    # Example with synthetic data
    # Replace with your actual data loading

    # Create sample monthly data
    dates = pd.date_range("2018-09-01", "2025-06-01", freq="MS")
    np.random.seed(42)
    values = 5000 + np.cumsum(np.random.randn(len(dates)) * 500 + 300)

    df = pd.DataFrame({"date": dates, "bev": values})

    # Prepare series
    series = prepare_time_series(df, "date", "bev")
    print(f"Series shape: {series.shape}")
    print(f"Date range: {series.index.min()} to {series.index.max()}")

    # Fit ARIMA(1,1,1) - adjust based on your SAS model
    results = fit_arima(series, order=(1, 1, 1), trend="n")

    # Print summary (matches SAS PROC ARIMA output structure)
    print("\n" + "=" * 60)
    print("MODEL SUMMARY")
    print("=" * 60)
    print(results.summary())

    # Get structured info
    info = get_model_info(results)
    print(f"\nAIC: {info['aic']:.2f}")
    print(f"BIC: {info['bic']:.2f}")
    print(f"Parameters: {info['params']}")

    # Generate 4-month forecast (for holdout validation)
    fc = forecast(results, steps=4)
    print("\n" + "=" * 60)
    print("FORECAST")
    print("=" * 60)
    print(fc)

    # If you have actual holdout data:
    # actual_holdout = pd.Series([...], index=fc.index)
    # metrics = calculate_accuracy(actual_holdout, fc["forecast"])
    # print(f"MAPE: {metrics['MAPE']:.2f}%")


# =============================================================================
# SAS TO PYTHON TRANSLATION GUIDE
# =============================================================================
"""
SAS PROC ARIMA                          Python statsmodels
----------------                        ------------------
proc arima data=mydata;                 model = ARIMA(series, order=(p,d,q))
  identify var=y(1);                    # d=1 in order tuple
  estimate p=1 q=1;                     # p=1, q=1 in order tuple
  forecast lead=12 out=forecast;        results.get_forecast(steps=12)
run;

SAS Options:
  NOCONSTANT / NOINT                    trend="n"
  MU (include mean)                     trend="c"
  METHOD=ML                             Default in statsmodels
  METHOD=CLS (conditional LS)           Not directly available, but similar

SAS Output vs Python:
  Parameter Estimates table             results.params, results.bse, results.pvalues
  AIC/SBC (BIC)                         results.aic, results.bic
  Residual diagnostics                  results.resid, acorr_ljungbox()
  Forecast values                       results.get_forecast().predicted_mean
  Confidence limits                     results.get_forecast().conf_int()

Common order specifications:
  ARIMA(1,1,1)  - order=(1,1,1)         One AR, one difference, one MA
  ARIMA(2,1,0)  - order=(2,1,0)         Two AR, one difference, no MA
  ARIMA(0,1,1)  - order=(0,1,1)         No AR, one difference, one MA (random walk + noise)
  ARIMA(1,2,1)  - order=(1,2,1)         One AR, two differences, one MA

Seasonal ARIMA (SARIMA):
  SAS: estimate p=1 q=1 noint (12)      Python: SARIMAX(series, order=(1,0,1),
       input=(1 12 2 12);                        seasonal_order=(1,1,1,12))
"""
