from __future__ import annotations

import logging
from pathlib import Path

log = logging.getLogger("owm_bot.setup")

from owm_bot.core.paths import ENSURE_DIRS

from red_utils.std import path_utils

def setup_dirs(ensure_dirs: list[Path] = ENSURE_DIRS):
    try:
        path_utils.ensure_dirs_exist(ensure_dirs=ensure_dirs)
    except Exception as exc:
        msg = Exception(
            f"Unhandled exception creating initial directory/ies. Details: {exc}"
        )
        log.debug(msg)

        raise exc
