import typing as t
import logging
from pathlib import Path

from owm_bot.domain.Weather.current.schemas import OWMCurrentWeather
from owm_bot.domain.Weather.forecast.schemas import OWMForecastWeather

log = logging.getLogger("owm_bot.weather.methods")

from owm_bot.core.paths import LOCATIONS_PQ_FILE
from owm_bot.domain.Location import JsonLocation, JsonLocationsLoader, OwmGeoLookup
from owm_bot.core.config import owm_settings
from owm_bot.core.depends import owm_hishel_filestorage_dependency
from owm_bot.utils import data_utils
from owm_bot.utils.owm_utils import handle_missing_coords
from .current import current_weather
from .forecast import weather_forecast

import hishel
import httpx
import pandas as pd


def get_current_weather(
    api_key: str = owm_settings.api_key,
    location_obj: JsonLocation = None,
    units: str = "standard",
    cache_storage: (
        t.Union[hishel.FileStorage, hishel.SQLiteStorage, hishel.InMemoryStorage] | None
    ) = None,
    debug_http_response: bool = False,
) -> OWMCurrentWeather:
    if cache_storage is None:
        cache_storage = owm_hishel_filestorage_dependency()

    if location_obj.lat is None or location_obj.lon is None:
        location_obj = handle_missing_coords(location_obj=location_obj)

    try:
        _current_weather: OWMCurrentWeather = current_weather(
            api_key=api_key, location=location_obj, units=units
        )
    except Exception as exc:
        msg = Exception(f"Unhandled exception getting current weather. Details: {exc}")
        log.error(msg)

        raise exc

    return _current_weather


def get_forecast_weather(
    api_key: str = owm_settings.api_key,
    location_obj: JsonLocation = None,
    units: str = "standard",
    days: int = 16,
    cache_storage: (
        t.Union[hishel.FileStorage, hishel.SQLiteStorage, hishel.InMemoryStorage] | None
    ) = None,
    debug_http_response: bool = False,
) -> OWMForecastWeather:
    if cache_storage is None:
        cache_storage = owm_hishel_filestorage_dependency()

    if location_obj.lat is None or location_obj.lon is None:
        location_obj = handle_missing_coords(location_obj=location_obj)

    try:
        _weather_forecast: OWMForecastWeather = weather_forecast(
            api_key=api_key, location=location_obj, units=units, days=days
        )
    except Exception as exc:
        msg = Exception(f"Unhandled exception getting weather forecast. Details: {exc}")
        log.error(msg)

        raise exc

    return _weather_forecast
