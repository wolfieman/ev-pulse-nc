# EV Pulse NC

> **North Carolina's battery-electric vehicle fleet grew 1,727% from September 2018 to June 2025 — public charging infrastructure didn't keep pace.** This project quantifies the gap county-by-county, applies a Justice40 equity overlay, and produces a NEVI Priority Score to help direct North Carolina's $109M federal NEVI Formula Program funding.

![License: Polyform-NC](https://img.shields.io/badge/license-Polyform--NC--1.0-blue) ![Python 3.14+](https://img.shields.io/badge/python-3.14%2B-blue) ![Status: Research Complete](https://img.shields.io/badge/status-research--complete-brightgreen) ![Dependency Manager: uv](https://img.shields.io/badge/dependency-uv-purple)

![Underserved ZIP areas in North Carolina](output/figures/fig-25-underserved-choropleth.png)

*Statewide map of under-served ZIP areas. Darker shades = greater infrastructure gap relative to population. Phase 3 analysis identifies the 20 worst-served ZIPs for NEVI deployment targeting.*

---

## Headline Findings

- **Demand explosion** — BEV registrations grew **1,727%** (Sept 2018 → June 2025); 53.8% CAGR
- **Extreme concentration** — Statewide Gini coefficient of **0.805**; top 10 counties hold 72% of all BEVs
- **Within-county inequality dominates** — Theil-T decomposition: **84.5% of ZIP-level infrastructure inequality is within counties**, only 15.5% between
- **Infrastructure scope** — 1,985 stations / 6,145 connectors (AFDC, Feb 2026; all levels L1/L2/DCFC)
- **Justice40 overlay** — **43.0%** of NC census tracts disadvantaged per CEJST v2.0; 24.5% of stations sit in those tracts
- **Forecasting validation** — Python-replicated ARIMA matches SAS Model Studio at **MAPE = 4.36%**

## NEVI Priority Top 3

| Rank | County | NEVI Score | Archetype |
|---:|---|---:|---|
| 1 | Union | 0.561 | Utilization-driven (high BEV/port ratio) |
| 2 | Mecklenburg | 0.548 | Equity-driven (Justice40 + Gini) |
| 3 | Guilford | 0.465 | Balanced |

*Full 100-county rankings: `data/processed/scoring-framework-final.csv` after running the pipeline. See [`frameworks/analytical-pipeline.md`](frameworks/analytical-pipeline.md) for the scoring formula (`0.40·Equity + 0.35·Utilization + 0.25·Cost-Effectiveness`).*

---

## Featured Findings

### Theil decomposition — where the inequality lives

![Theil decomposition](output/figures/fig-33-theil-decomposition.png)

*84.5% of NC's ZIP-level infrastructure inequality is within counties, not between them. **Policy implication:** county-level fund allocation alone won't close the gap — ZIP-level deployment targeting is required.*

### Justice40 alignment

![Stations vs Justice40 tracts](output/figures/fig-42-stations-justice40-overlay.png)

*Charging stations overlaid on Justice40-disadvantaged census tracts. 24.5% of NC's mapped stations sit in disadvantaged tracts — close to proportional to the disadvantaged-tract share (43.0%) but with strong regional variation.*

---

## Methodology — 5-Phase Pipeline

![EV Pulse NC Analytical Pipeline Architecture](docs/figures/analytical-pipeline.png)

*Two foundation phases (Phase 1 demand validation + Phase 2 infrastructure inventory) converge at Gap Analysis. Three analytical lenses (Phase 3 ZIP-level, Phase 4 workplace, Phase 5 equity) then feed a prescriptive NEVI scoring framework that produces ranked county allocations.*

1. **Phase 1 — Validation:** Python ARIMA replication of SAS Model Studio county-level BEV forecasts (MAPE 4.36%; 100 counties; 8 publication figures)
2. **Phase 2 — Infrastructure inventory:** Full AFDC API pull (Feb 2026); 1,985 stations, 6,145 connectors, all charging levels
3. **Phase 3 — ZIP/County equity:** Gini coefficient (0.805 demand-side; 0.566 supply-side weighted) + Theil decomposition (84.5% within-county); 134 ZIPs ranked; 27 figures
4. **Phase 4 — Workplace charging:** LEHD LODES 2021 commuting flows + ACS income/tenure; 859,260 adjusted statewide workplace-charging demand; Mecklenburg/Wake/Durham top 3
5. **Phase 5 — Justice40 equity overlay:** CEJST v2.0 disadvantaged-community designation + climate-sensitivity check + weight-sensitivity grid
6. **Scoring framework:** Composite NEVI Priority Score per county = `0.40·Equity + 0.35·Utilization + 0.25·Cost-Effectiveness`; VIF-checked for multicollinearity

Full pipeline spec: [`frameworks/analytical-pipeline.md`](frameworks/analytical-pipeline.md). Per-dataset schema: [`data/DATA-DICTIONARY.md`](data/DATA-DICTIONARY.md). Model locations: [`output/models/README.md`](output/models/README.md).

---

## Quickstart — reproduce the top-3 NEVI ranking in under 5 minutes

```bash
# 1. Clone (requires Git LFS — see https://git-lfs.github.com/)
git clone https://github.com/wolfieman/ev-pulse-nc.git
cd ev-pulse-nc

# 2. Pull LFS-managed datasets (~190 MB)
git lfs pull

# 3. Set up the Python environment (uses uv — install via https://docs.astral.sh/uv/)
uv sync

# 4. Run the scoring framework — produces the top-3 ranking shown above
uv run code/python/analysis/scoring_framework_skeleton.py
uv run code/python/analysis/scoring_framework_final.py
```

You've reproduced the headline finding if the final script prints:

```
[CHECK 5] Intuition checks:
    Top 3: ['Union', 'Mecklenburg', 'Guilford']
    PASS — Guilford/Mecklenburg in top 3 as expected
```

Total elapsed time: under 5 minutes on a modern laptop.

---

## Full Reproducibility

To regenerate every output (all 42 figures, all CSVs, all phases) from raw inputs:

```bash
# Phase 1 — Validation
uv run code/python/analysis/validate_sas_forecasts.py
uv run code/python/analysis/generate_phase1_figures.py
uv run code/python/analysis/arima_bev_forecast.py

# Phase 3 — ZIP/County equity
uv run code/python/analysis/phase3_zip_mapping.py
uv run code/python/analysis/phase3_zip_density.py
uv run code/python/analysis/phase3_gini_inequality.py
uv run code/python/analysis/phase3_theil_decomposition.py
uv run code/python/analysis/phase3_top20_underserved.py
uv run code/python/analysis/phase3_county_heatmaps.py
uv run code/python/analysis/phase3_fig25_underserved_choropleth.py
uv run code/python/analysis/phase3_fig26_to_fig29.py
uv run code/python/analysis/phase3_fig30_to_fig32.py
uv run code/python/analysis/phase3_fig33_fig34.py

# Phase 4 — Workplace charging
uv run code/python/analysis/phase4_workplace_charging.py
uv run code/python/analysis/phase4_fig35_to_fig38.py

# Phase 5 — Justice40
uv run code/python/analysis/phase5_tract_zcta_crosswalk.py
uv run code/python/analysis/phase5_climate_sensitivity.py
uv run code/python/analysis/phase5_weight_sensitivity.py
uv run code/python/analysis/phase5_fig39_to_fig42.py

# Scoring framework (sequential — final reads skeleton's output, VIF reads final's output)
uv run code/python/analysis/scoring_framework_skeleton.py
uv run code/python/analysis/scoring_framework_final.py
uv run code/python/analysis/scoring_framework_vif.py
```

**Notes:**

- Raw data is fetched from `data/raw/` (LFS-tracked). To re-fetch from source APIs, see scripts in `code/python/data-acquisition/`.
- `data/processed/` outputs are gitignored — they regenerate from the scripts above. The `phase3_zip_mapping.py` step depends on the consolidated AFDC CSV being present in `data/raw/`.
- `output/figures/` is committed in the repo (PDF + PNG, 600 DPI). Re-running the figure scripts overwrites them in place.

---

## Tech Stack

- **Python 3.14+** — primary analytics platform
  - **pandas / numpy** — data manipulation
  - **statsmodels** — ARIMA / SARIMA / exponential smoothing forecasts; VIF; Ljung-Box
  - **geopandas / shapely** — spatial joins (NC State Plane EPSG:32119), choropleths
  - **matplotlib / seaborn** — publication-quality figures (600 DPI, PDF + PNG)
  - **requests / openpyxl** — API ingestion + Excel I/O
- **SAS Model Studio** — reference forecasts (auto-selected ESM × 82, ARIMA × 13, UCM × 5 across 100 counties)
- **Git LFS** — large data files (~190 MB total: CSVs, GeoJSONs, Excel)
- **uv** — Python dependency manager (replaces pip + venv + pip-tools)

### Analytical Framework (5-part)

Exploratory → Descriptive → Diagnostic → Predictive → Prescriptive. Applied across the 5 phases above.

---

## Repository Structure

```
ev-pulse-nc/
├── README.md                     # This file
├── CITATION.cff                  # Machine-readable citation metadata
├── INSTALLATION.md               # Setup guide
├── QUICK-REFERENCE.md            # Daily workflow commands
├── LICENSE                       # Polyform Noncommercial License 1.0.0
├── NOTICE.md                     # Copyright notice
├── .gitignore                    # Git ignore patterns
├── .gitattributes                # Git LFS tracking rules
│
├── data/                         # Dataset directory (Git LFS)
│   ├── raw/                      # Original datasets
│   ├── processed/                # Analysis-ready outputs (CSVs gitignored, regenerable)
│   ├── reference-forecasts/      # SAS Model Studio outputs (LFS)
│   ├── DATA-DICTIONARY.md         # Column definitions for all datasets
│   └── README.md                 # Directory overview & provenance
│
├── code/
│   └── python/                   # Python scripts
│       ├── data-acquisition/     # API ingestion scripts (AFDC, Census, LEHD, CEJST)
│       ├── analysis/             # Phase 1-5 + scoring scripts
│       ├── blog/                 # Blog graphics package
│       └── docs/                 # Documentation-asset generators (e.g. pipeline diagram)
│
├── docs/                         # Project documentation
│   ├── eda-reports/              # Exploratory data analysis reports
│   ├── figures/                  # Pipeline diagram + thumbnails
│   ├── internal/                 # Internal working artifacts (drift audits, AI logs)
│   └── research/                 # Supporting research papers + literature checks
│
├── frameworks/                   # Analytical frameworks and methodology specs
│   ├── analytical-pipeline.md    # Full 5-phase pipeline + scoring formula
│   ├── afdc-dataset-reference.md # AFDC source, vintage, counts
│   ├── afdc-data-structure.md    # AFDC field-level schema
│   └── ...                       # Per-dataset and per-method docs
│
├── output/                       # Generated outputs
│   ├── figures/                  # 42 publication-quality figures (PDF + PNG)
│   ├── validation/               # Forecast validation results
│   └── models/                   # Model index — pointers to where each model lives
│
├── paper/                        # Research paper directory
│   ├── README.md                 # Paper status + structure
│   └── PAPER-BRIEF.md            # 1-page public summary (manuscript in prep)
│
└── references/                   # Supporting materials
    └── data-sources.md           # Citations & links
```

### Key Documentation

| Document | Description |
|----------|-------------|
| [CITATION.cff](CITATION.cff) | Machine-readable citation metadata (powers GitHub's "Cite this repository" button) |
| [paper/PAPER-BRIEF.md](paper/PAPER-BRIEF.md) | 1-page public summary of the in-preparation manuscript |
| [frameworks/analytical-pipeline.md](frameworks/analytical-pipeline.md) | Full 5-phase pipeline and NEVI scoring formula |
| [data/DATA-DICTIONARY.md](data/DATA-DICTIONARY.md) | Column definitions for all 6 datasets (NCDOT, AFDC, SAS, LEHD, CEJST, ACS) |
| [paper/PROJECT-BRIEF.md](paper/PROJECT-BRIEF.md) | Executive project summary |
| [paper/PROJECT-EXPLANATION.md](paper/PROJECT-EXPLANATION.md) | Detailed project explanation with methodology deep-dive |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Contribution guidelines, branching model |
| [STYLE-GUIDE.md](STYLE-GUIDE.md) | Code style, naming conventions, formatting |
| [INSTALLATION.md](INSTALLATION.md) | Full setup guide (from clone or from scratch) |
| [output/models/README.md](output/models/README.md) | Model index — where every model in the project lives |
| [docs/internal/README.md](docs/internal/README.md) | Internal working artifacts (drift audits, content protocols) |
| [references/data-sources.md](references/data-sources.md) | Data source citations and reference links |

---

## Citation

This work is citable. Click **"Cite this repository"** in the right-hand sidebar of the GitHub page, or open [`CITATION.cff`](CITATION.cff) directly for the raw metadata.

If you reference the methodology specifically, please cite the in-preparation manuscript using [`paper/PAPER-BRIEF.md`](paper/PAPER-BRIEF.md) until publication.

---

## Acknowledgments

- **Author:** Wolfgang Sanyer — sole author of the analysis, code, and manuscript
- **Faculty Advisor:** Dr. Majed Al-Ghandour, Fayetteville State University
- **Data Providers:**
  - North Carolina Department of Transportation (NCDOT) — vehicle registrations
  - U.S. Department of Energy / NREL — Alternative Fuels Data Center (AFDC) charging-station inventory
  - U.S. Census Bureau — American Community Survey (ACS), TIGER boundaries, ZCTA crosswalks
  - U.S. Census Bureau / Center for Economic Studies — LEHD LODES workplace commuting data
  - Climate and Economic Justice Screening Tool (CEJST v2.0) — Justice40 disadvantaged-community designation; archived by Public Environmental Data Partners after the federal source went offline

---

## License

[Polyform Noncommercial License 1.0.0](LICENSE) — research, academic, and public-interest use permitted; commercial use restricted. See also [`NOTICE.md`](NOTICE.md).
