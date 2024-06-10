from __future__ import annotations

from contextlib import AbstractContextManager
import logging
from pathlib import Path
import typing as t

from owm_bot.domain.Weather import OWMCurrentWeather, OWMForecastWeather

log = logging.getLogger("owm_bot.controllers.openweathermap_controller")

from owm_bot.core import (
    CACHE_DIR,
    CURRENT_WEATHER_PQ_FILE,
    DATA_DIR,
    ENSURE_DIRS,
    FORECAST_WEATHER_PQ_FILE,
    HTTP_CACHE_DIR,
    LOCATION_PQ_FILE,
    OWM_HTTP_CACHE_DIR,
    PQ_DIR,
    owm_settings,
    settings,
)
from owm_bot.location import LocationJSONFileController, LocationPQFileController
from owm_bot.weather import (
    CurrentWeatherPQFileController,
    ForecastWeatherPQFileController,
)

import pandas as pd

def update_locations_json_file(location_file: t.Union[str, Path] = LOCATION_PQ_FILE):
    raise NotImplementedError("Updating location .json file not yet supported")


def update_locations_parquet_file(
    location_pq_file: t.Union[str, Path] = LOCATION_PQ_FILE
):
    raise NotImplementedError("Updating location .parquet file not yet supported")


def update_current_weather_parqeut_file(
    new_data: t.Union[pd.DataFrame, dict, list[pd.DataFrame], list[dict]],
    pq_file: t.Union[str, Path] = CURRENT_WEATHER_PQ_FILE,
):
    with CurrentWeatherPQFileController(
        current_weather_pq_file=pq_file
    ) as current_weather_pq_ctl:
        try:
            current_weather_pq_ctl.update_df(new_data=new_data)
        except Exception as exc:
            msg = Exception(
                f"Unhandled exception updating current weather Parquet file. Details: {exc}"
            )
            log.error(msg)

            raise exc


def update_weather_forecast_parquet_file(
    new_data: t.Union[pd.DataFrame, dict, list[pd.DataFrame], list[dict]],
    pq_file: t.Union[str, Path] = FORECAST_WEATHER_PQ_FILE,
):
    with ForecastWeatherPQFileController(
        forecast_weather_pq_file=pq_file
    ) as forecast_weather_pq_ctl:
        try:
            forecast_weather_pq_ctl.update_df(new_data=new_data)
        except Exception as exc:
            msg = Exception(
                f"Unhandled exception updating weather forecast Parquet file. Details: {exc}"
            )
            log.error(msg)

            raise exc
