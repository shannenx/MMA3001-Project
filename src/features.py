"""Feature selection and row-selection helpers for FD001.

These functions turn the loaded tables into model inputs. The default choices
(which columns to drop) come from the exploratory analysis in
``notebooks/01_exploration.ipynb``; change them there first, then here.
"""

from __future__ import annotations

import pandas as pd

from src.data_loader import SENSOR_COLUMNS, SETTING_COLUMNS

#: Sensors constant (or nearly constant) in the FD001 training data.
#: sensor_6 takes only two values and has a weak relationship with RUL.
DROPPED_SENSORS = [
    "sensor_1", "sensor_5", "sensor_6", "sensor_10",
    "sensor_16", "sensor_18", "sensor_19",
]


def get_feature_columns(
    drop_sensors: list[str] | None = None,
    include_settings: bool = False,
) -> list[str]:
    """Return the list of model input columns.

    Args:
        drop_sensors: Sensor columns to exclude. ``None`` uses
            :data:`DROPPED_SENSORS`. Pass a longer list to test removing
            further sensors (for example ``DROPPED_SENSORS + ["sensor_9",
            "sensor_14"]``).
        include_settings: If True, also include the three operational
            settings. In FD001 they carry no useful information (single
            operating condition), so the default is False.

    Returns:
        Column names in file order.

    Raises:
        ValueError: If ``drop_sensors`` contains a name that is not a sensor
            column (guards against typos silently dropping nothing).
    """
    drop = DROPPED_SENSORS if drop_sensors is None else list(drop_sensors)
    unknown = [c for c in drop if c not in SENSOR_COLUMNS]
    if unknown:
        raise ValueError(f"Unknown sensor columns: {unknown}")
    cols = [c for c in SENSOR_COLUMNS if c not in drop]
    if include_settings:
        cols = SETTING_COLUMNS + cols
    return cols


def last_rows(df: pd.DataFrame) -> pd.DataFrame:
    """Return each engine's final recorded cycle, one row per engine.

    This is the row used to predict an engine's RUL at the end of its
    (truncated) test record. Rows are ordered by engine ID, so row ``i``
    lines up with row ``i`` of the ``RUL_FD001`` table when engine IDs run
    1..N.

    Args:
        df: Table with ``engine`` and ``cycle`` columns.

    Returns:
        One row per engine, sorted by engine, with a fresh index.

    Raises:
        ValueError: If ``engine`` or ``cycle`` is missing.
    """
    missing = [c for c in ("engine", "cycle") if c not in df.columns]
    if missing:
        raise ValueError(f"df is missing required columns: {missing}")
    idx = df.groupby("engine")["cycle"].idxmax()
    return df.loc[idx].sort_values("engine").reset_index(drop=True)
