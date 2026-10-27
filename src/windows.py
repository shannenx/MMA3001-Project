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
    names = feature_names(list(feature_cols), stats)
    pieces = []
    for engine, g in df.sort_values(["engine", "cycle"]).groupby("engine", sort=True):
        if len(g) < window:
            continue
        feats = _window_stats(g[list(feature_cols)].to_numpy(dtype=float), window, stats)
        piece = pd.DataFrame(feats, columns=names)
        piece.insert(0, "cycle", g["cycle"].to_numpy()[window - 1:])
        piece.insert(0, "engine", engine)
        if "RUL" in g.columns:
            piece.insert(2, "RUL", g["RUL"].to_numpy()[window - 1:])
        pieces.append(piece)
    if not pieces:
        return pd.DataFrame(columns=["engine", "cycle", *names])
    out = pd.concat(pieces, ignore_index=True)
    out["engine"] = out["engine"].astype(int)
    out["cycle"] = out["cycle"].astype(int)
    return out


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
    table = window_table(df, feature_cols, window, stats)
    return table.loc[table.groupby("engine")["cycle"].idxmax()].sort_values("engine").reset_index(drop=True)
