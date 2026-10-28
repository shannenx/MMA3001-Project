"""Tests for src.benchmark."""

import time

import numpy as np
import pytest

from src.benchmark import empirical_exponent, peak_memory_mib, time_repeated


def test_time_repeated_calls_function_warmup_plus_repeats_times():
    calls = []
    time_repeated(lambda: calls.append(1), repeats=4, warmup=2)
    assert len(calls) == 6


def test_time_repeated_measures_a_known_delay():
    out = time_repeated(lambda: time.sleep(0.02), repeats=3, warmup=0)
    assert 0.015 < out["median_s"] < 0.2
    assert out["min_s"] <= out["median_s"] <= out["max_s"]
    assert out["repeats"] == 3


@pytest.mark.parametrize("kwargs", [{"repeats": 0}, {"warmup": -1}])
def test_time_repeated_rejects_bad_arguments(kwargs):
    with pytest.raises(ValueError):
        time_repeated(lambda: None, **kwargs)


def test_peak_memory_sees_a_known_allocation():
    # 5,000,000 float64 values = 40,000,000 bytes, about 38 MiB.
    peak = peak_memory_mib(lambda: np.zeros(5_000_000))
    assert 30 < peak < 60


def test_peak_memory_small_for_trivial_function():
    assert peak_memory_mib(lambda: sum(range(10))) < 1


def test_empirical_exponent_recovers_known_powers():
    sizes = np.array([100, 200, 400, 800])
    assert empirical_exponent(sizes, sizes ** 2.0) == pytest.approx(2.0)
    assert empirical_exponent(sizes, 3.0 * sizes) == pytest.approx(1.0)
    assert empirical_exponent(sizes, np.ones(4)) == pytest.approx(0.0)


@pytest.mark.parametrize(
    "sizes, times",
    [([1], [1]), ([1, 2], [1]), ([1, -2], [1, 2]), ([1, 2], [0, 1])],
)
def test_empirical_exponent_rejects_bad_input(sizes, times):
    with pytest.raises(ValueError):
        empirical_exponent(sizes, times)
