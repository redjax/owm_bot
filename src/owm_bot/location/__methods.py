import typing as t
import logging
from pathlib import Path

log = logging.getLogger("owm_bot.location.methods")

from owm_bot.core.paths import LOCATIONS_PQ_FILE
from owm_bot.domain.Location import JsonLocation, JsonLocationsLoader, OwmGeoLookup
from owm_bot.core.config import owm_settings
from owm_bot.core.depends import owm_hishel_filestorage_dependency
from owm_bot.location.geolocate import get_coords
from owm_bot.utils import data_utils

import hishel
import httpx
import pandas as pd


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

        if updated_location.state_code is None:
            updated_location.state_code = location_obj.state_code

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
) -> JsonLocation:
    location_loader = JsonLocationsLoader(location_file=location_file)

    updated_location: JsonLocation = get_missing_coords(
        location_obj=location,
        cache_storage=cache_storage,
        debug_http_response=debug_http_response,
    )

    if updated_location.state_code is None:
        updated_location.state_code = location.state

    location_loader.location = updated_location

    return updated_location


def save_location_dict_to_file(
    location: t.Union[JsonLocation, OwmGeoLookup] = None,
    location_file: t.Union[str, Path] = owm_settings.location_file,
):
    if isinstance(location, OwmGeoLookup):
        log.debug(f"Converting OwmGeoLookup object to JsonLocation.")
        location = JsonLocation(
            city_name=location.name,
            state_code=location.state,
            country_code=location.country,
            zip_code=location.zip,
            lat=location.lat,
            lon=location.lon,
        )

    location_file = Path(f"{location_file}")

    if not location_file.exists():
        log.warning(f"Could not find locations file '{location_file}'")

        raise FileNotFoundError

    location_loader = JsonLocationsLoader(location_file=location_file)
    location_loader.location = location

    try:
        location_loader.save_to_file(overwrite=True)
    except Exception as exc:
        msg = Exception(
            f"Unhandled exception saving location to JSON file '{location_file}'. Details: {exc}"
        )
        log.error(msg)

        raise exc


def init_location(
    location_file: t.Union[str, Path] = owm_settings.location_file,
    cache_storage: (
        t.Union[hishel.FileStorage, hishel.InMemoryStorage, hishel.SQLiteStorage] | None
    ) = None,
    debug_http_response: bool = False,
) -> JsonLocation:
    assert location_file, ValueError("Missing a location_file path")
    location_file: Path = Path(f"{location_file}")

    ## Load initial list of JsonLocation objects
    location: list[JsonLocation] = load_location_from_file(location_file=location_file)
    log.debug(f"Updating location coords")
    ## Update location objects
    try:
        updated_location: list[JsonLocation] = update_location_coords(
            location=location,
            location_file=location_file,
            cache_storage=cache_storage,
            debug_http_response=debug_http_response,
        )
    except RecursionError as recur:
        msg = Exception(
            f"update_location_coords() looped too many times. Check your code. Details: {recur}"
        )
        log.error(msg)

        raise recur
    except Exception as exc:
        msg = Exception(f"Unhandled exception updating location coords. Details: {exc}")
        log.error(msg)

        raise exc

    log.debug(f"Saving updated location coords")
    try:
        save_location_dict_to_file(
            location=updated_location, location_file=location_file
        )
    except Exception as exc:
        msg = Exception(
            f"Unhandled exception saving updated location coordinates. Details: {exc}"
        )
        log.error(msg)

        raise exc

    ## Reload location from file
    location: JsonLocation = load_location_from_file(location_file=location_file)

    return location
