# AFDC Data Structure

**Purpose:** Field-level schema reference for the AFDC charging-station dataset used by EV Pulse NC. Documents the 76-column station-level CSV produced by the NREL `alt-fuel-stations/v1` API and identifies which fields the project consumes.

The AFDC dataset was originally planned as a dual-snapshot comparison between a "July 2024" file and a 2026 update; during Phase 2 the older file was identified as a DCFC-only public extract, and the project now uses the Feb 2026 full API pull (1,985 stations, 6,145 connectors, all charging levels and all access types) as its single authoritative baseline. The schema below describes that current file.

For source, vintage, and counts see [`afdc-dataset-reference.md`](./afdc-dataset-reference.md).

---

## File

| Attribute | Value |
|---|---|
| **Path** | `data/raw/afdc-charging-stations-connector-2026-02.csv` |
| **Granularity** | One row per station |
| **Columns** | 76 |
| **Port counts** | Stored in aggregate columns (`ev_level1_evse_num`, `ev_level2_evse_num`, `ev_dc_fast_num`) |

## Core Identification

| Field | Type | Description |
|---|---|---|
| `id` | integer | Unique station identifier (primary key) |
| `station_name` | string | Official station name |
| `access_code` | string | `public` or `private` |
| `status_code` | string | `E` Available, `P` Planned, `T` Temporarily Unavailable |
| `fuel_type_code` | string | `ELEC` for all rows in this dataset |

## Geographic Location

| Field | Type | Use |
|---|---|---|
| `street_address` | string | Address, geocoding validation |
| `city` | string | Municipal aggregation |
| `state` | string | `NC` (filtered at query time) |
| `zip` | string | ZIP-level aggregation (Phase 3) |
| `latitude` | float | Spatial join to county / tract |
| `longitude` | float | Spatial join to county / tract |
| `geocode_status` | string | `GPS` (surveyed) or `200-9` (address-based) |

## Charging Infrastructure

| Field | Type | Use |
|---|---|---|
| `ev_level1_evse_num` | integer | Count of L1 ports (120 V, ~1.4–1.9 kW) |
| `ev_level2_evse_num` | integer | Count of L2 ports (240 V, ~3–19 kW) |
| `ev_dc_fast_num` | integer | Count of DCFC ports (≥50 kW) |
| `ev_connector_types` | array | NACS, J1772COMBO, CHADEMO, J1772 |
| `ev_network` | string | Tesla Supercharger, ChargePoint, Electrify America, eVgo, Non-Networked, etc. |
| `ev_pricing` | string | Pricing model (free text) |

**Charging-level vocabulary** used throughout the project:

- **L1** — 120 V household-style outlets (excluded from public gap analysis but counted)
- **L2** — 240 V dedicated circuits, the bulk of NC's charging network (1,636 L2-only stations)
- **DCFC** — DC fast charging, ≥50 kW, used for highway corridors and high-throughput sites

## Facility & Access

| Field | Type | Use |
|---|---|---|
| `facility_type` | string | `WORKPLACE`, `SHOPPING_MALL`, `PARKING_LOT`, `PARKING_GARAGE`, `HOTEL`, `CAR_DEALER`, `GAS_STATION`, `GOVERNMENT_FACILITY`, etc. — drives Phase 4 workplace classification |
| `owner_type_code` | string | `P` Private, `LG` Local Gov, `FG` Federal Gov, `SG` State Gov, `T` Utility |
| `access_days_time` | string | Hours of operation (free text) |
| `access_detail_code` | string | `PUBLIC`, `WORKPLACE_ONLY`, `CALL_AHEAD`, etc. |
| `restricted_access` | boolean | Restricted-access flag |
| `groups_with_access_code` | string | Restriction notes |

**Known classification edge case:** `facility_type=WORKPLACE` paired with `access_code=public` typically indicates employer-provided charging that is technically open to visitors during business hours. Phase 4 treats these as workplace, not public.

## Temporal Metadata

| Field | Type | Use |
|---|---|---|
| `date_last_confirmed` | date | Last verification date — staleness detection |
| `updated_at` | timestamp | Last database modification |
| `open_date` | date | Station opening date — deployment-timeline analysis |
| `expected_date` | date | Expected open date for `status_code=P` planned stations |

## Other Fuels (Not Used)

The API schema includes columns for CNG, LNG, LPG, hydrogen, biodiesel, ethanol, and renewable diesel (`cng_*`, `lng_*`, `lpg_*`, `hy_*`, `bd_*`, `e85_*`, `rd_*`, `ng_*`). These are present in the CSV but always null for `fuel_type=ELEC` rows and are ignored by the project.

## French-Localization Fields (Not Used)

Several `*_fr` fields (`access_days_time_fr`, `intersection_directions_fr`, `bd_blends_fr`, `groups_with_access_code_fr`, `ev_pricing_fr`) duplicate English fields for Canadian bilingual records. Ignored.

## Fields the Project Actively Uses

`id`, `station_name`, `access_code`, `status_code`, `latitude`, `longitude`, `city`, `zip`, `ev_level1_evse_num`, `ev_level2_evse_num`, `ev_dc_fast_num`, `ev_connector_types`, `ev_network`, `facility_type`, `owner_type_code`, `open_date`, `date_last_confirmed`.

## Related Documents

- [`afdc-dataset-reference.md`](./afdc-dataset-reference.md) — source, vintage, current counts
- [`analytical-pipeline.md`](./analytical-pipeline.md) — pipeline context
- [`README.md`](./README.md) — frameworks directory
- [`../data/raw/AFDC-DATA-COMPARISON.md`](../data/raw/AFDC-DATA-COMPARISON.md) — old vs. new file comparison

---

*Replaces: `afdc-data-structure-snapshot-comparison-framework.md` (Feb 2026 dual-snapshot methodology document, superseded by Phase 2 outcome).*
