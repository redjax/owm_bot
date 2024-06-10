from __future__ import annotations

import logging
import typing as t

log = logging.getLogger("owm_bot.location.geolocate")

from owm_bot.core.config import owm_settings
from owm_bot.core.constants import OPENWEATHERMAP_GEO_URL
from owm_bot.core.depends import owm_hishel_filestorage_dependency

import hishel
import httpx
from red_utils.ext import httpx_utils

def get_coords(
    city_name: str | None = None,
    state_code: str | None = None,
    country_code: str | None = None,
    zip_code: str | None = None,
    response_format: str = "json",
    limit: int = 5,
    api_key: str = owm_settings.api_key,
    cache_storage: (
        t.Union[hishel.FileStorage, hishel.SQLiteStorage, hishel.InMemoryStorage] | None
    ) = None,
    cache_ttl: int = 900,
    debug_http_response: bool = False,
) -> dict | None:

    if cache_storage is None:
        cache_storage = owm_hishel_filestorage_dependency()

    ## Initialize USE_ZIP as False
    USE_ZIP: bool = False

    ## Ensure a country_code was passed
    assert country_code, ValueError("Must pass a country_code, i.e. 'US'")

    ## Check input params
    if not city_name and not state_code and not country_code and not zip_code:
        raise ValueError(
            "Must pass a city_name state_code and country_code, or a zip_code"
        )

    if not zip_code:
        ## No zip_code passed, check for city_name + state_code + country_code
        assert city_name and state_code and country_code, ValueError(
            f"Must pass a city, state, and country. Got values ({city_name}, {state_code}, {country_code})"
        )

        ## Build query string
        q: str = f"{city_name},{state_code},{country_code}"
        ## Set log print message
        print_msg: str = (
            f"Requesting weather in {city_name.title()}, {state_code.upper()} {country_code.upper()}"
        )
        ## Tell request not to use zip_code query
        USE_ZIP = False
        ## Build params dict
        params = {"q": q, "limit": limit, "appid": api_key, "format": response_format}

    else:
        ## Zip code was passed, check for country_code
        assert country_code, ValueError(
            "When passing a zip_code, you must also pass a country_code."
        )
        ## Build query string
        q = f"{zip_code},{country_code}"
        ## Set log print message
        print_msg = f"Requesting weather in {zip_code}, {country_code.upper()}"
        ## Tell request to use zip_code query
        USE_ZIP = True
        ## Build params dict
        params = {"zip": q, "limit": limit, "appid": api_key, "format": response_format}

    with httpx_utils.HishelCacheClientController(
        force_cache=True, storage=cache_storage, follow_redirects=True
    ) as cache_ctl:
        req: httpx.Request = cache_ctl.new_request(
            url=f"{OPENWEATHERMAP_GEO_URL}{'/zip' if USE_ZIP else '/direct'}",
            params=params,
        )

        try:
            res: httpx.Response = cache_ctl.send_request(
                request=req, debug_response=debug_http_response
            )

        except Exception as exc:
            msg = Exception(
                f"Unhandled exception sending geolocation request. Details: {exc}"
            )
            log.error(msg)

            raise exc

        ## Check response status code
        if res.status_code == 200:
            ## Success, decode response
            try:
                _decode = cache_ctl.decode_res_content(res=res)
                return _decode

            except Exception as exc:
                msg = Exception(
                    f"Unhandled exception decoding geolocaate response content. Details: {exc}"
                )
                log.error(msg)

                raise exc

        else:
            ## Non-200 response code
            log.warning(
                f"Response non-successful: [{res.status_code}: {res.reason_phrase}]: {res.text}"
            )

            return None


def reverse_geocode(
    lat: str = None,
    lon: str = None,
    limit: int = 5,
    cache_storage: (
        t.Union[hishel.FileStorage, hishel.InMemoryStorage, hishel.SQLiteStorage] | None
    ) = None,
    api_key: str = owm_settings.api_key,
) -> dict | None:
    if cache_storage is None:
        cache_storage = owm_hishel_filestorage_dependency()

    with httpx_utils.HishelCacheClientController(
        force_cache=True, storage=cache_storage
    ) as httpx_ctl:
        req = httpx_ctl.new_request(
            url=f"{OPENWEATHERMAP_GEO_URL}/reverse",
            params={"lat": lat, "lon": lon, "limit": limit, "appid": api_key},
        )

        log.info(f"Reverse geocoding lat-{lat}, lon-{lon}")
        # log.debug(f"URL: {req.url}")
        try:
            res = httpx_ctl.send_request(request=req)
        except Exception as exc:
            msg = Exception(
                f"Unhandled exception sending geolocation request. Details: {exc}"
            )
            log.error(msg)

            raise exc

    # log.info(f"Reverse geocode response: [{res.status_code}: {res.reason_phrase}]")

    if res.status_code == 200:
        try:
            _decode = httpx_ctl.decode_res_content(res=res)
        except Exception as exc:
            msg = Exception(
                f"Unhandled exception decoding reverse geocode response content. Details: {exc}"
            )
            log.error(msg)

            raise exc

    else:
        log.warning(
            f"Response non-successful: [{res.status_code}: {res.reason_phrase}]: {res.text}"
        )

        return None

    if isinstance(_decode, list):
        if len(_decode) == 0:
            return None
        if len(_decode) == 1:
            return _decode[0]
        else:
            log.warning(f"Multiple results for lat: {lat} / lon: {lon}.")

    return _decode
