import logging
import threading
from dataclasses import dataclass, field
from typing import Optional

import pandas as pd

from app.config import get_config
from app.services.data_fetcher import fetch_data, fetch_ticker_data, FetchResult
from app.services.data_validator import validate
from app.services import parquet_store
from app.services.indicator_engine import compute_indicators
from app.services.regime_detector import detect_regime, RegimeResult
from app.services.heat_score import compute_heat_score, HeatScoreResult
from app.services.dca_engine import compute_dca, DCAResult
from app.services.report_generator import generate_report

logger = logging.getLogger(__name__)


@dataclass
class PipelineState:
    active_ticker: str = ""
    used_fallback: bool = False
    fallback_reason: Optional[str] = None
    hourly_df: pd.DataFrame = field(default_factory=pd.DataFrame)
    daily_df: pd.DataFrame = field(default_factory=pd.DataFrame)
    regime: Optional[RegimeResult] = None
    heat_score: Optional[HeatScoreResult] = None
    dca: Optional[DCAResult] = None
    report: str = ""
    last_refresh: Optional[str] = None
    ready: bool = False


# Per-ticker states — populated on startup and on demand
_states: dict[str, PipelineState] = {}

# Default ticker symbol (set on startup)
_default_ticker: str = "SPY"

# Per-ticker locks to prevent parallel fetches for the same ticker
_locks: dict[str, threading.Lock] = {}
_locks_lock = threading.Lock()


def _get_ticker_lock(ticker: str) -> threading.Lock:
    with _locks_lock:
        if ticker not in _locks:
            _locks[ticker] = threading.Lock()
        return _locks[ticker]


def get_default_ticker() -> str:
    return _default_ticker


def _run_pipeline(result: FetchResult, ticker: str) -> PipelineState:
    """Run the full analysis pipeline on fetched data."""
    # Validate
    hourly = validate(result.hourly, label="hourly")
    daily = validate(result.daily, label="daily")

    # Store
    parquet_store.save(hourly, "hourly", ticker=ticker)
    parquet_store.save(daily, "daily", ticker=ticker)
    parquet_store.save_metadata(
        result.active_ticker, result.used_fallback, result.fallback_reason,
        ticker=ticker,
    )

    # Compute indicators
    daily_ind = compute_indicators(daily)
    hourly_ind = compute_indicators(hourly)

    if daily_ind.empty:
        logger.error(f"No daily data after indicator computation for {ticker}")
        return PipelineState(active_ticker=ticker, ready=False)

    latest = daily_ind.iloc[-1].to_dict()
    prev_row = daily_ind.iloc[-2].to_dict() if len(daily_ind) > 1 else None

    # Regime detection
    regime = detect_regime(latest, prev_row)

    # Heat score
    heat = compute_heat_score(latest)

    # DCA
    dca = compute_dca(heat.score, heat.label, regime.regime.value)

    # Report
    report = generate_report(
        heat=heat,
        regime=regime,
        dca=dca,
        active_ticker=result.active_ticker,
        used_fallback=result.used_fallback,
        fallback_reason=result.fallback_reason,
        latest=latest,
    )

    meta = parquet_store.load_metadata(ticker=ticker)
    return PipelineState(
        active_ticker=result.active_ticker,
        used_fallback=result.used_fallback,
        fallback_reason=result.fallback_reason,
        hourly_df=hourly_ind,
        daily_df=daily_ind,
        regime=regime,
        heat_score=heat,
        dca=dca,
        report=report,
        last_refresh=meta["last_refresh"] if meta else None,
        ready=True,
    )


def refresh_ticker(ticker: str) -> PipelineState:
    """Refresh data for a specific ticker."""
    logger.info(f"Starting pipeline refresh for {ticker}...")
    result: FetchResult = fetch_ticker_data(ticker)
    state = _run_pipeline(result, ticker)
    _states[ticker] = state
    logger.info(f"Pipeline refresh complete for {ticker}")
    return state


def refresh() -> PipelineState:
    """Refresh the default ticker using the original primary/fallback logic."""
    global _states
    logger.info("Starting pipeline refresh (default)...")
    result: FetchResult = fetch_data()
    ticker = result.active_ticker
    state = _run_pipeline(result, ticker)
    _states[ticker] = state
    logger.info("Pipeline refresh complete")
    return state


def initialize_ticker(ticker: str) -> PipelineState:
    """Initialize a specific ticker — load from cache or fetch."""
    cfg = get_config()
    max_age = cfg["data"]["max_age_hours"]

    if parquet_store.needs_refresh(max_age, ticker=ticker):
        logger.info(f"Data for {ticker} is stale or missing, refreshing...")
        return refresh_ticker(ticker)
    else:
        logger.info(f"Data for {ticker} is fresh, loading from cache...")
        return _load_from_cache(ticker)


def initialize() -> PipelineState:
    """Initialize on startup — loads the default ticker from config."""
    global _default_ticker
    cfg = get_config()

    # Set default ticker from etfs config if available
    etfs = cfg.get("etfs", [])
    if etfs:
        _default_ticker = etfs[0]["symbol"]
    else:
        _default_ticker = cfg["tickers"]["fallback"]

    max_age = cfg["data"]["max_age_hours"]

    if parquet_store.needs_refresh(max_age, ticker=_default_ticker):
        logger.info("Data is stale or missing, refreshing...")
        # Use the original primary/fallback logic for first startup
        result: FetchResult = fetch_data()
        state = _run_pipeline(result, result.active_ticker)
        _states[result.active_ticker] = state
        # If fallback was used, also store under the default ticker key
        if result.active_ticker != _default_ticker:
            _states[_default_ticker] = state
        return state
    else:
        logger.info("Data is fresh, loading from parquet...")
        return _load_from_cache(_default_ticker)


def _load_from_cache(ticker: str) -> PipelineState:
    hourly = parquet_store.load("hourly", ticker=ticker)
    daily = parquet_store.load("daily", ticker=ticker)
    meta = parquet_store.load_metadata(ticker=ticker)

    if daily.empty or meta is None:
        logger.warning(f"Cache empty for {ticker}, forcing refresh")
        return refresh_ticker(ticker)

    daily_ind = compute_indicators(daily)
    hourly_ind = compute_indicators(hourly)

    latest = daily_ind.iloc[-1].to_dict()
    prev_row = daily_ind.iloc[-2].to_dict() if len(daily_ind) > 1 else None

    regime = detect_regime(latest, prev_row)
    heat = compute_heat_score(latest)
    dca = compute_dca(heat.score, heat.label, regime.regime.value)
    report = generate_report(
        heat=heat,
        regime=regime,
        dca=dca,
        active_ticker=meta["active_ticker"],
        used_fallback=meta["used_fallback"],
        fallback_reason=meta.get("fallback_reason"),
        latest=latest,
    )

    state = PipelineState(
        active_ticker=meta["active_ticker"],
        used_fallback=meta["used_fallback"],
        fallback_reason=meta.get("fallback_reason"),
        hourly_df=hourly_ind,
        daily_df=daily_ind,
        regime=regime,
        heat_score=heat,
        dca=dca,
        report=report,
        last_refresh=meta["last_refresh"],
        ready=True,
    )

    _states[ticker] = state
    logger.info(f"Loaded {ticker} from cache successfully")
    return state


def get_state(ticker: str | None = None) -> PipelineState:
    """Get state for a ticker. Lazily initializes if not yet loaded."""
    if ticker is None:
        ticker = _default_ticker

    if ticker not in _states:
        lock = _get_ticker_lock(ticker)
        with lock:
            # Double-check after acquiring lock
            if ticker not in _states:
                initialize_ticker(ticker)

    return _states.get(ticker, PipelineState())
