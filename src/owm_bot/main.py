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

if __name__ == "__main__":
    setup_logging(name="owm_bot", log_level=settings.log_level)
    setup_dirs()

    log.debug(f"Settings: {settings}")
    log.debug(f"OWM Settings: {owm_settings}")

    location: JsonLocation = init_location()
    log.debug(f"Location: {location}")

    # reverse_lookup = geolocate.reverse_geocode(
    #     lat=updated_location.lat, lon=updated_location.lon
    # )
    # log.debug(f"Reverse geolocation lookup: {reverse_lookup}")
