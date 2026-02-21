#!/usr/bin/env python3
"""
Generate Phase 1 Validation Figures - Publication Quality

Creates publication-ready visualizations for Phase 1 validation:
1. Predicted vs Actual scatter plot
2. Error distribution histogram
3. Metrics by model type bar chart
4. Confidence interval coverage comparison
5. Time series examples with confidence bands
6. MAPE boxplot by model type
7. County performance lollipop chart

Usage:
    python generate_phase1_figures.py
    python generate_phase1_figures.py --output ../../../output/figures
    python generate_phase1_figures.py --nice-to-have
"""

import argparse
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Import publication styling
from publication_style import (
    COLORS,
    FIGURE_SIZES,
    FONT_SIZES,
    add_panel_label,
    add_stats_annotation,
    save_figure,
    setup_publication_style,
    style_boxplot,
)

# =============================================================================
# APPLY PUBLICATION STYLE
# =============================================================================
setup_publication_style(use_serif=True, context="paper")

# Export formats (PNG for review, PDF for final submission)
EXPORT_FORMATS = ["png", "pdf"]


def load_validation_data(data_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load validation comparison and model metrics data.

    Args:
        data_dir: Path to validation output directory.

    Returns:
        Tuple of (comparison_df, model_metrics_df).
    """
    comparison = pd.read_csv(data_dir / "sas-validation-comparison.csv")
    model_metrics = pd.read_csv(data_dir / "sas-validation-by-model.csv")
    return comparison, model_metrics


def fig01_predicted_vs_actual(df: pd.DataFrame, output_dir: Path) -> None:
    """Create scatter plot of predicted vs actual values.

    Publication-ready scatter plot with identity line for forecast validation.
    Points above the identity line indicate underprediction.

    Args:
        df: Comparison DataFrame with Predicted and Actual columns.
        output_dir: Directory to save figure.
    """
    fig, ax = plt.subplots(figsize=FIGURE_SIZES["medium_square"])

    # Plot by model type with consistent ordering
    model_order = ["ESM", "ARIMA", "UCM"]

    for model_type in model_order:
        subset = df[df["ModelType"] == model_type]
        if len(subset) == 0:
            continue

        ax.scatter(
            subset["Predicted"],
            subset["Actual"],
            c=COLORS[model_type],
            label=f"{model_type} (n={len(subset)})",
            alpha=0.7,
            s=45,
            edgecolors="white",
            linewidths=0.5,
            zorder=3,
        )

    # Identity line (perfect prediction)
    max_val = max(df["Predicted"].max(), df["Actual"].max()) * 1.05
    ax.plot(
        [0, max_val], [0, max_val], "k--", lw=1.5, label="Perfect prediction", zorder=2
    )

    # Axis configuration
    ax.set_xlabel("Predicted BEV Registrations")
    ax.set_ylabel("Actual BEV Registrations")
    ax.set_title("Forecast Validation: Predicted vs Actual\n(Jul-Oct 2025)")
    ax.set_xlim(0, max_val)
    ax.set_ylim(0, max_val)
    ax.set_aspect("equal", adjustable="box")

    # Legend with better positioning
    ax.legend(loc="lower right", framealpha=0.95)

    # Underprediction annotation
    underpred_pct = (df["Actual"] > df["Predicted"]).mean() * 100
    add_stats_annotation(
        ax,
        f"{underpred_pct:.1f}% of points above line\n(underprediction)",
        loc="upper left",
        facecolor="#FFF8E1",
    )

    # Save figure
    save_figure(fig, "fig-01-predicted-vs-actual-scatter", output_dir, EXPORT_FORMATS)
    plt.close(fig)
    print("[ok] fig-01-predicted-vs-actual-scatter")


def fig02_error_distribution(df: pd.DataFrame, output_dir: Path) -> None:
    """Create histogram of forecast errors with bias annotation.

    Publication-ready histogram showing error distribution with reference lines
    for zero (unbiased) and mean bias.

    Args:
        df: Comparison DataFrame with Error column.
        output_dir: Directory to save figure.
    """
    fig, ax = plt.subplots(figsize=FIGURE_SIZES["wide"])

    # Calculate statistics
    errors = df["Error"]
    mean_bias = errors.mean()
    median_bias = errors.median()
    std_dev = errors.std()
    underpred_pct = (errors > 0).mean() * 100

    # Determine bin edges for better visualization
    # Use Freedman-Diaconis rule but cap at 50 bins
    q75, q25 = np.percentile(errors, [75, 25])
    iqr = q75 - q25
    bin_width = 2 * iqr / (len(errors) ** (1 / 3)) if iqr > 0 else 1
    n_bins = min(50, max(15, int((errors.max() - errors.min()) / bin_width)))

    # Histogram with improved styling
    n, bins, patches = ax.hist(
        errors,
        bins=n_bins,
        color=COLORS["ESM"],
        alpha=0.75,
        edgecolor="white",
        linewidth=0.8,
    )

    # Reference lines
    ax.axvline(
        x=0,
        color=COLORS["reference"],
        linestyle="-",
        lw=2,
        label="Zero (unbiased)",
        zorder=10,
    )
    ax.axvline(
        x=mean_bias,
        color=COLORS["negative"],
        linestyle="--",
        lw=2,
        label=f"Mean bias: {mean_bias:+.1f}",
        zorder=10,
    )

    # Axis labels
    ax.set_xlabel("Forecast Error (Actual - Predicted)")
    ax.set_ylabel("Frequency")
    ax.set_title("Distribution of Forecast Errors\n(Positive = Underprediction)")

    # Legend
    ax.legend(loc="upper left", framealpha=0.95)

    # Statistics annotation box
    stats_text = (
        f"Mean: {mean_bias:+.1f}\n"
        f"Median: {median_bias:+.1f}\n"
        f"Std Dev: {std_dev:.1f}\n"
        f"Underpredicted: {underpred_pct:.1f}%"
    )
    add_stats_annotation(ax, stats_text, loc="upper right")

    # Save figure
    save_figure(fig, "fig-02-error-distribution-histogram", output_dir, EXPORT_FORMATS)
    plt.close(fig)
    print("[ok] fig-02-error-distribution-histogram")


def fig03_metrics_by_model(model_metrics: pd.DataFrame, output_dir: Path) -> None:
    """Create grouped bar chart of metrics by model type.

    Three-panel figure showing MAPE, Mean Bias, and Underprediction Rate
    for each model type.

    Args:
        model_metrics: DataFrame with metrics grouped by ModelType.
        output_dir: Directory to save figure.
    """
    fig, axes = plt.subplots(1, 3, figsize=(10, 4))

    models = model_metrics["ModelType"].tolist()
    colors = [COLORS.get(m, COLORS["neutral"]) for m in models]
    x = np.arange(len(models))
    bar_width = 0.7

    # Create x-axis labels with county counts
    labels = [
        f"{m}\n(n={int(model_metrics[model_metrics['ModelType'] == m]['Counties'].values[0])})"
        for m in models
    ]

    # Panel A: MAPE
    mape_values = model_metrics["MAPE"].values
    bars_a = axes[0].bar(
        x, mape_values, width=bar_width, color=colors, edgecolor="white"
    )
    axes[0].set_ylabel("MAPE (%)")
    axes[0].set_title("Point Forecast Accuracy")
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(labels)
    axes[0].set_ylim(0, max(mape_values) * 1.2)

    # Value labels
    for i, v in enumerate(mape_values):
        axes[0].text(
            i,
            v + max(mape_values) * 0.03,
            f"{v:.2f}%",
            ha="center",
            va="bottom",
            fontsize=FONT_SIZES["annotation"],
        )

    add_panel_label(axes[0], "A")

    # Panel B: Mean Bias
    bias_values = model_metrics["MeanBias"].values
    bars_b = axes[1].bar(
        x, bias_values, width=bar_width, color=colors, edgecolor="white"
    )
    axes[1].set_ylabel("Mean Bias (vehicles)")
    axes[1].set_title("Systematic Bias")
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(labels)
    axes[1].axhline(y=0, color=COLORS["reference"], linestyle="-", lw=1)

    # Value labels (positioned based on sign)
    for i, v in enumerate(bias_values):
        offset = abs(max(bias_values) - min(bias_values)) * 0.05
        y_pos = v + offset if v >= 0 else v - offset
        va = "bottom" if v >= 0 else "top"
        axes[1].text(
            i, y_pos, f"{v:+.1f}", ha="center", va=va, fontsize=FONT_SIZES["annotation"]
        )

    add_panel_label(axes[1], "B")

    # Panel C: Underprediction Rate
    underpred = model_metrics["PctUnderpredicted"].values * 100
    bars_c = axes[2].bar(x, underpred, width=bar_width, color=colors, edgecolor="white")
    axes[2].set_ylabel("Underprediction Rate (%)")
    axes[2].set_title("Bias Direction")
    axes[2].set_xticks(x)
    axes[2].set_xticklabels(labels)
    axes[2].axhline(
        y=50, color=COLORS["gray_medium"], linestyle="--", lw=1, label="50% (unbiased)"
    )
    axes[2].set_ylim(0, 100)
    axes[2].legend(loc="lower right", fontsize=FONT_SIZES["annotation"])

    # Value labels
    for i, v in enumerate(underpred):
        axes[2].text(
            i,
            v + 2,
            f"{v:.1f}%",
            ha="center",
            va="bottom",
            fontsize=FONT_SIZES["annotation"],
        )

    add_panel_label(axes[2], "C")

    # Main title
    fig.suptitle(
        "Forecast Performance by Model Type",
        fontsize=FONT_SIZES["title"] + 1,
        fontweight="bold",
        y=1.02,
    )

    # Save figure
    save_figure(fig, "fig-03-metrics-by-model-type", output_dir, EXPORT_FORMATS)
    plt.close(fig)
    print("[ok] fig-03-metrics-by-model-type")


def fig04_ci_coverage(model_metrics: pd.DataFrame, output_dir: Path) -> None:
    """Create bar chart comparing CI coverage vs 95% target.

    Publication-ready bar chart showing confidence interval coverage
    with gap annotations from the 95% target.

    Args:
        model_metrics: DataFrame with CI_Coverage column.
        output_dir: Directory to save figure.
    """
    fig, ax = plt.subplots(figsize=FIGURE_SIZES["wide"])

    models = model_metrics["ModelType"].tolist()
    coverage = model_metrics["CI_Coverage"].values * 100
    colors = [COLORS.get(m, COLORS["neutral"]) for m in models]
    x = np.arange(len(models))
    bar_width = 0.6

    # Create x-axis labels with county counts
    labels = [
        f"{m}\n(n={int(model_metrics[model_metrics['ModelType'] == m]['Counties'].values[0])})"
        for m in models
    ]

    # Bars
    bars = ax.bar(
        x, coverage, width=bar_width, color=colors, alpha=0.85, edgecolor="white"
    )

    # 95% target line
    ax.axhline(y=95, color=COLORS["negative"], linestyle="--", lw=2, label="95% Target")

    # Axis configuration
    ax.set_ylabel("Confidence Interval Coverage (%)")
    ax.set_xlabel("Model Type")
    ax.set_title("95% CI Coverage: Observed vs Target")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylim(0, 110)

    # Legend
    ax.legend(loc="upper right", framealpha=0.95)

    # Value labels with gap annotation
    for i, (v, m) in enumerate(zip(coverage, models)):
        # Main value label
        ax.text(
            i,
            v + 2,
            f"{v:.1f}%",
            ha="center",
            va="bottom",
            fontsize=FONT_SIZES["annotation"] + 1,
            fontweight="bold",
        )

        # Gap annotation (if below target)
        gap = 95 - v
        if gap > 0:
            ax.text(
                i,
                v - 4,
                f"(-{gap:.1f}pp)",
                ha="center",
                va="top",
                fontsize=FONT_SIZES["annotation"],
                color=COLORS["negative"],
            )

    # Summary annotation
    overall_coverage = coverage.mean()
    summary_text = (
        f"Overall coverage: {overall_coverage:.1f}%\n"
        f"Gap from target: {95 - overall_coverage:.1f} pp\n\n"
        "Undercoverage indicates\n"
        "confidence intervals are\n"
        "too narrow or biased."
    )
    add_stats_annotation(ax, summary_text, loc="upper left")

    # Save figure
    save_figure(fig, "fig-04-confidence-interval-coverage", output_dir, EXPORT_FORMATS)
    plt.close(fig)
    print("[ok] fig-04-confidence-interval-coverage")


def fig05_time_series_examples(comparison: pd.DataFrame, output_dir: Path) -> None:
    """Create time series plots for representative counties.

    Two-panel figure showing predicted vs actual with confidence bands for:
    - High performer (Caldwell)
    - Urban underprediction case (Wake)

    Args:
        comparison: Comparison DataFrame with all columns.
        output_dir: Directory to save figure.
    """
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))

    counties = ["Caldwell", "Wake"]
    titles = ["Best Performer: Caldwell (0.30% MAPE)", "Largest Miss: Wake County"]
    panel_labels = ["A", "B"]

    for ax, county, title, panel in zip(axes, counties, titles, panel_labels):
        subset = comparison[comparison["County"] == county].copy()

        # Sort by month
        months = ["Jul 2025", "Aug 2025", "Sep 2025", "Oct 2025"]
        month_order = {m: i for i, m in enumerate(months)}
        subset["MonthOrder"] = subset["MonthDate"].map(month_order)
        subset = subset.sort_values("MonthOrder")

        x = np.arange(len(subset))

        # Confidence band (behind everything)
        ax.fill_between(
            x,
            subset["LOWER"],
            subset["UPPER"],
            alpha=0.25,
            color=COLORS["ESM"],
            label="95% CI",
            zorder=1,
        )

        # Predicted line with markers
        ax.plot(
            x,
            subset["Predicted"],
            color=COLORS["ESM"],
            lw=2,
            marker="s",
            markersize=8,
            markerfacecolor=COLORS["ESM"],
            markeredgecolor="white",
            markeredgewidth=1.5,
            label="Predicted",
            zorder=3,
        )

        # Actual points (on top)
        ax.scatter(
            x,
            subset["Actual"],
            color=COLORS["negative"],
            s=80,
            marker="o",
            edgecolors="white",
            linewidths=1.5,
            label="Actual",
            zorder=5,
        )

        # Axis configuration
        ax.set_xticks(x)
        ax.set_xticklabels(["Jul", "Aug", "Sep", "Oct"])
        ax.set_xlabel("Month (2025)")
        ax.set_ylabel("BEV Registrations")
        ax.set_title(title)
        ax.legend(loc="upper left", framealpha=0.95)

        # Add panel label
        add_panel_label(ax, panel)

    # Main title
    fig.suptitle(
        "Time Series Validation Examples",
        fontsize=FONT_SIZES["title"] + 1,
        fontweight="bold",
        y=1.02,
    )

    # Save figure
    save_figure(fig, "fig-05-time-series-examples", output_dir, EXPORT_FORMATS)
    plt.close(fig)
    print("[ok] fig-05-time-series-examples")


def fig06_mape_boxplot(county_metrics: pd.DataFrame, output_dir: Path) -> None:
    """Create boxplot of MAPE distribution by model type.

    Publication-ready boxplot showing the distribution of MAPE values
    across counties for each model type.

    Args:
        county_metrics: DataFrame with county-level metrics.
        output_dir: Directory to save figure.
    """
    fig, ax = plt.subplots(figsize=FIGURE_SIZES["wide"])

    # Prepare data
    model_types = ["ESM", "ARIMA", "UCM"]
    data = [
        county_metrics[county_metrics["ModelType"] == m]["MAPE"].values
        for m in model_types
    ]
    colors = [COLORS[m] for m in model_types]

    # Create boxplot
    bp = ax.boxplot(
        data,
        labels=model_types,
        patch_artist=True,
        widths=0.6,
        showmeans=True,
        meanprops=dict(
            marker="D",
            markerfacecolor="white",
            markeredgecolor=COLORS["reference"],
            markersize=6,
        ),
    )

    # Apply custom styling
    style_boxplot(bp, colors=colors, alpha=0.75)

    # Add sample size labels below x-axis
    for i, m in enumerate(model_types):
        n = len(county_metrics[county_metrics["ModelType"] == m])
        ax.text(
            i + 1,
            ax.get_ylim()[0] - 0.8,
            f"n={n}",
            ha="center",
            fontsize=FONT_SIZES["annotation"],
        )

    # Axis configuration
    ax.set_ylabel("MAPE (%)")
    ax.set_xlabel("Model Type")
    ax.set_title("MAPE Distribution by Model Type")

    # Add threshold reference line
    ax.axhline(
        y=5, color=COLORS["gray_medium"], linestyle="--", lw=1.5, label="5% threshold"
    )
    ax.legend(loc="upper right", framealpha=0.95)

    # Ensure y-axis starts at 0
    ax.set_ylim(bottom=0)

    # Save figure
    save_figure(fig, "fig-06-mape-boxplot-by-model", output_dir, EXPORT_FORMATS)
    plt.close(fig)
    print("[ok] fig-06-mape-boxplot-by-model")


def fig07_county_performance(
    county_metrics: pd.DataFrame, output_dir: Path, n: int = 5
) -> None:
    """Create lollipop chart of top/bottom performing counties.

    Horizontal lollipop chart showing the best and worst performing counties
    by MAPE, color-coded by model type.

    Args:
        county_metrics: DataFrame with county-level metrics.
        output_dir: Directory to save figure.
        n: Number of top and bottom counties to show.
    """
    # Sort and select top/bottom counties
    sorted_df = county_metrics.sort_values("MAPE")
    top_n = sorted_df.head(n).copy()
    bottom_n = sorted_df.tail(n).copy()

    # Reverse bottom_n so worst is at top
    bottom_n = bottom_n.iloc[::-1]

    # Combine with gap
    combined = pd.concat([bottom_n, top_n])

    fig, ax = plt.subplots(figsize=(9, max(6, n * 0.55)))

    y_positions = np.arange(len(combined))
    colors = [COLORS.get(m, COLORS["neutral"]) for m in combined["ModelType"]]

    # Lollipop stems
    for i, (idx, row) in enumerate(combined.iterrows()):
        ax.hlines(
            y=i,
            xmin=0,
            xmax=row["MAPE"],
            color=COLORS.get(row["ModelType"], COLORS["neutral"]),
            alpha=0.7,
            lw=2.5,
        )

    # Lollipop heads
    ax.scatter(
        combined["MAPE"],
        y_positions,
        c=colors,
        s=120,
        edgecolors="white",
        linewidths=1.5,
        zorder=5,
    )

    # Y-axis labels
    labels = [f"{row['County']} ({row['ModelType']})" for _, row in combined.iterrows()]
    ax.set_yticks(y_positions)
    ax.set_yticklabels(labels)

    # Value annotations
    for i, (_, row) in enumerate(combined.iterrows()):
        ax.text(
            row["MAPE"] + 0.4,
            i,
            f"{row['MAPE']:.1f}%",
            va="center",
            fontsize=FONT_SIZES["annotation"],
        )

    # Separator line and label
    separator_y = n - 0.5
    ax.axhline(y=separator_y, color=COLORS["reference"], linestyle="-", lw=1)
    ax.text(
        ax.get_xlim()[1] * 0.5,
        separator_y,
        f"  Top {n}  |  Bottom {n}  ",
        ha="center",
        va="center",
        fontsize=FONT_SIZES["annotation"],
        bbox=dict(
            boxstyle="round,pad=0.3", facecolor="white", edgecolor=COLORS["gray_light"]
        ),
    )

    # Axis configuration
    ax.set_xlabel("MAPE (%)")
    ax.set_title(f"County Forecast Performance: Top {n} vs Bottom {n}")
    ax.set_xlim(0, combined["MAPE"].max() * 1.18)

    # Model type legend
    from matplotlib.patches import Patch

    legend_elements = [
        Patch(facecolor=COLORS[m], edgecolor="white", label=m)
        for m in ["ESM", "ARIMA", "UCM"]
    ]
    ax.legend(handles=legend_elements, loc="lower right", framealpha=0.95)

    # Remove top and right spines (already done by rcParams but explicit)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Save figure
    suffix = f"{n}x{n}"
    save_figure(fig, f"fig-07-county-performance-{suffix}", output_dir, EXPORT_FORMATS)
    plt.close(fig)
    print(f"[ok] fig-07-county-performance-{suffix}")


def main() -> None:
    """Generate all Phase 1 validation figures."""
    parser = argparse.ArgumentParser(description="Generate Phase 1 validation figures")
    parser.add_argument(
        "--output",
        default="../../../output/figures",
        help="Output directory for figures",
    )
    parser.add_argument(
        "--data",
        default="../../../output/validation",
        help="Input directory with validation CSVs",
    )
    parser.add_argument(
        "--nice-to-have",
        action="store_true",
        help="Also generate nice-to-have figures",
    )
    parser.add_argument(
        "--png-only",
        action="store_true",
        help="Export PNG only (skip PDF)",
    )
    args = parser.parse_args()

    # Update export formats if PNG only
    global EXPORT_FORMATS
    if args.png_only:
        EXPORT_FORMATS = ["png"]

    script_dir = Path(__file__).parent
    output_dir = Path(args.output)
    data_dir = Path(args.data)

    if not output_dir.is_absolute():
        output_dir = script_dir / output_dir
    if not data_dir.is_absolute():
        data_dir = script_dir / data_dir

    output_dir.mkdir(parents=True, exist_ok=True)

    # Verify required input files exist (generated by validate_sas_forecasts.py)
    required_files = [
        data_dir / "sas-validation-comparison.csv",
        data_dir / "sas-validation-by-model.csv",
        data_dir / "sas-validation-by-county.csv",
    ]
    for fpath in required_files:
        if not fpath.exists():
            print(
                f"[error] Missing {fpath.name}. Run validate_sas_forecasts.py first.",
                file=sys.stderr,
            )
            sys.exit(1)

    print("[i] Loading validation data...")
    comparison, model_metrics = load_validation_data(data_dir)
    county_metrics = pd.read_csv(data_dir / "sas-validation-by-county.csv")
    print(f"    {len(comparison)} observations loaded")

    print(f"[i] Export formats: {EXPORT_FORMATS}")
    print("[i] Generating required figures...")
    fig01_predicted_vs_actual(comparison, output_dir)
    fig02_error_distribution(comparison, output_dir)
    fig03_metrics_by_model(model_metrics, output_dir)
    fig04_ci_coverage(model_metrics, output_dir)

    if args.nice_to_have:
        print("[i] Generating nice-to-have figures...")
        fig05_time_series_examples(comparison, output_dir)
        fig06_mape_boxplot(county_metrics, output_dir)
        fig07_county_performance(county_metrics, output_dir, n=5)
        fig07_county_performance(county_metrics, output_dir, n=10)

    print(f"\n[done] Figures saved to {output_dir.resolve()}")
    print("[i] Both PNG (for review) and PDF (for submission) versions created.")


if __name__ == "__main__":
    main()
