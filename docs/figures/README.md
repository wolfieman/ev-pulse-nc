# Figures

Project-level diagram assets used in top-level documentation and the paper brief.

## Contents

| File | DPI | Purpose |
|------|-----|---------|
| `analytical-pipeline.png` | 600 | Full-resolution pipeline architecture diagram. Embedded in root [`README.md`](../../README.md) and [`paper/PAPER-BRIEF.md`](../../paper/PAPER-BRIEF.md) |
| `analytical-pipeline-thumb.png` | 150 | Thumbnail for inline previews / lightweight contexts |

## Regenerating

Both PNGs are produced from a single matplotlib script. To regenerate after editing:

```bash
uv run scripts/generate_pipeline_diagram.py
```

The generator lives at [`scripts/generate_pipeline_diagram.py`](../../scripts/generate_pipeline_diagram.py) and overwrites both files on each run.

## Scope

This directory holds **project-level architectural diagrams only** — pipeline overview, framework illustrations, and similar meta-figures.

Publication-quality figures produced by the analysis pipeline (fig-01 through fig-42, referenced in the paper) live in [`output/figures/`](../../output/figures/), not here.
