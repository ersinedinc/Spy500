import logging
from typing import Optional

import pandas as pd
import yfinance as yf

from app.config import get_config

logger = logging.getLogger(__name__)


class FetchResult:
    def __init__(
        self,
        hourly: pd.DataFrame,
        daily: pd.DataFrame,
        active_ticker: str,
        used_fallback: bool,
        fallback_reason: Optional[str] = None,
    ):
        self.hourly = hourly
        self.daily = daily
        self.active_ticker = active_ticker
        self.used_fallback = used_fallback
        self.fallback_reason = fallback_reason


def _download(ticker: str, interval: str, period: str) -> pd.DataFrame:
    logger.info(f"Downloading {ticker} interval={interval} period={period}")
    df = yf.download(ticker, interval=interval, period=period, progress=False)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.droplevel(1)
    if df.index.tz is None:
        df.index = df.index.tz_localize("UTC")
    else:
        df.index = df.index.tz_convert("UTC")
    df.index.name = "Datetime"

    # Some tickers (e.g. European ETFs) return intraday data even for "1d"
    # interval. Resample to true daily bars to avoid duplicate date issues.
    if interval == "1d" and not df.empty:
        dates = df.index.normalize()
        if dates.duplicated().any():
            logger.info(f"Resampling {ticker} daily data: {len(df)} rows have duplicate dates")
            df = df.resample("1D").agg({
                "Open": "first",
                "High": "max",
                "Low": "min",
                "Close": "last",
                "Volume": "sum",
            }).dropna(subset=["Close"])
            logger.info(f"Resampled to {len(df)} daily rows")

    return df


def fetch_data() -> FetchResult:
    cfg = get_config()
    primary = cfg["tickers"]["primary"]
    fallback = cfg["tickers"]["fallback"]
    min_rows = cfg["tickers"]["min_rows_threshold"]
    hourly_period = cfg["data"]["hourly_period"]
    daily_period = cfg["data"]["daily_period"]

    # Try primary ticker for hourly data
    hourly = _download(primary, "1h", hourly_period)
    active_ticker = primary
    used_fallback = False
    fallback_reason = None

    if len(hourly) < min_rows:
        fallback_reason = (
            f"{primary} returned only {len(hourly)} hourly rows "
            f"(minimum {min_rows}). Falling back to {fallback}."
        )
        logger.warning(fallback_reason)
        hourly = _download(fallback, "1h", hourly_period)
        active_ticker = fallback
        used_fallback = True

    # Always fetch daily data from the active ticker
    daily = _download(active_ticker, "1d", daily_period)

    logger.info(
        f"Fetch complete: ticker={active_ticker}, "
        f"hourly={len(hourly)} rows, daily={len(daily)} rows, "
        f"fallback={used_fallback}"
    )

    return FetchResult(
        hourly=hourly,
        daily=daily,
        active_ticker=active_ticker,
        used_fallback=used_fallback,
        fallback_reason=fallback_reason,
    )


def fetch_ticker_data(ticker: str) -> FetchResult:
    """Fetch data for a specific ticker directly (no primary/fallback logic)."""
    cfg = get_config()
    hourly_period = cfg["data"]["hourly_period"]
    daily_period = cfg["data"]["daily_period"]

    hourly = _download(ticker, "1h", hourly_period)
    daily = _download(ticker, "1d", daily_period)

    logger.info(
        f"Fetch complete: ticker={ticker}, "
        f"hourly={len(hourly)} rows, daily={len(daily)} rows"
    )

    return FetchResult(
        hourly=hourly,
        daily=daily,
        active_ticker=ticker,
        used_fallback=False,
        fallback_reason=None,
    )
