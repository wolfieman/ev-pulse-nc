#!/usr/bin/env python3
"""
Generate Phase 1 Validation Figures

Creates the four required visualizations for Phase 1 validation:
1. Predicted vs Actual scatter plot
2. Error distribution histogram
3. Metrics by model type bar chart
4. Confidence interval coverage comparison

Usage:
    python generate_phase1_figures.py
    python generate_phase1_figures.py --output ../../../output/figures
"""

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

# Style configuration
plt.style.use("seaborn-v0_8-whitegrid")
COLORS = {"ESM": "#2ecc71", "ARIMA": "#3498db", "UCM": "#9b59b6"}
DPI = 300


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

    Points above the identity line indicate underprediction.

    Args:
        df: Comparison DataFrame with Predicted and Actual columns.
        output_dir: Directory to save figure.
    """
    fig, ax = plt.subplots(figsize=(8, 8))

    # Plot by model type
    for model_type in ["ESM", "ARIMA", "UCM"]:
        subset = df[df["ModelType"] == model_type]
        ax.scatter(
            subset["Predicted"],
            subset["Actual"],
            c=COLORS.get(model_type, "#95a5a6"),
            label=f"{model_type} (n={len(subset)})",
            alpha=0.6,
            s=30,
        )

    # Identity line
    max_val = max(df["Predicted"].max(), df["Actual"].max()) * 1.05
    ax.plot([0, max_val], [0, max_val], "k--", lw=1.5, label="Perfect prediction")

    # Labels and formatting
    ax.set_xlabel("Predicted BEV Registrations", fontsize=12)
    ax.set_ylabel("Actual BEV Registrations", fontsize=12)
    ax.set_title("Forecast Validation: Predicted vs Actual\n(Jul-Oct 2025)", fontsize=14)
    ax.legend(loc="lower right")
    ax.set_xlim(0, max_val)
    ax.set_ylim(0, max_val)

    # Add annotation about underprediction
    underpred_pct = (df["Actual"] > df["Predicted"]).mean() * 100
    ax.annotate(
        f"{underpred_pct:.1f}% of points above line\n(underprediction)",
        xy=(0.05, 0.95),
        xycoords="axes fraction",
        fontsize=10,
        verticalalignment="top",
        bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5),
    )

    plt.tight_layout()
    fig.savefig(output_dir / "fig-01-predicted-vs-actual-scatter.png", dpi=DPI)
    plt.close(fig)
    print("[ok] fig-01-predicted-vs-actual-scatter.png")


def fig02_error_distribution(df: pd.DataFrame, output_dir: Path) -> None:
    """Create histogram of forecast errors with bias annotation.

    Args:
        df: Comparison DataFrame with Error column.
        output_dir: Directory to save figure.
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    # Histogram
    ax.hist(df["Error"], bins=50, color="#3498db", alpha=0.7, edgecolor="white")

    # Reference lines
    mean_bias = df["Error"].mean()
    ax.axvline(x=0, color="black", linestyle="-", lw=2, label="Zero (unbiased)")
    ax.axvline(
        x=mean_bias, color="red", linestyle="--", lw=2, label=f"Mean bias: {mean_bias:+.1f}"
    )

    # Labels
    ax.set_xlabel("Forecast Error (Actual - Predicted)", fontsize=12)
    ax.set_ylabel("Frequency", fontsize=12)
    ax.set_title("Distribution of Forecast Errors\n(Positive = Underprediction)", fontsize=14)
    ax.legend(loc="upper right")

    # Stats annotation
    stats_text = (
        f"Mean: {mean_bias:+.1f}\n"
        f"Median: {df['Error'].median():+.1f}\n"
        f"Std Dev: {df['Error'].std():.1f}\n"
        f"Underpredicted: {(df['Error'] > 0).mean()*100:.1f}%"
    )
    ax.annotate(
        stats_text,
        xy=(0.98, 0.95),
        xycoords="axes fraction",
        fontsize=10,
        verticalalignment="top",
        horizontalalignment="right",
        bbox=dict(boxstyle="round", facecolor="lightyellow", alpha=0.8),
    )

    plt.tight_layout()
    fig.savefig(output_dir / "fig-02-error-distribution-histogram.png", dpi=DPI)
    plt.close(fig)
    print("[ok] fig-02-error-distribution-histogram.png")


def fig03_metrics_by_model(model_metrics: pd.DataFrame, output_dir: Path) -> None:
    """Create grouped bar chart of metrics by model type.

    Args:
        model_metrics: DataFrame with metrics grouped by ModelType.
        output_dir: Directory to save figure.
    """
    fig, axes = plt.subplots(1, 3, figsize=(14, 5))

    models = model_metrics["ModelType"].tolist()
    colors = [COLORS.get(m, "#95a5a6") for m in models]
    x = range(len(models))

    # MAPE
    axes[0].bar(x, model_metrics["MAPE"], color=colors)
    axes[0].set_ylabel("MAPE (%)", fontsize=11)
    axes[0].set_title("Point Forecast Accuracy", fontsize=12)
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(models)
    for i, v in enumerate(model_metrics["MAPE"]):
        axes[0].text(i, v + 0.1, f"{v:.2f}%", ha="center", fontsize=10)

    # Mean Bias
    axes[1].bar(x, model_metrics["MeanBias"], color=colors)
    axes[1].set_ylabel("Mean Bias (vehicles)", fontsize=11)
    axes[1].set_title("Systematic Bias", fontsize=12)
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(models)
    axes[1].axhline(y=0, color="black", linestyle="-", lw=1)
    for i, v in enumerate(model_metrics["MeanBias"]):
        axes[1].text(i, v + 1, f"{v:+.1f}", ha="center", fontsize=10)

    # Underprediction Rate
    underpred = model_metrics["PctUnderpredicted"] * 100
    axes[2].bar(x, underpred, color=colors)
    axes[2].set_ylabel("Underprediction Rate (%)", fontsize=11)
    axes[2].set_title("Bias Direction", fontsize=12)
    axes[2].set_xticks(x)
    axes[2].set_xticklabels(models)
    axes[2].axhline(y=50, color="gray", linestyle="--", lw=1, label="50% (unbiased)")
    for i, v in enumerate(underpred):
        axes[2].text(i, v + 1, f"{v:.1f}%", ha="center", fontsize=10)

    # Add county counts to x-axis labels
    for ax in axes:
        labels = [f"{m}\n(n={int(model_metrics[model_metrics['ModelType']==m]['Counties'].values[0])})"
                  for m in models]
        ax.set_xticklabels(labels)

    fig.suptitle("Forecast Performance by Model Type", fontsize=14, y=1.02)
    plt.tight_layout()
    fig.savefig(output_dir / "fig-03-metrics-by-model-type.png", dpi=DPI)
    plt.close(fig)
    print("[ok] fig-03-metrics-by-model-type.png")


def fig04_ci_coverage(model_metrics: pd.DataFrame, output_dir: Path) -> None:
    """Create bar chart comparing CI coverage vs 95% target.

    Args:
        model_metrics: DataFrame with CI_Coverage column.
        output_dir: Directory to save figure.
    """
    fig, ax = plt.subplots(figsize=(8, 6))

    models = model_metrics["ModelType"].tolist()
    coverage = model_metrics["CI_Coverage"] * 100
    colors = [COLORS.get(m, "#95a5a6") for m in models]
    x = range(len(models))

    # Bars
    bars = ax.bar(x, coverage, color=colors, alpha=0.8)

    # 95% target line
    ax.axhline(y=95, color="red", linestyle="--", lw=2, label="95% Target")

    # Labels
    ax.set_ylabel("Confidence Interval Coverage (%)", fontsize=12)
    ax.set_xlabel("Model Type", fontsize=12)
    ax.set_title("95% CI Coverage: Observed vs Target", fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels([f"{m}\n(n={int(model_metrics[model_metrics['ModelType']==m]['Counties'].values[0])})"
                        for m in models])
    ax.set_ylim(0, 110)
    ax.legend(loc="upper right")

    # Value labels with gap annotation
    for i, (v, m) in enumerate(zip(coverage, models)):
        gap = 95 - v
        ax.text(i, v + 2, f"{v:.1f}%", ha="center", fontsize=11, fontweight="bold")
        if gap > 0:
            ax.text(i, v - 5, f"(-{gap:.1f}pp)", ha="center", fontsize=9, color="red")

    # Annotation
    overall_coverage = coverage.mean()
    ax.annotate(
        f"Overall coverage: {overall_coverage:.1f}%\n"
        f"Gap from target: {95 - overall_coverage:.1f} pp\n\n"
        "Undercoverage indicates\nconfidence intervals are\ntoo narrow or biased.",
        xy=(0.02, 0.98),
        xycoords="axes fraction",
        fontsize=10,
        verticalalignment="top",
        bbox=dict(boxstyle="round", facecolor="lightyellow", alpha=0.8),
    )

    plt.tight_layout()
    fig.savefig(output_dir / "fig-04-confidence-interval-coverage.png", dpi=DPI)
    plt.close(fig)
    print("[ok] fig-04-confidence-interval-coverage.png")


def fig05_time_series_examples(comparison: pd.DataFrame, output_dir: Path) -> None:
    """Create time series plots for representative counties.

    Shows predicted vs actual with confidence bands for:
    - High performer (Caldwell)
    - Urban underprediction case (Wake)

    Args:
        comparison: Comparison DataFrame with all columns.
        output_dir: Directory to save figure.
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    counties = ["Caldwell", "Wake"]
    titles = ["Best Performer: Caldwell (0.30% MAPE)", "Largest Miss: Wake County"]

    for ax, county, title in zip(axes, counties, titles):
        subset = comparison[comparison["County"] == county].copy()
        subset = subset.sort_values("MonthDate")

        months = ["Jul 2025", "Aug 2025", "Sep 2025", "Oct 2025"]
        subset["MonthOrder"] = subset["MonthDate"].apply(lambda x: months.index(x))
        subset = subset.sort_values("MonthOrder")

        x = range(len(subset))

        # Confidence band
        ax.fill_between(
            x,
            subset["LOWER"],
            subset["UPPER"],
            alpha=0.3,
            color="#3498db",
            label="95% CI",
        )

        # Predicted line
        ax.plot(x, subset["Predicted"], "b-", lw=2, marker="s", label="Predicted")

        # Actual points
        ax.plot(x, subset["Actual"], "ro", ms=10, label="Actual", zorder=5)

        ax.set_xticks(x)
        ax.set_xticklabels(["Jul", "Aug", "Sep", "Oct"])
        ax.set_xlabel("Month (2025)", fontsize=11)
        ax.set_ylabel("BEV Registrations", fontsize=11)
        ax.set_title(title, fontsize=12)
        ax.legend(loc="upper left")

    fig.suptitle("Time Series Validation Examples", fontsize=14, y=1.02)
    plt.tight_layout()
    fig.savefig(output_dir / "fig-05-time-series-examples.png", dpi=DPI)
    plt.close(fig)
    print("[ok] fig-05-time-series-examples.png")


def fig06_mape_boxplot(county_metrics: pd.DataFrame, output_dir: Path) -> None:
    """Create boxplot of MAPE distribution by model type.

    Args:
        county_metrics: DataFrame with county-level metrics.
        output_dir: Directory to save figure.
    """
    fig, ax = plt.subplots(figsize=(8, 6))

    model_types = ["ESM", "ARIMA", "UCM"]
    data = [county_metrics[county_metrics["ModelType"] == m]["MAPE"].values for m in model_types]
    colors = [COLORS.get(m, "#95a5a6") for m in model_types]

    bp = ax.boxplot(data, labels=model_types, patch_artist=True)

    for patch, color in zip(bp["boxes"], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)

    # Add county counts
    for i, m in enumerate(model_types):
        n = len(county_metrics[county_metrics["ModelType"] == m])
        ax.text(i + 1, ax.get_ylim()[0] - 1, f"n={n}", ha="center", fontsize=10)

    ax.set_ylabel("MAPE (%)", fontsize=12)
    ax.set_xlabel("Model Type", fontsize=12)
    ax.set_title("MAPE Distribution by Model Type", fontsize=14)
    ax.axhline(y=5, color="gray", linestyle="--", lw=1, label="5% threshold")
    ax.legend(loc="upper right")

    plt.tight_layout()
    fig.savefig(output_dir / "fig-06-mape-boxplot-by-model.png", dpi=DPI)
    plt.close(fig)
    print("[ok] fig-06-mape-boxplot-by-model.png")


def fig07_county_performance(county_metrics: pd.DataFrame, output_dir: Path, n: int = 5) -> None:
    """Create lollipop chart of top/bottom performing counties.

    Args:
        county_metrics: DataFrame with county-level metrics.
        output_dir: Directory to save figure.
        n: Number of top and bottom counties to show.
    """
    sorted_df = county_metrics.sort_values("MAPE")
    top_n = sorted_df.head(n).copy()
    bottom_n = sorted_df.tail(n).copy()

    # Combine with separator
    combined = pd.concat([top_n, bottom_n])

    fig, ax = plt.subplots(figsize=(10, max(6, n * 0.6)))

    y_positions = range(len(combined))
    colors = [COLORS.get(m, "#95a5a6") for m in combined["ModelType"]]

    # Lollipop stems
    ax.hlines(y=y_positions, xmin=0, xmax=combined["MAPE"], color=colors, alpha=0.7, lw=2)

    # Lollipop heads
    ax.scatter(combined["MAPE"], y_positions, c=colors, s=100, zorder=5)

    # Labels
    labels = [f"{row['County']} ({row['ModelType']})" for _, row in combined.iterrows()]
    ax.set_yticks(y_positions)
    ax.set_yticklabels(labels)

    # Value annotations
    for i, (_, row) in enumerate(combined.iterrows()):
        ax.text(row["MAPE"] + 0.3, i, f"{row['MAPE']:.1f}%", va="center", fontsize=9)

    # Separator line
    ax.axhline(y=n - 0.5, color="black", linestyle="-", lw=1)
    ax.text(ax.get_xlim()[1] * 0.5, n - 0.5, f"  Top {n} ▲ | ▼ Bottom {n}  ",
            ha="center", va="center", fontsize=10,
            bbox=dict(boxstyle="round", facecolor="white", edgecolor="gray"))

    ax.set_xlabel("MAPE (%)", fontsize=12)
    ax.set_title(f"County Forecast Performance: Top {n} vs Bottom {n}", fontsize=14)
    ax.set_xlim(0, combined["MAPE"].max() * 1.15)

    # Legend for model types
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=COLORS[m], label=m) for m in ["ESM", "ARIMA", "UCM"]]
    ax.legend(handles=legend_elements, loc="lower right")

    plt.tight_layout()
    suffix = f"{n}x{n}"
    fig.savefig(output_dir / f"fig-07-county-performance-{suffix}.png", dpi=DPI)
    plt.close(fig)
    print(f"[ok] fig-07-county-performance-{suffix}.png")


def main():
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
    args = parser.parse_args()

    script_dir = Path(__file__).parent
    output_dir = Path(args.output)
    data_dir = Path(args.data)

    if not output_dir.is_absolute():
        output_dir = script_dir / output_dir
    if not data_dir.is_absolute():
        data_dir = script_dir / data_dir

    output_dir.mkdir(parents=True, exist_ok=True)

    print("[i] Loading validation data...")
    comparison, model_metrics = load_validation_data(data_dir)
    county_metrics = pd.read_csv(data_dir / "sas-validation-by-county.csv")
    print(f"    {len(comparison)} observations loaded")

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


if __name__ == "__main__":
    main()
