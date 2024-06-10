from __future__ import annotations

from pathlib import Path
import typing as t

from dynaconf import Dynaconf
from pydantic import Field, ValidationError, field_validator
from pydantic_settings import BaseSettings

DYNACONF_SETTINGS: Dynaconf = Dynaconf(
    environments=True,
    envvar_prefix="DYNACONF",
    settings_files=["settings.toml", ".secrets.toml"],
)

DYNACONF_OWM_SETTINGS: Dynaconf = Dynaconf(
    environments=True,
    envvar_prefix="OWM",
    settings_files=["openweathermap/settings.toml", "openweathermap/.secrets.toml"],
)


class AppSettings(BaseSettings):
    env: str = Field(default=DYNACONF_SETTINGS.ENV, env="ENV")
    container_env: bool = Field(
        default=DYNACONF_SETTINGS.CONTAINER_ENV, env="CONTAINER_ENV"
    )
    log_level: str = Field(default=DYNACONF_SETTINGS.LOG_LEVEL, env="LOG_LEVEL")


class OpenweathermapSettings(BaseSettings):
    api_key: str = Field(
        default=DYNACONF_OWM_SETTINGS.OWM_API_KEY, env="OWM_API_KEY", repr=False
    )
    location_file: t.Union[str, Path] = Field(
        default=DYNACONF_OWM_SETTINGS.OWM_LOCATION_FILE, env="OWM_LOCATION_FILE"
    )
    units: str = Field(default=DYNACONF_OWM_SETTINGS.OWM_UNITS, env="OWM_UNITS")


settings: AppSettings = AppSettings()
owm_settings: OpenweathermapSettings = OpenweathermapSettings()
