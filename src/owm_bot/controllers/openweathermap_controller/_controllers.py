import typing as t
from pathlib import Path
import logging
from contextlib import AbstractContextManager

log = logging.getLogger("owm_bot.controllers.openweathermap_controller")

from owm_bot.core import settings, owm_settings
from owm_bot.core import (
    DATA_DIR,
    PQ_DIR,
    CACHE_DIR,
    ENSURE_DIRS,
    OWM_HTTP_CACHE_DIR,
    HTTP_CACHE_DIR,
)
from owm_bot.core.depends import (
    hishel_filestorage_dependency,
    owm_hishel_filestorage_dependency,
)
from owm_bot.location import (
    LocationsPQFileController,
    LocationsJSONFileController,
)
from owm_bot.weather import (
    CurrentWeatherPQFileController,
    ForecastWeatherPQFileController,
)
from owm_bot.domain.Location import JsonLocation, JsonLocationsLoader
from owm_bot.utils.encoders import DecimalJsonEncoder
from owm_bot.location import (
    load_location_from_file,
    init_location,
    save_location_dict_to_file,
    update_location_coords,
)
from owm_bot.weather import get_current_weather

import hishel
import httpx


class OpenWeathermapController(AbstractContextManager):
    def __init__(
        self,
        location_file: t.Union[str, Path] = owm_settings.location_file,
        api_key: str = owm_settings.api_key,
        # location: JsonLocation = None,
        cache_storage: (
            t.Union[hishel.FileStorage, hishel.InMemoryStorage, hishel.SQLiteStorage]
            | None
        ) = None,
        cache_ttl: int = 900,
        force_cache: bool = True,
        debug_http_response: bool = False,
    ):
        self.location_file: str | Path = location_file
        self.api_key: str = api_key
        if cache_storage is None:
            cache_storage = owm_hishel_filestorage_dependency(ttl=cache_ttl)
        self.cache_storage: t.Union[
            hishel.FileStorage, hishel.InMemoryStorage, hishel.SQLiteStorage
        ] = cache_storage
        self.force_cache: bool = force_cache
        self.debug_http_response: bool = debug_http_response

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

    def current_weather(self):
        current_weather = get_current_weather(
            location_obj=self.location,
            cache_storage=self.cache_storage,
            debug_http_response=self.debug_http_response,
        )

        return current_weather

    def weather_forecast(self):
        pass
