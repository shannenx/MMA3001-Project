"""Tests for src.windows."""

import numpy as np
import pandas as pd
import pytest

from src.windows import (
    DEFAULT_STATS,
    feature_names,
    last_window_rows,
    window_table,
)


def _fleet():
    """Two engines. Sensor 'a' = 2 * cycle for engine 1 (5 cycles) and
    a constant 100 for engine 2 (4 cycles). 'b' is a second sensor."""
    rows = []
    for c in range(1, 6):
        rows.append({"engine": 1, "cycle": c, "a": 2.0 * c, "b": 10.0, "RUL": 5 - c})
    for c in range(1, 5):
        rows.append({"engine": 2, "cycle": c, "a": 100.0, "b": float(c), "RUL": 4 - c})
    return pd.DataFrame(rows)


COLS = ["a", "b"]


def test_known_values_for_one_window():
    out = window_table(_fleet(), COLS, window=3, stats=("last", "mean", "std", "slope"))
    row = out[(out.engine == 1) & (out.cycle == 5)].iloc[0]  # window = cycles 3,4,5 -> a = 6, 8, 10
    assert row["a__last"] == pytest.approx(10.0)
    assert row["a__mean"] == pytest.approx(8.0)
    assert row["a__std"] == pytest.approx(np.sqrt(8 / 3))
    assert row["a__slope"] == pytest.approx(2.0)      # 2 units per cycle
    assert row["b__slope"] == pytest.approx(0.0)      # constant sensor
    assert row["b__std"] == pytest.approx(0.0)


def test_only_complete_windows_are_kept():
    out = window_table(_fleet(), COLS, window=3)
    assert out[out.engine == 1]["cycle"].tolist() == [3, 4, 5]
    assert out[out.engine == 2]["cycle"].tolist() == [3, 4]


def test_engine_shorter_than_window_contributes_no_rows():
    out = window_table(_fleet(), COLS, window=5)
    assert set(out["engine"]) == {1}


def test_windows_do_not_cross_engine_boundaries():
    out = window_table(_fleet(), COLS, window=3, stats=("mean",))
    # Engine 2's first window uses only engine 2's values (a is always 100),
    # not the tail of engine 1.
    first = out[(out.engine == 2) & (out.cycle == 3)].iloc[0]
    assert first["a__mean"] == pytest.approx(100.0)


def test_no_lookahead():
    df = _fleet()
    before = window_table(df, COLS, window=3)
    changed = df.copy()
    changed.loc[(changed.engine == 1) & (changed.cycle == 5), "a"] = 9999.0
    after = window_table(changed, COLS, window=3)
    unaffected = before["cycle"] < 5
    pd.testing.assert_frame_equal(
        before[(before.engine == 1) & unaffected].reset_index(drop=True),
        after[(after.engine == 1) & unaffected].reset_index(drop=True),
    )


def test_rul_is_taken_from_the_end_of_the_window():
    out = window_table(_fleet(), COLS, window=3)
    row = out[(out.engine == 1) & (out.cycle == 3)].iloc[0]
    assert row["RUL"] == 2


def test_window_of_one_matches_original_values():
    df = _fleet()
    out = window_table(df, COLS, window=1, stats=("last", "std", "slope"))
    assert len(out) == len(df)
    assert out["a__last"].tolist() == df["a"].tolist()
    assert (out["a__slope"] == 0).all() and (out["a__std"] == 0).all()


def test_feature_names_and_column_order():
    assert feature_names(COLS, ("last", "slope")) == ["a__last", "b__last", "a__slope", "b__slope"]
    out = window_table(_fleet(), COLS, window=2, stats=("last", "slope"))
    assert list(out.columns) == ["engine", "cycle", "RUL", "a__last", "b__last", "a__slope", "b__slope"]


def test_works_without_rul_column():
    out = window_table(_fleet().drop(columns="RUL"), COLS, window=2)
    assert "RUL" not in out.columns


def test_unsorted_input_gives_same_result():
    df = _fleet()
    shuffled = df.sample(frac=1, random_state=0)
    pd.testing.assert_frame_equal(
        window_table(df, COLS, window=3),
        window_table(shuffled, COLS, window=3),
    )


# ------------------------------------------------------- last_window_rows

def test_last_window_rows_one_per_engine():
    out = last_window_rows(_fleet(), COLS, window=3)
    assert out["engine"].tolist() == [1, 2]
    assert out["cycle"].tolist() == [5, 4]


def test_last_window_rows_short_engine_raises():
    with pytest.raises(ValueError, match="fewer than 5 cycles"):
        last_window_rows(_fleet(), COLS, window=5)  # engine 2 has only 4 cycles


# ------------------------------------------------------------ bad arguments

@pytest.mark.parametrize("window", [0, -3, 2.5])
def test_bad_window_raises(window):
    with pytest.raises(ValueError, match="window"):
        window_table(_fleet(), COLS, window=window)


def test_bad_stat_raises():
    with pytest.raises(ValueError, match="stats"):
        window_table(_fleet(), COLS, window=3, stats=("median",))


def test_empty_stats_raises():
    with pytest.raises(ValueError, match="stats"):
        window_table(_fleet(), COLS, window=3, stats=())


def test_missing_column_raises():
    with pytest.raises(ValueError, match="missing"):
        window_table(_fleet(), ["a", "nope"], window=3)


def test_default_stats_are_valid():
    assert set(DEFAULT_STATS) <= {"last", "mean", "std", "slope"}


def test_last_window_rows_matches_the_full_table_approach():
    """The fast path must give exactly what 'build every window, keep the last' gives."""
    rng = np.random.default_rng(0)
    rows = []
    for eng, n in [(1, 12), (2, 7), (3, 20)]:
        for c in range(1, n + 1):
            rows.append({"engine": eng, "cycle": c, "a": rng.normal(), "b": rng.normal(), "RUL": n - c})
    df = pd.DataFrame(rows)
    for window in (1, 3, 7):
        full = window_table(df, COLS, window, stats=("last", "mean", "std", "slope"))
        expected = (full.loc[full.groupby("engine")["cycle"].idxmax()]
                    .sort_values("engine").reset_index(drop=True))
        got = last_window_rows(df, COLS, window, stats=("last", "mean", "std", "slope"))
        pd.testing.assert_frame_equal(got, expected)
