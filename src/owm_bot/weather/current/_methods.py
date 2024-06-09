import typing as t
import logging

log = logging.getLogger("owm_bot.weather.current")

from owm_bot.core import settings, owm_settings
from owm_bot.core.paths import DATA_DIR, CACHE_DIR, HTTP_CACHE_DIR, OWM_HTTP_CACHE_DIR
from owm_bot.core.constants import (
    PQ_ENGINE,
    OPENWEATHERMAP_BASE_URL,
    OPENWEATHERMAP_CURRENT_WEATHER_URL,
    OPENWEATHERMAP_DAILY_FORECAST_WEATHER_URL,
)
from owm_bot.core.depends import (
    owm_hishel_filestorage_dependency,
    hishel_filestorage_dependency,
)
from owm_bot.domain.Location import JsonLocation

from owm_bot.domain.Weather import OWMCurrentWeather

from red_utils.ext import httpx_utils
import httpx
import hishel


def current_weather(
    location: JsonLocation = None,
    api_key: str = owm_settings.api_key,
    cache_storage: (
        t.Union[hishel.FileStorage, hishel.InMemoryStorage, hishel.SQLiteStorage] | None
    ) = None,
    cache_ttl: int = 900,
    force_cache: bool = True,
) -> OWMCurrentWeather:
    if cache_storage is None:
        cache_storage = owm_hishel_filestorage_dependency(ttl=cache_ttl)

    params: dict = {"lat": location.lat, "lon": location.lon, "appid": api_key}

    with httpx_utils.HishelCacheClientController(
        force_cache=force_cache, storage=cache_storage
    ) as http_ctl:
        req: httpx.Request = http_ctl.new_request(
            url=OPENWEATHERMAP_CURRENT_WEATHER_URL, params=params
        )

        try:
            res: httpx.Response = http_ctl.send_request(request=req)
        except Exception as exc:
            msg = Exception(
                f"Unhandled exception requesting current weather. Details: {exc}"
            )
            log.error(msg)

            raise exc

    if not res.status_code == 200:
        log.warning(
            f"Non-200 response requesting current weather. [{res.status_code}: {res.reason_phrase}]: {res.text}"
        )

        return None

    try:
        current_weather_dict = http_ctl.decode_res_content(res)
    except Exception as exc:
        msg = Exception(
            f"Unhandled exception decoding response content. Details: {exc}"
        )
        log.error(msg)

        raise exc
    log.debug(f"Current weather dict: {current_weather_dict}")

    try:
        _current_weather: OWMCurrentWeather = OWMCurrentWeather.model_validate(
            current_weather_dict
        )
    except Exception as exc:
        msg = Exception(
            f"Unhandled exception converting current weather dict to OWMCurrentWeather object. Details: {exc}"
        )
        log.error(msg)

        raise exc

    return _current_weather
