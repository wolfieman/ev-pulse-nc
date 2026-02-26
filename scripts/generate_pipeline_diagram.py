"""
EV Pulse NC — Analytical Pipeline Architecture Diagram
BIDA 670 Capstone Project — Fayetteville State University

Generates a publication-quality pipeline visualization using matplotlib.
Output: docs/figures/analytical-pipeline.png (600 DPI)
        docs/figures/analytical-pipeline-thumb.png (150 DPI)
"""

import os
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.patheffects as pe
import numpy as np

# ─── Configuration ─────────────────────────────────────────────────────────────

# Output paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "docs", "figures")

# Colors
C_COMPLETE = "#366092"       # Dark blue — complete phases
C_NEXT = "#2E75B6"           # Slightly brighter blue for NEXT status
C_PENDING = "#5B9BD5"        # Medium blue — pending phases
C_OPTIONAL = "#D9D9D9"       # Light gray — optional phases
C_CONVERGE = "#548235"       # Dark green — convergence points
C_OUTPUT = "#ED7D31"         # Gold/amber — final output
C_ARROW = "#404040"          # Dark gray arrows
C_BG = "#FAFBFC"             # Very subtle off-white background
C_BORDER_COMPLETE = "#1F3864"
C_BORDER_NEXT = "#1F4E79"
C_BORDER_PENDING = "#2F5597"
C_BORDER_OPTIONAL = "#A6A6A6"
C_BORDER_CONVERGE = "#375623"
C_BORDER_OUTPUT = "#C55A11"
C_TEXT_LIGHT = "#FFFFFF"
C_TEXT_DARK = "#333333"
C_SUBTITLE = "#666666"
C_DATA_LABEL = "#555555"

# Font settings
FONT_FAMILY = "DejaVu Sans"
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = [FONT_FAMILY, "Arial", "Calibri", "Helvetica"]


# ─── Helper Functions ──────────────────────────────────────────────────────────

def draw_rounded_box(ax, x, y, width, height, facecolor, edgecolor,
                     linewidth=1.5, alpha=1.0, linestyle="-", zorder=2):
    """Draw a rounded rectangle centered at (x, y) and return it."""
    box = FancyBboxPatch(
        (x - width / 2, y - height / 2), width, height,
        boxstyle="round,pad=0.02,rounding_size=0.03",
        facecolor=facecolor, edgecolor=edgecolor,
        linewidth=linewidth, alpha=alpha, linestyle=linestyle,
        zorder=zorder, transform=ax.transData
    )
    ax.add_patch(box)
    return box


def draw_text(ax, x, y, text, fontsize=10, color="white", weight="normal",
              ha="center", va="center", zorder=3, fontstyle="normal"):
    """Draw text at a position."""
    ax.text(x, y, text, fontsize=fontsize, color=color, weight=weight,
            ha=ha, va=va, zorder=zorder, fontfamily=FONT_FAMILY,
            fontstyle=fontstyle)


def draw_arrow(ax, x_start, y_start, x_end, y_end, color=C_ARROW,
               linewidth=1.8, style="->", linestyle="-", zorder=1,
               connectionstyle="arc3,rad=0.0", mutation_scale=15):
    """Draw a curved or straight arrow between two points."""
    arrow = FancyArrowPatch(
        (x_start, y_start), (x_end, y_end),
        arrowstyle=style, color=color, linewidth=linewidth,
        linestyle=linestyle, zorder=zorder,
        connectionstyle=connectionstyle,
        mutation_scale=mutation_scale
    )
    ax.add_patch(arrow)
    return arrow


def draw_data_label(ax, x, y, text, fontsize=6.5, color=C_DATA_LABEL):
    """Draw a small italic data-flow label near an arrow."""
    ax.text(x, y, text, fontsize=fontsize, color=color, ha="center", va="center",
            fontstyle="italic", zorder=4, fontfamily=FONT_FAMILY,
            bbox=dict(boxstyle="round,pad=0.15", facecolor="white",
                      edgecolor="#E0E0E0", alpha=0.92, linewidth=0.5))


def draw_status_badge(ax, x, y, status, fontsize=7):
    """Draw a small status badge (COMPLETE, NEXT, PENDING, etc.)."""
    colors = {
        "COMPLETE": ("#E2EFDA", "#548235"),
        "NEXT": ("#FFF2CC", "#BF8F00"),
        "PENDING": ("#D6E4F0", "#2F5597"),
        "TBD": ("#F2F2F2", "#808080"),
        "OPTIONAL": ("#F2F2F2", "#808080"),
    }
    bg, fg = colors.get(status, ("#F2F2F2", "#808080"))
    ax.text(x, y, status, fontsize=fontsize, color=fg, ha="center", va="center",
            fontweight="bold", fontfamily=FONT_FAMILY, zorder=5,
            bbox=dict(boxstyle="round,pad=0.2", facecolor=bg,
                      edgecolor=fg, alpha=0.95, linewidth=0.8))


# ─── Main Diagram ─────────────────────────────────────────────────────────────

def create_pipeline_diagram():
    """Create the full analytical pipeline architecture diagram."""

    fig, ax = plt.subplots(1, 1, figsize=(12, 16))
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)

    # Set coordinate system (0-10 x, 0-16 y, origin at bottom)
    ax.set_xlim(-0.5, 10.5)
    ax.set_ylim(-0.5, 16.5)
    ax.set_aspect("equal")
    ax.axis("off")

    # ── Title ──────────────────────────────────────────────────────────────
    draw_text(ax, 5, 15.9, "EV Pulse NC", fontsize=22, color="#1F3864",
              weight="bold")
    draw_text(ax, 5, 15.45, "Analytical Pipeline Architecture", fontsize=16,
              color="#366092", weight="semibold")
    draw_text(ax, 5, 15.05, "BIDA 670 Capstone Project  \u2014  Fayetteville State University",
              fontsize=10, color=C_SUBTITLE)

    # Thin separator line
    ax.plot([1.5, 8.5], [14.75, 14.75], color="#C0C0C0", linewidth=0.8, zorder=1)

    # ── Layer labels (right margin) ────────────────────────────────────────
    layer_labels = [
        (14.1, "FOUNDATION"),
        (12.15, "CONVERGENCE"),
        (9.65, "ANALYTICAL\nLENSES"),
        (7.1, "SCORING"),
        (5.3, "OUTPUT"),
    ]
    for y_pos, label in layer_labels:
        ax.text(10.35, y_pos, label, fontsize=6, color="#B0B0B0", ha="right",
                va="center", fontweight="bold", fontfamily=FONT_FAMILY,
                rotation=0, fontstyle="normal", linespacing=1.1)

    # ════════════════════════════════════════════════════════════════════════
    # LAYER 1: FOUNDATION — Two parallel inputs
    # ════════════════════════════════════════════════════════════════════════

    box_w = 3.6
    box_h = 1.15
    y1 = 14.0

    # Phase 1 — Demand Validation (LEFT)
    x1_left = 2.6
    draw_rounded_box(ax, x1_left, y1, box_w, box_h, C_COMPLETE, C_BORDER_COMPLETE, linewidth=2)
    draw_text(ax, x1_left, y1 + 0.28, "Phase 1: Demand Validation", fontsize=9.5,
              color=C_TEXT_LIGHT, weight="bold")
    draw_text(ax, x1_left, y1 - 0.05, "BEV forecasts verified", fontsize=8,
              color="#B4C7E0")
    draw_text(ax, x1_left, y1 - 0.28, "MAPE 4.36%", fontsize=8.5,
              color="#D4E4F7", weight="semibold")
    draw_status_badge(ax, x1_left + box_w / 2 - 0.55, y1 + box_h / 2 + 0.22, "COMPLETE")

    # Phase 2 — Infrastructure Data (RIGHT)
    x1_right = 7.4
    draw_rounded_box(ax, x1_right, y1, box_w, box_h, C_COMPLETE, C_BORDER_COMPLETE, linewidth=2)
    draw_text(ax, x1_right, y1 + 0.28, "Phase 2: Infrastructure Data", fontsize=9.5,
              color=C_TEXT_LIGHT, weight="bold")
    draw_text(ax, x1_right, y1 - 0.05, "NC stations via AFDC API", fontsize=8,
              color="#B4C7E0")
    draw_text(ax, x1_right, y1 - 0.28, "1,985 stations", fontsize=8.5,
              color="#D4E4F7", weight="semibold")
    draw_status_badge(ax, x1_right + box_w / 2 - 0.55, y1 + box_h / 2 + 0.22, "COMPLETE")

    # ════════════════════════════════════════════════════════════════════════
    # Data flow labels from Layer 1
    # ════════════════════════════════════════════════════════════════════════

    draw_data_label(ax, 1.3, 13.0, "Validated BEV forecasts\nUnderprediction bias")
    draw_data_label(ax, 8.7, 13.0, "Station locations, ZIP codes\nCharging levels, facility types")

    # ════════════════════════════════════════════════════════════════════════
    # LAYER 2: CONVERGENCE — Gap Analysis
    # ════════════════════════════════════════════════════════════════════════

    y_gap = 12.15
    gap_w = 3.8
    gap_h = 0.85
    x_gap = 5.0

    # Arrows from Phase 1 & 2 down to Gap Analysis
    draw_arrow(ax, x1_left + 0.3, y1 - box_h / 2, x_gap - gap_w / 2 + 0.6, y_gap + gap_h / 2,
               linewidth=2.0, color="#4A6D8C")
    draw_arrow(ax, x1_right - 0.3, y1 - box_h / 2, x_gap + gap_w / 2 - 0.6, y_gap + gap_h / 2,
               linewidth=2.0, color="#4A6D8C")

    draw_rounded_box(ax, x_gap, y_gap, gap_w, gap_h, C_CONVERGE, C_BORDER_CONVERGE, linewidth=2.2)
    draw_text(ax, x_gap, y_gap + 0.12, "GAP ANALYSIS", fontsize=12,
              color=C_TEXT_LIGHT, weight="bold")
    draw_text(ax, x_gap, y_gap - 0.18, "Demand vs. Supply", fontsize=8,
              color="#C5DEB5")

    # ════════════════════════════════════════════════════════════════════════
    # LAYER 3: THREE ANALYTICAL LENSES
    # ════════════════════════════════════════════════════════════════════════

    y_lenses = 9.65
    lens_box_h = 1.55
    lens_w = 2.7
    x_lens = [1.8, 5.0, 8.2]

    # Three arrows branching down from Gap Analysis
    draw_arrow(ax, x_gap - 1.0, y_gap - gap_h / 2, x_lens[0], y_lenses + lens_box_h / 2,
               linewidth=1.8, color="#4A6D8C")
    draw_arrow(ax, x_gap, y_gap - gap_h / 2, x_lens[1], y_lenses + lens_box_h / 2,
               linewidth=1.8, color="#4A6D8C")
    draw_arrow(ax, x_gap + 1.0, y_gap - gap_h / 2, x_lens[2], y_lenses + lens_box_h / 2,
               linewidth=1.8, color="#4A6D8C")

    # Phase 3 — ZIP Code (WHERE) — NEXT
    draw_rounded_box(ax, x_lens[0], y_lenses, lens_w, lens_box_h, C_NEXT,
                     C_BORDER_NEXT, linewidth=2)
    draw_text(ax, x_lens[0], y_lenses + 0.45, "Phase 3", fontsize=8,
              color="#D4E4F7")
    draw_text(ax, x_lens[0], y_lenses + 0.15, "ZIP Code", fontsize=11,
              color=C_TEXT_LIGHT, weight="bold")
    draw_text(ax, x_lens[0], y_lenses - 0.12, "WHERE", fontsize=9,
              color="#D4E4F7", weight="semibold")
    draw_text(ax, x_lens[0], y_lenses - 0.40, "Sub-county gaps", fontsize=7.5,
              color="#B4C7E0")
    draw_text(ax, x_lens[0], y_lenses - 0.58, "4\u20136 hrs", fontsize=7,
              color="#A0B8D0")
    draw_status_badge(ax, x_lens[0] + lens_w / 2 - 0.4, y_lenses + lens_box_h / 2 + 0.22, "NEXT")

    # Phase 4 — CTPP Workplace (WHO) — PENDING
    draw_rounded_box(ax, x_lens[1], y_lenses, lens_w, lens_box_h, C_PENDING,
                     C_BORDER_PENDING, linewidth=1.8)
    draw_text(ax, x_lens[1], y_lenses + 0.45, "Phase 4", fontsize=8,
              color="#E8F0F8")
    draw_text(ax, x_lens[1], y_lenses + 0.15, "CTPP Workplace", fontsize=10.5,
              color=C_TEXT_LIGHT, weight="bold")
    draw_text(ax, x_lens[1], y_lenses - 0.12, "WHO", fontsize=9,
              color="#E0ECF5", weight="semibold")
    draw_text(ax, x_lens[1], y_lenses - 0.40, "Commuter charging", fontsize=7.5,
              color="#C0D4E8")
    draw_text(ax, x_lens[1], y_lenses - 0.58, "3 hrs", fontsize=7,
              color="#A8C4DC")
    draw_status_badge(ax, x_lens[1] + lens_w / 2 - 0.55, y_lenses + lens_box_h / 2 + 0.22, "PENDING")

    # Phase 5 — HEPGIS Equity (EQUITY) — PENDING
    draw_rounded_box(ax, x_lens[2], y_lenses, lens_w, lens_box_h, C_PENDING,
                     C_BORDER_PENDING, linewidth=1.8)
    draw_text(ax, x_lens[2], y_lenses + 0.45, "Phase 5", fontsize=8,
              color="#E8F0F8")
    draw_text(ax, x_lens[2], y_lenses + 0.15, "HEPGIS Equity", fontsize=10.5,
              color=C_TEXT_LIGHT, weight="bold")
    draw_text(ax, x_lens[2], y_lenses - 0.12, "EQUITY", fontsize=9,
              color="#E0ECF5", weight="semibold")
    draw_text(ax, x_lens[2], y_lenses - 0.40, "Justice40 communities", fontsize=7.5,
              color="#C0D4E8")
    draw_text(ax, x_lens[2], y_lenses - 0.58, "TBD", fontsize=7,
              color="#A8C4DC")
    draw_status_badge(ax, x_lens[2] + lens_w / 2 - 0.55, y_lenses + lens_box_h / 2 + 0.22, "PENDING")

    # ════════════════════════════════════════════════════════════════════════
    # Cross-feed arrows (secondary data flows)
    # ════════════════════════════════════════════════════════════════════════

    # Phase 2 feeds into Phase 3 (dashed)
    draw_arrow(ax, x1_right - box_w / 2 + 0.2, y1 - box_h / 2,
               x_lens[0] + lens_w / 2, y_lenses + lens_box_h / 2,
               color="#8FAEC4", linewidth=1.0, linestyle="--", zorder=0,
               connectionstyle="arc3,rad=0.15")

    # Phase 3 feeds into Phase 5 (dashed, curved underneath)
    draw_arrow(ax, x_lens[0] + lens_w / 2, y_lenses - 0.35,
               x_lens[2] - lens_w / 2, y_lenses - 0.35,
               color="#8FAEC4", linewidth=1.0, linestyle="--", zorder=0,
               connectionstyle="arc3,rad=-0.4")
    draw_data_label(ax, 5.0, 8.12, "Phase 3 \u2192 Phase 5 (ZIP equity data)")

    # ════════════════════════════════════════════════════════════════════════
    # Data flow labels below the lenses
    # ════════════════════════════════════════════════════════════════════════

    draw_data_label(ax, x_lens[0], 8.58, "Infrastructure density\nUnderserved ZIPs")
    draw_data_label(ax, x_lens[1], 8.58, "Workplace port needs\nEmployment rankings")
    draw_data_label(ax, x_lens[2], 8.58, "Equity scores\nJustice40 overlay")

    # ════════════════════════════════════════════════════════════════════════
    # LAYER 4: SCORING FRAMEWORK
    # ════════════════════════════════════════════════════════════════════════

    y_score = 7.1
    score_h = 1.55
    score_w = 7.6

    # Arrows from three lenses down to Scoring Framework
    draw_arrow(ax, x_lens[0], y_lenses - lens_box_h / 2,
               x_gap - 1.2, y_score + score_h / 2, linewidth=1.8, color="#4A6D8C")
    draw_arrow(ax, x_lens[1], y_lenses - lens_box_h / 2,
               x_gap, y_score + score_h / 2, linewidth=1.8, color="#4A6D8C")
    draw_arrow(ax, x_lens[2], y_lenses - lens_box_h / 2,
               x_gap + 1.2, y_score + score_h / 2, linewidth=1.8, color="#4A6D8C")

    draw_rounded_box(ax, 5.0, y_score, score_w, score_h, C_CONVERGE,
                     C_BORDER_CONVERGE, linewidth=2.5)
    draw_text(ax, 5.0, y_score + 0.45, "NEVI Scoring Framework", fontsize=13,
              color=C_TEXT_LIGHT, weight="bold")
    draw_text(ax, 5.0, y_score + 0.05,
              "Score = 0.40 \u00d7 Equity + 0.35 \u00d7 Utilization + 0.25 \u00d7 Cost-Eff.",
              fontsize=8.5, color="#D5E8C5", weight="semibold")
    draw_text(ax, 5.0, y_score - 0.30,
              "Dr. Al-Ghandour\u2019s prescriptive framework",
              fontsize=7.5, color="#B8D4A0", fontstyle="italic")

    # ════════════════════════════════════════════════════════════════════════
    # LAYER 5: OUTPUT — NEVI County Rankings
    # ════════════════════════════════════════════════════════════════════════

    y_out = 5.3
    out_h = 1.1
    out_w = 5.5

    # Arrow from Scoring to Output
    draw_arrow(ax, 5.0, y_score - score_h / 2, 5.0, y_out + out_h / 2,
               linewidth=2.5, color=C_OUTPUT)
    draw_data_label(ax, 6.5, 6.0, "County rankings")

    draw_rounded_box(ax, 5.0, y_out, out_w, out_h, C_OUTPUT, C_BORDER_OUTPUT,
                     linewidth=2.5)
    draw_text(ax, 5.0, y_out + 0.22, "NEVI County Rankings", fontsize=14,
              color=C_TEXT_LIGHT, weight="bold")
    draw_text(ax, 5.0, y_out - 0.18,
              "100 NC counties prioritized for infrastructure investment",
              fontsize=8, color="#FDE4CC")

    # ════════════════════════════════════════════════════════════════════════
    # OPTIONAL SIDEBAR — Phase 6 & 7
    # ════════════════════════════════════════════════════════════════════════

    sb_x = 1.8
    sb_y = 3.1
    sb_w = 3.0
    sb_h = 2.1

    # Subtle background
    draw_rounded_box(ax, sb_x, sb_y, sb_w, sb_h, "#F7F7F7", "#BBBBBB",
                     linewidth=1.0, alpha=0.8, linestyle="--")

    draw_text(ax, sb_x, sb_y + 0.72, "Optional Enhancements", fontsize=8.5,
              color="#888888", weight="bold")

    # Phase 6
    p6_y = sb_y + 0.2
    draw_rounded_box(ax, sb_x, p6_y, sb_w - 0.4, 0.55, C_OPTIONAL, C_BORDER_OPTIONAL,
                     linewidth=1.0, linestyle="--")
    draw_text(ax, sb_x, p6_y + 0.07, "Phase 6: Buffer Analysis", fontsize=8,
              color=C_TEXT_DARK, weight="semibold")
    draw_text(ax, sb_x, p6_y - 0.14, "Enhancement to Phase 3", fontsize=6.5,
              color="#777777")

    # Phase 7
    p7_y = sb_y - 0.5
    draw_rounded_box(ax, sb_x, p7_y, sb_w - 0.4, 0.55, C_OPTIONAL, C_BORDER_OPTIONAL,
                     linewidth=1.0, linestyle="--")
    draw_text(ax, sb_x, p7_y + 0.07, "Phase 7: NCDOT Corridor", fontsize=8,
              color=C_TEXT_DARK, weight="semibold")
    draw_text(ax, sb_x, p7_y - 0.14, "Optional benchmark", fontsize=6.5,
              color="#777777")

    draw_status_badge(ax, sb_x + sb_w / 2 - 0.55, p6_y + 0.37, "OPTIONAL")
    draw_status_badge(ax, sb_x + sb_w / 2 - 0.55, p7_y + 0.37, "OPTIONAL")

    # Dashed connector from Phase 3 area to sidebar
    ax.annotate("", xy=(sb_x + sb_w / 2, sb_y + sb_h / 2),
                xytext=(x_lens[0] - 0.2, y_lenses - lens_box_h / 2),
                arrowprops=dict(arrowstyle="->", color="#B0B0B0",
                                linewidth=1.0, linestyle="dashed",
                                connectionstyle="arc3,rad=0.35"),
                zorder=0)

    # ════════════════════════════════════════════════════════════════════════
    # LEGEND
    # ════════════════════════════════════════════════════════════════════════

    leg_x = 8.2
    leg_y = 3.1
    leg_w = 2.8
    leg_h = 2.75

    # Legend background
    draw_rounded_box(ax, leg_x, leg_y, leg_w, leg_h, "white", "#D0D0D0",
                     linewidth=1.0)

    draw_text(ax, leg_x, leg_y + leg_h / 2 - 0.25, "LEGEND", fontsize=9,
              color="#555555", weight="bold")

    legend_items = [
        (leg_y + 0.75, C_COMPLETE, C_BORDER_COMPLETE, "Complete"),
        (leg_y + 0.35, C_NEXT, C_BORDER_NEXT, "Next"),
        (leg_y - 0.05, C_PENDING, C_BORDER_PENDING, "Pending"),
        (leg_y - 0.45, C_CONVERGE, C_BORDER_CONVERGE, "Convergence"),
        (leg_y - 0.85, C_OUTPUT, C_BORDER_OUTPUT, "Output"),
    ]

    swatch_x = leg_x - leg_w / 2 + 0.2
    for item_y, fc, ec, label in legend_items:
        box = FancyBboxPatch(
            (swatch_x, item_y - 0.12), 0.5, 0.24,
            boxstyle="round,pad=0.02,rounding_size=0.02",
            facecolor=fc, edgecolor=ec, linewidth=1.0, zorder=3
        )
        ax.add_patch(box)
        draw_text(ax, swatch_x + 0.7, item_y, label, fontsize=7.5,
                  color="#555555", ha="left")

    # Optional legend item (dashed border)
    opt_item_y = leg_y - 1.25
    box = FancyBboxPatch(
        (swatch_x, opt_item_y - 0.12), 0.5, 0.24,
        boxstyle="round,pad=0.02,rounding_size=0.02",
        facecolor=C_OPTIONAL, edgecolor=C_BORDER_OPTIONAL,
        linewidth=1.0, linestyle="--", zorder=3
    )
    ax.add_patch(box)
    draw_text(ax, swatch_x + 0.7, opt_item_y, "Optional", fontsize=7.5,
              color="#555555", ha="left")

    # ════════════════════════════════════════════════════════════════════════
    # Footer
    # ════════════════════════════════════════════════════════════════════════

    ax.text(5.0, 0.3,
            "Wolfgang Sanyer  |  Broadwell College of Business & Economics  |  Spring 2026",
            fontsize=7.5, color="#AAAAAA", ha="center", va="center",
            fontfamily=FONT_FAMILY)

    # ════════════════════════════════════════════════════════════════════════
    # Save
    # ════════════════════════════════════════════════════════════════════════

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Full resolution (600 DPI)
    full_path = os.path.join(OUTPUT_DIR, "analytical-pipeline.png")
    fig.savefig(full_path, dpi=600, bbox_inches="tight", facecolor=C_BG,
                edgecolor="none", pad_inches=0.3)
    print(f"Saved: {full_path} (600 DPI)")

    # Thumbnail (150 DPI)
    thumb_path = os.path.join(OUTPUT_DIR, "analytical-pipeline-thumb.png")
    fig.savefig(thumb_path, dpi=150, bbox_inches="tight", facecolor=C_BG,
                edgecolor="none", pad_inches=0.3)
    print(f"Saved: {thumb_path} (150 DPI)")

    plt.close(fig)

    # Report file sizes
    for path in [full_path, thumb_path]:
        size_mb = os.path.getsize(path) / (1024 * 1024)
        print(f"  {os.path.basename(path)}: {size_mb:.2f} MB")


if __name__ == "__main__":
    create_pipeline_diagram()
    print("\nDone! Pipeline diagram generated successfully.")
