"""Metrics and validation for RUL prediction.

Validation is **grouped by engine**: all rows of one engine are either in the
training part or in the validation part of a fold, never both. Splitting by
row would let the model see near-identical neighbouring cycles of the same
engine during training and give falsely good scores.
"""

from __future__ import annotations

import time
from typing import Callable, Iterator

import numpy as np
import pandas as pd
from sklearn.model_selection import GroupKFold


def rmse(y_true, y_pred) -> float:
    """Root mean squared error, in cycles.

    Args:
        y_true: True RUL values.
        y_pred: Predicted RUL values (same length).

    Returns:
        The RMSE.

    Raises:
        ValueError: If the inputs have different lengths or are empty.
    """
    y_true, y_pred = _as_pair(y_true, y_pred)
    return float(np.sqrt(np.mean((y_pred - y_true) ** 2)))


def mae(y_true, y_pred) -> float:
    """Mean absolute error, in cycles.

    Args:
        y_true: True RUL values.
        y_pred: Predicted RUL values (same length).

    Returns:
        The MAE.

    Raises:
        ValueError: If the inputs have different lengths or are empty.
    """
    y_true, y_pred = _as_pair(y_true, y_pred)
    return float(np.mean(np.abs(y_pred - y_true)))


def nasa_score(y_true, y_pred) -> float:
    """Asymmetric scoring function from the PHM08 challenge (lower is better).

    With error ``d = predicted - true``, each prediction contributes
    ``exp(-d/13) - 1`` if ``d < 0`` (predicted too early) and
    ``exp(d/10) - 1`` if ``d >= 0`` (predicted too late). Late predictions are
    penalised more heavily, because an engine predicted to last longer than it
    does is the dangerous case. The score grows exponentially with error, so
    a few large mistakes dominate it.

    Args:
        y_true: True RUL values.
        y_pred: Predicted RUL values (same length).

    Returns:
        The summed score.

    Raises:
        ValueError: If the inputs have different lengths or are empty.
    """
    y_true, y_pred = _as_pair(y_true, y_pred)
    d = y_pred - y_true
    return float(np.sum(np.where(d < 0, np.exp(-d / 13.0) - 1, np.exp(d / 10.0) - 1)))


def _as_pair(y_true, y_pred) -> tuple[np.ndarray, np.ndarray]:
    """Convert inputs to float arrays and check they are comparable."""
    a = np.asarray(y_true, dtype=float).ravel()
    b = np.asarray(y_pred, dtype=float).ravel()
    if a.shape != b.shape:
        raise ValueError(f"Length mismatch: {a.shape[0]} vs {b.shape[0]}.")
    if a.size == 0:
        raise ValueError("Inputs must not be empty.")
    return a, b


def grouped_splits(groups, n_splits: int = 5) -> Iterator[tuple[np.ndarray, np.ndarray]]:
    """Yield (train_index, validation_index) pairs, split by group.

    Args:
        groups: Group label for each row (here, the engine ID).
        n_splits: Number of folds.

    Yields:
        Pairs of integer index arrays. No group appears in both arrays of a
        pair, and every group is in exactly one validation set.

    Raises:
        ValueError: If there are fewer distinct groups than ``n_splits``.
    """
    groups = np.asarray(groups)
    if len(np.unique(groups)) < n_splits:
        raise ValueError("Need at least as many engines as folds.")
    dummy = np.zeros(len(groups))
    yield from GroupKFold(n_splits=n_splits).split(dummy, dummy, groups)


def cross_validate(
    model_factory: Callable[[], object],
    train: pd.DataFrame,
    feature_cols: list[str],
    cap: int | None = 125,
    n_splits: int = 5,
    eval_cap: int | None | str = "same",
) -> pd.DataFrame:
    """Grouped cross-validation of one model on the training engines.

    A fresh model is built for every fold (so nothing leaks between folds).
    Training labels are capped at ``cap``. By default the validation targets
    use the same cap, so the model is judged against the label definition it
    learned. To compare *different* caps fairly, pass the same ``eval_cap`` to
    every run: errors measured against different targets are not comparable.
    Fitting and prediction times are recorded for each fold.

    Args:
        model_factory: Zero-argument function returning an unfitted
            scikit-learn-style model (``fit`` / ``predict``). Preprocessing
            such as scaling should live inside it (e.g. a Pipeline) so it is
            fitted on the training part of each fold only.
        train: Training table with ``engine``, ``RUL`` and the feature columns
            (see :func:`src.data_loader.add_rul`).
        feature_cols: Columns used as model inputs.
        cap: Upper limit applied to RUL, or ``None`` for no cap.
        n_splits: Number of folds.
        eval_cap: Cap applied to the validation targets. ``"same"`` (default)
            uses ``cap``; ``None`` means no cap (true RUL); an integer uses
            that cap.

    Returns:
        One row per fold with columns ``fold``, ``rmse``, ``mae``,
        ``nasa_score``, ``fit_s`` and ``predict_s``.

    Raises:
        ValueError: If ``train`` lacks ``RUL``/``engine`` or any feature column.
    """
    needed = ["engine", "RUL"] + list(feature_cols)
    missing = [c for c in needed if c not in train.columns]
    if missing:
        raise ValueError(f"train is missing required columns: {missing}")

    X = train[feature_cols].to_numpy()
    y_raw = train["RUL"].to_numpy(dtype=float)
    y = y_raw if cap is None else np.minimum(y_raw, cap)
    val_cap = cap if isinstance(eval_cap, str) and eval_cap == "same" else eval_cap
    y_eval = y_raw if val_cap is None else np.minimum(y_raw, val_cap)

    rows = []
    for fold, (tr, va) in enumerate(grouped_splits(train["engine"], n_splits)):
        model = model_factory()
        t0 = time.perf_counter()
        model.fit(X[tr], y[tr])
        t1 = time.perf_counter()
        pred = model.predict(X[va])
        t2 = time.perf_counter()
        rows.append({
            "fold": fold,
            "rmse": rmse(y_eval[va], pred),
            "mae": mae(y_eval[va], pred),
            "nasa_score": nasa_score(y_eval[va], pred),
            "fit_s": t1 - t0,
            "predict_s": t2 - t1,
        })
    return pd.DataFrame(rows)
