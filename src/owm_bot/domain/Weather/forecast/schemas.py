from __future__ import annotations

import logging
import typing as t

log = logging.getLogger("owm_bot.domain.Weather.forecast")

from decimal import Decimal

from owm_bot.domain.Common.schemas import OWMCoord

from pydantic import BaseModel, Field, ValidationError, computed_field, field_validator
from red_utils.ext import time_utils

class OWMForecastMain(BaseModel):
    temp: Decimal = Field(default=None, decimal_places=2)
    feels_like: Decimal = Field(default=None, decimal_places=2)
    temp_max: Decimal = Field(default=None, decimal_places=2)
    pressure: int = Field(default=None)
    sea_level: int = Field(default=None)
    grnd_level: int = Field(default=None)
    humidiy: int = Field(default=None)
    temp_kf: Decimal = Field(default=None, decimal_places=2)


class OWMForecastWeather(BaseModel):
    id: int = Field(default=None)
    main: str = Field(default=None)
    description: str = Field(default=None)
    icon: str = Field(default=None)


class OWMForecastClouds(BaseModel):
    all: int = Field(default=None)


class OWMForecastWind(BaseModel):
    speed: Decimal = Field(default=None, decimal_places=2)
    deg: int = Field(default=None)
    gust: Decimal = Field(default=None, decimal_places=2)


class OWMForecastSys(BaseModel):
    pod: str = Field(default=None)


class OWMForecastWeatherEntry(BaseModel):
    dt: int = Field(default=None)
    main: OWMForecastMain = Field(default=None)
    weather: list[OWMForecastWeather] = Field(default=None)
    clouds: OWMForecastClouds = Field(default=None)
    wind: OWMForecastWind = Field(default=None)
    visibility: int = Field(default=None)
    pop: Decimal = Field(default=None, decimal_places=2)
    sys: OWMForecastSys = Field(default=None)
    dt_txt: str = Field(default=None)

    @computed_field
    @property
    def timestamp(self) -> str:
        return time_utils.get_ts(as_str=True)

    @field_validator("pop")
    def validate_pop(cls, v) -> Decimal:
        if isinstance(v, Decimal):
            return v
        elif isinstance(v, int):
            _v = Decimal(f"{v}")

            return _v
        elif isinstance(v, str):
            try:
                _v = Decimal(v)

                return _v
            except Exception as exc:
                msg = Exception(
                    f"Unhandled exception converting string '{v}' to Decimal. Details: {exc}"
                )
                log.error(msg)

                raise exc

        raise ValidationError


class OwmForecastWeatherCity(BaseModel):
    id: int = Field(default=None)
    name: str = Field(default=None)
    coord: OWMCoord = Field(default=None)
    country: str = Field(default=None)
    population: int = Field(default=None)
    timezone: int = Field(defaault=None)
    sunrise: int = Field(default=None)
    sunset: int = Field(default=None)


class OWMForecastWeatherBase(BaseModel):
    cod: str = Field(default=None)
    message: int = Field(default=None)
    cnt: int = Field(default=None)
    entries: list[OWMForecastWeatherEntry] = Field(default=None, alias="list")


class OWMForecastWeather(OWMForecastWeatherBase):
    pass
