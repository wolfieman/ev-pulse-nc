# Figures

Project-level diagram assets used in top-level documentation.

## Contents

| File | DPI | Purpose |
|------|-----|---------|
| `analytical-pipeline.png` | 600 | Full-resolution pipeline architecture diagram. Embedded in root [`README.md`](../../README.md) |
| `analytical-pipeline-thumb.png` | 150 | Thumbnail for inline previews / lightweight contexts |

## Regenerating

Both PNGs are produced from a single matplotlib script. To regenerate after editing:

```bash
uv run code/python/docs/generate_pipeline_diagram.py
```

The generator lives at [`code/python/docs/generate_pipeline_diagram.py`](../../code/python/docs/generate_pipeline_diagram.py) and overwrites both files on each run.

## Scope

This directory holds **project-level architectural diagrams only** — pipeline overview, framework illustrations, and similar meta-figures.

Publication-quality figures produced by the analysis pipeline (fig-01 through fig-45, plus 4 supplementary variants, referenced in the paper) live in [`output/figures/`](../../output/figures/), not here.
