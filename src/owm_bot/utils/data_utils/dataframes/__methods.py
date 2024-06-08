from __future__ import annotations

import logging
from pathlib import Path
import typing as t

log = logging.getLogger("owm_bot.utils.data_utils.dataframes")

from owm_bot.core.constants import PQ_ENGINE
from owm_bot.core.paths import PQ_DIR

import pandas as pd
from red_utils.ext.dataframe_utils import pandas_utils


def set_pandas_decimal_precision(precision: int = 2):
    assert precision, ValueError("Missing an integer representing decimal precision")
    assert isinstance(precision, int), TypeError(
        f"precision must be an integer. Got type: ({type(precision)})"
    )

    pd.set_option("display.precision", precision)


def load_locations_json(locations_file: t.Union[str, Path] = None):
    assert locations_file, ValueError("Missing locations_file path")
    locations_file: Path = Path(f"{locations_file}")
    if "~" in f"{locations_file}":
        locations_file = locations_file.expanduser()

    try:
        df: pd.DataFrame = pd.read_json(locations_file)

        return df
    except Exception as exc:
        msg = Exception(
            f"Unhandled exception reading locations into DataFrame from JSON file '{locations_file}'. Details: {exc}"
        )
        log.error(msg)

        raise exc


def save_locations_df_to_pq(
    df: pd.DataFrame = None, pq_file: t.Union[str, Path] = None, dedupe: bool = True
):
    assert pq_file, ValueError("Missing path to .parquet file")

    try:
        pandas_utils.save_pq(df=df, pq_file=pq_file, dedupe=dedupe)
    except Exception as exc:
        msg = Exception(
            f"Unhandled exception saving DataFrame to Parquet file '{pq_file}'. Details: {exc}"
        )
        log.error(msg)

        raise exc
