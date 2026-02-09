import logging
from dataclasses import dataclass, field
from typing import Optional

import pandas as pd

from app.config import get_config
from app.services.data_fetcher import fetch_data, FetchResult
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


# Global state — populated on startup and refresh
state = PipelineState()


def refresh() -> PipelineState:
    global state
    logger.info("Starting pipeline refresh...")

    # 1. Fetch
    result: FetchResult = fetch_data()

    # 2. Validate
    hourly = validate(result.hourly, label="hourly")
    daily = validate(result.daily, label="daily")

    # 3. Store
    parquet_store.save(hourly, "hourly")
    parquet_store.save(daily, "daily")
    parquet_store.save_metadata(
        result.active_ticker, result.used_fallback, result.fallback_reason
    )

    # 4. Compute indicators (on daily — more robust for SMA200 etc.)
    daily_ind = compute_indicators(daily)
    hourly_ind = compute_indicators(hourly)

    # 5. Get latest row from daily data for scoring
    if daily_ind.empty:
        logger.error("No daily data after indicator computation")
        state.ready = False
        return state

    latest = daily_ind.iloc[-1].to_dict()
    prev_row = daily_ind.iloc[-2].to_dict() if len(daily_ind) > 1 else None

    # 6. Regime detection
    regime = detect_regime(latest, prev_row)

    # 7. Heat score
    heat = compute_heat_score(latest)

    # 8. DCA
    dca = compute_dca(heat.score, heat.label, regime.regime.value)

    # 9. Report
    report = generate_report(
        heat=heat,
        regime=regime,
        dca=dca,
        active_ticker=result.active_ticker,
        used_fallback=result.used_fallback,
        fallback_reason=result.fallback_reason,
        latest=latest,
    )

    # Update state
    meta = parquet_store.load_metadata()
    state = PipelineState(
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

    logger.info("Pipeline refresh complete")
    return state


def initialize() -> PipelineState:
    cfg = get_config()
    max_age = cfg["data"]["max_age_hours"]

    if parquet_store.needs_refresh(max_age):
        logger.info("Data is stale or missing, refreshing...")
        return refresh()
    else:
        logger.info("Data is fresh, loading from parquet...")
        return _load_from_cache()


def _load_from_cache() -> PipelineState:
    global state

    hourly = parquet_store.load("hourly")
    daily = parquet_store.load("daily")
    meta = parquet_store.load_metadata()

    if daily.empty or meta is None:
        logger.warning("Cache empty, forcing refresh")
        return refresh()

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

    logger.info("Loaded from cache successfully")
    return state


def get_state() -> PipelineState:
    return state
