"""Unit tests for the Theil indices and their decomposition.

The additive within/between identity (T_total = T_between + T_within) is the
mathematical backbone of the paper's headline finding that 84.5% of
infrastructure inequality is within counties, so it is pinned to machine
precision here, alongside the closed-form zero at perfect equality.

Copyright © 2026 Wolfgang Sanyer
Licensed under the Polyform Noncommercial License 1.0.0 (see LICENSE).
"""

from __future__ import annotations

import math

import numpy as np
import pandas as pd
import phase3_theil_decomposition as theil
import pytest

pytestmark = pytest.mark.unit

DECOMP_TOL = 1e-10


def _two_county_frame() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "ports_per_10k": [2.0, 6.0, 10.0, 1.0, 3.0, 30.0],
            "population": [1000, 2000, 1500, 800, 1200, 500],
            "county_fips": ["37001", "37001", "37001", "37002", "37002", "37002"],
            "county_name": ["Alpha", "Alpha", "Alpha", "Bravo", "Bravo", "Bravo"],
        }
    )


def test_theil_t_uniform_is_zero():
    assert theil.theil_t(np.full(3, 4.0), np.ones(3)) == pytest.approx(0.0)


def test_theil_l_uniform_is_zero():
    assert theil.theil_l(np.full(3, 4.0), np.ones(3)) == pytest.approx(0.0)


def test_theil_t_positive_under_concentration():
    assert theil.theil_t(np.array([1.0, 1.0, 1.0, 8.0]), np.ones(4)) > 0.0


def test_theil_nan_guard_below_two_observations():
    assert math.isnan(theil.theil_t(np.array([4.0]), np.array([1.0])))


def test_decompose_theil_t_identity_holds():
    t_total, t_between, t_within, detail = theil.decompose_theil_t(_two_county_frame())
    assert abs(t_total - (t_between + t_within)) < DECOMP_TOL
    assert len(detail) == 2


def test_decompose_theil_l_identity_holds():
    l_total, l_between, l_within = theil.decompose_theil_l(_two_county_frame())
    assert abs(l_total - (l_between + l_within)) < DECOMP_TOL


def test_single_county_puts_all_inequality_within():
    df = _two_county_frame()
    df["county_fips"] = "37001"
    df["county_name"] = "Alpha"
    t_total, t_between, t_within, _ = theil.decompose_theil_t(df)
    assert t_between == pytest.approx(0.0, abs=DECOMP_TOL)
    assert t_within == pytest.approx(t_total, abs=DECOMP_TOL)
