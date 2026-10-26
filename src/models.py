"""Baseline regression models for RUL prediction from a single cycle's sensors.

Each entry is a zero-argument *factory* that builds a fresh, unfitted model, so
cross-validation can create a new model for every fold. Models that need
scaled inputs wrap the scaler in a Pipeline so the scaler is fitted on the
training part of each fold only (no leakage from the validation engines).
"""

from __future__ import annotations

from typing import Callable

from sklearn.dummy import DummyRegressor
from sklearn.ensemble import HistGradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

RANDOM_SEED = 0


def baseline_models() -> dict[str, Callable[[], object]]:
    """Return the baseline models as ``{name: factory}``.

    * ``mean``: always predicts the training-set mean RUL. Any useful model
      must beat this.
    * ``ridge``: linear regression with L2 regularisation on standardised
      inputs.
    * ``random_forest``: 100 trees, fixed seed.
    * ``hist_gradient_boosting``: gradient-boosted trees, fixed seed.

    Returns:
        Mapping from model name to a factory function.
    """
    return {
        "mean": lambda: DummyRegressor(strategy="mean"),
        "ridge": lambda: make_pipeline(StandardScaler(), Ridge(alpha=1.0)),
        "random_forest": lambda: RandomForestRegressor(
            n_estimators=100, random_state=RANDOM_SEED, n_jobs=-1
        ),
        "hist_gradient_boosting": lambda: HistGradientBoostingRegressor(
            random_state=RANDOM_SEED
        ),
    }
