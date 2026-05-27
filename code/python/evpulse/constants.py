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

# Projected CRS for every map and area/length computation. NC State Plane
# (NAD83, meters) keeps areas and distances accurate statewide; defined once so
# all geographic figures share one projection and per-area metrics stay
# comparable across maps.
TARGET_CRS = "EPSG:32119"  # NC State Plane (NAD83, meters)

# Sequential colormap for the choropleth/heat maps. Shared so the figure set
# reads as one visual family rather than drifting per script.
COLORMAP = "YlGnBu"

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
