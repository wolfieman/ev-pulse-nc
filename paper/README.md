# Research Paper

> **EV Pulse NC: A Data-Driven Framework for North Carolina's NEVI Funding Allocation** — the BIDA 670 capstone research paper. Sole author: Wolfgang Sanyer. Faculty advisor: Dr. Majed Al-Ghandour. Spring 2026.

## Canonical Artifact

📄 **[ev-pulse-nc-sanyer.pdf](ev-pulse-nc-sanyer.pdf)** — 108 pages, 4.6 MB, all figures embedded, full APA 7 formatting

The PDF is the canonical public artifact. See the [repo-root README](../README.md) for the project at-a-glance, executive summary, and the 5 novel contributions enumerated.

## Build Pipeline

```
paper/manuscript.md  →  code/python/paper/build_docx.py  →  paper/manuscript.docx  →  (manual export)  →  paper/ev-pulse-nc-sanyer.pdf
```

Only the final PDF and this README are tracked in git. The markdown source (`manuscript.md`), intermediate `.docx`, the presentation `.pptx`, and the local `sources/` library are all gitignored — they're regenerable from the analytical pipeline and the build script.

To rebuild the .docx from source:

```bash
uv run python code/python/paper/build_docx.py
```

The script reads `paper/manuscript.md`, embeds figures from `output/figures/`, and writes `paper/manuscript.docx`. From there, Word's *File → Save As PDF* produces the canonical PDF.

## Standalone methodology artifacts

The two methodology reviews are integrated into the paper as Appendices A and B. The AI methodology disclosure is available as paper Appendix B; the data quality review is also available as standalone PDFs in [`docs/research/`](../docs/research/):

- `data-quality-review.pdf` — Data quality review, short version (paper App. A)
- `data-quality-review-full.pdf` — Data quality review, full version with all panel transcripts

## See also

- **[Repo-root README](../README.md)** — project at-a-glance, executive summary, 5 novel contributions, who-this-is-for, beyond NC
- **[CITATION.cff](../CITATION.cff)** — machine-readable citation metadata
- **[code/python/paper/build_docx.py](../code/python/paper/build_docx.py)** — manuscript .docx build script
