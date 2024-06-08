import logging

from owm_bot.core.config import AppSettings, settings
from owm_bot.setup import setup_logging, setup_dirs
from owm_bot.core.paths import (
    CACHE_DIR,
    DATA_DIR,
    ENSURE_DIRS,
    OUTPUT_DIR,
    SERIALIZE_DIR,
)

log = logging.getLogger("owm_bot")

if __name__ == "__main__":
    setup_logging(name="owm_bot", log_level=settings.log_level)
    setup_dirs()
