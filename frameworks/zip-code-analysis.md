# Phase 3: ZIP Code Analysis — Delivered Framework

## Executive Summary

Phase 3 delivered sub-county infrastructure magnification in North Carolina's urban counties, where county-level aggregation obscures critical spatial patterns. The analysis geocoded all 6,145 AFDC connectors to ZIP codes and calculated density, inequality, and underservice metrics across 134 ZIPs in the top 10 urban counties (roughly 80% of statewide BEV population).

**Critical finding:** A Theil decomposition attributes **84.5% of statewide spatial inequality to within-county variation** — meaning the bulk of the equity problem is hidden below the county level. Within Charlotte alone, the port density gap between ZIP 28202 and ZIP 28215 is roughly 250-fold. This is exactly the signal county-only analysis cannot see.

Phase 3 outputs feed both the Utilization Score and the Equity Score of the NEVI scoring framework.

## Results

| Output | File | Description |
|--------|------|-------------|
| County Gini | `data/processed/phase3-county-gini.csv` | Within-county infrastructure Gini coefficients |
| Statewide Gini | `data/processed/phase3-statewide-gini.csv` | Statewide connector Gini (0.805) |
| Theil decomposition | `data/processed/phase3-theil-decomposition.csv` | Within vs. between county inequality (84.5% within) |
| ZIP density | `data/processed/phase3-zip-density.csv` | Ports per sq mi, per capita, per BEV by ZIP |
| Top-20 underserved | `data/processed/phase3-top20-underserved.csv` | Site-selection priority ZIPs |
| Top 10 counties | `data/processed/phase3-top10-counties.csv` | Urban counties analyzed in Phase 3 |
| Station-county mapping | `data/processed/phase3-station-county-mapping.csv` | Geocoded station-to-county join |

Phase 3 produced 34 publication figures (fig-08 through fig-34) and populated the first 9 of 17 columns of the scoring framework skeleton. See `frameworks/analytical-pipeline.md` for how Phase 3 feeds the scoring framework.

---

## Methodology Notes

- **Scope:** Phase 3 analyzed 134 ZIP codes within North Carolina's top 10 urban counties, capturing roughly 80% of statewide BEV population. The full-state ZIP scope (~800 ZIPs) was excluded because data sparsity below the top urban counties yields unreliable inequality measurements.
- **Approach:** The analysis was descriptive only — no ZIP-level forecasting was attempted, since NCDOT does not publish ZIP-level BEV registration data and per-ZIP time-series modeling would have introduced sparsity-driven noise without analytical benefit.
- **Spatial join:** ZIP↔tract overlays use area-weighted interpolation in EPSG:32119 (NC State Plane, meters) rather than degree-space, avoiding distortion.
- **ZCTA caveat:** Sub-county geometries are reported as ZCTAs (Census areal approximations of USPS ZIP codes); a small share of addresses may fall outside their nominal ZCTA polygon.
