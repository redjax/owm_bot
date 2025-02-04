import logging

from owm_bot.core.config import (
    AppSettings,
    settings,
    OpenweathermapSettings,
    owm_settings,
)
from owm_bot.domain.Location.schemas import JsonLocation
from owm_bot.setup import setup_logging, setup_dirs
from owm_bot.core.paths import (
    CACHE_DIR,
    DATA_DIR,
    ENSURE_DIRS,
    OUTPUT_DIR,
    SERIALIZE_DIR,
)
from owm_bot.location import (
    load_location_from_file,
    get_missing_coords,
    update_location_coords,
    save_location_dict_to_file,
    init_location,
    geolocate,
)

log = logging.getLogger("owm_bot")


def validate_location(location: JsonLocation = None) -> None:
    assert location, ValueError("Missing a location to validate")
    assert isinstance(location, JsonLocation), TypeError(
        f"location must be a JsonLocation object. Got type: ({type(location)})"
    )

    log.info(f"Validating location")
    reverse_lookup = geolocate.reverse_geocode(lat=location.lat, lon=location.lon)
    log.debug(f"Reverse lookup ({type(reverse_lookup)}): {reverse_lookup}")

    assert location.city_name == reverse_lookup["name"], ValueError(
        f"Location name '{location.city_name}' and reverse lookup name '{reverse_lookup['name']} must match."
    )
    assert (
        location.lat == reverse_lookup["lat"] and location.lon == reverse_lookup["lon"]
    ), ValueError(
        f"Location lat: '{location.lat}' / lon: {location.lon} and reverse lookup lat: '{reverse_lookup['lat']} / lon: {reverse_lookup['lon']} must match."
    )


if __name__ == "__main__":
    setup_logging(name="owm_bot", log_level=settings.log_level)
    setup_dirs()

    log.debug(f"Settings: {settings}")
    log.debug(f"OWM Settings: {owm_settings}")

    location: JsonLocation = init_location()
    log.debug(f"Location: {location}")
