from __future__ import annotations

import logging
import typing as t
from pathlib import Path

log = logging.getLogger("owm_bot.core.depends")

from owm_bot.core.paths import CACHE_DIR, HTTP_CACHE_DIR, OWM_HTTP_CACHE_DIR

import hishel
from red_utils.ext import httpx_utils


def hishel_filestorage_dependency(
    cache_dir: t.Union[str, Path] = HTTP_CACHE_DIR, ttl: int = 900
) -> hishel.FileStorage:
    cache_storage: hishel.FileStorage = httpx_utils.get_hishel_file_storage(
        cache_dir=cache_dir, ttl=ttl
    )

    return cache_storage


def owm_hishel_filestorage_dependency(
    cache_dir: t.Union[str, Path] = OWM_HTTP_CACHE_DIR, ttl: int = 900
) -> hishel.FileStorage:
    cache_storage: hishel.FileStorage = httpx_utils.get_hishel_file_storage(
        cache_dir=cache_dir, ttl=ttl
    )

    return cache_storage
