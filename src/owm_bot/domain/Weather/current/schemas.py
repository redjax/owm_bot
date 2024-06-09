from __future__ import annotations

import typing as t
from datetime import datetime
import logging

log = logging.getLogger("weatherbot.domain.owm.weather.current")

from decimal import Decimal

from owm_bot.domain.Common.schemas import OWMCoord

import pendulum
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    ValidationError,
    computed_field,
    field_validator,
)
from red_utils.ext import time_utils


class OWMWeather(BaseModel):
    id: int = Field(default=None)
    main: str = Field(default=None)
    description: str = Field(default=None)
    icon: str = Field(default=None)


class OWMWeatherMain(BaseModel):
    temp: Decimal = Field(default=None)
    feels_like: Decimal = Field(default=None)
    temp_min: Decimal = Field(default=None)
    temp_max: Decimal = Field(default=None)
    pressure: int = Field(default=None)
    humidity: int = Field(default=None)


class OWMWind(BaseModel):
    speed: Decimal = Field(default=None)
    deg: int = Field(default=None)
    gust: Decimal | None = Field(default=None)


class OWMRain(BaseModel):
    one_hour: Decimal = Field(default=None, alias="1h")


class OWMClouds(BaseModel):
    all: int = Field(default=None)


class OWMSys(BaseModel):
    type: int = Field(default=None)
    id: int = Field(default=None)
    country: str = Field(default=None)
    sunrise: int = Field(default=None)
    sunset: int = Field(default=None)


class OWMCurrentWeatherBase(BaseModel):
    coord: OWMCoord = Field(default=None)
    weather: list[OWMWeather] = Field(default=None)
    base: str = Field(default=None)
    main: OWMWeatherMain = Field(default=None)
    visibility: int = Field(default=None)
    wind: OWMWind = Field(default=None)
    rain: OWMRain | None = Field(default=None)
    clouds: OWMClouds = Field(default=None)
    sys: OWMSys = Field(default=None)
    timezone: int = Field(default=None)
    id: int = Field(default=None)
    name: str = Field(default=None)
    cod: int = Field(default=None)

    @computed_field
    @property
    def timestamp(self) -> str:
        return time_utils.get_ts(as_str=True)


class OWMCurrentWeather(OWMCurrentWeatherBase):
    pass
