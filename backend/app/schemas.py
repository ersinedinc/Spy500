from pydantic import BaseModel


class TickerInfo(BaseModel):
    symbol: str
    name: str


class TickersResponse(BaseModel):
    tickers: list[TickerInfo]
    default: str


class HealthResponse(BaseModel):
    status: str
    active_ticker: str
    used_fallback: bool
    fallback_reason: str | None
    last_refresh: str | None
    hourly_rows: int
    daily_rows: int
    ready: bool


class ScoreComponentSchema(BaseModel):
    name: str
    raw_value: float
    normalized: float
    weight: float
    contribution: float
    description: str


class HeatScoreResponse(BaseModel):
    score: float
    label: str
    components: list[ScoreComponentSchema]


class RegimeResponse(BaseModel):
    regime: str
    risk_flags: list[str]
    confidence: float
    details: dict[str, str]


class ActionPlanResponse(BaseModel):
    action: str
    base_amount: float
    multiplier: float
    suggested_amount: float
    currency: str
    reasoning: list[str]


class ReportResponse(BaseModel):
    markdown: str


class OHLCVPoint(BaseModel):
    time: str
    open: float
    high: float
    low: float
    close: float
    volume: float


class IndicatorPoint(BaseModel):
    time: str
    value: float | None


class IndicatorsResponse(BaseModel):
    ticker: str
    timeframe: str
    ohlcv: list[OHLCVPoint]
    sma20: list[IndicatorPoint]
    sma50: list[IndicatorPoint]
    sma200: list[IndicatorPoint]
    ema20: list[IndicatorPoint]
    ema50: list[IndicatorPoint]
    rsi: list[IndicatorPoint]
    macd: list[IndicatorPoint]
    macd_signal: list[IndicatorPoint]
    macd_histogram: list[IndicatorPoint]
    bb_upper: list[IndicatorPoint]
    bb_middle: list[IndicatorPoint]
    bb_lower: list[IndicatorPoint]
    volatility: list[IndicatorPoint]
    drawdown: list[IndicatorPoint]
