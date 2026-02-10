import json
import logging
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from app.config import DATA_DIR

logger = logging.getLogger(__name__)


def _ticker_dir(ticker: str) -> Path:
    # Replace dots/slashes in ticker symbols for safe directory names
    safe = ticker.replace(".", "_").replace("/", "_")
    return DATA_DIR / safe


def _metadata_file(ticker: str) -> Path:
    return _ticker_dir(ticker) / "metadata.json"


def _ensure_dirs(ticker: str):
    base = _ticker_dir(ticker)
    (base / "hourly").mkdir(parents=True, exist_ok=True)
    (base / "daily").mkdir(parents=True, exist_ok=True)


def _parquet_path(ticker: str, timeframe: str) -> Path:
    return _ticker_dir(ticker) / timeframe / f"{timeframe}.parquet"


def save(df: pd.DataFrame, timeframe: str, ticker: str = "SPY") -> None:
    _ensure_dirs(ticker)
    path = _parquet_path(ticker, timeframe)

    if path.exists():
        existing = pd.read_parquet(path)
        combined = pd.concat([existing, df])
        combined = combined[~combined.index.duplicated(keep="last")]
        combined = combined.sort_index()
        combined.to_parquet(path, engine="pyarrow")
        logger.info(
            f"Merged {ticker}/{timeframe}: {len(existing)}+{len(df)} "
            f"→ {len(combined)} rows"
        )
    else:
        df.to_parquet(path, engine="pyarrow")
        logger.info(f"Saved {ticker}/{timeframe}: {len(df)} rows")


def load(timeframe: str, ticker: str = "SPY") -> pd.DataFrame:
    path = _parquet_path(ticker, timeframe)
    if not path.exists():
        return pd.DataFrame()
    df = pd.read_parquet(path)
    return df


def save_metadata(
    active_ticker: str,
    used_fallback: bool,
    fallback_reason: str | None,
    ticker: str = "SPY",
):
    _ensure_dirs(ticker)
    meta = {
        "last_refresh": datetime.now(timezone.utc).isoformat(),
        "active_ticker": active_ticker,
        "used_fallback": used_fallback,
        "fallback_reason": fallback_reason,
    }
    with open(_metadata_file(ticker), "w") as f:
        json.dump(meta, f, indent=2)
    logger.info(f"Metadata saved for {ticker}: active={active_ticker}, fallback={used_fallback}")


def load_metadata(ticker: str = "SPY") -> dict | None:
    mf = _metadata_file(ticker)
    if not mf.exists():
        return None
    with open(mf, "r") as f:
        return json.load(f)


def needs_refresh(max_age_hours: float = 1.0, ticker: str = "SPY") -> bool:
    meta = load_metadata(ticker)
    if meta is None:
        return True
    last = datetime.fromisoformat(meta["last_refresh"])
    age = (datetime.now(timezone.utc) - last).total_seconds() / 3600
    return age > max_age_hours
