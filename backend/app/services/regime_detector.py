import logging
from dataclasses import dataclass, field

from app.config import get_config
from app.models.enums import MarketRegime, RiskFlag

logger = logging.getLogger(__name__)


@dataclass
class RegimeResult:
    regime: MarketRegime
    risk_flags: list[RiskFlag]
    confidence: float
    details: dict[str, str] = field(default_factory=dict)


def detect_regime(latest: dict, prev_row: dict | None = None) -> RegimeResult:
    cfg = get_config()["regime"]
    risk_flags: list[RiskFlag] = []
    details: dict[str, str] = {}

    close = latest.get("Close", 0)
    sma50 = latest.get("SMA_50")
    sma200 = latest.get("SMA_200")
    rsi = latest.get("RSI_14")
    volatility = latest.get("volatility")
    drawdown = latest.get("drawdown")

    # --- Trend detection ---
    regime = MarketRegime.RANGE
    confidence = 0.5

    if sma50 is not None and sma200 is not None and close > 0:
        if close > sma50 > sma200:
            regime = MarketRegime.TREND_UP
            confidence = 0.8
            details["trend"] = (
                f"Bullish alignment: Price ({close:.2f}) > "
                f"SMA50 ({sma50:.2f}) > SMA200 ({sma200:.2f})"
            )
        elif close < sma50 < sma200:
            regime = MarketRegime.TREND_DOWN
            confidence = 0.8
            details["trend"] = (
                f"Bearish alignment: Price ({close:.2f}) < "
                f"SMA50 ({sma50:.2f}) < SMA200 ({sma200:.2f})"
            )
        else:
            details["trend"] = (
                f"Mixed signals: Price={close:.2f}, "
                f"SMA50={sma50:.2f}, SMA200={sma200:.2f}"
            )
    else:
        details["trend"] = "Insufficient data for trend detection"
        confidence = 0.3

    # --- Risk flags ---
    if rsi is not None:
        if rsi > cfg["overbought_rsi"]:
            risk_flags.append(RiskFlag.OVERBOUGHT)
            details["rsi"] = f"RSI={rsi:.1f} > {cfg['overbought_rsi']} (overbought)"
        elif rsi < cfg["oversold_rsi"]:
            risk_flags.append(RiskFlag.OVERSOLD)
            details["rsi"] = f"RSI={rsi:.1f} < {cfg['oversold_rsi']} (oversold)"
        else:
            details["rsi"] = f"RSI={rsi:.1f} (neutral)"

    if volatility is not None:
        if volatility > cfg["high_volatility_threshold"]:
            risk_flags.append(RiskFlag.HIGH_VOLATILITY)
            details["volatility"] = (
                f"Annualized volatility={volatility:.1%} > "
                f"{cfg['high_volatility_threshold']:.0%}"
            )
        else:
            details["volatility"] = f"Annualized volatility={volatility:.1%}"

    if drawdown is not None:
        if drawdown < cfg["extreme_drawdown_threshold"]:
            risk_flags.append(RiskFlag.EXTREME_DRAWDOWN)
            details["drawdown"] = (
                f"Drawdown={drawdown:.1%} < "
                f"{cfg['extreme_drawdown_threshold']:.0%}"
            )
        else:
            details["drawdown"] = f"Drawdown={drawdown:.1%}"

    # SMA crossover detection (compare with previous row)
    if prev_row is not None and sma50 is not None and sma200 is not None:
        prev_sma50 = prev_row.get("SMA_50")
        prev_sma200 = prev_row.get("SMA_200")
        if prev_sma50 is not None and prev_sma200 is not None:
            if prev_sma50 < prev_sma200 and sma50 >= sma200:
                risk_flags.append(RiskFlag.GOLDEN_CROSS)
                details["crossover"] = "Golden Cross: SMA50 crossed above SMA200"
            elif prev_sma50 > prev_sma200 and sma50 <= sma200:
                risk_flags.append(RiskFlag.DEATH_CROSS)
                details["crossover"] = "Death Cross: SMA50 crossed below SMA200"

    logger.info(
        f"Regime: {regime.value}, flags={[f.value for f in risk_flags]}, "
        f"confidence={confidence:.2f}"
    )

    return RegimeResult(
        regime=regime,
        risk_flags=risk_flags,
        confidence=confidence,
        details=details,
    )
