from __future__ import annotations

OPENWEATHERMAP_BASE_URL: str = "https://api.openweathermap.org"
OPENWEATHERMAP_ONECALL_URL: str = f"{OPENWEATHERMAP_BASE_URL}/data/3.0/onecall"
OPENWEATHERMAP_GEO_URL: str = f"{OPENWEATHERMAP_BASE_URL}/geo/1.0"
OPENWEATHERMAP_CURRENT_WEATHER_URL: str = f"{OPENWEATHERMAP_BASE_URL}/data/2.5/weather"
OPENWEATHERMAP_DAILY_FORECAST_WEATHER_URL: str = (
    f"{OPENWEATHERMAP_BASE_URL}/data/2.5/forecast"
)


PQ_ENGINE: str = "pyarrow"
