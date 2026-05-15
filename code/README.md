# Code Directory

All analysis code is Python. **Run everything via `uv run`** — never invoke `.venv/Scripts/python.exe` or system `python` directly. See [`../INSTALLATION.md`](../INSTALLATION.md) for environment setup and the **Full Reproducibility** section of [`../README.md`](../README.md) for the canonical end-to-end pipeline order.

---

## Layout

```
code/python/
├── data-acquisition/   # API downloads (NCDOT, AFDC, Census, CEJST, LEHD)
├── analysis/           # Phase 1-5 analytics + scoring framework + ARIMA + EDA
└── blog/               # Importable package for blog graphics
```

---

## `data-acquisition/` — 8 scripts

API ingestion. Each script writes to `data/raw/`. Two require credentials in `.env`:

- `NREL_API_KEY` — for `afdc_api_download.py`
- `CENSUS_API_KEY` — for `census_zip_population.py`

| Script | Source | Output |
|---|---|---|
| `ncdot_ev_pipeline.py` | NCDOT registration spreadsheets | County-month panel CSV |
| `afdc_api_download.py` | NREL Alternative Fuels Data Center API | Charging-station inventory CSV |
| `census_county_boundaries.py` | Census TIGER | NC county boundary GeoJSON |
| `census_tract_boundaries.py` | Census TIGER | NC + 4 border states (GA, SC, TN, VA) tract boundaries — Phase 5 crosswalk |
| `census_zcta_boundaries.py` | Census TIGER | NC ZCTA boundary GeoJSON |
| `census_zip_population.py` | Census ACS 5-Year API | NC ZCTA population CSV |
| `lehd_lodes_download.py` | Census LEHD LODES + ACS | NC commuter flow CSVs (gzipped) + ACS income/tenure tract CSV |
| `cejst_justice40_download.py` | Public Environmental Data Partners archive | NC Justice40 tract CSVs |

**Run pattern:**

```bash
uv run code/python/data-acquisition/afdc_api_download.py
```

---

## `analysis/` — 28 scripts

Phase-prefixed naming gives consistent grouping. See [`../frameworks/analytical-pipeline.md`](../frameworks/analytical-pipeline.md) for the methodology and the root [`../README.md`](../README.md) "Full Reproducibility" section for the canonical run order.

| Group | Pattern | Role |
|---|---|---|
| **Phase 1 — Validation** | `validate_sas_forecasts.py`, `arima_bev_forecast.py`, `arima_template.py`, `generate_phase1_figures.py` | Cross-validate SAS forecasts in Python (MAPE 4.36%) |
| **Phase 3 — ZIP/County equity** | `phase3_zip_mapping.py`, `phase3_zip_density.py`, `phase3_gini_inequality.py`, `phase3_theil_decomposition.py`, `phase3_top20_underserved.py`, `phase3_county_heatmaps.py`, `phase3_fig25_underserved_choropleth.py`, `phase3_fig26_to_fig29.py`, `phase3_fig30_to_fig32.py`, `phase3_fig33_fig34.py` | Gini, Theil decomposition, choropleth, county heatmaps |
| **Phase 4 — Workplace charging** | `phase4_workplace_charging.py`, `phase4_fig35_to_fig38.py` | LEHD LODES + ACS workplace-demand model |
| **Phase 5 — Justice40** | `phase5_tract_zcta_crosswalk.py`, `phase5_climate_sensitivity.py`, `phase5_weight_sensitivity.py`, `phase5_fig39_to_fig42.py` | CEJST overlay + climate / weight sensitivity |
| **Scoring framework (sequential)** | `scoring_framework_skeleton.py` → `scoring_framework_final.py` → `scoring_framework_vif.py` | Build skeleton, fill Phase 5 columns, VIF check |
| **EDA** | `eda_cejst_justice40.py`, `eda_census_zip_population.py`, `eda_phase4_lehd_acs.py`, `generate_phase3_afdc_eda.py` | Exploratory profiling per dataset |
| **Shared utility** | `publication_style.py` | matplotlib defaults (600 DPI, color palette) imported by figure scripts |

**Run pattern:**

```bash
uv run code/python/analysis/scoring_framework_final.py
```

---

## `blog/` — Importable package

Used to generate blog graphics (LinkedIn, Substack). Not part of the analytics pipeline.

| File | Purpose |
|---|---|
| `__init__.py` | Package init |
| `blog_graphics.py` | Stat cards, multi-panel infographics, social-preview images |

---

## Convention reminders

| Rule | Where it's enforced |
|---|---|
| Run via `uv run` — never `python script.py` or `.venv/Scripts/python.exe` | Project memory; this README |
| `snake_case` filenames; `PascalCase` classes; `UPPER_SNAKE` module constants | [`../STYLE-GUIDE.md`](../STYLE-GUIDE.md) |
| Module docstring at top of every script | [`../STYLE-GUIDE.md`](../STYLE-GUIDE.md) |
| Outputs to `data/processed/` or `output/` — never `data/raw/` or alongside the script | This README |
| No hardcoded credentials — `.env` only; load via `python-dotenv` | [`../.gitignore`](../.gitignore) (`.env` is ignored) |
| Line length 88; `target-version = "py314"` | [`../pyproject.toml`](../pyproject.toml) (ruff-enforced) |
