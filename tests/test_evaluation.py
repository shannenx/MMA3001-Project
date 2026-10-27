"""Tests for src.features, src.evaluation and src.models."""

import numpy as np
import pandas as pd
import pytest

from src.data_loader import SENSOR_COLUMNS, SETTING_COLUMNS, add_rul
from src.evaluation import (
    cross_validate,
    out_of_fold_predictions,
    grouped_splits,
    mae,
    nasa_score,
    rmse,
)
from src.features import DROPPED_SENSORS, get_feature_columns, last_rows
from src.models import baseline_models


# ------------------------------------------------------------------ metrics

def test_rmse_known_value():
    # errors 3 and 4 -> sqrt((9 + 16) / 2)
    assert rmse([0, 0], [3, 4]) == pytest.approx(np.sqrt(12.5))


def test_mae_known_value():
    assert mae([0, 0], [3, -4]) == pytest.approx(3.5)


def test_metrics_zero_for_perfect_prediction():
    y = [5, 10, 20]
    assert rmse(y, y) == 0 and mae(y, y) == 0 and nasa_score(y, y) == 0


def test_nasa_score_known_values():
    # Early by 13 cycles: exp(13/13) - 1.  Late by 10 cycles: exp(10/10) - 1.
    assert nasa_score([20], [7]) == pytest.approx(np.e - 1)
    assert nasa_score([20], [30]) == pytest.approx(np.e - 1)


def test_nasa_score_penalises_late_more_than_early():
    assert nasa_score([50], [60]) > nasa_score([50], [40])


@pytest.mark.parametrize("fn", [rmse, mae, nasa_score])
def test_metrics_reject_bad_input(fn):
    with pytest.raises(ValueError):
        fn([1, 2], [1])
    with pytest.raises(ValueError):
        fn([], [])


# --------------------------------------------------------- feature selection

def test_default_features_are_fourteen_sensors():
    cols = get_feature_columns()
    assert len(cols) == 14
    assert not set(cols) & set(DROPPED_SENSORS)
    assert not set(cols) & set(SETTING_COLUMNS)


def test_include_settings_adds_three_columns():
    assert len(get_feature_columns(include_settings=True)) == 17


def test_drop_extra_sensors():
    cols = get_feature_columns(DROPPED_SENSORS + ["sensor_9", "sensor_14"])
    assert len(cols) == 12 and "sensor_9" not in cols


def test_unknown_sensor_name_raises():
    with pytest.raises(ValueError, match="Unknown"):
        get_feature_columns(["sensor_99"])


def test_last_rows_one_per_engine_in_order():
    df = pd.DataFrame({
        "engine": [2, 1, 1, 2, 2],
        "cycle": [1, 1, 2, 2, 3],
        "value": [10, 20, 30, 40, 50],
    })
    out = last_rows(df)
    assert out["engine"].tolist() == [1, 2]
    assert out["cycle"].tolist() == [2, 3]
    assert out["value"].tolist() == [30, 50]


def test_last_rows_missing_columns_raises():
    with pytest.raises(ValueError, match="missing"):
        last_rows(pd.DataFrame({"engine": [1]}))


# ---------------------------------------------------- grouped cross-validation

def _synthetic_train(n_engines=10, n_cycles=30, seed=0):
    """Fake fleet where one sensor falls linearly toward failure."""
    rng = np.random.default_rng(seed)
    rows = []
    for e in range(1, n_engines + 1):
        for c in range(1, n_cycles + 1):
            row = {"engine": e, "cycle": c}
            row.update({s: rng.normal(size=1)[0] for s in SENSOR_COLUMNS})
            row["sensor_2"] = -c + rng.normal(scale=0.1)
            rows.append(row)
    return add_rul(pd.DataFrame(rows))


def test_grouped_splits_never_share_engines():
    groups = np.repeat(np.arange(1, 11), 5)
    seen_validation = []
    for tr, va in grouped_splits(groups, n_splits=5):
        assert not set(groups[tr]) & set(groups[va])
        seen_validation.extend(set(groups[va]))
    assert sorted(seen_validation) == list(range(1, 11))  # each engine once


def test_grouped_splits_too_few_engines_raises():
    with pytest.raises(ValueError):
        list(grouped_splits([1, 1, 2, 2], n_splits=5))


def test_cross_validate_output_columns_and_folds():
    train = _synthetic_train()
    result = cross_validate(
        baseline_models()["ridge"], train, ["sensor_2"], cap=None, n_splits=5
    )
    assert len(result) == 5
    assert {"rmse", "mae", "nasa_score", "fit_s", "predict_s"} <= set(result.columns)


def test_informative_model_beats_mean_baseline():
    train = _synthetic_train()
    models = baseline_models()
    mean_rmse = cross_validate(models["mean"], train, ["sensor_2"], cap=None)["rmse"].mean()
    ridge_rmse = cross_validate(models["ridge"], train, ["sensor_2"], cap=None)["rmse"].mean()
    assert ridge_rmse < 0.2 * mean_rmse


def test_cross_validate_missing_column_raises():
    train = _synthetic_train(n_engines=6)
    with pytest.raises(ValueError, match="missing"):
        cross_validate(baseline_models()["mean"], train, ["not_a_column"])


def test_cap_limits_validation_target():
    # With a cap of 1 every target is <= 1, so a perfect-mean model has tiny error.
    train = _synthetic_train(n_engines=6)
    capped = cross_validate(baseline_models()["mean"], train, ["sensor_2"], cap=1, n_splits=3)
    uncapped = cross_validate(baseline_models()["mean"], train, ["sensor_2"], cap=None, n_splits=3)
    assert capped["rmse"].mean() < uncapped["rmse"].mean()


def test_eval_cap_changes_the_validation_target():
    train = _synthetic_train(n_engines=6)
    m = baseline_models()["mean"]
    same = cross_validate(m, train, ["sensor_2"], cap=5, n_splits=3)["rmse"].mean()
    true_target = cross_validate(m, train, ["sensor_2"], cap=5, n_splits=3, eval_cap=None)["rmse"].mean()
    assert true_target > same  # judged against uncapped RUL, a cap-5 model looks worse


# ----------------------------------------- linear model, training error, OOF

def test_linear_model_is_available_and_recovers_a_line():
    X = np.arange(20, dtype=float).reshape(-1, 1)
    y = 3 * X.ravel() + 2
    model = baseline_models()["linear"]().fit(X, y)
    assert model.predict([[10.0]])[0] == pytest.approx(32.0)


def test_cross_validate_reports_training_error():
    train = _synthetic_train()
    res = cross_validate(baseline_models()["linear"], train, ["sensor_2"], cap=None)
    assert "train_rmse" in res.columns
    assert (res["train_rmse"] >= 0).all()


def test_flexible_model_has_lower_training_than_validation_error():
    # Pure-noise features: a flexible model memorises training rows
    # (low training error) but cannot generalise (high validation error).
    train = _synthetic_train(n_engines=10, n_cycles=40)
    noise_cols = ["sensor_3", "sensor_4", "sensor_7"]
    res = cross_validate(baseline_models()["random_forest"], train, noise_cols, cap=None)
    assert res["train_rmse"].mean() < res["rmse"].mean()


def test_out_of_fold_predictions_cover_every_row_once():
    train = _synthetic_train(n_engines=10, n_cycles=20)
    oof = out_of_fold_predictions(baseline_models()["linear"], train, ["sensor_2"], cap=None)
    assert len(oof) == len(train)
    assert not oof["pred"].isna().any()
    assert np.allclose(oof["error"], oof["pred"] - oof["true"])


def test_out_of_fold_predictions_missing_column_raises():
    train = _synthetic_train(n_engines=6)
    with pytest.raises(ValueError, match="missing"):
        out_of_fold_predictions(baseline_models()["mean"], train, ["nope"])
