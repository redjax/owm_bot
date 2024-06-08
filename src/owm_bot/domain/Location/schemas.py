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
    location_file: t.Union[str, Path] = Field(default=None)
    location: JsonLocation | None = Field(default=None)

    @property
    def file_exists(self) -> bool:
        return self.location_file.exists()

    @field_validator("location_file")
    def validate_location_file(cls, v):
        v = Path(f"{v}")

        return v


class JsonLocationsLoader(JsonLocationsLoaderBase):

    def load_from_file(self) -> list[JsonLocation]:
        if not self.file_exists:
            msg = FileNotFoundError(
                f"Could not find location file at {self.location_file}. Create a JSON file with data about the location you want weather for, before re-running."
            )
            log.error(msg)

            raise msg

        try:
            with open(self.location_file, "r") as f:
                location_dict = json.loads(f.read())

        except Exception as exc:
            msg = Exception(
                f"Unhandled exception reading location file into dict. Details: {exc}"
            )
            log.error(msg)
            location_dict = None

            raise exc

        try:
            _location: JsonLocation = JsonLocation.model_validate(location_dict)

        except Exception as exc:
            msg = Exception(
                f"Unhandled exception converting location dict loaded from JSON file '{self.location_file}'. Details: {exc}"
            )
            log.warning(msg)

        self.location = _location

        return _location

    def save_to_file(self, overwrite: bool = True) -> bool:
        if self.location is None:
            log.warning(f"Locations list is empty.")

            return False

        if self.file_exists and not overwrite:
            log.warning(
                f"File '{self.location_file}' exists, and overwrite=False. Skipping save."
            )

            return False

        try:
            json_data = self.location.model_dump()
        except Exception as exc:
            msg = Exception(
                f"Unhandled exception dumping location to JSON string. Details: {exc}"
            )
            log.error(msg)

            return False

        log.debug(f"Saving location to file: {self.location_file}")
        try:
            with open(self.location_file, "w") as f:
                json.dump(json_data, f, indent=2, cls=DecimalJsonEncoder)

            return True
        except Exception as exc:
            msg = Exception(
                f"Unhandled exception dumping location to file '{self.location_file}'. Details: {exc}"
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
