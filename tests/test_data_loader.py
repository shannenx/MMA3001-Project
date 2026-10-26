"""Tests for src.data_loader.

Two groups:
* Checks on the real FD001 files (skipped if the data folder is missing).
* Checks on tiny synthetic files, to confirm bad input is rejected.
"""

import numpy as np
import pandas as pd
import pytest

from src.data_loader import (
    COLUMN_NAMES,
    DEFAULT_DATA_DIR,
    SENSOR_COLUMNS,
    SETTING_COLUMNS,
    add_rul,
    load_fd001,
)

# ---------------------------------------------------------------- real data

needs_data = pytest.mark.skipif(
    not (DEFAULT_DATA_DIR / "train_FD001.txt").is_file(),
    reason="FD001 data files not found in data/ (see data/README.md)",
)


@pytest.fixture(scope="module")
def real_data():
    return load_fd001()


@needs_data
def test_real_shapes(real_data):
    train, test, rul = real_data
    assert train.shape == (20631, 26)
    assert test.shape == (13096, 26)
    assert rul.shape == (100, 1)


@needs_data
def test_real_engine_counts(real_data):
    train, test, rul = real_data
    assert train["engine"].nunique() == 100
    assert test["engine"].nunique() == 100
    assert sorted(test["engine"].unique()) == list(range(1, 101))


@needs_data
def test_real_column_names(real_data):
    train, _, _ = real_data
    assert list(train.columns) == COLUMN_NAMES


@needs_data
def test_real_no_missing_values(real_data):
    for df in real_data:
        assert not df.isna().any().any()


@needs_data
def test_real_rul_range(real_data):
    _, _, rul = real_data
    assert rul["RUL"].min() == 7
    assert rul["RUL"].max() == 145


@needs_data
def test_real_constant_columns_in_training(real_data):
    train, _, _ = real_data
    constant = [c for c in SETTING_COLUMNS + SENSOR_COLUMNS if train[c].nunique() == 1]
    assert constant == [
        "setting_3", "sensor_1", "sensor_5", "sensor_10",
        "sensor_16", "sensor_18", "sensor_19",
    ]


@needs_data
def test_real_training_lifetimes(real_data):
    train, _, _ = real_data
    lifetimes = train.groupby("engine")["cycle"].max()
    assert lifetimes.min() == 128
    assert lifetimes.max() == 362


# ------------------------------------------------------------ synthetic data

def _write_rows(path, rows):
    """Write rows (lists of numbers) as a space-separated text file."""
    path.write_text("\n".join(" ".join(str(v) for v in r) for r in rows) + "\n")


def _engine_rows(engine, n_cycles):
    return [[engine, c] + [0.5] * 24 for c in range(1, n_cycles + 1)]


@pytest.fixture
def tiny_dir(tmp_path):
    """A valid miniature dataset: 2 train engines, 2 test engines."""
    _write_rows(tmp_path / "train_FD001.txt", _engine_rows(1, 4) + _engine_rows(2, 3))
    _write_rows(tmp_path / "test_FD001.txt", _engine_rows(1, 2) + _engine_rows(2, 3))
    _write_rows(tmp_path / "RUL_FD001.txt", [[10], [20]])
    return tmp_path


def test_tiny_dataset_loads(tiny_dir):
    train, test, rul = load_fd001(tiny_dir)
    assert len(train) == 7 and len(test) == 5 and len(rul) == 2


def test_missing_file_raises(tiny_dir):
    (tiny_dir / "RUL_FD001.txt").unlink()
    with pytest.raises(FileNotFoundError):
        load_fd001(tiny_dir)


def test_wrong_column_count_raises(tiny_dir):
    _write_rows(tiny_dir / "train_FD001.txt", [[1, 1, 0.5, 0.5]])
    with pytest.raises(ValueError, match="columns"):
        load_fd001(tiny_dir)


def test_missing_value_raises(tiny_dir):
    rows = _engine_rows(1, 3)
    rows[1][5] = np.nan
    _write_rows(tiny_dir / "train_FD001.txt", rows)
    with pytest.raises(ValueError, match="missing"):
        load_fd001(tiny_dir)


def test_non_consecutive_cycles_raise(tiny_dir):
    rows = _engine_rows(1, 3)
    rows[2][1] = 5  # cycles 1, 2, 5
    _write_rows(tiny_dir / "train_FD001.txt", rows)
    with pytest.raises(ValueError, match="cycles"):
        load_fd001(tiny_dir)


def test_rul_length_mismatch_raises(tiny_dir):
    _write_rows(tiny_dir / "RUL_FD001.txt", [[10]])
    with pytest.raises(ValueError, match="RUL"):
        load_fd001(tiny_dir)


def test_negative_rul_raises(tiny_dir):
    _write_rows(tiny_dir / "RUL_FD001.txt", [[10], [-1]])
    with pytest.raises(ValueError, match="negative"):
        load_fd001(tiny_dir)


# ------------------------------------------------------------------ add_rul

def test_add_rul_values(tiny_dir):
    train, _, _ = load_fd001(tiny_dir)
    labelled = add_rul(train)
    # Engine 1 has 4 cycles -> RUL 3, 2, 1, 0; engine 2 has 3 -> 2, 1, 0.
    assert labelled.loc[labelled["engine"] == 1, "RUL"].tolist() == [3, 2, 1, 0]
    assert labelled.loc[labelled["engine"] == 2, "RUL"].tolist() == [2, 1, 0]


def test_add_rul_cap(tiny_dir):
    train, _, _ = load_fd001(tiny_dir)
    labelled = add_rul(train, cap=2)
    assert labelled["RUL"].max() == 2


def test_add_rul_does_not_modify_input(tiny_dir):
    train, _, _ = load_fd001(tiny_dir)
    add_rul(train)
    assert "RUL" not in train.columns


def test_add_rul_bad_cap_raises(tiny_dir):
    train, _, _ = load_fd001(tiny_dir)
    with pytest.raises(ValueError, match="cap"):
        add_rul(train, cap=0)


def test_add_rul_missing_columns_raises():
    with pytest.raises(ValueError, match="missing"):
        add_rul(pd.DataFrame({"engine": [1, 1]}))
