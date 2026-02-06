# Data Dictionary: nc-ev-registrations-2025

**File:** `nc-ev-registrations-2025.csv`
**Created:** 2026-02-01
**Script:** `code/python/data-acquisition/ncdot_ev_pipeline.py`

---

## Overview

| Property | Value |
|----------|-------|
| Description | Monthly EV registration counts by NC county (2025) |
| Source | NCDOT Climate Change Documents |
| Rows | 1,000 (100 counties × 10 months) |
| Grain | County-Month |
| Period | January - October 2025 |

---

## Variables

| Variable | Type | Description | Source | Example |
|----------|------|-------------|--------|---------|
| `County` | string | North Carolina county name | NCDOT | "Wake", "Mecklenburg" |
| `BEV` | integer | Battery Electric Vehicle registrations | NCDOT | 28098 |
| `PHEV` | integer | Plug-in Hybrid Electric Vehicle registrations | NCDOT | 8234 |
| `Hybrid` | integer | Traditional hybrid vehicle registrations | NCDOT | 15432 |
| `AllHybrids` | integer | PHEV + Hybrid combined | NCDOT | 23666 |
| `Gas` | integer | Gasoline vehicle registrations | NCDOT | 892341 |
| `Diesel` | integer | Diesel vehicle registrations | NCDOT | 45231 |
| `Date` | date | First day of month (YYYY-MM-DD) | Derived | 2025-07-01 |
| `TotalEV` | integer | BEV + PHEV | Derived | 36332 |
| `EV_Share` | float | TotalEV / (TotalEV + Gas + Diesel) | Derived | 0.0385 |
| `Methodology_PostMay2025` | boolean | Flag for NCDOT methodology change | Derived | True |

---

## Variable Details

### BEV (Battery Electric Vehicle)
- **Definition:** Count of fully electric vehicles registered in the county
- **Primary analysis variable** for this study
- **Range:** 0 - 28,098 (Oct 2025)
- **Note:** Cumulative registrations, not new registrations

### PHEV (Plug-in Hybrid Electric Vehicle)
- **Definition:** Count of plug-in hybrid vehicles
- **Included in TotalEV** but not primary focus
- **Range:** 0 - 8,500+

### TotalEV
- **Formula:** `BEV + PHEV`
- **Purpose:** Combined EV count for market analysis
- **Note:** Does not include traditional hybrids

### EV_Share
- **Formula:** `TotalEV / (TotalEV + Gas + Diesel)`
- **Purpose:** Market penetration rate
- **Range:** 0.0 - 1.0 (typically 0.01 - 0.05 in NC)
- **Note:** Denominator excludes hybrids

### Methodology_PostMay2025
- **Definition:** Boolean flag indicating NCDOT methodology change
- **True:** Data collected after May 2025 (new methodology)
- **False:** Data collected May 2025 or earlier
- **Impact:** May affect comparability across time periods

---

## Data Quality

### Missing Values
| Variable | Missing Rate |
|----------|--------------|
| All variables | 0.0% |

### Coverage
- **Counties:** 100 (all NC counties present)
- **Months:** 10 (January - October 2025)
- **Completeness:** 100%

### Validation
- See `nc-ev-registrations-2025.qa.txt` for detailed QA report
- Statewide BEV totals show expected monotonic growth
- No implausible values detected

---

## Usage Notes

1. **For validation analysis:** Use `BEV` column to compare against SAS forecasts
2. **County name matching:** Names are title-cased (e.g., "McDowell" not "Mcdowell")
3. **Date filtering:** Use `Date >= '2025-07-01'` for validation period (Jul-Oct)
4. **Methodology flag:** Consider `Methodology_PostMay2025` when analyzing trends

---

## Related Files

| File | Relationship |
|------|--------------|
| `sas-forecasts.csv` | Predictions to compare against |
| `sas-validation-comparison.csv` | Merged comparison output |
| `validate_sas_forecasts.py` | Script that uses this data |
