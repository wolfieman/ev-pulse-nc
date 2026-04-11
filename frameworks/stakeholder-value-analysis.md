# Stakeholder Value Analysis

**Purpose:** Identifies the stakeholders served by the EV Pulse NC scoring framework and summarizes what each gets from the delivered NEVI county-allocation methodology and underlying analyses.

The framework integrates a complete AFDC infrastructure baseline (1,985 stations, 6,145 connectors, all charging levels and access types — Feb 2026 API pull), validated BEV demand forecasts, ZIP-level spatial analysis, CTPP workplace-charging classification, and CEJST Justice40 equity overlays into a single weighted county score:

```
NEVI Priority Score(county) = w1 × Equity + w2 × Utilization + w3 × Cost-Effectiveness
```

---

## Stakeholders

### NEVI Formula Program Administrators (NCDOT, FHWA)

**What they get:**
- A defensible, weighted ranking of the top 10 NC counties (73% of statewide BEV fleet) for NEVI prioritization, with framework designed for statewide extension
- Equity weighting aligned with the federal Justice40 initiative (CEJST tract-level designations)
- Sensitivity analysis demonstrating that top-ranked counties are robust across reasonable weight variations
- A methodology that translates findings into allocation decisions, directly responsive to the proposal feedback to "clearly define prioritization criteria within a scoring framework"

**Key value:** Audit-ready justification for funding decisions tied to federal program requirements.

### County and Regional Planners

**What they get:**
- County-level utilization metrics (BEVs per port across all charging levels, not just DCFC)
- ZIP-level infrastructure distribution identifying intra-county gaps (Phase 3)
- Workplace-vs-residential demand context from CTPP commuting flows (Phase 4)
- Identification of zero-infrastructure ZIPs and rural-access gaps

**Key value:** Sub-county granularity to inform local site selection and grant applications.

### Private-Sector Charging Network Operators

**What they get:**
- Complete competitive baseline of NC charging infrastructure including all networks and access types
- Network-level market share data (`ev_network` field) across L1, L2, and DCFC
- Identification of underserved geographies where additional public or private investment would relieve demand pressure
- Workplace-charging market sizing from CTPP commuting flows

**Key value:** Market intelligence and white-space identification for capital deployment decisions.

### Academic and Research Community

**What they get:**
- A reproducible methodology with documented data sources, schemas, and processing scripts
- A publicly accessible scoring framework that other states can adapt
- Validation work (MAPE 4.34%, 69.00% underprediction characterization) usable as a forecasting case study
- Integration of CEJST equity data with infrastructure analysis — a methodological contribution

**Key value:** Reproducibility and methodological transparency for further research and peer review.

### Public and Community Stakeholders (including Justice40 communities)

**What they get:**
- Equity-weighted analysis that explicitly elevates disadvantaged communities (CEJST Justice40 designations)
- Transparency into how funding allocation decisions are made
- Identification of communities currently underserved by charging infrastructure
- A 40% benefits floor consistent with the federal Justice40 initiative

**Key value:** Procedural and distributional fairness in how public infrastructure investments are prioritized.

---

## How the Framework Serves All Stakeholders Simultaneously

| Score Component | Source Phase | Primary Stakeholder Beneficiary |
|---|---|---|
| **Equity** (Justice40 %, Gini, rural-access gap) | Phase 5 (CEJST) + Phase 3 (ZIP) | Public communities, NEVI administrators |
| **Utilization** (BEVs/port across all levels) | Phase 1 (Validation) + Phase 2 (AFDC) | County planners, private operators |
| **Cost-Effectiveness** (workplace efficiency, density) | Phase 4 (CTPP) | Private operators, county planners |

The single weighted score reconciles these stakeholder perspectives rather than producing separate rankings for each. Sensitivity analysis on the weights (w1, w2, w3) shows that the top-priority counties remain stable across the literature-supported range (equity-heavy ~0.40 / 0.35 / 0.25), giving administrators confidence that the ranking does not depend on a single defensible weight choice.

## Related Documents

- [`README.md`](./README.md) — frameworks directory and phase status
- [`analytical-pipeline.md`](./analytical-pipeline.md) — full analytical pipeline
- [`afdc-dataset-reference.md`](./afdc-dataset-reference.md) — supply-side data foundation
- [`afdc-data-structure.md`](./afdc-data-structure.md) — schema reference

---

*Replaces: `priority-5-stakeholder-value-integration-analysis.md` (Feb 2026 stakeholder analysis built on the abandoned dual-snapshot framing).*
