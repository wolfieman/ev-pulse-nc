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
