from pathlib import Path

DATA_DIR: Path = Path(f".data/owm-bot")
CACHE_DIR: Path = Path(f"{DATA_DIR}/cache")
SERIALIZE_DIR: Path = Path(f"{DATA_DIR}/serialize")
PQ_DIR: Path = Path(f"{DATA_DIR}/parquet")
OUTPUT_DIR: Path = Path(f"{DATA_DIR}/output")

ENSURE_DIRS: list[Path] = [DATA_DIR, CACHE_DIR, SERIALIZE_DIR, PQ_DIR, OUTPUT_DIR]
