"""Load and validate the NASA C-MAPSS FD001 turbofan dataset.

The FD001 subset contains simulated run-to-failure data for a fleet of 100
turbofan engines (one operating condition, one fault mode: HPC degradation).

Each raw file is plain text, space-separated, with no header and 26 columns:
engine ID, cycle number, 3 operational settings and 21 sensor readings.

Data source and citation: see ``data/README.md``.

Typical use::

    from src.data_loader import load_fd001, add_rul

    train, test, rul = load_fd001()
    train = add_rul(train, cap=125)
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

#: Default location of the raw files: the ``data`` folder at the repo root.
DEFAULT_DATA_DIR = Path(__file__).resolve().parents[1] / "data"

INDEX_COLUMNS = ["engine", "cycle"]
SETTING_COLUMNS = [f"setting_{i}" for i in range(1, 4)]
SENSOR_COLUMNS = [f"sensor_{i}" for i in range(1, 22)]
#: Column names, in file order (26 in total).
COLUMN_NAMES = INDEX_COLUMNS + SETTING_COLUMNS + SENSOR_COLUMNS


def _read_table(path: Path, n_columns: int) -> pd.DataFrame:
    """Read one whitespace-separated, header-less numeric text file.

    Args:
        path: Path to the file.
        n_columns: Number of columns the file must contain.

    Returns:
        The file contents with default integer column labels.

    Raises:
        FileNotFoundError: If ``path`` does not exist.
        ValueError: If the file does not have exactly ``n_columns`` columns,
            or contains non-numeric entries.
    """
    if not path.is_file():
        raise FileNotFoundError(
            f"Expected data file not found: {path}. "
            "See data/README.md for where to obtain the FD001 files."
        )
    df = pd.read_csv(path, sep=r"\s+", header=None)
    if df.shape[1] != n_columns:
        raise ValueError(
            f"{path.name}: expected {n_columns} columns, found {df.shape[1]}."
        )
    if not all(pd.api.types.is_numeric_dtype(t) for t in df.dtypes):
        raise ValueError(f"{path.name}: contains non-numeric entries.")
    return df


def _validate_engine_frame(df: pd.DataFrame, name: str) -> pd.DataFrame:
    """Check an engine time-series table and set integer ID/cycle columns.

    Checks that there are no missing values, that engine and cycle values are
    whole numbers, and that each engine's cycles run 1, 2, 3, ... in order.

    Args:
        df: Table with the 26 named columns.
        name: Label used in error messages (e.g. ``"train"``).

    Returns:
        The table with ``engine`` and ``cycle`` converted to integers.

    Raises:
        ValueError: If any check fails.
    """
    if df.isna().any().any():
        raise ValueError(f"{name}: contains missing values.")
    for col in INDEX_COLUMNS:
        if (df[col] % 1 != 0).any():
            raise ValueError(f"{name}: column '{col}' has non-integer values.")
    df = df.astype({"engine": int, "cycle": int})
    position = df.groupby("engine").cumcount() + 1
    if (df["cycle"] != position).any():
        raise ValueError(
            f"{name}: cycles must run 1, 2, 3, ... in order for every engine."
        )
    return df


def load_fd001(
    data_dir: str | Path | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Load the FD001 training set, test set and true test RUL values.

    Args:
        data_dir: Folder containing ``train_FD001.txt``, ``test_FD001.txt`` and
            ``RUL_FD001.txt``. Defaults to the repository's ``data`` folder.

    Returns:
        A tuple ``(train, test, rul)``:

        * ``train``: one row per engine per cycle, run to failure. Columns are
          ``COLUMN_NAMES`` (26 columns). It has no RUL column; see
          :func:`add_rul`.
        * ``test``: same columns, but each engine's record stops before failure.
        * ``rul``: one column ``RUL`` (cycles remaining after the last test
          cycle). Row ``i`` belongs to test engine ``i + 1``.

    Raises:
        FileNotFoundError: If any of the three files is missing.
        ValueError: If a file has the wrong number of columns, contains
            non-numeric or missing values, has cycles that are not consecutive
            from 1, or if the number of RUL values differs from the number of
            test engines, or any RUL value is negative.
    """
    base = Path(data_dir) if data_dir is not None else DEFAULT_DATA_DIR

    train = _read_table(base / "train_FD001.txt", len(COLUMN_NAMES))
    train.columns = COLUMN_NAMES
    train = _validate_engine_frame(train, "train_FD001")

    test = _read_table(base / "test_FD001.txt", len(COLUMN_NAMES))
    test.columns = COLUMN_NAMES
    test = _validate_engine_frame(test, "test_FD001")

    rul = _read_table(base / "RUL_FD001.txt", 1)
    rul.columns = ["RUL"]
    if rul["RUL"].isna().any():
        raise ValueError("RUL_FD001: contains missing values.")
    if (rul["RUL"] < 0).any():
        raise ValueError("RUL_FD001: contains negative values.")
    if len(rul) != test["engine"].nunique():
        raise ValueError(
            f"RUL_FD001 has {len(rul)} values but test set has "
            f"{test['engine'].nunique()} engines."
        )
    return train, test, rul


def add_rul(train: pd.DataFrame, cap: int | None = None) -> pd.DataFrame:
    """Add a remaining-useful-life (RUL) label to the training data.

    For each engine, ``RUL = (engine's last cycle) - (current cycle)``, so it
    is 0 on the failure cycle and counts up backwards through time.

    Args:
        train: Training table with ``engine`` and ``cycle`` columns.
        cap: Optional upper limit on RUL (in cycles). Early in an engine's life
            degradation is not observable, so a cap such as 125 is often used.
            ``None`` means no cap.

    Returns:
        A copy of ``train`` with an extra ``RUL`` column. The input is not
        modified.

    Raises:
        ValueError: If ``engine`` or ``cycle`` is missing, or ``cap`` is not
            positive.
    """
    missing = [c for c in INDEX_COLUMNS if c not in train.columns]
    if missing:
        raise ValueError(f"train is missing required columns: {missing}")
    if cap is not None and cap <= 0:
        raise ValueError("cap must be positive.")

    out = train.copy()
    last_cycle = out.groupby("engine")["cycle"].transform("max")
    out["RUL"] = last_cycle - out["cycle"]
    if cap is not None:
        out["RUL"] = out["RUL"].clip(upper=cap)
    return out
