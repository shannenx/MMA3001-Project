"""Small helpers for timing and memory measurements.

Used by ``notebooks/05_performance.ipynb``. They are kept in a module so they
can be tested and reused.

Notes on accuracy of the measurements:

* Timing uses ``time.perf_counter`` (wall-clock). Repeat runs are reported as
  median/min/max because a single timing is noisy (other programs, CPU
  frequency changes, caches).
* Memory uses ``tracemalloc``, which sees memory allocated through Python and
  NumPy but **not** all memory allocated inside compiled libraries, so treat it
  as a lower bound on total memory use.
"""

from __future__ import annotations

import time
import tracemalloc
from typing import Callable

import numpy as np


def time_repeated(fn: Callable[[], object], repeats: int = 5, warmup: int = 1) -> dict:
    """Time a zero-argument function several times.

    Args:
        fn: Function to time. Called ``warmup + repeats`` times in total.
        repeats: Number of timed runs (>= 1).
        warmup: Number of untimed runs first (>= 0), so one-off costs such as
            imports and cache warm-up are not counted.

    Returns:
        A dict with ``median_s``, ``min_s``, ``max_s`` (seconds) and
        ``repeats``.

    Raises:
        ValueError: If ``repeats`` < 1 or ``warmup`` < 0.
    """
    if repeats < 1:
        raise ValueError("repeats must be at least 1.")
    if warmup < 0:
        raise ValueError("warmup must not be negative.")
    for _ in range(warmup):
        fn()
    times = []
    for _ in range(repeats):
        t0 = time.perf_counter()
        fn()
        times.append(time.perf_counter() - t0)
    arr = np.asarray(times)
    return {
        "median_s": float(np.median(arr)),
        "min_s": float(arr.min()),
        "max_s": float(arr.max()),
        "repeats": repeats,
    }


def peak_memory_mib(fn: Callable[[], object]) -> float:
    """Peak extra memory (MiB) allocated while ``fn`` runs, via tracemalloc.

    Memory already allocated before the call is not counted. Allocations made
    inside compiled libraries that bypass Python/NumPy are not seen, so this
    is a lower bound. Tracing slows the code down, so never use this run for
    timing.

    Args:
        fn: Function to run.

    Returns:
        Peak traced allocation in MiB (1 MiB = 1,048,576 bytes).
    """
    was_tracing = tracemalloc.is_tracing()
    if was_tracing:
        tracemalloc.stop()
    tracemalloc.start()
    try:
        fn()
        _, peak = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()
    return peak / (1024 ** 2)


def empirical_exponent(sizes, times) -> float:
    """Estimate ``k`` in ``time ~ size**k`` from measurements.

    Fits a straight line to ``log(time)`` against ``log(size)``. A value near
    1 means time grows roughly linearly with data size, near 2 quadratically,
    and below 1 means fixed overheads dominate at these sizes.

    Args:
        sizes: Problem sizes (for example number of training rows). Positive.
        times: Measured times for each size. Positive.

    Returns:
        The fitted slope.

    Raises:
        ValueError: If fewer than two points are given, the lengths differ, or
            any value is not positive.
    """
    s = np.asarray(sizes, dtype=float)
    t = np.asarray(times, dtype=float)
    if s.shape != t.shape or s.size < 2:
        raise ValueError("Need at least two matching sizes and times.")
    if (s <= 0).any() or (t <= 0).any():
        raise ValueError("Sizes and times must be positive.")
    return float(np.polyfit(np.log(s), np.log(t), 1)[0])
