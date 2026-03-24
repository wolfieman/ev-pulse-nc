# VIF / Multicollinearity Analysis — NEVI Scoring Framework Action Plan

**Created:** 2026-03-23
**Source:** SAS Training 2 Module 5 (Multicollinearity) + Module 5 EV Pulse Applicability doc
**Status:** NOT YET IMPLEMENTED — code provided below, ready to execute

---

## 1. Current State: VIF Analysis Does NOT Exist

Searched both repos (`ev-pulse-nc/` and `spring-26-bida670-advanced-analytics/`):

- **No Python script** computes VIF or checks multicollinearity for the scoring framework
- **No results** (tables, figures, or printed output) exist in any markdown or CSV
- **Planning docs exist** in `module-5-ev-pulse-applicability.md` — VIF is flagged as "HIGH" priority (row 20 in the technique-application table) and called "Critical for defensibility"
- The scoring framework final script (`scoring_framework_final.py`) has no collinearity checks

---

## 2. Why This Matters

The NEVI scoring equation is:

```
NEVI Score(county) = 0.40 * Equity + 0.35 * Utilization + 0.25 * Cost-Effectiveness
```

If the three sub-scores are correlated (e.g., high-equity counties also have high utilization), the weighted sum **double-counts** the same underlying factor. The 0.40/0.35/0.25 weights become misleading — they imply three independent dimensions, but the actual effective weighting is skewed.

VIF quantifies this. From Module 5:
- VIF = 1 / (1 - R^2), where R^2 is from regressing one component on the other two
- VIF = 1.0: perfectly orthogonal (ideal)
- VIF < 5: acceptable
- VIF 5-10: concerning, investigate
- VIF > 10: problematic, components may be redundant

---

## 3. Where to Add It

### Primary: ev-pulse-nc repo

**Script:** `code/python/analysis/scoring_framework_vif.py` (new, small standalone script)

- Reads `data/processed/scoring-framework-final.csv`
- Computes VIF for the three sub-scores
- Computes pairwise Pearson correlations
- Prints results and saves a small summary CSV

**Paper placement:**
- **Methodology section** — describe VIF as a validation step for scoring framework independence
- **Results section** — report VIF values and correlation matrix as a table
- **If VIF < 5 for all three:** one paragraph stating the pillars are sufficiently independent, strengthening the defensibility claim
- **If VIF > 5 for any:** discuss in Limitations, consider PCA or removing redundant pillar

### PAPER-NOTES.md

Add a note under an appropriate section referencing the VIF results.

---

## 4. Exact Python Code

```python
#!/usr/bin/env python3
"""
NEVI Scoring Framework — VIF / Multicollinearity Check.

Computes Variance Inflation Factors for the three scoring pillars
(equity, utilization, cost-effectiveness) to verify they are
sufficiently independent to justify the weighted composite.

Usage:
    uv run code/python/analysis/scoring_framework_vif.py
"""

from pathlib import Path

import pandas as pd
from statsmodels.stats.outliers_influence import variance_inflation_factor
import statsmodels.api as sm

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
FINAL_CSV = PROJECT_ROOT / "data" / "processed" / "scoring-framework-final.csv"

df = pd.read_csv(FINAL_CSV)
scores = df[["equity_score", "util_score", "cost_score"]].copy()

# --- Pairwise Correlations ---
print("=" * 60)
print("PAIRWISE CORRELATIONS (Pearson)")
print("=" * 60)
corr = scores.corr()
print(corr.round(4))

# --- VIF ---
print("\n" + "=" * 60)
print("VARIANCE INFLATION FACTORS")
print("=" * 60)
X = sm.add_constant(scores)
vif_data = pd.DataFrame({
    "Variable": scores.columns,
    "VIF": [variance_inflation_factor(X.values, i + 1) for i in range(len(scores.columns))]
})
print(vif_data.to_string(index=False))

# --- Interpretation ---
max_vif = vif_data["VIF"].max()
print(f"\nMax VIF: {max_vif:.2f}")
if max_vif < 5:
    print("RESULT: No multicollinearity concern (all VIF < 5).")
    print("The three scoring pillars are sufficiently independent.")
    print("The 0.40/0.35/0.25 weights are defensible.")
elif max_vif < 10:
    print("WARNING: Moderate multicollinearity detected (VIF 5-10).")
    print("Investigate which pillars overlap. Consider combining or PCA.")
else:
    print("PROBLEM: High multicollinearity (VIF > 10).")
    print("Scoring pillars are redundant. Weights are unstable.")

# --- Save ---
output = PROJECT_ROOT / "data" / "processed" / "scoring-vif-check.csv"
vif_data.to_csv(output, index=False)
print(f"\nSaved: {output}")
```

---

## 5. What to Expect (Informed Prediction)

Looking at the actual data (10 counties, `scoring-framework-final.csv`):

- **Equity** is driven by Justice40%, Gini, underserved ZIPs — socioeconomic/demographic factors
- **Utilization** is driven by BEV-per-port — a demand/supply ratio
- **Cost-effectiveness** is driven by workplace charging efficiency, commuter demand, pop density — economic/geographic factors

**Likely outcome:** VIF will probably be **low (1-3)** because:
1. Equity measures *who needs it* (disadvantaged communities)
2. Utilization measures *how strained existing infrastructure is*
3. Cost-effectiveness measures *where investment dollars go furthest*

These are conceptually distinct. However, there could be moderate correlation between cost-effectiveness and utilization (both relate to population density and economic activity).

**Even if VIF is low, reporting it is valuable** because:
- It directly addresses Dr. Al-Ghandour's feedback about defensibility
- It shows methodological rigor (the student didn't just assume independence)
- It's a standard check that reviewers expect when using weighted composites

---

## 6. Important Caveat: n = 10

The scoring framework currently covers only 10 counties (top BEV counties). With n = 10 and k = 3 predictors, VIF is computable but has low statistical power. This should be noted:

- "VIF was computed as a diagnostic check with the caveat that n = 10 limits statistical precision"
- If the framework is extended to all 100 NC counties, VIF should be recomputed

---

## 7. Checklist

- [ ] Create `scoring_framework_vif.py` in `ev-pulse-nc/code/python/analysis/`
- [ ] Run it and capture output
- [ ] Add VIF table to paper Results section
- [ ] Add one-paragraph interpretation to paper Discussion/Methodology
- [ ] Add note to PAPER-NOTES.md
- [ ] If VIF > 5 for any pillar, investigate and document mitigation
- [ ] Rerun after extending to 100 counties (if applicable)
