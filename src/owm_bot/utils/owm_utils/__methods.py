from __future__ import annotations

import logging
import typing as t

log = logging.getLogger("owm_bot.controllers.openweathermap_controller.methods")

from owm_bot.core.config import owm_settings
from owm_bot.domain.Location import JsonLocation
from owm_bot.location import geolocate

def handle_missing_coords(
    location_obj: JsonLocation = None, debug_http_response: bool = False
) -> JsonLocation:

    if location_obj.lat is None or location_obj.lon is None:
        log.info(
            f"Updating latitude & longitude for location '{location_obj.city_name}, '{location_obj.country_code}'"
        )
        try:

            _updated_location_dict: dict | None = geolocate.get_coords(
                city_name=location_obj.city_name,
                state_code=location_obj.state_code,
                country_code=location_obj.country_code,
                zip_code=location_obj.zip_code,
                api_key=owm_settings.api_key,
                debug_http_response=debug_http_response,
            )
        except Exception as exc:
            msg = Exception(f"Unhandled exception getting coordinates. Details: {exc}")
            log.error(msg)

            raise exc

        if _updated_location_dict is None:
            msg = ValueError(
                f"Updated location should have been a dict, but was None instead."
            )
            log.error(msg)

            raise msg

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
