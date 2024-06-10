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
    OWM_HTTP_CACHE_DIR,
    PQ_DIR,
    owm_settings,
    settings,
)
from owm_bot.core.depends import (
    hishel_filestorage_dependency,
    owm_hishel_filestorage_dependency,
)
from owm_bot.domain.Location import JsonLocation, JsonLocationsLoader
from owm_bot.location import (
    LocationJSONFileController,
    LocationPQFileController,
    init_location,
    load_location_from_file,
    save_location_dict_to_file,
    update_location_coords,
)
from owm_bot.utils.encoders import DecimalJsonEncoder
from owm_bot.weather import (
    CurrentWeatherPQFileController,
    ForecastWeatherPQFileController,
    get_current_weather,
    get_forecast_weather,
)

from .__methods import (
    update_current_weather_parqeut_file,
    update_weather_forecast_parquet_file,
)

import hishel
import httpx


class OpenWeathermapController(AbstractContextManager):
    def __init__(
        self,
        location_file: t.Union[str, Path] = owm_settings.location_file,
        units: str = owm_settings.units,
        forecast_days: int = 16,
        api_key: str = owm_settings.api_key,
        # location: JsonLocation = None,
        cache_storage: (
            t.Union[hishel.FileStorage, hishel.InMemoryStorage, hishel.SQLiteStorage]
            | None
        ) = None,
        cache_ttl: int = 900,
        force_cache: bool = True,
        debug_http_response: bool = False,
        current_weather_pq_file: t.Union[str, Path] = CURRENT_WEATHER_PQ_FILE,
        weather_forecast_pq_file: t.Union[str, Path] = FORECAST_WEATHER_PQ_FILE,
    ) -> None:
        self.location_file: str | Path = location_file
        self.api_key: str = api_key
        self.units: str = units.lower()
        self.forecast_days: int = forecast_days
        if cache_storage is None:
            cache_storage = owm_hishel_filestorage_dependency(ttl=cache_ttl)
        self.cache_storage: t.Union[
            hishel.FileStorage, hishel.InMemoryStorage, hishel.SQLiteStorage
        ] = cache_storage
        self.force_cache: bool = force_cache
        self.debug_http_response: bool = debug_http_response
        self.current_weather_pq_file: Path = Path(f"{current_weather_pq_file}")
        self.weather_forecast_pq_file: Path = Path(f"{weather_forecast_pq_file}")

        self.location: JsonLocation | None = None

    def __enter__(self):
        _location: JsonLocation = init_location(
            cache_storage=self.cache_storage,
            debug_http_response=self.debug_http_response,
        )
        log.debug(f"Location: {_location}")
        self.location: JsonLocation = _location

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_value:
            log.error(f"({exc_type}): {exc_value}")

        if traceback:
            raise traceback

    def current_weather(self, save_pq: bool = False) -> OWMCurrentWeather:
        try:
            _current_weather: OWMCurrentWeather = get_current_weather(
                api_key=self.api_key,
                location_obj=self.location,
                units=self.units,
                cache_storage=self.cache_storage,
                debug_http_response=self.debug_http_response,
            )

        except Exception as exc:
            msg = Exception(
                f"Unhandled exception getting current weather. Details: {exc}"
            )
            log.error(msg)

            raise exc

        if save_pq:
            log.info(f"Saving current weather to file '{self.current_weather_pq_file}'")

            try:
                update_current_weather_parqeut_file(
                    new_data=_current_weather.model_dump(),
                    pq_file=self.current_weather_pq_file,
                )
            except Exception as exc:
                msg = Exception(
                    f"Unhandled exception updating current weather history file '{self.current_weather_pq_file}.' Details: {exc}"
                )
                log.error(msg)

                pass

        return _current_weather

    def weather_forecast(self, save_pq: bool = False) -> OWMForecastWeather:
        try:
            _weather_forecast: OWMForecastWeather = get_forecast_weather(
                api_key=self.api_key,
                location_obj=self.location,
                units=self.units,
                days=self.forecast_days,
                cache_storage=self.cache_storage,
                debug_http_response=self.debug_http_response,
            )

        except Exception as exc:
            msg = Exception(
                f"Unhandled exception getting weather forecast. Details: {exc}"
            )
            log.error(msg)

            raise exc

        if save_pq:
            log.info(
                f"Saving weather forecast to file '{self.weather_forecast_pq_file}'"
            )

            try:
                update_current_weather_parqeut_file(
                    new_data=_weather_forecast.model_dump(),
                    pq_file=self.weather_forecast_pq_file,
                )
            except Exception as exc:
                msg = Exception(
                    f"Unhandled exception updating weather forecast history file '{self.weather_forecast_pq_file}.' Details: {exc}"
                )
                log.error(msg)

                pass

        return _weather_forecast
