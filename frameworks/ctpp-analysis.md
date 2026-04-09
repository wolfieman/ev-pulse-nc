# Phase 4: Workplace Charging (LEHD/LODES) — Delivered Framework

## Executive Summary

Phase 4 transformed EV infrastructure analysis from a single-dimension residential model to a dual-dimension residential + workplace model by incorporating inter-county commuting flows. The delivered analysis used **LEHD LODES** (Origin-Destination, Workplace Area Characteristics, and geography crosswalk) rather than CTPP, which was the originally planned source. LODES provides more recent data (2021) and higher geographic fidelity than CTPP, and was cross-corrected with ACS income tabulations and a Barrero, Bloom & Davis (2023) 0.85 remote-work multiplier.

**Critical finding:** Employment centers need 2-3x more infrastructure than residential-only analysis suggests. Workplace infrastructure serves roughly **15 BEVs/port vs. 7.5 BEVs/port for residential public** — a 2x efficiency gain driven by consistent Mon-Fri demand and 8-hour dwell times. Statewide adjusted workplace demand is **859,260 commuter-based EV charging events**, with Mecklenburg (+194,361 net inbound commuters), Wake (+126,517), and Durham (+89,450) as the dominant net employment centers.

Phase 4 outputs feed the Cost-Effectiveness Score of the NEVI scoring framework.

## Results

| Output | File | Description |
|--------|------|-------------|
| Cost-effectiveness | `data/processed/phase4-cost-effectiveness.csv` | Workplace vs. residential efficiency by county |
| Employment centers | `data/processed/phase4-employment-centers.csv` | Net inbound/outbound commuter flows, adjusted EV workplace demand |

### Key Findings

- **Statewide adjusted workplace demand:** 859,260 EV commuter charging events (post-SE03 income filter, post-0.85 remote-work multiplier)
- **Top net employment centers:** Mecklenburg +194,361, Wake +126,517, Durham +89,450
- **Workplace efficiency:** ~15 BEVs/port vs. ~7.5 BEVs/port residential public (2x efficiency)
- **Income filter:** LODES SE03 (earnings > $3,333/month) as proxy for workers with EV-consistent income profiles
- **Remote work adjustment:** 0.85 multiplier, Barrero/Bloom/Davis (2023), "The Evolution of Work from Home"
- **EV adoption rate:** Applied at origin county (determines home charging access), with 1.25 commuter-income premium

Phase 4 produced figures fig-35 through fig-38. See `frameworks/analytical-pipeline.md` for integration with the scoring framework.

---

## Methodology Notes

- **Data source choice:** Phase 4 used LEHD LODES (Origin-Destination, Workplace Area Characteristics, geography crosswalk) rather than the originally planned CTPP. LODES provides 2021 vintage versus CTPP's 2012-2016 vintage, and tabulates flows at the Census block level rather than county level, enabling sub-county workplace demand estimation.
- **Income filter:** The SE03 income segment (workers earning > $3,333/month, ≈$40k/year) was used as the primary EV-affordability proxy.
- **Adoption rate method:** Origin-county BEV adoption rates were applied (where commuters live, since home location determines charging access), multiplied by a 1.25 commuter-income premium reflecting that commuters earn ~25% more than non-commuters in NC.
- **Remote work adjustment:** A 0.85 remote-work multiplier (Barrero, Bloom, and Davis 2023) was applied uniformly to dampen 2021 LODES flows for post-COVID hybrid work patterns.
- **Scope:** The analysis focused on the top 15 employment centers, which capture roughly 80% of statewide net workplace demand.
