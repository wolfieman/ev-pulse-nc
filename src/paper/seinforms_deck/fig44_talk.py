"""Render a talk version of Fig 44 (forecast validation scatter) for the deck.

Reuses the paper's figure code unchanged (``create_fig44`` in
``src/analysis/phase1_fig44_validation_scatter.py``) on the same validation
results, then restyles the finished figure for projection: spelled-out model
names with county counts in the legend, larger text, a larger
Mecklenburg callout, and no statistics inset (the slide lists those numbers
beside the chart). Same data, same points; the paper's figure is not touched.

Run from the repo root:

    uv run python src/paper/seinforms_deck/fig44_talk.py

Output: src/paper/seinforms_deck/assets/fig-44-validation-scatter-talk.png

Copyright © 2026 Wolfgang Sanyer
Licensed under the Polyform Noncommercial License 1.0.0 (see LICENSE).
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.collections import PathCollection
from matplotlib.text import Annotation

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "src" / "analysis"))

import phase1_fig44_validation_scatter as fig44  # noqa: E402

from evpulse.style import setup_publication_style  # noqa: E402

OUT = Path(__file__).resolve().parent / "assets" / "fig-44-validation-scatter-talk.png"

# Size of the figure's slot on the slide (inches), so point sizes map 1:1.
SLOT_W, SLOT_H = 7.3, 5.3

LEGEND_NAMES = {
    "ESM": "Exponential smoothing (ESM)",
    "ARIMA": "ARIMA (autoregressive integrated\nmoving average)",
    "UCM": "Unobserved components (UCM)",
}

# County counts per model type as printed in the paper (§4.2, §6.1). Each
# county contributes four holdout months, so the figure's n must be 4x these.
PAPER_COUNTIES = {"ESM": 82, "ARIMA": 13, "UCM": 5}


def restyle(fig: plt.Figure) -> dict[str, str]:
    """Restyle the paper figure for the talk and return what was checked."""
    ax = fig.axes[0]
    fig.set_size_inches(SLOT_W, SLOT_H)

    # Drop the statistics inset; keep the Mecklenburg annotation.
    checked = {}
    for t in list(ax.texts):
        if isinstance(t, Annotation):
            checked["annotation"] = t.get_text().replace("\n", " ")
            t.set_fontsize(15)
            t.set_fontweight("bold")
            # Move the label left of the point, clear of the top edge.
            px, py = t.xy
            t.set_position((px * 0.07, py * 0.55))
            if t.arrow_patch is not None:
                t.arrow_patch.set_linewidth(1.6)
        elif t.get_text().startswith("MAPE:"):
            t.remove()

    # Larger highlight circle (the only unfilled scatter).
    for coll in ax.collections:
        if isinstance(coll, PathCollection) and len(coll.get_facecolors()) == 0:
            coll.set_sizes([420])
            coll.set_linewidth(2.8)

    # Spelled-out legend with the paper's county counts.
    handles, labels = ax.get_legend_handles_labels()
    new_labels = []
    for label in labels:
        model = label.split(" (n=")[0]
        if model in LEGEND_NAMES:
            n = label.split("n=")[1].rstrip(")")
            assert int(n) == 4 * PAPER_COUNTIES[model], (model, n)
            new_labels.append(
                f"{LEGEND_NAMES[model]}:\n{PAPER_COUNTIES[model]} counties"
            )
            checked[model] = n
        else:
            new_labels.append("Identity line (actual = predicted)")
    # The upper-left triangle is empty (every point sits near the diagonal).
    ax.legend(
        handles,
        new_labels,
        loc="upper left",
        frameon=True,
        fontsize=12.5,
        markerscale=2.0,
        handlelength=1.6,
        labelspacing=0.8,
    )

    # Projector-sized axes; the slide carries the title.
    for loc in ("left", "center", "right"):
        ax.set_title("", loc=loc)
    ax.xaxis.label.set_fontsize(15)
    ax.yaxis.label.set_fontsize(15)
    ax.tick_params(axis="both", which="major", labelsize=13)
    return checked


def main() -> None:
    setup_publication_style()
    df = fig44.load_validation_data()
    fig = fig44.create_fig44(df)
    checked = restyle(fig)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=300)
    plt.close(fig)
    print(f"points: {len(df)}; legend counts: {checked}")
    print(f"wrote {OUT.relative_to(REPO)}")


if __name__ == "__main__":
    main()
