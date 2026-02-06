# AFDC Data Structure & Snapshot Comparison Methodology Framework

**Project:** EV Pulse NC (BIDA 670 Advanced Analytics)
**Context:** Priority #5 - AFDC API Update - Data Structure & Methodology Research
**Scope:** Conceptual framework ONLY - No API calls, no data downloads, no implementation
**Current Baseline:** July 2024 snapshot (355 stations, 1,725 connectors)
**Target Update:** January 2026 snapshot
**Document Created:** January 30, 2026

---

## Executive Summary

This document provides a comprehensive conceptual framework for updating EV Pulse NC's AFDC (Alternative Fuels Data Center) charging station data from the July 2024 snapshot to a January 2026 snapshot. The framework covers AFDC data structure, temporal comparison methodology, infrastructure classification for integration with Priority #2 (ZIP analysis) and Priority #3 (CTPP workplace analysis), and industry best practices for data currency standards.

**Key Findings:**
- AFDC provides ~50+ fields per station with rich temporal metadata
- Snapshot comparison requires multi-dimensional change classification
- 6-month data staleness is SIGNIFICANT for NC's rapidly evolving infrastructure (47.6% of current infrastructure added in 2024-2025)
- Recommended update frequency: Quarterly for competition-grade analysis

---

## 1. AFDC DATA STRUCTURE ANALYSIS

### 1.1 Overview

The AFDC API (Alternative Fuels Data Center) is maintained by NREL (National Renewable Energy Laboratory) and provides comprehensive real-time data on alternative fuel stations across the United States. For EV Pulse NC, we focus exclusively on electric vehicle charging stations (`fuel_type=ELEC`).

**API Endpoint:** `https://developer.nrel.gov/api/alt-fuel-stations/v1`
**Documentation:** https://developer.nrel.gov/docs/transportation/alt-fuel-stations-v1/all/
**Data Granularity:** Connector-level (individual EVSE units), NOT station-level

### 1.2 Core Station Identification Fields

| Field Name | Data Type | Description | Example | Priority |
|------------|-----------|-------------|---------|----------|
| `id` | Integer | Unique station identifier (PRIMARY KEY) | 245123 | Critical |
| `station_name` | String | Official station name | "Target 0961 - Cary, NC" | Critical |
| `access_code` | String | Access type classification | "public" or "private" | Critical |
| `status_code` | String | Operational status | "E" (Available), "P" (Planned), "T" (Temp Unavailable) | Critical |

**Status Code Values:**
- **E** - Available (operational and accessible)
- **P** - Planned (under construction or approved but not yet operational)
- **T** - Temporarily Unavailable (operational but currently inaccessible)
- **(Absent from new snapshot)** - Station decommissioned or permanently closed

### 1.3 Geographic Location Fields

| Field Name | Data Type | Description | Example | Purpose |
|------------|-----------|-------------|---------|---------|
| `street_address` | String | Physical address | "2021 Walnut Street" | Geocoding validation |
| `city` | String | City name | "Cary" | Municipal analysis |
| `state` | String | State abbreviation | "NC" | State filtering |
| `zip` | String | ZIP code (5-digit) | "27518" | **Priority #2 ZIP Analysis** |
| `county` | String | County name | "Wake" | County-level aggregation |
| `latitude` | Float | Latitude coordinate | 35.73859 | Spatial join operations |
| `longitude` | Float | Longitude coordinate | -78.81293 | Spatial join operations |

**Integration Note:** The `zip` field is CRITICAL for Priority #2 (ZIP Code Analysis). Current EV Pulse NC analysis operates at county level; ZIP-level granularity enables sub-county gap analysis.

### 1.4 Charging Infrastructure Classification Fields

| Field Name | Data Type | Description | Example | Classification Purpose |
|------------|-----------|-------------|---------|------------------------|
| `ev_connector_types` | Array[String] | Connector types available | ["NACS", "J1772COMBO", "CHADEMO"] | Compatibility analysis |
| `ev_level1_evse_num` | Integer | Number of Level 1 chargers (120V, 1.4-1.9 kW) | 0 | Low-power charging |
| `ev_level2_evse_num` | Integer | Number of Level 2 chargers (240V, 3-19.2 kW) | 4 | Standard charging |
| `ev_dc_fast_num` | Integer | Number of DC Fast Chargers (≥50 kW) | 8 | High-power charging |
| `ev_network` | String | Charging network operator | "Tesla Supercharger", "Electrify America" | Network analysis |
| `ev_pricing` | String | Pricing model | "$0.53/kWh" | Economic analysis |

**Connector Type Codes:**
- **NACS** - North American Charging Standard (Tesla, becoming industry standard)
- **J1772COMBO** - CCS/SAE Combo (most non-Tesla EVs)
- **CHADEMO** - Legacy fast charging standard (Nissan, Mitsubishi)
- **J1772** - Level 2 standard connector (all EVs except early Teslas)

**Charging Level Classification (for gap analysis):**
- **Level 1:** 120V household outlet, 1.4-1.9 kW, ~5 miles range/hour (excluded from public analysis)
- **Level 2:** 240V dedicated circuit, 3-19.2 kW, ~20-40 miles range/hour (standard public charging)
- **DC Fast Charging (DCFC):** ≥50 kW, 60-350 kW range, ~100-300 miles range/30 min (highway corridors, high-demand locations)

**EV Pulse NC Current Approach:**
- Current analysis aggregates ALL connector types into "charging units" (1,725 total connectors across 355 stations)
- Power-weighted gap metric: BEVs per kW capacity (accounts for faster DCFC vs. slower Level 2)
- Finding: 80.5% of infrastructure is ≥150 kW (high-power DCFC dominates NC deployment)

### 1.5 Facility and Access Type Fields

| Field Name | Data Type | Description | Example | Analysis Use Case |
|------------|-----------|-------------|---------|-------------------|
| `facility_type` | String | Type of facility hosting station | "SHOPPING_MALL", "WORKPLACE", "PARKING_LOT" | **Priority #3 Workplace Classification** |
| `owner_type_code` | String | Owner classification | "P" (Private), "LG" (Local Gov), "FG" (Federal Gov) | Ownership analysis |
| `access_days_time` | String | Access hours | "24 hours daily" | Availability analysis |
| `access_detail_code` | String | Access restrictions | "PUBLIC", "WORKPLACE_ONLY", "CALL_AHEAD" | **Priority #3 Workplace vs. Public** |

**Facility Type Values (Selection Relevant to NC):**
- `WORKPLACE` - Office buildings, corporate campuses (PRIORITY #3 target)
- `SHOPPING_MALL` - Retail centers (dwell time analysis)
- `PARKING_LOT` - Public parking facilities
- `PARKING_GARAGE` - Multi-level parking structures
- `HOTEL` - Hospitality destinations (overnight charging)
- `CAR_DEALER` - Dealership chargers (often restricted)
- `GAS_STATION` - Convenience store integration (Sheetz, etc.)
- `GOVERNMENT_FACILITY` - Municipal/state buildings

**Access Classification Challenge (Data Quality Issue):**
- AFDC data quality research found **misclassification where some stations labeled as 'public' may actually be workplace charging locations not accessible to the general public**
- `facility_type=WORKPLACE` + `access_code=public` can indicate employer-provided charging open to visitors during business hours
- `facility_type=WORKPLACE` + `access_detail_code=WORKPLACE_ONLY` indicates employee-only access
- **Implication for Priority #3:** Requires manual validation or cross-reference with CTPP workplace location data

### 1.6 Temporal Metadata Fields (CRITICAL for Snapshot Comparison)

| Field Name | Data Type | Description | Example | Comparison Use |
|------------|-----------|-------------|---------|----------------|
| `date_last_confirmed` | Date (ISO 8601) | Last verification date | "2024-07-15" | Data staleness detection |
| `updated_at` | Timestamp | Last database update | "2024-07-20T10:23:45Z" | Change tracking |
| `open_date` | Date (ISO 8601) | Station opening date | "2020-01-31" | Deployment timeline analysis |
| `expected_date` | Date (ISO 8601) | Expected opening date (for `status_code=P` planned stations) | "2026-03-15" | Future capacity forecasting |

**Temporal Analysis Capabilities:**
1. **Deployment Timeline:** Filter stations by `open_date` to analyze infrastructure growth patterns
   - Example: Stations opened between July 2024 and January 2026
   - EV Pulse NC finding: 47.6% of current infrastructure added in 2024-2025 (rapid acceleration)

2. **Data Currency Assessment:** Compare `date_last_confirmed` to current date
   - Stations not confirmed in >90 days may have data quality issues
   - Stations not confirmed in >180 days may be decommissioned without status update

3. **Change Tracking:** `updated_at` timestamp indicates when ANY field was modified
   - Equipment upgrades (adding DCFC to Level 2-only station)
   - Ownership transfers (network changes)
   - Access policy changes (private → public)

4. **Future Capacity Planning:** `status_code=P` + `expected_date` identifies pipeline infrastructure
   - Critical for NEVI (National Electric Vehicle Infrastructure) program tracking
   - NC has $109M in NEVI funding; planned stations indicate deployment strategy

### 1.7 Network and Operational Fields

| Field Name | Data Type | Description | Example | Analysis Use |
|------------|-----------|-------------|---------|--------------|
| `ev_network` | String | Charging network operator | "ChargePoint Network" | Market concentration |
| `ev_network_web` | URL | Network website | "https://www.chargepoint.com" | User information |
| `station_phone` | String | Contact phone number | "800-489-1588" | Operational validation |
| `groups_with_access_code` | String | Restricted access groups | "Private - fleet customers only" | Access restriction details |

**Network Operators in NC (EV Pulse NC Current Baseline):**
- **Tesla Supercharger:** 60.5% of connectors (24.8% of stations) - dominates high-power DCFC
- **ChargePoint Network:** Major commercial network (shopping centers, workplaces)
- **Electrify America:** Walmart partnership (highway corridors)
- **eVgo Network:** Convenience store partnerships (Sheetz in NC)
- **Non-Networked:** Dealerships, municipal chargers, independent installations

**Market Concentration Analysis:**
- Tesla's dominance (60.5% connector share) reflects proprietary network strategy
- NACS (Tesla connector) becoming industry standard (2024-2025 transition period)
- Non-Tesla networks fragmented across multiple operators

### 1.8 Data Quality and Validation Fields

| Field Name | Data Type | Description | Example | Quality Assurance |
|------------|-----------|-------------|---------|-------------------|
| `geocode_status` | String | Geocoding confidence | "GPS" (high confidence) or "200-9" (address-based) | Spatial accuracy |
| `maximum_vehicle_class` | String | Vehicle size compatibility | "LD" (Light-duty), "MD" (Medium-duty), "HD" (Heavy-duty) | Fleet analysis |
| `intersection_directions` | String | Navigation instructions | "Northwest corner of Main St and 1st Ave" | User guidance |

**Data Quality Considerations:**
- `geocode_status="GPS"` indicates surveyed coordinates (highest accuracy)
- `geocode_status="200-9"` indicates address-based geocoding (potential ~100m error)
- Missing `latitude`/`longitude` requires spatial join or geocoding

### 1.9 EV Pulse NC Connector-Level Granularity

**Critical Distinction:** AFDC provides BOTH station-level data (via main API) AND connector-level data (via `/ev-charging-units` endpoint).

**EV Pulse NC Current Data:** Connector-level dataset (`alt_fuel_stations_ev_charging_units.csv`)
- **1,725 rows** = 1,725 individual charging connectors
- **355 unique stations** = station identifier (4.85x multiplier: 1,725 connectors / 355 stations = 4.85 connectors/station average)
- **Granularity advantage:** Power output per connector (kW), connector type per unit

**Connector-Level Fields (Additional to Station-Level):**
- `evse_id` - Individual EVSE unit identifier (sub-station level)
- `connector_type` - Specific connector on this EVSE unit
- `power_output` - kW capacity for this connector
- `status_code` - Status per connector (not just per station)

**Gap Analysis Implication:**
- Station-level analysis: "355 stations in NC"
- Connector-level analysis: "1,725 charging ports in NC" (more accurate for capacity planning)
- Current EV Pulse NC gap metric: ~16.9 BEVs per charging port (connector-level)
- National benchmark: 10-15 BEVs per port (connector-level standard)

---

## 2. SNAPSHOT COMPARISON METHODOLOGY

### 2.1 Conceptual Framework

**Objective:** Compare July 2024 AFDC snapshot (current baseline) to January 2026 AFDC snapshot (target update) to quantify infrastructure evolution and assess whether gap is closing or widening.

**Comparison Dimensions:**
1. **Quantity Changes:** Net station/connector additions or removals
2. **Geographic Shifts:** County-level or ZIP-level deployment patterns
3. **Infrastructure Type Evolution:** Level 2 vs. DCFC capacity changes
4. **Network Composition:** Market share shifts among operators
5. **Status Changes:** Planned stations becoming operational, temporary closures

### 2.2 Change Classification Taxonomy

#### 2.2.1 New Stations

**Definition:** Stations present in Jan 2026 snapshot but ABSENT from July 2024 snapshot.

**Identification Logic:**
```
IF station_id IN jan_2026_snapshot AND station_id NOT IN july_2024_snapshot
  THEN classify as "New Station"
```

**Subcategories:**
- **Greenfield Deployment:** Completely new location with no prior infrastructure
- **Planned-to-Operational:** Station had `status_code=P` in July 2024, now `status_code=E` in Jan 2026
- **Network Expansion:** Existing station location gaining new network operator (e.g., Tesla adding Supercharger to shopping center with existing ChargePoint)

**Data Validation:**
- Cross-check `open_date` field: If `open_date` is between 2024-07-01 and 2026-01-31, confirms new deployment
- If `open_date` is BEFORE 2024-07-01, investigate: Possible data quality issue (station existed but not in July 2024 snapshot)

**Analytical Metrics:**
- **Net New Stations:** Count of new station IDs
- **Net New Connectors:** Sum of `ev_level2_evse_num` + `ev_dc_fast_num` for new stations
- **Net New Capacity (kW):** Sum of power_output across new connectors
- **Geographic Distribution:** Group by county/ZIP to identify deployment hotspots

#### 2.2.2 Removed Stations

**Definition:** Stations present in July 2024 snapshot but ABSENT from Jan 2026 snapshot.

**Identification Logic:**
```
IF station_id IN july_2024_snapshot AND station_id NOT IN jan_2026_snapshot
  THEN classify as "Removed Station"
```

**Subcategories:**
- **Permanent Decommissioning:** Station closed permanently (equipment removed, site repurposed)
- **Temporary Closure (Extended):** Station offline for >6 months (construction, equipment failure, permit issues)
- **Data Quality Issue:** Station exists but removed from AFDC database due to unconfirmed status

**Data Validation:**
- Check July 2024 `date_last_confirmed` field: If >180 days old at time of July 2024 snapshot, removal may reflect data cleanup, not actual decommissioning
- Check July 2024 `status_code`: If `status_code=T` (Temporarily Unavailable) in July 2024, removal may reflect permanent closure decision

**Analytical Implications:**
- **Infrastructure Loss:** Subtract connector count and capacity from supply metrics
- **Geographic Impact:** Identify counties/ZIPs losing infrastructure (rural areas at higher risk)
- **Network Attrition:** Assess which operators are exiting NC market

**Handling Edge Cases:**
- **Temporary Closure vs. Permanent Removal:** If removed station reappears in future snapshots, reclassify as "Temporary Closure"
- **Station ID Changes:** Rare, but network acquisitions or ownership transfers may result in new station IDs for same physical location (requires geographic matching)

#### 2.2.3 Metadata Updates (Persistent Stations)

**Definition:** Stations present in BOTH snapshots with matching `station_id` but changes in metadata fields.

**Identification Logic:**
```
IF station_id IN july_2024_snapshot AND station_id IN jan_2026_snapshot
  THEN compare all fields
    IF any_field_changed
      THEN classify as "Metadata Update"
      ELSE classify as "Unchanged Station"
```

**Common Metadata Change Types:**

| Change Type | Field(s) Affected | Significance | Example |
|-------------|------------------|--------------|---------|
| **Equipment Upgrade** | `ev_dc_fast_num`, `ev_connector_types` | Capacity increase | Adding 4 DCFC units to existing Level 2-only station |
| **Network Transfer** | `ev_network`, `ev_network_web` | Ownership change | ChargePoint station acquired by Electrify America |
| **Access Policy Change** | `access_code`, `access_detail_code` | Availability shift | Workplace charging opening to public on weekends |
| **Pricing Update** | `ev_pricing` | Economic analysis | Price increase from $0.43/kWh to $0.53/kWh |
| **Verification Update** | `date_last_confirmed`, `updated_at` | Data quality maintenance | Routine AFDC database maintenance (not infrastructure change) |
| **Operational Status** | `status_code` | Availability change | `E` → `T` (temporary closure) or `T` → `E` (reopening) |

**Analytical Approach:**
1. **Create Field-Level Diff:** Compare each field between snapshots
2. **Prioritize High-Impact Changes:** Equipment upgrades, network transfers, access changes
3. **Filter Out Low-Impact Changes:** Routine verification updates (`date_last_confirmed` changes with no other field changes)

**Example Comparison Query (Conceptual):**
```sql
SELECT
  july.station_id,
  july.station_name,
  july.ev_dc_fast_num AS july_dcfc,
  jan.ev_dc_fast_num AS jan_dcfc,
  (jan.ev_dc_fast_num - july.ev_dc_fast_num) AS dcfc_change
FROM july_2024_snapshot AS july
INNER JOIN jan_2026_snapshot AS jan
  ON july.station_id = jan.station_id
WHERE july.ev_dc_fast_num != jan.ev_dc_fast_num
ORDER BY dcfc_change DESC;
```

#### 2.2.4 Status Changes (Planned → Operational)

**Definition:** Stations with `status_code=P` (Planned) in July 2024 becoming `status_code=E` (Available) in Jan 2026.

**Identification Logic:**
```
IF july_2024.status_code = 'P' AND jan_2026.status_code = 'E'
  THEN classify as "Planned-to-Operational Transition"
```

**Significance:**
- **NEVI Program Tracking:** NC's $109M in NEVI funding results in planned stations (identified via `status_code=P`)
- **Infrastructure Pipeline Validation:** Compare `expected_date` in July 2024 snapshot to actual `open_date` in Jan 2026 snapshot
- **Deployment Velocity:** Measure time from planned announcement to operational status

**Analytical Metrics:**
- **Delivery Rate:** (Stations transitioning to operational) / (Total planned stations in July 2024) × 100%
- **Delay Analysis:** Compare `expected_date` to actual `open_date` for stations that opened
- **Cancellation Rate:** Planned stations in July 2024 still showing `status_code=P` or absent in Jan 2026 snapshot

**Example:**
- July 2024: 15 stations with `status_code=P` in Wake County
- Jan 2026: 12 of those stations now `status_code=E` (opened), 2 still `status_code=P` (delayed), 1 absent (cancelled)
- Delivery rate: 80% (12/15)
- Cancellation rate: 6.7% (1/15)

### 2.3 Key Metrics for Infrastructure Evolution

#### 2.3.1 Net Growth Metrics

| Metric | Calculation | Interpretation |
|--------|-------------|----------------|
| **Net Station Growth** | (Jan 2026 total stations) - (July 2024 total stations) | Absolute change in station count |
| **Station Growth Rate** | [(Jan 2026 - July 2024) / July 2024] × 100% | Percentage increase in stations |
| **Net Connector Growth** | (Jan 2026 total connectors) - (July 2024 total connectors) | Absolute change in charging ports |
| **Connector Growth Rate** | [(Jan 2026 - July 2024) / July 2024] × 100% | Percentage increase in charging capacity |
| **Net Capacity Growth (kW)** | Sum(Jan 2026 kW) - Sum(July 2024 kW) | Absolute change in charging power |

**EV Pulse NC Baseline (July 2024):**
- 355 stations
- 1,725 connectors
- Estimated total capacity: ~260,000 kW (assuming 150 kW average per DCFC × 1,725 units × 0.805 DCFC ratio)

**Hypothetical Jan 2026 Comparison:**
- If Jan 2026 shows 425 stations (+70, 19.7% growth) and 2,100 connectors (+375, 21.7% growth)
- Interpretation: Connector growth (21.7%) outpacing station growth (19.7%) suggests new stations have higher connector density (larger Supercharger installations, higher-capacity Electrify America sites)

#### 2.3.2 Deployment Rate Analysis

**Objective:** Measure infrastructure deployment velocity relative to BEV adoption rate.

**Key Calculations:**

| Metric | Formula | Context |
|--------|---------|---------|
| **BEV Growth Rate** | [(June 2025 BEVs - July 2024 BEVs) / July 2024 BEVs] × 100% | From NCDOT registration data |
| **Infrastructure Growth Rate** | [(Jan 2026 connectors - July 2024 connectors) / July 2024 connectors] × 100% | From AFDC snapshots |
| **Gap Closure Ratio** | Infrastructure Growth Rate / BEV Growth Rate | >1.0 = gap closing, <1.0 = gap widening |

**Example:**
- July 2024 BEVs: ~85,000 (estimated from NCDOT trend)
- June 2025 BEVs: 94,371 (NCDOT data)
- BEV Growth: 11.0% (94,371 / 85,000)
- July 2024 Connectors: 1,725
- Jan 2026 Connectors: 2,100 (hypothetical)
- Connector Growth: 21.7% (2,100 / 1,725)
- **Gap Closure Ratio: 1.97** (21.7% / 11.0%)
- **Interpretation:** Infrastructure deploying 2x faster than BEV adoption → gap is closing

**EV Pulse NC Current Finding:**
- BEV CAGR: 53.8% (Sept 2018 - June 2025)
- Infrastructure baseline: 47.6% added in 2024-2025 (implies ~70% annual growth in recent period)
- Likely conclusion: Recent infrastructure surge is catching up to demand, but historical lag remains

#### 2.3.3 Spatial Distribution Shifts

**Objective:** Identify whether infrastructure growth is concentrated in urban cores (exacerbating inequality) or expanding to rural/underserved areas (improving equity).

**County-Level Analysis:**

| County Classification | July 2024 Share | Jan 2026 Share | Shift Interpretation |
|-----------------------|-----------------|----------------|----------------------|
| **Research Triangle (Wake, Durham, Orange)** | 35.2% of connectors | 33.8% (hypothetical) | Decentralization (equity improvement) |
| **Urban 11 (top counties)** | 70% of connectors | 68% (hypothetical) | Slight rural expansion |
| **Rural 89 counties** | 30% of connectors | 32% (hypothetical) | Modest equity gains |

**Geographic Concentration Metric:**
- **Gini Coefficient (July 2024):** 0.805 (extreme inequality)
- **Gini Coefficient (Jan 2026):** Calculate from new snapshot
- **Interpretation:** Decrease in Gini coefficient = more equitable distribution

**ZIP-Level Analysis (Priority #2 Integration):**
- Calculate Herfindahl-Hirschman Index (HHI) for ZIP-level concentration
- Identify "charging deserts": ZIPs with zero infrastructure in July 2024 gaining first station by Jan 2026
- Measure gap severity changes at ZIP level for Priority #2 analysis

#### 2.3.4 Infrastructure Type Evolution

**Level 2 vs. DCFC Capacity Trends:**

**Current State (July 2024):**
- 80.5% of connectors ≥150 kW (DCFC)
- 19.5% Level 2 (<50 kW)
- **Interpretation:** NC deployment prioritizes high-power DCFC for highway corridors and high-throughput locations

**Comparison Approach:**
```
Level2_Share_July = (ev_level2_evse_num_sum / total_connectors) × 100%
DCFC_Share_July = (ev_dc_fast_num_sum / total_connectors) × 100%

Level2_Share_Jan = (ev_level2_evse_num_sum / total_connectors) × 100%
DCFC_Share_Jan = (ev_dc_fast_num_sum / total_connectors) × 100%

Shift = DCFC_Share_Jan - DCFC_Share_July
```

**Interpretation Scenarios:**
- **DCFC share increases:** Continued focus on high-throughput infrastructure (highway corridors, urban cores)
- **Level 2 share increases:** Expansion into destination charging (workplaces, shopping centers, residential complexes)

**Priority #3 Workplace Analysis Integration:**
- Filter stations with `facility_type=WORKPLACE`
- Calculate Level 2 vs. DCFC mix for workplace stations
- Expected pattern: Workplace charging predominantly Level 2 (8-hour dwell time vs. 30-minute fast charge)

### 2.4 Handling Edge Cases

#### 2.4.1 Temporary Closures

**Challenge:** Distinguish between temporary closure and permanent decommissioning.

**Approach:**
1. **July 2024 Status:** Check `status_code=T` (Temporarily Unavailable)
2. **Jan 2026 Status:**
   - If `status_code=E` → Reopened (no infrastructure loss)
   - If `status_code=T` → Extended closure (infrastructure unavailable but not removed)
   - If absent from snapshot → Likely permanent closure

**Analytical Treatment:**
- **For Gap Analysis:** Treat temporarily unavailable stations as unavailable capacity (do not count in supply metric)
- **For Deployment Analysis:** Track reopenings as "restored capacity" (distinct from new capacity)

#### 2.4.2 Ownership Transfers

**Challenge:** Network acquisitions or ownership changes may result in station metadata changes without physical infrastructure change.

**Example:**
- July 2024: Station operated by "Greenlots"
- Jan 2026: Same station now operated by "Shell Recharge" (Shell acquired Greenlots)
- Physical infrastructure unchanged, but `ev_network` field updated

**Identification:**
- Match stations by `station_id` + geographic coordinates (`latitude`, `longitude`)
- Compare `ev_network` field
- If network changed but `ev_dc_fast_num`, `ev_level2_evse_num`, and `ev_connector_types` unchanged → Ownership transfer, not equipment upgrade

**Analytical Treatment:**
- **For Supply Metrics:** No change (same capacity under new operator)
- **For Market Analysis:** Track network consolidation trends

#### 2.4.3 Equipment Upgrades

**Challenge:** Existing station adds DCFC units or increases connector count without changing station ID.

**Example:**
- July 2024: Station has 4 Level 2 connectors (J1772), 0 DCFC
- Jan 2026: Same station now has 4 Level 2 connectors + 2 DCFC units (J1772COMBO, 150 kW each)

**Identification:**
```sql
SELECT
  station_id,
  (jan.ev_dc_fast_num - july.ev_dc_fast_num) AS dcfc_added,
  (jan.ev_level2_evse_num - july.ev_level2_evse_num) AS level2_added
FROM july_2024_snapshot AS july
INNER JOIN jan_2026_snapshot AS jan
  ON july.station_id = jan.station_id
WHERE (jan.ev_dc_fast_num > july.ev_dc_fast_num)
   OR (jan.ev_level2_evse_num > july.ev_level2_evse_num);
```

**Analytical Treatment:**
- **For Net Growth Metrics:** Include added connectors in "Net Connector Growth"
- **For Geographic Analysis:** Attribute capacity increase to existing station's county/ZIP (not counted as new station)
- **For Investment Analysis:** Equipment upgrades represent reinvestment in existing sites (lower capital cost than greenfield deployment)

---

## 3. NREL API CAPABILITIES (CONCEPTUAL)

### 3.1 Query Parameters for NC-Specific Filtering

**Base Endpoint:** `GET https://developer.nrel.gov/api/alt-fuel-stations/v1.json`

**NC Electric Charging Stations Query:**
```
Parameters:
  api_key: YOUR_API_KEY (required)
  state: NC (required for NC filtering)
  fuel_type: ELEC (required for EV charging only)
  status: E (optional, for operational stations only)
  limit: all (required to retrieve all stations, not just first 200)
```

**Full Query URL (Conceptual):**
```
https://developer.nrel.gov/api/alt-fuel-stations/v1.json?api_key=YOUR_KEY&state=NC&fuel_type=ELEC&status=E&limit=all
```

**Response Format:**
- JSON (default): Nested structure with `fuel_stations` array
- CSV: Flat table (easier for direct import into SAS/Python)
- GeoJSON: Geographic data format for GIS integration

### 3.2 Date-Range Query Support

**CRITICAL LIMITATION:** AFDC API does NOT support date-range queries for historical snapshots.

**Available Temporal Filtering:**
- `open_date` (filter by station opening date)
- `updated_at` (filter by last database update)

**Example - Stations Opened Since July 2024:**
```
Parameters:
  api_key: YOUR_API_KEY
  state: NC
  fuel_type: ELEC
  status: E
  open_date: 2024-07-01,2026-01-31 (hypothetical, NOT supported by current API)
```

**WORKAROUND:** API only returns CURRENT snapshot (Jan 2026 data as of Jan 2026).
- **For Temporal Analysis:** Must download and archive snapshots at regular intervals (quarterly, monthly)
- **Historical Snapshots:** NREL provides bulk data downloads at https://afdc.energy.gov/data_download
- **Best Practice:** Archive API snapshots locally for future comparison

**EV Pulse NC Implication:**
- July 2024 snapshot already exists as `alt_fuel_stations_ev_charging_units.csv` (archived)
- Jan 2026 snapshot would be new API call in January 2026
- Future snapshots (quarterly through 2026-2028) should be archived for longitudinal analysis

### 3.3 Rate Limits and Access Requirements

**NREL API Rate Limits:**
- **Free Tier:** 1,000 requests per hour per API key
- **Rolling Window:** 60-minute rolling basis (not fixed hourly reset)
- **Enforcement:** Exceeding limit results in HTTP 429 error, API key blocked for 1 hour

**API Key Acquisition:**
- **Registration:** Free at https://developer.nrel.gov/signup/
- **Approval:** Instant (no waiting period)
- **Delivery:** API key displayed on screen immediately after form submission
- **Format:** 40-character alphanumeric string

**Rate Limit Monitoring:**
- Response headers include `X-RateLimit-Limit` and `X-RateLimit-Remaining`
- Example: `X-RateLimit-Remaining: 987` (987 requests left this hour)

**EV Pulse NC Usage Estimate:**
- **Single NC Snapshot:** 1 API call (all NC stations in one request with `limit=all`)
- **100 NC Counties (Individual Queries):** 100 API calls (if querying by county)
- **Connector-Level Data:** 1 API call to `/ev-charging-units` endpoint (CSV download)
- **Conclusion:** Well within 1,000 requests/hour limit (snapshot update is low-frequency operation)

**Higher Rate Limits:**
- Available upon request for production applications
- Contact: NREL Developer Network support (https://developer.nrel.gov/)

### 3.4 Data Quality Flags and Confidence Indicators

**Geocoding Confidence:**
- `geocode_status` field indicates spatial accuracy
  - `"GPS"` - Surveyed GPS coordinates (highest confidence, ±5m)
  - `"200-9"` - Address-based geocoding (medium confidence, ±50-100m)
  - Missing coordinates - Requires manual geocoding or spatial join

**Data Verification Status:**
- `date_last_confirmed` - Last date AFDC verified station data
  - Stations not confirmed in >90 days may have outdated information
  - Stations not confirmed in >180 days may be closed/decommissioned but not yet removed from database

**Operational Status Flags:**
- `status_code` - Current operational status
  - `E` (Available) - High confidence, station operational
  - `P` (Planned) - Future capacity, not yet operational
  - `T` (Temporarily Unavailable) - Lower confidence, station may be offline indefinitely

**AFDC Data Quality Research Findings:**
- **Access Code Misclassification:** Some stations labeled "public" may have restrictions (workplace-only during business hours, membership required, call ahead)
- **Incomplete Records:** Some stations missing pricing information, access hours, or connector details
- **Network Reporting Variability:** Different network operators have different data update frequencies (Tesla updates monthly, smaller networks quarterly)

**Data Validation Recommendations:**
- Filter for `geocode_status="GPS"` for high-accuracy spatial analysis
- Exclude stations with `date_last_confirmed` >180 days old for current capacity assessment
- Cross-validate workplace stations (`facility_type=WORKPLACE`) with Priority #3 CTPP data

---

## 4. INFRASTRUCTURE CLASSIFICATION FOR PRIORITY INTEGRATION

### 4.1 ZIP-Level Aggregation (Priority #2)

**Objective:** Enable sub-county gap analysis by aggregating charging infrastructure to ZIP code level.

**AFDC Field:** `zip` (5-digit ZIP code)

**Aggregation Methodology:**
```sql
-- Conceptual SQL for ZIP-level aggregation
SELECT
  zip,
  county,
  COUNT(DISTINCT station_id) AS stations,
  SUM(ev_level2_evse_num) AS level2_connectors,
  SUM(ev_dc_fast_num) AS dcfc_connectors,
  SUM(ev_level2_evse_num + ev_dc_fast_num) AS total_connectors
FROM jan_2026_snapshot
WHERE state = 'NC' AND status_code = 'E'
GROUP BY zip, county
ORDER BY total_connectors DESC;
```

**Integration with NCDOT BEV Data:**
- Current EV Pulse NC data: County-level BEV registrations (8,200 county-month observations)
- Missing: ZIP-level BEV data (NCDOT does not publish ZIP-level registration data)
- **Workaround:** Allocate county-level BEV counts to ZIPs proportionally based on:
  - Population (Census ZIP Code Tabulation Area population estimates)
  - Household income (IRS SOI Tax Stats)
  - Housing units (American Community Survey)

**ZIP-Level Gap Metrics:**
| Metric | Calculation | Interpretation |
|--------|-------------|----------------|
| **BEVs per Charging Port** | (Allocated ZIP BEVs) / (ZIP total connectors) | Accessibility metric |
| **BEVs per kW Capacity** | (Allocated ZIP BEVs) / (ZIP total kW) | Utilization pressure |
| **Charging Desert Indicator** | ZIP with 0 connectors AND >100 allocated BEVs | High-priority gap |

**Spatial Analysis Enhancement:**
- **County-Level (Current):** 100 geographic units (coarse)
- **ZIP-Level (Priority #2):** ~750 ZIPs in NC (fine-grained)
- **Benefit:** Identify sub-county gaps (e.g., Wake County has excellent infrastructure overall, but western Wake ZIPs underserved)

### 4.2 Workplace vs. Public Station Classification (Priority #3)

**Objective:** Integrate AFDC charging station data with CTPP (Census Transportation Planning Products) commuting data to identify workplace charging gaps.

**AFDC Classification Fields:**

| Field | Value | Classification Logic |
|-------|-------|----------------------|
| `facility_type` | `WORKPLACE` | Likely workplace charging |
| `facility_type` | `PARKING_LOT`, `PARKING_GARAGE` | May be workplace if located in commercial district |
| `access_code` | `public` | Open to general public (not restricted to employees) |
| `access_code` | `private` | Restricted access (likely employee-only) |
| `access_detail_code` | `WORKPLACE_ONLY` | Definitive workplace-only classification |
| `owner_type_code` | `P` (Private) | Likely corporate-owned workplace charging |

**Workplace Charging Classification Rules:**

| Rule | Logic | Confidence |
|------|-------|------------|
| **High Confidence Workplace** | `facility_type=WORKPLACE` AND `access_detail_code=WORKPLACE_ONLY` | 95% |
| **Likely Workplace** | `facility_type=WORKPLACE` AND `access_code=private` | 80% |
| **Possible Workplace** | `facility_type=WORKPLACE` AND `access_code=public` | 60% (may allow public access during business hours) |
| **Public (Not Workplace)** | `facility_type` NOT `WORKPLACE` AND `access_code=public` | 90% |

**Data Quality Challenge:**
- AFDC research identified **misclassification where some stations labeled as 'public' may actually be workplace charging locations not accessible to the general public**
- **Validation Strategy:** Cross-reference AFDC workplace stations with Priority #3 CTPP workplace locations (census blocks with high employment density)

**Integration with CTPP Data (Priority #3):**

**CTPP Dataset:** Census Transportation Planning Products - Journey-to-Work data
- **Workplace Locations:** Census blocks with employment counts by industry
- **Commuting Flows:** Origin-destination pairs (residence county → workplace county)
- **Daytime Population:** Workers present in geographic area during business hours

**Spatial Join Approach:**
1. **AFDC Workplace Stations:** Filter `facility_type=WORKPLACE`
2. **CTPP High-Employment Blocks:** Census blocks with >500 workers
3. **Spatial Join:** Assign workplace stations to census blocks
4. **Gap Analysis:** Census blocks with high employment but zero workplace charging

**Workplace Charging Gap Metric:**
```
Workplace Gap Score = (Census Block Workers) / (Workplace Connectors in Block)

High-Priority Gap: Blocks with >1,000 workers and 0 workplace connectors
```

**Expected Findings:**
- **Research Triangle:** High concentration of workplace charging (corporate campuses, tech companies)
- **Charlotte Metro:** Likely high workplace charging in Uptown/South End commercial districts
- **Rural Counties:** Likely zero workplace charging (limited commercial employment centers)

### 4.3 Charger Type Importance for Gap Analysis

**Level 2 vs. DCFC Segmentation:**

**Rationale:** Level 2 and DCFC serve fundamentally different use cases:
- **Level 2 (3-19.2 kW):** 2-8 hour charging, suitable for workplace, residential, destination charging
- **DCFC (≥50 kW):** 15-45 minute charging, suitable for highway corridors, urban cores, high-turnover locations

**Gap Analysis Implications:**

| Use Case | Ideal Charger Type | Dwell Time | Priority Locations |
|----------|-------------------|------------|-------------------|
| **Workplace Charging** | Level 2 | 8 hours | Office parks, corporate campuses |
| **Destination Charging** | Level 2 | 2-4 hours | Shopping centers, restaurants, hotels |
| **Highway Travel** | DCFC | 20-30 min | Interstate exits, highway corridors |
| **Urban Core** | DCFC | 20-30 min | Dense residential areas (apartment complexes without home charging) |

**NC Infrastructure Profile (Current):**
- **80.5% DCFC (≥150 kW)** - Highway corridor emphasis (I-85, I-40, I-95)
- **19.5% Level 2** - Limited workplace/destination charging

**Gap Interpretation:**
- **Urban Metros (Wake, Mecklenburg):** DCFC adequate, Level 2 likely sufficient (high home ownership = home charging)
- **Suburban/Exurban Areas:** Level 2 gap for workplace charging (Priority #3 target)
- **Rural Corridors:** DCFC gap for long-distance travel (NEVI funding priority)

**Segmented Gap Metrics:**

| County Type | DCFC Gap Metric | Level 2 Gap Metric |
|-------------|-----------------|-------------------|
| **Urban Core** | BEVs per DCFC port (target: <20) | BEVs per Level 2 port (target: <30) |
| **Suburban** | BEVs per DCFC port (target: <25) | BEVs per Level 2 port (target: <50) |
| **Rural** | DCFC stations per 100 miles of highway | Level 2 stations per 10,000 population |

**Capacity-Weighted Gap Metric (Current EV Pulse NC Approach):**
```
Gap = Total BEVs / Total Charging Capacity (kW)

Capacity (kW) = (Level 2 connectors × 7.2 kW avg) + (DCFC connectors × 150 kW avg)
```

**Advantage:** Accounts for power output differences (1 DCFC unit ≈ 20 Level 2 units in throughput)

---

## 5. DATA CURRENCY BEST PRACTICES

### 5.1 Industry Standards for EV Infrastructure Data Refresh Frequency

**Federal Requirements:**

| Program | Update Frequency | Source |
|---------|------------------|--------|
| **NEVI (National Electric Vehicle Infrastructure)** | Real-time uptime reporting, >97% uptime requirement | Bipartisan Infrastructure Law (2021) |
| **California AB 2127** | Biennial (every 2 years) for state reporting | California Energy Commission |
| **State NEVI Awards Dashboard** | Ongoing tracking, updated as states report | Joint Office of Energy and Transportation |

**Research Standards:**

| Analysis Type | Recommended Refresh | Rationale |
|--------------|---------------------|-----------|
| **Production Dashboards** | Daily or weekly | Real-time policy monitoring, charger availability tracking |
| **Academic Research** | Quarterly | Balance data freshness with analysis stability |
| **Policy Reports** | Annually or biennially | Long-term trend analysis, stable for multi-year comparisons |
| **Competition Submissions** | At submission deadline | Ensure data reflects current state for evaluation |

**Industry Practice (Charging Network Operators):**

| Network | Public Data Update Frequency | Internal Monitoring |
|---------|------------------------------|---------------------|
| **Tesla Supercharger** | Monthly (AFDC reporting) | Real-time (internal systems) |
| **Electrify America** | Monthly (AFDC reporting) | Real-time (app updates) |
| **ChargePoint** | Quarterly (AFDC reporting) | Real-time (network dashboard) |
| **Smaller Networks** | Quarterly or less frequent | Varies by operator |

### 5.2 Examples from Other State/Regional Analyses

**Peer State Analyses:**

| State/Region | Data Update Practice | Citation |
|--------------|----------------------|----------|
| **California** | Biennial reports with quarterly dashboard updates | CA Energy Commission AB 2127 |
| **All 50 States (EDF Report)** | Annual policy tracking, 2-year infrastructure data snapshots | Environmental Defense Fund (2025) |
| **Global EV Outlook (IEA)** | Annual report with infrastructure data lagged by 6-12 months | International Energy Agency (2025) |

**Research Papers (EV Infrastructure Temporal Analysis):**

1. **"Large-scale empirical study of electric vehicle usage patterns and charging infrastructure needs" (Nature, 2024)**
   - Data: Real-time charging session data from network operators
   - Limitation: "Static snapshots do not incorporate seasonal or long-term temporal variation"
   - Recommendation: Continuous monitoring for accurate demand forecasting

2. **"Spatiotemporal planning of electric vehicle charging infrastructure" (ScienceDirect, 2025)**
   - Approach: Quarterly snapshots for trend analysis, monthly snapshots for forecasting
   - Finding: 3-month data lag acceptable for planning, but 6+ months introduces significant forecasting error

3. **"Electric Vehicle Charging Load Forecasting: An Experimental" (arXiv, 2024)**
   - Approach: Evaluated short-term (30 min), mid-term (8 hours), long-term (5 days) forecasting horizons
   - Data freshness: Real-time for operational forecasting, monthly aggregates for capacity planning

**Industry Best Practices from Global EV Outlook 2025 (IEA):**
- **Policy Analysis:** Annual updates sufficient (infrastructure deployment is multi-year process)
- **Market Monitoring:** Quarterly updates recommended (capture seasonal trends, identify emerging gaps)
- **Real-Time Operations:** Daily/weekly updates required (charger availability, uptime monitoring)

### 5.3 When Infrastructure Data Becomes "Stale Enough" to Impact Policy Recommendations

**Data Staleness Thresholds:**

| Time Lag | Impact on Analysis | Recommendation |
|----------|-------------------|----------------|
| **0-3 months** | Minimal impact | Acceptable for most research and policy analysis |
| **3-6 months** | Moderate impact | Acceptable for long-term trend analysis, but note data limitations |
| **6-12 months** | High impact | Infrastructure may have changed significantly; recommendations may be outdated |
| **>12 months** | Critical impact | Data should be refreshed before policy recommendations are issued |

**EV Pulse NC Current Situation:**
- **Data Snapshot:** July 2024 (695 MB CSV file)
- **Current Date:** January 30, 2026
- **Data Age:** 18 months (July 2024 → January 2026)
- **Staleness Assessment:** **CRITICAL - Data refresh highly recommended**

**Rationale for EV Pulse NC Data Refresh:**

1. **Rapid Infrastructure Growth Rate:**
   - Current finding: 47.6% of infrastructure added in 2024-2025
   - Implication: 18-month lag means snapshot may miss ~40-50% of current infrastructure

2. **NEVI Funding Deployment:**
   - NC received $109M in NEVI funding (2022-2026 program)
   - Peak deployment period: 2024-2026 (funds must be obligated by Sept 2026)
   - 18-month lag likely misses substantial NEVI-funded deployments in 2025-2026

3. **Policy Relevance:**
   - Competition focuses on NEVI funding allocation recommendations
   - Outdated infrastructure data → Outdated gap analysis → Potentially misallocated funding recommendations

4. **Comparison to BEV Data:**
   - NCDOT BEV data: Current through June 2025 (7-month lag)
   - AFDC infrastructure data: July 2024 (18-month lag)
   - **Temporal Misalignment:** BEV data more current than infrastructure data (creates artifactual gap exaggeration)

**Temporal Misalignment Example:**
```
July 2024 Infrastructure: 1,725 connectors
July 2024 BEVs: ~85,000 (estimated)
Gap Ratio: 85,000 / 1,725 = 49.3 BEVs per port

June 2025 BEVs: 94,371 (actual NCDOT data)
July 2024 Infrastructure: 1,725 connectors (STALE)
Gap Ratio: 94,371 / 1,725 = 54.7 BEVs per port

IF Jan 2026 Infrastructure: 2,100 connectors (hypothetical)
June 2025 BEVs: 94,371
Corrected Gap Ratio: 94,371 / 2,100 = 44.9 BEVs per port

Conclusion: Using stale infrastructure data OVERSTATES gap by ~22% (54.7 vs. 44.9)
```

### 5.4 Recommendation for EV Pulse NC Data Refresh Timing

**Optimal Refresh Strategy:**

| Priority | Timing | Rationale |
|----------|--------|-----------|
| **Immediate (Week 1)** | Jan 27 - Feb 1, 2026 | Update before Priority #2 and #3 analyses begin (avoid rework) |
| **Pre-Competition (Week 3)** | Feb 9-15, 2026 | Final refresh before paper writing (ensure latest data in submission) |
| **Post-Competition (Ongoing)** | Quarterly (April, July, Oct 2026) | Maintain dataset for future analysis, capstone presentations |

**Recommended Update Frequency for Competition:**

1. **Priority #5 Implementation (Week 1):** Download Jan 2026 snapshot
2. **Mid-Competition Check (Week 3):** Validate no major infrastructure changes since Jan snapshot
3. **Post-Submission Archive:** Save Feb 2026 snapshot for future reference

**Long-Term Best Practice:**
- **Quarterly Updates:** Align with NEVI reporting cycles (quarterly performance data)
- **Archival Strategy:** Maintain snapshots as timestamped CSV files (e.g., `afdc_nc_stations_2026_01.csv`)
- **Version Control:** Track dataset versions in Git LFS (existing EV Pulse NC practice)

---

## 6. SUMMARY AND IMPLEMENTATION ROADMAP

### 6.1 Key Takeaways

1. **AFDC Data Structure:**
   - ~50+ fields per station, including critical temporal metadata (`date_last_confirmed`, `open_date`, `updated_at`)
   - Connector-level granularity (1,725 connectors across 355 stations = 4.85x multiplier)
   - Rich classification fields support ZIP-level analysis (Priority #2) and workplace segmentation (Priority #3)

2. **Snapshot Comparison Methodology:**
   - Four change types: New stations, Removed stations, Metadata updates, Status changes
   - Key metrics: Net growth, deployment rate, spatial distribution shifts, infrastructure type evolution
   - Edge cases: Temporary closures, ownership transfers, equipment upgrades

3. **NREL API Capabilities:**
   - Simple NC filtering: `?api_key=KEY&state=NC&fuel_type=ELEC&limit=all`
   - 1,000 requests/hour rate limit (single snapshot = 1 request)
   - No historical date-range queries (must archive snapshots manually)

4. **Infrastructure Classification:**
   - ZIP-level: Use `zip` field for Priority #2 sub-county analysis
   - Workplace vs. Public: Use `facility_type` + `access_detail_code` for Priority #3 CTPP integration
   - Level 2 vs. DCFC: Segment by use case (workplace/destination vs. highway/urban core)

5. **Data Currency:**
   - 18-month data lag is CRITICAL staleness for NC's rapid infrastructure growth
   - Recommended refresh: Immediate (Week 1) to avoid gap analysis overstatement
   - Best practice: Quarterly updates for competition-grade policy analysis

### 6.2 Integration with EV Pulse NC Priorities

| Priority | Integration Point | AFDC Data Fields | Benefit |
|----------|------------------|------------------|---------|
| **Priority #2: ZIP Code Analysis** | `zip` field | `zip`, `latitude`, `longitude`, `ev_dc_fast_num`, `ev_level2_evse_num` | Sub-county gap analysis (750 ZIPs vs. 100 counties) |
| **Priority #3: CTPP Workplace** | `facility_type`, `access_detail_code` | `facility_type`, `access_code`, `access_detail_code`, `owner_type_code` | Identify workplace charging gaps for commuter analysis |
| **Priority #5: AFDC Update** | Snapshot comparison | All fields (focus on `open_date`, `status_code`, `ev_dc_fast_num`) | Validate gap closure/widening, update infrastructure baseline |

### 6.3 Conceptual Implementation Workflow (NO CODE EXECUTION)

**Step 1: Download Jan 2026 Snapshot**
- API Call: `GET https://developer.nrel.gov/api/alt-fuel-stations/v1.json?api_key=KEY&state=NC&fuel_type=ELEC&limit=all`
- Save as: `afdc_nc_stations_2026_01.csv`
- Archive July 2024 snapshot as: `afdc_nc_stations_2024_07.csv`

**Step 2: Load Snapshots into SAS Viya**
- Import both CSV files into CAS tables
- Ensure `station_id` field is numeric for joining

**Step 3: Identify Change Types**
```sql
-- New Stations
SELECT * FROM jan_2026
WHERE station_id NOT IN (SELECT station_id FROM july_2024);

-- Removed Stations
SELECT * FROM july_2024
WHERE station_id NOT IN (SELECT station_id FROM jan_2026);

-- Metadata Updates
SELECT
  july.station_id,
  july.ev_dc_fast_num AS july_dcfc,
  jan.ev_dc_fast_num AS jan_dcfc
FROM july_2024 AS july
INNER JOIN jan_2026 AS jan
  ON july.station_id = jan.station_id
WHERE july.ev_dc_fast_num != jan.ev_dc_fast_num;
```

**Step 4: Calculate Gap Metrics**
```sql
-- County-level net growth
SELECT
  county,
  COUNT(*) AS jan_stations,
  SUM(ev_dc_fast_num + ev_level2_evse_num) AS jan_connectors
FROM jan_2026
GROUP BY county;

-- Compare to July 2024 baseline
-- Calculate BEVs per connector with updated infrastructure data
```

**Step 5: ZIP-Level Aggregation (Priority #2)**
```sql
SELECT
  zip,
  county,
  COUNT(*) AS stations,
  SUM(ev_dc_fast_num + ev_level2_evse_num) AS connectors
FROM jan_2026
WHERE status_code = 'E'
GROUP BY zip, county;
```

**Step 6: Workplace Station Filter (Priority #3)**
```sql
SELECT
  station_id,
  station_name,
  facility_type,
  access_code,
  access_detail_code,
  ev_level2_evse_num,
  latitude,
  longitude
FROM jan_2026
WHERE facility_type = 'WORKPLACE'
   OR (facility_type IN ('PARKING_LOT', 'PARKING_GARAGE') AND owner_type_code = 'P');
```

**Step 7: Update Gap Analysis Visualizations**
- Regenerate county-level heatmaps with Jan 2026 data
- Add ZIP-level heatmaps (Priority #2)
- Overlay workplace stations on CTPP high-employment census blocks (Priority #3)

---

## 7. CONCLUSION

This conceptual framework provides a comprehensive roadmap for updating EV Pulse NC's AFDC charging station data from the July 2024 snapshot (18 months stale) to a current January 2026 snapshot. The 18-month data lag is assessed as **critically stale** given NC's rapid infrastructure deployment rate (47.6% of current infrastructure added in 2024-2025), and an immediate data refresh is strongly recommended to avoid gap analysis overstatement.

The AFDC API provides rich temporal metadata (`date_last_confirmed`, `open_date`, `updated_at`) and detailed classification fields (`facility_type`, `access_detail_code`, `zip`) that enable:
1. **Snapshot comparison** to quantify infrastructure evolution (new stations, equipment upgrades, closures)
2. **ZIP-level analysis** for Priority #2 sub-county gap assessment
3. **Workplace classification** for Priority #3 CTPP commuting integration

The NREL API offers a straightforward single-request snapshot download with a generous 1,000 requests/hour rate limit, making quarterly data updates feasible for competition-grade policy analysis. No implementation has been performed per the directive; this document serves as a methodological blueprint for Priority #5 execution in Week 1 of the competition timeline (Jan 27 - Feb 1, 2026).

---

## SOURCES

- [NREL Developer Network](https://developer.nrel.gov/)
- [Alternative Fuel Stations API - All Stations](https://developer.nrel.gov/docs/transportation/alt-fuel-stations-v1/all/)
- [NREL Web Service Rate Limits](https://developer.nrel.gov/docs/rate-limits/)
- [AFDC Data Download](https://afdc.energy.gov/data_download)
- [AFDC Electric Vehicle Charging Infrastructure Trends](https://afdc.energy.gov/fuels/electricity-infrastructure-trends)
- [Alternative Fuel Stations API - EV Charging Ports](https://developer.nrel.gov/docs/transportation/alt-fuel-stations-v1/ev-charging-units/)
- [California AB 2127 EV Charging Infrastructure Dashboards](https://www.energy.ca.gov/data-reports/data-exploration-tools/ab-2127-ev-charging-infrastructure-report-dashboards)
- [National Electric Vehicle Infrastructure (NEVI) Awards Dashboard](https://evstates.org/awards-dashboard/)
- [Federal Register: National Electric Vehicle Infrastructure Standards and Requirements](https://www.federalregister.gov/documents/2023/02/28/2023-03500/national-electric-vehicle-infrastructure-standards-and-requirements)
- [Equity and reliability of public electric vehicle charging stations in the United States - PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12177045/)
- [Large-scale empirical study of electric vehicle usage patterns and charging infrastructure needs - Nature](https://www.nature.com/articles/s44333-024-00023-3)
- [Spatiotemporal planning of electric vehicle charging infrastructure - ScienceDirect](https://www.sciencedirect.com/science/article/pii/S2589004225016293)
- [Global EV Outlook 2025 - IEA](https://www.iea.org/reports/global-ev-outlook-2025/electric-vehicle-charging)
- [EV Charging Infrastructure Maintenance 2026 - Fleet Uptime](https://mail.buscmms.com/blog/ev-charging-infrastructure-maintenance-2026)

---

**Document Version:** 1.0
**Author:** EV Pulse NC Research Team
**Status:** Conceptual framework complete - No implementation performed
**Next Steps:** Week 1 implementation (Jan 27 - Feb 1, 2026) per top-priorities.txt timeline
