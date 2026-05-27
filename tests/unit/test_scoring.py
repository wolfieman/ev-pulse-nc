"""Unit tests for the NEVI scoring primitives in scoring_framework_final.

Pins the min-max normalizer's zero-variance behavior (which the
equity-zero-station column depends on) and the composite weight definition
(0.40 equity / 0.35 utilization / 0.25 cost-effectiveness) that produces the
published priority scores.

Copyright © 2026 Wolfgang Sanyer
Licensed under the Polyform Noncommercial License 1.0.0 (see LICENSE).
"""

from __future__ import annotations

import pandas as pd
import pytest
import scoring_framework_final as scoring

pytestmark = pytest.mark.unit


def test_minmax_maps_to_unit_interval():
    out = scoring.minmax(pd.Series([10.0, 20.0, 30.0]))
    assert out.min() == pytest.approx(0.0)
    assert out.max() == pytest.approx(1.0)
    assert out.iloc[1] == pytest.approx(0.5)


def test_minmax_zero_variance_returns_zero():
    out = scoring.minmax(pd.Series([7.0, 7.0, 7.0]))
    assert (out == 0.0).all()


def test_composite_weights_sum_to_one():
    total = (
        scoring.WEIGHT_EQUITY
        + scoring.WEIGHT_UTILIZATION
        + scoring.WEIGHT_COST_EFFECTIVENESS
    )
    assert total == pytest.approx(1.0)


def test_composite_weight_values():
    assert scoring.WEIGHT_EQUITY == 0.40
    assert scoring.WEIGHT_UTILIZATION == 0.35
    assert scoring.WEIGHT_COST_EFFECTIVENESS == 0.25
