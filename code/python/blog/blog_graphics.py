#!/usr/bin/env python3
"""
Blog Graphics Generator for EV Pulse NC

This module provides functions to create publication-quality graphics
optimized for LinkedIn and Substack blog posts.

Features:
- Stat cards for key metrics
- Multi-panel infographics
- Social media preview images
- Interactive Plotly charts (for web embedding)

Usage:
    from blog_graphics import (
        create_stat_card,
        create_stat_grid,
        create_social_preview,
        create_comparison_chart
    )

    # Create a stat card
    create_stat_card('1,727%', 'BEV Growth', 'stat_card.png')

    # Create social preview
    create_social_preview(
        "NC's EV Revolution",
        "94,000 vehicles. 1,700 chargers. Do the math.",
        "preview.png"
    )

Author: Wolfgang Sanyer
Project: EV Pulse NC
Date: February 2026
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patheffects import withStroke
import numpy as np
from pathlib import Path
from typing import Optional, Union, Literal

# Try to import Pillow for social previews
try:
    from PIL import Image, ImageDraw, ImageFont
    HAS_PILLOW = True
except ImportError:
    HAS_PILLOW = False
    print("Warning: Pillow not installed. Social preview images unavailable.")
    print("Install with: pip install pillow")

# Try to import Plotly for interactive charts
try:
    import plotly.express as px
    import plotly.graph_objects as go
    HAS_PLOTLY = True
except ImportError:
    HAS_PLOTLY = False


# =============================================================================
# COLOR PALETTE - Blog-Optimized
# =============================================================================

BLOG_COLORS = {
    # Primary accent colors
    "primary": "#2ecc71",      # Emerald green (EV/sustainability)
    "secondary": "#3498db",    # Blue (trust/data)
    "accent": "#9b59b6",       # Purple (insight/premium)
    "warning": "#f39c12",      # Orange (attention)
    "alert": "#e74c3c",        # Red (urgency/gap)

    # Backgrounds
    "dark_bg": "#1a365d",      # Dark blue (professional)
    "light_bg": "#f7fafc",     # Off-white
    "card_bg": "#ffffff",      # White

    # Text
    "text_dark": "#2d3748",    # Near-black
    "text_light": "#718096",   # Gray
    "text_white": "#ffffff",   # White

    # Chart colors (ordered for comparison)
    "chart_1": "#2ecc71",
    "chart_2": "#3498db",
    "chart_3": "#9b59b6",
    "chart_4": "#f39c12",
    "chart_5": "#e74c3c",
}


# =============================================================================
# STAT CARDS
# =============================================================================

def create_stat_card(
    value: str,
    label: str,
    output_path: Union[str, Path],
    color: str = BLOG_COLORS["primary"],
    size: tuple[float, float] = (3, 2.5),
    dpi: int = 300,
) -> Path:
    """
    Create a single statistic card for blog infographics.

    Args:
        value: The main statistic value (e.g., "1,727%", "94,371", "$109M")
        label: Description label (e.g., "BEV Growth\\n(2018-2025)")
        output_path: Where to save the image
        color: Accent color for the card
        size: Figure size in inches (width, height)
        dpi: Resolution for export

    Returns:
        Path to saved image

    Example:
        >>> create_stat_card('16.9', 'BEVs per\\nCharging Port', 'stat.png')
    """
    fig, ax = plt.subplots(figsize=size)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    fig.patch.set_facecolor('white')

    # Card background with rounded corners
    card = patches.FancyBboxPatch(
        (0.05, 0.05), 0.9, 0.9,
        boxstyle="round,pad=0.02,rounding_size=0.08",
        facecolor=color,
        alpha=0.12,
        edgecolor=color,
        linewidth=3
    )
    ax.add_patch(card)

    # Top accent bar
    accent_bar = patches.Rectangle(
        (0.05, 0.85), 0.9, 0.1,
        facecolor=color,
        alpha=0.9
    )
    ax.add_patch(accent_bar)

    # Large stat value
    ax.text(
        0.5, 0.52,
        value,
        fontsize=42,
        fontweight='bold',
        ha='center',
        va='center',
        color=color,
        path_effects=[withStroke(linewidth=1, foreground='white')]
    )

    # Label below
    ax.text(
        0.5, 0.18,
        label,
        fontsize=11,
        ha='center',
        va='center',
        color=BLOG_COLORS["text_dark"],
        linespacing=1.3
    )

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=dpi, bbox_inches='tight',
                facecolor='white', edgecolor='none', pad_inches=0.1)
    plt.close(fig)

    return output_path


def create_stat_grid(
    stats: dict[str, str],
    title: str,
    output_path: Union[str, Path],
    colors: Optional[list[str]] = None,
    dpi: int = 300,
) -> Path:
    """
    Create a multi-panel grid of statistic cards.

    Args:
        stats: Dictionary of {label: value} pairs
        title: Main title above the grid
        output_path: Where to save the image
        colors: List of colors (cycles if fewer than stats)
        dpi: Resolution for export

    Returns:
        Path to saved image

    Example:
        >>> create_stat_grid(
        ...     {'BEV Growth': '1,727%', 'Total BEVs': '94,371',
        ...      'BEVs/Port': '16.9', 'NEVI Funding': '$109M'},
        ...     'NC EV Infrastructure Snapshot',
        ...     'infographic.png'
        ... )
    """
    n_stats = len(stats)
    if colors is None:
        colors = [
            BLOG_COLORS["primary"],
            BLOG_COLORS["secondary"],
            BLOG_COLORS["accent"],
            BLOG_COLORS["warning"],
            BLOG_COLORS["alert"],
        ]

    # Determine grid layout
    if n_stats <= 2:
        n_cols = n_stats
        n_rows = 1
    elif n_stats <= 4:
        n_cols = 2
        n_rows = 2
    elif n_stats <= 6:
        n_cols = 3
        n_rows = 2
    else:
        n_cols = 4
        n_rows = (n_stats + 3) // 4

    fig_width = n_cols * 2.8
    fig_height = n_rows * 2.2 + 0.8  # Extra for title

    fig, axes = plt.subplots(n_rows, n_cols, figsize=(fig_width, fig_height))
    fig.patch.set_facecolor('white')

    # Flatten axes for iteration
    if n_stats == 1:
        axes = np.array([[axes]])
    elif n_rows == 1:
        axes = np.array([axes])

    axes_flat = axes.flatten()

    for idx, ((label, value), ax) in enumerate(zip(stats.items(), axes_flat)):
        color = colors[idx % len(colors)]

        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')

        # Circular background
        circle = plt.Circle((0.5, 0.55), 0.35, color=color, alpha=0.15)
        ax.add_patch(circle)
        circle_border = plt.Circle(
            (0.5, 0.55), 0.35,
            fill=False, color=color, linewidth=3
        )
        ax.add_patch(circle_border)

        # Value
        ax.text(
            0.5, 0.55,
            value,
            fontsize=24,
            fontweight='bold',
            ha='center',
            va='center',
            color=color
        )

        # Label
        ax.text(
            0.5, 0.08,
            label,
            fontsize=9,
            ha='center',
            va='center',
            color=BLOG_COLORS["text_dark"],
            wrap=True
        )

    # Hide unused axes
    for ax in axes_flat[n_stats:]:
        ax.axis('off')

    # Title
    fig.suptitle(
        title,
        fontsize=14,
        fontweight='bold',
        color=BLOG_COLORS["text_dark"],
        y=0.98
    )

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=dpi, bbox_inches='tight',
                facecolor='white', pad_inches=0.3)
    plt.close(fig)

    return output_path


# =============================================================================
# SOCIAL MEDIA PREVIEW IMAGES
# =============================================================================

def create_social_preview(
    title: str,
    subtitle: str,
    output_path: Union[str, Path],
    platform: Literal["linkedin", "twitter", "substack"] = "linkedin",
    bg_color: str = BLOG_COLORS["dark_bg"],
    accent_color: str = BLOG_COLORS["primary"],
    dpi: int = 150,
) -> Path:
    """
    Create a social media preview image.

    Uses Pillow if available, falls back to matplotlib.

    Args:
        title: Main title (keep under 60 characters)
        subtitle: Subtitle/tagline (keep under 100 characters)
        output_path: Where to save the image
        platform: Target platform (affects dimensions)
        bg_color: Background color
        accent_color: Accent bar color
        dpi: Resolution (150 is fine for social)

    Returns:
        Path to saved image

    Example:
        >>> create_social_preview(
        ...     "NC's EV Revolution: 1,727% Growth",
        ...     "How infrastructure is struggling to keep pace",
        ...     "linkedin_preview.png"
        ... )
    """
    # Platform-specific dimensions
    sizes = {
        "linkedin": (1200, 628),
        "twitter": (1200, 675),
        "substack": (1456, 600),
    }
    size = sizes.get(platform, sizes["linkedin"])

    if HAS_PILLOW:
        return _create_preview_pillow(
            title, subtitle, output_path, size, bg_color, accent_color
        )
    else:
        return _create_preview_matplotlib(
            title, subtitle, output_path, size, bg_color, accent_color, dpi
        )


def _create_preview_pillow(
    title: str,
    subtitle: str,
    output_path: Union[str, Path],
    size: tuple[int, int],
    bg_color: str,
    accent_color: str,
) -> Path:
    """Create preview using Pillow (preferred)."""
    img = Image.new('RGB', size, color=bg_color)
    draw = ImageDraw.Draw(img)

    # Try to load fonts
    try:
        title_font = ImageFont.truetype('arial.ttf', 52)
        subtitle_font = ImageFont.truetype('arial.ttf', 26)
    except OSError:
        try:
            # Linux fallback
            title_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 52)
            subtitle_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 26)
        except OSError:
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()

    # Subtle gradient overlay
    for i in range(size[1]):
        alpha = int(30 * (1 - i / size[1]))
        draw.line([(0, i), (size[0], i)], fill=(255, 255, 255, alpha))

    # Title
    title_y = size[1] // 2 - 50
    draw.text((60, title_y), title, font=title_font, fill='white')

    # Subtitle
    subtitle_y = size[1] // 2 + 30
    draw.text((60, subtitle_y), subtitle, font=subtitle_font, fill='#a0aec0')

    # Accent bar at bottom
    bar_height = 8
    # Convert hex to RGB
    accent_rgb = tuple(int(accent_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
    draw.rectangle(
        [(0, size[1] - bar_height), (size[0], size[1])],
        fill=accent_rgb
    )

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(output_path, quality=95)

    return output_path


def _create_preview_matplotlib(
    title: str,
    subtitle: str,
    output_path: Union[str, Path],
    size: tuple[int, int],
    bg_color: str,
    accent_color: str,
    dpi: int,
) -> Path:
    """Create preview using matplotlib (fallback)."""
    fig_width = size[0] / dpi
    fig_height = size[1] / dpi

    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    fig.patch.set_facecolor(bg_color)
    ax.set_facecolor(bg_color)

    # Title
    ax.text(
        0.05, 0.55,
        title,
        fontsize=28,
        fontweight='bold',
        color='white',
        va='center'
    )

    # Subtitle
    ax.text(
        0.05, 0.4,
        subtitle,
        fontsize=14,
        color='#a0aec0',
        va='center'
    )

    # Accent bar
    bar = patches.Rectangle(
        (0, 0), 1, 0.02,
        facecolor=accent_color,
        transform=ax.transAxes
    )
    ax.add_patch(bar)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(
        output_path, dpi=dpi, bbox_inches='tight',
        facecolor=bg_color, pad_inches=0
    )
    plt.close(fig)

    return output_path


# =============================================================================
# COMPARISON CHARTS
# =============================================================================

def create_comparison_bar(
    labels: list[str],
    values: list[float],
    output_path: Union[str, Path],
    title: str = "",
    ylabel: str = "",
    reference_line: Optional[float] = None,
    reference_label: str = "",
    colors: Optional[list[str]] = None,
    dpi: int = 300,
) -> Path:
    """
    Create a horizontal bar chart for comparisons.

    Args:
        labels: Category labels
        values: Corresponding values
        output_path: Where to save
        title: Chart title
        ylabel: Y-axis label
        reference_line: Optional horizontal reference line
        reference_label: Label for reference line
        colors: Bar colors (uses default palette if None)
        dpi: Resolution

    Returns:
        Path to saved image
    """
    if colors is None:
        colors = [BLOG_COLORS["primary"]] * len(labels)

    fig, ax = plt.subplots(figsize=(8, max(4, len(labels) * 0.5)))

    y_pos = np.arange(len(labels))
    bars = ax.barh(y_pos, values, color=colors, edgecolor='white', height=0.6)

    # Reference line
    if reference_line is not None:
        ax.axvline(
            x=reference_line,
            color=BLOG_COLORS["alert"],
            linestyle='--',
            linewidth=2,
            label=reference_label
        )

    # Value labels
    for bar, val in zip(bars, values):
        ax.text(
            val + max(values) * 0.02,
            bar.get_y() + bar.get_height() / 2,
            f'{val:,.1f}' if isinstance(val, float) else str(val),
            va='center',
            fontsize=9
        )

    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels)
    ax.set_xlabel(ylabel)
    ax.set_title(title, fontweight='bold', pad=10)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    if reference_line is not None:
        ax.legend(loc='lower right')

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=dpi, bbox_inches='tight', facecolor='white')
    plt.close(fig)

    return output_path


# =============================================================================
# INTERACTIVE CHARTS (PLOTLY)
# =============================================================================

def create_interactive_line(
    data: "pd.DataFrame",
    x_col: str,
    y_col: str,
    output_path: Union[str, Path],
    title: str = "",
    color_col: Optional[str] = None,
) -> Optional[Path]:
    """
    Create an interactive Plotly line chart.

    Args:
        data: pandas DataFrame with the data
        x_col: Column name for x-axis
        y_col: Column name for y-axis
        output_path: Where to save (.html for interactive, .png for static)
        title: Chart title
        color_col: Column for color grouping (optional)

    Returns:
        Path to saved file, or None if Plotly not available
    """
    if not HAS_PLOTLY:
        print("Warning: Plotly not installed. Skipping interactive chart.")
        return None

    fig = px.line(
        data,
        x=x_col,
        y=y_col,
        color=color_col,
        title=title,
        template='plotly_white'
    )

    fig.update_layout(
        font_family="Arial",
        title_font_size=16,
        hovermode='x unified'
    )

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if output_path.suffix == '.html':
        fig.write_html(output_path)
    else:
        fig.write_image(output_path, scale=2)

    return output_path


# =============================================================================
# QUICK TEMPLATES - EV PULSE NC SPECIFIC
# =============================================================================

def create_ev_pulse_hero(output_path: Union[str, Path]) -> Path:
    """Create the standard EV Pulse NC hero/preview image."""
    return create_social_preview(
        "NC's EV Infrastructure Gap",
        "94,371 EVs. 1,725 chargers. Where should $109M go?",
        output_path,
        platform="linkedin"
    )


def create_ev_pulse_stats(output_path: Union[str, Path]) -> Path:
    """Create the standard EV Pulse NC statistics infographic."""
    return create_stat_grid(
        {
            'BEV Growth': '1,727%',
            'Total BEVs': '94,371',
            'BEVs/Port': '16.9',
            'NEVI Funding': '$109M'
        },
        'North Carolina EV Infrastructure: Key Numbers',
        output_path
    )


# =============================================================================
# MAIN - Demo
# =============================================================================

if __name__ == "__main__":
    output_dir = Path(__file__).parent.parent.parent.parent / "output" / "blog"
    output_dir.mkdir(parents=True, exist_ok=True)

    print("Generating blog graphics demo...")

    # Stat card
    path = create_stat_card(
        '1,727%',
        'BEV Growth\n(2018-2025)',
        output_dir / 'demo-stat-card.png'
    )
    print(f"  Created: {path}")

    # Stat grid
    path = create_stat_grid(
        {
            'BEV Growth': '1,727%',
            'Total BEVs': '94,371',
            'BEVs/Port': '16.9',
            'NEVI Funding': '$109M'
        },
        'North Carolina EV Infrastructure Snapshot',
        output_dir / 'demo-stat-grid.png'
    )
    print(f"  Created: {path}")

    # Social preview
    path = create_social_preview(
        "NC's EV Revolution: 1,727% Growth",
        "How 94,000 electric vehicles are reshaping infrastructure needs",
        output_dir / 'demo-linkedin-preview.png',
        platform='linkedin'
    )
    print(f"  Created: {path}")

    # Comparison bar
    path = create_comparison_bar(
        labels=['Wake', 'Mecklenburg', 'Durham', 'Guilford', 'Forsyth'],
        values=[18500, 12300, 8200, 4100, 3200],
        output_path=output_dir / 'demo-comparison-bar.png',
        title='Top 5 Counties by BEV Registrations',
        ylabel='BEV Count',
        reference_line=10000,
        reference_label='10K threshold'
    )
    print(f"  Created: {path}")

    print(f"\nAll demo graphics saved to: {output_dir}")
