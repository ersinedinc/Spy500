import json
import logging
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from app.config import DATA_DIR

logger = logging.getLogger(__name__)

METADATA_FILE = DATA_DIR / "metadata.json"


def _ensure_dirs():
    (DATA_DIR / "hourly").mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "daily").mkdir(parents=True, exist_ok=True)


def _parquet_path(timeframe: str) -> Path:
    return DATA_DIR / timeframe / f"{timeframe}.parquet"


def save(df: pd.DataFrame, timeframe: str) -> None:
    _ensure_dirs()
    path = _parquet_path(timeframe)

    if path.exists():
        existing = pd.read_parquet(path)
        combined = pd.concat([existing, df])
        combined = combined[~combined.index.duplicated(keep="last")]
        combined = combined.sort_index()
        combined.to_parquet(path, engine="pyarrow")
        logger.info(
            f"Merged {timeframe}: {len(existing)}+{len(df)} "
            f"→ {len(combined)} rows"
        )
    else:
        df.to_parquet(path, engine="pyarrow")
        logger.info(f"Saved {timeframe}: {len(df)} rows")


def load(timeframe: str) -> pd.DataFrame:
    path = _parquet_path(timeframe)
    if not path.exists():
        return pd.DataFrame()
    df = pd.read_parquet(path)
    return df


def save_metadata(active_ticker: str, used_fallback: bool, fallback_reason: str | None):
    _ensure_dirs()
    meta = {
        "last_refresh": datetime.now(timezone.utc).isoformat(),
        "active_ticker": active_ticker,
        "used_fallback": used_fallback,
        "fallback_reason": fallback_reason,
    }
    with open(METADATA_FILE, "w") as f:
        json.dump(meta, f, indent=2)
    logger.info(f"Metadata saved: {active_ticker}, fallback={used_fallback}")


def load_metadata() -> dict | None:
    if not METADATA_FILE.exists():
        return None
    with open(METADATA_FILE, "r") as f:
        return json.load(f)


def needs_refresh(max_age_hours: float = 1.0) -> bool:
    meta = load_metadata()
    if meta is None:
        return True
    last = datetime.fromisoformat(meta["last_refresh"])
    age = (datetime.now(timezone.utc) - last).total_seconds() / 3600
    return age > max_age_hours
