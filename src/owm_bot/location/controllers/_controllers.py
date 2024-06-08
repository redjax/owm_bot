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
    DATA_DIR,
    PQ_DIR,
    SERIALIZE_DIR,
    CURRENT_WEATHER_PQ_FILE,
    FORECAST_WEATHER_PQ_FILE,
    LOCATIONS_PQ_FILE,
)
from owm_bot.utils import data_utils
from owm_bot.domain.Location import JsonLocation

import pandas as pd
from red_utils.ext.dataframe_utils import pandas_utils


class LocationsPQFileController(AbstractContextManager):
    def __init__(
        self,
        pq_filepath: t.Union[str, Path] = LOCATIONS_PQ_FILE,
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


class LocationsJSONFileController(AbstractContextManager):
    def __init__(self):
        pass

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        pass


class CurrentWeatherPQFileController(AbstractContextManager):
    def __init__(
        self,
        current_weather_pq_file: t.Union[str, Path] = CURRENT_WEATHER_PQ_FILE,
        pq_engine: str = PQ_ENGINE,
    ):
        self.pq_file = current_weather_pq_file
        self.pq_engine = pq_engine

        self.df: pd.DataFrame | None = None

    def __enter__(self):
        if not self.pq_file.exists():
            log.warning(
                f"Current weather Parquet file does not exist at path '{self.pq_file}'. Creating empty DataFrame"
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

    def update_df(
        self,
        new_data: t.Union[pd.DataFrame, dict, list[dict], list[pd.DataFrame]] = None,
        save_pq: bool = True,
    ):
        ## If self.df is None or an empty DataFrame, set to True with if statement below
        EMPTY_INIT_DF: bool = False
        if (isinstance(self.df, pd.DataFrame) and self.df.empty) or self.df is None:
            log.warning(
                f"DataFrame is empty. DataFrame will be initialized with new data."
            )
            EMPTY_INIT_DF: bool = True

        new_data_df: pd.DataFrame = None

        if isinstance(new_data, pd.DataFrame):
            new_data_df = new_data

        elif isinstance(new_data, dict):
            ## Create DataFrame from single dict
            try:
                new_data_df = pd.DataFrame([new_data])
            except Exception as exc:
                msg = Exception(
                    f"Unhandled exception converting dict to DataFrame. Details: {exc}"
                )
                log.error(msg)

                raise exc

        elif isinstance(new_data, list):
            ## Ensure all items are dataframes or dicts
            assert all(isinstance(item, pd.DataFrame) for item in new_data) or all(
                isinstance(item, dict) for item in new_data
            ), TypeError(
                f"Every object in the new_data list must be either a dict or Pandas.DataFrame. At least 1 list object is of a different type."
            )

            ## Assemble dataframe from list
            try:
                new_data_df = pd.DataFrame(new_data)
            except Exception as exc:
                msg = Exception(
                    f"Unhandled exception converting list of dicts or DataFrames to a DataFrame. Details: {exc}"
                )
                log.error(msg)

                raise exc

        if EMPTY_INIT_DF:
            log.debug(
                f"Initial DataFrame was empty. Setting controller DataFrame to new_data"
            )
            self.df = new_data_df
        else:
            ## self.df was not None or empty, update data
            log.info("Updating current weather updates history")
            try:
                updated_df = pd.concat([self.df, new_data_df])
                self.df = updated_df
            except Exception as exc:
                msg = Exception(
                    f"Unhandled exception joining existing current weather DataFrame data with new DataFrame data. Details: {exc}"
                )
                log.error(msg)

                raise exc

        if save_pq:
            log.info(f"Saving DataFrame to file: {self.pq_file}")
            try:
                self.df.to_parquet(self.pq_file, engine=self.pq_engine)
            except Exception as exc:
                msg = Exception(
                    f"Unhandled exception saving DataFrame to file '{self.pq_file}'. Details: {exc}"
                )
                log.error(msg)

                raise exc

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


class ForecastWeatherPQFileController(AbstractContextManager):
    def __init__(
        self,
        forecast_weather_pq_file: t.Union[str, Path] = FORECAST_WEATHER_PQ_FILE,
        pq_engine: str = PQ_ENGINE,
    ):
        self.pq_file = forecast_weather_pq_file
        self.pq_engine = pq_engine

        self.df: pd.DataFrame | None = None

    def __enter__(self):
        if not self.pq_file.exists():
            log.warning(
                f"Weather Forecast Parquet file does not exist at path '{self.pq_file}'. Creating empty DataFrame"
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

    def update_df(
        self,
        new_data: t.Union[pd.DataFrame, dict, list[dict], list[pd.DataFrame]] = None,
        save_pq: bool = True,
    ):
        ## If self.df is None or an empty DataFrame, set to True with if statement below
        EMPTY_INIT_DF: bool = False
        if (isinstance(self.df, pd.DataFrame) and self.df.empty) or self.df is None:
            log.warning(
                f"DataFrame is empty. DataFrame will be initialized with new data."
            )
            EMPTY_INIT_DF: bool = True

        new_data_df: pd.DataFrame = None

        if isinstance(new_data, pd.DataFrame):
            new_data_df = new_data

        elif isinstance(new_data, dict):
            ## Create DataFrame from single dict
            try:
                new_data_df = pd.DataFrame([new_data])
            except Exception as exc:
                msg = Exception(
                    f"Unhandled exception converting dict to DataFrame. Details: {exc}"
                )
                log.error(msg)

                raise exc

        elif isinstance(new_data, list):
            ## Ensure all items are dataframes or dicts
            assert all(isinstance(item, pd.DataFrame) for item in new_data) or all(
                isinstance(item, dict) for item in new_data
            ), TypeError(
                f"Every object in the new_data list must be either a dict or Pandas.DataFrame. At least 1 list object is of a different type."
            )

            ## Assemble dataframe from list
            try:
                new_data_df = pd.DataFrame(new_data)
            except Exception as exc:
                msg = Exception(
                    f"Unhandled exception converting list of dicts or DataFrames to a DataFrame. Details: {exc}"
                )
                log.error(msg)

                raise exc

        if EMPTY_INIT_DF:
            log.debug(
                f"Initial DataFrame was empty. Setting controller DataFrame to new_data"
            )
            self.df = new_data_df
        else:
            ## self.df was not None or empty, update data
            log.info("Updating current weather updates history")
            try:
                updated_df = pd.concat([self.df, new_data_df])
                self.df = updated_df
            except Exception as exc:
                msg = Exception(
                    f"Unhandled exception joining existing current weather DataFrame data with new DataFrame data. Details: {exc}"
                )
                log.error(msg)

                raise exc

        if save_pq:
            log.info(f"Saving DataFrame to file: {self.pq_file}")
            try:
                self.df.to_parquet(self.pq_file, engine=self.pq_engine)
            except Exception as exc:
                msg = Exception(
                    f"Unhandled exception saving DataFrame to file '{self.pq_file}'. Details: {exc}"
                )
                log.error(msg)

                raise exc

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
