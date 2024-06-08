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
    geolocate,
)

log = logging.getLogger("owm_bot")

if __name__ == "__main__":
    setup_logging(name="owm_bot", log_level=settings.log_level)
    setup_dirs()

    log.debug(f"Settings: {settings}")
    log.debug(f"OWM Settings: {owm_settings}")

    location: JsonLocation = load_location_from_file()
    log.debug(f"Location: {location}")

    updated_location: JsonLocation = get_missing_coords(location_obj=location)
    log.debug(f"Updated location: {updated_location}")

    reverse_lookup = geolocate.reverse_geocode(
        lat=updated_location.lat, lon=updated_location.lon
    )
    log.debug(f"Reverse geolocation lookup: {reverse_lookup}")
