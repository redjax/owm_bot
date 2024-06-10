from __future__ import annotations

import json
import logging
from pathlib import Path
import typing as t

log = logging.getLogger("owm_bot.location.controllers")

from contextlib import AbstractContextManager, contextmanager

from owm_bot.core.constants import PQ_ENGINE
from owm_bot.core.paths import (
    CACHE_DIR,
    CURRENT_WEATHER_PQ_FILE,
    DATA_DIR,
    FORECAST_WEATHER_PQ_FILE,
    LOCATION_PQ_FILE,
    PQ_DIR,
    SERIALIZE_DIR,
)
from owm_bot.domain.Location import JsonLocation
from owm_bot.utils import data_utils

import pandas as pd
from red_utils.ext.dataframe_utils import pandas_utils

class LocationPQFileController(AbstractContextManager):
    def __init__(
        self,
        pq_filepath: t.Union[str, Path] = LOCATION_PQ_FILE,
        pq_engine: str = PQ_ENGINE,
    ):
        self.pq_file = pq_filepath
        self.pq_engine = pq_engine

        self.df: pd.DataFrame | None = None

    def __enter__(self):
        if not self.pq_file.exists():
            log.warning(
                f"Locations Parquet file does not exist at path '{self.pq_file}'. Creating empty DataFrame"
            )
            _df = pd.DataFrame()
            self.df = _df

            return self

        try:
            _df = pd.read_parquet(self.pq_file, engine=self.pq_engine)

            self.df = _df
        except Exception as exc:
            msg = Exception(
                f"Unhandled exception loading DataFrame from file '{self.pq_file}'. Details: {exc}"
            )
            log.error(msg)

            raise exc

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_value:
            log.error(f"({exc_type}) {exc_value}")

        if traceback:
            raise traceback

    def rows_to_dict(self, orient: str = "records") -> list[dict]:
        if not self.df:
            raise ValueError("DataFrame is empty or None")

        try:
            dicts: list[dict] = self.df.to_dict(orient="records")
        except Exception as exc:
            msg = Exception(
                f"Unhandled exception converting DataFrame rows to list of dicts. Details: {exc}"
            )
            log.error(msg)

            raise exc

        return dicts


class LocationJSONFileController(AbstractContextManager):
    def __init__(self):
        pass

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        pass
