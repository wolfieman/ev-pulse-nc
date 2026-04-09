# AFDC Dataset Reference

**Purpose:** Current-state reference for the AFDC (Alternative Fuels Data Center) charging-station dataset used as the supply-side foundation for EV Pulse NC.

The AFDC dataset was originally planned as a dual-snapshot comparison between a "July 2024" file and a 2026 update. During Phase 2 the older file was identified as a DCFC-only, public-only connector-level extract (not a full snapshot), so the dual-snapshot framing was abandoned. The Feb 2026 full API pull is now the single authoritative infrastructure baseline.

---

## Source

| Attribute | Value |
|---|---|
| **Provider** | NREL — Alternative Fuels Data Center |
| **API endpoint** | `https://developer.nrel.gov/api/alt-fuel-stations/v1.json` |
| **Query parameters** | `state=NC`, `fuel_type=ELEC` |
| **API key** | Free, instant approval at `https://developer.nrel.gov/signup/` |
| **Rate limit** | 1,000 requests/hour |
| **Download script** | `code/python/data-acquisition/afdc_api_download.py` |

## Authoritative File

| Attribute | Value |
|---|---|
| **Path** | `data/raw/afdc-charging-stations-connector-2026-02.csv` |
| **Vintage** | February 2026 API pull |
| **Granularity** | Station-level (one row per station) |
| **Columns** | 76 |
| **Schema doc** | [`afdc-data-structure.md`](./afdc-data-structure.md) |

## Current Counts (Feb 2026 baseline)

| Metric | Count |
|---|---:|
| **Stations** | 1,985 |
| **Connectors (all levels)** | 6,145 |
| &nbsp;&nbsp;DCFC ports | 1,747 |
| &nbsp;&nbsp;Level 2 ports | 4,363 |
| &nbsp;&nbsp;Level 1 ports | 35 |
| **Unique cities** | 267 |
| **Unique ZIP codes** | 358 |
| **Public stations** | 1,876 |
| **L2-only stations** | 1,636 (82.4% of total) |

Coverage spans **all charging levels** (L1, L2, DCFC) and **all access types** (public, private, workplace, fleet).

## Reference / Legacy File

| Attribute | Value |
|---|---|
| **Path** | `data/raw/afdc-charging-stations-connector-2024-07.csv` |
| **Status** | Retained for reproducibility — NOT used in analysis |
| **Why retained** | Source for the comparison documented in `data/raw/AFDC-DATA-COMPARISON.md` |
| **Scope** | DCFC-only, public-only, connector-level (355 stations, 1,725 rows) |

The "2024-07" filename is misleading: the file's `Updated At` field extends to 2025-12-22. It was a filtered AFDC website export, not a full point-in-time snapshot.

## Refresh Cadence

The Feb 2026 pull is the canonical baseline for the capstone deliverables. No additional refreshes are planned within the capstone window. For post-capstone roadmap work, the API can be re-queried at any time using the download script; quarterly is the recommended cadence for policy-grade analysis.

## How the Dataset Is Used

| Phase | Use |
|---|---|
| **Phase 2** | Supply-side foundation; complete infrastructure inventory |
| **Phase 3 (ZIP analysis)** | ZIP-level station distribution across all charging levels |
| **Phase 4 (CTPP workplace)** | Facility-type and L2 classification for workplace-charging analysis |
| **Phase 5 (Scoring framework)** | BEVs-per-port utilization scores against full inventory (not DCFC-only) |
| **Phase 6 (Buffer — future)** | Coverage zones using complete station locations |

## Related Documents

- [`afdc-data-structure.md`](./afdc-data-structure.md) — field-level schema reference
- [`analytical-pipeline.md`](./analytical-pipeline.md) — how supply data feeds the full pipeline
- [`README.md`](./README.md) — frameworks directory and phase status
- [`../data/raw/AFDC-DATA-COMPARISON.md`](../data/raw/AFDC-DATA-COMPARISON.md) — full old-vs-new comparison

---

*Replaces: `priority-5-afdc-update-decision-framework.md` (Feb 2026 decision-tree document, superseded by Phase 2 outcome).*
