# AFDC Data Comparison: Old Extract vs. New API Download

> **Date:** February 26, 2026
> **Author:** Wolfgang Sanyer
> **Project:** EV Pulse NC — North Carolina Electric Vehicle Analytics

---

## Executive Summary

A detailed comparison of the two AFDC data files in this project reveals that the original file (`afdc-charging-stations-connector-2024-07.csv`) was **not a full snapshot** of North Carolina EV charging infrastructure. It was a DCFC-only, public-access-only, connector-level extract containing only 355 unique stations. The new API download (`afdc-charging-stations-connector-2026-02.csv`) is a **complete station-level dataset** with 1,985 stations across all charging levels and access types.

This finding fundamentally redefines Priority 5 of the project. The task is no longer "update stale data to fix a temporal gap" but rather "replace an incomplete DCFC-only extract with a complete all-levels API dataset."

---

## File Specifications

### Old File: `afdc-charging-stations-connector-2024-07.csv`

| Attribute | Value |
|-----------|-------|
| **Filename** | `afdc-charging-stations-connector-2024-07.csv` |
| **Rows** | 1,725 |
| **Unique Stations** | 355 |
| **Granularity** | Connector-level (one row per connector port) |
| **Charging Levels** | DCFC only (with minor L2 co-located at DCFC stations) |
| **Access Types** | Public only |
| **Columns** | 74 |
| **Max `Updated At` Date** | 2025-12-22 |
| **Actual Data Currency** | Through December 2025 (not July 2024 as filename implies) |

**Key Observations:**
- The "2024-07" in the filename is misleading. The data contains records updated as recently as December 22, 2025, indicating the file was likely downloaded from the AFDC website in late December 2025 or January 2026.
- The connector-level granularity means each physical port at a station generates a separate row. A single station with 8 DCFC connectors produces 8 rows.
- The 65 L2 ports in this file are co-located at DCFC stations, not standalone L2 stations.
- This file was likely generated via a filtered AFDC website export (DCFC + public + NC), not a full API download.

### New File: `afdc-charging-stations-connector-2026-02.csv`

| Attribute | Value |
|-----------|-------|
| **Filename** | `afdc-charging-stations-connector-2026-02.csv` |
| **Rows** | 1,985 |
| **Unique Stations** | 1,985 |
| **Granularity** | Station-level (one row per station) |
| **Charging Levels** | All (Level 1, Level 2, DCFC) |
| **Access Types** | All (public and private) |
| **Columns** | 76 |
| **Download Method** | NREL AFDC API (`alt-fuel-stations/v1.json`) |
| **Download Date** | February 2026 |

**Key Observations:**
- Downloaded programmatically via the AFDC API using `code/python/data-acquisition/afdc_api_download.py`.
- Station-level granularity: one row per station, with port counts stored in aggregate columns (`ev_level1_evse_num`, `ev_level2_evse_num`, `ev_dc_fast_num`).
- Includes all access types: public, private, and restricted stations.
- Two additional columns compared to the old file (76 vs. 74).

---

## High-Level Comparison

| Metric | Old File (355 stns) | New All (1,985) | New Public (1,876) | New Pub DCFC (336) |
|--------|--------------------:|----------------:|-------------------:|-------------------:|
| **Stations** | 355 | 1,985 | 1,876 | 336 |
| **Unique Cities** | 135 | 267 | 257 | 129 |
| **Unique ZIPs** | 179 | 358 | 347 | 171 |
| **Total DCFC Ports** | 1,742 | 1,747 | 1,745 | 1,745 |
| **Total L2 Ports** | 65 | 4,363 | 3,899 | 54 |
| **Total L1 Ports** | 0 | 35 | 9 | 0 |

**Interpretation:**
- The old file captured nearly all DCFC ports (1,742 vs. 1,745 in the apples-to-apples public DCFC comparison), confirming it was a thorough DCFC extract.
- The old file missed 4,298 L2 ports (4,363 total minus 65 co-located) and all 35 L1 ports.
- The new file doubles the geographic coverage: 267 cities vs. 135, and 358 ZIP codes vs. 179.

---

## Station ID Overlap Analysis

To assess continuity between the old and new datasets, station IDs from both files were matched. The comparison uses the new file filtered to public DCFC stations only (336 stations) against the old file's 355 unique stations.

| Category | Count | % of Old File |
|----------|------:|:-------------:|
| **Overlap** (present in both files) | 322 | 90.7% |
| **Lost** (old file only, absent from new) | 33 | 9.3% |
| **Gained** (new DCFC-public only, absent from old) | 14 | -- |

**Interpretation:**
- 90.7% of old-file stations appear in the new file, indicating strong continuity.
- The 33 "lost" stations likely reflect closures, decommissions, status changes (e.g., moved to non-operational), or data corrections between the two extracts.
- The 14 "gained" stations represent genuinely new DCFC installations not present in the old extract.
- Net DCFC change: 336 - 355 = -19 stations, but port counts are nearly identical (1,745 vs. 1,742), suggesting station consolidation with higher port density.

---

## Composition of the New File

The new file's 1,985 stations break down by charging level and access type as follows:

| Category | Stations | % of Total |
|----------|:--------:|:----------:|
| **L2-only stations** (entirely absent from old file) | 1,636 | 82.4% |
| **DCFC stations (public)** | 336 | 16.9% |
| **L1-only stations** | 9 | 0.5% |
| **DCFC stations (private)** | 2 | 0.1% |
| **Mixed L2 + L1** | 2 | 0.1% |

**Key Finding:** 82.4% of the new file's stations were entirely absent from the old file -- not because they are new installations, but because the old file never included L2 stations. The overwhelming majority of North Carolina's charging infrastructure is Level 2, and the old extract excluded it entirely.

---

## Methodology

### Data Loading
Both CSV files were loaded from `data/raw/` and examined for structure, row counts, column counts, and unique station identifiers.

### Old File Deduplication
Because the old file uses connector-level granularity (multiple rows per station), station-level metrics were derived by grouping on station ID and aggregating port counts.

### Apples-to-Apples Filtering
To enable fair comparison, the new file was filtered to match the old file's scope:
- **Access type:** Public only (`access_code == "public"`)
- **Charging level:** DCFC only (stations where `ev_dc_fast_num > 0`)

### Station ID Matching
Station IDs were compared between datasets using set operations (intersection, difference) to calculate overlap, lost, and gained station counts.

### Port Count Aggregation
Port counts were summed by charging level (L1, L2, DCFC) for each dataset and each filtered subset.

---

## Implications for Priority 5

### Original Premise (Now Incorrect)

Priority 5 was originally framed as:
> "Update stale July 2024 infrastructure data to close a 6-month temporal gap with October 2025 BEV registration data."

This premise rested on two assumptions, both of which proved incorrect:

1. **Assumption:** The old file was a complete snapshot of NC charging infrastructure as of July 2024.
   **Reality:** It was a DCFC-only, public-only extract. The date in the filename does not reflect the data's actual currency.

2. **Assumption:** There was a 6-month staleness gap (July 2024 to January 2026).
   **Reality:** The old file's data extends through December 2025 (`Updated At` max: 2025-12-22). The actual temporal gap is minimal for the DCFC stations it covers.

### Redefined Scope

**Priority 5 is now:** Replace an incomplete DCFC-only connector-level extract with a complete all-levels station-level API dataset.

The value of the new file is **completeness, not temporal currency:**
- 1,636 L2-only stations (82.4% of the new file) were entirely missing from the old file.
- Geographic coverage doubles (267 cities vs. 135; 358 ZIPs vs. 179).
- All access types included (public + private).
- Station-level granularity simplifies downstream analysis (no deduplication needed).

### Impact on Project Analyses

| Analysis | Impact of Dataset Replacement |
|----------|-------------------------------|
| **Gap analysis** | Now includes L2 infrastructure; gap calculations shift from DCFC-only to all-levels |
| **ZIP-level analysis** | Coverage doubles from 179 to 358 ZIP codes |
| **Workplace charging** | L2 stations are the primary workplace charging type; old file excluded them |
| **Equity analysis** | L2 stations serve different demographics than DCFC; inclusion changes equity picture |
| **Buffer/coverage analysis** | Coverage zones expand substantially with 1,636 additional L2 stations |
| **ARIMA forecasting** | Infrastructure supply baseline changes from 355 to 1,985 stations |

---

## Conclusion

The AFDC data comparison reveals that the project's original infrastructure dataset was far more limited than previously understood. The old file captured DCFC infrastructure thoroughly (90.7% station overlap, near-identical port counts) but excluded the vast majority of NC's charging network. The new API download provides the complete picture needed for a rigorous capstone analysis.

**Action items:**
1. Use `afdc-charging-stations-connector-2026-02.csv` as the primary infrastructure dataset for all analyses going forward.
2. Retain `afdc-charging-stations-connector-2024-07.csv` in `data/raw/` for reference and reproducibility.
3. Update all downstream analyses to account for the expanded station universe (1,985 vs. 355).
4. Revise the Priority 5 framework documentation to reflect the redefined scope.

---

*This document was generated as part of the Phase 2 AFDC update for EV Pulse NC.*
