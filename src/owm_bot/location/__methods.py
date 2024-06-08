import typing as t
import logging
from pathlib import Path

log = logging.getLogger("owm_bot.location.methods")

from owm_bot.domain.Location import JsonLocation, JsonLocationsLoader
from owm_bot.core.config import owm_settings
from owm_bot.core.depends import owm_hishel_filestorage_dependency
from owm_bot.location.geolocate import get_coords

import hishel
import httpx


def load_location_from_file(
    location_file: t.Union[str, Path] = owm_settings.location_file
) -> JsonLocation:
    location_loader = JsonLocationsLoader(location_file=location_file)

    try:
        return location_loader.load_from_file()
    except Exception as exc:
        msg = Exception(
            f"Unhandled exception loading location from file '{location_file}'. Details: {exc}"
        )
        log.error(msg)

        raise exc


def get_missing_coords(
    location_obj: JsonLocation = None,
    cache_storage: (
        hishel.FileStorage | hishel.SQLiteStorage | hishel.InMemoryStorage
    ) = None,
    debug_http_response: bool = False,
) -> JsonLocation:
    if cache_storage is None:
        # cache_storage = httpx_utils.get_hishel_file_storage(cache_dir=CACHE_DIR)
        cache_storage = owm_hishel_filestorage_dependency()

    if location_obj.lat is None or location_obj.lon is None:
        log.info(
            f"Updating latitude & longitude for location '{location_obj.city_name}, '{location_obj.country_code}'"
        )
        _updated_location_dict = get_coords(
            city_name=location_obj.city_name,
            state_code=location_obj.state_code,
            country_code=location_obj.country_code,
            zip_code=location_obj.zip_code,
            api_key=owm_settings.api_key,
            debug_http_response=debug_http_response,
        )

        try:
            updated_location: JsonLocation = JsonLocation(
                city_name=_updated_location_dict["name"],
                zip_code=_updated_location_dict["zip"],
                country_code=_updated_location_dict["country"],
                lat=_updated_location_dict["lat"],
                lon=_updated_location_dict["lon"],
            )
        except Exception as exc:
            msg = Exception(
                f"Unhandled exception updating location object. Details: {exc}"
            )
            log.error(msg)

            raise exc

        return updated_location
    else:
        return_location: JsonLocation = location_obj

        return return_location


def update_location_coords(
    location: JsonLocation = None,
    location_file: t.Union[str, Path] = owm_settings.location_file,
    cache_storage: (
        t.Union[hishel.FileStorage, hishel.SQLiteStorage, hishel.InMemoryStorage] | None
    ) = None,
    debug_http_response: bool = False,
) -> list[JsonLocation]:
    location_loader = JsonLocationsLoader(location_file=location_file)

    raise NotImplementedError("update_location_coords not fully implemented")
