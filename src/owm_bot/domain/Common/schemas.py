from __future__ import annotations

import logging
import typing as t

log = logging.getLogger("owm_bot.domain.Common")

from decimal import Decimal

from pydantic import BaseModel, Field, ValidationError, field_validator

class OWMCoord(BaseModel):
    lat: Decimal = Field(default=None)
    lon: Decimal = Field(default=None)
