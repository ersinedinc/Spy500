from enum import Enum


class MarketRegime(str, Enum):
    TREND_UP = "Trend Up"
    TREND_DOWN = "Trend Down"
    RANGE = "Range"


class RiskFlag(str, Enum):
    OVERBOUGHT = "Overbought"
    OVERSOLD = "Oversold"
    HIGH_VOLATILITY = "High Volatility"
    EXTREME_DRAWDOWN = "Extreme Drawdown"
    DEATH_CROSS = "Death Cross"
    GOLDEN_CROSS = "Golden Cross"
