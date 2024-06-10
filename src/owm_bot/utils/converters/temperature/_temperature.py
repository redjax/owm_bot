import typing as t
from decimal import Decimal

import logging

log = logging.getLogger("owm_bot.utils.converters.temperature")

VALID_UNITS: list[str] = ["standard", "metric", "imperial"]
TEMPERATURE_SYMBOL_MAP: dict = {"standard": "K", "metric": "C", "imperial": "F"}


def _c_to_f(v: t.Union[int, Decimal, float]):
    return v * 1.8 + 32


def _c_to_k(v: t.Union[int, Decimal, float]):
    return v + 273.15


def _f_to_c(v: t.Union[int, Decimal, float]):
    return (v - 32) / 1.8


def _f_to_k(v: t.Union[int, Decimal, float]):
    return (v + 459.67) * 5 / 9


def _k_to_c(v: t.Union[int, Decimal, float]):
    return v - 273.15


def _k_to_f(v: t.Union[int, Decimal, float]):
    return v * 9 / 5 - 459.67


def _parse_conversion(
    temp_in: t.Union[int, float, Decimal], units_in: str, convert_to_units: str
):
    ## Convert temperature
    log.info(f"Converting input temperature from {units_in} to {convert_to_units}")
    match units_in:
        case "standard":
            match convert_to_units:
                case "metric":
                    ## Convert K to C
                    return _k_to_c(v=temp_in)
                case "imperial":
                    ## Convert K to F
                    return _k_to_f(v=temp_in)
                case _:
                    raise ValueError(f"Invalid convert_to_units: {convert_to_units}")
        case "metric":
            match convert_to_units:
                case "standard":
                    ## Convert C to K
                    return _c_to_k(v=temp_in)
                case "imperial":
                    ## Convert C to F
                    return _c_to_f(v=temp_in)
                case _:
                    raise ValueError(f"Invalid convert_to_units: {convert_to_units}")
        case "imperial":
            match convert_to_units:
                case "metric":
                    ## Convert F to C
                    return _f_to_c(v=temp_in)
                case "standard":
                    ## Convert F to K
                    return _f_to_k(v=temp_in)
                case _:
                    raise ValueError(f"Invalid convert_to_units: {convert_to_units}")
        case _:
            raise ValueError(f"Invalid units_in: {units_in}")


def convert_temperature(
    temp_in: t.Union[int, float, Decimal],
    units_in: str = "standard",
    convert_to_units: str = "imperial",
):
    assert temp_in, ValueError("Missing an input temperature to convert")
    assert (
        isinstance(temp_in, int)
        or isinstance(temp_in, float)
        or isinstance(temp_in, Decimal)
    ), TypeError(
        f"Input temperature must be an int, float, or Decimal. Got type: ({type(temp_in)})"
    )

    assert units_in, ValueError(
        f"Missing input units. Please pass one of {VALID_UNITS}"
    )
    assert isinstance(units_in, str), TypeError(
        f"units_in must be a string. Got type: ({type(units_in)})"
    )
    assert units_in in VALID_UNITS, ValueError(
        f"Invalid units_in: '{units_in}'. Must be one of {VALID_UNITS}"
    )

    assert convert_to_units, ValueError("Missing a convert_to_units value")
    assert isinstance(convert_to_units, str), TypeError(
        f"convert_to_units must be a string. Got type: ({type(convert_to_units)})"
    )
    assert convert_to_units in VALID_UNITS, ValueError(
        f"Invalid convert_to_units: '{convert_to_units}'. Must be one of {VALID_UNITS}"
    )

    if units_in == convert_to_units:
        log.warning(
            f"units_in and convert_to_units are both '{units_in}'. Returning temperature"
        )

        return temp_in

    converted_temperature = _parse_conversion(
        temp_in=temp_in, units_in=units_in, convert_to_units=convert_to_units
    )

    return converted_temperature
