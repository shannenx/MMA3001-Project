"""Windowed (recent-history) features for RUL prediction.

A single cycle's sensor readings are noisy. Looking at the last ``window``
cycles lets a model average out the noise and see the *direction* sensors are
moving. For every sensor and every cycle we summarise the window that ends at
that cycle:

* ``last``  - the reading at the window's final cycle
* ``mean``  - the average over the window
* ``std``   - the spread over the window (population standard deviation)
* ``slope`` - the least-squares trend, in sensor units per cycle

Rules (also documented in the project README):

* A window only uses cycles of **one engine** and never looks ahead, so the
  features at cycle ``t`` depend only on cycles ``t - window + 1 ... t``.
* **Training tables** keep only rows with a complete window, i.e. cycles
  ``>= window``. Nothing is padded or invented.
* **Prediction from a test engine** uses its final window. If an engine has
  fewer than ``window`` cycles, :func:`last_window_rows` raises an error
  rather than padding. (The shortest FD001 test engine has 31 cycles, so
  windows up to 31 are usable on FD001.)
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from numpy.lib.stride_tricks import sliding_window_view

VALID_STATS = ("last", "mean", "std", "slope")
DEFAULT_STATS = ("last", "mean", "slope")


def _check_args(df: pd.DataFrame, feature_cols, window: int, stats) -> None:
    """Validate arguments shared by the public functions."""
    if not isinstance(window, (int, np.integer)) or window < 1:
        raise ValueError("window must be a positive integer.")
    unknown = [s for s in stats if s not in VALID_STATS]
    if unknown or len(stats) == 0:
        raise ValueError(f"stats must be a non-empty subset of {VALID_STATS}; got {list(stats)}.")
    missing = [c for c in ["engine", "cycle", *feature_cols] if c not in df.columns]
    if missing:
        raise ValueError(f"df is missing required columns: {missing}")


def feature_names(feature_cols: list[str], stats=DEFAULT_STATS) -> list[str]:
    """Return the output column names, e.g. ``sensor_2__mean``.

    Args:
        feature_cols: Input sensor column names.
        stats: Which window statistics are produced (see :data:`VALID_STATS`).

    Returns:
        Names ordered by statistic, then by sensor.
    """
    return [f"{c}__{s}" for s in stats for c in feature_cols]


def _window_stats(values: np.ndarray, window: int, stats) -> np.ndarray:
    """Summarise every complete window of one engine.

    Args:
        values: Array of shape ``(n_cycles, n_sensors)``, ordered by cycle.
        window: Window length in cycles.
        stats: Statistics to compute.

    Returns:
        Array of shape ``(n_cycles - window + 1, n_sensors * len(stats))``.
        Row ``i`` summarises cycles ``i ... i + window - 1``.
    """
    w = sliding_window_view(values, window, axis=0)  # (n_win, n_sensors, window)
    out = []
    t = np.arange(window, dtype=float)
    t_centred = t - t.mean()
    denom = float((t_centred ** 2).sum())
    for s in stats:
        if s == "last":
            out.append(w[..., -1])
        elif s == "mean":
            out.append(w.mean(axis=-1))
        elif s == "std":
            out.append(w.std(axis=-1))
        elif s == "slope":
            if window == 1:
                out.append(np.zeros(w.shape[:2]))
            else:
                out.append((w * t_centred).sum(axis=-1) / denom)
    return np.concatenate(out, axis=1)


def window_table(
    df: pd.DataFrame,
    feature_cols: list[str],
    window: int = 30,
    stats=DEFAULT_STATS,
) -> pd.DataFrame:
    """Build one windowed-feature row for every complete window.

    Args:
        df: Table with ``engine``, ``cycle`` and the sensor columns, with
            consecutive cycles per engine (as returned by
            :func:`src.data_loader.load_fd001`). A ``RUL`` column, if present,
            is carried through: the RUL at the *end* of each window.
        feature_cols: Sensor columns to summarise.
        window: Window length in cycles (>= 1). ``window=1`` reduces to the
            single-cycle features (``slope`` is 0 and ``std`` is 0).
        stats: Subset of :data:`VALID_STATS`.

    Returns:
        One row per engine-cycle with ``cycle >= window``, with columns
        ``engine``, ``cycle``, ``RUL`` (if present in ``df``) and the
        windowed features named by :func:`feature_names`. Engines shorter than
        ``window`` contribute no rows. Rows are ordered by engine, then cycle.

    Raises:
        ValueError: If ``window`` is not a positive integer, ``stats`` is
            invalid or empty, or a required column is missing.
    """
    _check_args(df, feature_cols, window, stats)
    return _build_rows(df, feature_cols, window, stats, last_only=False)


def _build_rows(df, feature_cols, window, stats, last_only: bool) -> pd.DataFrame:
    """Shared builder for :func:`window_table` and :func:`last_window_rows`.

    Args:
        df: Validated input table.
        feature_cols: Sensor columns to summarise.
        window: Window length.
        stats: Statistics to compute.
        last_only: If True, summarise only each engine's final window instead
            of every window (about ``n_cycles`` times less work).

    Returns:
        The windowed table, ordered by engine and cycle.
    """
    names = feature_names(list(feature_cols), stats)
    d = df.sort_values(["engine", "cycle"])
    eng = d["engine"].to_numpy()
    cyc = d["cycle"].to_numpy()
    vals = d[list(feature_cols)].to_numpy(dtype=float)
    rul = d["RUL"].to_numpy() if "RUL" in d.columns else None

    # Engine boundaries in the sorted arrays. All the work below is on NumPy
    # arrays; building one small DataFrame per engine was the main cost
    # (see notebooks/05_performance.ipynb).
    starts = np.flatnonzero(np.r_[True, eng[1:] != eng[:-1]]) if len(eng) else np.array([], dtype=int)
    ends = np.r_[starts[1:], len(eng)] if len(eng) else np.array([], dtype=int)

    feats, e_parts, c_parts, r_parts = [], [], [], []
    for s, e in zip(starts, ends):
        if e - s < window:
            continue
        lo = e - window if last_only else s
        f = _window_stats(vals[lo:e], window, stats)
        feats.append(f)
        e_parts.append(np.full(len(f), eng[s]))
        c_parts.append(cyc[lo + window - 1:e])
        if rul is not None:
            r_parts.append(rul[lo + window - 1:e])
    if not feats:
        return pd.DataFrame(columns=["engine", "cycle", *names])

    data = {"engine": np.concatenate(e_parts).astype(int),
            "cycle": np.concatenate(c_parts).astype(int)}
    if rul is not None:
        data["RUL"] = np.concatenate(r_parts)
    out = pd.DataFrame(data)
    return pd.concat([out, pd.DataFrame(np.vstack(feats), columns=names)], axis=1)


def last_window_rows(
    df: pd.DataFrame,
    feature_cols: list[str],
    window: int = 30,
    stats=DEFAULT_STATS,
) -> pd.DataFrame:
    """Build the windowed features for each engine's final window.

    This is the input used to predict an engine's RUL at the end of its
    (truncated) test record.

    Args:
        df: Table with ``engine``, ``cycle`` and the sensor columns.
        feature_cols: Sensor columns to summarise.
        window: Window length in cycles.
        stats: Subset of :data:`VALID_STATS`.

    Returns:
        One row per engine, ordered by engine ID, with the same columns as
        :func:`window_table`.

    Raises:
        ValueError: If any engine has fewer than ``window`` cycles (no
            padding is applied), or the arguments are invalid.
    """
    _check_args(df, feature_cols, window, stats)
    lengths = df.groupby("engine")["cycle"].size()
    short = lengths[lengths < window]
    if len(short):
        raise ValueError(
            f"{len(short)} engine(s) have fewer than {window} cycles "
            f"(shortest: {int(lengths.min())}); no padding is applied. "
            f"Use a window of at most {int(lengths.min())}."
        )
    return _build_rows(df, feature_cols, window, stats, last_only=True)
