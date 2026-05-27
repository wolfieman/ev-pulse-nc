#!/usr/bin/env python3
"""
Publication-Ready Figure Styling for EV Pulse NC

This module provides a comprehensive matplotlib/seaborn styling configuration
optimized for academic publication standards. Import and call setup_publication_style()
at the beginning of any figure generation script.

Features:
- 600 DPI for print-quality resolution
- IEEE/Elsevier/PLOS-compatible figure dimensions
- Colorblind-friendly palette (IBM Design Library)
- Cross-platform font stack with fallbacks
- Consistent typography hierarchy

Usage:
    from evpulse.style import setup_publication_style, COLORS, save_figure
    setup_publication_style()
    # ... create your figures ...
    save_figure(fig, "my-figure", output_dir)

Copyright © 2026 Wolfgang Sanyer
Licensed under the Polyform Noncommercial License 1.0.0 (see LICENSE).
"""
from __future__ import annotations

from pathlib import Path
from typing import Literal

import matplotlib.pyplot as plt

# =============================================================================
# COLOR PALETTE - IBM Design Library (Colorblind Safe)
# =============================================================================
# This palette passes WCAG 2.1 AAA contrast requirements and is distinguishable
# by people with deuteranopia, protanopia, and tritanopia.

COLORS = {
    # Primary model colors (Flat UI - vivid and modern)
    "ESM": "#2ecc71",  # Emerald Green - fresh, vibrant
    "ARIMA": "#3498db",  # Peter River Blue - classic, trustworthy
    "UCM": "#9b59b6",  # Amethyst Purple - distinctive, sophisticated
    # Semantic colors
    "positive": "#2ecc71",  # Green
    "negative": "#e74c3c",  # Alizarin Red - vivid warning
    "neutral": "#3498db",  # Blue
    "highlight": "#f39c12",  # Orange - attention-grabbing
    "reference": "#2c3e50",  # Dark slate for reference lines
    # Grays for annotations
    "gray_dark": "#525252",
    "gray_medium": "#8D8D8D",
    "gray_light": "#C6C6C6",
    "gray_bg": "#F4F4F4",
}

# Sequential palettes for heatmaps/gradients (colorblind safe)
PALETTE_SEQUENTIAL = [
    "#FFF7FB",
    "#ECE7F2",
    "#D0D1E6",
    "#A6BDDB",
    "#74A9CF",
    "#3690C0",
    "#0570B0",
    "#034E7B",
]

# Model color list for iteration
MODEL_COLORS = [COLORS["ESM"], COLORS["ARIMA"], COLORS["UCM"]]


# =============================================================================
# PUBLICATION STANDARDS
# =============================================================================

# Standard figure dimensions (width, height) in inches
FIGURE_SIZES = {
    "small_square": (3.5, 3.5),
    "medium_square": (5.0, 5.0),
    "large_square": (7.0, 7.0),
    "wide": (7.0, 4.0),
    "tall": (3.5, 5.5),
    "subplot_2col": (7.0, 3.5),
    "subplot_3col": (7.0, 2.5),
}

# Export settings
EXPORT_DPI = 600  # Print quality (300 min, 600 recommended)
SCREEN_DPI = 150  # For preview/screen display


# =============================================================================
# TYPOGRAPHY - Cross-Platform Font Stack
# =============================================================================

# Font family priority (first available will be used)
FONT_FAMILIES = [
    "Times New Roman",  # Windows/Mac - classic academic
    "Liberation Serif",  # Linux equivalent
    "DejaVu Serif",  # Cross-platform fallback
    "serif",  # System default
]

# Sans-serif alternative for presentations/posters
FONT_FAMILIES_SANS = [
    "Arial",
    "Helvetica",
    "Liberation Sans",
    "DejaVu Sans",
    "sans-serif",
]

# Font sizes (based on 10pt body text standard)
FONT_SIZES = {
    "title": 11,
    "subtitle": 10,
    "axis_label": 10,
    "tick_label": 9,
    "legend": 9,
    "annotation": 8,
    "caption": 8,
}


# =============================================================================
# RCPARAMS CONFIGURATION
# =============================================================================


def get_publication_rcparams(
    use_serif: bool = True,
    use_latex: bool = False,
) -> dict:
    """
    Return matplotlib rcParams dictionary for publication-quality figures.

    Args:
        use_serif: If True, use serif fonts (academic papers).
                   If False, use sans-serif (presentations).
        use_latex: If True, enable LaTeX rendering (requires LaTeX installation).

    Returns:
        Dictionary of rcParams settings.
    """
    font_family = FONT_FAMILIES if use_serif else FONT_FAMILIES_SANS

    rcparams = {
        # =====================================================================
        # FIGURE
        # =====================================================================
        "figure.figsize": (7.0, 4.5),
        "figure.dpi": SCREEN_DPI,
        "figure.facecolor": "white",
        "figure.edgecolor": "white",
        "figure.autolayout": False,  # We'll use tight_layout manually
        "figure.constrained_layout.use": True,  # Better than tight_layout
        # =====================================================================
        # FONT
        # =====================================================================
        "font.family": font_family[0] if not use_latex else "serif",
        "font.size": FONT_SIZES["tick_label"],
        "font.weight": "normal",
        # =====================================================================
        # TEXT
        # =====================================================================
        "text.usetex": use_latex,
        "text.color": COLORS["gray_dark"],
        # =====================================================================
        # AXES
        # =====================================================================
        "axes.titlesize": FONT_SIZES["title"],
        "axes.titleweight": "bold",
        "axes.titlepad": 12,
        "axes.labelsize": FONT_SIZES["axis_label"],
        "axes.labelweight": "normal",
        "axes.labelpad": 8,
        "axes.labelcolor": COLORS["gray_dark"],
        "axes.linewidth": 0.8,
        "axes.edgecolor": COLORS["gray_medium"],
        "axes.facecolor": "white",
        "axes.grid": True,
        "axes.grid.axis": "both",
        "axes.axisbelow": True,  # Grid behind data
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.prop_cycle": plt.cycler(color=MODEL_COLORS),
        # =====================================================================
        # GRID
        # =====================================================================
        "grid.color": COLORS["gray_light"],
        "grid.linestyle": "-",
        "grid.linewidth": 0.5,
        "grid.alpha": 0.7,
        # =====================================================================
        # TICKS
        # =====================================================================
        "xtick.labelsize": FONT_SIZES["tick_label"],
        "ytick.labelsize": FONT_SIZES["tick_label"],
        "xtick.color": COLORS["gray_dark"],
        "ytick.color": COLORS["gray_dark"],
        "xtick.direction": "out",
        "ytick.direction": "out",
        "xtick.major.size": 4,
        "ytick.major.size": 4,
        "xtick.major.width": 0.8,
        "ytick.major.width": 0.8,
        "xtick.minor.size": 2,
        "ytick.minor.size": 2,
        "xtick.major.pad": 6,
        "ytick.major.pad": 6,
        # =====================================================================
        # LEGEND
        # =====================================================================
        "legend.fontsize": FONT_SIZES["legend"],
        "legend.frameon": True,
        "legend.framealpha": 0.95,
        "legend.facecolor": "white",
        "legend.edgecolor": COLORS["gray_light"],
        "legend.borderpad": 0.5,
        "legend.labelspacing": 0.4,
        "legend.handlelength": 1.5,
        "legend.handleheight": 0.7,
        "legend.handletextpad": 0.5,
        "legend.columnspacing": 1.0,
        "legend.markerscale": 1.0,
        # =====================================================================
        # LINES
        # =====================================================================
        "lines.linewidth": 1.5,
        "lines.markersize": 6,
        "lines.markeredgewidth": 0.8,
        "lines.markeredgecolor": "white",
        # =====================================================================
        # SCATTER
        # =====================================================================
        "scatter.edgecolors": "white",
        # =====================================================================
        # PATCHES (bars, etc.)
        # =====================================================================
        "patch.linewidth": 0.8,
        "patch.edgecolor": "white",
        "patch.facecolor": COLORS["ESM"],
        # =====================================================================
        # HISTOGRAM
        # =====================================================================
        "hist.bins": "auto",
        # =====================================================================
        # BOXPLOT
        # =====================================================================
        "boxplot.boxprops.linewidth": 1.0,
        "boxplot.whiskerprops.linewidth": 1.0,
        "boxplot.capprops.linewidth": 1.0,
        "boxplot.medianprops.linewidth": 1.5,
        "boxplot.medianprops.color": COLORS["negative"],
        "boxplot.flierprops.marker": "o",
        "boxplot.flierprops.markersize": 4,
        "boxplot.flierprops.markerfacecolor": COLORS["gray_medium"],
        "boxplot.flierprops.markeredgecolor": "white",
        # =====================================================================
        # ERRORBAR
        # =====================================================================
        "errorbar.capsize": 3,
        # =====================================================================
        # SAVING
        # =====================================================================
        "savefig.dpi": EXPORT_DPI,
        "savefig.facecolor": "white",
        "savefig.edgecolor": "white",
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.1,
        "savefig.transparent": False,
        # =====================================================================
        # PDF/SVG EXPORT
        # =====================================================================
        "pdf.fonttype": 42,  # TrueType (editable text in PDF)
        "ps.fonttype": 42,
        "svg.fonttype": "none",  # Text as text, not paths
    }

    return rcparams


def setup_publication_style(
    use_serif: bool = True,
    use_latex: bool = False,
    context: Literal["paper", "notebook", "talk", "poster"] = "paper",
) -> None:
    """
    Apply publication-ready styling to all matplotlib/seaborn figures.

    Call this function once at the beginning of your script, before creating
    any figures.

    Args:
        use_serif: If True, use serif fonts (academic papers).
                   If False, use sans-serif (presentations).
        use_latex: If True, enable LaTeX rendering for math.
                   Requires LaTeX installation.
        context: Scaling context:
                 - "paper": Default, optimized for journal figures
                 - "notebook": Slightly larger for Jupyter
                 - "talk": Larger fonts for presentations
                 - "poster": Largest fonts for posters

    Example:
        >>> from publication_style import setup_publication_style
        >>> setup_publication_style()
        >>> # Now create your figures
        >>> fig, ax = plt.subplots()
    """
    # Get base rcparams
    rcparams = get_publication_rcparams(use_serif=use_serif, use_latex=use_latex)

    # Apply context scaling
    scale_factors = {
        "paper": 1.0,
        "notebook": 1.1,
        "talk": 1.3,
        "poster": 1.5,
    }
    scale = scale_factors.get(context, 1.0)

    if scale != 1.0:
        # Scale font sizes
        for key in rcparams:
            if "size" in key and isinstance(rcparams[key], (int, float)):
                rcparams[key] = rcparams[key] * scale
        # Scale line widths
        for key in ["lines.linewidth", "axes.linewidth", "grid.linewidth"]:
            if key in rcparams:
                rcparams[key] = rcparams[key] * scale

    # Apply all settings
    plt.rcParams.update(rcparams)

    # Try to set up seaborn if available
    try:
        import seaborn as sns

        sns.set_theme(style="whitegrid", rc=rcparams)
    except ImportError:
        pass


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================


def save_figure(
    fig: plt.Figure,
    filename: str,
    output_dir: Path,
    formats: list[str] | None = None,
    dpi: int | None = None,
) -> list[Path]:
    """
    Save figure in multiple formats with publication-quality settings.

    Args:
        fig: Matplotlib figure to save.
        filename: Base filename (without extension).
        output_dir: Directory to save figures.
        formats: List of formats to export (png, pdf, svg, eps, tiff).
        dpi: Override DPI (default uses EXPORT_DPI=600).

    Returns:
        List of saved file paths.

    Example:
        >>> save_figure(fig, "fig-01-scatter", Path("./figures"))
        [Path('./figures/fig-01-scatter.png'), Path('./figures/fig-01-scatter.pdf')]
    """
    if formats is None:
        formats = ["png", "pdf"]
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    saved_paths = []
    export_dpi = dpi or EXPORT_DPI

    for fmt in formats:
        filepath = output_dir / f"{filename}.{fmt}"

        # Format-specific settings
        if fmt == "pdf":
            # Omit the CreationDate metadata, which matplotlib otherwise stamps
            # with the wall clock. Without this every regeneration rewrites the
            # tracked output/figures/*.pdf with a new timestamp, producing
            # spurious diffs even when the figure is byte-identical otherwise.
            fig.savefig(
                filepath,
                format="pdf",
                dpi=export_dpi,
                bbox_inches="tight",
                pad_inches=0.1,
                metadata={"CreationDate": None},
            )
        elif fmt == "svg":
            fig.savefig(filepath, format="svg", bbox_inches="tight", pad_inches=0.1)
        elif fmt == "eps":
            fig.savefig(
                filepath,
                format="eps",
                dpi=export_dpi,
                bbox_inches="tight",
                pad_inches=0.1,
            )
        elif fmt == "tiff":
            fig.savefig(
                filepath,
                format="tiff",
                dpi=export_dpi,
                bbox_inches="tight",
                pad_inches=0.1,
                pil_kwargs={"compression": "tiff_lzw"},
            )
        else:  # png and others
            fig.savefig(
                filepath,
                format=fmt,
                dpi=export_dpi,
                bbox_inches="tight",
                pad_inches=0.1,
            )

        saved_paths.append(filepath)

    return saved_paths


def add_panel_label(
    ax: plt.Axes,
    label: str,
    loc: Literal[
        "upper left", "upper right", "lower left", "lower right"
    ] = "upper left",
    fontsize: int | None = None,
    fontweight: str = "bold",
    offset: tuple[float, float] = (0.02, 0.98),
) -> None:
    """
    Add panel label (A, B, C, etc.) to subplot for multi-panel figures.

    Args:
        ax: Matplotlib axes.
        label: Panel label (e.g., "A", "B", "(a)", "(b)").
        loc: Position of label.
        fontsize: Font size (default: title size + 1).
        fontweight: Font weight.
        offset: (x, y) offset in axes coordinates.

    Example:
        >>> fig, axes = plt.subplots(1, 2)
        >>> add_panel_label(axes[0], "A")
        >>> add_panel_label(axes[1], "B")
    """
    fontsize = fontsize or FONT_SIZES["title"] + 1

    positions = {
        "upper left": (offset[0], offset[1]),
        "upper right": (1 - offset[0], offset[1]),
        "lower left": (offset[0], offset[0]),
        "lower right": (1 - offset[0], offset[0]),
    }

    ha_map = {
        "upper left": "left",
        "upper right": "right",
        "lower left": "left",
        "lower right": "right",
    }
    va_map = {
        "upper left": "top",
        "upper right": "top",
        "lower left": "bottom",
        "lower right": "bottom",
    }

    x, y = positions.get(loc, positions["upper left"])

    ax.text(
        x,
        y,
        label,
        transform=ax.transAxes,
        fontsize=fontsize,
        fontweight=fontweight,
        ha=ha_map.get(loc, "left"),
        va=va_map.get(loc, "top"),
    )


def add_stats_annotation(
    ax: plt.Axes,
    text: str,
    loc: Literal[
        "upper left", "upper right", "lower left", "lower right"
    ] = "upper right",
    fontsize: int | None = None,
    boxstyle: str = "round,pad=0.4",
    facecolor: str = "#FFFDE7",  # Light yellow
    alpha: float = 0.9,
    offset: tuple[float, float] = (0.02, 0.02),
) -> None:
    """
    Add statistics annotation box to plot.

    Args:
        ax: Matplotlib axes.
        text: Annotation text (supports newlines).
        loc: Position of annotation box.
        fontsize: Font size (default: annotation size).
        boxstyle: Matplotlib boxstyle string.
        facecolor: Background color of box.
        alpha: Box transparency.
        offset: (x, y) offset from corner.
    """
    fontsize = fontsize or FONT_SIZES["annotation"]

    positions = {
        "upper left": (offset[0], 1 - offset[1]),
        "upper right": (1 - offset[0], 1 - offset[1]),
        "lower left": (offset[0], offset[1]),
        "lower right": (1 - offset[0], offset[1]),
    }

    ha_map = {
        "upper left": "left",
        "upper right": "right",
        "lower left": "left",
        "lower right": "right",
    }
    va_map = {
        "upper left": "top",
        "upper right": "top",
        "lower left": "bottom",
        "lower right": "bottom",
    }

    x, y = positions.get(loc, positions["upper right"])

    ax.annotate(
        text,
        xy=(x, y),
        xycoords="axes fraction",
        fontsize=fontsize,
        ha=ha_map.get(loc, "right"),
        va=va_map.get(loc, "top"),
        bbox=dict(
            boxstyle=boxstyle,
            facecolor=facecolor,
            edgecolor=COLORS["gray_light"],
            alpha=alpha,
        ),
    )


# =============================================================================
# FIGURE-TYPE-SPECIFIC STYLE HELPERS
# =============================================================================


def style_boxplot(
    bp: dict,
    colors: list[str] | None = None,
    alpha: float = 0.7,
) -> None:
    """
    Apply styling to boxplot elements.

    Args:
        bp: Boxplot dict returned by ax.boxplot().
        colors: List of colors for each box.
        alpha: Transparency of box fills.
    """
    if colors is None:
        colors = MODEL_COLORS

    for _i, (box, color) in enumerate(zip(bp["boxes"], colors, strict=False)):
        box.set_facecolor(color)
        box.set_alpha(alpha)
        box.set_edgecolor(COLORS["gray_dark"])

    for whisker in bp["whiskers"]:
        whisker.set_color(COLORS["gray_dark"])

    for cap in bp["caps"]:
        cap.set_color(COLORS["gray_dark"])

    for median in bp["medians"]:
        median.set_color(COLORS["negative"])
        median.set_linewidth(2)
