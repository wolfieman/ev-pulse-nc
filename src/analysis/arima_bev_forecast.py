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

The data loading, stationarity tests, model fitting, forecasting, and order
selection live in evpulse.arima; this script handles console reporting,
diagnostics/forecast plotting, and the command-line interface.

Author: Wolfgang Sanyer
License: Polyform Noncommercial 1.0.0 (see LICENSE)
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.stats.stattools import jarque_bera

from evpulse.arima import (
    DEFAULT_ORDER,
    auto_select_order,
    fit_arima_model,
    generate_forecast,
    load_holdout_data,
    load_training_data,
    test_stationarity,
)
from evpulse.paths import PROJECT_ROOT

# =============================================================================
# Configuration
# =============================================================================

OUTPUT_DIR = PROJECT_ROOT / "output" / "arima"


# =============================================================================
# Model Summary Reporting
# =============================================================================


def print_model_summary(fitted_model, sas_comparison: dict | None = None) -> None:
    """
    Print model summary with coefficient estimates and fit statistics.

    Args:
        fitted_model: Fitted ARIMA/SARIMAX results
        sas_comparison: Optional dict with SAS results for comparison
    """
    print("\n" + "=" * 60)
    print("MODEL SUMMARY")
    print("=" * 60)

    # Full statsmodels summary
    print(fitted_model.summary())

    # Extract key statistics
    print("\n" + "-" * 40)
    print("KEY FIT STATISTICS")
    print("-" * 40)
    print(f"  AIC:       {fitted_model.aic:.4f}")
    print(f"  BIC:       {fitted_model.bic:.4f}")
    print(f"  HQIC:      {fitted_model.hqic:.4f}")
    print(f"  Log-Lik:   {fitted_model.llf:.4f}")

    # Residual statistics
    resid = fitted_model.resid
    print(f"\n  Residual Std Dev:  {resid.std():.4f}")
    print(f"  Residual Mean:     {resid.mean():.4f}")

    # Coefficient table
    print("\n" + "-" * 40)
    print("COEFFICIENT ESTIMATES")
    print("-" * 40)
    print(
        f"{'Parameter':<15} {'Estimate':>12} {'Std Error':>12} "
        f"{'z-stat':>10} {'p-value':>10}"
    )
    print("-" * 60)

    params = fitted_model.params
    stderr = fitted_model.bse
    zvalues = fitted_model.zvalues
    pvalues = fitted_model.pvalues

    for param_name in params.index:
        print(
            f"{param_name:<15} {params[param_name]:>12.4f} {stderr[param_name]:>12.4f} "
            f"{zvalues[param_name]:>10.4f} {pvalues[param_name]:>10.4f}"
        )

    # SAS comparison if provided
    if sas_comparison:
        print("\n" + "-" * 40)
        print("SAS vs PYTHON COMPARISON")
        print("-" * 40)
        if "aic" in sas_comparison:
            diff = abs(fitted_model.aic - sas_comparison["aic"])
            print(
                f"  AIC - SAS: {sas_comparison['aic']:.4f}, "
                f"Python: {fitted_model.aic:.4f}, Diff: {diff:.4f}"
            )
        if "params" in sas_comparison:
            print("\n  Coefficient Differences:")
            for param, sas_val in sas_comparison["params"].items():
                if param in params.index:
                    py_val = params[param]
                    diff = abs(py_val - sas_val)
                    print(
                        f"    {param}: SAS={sas_val:.4f}, "
                        f"Python={py_val:.4f}, Diff={diff:.4f}"
                    )


# =============================================================================
# Model Diagnostics
# =============================================================================


def run_diagnostics(fitted_model, output_dir: Path | None = None) -> None:
    """
    Run and display model diagnostics.

    Args:
        fitted_model: Fitted ARIMA results
        output_dir: Optional path to save diagnostic plots
    """
    print("\n" + "=" * 60)
    print("MODEL DIAGNOSTICS")
    print("=" * 60)

    resid = fitted_model.resid.dropna()

    # Ljung-Box test for autocorrelation in residuals
    print("\nLjung-Box Test for Residual Autocorrelation:")
    lb_results = acorr_ljungbox(resid, lags=[10, 20], return_df=True)
    print(lb_results)

    # Jarque-Bera test for normality (statsmodels returns skew & kurtosis too)
    jb_stat, jb_pvalue, skew, kurtosis = jarque_bera(resid)
    print("\nJarque-Bera Normality Test:")
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
# Validation Against Holdout Data
# =============================================================================


def validate_forecast(
    forecast_df: pd.DataFrame, actual_df: pd.DataFrame, output_dir: Path | None = None
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
    print("\n" + "=" * 60)
    print("FORECAST VALIDATION (Holdout Period)")
    print("=" * 60)

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
        "RMSE": np.sqrt((errors**2).mean()),
        "MAPE": pct_errors.mean(),
        "MedAPE": pct_errors.median(),
        "MPE": (errors / actual_values * 100).mean(),  # Mean Percentage Error (bias)
        "MaxAPE": pct_errors.max(),
    }

    print(
        f"\nValidation Period: {common_idx.min().strftime('%Y-%m')} "
        f"to {common_idx.max().strftime('%Y-%m')}"
    )
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
    print("-" * 80)
    print(
        f"{'Month':<12} {'Actual':>12} {'Forecast':>12} "
        f"{'Error':>12} {'APE %':>10} {'In CI?':>10}"
    )
    print("-" * 80)

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
        print(
            f"{month_str:<12} {actual:>12,.0f} {forecast:>12,.0f} "
            f"{error:>12,.0f} {ape:>10.2f} {in_ci:>10}"
        )

    # CI coverage
    in_ci_count = sum(
        1
        for idx in common_idx
        if forecast_df.loc[idx, "Lower_CI"]
        <= actual_df.loc[idx, "BEV"]
        <= forecast_df.loc[idx, "Upper_CI"]
    )
    metrics["CI_Coverage"] = in_ci_count / len(common_idx) * 100
    print(
        f"\nConfidence Interval Coverage: {metrics['CI_Coverage']:.1f}% "
        f"({in_ci_count}/{len(common_idx)} periods)"
    )

    # Create validation plot
    if output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)

        fig, ax = plt.subplots(figsize=(10, 6))

        x = range(len(common_idx))
        ax.bar(
            x,
            actual_values.values,
            width=0.4,
            label="Actual",
            alpha=0.8,
            color="steelblue",
        )
        ax.bar(
            [i + 0.4 for i in x],
            forecast_values.values,
            width=0.4,
            label="Forecast",
            alpha=0.8,
            color="coral",
        )

        # Add error bars for CI
        ax.errorbar(
            [i + 0.4 for i in x],
            forecast_values.values,
            yerr=[
                forecast_df.loc[common_idx, "Lower_CI"].values
                - forecast_values.values
                + forecast_values.values
                - forecast_df.loc[common_idx, "Lower_CI"].values,
                forecast_df.loc[common_idx, "Upper_CI"].values - forecast_values.values,
            ],
            fmt="none",
            color="black",
            capsize=3,
        )

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
    actual_holdout: pd.DataFrame | None = None,
    output_dir: Path | None = None,
) -> None:
    """Create forecast visualization with historical data and predictions.

    Args:
        train_data: Historical training data with BEV column
        forecast_df: Forecast results with Forecast, Lower_CI, Upper_CI columns
        fitted_model: Fitted ARIMA model results
        actual_holdout: Optional actual values for validation period
        output_dir: Optional directory to save plots
    """
    if output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(14, 7))

    # Historical data
    ax.plot(
        train_data.index,
        train_data["BEV"],
        label="Historical Data",
        color="steelblue",
        linewidth=1.5,
    )

    # Fitted values (in-sample)
    fitted_values = fitted_model.fittedvalues
    ax.plot(
        fitted_values.index,
        fitted_values,
        label="Fitted Values",
        color="green",
        linewidth=1,
        alpha=0.7,
        linestyle="--",
    )

    # Forecast
    ax.plot(
        forecast_df.index,
        forecast_df["Forecast"],
        label="Forecast",
        color="coral",
        linewidth=2,
        marker="o",
        markersize=4,
    )

    # Confidence interval
    ax.fill_between(
        forecast_df.index,
        forecast_df["Lower_CI"],
        forecast_df["Upper_CI"],
        color="coral",
        alpha=0.2,
        label="95% CI",
    )

    # Actual holdout data if available
    if actual_holdout is not None and not actual_holdout.empty:
        ax.scatter(
            actual_holdout.index,
            actual_holdout["BEV"],
            color="red",
            s=80,
            zorder=5,
            label="Actual (Holdout)",
            marker="D",
        )

    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("BEV Registrations", fontsize=12)
    ax.set_title("NC Statewide BEV Registrations: ARIMA Forecast", fontsize=14)
    ax.legend(loc="upper left")
    ax.grid(alpha=0.3)

    # Format y-axis with thousands separator
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: format(int(x), ",")))

    fig.tight_layout()

    if output_dir:
        fig.savefig(output_dir / "forecast_plot.png", dpi=150, bbox_inches="tight")
        print(f"\n  Saved: {output_dir / 'forecast_plot.png'}")

    plt.close(fig)


# =============================================================================
# Main Execution
# =============================================================================


def main() -> None:
    """Run ARIMA forecasting pipeline with CLI argument parsing."""
    parser = argparse.ArgumentParser(
        description="ARIMA Model for NC BEV Registration Forecasting",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--order",
        "-o",
        nargs=3,
        type=int,
        default=list(DEFAULT_ORDER),
        metavar=("P", "D", "Q"),
        help=f"ARIMA order (p, d, q). Default: {DEFAULT_ORDER}",
    )

    parser.add_argument(
        "--auto-select",
        action="store_true",
        help="Automatically select best ARIMA order",
    )

    parser.add_argument(
        "--forecast-steps",
        "-f",
        type=int,
        default=12,
        help="Number of months to forecast (default: 12)",
    )

    parser.add_argument("--no-plots", action="store_true", help="Skip generating plots")

    parser.add_argument("--sas-aic", type=float, help="SAS AIC value for comparison")

    args = parser.parse_args()

    # Setup output directory
    output_dir = OUTPUT_DIR if not args.no_plots else None

    print("=" * 70)
    print("NC STATEWIDE BEV REGISTRATION ARIMA FORECASTING")
    print("=" * 70)

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
        validate_forecast(forecast_df, holdout_data, output_dir)

    # Create forecast plot
    if output_dir:
        plot_forecast(train_data, forecast_df, fitted_model, holdout_data, output_dir)

    print("\n" + "=" * 70)
    print("ANALYSIS COMPLETE")
    print("=" * 70)

    if output_dir:
        print(f"\nOutput files saved to: {output_dir}")


if __name__ == "__main__":
    main()
