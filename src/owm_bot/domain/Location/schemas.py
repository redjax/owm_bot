from __future__ import annotations

import json
import logging
from pathlib import Path
import typing as t

log = logging.getLogger("owm_bot.domain.owm.location")

from decimal import Decimal

from owm_bot.utils.encoders import DecimalJsonEncoder

from pydantic import BaseModel, Field, ValidationError, field_validator


class JsonLocationBase(BaseModel):
    city_name: str | None = Field(default=None)
    local_names: dict | None = Field(default=None)
    state_code: str | None = Field(default=None)
    country_code: str | None = Field(default=None)
    zip_code: str | None = Field(default=None)
    lat: Decimal | None = Field(default=None)
    lon: Decimal | None = Field(default=None)


class JsonLocation(JsonLocationBase):
    pass


class JsonLocationsLoaderBase(BaseModel):
    pass


class JsonLocationsLoader(JsonLocationsLoaderBase):
    locations_file: t.Union[str, Path] = Field(default=None)
    locations: list[JsonLocation] = Field(default=[])

    @field_validator("locations_file")
    def validate_locations_file(cls, v):
        v = Path(f"{v}")

        return v

    @property
    def file_exists(self) -> bool:
        return self.locations_file.exists()

    @property
    def count_locations(self) -> int:
        if (
            self.locations is None
            or isinstance(self.locations, list)
            and len(self.locations) == 0
        ):
            return 0
        else:
            return len(self.locations)

    def load_from_file(self) -> list[JsonLocation]:
        try:
            with open(self.locations_file, "r") as f:
                locations = json.loads(f.read())
                log.debug(
                    f"Loaded [{len(locations)}] location(s) from OpenWeathermap locations file: {self.locations_file}"
                )
        except FileNotFoundError as fnf_err:
            log.warning(
                f"Could not find locations file at {self.locations_file}. Create a file with location(s) for the app before re-running."
            )

            raise fnf_err
        except Exception as exc:
            msg = Exception(
                f"Unhandled exception reading locations file into dict. Details: {exc}"
            )
            log.error(msg)
            locations = None

            raise exc

        _locations: list[JsonLocation] = []

        for location_dict in locations:
            try:
                _loc: JsonLocation = JsonLocation.model_validate(location_dict)
                _locations.append(_loc)
            except Exception as exc:
                msg = Exception(
                    f"Unhandled exception converting location dict loaded from JSON file '{self.locations_file}'. Details: {exc}"
                )
                log.warning(msg)

                continue

        self.locations = _locations

        return _locations

    def save_to_file(self, overwrite: bool = True) -> bool:
        if (
            self.locations is None
            or isinstance(self.locations, list)
            and len(self.locations) == 0
        ):
            log.warning(f"Locations list is empty.")

            return False

        if self.file_exists and not overwrite:
            log.warning(
                f"File '{self.locations_file}' exists, and overwrite=False. Skipping save."
            )

            return False

        try:
            json_data = [location.model_dump() for location in self.locations]
        except Exception as exc:
            msg = Exception(
                f"Unhandled exception dumping locations to JSON string. Details: {exc}"
            )
            log.error(msg)

            return False

        log.debug(
            f"Saving [{self.count_locations}] location(s) to file: {self.locations_file}"
        )
        try:
            with open(self.locations_file, "w") as f:
                json.dump(json_data, f, indent=2, cls=DecimalJsonEncoder)

            return True
        except Exception as exc:
            msg = Exception(
                f"Unhandled exception dumping locations to file '{self.locations_file}'. Details: {exc}"
            )
            log.error(msg)

            return False


class OwmGeoLookupBase(BaseModel):
    name: str | None = Field(default=None)
    local_names: dict | None = Field(default=None)
    state: str | None = Field(default=None)
    country: str | None = Field(default=None)
    zip: str | None = Field(default=None)
    lat: Decimal | None = Field(default=None)
    lon: Decimal | None = Field(default=None)


class OwmGeoLookup(OwmGeoLookupBase):
    pass
