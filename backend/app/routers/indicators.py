from fastapi import APIRouter, HTTPException, Query

from app.schemas import IndicatorsResponse, OHLCVPoint, IndicatorPoint
from app.services.orchestrator import get_state, get_default_ticker

router = APIRouter()


def _safe_float(val) -> float | None:
    try:
        v = float(val)
        if v != v:  # NaN check
            return None
        return v
    except (TypeError, ValueError):
        return None


@router.get("/indicators", response_model=IndicatorsResponse)
def get_indicators(
    timeframe: str = Query("daily", pattern="^(daily|hourly)$"),
    ticker: str = Query(None),
):
    t = ticker or get_default_ticker()
    s = get_state(t)
    if not s.ready:
        raise HTTPException(status_code=503, detail="Data not ready")

    df = s.daily_df if timeframe == "daily" else s.hourly_df
    if df.empty:
        raise HTTPException(status_code=404, detail=f"No {timeframe} data available")

    ohlcv = []
    for ts, row in df.iterrows():
        t_str = ts.isoformat()
        o = _safe_float(row.get("Open"))
        h = _safe_float(row.get("High"))
        l = _safe_float(row.get("Low"))
        c = _safe_float(row.get("Close"))
        v = _safe_float(row.get("Volume"))
        if c is not None:
            ohlcv.append(OHLCVPoint(
                time=t_str,
                open=o or c,
                high=h or c,
                low=l or c,
                close=c,
                volume=v or 0,
            ))

    def _series(col: str) -> list[IndicatorPoint]:
        if col not in df.columns:
            return []
        points = []
        for ts, val in df[col].items():
            v = _safe_float(val)
            points.append(IndicatorPoint(time=ts.isoformat(), value=v))
        return points

    return IndicatorsResponse(
        ticker=s.active_ticker,
        timeframe=timeframe,
        ohlcv=ohlcv,
        sma20=_series("SMA_20"),
        sma50=_series("SMA_50"),
        sma200=_series("SMA_200"),
        ema20=_series("EMA_20"),
        ema50=_series("EMA_50"),
        rsi=_series("RSI_14"),
        macd=_series("MACD_12_26_9"),
        macd_signal=_series("MACDs_12_26_9"),
        macd_histogram=_series("MACDh_12_26_9"),
        bb_upper=_series("BBU_20_2.0"),
        bb_middle=_series("BBM_20_2.0"),
        bb_lower=_series("BBL_20_2.0"),
        volatility=_series("volatility"),
        drawdown=_series("drawdown"),
    )
