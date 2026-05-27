"""Load-bearing constants shared across the analysis pipeline.

Single source of truth for values that were previously duplicated across
scripts, where drift between copies would silently change published results.

Copyright © 2026 Wolfgang Sanyer
Licensed under the Polyform Noncommercial License 1.0.0 (see LICENSE).
"""

from __future__ import annotations

# NEVI Priority Score pillar weights (manuscript Section 2.3). They sum to 1.0
# and define the headline composite score, so they are defined once here and
# imported everywhere rather than redeclared per script.
WEIGHT_EQUITY = 0.40
WEIGHT_UTILIZATION = 0.35
WEIGHT_COST_EFFECTIVENESS = 0.25

# The ten study counties (top-10 by BEV registration) that the analysis scores.
# Bare county names; consumers that match census-style "X County" labels append
# the suffix. The scoring pipeline derives its working cohort from the data, so
# this list is the canonical set of names, not a computational input.
STUDY_COUNTIES = [
    "Wake",
    "Mecklenburg",
    "Durham",
    "Guilford",
    "Union",
    "Buncombe",
    "Cabarrus",
    "Orange",
    "Forsyth",
    "New Hanover",
]
