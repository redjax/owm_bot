from pathlib import Path

DATA_DIR: Path = Path(f".data/owm-bot")
CACHE_DIR: Path = Path(f"{DATA_DIR}/cache")
SERIALIZE_DIR: Path = Path(f"{DATA_DIR}/serialize")
PQ_DIR: Path = Path(f"{DATA_DIR}/parquet")
OUTPUT_DIR: Path = Path(f"{DATA_DIR}/output")

HTTP_CACHE_DIR: Path = Path(f"{CACHE_DIR}/http")
OWM_HTTP_CACHE_DIR: Path = Path(f"{HTTP_CACHE_DIR}/openweathermap")

LOCATIONS_PQ_FILE: Path = Path(f"{PQ_DIR}/openweathermap/locations.parquet")
CURRENT_WEATHER_PQ_FILE: Path = Path(
    f"{PQ_DIR}/openweathermap/current_weather_history.parquet"
)
FORECAST_WEATHER_PQ_FILE: Path = Path(
    f"{PQ_DIR}/openweathermap/forecast_weather_history.parquet"
)

ENSURE_DIRS: list[Path] = [
    DATA_DIR,
    CACHE_DIR,
    HTTP_CACHE_DIR,
    OWM_HTTP_CACHE_DIR,
    SERIALIZE_DIR,
    PQ_DIR,
    OUTPUT_DIR,
]
