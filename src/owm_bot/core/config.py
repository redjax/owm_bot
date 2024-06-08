from typing import Union

from dynaconf import Dynaconf
from pydantic import Field, ValidationError, field_validator
from pydantic_settings import BaseSettings

DYNACONF_SETTINGS: Dynaconf = Dynaconf(
    environments=True,
    envvar_prefix="DYNACONF",
    settings_files=["settings.toml", ".secrets.toml"],
)


class AppSettings(BaseSettings):
    env: str = Field(default=DYNACONF_SETTINGS.ENV, env="ENV")
    container_env: bool = Field(
        default=DYNACONF_SETTINGS.CONTAINER_ENV, env="CONTAINER_ENV"
    )
    log_level: str = Field(default=DYNACONF_SETTINGS.LOG_LEVEL, env="LOG_LEVEL")


settings: AppSettings = AppSettings()
