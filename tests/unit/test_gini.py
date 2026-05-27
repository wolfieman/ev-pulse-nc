"""Unit tests for the inequality metrics in phase3_gini_inequality.

These pin the closed-form properties of the estimators (perfect equality
gives zero, the two-point maximum is 0.5) and the NaN/inf guards that the
downstream county and statewide summaries rely on.

Copyright © 2026 Wolfgang Sanyer
Licensed under the Polyform Noncommercial License 1.0.0 (see LICENSE).
"""

from __future__ import annotations

import math

import numpy as np
import phase3_gini_inequality as gini
import pytest

pytestmark = pytest.mark.unit


def test_gini_uniform_is_zero():
    assert gini.gini_unweighted(np.array([5.0, 5.0, 5.0, 5.0])) == 0.0


def test_gini_two_point_is_one_half():
    assert gini.gini_unweighted(np.array([0.0, 1.0])) == pytest.approx(0.5)


def test_gini_unweighted_nan_guards():
    assert math.isnan(gini.gini_unweighted(np.array([5.0])))         # n < 2
    assert math.isnan(gini.gini_unweighted(np.array([])))            # empty
    assert math.isnan(gini.gini_unweighted(np.array([0.0, 0.0])))    # all zero


def test_gini_stays_in_unit_interval():
    rng = np.random.default_rng(0)
    values = rng.gamma(2.0, 3.0, size=50)
    assert 0.0 <= gini.gini_unweighted(values) <= 1.0


def test_gini_weighted_equal_weights_matches_unweighted():
    values = np.array([1.0, 2.0, 8.0, 20.0])
    weights = np.ones_like(values)
    assert gini.gini_weighted(values, weights) == pytest.approx(
        gini.gini_unweighted(values)
    )


def test_gini_weighted_nan_guards():
    assert math.isnan(gini.gini_weighted(np.array([1.0]), np.array([1.0])))
    assert math.isnan(
        gini.gini_weighted(np.array([1.0, 2.0]), np.array([0.0, 0.0]))
    )


def test_ratio_max_min_is_inf_when_min_is_zero():
    assert gini.ratio_max_min(np.array([0.0, 5.0])) == float("inf")


def test_iqr_requires_four_values():
    assert math.isnan(gini.iqr(np.array([1.0, 2.0, 3.0])))
    assert gini.iqr(np.array([1.0, 2.0, 3.0, 4.0])) == pytest.approx(1.5)
