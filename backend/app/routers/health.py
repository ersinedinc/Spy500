from fastapi import APIRouter, Query

from app.schemas import HealthResponse
from app.services.orchestrator import get_state, refresh_ticker, get_default_ticker

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health(ticker: str = Query(None)):
    t = ticker or get_default_ticker()
    s = get_state(t)
    return HealthResponse(
        status="ok" if s.ready else "initializing",
        active_ticker=s.active_ticker,
        used_fallback=s.used_fallback,
        fallback_reason=s.fallback_reason,
        last_refresh=s.last_refresh,
        hourly_rows=len(s.hourly_df),
        daily_rows=len(s.daily_df),
        ready=s.ready,
    )


@router.post("/refresh", response_model=HealthResponse)
def refresh_data(ticker: str = Query(None)):
    t = ticker or get_default_ticker()
    refresh_ticker(t)
    s = get_state(t)
    return HealthResponse(
        status="ok" if s.ready else "initializing",
        active_ticker=s.active_ticker,
        used_fallback=s.used_fallback,
        fallback_reason=s.fallback_reason,
        last_refresh=s.last_refresh,
        hourly_rows=len(s.hourly_df),
        daily_rows=len(s.daily_df),
        ready=s.ready,
    )
